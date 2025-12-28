import zipfile
import os
import pandas as pd
from tableaudocumentapi import Workbook

def unzip_twbx(twbx_path, extract_dir="extracted_workbook"):
    """
    Unzips a Tableau .twbx file and returns the path to the extracted .twb file.
    """
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(twbx_path, 'r') as z:
        z.extractall(extract_dir)

    # Find the .twb file inside the extracted folder
    twb_file = None
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file.endswith(".twb"):
                twb_file = os.path.join(root, file)
                break

    if not twb_file:
        raise FileNotFoundError("No .twb file found inside the .twbx package")

    return twb_file

def collect_metadata(workbook_path):
    """
    Collects Tableau workbook metadata into a pandas DataFrame,
    including whether each field is used in its view and whether it is calculated.
    """
    wb = Workbook(workbook_path)
    workbook_name = os.path.basename(workbook_path)

    records = []
    for ws in wb.worksheets:
        view_name = ws.name
        ds_name = ws.datasource.name if ws.datasource else "No Data Source"

        # Fields actually used in the worksheet
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

if __name__ == "__main__":
    # Example: handle both .twb and .twbx
    input_path = "example.twbx"  # or "example.twb"

    if input_path.endswith(".twbx"):
        twb_file_path = unzip_twbx(input_path)
    else:
        twb_file_path = input_path

    df = collect_metadata(twb_file_path)

    # Export to CSV
    df.to_csv("tableau_metadata_with_calculations.csv", index=False)
    print("Metadata exported to tableau_metadata_with_calculations.csv")

"""
Example Output
Workbook Name,View Name,Data Source Name,Field Name,Field Used in View,Is Calculated Field,Calculation Formula
Sales_Report.twb,Regional Sales,Sales_DB,Region,Yes,No,
Sales_Report.twb,Regional Sales,Sales_DB,Sales,Yes,No,
Sales_Report.twb,Regional Sales,Sales_DB,Profit Margin,Yes,Yes,[Profit]/[Sales]
"""
