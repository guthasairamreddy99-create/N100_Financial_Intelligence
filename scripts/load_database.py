import os
import sqlite3
import pandas as pd

RAW_DATA_PATH = "data/raw"
DATABASE = "nifty100.db"

excel_files = {
    "analysis.xlsx": "analysis",
    "balancesheet.xlsx": "balancesheet",
    "cashflow.xlsx": "cashflow",
    "companies.xlsx": "companies",
    "documents.xlsx": "documents",
    "market_cap.xlsx": "market_cap",
    "peer_groups.xlsx": "peer_groups",
    "profitandloss.xlsx": "profitandloss",
    "prosandcons.xlsx": "prosandcons",
    "sectors.xlsx": "sectors",
    "stock_prices.xlsx": "stock_prices",
}

# Correct header row for each Excel file
header_map = {
    "analysis.xlsx": 1,
    "balancesheet.xlsx": 1,
    "cashflow.xlsx": 1,
    "companies.xlsx": 1,
    "documents.xlsx": 1,
    "market_cap.xlsx": 0,
    "peer_groups.xlsx": 1,
    "profitandloss.xlsx": 1,
    "prosandcons.xlsx": 1,
    "sectors.xlsx": 0,
    "stock_prices.xlsx": 1,
}

conn = sqlite3.connect(DATABASE)

print("=" * 60)
print("Loading Excel Files into SQLite")
print("=" * 60)

for file, table in excel_files.items():

    path = os.path.join(RAW_DATA_PATH, file)

    try:
        header = header_map[file]

        df = pd.read_excel(
            path,
            engine="openpyxl",
            header=header
        )

        df.to_sql(
            table,
            conn,
            if_exists="replace",
            index=False
        )

        print(f"✓ {table} ({len(df)} rows)")

    except Exception as e:
        print(f"✗ {table}")
        print(e)

conn.close()

print("=" * 60)
print("Database Loading Completed")
print("=" * 60)