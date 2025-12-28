import requests
import pandas as pd

# Tableau Server details
TABLEAU_SERVER = "https://your-tableau-server.com"
USERNAME = "your-username"
PASSWORD = "your-password"
SITE = ""  # empty string for default site

# Authenticate and get token
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

# Get all workbooks
workbooks_url = f"{TABLEAU_SERVER}/api/3.18/sites/{site_id}/workbooks"
workbooks_resp = requests.get(workbooks_url, headers=headers).json()

records = []

for wb in workbooks_resp["workbooks"]["workbook"]:
    workbook_name = wb["name"]
    workbook_id = wb["id"]
    project_name = wb["project"]["name"]

    # Last published date and publisher
    last_published_date = wb.get("updatedAt", "N/A")
    publisher = wb["owner"]["name"] if "owner" in wb else "N/A"

    # Get views in the workbook
    views_url = f"{TABLEAU_SERVER}/api/3.18/sites/{site_id}/workbooks/{workbook_id}/views"
    views_resp = requests.get(views_url, headers=headers).json()

    for view in views_resp["views"]["view"]:
        view_name = view["name"]
        view_id = view["id"]
        last_accessed = view.get("lastViewedAt", "N/A")

        # Published status
        view_published = "Yes" if view.get("contentUrl") else "No"

        # Get datasources used by workbook
        ds_url = f"{TABLEAU_SERVER}/api/3.18/sites/{site_id}/workbooks/{workbook_id}/connections"
        ds_resp = requests.get(ds_url, headers=headers).json()
        datasources = [conn["datasource"]["name"] for conn in ds_resp.get("connections", {}).get("connection", [])]

        # Get users who viewed this view (row‑wise)
        viewed_by_url = f"{TABLEAU_SERVER}/api/3.18/sites/{site_id}/views/{view_id}/users"
        viewed_by_resp = requests.get(viewed_by_url, headers=headers).json()
        users = viewed_by_resp.get("users", {}).get("user", [])

        if users:
            for user in users:
                records.append({
                    "Project Name": project_name,
                    "Workbook": workbook_name,
                    "View": view_name,
                    "Date Accessed": last_accessed,
                    "Datasources Used": ", ".join(datasources) if datasources else "N/A",
                    "View Published": view_published,
                    "Last Published Date": last_published_date,
                    "Published By": publisher,
                    "Viewed By": user["name"]
                })
        else:
            # No viewers recorded
            records.append({
                "Project Name": project_name,
                "Workbook": workbook_name,
                "View": view_name,
                "Date Accessed": last_accessed,
                "Datasources Used": ", ".join(datasources) if datasources else "N/A",
                "View Published": view_published,
                "Last Published Date": last_published_date,
                "Published By": publisher,
                "Viewed By": "N/A"
            })

# Convert to DataFrame
df = pd.DataFrame(records)

# Export to CSV
df.to_csv("tableau_usage_history_rowwise.csv", index=False)
print("Usage history exported to tableau_usage_history_rowwise.csv")
