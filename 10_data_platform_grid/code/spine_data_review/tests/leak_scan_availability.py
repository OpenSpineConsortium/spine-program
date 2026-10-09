"""Scan run directories for credential VALUES (loaded from the store by name) and for header or
parameter patterns that would carry one. Prints file names and counts only; never a value.
Usage (WSL): ~/sdr_venv/bin/python tests/leak_scan_availability.py runs/review_availability ...
"""
import os
import re
import sys
from pathlib import Path

store = Path(os.environ.get("FLUOROCAP_CREDS", "~/.fluorocap")).expanduser() / "credentials.env"
vals = {}
if store.exists():
    for line in store.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            v = v.strip().strip('"').strip("'")
            if len(v) >= 6:
                vals[k.strip()] = v
for k in ("HF_TOKEN", "GITHUB_TOKEN", "OSF_TOKEN", "KAGGLE_KEY"):
    if os.environ.get(k):
        vals[k] = os.environ[k]
pat = re.compile(r"Bearer [A-Za-z0-9_\-]{8,}|api_key=[^&\s\"<]{4,}|x-api-key|Authorization", re.I)
hits, nfiles = 0, 0
for root in sys.argv[1:]:
    paths = [Path(root)] if Path(root).is_file() else [p for p in Path(root).rglob("*") if p.is_file()]
    for p in paths:
        nfiles += 1
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for k, v in vals.items():
            if v in t:
                hits += 1
                print(f"VALUE LEAK: credential {k} found in {p}")
        for m in pat.finditer(t):
            s = m.group(0)
            if s.lower() in ("authorization", "x-api-key") and "<redacted>" in t[m.start():m.start() + 80]:
                continue
            hits += 1
            print(f"PATTERN: {s[:12]}... in {p}")
print(f"scanned {nfiles} files under {sys.argv[1:]}; {len(vals)} credential values loaded by name; {hits} hits")
