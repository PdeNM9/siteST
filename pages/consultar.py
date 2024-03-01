import requests
import json
import streamlit as st

st.markdown('# Consultar Processo.')
# Função para formatar o número do processo
def formatar_numero_processo(numero):
    return numero.replace("-", "").replace(".", "")

# Função para apresentar os dados - certifique-se de que esta função está definida
def apresentar_dados(response_data):
    for processo in response_data['hits']['hits']:
        processo_info = processo['_source']
        st.subheader(f"Processo Número: {processo_info['numeroProcesso']}")

        with st.expander("Ver detalhes do processo"):
            st.write(f"Classe: {processo_info['classe']['nome']}")
            st.write(f"Sistema: {processo_info['sistema']['nome']}")
            st.write(f"Tribunal: {processo_info['tribunal']}")
            st.write(f"Data de Ajuizamento: {processo_info['dataAjuizamento']}")
            st.write(f"Última Atualização: {processo_info['dataHoraUltimaAtualizacao']}")

            # Apresentar movimentos processuais sem usar outro expander
            st.write("Movimentos Processuais:")
            for movimento in processo_info['movimentos']:
                st.write(f"- {movimento['nome']} ({movimento['dataHora']})")

            st.write("Assuntos:")
            for assunto in processo_info['assuntos']:
                st.write(f"- {assunto['nome']}")
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

    #Substituir <API Key> pela Chave Pública
    headers = {
      'Authorization': 'ApiKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        response_json = response.json()
        # Chame a função aqui, dentro do bloco condicional onde response_json é definida
        apresentar_dados(response_json)
    else:
        st.error(f"Erro ao fazer a solicitação: {response.status_code}")
