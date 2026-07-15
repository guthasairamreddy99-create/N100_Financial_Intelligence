import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql(
    "SELECT company_id, year, net_profit_margin_pct, operating_profit_margin_pct, return_on_equity_pct FROM financial_ratios",
    conn
)

print("=" * 60)
print("KPI Validation")
print("=" * 60)

print("\nNet Profit Margin")
print(df["net_profit_margin_pct"].describe())

print("\nOperating Profit Margin")
print(df["operating_profit_margin_pct"].describe())

print("\nReturn On Equity")
print(df["return_on_equity_pct"].describe())

print("\nTop 10 Highest ROE")

print(
    df.sort_values(
        by="return_on_equity_pct",
        ascending=False
    )[["company_id","year","return_on_equity_pct"]].head(10)
)

conn.close()