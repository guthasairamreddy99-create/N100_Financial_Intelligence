import sys
from pathlib import Path
import plotly.express as px

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import streamlit as st

from dashboard.utils.db import (
    get_companies,
    get_company_details,
    get_pl,
    get_ratios,
)

st.set_page_config(page_title="Company Profile", layout="wide")

st.title("🏢 Company Profile")

st.write("Search and explore any Nifty 100 company.")

companies = get_companies()

selected_company = st.selectbox(
    "Select Company",
    companies
)

company = get_company_details(selected_company)

if company.empty:
    st.error("Company not found.")
    st.stop()

company = company.iloc[0]

st.success(f"Selected Company: {selected_company}")

st.divider()

col_logo, col_title = st.columns([1, 5])

with col_logo:
    st.image(
        company["company_logo"],
        width=100
    )

with col_title:
    st.subheader(company["company_name"])

# Company Information
st.write(f"**Company ID:** {company['id']}")
st.write(f"**Face Value:** {company['face_value']}")
st.write(f"**Book Value:** {company['book_value']}")

st.divider()

# Latest Financial KPIs
ratios = get_ratios(selected_company)

if not ratios.empty:

    latest_ratio = (
        ratios.sort_values("year")
        .iloc[-1]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "ROE",
            f"{latest_ratio['return_on_equity_pct']:.2f}%"
        )

    with col2:
        st.metric(
            "Net Margin",
            f"{latest_ratio['net_profit_margin_pct']:.2f}%"
        )

    with col3:
        st.metric(
            "Debt / Equity",
            f"{latest_ratio['debt_to_equity']:.2f}"
        )

    with col4:
        st.metric(
            "Asset Turnover",
            f"{latest_ratio['asset_turnover']:.2f}"
        )

    col5, col6, col7 = st.columns(3)

    with col5:
        st.metric(
            "Interest Coverage",
            f"{latest_ratio['interest_coverage']:.2f}"
        )

    with col6:
        st.metric(
            "Free Cash Flow",
            f"{latest_ratio['free_cash_flow_cr']:.2f} Cr"
        )

    with col7:
        st.metric(
            "EPS",
            f"{latest_ratio['earnings_per_share']:.2f}"
        )

else:
    st.warning("Financial ratio data not available.")

st.divider()

st.subheader("Useful Links")

col1, col2, col3 = st.columns(3)

with col1:
    st.link_button(
        "🌐 Website",
        company["website"]
    )

with col2:
    st.link_button(
        "📈 NSE Profile",
        company["nse_profile"]
    )

with col3:
    st.link_button(
        "🏦 BSE Profile",
        company["bse_profile"]
    )

st.divider()

st.subheader("About Company")

st.write(company["about_company"])

st.divider()

st.subheader("Revenue Trend")

pl = get_pl(selected_company)

if not pl.empty:

    fig = px.line(
        pl,
        x="year",
        y="sales",
        markers=True,
        title="Sales Over Years"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.warning("No Profit & Loss data available.")

st.divider()

st.subheader("Net Profit Trend")

if not pl.empty:

    fig = px.line(
        pl,
        x="year",
        y="net_profit",
        markers=True,
        title="Net Profit Over Years"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.warning("No Net Profit data available.")

st.divider()

st.subheader("ROE Trend")

ratios = get_ratios(selected_company)

if not ratios.empty:

    fig = px.line(
        ratios,
        x="year",
        y="return_on_equity_pct",
        markers=True,
        title="Return on Equity (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.warning("No ROE data available.")

st.divider()

st.subheader("Free Cash Flow Trend")

if not ratios.empty:

    fig = px.line(
        ratios,
        x="year",
        y="free_cash_flow_cr",
        markers=True,
        title="Free Cash Flow (Cr)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.warning("No Free Cash Flow data available.")

st.divider()

st.subheader("Cash From Operations Trend")

if not ratios.empty:

    fig = px.line(
        ratios,
        x="year",
        y="cash_from_operations_cr",
        markers=True,
        title="Cash From Operations (Cr)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.warning("No Cash From Operations data available.")

st.divider()

st.subheader("Financial Ratios History")

if not ratios.empty:

    display_ratios = ratios.copy()

    st.dataframe(
        display_ratios,
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("No financial ratio history available.")