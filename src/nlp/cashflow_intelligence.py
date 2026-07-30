import os
import pandas as pd

# -----------------------------------
# Configuration
# -----------------------------------
INPUT_FILE = "data/raw/cashflow.xlsx"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "cashflow_insights.csv"
)

# -----------------------------------
# Read dataset
# -----------------------------------
df = pd.read_excel(INPUT_FILE, header=1)

companies = []

# -----------------------------------
# Process each company
# -----------------------------------
for company in df["company_id"].unique():

    company_df = df[df["company_id"] == company]

    latest = company_df.sort_values(
        "year",
        ascending=False
    ).iloc[0]

    pros = []
    cons = []

    operating = latest["operating_activity"]
    investing = latest["investing_activity"]
    financing = latest["financing_activity"]
    net = latest["net_cash_flow"]

    # -----------------------------
    # Rules
    # -----------------------------

    if operating > 0:
        pros.append("Positive Operating Cash Flow")
    else:
        cons.append("Negative Operating Cash Flow")

    if net > 0:
        pros.append("Positive Net Cash Flow")
    else:
        cons.append("Negative Net Cash Flow")

    if investing < 0:
        pros.append("Investing for Future Growth")

    if financing < 0:
        pros.append("Debt Reduction / Shareholder Returns")
    else:
        cons.append("High Financing Dependence")

    score = len(pros) - len(cons)

    if score >= 3:
        rating = "Excellent"
        confidence = 95

    elif score >= 1:
        rating = "Good"
        confidence = 85

    elif score == 0:
        rating = "Average"
        confidence = 75

    else:
        rating = "Needs Improvement"
        confidence = 60

    companies.append(
        {
            "company_id": company,
            "operating_activity": operating,
            "investing_activity": investing,
            "financing_activity": financing,
            "net_cash_flow": net,
            "pros": "; ".join(pros),
            "cons": "; ".join(cons),
            "confidence": confidence,
            "rating": rating,
        }
    )

result = pd.DataFrame(companies)

result.to_csv(
    OUTPUT_FILE,
    index=False
)

print("=" * 60)
print("Cash Flow Intelligence Completed")
print("=" * 60)
print(result.head())
print()
print(f"Companies Processed : {len(result)}")
print(f"Saved : {OUTPUT_FILE}")