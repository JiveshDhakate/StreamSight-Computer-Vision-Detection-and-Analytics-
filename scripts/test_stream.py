import os
import cv2

# Get stream URL from env or fallback default
stream_url = os.getenv("STREAM_URL", "templebar.mp4")

print(f"🎥 Trying to open stream: {stream_url}")

cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print(f"❌ Failed to open stream: {stream_url}")
    exit(1)

print("✅ Stream opened successfully!")

# Try reading a single frame
ret, frame = cap.read()

if ret:
    print(f"✅ Got a frame! Shape: {frame.shape}")
    
    # Save frame to disk for verification
    os.makedirs("data", exist_ok=True)
    frame_path = os.path.join("data", "snapshot.jpg")
    cv2.imwrite(frame_path, frame)
    print(f"🖼️ Saved snapshot to {frame_path}")
else:
    print("❌ Failed to read a frame from the stream.")

cap.release()
