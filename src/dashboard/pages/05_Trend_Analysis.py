import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Trend Analysis",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Financial Trend Analysis")

# --------------------------------------------------
# Load Data
# --------------------------------------------------
file_path = "outputs/company_insights.csv"

if not os.path.exists(file_path):
    st.error("company_insights.csv not found.")
    st.stop()

df = pd.read_csv(file_path)

# --------------------------------------------------
# Company Selection
# --------------------------------------------------
companies = sorted(df["company_id"].unique())

selected_company = st.selectbox(
    "Select Company",
    companies
)

company = df[df["company_id"] == selected_company].iloc[0]

st.markdown("---")

# --------------------------------------------------
# Overall Metrics
# --------------------------------------------------
st.subheader("📊 Overall Analysis")

col1, col2 = st.columns(2)

col1.metric(
    "Rating",
    company["rating"]
)

col2.metric(
    "Confidence",
    f"{company['confidence']}%"
)

st.markdown("---")

# --------------------------------------------------
# Confidence Chart
# --------------------------------------------------
st.subheader("📈 Confidence Comparison")

chart_df = df.set_index("company_id")[["confidence"]]

st.bar_chart(chart_df)

st.markdown("---")

# --------------------------------------------------
# Rating Distribution
# --------------------------------------------------
st.subheader("⭐ Rating Distribution")

rating_df = df["rating"].value_counts()

st.bar_chart(rating_df)

st.markdown("---")

# --------------------------------------------------
# Pros
# --------------------------------------------------
st.subheader("✅ Financial Strengths")

pros = str(company["pros"]).split(";")

for p in pros:
    p = p.strip()
    if p:
        st.success(p)

# --------------------------------------------------
# Cons
# --------------------------------------------------
st.subheader("⚠ Financial Weaknesses")

cons = str(company["cons"]).split(";")

for c in cons:
    c = c.strip()
    if c:
        st.error(c)

st.markdown("---")

# --------------------------------------------------
# Complete Record
# --------------------------------------------------
st.subheader("📄 Complete Record")

st.dataframe(
    company.to_frame().T,
    use_container_width=True
)