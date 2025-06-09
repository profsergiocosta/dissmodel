

import random
from matplotlib.colors import ListedColormap

import streamlit as st

from dissmodel.geo import regular_grid, fill, FillStrategy
from dissmodel.core import Environment
from dissmodel.visualization.map import Map

from dissmodel.models.ca import GameOfLife

### espaço 


gdf = regular_grid(dimension=(20, 20), resolution=1, attrs={'state': 0})


### instanciação de um modelo
### ambiente que integra o espaço e os modelos
env = Environment (
    end_time = 10,
    start_time=0
)

## instanciacao do modelo
gol = GameOfLife(gdf=gdf)

'''
fill(
    strategy=FillStrategy.RANDOM_SAMPLE,
    gdf=gdf,
    attr="state",
    data={0: .80, 1: 0.20},  # 70% de células com 0, 30% com 1
    seed=42
)
'''

# usar a inicializacao definida no modelo
gol.initialize()


## visualização
custom_cmap = ListedColormap(['green', 'red'])
plot_params={ "column": "state","cmap": custom_cmap,  "ec" : 'black'}
Map( 
    gdf=gdf,
    plot_params={ "column": "state","cmap": custom_cmap,  "ec" : 'black'}
)

## execução
env.run()