import streamlit as st
import pandas as pd
import serial
import time

# Thresholds
VIBRATION_LIMIT = 5.0
ALARM_INTERVAL = 30  # seconds between repeated alarms

st.title("📡 Live Vibration Dashboard (ADXL345)")

# Connect to Arduino (adjust COM port if needed)
ser = serial.Serial('COM4', 9600)

# Session state to persist across reruns
if "data" not in st.session_state:
    st.session_state.data = []
if "anomalies" not in st.session_state:
    st.session_state.anomalies = []
if "last_alarm_time" not in st.session_state:
    st.session_state.last_alarm_time = 0

placeholder_chart = st.empty()
placeholder_table = st.empty()

# --- Read one line per rerun ---
line = ser.readline().decode('utf-8').strip()
if line and not line.startswith("Time"):
    parts = line.split(',')
    if len(parts) == 4:  # Time, X, Y, Z
        st.session_state.data.append(parts)
        if len(st.session_state.data) > 200:
            st.session_state.data = st.session_state.data[-200:]

        # Convert to DataFrame
        df = pd.DataFrame(st.session_state.data, columns=["Time (min)", "Accel_X", "Accel_Y", "Accel_Z"])
        df = df.astype(float)

        # --- Plot live chart ---
        with placeholder_chart.container():
            st.line_chart(df[["Accel_X", "Accel_Y", "Accel_Z"]])

        # Latest values
        latest_x = df["Accel_X"].iloc[-1]
        latest_y = df["Accel_Y"].iloc[-1]
        latest_z = df["Accel_Z"].iloc[-1]

        # --- Anomaly detection ---
        if abs(latest_x) > VIBRATION_LIMIT or abs(latest_y) > VIBRATION_LIMIT or abs(latest_z) > VIBRATION_LIMIT:
            current_time = time.time()
            if current_time - st.session_state.last_alarm_time > ALARM_INTERVAL:
                comment = "⚠️ Vibration anomaly detected! Possible causes: imbalance, misalignment, loose parts, or bearing wear."
                st.session_state.anomalies.append([df["Time (min)"].iloc[-1], latest_x, latest_y, latest_z, comment])
                st.error(comment)
                st.session_state.last_alarm_time = current_time

        # --- Show anomaly table ---
        if st.session_state.anomalies:
            anomalies_df = pd.DataFrame(st.session_state.anomalies,
                                        columns=["Time (min)", "Accel_X", "Accel_Y", "Accel_Z", "Comment"])
            with placeholder_table.container():
                st.subheader("📋 Anomaly Log")
                st.table(anomalies_df)
