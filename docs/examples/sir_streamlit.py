import streamlit as st

from dissmodel.core import Model, Environment

from dissmodel.visualization import Plot, Chart

from dissmodel.visualization.streamlit import StreamlitInputMixin, StreamlitChart, display_inputs

class SIR(Model):

    ## esses parametros será criado interface de entrada e dados
    susceptible: int
    infected: int
    recovered: int
    duration: int

    def __init__(self, susceptible=9998, infected=2, recovered=0, duration=2,
                 contacts=6, probability=0.25, final_time=30):
        super().__init__()

        # Inicialização dos parâmetros do modelo SIR, agora com valores passados na instância
        self.susceptible = susceptible
        self.infected = infected
        self.recovered = recovered
        self.duration = duration
        self.contacts = contacts
        self.probability = probability
        self.final_time = final_time


    # Usando o decorador para registrar informações de plotagem
    @Plot("line", "Susceptible", "green")
    def set_susceptible(self, value):
        self.susceptible = value

    @Plot("line", "Infected", "red")
    def set_infected(self, value):
        self.infected = value

    @Plot("line", "Recovered", "blue")
    def set_recovered(self, value):
        self.recovered = value

    def update(self):
        #print ("update")
        # Cálculos do modelo SIR
        total = self.susceptible + self.infected + self.recovered
        alpha = self.contacts * self.probability

        # Probabilidade de infecção
        prop = self.susceptible / total
        new_infected = self.infected * alpha * prop
        new_recovered = self.infected / self.duration

        # Atualizando os números de cada grupo
        self.set_susceptible(self.susceptible - new_infected)
        self.set_infected(self.infected + new_infected - new_recovered)
        self.set_recovered(self.recovered + new_recovered)


    def execute(self):
        self.update()




## a configuracao começaria aqui

# Configurações da aplicação
st.set_page_config(page_title="SIR Model", layout="centered")
st.title("SIR Model (DisSModel)")


st.sidebar.title("Parametros do Modelo")


# Parâmetros do usuário
steps = st.sidebar.slider("Número de passos da simulação", min_value=1, max_value=50, value=10)






env = Environment(
        end_time=steps, start_time=0
)





# simulação    
sir = SIR(susceptible=9998, infected=2, recovered=0, duration=2, contacts=6,
          probability=0.25, final_time=30)








display_inputs(sir, st.sidebar)




# Inicializar estado da sessão
if st.button("Executar Simulação"):
    # Área de plotagem reservada
    plot_area = st.empty()
    

    # visualizacao
    StreamlitChart(plot_area=plot_area)
   
  
    env.run()

    