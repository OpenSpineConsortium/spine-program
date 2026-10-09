"""VERIFY item 3, written without importing eval_gate / patient_keys / checkpoint_lineage.

(a) The 40 new arc subjects against every train AND val list of every chain the curve scored, read from the files the
    runs recorded (list .txt files, Ultralytics label caches written at launch, and today's directory listings).
    The old 17 are run through the same code as a positive control.
(b) Identity: any other TotalSegmentator id whose CT is byte-identical (md5) or the same grid (shape + affine) as a
    chosen subject's, looked up in either release, and whether THAT id is in a list.
(c) Two curve cells re-derived from matches.json with separate code, bootstrap included.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

G = Path(__file__).resolve().parent / "grid"
REPO = Path(r"spinesurg-ct-nnunet:")
out = {}

new = json.load(open(REPO / "SchwingNet/results/arc/recall_vs_angle_unseen/subjects.json"))["subjects"]
new_grid = json.load(open(G / "arc_new/subjects.json"))["subjects"]
seti_new = json.load(open(G / "arc_new/SET_INFO.json"))["subjects"]
old = json.load(open(G / "arc_old/SET_INFO.json"))["subjects"]
assert sorted(new) == sorted(new_grid) == sorted(seti_new), "repo subjects.json / grid subjects.json / SET_INFO differ"
out["n_new"], out["n_old"] = len(new), len(old)
out["new_and_old_overlap"] = sorted(set(new) & set(old))

TOK = re.compile(r"(?<![0-9A-Za-z])s(\d{4})(?!\d)")


def tokens_in_lines(lines):
    """Every TS subject token (s####) in a list of paths, counted by the path's basename only (a directory named
    s#### would otherwise be counted too; none of these roots has one, and that is checked below)."""
    c = Counter()
    for ln in lines:
        b = ln.strip().rsplit("/", 1)[-1]
        for m in TOK.finditer(b):
            c["s" + m.group(1)] += 1
    return c


def cache_files(p):
    d = np.load(p, allow_pickle=True).item()
    return [l["im_file"] for l in d["labels"]]


SOURCES = {
    # chain -> [(label, split, lines)]
    "pooled (dc_P_pooled; root yolo11m COCO)": [
        ("P_pooled/train.txt", "train", open(G / "lists/P_pooled/train.txt").read().splitlines()),
        ("P_pooled/val.txt", "val", open(G / "lists/P_pooled/val.txt").read().splitlines())],
    "lodoA (dc_A_held_surgio_b51_dr; root yolo11m COCO)": [
        ("A_held_surgio_b51_dr/train.txt", "train", open(G / "lists/A_held/train.txt").read().splitlines()),
        ("A_held_surgio_b51_dr/val.txt", "val", open(G / "lists/A_held/val.txt").read().splitlines())],
    "lodoB (dc_B_held_surgio_b51_dr_s1; root yolo11m COCO)": [
        ("B_held_surgio_b51_dr_s1/train.txt", "train", open(G / "lists/B_held/train.txt").read().splitlines()),
        ("B_held_surgio_b51_dr_s1/val.txt", "val", open(G / "lists/B_held/val.txt").read().splitlines())],
    "real_lodo (rx_lodo_carmlspine_1024 -> anchor_none_v2_17-1882 -> yolo11m COCO)": [
        ("rx_lodo train: cobra_elekta/labels/train.cache (written at launch, 4 dirs)", "train",
         cache_files(G / "caches/cobra_train.cache")),
        ("rx_lodo val: cobra_elekta/labels/test.cache (written at launch, 2 dirs)", "val",
         cache_files(G / "caches/cobra_test.cache")),
        ("rx_lodo train dirs today: cobra_elekta train+val, deepfluoro train+val", "train",
         sum((open(G / f"dirs/{n}.ls").read().splitlines() for n in
              ("cobra_elekta_train", "cobra_elekta_val", "deepfluoro_train", "deepfluoro_val")), [])),
        ("rx_lodo val dirs today: cobra_elekta test, deepfluoro test", "val",
         sum((open(G / f"dirs/{n}.ls").read().splitlines() for n in ("cobra_elekta_test", "deepfluoro_test")), [])),
        ("ancestor anchor_none_v2_17-1882 labels/train.cache (written at launch)", "train",
         cache_files(G / "caches/anchor_train.cache")),
        ("ancestor anchor_none_v2_17-1882 labels/val.cache (written at launch)", "val",
         cache_files(G / "caches/anchor_val.cache")),
        ("ancestor anchor_none_v2_17-1882 images/train today", "train", open(G / "dirs/anchor_train.ls").read().splitlines()),
        ("ancestor anchor_none_v2_17-1882 images/val today", "val", open(G / "dirs/anchor_val.ls").read().splitlines())],
}

# (b) identity: other ids with the same CT
fp = json.load(open(G / "ct_fingerprints.json"))
by_md5, by_grid = defaultdict(set), defaultdict(set)
for r in fp:
    by_md5[r["md5"]].add((r["rel"], r["sid"]))
    by_grid[(tuple(r["shape"]), tuple(round(x, 3) for x in r["affine"]))].add((r["rel"], r["sid"]))
rec = {(r["rel"], r["sid"]): r for r in fp}


def aliases(sid):
    """Other TS ids (either release) that hold the same CT as v300 <sid>, by md5 or by identical grid."""
    r = rec.get(("v300", sid))
    if r is None:
        return None
    al = by_md5[r["md5"]] | by_grid[(tuple(r["shape"]), tuple(round(x, 3) for x in r["affine"]))]
    return sorted({s for rel, s in al if s != sid})


alias_map = {s: aliases(s) for s in new}
out["identity"] = dict(no_fingerprint=[s for s, a in alias_map.items() if a is None],
                       with_other_ids={s: a for s, a in alias_map.items() if a})
check_ids_new = set(new) | {a for al in alias_map.values() if al for a in al}

res = {}
for chain, srcs in SOURCES.items():
    rows = []
    for label, split, lines in srcs:
        c = tokens_in_lines(lines)
        dirs_with_token = sum(1 for ln in lines if TOK.search(ln.strip().rsplit("/", 1)[0].rsplit("/", 1)[-1] if "/" in ln else ""))
        hit_new = sorted(s for s in new if s in c)
        hit_alias = sorted(s for s in check_ids_new - set(new) if s in c)
        hit_old = sorted(s for s in old if s in c)
        # a raw substring search as well (catches a spelling the token rule would miss, e.g. TS_s0586 or totalseg_s0586)
        blob = "\n".join(lines)
        raw_new = sorted(s for s in new if s in blob)
        rows.append(dict(source=label, split=split, n_lines=len(lines), n_ts_subjects=len(c), new_hits=hit_new,
                         new_raw_substring_hits=raw_new, alias_hits=hit_alias, old17_hits=hit_old,
                         n_old17_hits=len(hit_old), parent_dir_named_like_subject=dirs_with_token))
    res[chain] = rows
out["lists"] = res

# (c) curve cells from the raw dump
m = json.load(open(G / "arc_new/matches.json"))
cur = json.load(open(G / "arc_new/recall_vs_angle.json"))
out["matches_eval_gate"] = dict(held_out=m["eval_gate"]["held_out"], overlap=m["eval_gate"]["overlap"],
                                unresolved=m["eval_gate"]["unresolved"],
                                checkpoints=[c["checkpoint"] for c in m["eval_gate"]["checks"]])
out["matches_weights_equal_subjects_json"] = m["weights"] == json.load(open(G / "arc_new/subjects.json"))["weights"]
recs = m["records"]
subj_in_records = sorted({r["subject"] for r in recs})
out["record_subjects_equal_set"] = subj_in_records == sorted(new)


def cell(det, card, conf, cls, tilt, lat, boot=2000, seed=0):
    subjects = subj_in_records
    idx = {s: i for i, s in enumerate(subjects)}
    n = np.zeros(len(subjects)); k = np.zeros(len(subjects))
    for r in recs:
        if r["det"] == det and r["card"] == card and r["cls"] == cls and r["tilt"] == tilt and r["lat"] == lat:
            n[idx[r["subject"]]] += 1
            k[idx[r["subject"]]] += int(r["conf"] is not None and r["conf"] >= conf)
    rng = np.random.default_rng(seed)
    draws = rng.integers(0, len(subjects), size=(boot, len(subjects)))
    W = np.stack([np.bincount(d, minlength=len(subjects)) for d in draws])
    b = (W @ k) / (W @ n)
    return dict(n=int(n.sum()), k=int(k.sum()), recall=float(k.sum() / n.sum()),
                lo=float(np.nanpercentile(b, 2.5)), hi=float(np.nanpercentile(b, 97.5)))


cells = []
for det, card, lat in (("pooled", "elekta_xvi", -90.0), ("real_lodo", "surgio_b51_dr", 0.0), ("lodoA", "elekta_xvi", 0.0)):
    mine = cell(det, card, 0.25, 0, 0.0, lat)
    theirs = next(x for x in cur["curves"][det][card]["0.25"]["body"]["0.0"] if x["lat"] == lat)
    cells.append(dict(det=det, card=card, conf=0.25, cls="body", tilt=0.0, lat=lat, mine=mine, published=theirs,
                      match=(mine["n"] == theirs["n"] and abs(mine["recall"] - theirs["recall"]) < 1e-12
                             and abs(mine["lo"] - theirs["lo"]) < 1e-12 and abs(mine["hi"] - theirs["hi"]) < 1e-12)))
out["cells"] = cells
json.dump(out, open(Path(__file__).resolve().parent / "verify_arc_lists.json", "w"), indent=1)

print("new/old overlap:", out["new_and_old_overlap"])
print("identity:", out["identity"])
for chain, rows in res.items():
    print("==", chain)
    for r in rows:
        print(f"   {r['split']:5s} {r['n_lines']:6d} lines {r['n_ts_subjects']:4d} TS subj | new {r['new_hits']} raw {r['new_raw_substring_hits']} alias {r['alias_hits']} | old17 {r['n_old17_hits']} | {r['source']}")
print("matches gate:", out["matches_eval_gate"], "weights==subjects.json:", out["matches_weights_equal_subjects_json"],
      "record subjects == 40:", out["record_subjects_equal_set"])
for c in cells:
    print(c["det"], c["card"], c["lat"], "mine", c["mine"], "published", c["published"], "MATCH" if c["match"] else "DIFFER")
