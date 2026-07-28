import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_sectors,
    get_companies,
    get_market_cap,
    get_ratios,
)

st.set_page_config(
    page_title="Sector Analysis",
    page_icon="🏭",
    layout="wide",
)

st.title("🏭 Sector Analysis")
st.markdown("---")

# ==========================================
# LOAD DATA
# ==========================================

sector_df = get_sectors()
companies_df = get_companies()
market_df = get_market_cap()

if sector_df.empty:
    st.warning("Sector data not available.")
    st.stop()

# ==========================================
# SECTOR SELECTOR
# ==========================================

sector_name = st.selectbox(
    "Select Sector",
    sorted(sector_df["broad_sector"].dropna().unique())
)

selected = sector_df[
    sector_df["broad_sector"] == sector_name
].copy()

st.success(f"Showing analysis for {sector_name}")

st.markdown("---")

# ==========================================
# COMPANY TABLE
# ==========================================

company_map = dict(
    zip(
        companies_df["id"],
        companies_df["company_name"]
    )
)

selected["Company"] = selected["company_id"].map(company_map)

st.subheader("🏢 Companies")

st.dataframe(
    selected[
        [
            "Company",
            "company_id"
        ]
    ],
    use_container_width=True,
)

# ==========================================
# KPI DATA
# ==========================================

rows = []

for company in selected["company_id"]:

    ratios = get_ratios(company)

    if ratios.empty:
        continue

    latest = ratios.sort_values("year").iloc[-1]

    rows.append({
        "Company": company_map.get(company, company),
        "ROE": latest["return_on_equity_pct"],
        "Net Margin": latest["net_profit_margin_pct"],
        "Debt": latest["debt_to_equity"],
    })

summary = pd.DataFrame(rows)

st.markdown("## 📌 Sector Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Companies",
        len(summary)
    )

with c2:
    st.metric(
        "Average ROE",
        f"{summary['ROE'].mean():.2f}%"
    )

with c3:
    st.metric(
        "Average Margin",
        f"{summary['Net Margin'].mean():.2f}%"
    )

with c4:
    st.metric(
        "Average Debt",
        f"{summary['Debt'].mean():.2f}"
    )

st.markdown("---")

st.subheader("📈 Return on Equity")

fig = px.bar(
    summary.sort_values(
        "ROE",
        ascending=False
    ),
    x="Company",
    y="ROE",
    text="ROE",
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside",
)

fig.update_layout(
    height=500,
)

fig.update_xaxes(
    tickangle=-35
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================
# MARKET CAP ANALYSIS
# ==========================================

market_latest = market_df.sort_values("year").groupby("company_id").tail(1)

market_latest["Company"] = market_latest["company_id"].map(company_map)

market_sector = market_latest[
    market_latest["company_id"].isin(selected["company_id"])
].copy()

st.subheader("💰 Market Capitalization")

fig = px.bar(
    market_sector.sort_values(
        "market_cap_crore",
        ascending=False
    ),
    x="Company",
    y="market_cap_crore",
    text="market_cap_crore",
)

fig.update_traces(
    texttemplate="%{text:.0f}",
    textposition="outside",
)

fig.update_layout(height=500)

fig.update_xaxes(
    tickangle=-35
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================
# NET PROFIT MARGIN
# ==========================================

st.subheader("💵 Net Profit Margin")

fig = px.bar(
    summary.sort_values(
        "Net Margin",
        ascending=False
    ),
    x="Company",
    y="Net Margin",
    text="Net Margin",
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside",
)

fig.update_layout(height=500)

fig.update_xaxes(
    tickangle=-35
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================
# DEBT TO EQUITY
# ==========================================

st.subheader("🏦 Debt to Equity")

fig = px.bar(
    summary.sort_values(
        "Debt"
    ),
    x="Company",
    y="Debt",
    text="Debt",
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside",
)

fig.update_layout(height=500)

fig.update_xaxes(
    tickangle=-35
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================
# MARKET CAP DISTRIBUTION
# ==========================================

st.subheader("🥧 Market Cap Distribution")

fig = px.pie(
    market_sector,
    names="Company",
    values="market_cap_crore",
)

fig.update_layout(
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================
# EXPORT
# ==========================================

st.markdown("---")

export_df = summary.copy()

st.download_button(
    label="📥 Download Sector Analysis CSV",
    data=export_df.to_csv(index=False),
    file_name=f"{sector_name}_sector_analysis.csv",
    mime="text/csv",
)