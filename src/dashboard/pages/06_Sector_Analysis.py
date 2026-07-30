import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Sector Analysis",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Sector Analysis")

# ---------------------------------------
# Load Data
# ---------------------------------------
if not os.path.exists("outputs/company_insights.csv"):
    st.error("company_insights.csv not found.")
    st.stop()

df = pd.read_csv("outputs/company_insights.csv")

# ---------------------------------------
# Check Sector Column
# ---------------------------------------
if "sector" not in df.columns:
    st.warning("Sector information is not available in company_insights.csv")
    st.info("Showing overall company statistics instead.")

    col1, col2, col3 = st.columns(3)

    col1.metric("Companies", len(df))
    col2.metric("Average Confidence", f"{df['confidence'].mean():.2f}%")
    col3.metric("Unique Ratings", df["rating"].nunique())

    st.markdown("---")

    st.subheader("Company Ratings")

    rating_count = df["rating"].value_counts()

    st.bar_chart(rating_count)

    st.subheader("Company Insights")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.stop()

# ---------------------------------------
# Sector Selection
# ---------------------------------------
sectors = sorted(df["sector"].dropna().unique())

selected_sector = st.selectbox(
    "Select Sector",
    sectors
)

sector_df = df[df["sector"] == selected_sector]

# ---------------------------------------
# Metrics
# ---------------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Companies", len(sector_df))

col2.metric(
    "Average Confidence",
    f"{sector_df['confidence'].mean():.2f}%"
)

top_company = sector_df.loc[
    sector_df["confidence"].idxmax(),
    "company_id"
]

col3.metric("Top Company", top_company)

st.markdown("---")

# ---------------------------------------
# Rating Distribution
# ---------------------------------------
st.subheader("Rating Distribution")

rating_df = sector_df["rating"].value_counts()

st.bar_chart(rating_df)

# ---------------------------------------
# Company List
# ---------------------------------------
st.subheader("Sector Companies")

st.dataframe(
    sector_df,
    use_container_width=True
)

# ---------------------------------------
# Download
# ---------------------------------------
csv = sector_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Sector Data",
    csv,
    file_name=f"{selected_sector}_companies.csv",
    mime="text/csv"
)

st.success("Sector analysis completed successfully.")