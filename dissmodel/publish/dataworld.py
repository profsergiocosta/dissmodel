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