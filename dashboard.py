import streamlit as st
import pandas as pd
import serial
import time

# --- Settings ---
VIBRATION_LIMIT = 5.0   # g-force threshold for anomaly
ALARM_INTERVAL = 30     # seconds between repeated alarms

st.title("📡 Live Vibration Dashboard (ADXL345)")

# Try opening COM4 safely
try:
    ser = serial.Serial('COM4', 9600, timeout=1)
except serial.SerialException as e:
    st.error(f"❌ Could not open COM4: {e}")
    st.stop()

# Use session_state to persist data and anomalies
if "data" not in st.session_state:
    st.session_state.data = []
if "last_alarm_time" not in st.session_state:
    st.session_state.last_alarm_time = 0

placeholder_chart = st.empty()
placeholder_table = st.empty()

# --- Read one line per rerun ---
try:
    line = ser.readline().decode('utf-8', errors='ignore').strip()
except Exception as e:
    st.error(f"❌ Serial read error: {e}")
    line = ""

if line and not line.startswith("Time"):
    parts = line.split(',')
    if len(parts) == 4:  # Time, X, Y, Z
        st.session_state.data.append(parts)
        if len(st.session_state.data) > 200:
            st.session_state.data = st.session_state.data[-200:]

        # Build DataFrame
        df = pd.DataFrame(st.session_state.data, columns=["Time (ms)", "Accel_X", "Accel_Y", "Accel_Z"])
        df = df.astype(float)

        # Add Comment column if not exists
        if "Comment" not in df.columns:
            df["Comment"] = ""

        latest_x = df["Accel_X"].iloc[-1]
        latest_y = df["Accel_Y"].iloc[-1]
        latest_z = df["Accel_Z"].iloc[-1]

        # --- Anomaly detection ---
        if latest_x > VIBRATION_LIMIT or latest_y > VIBRATION_LIMIT or latest_z > VIBRATION_LIMIT:
            current_time = time.time()
            if current_time - st.session_state.last_alarm_time > ALARM_INTERVAL:
                comment = "⚠️ Vibration anomaly detected! Possible causes: imbalance, misalignment, loose parts, or bearing wear."
                st.error(comment)
                # Add comment to the latest row
                df.loc[df.index[-1], "Comment"] = comment
                st.session_state.last_alarm_time = current_time

        # --- Show chart ---
        with placeholder_chart.container():
            st.line_chart(df[["Accel_X", "Accel_Y", "Accel_Z"]])

        # --- Show table ---
        with placeholder_table.container():
            st.subheader("📋 Data Log with Anomaly Comments")
            st.dataframe(df)
