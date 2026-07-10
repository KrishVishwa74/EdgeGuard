import streamlit as st
import pandas as pd
import time
import os

st.set_page_config(page_title="Edge-Guard Threat Control Panel", layout="wide")

st.title("🛡️ Edge-Guard: Real-Time Threat Control Panel")
st.subheader("Live Edge Machine Anomaly Monitoring Console")

# Sidebar
st.sidebar.header("System Architecture")
st.sidebar.success("C++ Ingestion Engine: ONLINE")
st.sidebar.success("Python Inference Backend: ONLINE")

FILE_NAME = "alerts_log.csv"

if os.path.exists(FILE_NAME):
    try:
        df = pd.read_csv("alerts_log.csv", header=None)

        # Force correct columns
        df.columns = ["Timestamp", "Event_ID", "Frequency", "Payload_Size", "Failed_Logins"]

        # Fill missing values
        df = df.fillna({
            "Event_ID": "UNKNOWN",
            "Frequency": 0,
            "Payload_Size": 0,
            "Failed_Logins": 0
        })

        # Convert safely
        df["Frequency"] = pd.to_numeric(df["Frequency"], errors="coerce").fillna(0)
        df["Failed_Logins"] = pd.to_numeric(df["Failed_Logins"], errors="coerce").fillna(0)

        st.write("DEBUG DATA 👇")
        st.write(df)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Threats", len(df))

        with col2:
            st.metric("Max Frequency", int(df["Frequency"].max()))

        with col3:
            st.metric("Critical Alerts", int((df["Failed_Logins"] > 5).sum()))

        st.dataframe(df)

    except Exception as e:
        st.error(f"Error reading data: {e}")

else:
    st.info("🔄 Awaiting initial real-time alerts from the C++ Engine...")

time.sleep(2)
st.rerun()