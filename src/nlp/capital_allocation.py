import os
import pandas as pd

# -----------------------------------
# Configuration
# -----------------------------------
INPUT_FILE = "data/raw/balancesheet.xlsx"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "capital_allocation_report.csv"
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

    equity = latest["equity_capital"]
    reserves = latest["reserves"]
    borrowings = latest["borrowings"]
    liabilities = latest["total_liabilities"]
    fixed_assets = latest["fixed_assets"]
    investments = latest["investments"]
    total_assets = latest["total_assets"]

    pros = []
    cons = []

    # -----------------------------------
    # Capital Allocation Rules
    # -----------------------------------

    if reserves > equity:
        pros.append("Strong Reserve Base")
    else:
        cons.append("Low Reserve Base")

    if borrowings < liabilities * 0.30:
        pros.append("Low Borrowings")
    else:
        cons.append("High Borrowings")

    if fixed_assets > 0:
        pros.append("Healthy Fixed Asset Base")

    if investments > 0:
        pros.append("Investment Portfolio Available")

    if total_assets > liabilities:
        pros.append("Strong Asset Position")
    else:
        cons.append("Weak Asset Position")

    # -----------------------------------
    # Rating
    # -----------------------------------

    score = len(pros) - len(cons)

    if score >= 4:
        rating = "Excellent"
        confidence = 95

    elif score >= 2:
        rating = "Good"
        confidence = 85

    elif score >= 0:
        rating = "Average"
        confidence = 75

    else:
        rating = "Needs Improvement"
        confidence = 60

    companies.append(
        {
            "company_id": company,
            "equity_capital": equity,
            "reserves": reserves,
            "borrowings": borrowings,
            "total_assets": total_assets,
            "pros": "; ".join(pros),
            "cons": "; ".join(cons),
            "confidence": confidence,
            "rating": rating,
        }
    )

# -----------------------------------
# Save results
# -----------------------------------
result = pd.DataFrame(companies)

result.to_csv(
    OUTPUT_FILE,
    index=False
)

print("=" * 60)
print("Capital Allocation Report Completed")
print("=" * 60)
print(result.head())
print()
print(f"Companies Processed : {len(result)}")
print(f"Saved : {OUTPUT_FILE}")