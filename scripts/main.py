import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.detect import run_yolo_stream
from app.binning import aggregate_and_save
import multiprocessing
import subprocess
import time

YOUTUBE_URL = "https://www.youtube.com/watch?v=u4UZ4UvZXrg&ab_channel=EarthCam"

def detection_loop():
    duration_minutes = 60
    interval_sec = 60

    for i in range(duration_minutes):
        print(f"🔄 Running detection cycle {i+1}/{duration_minutes}")
        records = run_yolo_stream(YOUTUBE_URL, fps=1, duration_sec=interval_sec)
        aggregate_and_save(records)
        print("✅ Saved bins for this minute.\n")
        time.sleep(1)

def dashboard_loop():
    print("📊 Launching Streamlit dashboard...")
    subprocess.run(["streamlit", "run", "scripts/streamlit_dashboard.py"])

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=detection_loop)
    p2 = multiprocessing.Process(target=dashboard_loop)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
