#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/spineps_ids_f5_checks.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""F5 adversarial checks of the SPINEPS-id repair: what the "clean" consumers still carry from VERIDAH's own naming.

json/csv only, no masks, runs anywhere (SchwingNet/results/spineps_ids/VERIFY.md items 1 and 3):

  skips      post-fix trees (carmlspine, cobra lstv/seg, cobra_varian, spineps/ctsp): ctds that skip a mandatory name
             at a normal spacing (tools/spineps_ids._ctd_gaps on the census instance centroids, which equal the ctd
             names in these verse_ok trees), and the G3 COBRA transitional calls that rest on one;
  ctsp_shift the post-fix CTSP masks the guard PASSES whose lumbar names are on the wrong bone by the reader labels
             (>= 2 of L1-L5 with Dice < 0.5 in the post-fix re-score, repair/rescore/ctsp_postfix/per_case.csv);
  polypose   the same test on PolyPose's inspected CTSP cases (results/polypose/validation/inspect/inspect.json);
  carm_l6    TotalSegmentator's names beside VERIDAH's on the three C-ArmLSpine "L6 patients" (carmlspine levels.json).

    python tools/spineps_ids_f5_checks.py --census SchwingNet/results/spineps_ids/census_rows.jsonl.gz \
        --stratify SchwingNet/results/rare_class/stratify.json --cases benchmark/cases.csv \
        --rescore SchwingNet/results/spineps_ids/repair/rescore/ctsp_postfix/per_case.csv \
        --polypose SchwingNet/results/polypose/validation/inspect/inspect.json \
        --carm-levels <copy of /rs/rs_grp_oschome/go2432/data/carmlspine/levels.json> --out <json>
"""
import argparse
import csv
import gzip
import json
import os
import re
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spineps_ids as S  # noqa: E402

LUMBAR = ["L1", "L2", "L3", "L4", "L5"]


def call_of(labs):
    return ("L6" if 25 in labs and 28 not in labs else "T13" if 28 in labs and 25 not in labs
            else "both" if 25 in labs else "none")


def tree_of(p):
    if "/carmlspine/spineps/" in p:
        return "carmlspine_veridah" if p.endswith("_veridah.nii.gz") else "carmlspine"
    if "/cobra2026/lstv/seg/" in p:
        return "cobra_lstv"
    if "/spineps/cobra_varian/" in p:
        return "cobra_varian"
    if "/spineps/ctsp/" in p:
        return "ctsp_postfix"
    return None


def skips(census, strat):
    rows = [json.loads(l) for l in gzip.open(census, "rt")]
    tally, out = Counter(), defaultdict(list)
    for r in rows:
        t = tree_of(r["path"]) if r.get("kind") == "seg-vert" else None
        if not t:
            continue
        labs = set(int(x) for x in (r.get("ctd_labels") or []))
        pts = {int(k): np.asarray(v, float) for k, v in (r.get("centroid_ras") or {}).items()
               if int(k) in S.ANAT and int(k) in labs}
        tally[t] += 1
        tally[f"{t}|call|{call_of(labs)}"] += 1
        if len(pts) < 2:
            continue
        try:
            ref, _ = S._ctd_gaps(pts)
        except Exception:  # noqa: BLE001
            continue
        sk = [g for g in ref if "normal vertebral spacing" in g.get("why", "")]
        if sk:
            tally[f"{t}|skip"] += 1
            tally[f"{t}|skip|{call_of(labs)}"] += 1
            out[t].append(dict(case=r["case"], call=call_of(labs),
                               ctd=[S.name(x) for x in sorted(labs, key=lambda l: S.ANAT.get(l, 99))], skip=sk[0]))
    cobra = json.load(open(strat))["cobra"]
    on_skip = {d["case"] for t in ("cobra_lstv", "cobra_varian") for d in out.get(t, [])}
    calls = {k: v for k, v in cobra.items() if v["status"] == "transitional_call"}
    return dict(tally=dict(sorted(tally.items())), skips=dict(out),
                g3_cobra_transitional_calls=dict(Counter(v["call"] for v in calls.values())),
                g3_cobra_L6_calls_without_L1=sorted(k for k, v in calls.items()
                                                    if v["call"] == "L6" and not re.search(r"\bL1\b", v["reason"])),
                g3_cobra_T13_calls_L1_to_L4_only=sorted(k for k, v in calls.items()
                                                        if v["call"] == "T13" and "L5" not in v["reason"]),
                g3_cobra_calls_on_skipped_ctd=sorted(k for k in calls if k.split(":", 1)[1] in on_skip))


def ctsp_shift(cases, rescore, skip_ctsp_ids):
    ct2tok, tok2ct = {}, {}
    for r in csv.DictReader(open(cases)):
        m = re.search(r"/(\d{4})_ct\.nii", r["ct"])
        if m:
            ct2tok[m.group(1)], tok2ct[r["case"]] = r["case"], m.group(1)
    skip_tok = {ct2tok.get(i) for i in skip_ctsp_ids}
    per = {r["case"]: r for r in csv.DictReader(open(rescore))}
    c, shifted = Counter(), []
    for tok, r in per.items():
        grp = "t12_skip_refused" if tok in skip_tok else "guard_passes"
        low = [l for l in LUMBAR if r[f"dice_{l}"] != "" and float(r[f"dice_{l}"]) < 0.5]
        k = "lumbar_names_shifted" if len(low) >= 2 else ("one_low" if low else "ok")
        c[f"{grp}|{r['status']}|{k}"] += 1
        if grp == "guard_passes" and k == "lumbar_names_shifted":
            shifted.append(dict(ctsp=tok2ct.get(tok), token=tok, status=r["status"], subtype=r["subtype"],
                                gt_lumbar=r["gt_lumbar"], pred_lumbar=r["pred_lumbar"], low=low))
    return dict(counts=dict(sorted(c.items())), guard_passes_shifted=sorted(shifted, key=lambda x: x["ctsp"])), tok2ct, per


def polypose(inspect, tok2ct, per):
    ct2tok = {v: k for k, v in tok2ct.items()}
    d = json.load(open(inspect))
    out = {}
    for c, v in d.items():
        r = per.get(ct2tok.get(c))
        if not r:
            out[c] = "no rescore row"
            continue
        lv = ["T10", "T11", "T12", "T13"] + LUMBAR + ["L6"]
        out[c] = dict(body_mask=(v.get("body_mask") or {}).get("path"), subtype=r["subtype"],
                      gt_lumbar=r["gt_lumbar"], pred_lumbar=r["pred_lumbar"],
                      dice_below_0_5=[l for l in lv if r[f"dice_{l}"] != "" and float(r[f"dice_{l}"]) < 0.5])
    return out


def carm_l6(levels, cases=("case42", "case121", "case136")):
    L = json.load(open(levels))
    L = L.get("cases", L)
    return {c: dict(pairs=[dict(ts=x["ts"], veridah=x["spineps"], dice=x["dice"], level=x["level"])
                           for x in L[c]["vertebrae"]], flags=L[c].get("variant_flags"),
                    agreed_levels=[x["level"] for x in L[c]["vertebrae"] if x["level"]]) for c in cases if c in L}


def main():
    ap = argparse.ArgumentParser()
    for k in ("census", "stratify", "cases", "rescore", "polypose", "carm_levels", "out"):
        ap.add_argument("--" + k.replace("_", "-"), required=True)
    a = ap.parse_args()
    res = dict(skips=skips(a.census, a.stratify))
    skip_ids = [d["case"].split("_", 1)[1] for d in res["skips"]["skips"].get("ctsp_postfix", [])]
    res["ctsp_shift"], tok2ct, per = ctsp_shift(a.cases, a.rescore, skip_ids)
    res["polypose_inspect"] = polypose(a.polypose, tok2ct, per)
    res["carm_l6"] = carm_l6(a.carm_levels)
    json.dump(res, open(a.out, "w"), indent=1, default=str)
    s = res["skips"]
    print(json.dumps(dict(tally=s["tally"], cobra_calls_on_skip=s["g3_cobra_calls_on_skipped_ctd"],
                          L6_without_L1=len(s["g3_cobra_L6_calls_without_L1"]),
                          T13_L1_L4_only=len(s["g3_cobra_T13_calls_L1_to_L4_only"]),
                          ctsp_shift=res["ctsp_shift"]["counts"]), indent=1))


if __name__ == "__main__":
    main()
