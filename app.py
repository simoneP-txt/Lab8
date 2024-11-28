import streamlit as st
import polars as pl
import altair as alt
from vega_datasets import data
from icecream import ic
import geopandas as gpd

url = "https://www.dei.unipd.it/~ceccarello/data/gapminder.csv"

data1 = pl.read_csv(url)

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
st.dataframe(data_07)

pie_chart = (
    alt.Chart(data_07)
    .mark_arc( radius = 110, radius2 = 165, cornerRadius=5)
    .transform_aggregate(
        pop = "sum(pop)",
        groupby = ["continent"]
    )
    .encode(
        alt.Theta("pop", aggregate = "sum"),
        alt.Color("continent")
    )
)

st.altair_chart(
    pie_chart,
    use_container_width=True
)

@st.cache_data
def get_data(url):
    return pl.read_csv(url)

data = get_data(url)
data2007 = data.filter(pl.col("year") == 2007)

total_pop_2007 = data2007.select(pl.col("pop").sum())


base_chart = (
    alt.Chart(data)
    .transform_aggregate(
        pop = "sum(pop)",
        groupby = ["continent"]
    )
)

base_pie = (
    base_chart
    .mark_arc(
        radius = 80,
        radius2 = 120,
        cornerRadius = 20
    )
    .encode(
        alt.Theta("pop"),
        alt.Color("continent")
    )
)

text_pie = (
    base_chart
    .mark_text(
        radius = 150,
        size=15
    )
    .transform_calculate(
        label = "round(datum.pop / 1000000) + ' M'"
    )
    .encode(
        alt.Text("label:N"),
        alt.Theta("pop", stack=True),
        alt.Order("continent")
    )
)

text_total = (
    base_chart
    .mark_text(
        radius = 0,
        size=30
    )
    .transform_aggregate(
        pop = "sum(pop)"
    )
    .transform_calculate(
        label = "round(datum.pop / 1000000) + ' M'"
    )
    .encode(
        alt.Text("label:N")
    )
)

chart = (
    base_pie + text_pie + text_total
).properties(
    height = 30,
    width = 30
).facet(
    "year", columns=2
)

st.altair_chart(
    chart,
    use_container_width=True
)
###########################################################################################
#congo, dem congo, repubblica centro africana, sudan del sud
data_07_new = data_07.with_columns(
        pl.when(pl.col("country") == "United States")
        .then("United States of America")
        .otherwise(pl.col("country"))
        .alias("country")
    )
print(data_07_new)

map110 = (alt.Chart(alt.topo_feature("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json", 'countries'))
         .mark_geoshape(stroke = "black").encode(
    color=alt.Color('lifeExp:Q', scale=alt.Scale(scheme='greens')),
    tooltip=['country:N', 'lifeExp:Q']  # tooltip per visualizzare informazioni
    ).transform_lookup(
    lookup='properties.name',  # chiave comune per unire (nel TopoJSON)
    from_=alt.LookupData(data_07, 'country', ['lifeExp'])  # fonte dei dati
    ).project(
    type='mercator'  # proiezione geografica
    ).properties(
    width=800,
    height=600,
    title="Aspettativa di vita nel 2007, scala 1:110"
    )
)

st.altair_chart(
    map110,
    use_container_width=True
)



###########################################################################################################
