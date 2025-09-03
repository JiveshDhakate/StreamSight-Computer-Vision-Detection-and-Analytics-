import os, csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

def round_to_minute(dt):
    return dt.replace(second=0, microsecond=0)

def floor_to_15min(dt):
    minute = (dt.minute // 15) * 15
    return dt.replace(minute=minute, second=0, microsecond=0)

def aggregate_and_save(records, output_dir="data"):
    minute_bins = defaultdict(list)
    quarter_bins = defaultdict(list)

    for record in records:
        dt = datetime.fromisoformat(record["timestamp"])
        minute_bins[round_to_minute(dt)].append(record["people"])
        quarter_bins[floor_to_15min(dt)].append(record["people"])

    # Save per-minute
    minute_dir = os.path.join(output_dir, "minute_logs")
    Path(minute_dir).mkdir(parents=True, exist_ok=True)
    for ts, people_counts in minute_bins.items():
        filename = f"{ts.strftime('%Y-%m-%d_%H%M')}.csv"
        filepath = os.path.join(minute_dir, filename)
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "people_avg", "frames"])
            writer.writeheader()
            writer.writerow({
                "timestamp": ts.isoformat(),
                "people_avg": round(sum(people_counts) / len(people_counts)),
                "frames": len(people_counts)
            })

    # Save per-15-min
    bin_dir = os.path.join(output_dir, "15min_bins")
    Path(bin_dir).mkdir(parents=True, exist_ok=True)
    for ts, people_counts in quarter_bins.items():
        filename = f"{ts.strftime('%Y-%m-%d_%H%M')}.csv"
        filepath = os.path.join(bin_dir, filename)
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "people_avg", "frames"])
            writer.writeheader()
            writer.writerow({
                "timestamp": ts.isoformat(),
                "people_avg": round(sum(people_counts) / len(people_counts)),
                "frames": len(people_counts)
            })
