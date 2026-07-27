import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql(
    "SELECT * FROM company_master LIMIT 5",
    conn
)

print("\nColumns:\n")
for col in df.columns:
    print(col)

print("\nSample Data:\n")
print(df.head())

conn.close()