import requests
import pandas as pd
from datetime import datetime, timedelta

# Tableau Server details
TABLEAU_SERVER = "https://your-tableau-server.com"
USERNAME = "your-username"
PASSWORD = "your-password"
SITE = ""  # empty string for default site

# Authenticate
auth_url = f"{TABLEAU_SERVER}/api/3.18/auth/signin"
auth_payload = {
    "credentials": {
        "name": USERNAME,
        "password": PASSWORD,
        "site": {"contentUrl": SITE}
    }
}
auth_resp = requests.post(auth_url, json=auth_payload)
auth_token = auth_resp.json()["credentials"]["token"]
site_id = auth_resp.json()["credentials"]["site"]["id"]

headers = {"X-Tableau-Auth": auth_token}

records = []

# Step 1: Get all data sources
datasources_url = f"{TABLEAU_SERVER}/api/3.18/sites/{site_id}/datasources"
datasources_resp = requests.get(datasources_url, headers=headers).json()

datasource_map = {}
for ds in datasources_resp["datasources"]["datasource"]:
    ds_id = ds["id"]
    ds_name = ds["name"]
    refresh_freq = ds.get("extract", {}).get("refreshSchedule", "N/A")
    datasource_map[ds_id] = {"name": ds_name, "refresh_freq": refresh_freq}

# Step 2: Get all workbooks
workbooks_url = f"{TABLEAU_SERVER}/api/3.18/sites/{site_id}/workbooks"
workbooks_resp = requests.get(workbooks_url, headers=headers).json()

for wb in workbooks_resp["workbooks"]["workbook"]:
    workbook_name = wb["name"]
    workbook_id = wb["id"]
    project_name = wb["project"]["name"]

    # Workbook usage (last viewed date)
    last_viewed = wb.get("lastViewedAt", "N/A")

    # Step 3: Get connections (data sources used by workbook)
    connections_url = f"{TABLEAU_SERVER}/api/3.18/sites/{site_id}/workbooks/{workbook_id}/connections"
    connections_resp = requests.get(connections_url, headers=headers).json()

    for conn in connections_resp.get("connections", {}).get("connection", []):
        ds_id = conn["datasource"]["id"]
        ds_info = datasource_map.get(ds_id, {"name": "Unknown", "refresh_freq": "N/A"})

        # --- Mismatch flag logic ---
        mismatch_flag = "No"
        if last_viewed != "N/A" and ds_info["refresh_freq"] != "N/A":
            try:
                last_viewed_dt = datetime.fromisoformat(last_viewed.replace("Z", "+00:00"))
                days_since_view = (datetime.utcnow() - last_viewed_dt).days

                # Example rule: if datasource refreshes daily but workbook not viewed in >30 days → mismatch
                if "Daily" in ds_info["refresh_freq"] and days_since_view > 30:
                    mismatch_flag = "Yes"
                # If datasource refreshes weekly but workbook not viewed in >90 days → mismatch
                elif "Weekly" in ds_info["refresh_freq"] and days_since_view > 90:
                    mismatch_flag = "Yes"
            except Exception:
                mismatch_flag = "N/A"

        records.append({
            "Project Name": project_name,
            "Workbook Name": workbook_name,
            "Last Viewed": last_viewed,
            "Data Source Name": ds_info["name"],
            "Extract Refresh Frequency": ds_info["refresh_freq"],
            "Mismatch Flag": mismatch_flag
        })

# Step 4: Export to CSV
df = pd.DataFrame(records)
df.to_csv("tableau_datasource_usage_mismatch.csv", index=False)
print("Datasource usage exported to tableau_datasource_usage_mismatch.csv")
