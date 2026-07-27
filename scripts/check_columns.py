import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios LIMIT 1",
    conn
)

print("\nColumns in financial_ratios:\n")
for col in df.columns:
    print(col)

conn.close()