from pathlib import Path
import pandas as pd


# Project folders
PROJECT_DIR = Path(r"D:\Celebal Internship\Project - Indian Startup Funding")
DATASET_DIR = PROJECT_DIR / "Dataset"


# Find CSV file
csv_files = list(DATASET_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(
        f"No CSV file found inside: {DATASET_DIR}"
    )

dataset_file = csv_files[0]

print("=" * 60)
print("INDIAN STARTUP FUNDING DATASET")
print("=" * 60)

print(f"\nDataset file: {dataset_file.name}")


# Load CSV
df = pd.read_csv(dataset_file)


# Dataset size
print("\n--- Dataset Shape ---")
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")


# Column names
print("\n--- Column Names ---")

for column in df.columns:
    print(f"- {column}")


# First 5 rows
print("\n--- First 5 Records ---")
print(df.head())


# Data types
print("\n--- Data Types ---")
print(df.dtypes)


# Missing values
print("\n--- Missing Values ---")
print(df.isnull().sum())


# Duplicate records
print("\n--- Duplicate Records ---")
print(f"Duplicate rows: {df.duplicated().sum()}")


# Basic statistics
print("\n--- Numerical Statistics ---")
print(df.describe())


print("\n" + "=" * 60)
print("DATASET INSPECTION COMPLETED")
print("=" * 60)

# Unique values in important categorical columns
columns_to_check = [
    "Industry",
    "SubVertical",
    "City",
    "InvestmentType"
]

print("\n--- Unique Value Analysis ---")

for column in columns_to_check:
    print(f"\n{column}")
    print("-" * len(column))

    unique_values = df[column].dropna().unique()

    print(f"Number of unique values: {len(unique_values)}")

    for value in unique_values:
        print(f"- {value}")


# Date analysis
print("\n--- Date Analysis ---")

date_values = pd.to_datetime(
    df["Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

print(f"Invalid dates: {date_values.isna().sum()}")
print(f"Earliest date: {date_values.min()}")
print(f"Latest date: {date_values.max()}")

print("\nRecords by year:")
print(date_values.dt.year.value_counts().sort_index())


# Investment amount analysis
print("\n--- Investment Amount Analysis ---")

amount_column = "InvestmentAmount_USD"

print(f"Zero amounts: {(df[amount_column] == 0).sum()}")
print(f"Negative amounts: {(df[amount_column] < 0).sum()}")
print(f"Minimum amount: ${df[amount_column].min():,.2f}")
print(f"Maximum amount: ${df[amount_column].max():,.2f}")
print(f"Mean amount: ${df[amount_column].mean():,.2f}")
print(f"Median amount: ${df[amount_column].median():,.2f}")

# Investor analysis
print("\n--- Investor Analysis ---")

investor_values = df["Investors"].dropna()

print(f"Total investor records: {len(investor_values)}")

print(
    f"Records containing multiple investors: "
    f"{investor_values.str.contains(",").sum()}"
)

print("\nSample investor records:")

for value in investor_values.head(20):
    print(f"- {value}")