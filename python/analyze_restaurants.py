import pandas as pd

df = pd.read_csv(
    "data/raw/business_licenses.csv",
    low_memory=False
)

# Find food-related licenses
food_mask = (
    df["license_description"].str.contains(
        "Food|Tavern|Kitchen|Caterer",
        case=False,
        na=False
    )
    |
    df["business_activity"].str.contains(
        "Food|Dining|Kitchen|Cater",
        case=False,
        na=False
    )
)

food = df[food_mask].copy()

print("=== FOOD MARKET ===")
print(f"Food-related license records: {len(food):,}")

print("\n=== UNIQUE LICENSE HOLDERS ===")
print(
    "Unique account numbers:",
    food["account_number"].nunique()
)

print(
    "Unique business names:",
    food["doing_business_as_name"].nunique()
)

print(
    "Unique legal names:",
    food["legal_name"].nunique()
)

print("\n=== TOP FOOD LICENSE TYPES ===")
print(
    food["license_description"]
    .value_counts()
    .head(20)
)

print("\n=== TOP FOOD BUSINESS ACTIVITIES ===")
print(
    food["business_activity"]
    .value_counts()
    .head(20)
)

print("\n=== TOP FOOD NEIGHBORHOODS ===")
print(
    food["neighborhood"]
    .value_counts()
    .head(30)
)

print("\n=== TOP FOOD COMMUNITY AREAS ===")
print(
    food["community_area_name"]
    .value_counts()
    .head(30)
)