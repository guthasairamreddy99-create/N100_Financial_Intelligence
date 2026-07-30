import os
import pandas as pd

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ------------------------------------
# Configuration
# ------------------------------------
COMPANY_FILE = "outputs/company_insights.csv"
CASHFLOW_FILE = "outputs/cashflow_insights.csv"
CAPITAL_FILE = "outputs/capital_allocation_report.csv"

OUTPUT_DIR = "outputs/pdf_reports"

os.makedirs(OUTPUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()

# ------------------------------------
# Read Data
# ------------------------------------
company_df = pd.read_csv(COMPANY_FILE)
cashflow_df = pd.read_csv(CASHFLOW_FILE)
capital_df = pd.read_csv(CAPITAL_FILE)

# ------------------------------------
# Generate PDFs
# ------------------------------------
for _, company in company_df.iterrows():

    company_id = company["company_id"]

    cash = cashflow_df[
        cashflow_df["company_id"] == company_id
    ].iloc[0]

    capital = capital_df[
        capital_df["company_id"] == company_id
    ].iloc[0]

    pdf_file = os.path.join(
        OUTPUT_DIR,
        f"{company_id}.pdf"
    )

    doc = SimpleDocTemplate(pdf_file)

    story = []

    story.append(
        Paragraph(
            f"<b>{company_id} Financial Tearsheet</b>",
            styles["Title"],
        )
    )

    story.append(
        Paragraph(
            "<br/><b>Pros</b><br/>"
            + str(company["pros"]),
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            "<br/><b>Cons</b><br/>"
            + str(company["cons"]),
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            f"<br/><b>Overall Rating:</b> {company['rating']}",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Confidence:</b> {company['confidence']}%",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            "<br/><b>Cash Flow Intelligence</b>",
            styles["Heading2"],
        )
    )

    story.append(
        Paragraph(
            f"""
Operating Activity : {cash['operating_activity']}<br/>
Investing Activity : {cash['investing_activity']}<br/>
Financing Activity : {cash['financing_activity']}<br/>
Net Cash Flow : {cash['net_cash_flow']}
""",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            "<br/><b>Capital Allocation</b>",
            styles["Heading2"],
        )
    )

    story.append(
        Paragraph(
            f"""
Equity Capital : {capital['equity_capital']}<br/>
Reserves : {capital['reserves']}<br/>
Borrowings : {capital['borrowings']}<br/>
Total Assets : {capital['total_assets']}
""",
            styles["BodyText"],
        )
    )

    doc.build(story)

print("=" * 60)
print("PDF Tearsheet Generator Completed")
print("=" * 60)
print(f"Companies Processed : {len(company_df)}")
print(f"PDFs Generated : {OUTPUT_DIR}")