import streamlit as st

st.set_page_config(
    page_title="N100 Financial Intelligence",
    page_icon="📈",
    layout="wide",
)

st.title("📈 N100 Financial Intelligence Platform")

st.markdown("""
Welcome to the **N100 Financial Intelligence Dashboard**.

### Dashboard Modules

- 🏠 Home
- 🏢 Company Profile
- 🔍 Stock Screener
- 📊 Peer Comparison
- 📈 Trend Analysis
- 🏭 Sector Analysis
- 💰 Capital Allocation
- 📄 Reports
- 📋 Portfolio Summary

Use the **sidebar** to open any module.
""")

st.info("Select a page from the sidebar.")