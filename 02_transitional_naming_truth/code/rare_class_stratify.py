#!/usr/bin/env python
# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/rare_class_stratify.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""The stratification file for the ONE final bank, and the plan that reads what it does to the split.

    build  SchwingNet/results/rare_class/transitional_subtypes.csv  (+ the TS ctd correction)
           -> SchwingNet/results/rare_class/stratify.json   {patient_key: subtype[/stratum]}
    plan   a --split-report from `make_context_crops.py --dry-run --stratify-json ...` (+ the patient keys)
           -> SchwingNet/results/rare_class/split_plan.md

WHAT A STRATUM IS. The subtype is the anatomy (L6, T13, sacralised_L5_fused, castellvi_I_II, lumbar_rib,
unassigned). A stratum after the slash is how the MASK represents it, where that decides what a detector can
possibly box, or how strong the truth is:

  sacralised_L5_fused/merged_into_sacrum   CTSP: only 4 lumbar ids, the fused body carries the sacrum id 26 --
                                           the renders can only ever show ONE body there
  sacralised_L5_fused/own_id               L5 keeps its own id (CTSP 24, VerSe raw 24) -- TWO bodies are boxed
  sacralised_L5_fused/four_lumbar_unchecked VerSe 4-lumbar scans whose fused body was not checked at voxel level
  L6/raw_mask                              VerSe L6 verified by raw-mask id 25
  L6/audit_only                            VerSe L6 from the audit string only; the mask was not checked

make_context_crops.py draws within each (value, corpus) cell, so strata are split separately and the
one-body-or-two question is answerable on each.

TWO CORRECTIONS TO THE SUBTYPE TABLE ARE APPLIED HERE, not upstream (both are recorded in the output):
  * TotalSegmentator: the table calls all 12 bench cases L6 off scrambled SPINEPS instance ids. The VERIDAH ctd
    naming (ts12_ctd_subtypes.json) calls 2 L6, 3 T13, 7 normal. The ctd call is used; the 7 normal spines are
    NOT stratified (they are ordinary people and follow the global split).
  * three TS rows carry the key `ts:TS_s1178` form; patient_keys.py keys that person `ts:s1178`. Normalised.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

RC = Path(__file__).resolve().parent.parent / "SchwingNet" / "results" / "rare_class"


def norm_key(k: str) -> str:
    m = re.match(r"^ts:TS_(s\d+)$", k)
    return f"ts:{m.group(1)}" if m else k


def stratum(row: dict, verse_raw: set) -> str:
    sub, src, rep = row["subtype"], row["source"], (row.get("mask_representation") or "")
    if sub == "sacralised_L5_fused":
        if rep.startswith("only 4 lumbar ids"):
            return f"{sub}/merged_into_sacrum"
        if "keeps its own id" in rep:
            return f"{sub}/own_id"
        if rep.startswith("4 lumbar ids in the raw mask"):
            return f"{sub}/four_lumbar_unchecked"
        raise SystemExit(f"unrecognised mask_representation for {row['case']}: {rep[:80]!r}")
    if sub == "L6" and src == "verse":
        return "L6/raw_mask" if row["case"] in verse_raw else "L6/audit_only"
    return sub


def build(a) -> int:
    rows = list(csv.DictReader(open(a.table, newline="")))
    # 2026-09-23: transitional_subtypes.py now applies the VERIFIED TS subtypes itself (ts12_subtype_override.json,
    # F1 TS12_VERIFY.md) and writes the column subtype_veridah. On such a table the ctd json below must NOT be
    # applied again: it calls TS_s1178 L6 (refuted: a normal spine with T12 skipped) and TS_s1088/TS_s1123 T13
    # (L6-pattern under the rib convention). tools/make_split.py is the writer of stratify.json from now on.
    if rows and "subtype_veridah" in rows[0]:
        raise SystemExit(f"{a.table} already carries the verified TS subtypes; re-applying {a.ts_ctd} would undo them. "
                         "stratify.json is written by tools/make_split.py split.")
    ctd = json.load(open(a.ts_ctd))["subtype_by_ctd"]
    verse_raw = set(json.load(open(a.verse56)))
    by_person = defaultdict(set)
    dropped, corrected = {}, {}
    for r in rows:
        k = norm_key(r["patient_key"].strip())
        if not k:
            raise SystemExit(f"row without a patient key: {r['source']} {r['case']}")
        if r["source"] == "totalsegmentator":
            call = ctd.get(r["case"])
            if call is None:
                raise SystemExit(f"TS case {r['case']} has no ctd call")
            if call != r["subtype"]:
                corrected[k] = f"{r['subtype']} -> {call} (VERIDAH ctd)"
            if call == "none":
                dropped[k] = "VERIDAH ctd names a normal spine; not transitional, follows the global split"
                continue
            r = dict(r, subtype=call)
        by_person[k].add(stratum(r, verse_raw))
    # a person whose two series disagree on the stratum: L6/raw_mask wins over L6/audit_only (the mask was checked
    # on one of them); any other disagreement stops the build
    strata = {}
    for k, ss in sorted(by_person.items()):
        if ss == {"L6/raw_mask", "L6/audit_only"}:
            ss = {"L6/raw_mask"}
        if len(ss) != 1:
            raise SystemExit(f"{k} carries two strata {sorted(ss)}")
        strata[k] = ss.pop()
    out = {"_about": "patient_key -> subtype[/stratum] for tools/make_context_crops.py --stratify-json; built by "
                     "tools/rare_class_stratify.py build from transitional_subtypes.csv with the TS ctd correction",
           "_dropped": dropped, "_corrected": corrected}
    out.update(strata)
    Path(a.out).write_text(json.dumps(out, indent=1))
    cnt = defaultdict(int)
    for k, v in strata.items():
        cnt[(v, k.split(":", 1)[0])] += 1
    print(f"{len(strata)} people stratified; {len(dropped)} dropped; {len(corrected)} TS calls corrected")
    for (v, c), n in sorted(cnt.items()):
        print(f"  {v:<42} {c:<11} {n:>3}")
    print("wrote", a.out)
    return 0


def plan(a) -> int:
    rep = json.load(open(a.report))
    keys = json.load(open(a.keys)) if a.keys else None
    cells = rep["cells"]
    L = []
    L.append("# Stratified split plan for the ONE final bank (dry run -- nothing built)\n")
    L.append(f"Seed {rep['seed']}; stratified people drawn ~{1 - rep['stratify_val_frac']:.0%}/"
             f"{rep['stratify_val_frac']:.0%} train/validation WITHIN each (subtype, corpus) cell; every other "
             f"person drawn by the global person shuffle at validation share {rep['val_frac']}. C-ArmLSpine "
             f"patients are forced to validation (real-data check, never trained on). A person's side holds for "
             f"every root and every rendering, because the split is drawn on the patient key, not the file.\n")
    L.append("Roots in this dry run: " + ", ".join(f"`{r}`" for r in rep["roots"]) + "\n")
    if keys:
        L.append(f"Patient keys: `{rep['patient_json']}` -- {len(keys['keys'])} cases -> {keys['n_people']} people "
                 f"over {len(keys['roots'])} roots; **unmatched {len(keys['unmatched'])}**.\n")
    # per subtype (aggregating strata and corpora)
    agg = defaultdict(lambda: [0, 0, 0, 0, 0])
    for c in cells.values():
        s = c["subtype"].split("/", 1)[0]
        g = agg[s]
        g[0] += len(c["people_train"]); g[1] += len(c["people_val"]); g[2] += len(c["people_absent"])
        g[3] += c["frames_train"]; g[4] += c["frames_val"]
    L.append("## Per subtype (people are the statistical unit; frames are renders of them)\n")
    L.append("| subtype | people train | people val | not in any root | frames train | frames val |")
    L.append("|---|---:|---:|---:|---:|---:|")
    for s in sorted(agg):
        g = agg[s]
        L.append(f"| {s} | {g[0]} | {g[1]} | {g[2]} | {g[3]} | {g[4]} |")
    L.append("\n## Per cell (subtype/stratum x corpus) -- the unit the draw is made in\n")
    L.append("| subtype/stratum | corpus | people train | people val | absent | frames train | frames val | frames by root |")
    L.append("|---|---|---:|---:|---:|---:|---:|---|")
    for name in sorted(cells):
        c = cells[name]
        fr = ", ".join(f"{k} {v}" for k, v in sorted(c["frames_by_root"].items()))
        L.append(f"| {c['subtype']} | {c['corpus']} | {len(c['people_train'])} | {len(c['people_val'])} | "
                 f"{len(c['people_absent'])} | {c['frames_train']} | {c['frames_val']} | {fr} |")
    L.append("\n## Validation people by cell (the evidence)\n")
    for name in sorted(cells):
        c = cells[name]
        if c["people_val"]:
            L.append(f"- {c['subtype']} / {c['corpus']}: " + ", ".join(sorted(c["people_val"])))
    side = rep.get("side_of_person", {})
    nv = sum(1 for s in side.values() if s == "val")
    L.append(f"\n## Whole bank\n\n{len(side)} people in these roots: {len(side) - nv} train, {nv} validation "
             f"(stratified and global together). People on both sides: 0 (checked by the builder, which stops "
             f"otherwise).\n")
    dis = rep.get("ann_subtype_disagreements", {})
    L.append(f"## Ann subtype fields against the stratify file\n\n{len(dis)} (person, label) pairs disagree.\n")
    for k, n in sorted(dis.items()):
        L.append(f"- {k}: {n} frames")
    Path(a.out).write_text("\n".join(L) + "\n")
    print("wrote", a.out)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    b = sp.add_parser("build")
    b.add_argument("--table", default=str(RC / "transitional_subtypes.csv"))
    b.add_argument("--ts-ctd", default=str(RC / "ts12_ctd_subtypes.json"))
    b.add_argument("--verse56", default=str(RC / "verse56_subtypes.json"))
    b.add_argument("--out", default=str(RC / "stratify.json"))
    p = sp.add_parser("plan")
    p.add_argument("--report", required=True)
    p.add_argument("--keys", default=None, help="patient_keys_final.json, for the unmatched count")
    p.add_argument("--out", default=str(RC / "split_plan.md"))
    a = ap.parse_args()
    return build(a) if a.cmd == "build" else plan(a)


if __name__ == "__main__":
    raise SystemExit(main())
