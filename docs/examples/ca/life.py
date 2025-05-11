
from dissmodel.core import Model, Environment

from dissmodel.visualization.map import Map

from dissmodel.core.spatial import regular_grid, fill


from matplotlib.colors import ListedColormap

from dissmodel.models.ca import GameOfLife

### espaço 
gdf = regular_grid (bounds=(0, 0, 100, 100), dim=20, attrs={'state': 0})


fill(
        strategy="pattern",
        gdf=gdf,
        attr="state",
        pattern=GameOfLife.patterns["glider"],
        start_x=5,
        start_y=5
)


### instanciação de um modelo
### ambiente que integra o espaço e os modelos
env = Environment (
    gdf = gdf,
    end_time = 10,
    start_time=0
)

## instanciacao do modelo
gol = GameOfLife(create_neighbohood="Queen")

## visualização
custom_cmap = ListedColormap(['green', 'red'])
plot_params={ "column": "state","cmap": custom_cmap,  "ec" : 'black'}
Map( 
    plot_params={ "column": "state","cmap": custom_cmap,  "ec" : 'black'}
)

## execução
env.run()