import requests
import pandas as pd

url = (
    "https://data.cityofchicago.org/resource/"
    "ijzp-q8t2.json"
)

params = {
    "$select": "community_area, count(*) as crime_count",
    "$where": "community_area IS NOT NULL",
    "$group": "community_area",
    "$order": "community_area",
    "$limit": 100
}

response = requests.get(url, params=params)

print("Status:", response.status_code)

if response.status_code != 200:
    print(response.text)
    raise SystemExit()

data = response.json()

df = pd.DataFrame(data)

print("\n=== CRIME BY COMMUNITY AREA ===")
print(df)

print("\nRows:", len(df))

df.to_csv(
    "data/raw/crime_by_community_area.csv",
    index=False
)

print("\nSaved to:")
print("data/raw/crime_by_community_area.csv")