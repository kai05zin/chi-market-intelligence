import pandas as pd

# Load data
df = pd.read_csv("data/raw/business_licenses.csv")

# Basic information
print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isna().sum().sort_values(ascending=False).head(15))