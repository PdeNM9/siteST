import streamlit as st
st.set_page_config(page_title="Assessor 2.0!", page_icon="📣", layout="centered")
from sqlalchemy.sql.expression import text

st.markdown('# Incluir Minuta.')

# Configurar conexão ao banco de dados
conexao = st.connection('mysql', type='sql')

# Cria campos de entrada para os dados da minuta
nome_da_minuta = st.text_input("Nome da Minuta")
campos = st.text_input("Campos")
conteudo_da_minuta = st.text_area("Conteúdo da Minuta")
fase = st.text_input("Fase")
ramo = st.text_input("Ramo")
tipo = st.text_input("Tipo")
variaveis = st.text_input("Variáveis")


# Definição da função
def adicionar_minuta(nome_da_minuta, campos, conteudo_da_minuta, fase, ramo, tipo, variaveis):
    try:
        # Concatenar strings para construir o comando SQL
        comando_sql = "INSERT INTO minutas (Nome_da_Minuta, Campos, Conteudo_da_minuta, Fase, Ramo, Tipo, Variáveis) VALUES ('"
        comando_sql += nome_da_minuta + "', '" + campos + "', '" + conteudo_da_minuta + "', '" + fase + "', '" + ramo + "', '" + tipo + "', '" + variaveis + "')"

        # Declarar o comando SQL como string
        comando_sql = text(comando_sql)

        # Utilizando a sessão para executar o comando SQL
        with conexao.session as s:
            s.execute(comando_sql)
            s.commit()
        st.success("Minuta adicionada com sucesso!")
    except Exception as e:
        st.error(f"Erro ao adicionar minuta: {e}")

# Botão para adicionar a minuta
if st.button('Adicionar Minuta'):
    adicionar_minuta(nome_da_minuta, campos, conteudo_da_minuta, fase, ramo, tipo, variaveis)

