import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

bs = pd.read_sql("""
SELECT *
FROM balancesheet
WHERE company_id='INDIGO'
AND year='Mar 2013'
""", conn)

pl = pd.read_sql("""
SELECT *
FROM profitandloss
WHERE company_id='INDIGO'
AND year='Mar 2013'
""", conn)

print("=" * 60)
print("BALANCE SHEET")
print("=" * 60)
print(bs)

print()

print("=" * 60)
print("PROFIT & LOSS")
print("=" * 60)
print(pl)

conn.close()