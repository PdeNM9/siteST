import streamlit as st
import sqlite3
import pandas as pd
import os

# Caminho do banco de dados SQLite (mesmo diretório do script)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minutas.db")


def get_connection():
    """Retorna uma conexão com o banco SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def buscar_minutas_por_nome(name_input):
    """Busca minutas cujo nome contenha o termo informado."""
    conn = get_connection()
    query = "SELECT Nome_da_Minuta, Conteudo_da_Minuta, Campos, Fase, Ramo, Tipo, Variáveis FROM minutas WHERE Nome_da_Minuta LIKE ?"
    df = pd.read_sql_query(query, conn, params=(f"%{name_input}%",))
    conn.close()

    if df is not None and not df.empty:
        return df
    else:
        return None


def listar_todas_minutas():
    """Retorna todas as minutas cadastradas no banco."""
    conn = get_connection()
    query = "SELECT Nome_da_Minuta, Conteudo_da_Minuta, Campos, Fase, Ramo, Tipo, Variáveis FROM minutas"
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df is not None and not df.empty:
        return df
    else:
        return None


def atualizar_minuta(nome_da_minuta, campos, conteudo_da_minuta, fase, ramo, tipo, variaveis):
    """Atualiza uma minuta existente no banco."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE minutas
               SET Campos = ?, Conteudo_da_Minuta = ?, Fase = ?, Ramo = ?, Tipo = ?, Variáveis = ?
               WHERE Nome_da_Minuta = ?""",
            (campos, conteudo_da_minuta, fase, ramo, tipo, variaveis, nome_da_minuta)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar minuta: {e}")
        return False


def adicionar_minuta(nome_da_minuta, campos, conteudo_da_minuta, fase, ramo, tipo, variaveis):
    """Adiciona uma nova minuta ao banco."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO minutas (Nome_da_Minuta, Campos, Conteudo_da_Minuta, Fase, Ramo, Tipo, Variáveis)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (nome_da_minuta, campos, conteudo_da_minuta, fase, ramo, tipo, variaveis)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao adicionar minuta: {e}")
        return False


def deletar_minuta(nome_da_minuta):
    """Apaga uma minuta do banco pelo nome."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM minutas WHERE Nome_da_Minuta = ?", (nome_da_minuta,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao apagar minuta: {e}")
        return False


# Cria sidebar
def sidebar():
    st.sidebar.title('Informações')
    st.sidebar.markdown("Desenvolvido por **PdeNM9**. Contribua para o projeto pela chave PIX: pdenm9@gmail.com")
