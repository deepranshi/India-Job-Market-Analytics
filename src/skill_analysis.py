import pandas as pd
from pathlib import Path

# -----------------------------
# 1. Project paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "jobs_cleaned.csv"


# -----------------------------
# 2. Load dataset
# -----------------------------

print("Loading cleaned dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Dataset loaded: {df.shape}")


# -----------------------------
# 3. Convert skills into lists
# -----------------------------

df["skill_list"] = (
    df["tagsAndSkills"]
    .fillna("")
    .astype(str)
    .str.split(",")
)


# -----------------------------
# 4. Separate individual skills
# -----------------------------

skills = df[["jobId", "skill_list"]].explode("skill_list")


# -----------------------------
# 5. Basic cleaning
# -----------------------------

skills["skill"] = (
    skills["skill_list"]
    .astype(str)
    .str.strip()
    .str.lower()
)


# Remove empty values
skills = skills[
    (skills["skill"] != "") &
    (skills["skill"] != "nan")
]


# -----------------------------
# 6. Normalize common skill names
# -----------------------------

skill_mapping = {

    "powerbi": "power bi",
    "power bi desktop": "power bi",
    "ms power bi": "power bi",

    "ms excel": "excel",
    "microsoft excel": "excel",

    "structured query language": "sql",
    "mysql": "sql",
    "ms sql": "sql",
    "microsoft sql server": "sql",

    "python programming": "python",
    "python 3": "python",

    "machine learning": "machine learning",
    "ml": "machine learning",

    "artificial intelligence": "artificial intelligence",
    "ai": "artificial intelligence",

    "amazon web services": "aws",

    "postgres": "postgresql",
    "postgre sql": "postgresql",

    "js": "javascript",

    "node js": "node.js",
    "nodejs": "node.js",

    "react js": "react",
    "reactjs": "react",

    "c plus plus": "c++",

    "c sharp": "c#",
    "c-sharp": "c#"
}


skills["skill"] = skills["skill"].replace(skill_mapping)


# -----------------------------
# 7. Count skill demand
# -----------------------------

skill_demand = (
    skills["skill"]
    .value_counts()
    .reset_index()
)

skill_demand.columns = [
    "skill",
    "job_count"
]


# -----------------------------
# 8. Display top 30 skills
# -----------------------------

print("\n🔥 TOP 30 NORMALIZED SKILLS:\n")

print(
    skill_demand
    .head(30)
    .to_string(index=False)
)
# -----------------------------
# 9. Save skill demand data
# -----------------------------

OUTPUT_FILE = BASE_DIR / "data" / "processed" / "skill_demand.csv"

skill_demand.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n✅ Skill demand file created!")
print(f"Saved to: {OUTPUT_FILE}")