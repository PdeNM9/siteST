import streamlit as st
from annotated_text import annotated_text

# Configuração da página deve ser a primeira coisa a ser chamada
st.set_page_config(page_title="Assessor 2.0!", page_icon="📣", layout="centered")

import funcoes
import variaveis

funcoes.sidebar()

def create_annotated_text(text, annotations):
    result = []
    i = 0
    while i < len(text):
        match = False
        for key, value in annotations.items():
            if text[i:i+len(value)] == value:
                result.append((value, key))
                i += len(value)
                match = True
                break
        if not match:
            result.append(text[i])
            i += 1
    return result

st.title('Consulta de Minutas.')

# Input para buscar pelo nome da minuta
name_input = st.text_input("Digite uma palavra para pesquisar:", key="input_search")

if name_input:
    resultados = funcoes.buscar_minutas_por_nome(funcoes.conexao, name_input)
    if resultados is not None and not resultados.empty:
        # Ajuste para extrair nomes das minutas de um DataFrame
        nomes_minutas = [row.Nome_da_Minuta for row in resultados.itertuples()]
        escolha = st.selectbox("Escolha uma minuta:", nomes_minutas, key="select_minuta")

        # Ajuste para extrair o conteúdo da minuta selecionada
        conteudo_da_minuta = next(
            row.Conteudo_da_Minuta for row in resultados.itertuples() if row.Nome_da_Minuta == escolha)

        # Identificar variáveis no conteúdo da minuta com base no dicionário de variáveis
        variaveis_encontradas = {descricao: variaveis.data[descricao]
                                 for descricao in variaveis.data if variaveis.data[descricao] in conteudo_da_minuta}
        valores_variaveis = {}
        for idx, (descricao, identificador) in enumerate(variaveis_encontradas.items()):
            valores_variaveis[identificador] = st.sidebar.text_input(f"{descricao}:", key=f"{identificador}_{idx}")

        # Substituir as variáveis no conteúdo da minuta pelos valores inseridos
        conteudo_modificado = conteudo_da_minuta
        for identificador, valor in valores_variaveis.items():
            conteudo_modificado = conteudo_modificado.replace(identificador, valor)

        # Criando colunas para exibir os textos lado a lado
        col1, col2 = st.columns(2)

        with col1:
            st.write("### Conteúdo Original da Minuta:")
            anotacoes = create_annotated_text(conteudo_da_minuta, variaveis.data)
            annotated_text(*anotacoes)
            if st.button("Copiar Conteúdo Original", key="copy_original_button"):
                st.session_state.clipboard = conteudo_da_minuta
                st.success("Conteúdo Original copiado!")

        with col2:
            st.write("### Conteúdo Modificado:")
            st.write(conteudo_modificado)
            if st.button("Copiar Conteúdo Modificado", key="copy_modificado_button"):
                st.session_state.clipboard = conteudo_modificado
                st.success("Conteúdo Modificado copiado!")

    else:
        st.warning("Nenhum registro encontrado para o termo pesquisado.")
