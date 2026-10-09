#!/usr/bin/env python
"""EVAL_LEAKS: the C-ArmLSpine zero-shot naming cells scored exactly as tools/rigor_fixes.py a7 scores `zeroshot2`,
on the `zeroshot_v9` prototype runs that already exist on the grid.

WHY. Every zero-shot row the manuscript quotes (96.3 % lateral, 37.9 % AP, lateral minus AP) was scored by the
allspine_v2_r1 encoder, whose training bank was deleted on 2026-09-20; CHK-9 therefore cannot establish what it saw
(UNRESOLVED, unknown is not clean). `zeroshot_v9_det_{train,val,test}` ran the same prototype over the same 148 cases
with the allspine_v9 encoder, whose lineage is complete (touched.json: no parent but declared ImageNet, no unresolved
link, no carmlspine key in train or val). This is NOT the same model -- it is the lineage-complete replacement the
manuscript could quote instead -- and the v9 run also used a recurrent head (head_allspine_v9_mixed_kmax4_seed0) where
zeroshot2 used none. Each score file is gated before it is read (rigor_fixes._gate_input -> eval_gate.carry: a pre-gate
dump is gated from its prototype_meta.json models).

    python SchwingNet/results/eval_gate/leaks/rescore_zeroshot_v9.py --out <json>      # grid; reads carmlspine/proto
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "tools"))
import eval_gate as EG  # noqa: E402
import rigor_fixes as RF  # noqa: E402

PROTO = "/rs/rs_grp_oschome/go2432/data/carmlspine/proto"


def cells(pattern, not_held_out=None):
    """The cells of one prototype run family. zeroshot2 is read under a declaration (its encoder's lineage is
    unresolved, so the strict gate refuses it -- that refusal is recorded separately), only to reproduce the quoted
    cells beside the replacement; zeroshot_v9 is read under the strict gate."""
    out = {}
    RF._GATE["blocks"], RF._GATE["not_held_out"] = [], not_held_out
    try:
        got = RF.cv_items(PROTO, pattern, "det", ks=["full"])
    finally:
        blocks, RF._GATE["blocks"], RF._GATE["not_held_out"] = RF._GATE["blocks"], [], None
    out["eval_gate"] = EG.merge(blocks) if blocks else None
    for k, (items, frames, files) in got.items():
        for view in ("LAT", "AP"):
            I = [x for x in items if x["view"] == view]
            if not I:
                continue
            ans = [x for x in I if not x["abstain"]]
            out[f"{pattern}/det/{view}/k{k}"] = dict(
                files=files, vertebrae=len(I), cases=len({x["case"] for x in I}),
                exact_full_coverage=RF.prop_ci(I, "case", "exact"),
                answered=RF.prop_ci([dict(case=x["case"], v=int(not x["abstain"])) for x in I], "case", "v"),
                exact_on_answered=RF.prop_ci(ans, "case", "exact") if ans else None,
                _items=I)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    res = {}
    # the strict gate first, on both: what it says is the verdict; the declared read of zeroshot2 only reproduces
    # the quoted cells so the old and new numbers sit side by side
    for pat in ("zeroshot2", "zeroshot_v9"):
        try:
            res[pat] = cells(pat)
        except Exception as e:  # noqa: BLE001  (a refused gate is reported, never skipped)
            res[pat] = dict(error=f"{type(e).__name__}: {str(e)[:1500]}")
    if "error" in res["zeroshot2"]:
        why = ("EVAL_LEAKS reproduction of the quoted zero-shot cells: the strict gate refused them ("
               + res["zeroshot2"]["error"][:300] + ")")
        try:
            res["zeroshot2_declared"] = cells("zeroshot2", not_held_out=why)
        except Exception as e:  # noqa: BLE001
            res["zeroshot2_declared"] = dict(error=f"{type(e).__name__}: {str(e)[:1500]}")
    # lateral minus AP on matched cases, as a3 zeroshot_lateral_vs_ap reads it (case-level exact-coverage difference)
    for pat in ("zeroshot2", "zeroshot2_declared", "zeroshot_v9"):
        c = res.get(pat) or {}
        pre = pat.replace("_declared", "")
        L, A = c.get(f"{pre}/det/LAT/kfull"), c.get(f"{pre}/det/AP/kfull")
        if isinstance(L, dict) and isinstance(A, dict) and "_items" in L:
            byc = {}
            for view, C in (("LAT", L), ("AP", A)):
                for x in C["_items"]:
                    byc.setdefault(x["case"], {}).setdefault(view, []).append(int(x["exact"]))
            both = {k: v for k, v in byc.items() if "LAT" in v and "AP" in v}
            lat_better = sum(1 for v in both.values() if sum(v["LAT"]) / len(v["LAT"]) > sum(v["AP"]) / len(v["AP"]))
            ap_better = sum(1 for v in both.values() if sum(v["AP"]) / len(v["AP"]) > sum(v["LAT"]) / len(v["LAT"]))
            res[pat]["lateral_vs_ap_cases"] = dict(cases_with_both=len(both), lateral_better=lat_better, ap_better=ap_better)
            # the paired contrast exactly as rigor_fixes._a3_zeroshot_lat_vs_ap pairs it: by (case, truth level)
            by = {}
            for view, C in (("LAT", L), ("AP", A)):
                for x in C["_items"]:
                    by.setdefault((x["case"], x["truth"]), {})[view] = x
            rows = [dict(case=c, lat=v["LAT"]["exact"], ap=v["AP"]["exact"]) for (c, _), v in by.items() if "LAT" in v and "AP" in v]
            res[pat]["lateral_minus_ap_paired"] = dict(RF.paired_ci(rows, "case", "lat", "ap"), matched_vertebrae=len(rows))
    for pat in res:
        for k, v in list(res[pat].items()):
            if isinstance(v, dict):
                v.pop("_items", None)
    json.dump(res, open(a.out, "w"), indent=1, default=str)
    for pat, c in res.items():
        for k, v in c.items():
            if isinstance(v, dict) and "exact_full_coverage" in v:
                e = v["exact_full_coverage"]
                print(f"{k:32s} {e['k']}/{e['n']} = {e['point']:.4f} pct {[round(x, 4) for x in e['percentile']]} "
                      f"cases {e['clusters']}  answered {v['answered']['point']:.3f}")
            elif k == "error" or k == "lateral_vs_ap_cases":
                print(pat, k, v)
    return 0


if __name__ == "__main__":
    sys.exit(main())
