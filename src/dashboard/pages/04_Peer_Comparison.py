import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Peer Comparison",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Peer Comparison")

# ----------------------------------------
# Load Data
# ----------------------------------------
if not os.path.exists("outputs/company_insights.csv"):
    st.error("company_insights.csv not found.")
    st.stop()

df = pd.read_csv("outputs/company_insights.csv")

# ----------------------------------------
# Company Selection
# ----------------------------------------
companies = sorted(df["company_id"].unique())

selected = st.multiselect(
    "Select Companies to Compare",
    companies,
    default=companies[:2] if len(companies) >= 2 else companies
)

if len(selected) < 2:
    st.warning("Please select at least two companies.")
    st.stop()

compare_df = df[df["company_id"].isin(selected)]

# ----------------------------------------
# Metrics
# ----------------------------------------
st.subheader("Comparison Summary")

col1, col2 = st.columns(2)

best_company = compare_df.loc[
    compare_df["confidence"].idxmax(),
    "company_id"
]

highest_conf = compare_df["confidence"].max()

col1.metric("Highest Confidence", f"{highest_conf}%")
col2.metric("Top Company", best_company)

st.markdown("---")

# ----------------------------------------
# Comparison Table
# ----------------------------------------
st.subheader("Company Comparison")

display_df = compare_df[
    [
        "company_id",
        "rating",
        "confidence",
        "pros",
        "cons"
    ]
]

st.dataframe(
    display_df,
    use_container_width=True
)

# ----------------------------------------
# Confidence Chart
# ----------------------------------------
st.subheader("Confidence Comparison")

chart_df = compare_df.set_index("company_id")["confidence"]

st.bar_chart(chart_df)

# ----------------------------------------
# Download
# ----------------------------------------
csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Comparison",
    data=csv,
    file_name="peer_comparison.csv",
    mime="text/csv"
)