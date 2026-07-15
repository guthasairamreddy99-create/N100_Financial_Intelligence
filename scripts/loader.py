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
    "stock_prices.xlsx"
]

loaded = {}

print("=" * 60)
print("Loading Excel Files")
print("=" * 60)

for file in excel_files:
    path = os.path.join(RAW_DATA_PATH, file)

    try:
        df = pd.read_excel(path, engine="openpyxl")
        loaded[file] = df
        print(f"✓ {file} -> {df.shape}")
    except Exception as e:
        print(f"✗ {file}")
        print(e)

print("=" * 60)
print(f"Loaded {len(loaded)} datasets.")