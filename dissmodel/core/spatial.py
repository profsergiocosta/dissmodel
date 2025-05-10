
import geopandas as gpd
import numpy as np
from shapely.geometry import box
from rasterstats import zonal_stats
import datadotworld as dw

import random


from dotenv import load_dotenv

# data world
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def dw_query (dataset, query, geo_column = 'wkt', query_type='sparql'):
    print ("loading data from DBCells")
    results = dw.query(dataset, query, query_type)
    gdf = gpd.GeoDataFrame(results.dataframe, geometry=gpd.GeoSeries.from_wkt(results.dataframe[geo_column]))
    return gdf

## issue: gera linhas com geometria nula, por exemplo, na dimensao 10
def regular_grid(gdf=None, bounds=None, dim=10, attrs={}, crs="EPSG:29902"):
    """
    Create a square grid that covers a GeoDataFrame area
    or a fixed boundary with x-y coordinates.
    
    Parameters:
        gdf (GeoDataFrame): Optional GeoDataFrame to cover with the grid.
        bounds (tuple): Optional tuple (xmin, ymin, xmax, ymax) defining the grid area.
        n_cells (int): Number of cells along one dimension (e.g., rows or columns).
        attrs (dict): Additional attributes to include in the grid GeoDataFrame.
        crs (str): Coordinate reference system for the output grid.
    
    Returns:
        GeoDataFrame: GeoDataFrame of grid polygons with attributes.
    """


    # Obter limites do GeoDataFrame ou usar limites fornecidos
    if bounds is not None:
        xmin, ymin, xmax, ymax = bounds
    else:
        xmin, ymin, xmax, ymax = gdf.total_bounds

    # Certificar que o grid cobre todo o espaço
    x_edges = np.linspace(xmin, xmax, dim + 1)
    y_edges = np.linspace(ymin, ymax, dim + 1)

    # Criar células do grid
    grid_cells = []
    ids = []
    for i in range(len(x_edges) - 1):
        for j in range(len(y_edges) - 1):
            x0, x1 = x_edges[i], x_edges[i + 1]
            y0, y1 = y_edges[j], y_edges[j + 1]
            poly = box(x0, y0, x1, y1)  # Criar um polígono representando a célula
            grid_cells.append(poly)
            ids.append(f"{j}-{i}")

    # Criar GeoDataFrame com células
    data = {"geometry": grid_cells, "id": ids}
    for key, value in attrs.items():
        data[key] = [value] * len(grid_cells)

    grid_gdf = gpd.GeoDataFrame(data, crs=crs)
    grid_gdf.set_index(["id"], inplace=True)

    return grid_gdf



def fill_regular_grid (gdf, attr, pattern, start_x=0, start_y=0):

        """
        Preenche atributos em um GeoDataFrame com base em um padrão regular (grid).

        Parameters:
            gdf (GeoDataFrame): GeoDataFrame cujas células serão preenchidas.
            attr (str): Nome do atributo a ser preenchido.
            pattern (list[list]): Padrão (grid) a ser aplicado.
            start_x (int): Offset inicial na direção x.
            start_y (int): Offset inicial na direção y.
        """    
    
        w = len(pattern)
        h = len(pattern[0])
        for i in range(w):
            for j in range(h):
                idx = f"{start_x + i}-{start_y + j}"
                #print ("loc", idx, "i-j", i, j)
                gdf.loc[idx,attr] = pattern[w-i-1][j]




## random



def generate_sample(data, size=1):
    """
    Gera uma amostra baseada em:
      - Lista de opções (uniforme ou não)
      - Dicionário com probabilidades
      - Intervalo de valores inteiros (min e max)
    
    Args:
        data (list, dict): 
            - Se `list`: opções com probabilidades uniformes.
            - Se `dict` com chaves:
                - `opção: probabilidade`: valores e respectivas probabilidades.
                - `min` e `max`: intervalo para números inteiros.
        size (int): Número de amostras a serem geradas.
    
    Returns:
        list: Uma lista com as amostras geradas.
    """
    if isinstance(data, dict):
        # Caso seja um intervalo com min e max
        if 'min' in data and 'max' in data:
            return [random.randint(data['min'], data['max']) for _ in range(size)]
        
        # Caso seja um dicionário com probabilidades
        options = list(data.keys())
        probabilities = list(data.values())
        return random.choices(options, weights=probabilities, k=size)

    elif isinstance(data, list):
        # Probabilidades uniformes com lista simples
        return random.choices(data, k=size)

    else:
        raise ValueError("O argumento `data` deve ser uma lista ou um dicionário.")


import random

def fill_random_sample(gdf, attr, data, seed=None):
    """
    Preenche o GeoDataFrame com valores aleatórios gerados pela função `generate_sample`.

    Args:
        gdf (GeoDataFrame): Grade a ser preenchida.
        attr (str): Nome do atributo a ser preenchido.
        data (list|dict): Fonte de dados para amostragem.
        seed (int, optional): Semente aleatória para reprodutibilidade.
    """
    if seed is not None:
        random.seed(seed)

    size = len(gdf)
    samples = generate_sample(data, size=size)
    gdf[attr] = samples


### Preenchimento

def fill_zonal_stats(vectors, raster_data, affine, stats, prefix="attr_", nodata=-999):
    """
    Preenche atributos em `vectors` usando estatísticas zonais de um raster.
    
    Parameters:
        vectors (GeoDataFrame): GeoDataFrame com polígonos para análise.
        raster_data (numpy array): Dados do raster.
        affine (Affine): Transformação affine do raster.
        stats (list): Lista de estatísticas zonais a serem calculadas.
        prefix (str): Prefixo para os atributos adicionados.
    """
    stats_output = zonal_stats(
        vectors=vectors, 
        raster=raster_data, 
        affine=affine, 
        nodata = nodata,
        stats=stats
    )
    
    for stat in stats:
        vectors[f"{prefix}{stat}"] = [feature[stat] for feature in stats_output]

def fill_min_distance(from_gdf, to_gdf, attr_name="min_distance"):
    """
    Preenche atributos em `from_gdf` com a distância mínima até geometrias de `to_gdf`.

    Parameters:
        from_gdf (GeoDataFrame): GeoDataFrame com os polígonos a serem preenchidos.
        to_gdf (GeoDataFrame): GeoDataFrame com os pontos de referência.
        attr_name (str): Nome do atributo para armazenar as distâncias mínimas.
    """
    from_gdf[attr_name] = from_gdf.geometry.apply(
        lambda geom: to_gdf.geometry.distance(geom).min()
    )

def fill (strategy, **kwargs):
    """
    Interface principal para escolher a estratégia de preenchimento de atributos.

    Parameters:
        strategy (str): Estratégia de preenchimento ("zonal_stats" ou "min_distance").
        kwargs: Argumentos específicos para cada estratégia.
    """
    if strategy == "zonal_stats":
        fill_zonal_stats(**kwargs)
    elif strategy == "min_distance":
        fill_min_distance(**kwargs)
    elif strategy == "pattern":
        fill_regular_grid(**kwargs)
    elif strategy == "random_sample":
        fill_random_sample(**kwargs)
    else:
        raise ValueError(f"Estratégia desconhecida: {strategy}")