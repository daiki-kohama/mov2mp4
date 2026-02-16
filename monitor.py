# monitor.py
import os
import time
import re
import subprocess
from datetime import datetime, timedelta

WATCH_DIR = os.environ.get("WATCH_DIR", "/watch")
PAT = re.compile(r"^(.*) (\d{4}-\d{2}-\d{2} \d{1,2}\.\d{2}\.\d{2})\.mov$")


def parse_dt(s):
    # "YYYY-MM-DD HH.MM.SS" → "YYYY-MM-DD HH:MM:SS"
    date_part, time_part = s.split(" ")
    time_part = time_part.replace(".", ":")
    return datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M:%S")


def convert(src, dst):
    cmd = ["ffmpeg", "-i", src, dst]
    subprocess.run(cmd, check=True)


def main():
    while True:
        now = datetime.now()
        cutoff = now - timedelta(days=1)
        files = os.listdir(WATCH_DIR)
        # mov ファイルをソートしておけば、古い順に処理されます
        for f in sorted(files):
            m = PAT.match(f)
            if not m:
                continue
            base, dt_str = m.groups()
            dt = parse_dt(dt_str)
            if dt < cutoff:
                continue
            mov = os.path.join(WATCH_DIR, f)
            mp4 = os.path.join(WATCH_DIR, f[:-4] + ".mp4")
            if os.path.exists(mp4):
                continue
            try:
                print(f"[{datetime.now()}] convert {mov} → {mp4}")
                convert(mov, mp4)
            except Exception as e:
                print(f"ERROR converting {mov}: {e}")
        time.sleep(5)


if __name__ == "__main__":
    main()
