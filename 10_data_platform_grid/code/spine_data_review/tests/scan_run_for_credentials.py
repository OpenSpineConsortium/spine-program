"""Reviewer check: does any credential VALUE appear in a run directory or a log file?
Loads the values through sdr.creds (never prints them), scans every file under the given paths
byte-wise for each value of six or more characters and for its base64(user:key) Kaggle form, and
prints only the credential NAME and the file path on a hit. Exit 1 on any hit.
Usage: ~/sdr_venv/bin/python tests/scan_run_for_credentials.py <path> [<path> ...]"""
import base64, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sdr import creds
vals = {k: v for k, v in creds._load().items() if len(v) >= 6}
if creds.cred("KAGGLE_USERNAME") and creds.cred("KAGGLE_KEY"):
    vals["KAGGLE_BASIC_B64"] = base64.b64encode(f"{creds.cred('KAGGLE_USERNAME')}:{creds.cred('KAGGLE_KEY')}".encode()).decode()
print("credential names loaded:", sorted(vals))
hits, n = [], 0
for root in sys.argv[1:]:
    for p in Path(root).rglob("*"):
        if p.is_file():
            n += 1
            data = p.read_bytes()
            for k, v in vals.items():
                if v.encode("utf-8") in data:
                    hits.append((k, str(p)))
print(f"files scanned: {n}")
for k, p in hits:
    print("HIT", k, p)
print("result:", "LEAK" if hits else "clean")
sys.exit(1 if hits else 0)
