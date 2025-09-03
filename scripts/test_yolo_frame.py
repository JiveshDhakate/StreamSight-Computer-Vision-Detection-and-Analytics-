import os
import cv2
from ultralytics import YOLO

# Load YOLO model (CPU by default)
model = YOLO("/Users/jiveshdhakate/Documents/Yolo Project/yolo11n.pt")  # downloads on first use

# Read stream or file
stream_url = os.getenv("STREAM_URL", "templebar.mp4")
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print(f"❌ Cannot open stream: {stream_url}")
    exit(1)

ret, frame = cap.read()
cap.release()

if not ret:
    print("❌ Failed to read a frame")
    exit(1)

# Run YOLO detection (only on class 0 = person)
results = model.predict(source=frame, conf=0.25, classes=[0])

# Draw bounding boxes on frame
annotated = results[0].plot()

# Save output
os.makedirs("data", exist_ok=True)
cv2.imwrite("data/yolo_output.jpg", annotated)
print("✅ YOLO detection complete. Saved to data/yolo_output.jpg")
