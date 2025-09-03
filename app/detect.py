# app/detect.py

"""
This module handles:
- Live stream ingestion from YouTube (via streamlink + ffmpeg)
- Frame capture at 1 FPS
- YOLOv11 person detection
- Returns list of detection records (timestamp, count, frame_id)
"""

from ultralytics import YOLO
import subprocess, numpy as np, cv2, time
from datetime import datetime,timezone

"""
| Parameter      | Meaning                                                                                      |
| -------------- | -------------------------------------------------------------------------------------------- |
| `youtube_url`  | YouTube link to the **EarthCam live stream**                                                 |
| `fps`          | Frames per second to **process** (we use 1 FPS for efficiency)                               |
| `duration_sec` | How long to run the detection loop (e.g. 60 seconds = 1 min)                                 |
| `conf_thresh`  | Minimum **confidence score** for YOLO to consider a detection valid (lower = more sensitive) |
"""

def run_yolo_stream(youtube_url: str, fps: int = 1, duration_sec: int = 60, conf_thresh: float = 0.25):
    width, height = 1920, 1080
    frame_size = width * height * 3
    model = YOLO("models/yolo11n.pt")
    
    """
    | Tool                 | Role                                                                                  |
    | -------------------- | ------------------------------------------------------------------------------------- |
    | `streamlink`         | Grabs YouTube live stream and sends video to `stdout`                                 |
    | `ffmpeg`             | Converts that stream into raw pixel format (`bgr24`) so that OpenCV/Numpy can read it |
    | `proc.stdout.read()` | Where your Python code **reads raw frame bytes**                                      |
    """
    cmd = (
        f'streamlink --stdout "{youtube_url}" 1080p | '
        'ffmpeg -re -i - -f rawvideo -pix_fmt bgr24 -'
    )
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    start_time = time.time()
    frame_id = 0
    records = []
    """
        | Step                 | Meaning                                                   |
        | -------------------- | --------------------------------------------------------- |
        | `np.frombuffer()`    | Converts raw byte stream → image array                    |
        | `reshape(...)`       | Converts flat array into 2D image (1920x1080, 3 channels) |
        | `model.predict(...)` | Runs YOLO detection on the frame                          |
        | `classes=[0]`        | Only detect **people** (class 0)                          |
        | `num_people`         | Number of people detected in that frame                   |

    """

    SKIP_FRAMES = int(30 / fps)  # assuming input stream ~30FPS

    while time.time() - start_time < duration_sec:
        raw_frame = proc.stdout.read(frame_size)
        if len(raw_frame) != frame_size:
            print("Skipped partial frame.")
            continue

        frame_id += 1

        # Only process every N-th frame
        if frame_id % SKIP_FRAMES != 0:
            continue

        frame = np.frombuffer(raw_frame, np.uint8).reshape((height, width, 3))
        results = model.predict(source=frame, conf=conf_thresh, classes=[0], verbose=False)

        cv2.imshow("YOLO Frame", results[0].plot())
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        num_people = len(results[0].boxes)
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")

        print(f"[{now}] 🧍 {num_people} people (frame {frame_id})")

        records.append({
            "timestamp": now,
            "frame": frame_id,
            "people": num_people
        })

    proc.kill()
    return records
