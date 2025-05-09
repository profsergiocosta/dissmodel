
from dissmodel.core import Model, Environment, RegularGrid

from dissmodel.visualization.map import Map

from dissmodel.models.toys import GameOfLife

from matplotlib.colors import ListedColormap

custom_cmap = ListedColormap(['green', 'red'])
plot_params={ "column": "state","cmap": custom_cmap,  "ec" : 'black'}


grid = RegularGrid(bounds=(0, 0, 100, 100), dim=10, attrs={'state': 0})
glider_pattern = [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]
]

grid.fill (attr='state', pattern=glider_pattern, start_x=3, start_y=3)

env = Environment (
    gdf = grid.to_geodaframe(),
    end_time = 10,
    start_time=0
)


GameOfLife(create_neighbohood="Queen")

Map( 
    plot_params={ "column": "state","cmap": custom_cmap,  "ec" : 'black'}
)

env.run()