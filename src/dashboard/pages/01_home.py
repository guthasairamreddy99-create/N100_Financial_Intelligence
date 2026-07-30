import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 N100 Financial Intelligence Dashboard")
st.markdown("---")

st.markdown("""
Welcome to the **N100 Financial Intelligence Platform**.

This dashboard provides financial analytics, peer comparison,
screening, trend analysis, capital allocation insights,
and AI-generated reports for Nifty 100 companies.
""")

st.markdown("## 📊 Project Overview")

col1, col2, col3 = st.columns(3)

company_count = 0
report_count = 0
avg_confidence = 0

if os.path.exists("outputs/company_insights.csv"):
    company_df = pd.read_csv("outputs/company_insights.csv")
    company_count = len(company_df)

    if "confidence" in company_df.columns:
        avg_confidence = round(company_df["confidence"].mean(), 2)

if os.path.exists("outputs/report_summary.csv"):
    report_df = pd.read_csv("outputs/report_summary.csv")
    report_count = len(report_df)

col1.metric("Companies Analyzed", company_count)
col2.metric("Reports Generated", report_count)
col3.metric("Average Confidence", f"{avg_confidence}%")

st.markdown("---")

st.subheader("📌 Available Modules")

modules = [
    "🏢 Company Profile",
    "🔍 Stock Screener",
    "📊 Peer Comparison",
    "📈 Trend Analysis",
    "🏭 Sector Analysis",
    "💰 Capital Allocation",
    "📄 Reports",
    "📋 Portfolio Summary"
]

for module in modules:
    st.write(f"✅ {module}")

st.markdown("---")

st.subheader("📂 Project Outputs")

files = [
    "outputs/company_insights.csv",
    "outputs/cashflow_insights.csv",
    "outputs/capital_allocation_report.csv",
    "outputs/report_summary.csv"
]

for file in files:
    if os.path.exists(file):
        st.success(f"✔ {file}")
    else:
        st.error(f"✘ {file} not found")

st.markdown("---")

st.info("Use the sidebar to navigate through the dashboard modules.")