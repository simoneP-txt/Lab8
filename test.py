from vega_datasets import data
import geopandas as gpd
from icecream import ic

#countries = gpd.read_file(data.world_110m.url, layer='countries')
#ic(countries)
#print(countries)
gdf_world = gpd.read_file(data.world_110m.url, driver="TopoJSON")
print(gdf_world)