import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Capital Allocation",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Capital Allocation Analysis")

# --------------------------------------
# Load Data
# --------------------------------------
file_path = "outputs/capital_allocation_report.csv"

if not os.path.exists(file_path):
    st.error("capital_allocation_report.csv not found.")
    st.stop()

df = pd.read_csv(file_path)

# --------------------------------------
# Company Selection
# --------------------------------------
companies = sorted(df["company_id"].unique())

selected_company = st.selectbox(
    "Select Company",
    companies
)

company = df[df["company_id"] == selected_company].iloc[0]

st.markdown("---")

# --------------------------------------
# Key Financial Metrics
# --------------------------------------
st.subheader("📊 Capital Structure")

col1, col2 = st.columns(2)

col1.metric(
    "Equity Capital",
    f"{company['equity_capital']:,}"
)

col2.metric(
    "Reserves",
    f"{company['reserves']:,}"
)

col3, col4 = st.columns(2)

col3.metric(
    "Borrowings",
    f"{company['borrowings']:,}"
)

col4.metric(
    "Total Assets",
    f"{company['total_assets']:,}"
)

st.markdown("---")

# --------------------------------------
# Assets vs Liabilities
# --------------------------------------
st.subheader("📈 Assets vs Liabilities")

chart_df = pd.DataFrame(
    {
        "Value": [
            company["equity_capital"],
            company["reserves"],
            company["borrowings"],
            company["total_assets"]
        ]
    },
    index=[
        "Equity Capital",
        "Reserves",
        "Borrowings",
        "Total Assets"
    ]
)

st.bar_chart(chart_df)

st.markdown("---")

# --------------------------------------
# Company Data
# --------------------------------------
st.subheader("📄 Complete Capital Allocation Data")

st.dataframe(
    company.to_frame().T,
    use_container_width=True
)

st.markdown("---")

# --------------------------------------
# Download
# --------------------------------------
csv = (
    company.to_frame()
    .T
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    "📥 Download Company Report",
    csv,
    file_name=f"{selected_company}_capital_allocation.csv",
    mime="text/csv"
)

st.success("Capital allocation analysis completed successfully.")

st.markdown("---")

st.subheader("✅ Strengths")

pros = str(company["pros"]).split(";")

for p in pros:
    if p.strip():
        st.success(p.strip())

st.subheader("⚠ Weaknesses")

cons = str(company["cons"]).split(";")

for c in cons:
    if c.strip():
        st.error(c.strip())

st.markdown("---")

col1, col2 = st.columns(2)

col1.metric("Rating", company["rating"])
col2.metric("Confidence", f"{company['confidence']}%")