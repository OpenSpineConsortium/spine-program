#!/usr/bin/env python
"""Rebuild the shipped C-ArmLSpine CV fold directories on the release AS IT WAS when the quoted numbers were scored.

WHY. The shipped fold directories (realxray/carmlspine_cv/fold<K>, carmlspine_cvday/fold<K>, written 2026-09-21/22)
are symlinks into realxray/carmlspine and realxray/carmlspine_crops. The export behind them was rewritten on
2026-09-23 04:49-05:28 (images and meta; case118's -58 degree frame became case118_OBL, case134 added) and the crops
were regenerated at 06:14 (results/indomain/INVENTORY.md, "Corrections"). So the same symlinks now point at a
different truth, and a re-run through them changes two things at once: the initialisation and the truth. The shipped
fold-0 model re-run through them (the code-drift control of slurm/carmlspine_cv_v9init.sh) scores 145 lateral
vertebrae where the shipped file scored 146.

WHAT THIS DOES. The pre-repair export was kept whole (realxray/carmlspine_pre_repair_2026-09-23: images, meta,
labels). (1) The k-vertebra crops are regenerated from it with the shipped crop tool (tools/carmlspine_eval.py crops,
deterministic: windows from the truth boxes, no randomness) into realxray/carmlspine_pre_repair_2026-09-23_crops.
(2) Every shipped fold directory is mirrored link for link: the same file names (so the same cases, frames and crops,
by construction), each target moved from the repaired export to the pre-repair one. A link whose pre-repair target is
missing is reported and not made, and so is a regenerated crop of a fold case that the shipped directory did not hold;
either makes the exit status 3. Nothing under realxray/carmlspine* is modified.

WHAT IT CANNOT RESTORE. The whole frames and their meta are exactly the shipped ones (the pre-repair meta was last
written 2026-09-21 20:26-20:47, before the shipped CV was scored at about 22:40). The shipped CROPS were cut earlier, at
19:53, from a meta that the 20:26-20:47 pass then rewrote, and that earlier meta was not kept. Regenerated crops can
therefore differ from the shipped ones. Found on the first run (job 40436575): case13_LAT has one window fewer at every
k (its last crop, k1_5 ... k5_1), in case fold 0 and day fold 2; every other shipped crop name exists. Whether the
pixels of the others match is measured by re-running the SHIPPED fold models on this mirror
(slurm/carmlspine_cv_v9init_prerepair.sh step 4, declared controls), which is the like-for-like old value at k = 1..5.

    python SchwingNet/results/eval_gate/closure/cv_v9/prerepair_fold_dirs.py      # grid, CPU job
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import subprocess
import sys
from pathlib import Path

RX = "/rs/rs_grp_oschome/go2432/data/realxray"
CUR, CUR_CROPS = f"{RX}/carmlspine", f"{RX}/carmlspine_crops"
PRE = f"{RX}/carmlspine_pre_repair_2026-09-23"
PRE_CROPS = f"{PRE}_crops"
SETS = {"carmlspine_cv": (f"{RX}/carmlspine_cv", f"{RX}/carmlspine_cv_prerepair", [0, 1, 2, 3, 4]),
        "carmlspine_cvday": (f"{RX}/carmlspine_cvday", f"{RX}/carmlspine_cvday_prerepair", [0, 1, 2])}
KS = ["full", "1", "2", "3", "4", "5"]
REPO = Path(__file__).resolve().parents[5]


def retarget(t):
    if t.startswith(CUR_CROPS + "/"):
        return PRE_CROPS + t[len(CUR_CROPS):]
    if t.startswith(CUR + "/"):
        return PRE + t[len(CUR):]
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--python", default=sys.executable)
    a = ap.parse_args()
    if not os.path.isdir(os.path.join(PRE_CROPS, "k3")):
        print(f"regenerating the pre-repair crops into {PRE_CROPS}", flush=True)
        subprocess.run([a.python, "-u", str(REPO / "tools" / "carmlspine_eval.py"), "crops", "--data", PRE, "--out", PRE_CROPS],
                       check=True)
    report = dict(pre=PRE, pre_crops=PRE_CROPS, sets={}, problems=[])
    for name, (src_root, dst_root, folds) in SETS.items():
        for K in folds:
            for k in KS:
                sd = os.path.join(src_root, f"fold{K}", f"k{k}")
                dd = os.path.join(dst_root, f"fold{K}", f"k{k}")
                cnt = collections.Counter()
                cases = set()
                for sub in ("images", "meta"):
                    os.makedirs(os.path.join(dd, sub), exist_ok=True)
                    for lp in sorted(glob.glob(os.path.join(sd, sub, "*"))):
                        if not os.path.islink(lp):
                            report["problems"].append(f"not a link: {lp}")
                            continue
                        t = os.readlink(lp)
                        nt = retarget(t)
                        if nt is None:
                            report["problems"].append(f"unexpected target {lp} -> {t}")
                            continue
                        if not os.path.exists(nt):
                            report["problems"].append(f"missing pre-repair target {nt} (for {lp})")
                            cnt[f"{sub}_missing"] += 1
                            continue
                        dst = os.path.join(dd, sub, os.path.basename(lp))
                        if os.path.lexists(dst):
                            if os.readlink(dst) != nt:
                                report["problems"].append(f"existing link differs: {dst}")
                        else:
                            os.symlink(nt, dst)
                        cnt[sub] += 1
                        if sub == "meta":
                            cases.add(json.load(open(nt))["case"])
                # every regenerated crop of this fold's cases must be one the shipped directory held
                if k != "full":
                    have = {os.path.basename(p) for p in glob.glob(os.path.join(dd, "images", "*.png"))}
                    extra = []
                    for mp in glob.glob(os.path.join(PRE_CROPS, f"k{k}", "*", "meta", "*.json")):
                        m = json.load(open(mp))
                        if m["case"] in cases and f"{m['stem']}.png" not in have:
                            extra.append(m["stem"])
                    if extra:
                        report["problems"].append(f"{name} fold{K} k{k}: {len(extra)} regenerated crops of fold cases the "
                                                  f"shipped directory did not hold, e.g. {extra[:3]}")
                    cnt["regenerated_not_in_shipped"] = len(extra)
                report["sets"][f"{name}/fold{K}/k{k}"] = dict(cnt, cases=len(cases))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prerepair_fold_dirs.json")
    json.dump(report, open(out, "w"), indent=1)
    for key, v in report["sets"].items():
        print(key, v)
    print(f"problems: {len(report['problems'])}", *report["problems"][:20], sep="\n  ")
    print("wrote", out)
    return 0 if not report["problems"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
