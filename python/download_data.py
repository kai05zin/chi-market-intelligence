import requests
import pandas as pd
from pathlib import Path

API_URL = "https://data.cityofchicago.org/resource/uupf-x98q.json"

LIMIT = 5000
offset = 0
all_data = []

while True:
    print(f"Downloading rows {offset}–{offset + LIMIT}...")

    params = {
        "$limit": LIMIT,
        "$offset": offset
    }

    response = requests.get(API_URL, params=params)
    response.raise_for_status()

    data = response.json()

    if not data:
        break

    all_data.extend(data)
    offset += LIMIT

    print(f"Downloaded: {len(all_data)} rows")

df = pd.DataFrame(all_data)

output_path = Path("data/raw/business_licenses.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

print("\nDone!")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {output_path}")