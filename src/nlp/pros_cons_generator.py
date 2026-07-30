import os
import pandas as pd

# -----------------------------
# Configuration
# -----------------------------
INPUT_FILE = "outputs/analysis_parsed.csv"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "company_insights.csv")

# -----------------------------
# Read parsed metrics
# -----------------------------
df = pd.read_csv(INPUT_FILE)

companies = []

# Process each company
for company in df["company_id"].unique():

    company_df = df[df["company_id"] == company]

    pros = []
    cons = []

    for _, row in company_df.iterrows():

        metric = row["metric_type"]
        value = row["value_pct"]

        # -----------------------------
        # ROE Rules
        # -----------------------------
        if metric == "roe":

            if value >= 20:
                pros.append("Strong ROE")

            elif value < 10:
                cons.append("Weak ROE")

        # -----------------------------
        # Sales Growth Rules
        # -----------------------------
        elif metric == "compounded_sales_growth":

            if value >= 15:
                pros.append("Strong Sales Growth")

            elif value < 5:
                cons.append("Weak Sales Growth")

        # -----------------------------
        # Profit Growth Rules
        # -----------------------------
        elif metric == "compounded_profit_growth":

            if value >= 15:
                pros.append("Strong Profit Growth")

            elif value < 5:
                cons.append("Weak Profit Growth")

        # -----------------------------
        # Stock CAGR Rules
        # -----------------------------
        elif metric == "stock_price_cagr":

            if value >= 15:
                pros.append("Excellent Stock CAGR")

            elif value < 0:
                cons.append("Negative Stock CAGR")

    # -----------------------------
    # Confidence & Rating
    # -----------------------------
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
        "pros": "; ".join(sorted(set(pros))),
        "cons": "; ".join(sorted(set(cons))),
        "confidence": confidence,
        "rating": rating,
    }
)

# Save results
result = pd.DataFrame(companies)

result.to_csv(OUTPUT_FILE, index=False)

print("=" * 50)
print("Pros & Cons Generator Completed")
print("=" * 50)
print(result.head())
print()
print(f"Companies Processed : {len(result)}")
print(f"Saved : {OUTPUT_FILE}")