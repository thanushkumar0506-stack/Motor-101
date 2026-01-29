import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Predictive Maintenance Dashboard", layout="wide")

st.title("🛠️ Predictive Maintenance Dashboard")
st.markdown("Monitor motor health using sensor trends and AI-based diagnostics.")

# Upload CSV
uploaded_file = st.file_uploader("Upload sensor data CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Show raw data
    with st.expander("📄 Raw Data"):
        st.dataframe(df)

    # Plot trends
    st.subheader("📈 Sensor Trends Over Time")
    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    axs[0].plot(df["Time (s)"], df["Temperature (°C)"], color='red')
    axs[0].set_ylabel("Temperature (°C)")
    axs[0].grid(True)

    axs[1].plot(df["Time (s)"], df["Current (A)"], color='blue')
    axs[1].set_ylabel("Current (A)")
    axs[1].grid(True)

    axs[2].plot(df["Time (s)"], df["Vibration"], color='green')
    axs[2].set_ylabel("Vibration")
    axs[2].set_xlabel("Time (s)")
    axs[2].grid(True)

    st.pyplot(fig)

    # Show AI alerts
    st.subheader("⚠️ AI-Detected Anomalies")
    alerts = df[df["AI Alert"].notna()][["Time (s)", "AI Alert"]]
    if not alerts.empty:
        st.dataframe(alerts)
    else:
        st.success("No anomalies detected in the uploaded data.")
else:
    st.info("Upload a CSV file to begin.")