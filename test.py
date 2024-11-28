import polars as pl

url = "https://www.dei.unipd.it/~ceccarello/data/gapminder.csv"

data1 = pl.read_csv(url)
data_07 = data1.filter(pl.col("year") == 2007)
print(data_07)
data_07.write_csv("data_07.csv")