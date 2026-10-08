import pandas as pd

df = pd.read_csv(
    "data/raw/business_licenses.csv",
    low_memory=False
)

print("\n=== LICENSE STATUS ===")
print(df["license_status"].value_counts(dropna=False))

print("\n=== TOP LICENSE DESCRIPTIONS ===")
print(df["license_description"].value_counts().head(30))

print("\n=== TOP BUSINESS ACTIVITIES ===")
print(df["business_activity"].value_counts().head(30))

print("\n=== TOP NEIGHBORHOODS ===")
print(df["neighborhood"].value_counts().head(30))

print("\n=== TOP COMMUNITY AREAS ===")
print(df["community_area_name"].value_counts().head(30))