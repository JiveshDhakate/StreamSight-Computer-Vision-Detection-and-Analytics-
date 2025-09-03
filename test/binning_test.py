import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.binning import save_records_to_bins

mock_records = [
    {"timestamp": "2025-09-03T10:01:00", "frame": 0, "people": 10},
    {"timestamp": "2025-09-03T10:02:00", "frame": 1, "people": 12},
    {"timestamp": "2025-09-03T10:17:00", "frame": 2, "people": 11},
    {"timestamp": "2025-09-03T10:29:00", "frame": 3, "people": 15},
]

save_records_to_bins(mock_records)
print("Binning test completed. Check data/bins/ for output CSVs.")