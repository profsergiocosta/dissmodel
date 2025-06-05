
from dissmodel.core import Model, Environment


from dissmodel.core.spatial import regular_grid, fill


from dissmodel.visualization import Map




from matplotlib.colors import ListedColormap

import streamlit as st


from dissmodel.models.ca import FireModel

## a configuracao começaria aqui

# Configurações da aplicação
st.set_page_config(page_title="Fire Model", layout="centered")
st.title("Fire Model (DisSModel)")

# Parâmetros do usuário
steps = st.slider("Número de passos da simulação", min_value=1, max_value=50, value=10)
grid_dim = st.slider("Tamanho da grade", min_value=5, max_value=50, value=20)



gdf = regular_grid (bounds=(0, 0, 100, 100), dim=grid_dim, attrs={'state': 0})
gdf.loc["10-10","state"] = FireModel.BURNING

env = Environment (
        gdf = gdf,
        end_time = steps,
        start_time=0
)

# simulação  
FireModel( gdf = gdf)


# Inicializar estado da sessão
if st.button("Executar Simulação"):

    # Área de plotagem reservada
    plot_area = st.empty()
  
    # visualizacao
    custom_cmap = ListedColormap(['green', 'red', 'brown'])
    plot_params={ "column": "state","cmap": custom_cmap,  "ec" : 'black'}

    Map(  
        gdf = gdf,
        plot_area = plot_area,
        plot_params={ "column": "state","cmap": custom_cmap,  "ec" : 'black'}
    )

    env.run()