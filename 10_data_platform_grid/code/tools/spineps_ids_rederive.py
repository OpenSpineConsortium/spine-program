#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/spineps_ids_rederive.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Re-derive the numbers the raw SPINEPS ids reached, from the repaired (ctd-relabelled) trees -- json only, no masks.

Inputs (all small, all on disk locally):
  --records   the per-case relabel records of every repaired tree (tools/spineps_ids.py relabel writes
              <out>/relabel_shard<i>.jsonl; SchwingNet/slurm/spineps_ids_repair.sh; concatenated + gzipped)
  --inventory SchwingNet/results/anomalous_inventory.json      (the transitional inventory as it stands now)
  --power     SchwingNet/results/power_table.json               (what Figure 6d / NUMBERS.md quote today)
  --census    SchwingNet/results/spineps_ids/census_rows.jsonl.gz (the F2 census: "id 25 present" per raw mask)

Writes one json with:
  1. per tree: masks, relabelled / passed through / refused (with reasons), VERIDAH's own call per case read from the
     ctd (L6 / T13 / both / none), T12 skips reproduced, C1 named, sacrum state;
  2. the TotalSegmentator v2 row under each reading: the manuscript's (id 25 present), the id-25 reader against the
     ctd on the same masks, VERIDAH's ctd over the whole v2 bench, and the corrected inventory on disk;
  3. the Table 4 / Figure 6d arithmetic under each reading, with the Wilson bound computed by the SAME formula as
     SchwingNet/tools/fig_claim.py (checked against power_table.json's own grid before it is used).
Nothing here is a reader's truth: VERIDAH's calls are pseudo-truth (CONSUMERS.md section 4: on CTSP, 10 of its 24
L6 calls are reader L6).

    python tools/spineps_ids_rederive.py --records SchwingNet/results/spineps_ids/repair/relabel_records.jsonl.gz \
        --inventory SchwingNet/results/anomalous_inventory.json --power SchwingNet/results/power_table.json \
        --census SchwingNet/results/spineps_ids/census_rows.jsonl.gz --out SchwingNet/results/spineps_ids/rederived.json
"""
from __future__ import annotations

import argparse
import gzip
import json
import math
import re
from collections import Counter, defaultdict

Z95 = 1.959964


def wilson_lower(errors: int, n: int, z: float = Z95) -> float:
    """SchwingNet/tools/fig_claim.py wilson_lower, verbatim."""
    p = (n - errors) / n
    centre = p + z * z / (2 * n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (centre - half) / (1 + z * z / n)


def tree_of(src: str) -> str:
    if "/bench_ts/spineps/native/TS_" in src:
        return "TS v2 (bench_ts)"
    if "/bench_ts/spineps/native/VERSE_" in src:
        return "VerSe (bench_ts)"
    if "/bench/spineps/native/" in src:
        return "CTSP benchmark (bench, COLONOG)"
    if "/data/spineps/tsv3/" in src:
        return "TS v3 (tsv3)"
    if "/cobra2026/seg/spineps/" in src:
        return "COBRA Elekta v1"
    if "/deepfluoro/" in src:
        return "DeepFluoro"
    if "/geneva_hip/" in src:
        return "Geneva hip phantom"
    return "other"


def call_of(r: dict) -> str | None:
    """VERIDAH's own count call for one case: from the ctd for a relabelled case, from the (already VerSe-named)
    ids for a pass-through; None for a refused case."""
    if r["action"] == "relabelled":
        return r.get("ctd_call")
    if r["action"] == "passthrough":
        ids = set(int(i) for i in r.get("source_ids") or [])
        return "both" if {25, 28} <= ids else ("L6" if 25 in ids else ("T13" if 28 in ids else "none"))
    return None


def readings(inv_now: dict, power: dict) -> dict:
    """Table 4 / Figure 6d arithmetic under the readings of the TotalSegmentator row. The other sources are taken
    from the inventory on disk (VerSe 56 = 50 L6 + 6 T13, CTSP 18 L6, C-ArmLSpine 3 L6); only the TS row varies."""
    fixed = {k: v for k, v in inv_now.items() if k != "totalsegmentator"}
    real = fixed["carmlspine_real"]["total"]
    train_fixed = sum(v.get("train", 0) for k, v in fixed.items())
    ts_rows = {
        "manuscript today (id 25 present on raw masks)": dict(l6=12, t13=0, train=9, note="12 L6; 9 in the v8 train half"),
        "VERIDAH ctd on the 12, s1178 refuted (TS12_VERIFY)": dict(l6=1, t13=3, train=4,
                                                                   note="s1089 L6; s0616, s1088, s1123 T13"),
        "independent count on the 12 (F1 rib count; the inventory on disk now)": dict(
            l6=inv_now["totalsegmentator"]["l6"], t13=inv_now["totalsegmentator"]["t13"],
            train=inv_now["totalsegmentator"].get("train", 0), note="s1088, s1089, s1123 L6-pattern; s0616 T13"),
        "no TotalSegmentator row (no reader truth)": dict(l6=0, t13=0, train=0, note="drop the row"),
    }
    out = {}
    for name, ts in ts_rows.items():
        ts_total = ts["l6"] + ts["t13"]
        ct = sum(v["total"] for k, v in fixed.items() if k != "carmlspine_real") + ts_total
        total = ct + real
        t40 = real + round(0.40 * ct)
        t50 = real + round(0.50 * ct)
        l6 = sum(v.get("l6", 0) for v in fixed.values()) + ts["l6"]
        t13 = sum(v.get("t13", 0) for v in fixed.values()) + ts["t13"]
        out[name] = dict(ts_l6=ts["l6"], ts_t13=ts["t13"], note=ts["note"], count_changing_persons=total,
                         l6_persons=l6, t13_persons=t13, ct_subjects=ct, test_persons_40pct=t40,
                         test_persons_50pct_rule=t50, in_v8_train_half=train_fixed + ts["train"],
                         wilson_lower_pct_k0=round(100 * wilson_lower(0, t40), 1),
                         wilson_lower_pct_k1=round(100 * wilson_lower(1, t40), 1),
                         meets_90_at_k0=wilson_lower(0, t40) >= 0.90)
    today = power.get("inventory_today", {})
    out["_check_against_power_table"] = dict(
        power_table_inventory_today=today,
        recomputed_manuscript_row=dict(total=out["manuscript today (id 25 present on raw masks)"]["count_changing_persons"],
                                       test_40=out["manuscript today (id 25 present on raw masks)"]["test_persons_40pct"]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True)
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--power", required=True)
    ap.add_argument("--census", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    # the Wilson formula must reproduce the grid power_table.json already quotes
    power = json.load(open(a.power))
    grid = power["lower_bound_pct_by_k_then_n"]
    bad = [(k, n) for k, row in grid.items() for n, v in row.items()
           if abs(round(100 * wilson_lower(int(k), int(n)), 2) - v) > 0.006]
    if bad:
        raise SystemExit(f"wilson_lower does not reproduce power_table.json at {bad[:5]}")

    recs = {}
    for line in gzip.open(a.records, "rt"):
        if not line.strip():
            continue
        r = json.loads(line)
        if r["source"] in recs and r["action"] == "error":
            continue                                   # a --force fixup record wins over the first pass's error
        recs[r["source"]] = r

    per = defaultdict(list)
    for src, r in recs.items():
        per[tree_of(src)].append(r)
    trees = {}
    for t, rs in sorted(per.items()):
        act = Counter(r["action"] for r in rs)
        calls = Counter(call_of(r) for r in rs if call_of(r) is not None)
        reasons = Counter()
        for r in rs:
            if r["action"] in ("refused", "error"):
                for m in r.get("refused") or [r.get("error", "error")]:
                    reasons[re.sub(r"[-\d.]+", "#", str(m))[:110]] += 1
        trees[t] = dict(masks=len(rs), actions=dict(act), veridah_call_by_ctd=dict(calls),
                        t12_skip_reproduced=sum(1 for r in rs if r["action"] == "relabelled" and r.get("veridah_skipped_names")),
                        c1_named=sum(1 for r in rs if any("named C1" in n for n in r.get("notes") or [])),
                        sacrum=dict(Counter(str(r.get("sacrum", "")).split(":")[0] for r in rs if r["action"] == "relabelled")),
                        max_dz_mm_p95=sorted(r["max_dz_mm"] for r in rs if "max_dz_mm" in r)[
                            int(0.95 * max(0, sum(1 for r in rs if "max_dz_mm" in r) - 1))] if any("max_dz_mm" in r for r in rs) else None,
                        refusal_reasons=dict(reasons.most_common()),
                        refused_cases=sorted(r["case"] for r in rs if r["action"] in ("refused", "error")))
    ts12 = ["s0224", "s0616", "s0790", "s1088", "s1089", "s1123", "s1124", "s1171", "s1178", "s1304", "s1350", "s1380"]
    ts12_calls = {s: (recs.get(next((k for k in recs if k.endswith(f"/TS_{s}_seg-vert_msk.nii.gz")), ""), {}).get("action"),
                      call_of(recs.get(next((k for k in recs if k.endswith(f"/TS_{s}_seg-vert_msk.nii.gz")), ""), {"action": "none"})))
                  for s in ts12}

    # the id-25 reader on the raw TS v2 masks against the ctd call, from the census rows
    id25 = Counter()
    id25_cases = []
    for line in gzip.open(a.census, "rt"):
        r = json.loads(line)
        if r.get("kind") != "seg-vert" or "/bench_ts/spineps/native/TS_" not in r.get("path", ""):
            continue
        ids = set(int(i) for i in r.get("ids") or [])
        ctd = set(int(i) for i in r.get("ctd_labels") or [])
        if 25 in ids:
            id25["id25_present"] += 1
            id25["and_ctd_L6"] += int(25 in ctd)
            id25["and_ctd_T13"] += int(28 in ctd and 25 not in ctd)
            id25["and_ctd_none"] += int(25 not in ctd and 28 not in ctd)
            id25["raw_instance"] += int(bool(r.get("raw_instance")))
            id25_cases.append(r.get("case"))

    inv_now = json.load(open(a.inventory))["summary"]
    out = dict(trees=trees, ts12_after_relabel=ts12_calls,
               ts_v2_id25_reader_vs_ctd=dict(id25, cases=sorted(id25_cases)),
               readings=readings(inv_now, power),
               wilson_formula_checked_against=f"{a.power}#lower_bound_pct_by_k_then_n (30 cells)",
               caveat="VERIDAH's call is pseudo-truth: on CTSP 10 of its 24 L6 calls are reader L6 "
                      "(SchwingNet/results/spineps_ids/veridah_check.json)")
    json.dump(out, open(a.out, "w"), indent=1)
    for t, d in trees.items():
        print(f"{t:34s} masks {d['masks']:5d} {d['actions']} calls {d['veridah_call_by_ctd']} T12-skip {d['t12_skip_reproduced']}")
    print("TS12 after relabel:", ts12_calls)
    print("id25 reader on TS v2:", dict(id25))
    for k, v in out["readings"].items():
        if not k.startswith("_"):
            print(f"{k:72s} persons {v['count_changing_persons']:3d} L6 {v['l6_persons']:3d} T13 {v['t13_persons']:2d} "
                  f"test40 {v['test_persons_40pct']} (k0 {v['wilson_lower_pct_k0']} k1 {v['wilson_lower_pct_k1']}) "
                  f"50% {v['test_persons_50pct_rule']} train-half {v['in_v8_train_half']}")
    print(out["readings"]["_check_against_power_table"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
