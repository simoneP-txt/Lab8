from vega_datasets import data
import geopandas as gpd
from icecream import ic

#countries = gpd.read_file(data.world_110m.url, layer='countries')
#ic(countries)
#print(countries)
gdf_us_counties = gpd.read_file(data.us_10m.url, driver = "TopoJSON")
print(gdf_us_counties)