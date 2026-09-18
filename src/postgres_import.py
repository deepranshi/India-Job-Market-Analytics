import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

# -----------------------------
# 1. Project paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = BASE_DIR / "data" / "processed" / "jobs_cleaned.csv"


# -----------------------------
# 2. PostgreSQL connection
# -----------------------------

DATABASE_URL = "postgresql+psycopg2://postgres:Postgres123@localhost:5432/job_market_analytics"

engine = create_engine(DATABASE_URL)


# -----------------------------
# 3. Load cleaned CSV
# -----------------------------

print("Loading cleaned dataset...")

df = pd.read_csv(CSV_FILE)

print(f"Rows loaded: {len(df)}")


# -----------------------------
# 4. Rename columns
# -----------------------------

df = df.rename(columns={
    "jobId": "job_id",
    "jobUploaded": "job_uploaded",
    "companyName": "company_name",
    "tagsAndSkills": "tags_and_skills",
    "companyId": "company_id",
    "ReviewsCount": "reviews_count",
    "AggregateRating": "aggregate_rating",
    "jobDescription": "job_description",
    "minimumSalary": "minimum_salary",
    "maximumSalary": "maximum_salary",
    "minimumExperience": "minimum_experience",
    "maximumExperience": "maximum_experience"
})
# Remove duplicate job IDs

duplicate_job_ids = df["job_id"].duplicated().sum()

print(f"Duplicate job IDs found: {duplicate_job_ids}")

df = df.drop_duplicates(
    subset="job_id",
    keep="first"
)

print(f"Rows after removing duplicate job IDs: {len(df)}")

# -----------------------------
# 5. Import into PostgreSQL
# -----------------------------

print("Importing data into PostgreSQL...")

df.to_sql(
    "jobs",
    engine,
    if_exists="append",
    index=False,
    chunksize=5000
)

print("✅ Data imported successfully!")