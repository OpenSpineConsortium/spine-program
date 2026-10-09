#!/usr/bin/env python
"""EVAL_LEAKS: the recall-against-angle curve on its 17 selection subjects (void) against its re-score on 40 subjects
the gate passes for every detector (results/arc/recall_vs_angle_unseen, grid job 40428072). A read of the two result
files; nothing is re-run here.

    python SchwingNet/results/eval_gate/leaks/arc_old_vs_new.py      # -> leaks/arc_old_vs_new.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARC = HERE.parents[1] / "arc"
OLD = ARC / "recall_vs_angle_selection_leaked" / "recall_vs_angle.json"
NEW = ARC / "recall_vs_angle_unseen" / "recall_vs_angle.json"


def cell(d, det, card, conf, cls="body", tilt="0.0", lat=0.0):
    for x in d["curves"][det][card][conf][cls][tilt]:
        if abs(x["lat"] - lat) < 1e-6:
            return x
    return None


def pooled(d, det, card, conf, cls="body", tilt="0.0"):
    """recall pooled over every lateral angle (n-weighted), the curve's one-number summary"""
    xs = d["curves"][det][card][conf][cls][tilt]
    n = sum(x["n"] for x in xs)
    return dict(n=n, recall=sum(x["recall"] * x["n"] for x in xs) / n if n else None)


def main() -> int:
    o, w = json.load(open(OLD)), json.load(open(NEW))
    out = dict(old=dict(file=str(OLD.relative_to(HERE.parents[3])), subjects=o["n_subjects"], frames_per_card=o["frames_per_card"],
                        gate="none written; CHK-9 arc17: SEEN (the 17 are the val/selection subjects of dc_P_pooled, dc_A, dc_B; "
                             "rx_lodo_carmlspine_1024's parent anchor_none_v2_17-1882 trained on 5 and selected on 1)"),
               new=dict(file=str(NEW.relative_to(HERE.parents[3])), subjects=w["n_subjects"], frames_per_card=w["frames_per_card"],
                        gate={k: w["eval_gate"][k] for k in ("held_out", "overlap", "unresolved", "n_checks")}),
               cells=[])
    for det in w["curves"]:
        for card in w["curves"][det]:
            for conf in ("0.25", "0.74"):
                try:
                    a, b = cell(o, det, card, conf), cell(w, det, card, conf)
                    pa, pb = pooled(o, det, card, conf), pooled(w, det, card, conf)
                except KeyError:
                    continue
                out["cells"].append(dict(detector=det, card=card, conf=conf, lat0_old=a, lat0_new=b,
                                         all_angles_old=pa, all_angles_new=pb))
    json.dump(out, open(HERE / "arc_old_vs_new.json", "w"), indent=1)
    for c in out["cells"]:
        a, b = c["lat0_old"], c["lat0_new"]
        print(f"{c['detector']:10s} {c['card']:14s} {c['conf']}  lat0 {a['recall']:.3f} (n {a['n']}) -> {b['recall']:.3f} "
              f"[{b['lo']:.3f}, {b['hi']:.3f}] (n {b['n']})   all angles {c['all_angles_old']['recall']:.3f} -> "
              f"{c['all_angles_new']['recall']:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
