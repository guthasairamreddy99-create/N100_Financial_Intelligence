import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Nifty 100 Analytics Dashboard")

st.markdown(
    """
Welcome to the **N100 Financial Intelligence Platform**.

### Available Dashboard Modules

- 🏠 Home
- 🏢 Company Profile
- 🔍 Stock Screener
- 📊 Peer Comparison
- 📈 Trend Analysis
- 🏭 Sector Analysis
- 💰 Capital Allocation
- 📄 Annual Reports

Use the sidebar to navigate through the dashboard.
"""
)

st.success("Dashboard initialized successfully!")