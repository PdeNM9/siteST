import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
from annotated_text import annotated_text

# Configuração da página deve ser a primeira coisa a ser chamada
st.set_page_config(page_title="Assessor 2.0!", page_icon="🎈", layout="centered")

import funcoes
import variaveis

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

st.title('Consulta de Arquivos.')

# Input para buscar pelo nome da minuta
name_input = st.text_input("Digite uma palavra para pesquisar:")

if name_input:
    resultados = funcoes.buscar_minutas_por_nome(funcoes.conexao, name_input)
    if resultados is not None and not resultados.empty:
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

        # Criando colunas para exibir os textos lado a lado
        col1, col2 = st.columns(2)

        with col1:
            st.write("### Conteúdo Original da Minuta:")
            anotacoes = create_annotated_text(conteudo_da_minuta, variaveis.data)
            annotated_text(*anotacoes)

        with col2:
            st.write("### Conteúdo Modificado:")
            st.write(conteudo_modificado)
            # Após o conteúdo modificado ser definido
            if 'conteudo_modificado' in locals():
                # Utilize o st.button para detectar quando o botão é clicado
                st_copy_to_clipboard(conteudo_modificado, "Copiar!", "✅!")
                # Utilize st.success para mostrar a mensagem de sucesso
      

    else:
        st.warning("Nenhum registro encontrado para o termo pesquisado.")
