```sql
-- =========================================================
-- Job Market Skills Demand & Skill Gap Dashboard
-- SQL Analysis Queries
-- =========================================================

-- 1. Total Data Analyst Job Postings
SELECT COUNT(*) AS total_data_analyst_jobs
FROM jobs
WHERE POSITION('data analyst' IN LOWER(title)) > 0;


-- 2. Top Data Analyst Job Locations
SELECT
    TRIM(location) AS location,
    COUNT(*) AS job_count
FROM jobs
WHERE title IS NOT NULL
  AND POSITION('data analyst' IN LOWER(title)) > 0
  AND location IS NOT NULL
  AND TRIM(location) <> ''
GROUP BY TRIM(location)
ORDER BY job_count DESC
LIMIT 10;


-- 3. Data Analyst Jobs by Experience Level
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
  AND POSITION('data analyst' IN LOWER(title)) > 0
  AND minimum_experience IS NOT NULL
  AND minimum_experience >= 0
GROUP BY 1
ORDER BY job_count DESC;


-- 4. Top Data Analyst Job Titles
SELECT
    TRIM(title) AS job_title,
    COUNT(*) AS job_count
FROM jobs
WHERE title IS NOT NULL
  AND TRIM(title) <> ''
  AND LOWER(TRIM(title)) LIKE '%data analyst%'
GROUP BY TRIM(title)
ORDER BY job_count DESC
LIMIT 10;


-- 5. Salary Analysis
SELECT
    ROUND(AVG(minimum_salary), 2) AS average_minimum_salary,
    ROUND(AVG(maximum_salary), 2) AS average_maximum_salary,
    ROUND(MIN(minimum_salary), 2) AS lowest_salary,
    ROUND(MAX(maximum_salary), 2) AS highest_salary
FROM jobs
WHERE POSITION('data analyst' IN LOWER(title)) > 0
  AND minimum_salary > 10000
  AND maximum_salary > 10000
  AND minimum_salary <= maximum_salary
  AND maximum_salary <= 5000000;


-- 6. Data Analyst Skill Demand
WITH skill_counts AS (
    SELECT
        CASE
            WHEN LOWER(TRIM(skill.skill)) IN
                 ('bi', 'business intelligence')
                THEN 'business intelligence'

            WHEN LOWER(TRIM(skill.skill)) IN
                 ('advanced excel', 'excel')
                THEN 'excel'

            ELSE LOWER(TRIM(skill.skill))
        END AS normalized_skill,

        COUNT(DISTINCT jobs.job_id) AS job_count

    FROM jobs

    CROSS JOIN LATERAL
        UNNEST(
            STRING_TO_ARRAY(jobs.tags_and_skills, ',')
        ) skill(skill)

    WHERE POSITION('data analyst' IN LOWER(jobs.title)) > 0
      AND jobs.tags_and_skills IS NOT NULL
      AND TRIM(skill.skill) <> ''

      AND LOWER(TRIM(skill.skill)) IN (
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
    normalized_skill AS skill,
    job_count,
    ROUND(
        job_count * 100.0 /
        NULLIF(SUM(job_count) OVER (), 0),
        2
    ) AS demand_percentage
FROM skill_counts
ORDER BY demand_percentage DESC;
```
