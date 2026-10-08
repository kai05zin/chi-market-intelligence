import pandas as pd

input_file = "data/raw/business_licenses.csv"
output_file = "data/processed/community_coordinates.csv"

df = pd.read_csv(input_file)

df["community_area"] = pd.to_numeric(
    df["community_area"], errors="coerce"
)

df["latitude"] = pd.to_numeric(
    df["latitude"], errors="coerce"
)

df["longitude"] = pd.to_numeric(
    df["longitude"], errors="coerce"
)

coords = (
    df[
        df["community_area"].between(1, 77)
        & df["latitude"].notna()
        & df["longitude"].notna()
    ]
    .groupby("community_area")
    .agg(
        latitude=("latitude", "median"),
        longitude=("longitude", "median")
    )
    .reset_index()
)

coords["community_area"] = coords["community_area"].astype(int)

coords.to_csv(output_file, index=False)

print(f"Created {output_file}")
print(f"Community areas: {len(coords)}")
print(coords.head(10))