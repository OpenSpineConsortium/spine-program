#!/usr/bin/env python
"""EVAL_LEAKS: every checkpoint in the lineage store whose initialisation chain passes through a render-only anchor
detector (anchor_none_v2_*), with what the anchor itself trained and was selected on.

WHY. rx_lodo_carmlspine_1024 -- the headline "real-frames-only" detector -- was initialised from
anchor_none_v2_17-1882, which trained on 14 renders each of five TotalSegmentator subjects and was selected on a sixth.
Any number scored on those subjects, by the anchor or by anything fine-tuned from it, is not held out. This lists the
whole family from touched.json (+ the on-demand rows beside it), so the sweep can name every quoted number that rests
on one of them rather than only the one that was caught.

    python SchwingNet/results/eval_gate/leaks/anchor_descendants.py --touched <touched.json> --out <json>
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "tools"))
import eval_gate as EG  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--touched", default=EG.GRID_TOUCHED)
    ap.add_argument("--pattern", default="anchor_none_v2_")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    store = EG.load_store(a.touched)
    anchors = sorted(k for k in store.entries if a.pattern in k and k.endswith(".pt"))
    out = dict(touched=a.touched, pattern=a.pattern, anchors={}, descendants={})
    for k in anchors:
        e = store.entries[k]
        out["anchors"][k] = dict(train_keys=len(e.get("train_keys") or []), val_keys=len(e.get("val_keys") or []),
                                 train_by_corpus=dict(Counter(x.split(":", 1)[0] for x in e.get("train_keys") or [])),
                                 val_by_corpus=dict(Counter(x.split(":", 1)[0] for x in e.get("val_keys") or [])),
                                 train_sample=sorted(e.get("train_keys") or [])[:12], val_sample=sorted(e.get("val_keys") or [])[:12],
                                 pose_keys=len(set(e.get("train_pose_keys") or []) | set(e.get("val_pose_keys") or [])),
                                 unresolved=len(e.get("unresolved") or []))
    for k, e in store.entries.items():
        if k in anchors:
            continue
        try:
            _, _, nodes, _ = EG.chain_of(k, store, compute=False)
        except EG.EvalGateError:
            continue
        via = [n for n, _ in nodes[1:] if n in anchors]
        if via:
            out["descendants"][k] = dict(anchors=via, parents=e.get("parents") or [], family=e.get("family"),
                                         train_keys=len(e.get("train_keys") or []), val_keys=len(e.get("val_keys") or []),
                                         val_by_corpus=dict(Counter(x.split(":", 1)[0] for x in e.get("val_keys") or [])),
                                         unresolved=len(e.get("unresolved") or []))
    json.dump(out, open(a.out, "w"), indent=1)
    print(f"{len(anchors)} anchors, {len(out['descendants'])} descendants -> {a.out}")
    for k, d in sorted(out["descendants"].items()):
        print(f"  {k}  <- {[x.split('/runs/')[-1] for x in d['anchors']]}  val {d['val_by_corpus']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
