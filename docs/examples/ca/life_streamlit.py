
from dissmodel.core import Model, Environment


from dissmodel.core.spatial import regular_grid, fill


from dissmodel.visualization.map import Map

from dissmodel.visualization.streamlit import StreamlitMap


from matplotlib.colors import ListedColormap

import streamlit as st

import random

from dissmodel.models.ca import GameOfLife
from dissmodel.models.ca.life import patterns



## a configuracao começaria aqui

# Configurações da aplicação
st.set_page_config(page_title="Modelo Game of Life", layout="centered")
st.title("Simulação com Game of Life (DisSModel)")

# Parâmetros do usuário
st.sidebar.title("Parametros do Modelo")

steps = st.sidebar.slider("Número de passos da simulação", min_value=1, max_value=50, value=10)
grid_dim = st.sidebar.slider("Tamanho da grade", min_value=5, max_value=50, value=20)

custom_cmap = ListedColormap(['green', 'red'])
plot_params={ "column": "state","cmap": custom_cmap,  "ec" : 'black'}



grid = regular_grid (bounds=(0, 0, 100, 100), dim=grid_dim, attrs={'land_use': 0})

print (grid_dim)
for name, pattern in patterns.items():
    start_x = random.randint(0, 15)
    start_y = random.randint(0, 15)
    
    fill(
        strategy="pattern",
        gdf=grid,
        attr="state",
        pattern=pattern,
        start_x=start_x,
        start_y=start_y
    )

env = Environment (
        gdf = grid,
        end_time = steps,
        start_time=0
)


GameOfLife(create_neighbohood="Queen")



# Inicializar estado da sessão
if st.button("Executar Simulação"):

    # Área de plotagem reservada
    plot_area = st.empty()

    StreamlitMap(  
        plot_area = plot_area,
        plot_params={ "column": "state","cmap": custom_cmap,  "ec" : 'black'}
    )

    env.run()