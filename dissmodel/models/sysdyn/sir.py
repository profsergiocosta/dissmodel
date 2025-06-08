from dissmodel.core import Model
from dissmodel.visualization import track_plot


############################
# Definição do Modelo SIR
############################

@track_plot("Susceptible", "green")
@track_plot("Infected", "red")
@track_plot("Recovered", "blue")
class SIR(Model):
    # Estes atributos poder ser usados para criar a interface de entrada com Streamlit
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
