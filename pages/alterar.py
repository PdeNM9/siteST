# alterar.py
import streamlit as st
st.set_page_config(page_title="Assessor 2.0!", page_icon="📣", layout="centered")
import funcoes

st.markdown('# Alterar Minuta.')

# Configurar conexão ao banco de dados
conexao = st.connection('mysql', type='sql')

# Input para buscar pelo nome da minuta
name_input = st.text_input("Digite uma palavra para pesquisar:")

if name_input:
    resultados = funcoes.buscar_minutas_por_nome(conexao, name_input)
    if not resultados.empty:
        # Ajuste para extrair nomes das minutas de um DataFrame
        nomes_minutas = [row.Nome_da_Minuta for row in resultados.itertuples()]
        escolha = st.selectbox("Escolha uma minuta:", nomes_minutas)

        # Ajuste para extrair o conteúdo da minuta selecionada
        campos = next(
            row.Campos for row in resultados.itertuples() if row.Nome_da_Minuta == escolha)
        conteudo_da_minuta = next(
            row.Conteudo_da_Minuta for row in resultados.itertuples() if row.Nome_da_Minuta == escolha)
        fase = next(
            row.Fase for row in resultados.itertuples() if row.Nome_da_Minuta == escolha)
        ramo = next(
            row.Ramo for row in resultados.itertuples() if row.Nome_da_Minuta == escolha)
        tipo = next(
            row.Tipo for row in resultados.itertuples() if row.Nome_da_Minuta == escolha)
        variaveis = next(
            row.Variáveis for row in resultados.itertuples() if row.Nome_da_Minuta == escolha)

        campos = st.text_input("**Campos:**", value=campos)
        conteudo_da_minuta = st.text_area("**Conteúdo da Minuta:**", value=conteudo_da_minuta, height=600)
        fase = st.text_input("**Fase:**", value=fase)
        ramo = st.text_input("**Ramo:**", value=ramo)
        tipo = st.text_input("**Tipo:**", value=tipo)
        variaveis = st.text_input("**Variáveis:**", value=variaveis)

        nome_da_minuta = escolha

        if st.button('Atualizar Minuta'):
            # Chama a função para atualizar a minuta
            sucesso = funcoes.atualizar_minuta(conexao, nome_da_minuta, campos, conteudo_da_minuta, fase, ramo, tipo, variaveis)

            if sucesso:
                st.success("Minuta atualizada com sucesso! - alterar")
            else:
                st.error("Erro ao atualizar a minuta - alterar.")

    else:
        st.write("Nenhum registro encontrado.")
