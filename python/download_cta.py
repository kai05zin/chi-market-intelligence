import pandas as pd
import requests

url = (
    "https://data.cityofchicago.org/resource/"
    "8pix-ypme.json?$limit=50000"
)

response = requests.get(url)

print("Status:", response.status_code)

if response.status_code != 200:
    print(response.text)
    raise SystemExit()

data = response.json()

df = pd.DataFrame(data)

print("\n=== CTA BUS STOPS ===")
print("Rows:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

df.to_csv(
    "data/raw/cta_bus_stops.csv",
    index=False
)

print("\nSaved to data/raw/cta_bus_stops.csv")