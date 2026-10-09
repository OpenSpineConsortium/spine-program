"""VERIFY item 2, a fourth CLEAN row (FIGREC:figure2/06, /08, /10): the three C-ArmLSpine L6 patients the Figure 2
held-out embedding calls never seen by the allspine_v9 rung-1 encoder. Read without eval_gate: the encoder's own
training record (result json / registry row / sidecar), its bank's case and source arrays (every split), and the
C-ArmLSpine case names in every string the bank holds.
"""
import glob
import json
import os
import re
import sys
from collections import Counter

import numpy as np

H = os.path.expanduser("~")
BANK = f"{H}/allspine_v9_fov96_ctx"
out = {}
for f in sorted(glob.glob(f"{BANK}/runs/*rung_1*aug2*")) + sorted(glob.glob(f"{BANK}/*.json"))[:20]:
    out.setdefault("files", []).append(f)
side = [f for f in glob.glob(f"{BANK}/runs/*.json") if "rung_1" in f]
for f in side[:6]:
    try:
        d = json.load(open(f))
        out.setdefault("sidecars", {})[f] = {k: d[k] for k in list(d)[:40] if isinstance(d[k], (str, int, float, bool))
                                             or k in ("init", "train_list", "val_list", "bank", "base_model")}
    except Exception as e:  # noqa: BLE001
        out.setdefault("sidecars", {})[f] = f"unreadable: {e}"
z = np.load(f"{BANK}/rung_1.npz", allow_pickle=True)
case = z["case"].astype(str)
split = z["split"].astype(str)
src = z["source"].astype(str) if "source" in z.files else np.array(["?"] * len(case))
out["n_crops"] = int(len(case))
out["splits"] = dict(Counter(split))
out["sources_by_split"] = {s: dict(Counter(src[split == s])) for s in sorted(set(split))}
R = re.compile(r"(?<![0-9A-Za-z])case(42|121|136)(?![0-9])")
hits = sorted({(c, s, so) for c, s, so in zip(case, split, src) if R.search(c)})
out["l6_patient_name_hits"] = [list(h) for h in hits[:50]]
out["n_l6_patient_name_hits"] = len(hits)
carm = sorted({(c, s, so) for c, s, so in zip(case, split, src) if re.search(r"(?i)carm|(?<![0-9A-Za-z])case\d+", c)})
out["any_carmlspine_like_case"] = [list(h) for h in carm[:30]]
out["n_any_carmlspine_like_case"] = len(carm)
# the Figure 2 held-out root: which patients its annotations name
root = "/rs/rs_grp_oschome/go2432/data/rare_class/carmlspine_cbct_drr"
anns = sorted(glob.glob(f"{root}/**/*.json", recursive=True))
pats = Counter()
for a in anns[:5000]:
    try:
        d = json.load(open(a))
    except Exception:  # noqa: BLE001
        continue
    p = d.get("patient") or d.get("case") or os.path.basename(a).split("_")[0]
    pats[str(p)] += 1
out["heldout_root_patients"] = dict(pats.most_common(20))
out["n_heldout_anns"] = len(anns)
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ("sidecars",)}, indent=1)[:4000])
print("sidecars:", json.dumps(out.get("sidecars"), indent=1)[:3000])
