import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql("SELECT * FROM financial_ratios", conn)

print("=" * 60)
print("Ratio Edge Cases")
print("=" * 60)

print("\nROE > 1000%")
print(df[df["return_on_equity_pct"] > 1000][
    ["company_id", "year", "return_on_equity_pct"]
])

print("\nOperating Margin > 500%")
print(df[df["operating_profit_margin_pct"] > 500][
    ["company_id", "year", "operating_profit_margin_pct"]
])

print("\nNegative ROE")
print(df[df["return_on_equity_pct"] < 0][
    ["company_id", "year", "return_on_equity_pct"]
].head(20))

conn.close()