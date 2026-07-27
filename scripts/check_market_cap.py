import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql("SELECT * FROM market_cap LIMIT 5", conn)

print("=" * 60)
print("Market Cap Table Columns")
print("=" * 60)

print(df.columns.tolist())

print("\nSample Data:")
print(df)

conn.close()