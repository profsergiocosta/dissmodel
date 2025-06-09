
import streamlit as st
from matplotlib.colors import ListedColormap
from dissmodel.geo import regular_grid
from dissmodel.core import Environment
from dissmodel.visualization.map import Map

from dissmodel.visualization import display_inputs

from dissmodel.geo import regular_grid, fill, FillStrategy


from dissmodel.models.ca import FireModel  # ou FireModelProb, conforme sua variação


# ---------------------------
# Configuração da interface
# ---------------------------

st.set_page_config(page_title="Fire Model", layout="centered")
st.title("Modelo de Propagação de Fogo (DisSModel)")

# Parâmetros ajustáveis pelo usuário
st.sidebar.title("Parâmetros do Modelo")
steps = st.sidebar.slider("Número de passos da simulação", min_value=1, max_value=50, value=10)
grid_dim = st.sidebar.slider("Tamanho da grade", min_value=5, max_value=100, value=20)
executar = st.button("Executar Simulação")

# ---------------------------
# Geração da grade espacial
# ---------------------------

gdf = regular_grid(
    dimension=(grid_dim, grid_dim),
    resolution=1,
    attrs={'state': 0}
)
gdf.loc["10-10","state"] = FireModel.BURNING

fill(
    strategy=FillStrategy.RANDOM_SAMPLE,
    gdf=gdf,
    attr="state",
    data={FireModel.FOREST: 0.95, FireModel.BURNING: 0.05},  # 70% de células com 0, 30% com 1
    seed=42
)


# ---------------------------
# Criação do ambiente e modelo
# ---------------------------

env = Environment(start_time=0, end_time=steps)
fire = FireModel(gdf=gdf)  # ou FireModelProb se estiver usando versão probabilística

# Exibir parâmetros ajustáveis do modelo (se houver)
display_inputs(fire, st.sidebar)

# ---------------------------
# Visualização inicial
# ---------------------------

plot_area = st.empty()

# Mapa de cores para os estados
custom_cmap = ListedColormap(['green', 'red', 'brown'])  # Floresta, queimando, queimado
plot_params = {"column": "state", "cmap": custom_cmap, "ec": "black"}

Map(
    gdf=gdf,
    plot_area=plot_area,
    plot_params=plot_params
)

# ---------------------------
# Execução da simulação
# ---------------------------

if executar:
    env.run()
