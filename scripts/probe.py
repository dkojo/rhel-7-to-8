"""The users: a request through the load balancer every 50 ms for the whole upgrade.
On SIGTERM it saves report/probe.json: requests, failures, and what share of responses came from RHEL 8 over time.

  python3 scripts/probe.py http://localhost:8080/
"""
import json
import os
import signal
import sys
import time
import urllib.error
import urllib.request

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080/"
stats = {"requests": 0, "failed": 0, "by_release": {"7": 0, "8": 0}, "errors": []}
per_second = []          # [(responses from RHEL 8, total)] for each second
running = True


def stop(*_):
    global running
    running = False


signal.signal(signal.SIGTERM, stop)
second, bucket = int(time.time()), [0, 0]
while running:
    try:
        with urllib.request.urlopen(URL, timeout=3) as r:
            body = r.read().decode()
        release = "8" if "RHEL 8" in body else "7"
        stats["by_release"][release] += 1
        bucket[0] += release == "8"
        bucket[1] += 1
    except (urllib.error.URLError, OSError) as e:
        stats["failed"] += 1
        stats["errors"].append(f"{time.strftime('%H:%M:%S')} {e}")
    stats["requests"] += 1
    if int(time.time()) != second:
        per_second.append(bucket)
        second, bucket = int(time.time()), [0, 0]
    time.sleep(0.05)

# Downsample to 30 points: the percentage of responses served by RHEL 8
step = max(1, len(per_second) // 30)
stats["rhel8_share_pct"] = [round(sum(b[0] for b in per_second[i:i + step]) / max(1, sum(b[1] for b in per_second[i:i + step])) * 100)
                            for i in range(0, len(per_second), step)]
os.makedirs("report", exist_ok=True)
with open("report/probe.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=2)
