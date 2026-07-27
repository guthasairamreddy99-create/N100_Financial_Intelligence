import sqlite3
import pandas as pd

DB_NAME = "nifty100.db"


def load_financial_ratios():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM financial_ratios", conn)
    conn.close()
    return df


def assign_sector(company_id):
    """
    Temporary sector mapping.
    Replace this with your actual sector data later.
    """
    sector_map = {
        "TCS": "IT",
        "INFY": "IT",
        "HCLTECH": "IT",
        "WIPRO": "IT",

        "HDFCBANK": "Banking",
        "ICICIBANK": "Banking",
        "SBIN": "Banking",
        "AXISBANK": "Banking",

        "RELIANCE": "Energy",
        "ONGC": "Energy",
        "BPCL": "Energy",
    }

    return sector_map.get(company_id, "Others")


def calculate_sector_ranks(df):

    result = df.copy()

    result["sector"] = result["company_id"].apply(assign_sector)

    metrics = [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "free_cash_flow_cr",
        "debt_to_equity",
    ]

    for metric in metrics:

        ascending = metric == "debt_to_equity"

        result[f"{metric}_sector_rank"] = (
            result.groupby("sector")[metric]
            .rank(
                method="average",
                pct=True,
                ascending=ascending
            )
            .mul(100)
            .round(2)
        )

    return result


if __name__ == "__main__":

    df = load_financial_ratios()

    ranked = calculate_sector_ranks(df)

    ranked.to_excel(
        "outputs/sector_peer_comparison.xlsx",
        index=False
    )

    print("=" * 60)
    print("Sector Peer Comparison")
    print("=" * 60)
    print(f"Records : {len(ranked)}")
    print("Saved : outputs/sector_peer_comparison.xlsx")