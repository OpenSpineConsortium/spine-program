"""VERIFY item 1, the keys-map route (grid): tools/learning_embed.py gates the bank's val crops as
`keys.get(case) or dict(case=case)`, so where ~/patient_keys_v9.json has a value, that pre-formed key is the only thing
checked. The map spells implant renders `implant:<case>_v<k>`; the lineage store keys the same renders to their SOURCE CT
(patient_keys.key_any through the implant records). This counts, over the v9 bank's val split, how many val cases the
map sends to an `implant:` key, what the gate's own keying (eval_gate.key_items on the case name) calls them, and how
many of those resolved persons are in the v9 encoder's TRAIN keys -- i.e. overlap the gate cannot see when handed the map.
"""
import json
import os
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.expanduser("~/spinesurg-ct-nnunet/tools"))
import eval_gate as EG  # noqa: E402

BANK = os.path.expanduser("~/allspine_v9_fov96_ctx/rung_1.npz")
V9 = "/wsu/home/go/go24/go2432/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt"
keys = json.load(open(os.path.expanduser("~/patient_keys_v9.json")))["keys"]
z = np.load(BANK, allow_pickle=True)
case, split = z["case"].astype(str), z["split"].astype(str)
val_cases = sorted(set(case[split == "val"]))
store = EG.load_store()
e = store.entries[V9]
train = {EG.PK.canon_key(k) for k in e["train_keys"]}
val = {EG.PK.canon_key(k) for k in e["val_keys"]}

imp = [c for c in val_cases if str(keys.get(c, "")).startswith("implant:")]
rows, by = [], Counter()
for c in imp:
    k, _, unk = EG.key_items([dict(case=c)])
    k = sorted(k)
    where = ("train" if set(k) & train else "") + ("+val" if set(k) & val else "")
    by[where or ("unkeyed" if unk else "neither")] += 1
    rows.append(dict(case=c, map_key=keys[c], gate_key=k, in_v9=where))
mapped = [keys.get(c) or c for c in val_cases]
hidden = sum(1 for r in rows if "train" in r["in_v9"])
# persons: what the gate sees as TRAIN overlap when handed the map (learning_embed's items) vs when it keys every case
items_map = [keys.get(c) or dict(case=c) for c in val_cases]
k_map = EG.key_items(items_map)[0]
k_own = EG.key_items([dict(case=c) for c in val_cases])[0]
tr_map, tr_own = k_map & train, k_own & train
hidden_persons = sorted(tr_own - tr_map)
out = dict(val_cases=len(val_cases), val_cases_mapped_to_implant_key=len(imp), their_gate_keys_in_v9=dict(by),
           hidden_train_persons_cases=hidden,
           implant_keys_in_touched_v9=sum(1 for k in e["train_keys"] + e["val_keys"] if str(k).startswith("implant:")),
           train_overlap_persons_with_map=len(tr_map), train_overlap_persons_keying_every_case=len(tr_own),
           persons_hidden_by_map=len(hidden_persons), hidden_person_examples=hidden_persons[:20],
           examples=rows[:12])
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "examples"}, indent=1))
print("examples", json.dumps(rows[:5]))
