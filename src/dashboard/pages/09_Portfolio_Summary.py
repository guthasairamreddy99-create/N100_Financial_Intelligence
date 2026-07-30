import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Portfolio Summary",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Portfolio Summary Dashboard")

# --------------------------------------------------
# Load Data
# --------------------------------------------------
company_file = "outputs/company_insights.csv"
cashflow_file = "outputs/cashflow_insights.csv"
capital_file = "outputs/capital_allocation_report.csv"
report_file = "outputs/report_summary.csv"

if not os.path.exists(company_file):
    st.error("company_insights.csv not found.")
    st.stop()

company_df = pd.read_csv(company_file)

cashflow_df = (
    pd.read_csv(cashflow_file)
    if os.path.exists(cashflow_file)
    else pd.DataFrame()
)

capital_df = (
    pd.read_csv(capital_file)
    if os.path.exists(capital_file)
    else pd.DataFrame()
)

report_df = (
    pd.read_csv(report_file)
    if os.path.exists(report_file)
    else pd.DataFrame()
)

# --------------------------------------------------
# Dashboard Metrics
# --------------------------------------------------
st.subheader("📊 Portfolio Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Companies",
    len(company_df)
)

col2.metric(
    "Reports",
    len(report_df)
)

avg_conf = (
    round(company_df["confidence"].mean(), 2)
    if "confidence" in company_df.columns
    else 0
)

col3.metric(
    "Average Confidence",
    f"{avg_conf}%"
)

top_company = company_df.loc[
    company_df["confidence"].idxmax(),
    "company_id"
]

col4.metric(
    "Top Company",
    top_company
)

st.markdown("---")

# --------------------------------------------------
# Confidence Chart
# --------------------------------------------------
st.subheader("📈 Company Confidence")

chart_df = company_df.set_index("company_id")[["confidence"]]

st.bar_chart(chart_df)

st.markdown("---")

# --------------------------------------------------
# Rating Distribution
# --------------------------------------------------
st.subheader("⭐ Rating Distribution")

rating_df = company_df["rating"].value_counts()

st.bar_chart(rating_df)

st.markdown("---")

# --------------------------------------------------
# Company Insights
# --------------------------------------------------
st.subheader("🏢 Company Insights")

st.dataframe(
    company_df,
    use_container_width=True
)

# --------------------------------------------------
# Cash Flow
# --------------------------------------------------
if not cashflow_df.empty:

    st.markdown("---")
    st.subheader("💰 Cash Flow Intelligence")

    st.dataframe(
        cashflow_df,
        use_container_width=True
    )

# --------------------------------------------------
# Capital Allocation
# --------------------------------------------------
if not capital_df.empty:

    st.markdown("---")
    st.subheader("🏦 Capital Allocation")

    st.dataframe(
        capital_df,
        use_container_width=True
    )

# --------------------------------------------------
# Report Summary
# --------------------------------------------------
if not report_df.empty:

    st.markdown("---")
    st.subheader("📄 Report Summary")

    st.dataframe(
        report_df,
        use_container_width=True
    )

# --------------------------------------------------
# Download Portfolio Summary
# --------------------------------------------------
csv = company_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Portfolio Summary",
    data=csv,
    file_name="portfolio_summary.csv",
    mime="text/csv"
)

st.success("Portfolio Summary Dashboard loaded successfully.")