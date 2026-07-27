import sys
from pathlib import Path

# Add src folder to Python path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_market_cap,
    get_sectors,
)

st.set_page_config(
    page_title="Home",
    layout="wide"
)

st.title("🏠 N100 Financial Intelligence Dashboard")
st.markdown("### Dashboard Overview")

# -----------------------------
# Load Data
# -----------------------------
companies = get_companies()
ratios = get_ratios("ABB")      # Temporary until company selector is added
market = get_market_cap()
sectors = get_sectors()

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Companies", len(companies))

with col2:
    avg_roe = ratios["return_on_equity_pct"].mean()
    st.metric("Avg ROE", f"{avg_roe:.2f}%")

with col3:
    avg_margin = ratios["net_profit_margin_pct"].mean()
    st.metric("Avg Net Margin", f"{avg_margin:.2f}%")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("Market Cap Records", len(market))

with col5:
    st.metric("Sectors", sectors["broad_sector"].nunique())

with col6:
    st.metric("Sub Sectors", sectors["sub_sector"].nunique())

st.divider()

# -----------------------------
# Sector Distribution
# -----------------------------
st.subheader("Sector Distribution")

sector_count = (
    sectors.groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
)


st.bar_chart(
    sector_count.set_index("broad_sector")
)

st.divider()

# -----------------------------
# Top Companies
# -----------------------------
st.subheader("Top 5 Companies")

top = companies[
    ["id", "company_name", "roe_percentage"]
].sort_values(
    by="roe_percentage",
    ascending=False
)

st.dataframe(
    top.head(5),
    use_container_width=True
)