
from dissmodel.core import Model, Environment, RegularGrid

from dissmodel.visualization.map import Map, StreamlitMap

from dissmodel.models.toys import GameOfLife

from matplotlib.colors import ListedColormap

import streamlit as st

## a configuracao começaria aqui

# Configurações da aplicação
st.set_page_config(page_title="Modelo Game of Life", layout="centered")
st.title("Simulação com Game of Life (LUCCMEpy)")

# Parâmetros do usuário
steps = st.slider("Número de passos da simulação", min_value=1, max_value=50, value=10)
grid_dim = st.slider("Tamanho da grade", min_value=5, max_value=50, value=20)

custom_cmap = ListedColormap(['green', 'red'])
plot_params={ "column": "state","cmap": custom_cmap,  "ec" : 'black'}



# Inicializar estado da sessão
if st.button("Executar Simulação"):

    # Área de plotagem reservada
    plot_area = st.empty()

    grid = RegularGrid(bounds=(0, 0, 100, 100), dim=grid_dim, attrs={'land_use': 0})
    glider_pattern = [
                [0, 1, 0],
                [0, 0, 1],
                [1, 1, 1]
    ]

    grid.fill (attr='state', pattern=glider_pattern, start_x=10, start_y=10)

    env = Environment (
        gdf = grid.to_geodaframe(),
        end_time = steps,
        start_time=0
    )


    GameOfLife(create_neighbohood="Queen")

    StreamlitMap(  
        plot_area = plot_area,
        plot_params={ "column": "state","cmap": custom_cmap,  "ec" : 'black'}
    )

    env.run()