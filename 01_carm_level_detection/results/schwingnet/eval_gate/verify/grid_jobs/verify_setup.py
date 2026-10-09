"""VERIFY item 1, setup (grid, inside the job): the inputs each wired evaluator is called with.

Nothing here is a real evaluation set. Each input exists only to put a patient the checkpoint (or an ancestor) saw in
front of an evaluator, so that the evaluator's own gate call has to refuse it before anything is scored.

  ARC17  the 17 TotalSegmentator subjects the void arc curve was scored on (val/selection subjects of every dc_* arm)
  s0970  a subject in the TRAIN set of anchor_none_v2_17-1882 only: an ancestor of rx_lodo_carmlspine_1024, never in
         rx_lodo's own lists
  CTSP_0001  a subject in the TRAIN set of model_scal_pt_render.pt only: the ancestor of model_scal_pt_ft.pt
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

V = Path(sys.argv[1])
ARC17 = ["s0585", "s0970", "s1045", "s1062", "s1159", "s1384", "s1535", "s1579", "s1700", "s1836", "s1842", "s1872",
         "s1880", "s1883", "s1902", "s2033", "s2053"]
LEVELS = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11",
          "T12", "T13", "L1", "L2", "L3", "L4", "L5", "L6", "sacrum"]
RUNS = "/wsu/home/go/go24/go2432/spine-detector/runs"
P_POOLED = f"{RUNS}/devcorpus/dc_P_pooled/weights/best.pt"
RX_POOLED = f"{RUNS}/realxray/rx_pooled_1024/weights/best.pt"
GT = "/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/touched.json"


def png(p):
    p.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.full((64, 64), 128, np.uint8)).save(p)


def rx_root(name, subjects):
    """A realxray-layout root (images/test + meta) of anglesweep-named frames whose meta `case` is the TS subject."""
    r = V / name
    for s in subjects:
        stem = f"{s}_lat+000_tilt+00"
        png(r / "images" / "test" / f"{stem}.png")
        (r / "meta").mkdir(parents=True, exist_ok=True)
        json.dump({"case": f"TS_{s}", "boxes": []}, open(r / "meta" / f"{stem}.json", "w"))


def set_root(name, subjects):
    r = V / name
    r.mkdir(parents=True, exist_ok=True)
    json.dump({"subjects": subjects, "anchor_tag": "verify", "note": "VERIFY fixture, not an evaluation set"},
              open(r / "SET_INFO.json", "w"))


def img_dir(name, stems):
    for s in stems:
        png(V / name / f"{s}.png")


def bank(name, val_cases, train_cases):
    r = V / name
    r.mkdir(parents=True, exist_ok=True)
    json.dump({"classes": LEVELS}, open(r / "meta.json", "w"))
    case = [c for c in val_cases for _ in range(2)] + [c for c in train_cases for _ in range(2)]
    split = ["val"] * (2 * len(val_cases)) + ["train"] * (2 * len(train_cases))
    n = len(case)
    np.savez(r / "rung_1.npz", X=np.zeros((n, 2, 8, 8), np.uint8), y=np.array([22, 23] * (n // 2)),
             case=np.array(case), split=np.array(split), source=np.array(["verify"] * n),
             scale=np.full((n, 2), np.nan, np.float32))


rx_root("rx_arc17", ARC17)
rx_root("rx_anc", ["s0970"])
set_root("set_anc", ["s0970"])
(V / "subjects_arc17.txt").write_text("\n".join(ARC17) + "\n")
(V / "subjects_anc.txt").write_text("s0970\n")
img_dir("img_arc17", [f"TS_{s}" for s in ARC17])
img_dir("img_anc", ["TS_s0970"])
img_dir("img_ctsp", ["CTSP_0001"])
bank("bank_arc17", [f"TS_{s}" for s in ARC17], ["TS_s0224"])
bank("bank_ctsp", ["CTSP_0001"], ["CTSP_0999"])
json.dump({"keys": {}}, open(V / "keys_empty.json", "w"))

# case134: no checkpoint in the store descends from one that saw case134, so a synthetic store is written in which
# dc_P_pooled's row names rx_pooled_1024 (which trained on case134 by the export's md5 split) as its parent; every other
# row is the real one. The spin evaluator must refuse dc_P_pooled THROUGH that parent.
T = json.load(open(GT))
syn = {k: T[k] for k in [RX_POOLED] + list(T[RX_POOLED].get("ancestors") or []) + list(T[RX_POOLED].get("parents") or [])}
syn.update({
       P_POOLED: dict(T[P_POOLED], parents=[RX_POOLED], ancestors=[RX_POOLED], train_keys=[], val_keys=[],
                      touched_keys=[], sha=None, _verify="SYNTHETIC: parent grafted to test the ancestor walk")})
json.dump(syn, open(V / "synthetic_touched_case134.json", "w"))
print("setup done", sorted(p.name for p in V.iterdir()))
print("rx_pooled_1024 has carmlspine:case134 in", [s for s in ("train_keys", "val_keys")
                                                   if "carmlspine:case134" in (T[RX_POOLED].get(s) or [])])
