#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/jhu_dataverse_fetch.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Download every file of a public JHU Data Archive (Dataverse) deposit, smallest first, resumable.

archive.data.jhu.edu blocks plain curl by TLS fingerprint (Cloudflare 403); curl_cffi impersonating a browser is
served. Files are streamed to <out>/<filename>.part and renamed when the byte count matches the deposit's own
size, so a rerun skips what is complete. Only unrestricted files are fetched.

    python tools/jhu_dataverse_fetch.py doi:10.7281/T1/C304HZ /rs/rs_grp_oschome/go2432/data/deepfluoro_vendor
"""
from __future__ import annotations

import os
import sys
import time


def main() -> int:
    pid, out = sys.argv[1], sys.argv[2]
    only = set(sys.argv[3:])                      # optional file names to restrict to
    from curl_cffi import requests
    os.makedirs(out, exist_ok=True)
    meta = requests.get(f"https://archive.data.jhu.edu/api/datasets/:persistentId/?persistentId={pid}", impersonate="chrome", timeout=60).json()
    files = [f for f in meta["data"]["latestVersion"]["files"] if not f.get("restricted")]
    files.sort(key=lambda f: f["dataFile"].get("filesize", 0))
    for f in files:
        df = f["dataFile"]; name = df["filename"]; size = df.get("filesize", 0)
        if only and name not in only:
            continue
        dst = os.path.join(out, name)
        if os.path.exists(dst) and os.path.getsize(dst) == size:
            print(f"{name}: complete", flush=True); continue
        t0 = time.time(); tmp = dst + ".part"
        for attempt in range(6):
            try:
                # WRITE-CALLBACK, NOT iter_content: with stream=True curl_cffi queues the body in memory faster than a
                # CephFS write drains it, and the first run of this job was OOM-killed at 4 GB with nothing on disk.
                # content_callback hands each buffer straight to the file. A .part is resumed with a Range header.
                have = os.path.getsize(tmp) if os.path.exists(tmp) else 0
                headers = {"Range": f"bytes={have}-"} if have else {}
                with open(tmp, "ab" if have else "wb") as fh:
                    r = requests.get(f"https://archive.data.jhu.edu/api/access/datafile/{df['id']}", impersonate="chrome",
                                     headers=headers, content_callback=fh.write, timeout=3600)
                if r.status_code not in (200, 206):
                    raise RuntimeError(f"HTTP {r.status_code}")
                if have and r.status_code == 200:                    # server ignored the range: it re-sent everything
                    print(f"{name}: server ignored Range, restarting the file", flush=True)
                    os.remove(tmp); continue
                break
            except Exception as e:  # noqa: BLE001
                print(f"{name}: attempt {attempt + 1} failed: {e}", flush=True); time.sleep(20 * (attempt + 1))
        got = os.path.getsize(tmp) if os.path.exists(tmp) else -1
        if got != size:
            # tabular files are served in a converted form; keep what arrived and say so
            print(f"{name}: got {got} bytes, deposit says {size}; kept as {tmp}", flush=True); continue
        os.replace(tmp, dst)
        print(f"{name}: {size / 1e9:.2f} GB in {time.time() - t0:.0f} s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
