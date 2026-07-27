import sqlite3
import pandas as pd
import yaml

DB_NAME = "nifty100.db"


def load_config():
    with open("config/screener_config.yaml", "r") as f:
        return yaml.safe_load(f)


def load_financial_ratios():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM financial_ratios", conn)
    conn.close()
    return df


def apply_filters(df, config):
    filters = config["filters"]

    result = df.copy()

    result = result[
        result["return_on_equity_pct"] >= filters["roe_min"]
    ]

    result = result[
        result["debt_to_equity"] <= filters["debt_to_equity_max"]
    ]

    result = result[
        result["free_cash_flow_cr"] >= filters["free_cash_flow_min"]
    ]

    return result


def quality_compounder(df):
    return df[
        (df["return_on_equity_pct"] >= 15) &
        (df["debt_to_equity"] <= 1) &
        (df["free_cash_flow_cr"] > 0)
    ]


def value_pick(df):
    return df[
        df["dividend_payout_ratio_pct"] > 0
    ]


def growth_accelerator(df):
    return df[
        df["net_profit_margin_pct"] >= 20
    ]


def dividend_champion(df):
    return df[
        df["dividend_payout_ratio_pct"] >= 20
    ]


def debt_free(df):
    return df[
        df["debt_to_equity"] == 0
    ]


def turnaround_watch(df):
    return df[
        df["free_cash_flow_cr"] > 0
    ]


def add_composite_score(df):
    result = df.copy()

    result["composite_score"] = (
        result["return_on_equity_pct"].fillna(0) * 0.35 +
        result["net_profit_margin_pct"].fillna(0) * 0.30 +
        result["free_cash_flow_cr"].fillna(0).clip(lower=0) / 100 * 0.20 +
        (1 / (result["debt_to_equity"].replace(0, 0.01))) * 0.15
    )

    result = result.sort_values(
        by="composite_score",
        ascending=False
    )

    return result


if __name__ == "__main__":

    config = load_config()

    df = load_financial_ratios()

    filtered = apply_filters(df, config)

    quality = add_composite_score(quality_compounder(filtered))
    value = add_composite_score(value_pick(filtered))
    growth = add_composite_score(growth_accelerator(filtered))
    dividend = add_composite_score(dividend_champion(filtered))
    debt = add_composite_score(debt_free(filtered))
    turnaround = add_composite_score(turnaround_watch(filtered))

    with pd.ExcelWriter("outputs/screener_output.xlsx") as writer:
        quality.to_excel(writer, sheet_name="Quality", index=False)
        value.to_excel(writer, sheet_name="Value", index=False)
        growth.to_excel(writer, sheet_name="Growth", index=False)
        dividend.to_excel(writer, sheet_name="Dividend", index=False)
        debt.to_excel(writer, sheet_name="DebtFree", index=False)
        turnaround.to_excel(writer, sheet_name="Turnaround", index=False)

    print("=" * 60)
    print("Sprint 3 - Screener Engine")
    print("=" * 60)

    print(f"Original Records : {len(df)}")
    print(f"Filtered Records : {len(filtered)}")
    print()

    print(f"Quality      : {len(quality)}")
    print(f"Value        : {len(value)}")
    print(f"Growth       : {len(growth)}")
    print(f"Dividend     : {len(dividend)}")
    print(f"Debt Free    : {len(debt)}")
    print(f"Turnaround   : {len(turnaround)}")

    print()
    print("Excel report saved to outputs/screener_output.xlsx")