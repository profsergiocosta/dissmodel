import streamlit as st

from dissmodel.core import Model, Environment
from dissmodel.visualization import Chart, track_plot
from dissmodel.visualization.streamlit import StreamlitChart, display_inputs


############################
# Definição do Modelo SIR
############################

@track_plot("Temperature", "red")
class TempSimulator(Model):

    temperature: int


    def __init__(self, temperature=45):
        super().__init__()

        # Inicialização dos parâmetros do modelo SIR
        self.temperature = temperature

    def execute(self):
       print (self.env.now(), self.temperature)
       self.temperature -= 1

############################
# Interface do Usuário com Streamlit
############################

# Configurações iniciais da página
st.set_page_config(page_title="Entendendo a geração de graficos", layout="centered")
st.title("Very Simple 'Model' (DisSModel)")

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
model = TempSimulator()

# Exibe os campos para entrada de dados do modelo
display_inputs(model, st.sidebar)


############################
# Visualização do resultado
############################


# Inicializa o componente de gráfico com uma area reservada para o gráfico
StreamlitChart(plot_area=st.empty())

# Executa a simulação ao clicar no botão
if executar:
    env.reset() # apagar as informacoe no plot, pensar depois se essa é a melhor abordagem
    env.run()
