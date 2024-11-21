import streamlit as st
import polars as pl
import altair as alt

url = "https://www.dei.unipd.it/~ceccarello/data/gapminder.csv"

data = pl.read_csv(url)

st.dataframe(data)

ts = (
    alt.Chart(data)
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

data_07 = data.filter(pl.col("year") == 2007)

pie_chart = (
    alt.Chart(data)
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

