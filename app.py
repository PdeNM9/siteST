import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
import re

# Configuração da página deve ser a primeira coisa a ser chamada
st.set_page_config(page_title="Assessor 2.0!", page_icon="📣", layout="centered")

import funcoes
import variaveis

funcoes.sidebar()


st.title('Consulta de Minutas.')

# Input para buscar pelo nome da minuta
name_input = st.text_input("Digite uma palavra para pesquisar:", key="input_search")

if name_input:
    resultados = funcoes.buscar_minutas_por_nome(funcoes.conexao, name_input)
    if resultados is not None and not resultados.empty:
        # Ajuste para extrair nomes das minutas de um DataFrame
        nomes_minutas = resultados['Nome_da_Minuta'].tolist()
        escolha = st.selectbox("Escolha uma minuta:", nomes_minutas, key="select_minuta")

        # Ajuste para extrair o conteúdo da minuta selecionada
        conteudo_da_minuta = resultados.loc[resultados['Nome_da_Minuta'] == escolha, 'Conteudo_da_Minuta'].values[0]

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

        if conteudo_modificado == conteudo_da_minuta:
            st.write("### Conteúdo Original da Minuta:")
            st_copy_to_clipboard(conteudo_da_minuta, "Copiar Conteúdo Original", "✅ Conteúdo Original Copiado!")
        else:
            st.write("### Conteúdo Modificado:")
            st.write(conteudo_modificado)
            st_copy_to_clipboard(conteudo_modificado, "Copiar Conteúdo Modificado", "✅ Conteúdo Modificado Copiado!")
    else:
        st.warning("Nenhum registro encontrado para o termo pesquisado.")
