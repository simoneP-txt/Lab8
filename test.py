import json
from urllib.request import urlopen
from vega_datasets import data
import polars as pl
import pandas as pd
from icecream import ic
import geopandas as gpd
import altair as alt
import streamlit as st

gdf_us_counties = gpd.read_file(data.us_10m.url, driver='TopoJSON', layer='counties')
df_us_unemp = data.unemployment()

map = alt.Chart(gdf_us_counties).mark_geoshape().transform_lookup(
    lookup='id',
    from_=alt.LookupData(data=df_us_unemp, key='id', fields=['rate'])
).encode(
    alt.Color('rate:Q')
).project(
    type='albersUsa'
)

st.altair_chart(
    map
)
#############################################################
url = data.world_110m.url
with urlopen(url) as response:
    topojson = json.load(response)

# Estrarre gli id e i nomi dai paesi
countries = topojson["objects"]["countries"]["geometries"]

# Analizza la struttura per identificare le chiavi disponibili
for country in countries[:5]:  # Guarda solo i primi 5 paesi per non sovraccaricare l'output
    print(country)

url = "https://www.dei.unipd.it/~ceccarello/data/gapminder.csv"

data1 = pl.read_csv(url)
data_07 = data1.filter(pl.col("year") == 2007)

#id_to_country = {
#    4: "Afghanistan",
#    24: "Angola",
#    8: "Albania",
#    784: "United Arab Emirates",
#    32: "Argentina",
#}
#
#country_to_id = {v: k for k, v in id_to_country.items()}
#
#data_07_1 = data_07.with_columns(
#    pl.col("country").map_elements(country_to_id).alias("id")
#)
#
