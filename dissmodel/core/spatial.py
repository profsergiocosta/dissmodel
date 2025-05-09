
import geopandas as gpd
import numpy as np
from shapely.geometry import box

class RegularGrid:
    def __init__(self, gdf=None, bounds=None, dim=10, attrs=None, crs="EPSG:29902"):
        self.dim = dim
        self.attrs = attrs or {}
        self.crs = crs

        if bounds:
            self.bounds = bounds
        elif gdf is not None:
            self.bounds = gdf.total_bounds
        else:
            raise ValueError("Either 'gdf' or 'bounds' must be provided.")
        
        self.grid = self._create_grid()
    
    def _create_grid(self):
        xmin, ymin, xmax, ymax = self.bounds
        x_edges = np.linspace(xmin, xmax, self.dim + 1)
        y_edges = np.linspace(ymin, ymax, self.dim + 1)

        grid_cells = []
        ids = []

        for i in range(len(x_edges) - 1):
            for j in range(len(y_edges) - 1):
                x0, x1 = x_edges[i], x_edges[i + 1]
                y0, y1 = y_edges[j], y_edges[j + 1]
                poly = box(x0, y0, x1, y1)
                grid_cells.append(poly)
                ids.append(f"{j}-{i}")

        data = {"geometry": grid_cells, "id": ids}
        for key, value in self.attrs.items():
            data[key] = [value] * len(grid_cells)

        gdf = gpd.GeoDataFrame(data, crs=self.crs)
        gdf.set_index("id", inplace=True)
        return gdf

    def fill(self, attr, pattern, start_x=0, start_y=0):
        w = len(pattern)
        h = len(pattern[0])
        for i in range(w):
            for j in range(h):
                idx = f"{start_x + i}-{start_y + j}"
                if idx in self.grid.index:
                    self.grid.loc[idx, attr] = pattern[w - i - 1][j]

    def to_geodaframe(self):
        return self.grid
