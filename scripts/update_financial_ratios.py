import sqlite3
import pandas as pd

DB_NAME = "nifty100.db"

conn = sqlite3.connect(DB_NAME)

df = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    """,
    conn
)

print("=" * 60)
print("Financial Ratios Summary")
print("=" * 60)

print(f"Total Rows : {len(df)}")
print(f"Companies  : {df['company_id'].nunique()}")

print("\nMissing Values\n")
print(df.isnull().sum())

print("\nStatistics\n")
print(df.describe())

conn.close()

print("=" * 60)
print("Completed")
print("=" * 60)