
import geopandas as gpd
import numpy as np
from shapely.geometry import box

import matplotlib.pyplot as plt
import rasterio

def regular_grid(gdf=None, bounds=None, resolution=1000, attrs={}, crs=None):
    """
    Cria um grid regular com células de tamanho fixo (homogêneo) que cobre um GeoDataFrame ou bounds.
    
    Parameters:
        gdf (GeoDataFrame): GeoDataFrame para extrair bounds.
        bounds (tuple): (xmin, ymin, xmax, ymax) se não quiser usar gdf.
        resolution (float): Tamanho das células (em unidades do CRS).
        attrs (dict): Atributos adicionais a adicionar ao grid.
        crs (str): CRS do grid.
    
    Returns:
        GeoDataFrame: Grid com células regulares (mesmo tamanho).
    """
    # Obter bounds
    if bounds is not None:
        xmin, ymin, xmax, ymax = bounds
    elif gdf is not None:
        xmin, ymin, xmax, ymax = gdf.total_bounds
    else:
        raise ValueError("Forneça um GeoDataFrame ou bounds explícito.")
    
    # Calcular largura e altura
    width = xmax - xmin
    height = ymax - ymin
    
    # Calcular o número necessário de células para cobrir a área
    n_cols = int(np.ceil(width / resolution))
    n_rows = int(np.ceil(height / resolution))
    
    # Ajustar xmax e ymax para que o grid tenha células completas
    xmax_adj = xmin + n_cols * resolution
    ymax_adj = ymin + n_rows * resolution
    
    # Gerar os limites das células
    x_edges = np.arange(xmin, xmax_adj, resolution)
    y_edges = np.arange(ymin, ymax_adj, resolution)
    
    grid_cells = []
    ids = []
    for i, x0 in enumerate(x_edges):
        for j, y0 in enumerate(y_edges):
            x1, y1 = x0 + resolution, y0 + resolution
            poly = box(x0, y0, x1, y1)
            grid_cells.append(poly)
            ids.append(f"{j}-{i}")
    
    data = {"geometry": grid_cells, "id": ids}
    for key, value in attrs.items():
        data[key] = [value] * len(grid_cells)
    
    grid_gdf = gpd.GeoDataFrame(data, crs=crs).set_index("id")
    return grid_gdf

