import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_companies,
    get_pl,
    get_bs,
    get_cf,
    get_ratios,
)

st.set_page_config(
    page_title="Trend Analysis",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Trend Analysis")
st.markdown("---")


# =====================================
# Load Companies
# =====================================

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company_id = companies.loc[
    companies["company_name"] == company,
    "id"
].values[0]


# =====================================
# Load Data
# =====================================

pl = get_pl(company_id)
bs = get_bs(company_id)
cf = get_cf(company_id)
ratios = get_ratios(company_id)

if (
    pl.empty
    or bs.empty
    or cf.empty
    or ratios.empty
):
    st.warning("Financial data not available.")
    st.stop()

st.success(f"Showing trends for {company}")

st.markdown("---")

st.subheader("📈 Revenue Trend")

fig = px.line(
    pl,
    x="year",
    y="sales",
    markers=True,
    line_shape="spline",
    title="Revenue"
)

fig.update_layout(
    height=500,
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("💰 Net Profit Trend")

fig = px.line(
    pl,
    x="year",
    y="net_profit",
    markers=True,
    title="Net Profit"
)

fig.update_layout(
    hovermode="x unified",
    height=500
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("📊 Return on Equity")

fig = px.line(
    ratios,
    x="year",
    y="return_on_equity_pct",
    markers=True
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("💵 Free Cash Flow")

fig = px.line(
    ratios,
    x="year",
    y="free_cash_flow_cr",
    markers=True
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True
)
