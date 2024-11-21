import streamlit as st
import polars as pl
import altair as alt
from vega_datasets import data
from icecream import ic
import geopandas as gpd

url = "https://www.dei.unipd.it/~ceccarello/data/gapminder.csv"

data1 = pl.read_csv(url)

st.dataframe(data1)

ts = (
    alt.Chart(data1)
    .mark_line()
    .encode(
        alt.X("year").scale(zero=False),
        alt.Y("lifeExp", aggregate = "mean").scale(zero = False),
        alt.Color("continent")
    )
)

st.altair_chart(
    ts,
    use_container_width=True
)

data_07 = data1.filter(pl.col("year") == 2007)

pie_chart = (
    alt.Chart(data_07)
    .mark_arc(radius = 100, radius2 = 150, cornerRadius=5)
    .encode(
        alt.Theta("pop", aggregate = "sum"),
        alt.Color("continent")
    )
)

st.altair_chart(
    pie_chart,
    use_container_width=True
)

source = alt.topo_feature(data.world_110m.url, 'countries')
input_dropdown = alt.binding_select(options=[
    "equalEarth",
    "naturalEarth1",
    "orthographic"
], name='Projection ')

param_projection = alt.param(value="equalEarth", bind=input_dropdown)

#from altair import expr
#
#countries = alt.topo_feature(data.world_110m.url, 'countries')
#
## Rinominare le colonne per corrispondere, se necessario (es: country -> name)
#data_07 = data_07.rename({"country": "name"})  # Adatta il nome se serve
#print(data_07)
## Unire i dati geografici con il dataset dei paesi
#merged_data = (
#    alt.Chart(countries)
#    .transform_lookup(
#        lookup="properties.name",  # Nome del campo geografico
#        from_=alt.LookupData(data_07.to_pandas(), "name", ["lifeExp"])  # Dati da unire
#    )
#)
#

df_us_unemp = data.unemployment()
print(df_us_unemp)

#countries = gpd.read_file(data.world_110m.url, driver='TopoJSON', layer='countries')
#print(countries)
map = (
    alt.Chart(source, width=500, height=300)
    .mark_geoshape(fill='lightgray', stroke='gray')
    #.transform_lookup()
    .project(type=alt.expr(param_projection.name))
    .add_params(param_projection)
    .encode(
        #color=data_07["lifeExp"]
    )
)

st.altair_chart(
    map,
    use_container_width=True
)

print(data_07.select("lifeExp"))

gdf_world = gpd.read_file(data.world_110m.url, driver="TopoJSON")

world = alt.Chart(gdf_world).mark_geoshape(
    fill="mintcream", stroke="black", strokeWidth=0.35
)

st.altair_chart(
    world,
    use_container_width=True
)