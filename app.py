import pyperclip
import streamlit as st
st.set_page_config(page_title="Assessor 2.0!", page_icon="🎈", layout="centered")

import funcoes
import variaveis

st.title('Consulta de Arquivos.')

# Input para buscar pelo nome da minuta
name_input = st.text_input("Digite uma palavra para pesquisar:")

if name_input:
    resultados = funcoes.buscar_minutas_por_nome(funcoes.conexao, name_input)
    if not resultados.empty:
        # Ajuste para extrair nomes das minutas de um DataFrame
        nomes_minutas = [row.Nome_da_Minuta for row in resultados.itertuples()]
        escolha = st.selectbox("Escolha uma minuta:", nomes_minutas)

        # Ajuste para extrair o conteúdo da minuta selecionada
        conteudo_da_minuta = next(
            row.Conteudo_da_Minuta for row in resultados.itertuples() if row.Nome_da_Minuta == escolha)

        # Identificar variáveis no conteúdo da minuta com base no dicionário de variáveis
        variaveis_encontradas = {descricao: variaveis.data[descricao]
                                 for descricao in variaveis.data if variaveis.data[descricao] in conteudo_da_minuta}
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
            # Utilize o st.button para detectar quando o botão é clicado
            if st.button("COPIAR"):
                # Utilize pyperclip para copiar o conteúdo modificado para a área de transferência
                pyperclip.copy(conteudo_modificado)
                # Utilize st.success para mostrar a mensagem de sucesso
                st.success("Copiado com sucesso!")

    else:
        st.write("Nenhum registro encontrado.")
