#!/usr/bin/env python
# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/alphabet_couple.py [tracked at 097933a]
"""Couple the morphology classifier to the count from the sacrum, one frame at a time, with sweep_map's alphabets.

THE TWO MECHANISMS. The level classifier names each vertebra from what it looks like; it is quick, it works on a
limited field, and it names an extra vertebra wrong because its vocabulary was learned on spines that have five
lumbar bodies. The count from the sacrum names nothing: it gives each body an ORDINAL (1 = the body touching the
sacrum), and an ordinal cannot be fooled by an extra body. This tool couples the two, rule-based, no training:
each candidate alphabet turns the ordinals into names, the classifier's posteriors score every candidate, the best
alphabet is the variant call, its names are the corrected names, and a body whose classifier name differs from its
corrected name is a DISAGREEMENT -- the stop signal.

INPUT. One prototype JSON per frame from tools/level_prototype.py --dump-posterior: vertebrae[i].posterior is the
27-vector over meta.level_order (single crop blended with the recurrent head, flip-TTA averaged; --posterior single
uses the single-crop vector instead). The sacrum box is the JSON's own `sacrum_box` (filled by --sacrum-detector or
--box-detector) or, with --sacrum-from-meta, the truth meta's class-1 box -- the oracle-boxes convention, where
detection is taken as given.

ENUMERATOR. Ordinal 1 is the body nearest the sacrum, counting AWAY from it along the principal axis of the box
centres (sacrum included), signed from the sacrum toward the bodies. Nothing assumes which way is up: a frame stored
upside down, or a lateral of a prone patient, counts the same. A body that IS the sacrum (IoU > 0.5 with the sacrum
box) or lies on the sacrum's far side gets no ordinal, keeps its classifier name and takes no part in the score.

ALPHABETS. sweep_map.alphabet(l6, t13, l4): the same columns decode_alphabets scores on a sweep chain (std: ordinary,
L6, T13, both; ext adds the four-lumbar pair). With the sacrum at ordinal 0, alphabet A names ordinal n as
A(n) = col[len(col) - 1 - n]. The score is the one the chain decoder maximises,

    S(A) = mean over bodies with an ordinal of  log p_i( A(n_i) ),     log floored at 1e-9,

the call is argmax_A S(A), margin = S(A*) - S(ordinary) (0 when ordinary wins), and margin_next = S(A*) minus the
runner-up. Alphabets that give the window identical names are ONE candidate (a lumbar-only field cannot tell
ordinary from T13, and no coupler should pretend it can); ties go to the simpler alphabet. An alphabet that runs
out of names for an ordinal is not a candidate.

FLAG. any disagreement, or margin_next below --tau. THE THRESHOLD IS NOT CHOSEN HERE: SchwingNet/tools/
coupling_report.py sets it on the other folds and re-applies it; without --tau the flag is the disagreement alone.
No sacrum -> call "no anchor", names unchanged, flag "no_anchor".

TRUTH. With --meta, each body is matched to the truth body box by tools/carmlspine_eval.py's rule (call centre inside
the truth box, IoU >= 0.3, one to one, best IoU first) and compared where the truth carries a level. --truth-variant
case=TAG,... fills in names for frames whose truth boxes carry NO level (the two CBCT labellers disagreed): the truth
sacrum anchors the same enumerator over the truth boxes and TAG's alphabet names them. That truth is stated as what it
is in the output (`truth_source`), never as an agreed label.

    python tools/alphabet_couple.py --pred <dir or file> [--meta <dir>] [--sacrum-from-meta] --out <dir>
    python tools/alphabet_couple.py --self-test
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_context_crops import LEVEL_ORDER  # noqa: E402
from sweep_map import alphabet  # noqa: E402  the decoder's alphabets, not a copy of them
import eval_gate as EG  # noqa: E402

P_FLOOR = 1e-9                 # decode_alphabets' floor
IOU_IS_ANCHOR = 0.5            # a "vertebra" box this coincident with the sacrum box is the sacrum
IOU_TRUTH_MATCH = 0.3          # carmlspine_eval.py
IOU_TRUTH_DUP = 0.9            # two truth boxes this coincident are one body labelled twice
TIE_ORDER = ["ordinary", "L6", "T13", "both", "L4", "L4T13"]


def alphabet_tag(l6, t13, l4=False):
    return "L4T13" if (l4 and t13) else "L4" if l4 else "both" if (l6 and t13) else "L6" if l6 else "T13" if t13 else "ordinary"


def alphabet_combos(which="std"):
    """(l6, t13, l4) in sweep_map.decode_alphabets' order."""
    combos = [(l6, t13, False) for l6 in (False, True) for t13 in (False, True)]
    if which == "ext":
        combos += [(False, False, True), (False, True, True)]
    return combos


# ------------------------------------------------------------------------------------------------- geometry
def iou(a, b):
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0])); iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy; u = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / u if u > 0 else 0.0


def centre(b):
    return np.array([(b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0], float)


def order_from_anchor(anchor, boxes, named_sacrum=None):
    """Ordinals 1..n away from the anchor box, None where a box has none. Returns (ordinals, projections, why).

    The axis is the first principal direction of every centre (anchor included), signed from the anchor toward
    the bodies' centroid; a body's ordinal is its rank by projection among the bodies on the positive side.
    `named_sacrum` (optional, per box): True where the classifier itself calls the box "sacrum"; with the
    --exclude-named-sacrum switch such a box is not a vertebra to count (why = named_sacrum). The primary
    enumerator does not use it: it is name-free.
    """
    if not boxes:
        return [], [], []
    sc = centre(anchor); cs = np.array([centre(b) for b in boxes], float)
    if len(boxes) == 1:
        u = cs[0] - sc; n = np.linalg.norm(u); u = u / n if n > 0 else np.array([0.0, 1.0])
    else:
        pts = np.vstack([sc[None, :], cs]); X = pts - pts.mean(0)
        _, _, vt = np.linalg.svd(X, full_matrices=False); u = vt[0]
        if float(np.dot(cs.mean(0) - sc, u)) < 0:
            u = -u
    t = (cs - sc) @ u
    why = []
    for i, b in enumerate(boxes):
        if iou(b, anchor[:4]) > IOU_IS_ANCHOR:
            why.append("is_anchor")
        elif named_sacrum is not None and named_sacrum[i]:
            why.append("named_sacrum")
        elif t[i] <= 0:
            why.append("beyond_anchor")
        else:
            why.append("counted")
    order = sorted([i for i in range(len(boxes)) if why[i] == "counted"], key=lambda i: t[i])
    ords = [None] * len(boxes)
    for k, i in enumerate(order):
        ords[i] = k + 1
    return ords, [float(v) for v in t], why


# ------------------------------------------------------------------------------------------------- the coupling
def couple(P, level_order, ordinals, which="std"):
    """Score every alphabet against the ordinals. P is (n, C) posteriors in level_order; ordinals has None where a
    body is not counted. Returns the call, per-candidate scores, the corrected names and the margins."""
    ORD = {n: i for i, n in enumerate(level_order)}
    idx = [i for i, o in enumerate(ordinals) if o is not None]
    if not idx:
        return {"call": "no anchor", "candidates": {}, "names": [None] * len(ordinals), "score": None,
                "margin": None, "margin_next": None, "n_counted": 0}
    cands = {}
    for l6, t13, l4 in alphabet_combos(which):
        col = alphabet(l6, t13, l4); top = len(col) - 1
        if any(ordinals[i] > top for i in idx):
            continue
        names = {i: col[top - ordinals[i]] for i in idx}
        sc = float(np.mean([np.log(max(P_FLOOR, float(P[i][ORD[names[i]]]))) for i in idx]))
        key = tuple(names[i] for i in idx)
        tag = alphabet_tag(l6, t13, l4)
        if key in cands:
            cands[key]["aliases"].append(tag)
        else:
            cands[key] = {"tag": tag, "score": sc, "aliases": [tag], "names": names}
    if not cands:
        return {"call": "no alphabet", "candidates": {}, "names": [None] * len(ordinals), "score": None,
                "margin": None, "margin_next": None, "n_counted": len(idx)}
    ranked = sorted(cands.values(), key=lambda c: (-round(c["score"], 9), TIE_ORDER.index(c["tag"])))
    best = ranked[0]
    per = {c["tag"]: round(c["score"], 4) for c in cands.values()}
    aliases = {c["tag"]: c["aliases"] for c in cands.values()}
    ord_score = next((c["score"] for c in cands.values() if "ordinary" in c["aliases"]), None)
    margin = None if ord_score is None else (0.0 if "ordinary" in best["aliases"] else round(best["score"] - ord_score, 4))
    margin_next = round(best["score"] - ranked[1]["score"], 4) if len(ranked) > 1 else None
    names = [best["names"].get(i) for i in range(len(ordinals))]
    return {"call": best["tag"], "call_aliases": best["aliases"], "candidates": per, "candidate_aliases": aliases,
            "names": names, "score": round(best["score"], 4), "margin": margin, "margin_next": margin_next,
            "n_counted": len(idx)}


# ------------------------------------------------------------------------------------------------- truth
def match_truth(pred_boxes, truth_boxes):
    """carmlspine_eval.py's rule: call centre inside the truth box, IoU >= 0.3, one to one, best IoU first."""
    pairs = []
    for i, cb in enumerate(pred_boxes):
        cx, cy = (cb[0] + cb[2]) / 2, (cb[1] + cb[3]) / 2
        for j, tb in enumerate(truth_boxes):
            if tb[0] <= cx <= tb[2] and tb[1] <= cy <= tb[3]:
                o = iou(cb, tb)
                if o >= IOU_TRUTH_MATCH:
                    pairs.append((o, i, j))
    used_c, used_t, match = set(), set(), {}
    for o, i, j in sorted(pairs, reverse=True):
        if i in used_c or j in used_t:
            continue
        used_c.add(i); used_t.add(j); match[i] = j
    return match


def dedupe_boxes(boxes):
    keep = []
    for b in boxes:
        if all(iou(b["box"], k["box"]) <= IOU_TRUTH_DUP for k in keep):
            keep.append(b)
    return keep


def truth_from_variant(meta, tag):
    """Names for a truth meta whose bodies carry no level: TAG's alphabet read from the truth sacrum by the same
    enumerator. Returns (truth_boxes, names, sacrum_box) or (boxes, [None...], None) when there is no truth sacrum."""
    bodies = dedupe_boxes([b for b in meta["boxes"] if b["cls"] == 0])
    sac = [b for b in meta["boxes"] if b["cls"] == 1]
    if not sac:
        return bodies, [None] * len(bodies), None
    sb = max(sac, key=lambda b: (b["box"][2] - b["box"][0]) * (b["box"][3] - b["box"][1]))["box"]
    ords, _, _ = order_from_anchor(sb, [b["box"] for b in bodies])
    l6, t13, l4 = {"ordinary": (False, False, False), "L6": (True, False, False), "T13": (False, True, False),
                   "both": (True, True, False), "L4": (False, False, True), "L4T13": (False, True, True)}[tag]
    col = alphabet(l6, t13, l4); top = len(col) - 1
    names = [col[top - o] if (o is not None and o <= top) else None for o in ords]
    return bodies, names, sb


# ------------------------------------------------------------------------------------------------- one frame
def couple_frame(rec, sacrum_box, level_order, meta=None, truth_variant=None, which="std", posterior="blend",
                 classifier_field="level", tau=None, sacrum_min_conf=0.0, exclude_named_sacrum=False, dedupe_boxes=False):
    vert = rec.get("vertebrae", [])
    key = "posterior" if posterior == "blend" else "posterior_single"
    if vert and key not in vert[0]:
        raise SystemExit(f"{rec.get('image')}: no `{key}` in the vertebra records; re-run level_prototype.py --dump-posterior")
    n_dropped = 0
    if dedupe_boxes:
        # THE ORACLE ARM'S BOXES ARE THE TRUTH BOXES, and a truth body boxed by both CBCT labellers arrives twice
        # (IoU ~0.98). Counted twice it is two ordinals, and every body above it shifts by one -- a five-body
        # lumbar spine then scores as six and the L6 alphabet wins by construction (verifier's finding,
        # SchwingNet/results/COUPLING_CHECK.md). Off by default so the shipped outputs are reproducible; the
        # keypoint detector's boxes never duplicate.
        kept = []
        for v in vert:
            if all(iou(v["box"], k["box"]) <= IOU_TRUTH_DUP for k in kept):
                kept.append(v)
        n_dropped = len(vert) - len(kept); vert = kept
    boxes = [v["box"] for v in vert]
    P = np.array([v[key] for v in vert], float) if vert else np.zeros((0, len(level_order)))
    rejected = None
    if sacrum_box and len(sacrum_box) > 4 and sacrum_box[4] is not None and float(sacrum_box[4]) < sacrum_min_conf:
        rejected = {"box": [int(v) for v in sacrum_box[:4]], "conf": sacrum_box[4], "min_conf": sacrum_min_conf}
        sacrum_box = None
    out = {"image": rec.get("image"), "stem": Path(rec.get("image", "")).stem, "n_bodies": len(vert),
           "anchor": {"box": [int(v) for v in sacrum_box[:4]] if sacrum_box else None,
                      "conf": (sacrum_box[4] if (sacrum_box and len(sacrum_box) > 4) else None), "rejected": rejected},
           "posterior": posterior, "classifier_field": classifier_field, "alphabets": which,
           "sacrum_min_conf": sacrum_min_conf, "exclude_named_sacrum": bool(exclude_named_sacrum),
           "dedupe_boxes": bool(dedupe_boxes), "n_boxes_dropped_as_duplicates": n_dropped}
    named = [(v.get(classifier_field) == "sacrum") for v in vert] if exclude_named_sacrum else None
    if sacrum_box and vert:
        ords, proj, why = order_from_anchor(sacrum_box[:4], boxes, named)
    else:
        ords, proj, why = [None] * len(vert), [None] * len(vert), (["no_anchor"] * len(vert) if vert else [])
    ORD_COL = alphabet(False, False, False); top_ord = len(ORD_COL) - 1
    c = couple(P, level_order, ords, which) if sacrum_box and vert else \
        {"call": "no anchor", "candidates": {}, "names": [None] * len(vert), "score": None, "margin": None, "margin_next": None, "n_counted": 0}
    out.update({"call": c["call"], "call_aliases": c.get("call_aliases"), "candidates": c["candidates"],
                "candidate_aliases": c.get("candidate_aliases"), "score": c["score"], "margin": c["margin"],
                "margin_next": c["margin_next"], "n_counted": c["n_counted"]})
    bodies = []
    for i, v in enumerate(vert):
        cls_name = v.get(classifier_field) or level_order[int(np.argmax(P[i]))]
        am = level_order[int(np.argmax(P[i]))]
        coupled = c["names"][i] if c["names"][i] is not None else cls_name
        count_name = ORD_COL[top_ord - ords[i]] if (ords[i] is not None and ords[i] <= top_ord) else None
        b = {"i": i, "box": v["box"], "ordinal": ords[i], "why": why[i], "projection": (round(proj[i], 1) if proj[i] is not None else None),
             "classifier": cls_name, "argmax": am, "p_classifier": round(float(P[i][level_order.index(cls_name)]), 4) if cls_name in level_order else None,
             "coupled": coupled, "p_coupled": round(float(P[i][level_order.index(coupled)]), 4) if coupled in level_order else None,
             "count": count_name,       # the ordinary alphabet at this ordinal: the count alone, no classifier
             "corrected": bool(ords[i] is not None and coupled != cls_name),
             "disagree": bool(ords[i] is not None and coupled != cls_name),
             "abstain": bool(v.get("abstain")), "level_prob": v.get("level_prob")}
        bodies.append(b)
    out["bodies"] = bodies
    out["n_disagree"] = sum(b["disagree"] for b in bodies)
    out["flag_disagree"] = out["n_disagree"] > 0
    out["flag_low_margin"] = (tau is not None and c["margin_next"] is not None and c["margin_next"] < tau)
    out["tau"] = tau
    if not sacrum_box:
        out["flag"] = True; out["flag_reason"] = "no_anchor"
    elif not vert:
        out["flag"] = True; out["flag_reason"] = "no_vertebra"
    elif out["flag_disagree"]:
        out["flag"] = True; out["flag_reason"] = "disagreement"
    elif out["flag_low_margin"]:
        out["flag"] = True; out["flag_reason"] = "low_margin"
    else:
        out["flag"] = False; out["flag_reason"] = None
    # ---- truth
    if meta is not None:
        truth = [b for b in meta["boxes"] if b["cls"] == 0]
        tsac = [b for b in meta["boxes"] if b["cls"] == 1]
        out["truth_sacrum_in_frame"] = bool(tsac)
        source = "labellers_agree"
        if truth_variant and meta.get("case") in truth_variant and not any(t.get("level") for t in truth):
            truth, tnames, _ = truth_from_variant(meta, truth_variant[meta["case"]])
            truth = [dict(t, level=nm) for t, nm in zip(truth, tnames)]
            source = f"variant_alphabet:{truth_variant[meta['case']]}"
        out["truth_source"] = source
        out["case"] = meta.get("case"); out["view"] = meta.get("view"); out["k"] = meta.get("k", "full")
        match = match_truth(boxes, [t["box"] for t in truth])
        out["n_truth"] = len(truth); out["n_truth_named"] = sum(1 for t in truth if t.get("level")); out["n_matched"] = len(match)
        for i, j in match.items():
            tl = truth[j].get("level")
            if not tl:
                continue
            b = bodies[i]
            b["truth"] = tl; b["classifier_exact"] = (b["classifier"] == tl); b["coupled_exact"] = (b["coupled"] == tl)
            b["count_exact"] = (b["count"] == tl) if b["count"] is not None else None
        scored = [b for b in bodies if "truth" in b]
        out["n_scored"] = len(scored)
        out["classifier_correct"] = sum(b["classifier_exact"] for b in scored)
        out["coupled_correct"] = sum(b["coupled_exact"] for b in scored)
        out["count_correct"] = sum(1 for b in scored if b.get("count_exact"))
        out["n_scored_counted"] = sum(1 for b in scored if b["count"] is not None)
        out["frame_all_correct_coupled"] = bool(scored) and all(b["coupled_exact"] for b in scored)
        out["frame_all_correct_classifier"] = bool(scored) and all(b["classifier_exact"] for b in scored)
    return out


def sacrum_from_meta(meta):
    sac = [b for b in meta["boxes"] if b["cls"] == 1]
    if not sac:
        return None
    sb = max(sac, key=lambda b: (b["box"][2] - b["box"][0]) * (b["box"][3] - b["box"][1]))["box"]
    return [float(v) for v in sb] + [1.0]


# ------------------------------------------------------------------------------------------------- self-test
def _peaked(level_order, name, p=0.9, second=None, p2=None):
    C = len(level_order); v = np.full(C, (1.0 - p - (p2 or 0.0)) / (C - (2 if second else 1)))
    v[level_order.index(name)] = p
    if second:
        v[level_order.index(second)] = p2
    return v / v.sum()


def self_test():
    L = LEVEL_ORDER
    H = 100
    def stack(n, sacrum_at="bottom"):
        # n bodies stacked along y, the sacrum below the last (or above the first, for the upside-down check)
        boxes = [[400, 20 + k * (H + 30), 600, 20 + k * (H + 30) + H] for k in range(n)]
        y = boxes[-1][3] + 30 if sacrum_at == "bottom" else boxes[0][1] - 30 - 2 * H
        sac = [300, y, 700, y + 2 * H, 0.9]
        if sacrum_at == "top":
            boxes = boxes[::-1]        # listed caudal-first, so the ordering cannot be inherited from the list
        return boxes, sac
    def frame(boxes, posts, sac, names=None):
        vert = [{"box": b, "posterior": [float(x) for x in p], "level": (names[i] if names else L[int(np.argmax(p))]), "abstain": False}
                for i, (b, p) in enumerate(zip(boxes, posts))]
        return {"image": "synthetic.png", "vertebrae": vert, "sacrum_box": sac}
    # (a) ordinary: L1..L5 above the sacrum, all confident and right
    boxes, sac = stack(5); posts = [_peaked(L, n) for n in ["L1", "L2", "L3", "L4", "L5"]]
    o = couple_frame(frame(boxes, posts, sac), sac, L)
    assert o["call"] == "ordinary" and [b["coupled"] for b in o["bodies"]] == ["L1", "L2", "L3", "L4", "L5"], o
    assert o["margin"] == 0.0 and o["n_disagree"] == 0 and not o["flag"], o
    assert [b["ordinal"] for b in o["bodies"]] == [5, 4, 3, 2, 1], o
    print("  (a) ordinary run: call ordinary, names unchanged, no disagreement, margin 0            PASS")
    # (b) L6 spine: six bodies; the classifier reads the upper five as L1..L5 and the sixth (touching the
    #     sacrum) as "L5" too -- relative to a count that expects L5 at ordinal 1, everything above is shifted by one.
    #     The count says six bodies; the morphology says the top one is L1, not T12; the L6 alphabet must win and
    #     every corrected name must equal the truth L1..L6.
    boxes, sac = stack(6); posts = [_peaked(L, n) for n in ["L1", "L2", "L3", "L4", "L5"]] + [_peaked(L, "L5", 0.6, "L6", 0.3)]
    o = couple_frame(frame(boxes, posts, sac), sac, L)
    assert o["call"] == "L6", o["candidates"]
    assert [b["coupled"] for b in o["bodies"]] == ["L1", "L2", "L3", "L4", "L5", "L6"], o
    assert o["margin"] > 0 and o["n_disagree"] == 1 and o["bodies"][5]["disagree"] and o["flag_reason"] == "disagreement", o
    print(f"  (b) L6 run, classifier calls the sixth body L5: call L6 (margin {o['margin']:.2f}), all six names corrected  PASS")
    # (b') the same L6 spine stored upside down (every y mirrored, so the sacrum is at the TOP of the image) and
    #      the boxes listed in a scrambled order: the call, the names and the ordinals must not move.
    boxes, sac = stack(6); Y = 2000
    flip = lambda b: [b[0], Y - b[3], b[2], Y - b[1]] + list(b[4:])  # noqa: E731
    perm = [3, 0, 5, 1, 4, 2]
    fb = [flip(boxes[i]) for i in perm]; fp = [posts[i] for i in perm]; fs = flip(sac)
    o = couple_frame(frame(fb, fp, fs), fs, L)
    assert o["call"] == "L6" and [b["coupled"] for b in o["bodies"]] == [["L1", "L2", "L3", "L4", "L5", "L6"][i] for i in perm], o
    assert [b["ordinal"] for b in o["bodies"]] == [[6, 5, 4, 3, 2, 1][i] for i in perm], o
    print("  (b') the same spine upside down, boxes scrambled: identical call, names and ordinals             PASS")
    # (c) one confident classifier error on an ordinary spine: L3 called L2 at p 0.8. The ordinary alphabet still
    #     wins on the other four, the body is renamed L3 and flagged.
    boxes, sac = stack(5); posts = [_peaked(L, "L1"), _peaked(L, "L2"), _peaked(L, "L2", 0.8, "L3", 0.1), _peaked(L, "L4"), _peaked(L, "L5")]
    o = couple_frame(frame(boxes, posts, sac), sac, L)
    assert o["call"] == "ordinary" and [b["coupled"] for b in o["bodies"]] == ["L1", "L2", "L3", "L4", "L5"], o
    assert o["n_disagree"] == 1 and o["bodies"][2]["disagree"] and o["bodies"][2]["classifier"] == "L2" and o["flag"], o
    print("  (c) one confident classifier error: alphabet wins, the body is corrected and flagged          PASS")
    # (d) no sacrum: no correction, names unchanged, flag no_anchor
    boxes, _ = stack(5); posts = [_peaked(L, "L1"), _peaked(L, "L2"), _peaked(L, "L2", 0.8, "L3", 0.1), _peaked(L, "L4"), _peaked(L, "L5")]
    o = couple_frame(frame(boxes, posts, None), None, L)
    assert o["call"] == "no anchor" and [b["coupled"] for b in o["bodies"]] == ["L1", "L2", "L2", "L4", "L5"], o
    assert o["n_disagree"] == 0 and o["flag"] and o["flag_reason"] == "no_anchor" and all(b["ordinal"] is None for b in o["bodies"]), o
    print("  (d) no sacrum: call 'no anchor', names unchanged, flag no_anchor                              PASS")
    # (e) a detector box ON the sacrum (the sacrum boxed as a vertebra): it takes no ordinal and shifts nothing
    boxes, sac = stack(5); boxes2 = boxes + [[sac[0] + 5, sac[1] + 5, sac[2] - 5, sac[3] - 5]]
    posts = [_peaked(L, n) for n in ["L1", "L2", "L3", "L4", "L5", "sacrum"]]
    o = couple_frame(frame(boxes2, posts, sac), sac, L)
    assert [b["ordinal"] for b in o["bodies"]] == [5, 4, 3, 2, 1, None] and o["bodies"][5]["why"] == "is_anchor", o
    assert o["call"] == "ordinary" and [b["coupled"] for b in o["bodies"]] == ["L1", "L2", "L3", "L4", "L5", "sacrum"], o
    print("  (e) the sacrum boxed as a vertebra: no ordinal, count unshifted                               PASS")
    # (f) the truth rule for a variant case: truth boxes with no level, L6 alphabet from the truth sacrum
    boxes, sac = stack(5)
    meta = {"case": "caseX", "view": "AP", "boxes": [{"cls": 0, "box": b, "level": None} for b in boxes] + [{"cls": 0, "box": boxes[0], "level": None}]
            + [{"cls": 1, "box": sac[:4], "level": "sacrum"}]}
    posts = [_peaked(L, n) for n in ["L2", "L3", "L4", "L5", "L5"]]
    o = couple_frame(frame(boxes, posts, sac), sac, L, meta=meta, truth_variant={"caseX": "L6"})
    assert o["truth_source"] == "variant_alphabet:L6" and o["n_truth"] == 5, o     # the duplicate truth box was dropped
    assert [b["truth"] for b in o["bodies"]] == ["L2", "L3", "L4", "L5", "L6"], o
    assert o["classifier_correct"] == 4 and o["coupled_correct"] == 5 and o["call"] == "L6", o
    print("  (f) variant truth: duplicate truth box dropped, names from the truth sacrum, L6 corrected        PASS")
    # (g) the count-only names ride along (ordinary alphabet at the ordinal), and the sacrum-confidence floor and
    #     the named-sacrum switch behave: a low-confidence anchor is rejected (no anchor); a body the classifier
    #     calls "sacrum" that sits beside (not on) the sacrum box is counted by the name-free enumerator and
    #     excluded only under --exclude-named-sacrum.
    boxes, sac = stack(5); posts = [_peaked(L, n) for n in ["L1", "L2", "L3", "L4", "L5"]]
    o = couple_frame(frame(boxes, posts, sac), sac, L)
    assert [b["count"] for b in o["bodies"]] == ["L1", "L2", "L3", "L4", "L5"], o
    low = sac[:4] + [0.3]
    o = couple_frame(frame(boxes, posts, low), low, L, sacrum_min_conf=0.74)
    assert o["call"] == "no anchor" and o["anchor"]["rejected"]["conf"] == 0.3 and o["flag_reason"] == "no_anchor", o
    s1 = [[boxes[-1][0], boxes[-1][3] + 30, boxes[-1][2], boxes[-1][3] + 30 + H]]     # a small box between L5 and the sacrum box
    sac2 = [300, s1[0][3] + 10, 700, s1[0][3] + 10 + 2 * H, 0.9]
    posts2 = posts + [_peaked(L, "sacrum", 0.5, "L6", 0.3)]
    o = couple_frame(frame(boxes + s1, posts2, sac2), sac2, L)
    assert [b["ordinal"] for b in o["bodies"]] == [6, 5, 4, 3, 2, 1] and o["bodies"][5]["why"] == "counted", o
    o = couple_frame(frame(boxes + s1, posts2, sac2), sac2, L, exclude_named_sacrum=True)
    assert [b["ordinal"] for b in o["bodies"]] == [5, 4, 3, 2, 1, None] and o["bodies"][5]["why"] == "named_sacrum", o
    assert o["call"] == "ordinary" and [b["coupled"] for b in o["bodies"]] == ["L1", "L2", "L3", "L4", "L5", "sacrum"], o
    print("  (g) count-only names; anchor below the confidence floor rejected; named-sacrum switch                PASS")
    # (h) a T13 spine: seven bodies above the sacrum (L5..L1, T13, T12 from the sacrum up). The classifier reads
    #     the lumbar five right, the 13th thoracic as "T12" (p 0.6, T13 0.3) and the real T12 as T12. Ordinary
    #     names ordinal 7 T11 and T13 names it T12: only the T13 alphabet fits the morphology of the top body,
    #     so the call must be T13, the 13th thoracic renamed T13 and flagged, the other six untouched.
    #     (A lumbar-only field cannot make this call: ordinary and T13 are one candidate there, see (a).)
    boxes, sac = stack(7)
    posts = [_peaked(L, "T12"), _peaked(L, "T12", 0.6, "T13", 0.3)] + [_peaked(L, n) for n in ["L1", "L2", "L3", "L4", "L5"]]
    o = couple_frame(frame(boxes, posts, sac), sac, L)
    assert o["call"] == "T13", o["candidates"]
    assert [b["coupled"] for b in o["bodies"]] == ["T12", "T13", "L1", "L2", "L3", "L4", "L5"], o
    assert [b["ordinal"] for b in o["bodies"]] == [7, 6, 5, 4, 3, 2, 1], o
    assert o["n_disagree"] == 1 and o["bodies"][1]["disagree"] and o["bodies"][1]["classifier"] == "T12" and o["flag_reason"] == "disagreement", o
    assert o["margin"] > 0 and "T13" in o["candidates"] and "ordinary" in o["candidates"], o
    print(f"  (h) T13 run, classifier calls the 13th thoracic T12: call T13 (margin {o['margin']:.2f}), that body renamed, six untouched  PASS")
    # (i) BOTH: eight bodies above the sacrum (L6..L1, T13, T12). The classifier reads the sixth lumbar "L5"
    #     (p 0.6, L6 0.3), the 13th thoracic "T12" (0.6, T13 0.3), the rest right. Only the `both` alphabet names
    #     every ordinal as the morphology reads it; L6 alone would name the top body T11, T13 alone would shift the
    #     lumbar five. Call must be `both`, two disagreements, six names untouched.
    boxes, sac = stack(8)
    posts = [_peaked(L, "T12"), _peaked(L, "T12", 0.6, "T13", 0.3)] + [_peaked(L, n) for n in ["L1", "L2", "L3", "L4", "L5"]] + [_peaked(L, "L5", 0.6, "L6", 0.3)]
    o = couple_frame(frame(boxes, posts, sac), sac, L)
    assert o["call"] == "both", o["candidates"]
    assert [b["coupled"] for b in o["bodies"]] == ["T12", "T13", "L1", "L2", "L3", "L4", "L5", "L6"], o
    assert [b["ordinal"] for b in o["bodies"]] == [8, 7, 6, 5, 4, 3, 2, 1], o
    assert o["n_disagree"] == 2 and o["bodies"][1]["disagree"] and o["bodies"][7]["disagree"] and o["flag_reason"] == "disagreement", o
    assert set(o["candidates"]) == {"ordinary", "T13", "L6", "both"}, o["candidates"]
    assert o["candidates"]["both"] > o["candidates"]["L6"] > o["candidates"]["ordinary"] and o["candidates"]["both"] > o["candidates"]["T13"], o["candidates"]
    print(f"  (i) both L6 and T13, classifier calls them L5 and T12: call both (margin {o['margin']:.2f}), two renamed, six untouched      PASS")
    # (i') the same eight-body spine with the classifier reading every body as the ORDINARY count would (top two
    #      T11, T12): morphology and count agree on the ordinary alphabet and no variant may be called
    posts = [_peaked(L, n) for n in ["T10", "T11", "T12", "L1", "L2", "L3", "L4", "L5"]]
    o = couple_frame(frame(boxes, posts, sac), sac, L)
    assert o["call"] == "ordinary" and o["n_disagree"] == 0 and not o["flag"], o
    print("  (i') eight bodies the classifier reads as T10..L5: ordinary, no disagreement                       PASS")
    # (j) an ORDINARY five-body spine whose top body arrives twice (the oracle arm: both CBCT labellers boxed it,
    #     IoU ~0.98), the classifier reading both copies L1. Counted as is, the duplicate is a sixth ordinal and
    #     the L6 alphabet wins a spine that has five bodies; with --dedupe-boxes the copy is dropped and the call
    #     is ordinary with no disagreement. This is the defect found in the shipped oracle cells.
    boxes, sac = stack(5); dup = [boxes[0][0] + 1, boxes[0][1] - 1, boxes[0][2] + 1, boxes[0][3]]
    #     (j1) confident ordinary morphology: the call survives, but the copy is a sixth ordinal and the COUNT
    #          names one copy T12 -- the count-only baseline is wrong on a frame whose spine is right.
    posts = [_peaked(L, n) for n in ["L1", "L2", "L3", "L4", "L5"]]
    o = couple_frame(frame(boxes + [dup], posts + [_peaked(L, "L1")], sac), sac, L)
    assert o["call"] == "ordinary" and o["n_counted"] == 6 and sorted([o["bodies"][0]["count"], o["bodies"][5]["count"]]) == ["L1", "T12"], o
    o = couple_frame(frame(boxes + [dup], posts + [_peaked(L, "L1")], sac), sac, L, dedupe_boxes=True)
    assert o["n_counted"] == 5 and o["n_boxes_dropped_as_duplicates"] == 1 and [b["count"] for b in o["bodies"]] == ["L1", "L2", "L3", "L4", "L5"], o
    #     (j2) the posteriors of case42 AP (oracle, fold 2) in shape: the top body reads L2, the run leans one
    #          name caudal, the bottom body reads L5 at 0.99. With the copy counted the L6 alphabet wins (six
    #          ordinals, five bodies); with it dropped, ordinary wins. That is the shipped oracle L6 call.
    posts = [_peaked(L, "L2", 0.96, "L1", 0.03), _peaked(L, "L2", 0.96, "L1", 0.03), _peaked(L, "L3", 0.56, "L2", 0.44),
             _peaked(L, "L4", 0.87, "L3", 0.12), _peaked(L, "L4", 0.56, "L5", 0.42), _peaked(L, "L5", 0.99)]
    bx = [boxes[0], dup] + boxes[1:]
    o = couple_frame(frame(bx, posts, sac), sac, L)
    assert o["call"] == "L6" and o["n_counted"] == 6, (o["call"], o["candidates"])
    o = couple_frame(frame(bx, posts, sac), sac, L, dedupe_boxes=True)
    assert o["call"] == "ordinary" and o["n_counted"] == 5 and o["n_boxes_dropped_as_duplicates"] == 1, (o["call"], o["candidates"])
    print("  (j) a body boxed twice: the count misnames a copy; case42-shaped posteriors give a false L6; --dedupe-boxes -> ordinary  PASS")
    print("self-test PASS")
    return 0


# ------------------------------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred", help="prototype output directory (or one frame's JSON)")
    ap.add_argument("--meta", default=None, help="truth meta directory (docs/REAL_XRAY_DATASETS_SPEC.md); enables the truth comparison")
    ap.add_argument("--out", default=None, help="output directory: <stem>.couple.json per frame and couple_all.json")
    ap.add_argument("--sacrum-from-meta", action="store_true", help="anchor on the truth meta's class-1 box (the oracle-boxes convention) instead of the JSON's sacrum_box")
    ap.add_argument("--alphabets", default="std", choices=["std", "ext"])
    ap.add_argument("--posterior", default="blend", choices=["blend", "single"])
    ap.add_argument("--classifier-field", default="level", choices=["level", "single_crop"], help="which reported name counts as the classifier's")
    ap.add_argument("--tau", type=float, default=None, help="margin_next below which the frame is flagged; set by coupling_report.py on other folds, never here")
    ap.add_argument("--truth-variant", default=None, help="case=TAG,... : truth names for frames whose truth boxes carry no level (see module docstring)")
    ap.add_argument("--sacrum-min-conf", type=float, default=0.0,
                    help="a detected sacrum below this confidence is treated as absent (no anchor). 0.74 is the LODO detector's "
                         "cross-device operating point (tools/rigor_fixes.py A1, chosen on other devices); 0 keeps every detection")
    ap.add_argument("--exclude-named-sacrum", action="store_true",
                    help="a body the classifier itself names 'sacrum' takes no ordinal (the keypoint detector sometimes boxes S1 as a "
                         "vertebra). Off by default: the primary enumerator is name-free")
    ap.add_argument("--dedupe-boxes", action="store_true",
                    help="drop a vertebra box with IoU > 0.9 to an earlier one before counting (the oracle arm's truth boxes carry a "
                         "body twice when both CBCT labellers boxed it). Off by default")
    ap.add_argument("--self-test", action="store_true")
    EG.add_args(ap)
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.pred or not a.out:
        ap.error("--pred and --out are required (or --self-test)")
    tv = None
    if a.truth_variant:
        tv = dict(kv.split("=") for kv in a.truth_variant.split(","))
    pred = os.path.expanduser(a.pred)
    files = [pred] if os.path.isfile(pred) else sorted(p for p in glob.glob(os.path.join(pred, "*.json")) if not os.path.basename(p).startswith(("prototype_", "couple")))
    meta_j = json.load(open(os.path.join(pred if os.path.isdir(pred) else os.path.dirname(pred), "prototype_meta.json")))
    level_order = meta_j["level_order"]
    # the prototype run's held-out verdict (tools/eval_gate.carry_proto): its prototype_meta.json block, or -- for a
    # run written before the gate -- a gate now over its models (detector, encoder, head, sacrum detector) and images
    gate = EG.carry_proto(pred if os.path.isdir(pred) else os.path.dirname(pred), "tools/alphabet_couple.py",
                          not_held_out=a.not_held_out, touched=a.touched)
    out = Path(os.path.expanduser(a.out)); out.mkdir(parents=True, exist_ok=True)
    rows = []
    for f in files:
        rec = json.load(open(f))
        stem = Path(f).stem
        meta = None
        if a.meta:
            mp = os.path.join(os.path.expanduser(a.meta), stem + ".json")
            meta = json.load(open(mp)) if os.path.exists(mp) else None
        sac = rec.get("sacrum_box")
        src = rec.get("sacrum_source") or ("json" if sac else None)
        if a.sacrum_from_meta:
            sac = sacrum_from_meta(meta) if meta else None; src = "truth_meta" if sac else None
        r = couple_frame(rec, sac, level_order, meta=meta, truth_variant=tv, which=a.alphabets, posterior=a.posterior,
                         classifier_field=a.classifier_field, tau=a.tau, sacrum_min_conf=a.sacrum_min_conf,
                         exclude_named_sacrum=a.exclude_named_sacrum, dedupe_boxes=a.dedupe_boxes)
        r["anchor"]["source"] = src; r["stem"] = stem
        r["detected_sacrum_box"] = rec.get("sacrum_box"); r["detected_sacrum_source"] = rec.get("sacrum_source")
        json.dump(r, open(out / f"{stem}.couple.json", "w"), indent=1)
        rows.append(r)
        cls_ = " ".join(b["classifier"] for b in r["bodies"]); cp = " ".join(b["coupled"] for b in r["bodies"])
        tr = (" truth " + " ".join(str(b.get("truth", "-")) for b in r["bodies"])) if meta else ""
        print(f"{stem}: {r['call']} m={r['margin']} mn={r['margin_next']} | {cls_} -> {cp}{tr} | flag={r['flag_reason']}")
    json.dump(EG.stamp({"args": vars(a), "level_order": level_order, "prototype_meta": meta_j, "frames": rows}, gate),
              open(out / "couple_all.json", "w"), indent=1)
    n_anch = sum(1 for r in rows if r["call"] not in ("no anchor",))
    calls = {}
    for r in rows:
        calls[r["call"]] = calls.get(r["call"], 0) + 1
    print(f"{len(rows)} frames, {n_anch} with an anchor; calls {calls}; wrote {out / 'couple_all.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
