import pandas as pd
from pathlib import Path


# =========================
# Paths
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data/processed/market_analysis.csv"
OUTPUT_DIR = BASE_DIR / "data/processed"
OUTPUT_FILE = OUTPUT_DIR / "opportunity_ranking.csv"

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

# Minimum market size and purchasing power.
#
# These thresholds are not a prediction of restaurant success.
# They are used to remove very small / lower-income markets
# from the initial expansion screening.

MIN_POPULATION = 30000
MIN_MEDIAN_INCOME = 60000

qualified = df[
    (df["population"] >= MIN_POPULATION)
    & (df["median_income"] >= MIN_MEDIAN_INCOME)
].copy()


print()
print("=== MARKET QUALIFICATION ===")
print(f"Qualified markets: {len(qualified)}")
print(f"Excluded markets: {len(df) - len(qualified)}")


# =========================
# Percentile scores
# =========================

# Demand
# Larger population = larger potential customer base.
qualified["demand_score"] = (
    qualified["population"].rank(pct=True) * 100
)


# Purchasing power
# Higher median income = stronger purchasing power.
qualified["income_score"] = (
    qualified["median_income"].rank(pct=True) * 100
)


# Competition
# Lower restaurant density = less direct competition.
qualified["competition_score"] = (
    qualified["restaurant_density"]
    .rank(pct=True, ascending=False)
    * 100
)


# Accessibility
# Higher transit share = stronger transit accessibility.
qualified["accessibility_score"] = (
    qualified["transit_share"].rank(pct=True) * 100
)


# =========================
# Opportunity Score
# =========================

qualified["opportunity_score"] = (
    qualified["demand_score"] * 0.30
    + qualified["income_score"] * 0.25
    + qualified["competition_score"] * 0.25
    + qualified["accessibility_score"] * 0.20
)


# =========================
# Rank
# =========================

qualified = qualified.sort_values(
    "opportunity_score",
    ascending=False
).reset_index(drop=True)

qualified["opportunity_rank"] = qualified.index + 1


# =========================
# Market segment
# =========================

def classify_market(row):
    if (
        row["demand_score"] >= 75
        and row["income_score"] >= 75
        and row["competition_score"] >= 75
    ):
        return "High Potential"

    if (
        row["demand_score"] >= 60
        and row["income_score"] >= 60
        and row["competition_score"] >= 60
    ):
        return "Promising"

    return "Moderate"


qualified["market_segment"] = qualified.apply(
    classify_market,
    axis=1
)


# =========================
# Select final columns
# =========================

result = qualified[
    [
        "opportunity_rank",
        "community_area",
        "community_area_name",
        "market_segment",
        "opportunity_score",

        "population",
        "demand_score",

        "restaurant_businesses",
        "restaurant_density",
        "competition_score",

        "median_income",
        "income_score",

        "transit_share",
        "accessibility_score",
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
# Print results
# =========================

print()
print("=== TOP MARKET OPPORTUNITIES ===")

print(
    result.head(20).to_string(index=False)
)

print()
print("Saved to:")
print(OUTPUT_FILE)