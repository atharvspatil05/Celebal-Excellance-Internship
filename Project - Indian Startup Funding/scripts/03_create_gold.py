from pathlib import Path
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(
    r"D:\Celebal Internship\Project - Indian Startup Funding"
)

SILVER_FILE = (
    PROJECT_DIR
    / "silver"
    / "startup_funding_silver.csv"
)

GOLD_DIR = PROJECT_DIR / "gold"


# ============================================================
# 2. CREATE GOLD DIRECTORY
# ============================================================

GOLD_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 3. READ SILVER DATA
# ============================================================

print("=" * 70)
print("GOLD LAYER ANALYTICS")
print("=" * 70)

print("\nReading Silver data...")

df = pd.read_csv(SILVER_FILE)

print(f"Silver rows: {len(df)}")


# Make sure Date is treated as a date
df["Date"] = pd.to_datetime(df["Date"])

print(f"Silver columns: {len(df.columns)}")


# ============================================================
# GOLD 1 — TOP FUNDED SECTORS
# ============================================================

print("\n" + "=" * 70)
print("1. TOP FUNDED SECTORS")
print("=" * 70)

top_funded_sectors = (
    df.groupby("Industry", as_index=False)
    .agg(
        total_funding_usd=(
            "InvestmentAmount_USD",
            "sum"
        ),
        deal_count=(
            "Startup",
            "count"
        )
    )
    .sort_values(
        "total_funding_usd",
        ascending=False
    )
)

top_funded_sectors["rank"] = (
    top_funded_sectors["total_funding_usd"]
    .rank(
        method="dense",
        ascending=False
    )
    .astype(int)
)

top_funded_sectors = top_funded_sectors[
    [
        "rank",
        "Industry",
        "total_funding_usd",
        "deal_count"
    ]
]

top_funded_sectors.to_csv(
    GOLD_DIR / "top_funded_sectors.csv",
    index=False
)

print("\nTop funded sectors:")
print(top_funded_sectors)


# ============================================================
# GOLD 2 — CITY FUNDING RANK
# ============================================================

print("\n" + "=" * 70)
print("2. CITY FUNDING RANK")
print("=" * 70)

city_funding_rank = (
    df.groupby("City", as_index=False)
    .agg(
        total_funding_usd=(
            "InvestmentAmount_USD",
            "sum"
        ),
        deal_count=(
            "Startup",
            "count"
        )
    )
)

city_funding_rank["rank"] = (
    city_funding_rank["total_funding_usd"]
    .rank(
        method="min",
        ascending=False
    )
    .astype(int)
)

city_funding_rank = (
    city_funding_rank
    .sort_values(
        ["rank", "City"]
    )
)

city_funding_rank = city_funding_rank[
    [
        "rank",
        "City",
        "total_funding_usd",
        "deal_count"
    ]
]

city_funding_rank.to_csv(
    GOLD_DIR / "city_funding_rank.csv",
    index=False
)

print("\nCity funding ranking:")
print(city_funding_rank)


# ============================================================
# GOLD 3 — SECTOR YOY SNAPSHOT
# ============================================================

print("\n" + "=" * 70)
print("3. SECTOR YOY SNAPSHOT")
print("=" * 70)

sector_yoy_snapshot = (
    df.groupby(
        ["Industry", "Year"],
        as_index=False
    )
    .agg(
        total_funding_usd=(
            "InvestmentAmount_USD",
            "sum"
        ),
        deal_count=(
            "Startup",
            "count"
        )
    )
    .sort_values(
        ["Industry", "Year"]
    )
)

# Previous year's funding for each industry
sector_yoy_snapshot["previous_year_funding_usd"] = (
    sector_yoy_snapshot
    .groupby("Industry")["total_funding_usd"]
    .shift(1)
)

# Calculate year-over-year percentage change
sector_yoy_snapshot["yoy_change_percent"] = (
    (
        sector_yoy_snapshot["total_funding_usd"]
        - sector_yoy_snapshot["previous_year_funding_usd"]
    )
    /
    sector_yoy_snapshot["previous_year_funding_usd"]
    * 100
)

# First year of each sector has no previous year
sector_yoy_snapshot["yoy_change_percent"] = (
    sector_yoy_snapshot["yoy_change_percent"]
    .round(2)
)

sector_yoy_snapshot.to_csv(
    GOLD_DIR / "sector_yoy_snapshot.csv",
    index=False
)

print("\nSector year-over-year snapshot:")
print(
    sector_yoy_snapshot.head(30)
)


# ============================================================
# GOLD 4 — INVESTOR DEAL COUNT
# ============================================================

print("\n" + "=" * 70)
print("4. INVESTOR DEAL COUNT")
print("=" * 70)

# Split comma-separated investors into individual investors
investor_data = df[
    [
        "Startup",
        "Date",
        "Investors"
    ]
].copy()

investor_data["Investors"] = (
    investor_data["Investors"]
    .str.split(",")
)

investor_data = investor_data.explode(
    "Investors"
)

# Remove whitespace around investor names
investor_data["Investors"] = (
    investor_data["Investors"]
    .str.strip()
)

investor_deal_count = (
    investor_data
    .groupby(
        "Investors",
        as_index=False
    )
    .agg(
        deal_count=(
            "Startup",
            "count"
        )
    )
    .sort_values(
        "deal_count",
        ascending=False
    )
)

investor_deal_count["rank"] = (
    investor_deal_count["deal_count"]
    .rank(
        method="min",
        ascending=False
    )
    .astype(int)
)

investor_deal_count = investor_deal_count[
    [
        "rank",
        "Investors",
        "deal_count"
    ]
]

investor_deal_count.to_csv(
    GOLD_DIR / "investor_deal_count.csv",
    index=False
)

print("\nTop investors by deal count:")
print(
    investor_deal_count.head(20)
)


# ============================================================
# GOLD 5 — AVERAGE DEAL BY STAGE
# ============================================================

print("\n" + "=" * 70)
print("5. AVERAGE DEAL BY STAGE")
print("=" * 70)

avg_deal_by_stage = (
    df.groupby(
        "InvestmentType",
        as_index=False
    )
    .agg(
        average_deal_usd=(
            "InvestmentAmount_USD",
            "mean"
        ),
        deal_count=(
            "Startup",
            "count"
        )
    )
)

avg_deal_by_stage["average_deal_usd"] = (
    avg_deal_by_stage["average_deal_usd"]
    .round(2)
)

avg_deal_by_stage = (
    avg_deal_by_stage
    .sort_values(
        "average_deal_usd",
        ascending=False
    )
)

avg_deal_by_stage.to_csv(
    GOLD_DIR / "avg_deal_by_stage.csv",
    index=False
)

print("\nAverage deal size by investment type:")
print(avg_deal_by_stage)


# ============================================================
# 6. GOLD OUTPUT SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("GOLD OUTPUT FILES")
print("=" * 70)

gold_files = [
    "top_funded_sectors.csv",
    "city_funding_rank.csv",
    "sector_yoy_snapshot.csv",
    "investor_deal_count.csv",
    "avg_deal_by_stage.csv"
]

for file_name in gold_files:
    file_path = GOLD_DIR / file_name

    print(
        f"{file_name:<30} "
        f"{file_path.stat().st_size:,} bytes"
    )


print("\n" + "=" * 70)
print("GOLD LAYER ANALYTICS COMPLETED")
print("=" * 70)