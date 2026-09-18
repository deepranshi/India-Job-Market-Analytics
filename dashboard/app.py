import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

st.title("📊 Job Market Skills Demand & Skill Gap Dashboard")
st.write(
    "Analyze Data Analyst job-market trends, in-demand skills, "
    "salary patterns, locations, experience levels, and skill gaps."
)
st.info(
    "This dashboard analyzes Data Analyst job postings to identify "
    "in-demand skills, salary trends, job locations, experience levels, "
    "and the skills that can help reduce a candidate's skill gap."
)
st.caption(
    "📌 Use the filters and Skill Gap Analyzer to explore the Data Analyst "
    "job market and identify skills worth developing."
)

st.divider()

st.subheader("🎯 Select Target Role")

target_role = st.selectbox(
    "Choose the role you want to analyze:",
    ["Data Analyst"]
)

st.write("Selected Role:", target_role)

# PostgreSQL connection
# DATABASE_URL = "postgresql+psycopg2://postgres:Postgres123@localhost:5432/job_market_analytics"

# engine = create_engine(DATABASE_URL)
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

st.sidebar.title("🎛️ Dashboard Filters")
st.sidebar.caption("Customize your analysis")

location_filter_query = """
SELECT DISTINCT TRIM(location) AS location
FROM jobs
WHERE location IS NOT NULL
  AND TRIM(location) <> ''
ORDER BY location;
"""

location_filter_df = pd.read_sql(location_filter_query, engine)

selected_location = st.sidebar.selectbox(
    "Select Location",
    ["All"] + location_filter_df["location"].tolist()
)

# Load skill demand data

if selected_location == "All":

    query = """
    SELECT
        normalized_skill,
        job_count,
        demand_percentage
    FROM data_analyst_skill_demand
    ORDER BY demand_percentage DESC;
    """

    df = pd.read_sql(query, engine)

else:

    safe_location = selected_location.replace("'", "''")

    query = f"""
    WITH skill_counts AS (

        SELECT
            CASE
                WHEN lower(trim(skill.skill)) IN ('bi', 'business intelligence')
                    THEN 'business intelligence'
                WHEN lower(trim(skill.skill)) IN ('advanced excel', 'excel')
                    THEN 'excel'
                ELSE lower(trim(skill.skill))
            END AS normalized_skill,

            COUNT(DISTINCT jobs.job_id) AS job_count

        FROM jobs

        CROSS JOIN LATERAL unnest(
            string_to_array(jobs.tags_and_skills, ',')
        ) skill(skill)

        WHERE POSITION('data analyst' IN lower(jobs.title)) > 0
          AND POSITION(lower('{safe_location}') IN lower(jobs.location)) > 0
          AND jobs.tags_and_skills IS NOT NULL
          AND TRIM(skill.skill) <> ''

          AND lower(trim(skill.skill)) IN (
              'sql',
              'python',
              'power bi',
              'tableau',
              'excel',
              'advanced excel',
              'data visualization',
              'business intelligence',
              'bi',
              'data analytics'
          )

        GROUP BY normalized_skill
    )

    SELECT
        normalized_skill,
        job_count,
        ROUND(
            job_count * 100.0 /
            NULLIF(SUM(job_count) OVER (), 0),
            2
        ) AS demand_percentage

    FROM skill_counts

    ORDER BY demand_percentage DESC;
    """

    with engine.connect() as connection:
        result = connection.exec_driver_sql(query)

        df = pd.DataFrame(
            result.fetchall(),
            columns=result.keys()
        )
 

st.divider()    
st.subheader("Data Analyst Skill Demand")
if selected_location != "All":
    st.info(f"Showing analysis for: {selected_location}")
    safe_location = selected_location.replace("'", "''")    

    location_skill_query = f"""
    SELECT
        CASE
            WHEN lower(trim(skill.skill)) IN ('bi', 'business intelligence')
                THEN 'business intelligence'
            WHEN lower(trim(skill.skill)) IN ('advanced excel', 'excel')
                THEN 'excel'
            ELSE lower(trim(skill.skill))
        END AS normalized_skill,
        COUNT(DISTINCT jobs.job_id) AS job_count
    FROM jobs
    CROSS JOIN LATERAL unnest(
        string_to_array(jobs.tags_and_skills, ',')
    ) skill(skill)
    WHERE POSITION('data analyst' IN lower(jobs.title)) > 0
       AND POSITION(lower('{safe_location}') IN lower(jobs.location)) > 0
       AND jobs.tags_and_skills IS NOT NULL
      AND trim(skill.skill) <> ''
      AND lower(trim(skill.skill)) IN (
          'sql',
          'python',
          'power bi',
          'tableau',
          'excel',
          'advanced excel',
          'data visualization',
          'business intelligence',
          'bi',
          'data analytics'
      )
    GROUP BY normalized_skill
    ORDER BY job_count DESC;
    """

    with engine.connect() as connection:
        result = connection.exec_driver_sql(location_skill_query)

        location_skill_df = pd.DataFrame(
           result.fetchall(),
           columns=result.keys()
        )

if selected_location == "All":

    total_jobs_query = """
    SELECT COUNT(*)
    FROM jobs
    WHERE POSITION('data analyst' IN lower(title)) > 0;
    """

else:

    safe_location = selected_location.replace("'", "''")

    total_jobs_query = f"""
    SELECT COUNT(*)
    FROM jobs
    WHERE POSITION('data analyst' IN lower(title)) > 0
      AND POSITION(lower('{safe_location}') IN lower(location)) > 0;
    """

total_jobs = pd.read_sql(
    total_jobs_query,
    engine
).iloc[0, 0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "📌 Total Job Postings",
    f"{total_jobs:,}"
)

col2.metric(
    "🛠️ Skills Analyzed",
    f"{len(df):,}"
)

col3.metric(
    "📍 Selected Location",
    selected_location
)

st.caption(
    "Source: Indian job-market dataset 2025 | "
    "Analysis based on available job postings."
)

# st.dataframe(df)
display_df = df.rename(columns={
    "normalized_skill": "Skill",
    "job_count": "Job Count",
    "demand_percentage": "Demand (%)"
})

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Demand (%)": st.column_config.NumberColumn(
            "Demand (%)",
            format="%.2f%%"
        )
    }
)

st.subheader("📈 Skill Demand Visualization")
chart_df = display_df.set_index("Skill")["Job Count"]
st.bar_chart(chart_df)

st.divider()
st.subheader("Skill Gap Analyzer")
st.caption(
    "Select the skills you already know. The analyzer will identify "
    "missing skills based on their demand in Data Analyst job postings."
)
# User selects their skills
all_skills = sorted(df["normalized_skill"].unique())

user_skills = st.multiselect(
    "💼 Select the skills you already have:",
    all_skills,
    placeholder="Choose your skills..."
)

if user_skills:
    # Available skills
    available = df[df["normalized_skill"].isin(user_skills)]

    # Missing skills
    missing = df[~df["normalized_skill"].isin(user_skills)]

    missing = missing.copy()

    missing["priority"] = missing["demand_percentage"].apply(
        lambda x: "High" if x >= 25
        else "Medium" if x >= 15
        else "Low"
    )
    missing["priority_display"] = missing["priority"].map({
    "High": "🔴 High",
    "Medium": "🟡 Medium",
    "Low": "🟢 Low"
    })

    priority_order = {"High": 1, "Medium": 2, "Low": 3}

    missing["priority_order"] = missing["priority"].map(priority_order)

    missing = missing.sort_values(
    by=["priority_order", "demand_percentage"],
    ascending=[True, False])
    missing = missing.drop(columns=["priority_order"])

    recommended = missing[
    missing["priority"].isin(["High", "Medium"])
    ]
    recommended = recommended.sort_values(
        by="demand_percentage",
        ascending=False
    )

    st.subheader("🚀 Recommended Skills")

    st.caption(
    "Priority is based on skill demand: "
    "High ≥ 25%, Medium = 15–24.99%, Low < 15%."
    )
    

    recommended_display = recommended[["normalized_skill", "job_count", "demand_percentage", "priority_display"]].rename(columns={
       "normalized_skill": "Skill",
        "job_count": "Job Count",
        "demand_percentage": "Demand (%)",
        "priority_display": "Priority"
    })
    recommended_display["Why Learn?"] =recommended_display["Skill"].map({
    "sql": "Used for querying and analyzing data",
    "python": "Useful for data analysis and automation",
    "power bi": "Important for dashboards and reporting",
    "tableau": "Useful for data visualization",
    "excel": "Commonly used for analysis and reporting",
    "data analytics": "Core skill for analyzing business data",
    "business intelligence": "Helps convert data into business insights",
    "data visualization": "Helps present insights clearly"
    })
   
    st.dataframe(
        recommended_display, 
        use_container_width=True,
        hide_index=True,
        column_config={
            "Demand (%)": st.column_config.NumberColumn(
               "Demand (%)",
                format="%.2f%%"
            )
        }
    )
    st.subheader("📊 Recommended Skills Demand")

    skill_chart = recommended_display.set_index("Skill")["Demand (%)"]
    st.bar_chart(skill_chart)

    if not recommended.empty:
       top_skill = recommended.iloc[0]

       st.success(
           f"Recommended skill to learn first: "
           f"{top_skill['normalized_skill'].title()} "
           f"({top_skill['demand_percentage']:.2f}% job demand)"
        )

    total_skills = len(df)
    available_skills = len(available)
    coverage = (available_skills / total_skills) * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Skills", total_skills)
    col2.metric("Your Skills", available_skills)
    col3.metric("Missing Skills", len(missing))
    col4.metric("Skill Coverage", f"{coverage:.2f}%")
    
    st.progress(coverage / 100)

    if coverage >= 75:
        coverage_message = "Strong skill coverage"
    elif coverage >= 50:
        coverage_message = "Good skill coverage"
    elif coverage >= 25:
        coverage_message = "Developing skill coverage"
    else:
        coverage_message = "More skills can be added"
    
    st.caption(
        f"Skill Coverage: {coverage:.2f}% —     {coverage_message}. "
        "Coverage is calculated from the analyzed     skills in the job postings."
    )

    
    st.subheader("💼 Your Current Skills")

    current_skills_display = available[
        ["normalized_skill", "job_count", "demand_percentage"]
    ].rename(columns={
       "normalized_skill": "Skill",
       "job_count": "Job Count",
       "demand_percentage": "Demand (%)"
   })

    st.dataframe(
        current_skills_display,
        use_container_width=True,
        hide_index=True,
        column_config={
           "Demand (%)": st.column_config.NumberColumn(
              "Demand (%)",
              format="%.2f%%"
            )
        }
    ) 

    st.subheader("📌 Missing Skills")

    missing_display = missing[
       ["normalized_skill", "job_count", "demand_percentage", "priority_display"]
    ].rename(columns={
        "normalized_skill": "Skill",
        "job_count": "Job Count",
        "demand_percentage": "Demand (%)",
        "priority_display": "Priority"
    })

    missing_display["Why Learn?"] = missing_display["Skill"].map({
        "sql": "Used for querying and analyzing data",
        "python": "Useful for data analysis and automation",
        "power bi": "Important for dashboards and reporting",
        "tableau": "Useful for data visualization",
        "excel": "Commonly used for analysis and reporting",
        "data analytics": "Core skill for analyzing business data",
       "business intelligence": "Helps convert data into business insights",
       "data visualization": "Helps present insights clearly"
    })

    st.dataframe(
        missing_display,
        use_container_width=True,
        hide_index=True,
        column_config={
           "Demand (%)": st.column_config.NumberColumn(
             "Demand (%)",
             format="%.2f%%"
            )
        }
    )
    st.divider()
    st.subheader("💰 Salary Analysis")
    st.caption(
       "Salary figures are based on Data Analyst job postings with "
       "valid salary ranges and are displayed in LPA."
    )

    if selected_location == "All":

       salary_query = """
        SELECT
            ROUND(AVG(minimum_salary), 2) AS     avg_min_salary,
            ROUND(AVG(maximum_salary), 2) AS     avg_max_salary,
            ROUND(MIN(minimum_salary), 2) AS     lowest_salary,
            ROUND(MAX(maximum_salary), 2) AS     highest_salary
        FROM jobs
        WHERE POSITION('data analyst' IN lower(title)) > 0
          AND minimum_salary > 10000
          AND maximum_salary > 10000
          AND minimum_salary <= maximum_salary
          AND maximum_salary <= 5000000;
        """

    else:

        safe_location = selected_location.replace("'", "''")

        salary_query = f"""
        SELECT
           ROUND(AVG(minimum_salary), 2) AS avg_min_salary,
           ROUND(AVG(maximum_salary), 2) AS avg_max_salary,
           ROUND(MIN(minimum_salary), 2) AS lowest_salary,
           ROUND(MAX(maximum_salary), 2) AS highest_salary
        FROM jobs
        WHERE POSITION('data analyst' IN lower(title)) > 0
          AND POSITION(lower('{safe_location}') IN lower(location)) > 0
           AND minimum_salary > 10000
           AND maximum_salary > 10000
           AND minimum_salary <= maximum_salary
           AND maximum_salary <= 5000000;
        """

    salary_df = pd.read_sql_query(
        salary_query,
        engine
    )

    salary = salary_df.iloc[0]
    salary = salary.apply(pd.to_numeric)

    col1, col2 = st.columns(2)

    col1.metric(
        "Average Minimum Salary",
        f"₹{salary['avg_min_salary'] / 100000:.2f} LPA"
    )

    col2.metric(
        "Average Maximum Salary",
        f"₹{salary['avg_max_salary'] / 100000:.2f} LPA"
    )

    col3, col4 = st.columns(2)

    col3.metric(
      "Lowest Salary",
       f"₹{salary['lowest_salary'] / 100000:.2f} LPA"
    )

    col4.metric(
        "Highest Salary",
        f"₹{salary['highest_salary'] / 100000:.2f} LPA"
    )
    st.subheader("📊 Salary Overview")

    salary_chart_df = pd.DataFrame({
        "Salary Type": [
            "Average Minimum",
            "Average Maximum"
        ],
        "Salary (LPA)": [
            salary["avg_min_salary"] / 100000,
            salary["avg_max_salary"] / 100000
        ]
    })

    st.bar_chart(
        salary_chart_df.set_index("Salary Type")
    )
    st.subheader("📍 Job Locations")

    if selected_location == "All":

        location_query = """
        SELECT
            TRIM(location) AS location,
            COUNT(*) AS job_count
        FROM jobs
        WHERE title IS NOT NULL
          AND POSITION('data analyst' IN lower(title))     > 0
          AND location IS NOT NULL
          AND TRIM(location) <> ''
        GROUP BY TRIM(location)
        ORDER BY job_count DESC
        LIMIT 10;
        """

    else:

        safe_location = selected_location.replace("'",     "''")
    
        location_query = f"""
        SELECT
            TRIM(location) AS location,
            COUNT(*) AS job_count
        FROM jobs
        WHERE title IS NOT NULL
          AND POSITION('data analyst' IN lower(title))     > 0
          AND POSITION(lower('{safe_location}') IN lower    (location)) > 0
          AND location IS NOT NULL
          AND TRIM(location) <> ''
        GROUP BY TRIM(location)
        ORDER BY job_count DESC
        LIMIT 10;
        """

    location_df = pd.read_sql(location_query, engine)

    location_display = location_df.rename(columns={
       "location": "Location",
       "job_count": "Job Count"
    })

    st.dataframe(
        location_display,
        use_container_width=True
    )

    st.subheader("📊 Data Analyst Jobs by Location")

    st.bar_chart(
        location_df.set_index("location")["job_count"],
        horizontal=True
    )
    st.divider()
    st.subheader("💼 Experience Level Demand")

    if selected_location == "All":

        experience_query = """
        SELECT
            CASE
                WHEN minimum_experience <= 1 THEN     'Fresher (0–1 years)'
                WHEN minimum_experience <= 3 THEN     'Junior (1–3 years)'
                WHEN minimum_experience <= 5 THEN     'Mid-Level (3–5 years)'
                ELSE 'Experienced (5+ years)'
            END AS experience_level,
            COUNT(*) AS job_count
        FROM jobs
        WHERE title IS NOT NULL
          AND POSITION('data analyst' IN lower(title))     > 0
          AND minimum_experience IS NOT NULL
          AND minimum_experience >= 0
        GROUP BY 1
        ORDER BY job_count DESC;
        """

    else:

        safe_location = selected_location.replace("'", "''")

        experience_query = f"""
        SELECT
        CASE
            WHEN minimum_experience <= 1 THEN 'Fresher (0–1 years)'
            WHEN minimum_experience <= 3 THEN 'Junior (1–3 years)'
            WHEN minimum_experience <= 5 THEN 'Mid-Level (3–5 years)'
            ELSE 'Experienced (5+ years)'
        END AS experience_level,
        COUNT(*) AS job_count
        FROM jobs
        WHERE title IS NOT NULL
        AND POSITION('data analyst' IN lower(title)) > 0
        AND POSITION(lower('{safe_location}') IN lower(location)) > 0
        AND minimum_experience IS NOT NULL
        AND minimum_experience >= 0
        GROUP BY 1
        ORDER BY job_count DESC;
        """
    

    experience_df = pd.read_sql(experience_query, engine)

    experience_display = experience_df.rename(columns={
        "experience_level": "Experience Level",
        "job_count": "Job Count"
    })

    st.dataframe(
        experience_display,
        use_container_width=True
    )

    st.bar_chart(
        experience_df.set_index("experience_level")["job_count"]
    )
    experience_df["Demand (%)"] = (
    experience_df["job_count"]
    / experience_df["job_count"].sum()
    * 100
    ).round(2)

    st.subheader("📈 Experience Level Distribution")
    experience_share_display = experience_df.rename(columns={
       "experience_level": "Experience Level",
       "job_count": "Job Count",
       "Demand (%)": "Demand (%)"
    })

    st.dataframe(
       experience_share_display,
       use_container_width=True
    )
    st.subheader("📊 Experience Level Distribution (%)")
    st.bar_chart(
        experience_df.set_index("experience_level")["Demand (%)"]
    )
    st.divider()
    st.subheader("👔 Top Data Analyst Job Titles")
    st.caption(
    "Most frequently occurring Data Analyst job titles in the analyzed postings."
    )

    if selected_location == "All":

        job_role_query = """
        SELECT
            TRIM(title) AS job_title,
            COUNT(*) AS job_count,
            ROUND(
                COUNT(*) * 100.0 /
                SUM(COUNT(*)) OVER (),
                2
            ) AS demand_percentage
        FROM jobs
        WHERE title IS NOT NULL
          AND TRIM(title) <> ''
          AND LOWER(TRIM(title)) LIKE '%%data analyst%%'
        GROUP BY TRIM(title)
        ORDER BY job_count DESC
        LIMIT 10;
        """

    else:

        safe_location = selected_location.replace("'", "''")

        job_role_query = f"""
        SELECT
            TRIM(title) AS job_title,
            COUNT(*) AS job_count,
            ROUND(
                COUNT(*) * 100.0 /
                SUM(COUNT(*)) OVER (),
                2
            ) AS demand_percentage
        FROM jobs
        WHERE title IS NOT NULL
          AND TRIM(title) <> ''
          AND LOWER(TRIM(title)) LIKE '%%data analyst%%'
          AND POSITION(lower('{safe_location}') IN lower    (location)) > 0
        GROUP BY TRIM(title)
        ORDER BY job_count DESC
        LIMIT 10;
        """

    job_role_df = pd.read_sql(job_role_query, engine)
    
    job_role_display = job_role_df.rename(columns={
        "job_title": "Job Title",
        "job_count": "Job Count"
    })

    st.dataframe(
        job_role_display,
        use_container_width=True
    )

    st.bar_chart(
        job_role_df.set_index("job_title")["job_count"]
    )
    st.divider()
    st.subheader("💡 Key Insights")
    st.caption(
       "Key findings are generated from the currently selected location "
       "and Data Analyst job-posting data."
    )

    top_skill = df.iloc[0]

    st.info(
        f"🔹 **Most demanded skill:** {top_skill['normalized_skill'].title()} "
        f"with {top_skill['job_count']} job postings "
        f"({top_skill['demand_percentage']:.2f}% demand)."
    )

    if selected_location == "All":
        st.info(
           f"🔹 **Top job market location:** {location_df.iloc[0]['location']} "
           f"has the highest number of Data Analyst postings among the "
           f"top locations shown."
        )
    else:
        st.info(
           f"🔹 **Selected location:** {selected_location} "
           f"has {location_df['job_count'].sum():,} Data Analyst postings "
           f"represented in the location analysis."
        )

    st.info(
        f"🔹 **Most represented experience level:** "
        f"{experience_df.iloc[0]['experience_level']} "
        f"with {experience_df.iloc[0]['job_count']:,} postings."
    )

    st.subheader("Skill Demand in Data Analyst Jobs")

    chart_data = df.set_index("normalized_skill")["demand_percentage"]

    st.bar_chart(chart_data)

else:
    st.info("Please select your current skills.")