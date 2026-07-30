import os
import re
import pandas as pd

# -----------------------------
# Configuration
# -----------------------------
INPUT_FILE = "data/raw/analysis.xlsx"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "analysis_parsed.csv")
FAILURE_FILE = os.path.join(OUTPUT_DIR, "parse_failures.csv")

# Read Excel
df = pd.read_excel(INPUT_FILE, header=1)

# Columns to parse
FIELDS = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]

# Regex Pattern
pattern = re.compile(
    r"(?:(TTM)|(Last)\s*Year|(\d+)\s*Years?)\s*:?\s*(-?\d+(?:\.\d+)?)%",
    re.IGNORECASE,
)

parsed_rows = []
failed_rows = []

for _, row in df.iterrows():
    company = row["company_id"]

    for field in FIELDS:
        text = str(row[field]).strip()

        match = pattern.search(text)

        if match:

            if match.group(1):          # TTM
                years = 0

            elif match.group(2):        # Last Year
                years = 1

            else:                       # X Years
                years = int(match.group(3))

            value = float(match.group(4))

            parsed_rows.append(
                {
                    "company_id": company,
                    "metric_type": field,
                    "period_years": years,
                    "value_pct": value,
                }
            )

        else:
            failed_rows.append(
                {
                    "company_id": company,
                    "metric_type": field,
                    "original_text": text,
                }
            )

parsed_df = pd.DataFrame(parsed_rows)
failed_df = pd.DataFrame(failed_rows)

parsed_df.to_csv(OUTPUT_FILE, index=False)
failed_df.to_csv(FAILURE_FILE, index=False)

print("=" * 50)
print("Analysis Parser Completed")
print("=" * 50)
print(f"Parsed Records : {len(parsed_df)}")
print(f"Failed Records : {len(failed_df)}")
print(f"Saved : {OUTPUT_FILE}")
print(f"Saved : {FAILURE_FILE}")