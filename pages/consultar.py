import streamlit as st
import requests
import json

st.set_page_config(page_title="Assessor 2.0!", page_icon="📣", layout="centered")

st.markdown('# Consultar Processo.')

# Função para formatar o número do processo
def formatar_numero_processo(numero):
    return numero.replace("-", "").replace(".", "")

# Função para apresentar os dados - certifique-se de que esta função está definida
def apresentar_dados(response_data):
    if 'hits' in response_data and 'hits' in response_data['hits']:
        processo = response_data['hits']['hits'][0]  # Pegar apenas o primeiro processo
        processo_info = processo['_source']
        st.subheader(f"Processo Número: {processo_info['numeroProcesso']}")

        with st.expander("Ver detalhes do processo"):
            st.write(f"Classe: {processo_info['classe']['nome']}")
            st.write(f"Sistema: {processo_info['sistema']['nome']}")
            st.write(f"Tribunal: {processo_info['tribunal']}")
            st.write(f"Data de Ajuizamento: {processo_info['dataAjuizamento']}")
            st.write(f"Última Atualização: {processo_info['dataHoraUltimaAtualizacao']}")

            # Ordenar movimentos processuais pela data (mais recentes primeiro)
            movimentos_ordenados = sorted(processo_info['movimentos'], key=lambda x: x['dataHora'], reverse=True)

            st.write("Movimentos Processuais:")
            for movimento in movimentos_ordenados:
                st.write(f"- {movimento['nome']} ({movimento['dataHora']})")

            st.write("Assuntos:")
            for assunto in processo_info['assuntos']:
                st.write(f"- {assunto['nome']}")
    else:
        st.warning("Nenhum processo encontrado.")
    pass

# Input do usuário para o número do processo
numero_do_processo = st.text_input("Número do Processo")

if numero_do_processo:
    numero_formatado = formatar_numero_processo(numero_do_processo)
    st.write("Número formatado para a API:", numero_formatado)

    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjba/_search"

    payload = json.dumps({
      "query": {
        "match": {
          "numeroProcesso": numero_formatado
        }
      }
    })

    # Substituir <API Key> pela Chave Pública
    headers = {
      'Authorization': 'ApiKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        response_json = response.json()
        apresentar_dados(response_json)
    else:
        st.error(f"Erro ao fazer a solicitação: {response.status_code}")
