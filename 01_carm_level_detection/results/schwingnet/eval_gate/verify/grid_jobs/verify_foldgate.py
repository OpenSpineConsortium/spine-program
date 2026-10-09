"""VERIFY item 1, device cards: tools/device_fit.fold_gate -- the call cmd_fit makes before it fits -- on the real pair
names of each device, exactly as cmd_gate builds the folds, plus one adversarial fold list (a specimen filed under two
group names). A fold whose held subject was fitted on must raise SeenInEvaluation.
"""
import glob
import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.expanduser("~/spinesurg-ct-nnunet/tools"))
import device_fit as DF  # noqa: E402
import eval_gate as EG  # noqa: E402

out = {}


def frames_of(device, max_folds=6):
    dev = DF.DEVICES[device]
    files = sorted(glob.glob(os.path.join(dev["pairs"], "pair_*.npz")))
    frames = []
    for p in files:
        stem = Path(p).stem.replace("pair_", "")
        spec, pid = stem.rsplit("_", 1)
        frames.append(dict(spec=(pid if dev.get("group_by_pid") else spec), subject_spec=spec))
    groups = sorted({d["spec"] for d in frames})
    if len(groups) > max_folds:
        fold_of = {g: int(hashlib.md5(g.encode()).hexdigest(), 16) % max_folds for g in groups}
        for d in frames:
            d["spec"] = f"fold{fold_of[d['spec']]}"
        groups = sorted({d["spec"] for d in frames})
    return frames, groups


def attempt(label, device, frames, groups):
    try:
        blk = DF.fold_gate(device, frames, groups)
        out[label] = dict(raised=None, held_out=blk["held_out"], overlap=blk["overlap"], n_folds=len(groups))
    except EG.EvalGateError as e:
        out[label] = dict(raised=type(e).__name__, message=str(e).splitlines()[0][:300], n_folds=len(groups))
    print(label, out[label], flush=True)


for dev in ("bv_pulsera", "pixium_4600", "cios_fusion", "elekta_xvi"):
    try:
        fr, gr = frames_of(dev)
    except Exception as e:  # noqa: BLE001
        out[dev] = dict(error=f"{type(e).__name__}: {e}")
        print(dev, out[dev])
        continue
    attempt(dev, dev, fr, gr)

# adversarial: DeepFluoro specimen 18-1109 filed under a second group name in one fold (a re-export named differently);
# the keying must still find it on both sides
fr, gr = frames_of("cios_fusion")
extra = [dict(spec="zz_alias_group", subject_spec="18-1109")]
attempt("cios_fusion + 18-1109 under a second group name", "cios_fusion", fr + extra, sorted(set(gr) | {"zz_alias_group"}))
json.dump(out, open(sys.argv[1], "w"), indent=1)
