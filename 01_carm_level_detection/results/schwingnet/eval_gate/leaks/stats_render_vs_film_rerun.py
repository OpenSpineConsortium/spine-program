#!/usr/bin/env python
"""EVAL_LEAKS: the a3 render-vs-film statistics (tools/rigor_fixes._a3_render_vs_film: paired case-clustered bootstrap,
McNemar, cluster sign test) over the rows `rigor_fixes.py a3a-rows --only-unseen` wrote -- NHANES II spines the gate
passes for BOTH detectors. The verdict of both detectors is carried from a3a_rows_meta.json into the output's first block.

    python SchwingNet/results/eval_gate/leaks/stats_render_vs_film_rerun.py --results <dir with a3a_rows.csv> --out <json>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "tools"))
import eval_gate as EG  # noqa: E402
import rigor_fixes as RF  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--touched", default=None)
    a = ap.parse_args()
    RF._GATE["blocks"], RF._GATE["not_held_out"], RF._GATE["touched"] = [], None, a.touched
    res = RF._a3_render_vs_film(argparse.Namespace(results=a.results))
    for k in ("conf_0.05", "conf_0.25"):
        if isinstance(res.get(k), dict):
            res[k].pop("caveat", None)     # the shipped caveat is about the first 25 spines and the wrong list
    blocks, RF._GATE["blocks"] = RF._GATE["blocks"], []
    out = EG.stamp(res, EG.merge(blocks)) if blocks else res
    json.dump(out, open(a.out, "w"), indent=1, default=RF._jsonable)
    for k in ("conf_0.05", "conf_0.25"):
        r = res.get(k) or {}
        if r:
            print(f"{k}: {r.get('n_items')} bodies / {r.get('n_clusters')} spines  film {r.get('p_a'):.4f}  render {r.get('p_b'):.4f}  "
                  f"diff {r.get('diff_pp'):.1f} pp  pct {[round(x, 1) for x in r.get('percentile_pp') or []]}  "
                  f"spines film>render {r.get('clusters_favouring_a')} vs {r.get('clusters_favouring_b')}  sign p {r.get('cluster_sign_test_p')}")
    print("held_out", (out.get("eval_gate") or {}).get("held_out"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
