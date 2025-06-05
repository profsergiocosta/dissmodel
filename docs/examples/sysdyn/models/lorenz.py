from dissmodel.core import Model

from dissmodel.visualization import track_plot

@track_plot("X", "blue")
@track_plot("Y", "blue")
@track_plot("Z", "blue")
class Lorenz(Model):
    x: float
    y: float
    z: float
    delta: float
    rho: float
    sigma: float
    beta: float

    def __init__(
        self,
        x=1.0,
        y=1.0,
        z=1.0,
        delta=0.01,
        rho=28.0,
        sigma=10.0,
        beta=8.0/3.0
    ):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.delta = delta
        self.rho = rho
        self.sigma = sigma
        self.beta = beta

    def execute(self):
        """Executa um passo da simulação usando o método de Euler."""
        dx = self.sigma * (self.y - self.x)
        dy = self.x * (self.rho - self.z) - self.y
        dz = self.x * self.y - self.beta * self.z

        self.x += self.delta * dx
        self.y += self.delta * dy
        self.z += self.delta * dz
