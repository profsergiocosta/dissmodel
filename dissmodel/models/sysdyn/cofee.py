from dissmodel.core import Model
from dissmodel.visualization import track_plot

@track_plot("Temperature", "blue")
class Coffee(Model):
    temperature: float
    roomTemperature: float
    
    def __init__(self, temperature=80, roomTemperature=20, finalTime=20):
        super().__init__()
        self.temperature = temperature
        self.roomTemperature = roomTemperature
    
    def execute(self):
        """Executa um passo de simulação."""
        difference = self.temperature - self.roomTemperature
        self.temperature -= difference * 0.1
