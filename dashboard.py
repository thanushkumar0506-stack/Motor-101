import streamlit as st
import pandas as pd
import serial
import time
import winsound  # for beep alarm

VIBRATION_LIMIT = 5.0
ALARM_INTERVAL = 30

st.title("📡 Live Vibration Dashboard (ADXL345)")
ser = serial.Serial('COM4', 9600)

data = []
last_alarm_time = 0
placeholder = st.empty()

while True:
    line = ser.readline().decode('utf-8').strip()
    if line and not line.startswith("Time"):
        parts = line.split(',')
        if len(parts) == 4:
            data.append(parts)
            if len(data) > 200:
                data = data[-200:]

            df = pd.DataFrame(data, columns=["Time (min)", "Accel_X", "Accel_Y", "Accel_Z"])
            df = df.astype(float)

            with placeholder.container():
                st.line_chart(df[["Accel_X", "Accel_Y", "Accel_Z"]])

                latest_x = df["Accel_X"].iloc[-1]
                latest_y = df["Accel_Y"].iloc[-1]
                latest_z = df["Accel_Z"].iloc[-1]

                if abs(latest_x) > VIBRATION_LIMIT or abs(latest_y) > VIBRATION_LIMIT or abs(latest_z) > VIBRATION_LIMIT:
                    current_time = time.time()
                    if current_time - last_alarm_time > ALARM_INTERVAL:
                        # 🔔 Sound alarm
                        winsound.Beep(1000, 500)
                        st.error("⚠️ Vibration anomaly detected! Possible imbalance, misalignment, or bearing wear.")
                        last_alarm_time = current_time

    time.sleep(1)
