# Tableau
# Tableau Public URL: https://public.tableau.com/app/discover
Tableau Desktop
# Tableau Workbooks Automation

This repository provides Python scripts and utilities to **automate the extraction and auditing of Tableau workbook metadata**. It helps analysts, developers, and compliance teams quickly inspect Tableau `.twb` and `.twbx` files to understand:

- 📘 Workbook names
- 📊 View (worksheet) names
- 🔗 Data source names
- 🏷️ Field names
- ✅ Whether fields are used in views
- 🧮 Calculated fields and their formulas

---

## 🚀 Features
- Unzip `.twbx` packaged workbooks to access `.twb` files.
- Parse Tableau workbooks using the **Tableau Document API**.
- Collect metadata into a **pandas DataFrame**.
- Export results to **CSV** for reporting and compliance checks.
- Flag fields as **used vs unused** in each view.
- Capture **calculated fields** with their formulas.

---

## 📦 Requirements
- Python 3.8+
- [Tableau Document API](https://github.com/tableau/document-api-python)
- pandas

Install dependencies:
```bash
pip install tableaudocumentapi pandas
