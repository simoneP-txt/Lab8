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
###########################################################################################
source = alt.topo_feature(data.world_110m.url, 'countries')
input_dropdown = alt.binding_select(options=[
    "equalEarth",
    "naturalEarth1",
    "orthographic"
], name='Projection ')

param_projection = alt.param(value="equalEarth", bind=input_dropdown)

df_us_unemp = data.unemployment()
print(df_us_unemp)

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