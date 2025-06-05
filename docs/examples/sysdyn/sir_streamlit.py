import streamlit as st

from dissmodel.core import Environment
from dissmodel.visualization import Chart
from dissmodel.visualization.streamlit import  display_inputs

from models import SIR


############################
# Interface do Usuário com Streamlit
############################

# Configurações iniciais da página
st.set_page_config(page_title="SIR Model", layout="centered")
st.title("SIR Model (DisSModel)")

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

# Instancia o modelo com valores padrão
sir = SIR(susceptible=9998, infected=2, recovered=0, duration=2, contacts=6,
          probability=0.25, final_time=30)

# Exibe os campos para entrada de dados do modelo
display_inputs(sir, st.sidebar)

############################
# Visualização do resultado
############################


# Inicializa o componente de gráfico com uma area reservada para o gráfico
Chart(plot_area=st.empty())

# Executa a simulação ao clicar no botão
if executar:
    env.reset()
    env.run()
