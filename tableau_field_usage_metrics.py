"""feat: automate Tableau workbook download, metadata extraction, and cleanup

- Added Tableau Server REST API integration to sign in and list workbooks
- Implemented automatic download of .twbx files from Tableau Server
- Extracted .twb files and parsed metadata (views, datasources, fields, calculations)
- Combined results into a single CSV report for auditing
- Added cleanup routine to delete local .twbx and extracted files after processing
- Extended support for batch processing of multiple workbooks in one run"""
import requests
import zipfile
import os
import pandas as pd
from tableaudocumentapi import Workbook

# Tableau Server details
TABLEAU_SERVER = "https://your-tableau-server.com"
USERNAME = "your-username"
PASSWORD = "your-password"
SITE = ""  # empty string for default site

# --- Authentication ---
def tableau_signin():
    auth_url = f"{TABLEAU_SERVER}/api/3.18/auth/signin"
    auth_payload = {
        "credentials": {
            "name": USERNAME,
            "password": PASSWORD,
            "site": {"contentUrl": SITE}
        }
    }
    resp = requests.post(auth_url, json=auth_payload)
    resp.raise_for_status()
    token = resp.json()["credentials"]["token"]
    site_id = resp.json()["credentials"]["site"]["id"]
    return token, site_id

# --- Download workbook ---
def download_workbook(workbook_id, token, site_id, save_dir="downloads"):
    os.makedirs(save_dir, exist_ok=True)
    url = f"{TABLEAU_SERVER}/api/3.18/sites/{site_id}/workbooks/{workbook_id}/content"
    headers = {"X-Tableau-Auth": token}
    resp = requests.get(url, headers=headers, stream=True)
    resp.raise_for_status()

    file_path = os.path.join(save_dir, f"{workbook_id}.twbx")
    with open(file_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    return file_path

# --- Unzip twbx ---
def unzip_twbx(twbx_path, extract_dir="extracted_workbook"):
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(twbx_path, 'r') as z:
        z.extractall(extract_dir)

    twb_files = []
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file.endswith(".twb"):
                twb_files.append(os.path.join(root, file))

    if not twb_files:
        raise FileNotFoundError("No .twb file found inside the .twbx package")

    return twb_files

# --- Collect metadata ---
def collect_metadata(workbook_path):
    wb = Workbook(workbook_path)
    workbook_name = os.path.basename(workbook_path)
    records = []
    for ws in wb.worksheets:
        view_name = ws.name
        ds_name = ws.datasource.name if ws.datasource else "No Data Source"
        used_fields = set(ws.fields)
        if ws.datasource:
            for field in ws.datasource.fields.values():
                records.append({
                    "Workbook Name": workbook_name,
                    "View Name": view_name,
                    "Data Source Name": ds_name,
                    "Field Name": field.name,
                    "Field Used in View": "Yes" if field.name in used_fields else "No",
                    "Is Calculated Field": "Yes" if field.calculation is not None else "No",
                    "Calculation Formula": field.calculation if field.calculation else ""
                })
    return pd.DataFrame(records)

# --- Cleanup ---
def cleanup_files(*paths):
    for path in paths:
        if os.path.isfile(path):
            os.remove(path)
            print(f"Deleted file: {path}")
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for d in dirs:
                    os.rmdir(os.path.join(root, d))
            os.rmdir(path)
            print(f"Deleted directory: {path}")

# --- Main ---
if __name__ == "__main__":
    token, site_id = tableau_signin()

    # List workbooks
    list_url = f"{TABLEAU_SERVER}/api/3.18/sites/{site_id}/workbooks"
    headers = {"X-Tableau-Auth": token}
    resp = requests.get(list_url, headers=headers).json()

    all_records = []
    for wb in resp["workbooks"]["workbook"]:
        workbook_id = wb["id"]
        workbook_name = wb["name"]

        print(f"Processing workbook: {workbook_name}")
        twbx_path = download_workbook(workbook_id, token, site_id)
        twb_files = unzip_twbx(twbx_path)

        for twb in twb_files:
            df = collect_metadata(twb)
            all_records.append(df)

        # Cleanup downloaded twbx and extracted folder
        cleanup_files(twbx_path, "extracted_workbook")

    # Combine all workbook metadata
    if all_records:
        final_df = pd.concat(all_records, ignore_index=True)
        final_df.to_csv("tableau_server_metadata.csv", index=False)
        print("Metadata exported to tableau_server_metadata.csv")
