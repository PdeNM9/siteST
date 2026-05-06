import streamlit as st
import funcoes

st.set_page_config(page_title="Assessor 2.0! - Consultar", page_icon="📣", layout="wide")

funcoes.sidebar()

st.markdown('# Consultar Minutas.')
st.write("Abaixo estão todas as minutas cadastradas no banco de dados.")

# Adiciona um botão para atualizar os dados
if st.button("Atualizar Lista"):
    st.rerun()

# Busca todas as minutas no banco de dados
resultados = funcoes.listar_todas_minutas()

if resultados is not None and not resultados.empty:
    st.success(f"Total de minutas encontradas: {len(resultados)}")
    
    # Exibe as minutas em uma lista de expanders
    for index, row in resultados.iterrows():
        with st.expander(f"📄 {row['Nome_da_Minuta']}"):
            st.write("**Conteúdo:**")
            st.text_area("Conteúdo da Minuta", value=row['Conteudo_da_Minuta'], height=300, key=f"minuta_{index}")
            
            # Botão para apagar a minuta
            if st.button(f"🗑️ Apagar '{row['Nome_da_Minuta']}'", key=f"delete_{index}"):
                if funcoes.deletar_minuta(row['Nome_da_Minuta']):
                    st.success("Minuta apagada com sucesso!")
                    st.rerun()
            
            st.info("Você pode copiar o conteúdo acima diretamente.")
else:
    st.warning("Nenhuma minuta encontrada no banco de dados.")
