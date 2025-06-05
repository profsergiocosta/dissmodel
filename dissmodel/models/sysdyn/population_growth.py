
from dissmodel.core import Model
from dissmodel.visualization import track_plot

############################
# Definição do Modelo PopulationGrowth
############################

@track_plot("Population", "green")
class PopulationGrowth(Model):
    population: float
    growth: float
    growthChange: float

    def __init__(self, population=60, growth=0.5, growthChange=1):
        super().__init__()
        self.population = population
        self.growth = growth
        self.growthChange = growthChange

 
    def execute(self):
        """Executa um passo de simulação."""
        self.population *= (1 + self.growth)
        self.growth *= self.growthChange

