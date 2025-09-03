import subprocess
import numpy as np
import cv2
import time
import pandas as pd
from datetime import datetime
from ultralytics import YOLO
import os

# Config
youtube_url = "https://www.youtube.com/watch?v=u4UZ4UvZXrg"
width, height = 1920, 1080  # expected resolution from the stream
frame_size = width * height * 3  # for bgr24
fps = 1
duration_secs = 60
output_path = "data/footfal3.csv"

# Create output dir
os.makedirs("data", exist_ok=True)

# Prepare ffmpeg + streamlink pipeline
cmd = (
    f'streamlink --stdout "{youtube_url}" best | '
    'ffmpeg -i - -f rawvideo -pix_fmt bgr24 -'
)

# Start subprocess
proc = subprocess.Popen(
    cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
)

# Load YOLOv11 (or yolov8n)
model = YOLO("yolo11n.pt")

# Init frame counter and results
start_time = time.time()
frame_number = 0
records = []

print("⏱️ Running for 1 minute @ 1 FPS...")

while time.time() - start_time < duration_secs:
    raw_frame = proc.stdout.read(frame_size)

    if len(raw_frame) != frame_size:
        print(f"⚠️ Incomplete frame at second {frame_number}, skipping...")
        continue

    frame = np.frombuffer(raw_frame, np.uint8).reshape((height, width, 3))

    # Run YOLOv11 detection
    results = model.predict(source=frame, conf=0.15, classes=[0], verbose=False)
    num_people = len(results[0].boxes)

    now = datetime.now().isoformat(timespec='seconds')
    print(f"[{now}] 🧍 {num_people} people detected")

    records.append({
        "timestamp": now,
        "frame": frame_number,
        "people": num_people
    })

    frame_number += 1
    time.sleep(1)  # Wait 1 second between frames

# Save results to CSV
df = pd.DataFrame(records)
df.to_csv(output_path, index=False)
print(f"✅ Saved results to {output_path}")

# Cleanup
proc.kill()
