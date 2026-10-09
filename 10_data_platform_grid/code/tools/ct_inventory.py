#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/ct_inventory.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Every CT collection on this machine, how many distinct SUBJECTS each holds, and what truth it carries.

WHY. The benchmark's CT axis was written against the 802 CTSpinoPelvic1K records, which are abdominopelvic and
therefore see only the lower spine. Scoring a whole-spine counting method on that collection alone understates both
the range of anatomy it meets and the number of scans behind it. This file inventories what is actually here, by
distinct subject rather than by file, so the protocol can name a case list instead of a folder.

Distinct subject, not distinct render: a bank holds several poses and views of one CT (`<case>_lat_p3`), and several
banks hold the same person under different names. Subjects are counted with `tools.patient_keys`, the same keying
the split uses, so the number here and the number the split draws on cannot disagree.

    python tools/ct_inventory.py --out docs/CT_INVENTORY.md --json docs/CT_INVENTORY.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

import patient_keys as PK  # noqa: E402  (same directory)

HOME = Path(os.path.expanduser("~"))

# render bank -> (collection, what the labels are, what a whole-spine method sees)
BANKS = [
    ("ctsp_drr",       "CTSpinoPelvic1K",        "release labels, per level + ribs + pelvis", "abdominopelvic FOV"),
    ("physics_drr",    "CTSpinoPelvic1K",        "release labels", "abdominopelvic FOV, physics-styled"),
    ("physics_rare",   "CTSpinoPelvic1K (rare)", "release labels", "transitional subset"),
    ("verse_drr",      "VerSe 19/20",            "VerSe masks, C1-L6", "whole spine"),
    ("verse_soft_drr", "VerSe 19/20",            "VerSe masks", "whole spine, soft-tissue render"),
    ("ts_drr",         "TotalSegmentator v2",    "TS labels mapped by name", "whole body"),
    ("ts_drr_v3",      "TotalSegmentator v3",    "TS v3 labels mapped by name", "whole body"),
    ("spinalai_drr",   "SpinalAI",               "pseudolabels", "whole spine"),
    ("aasce_drr",      "AASCE",                  "pseudolabels", "whole spine"),
    ("anchor_drr",     "anchor set",             "release labels", "anchor crops"),
    ("carm_drr",       "C-ArmLSpine CBCT",       "SPINEPS + TS agreement", "lumbar CBCT"),
    ("fluorocap_drr",  "FluoroCap",              "none (test films)", "mixed"),
]
# CT roots on this machine. Each is probed rather than assumed: a root that is not here is reported absent instead
# of quietly contributing zero to a total.
CT_ROOTS = [
    ("CTSpinoPelvic1K",     "~/data/CTSpinoPelvic1K/ct"),
    ("VerSe 19/20",         "~/VerSeFusion/data/unified"),
    ("TotalSegmentator v2", "~/data/TotalSegmentator"),
    ("TotalSegmentator v3", "~/data/TotalSegmentator_v3"),
    ("RSNA cervical spine", "~/data/rsna_cspine"),
    ("spondylolisthesis landmarks", "~/data/spondy_landmark"),
    ("COBRA 2026",          "/rs/rs_grp_oschome/go2432/data/cobra2026"),
    ("C-ArmLSpine CBCT",    "/rs/rs_grp_oschome/go2432/data/carmlspine"),
    ("Ljubljana",           "/rs/rs_grp_oschome/go2432/data/ljubljana"),
    ("DeepFluoro (vendor)", "/rs/rs_grp_oschome/go2432/data/deepfluoro_vendor"),
    ("Geneva hip",          "/rs/rs_grp_oschome/go2432/data/geneva_hip_src"),
    ("SpineSAC",            "/rs/rs_grp_oschome/go2432/data/spinesac"),
]


def count_volumes(root):
    """(n_nifti, n_subdirs) under a root, without walking a deep tree more than twice."""
    p = Path(os.path.expanduser(root))
    if not p.exists():
        return None
    n_nii = len(list(p.glob("*.nii.gz"))) + len(list(p.glob("*/*.nii.gz")))
    n_dir = sum(1 for c in p.iterdir() if c.is_dir())
    return n_nii, n_dir
POSE = re.compile(r"_(?:lat|ap|obl\d*)_p\d+$")


def bank_subjects(bank, cross):
    r = HOME / bank
    ann = r / "ann"
    if not ann.exists():
        return None
    cases, people, unkeyed = 0, set(), 0
    for p in ann.glob("*.json"):
        cases += 1
        try:
            a = json.load(open(p))
        except Exception:                                    # noqa: BLE001
            a = None
        k = PK.key_for(p.stem, a, cross)
        if k is None:
            unkeyed += 1
            people.add("unkeyed:" + POSE.sub("", p.stem))     # counted, but flagged
        else:
            people.add(f"{k[0]}:{k[1]}")
    return dict(bank=bank, renders=cases, subjects=len(people), unkeyed=unkeyed,
                corpora=sorted({p.split(":")[0] for p in people}))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="docs/CT_INVENTORY.md")
    ap.add_argument("--json", default="docs/CT_INVENTORY.json")
    ap.add_argument("--d813", default="~/spinesurg-ct-nnunet/nnunet/raw/Dataset813_SpineSurgLSTVFullRibs")
    a = ap.parse_args()
    cross = PK.d813_crosswalk(a.d813)
    rows = []
    for bank, coll, truth, fov in BANKS:
        r = bank_subjects(bank, cross)
        if r is None:
            continue
        r.update(collection=coll, truth=truth, fov=fov)
        rows.append(r)
        print(f"{bank:<16} {r['renders']:>7} renders  {r['subjects']:>6} subjects  unkeyed {r['unkeyed']}", flush=True)

    vols = []
    for name, root in CT_ROOTS:
        c = count_volumes(root)
        vols.append(dict(collection=name, root=str(Path(os.path.expanduser(root))),
                         nifti=(c[0] if c else 0), subdirs=(c[1] if c else 0), present=c is not None))
        print(f"{name:<30} {'absent' if c is None else f'{c[0]:>6} nii, {c[1]:>6} dirs'}", flush=True)

    all_people = sum(r["subjects"] for r in rows)

    Path(a.json).parent.mkdir(parents=True, exist_ok=True)
    json.dump(dict(banks=rows, volumes=vols, sum_of_bank_subjects=all_people), open(a.json, "w"), indent=1)

    L = ["# Every CT collection here, by distinct subject", "",
         "Generated by `tools/ct_inventory.py`. Subjects are counted with `tools/patient_keys.py`, the same keying the",
         "split uses, so a bank's subject count and the number of people its split draws on cannot disagree.", "",
         "## Render banks", "",
         "| bank | collection | renders | distinct subjects | unkeyed | truth | field of view |",
         "|---|---|---:|---:|---:|---|---|"]
    for r in rows:
        L.append(f"| `{r['bank']}` | {r['collection']} | {r['renders']} | {r['subjects']} | {r['unkeyed']} | "
                 f"{r['truth']} | {r['fov']} |")
    L += ["", "## CT volumes on disk", "",
          "`nii` counts NIfTI files at the root and one level below it; `dirs` counts per-subject directories, which is",
          "the right number for the collections that ship one folder per subject (TotalSegmentator, the CBCT sets).", "",
          "| collection | nii | dirs | root |", "|---|---:|---:|---|"]
    for v in vols:
        if not v["present"]:
            L.append(f"| {v['collection']} | absent | absent | `{v['root']}` |")
        else:
            L.append(f"| {v['collection']} | {v['nifti']} | {v['subdirs']} | `{v['root']}` |")
    L += ["", "Bank subject counts are NOT additive across banks: several banks render the same collection. The",
          "benchmark's case list is drawn on patient keys over the union, which is what `tools/patient_keys.py` writes.", ""]
    Path(a.out).write_text("\n".join(L), encoding="utf-8")
    print("wrote", a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
