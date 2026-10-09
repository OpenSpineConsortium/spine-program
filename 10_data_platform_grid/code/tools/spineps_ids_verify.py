#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/spineps_ids_verify.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Check the ctd relabel (tools/spineps_ids.py relabel) against names it did not compute.

Three outside references, each a different route to a vertebra's name on the same CT:
  ctsp   ~/bench/spineps/native COLONOG_<n> (raw, pre-147428d) relabelled by ctd  vs  /rs/.../spineps/ctsp/CTSP_<id>
         -- a SEPARATE SPINEPS run on the same CT, harvested after the fix, whose ids VERIDAH wrote itself. The
         COLONOG -> CTSP join is the CT path in benchmark/cases.csv (<id>_ct.nii.gz), never the number.
  ts12   the relabelled bench_ts TS_<s>  vs  rare_class/ts_stage/TS_<s>/TS_<s>_msk.nii.gz, relabelled in place by
         tools/rare_class_ts_fixids.py (z-rank) and checked 280/280 by tools/ts12_verify_ids.py (POI in mask).
  cobra  cobra2026/seg/spineps (raw v1) relabelled by ctd  vs  or_ready/crossdev/levels/spineps_v1_relabel/
         <case>_seg-vert_msk_veridah.nii.gz, written by tools/spineps_relabel_from_poi.py (position only).
For every instance of the relabelled mask (>= 50 voxels), the reference's id at its world centroid: same / other /
none (spineps_ids.compare_masks; grids may differ). Also the reverse direction, so a level the relabel dropped or
invented shows up.

    python tools/spineps_ids_verify.py ctsp  --cases benchmark/cases.csv --new <dir> --ref <dir> --shard i --n-shards n --out rows_i.jsonl
    python tools/spineps_ids_verify.py ts12  --new <dir> --stage <dir> --out ts12.jsonl
    python tools/spineps_ids_verify.py cobra --new <dir> --ref <dir> --out cobra.jsonl
    python tools/spineps_ids_verify.py aggregate --rows 'glob' --out verify.json
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spineps_ids as S  # noqa: E402

TS12 = ["s0224", "s0616", "s0790", "s1088", "s1089", "s1123", "s1124", "s1171", "s1178", "s1304", "s1350", "s1380"]


def one(kind, case, new_p, ref_p, extra=None):
    rec = dict(kind=kind, case=case, new=new_p, ref=ref_p, **(extra or {}))
    rj = new_p.replace("_seg-vert_msk.nii.gz", "_relabel.json")
    if os.path.exists(rj):
        R = json.load(open(rj))
        rec["action"] = R.get("action")
        rec["source_verdict"] = R.get("source_verdict")
        rec["refused"] = R.get("refused")
    if not os.path.exists(new_p):
        rec["status"] = "no relabelled mask"
        return rec
    if not os.path.exists(ref_p):
        rec["status"] = "no reference mask"
        return rec
    try:
        rec["new_vs_ref"] = S.compare_masks(new_p, ref_p)
        rec["ref_vs_new"] = S.compare_masks(ref_p, new_p)
        rec["status"] = "compared"
    except Exception as e:                                    # noqa: BLE001
        rec["status"] = "error"
        rec["error"] = repr(e)[:300]
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["ctsp", "ts12", "cobra", "aggregate"])
    ap.add_argument("--cases")
    ap.add_argument("--new")
    ap.add_argument("--ref")
    ap.add_argument("--stage")
    ap.add_argument("--rows")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--n-shards", type=int, default=1)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    if a.mode == "aggregate":
        rows = []
        for f in sorted(glob.glob(a.rows)):
            rows += [json.loads(l) for l in open(f) if l.strip()]
        out = {}
        for kind in sorted({r["kind"] for r in rows}):
            rs = [r for r in rows if r["kind"] == kind]
            comp = [r for r in rs if r.get("status") == "compared"]
            tot = Counter()
            pairs = Counter()
            cases_all_same = 0
            for r in comp:
                nv = r["new_vs_ref"]
                tot["instances"] += nv["same"] + nv["diff"] + nv["miss"]
                tot["same"] += nv["same"]
                tot["diff"] += nv["diff"]
                tot["miss"] += nv["miss"]
                rv = r["ref_vs_new"]
                tot["ref_instances"] += rv["same"] + rv["diff"] + rv["miss"]
                tot["ref_same"] += rv["same"]
                tot["ref_diff"] += rv["diff"]
                tot["ref_miss"] += rv["miss"]
                cases_all_same += int(nv["diff"] == 0 and rv["diff"] == 0)
                for e in nv["examples"]:
                    pairs[e] += 1
            out[kind] = dict(cases=len(rs), status=dict(Counter(r.get("status") for r in rs)),
                             action=dict(Counter(str(r.get("action")) for r in rs)),
                             compared=len(comp), cases_without_a_name_difference=cases_all_same,
                             instances=dict(tot), name_differences=dict(pairs.most_common(40)),
                             cases_with_differences=[dict(case=r["case"], ref=os.path.basename(r["ref"]),
                                                          new_vs_ref=r["new_vs_ref"], ref_vs_new=r["ref_vs_new"])
                                                     for r in comp if r["new_vs_ref"]["diff"] or r["ref_vs_new"]["diff"]][:80])
        json.dump(out, open(a.out, "w"), indent=1)
        print(json.dumps({k: {kk: v[kk] for kk in ("cases", "status", "compared", "cases_without_a_name_difference",
                                                   "instances")} for k, v in out.items()}, indent=1))
        return 0

    fh = open(a.out, "w")
    if a.mode == "ctsp":
        rows = list(csv.DictReader(open(a.cases)))
        rows = [r for k, r in enumerate(rows) if k % a.n_shards == a.shard]
        for r in rows:
            ctid = os.path.basename(r["ct"]).split("_ct.nii")[0]
            rec = one("ctsp", r["case"], os.path.join(a.new, f"{r['case']}_seg-vert_msk.nii.gz"),
                      os.path.join(a.ref, f"CTSP_{ctid}_seg-vert_msk.nii.gz"), dict(ctsp=f"CTSP_{ctid}"))
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            print(rec["case"], rec.get("status"), rec.get("new_vs_ref"), flush=True)
    elif a.mode == "ts12":
        for s in TS12:
            rec = one("ts12", f"TS_{s}", os.path.join(a.new, f"TS_{s}_seg-vert_msk.nii.gz"),
                      os.path.join(a.stage, f"TS_{s}", f"TS_{s}_msk.nii.gz"))
            fh.write(json.dumps(rec) + "\n")
            print(rec["case"], rec.get("action"), rec.get("status"), rec.get("new_vs_ref"), rec.get("refused"), flush=True)
    elif a.mode == "cobra":
        for p in sorted(glob.glob(os.path.join(a.new, "*_seg-vert_msk.nii.gz"))):
            c = os.path.basename(p)[: -len("_seg-vert_msk.nii.gz")]
            rec = one("cobra", c, p, os.path.join(a.ref, f"{c}_seg-vert_msk_veridah.nii.gz"))
            fh.write(json.dumps(rec) + "\n")
            print(c, rec.get("action"), rec.get("status"), rec.get("new_vs_ref"), flush=True)
        # refused cases have no mask in --new: list them from the relabel records
        for rj in sorted(glob.glob(os.path.join(a.new, "*_relabel.json"))):
            R = json.load(open(rj))
            if R.get("action") in ("refused", "error"):
                fh.write(json.dumps(dict(kind="cobra", case=R["case"], status="no relabelled mask",
                                         action=R.get("action"), refused=R.get("refused"))) + "\n")
    fh.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
