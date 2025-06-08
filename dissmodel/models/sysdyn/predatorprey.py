from dissmodel.core import Model
from dissmodel.visualization import track_plot

@track_plot("prey", "green")
@track_plot("predator", "red")
class PredatorPrey(Model):
    predator: float
    prey: float
    preyGrowth: float
    preyDeathPred: float
    predDeath: float
    predGrowthKills: float

    def __init__(
        self,
        predator=40,
        prey=1000,
        preyGrowth=0.08,
        preyDeathPred=0.001,
        predDeath=0.02,
        predGrowthKills=0.00002
    ):
        super().__init__()
        self.predator = predator
        self.prey = prey
        self.preyGrowth = preyGrowth
        self.preyDeathPred = preyDeathPred
        self.predDeath = predDeath
        self.predGrowthKills = predGrowthKills

    def execute(self):
        """Executa um passo da simulação com base na dinâmica predador-presa."""
        self.prey += (
            self.preyGrowth * self.prey
            - self.preyDeathPred * self.prey * self.predator
        )

        self.predator += (
            -self.predDeath * self.predator
            + self.predGrowthKills * self.prey * self.predator
        )
