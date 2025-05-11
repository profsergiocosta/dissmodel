
from geopandas import GeoDataFrame

from dissmodel.core.spatial import dw_query


def test_dw_query():

    sparql = '''
PREFIX : <https://landchangedata.linked.data.world/d/dbcells/>
prefix geo: <http://www.opengis.net/ont/geosparql#>
prefix sdmx-dimension: <http://purl.org/linked-data/sdmx/2009/dimension#>

SELECT ?cell ?wkt
WHERE {
  ?cell geo:asWKT ?wkt.
   ?cell sdmx-dimension:refArea "AC".
}
'''


    gdf = dw_query ("landchangedata/dbcells", sparql)

    rows, _ = gdf.shape

    assert isinstance(gdf, GeoDataFrame) and rows == 1902