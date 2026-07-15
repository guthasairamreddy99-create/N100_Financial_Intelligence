import sqlite3
import pandas as pd

DB_NAME = "nifty100.db"

conn = sqlite3.connect(DB_NAME)

print("=" * 60)
print("Financial Ratios Table Verification")
print("=" * 60)

try:
    df = pd.read_sql("SELECT * FROM financial_ratios", conn)

    print(f"Rows Available : {len(df)}")
    print(f"Columns : {len(df.columns)}")
    print()

    print(df.head())
    print()

    print("Columns:")
    print(df.columns.tolist())

except Exception as e:
    print("Error:", e)

conn.close()

print("=" * 60)
print("Verification Completed")
print("=" * 60)