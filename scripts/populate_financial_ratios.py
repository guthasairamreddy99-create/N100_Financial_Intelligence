import os
import sys
import sqlite3
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    debt_to_equity,
    interest_coverage,
    asset_turnover,
)

DB_NAME = "nifty100.db"

conn = sqlite3.connect(DB_NAME)

# Load source tables
bs = pd.read_sql("SELECT * FROM balancesheet", conn)
pl = pd.read_sql("SELECT * FROM profitandloss", conn)
cf = pd.read_sql("SELECT * FROM cashflow", conn)

# Merge datasets
df = (
    bs.merge(pl, on=["company_id", "year"], how="inner")
      .merge(cf, on=["company_id", "year"], how="left")
)

ratios = pd.DataFrame()

ratios["company_id"] = df["company_id"]
ratios["year"] = df["year"]

# Financial Ratios
ratios["net_profit_margin_pct"] = df.apply(
    lambda r: net_profit_margin(r["net_profit"], r["sales"]),
    axis=1,
)

ratios["operating_profit_margin_pct"] = df.apply(
    lambda r: operating_profit_margin(r["operating_profit"], r["sales"]),
    axis=1,
)

ratios["return_on_equity_pct"] = df.apply(
    lambda r: return_on_equity(
        r["net_profit"],
        r["equity_capital"],
        r["reserves"],
    ),
    axis=1,
)

ratios["debt_to_equity"] = df.apply(
    lambda r: debt_to_equity(
        r["borrowings"],
        r["equity_capital"],
        r["reserves"],
    ),
    axis=1,
)

ratios["interest_coverage"] = df.apply(
    lambda r: interest_coverage(
        r["operating_profit"],
        r["interest"],
    ),
    axis=1,
)

ratios["asset_turnover"] = df.apply(
    lambda r: asset_turnover(
        r["sales"],
        r["total_assets"],
    ),
    axis=1,
)

# Additional fields
ratios["free_cash_flow_cr"] = (
    df["operating_activity"].fillna(0)
    + df["investing_activity"].fillna(0)
)

ratios["earnings_per_share"] = df["eps"]
ratios["dividend_payout_ratio_pct"] = df["dividend_payout"]
ratios["total_debt_cr"] = df["borrowings"]
ratios["cash_from_operations_cr"] = df["operating_activity"]

# Save to SQLite
ratios.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False,
)

conn.close()

print("=" * 60)
print("Financial Ratios Generated Successfully")
print("=" * 60)
print(f"Rows Created: {len(ratios)}")
print()
print(ratios.head())