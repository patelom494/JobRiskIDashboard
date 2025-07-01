import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import requests

# Load Lottie animation from a URL
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def main():
    st.set_page_config(page_title="Universal Job Risk Dashboard", layout="wide")

    # Title with animation
    st.title("📊 Job Risk Dashboard")
    lottie_url = "https://assets2.lottiefiles.com/packages/lf20_touohxv0.json"
    lottie_alert = load_lottie_url(lottie_url)
    if lottie_alert:
        st_lottie(lottie_alert, height=150, key="alert")
    else:
        st.warning("⚠️ Could not load Lottie animation.")

    # Upload section
    st.sidebar.header("📁 Upload CSV")
    uploaded_file = st.sidebar.file_uploader("Upload any CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            st.success("✅ File uploaded successfully.")

            # Let user map columns
            st.sidebar.header("🔧 Map Columns")
            columns = df.columns.tolist()

            job_id_col = st.sidebar.selectbox("Select Job ID column", columns)
            status_col = st.sidebar.selectbox("Select Status column", columns)
            risk_col = st.sidebar.selectbox("Select Risk Score column", columns)

            # Show basic table
            st.subheader("📋 Data Preview")
            st.dataframe(df[[job_id_col, status_col, risk_col]].head())

            # Filter by status
            status_filter = st.sidebar.selectbox("🔎 Filter by Status", ["All"] + sorted(df[status_col].dropna().unique().tolist()))
            filtered_df = df if status_filter == "All" else df[df[status_col] == status_filter]

            # Convert risk to numeric (in case it's string)
            filtered_df[risk_col] = pd.to_numeric(filtered_df[risk_col], errors="coerce")

            # Chart
            st.subheader("📊 Risk by Job")
            fig = px.bar(filtered_df, x=job_id_col, y=risk_col, color=status_col, title="Delay Risk by Job")
            st.plotly_chart(fig, use_container_width=True)

            # Insights
            st.subheader("🧠 Predictive Insights")
            st.markdown("- Jobs above *0.7 risk score* flagged for proactive attention.")
            st.markdown("- ML-ready format with adaptable schema.")

            # Alert high-risk jobs
            high_risk_jobs = filtered_df[filtered_df[risk_col] > 0.7][job_id_col].dropna().tolist()
            if high_risk_jobs:
                st.warning(f"⚠️ Jobs at high risk: {', '.join(map(str, high_risk_jobs))}")
            else:
                st.success("✅ No high-risk jobs found.")

        except Exception as e:
            st.error(f"❌ Failed to process file: {e}")
    else:
        st.info("📤 Upload a CSV file to get started.")

if __name__ == "__main__":
    main()