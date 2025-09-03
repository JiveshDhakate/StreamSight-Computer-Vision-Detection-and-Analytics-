import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
from pathlib import Path
from PIL import Image

import base64
from io import BytesIO

# === CONFIG ===
APP_TITLE = "StreamSight: Temple Bar Footfall Analytics"
CAMERA_NAME = "EarthCam Live: Dublin, Ireland"
MINUTE_DIR = "data/minute_logs"
BIN_DIR = "data/15min_bins"
LIVE_IMAGE = "data/live/latest.jpg"

# === PAGE SETUP ===
st.set_page_config(
    page_title=APP_TITLE,
    layout="wide",
)

def img_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# === Auto-refresh every 10 seconds ===
st_autorefresh(interval=5_000, limit=None, key="auto_refresh")

# === HEADER ===
st.title("🎥 StreamSight: Temple Bar Footfall Dashboard")
st.markdown(f"📍 **Live Feed:** *{CAMERA_NAME}*")
st.markdown("Detecting pedestrians from YouTube livestream using YOLO object detection")

st.divider()
# === Helper to load CSVs ===
@st.cache_data(show_spinner=False, ttl=5)
def load_data(folder_path):
    folder = Path(folder_path)
    all_data = []

    for file in sorted(folder.glob("*.csv")):
        df = pd.read_csv(file)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        all_data.append(df)

    if all_data:
        return pd.concat(all_data).sort_values("timestamp")
    return pd.DataFrame()

# === Load Logs ===
minute_df = load_data(MINUTE_DIR)
bin_df = load_data(BIN_DIR)

# === METRICS ===
latest_min = minute_df["people_avg"].iloc[-1] if not minute_df.empty else "–"
latest_bin = bin_df["people_avg"].iloc[-1] if not bin_df.empty else "–"

col_metrics = st.columns(2)
col_metrics[0].metric("👣 Last Minute Footfall", latest_min)
col_metrics[1].metric("⏱️ Last 15-Min Avg", latest_bin)

# === CHARTS ===
st.subheader("📈 Historical Footfall Trends")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👣 People Count (Per Minute)")
    if not minute_df.empty:
        st.line_chart(minute_df.set_index("timestamp")["people_avg"])
    else:
        st.info("Waiting for minute-level logs...")

with col2:
    st.markdown("### ⏱️ People Count (15-Min Bins)")
    if not bin_df.empty:
        st.line_chart(bin_df.set_index("timestamp")["people_avg"])
    else:
        st.info("Waiting for 15-minute bin data...")

# === LIVE FRAME ===
st.divider()
st.subheader("🖼️ Latest YOLO Frame (Live Detection)")

if Path(LIVE_IMAGE).exists():
    img = Image.open(LIVE_IMAGE)
    st.markdown(
        f"""
        <div style='text-align: center;'>
            <img src='data:image/jpeg;base64,{img_to_base64(img)}' width='900'/>
            <p style='font-size: 0.9rem; color: gray;'>Live Detection Frame (updated every 5s)</p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("No live image found yet. Run the detection script to see real-time visuals.")


# === FOOTER ===
st.divider()
st.markdown("🚀 Powered by **StreamSight** | Live YOLOv11 Detection • Streamlit • EarthCam • Dublin 🇮🇪 | Creator - Jivesh Dhakate")
