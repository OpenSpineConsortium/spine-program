#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/spineps_ids_rescore_report.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Read the re-scored SPINEPS column of the CTSP one-shot benchmark (slurm/spineps_ids_repair.sh rescore_*) against
the void original, and split it by what the relabel reproduced: cases where VERIDAH skipped T12 (its 11-thoracic call)
against the rest. Json/csv only.

    python tools/spineps_ids_rescore_report.py --dir SchwingNet/results/spineps_ids/repair/rescore \
        --records SchwingNet/results/spineps_ids/repair/relabel_records.jsonl.gz --out <json>
Inputs under --dir: <system>/summary.json and <system>/per_case.csv for bench_ctd and ctsp_postfix.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import os
from collections import Counter

LEVELS = ["T10", "T11", "T12", "L1", "L2", "L3", "L4", "L5", "L6", "sacrum"]


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 4) if xs else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--records", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    skip = set()
    for line in gzip.open(a.records, "rt"):
        r = json.loads(line)
        if "/bench/spineps/native/" in r["source"] and r.get("action") == "relabelled" and r.get("veridah_skipped_names"):
            skip.add(r["case"])

    out = {"t12_skip_cases_in_bench": len(skip)}
    for system in ("bench_ctd", "ctsp_postfix"):
        d = os.path.join(a.dir, system)
        if not os.path.exists(os.path.join(d, "summary.json")):
            out[system] = "missing"
            continue
        S = json.load(open(os.path.join(d, "summary.json")))
        rows = list(csv.DictReader(open(os.path.join(d, "per_case.csv"))))
        rec = {"n_cases": S["n_cases"], "n_transitional": S["n_transitional"],
               "dice_mean_all": {k: v for k, v in S["dice_mean"]["all"].items() if k in LEVELS},
               "dice_mean_typical": {k: v for k, v in S["dice_mean"]["typical"].items() if k in LEVELS},
               "dice_mean_transitional": {k: v for k, v in S["dice_mean"]["transitional"].items() if k in LEVELS},
               "rib_free_count": S["rib_free_count"]}
        for grp, sel in (("t12_skip", [r for r in rows if r["case"] in skip]),
                         ("no_skip", [r for r in rows if r["case"] not in skip])):
            g = {"n": len(sel),
                 "count_exact": round(sum(1 for r in sel if int(r["count_error"]) == 0) / max(1, len(sel)), 4),
                 "count_error_hist": dict(sorted(Counter(int(r["count_error"]) for r in sel).items()))}
            for lv in ("T12", "L1", "L2", "L3", "L4", "L5"):
                col = f"dice_{lv}"
                g[f"dice_{lv}"] = mean([float(r[col]) for r in sel if r.get(col) not in (None, "")])
            rec[grp] = g
        out[system] = rec
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps(out, indent=1)[:6000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
