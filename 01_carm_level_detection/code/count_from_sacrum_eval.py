#!/usr/bin/env python
# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/count_from_sacrum_eval.py [tracked at 097933a]
"""Counting accuracy from the sacrum, on real C-arm frames, from a detector's own boxes and nothing else.

THE PRODUCT is detection + counting from the anchor. A level is an ORDINAL from the sacrum, never a name from
morphology: a name follows by convention (ordinal 1 = L5 in a five-lumbar spine) and where it does not (L6, T13)
the ordinal is still the answer. No level classifier is used anywhere here.

DEFINITION (one frame)
  detected side  the detected sacrum (highest-confidence sacrum box at conf >= --conf) is ordinal 0. The detected
                 vertebral bodies are ordered along the spine axis (the principal direction of the box centres,
                 sacrum included) moving AWAY from the sacrum; the k-th body from the sacrum has ordinal k. Boxes
                 on the sacrum's caudal side are not counted (they are not between the sacrum and anything). The
                 cranial side is the side holding more boxes; a tie goes to the side whose nearest box is nearer
                 the sacrum, because the first vertebra abuts the sacrum while a spurious box on the pelvis lies
                 beyond it (one DeepFluoro frame turned on this).
  truth side     the frame's labelled bodies ordered the same way from the TRUTH sacrum; ordinal = rank among truth
                 bodies. This is name-free: an L6 or T13 spine needs no special case.
  matching       detections to truth one-to-one, greedy in descending confidence, each detection taking the
                 unmatched truth box of highest IoU, a hit at IoU >= 0.5 (tools/realxray_eval.sweep_matches).
  scoring        a matched truth body is COUNTED CORRECTLY when its detection's ordinal equals its truth ordinal;
                 WITHIN ONE when they differ by one. A missed body between the sacrum and a target shifts every
                 ordinal above it: that is the counting error measured here. A truth body with no matched
                 detection is MISSED. Counting is DEFINED on a frame when truth has a sacrum and a sacrum was
                 detected; when the sacrum is not in the frame counting from one frame is undefined (that is what
                 the level-map sweep is for, docs/SWEEP_PROTOCOL.md).
  orientation    ordering away from the sacrum needs no orientation flag: C-ArmLSpine AP and lateral frames of
                 prone/supine patients and DeepFluoro frames stored upside down are handled alike.

TRUTH comes from the YOLO label files (--labels), denormalised with the image size from the frame's meta, and is
cross-checked against the truth rows the dump carries (IoU >= 0.9 per box, same count per class). With
--convention outline (C-ArmLSpine: truth `box` is the vertebral BODY, every other device's truth is a whole-
vertebra OUTLINE) each label box is swapped for the meta's `outline_box` before matching, the convention
SchwingNet/tools/contribution_matrix.py scores C-ArmLSpine under. The truth level names, where labelled, are used
only as an OUTSIDE CHECK of the geometric ordering (L5 -> 1, L4 -> 2, ...), never for scoring.

INTERVALS: 2,000-resample bootstrap clustered by CASE (C-ArmLSpine case, DeepFluoro specimen, COBRA patient),
percentile and BCa (jackknife acceleration over cases); one cluster -> no interval, said so.

    python tools/count_from_sacrum_eval.py --dump <realxray_eval --dump-raw json> [more dumps] --labels <dir> \
        --conf 0.25 --out out.json [--convention outline] [--meta <dir>] [--arm NAME --set NAME]
    python tools/count_from_sacrum_eval.py --self-test
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np

N_BOOT = 2000
SEED = 0
IOU_MATCH = 0.5
IOU_TRUTH_CHECK = 0.9
# the conventional names of the ordinals in a five-lumbar spine, used ONLY to check the geometric truth ordering
CONVENTIONAL = {"L5": 1, "L4": 2, "L3": 3, "L2": 4, "L1": 5, "T12": 6, "T11": 7, "T10": 8, "T9": 9}


# ----------------------------------------------------------------------------------------------------- geometry
def iou(a, b):
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0])); iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy; u = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / u if u > 0 else 0.0


def centre(b):
    return np.array([(b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0])


def order_from_anchor(anchor, boxes):
    """Ordinals 1..N for `boxes` by the rank of each centre's projection on the spine axis, moving away from the
    anchor box. The axis is the principal direction of the centres (anchor included); its sign is chosen so that
    the side holding more boxes (ties: the side with the larger total distance) is the cranial side. A box on the
    caudal side gets None. Returns (ordinals, projections)."""
    if not boxes:
        return [], []
    sc = centre(anchor); cs = np.array([centre(b) for b in boxes], float)
    pts = np.vstack([sc[None, :], cs])
    if len(pts) >= 3:
        _, _, vt = np.linalg.svd(pts - pts.mean(0)); axis = vt[0]
    else:
        d = cs[0] - sc; axis = d / max(float(np.linalg.norm(d)), 1e-6)
    proj = (cs - sc) @ axis
    pos, neg = int((proj > 0).sum()), int((proj < 0).sum())
    # the cranial side holds more boxes; a tie goes to the side whose nearest box is nearer the anchor, because the
    # column is contiguous from the sacrum (a far box on the other side is the spurious one)
    if neg > pos or (neg == pos and neg > 0 and float(-proj[proj < 0].max()) < float(proj[proj > 0].min())):
        proj = -proj
    order = sorted([i for i in range(len(boxes)) if proj[i] > 0], key=lambda i: proj[i])
    ords = [None] * len(boxes)
    for k, i in enumerate(order):
        ords[i] = k + 1
    return ords, [float(p) for p in proj]


def match_pairs(preds, truths):
    """Greedy one-to-one, descending confidence, each prediction takes the unmatched truth of highest IoU; a hit
    at IoU >= 0.5. preds: [(box, conf)], truths: [box]. Returns {pred_idx: (truth_idx, iou)} for the hits."""
    order = sorted(range(len(preds)), key=lambda i: -preds[i][1])
    used = set(); pairs = {}
    for i in order:
        best, bj = 0.0, -1
        for j, t in enumerate(truths):
            if j in used:
                continue
            o = iou(preds[i][0], t)
            if o > best:
                best, bj = o, j
        if best >= IOU_MATCH:
            used.add(bj); pairs[i] = (bj, best)
    return pairs


# -------------------------------------------------------------------------------------------------------- truth
def image_size(meta, image_path):
    for k in ("size", "image_size"):
        v = meta.get(k) if meta else None
        if isinstance(v, (int, float)):
            return float(v), float(v)
        if isinstance(v, (list, tuple)) and len(v) == 2:
            return float(v[0]), float(v[1])
        if isinstance(v, dict) and "w" in v and "h" in v:
            return float(v["w"]), float(v["h"])
    if image_path and os.path.exists(image_path):
        from PIL import Image
        w, h = Image.open(image_path).size
        return float(w), float(h)
    raise SystemExit(f"no image size for {image_path}: meta has no size/image_size and the image is not on disk")


def read_labels(path, W, H):
    out = []
    for line in open(path).read().strip().splitlines():
        p = line.split()
        if len(p) < 5:
            continue
        c = int(float(p[0])); cx, cy, w, h = (float(x) for x in p[1:5])
        out.append((c, [(cx - w / 2) * W, (cy - h / 2) * H, (cx + w / 2) * W, (cy + h / 2) * H]))
    return out


def find_label(labels_dir, stem, image_path):
    cands = [Path(labels_dir) / f"{stem}.txt"]
    if image_path:
        cands.append(Path(labels_dir) / Path(image_path).parent.name / f"{stem}.txt")
    for c in cands:
        if c.exists():
            return c
    return None


def find_meta(meta_dir, stem, image_path):
    cands = []
    if meta_dir:
        cands.append(Path(meta_dir) / f"{stem}.json")
    if image_path:
        root = Path(image_path).parents[2]              # <dataset>/images/<split>/<stem>.png
        cands += [root / "meta" / f"{stem}.json", root / "meta" / Path(image_path).parent.name / f"{stem}.json"]
    for c in cands:
        if c.exists():
            return json.load(open(c))
    return None


def frame_truth(row, labels_dir, meta_dir, convention):
    """Truth boxes of one frame from its label file: (bodies [(box, level)], sacra [box], check dict)."""
    stem = row["stem"]; image = row.get("image")
    lp = find_label(labels_dir, stem, image)
    if lp is None:
        return None, None, dict(label_file=None)
    meta = find_meta(meta_dir, stem, image)
    if meta is not None and "crop" in meta:
        raise SystemExit(f"{stem}: a crop meta; this tool scores whole frames only")
    W, H = image_size(meta, image)
    lab = read_labels(lp, W, H)
    # cross-check against the truth the dump carries (built from the meta's kept boxes by realxray_eval.load_truth)
    dump_truth = [(int(c), [float(x) for x in b]) for c, b, _ in row.get("truth", [])]
    check = dict(label_file=str(lp), n_label=len(lab), n_dump=len(dump_truth), mismatched=0,
                 count_agrees=(sorted(c for c, _ in lab) == sorted(c for c, _ in dump_truth)))
    for c, b in lab:
        best = max((iou(b, tb) for tc, tb in dump_truth if tc == c), default=0.0)
        if best < IOU_TRUTH_CHECK:
            check["mismatched"] += 1
    # level names and (for the outline convention) the outline boxes, from the meta box of highest IoU
    mboxes = [b for b in (meta or {}).get("boxes", []) if b.get("kept", True)] if meta else []
    bodies = []; sacra = []
    for c, b in lab:
        mb, best = None, 0.0
        for m in mboxes:
            if m["cls"] != c:
                continue
            o = iou(b, m["box"])
            if o > best:
                best, mb = o, m
        if mb is not None and best < IOU_TRUTH_CHECK:
            mb = None
        box = b
        if convention == "outline" and mb is not None and mb.get("outline_box"):
            box = [float(x) for x in mb["outline_box"]]
        lvl = mb.get("level") if mb else None
        if c == 0:
            bodies.append((box, lvl))
        elif c == 1:
            sacra.append(box)
    return bodies, sacra, check


# ------------------------------------------------------------------------------------------------------- scoring
def score_frame(row, bodies, sacra, conf):
    """One frame. Returns the per-frame record (see the docstring of this module for the definitions)."""
    rec = dict(stem=row["stem"], case=row.get("case"), view=row.get("view"), n_truth_sacrum=len(sacra), n_truth_bodies=len(bodies))
    pred = [(int(c), [float(x) for x in b], float(s)) for c, b, s in row["raw"] if float(s) >= conf]
    psac = [q for q in pred if q[0] == 1]; pbod = [q for q in pred if q[0] == 0]
    rec["n_det_sacrum"] = len(psac); rec["n_det_bodies"] = len(pbod)
    if not sacra:
        rec.update(defined=False, why="no truth sacrum in the frame")
        return rec
    tsac = max(sacra, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
    # truth ordinals, name-free, from the truth sacrum
    t_ords, t_proj = order_from_anchor(tsac, [b for b, _ in bodies])
    rec["truth"] = [dict(ordinal=o, level=lv, box=[round(x, 1) for x in b], proj=round(p, 1)) for (b, lv), o, p in zip(bodies, t_ords, t_proj)]
    rec["truth_caudal_bodies"] = sum(1 for o in t_ords if o is None)
    named = [(o, CONVENTIONAL.get(lv)) for o, lv in zip(t_ords, (lv for _, lv in bodies)) if lv in CONVENTIONAL]
    rec["name_check"] = dict(named=len(named), agree=sum(1 for o, c in named if o == c))
    if not psac:
        rec.update(defined=False, why="sacrum not detected")
        return rec
    dsac = max(psac, key=lambda q: q[2])
    rec.update(defined=True, anchor_conf=round(dsac[2], 4), anchor_box=[round(x, 1) for x in dsac[1]],
               anchor_iou=round(iou(dsac[1], tsac), 3))
    rec["anchor_correct"] = rec["anchor_iou"] >= IOU_MATCH
    d_ords, d_proj = order_from_anchor(dsac[1], [q[1] for q in pbod])
    pairs = match_pairs([(q[1], q[2]) for q in pbod], [b for b, _ in bodies])
    rec["det"] = []
    for i, q in enumerate(pbod):
        d = dict(ordinal=d_ords[i], conf=round(q[2], 4), box=[round(x, 1) for x in q[1]], proj=round(d_proj[i], 1))
        if i in pairs:
            j, o = pairs[i]; d.update(truth_ordinal=t_ords[j], truth_level=bodies[j][1], iou=round(o, 3))
        rec["det"].append(d)
    rec["det_caudal_ignored"] = sum(1 for o in d_ords if o is None)
    rec["det_unmatched"] = sum(1 for i in range(len(pbod)) if i not in pairs)
    # per truth body
    per = []
    matched_of = {j: i for i, (j, _) in pairs.items()}
    for j, (b, lv) in enumerate(bodies):
        t = t_ords[j]
        if j not in matched_of:
            per.append("missed"); continue
        dord = d_ords[matched_of[j]]
        if dord is None or t is None:
            per.append("unranked")
        elif dord == t:
            per.append("correct")
        elif abs(dord - t) == 1:
            per.append("one_off")
        else:
            per.append("off_more")
    rec["per_truth"] = per
    rec["n_matched"] = len(pairs); rec["n_correct"] = per.count("correct"); rec["n_one_off"] = per.count("one_off")
    rec["n_off_more"] = per.count("off_more"); rec["n_unranked"] = per.count("unranked"); rec["n_missed"] = per.count("missed")
    rec["all_matched_correct"] = (rec["n_matched"] > 0 and rec["n_correct"] == rec["n_matched"])
    rec["exact"] = (len(bodies) > 0 and rec["n_correct"] == len(bodies))
    return rec


# ----------------------------------------------------------------------------------------------------- bootstrap
def bca_ratio(num, den, rng, n_boot=N_BOOT):
    """Ratio of sums over clusters; percentile and BCa 95 % intervals from `n_boot` cluster resamples."""
    num = np.asarray(num, float); den = np.asarray(den, float); n = len(num)
    if den.sum() <= 0:
        return dict(point=None, n_clusters=n)
    point = float(num.sum() / den.sum())
    out = dict(point=point, n_clusters=n, num=int(num.sum()), den=int(den.sum()))
    if n < 2:
        out.update(percentile=None, bca=None, interval="no interval: one cluster")
        return out
    idx = rng.integers(0, n, size=(n_boot, n))
    bn = num[idx].sum(1); bd = den[idx].sum(1)
    ok = bd > 0
    boot = bn[ok] / bd[ok]
    out["percentile"] = [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))]
    out["resamples_used"] = int(ok.sum())
    from scipy.stats import norm
    lt = float((boot < point).mean()); eq = float((boot == point).mean())
    p0 = lt + 0.5 * eq
    jack = []
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        if den[m].sum() > 0:
            jack.append(num[m].sum() / den[m].sum())
    jack = np.asarray(jack, float)
    if 0.0 < p0 < 1.0 and len(jack) >= 2 and np.std(jack) > 0:
        z0 = float(norm.ppf(p0)); jm = jack.mean()
        a = float(((jm - jack) ** 3).sum() / (6.0 * (((jm - jack) ** 2).sum()) ** 1.5))
        za, zb = norm.ppf(0.025), norm.ppf(0.975)
        a1 = float(norm.cdf(z0 + (z0 + za) / (1 - a * (z0 + za)))); a2 = float(norm.cdf(z0 + (z0 + zb) / (1 - a * (z0 + zb))))
        out["bca"] = [float(np.percentile(boot, 100 * a1)), float(np.percentile(boot, 100 * a2))]
        out["bca_note"] = f"z0={z0:.3f} a={a:.4f} (ties split; p0={p0:.3f})"
    else:
        out["bca"] = None; out["bca_note"] = f"BCa undefined (p0={p0:.3f}, jackknife spread {float(np.std(jack)) if len(jack) else 0:.4f}); percentile only"
    out["interval"] = f"case bootstrap, {n} clusters, {n_boot} resamples, seed {SEED}"
    return out


def pooled(frames, rng_seed=SEED):
    """Pooled numbers with case-cluster intervals. Every ratio is num/den with both summed per case."""
    cases = sorted({f["case"] for f in frames}, key=str)
    S = [f for f in frames if f["n_truth_sacrum"] > 0]                  # counting eligible: truth has a sacrum
    D = [f for f in S if f.get("defined")]                               # counting defined: sacrum detected too
    by = lambda fs, fn: np.array([sum(fn(f) for f in fs if f["case"] == c) for c in cases], float)  # noqa: E731
    R = lambda fs, fnum, fden: bca_ratio(by(fs, fnum), by(fs, fden), np.random.default_rng(rng_seed))  # noqa: E731
    out = dict(frames=len(frames), cases=len(cases), frames_no_truth_sacrum=len(frames) - len(S), frames_with_truth_sacrum=len(S),
               frames_defined=len(D), truth_bodies_all_frames=sum(f["n_truth_bodies"] for f in frames),
               truth_bodies_sacrum_frames=sum(f["n_truth_bodies"] for f in S), truth_bodies_defined=sum(f["n_truth_bodies"] for f in D),
               matched_bodies=sum(f["n_matched"] for f in D))
    out["defined_share"] = R(S, lambda f: int(bool(f.get("defined"))), lambda f: 1)
    out["anchor_correct_share"] = R(D, lambda f: int(bool(f.get("anchor_correct"))), lambda f: 1)
    out["matched_correct"] = R(D, lambda f: f["n_correct"], lambda f: f["n_matched"])
    out["matched_within_one"] = R(D, lambda f: f["n_correct"] + f["n_one_off"], lambda f: f["n_matched"])
    D1 = [f for f in D if f["n_matched"] > 0]; Db = [f for f in D if f["n_truth_bodies"] > 0]
    out["frames_with_a_match"] = len(D1); out["frames_defined_with_bodies"] = len(Db)
    out["frame_all_matched_correct"] = R(D1, lambda f: int(f["all_matched_correct"]), lambda f: 1)
    out["frame_exact"] = R(Db, lambda f: int(f["exact"]), lambda f: 1)
    out["truth_correct_defined"] = R(D, lambda f: f["n_correct"], lambda f: f["n_truth_bodies"])
    out["truth_one_off_defined"] = R(D, lambda f: f["n_one_off"], lambda f: f["n_truth_bodies"])
    out["truth_off_more_defined"] = R(D, lambda f: f["n_off_more"] + f["n_unranked"], lambda f: f["n_truth_bodies"])
    out["truth_missed_defined"] = R(D, lambda f: f["n_missed"], lambda f: f["n_truth_bodies"])
    out["truth_recall_defined"] = R(D, lambda f: f["n_matched"], lambda f: f["n_truth_bodies"])
    # the strictest single denominator: every truth body in every frame that contained the sacrum; a body in a frame
    # whose sacrum went undetected is not counted at all
    out["truth_correct_all_sacrum_frames"] = R(S, lambda f: f.get("n_correct", 0), lambda f: f["n_truth_bodies"])
    out["truth_within_one_all_sacrum_frames"] = R(S, lambda f: f.get("n_correct", 0) + f.get("n_one_off", 0), lambda f: f["n_truth_bodies"])
    # by truth ordinal (no interval: a breakdown, not a headline)
    byo = {}
    for f in D:
        for t, p in zip(f["truth"], f["per_truth"]):
            k = t["ordinal"]
            o = byo.setdefault(str(k), dict(n=0, correct=0, one_off=0, off_more=0, unranked=0, missed=0))
            o["n"] += 1; o[p] += 1
    for o in byo.values():
        o["correct_share"] = o["correct"] / o["n"] if o["n"] else None
    out["by_truth_ordinal"] = dict(sorted(byo.items(), key=lambda kv: (kv[0] == "None", int(kv[0]) if kv[0] != "None" else 0)))
    # by view / angle bin, where the frame carries it
    byv = {}
    for f in D:
        v = f.get("view_bin") or "all"
        o = byv.setdefault(v, dict(frames=0, matched=0, correct=0, truth=0, missed=0))
        o["frames"] += 1; o["matched"] += f["n_matched"]; o["correct"] += f["n_correct"]; o["truth"] += f["n_truth_bodies"]; o["missed"] += f["n_missed"]
    for o in byv.values():
        o["matched_correct"] = o["correct"] / o["matched"] if o["matched"] else None
        o["truth_correct"] = o["correct"] / o["truth"] if o["truth"] else None
    out["by_view"] = dict(sorted(byv.items()))
    # outside check of the truth ordering against the conventional names, where labelled
    nc = sum(f["name_check"]["named"] for f in S if "name_check" in f); na = sum(f["name_check"]["agree"] for f in S if "name_check" in f)
    out["truth_order_name_check"] = dict(named_bodies=nc, agree=na, share=(na / nc if nc else None),
                                         note="geometric truth ordinal vs the conventional name (L5=1, L4=2, ...); a check of the ordering, not a score; disagreement is expected in an L6 spine")
    out["truth_caudal_bodies"] = sum(f.get("truth_caudal_bodies", 0) for f in S)
    out["det_caudal_ignored"] = sum(f.get("det_caudal_ignored", 0) for f in D)
    out["det_unmatched_in_defined_frames"] = sum(f.get("det_unmatched", 0) for f in D)
    # per case (small sets): the reader sees the spread
    if 2 <= len(cases) <= 12:
        pc = {}
        for c in cases:
            fs = [f for f in D if f["case"] == c]; m = sum(f["n_matched"] for f in fs); k = sum(f["n_correct"] for f in fs)
            pc[str(c)] = dict(frames_defined=len(fs), matched=m, correct=k, matched_correct=(k / m if m else None))
        out["per_case"] = pc
    return out


def view_bin(row, meta_dir):
    v = row.get("view"); stem = row["stem"]
    if isinstance(v, str):
        return v
    if stem.endswith("_AP"):
        return "AP"
    if stem.endswith("_LAT"):
        return "LAT"
    m = find_meta(meta_dir, stem, row.get("image"))
    if m and isinstance(m.get("view"), dict) and m["view"].get("lat_from_ap_deg") is not None:
        d = abs(float(m["view"]["lat_from_ap_deg"]))
        return "0-30" if d < 30 else ("30-60" if d < 60 else "60-90")
    return "unknown"


# ------------------------------------------------------------------------------------------------------ self-test
def _box(cx, cy, w, h):
    return [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]


def self_test():
    """Synthetic frames on a 1024 square: a sacrum at the bottom and five bodies stacked upward (L5..L1, ordinals
    1..5), then the same spine with one body missed, with a spurious box between two bodies, with a spurious box
    caudal to the sacrum, stored upside down, and with the sacrum undetected."""
    sac = _box(512, 900, 500, 220)
    bodies = [(_box(512, 720 - 150 * k, 200, 120), lv) for k, lv in enumerate(["L5", "L4", "L3", "L2", "L1"])]
    def row(preds, stem):
        return dict(stem=stem, case="synthetic", raw=[[c, b, s] for c, b, s in preds])
    det_all = [(1, sac, 0.9)] + [(0, [x + 3 for x in b], 0.8 - 0.05 * k) for k, (b, _) in enumerate(bodies)]
    # 1 clean
    r = score_frame(row(det_all, "clean"), bodies, [sac], 0.25)
    assert r["defined"] and [t["ordinal"] for t in r["truth"]] == [1, 2, 3, 4, 5], r["truth"]
    assert [d["ordinal"] for d in r["det"]] == [1, 2, 3, 4, 5] and r["n_correct"] == 5 and r["exact"], r
    # 2 one missed body (L3, ordinal 3): L5, L4 right; L2 and L1 read one too low
    det = [q for q in det_all if not (q[0] == 0 and abs(centre(q[1])[1] - 420) < 5)]
    r = score_frame(row(det, "missed"), bodies, [sac], 0.25)
    assert r["per_truth"] == ["correct", "correct", "missed", "one_off", "one_off"], r["per_truth"]
    assert r["n_matched"] == 4 and r["n_correct"] == 2 and r["n_missed"] == 1 and not r["all_matched_correct"], r
    # 3 a spurious box in the L4-L3 disc (matches nothing): every body above it reads one too high
    det = det_all + [(0, _box(512, 495, 200, 60), 0.5)]
    r = score_frame(row(det, "spurious"), bodies, [sac], 0.25)
    assert r["per_truth"] == ["correct", "correct", "one_off", "one_off", "one_off"], r["per_truth"]
    assert r["det_unmatched"] == 1 and r["n_correct"] == 2 and r["n_one_off"] == 3, r
    # 4 a spurious box caudal to the sacrum is ignored, not counted
    det = det_all + [(0, _box(512, 1000, 120, 60), 0.5)]
    r = score_frame(row(det, "caudal"), bodies, [sac], 0.25)
    assert r["det_caudal_ignored"] == 1 and r["n_correct"] == 5 and r["exact"], r
    # 4b one true body beside the sacrum and one spurious box farther away on the other side (DeepFluoro 18-1109_003):
    #    the tie goes to the side nearer the sacrum, so the true body is ordinal 1 and the far box is ignored
    r = score_frame(row([(1, sac, 0.9), (0, [x + 3 for x in bodies[0][0]], 0.8), (0, _box(512, 1150, 200, 80), 0.4)], "tie"), bodies[:1], [sac], 0.25)
    assert r["per_truth"] == ["correct"] and r["det_caudal_ignored"] == 1, r
    # 5 stored upside down (sacrum at the top, bodies running down): identical ordinals without any flag
    flip = lambda b: [b[0], 1024 - b[3], b[2], 1024 - b[1]]  # noqa: E731
    r = score_frame(row([(c, flip(b), s) for c, b, s in det_all], "flipped"), [(flip(b), lv) for b, lv in bodies], [flip(sac)], 0.25)
    assert [t["ordinal"] for t in r["truth"]] == [1, 2, 3, 4, 5] and r["n_correct"] == 5, r
    # 6 a lateral-like tilt: the column leans 25 degrees and the sacrum centre sits off the column axis
    import math
    th = math.radians(25); rot = lambda b: (lambda c: _box(512 + (c[0] - 512) * math.cos(th) - (c[1] - 512) * math.sin(th), 512 + (c[0] - 512) * math.sin(th) + (c[1] - 512) * math.cos(th), b[2] - b[0], b[3] - b[1]))(centre(b))  # noqa: E731
    sac_t = rot(_box(600, 900, 500, 220))
    r = score_frame(row([(1, sac_t, 0.9)] + [(0, rot(b), 0.8) for b, _ in bodies], "tilted"), [(rot(b), lv) for b, lv in bodies], [sac_t], 0.25)
    assert [t["ordinal"] for t in r["truth"]] == [1, 2, 3, 4, 5] and r["n_correct"] == 5, r
    # 7 sacrum not detected: counting undefined
    r = score_frame(row([q for q in det_all if q[0] == 0], "nosac"), bodies, [sac], 0.25)
    assert r["defined"] is False and r["why"] == "sacrum not detected", r
    # 8 no truth sacrum: undefined
    r = score_frame(row(det_all, "notruthsac"), bodies, [], 0.25)
    assert r["defined"] is False and "no truth sacrum" in r["why"], r
    # 9 the name check agrees on the clean truth
    r = score_frame(row(det_all, "clean"), bodies, [sac], 0.25)
    assert r["name_check"] == dict(named=5, agree=5), r["name_check"]
    # 10 pooled + bootstrap on three synthetic cases
    frames = []
    for c in ("a", "b", "c"):
        for stem, det in (("clean", det_all), ("missed", [q for q in det_all if not (q[0] == 0 and abs(centre(q[1])[1] - 420) < 5)])):
            f = score_frame(row(det, f"{c}_{stem}"), bodies, [sac], 0.25); f["case"] = c; frames.append(f)
    P = pooled(frames)
    assert P["matched_correct"]["point"] == 21 / 27 and P["truth_correct_defined"]["point"] == 21 / 30, P["matched_correct"]
    assert P["by_truth_ordinal"]["3"]["missed"] == 3 and P["by_truth_ordinal"]["5"]["one_off"] == 3, P["by_truth_ordinal"]
    assert P["matched_correct"]["percentile"] is not None and P["matched_correct"]["n_clusters"] == 3
    print("SELF_TEST_OK: clean 5/5; one missed body -> 2/4 correct, 4/4 within one, 1 missed; spurious box -> 2/5 correct, 5/5 within one; "
          "caudal box ignored; flipped and tilted frames order identically; no sacrum -> undefined; pooled 21/27 with a 3-cluster interval")
    return 0


# ------------------------------------------------------------------------------------------------------------ main
def main() -> int:
    global N_BOOT, SEED
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump", nargs="+", help="realxray_eval.py --dump-raw json(s); several are pooled (e.g. DeepFluoro train+val+test)")
    ap.add_argument("--labels", help="YOLO labels dir (<stem>.txt, or <split>/<stem>.txt under it)")
    ap.add_argument("--meta", default=None, help="meta dir; default: <dataset>/meta beside the images the dump names")
    ap.add_argument("--convention", default="body", choices=["body", "outline"])
    ap.add_argument("--conf", type=float, default=0.25); ap.add_argument("--out")
    ap.add_argument("--arm", default=""); ap.add_argument("--set", default=""); ap.add_argument("--status", default="")
    ap.add_argument("--n-boot", type=int, default=N_BOOT); ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--self-test", action="store_true")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import eval_gate as EG
    EG.add_args(ap)
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not (a.dump and a.labels and a.out):
        ap.error("--dump, --labels and --out are required (or --self-test)")
    N_BOOT, SEED = a.n_boot, a.seed
    rows = []; sources = []; gates = []
    for p in a.dump:
        d = json.load(open(p)); sources.append(dict(file=p, frames=len(d["frames"]), weights=d.get("weights"), sweep_conf=d.get("conf")))
        # the dump's held-out verdict (tools/eval_gate.carry), before a frame is counted; a dump written before the
        # gate is gated now from its weights and frames
        gates.append(EG.carry(d, f"tools/count_from_sacrum_eval.py <- {p}", not_held_out=a.not_held_out, touched=a.touched))
        if not d["frames"] or "raw" not in d["frames"][0]:
            raise SystemExit(f"{p}: no raw predictions in the rows (needs realxray_eval.py --dump-raw)")
        rows += d["frames"]
    frames = []; checks = dict(frames=0, no_label_file=0, count_disagrees=0, boxes_mismatched=0, no_meta_level=0)
    for r in rows:
        bodies, sacra, ck = frame_truth(r, a.labels, a.meta, a.convention)
        if bodies is None:
            checks["no_label_file"] += 1; continue
        checks["frames"] += 1; checks["count_disagrees"] += int(not ck["count_agrees"]); checks["boxes_mismatched"] += ck["mismatched"]
        f = score_frame(r, bodies, sacra, a.conf); f["view_bin"] = view_bin(r, a.meta); f["label_file"] = ck["label_file"]
        frames.append(f)
    P = pooled(frames, a.seed)
    out = dict(arm=a.arm, set=a.set, status=a.status, conf=a.conf, convention=a.convention, iou=IOU_MATCH, n_boot=N_BOOT, seed=SEED,
               labels=a.labels, meta=a.meta, sources=sources, truth_check=checks,
               definition="ordinal from the detected sacrum by rank along the spine axis; truth ordinal likewise from the truth sacrum; "
                          "one-to-one greedy IoU>=0.5 matching in descending confidence (realxray_eval.sweep_matches); correct = ordinals equal",
               pooled=P, frames=frames)
    out = EG.stamp(out, EG.merge(gates))       # the carried verdicts, with the weights sha256 their dumps recorded
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)
    mc = P["matched_correct"]; tc = P["truth_correct_defined"]
    def ci(m):
        return f"[{100 * m['percentile'][0]:.1f}, {100 * m['percentile'][1]:.1f}]" if m.get("percentile") else "(one cluster)"
    print(f"{a.arm or 'arm'} {a.set or 'set'} conf {a.conf} {a.convention}: frames {P['frames']} (no truth sacrum {P['frames_no_truth_sacrum']}), "
          f"defined {P['frames_defined']}/{P['frames_with_truth_sacrum']}, matched {P['matched_bodies']}, ordinal correct "
          f"{100 * mc['point']:.1f} % {ci(mc)}" if mc["point"] is not None else "no matched bodies", flush=True)
    if tc["point"] is not None:
        print(f"   per truth body (defined frames): correct {100 * tc['point']:.1f} {ci(tc)}, missed {100 * P['truth_missed_defined']['point']:.1f}; "
              f"truth-order name check {P['truth_order_name_check']['agree']}/{P['truth_order_name_check']['named_bodies']}; "
              f"label-vs-dump mismatched boxes {checks['boxes_mismatched']}", flush=True)
    print("COUNT_EVAL_OK", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
