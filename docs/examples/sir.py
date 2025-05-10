



from dissmodel.core import Environment, Model

from dissmodel.visualization import Chart, track_plot






@track_plot("Susceptible", "green")
@track_plot("Infected", "red")
@track_plot("Recovered", "blue")
class SIR(Model):



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
        self.susceptible -= new_infected
        self.infected += new_infected - new_recovered
        self.recovered += new_recovered


    def execute(self):
        self.update()


# Preparando o ambiente de simulação e o gráfico
#print (10)
env = Environment()

SIR(susceptible=9998, infected=2, recovered=0, duration=2, contacts=6,
          probability=0.25, final_time=30)

Chart()

env.run(30)  