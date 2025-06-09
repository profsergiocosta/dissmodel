# Exemplo de execução do Game of Life com DisSModel + Streamlit

import sys
from pathlib import Path

# Permite importar módulos do diretório pai
sys.path.append(str(Path(__file__).resolve().parent.parent))

import random
from matplotlib.colors import ListedColormap

import streamlit as st

from dissmodel.geo import regular_grid, fill, FillStrategy
from dissmodel.core import Environment
from dissmodel.visualization.map import Map

from dissmodel.models.ca import GameOfLife



# -------------------------------------------------------------
# Configuração da interface com Streamlit
# -------------------------------------------------------------

st.set_page_config(page_title="Modelo Game of Life", layout="centered")
st.title("Simulação com Game of Life (DisSModel)")

# Parâmetros de entrada do usuário
st.sidebar.title("Parâmetros do Modelo")
steps = st.sidebar.slider("Número de passos da simulação", min_value=1, max_value=50, value=10)
grid_dim = st.sidebar.slider("Tamanho da grade", min_value=5, max_value=50, value=20)

# Colormap customizado: 0 = verde (morto), 1 = vermelho (vivo)
custom_cmap = ListedColormap(['green', 'red'])

# Parâmetros do gráfico
plot_params = {
    "column": "state",
    "cmap": custom_cmap,
    "ec": "black"
}

# -------------------------------------------------------------
# Criação da grade e preenchimento com padrões
# -------------------------------------------------------------



# Criação da grade espacial
grid = regular_grid(dimension=(grid_dim, grid_dim), resolution=1, attrs={'state': 0})


# Padrões clássicos do Game of Life
patterns = {
    "glider": [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1]
    ],
    "toad": [
        [0, 1, 1, 1],
        [1, 1, 1, 0]
    ],
    "blinker": [
        [1, 1, 1]
    ]
}

# Inserção aleatória dos padrões
for name, pattern in patterns.items():
    start_x = random.randint(0, grid_dim - len(pattern))
    start_y = random.randint(0, grid_dim - len(pattern[0]))
    
    fill(
        strategy=FillStrategy.PATTERN,
        gdf=grid,
        attr="state",
        pattern=pattern,
        start_x=start_x,
        start_y=start_y
    )

# -------------------------------------------------------------
# Inicialização do ambiente e modelo
# -------------------------------------------------------------

env = Environment(end_time=steps, start_time=0)
model = GameOfLife(gdf=grid)


# -------------------------------------------------------------
# Execução da simulação
# -------------------------------------------------------------

if st.button("Executar Simulação"):
    # Área reservada para o gráfico dinâmico
    plot_area = st.empty()

    # Criação do mapa com suporte à animação
    Map(
        gdf=grid,
        plot_area=plot_area,
        plot_params=plot_params
    )

    env.run()
