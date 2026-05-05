# alterar.py
import streamlit as st
st.set_page_config(page_title="Assessor 2.0!", page_icon="📣", layout="centered")
import funcoes

st.markdown('# Alterar Minuta.')

# Input para buscar pelo nome da minuta
name_input = st.text_input("Digite uma palavra para pesquisar:")

if name_input:
    resultados = funcoes.buscar_minutas_por_nome(name_input)
    if resultados is not None and not resultados.empty:
        # Extrair nomes das minutas
        nomes_minutas = resultados['Nome_da_Minuta'].tolist()
        escolha = st.selectbox("Escolha uma minuta:", nomes_minutas)

        # Extrair dados da minuta selecionada
        minuta = resultados.loc[resultados['Nome_da_Minuta'] == escolha].iloc[0]

        campos = st.text_input("**Campos:**", value=minuta['Campos'] or "")
        conteudo_da_minuta = st.text_area("**Conteúdo da Minuta:**", value=minuta['Conteudo_da_Minuta'] or "", height=600)
        fase = st.text_input("**Fase:**", value=minuta['Fase'] or "")
        ramo = st.text_input("**Ramo:**", value=minuta['Ramo'] or "")
        tipo = st.text_input("**Tipo:**", value=minuta['Tipo'] or "")
        variaveis = st.text_input("**Variáveis:**", value=minuta['Variáveis'] or "")

        nome_da_minuta = escolha

        if st.button('Atualizar Minuta'):
            sucesso = funcoes.atualizar_minuta(nome_da_minuta, campos, conteudo_da_minuta, fase, ramo, tipo, variaveis)
            if sucesso:
                st.success("Minuta atualizada com sucesso!")
            else:
                st.error("Erro ao atualizar a minuta.")
    else:
        st.write("Nenhum registro encontrado.")
