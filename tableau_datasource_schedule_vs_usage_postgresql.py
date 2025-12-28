#This way you get a row‑wise audit of datasource refresh schedules vs workbook usage, with mismatches flagged

import psycopg2
import pandas as pd

# Connection details for Tableau Server repository
conn = psycopg2.connect(
    host="your-tableau-server-host",
    port="8060",  # default Tableau repo port
    database="workgroup",
    user="readonly",
    password="your-password"
)

# SQL query: join datasources, workbooks, and usage events
query = """
SELECT
    p.name AS project_name,
    w.name AS workbook_name,
    d.name AS datasource_name,
    d.refresh_schedule AS extract_refresh_frequency,
    he.created_at AS last_viewed,
    u.name AS viewed_by
FROM workbooks w
JOIN projects p ON w.project_id = p.id
JOIN datasources d ON d.workbook_id = w.id
LEFT JOIN historical_events he ON he.workbook_id = w.id
LEFT JOIN users u ON he.user_id = u.id
WHERE he.event_type = 'ViewWorkbook'
ORDER BY project_name, workbook_name, datasource_name, last_viewed;
"""

df = pd.read_sql(query, conn)

# --- Add mismatch flag logic ---
def flag_mismatch(row):
    if row["extract_refresh_frequency"] is None or row["last_viewed"] is None:
        return "N/A"
    # Example rules:
    # Daily refresh but not viewed in >30 days
    if "Daily" in row["extract_refresh_frequency"] and (pd.Timestamp.now() - row["last_viewed"]).days > 30:
        return "Yes"
    # Weekly refresh but not viewed in >90 days
    if "Weekly" in row["extract_refresh_frequency"] and (pd.Timestamp.now() - row["last_viewed"]).days > 90:
        return "Yes"
    return "No"

df["Mismatch_Flag"] = df.apply(flag_mismatch, axis=1)

# Export to CSV
df.to_csv("tableau_datasource_usage_postgres.csv", index=False)
print("Datasource usage exported to tableau_datasource_usage_postgres.csv")

conn.close()
