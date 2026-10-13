import pandas as pd

# 1. Load the dataset skipping top metadata rows
df = pd.read_csv('API_IT.NET.USER.ZS_DS2_en_csv_v2_461985.csv')

# 2. Filter for countries and regional aggregates of interest
selected_entities = [
    'Australia',
    'United Kingdom',
    'Japan',
    'United States'
]
df_filtered = df[df['Country Name'].isin(selected_entities)]

# 3. Melt from wide to long format
df_long = df_filtered.melt(
    id_vars=['Country Name', 'Country Code'],  # Fixed identifier columns
    var_name='Year',                           # New column for years
    value_name='Adoption_Rate'                 # New column for data values
)

# 4. Clean up the melted dataframe
df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce')
df_long = df_long.dropna(subset=['Year', 'Adoption_Rate'])
df_long['Year'] = df_long['Year'].astype(int)

# Filter for relevant timeline (2007 to 2017)
df_long = df_long[(df_long['Year'] >= 1990) & (df_long['Year'] <= 2024)]

# 5. Export clean long data for Vega-Lite or Altair
df_long.to_csv('world_bank_long.csv', index=False)
df_long.to_json('world_bank_long.json', orient='records', indent=2)