from pathlib import Path
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(
    r"D:\Celebal Internship\Project - Indian Startup Funding"
)

BRONZE_FILE = (
    PROJECT_DIR
    / "bronze"
    / "raw"
    / "indian_startup_funding_2020_2025_sample.csv"
)

SILVER_DIR = PROJECT_DIR / "silver"

SILVER_FILE = (
    SILVER_DIR
    / "startup_funding_silver.csv"
)


# ============================================================
# 2. CREATE SILVER DIRECTORY
# ============================================================

SILVER_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 3. READ BRONZE DATA
# ============================================================

print("=" * 70)
print("SILVER LAYER TRANSFORMATION")
print("=" * 70)

print("\nReading Bronze data...")
print(f"Source: {BRONZE_FILE}")

df = pd.read_csv(BRONZE_FILE)

print(f"Bronze rows: {len(df)}")


# ============================================================
# 4. STANDARDIZE COLUMN NAMES
# ============================================================

df.columns = df.columns.str.strip()


# ============================================================
# 5. REMOVE EXTRA WHITESPACE FROM TEXT COLUMNS
# ============================================================

text_columns = [
    "Startup",
    "Industry",
    "SubVertical",
    "City",
    "Investors",
    "InvestmentType"
]

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()


# ============================================================
# 6. HANDLE NULL VALUES
# ============================================================

print("\nChecking missing values...")

missing_before = df.isnull().sum().sum()

print(f"Missing values before cleaning: {missing_before}")

# Remove rows where critical business fields are missing.
critical_columns = [
    "Startup",
    "Industry",
    "City",
    "InvestmentType",
    "InvestmentAmount_USD",
    "Date"
]

df = df.dropna(subset=critical_columns)

print(f"Rows after null handling: {len(df)}")


# ============================================================
# 7. STANDARDIZE CITY NAMES
# ============================================================

city_mapping = {
    "Bangalore": "Bengaluru",
    "bangalore": "Bengaluru",
    "BENGALURU": "Bengaluru",
    "Delhi NCR": "Delhi",
    "New Delhi": "Delhi"
}

df["City"] = df["City"].replace(city_mapping)


# ============================================================
# 8. STANDARDIZE INVESTMENT AMOUNT
# ============================================================

df["InvestmentAmount_USD"] = pd.to_numeric(
    df["InvestmentAmount_USD"],
    errors="coerce"
)


# ============================================================
# 9. PARSE DATE
# ============================================================

df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d-%m-%Y",
    errors="coerce"
)


# ============================================================
# 10. REMOVE INVALID RECORDS
# ============================================================

df = df.dropna(
    subset=[
        "InvestmentAmount_USD",
        "Date"
    ]
)


# ============================================================
# 11. REMOVE INVALID INVESTMENT AMOUNTS
# ============================================================

df = df[
    df["InvestmentAmount_USD"] > 0
]


# ============================================================
# 12. REMOVE DUPLICATES
# ============================================================

print("\nChecking duplicates...")

duplicates_before = df.duplicated().sum()

print(f"Duplicate rows before removal: {duplicates_before}")

df = df.drop_duplicates()

print(f"Rows after duplicate removal: {len(df)}")


# ============================================================
# 13. CREATE YEAR COLUMN
# ============================================================

df["Year"] = df["Date"].dt.year


# ============================================================
# 14. FINAL COLUMN ORDER
# ============================================================

df = df[
    [
        "Startup",
        "Industry",
        "SubVertical",
        "City",
        "Investors",
        "InvestmentType",
        "InvestmentAmount_USD",
        "Date",
        "Year"
    ]
]


# ============================================================
# 15. FINAL DATA QUALITY CHECKS
# ============================================================

print("\n--- FINAL SILVER DATA QUALITY CHECK ---")

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print(
    f"Missing values: {df.isnull().sum().sum()}"
)

print(
    f"Duplicate rows: {df.duplicated().sum()}"
)

print(
    f"Invalid investment amounts: "
    f"{(df['InvestmentAmount_USD'] <= 0).sum()}"
)

print(
    f"Invalid dates: "
    f"{df['Date'].isna().sum()}"
)


# ============================================================
# 16. SAVE SILVER DATA
# ============================================================

df.to_csv(
    SILVER_FILE,
    index=False
)

print("\nSilver data written successfully.")

print(f"Output: {SILVER_FILE}")


# ============================================================
# 17. DISPLAY SAMPLE
# ============================================================

print("\n--- SILVER SAMPLE ---")

print(df.head())


# ============================================================
# 18. COMPLETION MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("SILVER LAYER TRANSFORMATION COMPLETED")
print("=" * 70)