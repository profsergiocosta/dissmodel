import pandas as pd
import geopandas as gpd
from dissmodel.core import Model, Environment
from dissmodel.visualization import Map, Chart, track_plot

from matplotlib.colors import ListedColormap, BoundaryNorm


# Modelo Elevacao Simplificado
@track_plot("media_altitude", "blue")
class ElevacaoSimples(Model):

    seaLevelRiseRate: float
    media_altitude: float

    def setup(self, gdf, seaLevelRiseRate=0.01):
        self.gdf = gdf
        self.seaLevelRiseRate = seaLevelRiseRate
        self.media_altitude = 0

    def execute(self):
        print("execute:", self.env.now())
        self.gdf["Alt2"] += self.seaLevelRiseRate
        self.media_altitude = self.gdf["Alt2"].mean()


# Carrega os dados espaciais
file_name = "data/elevacao_pol.zip"
gdf = gpd.read_file(file_name)
gdf.set_index("object_id0", inplace=True)

# Cria o ambiente
env = Environment(start_time=1, end_time=20)

# Instancia o modelo
modelo = ElevacaoSimples(gdf=gdf, seaLevelRiseRate=0.01)

# Visualização do mapa da elevação
Map(gdf=gdf, plot_params={"column": "Alt2", "scheme": "quantiles", "k": 5, "legend": True, "cmap": "Blues"})


# Gráfico da média de altitude
Chart(select={"media_altitude"})

# Executa a simulação
env.run()
