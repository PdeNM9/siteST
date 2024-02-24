import streamlit as st
import funcoes

st.markdown('# Alterar Minuta.')

# Configurar conexão ao banco de dados
conection = st.connection('mysql', type='sql')

# Input para buscar pelo nome da minuta
name_input = st.text_input("Digite uma palavra para pesquisar:")

if name_input:
    resultados = funcoes.buscar_minutas_por_nome(funcoes.conection, name_input)
    if not resultados.empty:
        # Ajuste para extrair nomes das minutas de um DataFrame
        nomes_minutas = [row.Nome_da_Minuta for row in resultados.itertuples()]
        escolha = st.selectbox("Escolha uma minuta:", nomes_minutas)

        # Ajuste para extrair o conteúdo da minuta selecionada
        conteudo_da_minuta = next(
            row.Conteudo_da_Minuta for row in resultados.itertuples() if row.Nome_da_Minuta == escolha)
        campos = next(
            row.Campos for row in resultados.itertuples() if row.Nome_da_Minuta == escolha)
        fase = next(
            row.Fase for row in resultados.itertuples() if row.Nome_da_Minuta == escolha)
        ramo = next(
            row.Ramo for row in resultados.itertuples() if row.Nome_da_Minuta == escolha)
        tipo = next(
            row.Tipo for row in resultados.itertuples() if row.Nome_da_Minuta == escolha)
        variaveis = next(
            row.Variáveis for row in resultados.itertuples() if row.Nome_da_Minuta == escolha)
        st.write("**Conteúdo da Minuta:**")
        st.text_area("conteudo_da_minuta", value=conteudo_da_minuta, height=600)
        st.write("**Campos:**")
        st.text_input("Campos", value=campos)
        st.write("**Fase:**")
        st.text_input("Fase", value=fase)
        st.write("**Ramo:**")
        st.text_input("Ramo", value=ramo)
        st.write("**Tipo:**")
        st.text_input("Tipo", value=tipo)
        st.write("**Variáveis:**")
        st.text_input("Variáveis", value=variaveis)

        if st.button('Atualizar Minuta'):
            # Chama a função para atualizar a minuta
            sucesso = funcoes.atualizar_minuta(conection, escolha, campos, fase, ramo, tipo, variaveis, conteudo_da_minuta)
            if sucesso:
                st.success("Minuta atualizada com sucesso! -alterar")
            else:
                st.error("Erro ao atualizar a minuta - alterar.")

    else:
        st.write("Nenhum registro encontrado.")
