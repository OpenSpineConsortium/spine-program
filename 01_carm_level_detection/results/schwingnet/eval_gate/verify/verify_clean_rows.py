"""VERIFY item 2: three rows EVAL_LEAKS.md calls CLEAN, re-checked without eval_gate / patient_keys / touched.json.

Each checkpoint's train and val lists are read from the run's own args.yaml -> data.yaml (copied from the grid), and
from the Ultralytics label cache written at launch where one survives; each evaluation set from the directory the
number was scored on. Keys use the contract's rules (docs/DATA_ACCOUNTING.md s4) written out here:
  C-ArmLSpine  ^(case\\d+)_          COBRA  ^([A-Z]\\d{3})_          DeepFluoro  specimen id (\\d\\d-\\d{4})
  TotalSegmentator  s\\d{4} as the leading token of a render name.
A render's pose donor (the DeepFluoro / COBRA / C-ArmLSpine frame whose pose it reuses) is reported separately; the
rule scores patients, not poses.
"""
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

G = Path(__file__).resolve().parent / "grid"
R_CARM = re.compile(r"^(case\d+)_")
R_COBRA = re.compile(r"^([A-Z]\d{3})_\d{4}$")
R_DF = re.compile(r"(1[78]-\d{4})")
R_TS = re.compile(r"^(s\d{4})_")
R_DONOR = re.compile(r"^s\d{4}_\d+_(.+?)_(?:cios_fusion|surgio_b51_dr|elekta_xvi)_\d+$")


def key_of(path):
    """(patient key, pose donor or None) for one list line / cached image path."""
    stem = path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    if "/realxray/carmlspine" in path or "/carmlspine/" in path:
        m = R_CARM.match(stem)
        return (f"carmlspine:{m.group(1)}" if m else f"UNKEYED:{stem}"), None
    if "/realxray/cobra_elekta" in path:
        m = R_COBRA.match(stem)
        return (f"cobra:{m.group(1)}" if m else f"UNKEYED:{stem}"), None
    if "/realxray/deepfluoro" in path:
        m = R_DF.search(stem)
        return (f"deepfluoro:{m.group(1)}" if m else f"UNKEYED:{stem}"), None
    m = R_TS.match(stem)
    if m:
        d = R_DONOR.match(stem)
        return f"ts:{m.group(1)}", (d.group(1) if d else None)
    return f"UNKEYED:{stem}", None


def keys_of(lines):
    k, donors, unk = set(), Counter(), []
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        a, d = key_of(ln)
        if a.startswith("UNKEYED"):
            unk.append(a)
        else:
            k.add(a)
        if d:
            donors[d] += 1
    return k, donors, unk


def cache(p):
    return [l["im_file"] for l in np.load(p, allow_pickle=True).item()["labels"]]


def ls(name, root):
    return [f"{root}/{x}" for x in open(G / "dirs" / name).read().split() if x.endswith((".png", ".jpg"))]


def lsl(name, root):
    out = []
    for ln in open(G / "dirs" / name):
        f = ln.split()
        if len(f) >= 9 and f[-1].endswith((".png", ".jpg")):
            out.append(f"{root}/{f[-1]}")
    return out


RX = "/rs/rs_grp_oschome/go2432/data/realxray"
split_of = lambda c: (lambda h: "train" if h <= 6 else ("val" if h == 7 else "test"))(int(hashlib.md5(c.encode()).hexdigest(), 16) % 10)

report = {}

# ---- evaluation sets
carm_test_today = keys_of(lsl("carm_test.lsl", f"{RX}/carmlspine/images/test"))[0]
carm_test_0921 = {k for k in keys_of(p for p in cache(G / "dirs/carm_test_0921.cache") if "/carmlspine/" in p)[0]}
carm_test = carm_test_today | carm_test_0921
report["eval_carm_test"] = dict(n_today=len(carm_test_today), n_in_0921_cache=len(carm_test_0921),
                                same=carm_test_today == carm_test_0921, keys=sorted(carm_test))
sweep = keys_of(lsl("carm_sweep_test.lsl", f"{RX}/carmlspine_sweep/images/test"))[0]
report["eval_case134_spin"] = sorted(sweep)

# md5 rule, checked on every C-ArmLSpine case seen anywhere
allcases = set()
for n in ("carm_train.lsl", "carm_val.lsl", "carm_test.lsl"):
    allcases |= {k.split(":")[1] for k in keys_of(lsl(n, f"{RX}/carmlspine/images/x"))[0]}
viol = []
for n, sp in (("carm_train.lsl", "train"), ("carm_val.lsl", "val"), ("carm_test.lsl", "test")):
    for k in keys_of(lsl(n, f"{RX}/carmlspine/images/x"))[0]:
        c = k.split(":")[1]
        if split_of(c) != sp:
            viol.append((c, sp, split_of(c)))
report["md5_split_rule"] = dict(n_cases=len(allcases), violations=viol,
                                test_cases_by_rule=sorted(c for c in allcases if split_of(c) == "test"),
                                case134=split_of("case134"))

# ---- the lists each checkpoint trained and was selected on
anchor_tr = keys_of(cache(G / "caches/anchor_train.cache"))
anchor_va = keys_of(cache(G / "caches/anchor_val.cache"))
chains = {}
# rx_lodo_carmlspine_1024 (data.yaml: train cobra train+val, deepfluoro train+val; val cobra test, deepfluoro test)
chains["rx_lodo_carmlspine_1024"] = {
    "own train (cobra_elekta/labels/train.cache, launch)": keys_of(cache(G / "caches/cobra_train.cache")),
    "own val (cobra_elekta/labels/test.cache, launch)": keys_of(cache(G / "caches/cobra_test.cache")),
    "ancestor anchor_none_v2_17-1882 train (launch cache)": anchor_tr,
    "ancestor anchor_none_v2_17-1882 val (launch cache)": anchor_va}
# rx_pooled_1024 (data.yaml: train carmlspine/cobra/deepfluoro train; val carmlspine/cobra/deepfluoro val).
# Its launch caches were overwritten by later scans; the directories are read as they stand, and the C-ArmLSpine
# train and val dirs are also bounded by the md5 rule over every case the export holds.
carm_tr_bound = {f"carmlspine:{c}" for c in allcases if split_of(c) == "train"}
carm_va_bound = {f"carmlspine:{c}" for c in allcases if split_of(c) == "val"}
chains["rx_pooled_1024"] = {
    "own train: carmlspine/images/train today": keys_of(lsl("carm_train.lsl", f"{RX}/carmlspine/images/train")),
    "own train: carmlspine/labels/train.cache (2026-09-22 05:58, a later scan)":
        keys_of([p for p in cache(G / "dirs/carm_train_0922.cache") if "/carmlspine/" in p]),
    "own train: md5 rule bound (train)": (carm_tr_bound, Counter(), []),
    "own train: cobra_elekta + deepfluoro train today": keys_of(ls("cobra_elekta_train.ls", f"{RX}/cobra_elekta/images/train")
                                                                + ls("deepfluoro_train.ls", f"{RX}/deepfluoro/images/train")),
    "own val: carmlspine/images/val today": keys_of(lsl("carm_val.lsl", f"{RX}/carmlspine/images/val")),
    "own val: md5 rule bound (val)": (carm_va_bound, Counter(), []),
    "own val: cobra_elekta + deepfluoro val today": keys_of(ls("cobra_elekta_val.ls", f"{RX}/cobra_elekta/images/val")
                                                            + ls("deepfluoro_val.ls", f"{RX}/deepfluoro/images/val")),
    "ancestor anchor_none_v2_17-1882 train (launch cache)": anchor_tr,
    "ancestor anchor_none_v2_17-1882 val (launch cache)": anchor_va}
for arm, d in (("dc_P_pooled", "P_pooled"), ("dc_A_held_surgio_b51_dr", "A_held"), ("dc_B_held_surgio_b51_dr_s1", "B_held")):
    chains[arm] = {f"own train ({d}/train.txt)": keys_of(open(G / f"lists/{d}/train.txt").read().splitlines()),
                   f"own val ({d}/val.txt)": keys_of(open(G / f"lists/{d}/val.txt").read().splitlines())}


def check(row, pairs):
    out = []
    for ck, ev_name, ev in pairs:
        per = []
        for src, (k, donors, unk) in chains[ck].items():
            hit = sorted(ev & k)
            evp = {e.split(":")[1] for e in ev}
            dh = sorted(d for d in donors if d.split("-")[0] in evp or d[:7] in evp)
            per.append(dict(source=src, n_keys=len(k), n_unkeyed=len(unk), hits=hit,
                            corpora=dict(Counter(x.split(":")[0] for x in k)),
                            pose_donor_frames_of_eval_patients=sum(donors[d] for d in dh)))
        out.append(dict(checkpoint=ck, eval_set=ev_name, n_eval=len(ev), overlap=sorted({h for p in per for h in p["hits"]}),
                        sources=per))
    report[row] = out
    return out


check("NUMBERS:L105 (pooled_vs_lodo_carm)", [("rx_pooled_1024", "carm_test", carm_test),
                                             ("rx_lodo_carmlspine_1024", "carm_test", carm_test)])
check("FIG3:005 (lcurve: surgio arm 3, dc_B_held_surgio_b51_dr_s1 on carm_test)",
      [("dc_B_held_surgio_b51_dr_s1", "carm_test", carm_test)])
check("FIGREC:figS4/01 (case134 spin, four detectors)",
      [(c, "case134_spin", sweep) for c in ("dc_P_pooled", "dc_A_held_surgio_b51_dr", "dc_B_held_surgio_b51_dr_s1",
                                            "rx_lodo_carmlspine_1024")])
json.dump(report, open(Path(__file__).resolve().parent / "verify_clean_rows.json", "w"), indent=1, default=list)

print("carm_test:", report["eval_carm_test"]["n_today"], "today,", report["eval_carm_test"]["n_in_0921_cache"],
      "in the 09-21 cache, same:", report["eval_carm_test"]["same"])
print("case134 spin keys:", report["eval_case134_spin"])
print("md5 rule:", len(report["md5_split_rule"]["violations"]), "violations over", report["md5_split_rule"]["n_cases"],
      "cases; case134 ->", report["md5_split_rule"]["case134"])
for row in [k for k in report if k.startswith(("NUMBERS", "FIG3", "FIGREC"))]:
    print("==", row)
    for pr in report[row]:
        print(f"   {pr['checkpoint']} on {pr['eval_set']} ({pr['n_eval']} patients): overlap {pr['overlap']}")
        for s in pr["sources"]:
            print(f"      {len(s['hits']):3d} hits  {s['n_keys']:4d} keys {s['corpora']}  unkeyed {s['n_unkeyed']}  "
                  f"donor frames {s['pose_donor_frames_of_eval_patients']}  | {s['source']}")
