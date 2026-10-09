"""Independent check of the unseen arc set, written without eval_gate / checkpoint_lineage / arc_unseen_subjects.

1. every s#### token in the train and val inputs of each scored checkpoint and of its ancestor, read from the
   args.yaml -> data.yaml -> list files / image directories (symlink targets included), intersected with the 40
   chosen subjects (expect none) and with the 17 leaked ones (positive control: expect them);
2. identity from the CT fingerprints: no other TotalSegmentator id carries a chosen subject's CT;
3. the render parameters of the old and new sets are the same;
4. per subject, which truth boxes the lat-0 / lat-90 frames carry;
5. contact sheets of lat-0 and lat -90 frames, truth boxes drawn, old and new.
"""
import glob
import json
import os
import re
from collections import Counter

import numpy as np
from PIL import Image, ImageDraw

H = os.path.expanduser("~")
DATA = "/rs/rs_grp_oschome/go2432/data"
OUT = f"{DATA}/or_ready/eval_gate/arc_unseen/indep_check"
os.makedirs(OUT, exist_ok=True)
NEW = f"{DATA}/devcorpus_arc/anglesweep_unseen"
OLD = f"{DATA}/devcorpus_arc/anglesweep"
chosen = [l.strip() for l in open(f"{DATA}/or_ready/eval_gate/arc_unseen/subjects.txt") if l.strip()]
LEAKED = ["s0585", "s0970", "s1045", "s1062", "s1159", "s1384", "s1535", "s1579", "s1700", "s1836", "s1842", "s1872",
          "s1880", "s1883", "s1902", "s2033", "s2053"]
TOK = re.compile(r"s\d{4}")
rep = {"chosen": chosen, "leaked": LEAKED}


def yaml_min(p):
    """The few keys a YOLO data.yaml carries; no yaml dependency."""
    d, key = {}, None
    for line in open(p):
        if not line.strip() or line.strip().startswith("#"):
            continue
        m = re.match(r"^(\w+):\s*(.*)$", line.rstrip())
        if m:
            key, v = m.group(1), m.group(2).strip()
            d[key] = v if v else []
        elif line.strip().startswith("- ") and key:
            d[key].append(line.strip()[2:].strip())
    return d


def entries(spec, base):
    """Every image path a train/val spec names: list file lines, or a directory's files (+ symlink targets)."""
    specs = spec if isinstance(spec, list) else [spec]
    out = []
    for s in specs:
        p = s if os.path.isabs(s) else os.path.join(base, s)
        if os.path.isfile(p) and p.endswith(".txt"):
            out += [l.strip() for l in open(p) if l.strip()]
        elif os.path.isdir(p):
            for f in os.listdir(p):
                fp = os.path.join(p, f)
                out.append(fp)
                if os.path.islink(fp):
                    out.append(os.readlink(fp))
        else:
            out.append(f"MISSING:{p}")
    return out


def args_of(run):
    d = {}
    for line in open(os.path.join(run, "args.yaml")):
        m = re.match(r"^(\w+):\s*(.*)$", line.rstrip())
        if m:
            d[m.group(1)] = m.group(2).strip()
    return d


RUNS = f"{H}/spine-detector/runs"
scored = {"pooled": f"{RUNS}/devcorpus/dc_P_pooled", "lodoA": f"{RUNS}/devcorpus/dc_A_held_surgio_b51_dr",
          "lodoB": f"{RUNS}/devcorpus/dc_B_held_surgio_b51_dr_s1", "real_lodo": f"{RUNS}/realxray/rx_lodo_carmlspine_1024"}
chains = {}
for arm, run in scored.items():
    chain, r = [], run
    while True:
        a = args_of(r)
        chain.append(dict(run=r, model=a.get("model"), data=a.get("data")))
        m = a.get("model", "")
        if m.endswith("weights/best.pt") or m.endswith("weights/last.pt"):
            r = os.path.dirname(os.path.dirname(m))
            continue
        break
    chains[arm] = chain
rep["chains"] = chains
tokens = {}
for arm, chain in chains.items():
    for link in chain:
        dy = yaml_min(link["data"])
        base = dy.get("path") or os.path.dirname(link["data"])
        for split in ("train", "val", "test"):
            if split not in dy:
                continue
            ent = entries(dy[split], base)
            toks = set()
            for e in ent:
                toks |= set(TOK.findall(os.path.basename(e)))
            dirs = Counter(os.path.dirname(e).split("/images/")[0].split("/")[-1] for e in ent)
            tokens[f"{arm} :: {os.path.basename(link['run'])} :: {split}"] = dict(
                n_entries=len(ent), n_ts_subjects=len(toks), chosen_hits=sorted(toks & set(chosen)),
                leaked_hits=sorted(toks & set(LEAKED)), missing=[e for e in ent if e.startswith("MISSING")][:5],
                sources=dict(dirs.most_common(8)), model=link["model"])
rep["tokens"] = tokens
for k, v in tokens.items():
    print(f"{k:70s} entries {v['n_entries']:6d} ts {v['n_ts_subjects']:4d} chosen {v['chosen_hits']} "
          f"leaked {len(v['leaked_hits'])} missing {len(v['missing'])}", flush=True)

# 2. identity
fp = json.load(open(f"{H}/ts_dupscan_out/ct_fingerprints.json"))
by_md5 = {}
for r in fp:
    by_md5.setdefault(r["md5"], []).append(f"{r['rel']}:{r['sid']}")
by_id = {(r["rel"], r["sid"]): r for r in fp}
ident = {}
for s in chosen:
    r = by_id.get(("v300", s))
    same = by_md5.get(r["md5"], []) if r else []
    other = [x for x in same if x.split(":")[1] != s]
    o201 = by_id.get(("v201", s))
    ident[s] = dict(v300=bool(r), same_md5=same, other_ids=other,
                    v201_same_ct=(None if o201 is None else o201["md5"] == r["md5"]))
rep["identity"] = ident
print("identity: other ids", sum(bool(v["other_ids"]) for v in ident.values()), "v201 id reissued",
      sum(v["v201_same_ct"] is False for v in ident.values()), flush=True)

# 3. render parameters
so, sn = json.load(open(f"{OLD}/SET_INFO.json")), json.load(open(f"{NEW}/SET_INFO.json"))
cmp_ = {}
for k in ("pool", "anchor_tag", "anchor_angles", "cards", "lats", "tilts", "roll_deg", "down", "seed", "out_px",
          "convention"):
    cmp_[k] = dict(same=json.dumps(so.get(k), sort_keys=True) == json.dumps(sn.get(k), sort_keys=True),
                   old=so.get(k) if k not in ("lats",) else [min(so["lats"]), max(so["lats"]), len(so["lats"])],
                   new=sn.get(k) if k not in ("lats",) else [min(sn["lats"]), max(sn["lats"]), len(sn["lats"])])
rep["params"] = cmp_
print("params same:", {k: v["same"] for k, v in cmp_.items()}, flush=True)
rep["subjects_old"], rep["subjects_new"] = so["subjects"], sn["subjects"]
rep["targets_new"] = sn.get("targets")
rep["excluded_new"] = sn.get("excluded")

# 4. truth boxes per subject
boxes = {}
for tag, root, subs in (("old", OLD, so["subjects"]), ("new", NEW, sn["subjects"])):
    for s in subs:
        for lat in (0, -50, 50, -90, 90):
            m = json.load(open(f"{root}/elekta_xvi/meta/{s}_lat{lat:+04d}_tilt+00.json"))
            t = [b["name"].replace("vertebrae_", "") for b in m["boxes"] if b["inside"] >= 0.25]
            boxes.setdefault(tag, {}).setdefault(s, {})[str(lat)] = dict(
                truth=t, n_body=sum(1 for b in m["boxes"] if b["inside"] >= 0.25 and b["cls"] == 0),
                thickness_cm=m.get("thickness_cm"), trunc_frac=m.get("trunc_frac"), target=m.get("target"))
rep["boxes"] = boxes
for tag in ("old", "new"):
    nb = [boxes[tag][s]["0"]["n_body"] for s in boxes[tag]]
    nb90 = [boxes[tag][s]["-90"]["n_body"] for s in boxes[tag]]
    tr = [boxes[tag][s]["0"]["trunc_frac"] for s in boxes[tag]]
    print(f"{tag}: lat0 bodies per subject median {np.median(nb)} range {min(nb)}-{max(nb)}; lat-90 median "
          f"{np.median(nb90)}; trunc_frac lat0 median {np.median(tr):.3f} max {max(tr):.3f}", flush=True)
    print("  names at lat 0:", dict(Counter(n for s in boxes[tag] for n in boxes[tag][s]["0"]["truth"]).most_common()),
          flush=True)


# 5. contact sheets
def sheet(root, subs, card, lat, path, cols=8, tile=256):
    rows = (len(subs) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * tile, rows * (tile + 14)), (20, 20, 20))
    for i, s in enumerate(subs):
        stem = f"{s}_lat{lat:+04d}_tilt+00"
        im = Image.open(f"{root}/{card}/images/{stem}.jpg").convert("RGB")
        m = json.load(open(f"{root}/{card}/meta/{stem}.json"))
        dr = ImageDraw.Draw(im)
        for b in m["boxes"]:
            if b["inside"] >= 0.25:
                dr.rectangle(b["box"], outline=(255, 170, 40) if b["cls"] == 1 else (90, 230, 90), width=4)
        W, Hh = im.size
        sc = tile / max(W, Hh)
        im = im.resize((int(W * sc), int(Hh * sc)))
        x, y = (i % cols) * tile, (i // cols) * (tile + 14)
        canvas.paste(im, (x, y + 14))
        ImageDraw.Draw(canvas).text((x + 3, y + 1), f"{s} {m.get('thickness_cm', 0):.0f}cm", fill=(255, 255, 0))
    canvas.save(path)
    print("sheet", path, flush=True)


for tag, root, subs in (("new", NEW, sn["subjects"]), ("old", OLD, so["subjects"])):
    for card, lat in (("elekta_xvi", 0), ("surgio_b51_dr", 0), ("surgio_b51_dr", -90), ("elekta_xvi", -90),
                      ("elekta_xvi", 50), ("surgio_b51_dr", -50)):
        sheet(root, subs, card, lat, f"{OUT}/sheet_{tag}_{card}_lat{lat:+04d}.png")
json.dump(rep, open(f"{OUT}/indep_check.json", "w"), indent=1)
print("wrote", f"{OUT}/indep_check.json")
