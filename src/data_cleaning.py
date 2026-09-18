import pandas as pd
from pathlib import Path

# -----------------------------
# 1. Project paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------
# 2. Load dataset
# -----------------------------

file_path = RAW_DATA_DIR / "indian-job-market-dataset-2025.xlsx"

print("Loading dataset...")

df = pd.read_excel(file_path)

print(f"Original dataset shape: {df.shape}")


# -----------------------------
# 3. Remove duplicate rows
# -----------------------------

duplicate_count = df.duplicated().sum()

print(f"Duplicate rows found: {duplicate_count}")

df = df.drop_duplicates()

print(f"Shape after removing duplicates: {df.shape}")


# -----------------------------
# 4. Clean column names
# -----------------------------

df.columns = df.columns.str.strip()


# -----------------------------
# 5. Remove completely empty rows
# -----------------------------

df = df.dropna(how="all")

print(f"Shape after removing empty rows: {df.shape}")


# -----------------------------
# 6. Clean text columns
# -----------------------------

text_columns = [
    "title",
    "companyName",
    "tagsAndSkills",
    "experience",
    "salary",
    "location",
    "jobDescription"
]

for column in text_columns:

    if column in df.columns:
        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )


# -----------------------------
# 7. Convert numeric columns
# -----------------------------

numeric_columns = [
    "minimumSalary",
    "maximumSalary",
    "minimumExperience",
    "maximumExperience",
    "ReviewsCount",
    "AggregateRating"
]

for column in numeric_columns:

    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# -----------------------------
# 8. Convert job upload date
# -----------------------------

if "jobUploaded" in df.columns:

    df["jobUploaded"] = pd.to_datetime(
        df["jobUploaded"],
        errors="coerce"
    )


# -----------------------------
# 9. Save cleaned dataset
# -----------------------------

output_file = PROCESSED_DATA_DIR / "jobs_cleaned.csv"

df.to_csv(
    output_file,
    index=False
)

print("\n✅ Data cleaning completed!")

print(f"Final dataset shape: {df.shape}")

print(f"Cleaned dataset saved to:")

print(output_file)