import mysql.connector
from mysql.connector import Error

def connect_to_database(host, user, password, database):
    connection = None
    try:
        connection = mysql.connector.connect(
        host="db4free.net",
        port=3306,
        user="pdenm9",
        password="4BjsK5Y@77Bm7p_",
        database="assessor2ponto0"
        )
        print("Conexão ao DB bem-sucedida.")

    except Error as e:
        print(f"O erro {e} ocorreu")
    return connection

def buscar_minutas_por_nome(conexao, nome_pesquisa):
    cursor = conexao.cursor()
    query = "SELECT Nome_da_Minuta, Conteudo_da_Minuta FROM minutas WHERE Nome_da_Minuta LIKE %s"
    cursor.execute(query, ('%' + nome_pesquisa + '%',))
    return cursor.fetchall()

