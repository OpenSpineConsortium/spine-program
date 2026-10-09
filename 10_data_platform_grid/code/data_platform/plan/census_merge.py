#!/usr/bin/env python3
"""Merge the three storage-census outputs of 2026-10-07/08 into one census.tsv that build_plan.py --census reads.

Inputs (under /rs/rs_grp_oschome/go2432/data/inventory/census_2026-10-07/, or a local copy):
  census.json            job 40578909: HOME entries that sort before and including "FluoroCap" (rows: root, name, bytes;
                         depth2: root, parent, name, bytes), plus whatever else it reached before it was stopped
  ceph/census.tsv        job 40580051: the Ceph root, columns path, kind, gb, files, dirs, newest, oldest, top_ext
                         (depth-2 rows have kind "dir2")
  home_after_F/census.tsv job 40580052: HOME entries that sort after "FluoroCap", same columns

Output: one TSV with columns path, gb, files, kind, newest, source_job. A path seen in several inputs keeps the
newest-dated row. Sizes are apparent bytes / 1e9, as build_plan.py expects under its "gb" column.

    python3 census_merge.py --dir <folder holding census.json, ceph/, home_after_F/> --out census.tsv
"""
from __future__ import annotations

import argparse
import csv
import json
import os


def rows_from_json(path, tag):
    out = []
    if not os.path.exists(path):
        return out
    d = json.load(open(path, encoding="utf-8"))
    for r in d.get("rows", []):
        if r.get("kind") not in ("dir", "file"):
            continue
        out.append(dict(path=f'{r["root"]}/{r["name"]}', gb=r.get("bytes", 0) / 1e9, files=r.get("files", ""), kind=r["kind"], newest=r.get("newest", ""), source_job=tag))
    for r in d.get("depth2", []):
        out.append(dict(path=f'{r["root"]}/{r["parent"]}/{r["name"]}', gb=r.get("bytes", 0) / 1e9, files=r.get("files", ""), kind="dir2", newest=r.get("newest", ""), source_job=tag))
    return out


def rows_from_tsv(path, tag):
    out = []
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r.get("kind") not in ("dir", "file", "dir2"):
                continue
            try:
                gb = float(r.get("gb") or 0)
            except ValueError:
                continue
            out.append(dict(path=r["path"], gb=gb, files=r.get("files", ""), kind=r["kind"], newest=r.get("newest", ""), source_job=tag))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows = rows_from_json(os.path.join(a.dir, "census.json"), "40578909")
    rows += rows_from_tsv(os.path.join(a.dir, "ceph", "census.tsv"), "40580051")
    rows += rows_from_tsv(os.path.join(a.dir, "home_after_F", "census.tsv"), "40580052")
    best = {}
    for r in rows:
        p = r["path"].rstrip("/")
        if p not in best or (r["newest"] or "") >= (best[p]["newest"] or ""):
            best[p] = r
    with open(a.out, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["path", "gb", "files", "kind", "newest", "source_job"])
        for p in sorted(best):
            r = best[p]
            w.writerow([p, f'{r["gb"]:.3f}', r["files"], r["kind"], r["newest"], r["source_job"]])
    top = [r for r in best.values() if r["kind"] in ("dir", "file")]
    home = sum(r["gb"] for r in top if r["path"].startswith("/wsu/home"))
    ceph = sum(r["gb"] for r in top if r["path"].startswith("/rs/"))
    print(f"{len(best)} paths; top-level HOME {home:,.0f} GB, Ceph {ceph:,.0f} GB -> {a.out}")


if __name__ == "__main__":
    main()
