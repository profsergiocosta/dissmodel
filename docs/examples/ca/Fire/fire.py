
from dissmodel.core import Model, Environment


from dissmodel.geo.regular_grid import regular_grid
from dissmodel.geo.fill import  fill


from dissmodel.visualization import Map




from matplotlib.colors import ListedColormap

import streamlit as st


from dissmodel.core import Model

from dissmodel.geo.neihborhood import Neighborhood

# Fire in the forest
# https://github.com/TerraME/terrame/wiki/Paradigms

from libpysal.weights.contiguity import Rook
from libpysal.weights.contiguity import Queen

class FireModel(Model):

    FOREST = 0
    BURNING = 1
    BURNED = 2

    def setup (self,gdf):
         self.gdf = gdf
         self.neighborhood = Neighborhood(Queen, gdf, use_index=True)

    def rule(self, idx):

        state = self.gdf.loc[idx].state
             
        if state == FireModel.BURNING:
            return FireModel.BURNED
        elif state == FireModel.FOREST:
                neighs = self.neighborhood.neighs(idx)

                if (neighs.state == FireModel.BURNING).any():
                     return FireModel.BURNING
                else:
                     return state         
        else:
             return state
        

    def execute(self):
        # Aplicar a função `rule` a todos os índices e armazenar os novos estados
        self.gdf["state"] = self.gdf.index.map(self.rule)


## a configuracao começaria aqui

# Configurações da aplicação
st.set_page_config(page_title="Fire Model", layout="centered")
st.title("Fire Model (DisSModel)")

# Parâmetros do usuário
steps = st.slider("Número de passos da simulação", min_value=1, max_value=50, value=10)
grid_dim = st.slider("Tamanho da grade", min_value=5, max_value=50, value=20)




grid = regular_grid( dimension=(grid_dim, grid_dim), resolution =1,  attrs={'state': 0})
grid.loc["10-10","state"] = FireModel.BURNING

env = Environment (
        end_time = steps,
        start_time=0
)

# simulação  
FireModel( gdf = grid)


# Inicializar estado da sessão
if st.button("Executar Simulação"):

    # Área de plotagem reservada
    plot_area = st.empty()
  
    # visualizacao
    custom_cmap = ListedColormap(['green', 'red', 'brown'])
    plot_params={ "column": "state","cmap": custom_cmap,  "ec" : 'black'}

    Map(  
        gdf = grid,
        plot_area = plot_area,
        plot_params={ "column": "state","cmap": custom_cmap,  "ec" : 'black'}
    )

    env.run()