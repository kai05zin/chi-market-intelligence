import pandas as pd
from pathlib import Path


# =========================
# Paths
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

BUSINESS_FILE = BASE_DIR / "data/raw/business_licenses.csv"
CRIME_FILE = BASE_DIR / "data/raw/crime_by_community_area.csv"
CMAP_FILE = BASE_DIR / "data/raw/cmap_2026.csv"

OUTPUT_DIR = BASE_DIR / "data/processed"
OUTPUT_FILE = OUTPUT_DIR / "market_analysis.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# Load data
# =========================

print("Loading data...")

business = pd.read_csv(BUSINESS_FILE, low_memory=False)
crime = pd.read_csv(CRIME_FILE)
cmap = pd.read_csv(CMAP_FILE, low_memory=False)

print(f"Business licenses: {len(business):,}")
print(f"Crime areas: {len(crime):,}")
print(f"CMAP areas: {len(cmap):,}")


# =========================
# 1. Identify restaurant-like businesses
# =========================

# Normalize text fields
license_desc = (
    business["license_description"]
    .fillna("")
    .astype(str)
    .str.lower()
)

activity = (
    business["business_activity"]
    .fillna("")
    .astype(str)
    .str.lower()
)

# Restaurant / dining signals
restaurant_mask = (
    license_desc.str.contains(
        r"retail food establishment|tavern|caterer",
        regex=True,
        na=False
    )
    |
    activity.str.contains(
        r"preparation of food|food prepared onsite|dining on premises|"
        r"food preparation|restaurant|catering",
        regex=True,
        na=False
    )
)

restaurant = business[restaurant_mask].copy()

# Remove obvious non-restaurant food categories
restaurant_license_desc = (
    restaurant["license_description"]
    .fillna("")
    .astype(str)
    .str.lower()
)

restaurant_activity = (
    restaurant["business_activity"]
    .fillna("")
    .astype(str)
    .str.lower()
)

exclude_mask = (
    restaurant_license_desc.str.contains(
        r"wholesale|special event|shared kitchen",
        regex=True,
        na=False
    )
    |
    restaurant_activity.str.contains(
        r"wholesale|shared kitchen|retail sales of perishable foods",
        regex=True,
        na=False
    )
)

restaurant = restaurant[~exclude_mask].copy()


# =========================
# 2. Create community-area restaurant counts
# =========================

restaurant["community_area"] = pd.to_numeric(
    restaurant["community_area"],
    errors="coerce"
)

restaurant = restaurant.dropna(subset=["community_area"])

restaurant_counts = (
    restaurant.groupby("community_area")["account_number"]
    .nunique()
    .reset_index(name="restaurant_businesses")
)

print()
print("=== RESTAURANT MARKET ===")
print(f"Restaurant-related license records: {len(restaurant):,}")
print(
    f"Unique restaurant business accounts: "
    f"{restaurant_counts['restaurant_businesses'].sum():,}"
)


# =========================
# 3. Prepare CMAP data
# =========================

cmap_clean = pd.DataFrame({
    "community_area": pd.to_numeric(cmap["GEOID"], errors="coerce"),
    "community_area_name": cmap["GEOG"],
    "population": pd.to_numeric(cmap["TOT_POP"], errors="coerce"),
    "median_income": pd.to_numeric(cmap["MEDINC"], errors="coerce"),
    "per_capita_income": pd.to_numeric(
        cmap["INCPERCAP"], errors="coerce"
    ),
    "unemployment": pd.to_numeric(
        cmap["UNEMP"], errors="coerce"
    ),
    "transit_commuters": pd.to_numeric(
        cmap["TRANSIT"], errors="coerce"
    ),
    "total_commuters": pd.to_numeric(
        cmap["TOT_COMM"], errors="coerce"
    ),
})


# =========================
# 4. Prepare crime data
# =========================

crime_clean = crime.copy()

crime_clean["community_area"] = pd.to_numeric(
    crime_clean["community_area"],
    errors="coerce"
)

crime_clean["crime_count"] = pd.to_numeric(
    crime_clean["crime_count"],
    errors="coerce"
)

# Community area 0 is not a real community area
crime_clean = crime_clean[
    crime_clean["community_area"].between(1, 77)
]

crime_clean = crime_clean[
    ["community_area", "crime_count"]
]


# =========================
# 5. Merge datasets
# =========================

market = cmap_clean.merge(
    restaurant_counts,
    on="community_area",
    how="left"
)

market = market.merge(
    crime_clean,
    on="community_area",
    how="left"
)

market["restaurant_businesses"] = (
    market["restaurant_businesses"]
    .fillna(0)
    .astype(int)
)

market["crime_count"] = (
    market["crime_count"]
    .fillna(0)
)


# =========================
# 6. Calculate market metrics
# =========================

# Restaurant density per 10,000 residents
market["restaurant_density"] = (
    market["restaurant_businesses"]
    / market["population"]
    * 10000
)

# Transit share:
# TRANSIT is a subset of commuters,
# so denominator should be total commuters,
# not total population.
market["transit_share"] = (
    market["transit_commuters"]
    / market["total_commuters"]
    * 100
)

# Population served by each restaurant.
# Higher = potentially less competition.
market["population_per_restaurant"] = (
    market["population"]
    / market["restaurant_businesses"].replace(0, pd.NA)
)


# =========================
# 7. Clean values
# =========================

market = market.replace(
    [float("inf"), float("-inf")],
    pd.NA
)

# Keep only real Chicago community areas
market = market[
    market["community_area"].between(1, 77)
].copy()


# =========================
# 8. Sort
# =========================

market = market.sort_values(
    "restaurant_density",
    ascending=False
)


# =========================
# 9. Select final columns
# =========================

market = market[
    [
        "community_area",
        "community_area_name",
        "population",
        "restaurant_businesses",
        "restaurant_density",
        "population_per_restaurant",
        "median_income",
        "per_capita_income",
        "unemployment",
        "transit_commuters",
        "total_commuters",
        "transit_share",
        "crime_count",
    ]
]


# =========================
# 10. Save
# =========================

market.to_csv(
    OUTPUT_FILE,
    index=False
)


# =========================
# 11. Print results
# =========================

print()
print("=== MARKET ANALYSIS ===")

print(
    market[
        [
            "community_area",
            "community_area_name",
            "population",
            "restaurant_businesses",
            "restaurant_density",
            "population_per_restaurant",
            "median_income",
            "unemployment",
            "transit_share",
            "crime_count",
        ]
    ].head(20).to_string(index=False)
)

print()
print(f"Rows: {len(market)}")
print()
print("Saved to:")
print(OUTPUT_FILE)