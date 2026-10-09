"""Scan review outputs for any credential VALUE from ~/.fluorocap/credentials.env (and kaggle.json, HF_TOKEN).

Prints only counts and file names, never a value or a key name paired with a value. Exit 1 on any hit.
Run in WSL:  ~/sdr_venv/bin/python tests/check_no_credentials.py [paths...]
Default paths: runs/review_manuscript, tables, manuscript/main.tex, runs/smoke/manuscript, runs/smoke/tables.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ["runs/review_manuscript", "tables", "manuscript/main.tex", "runs/smoke/manuscript", "runs/smoke/tables",
           "runs/smoke/queries.json", "runs/smoke/counts.json", "runs/smoke/run_meta.json"]
SKIP_SUFFIX = {".pdf", ".png", ".aux", ".fdb_latexmk", ".fls", ".out", ".bbl", ".blg", ".pyc"}


def values() -> list[str]:
    vals: list[str] = []
    env = Path.home() / ".fluorocap" / "credentials.env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                v = line.split("=", 1)[1].strip().strip("'\"")
                if len(v) >= 8:  # ignore short/empty values that would match by chance
                    vals.append(v)
    kag = Path.home() / ".kaggle" / "kaggle.json"
    if kag.exists():
        try:
            vals += [str(v) for v in json.loads(kag.read_text(encoding="utf-8")).values() if len(str(v)) >= 8]
        except json.JSONDecodeError:
            pass
    if os.environ.get("HF_TOKEN") and len(os.environ["HF_TOKEN"]) >= 8:
        vals.append(os.environ["HF_TOKEN"])
    return vals


def main(argv: list[str]) -> int:
    vals = values()
    print(f"credential values loaded for scanning: {len(vals)} (values never printed)")
    paths = [ROOT / p for p in (argv or DEFAULT)]
    n_files, hits = 0, []
    for p in paths:
        files = [p] if p.is_file() else [f for f in p.rglob("*") if f.is_file()] if p.exists() else []
        for f in files:
            if f.suffix in SKIP_SUFFIX:
                continue
            n_files += 1
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            n = sum(text.count(v) for v in vals)
            if n:
                hits.append((str(f.relative_to(ROOT)), n))
    print(f"files scanned: {n_files}; files with a credential value: {len(hits)}")
    for f, n in hits:
        print(f"  HIT {f}: {n} occurrence(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
