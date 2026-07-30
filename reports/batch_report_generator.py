import os
import pandas as pd

# -----------------------------------
# Configuration
# -----------------------------------
PDF_DIR = "outputs/pdf_reports"
OUTPUT_FILE = "outputs/report_summary.csv"

records = []

# -----------------------------------
# Scan PDF folder
# -----------------------------------
for file in os.listdir(PDF_DIR):

    if file.endswith(".pdf"):

        filepath = os.path.join(PDF_DIR, file)

        records.append(
            {
                "company_id": file.replace(".pdf", ""),
                "filename": file,
                "size_kb": round(os.path.getsize(filepath) / 1024, 2),
            }
        )

# -----------------------------------
# Save Summary
# -----------------------------------
summary = pd.DataFrame(records)

summary.to_csv(OUTPUT_FILE, index=False)

print("=" * 60)
print("Batch Report Generator Completed")
print("=" * 60)

print(summary.head())

print()
print(f"Total Reports Generated : {len(summary)}")
print(f"Summary Saved : {OUTPUT_FILE}")