import pandas as pd

df = pd.read_csv("atm.csv")

# keep ATM rows only
df = df[df["Service Channel Type"] == "ADI-operated ATMs"]

# drop missing or out-of-range coordinates
df = df.dropna(subset=["Latitude", "Longitude"])
df = df[df["Longitude"].between(112, 154) & df["Latitude"].between(-44, -9)]

# keep only 2017 and 2026
df = df[df["year"].isin([2017, 2026])]

# keep only the columns the map uses
cols = ["year", "States and Territories", "Suburb or locality",
        "Institution Name", "Latitude", "Longitude", "Number"]
df = df[cols]

# one file per year
for y, g in df.groupby("year"):
    g.to_csv(f"atm{y}.csv", index=False)
    print(y, "rows:", len(g), "total ATMs:", g["Number"].sum())

print(df["States and Territories"].unique())