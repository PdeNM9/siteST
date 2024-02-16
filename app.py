import streamlit as st
import funcoes
import variaveis
from st_copy_to_clipboard import st_copy_to_clipboard

# Conectar ao banco de dados
connection = funcoes.connect_to_database('host', 'user', 'password', 'database')

st.title('Consulta de Arquivos')

# Input para buscar pelo nome da minuta
name_input = st.text_input("Digite uma palavra para pesquisar:")

if name_input:
    resultados = funcoes.buscar_minutas_por_nome(connection, name_input)
    if resultados:
        nomes_minutas = [nome for nome, _ in resultados]
        escolha = st.selectbox("Escolha uma minuta:", nomes_minutas)
        conteudo_da_minuta = next(conteudo for nome, conteudo in resultados if nome == escolha)

        # Identificar variáveis no conteúdo da minuta com base no dicionário de variáveis
        variaveis_encontradas = {descricao: variaveis.data[descricao] for descricao in variaveis.data if variaveis.data[descricao] in conteudo_da_minuta}
        valores_variaveis = {}
        for descricao, identificador in variaveis_encontradas.items():
            valores_variaveis[identificador] = st.sidebar.text_input(f"{descricao}:", key=identificador)

        # Substituir as variáveis no conteúdo da minuta pelos valores inseridos
        conteudo_modificado = conteudo_da_minuta
        for identificador, valor in valores_variaveis.items():
            conteudo_modificado = conteudo_modificado.replace(identificador, valor)

        st.write("**Conteúdo da Minuta:**")
        st.write(conteudo_modificado)

        # Após o conteúdo modificado ser definido
        if 'conteudo_modificado' in locals():
            # Corrigido para usar apenas um argumento, o conteúdo a ser copiado
            botao_de_copiar = st_copy_to_clipboard(conteudo_modificado)


    else:
        st.write("Nenhum registro encontrado.")
