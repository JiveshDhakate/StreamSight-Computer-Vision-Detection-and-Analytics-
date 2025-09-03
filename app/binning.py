"""
Function Purpose:
- Accept records = [{"timestamp": ..., "frame": ..., "people": ...}, ...]
- Group records into 15-minute bins
- Save each bin as a separate CSV in data/bins/
"""

import os
import csv
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

def floor_to_15min(dt):
    """Floors a datetime to the nearest 15-minute bin."""
    minute = (dt.minute // 15) * 15
    return dt.replace(minute=minute, second=0, microsecond=0)

def save_records_to_bins(records, output_dir="data/bins"):
    """Groups detection records into 15-min bins and saves to CSV files."""
    bins = defaultdict(list)

    # Group records by floored 15-min timestamp
    for record in records:
        dt = datetime.fromisoformat(record["timestamp"])
        floored = floor_to_15min(dt)
        bins[floored].append(record)

    # Ensure output folder exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Write each bin to CSV
    for bin_time, group in bins.items():
        filename = f"{bin_time.strftime('%Y-%m-%d_%H%M')}.csv"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "frame", "people"])
            writer.writeheader()
            writer.writerows(group)

        print(f"Saved {len(group)} records to: {filepath}")
