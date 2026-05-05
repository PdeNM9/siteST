"""
Script para converter o dump MySQL (minutas.sql) em banco SQLite (minutas.db).
Execute uma única vez: python convert_db.py
"""
import sqlite3
import re
import os

# Caminhos
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_FILE = os.path.join(SCRIPT_DIR, "minutas.sql")
DB_FILE = os.path.join(SCRIPT_DIR, "minutas.db")

def parse_sql_dump(sql_file):
    """Lê o dump MySQL e extrai os registros INSERT INTO."""
    with open(sql_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Criar tabela SQLite (adaptada do MySQL)
    create_table = """
    CREATE TABLE IF NOT EXISTS minutas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Campos TEXT,
        Conteudo_da_Minuta TEXT,
        Fase TEXT,
        Nome_da_Minuta TEXT,
        Ramo TEXT,
        Tipo TEXT,
        Variáveis TEXT
    )
    """

    # Extrair todos os blocos de VALUES do dump
    # O dump MySQL tem formato: INSERT INTO `minutas` (...) VALUES (...), (...), ...;
    # Precisamos extrair cada tupla de valores

    records = []

    # Encontrar todos os blocos INSERT INTO ... VALUES
    insert_pattern = re.compile(
        r"INSERT INTO `minutas`.*?VALUES\s*(.*?);",
        re.DOTALL
    )

    for match in insert_pattern.finditer(content):
        values_block = match.group(1)

        # Fazer parsing manual das tuplas respeitando strings com aspas
        # Cada registro é: ('campo1', 'campo2', ..., 'campo7')
        i = 0
        while i < len(values_block):
            # Encontrar início da tupla
            if values_block[i] == '(':
                i += 1
                fields = []
                current_field = []
                in_string = False
                escape_next = False

                while i < len(values_block):
                    char = values_block[i]

                    if escape_next:
                        # Tratar sequências de escape MySQL
                        if char == 'n':
                            current_field.append('\n')
                        elif char == 'r':
                            current_field.append('\r')
                        elif char == 't':
                            current_field.append('\t')
                        elif char == '\\':
                            current_field.append('\\')
                        elif char == "'":
                            current_field.append("'")
                        elif char == '"':
                            current_field.append('"')
                        else:
                            current_field.append(char)
                        escape_next = False
                        i += 1
                        continue

                    if char == '\\' and in_string:
                        escape_next = True
                        i += 1
                        continue

                    if char == "'" and not escape_next:
                        if in_string:
                            # Verificar se é escape de aspas simples ('')
                            if i + 1 < len(values_block) and values_block[i + 1] == "'":
                                current_field.append("'")
                                i += 2
                                continue
                            else:
                                in_string = False
                                i += 1
                                continue
                        else:
                            in_string = True
                            i += 1
                            continue

                    if not in_string:
                        if char == ',':
                            fields.append(''.join(current_field))
                            current_field = []
                            i += 1
                            # Pular espaços após vírgula
                            while i < len(values_block) and values_block[i] == ' ':
                                i += 1
                            continue
                        elif char == ')':
                            fields.append(''.join(current_field))
                            if len(fields) == 7:
                                records.append(tuple(fields))
                            i += 1
                            break
                        else:
                            i += 1
                            continue
                    else:
                        current_field.append(char)
                        i += 1
            else:
                i += 1

    return create_table, records


def main():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Banco existente removido: {DB_FILE}")

    print(f"Lendo dump MySQL: {SQL_FILE}")
    create_table, records = parse_sql_dump(SQL_FILE)
    print(f"Encontrados {len(records)} registros.")

    # Criar banco SQLite
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(create_table)

    # Inserir registros
    insert_sql = """
    INSERT INTO minutas (Campos, Conteudo_da_Minuta, Fase, Nome_da_Minuta, Ramo, Tipo, Variáveis)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    cursor.executemany(insert_sql, records)
    conn.commit()

    # Verificar
    cursor.execute("SELECT COUNT(*) FROM minutas")
    count = cursor.fetchone()[0]
    print(f"Banco SQLite criado com sucesso: {DB_FILE}")
    print(f"Total de registros inseridos: {count}")

    # Mostrar alguns nomes de minutas como amostra
    cursor.execute("SELECT Nome_da_Minuta FROM minutas LIMIT 5")
    print("\nAmostra de minutas:")
    for row in cursor.fetchall():
        print(f"  - {row[0][:80]}...")

    conn.close()


if __name__ == "__main__":
    main()
