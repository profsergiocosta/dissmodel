import streamlit as st

from dissmodel.core import Environment
from dissmodel.visualization import Chart
from dissmodel.visualization.streamlit import StreamlitChart, display_inputs

from dissmodel.models.sysdyn import PopulationGrowth


############################
# Interface do Usuário com Streamlit
############################

# Configurações iniciais da página
st.set_page_config(page_title="Population Growth Model", layout="centered")
st.title("Population Growth Model (DisSModel)")

# Painel lateral para os parâmetros do modelo
st.sidebar.title("Parâmetros do Modelo")

# Entrada para o número de passos da simulação
steps = st.sidebar.slider("Número de passos da simulação", min_value=1, max_value=50, value=10)

# Botão para executar a simulação
executar = st.button("Executar Simulação")

# Criação do ambiente de simulação
env = Environment(end_time=steps, start_time=0)

############################
# Instanciação do modelo e configuração dos inputs
############################

pop = PopulationGrowth()

# Exibe os campos para entrada de dados do modelo
display_inputs(pop, st.sidebar)

############################
# Visualização do resultado
############################

StreamlitChart(plot_area=st.empty())

if executar:
    env.run()
