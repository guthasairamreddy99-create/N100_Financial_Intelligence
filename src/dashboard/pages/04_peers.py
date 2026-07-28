import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.utils.db import (
    get_peers,
    get_companies,
    get_ratios,
)

st.set_page_config(
    page_title="Peer Comparison",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Peer Comparison")
st.markdown("---")


# =====================================================
# LOAD DATA
# =====================================================

peer_df = get_peers()
companies_df = get_companies()

if peer_df.empty:
    st.warning("No peer groups found.")
    st.stop()

if companies_df.empty:
    st.warning("Company data not found.")
    st.stop()


# =====================================================
# COMPANY NAME MAP
# =====================================================

company_map = {}

if "id" in companies_df.columns and "company_name" in companies_df.columns:
    company_map = dict(
        zip(
            companies_df["id"],
            companies_df["company_name"]
        )
    )

peer_df["company_name"] = peer_df["company_id"].map(company_map)


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Filters")

peer_groups = sorted(
    peer_df["peer_group_name"].dropna().unique()
)

selected_group = st.sidebar.selectbox(
    "Peer Group",
    peer_groups
)


# =====================================================
# FILTER PEERS
# =====================================================

group_df = peer_df[
    peer_df["peer_group_name"] == selected_group
].copy()

if group_df.empty:
    st.warning("No companies available.")
    st.stop()

group_df["Benchmark"] = group_df["is_benchmark"].replace(
    {
        1: "⭐ Benchmark",
        True: "⭐ Benchmark",
        0: "",
        False: ""
    }
)

st.subheader(selected_group)

st.dataframe(
    group_df[
        [
            "company_name",
            "company_id",
            "Benchmark"
        ]
    ],
    use_container_width=True,
)


# =====================================================
# BUILD METRIC TABLE
# =====================================================

comparison = []

for _, row in group_df.iterrows():

    ticker = row["company_id"]

    ratios = get_ratios(ticker)

    if ratios.empty:
        continue

    latest = ratios.sort_values(
        "year"
    ).iloc[-1]

    comparison.append(
        {
            "Company": company_map.get(
                ticker,
                ticker
            ),
            "Ticker": ticker,
            "Benchmark": row["is_benchmark"],
            "ROE": latest["return_on_equity_pct"],
            "Net Margin": latest["net_profit_margin_pct"],
            "Operating Margin": latest[
                "operating_profit_margin_pct"
            ],
            "Debt/Equity": latest["debt_to_equity"],
            "Interest Coverage": latest[
                "interest_coverage"
            ],
            "Asset Turnover": latest[
                "asset_turnover"
            ],
            "EPS": latest[
                "earnings_per_share"
            ],
            "Free Cash Flow": latest[
                "free_cash_flow_cr"
            ],
            "Cash From Operations": latest[
                "cash_from_operations_cr"
            ],
        }
    )

comparison_df = pd.DataFrame(comparison)

if comparison_df.empty:
    st.warning("No financial ratios available.")
    st.stop()


# =====================================================
# KPI CARDS
# =====================================================

st.markdown("## 📌 Peer Group Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Companies",
        len(comparison_df)
    )

with c2:
    st.metric(
        "Average ROE",
        f"{comparison_df['ROE'].mean():.2f}%"
    )

with c3:
    st.metric(
        "Average Margin",
        f"{comparison_df['Net Margin'].mean():.2f}%"
    )

with c4:
    st.metric(
        "Average Debt/Equity",
        f"{comparison_df['Debt/Equity'].mean():.2f}"
    )

st.markdown("---")

# =====================================================
# COMPARISON TABLE
# =====================================================

st.subheader("📋 Financial Comparison")

display_df = comparison_df.copy()

display_df["Benchmark"] = display_df["Benchmark"].replace(
    {
        1: "⭐",
        True: "⭐",
        0: "",
        False: ""
    }
)

display_df = display_df.sort_values(
    "ROE",
    ascending=False
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")


# =====================================================
# ROE CHART
# =====================================================

st.subheader("📈 Return on Equity (%)")

fig = px.bar(
    comparison_df.sort_values(
        "ROE",
        ascending=False
    ),
    x="Company",
    y="ROE",
    text="ROE",
)

fig.update_layout(
    xaxis_title="Company",
    yaxis_title="ROE (%)",
    height=500,
)

fig.update_layout(
    xaxis_tickangle=-35
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================================
# NET PROFIT MARGIN
# =====================================================

st.subheader("💰 Net Profit Margin (%)")

fig = px.bar(
    comparison_df.sort_values(
        "Net Margin",
        ascending=False
    ),
    x="Company",
    y="Net Margin",
    text="Net Margin",
)

fig.update_layout(
    height=500,
    xaxis_title="Company",
    yaxis_title="Net Margin (%)",
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================================
# DEBT TO EQUITY
# =====================================================

st.subheader("🏦 Debt to Equity")

fig = px.bar(
    comparison_df.sort_values(
        "Debt/Equity"
    ),
    x="Company",
    y="Debt/Equity",
    text="Debt/Equity",
)

fig.update_layout(
    height=500,
    xaxis_title="Company",
    yaxis_title="Debt / Equity",
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================================
# EPS
# =====================================================

st.subheader("💹 Earnings Per Share")

fig = px.bar(
    comparison_df.sort_values(
        "EPS",
        ascending=False
    ),
    x="Company",
    y="EPS",
    text="EPS",
)

fig.update_layout(
    height=500,
    xaxis_title="Company",
    yaxis_title="EPS",
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")