import pandas as pd

df = pd.read_csv("atm_years.csv")

# round coordinates so the same location matches across years
df["Latitude"] = df["Latitude"].round(4)
df["Longitude"] = df["Longitude"].round(4)

cols = ["Institution Name", "States and Territories", "Suburb or locality",
        "Latitude", "Longitude"]

# total ATMs per location for each year
g = (df[df["year"].isin([2017, 2026])]
       .groupby(cols + ["year"], as_index=False)["Number"].sum())

a = g[g["year"] == 2017].drop(columns="year").rename(columns={"Number": "n2017"})
b = g[g["year"] == 2026].drop(columns="year").rename(columns={"Number": "n2026"})

# join the two years; a location missing from one year gets 0
m = a.merge(b, on=cols, how="outer").fillna({"n2017": 0, "n2026": 0})

def status(r):
    if r.n2026 == 0:
        return "Closed"
    if r.n2017 == 0:
        return "New"
    return "Still open"

m["status"] = m.apply(status, axis=1)

# sort number so closed dots are drawn on top
m["rank"] = m["status"].map({"Still open": 0, "New": 1, "Closed": 2})

m.to_csv("atm_change.csv", index=False)

print(m["status"].value_counts())
print("2017 total:", m["n2017"].sum(), "| 2026 total:", m["n2026"].sum())