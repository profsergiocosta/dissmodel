import streamlit as st

from dissmodel.core import Model, Environment
from dissmodel.visualization import Chart, track_plot
from dissmodel.visualization.streamlit import StreamlitChart, display_inputs


############################
# Definição do Modelo SIR
############################

@track_plot("Susceptible", "green")
@track_plot("Infected", "red")
@track_plot("Recovered", "blue")
class SIR(Model):
    # Estes atributos serão usados para criar a interface de entrada com Streamlit
    susceptible: int
    infected: int
    recovered: int
    duration: int

    def __init__(self, susceptible=9998, infected=2, recovered=0, duration=2,
                 contacts=6, probability=0.25, final_time=30):
        super().__init__()

        # Inicialização dos parâmetros do modelo SIR
        self.susceptible = susceptible
        self.infected = infected
        self.recovered = recovered
        self.duration = duration
        self.contacts = contacts
        self.probability = probability
        self.final_time = final_time

    def update(self):
        # Cálculos do modelo SIR
        total = self.susceptible + self.infected + self.recovered
        alpha = self.contacts * self.probability

        # Cálculo de novas infecções e recuperações
        prop = self.susceptible / total
        new_infected = self.infected * alpha * prop
        new_recovered = self.infected / self.duration

        # Atualização dos grupos populacionais
        self.susceptible -= new_infected
        self.infected += new_infected - new_recovered
        self.recovered += new_recovered

    def execute(self):
        # Executa a atualização do modelo a cada passo de tempo
        self.update()


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
StreamlitChart(plot_area=st.empty())

# Executa a simulação ao clicar no botão
if executar:
    env.run()
