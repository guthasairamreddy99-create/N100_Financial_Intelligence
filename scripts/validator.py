import os
import pandas as pd

RAW_DATA_PATH = "data/raw"

excel_files = [
    "analysis.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "companies.xlsx",
    "documents.xlsx",
    "financial_ratios.xlsx",
    "market_cap.xlsx",
    "peer_groups.xlsx",
    "profitandloss.xlsx",
    "prosandcons.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx",
]


print("=" * 60)
print("Data Quality Validation")
print("=" * 60)

report = []

for file in excel_files:
    path = os.path.join(RAW_DATA_PATH, file)

    try:
        df = pd.read_excel(path, engine="openpyxl")

        report.append({
            "File": file,
            "Rows": len(df),
            "Columns": len(df.columns),
            "Missing Values": int(df.isnull().sum().sum()),
            "Duplicate Rows": int(df.duplicated().sum())
        })

        print(f"✓ {file}")

    except Exception as e:
        print(f"✗ {file}")
        print(e)

report_df = pd.DataFrame(report)

os.makedirs("outputs", exist_ok=True)
report_df.to_csv("outputs/validation_report.csv", index=False)

print("=" * 60)
print("Validation Report Saved")
print("outputs/validation_report.csv")
print("=" * 60)