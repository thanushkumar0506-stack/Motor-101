import streamlit as st
import pandas as pd
import serial
import time
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

# Store data and anomalies
data = []
last_alarm_time = 0
placeholder_chart = st.empty()
placeholder_table = st.empty()

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
    except Exception as e:
        st.error(f"❌ Serial read error: {e}")
        break

    if line and not line.startswith("Time"):
        parts = line.split(',')
        if len(parts) == 4:  # Time, X, Y, Z
            data.append(parts)
            if len(data) > 200:
                data = data[-200:]

            # Build DataFrame
            df = pd.DataFrame(data, columns=["Time (min)", "Accel_X", "Accel_Y", "Accel_Z"])
            df = df.astype(float)

            # Add Comment column (default empty)
            df["Comment"] = ""

            latest_x = df["Accel_X"].iloc[-1]
            latest_y = df["Accel_Y"].iloc[-1]
            latest_z = df["Accel_Z"].iloc[-1]

            # --- Anomaly detection ---
            if latest_x > VIBRATION_LIMIT or latest_y > VIBRATION_LIMIT or latest_z > VIBRATION_LIMIT:
                current_time = time.time()
                if current_time - last_alarm_time > ALARM_INTERVAL:
                    comment = "⚠️ Vibration anomaly detected! Possible causes: imbalance, misalignment, loose parts, or bearing wear."
                    st.error(comment)
                    # Add comment to the latest row
                    df.loc[df.index[-1], "Comment"] = comment
                    last_alarm_time = current_time

            # --- Show chart ---
            with placeholder_chart.container():
                st.line_chart(df[["Accel_X", "Accel_Y", "Accel_Z"]])

            # --- Show table ---
            with placeholder_table.container():
                st.subheader("📋 Data Log with Anomaly Comments")
                st.dataframe(df)

    time.sleep(1)
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

# Store data and anomalies
data = []
last_alarm_time = 0
placeholder_chart = st.empty()
placeholder_table = st.empty()

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
    except Exception as e:
        st.error(f"❌ Serial read error: {e}")
        break

    if line and not line.startswith("Time"):
        parts = line.split(',')
        if len(parts) == 4:  # Time, X, Y, Z
            data.append(parts)
            if len(data) > 200:
                data = data[-200:]

            # Build DataFrame
            df = pd.DataFrame(data, columns=["Time (min)", "Accel_X", "Accel_Y", "Accel_Z"])
            df = df.astype(float)

            # Add Comment column (default empty)
            df["Comment"] = ""

            latest_x = df["Accel_X"].iloc[-1]
            latest_y = df["Accel_Y"].iloc[-1]
            latest_z = df["Accel_Z"].iloc[-1]

            # --- Anomaly detection ---
            if latest_x > VIBRATION_LIMIT or latest_y > VIBRATION_LIMIT or latest_z > VIBRATION_LIMIT:
                current_time = time.time()
                if current_time - last_alarm_time > ALARM_INTERVAL:
                    comment = "⚠️ Vibration anomaly detected! Possible causes: imbalance, misalignment, loose parts, or bearing wear."
                    st.error(comment)
                    # Add comment to the latest row
                    df.loc[df.index[-1], "Comment"] = comment
                    last_alarm_time = current_time

            # --- Show chart ---
            with placeholder_chart.container():
                st.line_chart(df[["Accel_X", "Accel_Y", "Accel_Z"]])

            # --- Show table ---
            with placeholder_table.container():
                st.subheader("📋 Data Log with Anomaly Comments")
                st.dataframe(df)

    time.sleep(1)

