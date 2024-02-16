import streamlit as st

# Inicializar conexão.
conection = st.connection('mysql', type='sql')

# Perform query.
banco = conection.query('SELECT Nome_da_Minuta, Conteudo_da_Minuta FROM minutas')


def buscar_minutas_por_nome(conection, name_input):
    # Formatar a string de entrada para evitar problemas de SQL Injection
    name_input_formatted = '%' + name_input + '%'

    # Realizar a consulta ao banco de dados
    query = f"SELECT Nome_da_Minuta, Conteudo_da_Minuta FROM minutas WHERE Nome_da_Minuta LIKE '{name_input_formatted}'"
    resultados = conection.query(query)

    # Verificar se o DataFrame está vazio
    if resultados is not None and not resultados.empty:
        return resultados
    else:
        return None