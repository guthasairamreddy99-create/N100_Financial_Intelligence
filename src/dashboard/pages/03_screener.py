import sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_sectors,
)

st.set_page_config(
    page_title="Stock Screener",
    layout="wide"
)

st.title("📊 Stock Screener")
st.write("Filter Nifty 100 companies using financial metrics.")

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------
companies_df = get_companies()
sectors_df = get_sectors()

company_list = companies_df[["id", "company_name"]]

st.success(f"Loaded {len(company_list)} companies")

# ----------------------------------------------------
# Selected Company
# ----------------------------------------------------
selected_company = st.selectbox(
    "Select Company",
    company_list["id"]
)

st.write("Selected Company:", selected_company)

st.divider()

# ----------------------------------------------------
# Filters
# ----------------------------------------------------
sector_list = ["All"] + sorted(
    sectors_df["broad_sector"].dropna().unique().tolist()
)

selected_sector = st.selectbox(
    "Select Sector",
    sector_list
)

search_company = st.text_input(
    "🔍 Search Company",
    placeholder="Type company name..."
)

min_roe = st.slider(
    "Minimum ROE (%)",
    min_value=0.0,
    max_value=50.0,
    value=15.0,
    step=0.5,
)

max_debt = st.slider(
    "Maximum Debt / Equity",
    min_value=0.0,
    max_value=5.0,
    value=1.0,
    step=0.1,
)

min_margin = st.slider(
    "Minimum Net Profit Margin (%)",
    min_value=0.0,
    max_value=50.0,
    value=10.0,
    step=0.5,
)

# ----------------------------------------------------
# Selected Company Summary
# ----------------------------------------------------
ratios = get_ratios(selected_company)

if not ratios.empty:

    latest_ratio = ratios.sort_values("year").iloc[-1]

    st.metric(
        "Latest ROE",
        f"{latest_ratio['return_on_equity_pct']:.2f}%"
    )

    if (
        latest_ratio["return_on_equity_pct"] >= min_roe
        and latest_ratio["debt_to_equity"] <= max_debt
        and latest_ratio["net_profit_margin_pct"] >= min_margin
    ):
        st.success("✅ Company passes all selected filters")
    else:
        st.error("❌ Company does not pass all selected filters")

else:
    st.warning("No financial ratio data available.")

# ----------------------------------------------------
# Screening Results
# ----------------------------------------------------
st.divider()

st.subheader("📋 Screening Results")

results = []

for _, company in company_list.iterrows():

    sector = sectors_df[
        sectors_df["company_id"] == company["id"]
    ]

    if sector.empty:
        continue

    company_sector = sector.iloc[0]["broad_sector"]

    if (
        selected_sector != "All"
        and company_sector != selected_sector
    ):
        continue

    if (
        search_company
        and search_company.lower()
        not in company["company_name"].lower()
    ):
        continue

    ratios = get_ratios(company["id"])

    if ratios.empty:
        continue

    latest = ratios.sort_values("year").iloc[-1]

    if (
        latest["return_on_equity_pct"] >= min_roe
        and latest["debt_to_equity"] <= max_debt
        and latest["net_profit_margin_pct"] >= min_margin
    ):

        results.append({
            "Company": company["company_name"],
            "Sector": company_sector,
            "Year": latest["year"],
            "ROE (%)": round(latest["return_on_equity_pct"], 2),
            "Net Margin (%)": round(latest["net_profit_margin_pct"], 2),
            "Debt / Equity": round(latest["debt_to_equity"], 2),
            "EPS": round(latest["earnings_per_share"], 2),
        })

if results:

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        by="ROE (%)",
        ascending=False,
    )

    st.dataframe(
        results_df,
        use_container_width=True,
        hide_index=True,
    )

    csv = results_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Results (CSV)",
        data=csv,
        file_name="stock_screener_results.csv",
        mime="text/csv",
    )

    st.success(
        f"✅ {len(results_df)} companies matched the selected filters."
    )

else:
    st.warning("No companies matched the selected filters.")