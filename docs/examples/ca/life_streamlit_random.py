
from dissmodel.core import Model, Environment

from dissmodel.core.spatial import regular_grid, fill

from dissmodel.visualization.map import Map

from dissmodel.visualization.streamlit import StreamlitMap


from matplotlib.colors import ListedColormap

import streamlit as st

from dissmodel.models.ca import GameOfLife

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



gdf = regular_grid (bounds=(0, 0, 100, 100), dim=grid_dim, attrs={'state': 0})
    
n = len(gdf)
    
fill(
        strategy="random_sample",
        gdf=gdf,
        attr="state",
        data={0: 0.7, 1: 0.3},
        seed=42
    )

env = Environment (
        gdf = gdf,
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