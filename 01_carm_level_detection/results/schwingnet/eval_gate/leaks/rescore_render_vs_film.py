#!/usr/bin/env python
"""EVAL_LEAKS re-read: the render-trained vs film-trained detector comparison on the spines NEITHER detector saw.

WHY. results/a3.json#comparisons/render_vs_film_detector (NUMBERS.md 'render-trained vs film-trained detector on 233
bodies / 25 spines ... 71.67 % vs 99.14 %'; Table 2; supplement) scores anchor_det_v1 (renders only) and
detect_v5z_final (films) on 25 NHANES II spines. The shipped caveat counted 196 of the 233 bodies as in-sample against
the allspine_v7 LEVEL bank -- the wrong list. CHK-9 checks each spine's patient key against the train AND val lists of
each detector and of every ancestor (touched.json). This re-reads SchwingNet/results/a3a_rows.csv (one row per truth
body, found_render / found_film at conf 0.05 as scored) and restates the comparison on the spines the gate passes for
BOTH detectors, and for each detector alone. Nothing is re-run: the rows are the rows a3 was computed from.

    python SchwingNet/results/eval_gate/leaks/rescore_render_vs_film.py [--touched <touched.json>]
        -> SchwingNet/results/eval_gate/leaks/render_vs_film_unseen.json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "tools"))
import eval_gate as EG  # noqa: E402
import patient_keys as PK  # noqa: E402

ROWS = REPO / "SchwingNet" / "results" / "a3a_rows.csv"
HOMEG = "/wsu/home/go/go24/go2432"
DET = {"render": f"{HOMEG}/FluoroCap/anchor_det_v1.pt",
       "film": f"{HOMEG}/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt"}


def summary(rows, spines):
    R = [r for r in rows if r["spine"] in spines]
    n = len(R)
    if not n:
        return dict(bodies=0, spines=0)
    fr = sum(int(r["found_render"]) for r in R)
    ff = sum(int(r["found_film"]) for r in R)
    by = defaultdict(lambda: [0, 0, 0])
    for r in R:
        b = by[r["spine"]]
        b[0] += 1
        b[1] += int(r["found_render"])
        b[2] += int(r["found_film"])
    fav_film = sum(1 for b in by.values() if b[2] > b[1])
    fav_render = sum(1 for b in by.values() if b[1] > b[2])
    return dict(bodies=n, spines=len(by), render_found=fr, film_found=ff, render_recall=fr / n, film_recall=ff / n,
                film_minus_render_pp=100.0 * (ff - fr) / n, spines_favouring_film=fav_film,
                spines_favouring_render=fav_render, per_spine={k: dict(bodies=v[0], render=v[1], film=v[2]) for k, v in by.items()})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--touched", default=str(REPO / "SchwingNet" / "results" / "eval_gate" / "touched.json"))
    ap.add_argument("--out", default=str(HERE / "render_vs_film_unseen.json"))
    a = ap.parse_args()
    rows = [r for r in csv.DictReader(open(ROWS, newline="")) if r.get("conf") in ("0.05", "0.050")]
    spines = sorted({r["spine"] for r in rows})
    key_of = {s: PK.canon_key(next(r["patient"] for r in rows if r["spine"] == s)) for s in spines}
    verdict = {}
    for name, ck in DET.items():
        per = {}
        for s in spines:
            h = EG.assess([key_of[s]], ck, "leaks/rescore_render_vs_film.py", eval_set=f"nhanes25:{s}",
                          touched=a.touched, compute=False)
            per[s] = dict(key=key_of[s], overlap=h["overlap"], unresolved=h["unresolved"],
                          where=h.get("overlap_by") or {}, held_out=bool(h["overlap"] == 0 and h["unresolved"] == 0))
        verdict[name] = per
    unseen = {n: sorted(s for s in spines if verdict[n][s]["held_out"]) for n in DET}
    both = sorted(set(unseen["render"]) & set(unseen["film"]))
    seen_film = sorted(s for s in spines if verdict["film"][s]["overlap"])
    unres = {n: sorted(s for s in spines if verdict[n][s]["unresolved"]) for n in DET}
    out = dict(
        source=str(ROWS.relative_to(REPO)), conf=0.05, touched=a.touched, detectors=DET,
        as_quoted=summary(rows, set(spines)),
        unseen_by_both=dict(spine_ids=both, **{k: v for k, v in summary(rows, set(both)).items() if k != "per_spine"}),
        unseen_by_film_detector=dict(spine_ids=unseen["film"],
                                     **{k: v for k, v in summary(rows, set(unseen["film"])).items() if k != "per_spine"}),
        film_detector_seen=dict(n_spines=len(seen_film), where=dict(
            (k, sum(1 for s in seen_film if k in verdict["film"][s]["where"]))
            for k in sorted({w for s in seen_film for w in verdict["film"][s]["where"]}))),
        unresolved=unres, per_spine_gate=verdict)
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=1)
    q, b = out["as_quoted"], out["unseen_by_both"]
    print(f"as quoted: {q['spines']} spines / {q['bodies']} bodies  render {q['render_recall']:.4f}  film {q['film_recall']:.4f}")
    print(f"unseen by both: {b.get('spine_ids')}  bodies {b.get('bodies')}  render {b.get('render_recall')}  film {b.get('film_recall')}")
    print(f"film detector saw {len(seen_film)} of {len(spines)} spines: {out['film_detector_seen']['where']}")
    print(f"unresolved: { {k: len(v) for k, v in unres.items()} }")
    return 0


if __name__ == "__main__":
    sys.exit(main())
