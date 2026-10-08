import requests
import pandas as pd


BASE_URL = (
    "https://services5.arcgis.com/"
    "LcMXE3TFhi1BSaCY/arcgis/rest/services/"
    "CommunityDataSnapshots_Historical/FeatureServer/11/query"
)

params = {
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": "false",
    "f": "json"
}

response = requests.get(BASE_URL, params=params)

print("Status:", response.status_code)

if response.status_code != 200:
    print(response.text)
    raise SystemExit()

data = response.json()

if "features" not in data:
    print(data)
    raise SystemExit()

rows = [feature["attributes"] for feature in data["features"]]

df = pd.DataFrame(rows)

print("\n=== CMAP 2026 COMMUNITY DATA ===")
print("Rows:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 10 rows:")
print(df.head(10).to_string(index=False))

print("\nPossible population columns:")
for column in df.columns:
    if "pop" in column.lower():
        print(column)

df.to_csv(
    "data/raw/cmap_2026.csv",
    index=False
)

print("\nSaved to:")
print("data/raw/cmap_2026.csv")