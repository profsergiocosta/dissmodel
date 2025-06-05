
from dissmodel.core import Model, Environment

from dissmodel.geo.regular_grid import regular_grid
from dissmodel.geo.fill import  fill

from dissmodel.visualization import Map

from dissmodel.visualization.streamlit import display_inputs


from matplotlib.colors import ListedColormap

import streamlit as st

import random

import random
from dissmodel.core import Model


# Fire in the forest
# https://github.com/cesaraustralia/DynamicGrids.jl

from dissmodel.geo.neihborhood import Neighborhood

from libpysal.weights.contiguity import Rook
from libpysal.weights.contiguity import Queen

class FireModelProb(Model):

    FOREST = 0
    BURNING = 1
    BURNED = 2

    prob_regrowth: float
    prob_combustion: float

    def __init__(self, gdf,prob_combustion=0.001,  prob_regrowth=0.1, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        self.prob_combustion = prob_combustion
        self.prob_regrowth = prob_regrowth
        self.gdf = gdf
        self.neighborhood = Neighborhood(Queen, gdf, use_index=True)


    def rule(self, idx):
        state = self.gdf.loc[idx].state
        
        if state == FireModelProb.FOREST:
            neighs = self.neighborhood.neighs(idx)

            if (neighs.state == FireModelProb.BURNING).any():
                return FireModelProb.BURNING
            else:
                return FireModelProb.BURNING if random.random() <= self.prob_combustion else FireModelProb.FOREST

        elif state == FireModelProb.BURNING:
            return FireModelProb.BURNED
           
        else:
             return FireModelProb.FOREST if random.random() <= self.prob_regrowth else FireModelProb.BURNED
        

    def execute (self):
        self.gdf["state"] = self.gdf.index.map(self.rule)



############################
### Interface do usuário com Streamlit

# Configuração inicial da página
st.set_page_config(page_title="Fire Model", layout="centered")
st.title("Fire Model (DisSModel)")

# Painel lateral com parâmetros ajustáveis pelo usuário
st.sidebar.title("Parâmetros do Modelo")
steps = st.sidebar.slider("Número de passos da simulação", min_value=1, max_value=50, value=10)
grid_dim = st.sidebar.slider("Tamanho da grade", min_value=5, max_value=100, value=20)

# Botão principal para iniciar a simulação
executar = st.button("Executar Simulação")

############################
### Criação do espaço simulado

# Geração de uma grade regular como espaço simulado, sem dados espaciais externos
gdf = regular_grid( dimension=(grid_dim, grid_dim), resolution =1,  attrs={'state': 0})

# Criação do ambiente de simulação, que integra espaço, tempo e agentes
env = Environment(
    
    end_time=steps,
    start_time=0
)

############################
### Instanciação do modelo e exibição de parâmetros

# Criação do modelo de fogo com definição da vizinhança (Rook)
fire = FireModelProb(gdf=gdf)

# Exibição dos parâmetros do modelo na barra lateral
display_inputs(fire, st.sidebar)

############################
### Visualização da simulação

# Área da interface reservada para o mapa interativo
plot_area = st.empty()

# Mapeamento de cores personalizado para os estados das células
custom_cmap = ListedColormap(['green', 'red', 'brown'])
plot_params = {"column": "state", "cmap": custom_cmap, "ec": "black"}

# Componente de visualização do mapa
Map(
    gdf=gdf,
    plot_area=plot_area,
    plot_params=plot_params
)

############################
### Execução da simulação

# Inicia a simulação quando o botão for clicado
if executar:
    env.run()
