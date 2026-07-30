import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Reports",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Financial Reports")

# -------------------------------------
# Report Summary
# -------------------------------------
summary_file = "outputs/report_summary.csv"

if not os.path.exists(summary_file):
    st.error("report_summary.csv not found.")
    st.stop()

summary_df = pd.read_csv(summary_file)

st.subheader("📊 Report Summary")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Reports",
    len(summary_df)
)

col2.metric(
    "Average PDF Size",
    f"{summary_df['size_kb'].mean():.2f} KB"
)

col3.metric(
    "Largest Report",
    summary_df.loc[
        summary_df["size_kb"].idxmax(),
        "company_id"
    ]
)

st.markdown("---")

# -------------------------------------
# Reports Table
# -------------------------------------
st.subheader("Generated PDF Reports")

st.dataframe(
    summary_df,
    use_container_width=True
)

st.markdown("---")

# -------------------------------------
# Select Company
# -------------------------------------
company = st.selectbox(
    "Select Company",
    summary_df["company_id"]
)

selected = summary_df[
    summary_df["company_id"] == company
].iloc[0]

st.subheader("Report Details")

c1, c2 = st.columns(2)

c1.metric(
    "Company",
    selected["company_id"]
)

c2.metric(
    "PDF Size",
    f"{selected['size_kb']} KB"
)

st.write("**Filename:**", selected["filename"])

st.markdown("---")

# -------------------------------------
# Download Summary CSV
# -------------------------------------
csv = summary_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Report Summary",
    csv,
    file_name="report_summary.csv",
    mime="text/csv"
)

# -------------------------------------
# List PDF Files
# -------------------------------------
st.subheader("Available PDF Files")

pdf_folder = "outputs/pdf_reports"

if os.path.exists(pdf_folder):

    pdf_files = sorted(
        [
            f for f in os.listdir(pdf_folder)
            if f.endswith(".pdf")
        ]
    )

    if pdf_files:
        for pdf in pdf_files:
            st.success(pdf)
    else:
        st.warning("No PDF reports found.")

else:
    st.warning("PDF reports folder not found.")

st.success("Reports module loaded successfully.")