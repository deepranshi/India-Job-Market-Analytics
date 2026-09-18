# Job Market Skills Demand & Skill Gap Dashboard

## Project Overview

This project analyzes Data Analyst job postings to identify in-demand skills, salary patterns, job locations, experience levels, and job titles. It also includes a Skill Gap Analyzer that helps identify missing skills based on job-market demand.

## Project Objective

The main objectives of this project are:

- Analyze Data Analyst job postings using real-world job-market data.
- Identify the most in-demand skills for Data Analyst roles.
- Analyze salary patterns across job postings.
- Understand the geographical distribution of Data Analyst jobs.
- Analyze the experience levels required by employers.
- Identify commonly occurring Data Analyst job titles.
- Develop a Skill Gap Analyzer to identify skills that a candidate may need to develop based on job-market demand.

## Technologies Used

- **Python** – Data processing and analysis
- **Pandas** – Data cleaning and manipulation
- **NumPy** – Numerical operations
- **Matplotlib & Seaborn** – Data visualization
- **PostgreSQL** – Database storage and SQL analysis
- **SQLAlchemy** – Database connection between Python and PostgreSQL
- **Streamlit** – Interactive dashboard development
- **OpenPyXL** – Reading Excel dataset files

## Dataset

The project uses an Indian job-market dataset containing job postings and related information.

The dataset includes information such as:

- Job title
- Job ID
- Company name
- Job location
- Required skills and tags
- Salary range
- Required experience
- Job description
- Company rating and review count

### Dataset Size

- Original records: 97,929
- Duplicate records removed: 247
- Cleaned records: 97,682
- Records loaded into PostgreSQL: 97,679

## Project Workflow

The project follows these major steps:

1. Collect and load the job-market dataset.
2. Clean the raw dataset using Python and Pandas.
3. Remove duplicate job postings and handle invalid data.
4. Store the cleaned data in PostgreSQL.
5. Use SQL queries to analyze Data Analyst job postings.
6. Identify in-demand skills from job tags and skills.
7. Analyze salary, location, experience level, and job-title trends.
8. Develop the Skill Gap Analyzer based on skill demand.
9. Build an interactive dashboard using Streamlit.
10. Present the results through tables, charts, and key insights.

## Key Features

### 1. Data Analyst Skill Demand Analysis
Identifies the skills most frequently required in Data Analyst job postings.

### 2. Skill Gap Analyzer
Allows users to select the skills they already know and identifies missing skills based on job-market demand.

### 3. Location Analysis
Shows the locations with the highest number of Data Analyst job postings and allows users to filter the analysis by location.

### 4. Salary Analysis
Provides average minimum and maximum salary information along with the lowest and highest salary values from valid job postings.

### 5. Experience Level Analysis
Analyzes Data Analyst job postings according to required experience levels such as Fresher, Junior, Mid-Level, and Experienced.

### 6. Job Title Analysis
Identifies frequently occurring Data Analyst job titles in the analyzed postings.

### 7. Interactive Dashboard
Provides interactive tables, charts, filters, metrics, and key insights using Streamlit.

## Project Structure

```text
Job-Market-Skills-Analytics/
│
├── data/
│   ├── raw/
│   │   └── indian-job-market-dataset-2025.xlsx
│   └── processed/
│       └── jobs_cleaned.csv
│
├── src/
│   └── data_cleaning.py
│
├── sql/
│   └── SQL analysis scripts
│
├── dashboard/
│   └── app.py
│
└── README.md

## How to Run the Project

### 1. Open the Project

Open the project folder in Visual Studio Code.

### 2. Create a Virtual Environment

Open the VS Code terminal and run:

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

On Windows PowerShell, run:

```bash
venv\Scripts\Activate.ps1
```

### 4. Install Required Packages

Install the Python libraries required for the project:

```bash
pip install pandas numpy matplotlib seaborn openpyxl sqlalchemy psycopg2-binary streamlit
```

### 5. Set Up PostgreSQL

Create a PostgreSQL database named:

```text
job_market_analytics
```

The cleaned job-market data should be stored in the `jobs` table.

### 6. Run the Streamlit Dashboard

From the project folder, run:

```bash
streamlit run dashboard/app.py
```

The Streamlit dashboard will open in the web browser.

### 7. Use the Dashboard

Use the location filter and Skill Gap Analyzer to explore:

* Data Analyst skill demand
* Salary information
* Job locations
* Experience levels
* Job titles
* Skill gaps and recommended skills
























