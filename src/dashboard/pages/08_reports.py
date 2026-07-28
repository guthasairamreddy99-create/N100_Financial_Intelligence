import streamlit as st
import pandas as pd

from utils.db import (
    get_companies,
    get_company_details,
    get_pl,
    get_bs,
    get_cf,
    get_ratios,
)

st.set_page_config(
    page_title="Annual Reports",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Annual Reports")
st.markdown("---")

# ==========================================
# COMPANY SELECTOR
# ==========================================

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company_id = companies.loc[
    companies["company_name"] == company,
    "id"
].values[0]

details = get_company_details(company_id)
pl = get_pl(company_id)
bs = get_bs(company_id)
cf = get_cf(company_id)
ratios = get_ratios(company_id)

st.success(f"Annual Report for {company}")

st.markdown("---")

st.header("🏢 Company Information")

st.dataframe(
    details,
    use_container_width=True,
    hide_index=True,
)

st.header("💰 Profit & Loss")

st.dataframe(
    pl,
    use_container_width=True,
    hide_index=True,
)

st.header("🏦 Balance Sheet")

st.dataframe(
    bs,
    use_container_width=True,
    hide_index=True,
)

st.header("💵 Cash Flow")

st.dataframe(
    cf,
    use_container_width=True,
    hide_index=True,
)

st.header("📊 Financial Ratios")

st.dataframe(
    ratios,
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

report = pd.concat(
    [
        details,
        pl,
        bs,
        cf,
        ratios,
    ],
    axis=1,
)

st.download_button(
    "📥 Download Complete Report",
    report.to_csv(index=False),
    file_name=f"{company}_annual_report.csv",
    mime="text/csv",
)