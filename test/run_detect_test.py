import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.detect import run_yolo_stream
from app.binning import aggregate_and_save
import pandas as pd
import os

os.makedirs("data", exist_ok=True)

records = run_yolo_stream(
    youtube_url="https://www.youtube.com/watch?v=u4UZ4UvZXrg&ab_channel=EarthCam",
    fps=1,
    duration_sec=180,
    conf_thresh=0.2
)

# df = pd.DataFrame(records)
# df.to_csv("data/footfall.csv", index=False)
# print("Saved to data/footfall.csv")
aggregate_and_save(records)
