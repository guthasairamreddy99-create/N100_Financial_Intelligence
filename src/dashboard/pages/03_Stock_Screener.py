import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Stock Screener",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Stock Screener")

# ------------------------------------
# Load Data
# ------------------------------------
if not os.path.exists("outputs/company_insights.csv"):
    st.error("company_insights.csv not found.")
    st.stop()

df = pd.read_csv("outputs/company_insights.csv")

# ------------------------------------
# Sidebar Filters
# ------------------------------------
st.sidebar.header("Filter Companies")

ratings = sorted(df["rating"].dropna().unique())

selected_rating = st.sidebar.multiselect(
    "Select Rating",
    ratings,
    default=ratings
)

min_confidence = st.sidebar.slider(
    "Minimum Confidence",
    min_value=0,
    max_value=100,
    value=60
)

# ------------------------------------
# Apply Filters
# ------------------------------------
filtered_df = df[
    (df["rating"].isin(selected_rating)) &
    (df["confidence"] >= min_confidence)
]

# ------------------------------------
# Summary Metrics
# ------------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Companies Found", len(filtered_df))

avg_conf = (
    round(filtered_df["confidence"].mean(), 2)
    if len(filtered_df) > 0
    else 0
)

col2.metric("Average Confidence", f"{avg_conf}%")

best_rating = (
    filtered_df["rating"].mode()[0]
    if len(filtered_df) > 0
    else "-"
)

col3.metric("Most Common Rating", best_rating)

st.markdown("---")

# ------------------------------------
# Results
# ------------------------------------
st.subheader("Filtered Companies")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ------------------------------------
# Download
# ------------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Results",
    data=csv,
    file_name="filtered_companies.csv",
    mime="text/csv"
)