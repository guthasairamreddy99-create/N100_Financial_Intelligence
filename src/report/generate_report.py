import os
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd

DB_NAME = "nifty100.db"


def load_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM financial_ratios", conn)
    conn.close()
    return df


if __name__ == "__main__":

    os.makedirs("outputs", exist_ok=True)

    df = load_data()

    top10 = (
        df.sort_values("return_on_equity_pct", ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 5))
    plt.bar(top10["company_id"], top10["return_on_equity_pct"])
    plt.title("Top 10 Companies by ROE")
    plt.xlabel("Company")
    plt.ylabel("ROE (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("outputs/roe_chart.png")
    plt.close()

    table_html = top10.to_html(index=False)

    with open("templates/report.html", "r", encoding="utf-8") as f:
        html = f.read()

    chart_html = '<img src="roe_chart.png" width="900">'

    html = html.replace("{{TABLE}}", chart_html + "<br><br>" + table_html)

    with open(
        "outputs/financial_report.html",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(html)

    print("=" * 60)
    print("Financial Report Generated")
    print("=" * 60)
    print("Files created:")
    print(" - outputs/financial_report.html")
    print(" - outputs/roe_chart.png")