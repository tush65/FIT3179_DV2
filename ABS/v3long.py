import pandas as pd

# Load your original CSV file
df = pd.read_csv('v3.csv')

# 1. Clean column names (strip whitespace and remove '(%)')
df.columns = df.columns.str.replace(r'\s*\(%\)', '', regex=True).str.strip()

# 2. Unpivot (melt) wide data into long format for Vega-Lite
df_long = df.melt(
    id_vars=['Age Group'],
    var_name='Activity',
    value_name='Percentage'
)

# 3. Export to JSON or CSV for Vega-Lite
df_long.to_json('technology_usage_processed.json', orient='records', indent=2)
df_long.to_csv('technology_usage_processed.csv', index=False)

print("Preprocessing complete! Preview:")
print(df_long.head())