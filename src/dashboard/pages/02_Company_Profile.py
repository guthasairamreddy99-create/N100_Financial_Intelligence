import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Company Profile",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Company Profile")

# -------------------------------
# Load Data
# -------------------------------
if not os.path.exists("outputs/company_insights.csv"):
    st.error("company_insights.csv not found.")
    st.stop()

df = pd.read_csv("outputs/company_insights.csv")

# -------------------------------
# Company Selection
# -------------------------------
companies = sorted(df["company_id"].unique())

selected_company = st.selectbox(
    "Select Company",
    companies
)

company = df[df["company_id"] == selected_company].iloc[0]

st.markdown("---")

# -------------------------------
# Basic Metrics
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Rating",
    company["rating"]
)

col2.metric(
    "Confidence",
    f"{company['confidence']}%"
)

col3.metric(
    "Company",
    company["company_id"]
)

st.markdown("---")

# -------------------------------
# Pros
# -------------------------------
st.subheader("✅ Financial Strengths")

pros = str(company["pros"]).split(";")

for item in pros:
    item = item.strip()
    if item:
        st.success(item)

# -------------------------------
# Cons
# -------------------------------
st.subheader("⚠ Financial Weaknesses")

cons = str(company["cons"]).split(";")

for item in cons:
    item = item.strip()
    if item:
        st.error(item)

st.markdown("---")

# -------------------------------
# Complete Record
# -------------------------------
st.subheader("📄 Complete Company Data")

st.dataframe(
    company.to_frame().T,
    use_container_width=True
)