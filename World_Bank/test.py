import json
import pandas as pd

# Load the CSV, treating World Bank placeholders as missing
wb = pd.read_csv("v2.csv", na_values=["..", "", " "])
wb["Adoption_Rate"] = pd.to_numeric(wb["Adoption_Rate"], errors="coerce")

# Load the countries from the map file
topo = json.load(open("ne_110m_admin_0_countries.json"))
geoms = topo["objects"]["ne_110m_admin_0_countries"]["geometries"]
map_df = pd.DataFrame([g["properties"] for g in geoms])

# Natural Earth uses -99 for some ISO_A3 codes (France, Norway, Kosovo...),
# so fall back to ISO_A3_EH, then ADM0_A3
def pick_code(row):
    for col in ("ISO_A3", "ISO_A3_EH", "ADM0_A3"):
        if col in row and row[col] not in (None, "-99", -99):
            return row[col]
    return None

map_df["code"] = map_df.apply(pick_code, axis=1)

merged = map_df.merge(
    wb[["Country Code", "Adoption_Rate"]],
    left_on="code", right_on="Country Code", how="left", indicator=True
)

# 1) On the map, but not in the CSV at all
not_in_csv = merged[merged["_merge"] == "left_only"]

# 2) In the CSV, but the value is blank / ".."
blank_value = merged[(merged["_merge"] == "both") & merged["Adoption_Rate"].isna()]

print(f"Map countries: {len(map_df)}")
print(f"\nNot in CSV ({len(not_in_csv)}):")
print(not_in_csv[["NAME", "code"]].to_string(index=False))
print(f"\nIn CSV but no value ({len(blank_value)}):")
print(blank_value[["NAME", "code"]].to_string(index=False))

# Save the full list
pd.concat([not_in_csv, blank_value])[["NAME", "code"]] \
  .sort_values("NAME").to_csv("countries_no_data.csv", index=False)