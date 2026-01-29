import streamlit as st
import pandas as pd
import serial

# Thresholds for anomaly detection
VIBRATION_LIMIT = 5.0  # g-force threshold

st.title("📡 Live Vibration Dashboard (ADXL345)")

# Connect to Arduino (adjust COM port if needed)
ser = serial.Serial('COM4', 9600)

data = []
placeholder = st.empty()

while True:
    line = ser.readline().decode('utf-8').strip()
    if line and not line.startswith("Time"):
        parts = line.split(',')
        if len(parts) == 4:  # Time, X, Y, Z
            data.append(parts)
            if len(data) > 200:  # keep last 200 readings
                data = data[-200:]

            df = pd.DataFrame(data, columns=["Time (min)", "Accel_X", "Accel_Y", "Accel_Z"])
            df = df.astype(float)

            with placeholder.container():
                st.line_chart(df[["Accel_X", "Accel_Y", "Accel_Z"]])

                # Anomaly detection
                latest_x = df["Accel_X"].iloc[-1]
                latest_y = df["Accel_Y"].iloc[-1]
                latest_z = df["Accel_Z"].iloc[-1]

                if abs(latest_x) > VIBRATION_LIMIT or abs(latest_y) > VIBRATION_LIMIT or abs(latest_z) > VIBRATION_LIMIT:
                    st.error("⚠️ Vibration anomaly detected! Possible causes: imbalance, misalignment, loose parts, or bearing wear.")
