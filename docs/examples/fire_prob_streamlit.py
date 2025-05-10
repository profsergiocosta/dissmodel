
from dissmodel.core import Model, Environment

from dissmodel.core.spatial import regular_grid, fill

from dissmodel.visualization import Map

from dissmodel.visualization.streamlit import StreamlitMap, display_inputs


from matplotlib.colors import ListedColormap

import streamlit as st

import random


# Fire in the forest
# https://github.com/cesaraustralia/DynamicGrids.jl




FOREST = 0
BURNING = 1
BURNED = 2


class FireModelProb(Model):

    prob_regrowth: float
    prob_combustion: float

    def __init__(self, prob_combustion=0.001,  prob_regrowth=0.1, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        self.prob_combustion = prob_combustion
        self.prob_regrowth = prob_regrowth

    def rule(self, idx):
        state = self.env.gdf.loc[idx].state
        
        if state == FOREST:
            neighs = self.neighs(idx)

            if (neighs.state == BURNING).any():
                return BURNING
            else:
                return BURNING if random.random() <= self.prob_combustion else FOREST

        elif state == BURNING:
            return BURNED
           
        else:
             return FOREST if random.random() <= self.prob_regrowth else BURNED
        

    def execute (self):
        self.env.gdf["state"] = self.env.gdf.index.map(self.rule)


## a configuracao começaria aqui

# Configurações da aplicação
st.set_page_config(page_title="Fire Model", layout="centered")
st.title("Fire Model (DisSModel)")


# Parâmetros do usuário
st.sidebar.title("Parametros do Modelo")

steps = st.sidebar.slider("Número de passos da simulação", min_value=1, max_value=50, value=10)
grid_dim = st.sidebar.slider("Tamanho da grade", min_value=5, max_value=50, value=20)

custom_cmap = ListedColormap(['green', 'red', 'brown'])
plot_params={ "column": "state","cmap": custom_cmap,  "ec" : 'black'}


# Inicializar estado da sessão
if st.button("Executar Simulação"):

    # Área de plotagem reservada
    plot_area = st.empty()

    gdf = regular_grid (bounds=(0, 0, 100, 100), dim=grid_dim, attrs={'state': 0})
    gdf.loc["10-10","state"] = BURNING

    env = Environment (
        gdf = gdf,
        end_time = steps,
        start_time=0
    )

    # simulação  
    FireModelProb(create_neighbohood="Rook")

    # visualizacao
    StreamlitMap(  
        plot_area = plot_area,
        plot_params={ "column": "state","cmap": custom_cmap,  "ec" : 'black'}
    )

    env.run()