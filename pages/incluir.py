import streamlit as st
st.set_page_config(page_title="Assessor 2.0!", page_icon="📣", layout="centered")
import funcoes

st.markdown('# Incluir Minuta.')

# Campos de entrada para os dados da minuta
nome_da_minuta = st.text_input("Nome da Minuta")
campos = st.text_input("Campos")
conteudo_da_minuta = st.text_area("Conteúdo da Minuta")
fase = st.text_input("Fase")
ramo = st.text_input("Ramo")
tipo = st.text_input("Tipo")
variaveis = st.text_input("Variáveis")

# Botão para adicionar a minuta
if st.button('Adicionar Minuta'):
    if nome_da_minuta.strip():
        sucesso = funcoes.adicionar_minuta(nome_da_minuta, campos, conteudo_da_minuta, fase, ramo, tipo, variaveis)
        if sucesso:
            st.success("Minuta adicionada com sucesso!")
        else:
            st.error("Erro ao adicionar a minuta.")
    else:
        st.warning("O nome da minuta é obrigatório.")
