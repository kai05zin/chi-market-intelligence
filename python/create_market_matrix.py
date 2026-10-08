import pandas as pd
from pathlib import Path


# =========================
# Paths
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data/processed/market_analysis.csv"
OUTPUT_DIR = BASE_DIR / "data/processed"
OUTPUT_FILE = OUTPUT_DIR / "market_opportunity_matrix.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# Load data
# =========================

df = pd.read_csv(INPUT_FILE)

print("Loaded market analysis")
print(f"Rows: {len(df)}")


# =========================
# Market qualification
# =========================

MIN_POPULATION = 30000
MIN_MEDIAN_INCOME = 60000

df = df[
    (df["population"] >= MIN_POPULATION)
    & (df["median_income"] >= MIN_MEDIAN_INCOME)
].copy()

print(f"Qualified markets: {len(df)}")


# =========================
# Calculate percentiles
# =========================

df["population_percentile"] = (
    df["population"].rank(pct=True) * 100
)

df["income_percentile"] = (
    df["median_income"].rank(pct=True) * 100
)

df["competition_percentile"] = (
    df["restaurant_density"]
    .rank(pct=True, ascending=False)
    * 100
)


# =========================
# Market classification
# =========================

def classify_market(row):

    high_income = row["income_percentile"] >= 60
    low_competition = row["competition_percentile"] >= 60
    large_population = row["population_percentile"] >= 60

    if high_income and low_competition:
        return "High Opportunity"

    if large_population and low_competition:
        return "Large Market"

    if high_income and not low_competition:
        return "Competitive Market"

    return "Emerging Market"


df["market_segment"] = df.apply(
    classify_market,
    axis=1
)


# =========================
# Create opportunity score
# =========================

df["market_score"] = (
    df["population_percentile"] * 0.30
    + df["income_percentile"] * 0.30
    + df["competition_percentile"] * 0.40
)


# =========================
# Rank
# =========================

df = df.sort_values(
    "market_score",
    ascending=False
).reset_index(drop=True)

df["market_rank"] = df.index + 1


# =========================
# Select columns
# =========================

result = df[
    [
        "market_rank",
        "community_area",
        "community_area_name",
        "market_segment",

        "market_score",

        "population",
        "population_percentile",

        "median_income",
        "income_percentile",

        "restaurant_businesses",
        "restaurant_density",
        "competition_percentile",

        "transit_share",
    ]
]


# =========================
# Save
# =========================

result.to_csv(
    OUTPUT_FILE,
    index=False
)


# =========================
# Print summary
# =========================

print()
print("=== MARKET OPPORTUNITY MATRIX ===")

print(
    result[
        [
            "market_rank",
            "community_area_name",
            "market_segment",
            "market_score",
            "population",
            "median_income",
            "restaurant_density",
        ]
    ].head(20).to_string(index=False)
)


print()
print("=== MARKET SEGMENTS ===")

print(
    result["market_segment"]
    .value_counts()
    .to_string()
)

print()
print("Saved to:")
print(OUTPUT_FILE)