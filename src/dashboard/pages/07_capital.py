import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_companies,
    get_bs,
    get_cf,
)

st.set_page_config(
    page_title="Capital Allocation",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Capital Allocation")
st.markdown("---")

# =====================================
# COMPANY SELECTOR
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

bs = get_bs(company_id)
cf = get_cf(company_id)

if bs.empty or cf.empty:
    st.warning("Financial data not available.")
    st.stop()

st.success(f"Showing capital allocation for {company}")

st.markdown("---")

latest_bs = bs.sort_values("year").iloc[-1]
latest_cf = cf.sort_values("year").iloc[-1]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Assets",
        f"{latest_bs['total_assets']:,.0f} Cr"
    )

with c2:
    st.metric(
        "Borrowings",
        f"{latest_bs['borrowings']:,.0f} Cr"
    )

with c3:
    st.metric(
        "Total Liabilities",
        f"{latest_bs['total_liabilities']:,.0f} Cr"
    )

with c4:
    st.metric(
        "Net Cash Flow",
        f"{latest_cf['net_cash_flow']:,.0f} Cr"
    )

st.markdown("---")
 

st.subheader("🏦 Total Assets")

fig = px.line(
    bs,
    x="year",
    y="total_assets",
    markers=True,
    line_shape="spline",
)

fig.update_layout(
    height=500,
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("🏦 Total Assets")

fig = px.line(
    bs,
    x="year",
    y="total_assets",
    markers=True,
    line_shape="spline",
    title="Total Assets"
)

fig.update_layout(
    height=500,
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("💰 Investments")

fig = px.line(
    bs,
    x="year",
    y="investments",
    markers=True,
    line_shape="spline",
    title="Investments"
)

fig.update_layout(
    height=500,
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("💳 Borrowings")

fig = px.line(
    bs,
    x="year",
    y="borrowings",
    markers=True,
    line_shape="spline",
    title="Borrowings"
)

fig.update_layout(
    height=500,
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🏢 Total Liabilities")

fig = px.line(
    bs,
    x="year",
    y="total_liabilities",
    markers=True,
    line_shape="spline",
    title="Total Liabilities"
)

fig.update_layout(
    height=500,
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("💵 Net Cash Flow")

fig = px.line(
    cf,
    x="year",
    y="net_cash_flow",
    markers=True,
    line_shape="spline",
    title="Net Cash Flow"
)

fig.update_layout(
    height=500,
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Cash Flow Activities")

cash_df = cf.melt(
    id_vars="year",
    value_vars=[
        "operating_activity",
        "investing_activity",
        "financing_activity"
    ],
    var_name="Activity",
    value_name="Amount"
)

fig = px.line(
    cash_df,
    x="year",
    y="Amount",
    color="Activity",
    markers=True
)

fig.update_layout(
    height=600,
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

st.download_button(
    "📥 Download Capital Allocation Data",
    bs.to_csv(index=False),
    file_name=f"{company}_capital_allocation.csv",
    mime="text/csv"
)