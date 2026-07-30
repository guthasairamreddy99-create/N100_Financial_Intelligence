import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Trend Analysis",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Financial Trend Analysis")

# ---------------------------------------
# Load Data
# ---------------------------------------
if not os.path.exists("outputs/company_insights.csv"):
    st.error("company_insights.csv not found.")
    st.stop()

df = pd.read_csv("outputs/company_insights.csv")

# ---------------------------------------
# Company Selection
# ---------------------------------------
companies = sorted(df["company_id"].unique())

selected_company = st.selectbox(
    "Select Company",
    companies
)

company = df[df["company_id"] == selected_company].iloc[0]

st.markdown("---")

# ---------------------------------------
# Financial Metrics
# ---------------------------------------
metrics = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

available_metrics = [
    m for m in metrics if m in company.index
]

if available_metrics:

    trend_df = pd.DataFrame({
        "Metric": available_metrics,
        "Value": [company[m] for m in available_metrics]
    })

    st.subheader("Financial Growth Metrics")

    st.dataframe(
        trend_df,
        use_container_width=True
    )

    chart_df = trend_df.set_index("Metric")

    st.bar_chart(chart_df)

else:
    st.warning("Trend metrics are not available in company_insights.csv")

st.markdown("---")

# ---------------------------------------
# Rating
# ---------------------------------------
st.subheader("Overall Analysis")

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

# ---------------------------------------
# Insights
# ---------------------------------------
st.subheader("Pros")

pros = str(company["pros"]).split(";")

for p in pros:
    if p.strip():
        st.success(p.strip())

st.subheader("Cons")

cons = str(company["cons"]).split(";")

for c in cons:
    if c.strip():
        st.error(c.strip())