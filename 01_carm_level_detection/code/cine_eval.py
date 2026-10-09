#!/usr/bin/env python
# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/cine_eval.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""One scoring harness for vertebra detection, corners, level naming and TRACKING on image sequences (cine):
Bournemouth cervical quantitative fluoroscopy (tools/bournemouth_qf_eval.py), the C-ArmLSpine CBCT projection
sweeps (case134, case39), and the synthetic lumbar flexion-extension cine of CTSP 0533
(docs/CINE_DEMO_BUILD_PLAN_2026-09-26.md section 1b). Pure numpy / scipy / PIL: it runs on Windows for the self-test.

  score      a tools/level_prototype.py output (run with --dump-posterior --dump-corners; one directory, or one
             directory per sequence under it) against truth metas in the cine schema below: detection, IoU, centre
             error, corner error per GEOMETRIC slot, naming (exact, within one, abstain), by level, by level group and
             by bin (--bins); with --track <track.json>, the temporal metrics as well. The held-out verdict of every
             prototype run is carried (tools/eval_gate.carry_proto) and stamped on the result.
  track      an online, CAUSAL tracker over the prototype's per-frame detections (no future frame is read, so it is
             honest for a real-time claim). Its constants live in tracker_config.json, whose sha256 every output
             records, and are fixed before any Bournemouth frame is seen.
  video      truth and predictions drawn on the frames, piped as raw RGB to ffmpeg (libx264). No header text and no
             file name is ever drawn into a frame.
  self-test  the metric battery on a synthetic sequence, every result compared with its exact expected value.

TRUTH SCHEMA, one meta/<stem>.json per frame:
  {case, stem, seq, frame, view, px_mm|null, corner_order: "anatomical"|"geometric",
   boxes: [{gt_id, cls, level|null, box: [x0, y0, x1, y1], corners: [[x, y] x 4]|null, role}], extras: {...}}
  gt_id   a stable identity WITHIN the sequence (the level name, or the SPINEPS instance for case134): what the
          identity-switch scoring follows. Required by score --track.
  role    "score"       full truth: box, corners, recall denominator.
          "caudal_only" only the two caudal corners are truth (Bournemouth C2: points 2 and 3 are real, 1 and 4
                        arbitrary). It matches a prediction whose inferior edge lies within 0.25 x the median body
                        height of the truth's inferior edge -- its LOWER caudal corner (--caudal-ref; the plan's
                        wording, the mean of the two, fails a perfect C2 box on 17.7% of Bournemouth frames) -- and
                        whose x-range overlaps theirs; its corners are scored on geometric slots 2 and 3 only; its box
                        is never scored.
          "ignore"      a prediction there is neither a true nor a false positive (Bournemouth C0, C1, T1).
          Absent: "score" for cls 0, "ignore" for any other class (a sacrum the keypoint detector never boxes).
  corners anatomical order = anterior-superior, anterior-inferior, posterior-inferior, posterior-superior
          (Bournemouth's points 1-4); geometric = spine-detector canonical slots. Whatever the declaration, truth and
          prediction are BOTH re-sorted through canonical_slots (a copy of spine-detector/src/manifest.py) and compared
          slot to slot -- never by index: the detector's keypoint order is not the truth's. Beside that primary
          reading, an ORDER-FREE one (`assigned`): the one-to-one pairing with the least summed distance. It exists
          because canonical_slots splits top from bottom by y, and on Bournemouth 11.5% of C3-C7 truth quads have the
          anterior wall as their two topmost points and 11.7% sit within 5 px of that split (measured 2026-09-26):
          there a few px of error hands a corner to the other endplate's slot and charges an error the size of a body
          edge. Both are reported, with how often they disagree. The declaration is read only to find the caudal pair
          and to name each truth corner anatomically.

MATCHING (per frame; the tools/carmlspine_eval.py cmd_score rule, for comparability with the paper): a prediction
matches a score truth when its centre lies inside the truth box and IoU >= 0.3, one to one, greedy by IoU. Secondary
arm: IoU >= 0.5 alone (the VOC rule). Then caudal_only truths match among the remaining predictions (greedy by the
inferior-edge distance). An unmatched prediction whose centre lies in an ignore box is dropped; every other
unmatched prediction is a false positive.

TEMPORAL (score --track): the tracker's confirmed hypotheses (a confirmed track with a detection on the frame) are
matched to the truth by the same rule, frame by frame. CLEAR-MOT: an identity switch is a gt_id whose matched track
id differs from the one of its previous matched frame; fragmentation counts tracked -> untracked -> tracked
interruptions per gt_id; MOTA = 1 - (FN + FP + IDSW) / GT. IDF1 = 2 IDTP / (GT + HYP), IDTP from a global
linear_sum_assignment over the track x gt_id co-match counts. Name stability: name switches per gt_id per 100 of its
matched frames, for the prototype's independent per-frame names and for the tracked names; it needs no naming truth.

    python tools/cine_eval.py track --pred <proto out> --meta <meta dir> --fps 15 --out <arm>/track.json
    python tools/cine_eval.py score --pred <proto out> --meta <meta dir> --track <arm>/track.json \
        --corpus-hint bournemouth --bins machine_angle --level-group primary=C3,C4,C5,C6 --out <arm>/score.json
    python tools/cine_eval.py video --pred <proto out> --track <arm>/track.json --meta <meta dir> \
        --images <root>/images --fps 15 --out <arm>/video
    python tools/cine_eval.py self-test [--out DIR]
"""
from __future__ import annotations

import argparse
import collections
import glob
import gzip
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eval_gate as EG  # noqa: E402
from carmlspine_eval import ORDER, iou  # noqa: E402  (ORDER: T13 = 19.5, L6 = 24.5; iou: the paper scorer's)
from fluorocap_anchor import LEVEL_ORDER, STD, decode as anchor_decode  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
TRACKER_CONFIG = REPO / "SchwingNet" / "results" / "cine" / "tracker_config.json"
ROLES = ("score", "caudal_only", "ignore")
FLIP_SLOT = (1, 0, 3, 2)             # geometric slot k of a frame is slot FLIP_SLOT[k] of the mirrored frame
# geometric slot -> anatomical corner, by facing (the image side the ANTERIOR wall is on). y points down.
SLOT_ANAT = {"L": ("anterior_superior", "posterior_superior", "posterior_inferior", "anterior_inferior"),
             "R": ("posterior_superior", "anterior_superior", "anterior_inferior", "posterior_inferior")}
ANAT_ORDER = ("anterior_superior", "anterior_inferior", "posterior_inferior", "posterior_superior")  # Bournemouth 1-4
MATCH_IOU, MATCH_IOU_SECONDARY, CAUDAL_TOL = 0.3, 0.5, 0.25
STEM_RE = r"^(?P<seq>.+?)_(?:f|sw|p)(?P<frame>\d+)$"     # HV01a_flex_f0000, case134_sw000, ctsp_0533_lat_p000

# The tracker's constants, exactly as plan 1b states them. The committed tracker_config.json is what `track` reads
# (its sha256 goes into every output); this copy is only the self-test's reference, and the self-test fails if the
# committed file says anything else.
TRACKER_DEFAULTS = {
    "tracker": "tools/cine_eval.py track/1",
    "iou_gate": 0.1,                           # a pair is admissible if IoU >= 0.1 ...
    "centre_gate_x_median_det_height": 0.5,    # ... or its centre distance <= 0.5 x the frame's median detection height
    "max_cost": 0.9,                           # and an assigned pair with cost 1 - IoU > 0.9 is rejected
    "velocity_ema_alpha": 0.5,                 # centre velocity: EMA of the observed displacement per frame
    "logp_memory_lambda": 0.9,                 # logp <- lambda * logp + log(posterior + eps): about 10 frames of memory
    "posterior_eps": 1e-6,
    "min_consecutive_hits": 2,                 # a tentative track is confirmed after 2 consecutive hits
    "tentative_dies_on_miss": True,            # a tentative track that misses a frame is dropped
    "max_age_s": 0.33,                         # a confirmed track dies after round(max_age_s x fps) consecutive misses
    "coast_dedupe_iou": 0.5,                   # a coasting track overlapping a detected one this much is not named
    "abstain_below": 0.5,                      # the prototype's abstain rule, on the pooled posterior
    "w_rare": 1.0,                             # fluorocap_anchor.decode(..., direction_known=True, w_rare=1.0)
    "direction_known": True,
}


# ================================================================================================ geometry
def canonical_slots(pts):
    """COPIED from spine-detector/src/manifest.py::canonical_slots (verified 2026-09-26), so the harness needs no
    pandas and cannot drift from a refactor there. Sort four corners into slot order by IMAGE GEOMETRY:

        slot 0 = superior, smaller x      slot 1 = superior, larger x
        slot 3 = inferior, smaller x      slot 2 = inferior, larger x

    y increases DOWNWARD, so superior = smaller y. The detector was trained on these slots (flip_idx [1, 0, 3, 2])."""
    p = np.asarray(pts, dtype=float).reshape(4, 2)
    top = p[np.argsort(p[:, 1])[:2]]
    bot = p[np.argsort(p[:, 1])[2:]]
    s0, s1 = top[np.argsort(top[:, 0])]
    s3, s2 = bot[np.argsort(bot[:, 0])]
    return np.array([s0, s1, s2, s3], dtype=float)


def _centre(b):
    return 0.5 * (b[0] + b[2]), 0.5 * (b[1] + b[3])


def _shift(b, v):
    return [b[0] + v[0], b[1] + v[1], b[2] + v[0], b[3] + v[1]]


def _inside(pt, b):
    return b[0] <= pt[0] <= b[2] and b[1] <= pt[1] <= b[3]


def _finite_box(b):
    return b is not None and len(b) == 4 and all(v is not None and math.isfinite(float(v)) for v in b)


def _softmax(lp):
    e = np.exp(lp - lp.max())
    return e / e.sum()


def _r(x, n=4):
    if x is None:
        return None
    x = float(x)
    return round(x, n) if math.isfinite(x) else None


def _stats(v, n=4):
    v = [float(x) for x in v if x is not None and math.isfinite(float(x))]
    if not v:
        return dict(n=0, mean=None, median=None)
    return dict(n=len(v), mean=_r(np.mean(v), n), median=_r(np.median(v), n))


# ================================================================================================ truth and calls
def prep_truth(meta):
    """The truth boxes of one frame, normalised: role, geometric slots, caudal pair, facing, endplate length."""
    order = meta.get("corner_order", "geometric")
    ex = meta.get("extras") or {}
    out = []
    for b in meta.get("boxes") or []:
        role = b.get("role") or ("score" if int(b.get("cls", 0)) == 0 else "ignore")
        if role not in ROLES:
            raise ValueError(f"cine_eval: {meta.get('stem')}: truth role {role!r} is not one of {ROLES}")
        if not _finite_box(b.get("box")):
            continue
        t = dict(gt_id=b.get("gt_id"), level=b.get("level"), role=role, box=[float(v) for v in b["box"]])
        # "anatomical" or "anatomical:AS,AI,PI,PS" (tools/polypose/cine_render.py); anything else is geometric
        bo = "anatomical" if str(b.get("corner_order") or order or "").startswith("anatomical") else "geometric"
        c = b.get("corners")
        q = None
        if c is not None:
            q = np.asarray(c, float).reshape(4, 2)
            if not np.isfinite(q).all():
                q = None
        if q is not None:
            t["slots"] = canonical_slots(q)
            s = t["slots"]
            t["endplate"] = 0.5 * (np.linalg.norm(s[1] - s[0]) + np.linalg.norm(s[2] - s[3]))
            t["q"], t["q_anat"] = (q, True) if bo == "anatomical" else (s, False)
            ys = np.sort(q[:, 1])
            t["split_margin"] = float(ys[2] - ys[1])     # how far the quad is from a top/bottom tie in canonical_slots
            if bo == "anatomical":
                t["facing_corners"] = "L" if q[[0, 1], 0].mean() < q[[2, 3], 0].mean() else "R"
        if role == "caudal_only":
            cp = b.get("caudal")
            if cp is not None:
                cp = np.asarray(cp, float).reshape(2, 2)
            elif q is not None:
                cp = q[[1, 2]] if bo == "anatomical" else t["slots"][[2, 3]]
            if cp is None or not np.isfinite(cp).all():
                raise ValueError(f"cine_eval: {meta.get('stem')}: caudal_only truth {t['gt_id']} has no caudal corners "
                                 "(`caudal`, or anatomical/geometric `corners`)")
            s2, s3 = (cp[0], cp[1]) if cp[0][0] >= cp[1][0] else (cp[1], cp[0])     # slot 2 larger x, slot 3 smaller
            t["caudal"] = np.array([s2, s3])
            t["endplate"] = float(np.linalg.norm(s2 - s3))
            for k in ("slots", "q", "q_anat", "split_margin"):
                t.pop(k, None)                         # the superior corners of a caudal-only truth are not truth
        t["facing"] = ex.get("facing") or t.get("facing_corners")
        out.append(t)
    return out


def prep_calls(rec):
    """The predicted vertebrae of one frame with their corners re-sorted into geometric slots."""
    out = []
    for v in (rec or {}).get("vertebrae") or []:
        c = dict(v)
        c["box"] = [float(x) for x in v["box"]]
        k = v.get("corners")
        if k is not None:
            q = np.asarray(k, float).reshape(4, 2)
            c["slots"] = canonical_slots(q) if np.isfinite(q).all() else None
        else:
            c["slots"] = None
        out.append(c)
    return out


def body_height(truth, fallback=None):
    hs = [t["box"][3] - t["box"][1] for t in truth if t["role"] == "score"]
    return float(np.median(hs)) if hs else fallback


def match_frame(truth, calls, *, iou_min=MATCH_IOU, centre_rule=True, body_h=None, caudal_tol=CAUDAL_TOL,
                caudal_ref="lower"):
    """One frame's matching. Returns dict(pairs=[(call i, truth j, 'box'|'caudal')], fp=[i], ignored=[i]).

    caudal_ref: where a caudal-only truth's inferior edge is. "lower" (default): the lower of its two caudal corners,
    which is the inferior edge of a min/max box of the true corners -- the detector's own box convention. "mean": the
    plan's wording, the mean y of the two. On Bournemouth C2 the caudal endplate drops a median 0.32 body heights
    across its width, and under "mean" a PERFECT C2 box (min/max of its own four points) fails the 0.25-body-height
    tolerance on 13,005 of 73,305 frames (17.7%); under "lower" on none (measured 2026-09-26)."""
    pairs = []
    for i, c in enumerate(calls):
        cc = _centre(c["box"])
        for j, t in enumerate(truth):
            if t["role"] != "score":
                continue
            if centre_rule and not _inside(cc, t["box"]):
                continue
            o = iou(c["box"], t["box"])
            if o >= iou_min:
                pairs.append((o, i, j))
    used_c, used_t, out = set(), set(), []
    for o, i, j in sorted(pairs, key=lambda p: (-p[0], p[1], p[2])):
        if i in used_c or j in used_t:
            continue
        used_c.add(i); used_t.add(j); out.append((i, j, "box"))
    cands = []
    for j, t in enumerate(truth):
        if t["role"] != "caudal_only":
            continue
        cp = t["caudal"]
        ym = max(cp[0][1], cp[1][1]) if caudal_ref == "lower" else 0.5 * (cp[0][1] + cp[1][1])
        xlo, xhi = min(cp[0][0], cp[1][0]), max(cp[0][0], cp[1][0])
        for i, c in enumerate(calls):
            if i in used_c:
                continue
            b = c["box"]
            h = body_h if body_h else (b[3] - b[1])
            dy = abs(b[3] - ym)
            if dy <= caudal_tol * h and b[0] <= xhi and b[2] >= xlo:
                cands.append((dy, i, j))
    for dy, i, j in sorted(cands):
        if i in used_c or j in used_t:
            continue
        used_c.add(i); used_t.add(j); out.append((i, j, "caudal"))
    fp, ign = [], []
    ig = [t["box"] for t in truth if t["role"] == "ignore"]
    for i, c in enumerate(calls):
        if i in used_c:
            continue
        (ign if any(_inside(_centre(c["box"]), b) for b in ig) else fp).append(i)
    return dict(pairs=out, fp=fp, ignored=ign)


def _within1(call, truth):
    return call in ORDER and truth in ORDER and abs(ORDER[call] - ORDER[truth]) <= 1


def eval_frame(stem, meta, rec, *, entries=None, seq_h=None, mm=None, caudal_ref="lower"):
    """(row, items, temporal) for one frame. entries: this frame's track.json entries (None: no tracker)."""
    truth = prep_truth(meta)
    calls = prep_calls(rec)
    bh = body_height(truth, seq_h)
    m = match_frame(truth, calls, body_h=bh, caudal_ref=caudal_ref)
    m50 = match_frame(truth, calls, iou_min=MATCH_IOU_SECONDARY, centre_rule=False, body_h=bh,
                      caudal_ref=caudal_ref)
    by_t = {j: (i, k) for i, j, k in m["pairs"]}
    t50 = {j for _, j, _ in m50["pairs"]}
    tr = {e["det_index"]: e for e in (entries or []) if e.get("det_index") is not None}
    px_mm = mm if mm is not None else meta.get("px_mm")
    items = []
    for j, t in enumerate(truth):
        if t["role"] == "ignore":
            continue
        it = dict(stem=stem, gt_id=t["gt_id"], level=t["level"], role=t["role"], matched=j in by_t, m50=j in t50)
        if px_mm:
            it["px_mm"] = float(px_mm)
        if j in by_t:
            i, kind = by_t[j]
            c = calls[i]
            it["det_index"] = i
            L = t.get("endplate")
            if t["role"] == "score":
                it["iou"] = iou(c["box"], t["box"])
                (cx, cy), (tx, ty) = _centre(c["box"]), _centre(t["box"])
                e = math.hypot(cx - tx, cy - ty)
                den = L if L else (t["box"][3] - t["box"][1])
                it["centre_px"] = e
                it["centre_rel"] = e / den if den else None
                it["centre_norm"] = "endplate" if L else "box_height"
            err = [None] * 4
            ass, anat = None, None
            if c.get("slots") is not None:
                if t["role"] == "score" and t.get("slots") is not None:
                    err = [float(v) for v in np.linalg.norm(c["slots"] - t["slots"], axis=1)]
                    # the ORDER-FREE reading beside the plan's slot-to-slot one: the one-to-one pairing of truth and
                    # predicted corners with the least summed distance. On a quad near a top/bottom tie in y
                    # (canonical_slots' split), a few px of error can hand a corner to the other endplate's slot and
                    # charge a body-edge-length error the prediction did not make; the pairing cannot.
                    D = np.linalg.norm(t["q"][:, None, :] - c["slots"][None, :, :], axis=2)
                    r_, c_ = linear_sum_assignment(D)
                    ass = [float(D[i_, j_]) for i_, j_ in zip(r_, c_)]               # in the truth's own order
                    if t["q_anat"]:
                        anat = dict(zip(ANAT_ORDER, ass))
                    elif t.get("facing") in SLOT_ANAT:
                        anat = dict(zip(SLOT_ANAT[t["facing"]], ass))
                    it["split_margin"] = t["split_margin"]
                elif t["role"] == "caudal_only":
                    err[2] = float(np.linalg.norm(c["slots"][2] - t["caudal"][0]))
                    err[3] = float(np.linalg.norm(c["slots"][3] - t["caudal"][1]))
                    D = np.linalg.norm(t["caudal"][:, None, :] - c["slots"][None, [2, 3], :], axis=2)
                    r_, c_ = linear_sum_assignment(D)
                    ass = [float(D[i_, j_]) for i_, j_ in zip(r_, c_)]
                    # t["caudal"] is [slot 2 (larger x), slot 3 (smaller x)]: anatomical through the facing
                    nm2 = (SLOT_ANAT[t["facing"]][2], SLOT_ANAT[t["facing"]][3]) if t.get("facing") in SLOT_ANAT \
                        else ("caudal_slot2", "caudal_slot3")
                    anat = dict(zip(nm2, ass))
            if any(e is not None for e in err):
                it["corner_px"] = err
                it["corner_rel"] = [(e / L if (e is not None and L) else None) for e in err]
                it["corner_assigned_px"] = ass
                it["corner_assigned_rel"] = [e / L for e in ass] if L else None
                it["slot_disagree"] = abs(sum(e for e in err if e is not None) - sum(ass)) > 1e-6
                if anat:
                    it["corner_anat"] = anat
            if t["level"]:
                call = c.get("level")
                it.update(call=call, abstain=bool(c.get("abstain")), single=c.get("single_crop"),
                          exact=call == t["level"], within1=_within1(call, t["level"]),
                          single_exact=c.get("single_crop") == t["level"])
                if entries is not None:
                    e = tr.get(i)
                    ok = bool(e and e.get("confirmed") and e.get("name_tracked"))
                    it["tcall"] = e.get("name_tracked") if ok else None
                    it["tabstain"] = bool(e.get("abstain")) if ok else True
                    it["texact"] = ok and e.get("name_tracked") == t["level"]
                    it["twithin1"] = ok and _within1(e.get("name_tracked"), t["level"])
        items.append(it)
    ns = sum(1 for t in truth if t["role"] == "score")
    row = dict(stem=stem, case=meta.get("case"), seq=meta.get("seq"), frame=meta.get("frame"), n_truth=ns,
               n_caudal=sum(1 for t in truth if t["role"] == "caudal_only"), n_calls=len(calls),
               tp=len(m["pairs"]), fp=len(m["fp"]), ignored=len(m["ignored"]),
               fn=sum(1 for it in items if not it["matched"]), tp50=len(m50["pairs"]), fp50=len(m50["fp"]))
    if rec is not None and rec.get("error"):
        row["pred_error"] = True
    tmp = None
    if entries is not None:
        # CLEAR-MOT: the confirmed hypotheses of this frame, matched to the truth by the same rule
        hyps = [e for e in entries if e.get("confirmed") and e.get("det_index") is not None]
        hm = match_frame(truth, [dict(box=[float(v) for v in e["box"]]) for e in hyps], body_h=bh,
                         caudal_ref=caudal_ref)
        gt_tid = {}
        for i, j, _ in hm["pairs"]:
            gt_tid[j] = hyps[i]
        tmp = dict(gts=[], fp=len(hm["fp"]), hyp=len(hyps) - len(hm["ignored"]))
        for j, t in enumerate(truth):
            if t["role"] == "ignore":
                continue
            if t["gt_id"] is None:
                raise ValueError(f"cine_eval: {stem}: a truth box has no gt_id; score --track needs one per body")
            h = gt_tid.get(j)
            ind = calls[by_t[j][0]].get("level") if j in by_t else None
            ind_ab = bool(calls[by_t[j][0]].get("abstain")) if j in by_t else None
            tmp["gts"].append(dict(gt_id=t["gt_id"], level=t["level"], tid=(h["track_id"] if h else None),
                                   tname=(h.get("name_tracked") if h else None),
                                   tab=(bool(h.get("abstain")) if h else None), iname=ind, iab=ind_ab))
    return row, items, tmp


# ================================================================================================ summaries
def summarise(items, rows=None):
    sc = [x for x in items if x["role"] == "score"]
    ca = [x for x in items if x["role"] == "caudal_only"]
    ms = [x for x in sc if x["matched"]]
    s = dict(truth=len(sc), matched=len(ms), recall=_r(len(ms) / len(sc)) if sc else None,
             recall_iou50=_r(sum(x["m50"] for x in sc) / len(sc)) if sc else None,
             caudal_truth=len(ca), caudal_matched=sum(x["matched"] for x in ca),
             caudal_recall=_r(sum(x["matched"] for x in ca) / len(ca)) if ca else None)
    if rows is not None:
        tp = sum(r["tp"] for r in rows); fp = sum(r["fp"] for r in rows)
        tp50 = sum(r["tp50"] for r in rows); fp50 = sum(r["fp50"] for r in rows)
        s.update(frames=len(rows), calls=sum(r["n_calls"] for r in rows), tp=tp, fp=fp,
                 ignored=sum(r["ignored"] for r in rows), precision=_r(tp / (tp + fp)) if tp + fp else None,
                 tp_iou50=tp50, fp_iou50=fp50, precision_iou50=_r(tp50 / (tp50 + fp50)) if tp50 + fp50 else None,
                 pred_errors=sum(1 for r in rows if r.get("pred_error")))
    s["iou"] = _stats([x.get("iou") for x in ms])
    s["centre_px"] = _stats([x.get("centre_px") for x in ms])
    s["centre_rel"] = _stats([x.get("centre_rel") for x in ms])
    s["centre_rel_normaliser"] = dict(collections.Counter(x.get("centre_norm") for x in ms if x.get("centre_norm")))
    wc = [x for x in items if x.get("corner_px")]
    corner = {}
    for k in range(4):
        px = [x["corner_px"][k] for x in wc if x["corner_px"][k] is not None]
        rel = [x["corner_rel"][k] for x in wc if x["corner_rel"][k] is not None]
        mmv = [x["corner_px"][k] * x["px_mm"] for x in wc if x["corner_px"][k] is not None and x.get("px_mm")]
        corner[f"slot{k}"] = dict(px=_stats(px), rel=_stats(rel), **({"mm": _stats(mmv)} if mmv else {}))
    allpx = [e for x in wc for e in x["corner_px"] if e is not None]
    allrel = [e for x in wc for e in x["corner_rel"] if e is not None]
    corner["all"] = dict(px=_stats(allpx), rel=_stats(allrel))
    corner["assigned"] = dict(px=_stats([e for x in wc for e in (x.get("corner_assigned_px") or [])]),
                              rel=_stats([e for x in wc for e in (x.get("corner_assigned_rel") or [])]))
    dis = sum(1 for x in wc if x.get("slot_disagree"))
    corner["slot_vs_assignment_disagree"] = dict(n=dis, of=len(wc), share=_r(dis / len(wc)) if wc else None)
    sm = [x["split_margin"] for x in wc if x.get("split_margin") is not None]
    corner["truth_split_margin_px"] = dict(**_stats(sm), lt_5px_share=_r(np.mean(np.asarray(sm) < 5)) if sm else None)
    anat = collections.defaultdict(list)
    for x in wc:
        for nm, e in (x.get("corner_anat") or {}).items():
            anat[nm].append(e)
    corner["anatomical_px"] = {nm: _stats(v) for nm, v in sorted(anat.items())}
    corner["anatomical_from"] = ("the order-free pairing: each truth corner, named by the truth's anatomical order "
                                 "(or by its geometric slot and the sequence's facing), with the predicted corner it "
                                 "pairs with")
    s["corners"] = corner
    named = [x for x in items if x["matched"] and x.get("level") and "call" in x]
    ans = [x for x in named if not x["abstain"]]
    s.update(named=len(named), exact=_r(np.mean([x["exact"] for x in named])) if named else None,
             within1=_r(np.mean([x["within1"] for x in named])) if named else None,
             single_crop_exact=_r(np.mean([x["single_exact"] for x in named])) if named else None,
             answered=_r(len(ans) / len(named)) if named else None,
             abstain_rate=_r(1 - len(ans) / len(named)) if named else None,
             exact_answered=_r(np.mean([x["exact"] for x in ans])) if ans else None)
    fr = collections.defaultdict(list)
    for x in named:
        fr[x["stem"]].append(x["exact"])
    s["frame_exact"] = _r(np.mean([all(v) for v in fr.values()])) if fr else None
    if any("tcall" in x for x in named):
        tn = [x for x in named if "tcall" in x]
        tans = [x for x in tn if x["tcall"] and not x["tabstain"]]
        tfr = collections.defaultdict(list)
        for x in tn:
            tfr[x["stem"]].append(x["texact"])
        s["tracked_naming"] = dict(
            named=len(tn), confirmed=sum(1 for x in tn if x["tcall"]),
            exact=_r(np.mean([x["texact"] for x in tn])), within1=_r(np.mean([x["twithin1"] for x in tn])),
            answered=_r(len(tans) / len(tn)), exact_answered=_r(np.mean([x["texact"] for x in tans])) if tans else None,
            frame_exact=_r(np.mean([all(v) for v in tfr.values()])) if tfr else None,
            note="tracked names on the same matched detections; a detection with no confirmed track counts as "
                 "unanswered and not exact")
    return s


def temporal(frames_tmp, groups=None):
    """CLEAR-MOT, IDF1 and name stability over [(seq, frame, tmp)] in frame order within each sequence."""
    from scipy.optimize import linear_sum_assignment
    per_gt = collections.defaultdict(list)            # (seq, gt) -> [(frame, tid, level, iname, iab, tname, tab)]
    fp = collections.Counter(); hyp = collections.Counter()
    for seq, fr, tmp in frames_tmp:
        fp[seq] += tmp["fp"]; hyp[seq] += tmp["hyp"]
        for g in tmp["gts"]:
            per_gt[(seq, g["gt_id"])].append((fr, g["tid"], g["level"], g["iname"], g["iab"], g["tname"], g["tab"]))
    rows = {}
    for key, obs in per_gt.items():
        obs.sort(key=lambda o: o[0])
        idsw = 0; last = None; segs = 0; prev_tracked = False
        for o in obs:
            tracked = o[1] is not None
            if tracked:
                if last is not None and o[1] != last:
                    idsw += 1
                last = o[1]
                if not prev_tracked:
                    segs += 1
            prev_tracked = tracked

        def switches(names):
            n = [x for x in names if x is not None]
            return sum(1 for a, b in zip(n[:-1], n[1:]) if a != b), len(n)
        si, ni = switches([o[3] for o in obs])
        sia, nia = switches([o[3] for o in obs if o[3] is not None and not o[4]])
        st, nt = switches([o[5] for o in obs])
        sta, nta = switches([o[5] for o in obs if o[5] is not None and not o[6]])
        rows[key] = dict(gt=len(obs), fn=sum(1 for o in obs if o[1] is None), idsw=idsw, frag=max(0, segs - 1),
                         level=next((o[2] for o in obs if o[2]), None),
                         ind_sw=si, ind_n=ni, ind_sw_ans=sia, ind_n_ans=nia,
                         trk_sw=st, trk_n=nt, trk_sw_ans=sta, trk_n_ans=nta)
    idtp = collections.Counter()
    for seq in sorted({k[0] for k in per_gt}):
        gts = sorted({k[1] for k in per_gt if k[0] == seq}, key=str)
        co = collections.Counter()
        for g in gts:
            for o in per_gt[(seq, g)]:
                if o[1] is not None:
                    co[(g, o[1])] += 1
        tids = sorted({t for (_, t) in co}, key=str)
        if gts and tids:
            M = np.zeros((len(gts), len(tids)))
            gi = {g: i for i, g in enumerate(gts)}; ti = {t: i for i, t in enumerate(tids)}
            for (g, t), n in co.items():
                M[gi[g], ti[t]] = n
            r, c = linear_sum_assignment(-M)
            idtp[seq] = int(M[r, c].sum())

    def agg(keys, seqs, with_fp=True):
        R = [rows[k] for k in keys]
        GT = sum(r["gt"] for r in R); FN = sum(r["fn"] for r in R); SW = sum(r["idsw"] for r in R)
        out = dict(gt=GT, fn=FN, idsw=SW, frag=sum(r["frag"] for r in R), gt_ids=len(R))

        def per100(sw, n):
            return _r(100.0 * sw / n) if n else None
        out["name_stability"] = dict(
            independent=dict(switches=sum(r["ind_sw"] for r in R), frames=sum(r["ind_n"] for r in R),
                             per_100=per100(sum(r["ind_sw"] for r in R), sum(r["ind_n"] for r in R)),
                             answered_switches=sum(r["ind_sw_ans"] for r in R),
                             answered_frames=sum(r["ind_n_ans"] for r in R),
                             answered_per_100=per100(sum(r["ind_sw_ans"] for r in R), sum(r["ind_n_ans"] for r in R))),
            tracked=dict(switches=sum(r["trk_sw"] for r in R), frames=sum(r["trk_n"] for r in R),
                         per_100=per100(sum(r["trk_sw"] for r in R), sum(r["trk_n"] for r in R)),
                         answered_switches=sum(r["trk_sw_ans"] for r in R),
                         answered_frames=sum(r["trk_n_ans"] for r in R),
                         answered_per_100=per100(sum(r["trk_sw_ans"] for r in R), sum(r["trk_n_ans"] for r in R))))
        if with_fp:
            FP = sum(fp[s] for s in seqs); HYP = sum(hyp[s] for s in seqs); IDTP = sum(idtp[s] for s in seqs)
            out.update(fp=FP, hyp=HYP, mota=_r(1 - (FN + FP + SW) / GT) if GT else None, idtp=IDTP,
                       idfp=HYP - IDTP, idfn=GT - IDTP, idf1=_r(2 * IDTP / (GT + HYP)) if GT + HYP else None)
        return out
    seqs = sorted({k[0] for k in per_gt})
    res = dict(overall=agg(list(rows), seqs))
    res["per_sequence"] = {s: agg([k for k in rows if k[0] == s], [s]) for s in seqs}
    lv = collections.defaultdict(list)
    for k, r in rows.items():
        lv[r["level"] or f"id:{k[1]}"].append(k)
    res["per_level"] = {l: agg(ks, seqs, with_fp=False)
                        for l, ks in sorted(lv.items(), key=lambda kv: ORDER.get(kv[0], 99))}
    for name, levels in (groups or {}).items():
        ks = [k for k, r in rows.items() if r["level"] in levels]
        if ks:
            res.setdefault("groups", {})[name] = agg(ks, seqs, with_fp=False)
    res["note"] = ("FP, MOTA and IDF1 are over every hypothesis and so are reported overall and per sequence only; a "
                   "per-level or per-group block has no false positives to count")
    return res


def parse_bins(specs):
    out = []
    for s in specs or []:
        name, _, edges = s.partition(":")
        out.append((name, [float(x) for x in edges.split(",")] if edges else None))
    return out


def bin_value(meta, name):
    ex = meta.get("extras") or {}
    for k in (name, f"{name}_deg"):
        for src in (ex, meta):
            v = src.get(k)
            if isinstance(v, (int, float)) and math.isfinite(float(v)):
                return float(v)
    return None


def bin_label(v, edges, width=10.0):
    if v is None:
        return "none"
    if edges is None:
        lo = math.floor(v / width) * width
        return f"[{lo:g},{lo + width:g})"
    if v < edges[0]:
        return f"<{edges[0]:g}"
    for a, b in zip(edges[:-1], edges[1:]):
        if a <= v < b:
            return f"[{a:g},{b:g})"
    return f">={edges[-1]:g}"


def evaluate(frames, *, track=None, mm=None, groups=None, bins=None, caudal_ref="lower"):
    """frames: [(stem, meta, rec)] (rec None when the frame was never predicted: every truth a miss). track:
    {stem: entries} or None. Returns (result, rows, items)."""
    seq_h = collections.defaultdict(list)
    for stem, meta, rec in frames:
        h = body_height(prep_truth(meta))
        if h:
            seq_h[meta.get("seq")].append(h)
    seq_h = {s: float(np.median(v)) for s, v in seq_h.items()}
    rows, items, ftmp = [], [], []
    for stem, meta, rec in frames:
        ent = None
        if track is not None:
            ent = track.get(stem, [])
        row, it, tmp = eval_frame(stem, meta, rec, entries=ent, seq_h=seq_h.get(meta.get("seq")), mm=mm,
                                  caudal_ref=caudal_ref)
        row["bins"] = {n: bin_label(bin_value(meta, n), e) for n, e in (bins or [])}
        rows.append(row); items += it
        if tmp is not None:
            ftmp.append((meta.get("seq"), meta.get("frame"), tmp))
    res = dict(overall=summarise(items, rows))
    lv = collections.defaultdict(list)
    for x in items:
        lv[x["level"] or f"id:{x['gt_id']}"].append(x)
    res["per_level"] = {l: summarise(v) for l, v in sorted(lv.items(), key=lambda kv: ORDER.get(kv[0], 99))}
    if groups:
        res["groups"] = {g: summarise([x for x in items if x["level"] in ls]) for g, ls in groups.items()}
    if bins:
        res["bins"] = {}
        by_stem = collections.defaultdict(list)
        for x in items:
            by_stem[x["stem"]].append(x)
        for n, _ in bins:
            lab = collections.defaultdict(list)
            for r in rows:
                lab[r["bins"][n]].append(r)
            res["bins"][n] = {}
            for b in sorted(lab, key=lambda s: (s == "none", _bin_key(s))):
                R = lab[b]
                X = [x for r in R for x in by_stem[r["stem"]]]
                blk = summarise(X, R)
                blk["per_level"] = {l: {k: summarise([x for x in X if x["level"] == l])[k]
                                        for k in ("truth", "recall", "exact", "within1", "answered")}
                                    for l in sorted({x["level"] for x in X if x["level"]}, key=lambda l: ORDER.get(l, 99))}
                res["bins"][n][b] = blk
    conf = collections.Counter((x["level"], x["call"]) for x in items if "call" in x)
    res["confusion"] = [dict(truth=t, call=c, n=n) for (t, c), n in
                        sorted(conf.items(), key=lambda kv: (ORDER.get(kv[0][0], 99), -kv[1]))]
    if track is not None:
        res["temporal"] = temporal(ftmp, groups)
    return res, rows, items


def _bin_key(s):
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    return (float(m.group(0)) if m else 0.0) + (-0.5 if s.startswith("<") else 0.5 if s.startswith(">") else 0)


# ================================================================================================ inputs
def pred_dirs(root):
    root = Path(os.path.expanduser(str(root)))
    if (root / "prototype_meta.json").exists():
        return [root]
    ds = sorted(p.parent for p in root.glob("*/prototype_meta.json"))
    if not ds:
        raise SystemExit(f"cine_eval: {root}: no prototype_meta.json in it or one level down; not a "
                         "tools/level_prototype.py output")
    return ds


def load_pred_dir(d):
    d = Path(d)
    meta = json.load(open(d / "prototype_meta.json", encoding="utf-8"))
    rp = d / "prototype_results.json"
    if rp.exists():
        recs = json.load(open(rp, encoding="utf-8"))
    else:          # a run that stopped before its summary: its per-image records
        recs = [json.load(open(f, encoding="utf-8")) for f in sorted(d.glob("*.json"))
                if not f.name.startswith("prototype_")]
    out = {}
    for r in recs:
        img = r.get("image") if isinstance(r, dict) else None
        if not img:
            continue
        stem = Path(str(img).replace("\\", "/")).stem
        if stem in out:
            raise SystemExit(f"cine_eval: {d}: image stem {stem} twice in one prototype run")
        out[stem] = r
    return meta, out


def load_preds(root):
    """([(dir, prototype_meta, {stem: rec})], {stem: rec}) over every prototype run under root."""
    runs, merged = [], {}
    for d in pred_dirs(root):
        meta, recs = load_pred_dir(d)
        dup = sorted(set(recs) & set(merged))
        if dup:
            raise SystemExit(f"cine_eval: stem {dup[0]} (and {len(dup) - 1} more) predicted by two runs under {root}")
        runs.append((d, meta, recs)); merged.update(recs)
    return runs, merged


def pred_digest(merged):
    h = hashlib.sha256()
    for stem in sorted(merged):
        h.update(json.dumps([stem, [v.get("box") for v in merged[stem].get("vertebrae") or []]]).encode())
    return "sha256:" + h.hexdigest()


def meta_stems(meta_dir):
    """{stem: path} of every truth meta (file names only: nothing is read)."""
    out = {Path(p).stem: p for p in glob.glob(os.path.join(os.path.expanduser(str(meta_dir)), "*.json"))}
    if not out:
        raise SystemExit(f"cine_eval: {meta_dir}: no truth metas")
    return out


def load_metas(meta_dir, want=None):
    """{stem: meta}; with `want`, only those stems are read (73,305 Bournemouth metas are not read to score four
    sequences). A meta whose own `stem` differs from its file name is refused: stems are the join key."""
    out = {}
    for stem, p in sorted(meta_stems(meta_dir).items()):
        if want is not None and stem not in want:
            continue
        m = json.load(open(p, encoding="utf-8"))
        if m.get("stem") not in (None, stem):
            raise SystemExit(f"cine_eval: {p}: its stem field {m.get('stem')!r} is not its file name")
        out[stem] = m
    return out


def seq_frame(stem, metas, rx):
    m = metas.get(stem) if metas else None
    if m is not None and m.get("seq") is not None and m.get("frame") is not None:
        return str(m["seq"]), int(m["frame"])
    mm = rx.match(stem)
    if not mm:
        return None
    return mm.group("seq"), int(mm.group("frame"))


def load_track(p):
    T = json.load(open(os.path.expanduser(str(p)), encoding="utf-8"))
    by = {}
    for seq, S in T["sequences"].items():
        for f in S["frames"]:
            by[f["stem"]] = f["tracks"]
    return T, by


def parse_groups(specs):
    g = {}
    for s in specs or []:
        name, _, levels = s.partition("=")
        if not name or not levels:
            raise SystemExit(f"--level-group {s!r}: expected NAME=L1,L2,...")
        g[name] = [x.strip() for x in levels.split(",") if x.strip()]
    return g


# ================================================================================================ score
RULES = dict(
    primary="prediction centre inside the truth box and IoU >= 0.3, one to one, greedy by IoU "
            "(tools/carmlspine_eval.py cmd_score)",
    secondary="IoU >= 0.5, one to one, greedy by IoU (no centre rule)",
    caudal_only="predicted inferior edge within 0.25 x the frame's median body height (score truths; else the "
                "sequence's) of the caudal truth's inferior edge, x-ranges overlapping; one to one, greedy by that "
                "distance, after the primary matches. The inferior edge is the LOWER caudal corner under "
                "--caudal-ref lower (the default, recorded as `caudal_ref`): the edge a min/max box of the true corners "
                "has. `mean` is the plan's wording (the mean y of the two corners), under which a perfect C2 box fails "
                "on 17.7% of Bournemouth C2 frames, because the caudal endplate drops a median 0.32 body heights across "
                "its width. Corners scored on geometric slots 2 and 3 only; the box is never scored",
    ignore="an unmatched prediction whose centre lies in an ignore box is dropped: neither true nor false positive",
    corners="PRIMARY (plan 1b): truth and prediction both re-sorted through canonical_slots (spine-detector "
            "manifest.py) and compared slot to slot. BESIDE IT (`assigned`): the one-to-one pairing of truth and "
            "predicted corners with the least summed distance (scipy linear_sum_assignment), which a near-tie in "
            "canonical_slots' top/bottom split cannot flip; `slot_vs_assignment_disagree` counts the bodies where the "
            "two differ and `truth_split_margin_px` how close the truth quads sit to that tie. Anatomical names from "
            "the pairing. Normalised by the truth endplate length (mean of the superior and inferior endplates; the "
            "inferior one for a caudal-only truth)",
    centre="predicted box centre to truth box centre, normalised by the truth endplate length, or the truth box "
           "height when the truth has no corners",
    naming="exact / within one (tools/carmlspine_eval.ORDER: T13 = 19.5, L6 = 24.5) on matched truths with a level; "
           "answered = not abstained",
    temporal="confirmed track hypotheses matched by the primary rule; CLEAR-MOT IDSW, fragmentation, "
             "MOTA = 1 - (FN + FP + IDSW) / GT; IDF1 = 2 IDTP / (GT + HYP) with IDTP from a linear_sum_assignment "
             "over track x gt_id co-matches; name switches per gt_id per 100 matched frames")


def cmd_score(a):
    if not a.pred or not a.meta or not a.out:
        raise SystemExit("score needs --pred, --meta and --out")
    if not a.corpus_hint:
        raise SystemExit("score needs --corpus-hint: the corpus the scored cases key in (tools/patient_keys.key_any), "
                         "e.g. bournemouth, carmlspine, ctsp")
    runs, merged = load_preds(a.pred)
    names = meta_stems(a.meta)
    unpred = sorted(set(names) - set(merged))
    metas = load_metas(a.meta, None if a.allow_unpredicted else set(merged))
    stems = sorted(set(merged) & set(metas))
    if not stems:
        raise SystemExit(f"cine_eval: no frame has both a prediction under {a.pred} and a truth meta in {a.meta}")
    if unpred and not a.allow_unpredicted:
        print(f"cine_eval: {len(unpred)} truth frames have no prediction (e.g. {unpred[:3]}); they are left out. "
              "Pass --allow-unpredicted to score them as misses instead.", flush=True)
    # THE GATE, before anything is scored: each prototype run's verdict, carried over the frames scored from it
    blocks = []
    for d, _, recs in runs:
        its = [dict(case=metas[s].get("case"), stem=s, hint=a.corpus_hint) for s in stems if s in recs]
        if its:
            blocks.append(EG.carry_proto(d, "tools/cine_eval.py score", not_held_out=a.not_held_out,
                                         touched=a.touched, items=its))
    gate = blocks[0] if len(blocks) == 1 else EG.merge(blocks)
    track = trk = None
    if a.track:
        trk, track = load_track(a.track)
        dg = pred_digest(merged)
        if trk.get("pred_digest") != dg:
            raise SystemExit(f"cine_eval: {a.track} was made from other predictions (pred_digest "
                             f"{trk.get('pred_digest')}) than {a.pred} ({dg}); re-run track")
    frames = [(s, metas[s], merged.get(s)) for s in stems]
    if a.allow_unpredicted:
        frames += [(s, metas[s], None) for s in unpred]
    frames.sort(key=lambda f: (str(f[1].get("seq")), f[1].get("frame") if f[1].get("frame") is not None else -1, f[0]))
    groups = parse_groups(a.level_group)
    bins = parse_bins(a.bins)
    res, rows, items = evaluate(frames, track=track, mm=a.mm_per_px, groups=groups, bins=bins, caudal_ref=a.caudal_ref)
    for r in rows:
        r["hint"] = a.corpus_hint
        if not bins:
            r.pop("bins", None)
    out = Path(os.path.expanduser(a.out))
    out.parent.mkdir(parents=True, exist_ok=True)
    items_p = out.with_name(out.stem + "_items.jsonl.gz")
    body = dict(tool="tools/cine_eval.py score", tag=a.tag, pred=str(a.pred), meta=str(a.meta), corpus_hint=a.corpus_hint,
                track=str(a.track) if a.track else None,
                tracker_config_sha256=(trk or {}).get("config_sha256"), tracker_config=(trk or {}).get("config"),
                mm_per_px=a.mm_per_px, caudal_ref=a.caudal_ref, rules=RULES, level_groups=groups,
                bin_specs=[dict(name=n, edges=e) for n, e in bins],
                n_frames_scored=len(rows), n_truth_frames_unpredicted=len(unpred),
                unpredicted_frames_scored_as_misses=bool(a.allow_unpredicted),
                n_pred_frames_without_truth=len(set(merged) - set(names)), items_file=items_p.name, **res,
                frames=[{k: v for k, v in r.items()} for r in rows])
    res_out = EG.stamp(body, gate)
    json.dump(res_out, open(out, "w", encoding="utf-8"), indent=1, default=_json_default)
    with gzip.open(items_p, "wt", encoding="utf-8") as f:
        for x in items:
            f.write(json.dumps({k: v for k, v in x.items()}, default=_json_default) + "\n")
    o = res["overall"]
    print(f"cine_eval score: {len(rows)} frames, truth {o['truth']}, recall {o['recall']}, precision {o['precision']}, "
          f"FP {o['fp']}, IoU median {o['iou']['median']}, corner px median {o['corners']['all']['px']['median']}, "
          f"exact {o['exact']}, answered {o['answered']}", flush=True)
    if "temporal" in res:
        t = res["temporal"]["overall"]
        print(f"  temporal: GT {t['gt']}, FN {t['fn']}, FP {t['fp']}, IDSW {t['idsw']}, frag {t['frag']}, "
              f"MOTA {t['mota']}, IDF1 {t['idf1']}, name switches/100 independent "
              f"{t['name_stability']['independent']['per_100']} tracked {t['name_stability']['tracked']['per_100']}")
    print(f"  held_out={res_out['eval_gate'].get('held_out')} -> {out}", flush=True)
    return 0


def _json_default(o):
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.bool_,)):
        return bool(o)
    raise TypeError(type(o))


# ================================================================================================ track
def load_tracker_config(path=None):
    p = Path(os.path.expanduser(str(path))) if path else TRACKER_CONFIG
    if not p.exists():
        raise SystemExit(f"cine_eval track: {p} does not exist. The tracker's constants are an input fixed before "
                         "any Bournemouth frame is seen (plan 1b); commit tracker_config.json, do not run on defaults.")
    raw = p.read_bytes()
    cfg = json.loads(raw.decode("utf-8"))
    miss = [k for k in TRACKER_DEFAULTS if k not in cfg]
    if miss:
        raise SystemExit(f"cine_eval track: {p} lacks {miss}")
    return cfg, "sha256:" + hashlib.sha256(raw).hexdigest(), str(p)


class Tracker:
    """Online and causal: frame t is associated, updated and named from frames <= t only."""

    def __init__(self, cfg, fps, level_order=LEVEL_ORDER):
        self.c = cfg
        self.K = len(level_order)
        self.order = list(level_order)
        self.max_age = max(1, int(round(float(cfg["max_age_s"]) * float(fps))))
        self.tracks = []
        self.next_id = 1

    def _new(self, d):
        c = self.c
        t = dict(id=self.next_id, box=list(d["box"]), corners=d.get("corners"), v=np.zeros(2), hits=1, streak=1,
                 misses=0, logp=np.log(np.asarray(d["posterior"], float) + c["posterior_eps"]))
        t["confirmed"] = t["streak"] >= c["min_consecutive_hits"]
        self.next_id += 1
        return t

    def step(self, dets):
        """dets: [{box, corners, posterior, level, abstain, level_prob}] for one frame. Returns the frame's entries."""
        from scipy.optimize import linear_sum_assignment
        c = self.c
        for d in dets:
            p = d.get("posterior")
            if p is None or len(p) != self.K:
                raise SystemExit("cine_eval track: a detection has no posterior over meta.level_order; run "
                                 "tools/level_prototype.py with --dump-posterior")
        for t in self.tracks:
            t["pred"] = _shift(t["box"], t["v"] * (t["misses"] + 1))
        BIG = 1e6
        pairs = []
        if self.tracks and dets:
            h = float(np.median([d["box"][3] - d["box"][1] for d in dets]))
            cost = np.full((len(self.tracks), len(dets)), BIG)
            for i, t in enumerate(self.tracks):
                pc = _centre(t["pred"])
                for j, d in enumerate(dets):
                    o = iou(t["pred"], d["box"])
                    dc = _centre(d["box"])
                    gated = o >= c["iou_gate"] or math.hypot(pc[0] - dc[0], pc[1] - dc[1]) <= \
                        c["centre_gate_x_median_det_height"] * h
                    if gated and (1.0 - o) <= c["max_cost"]:
                        cost[i, j] = 1.0 - o
            r, cc = linear_sum_assignment(cost)
            pairs = [(i, j) for i, j in zip(r, cc) if cost[i, j] < BIG]
        mt = {i: j for i, j in pairs}
        md = {j: i for i, j in pairs}
        a, lam, eps = c["velocity_ema_alpha"], c["logp_memory_lambda"], c["posterior_eps"]
        keep, det_track = [], {}
        for i, t in enumerate(self.tracks):
            if i in mt:
                d = dets[mt[i]]
                dt = t["misses"] + 1
                c0, c1 = _centre(t["box"]), _centre(d["box"])
                vobs = np.array([(c1[0] - c0[0]) / dt, (c1[1] - c0[1]) / dt])
                t["v"] = a * vobs + (1 - a) * t["v"]
                t["box"] = list(d["box"]); t["corners"] = d.get("corners")
                t["logp"] = lam * t["logp"] + np.log(np.asarray(d["posterior"], float) + eps)
                t["hits"] += 1; t["streak"] += 1; t["misses"] = 0
                if t["streak"] >= c["min_consecutive_hits"]:
                    t["confirmed"] = True
                keep.append(t); det_track[mt[i]] = t
                continue
            t["misses"] += 1; t["streak"] = 0
            if not t["confirmed"] and c["tentative_dies_on_miss"]:
                continue
            if t["misses"] >= self.max_age:
                continue
            keep.append(t)
        for j, d in enumerate(dets):
            if j not in md:
                t = self._new(d)
                keep.append(t); det_track[j] = t
        self.tracks = keep
        # NAMING: every confirmed track, detected or coasting, sorted by y; the pooled posterior decoded as one run
        live = [t for t in self.tracks if t["confirmed"]]
        seen = [t["box"] for t in live if t["misses"] == 0]
        named = []
        for t in live:
            if t["misses"] == 0:
                named.append((t, t["box"]))
            else:
                pb = _shift(t["box"], t["v"] * t["misses"])
                if any(iou(pb, b) >= c["coast_dedupe_iou"] for b in seen):
                    continue
                named.append((t, pb))
        named.sort(key=lambda x: 0.5 * (x[1][1] + x[1][3]))
        nm = {}
        if named:
            P = np.stack([_softmax(t["logp"]) for t, _ in named])
            dec = anchor_decode(P, set(), {}, None, direction_known=bool(c["direction_known"]), w_rare=float(c["w_rare"]))
            names = dec.get("anchored_pred") or [self.order[int(k)] for k in P.argmax(1)]
            for (t, b), n, p in zip(named, names, P):
                k = self.order.index(n) if n in self.order else None
                pk = float(p[k]) if k is not None else 0.0
                nm[t["id"]] = (n, pk, bool(n != self.order[int(p.argmax())] or pk < c["abstain_below"]), b)
        out = []
        for j, d in enumerate(dets):
            t = det_track[j]
            n = nm.get(t["id"])
            out.append(dict(track_id=t["id"], det_index=j, box=[round(float(v), 2) for v in d["box"]],
                            confirmed=bool(t["confirmed"]), name_indep=d.get("level"),
                            abstain_indep=bool(d.get("abstain")),
                            name_tracked=n[0] if n else None, p=round(n[1], 4) if n else None,
                            abstain=n[2] if n else None))
        for t, _ in named:
            if t["misses"] > 0:
                n = nm[t["id"]]
                out.append(dict(track_id=t["id"], det_index=None, box=[round(float(v), 2) for v in n[3]],
                                confirmed=True, coasting=True, name_indep=None, abstain_indep=None,
                                name_tracked=n[0], p=round(n[1], 4), abstain=n[2]))
        return out


def run_tracker(seq_frames, cfg, fps, level_order=LEVEL_ORDER):
    """seq_frames: [(frame index, stem, rec or None)] of one sequence. A missing frame index (no record) is a frame
    with no detections: time passed. Returns [{stem, frame, tracks}] in frame order."""
    tr = Tracker(cfg, fps, level_order)
    by = {f: (s, r) for f, s, r in seq_frames}
    out = []
    lo, hi = min(by), max(by)
    for f in range(lo, hi + 1):
        stem, rec = by.get(f, (None, None))
        dets = []
        for v in (rec or {}).get("vertebrae") or []:
            dets.append(dict(box=[float(x) for x in v["box"]], corners=v.get("corners"), posterior=v.get("posterior"),
                             level=v.get("level"), abstain=v.get("abstain"), level_prob=v.get("level_prob")))
        ent = tr.step(dets)
        if stem is not None:
            out.append(dict(stem=stem, frame=f, tracks=ent))
    return out


def track_summary(frames):
    per = collections.defaultdict(list)
    for fr in frames:
        for e in fr["tracks"]:
            if e.get("confirmed") and e.get("det_index") is not None:
                per[e["track_id"]].append((e.get("name_tracked"), e.get("name_indep")))
    sw_t = sum(sum(1 for a, b in zip(v[:-1], v[1:]) if a[0] != b[0]) for v in per.values())
    sw_i = sum(sum(1 for a, b in zip(v[:-1], v[1:]) if a[1] != b[1]) for v in per.values())
    n = sum(len(v) for v in per.values())
    return dict(frames=len(frames), confirmed_tracks=len(per), confirmed_detections=n,
                median_track_length=float(np.median([len(v) for v in per.values()])) if per else None,
                name_switches_per_100_by_track=dict(tracked=_r(100 * sw_t / n) if n else None,
                                                    independent=_r(100 * sw_i / n) if n else None))


def cmd_track(a):
    if not a.pred or not a.out or not a.fps:
        raise SystemExit("track needs --pred, --fps and --out")
    cfg, csha, cpath = load_tracker_config(a.config)
    runs, merged = load_preds(a.pred)
    for d, meta, _ in runs:
        lo = meta.get("level_order")
        if lo is not None and list(lo) != list(LEVEL_ORDER):
            raise SystemExit(f"cine_eval track: {d}: prototype level_order differs from fluorocap_anchor.LEVEL_ORDER")
        if not meta.get("dump_posterior"):
            raise SystemExit(f"cine_eval track: {d}: the prototype ran without --dump-posterior; the tracker pools "
                             "the per-body posterior and has nothing to pool")
    metas = load_metas(a.meta, set(merged)) if a.meta else {}
    rx = re.compile(a.stem_regex)
    seqs = collections.defaultdict(list)
    bad = []
    for stem, rec in merged.items():
        sf = seq_frame(stem, metas, rx)
        if sf is None:
            bad.append(stem); continue
        seqs[sf[0]].append((sf[1], stem, rec))
    if bad:
        raise SystemExit(f"cine_eval track: {len(bad)} stems carry no sequence and frame (no meta, and --stem-regex "
                         f"{a.stem_regex!r} does not match), e.g. {bad[:3]}")
    out = dict(tool="tools/cine_eval.py track", pred=str(a.pred), pred_digest=pred_digest(merged), fps=float(a.fps),
               config_path=cpath, config_sha256=csha, config=cfg,
               max_age_frames=max(1, int(round(float(cfg["max_age_s"]) * float(a.fps)))),
               causal="frame t is associated, updated and named from frames <= t only", sequences={})
    t0 = time.time()
    for s in sorted(seqs):
        fr = run_tracker(sorted(seqs[s]), cfg, a.fps)
        out["sequences"][s] = dict(summary=track_summary(fr), frames=fr)
    p = Path(os.path.expanduser(a.out)); p.parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(p, "w", encoding="utf-8"), default=_json_default)
    n = sum(len(v["frames"]) for v in out["sequences"].values())
    print(f"cine_eval track: {len(seqs)} sequences, {n} frames, {time.time() - t0:.1f} s, config {csha[:23]} -> {p}",
          flush=True)
    return 0


# ================================================================================================ video
PALETTE = [(31, 119, 180), (255, 127, 14), (148, 103, 189), (23, 190, 207), (227, 119, 194), (188, 189, 34),
           (140, 86, 75), (174, 199, 232), (255, 187, 120), (197, 176, 213), (158, 218, 229), (247, 182, 210)]
C_TRUTH, C_IGNORE, C_FP, C_PLAIN, C_TENT = (60, 220, 90), (150, 150, 150), (235, 40, 40), (255, 210, 0), (230, 230, 230)


def _font(size=16):
    from PIL import ImageFont
    for name in ("DejaVuSans-Bold.ttf", "DejaVuSans.ttf", "arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size), True
        except Exception:  # noqa: BLE001
            pass
    try:
        return ImageFont.load_default(size=size), True
    except Exception:  # noqa: BLE001
        return ImageFont.load_default(), False


def find_ffmpeg(explicit=None):
    """The encoder: --ffmpeg, $FFMPEG, the fluorogen env's (grid: 8.1.2 with libx264), PATH, then imageio_ffmpeg's
    bundled binary (Windows). None: cv2.VideoWriter."""
    for c in (explicit, os.environ.get("FFMPEG"), os.path.expanduser("~/mambaforge/envs/fluorogen/bin/ffmpeg"),
              shutil.which("ffmpeg")):
        if c and os.path.isfile(c):
            return c
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:  # noqa: BLE001
        return None


class VideoOut:
    def __init__(self, path, W, H, fps, ffmpeg=None):
        self.path, self.W, self.H = str(path), W + (W % 2), H + (H % 2)
        self.exe = find_ffmpeg(ffmpeg)
        self.proc = self.cv = None
        if self.exe:
            cmd = [self.exe, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{self.W}x{self.H}",
                   "-r", f"{fps}", "-i", "-", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", self.path]
            self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            self.encoder = f"ffmpeg ({self.exe}) libx264 crf 18 yuv420p"
        else:
            import cv2
            self.cv = cv2.VideoWriter(self.path, cv2.VideoWriter_fourcc(*"mp4v"), float(fps), (self.W, self.H))
            self.encoder = "cv2.VideoWriter mp4v (no ffmpeg found)"

    def write(self, rgb):
        h, w = rgb.shape[:2]
        if (w, h) != (self.W, self.H):
            rgb = np.pad(rgb, ((0, self.H - h), (0, self.W - w), (0, 0)))
        if self.proc is not None:
            self.proc.stdin.write(np.ascontiguousarray(rgb, dtype=np.uint8).tobytes())
        else:
            self.cv.write(np.ascontiguousarray(rgb[:, :, ::-1]))

    def close(self):
        if self.proc is not None:
            self.proc.stdin.close()
            rc = self.proc.wait()
            if rc != 0:
                raise RuntimeError(f"ffmpeg exited {rc} writing {self.path}")
        else:
            self.cv.release()


def draw_frame(img, meta, rec, entries, *, hud=None, font=None, dot=3):
    """RGB uint8 frame with truth (thin green, corner dots; caudal-only: its two corners; ignore: grey) and
    predictions (track colour, 't07 C4 0.93' with '?' when abstained; false positives red). Never any file name."""
    from PIL import Image, ImageDraw
    im = Image.fromarray(img).convert("RGB")
    dr = ImageDraw.Draw(im)
    font = font or _font()[0]
    truth = prep_truth(meta) if meta else []
    calls = prep_calls(rec) if rec else []
    fp = set()
    if meta:
        fp = set(match_frame(truth, calls, body_h=body_height(truth))["fp"])
    for t in truth:
        b = t["box"]
        if t["role"] == "ignore":
            dr.rectangle(b, outline=C_IGNORE, width=1)
            continue
        if t["role"] == "caudal_only":
            p2, p3 = t["caudal"]
            dr.line([tuple(p3), tuple(p2)], fill=C_TRUTH, width=1)
            for p in (p2, p3):
                dr.ellipse([p[0] - dot, p[1] - dot, p[0] + dot, p[1] + dot], fill=C_TRUTH)
            continue
        dr.rectangle(b, outline=C_TRUTH, width=1)
        for p in (t.get("slots") if t.get("slots") is not None else []):
            dr.ellipse([p[0] - dot, p[1] - dot, p[0] + dot, p[1] + dot], fill=C_TRUTH)

    def label(b, txt, col):
        x, y = b[2] + 4, max(0, b[1])
        tw = dr.textlength(txt, font=font) if hasattr(dr, "textlength") else 8 * len(txt)
        dr.rectangle([x - 2, y - 1, x + tw + 3, y + 18], fill=(0, 0, 0))
        dr.text((x, y), txt, fill=col, font=font)
    if entries is not None:
        for e in entries:
            b = [float(v) for v in e["box"]]
            if e.get("det_index") is None:          # a coasting track: its predicted box, thin
                col = PALETTE[e["track_id"] % len(PALETTE)]
                dr.rectangle(b, outline=col, width=1)
                continue
            i = e["det_index"]
            conf = e.get("confirmed")
            col = PALETTE[e["track_id"] % len(PALETTE)] if conf else C_TENT
            dr.rectangle(b, outline=C_FP if i in fp else col, width=3 if i in fp else 2)
            c = calls[i] if i < len(calls) else {}
            for p in (c.get("slots") if c.get("slots") is not None else []):
                dr.ellipse([p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2], fill=col)
            if conf and e.get("name_tracked"):
                label(b, f"t{e['track_id']:02d} {e['name_tracked']} {e['p']:.2f}" + ("?" if e.get("abstain") else ""),
                      C_FP if i in fp else col)
    else:
        for i, c in enumerate(calls):
            b = c["box"]
            col = C_FP if i in fp else C_PLAIN
            dr.rectangle(b, outline=col, width=2)
            for p in (c.get("slots") if c.get("slots") is not None else []):
                dr.ellipse([p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2], fill=col)
            if c.get("level"):
                label(b, f"{c['level']} {float(c.get('level_prob') or 0):.2f}" + ("?" if c.get("abstain") else ""), col)
    if hud:
        tw = dr.textlength(hud, font=font) if hasattr(dr, "textlength") else 8 * len(hud)
        dr.rectangle([4, 4, 12 + tw, 26], fill=(0, 0, 0))
        dr.text((8, 6), hud, fill=(255, 255, 255), font=font)
    return np.asarray(im)


def hud_text(frame, meta, angle_key, latency_ms, unicode_ok=True):
    parts = [f"frame {frame}"]
    if meta and angle_key:
        keys = [angle_key] if angle_key != "auto" else ["machine_angle_deg", "lat_signed_deg", "angle_deg", "angle"]
        for k in keys:
            v = bin_value(meta, k)
            if v is not None:
                parts.append(f"{v:+.1f}" + ("\u00b0" if unicode_ok else " deg"))
                break
    if latency_ms is not None:
        parts.append(f"{latency_ms:.1f} ms")
    return "   ".join(parts)


def render_video(frames, loader, out_path, fps, *, angle_key="auto", latency=None, scale=1.0, ffmpeg=None):
    """frames: [(frame index, stem, meta or None, rec or None, entries or None)] in order; loader(stem) -> 2-D or
    RGB uint8 array (None: the frame is skipped). Returns a small record of what was written."""
    from PIL import Image
    font, uni = _font(18)
    vw = None
    n = skipped = 0
    for f, stem, meta, rec, ent in frames:
        img = loader(stem)
        if img is None:
            skipped += 1
            continue
        if img.ndim == 2:
            img = np.repeat(img[:, :, None], 3, 2)
        rgb = draw_frame(img.astype(np.uint8), meta, rec, ent,
                         hud=hud_text(f, meta, angle_key, (latency or {}).get(stem), uni), font=font)
        if scale != 1.0:
            h, w = rgb.shape[:2]
            rgb = np.asarray(Image.fromarray(rgb).resize((int(round(w * scale)), int(round(h * scale))), Image.BILINEAR))
        if vw is None:
            vw = VideoOut(out_path, rgb.shape[1], rgb.shape[0], fps, ffmpeg)
        vw.write(rgb); n += 1
    if vw is not None:
        vw.close()
    return dict(path=str(out_path), frames=n, skipped=skipped, fps=fps, encoder=vw.encoder if vw else None)


def image_index(root):
    idx = {}
    if not root:
        return idx
    for p in glob.glob(os.path.join(os.path.expanduser(str(root)), "**", "*.png"), recursive=True):
        idx.setdefault(Path(p).stem, p)
    return idx


def cmd_video(a):
    from PIL import Image
    if not a.pred or not a.out or not a.fps:
        raise SystemExit("video needs --pred, --fps and --out")
    _, merged = load_preds(a.pred)
    metas = load_metas(a.meta, set(merged)) if a.meta else {}
    track = load_track(a.track)[1] if a.track else None
    lat = None
    if a.latency:
        L = json.load(open(os.path.expanduser(a.latency), encoding="utf-8"))
        lat = L.get("per_frame") or {}
    idx = image_index(a.images)
    rx = re.compile(a.stem_regex)
    seqs = collections.defaultdict(list)
    for stem in set(merged) | set(metas):
        sf = seq_frame(stem, metas, rx)
        if sf:
            seqs[sf[0]].append((sf[1], stem))
    want = set(a.seq) if a.seq else None

    def loader(stem):
        p = idx.get(stem) or ((merged.get(stem) or {}).get("image"))
        if not p or not os.path.exists(p):
            return None
        return np.asarray(Image.open(p).convert("L"))
    out = Path(os.path.expanduser(a.out)); out.mkdir(parents=True, exist_ok=True)
    recs = []
    for s in sorted(seqs):
        if want and s not in want:
            continue
        fr = [(f, st, metas.get(st), merged.get(st), (track.get(st) if track is not None else None))
              for f, st in sorted(seqs[s])]
        r = render_video(fr, loader, out / f"{s}.mp4", a.fps, angle_key=a.hud_angle, latency=lat, scale=a.scale,
                         ffmpeg=a.ffmpeg)
        recs.append(dict(seq=s, **r))
        print(f"cine_eval video: {s}: {r['frames']} frames ({r['skipped']} without an image) -> "
              + (r["path"] if r["frames"] else "NO VIDEO (no frame had an image; see --images)"), flush=True)
    json.dump(dict(tool="tools/cine_eval.py video", pred=str(a.pred), track=a.track, meta=a.meta, videos=recs),
              open(out / "videos.json", "w", encoding="utf-8"), indent=1)
    return 0


# ================================================================================================ the metric battery
def posterior_for(level, p=0.9):
    v = np.full(len(LEVEL_ORDER), (1 - p) / (len(LEVEL_ORDER) - 1))
    v[LEVEL_ORDER.index(level)] = p
    return [float(x) for x in v]


def perfect_preds(metas, *, shift=(0.0, 0.0), noise=0.0, seed=0, rename=0):
    """Predictions made from the truth itself: every score and caudal_only truth with corners becomes a detection
    whose corners are the truth's (scrambled in index order: the scorer must not match by index), shifted and/or
    jittered, box = min/max of the corners (the detector's convention), named by the truth level (optionally
    `rename` steps caudal along the standard column)."""
    rng = np.random.default_rng(seed)
    out = {}
    for m in metas:
        vs = []
        for b in m["boxes"]:
            if b.get("role", "score") == "ignore" or b.get("corners") is None:
                continue
            q = np.asarray(b["corners"], float).reshape(4, 2)
            if not np.isfinite(q).all():
                continue
            q = q[[2, 0, 3, 1]] + np.asarray(shift, float)
            if noise:
                q = q + rng.normal(0, noise, q.shape)
            lvl = b.get("level")
            if lvl and rename:
                lvl = STD[STD.index(lvl) + rename]
            vs.append(dict(box=[float(q[:, 0].min()), float(q[:, 1].min()), float(q[:, 0].max()), float(q[:, 1].max())],
                           det_conf=0.9, level=lvl, level_prob=0.9, single_crop=lvl, abstain=False,
                           posterior=posterior_for(lvl) if lvl else None, corners=q.tolist()))
        vs.sort(key=lambda v: 0.5 * (v["box"][1] + v["box"][3]))
        out[m["stem"]] = dict(image=f"{m['stem']}.png", vertebrae=vs)
    return out


def oracle_track(metas, preds, *, swap=None, swap_at=None):
    """A perfect tracker's entries (track id = the gt_id's index), optionally with two gt_ids' ids swapped from
    frame `swap_at` on."""
    ids = {}
    out = {}
    for m in metas:
        ent = []
        truth = prep_truth(m)
        calls = prep_calls(preds[m["stem"]])
        mt = match_frame(truth, calls, body_h=body_height(truth))
        for i, j, _ in mt["pairs"]:
            g = truth[j]["gt_id"]
            tid = ids.setdefault(g, len(ids) + 1)
            if swap and swap_at is not None and m["frame"] >= swap_at and g in swap:
                o = swap[1] if g == swap[0] else swap[0]
                tid = ids.setdefault(o, len(ids) + 1)
            c = calls[i]
            ent.append(dict(track_id=tid, det_index=i, box=c["box"], confirmed=True, name_indep=c.get("level"),
                            abstain_indep=False, name_tracked=c.get("level"), p=0.9, abstain=False))
        out[m["stem"]] = ent
    return out


def flip_meta(m, W):
    """The frame mirrored left-right (x -> W - 1 - x, pixel centres), truth with it; anatomical order is kept."""
    m2 = json.loads(json.dumps(m))
    for b in m2["boxes"]:
        x0, y0, x1, y1 = b["box"]
        b["box"] = [W - 1 - x1, y0, W - 1 - x0, y1]
        if b.get("corners") is not None:
            b["corners"] = [[W - 1 - x, y] for x, y in b["corners"]]
        if b.get("caudal") is not None:
            b["caudal"] = [[W - 1 - x, y] for x, y in b["caudal"]]
    ex = m2.setdefault("extras", {})
    if ex.get("facing") in ("L", "R"):
        ex["facing"] = "R" if ex["facing"] == "L" else "L"
    ex["flipped"] = not ex.get("flipped", False)
    return m2


def flip_rec(rec, W):
    r = json.loads(json.dumps(rec))
    for v in r.get("vertebrae") or []:
        x0, y0, x1, y1 = v["box"]
        v["box"] = [W - 1 - x1, y0, W - 1 - x0, y1]
        if v.get("corners") is not None:
            v["corners"] = [[W - 1 - x, y] for x, y in v["corners"]]
    return r


def battery(metas, *, fps, drop_level="C5", drop_frames=range(10, 20), swap=("C4", "C5"), swap_at=50,
            ignore_level="C1", flip_metas=None, width=1024, cfg=None):
    """The tier-1 metric tests (plan 2, 'self-test'): predictions made from real truth with known perturbations,
    each result against its exact expected value. metas: one sequence's frames in order. Returns rows
    [{test, expected, actual, ok}]."""
    cfg = cfg or TRACKER_DEFAULTS
    metas = sorted(metas, key=lambda m: m["frame"])
    rows = []

    def row(test, expected, actual, ok):
        rows.append(dict(test=test, expected=expected, actual=actual, ok=bool(ok)))

    def run(preds, track=None):
        fr = [(m["stem"], m, preds[m["stem"]]) for m in metas]
        return evaluate(fr, track=track)[0]
    base = perfect_preds(metas)
    r0 = run(base, oracle_track(metas, base))
    o = r0["overall"]
    row("unperturbed: recall / precision / FP", "1.0 / 1.0 / 0", f"{o['recall']} / {o['precision']} / {o['fp']}",
        o["recall"] == 1.0 and o["precision"] == 1.0 and o["fp"] == 0)
    row("unperturbed: corner error (px, every slot)", "0.000", f"{o['corners']['all']['px']['mean']:.3f}",
        abs(o["corners"]["all"]["px"]["mean"]) < 1e-9)
    ca0 = o["caudal_truth"]
    row("unperturbed: a perfect caudal-only (C2) box matches on every frame (caudal recall)", "1.0",
        f"{o['caudal_recall']} (of {ca0}; under the plan's --caudal-ref mean: "
        f"{evaluate([(m['stem'], m, base[m['stem']]) for m in metas], caudal_ref='mean')[0]['overall']['caudal_recall']})",
        o["caudal_recall"] == 1.0 or ca0 == 0)
    t0 = r0["temporal"]["overall"]
    row("unperturbed, oracle tracks: IDSW / frag / MOTA / IDF1", "0 / 0 / 1.0 / 1.0",
        f"{t0['idsw']} / {t0['frag']} / {t0['mota']} / {t0['idf1']}",
        t0["idsw"] == 0 and t0["frag"] == 0 and t0["mota"] == 1.0 and t0["idf1"] == 1.0)
    # 1. every corner shifted by (3, 4) px
    r = run(perfect_preds(metas, shift=(3.0, 4.0)))
    ca = r["overall"]["corners"]
    allv = [ca[f"slot{k}"]["px"] for k in range(4)]
    dev = max(abs(s["mean"] - 5.0) for s in allv if s["n"]) if any(s["n"] for s in allv) else None
    c2 = r["per_level"].get("C2", {}).get("corners", {})
    c2slots = [k for k in range(4) if c2.get(f"slot{k}", {}).get("px", {}).get("n")]
    row("shift every corner by (3, 4) px: corner error, slot to slot and order-free", "5.000, 5.000 (C2: slots 2 and 3 "
        "only)", f"{ca['all']['px']['mean']:.3f}, {ca['assigned']['px']['mean']:.3f} (max |slot mean - 5| {dev:.1e}; "
        f"C2 slots {c2slots})", dev is not None and dev < 1e-9 and abs(ca["assigned"]["px"]["mean"] - 5.0) < 1e-9
        and (not c2 or c2slots == [2, 3]))
    # the order-free pairing is optimal, so on every body it can only be <= the slot-to-slot sum, and equal to it
    # where the two readings pair the corners the same way
    e_n = evaluate([(m["stem"], m, pr) for m, pr in zip(metas, [perfect_preds(metas, noise=1.5, seed=3)[m["stem"]]
                                                                 for m in metas])])[2]
    wc = [x for x in e_n if x.get("corner_px")]
    viol = sum(1 for x in wc if sum(x["corner_assigned_px"]) > sum(e for e in x["corner_px"] if e is not None) + 1e-9)
    same = all(abs(sum(x["corner_assigned_px"]) - sum(e for e in x["corner_px"] if e is not None)) < 1e-6
               for x in wc if not x["slot_disagree"])
    nd = sum(1 for x in wc if x["slot_disagree"])
    sm = [x["split_margin"] for x in wc if x.get("split_margin") is not None]
    row("1.5 px noise on every corner: order-free <= slot-to-slot on every body, equal where they pair alike",
        "0 violations, equal", f"{viol} violations, {'equal' if same else 'NOT equal'}; slot pairing flipped on {nd} of "
        f"{len(wc)} bodies ({(100 * nd / max(1, len(wc))):.1f}%); truth within 5 px of the slot tie "
        f"{(100 * np.mean(np.asarray(sm) < 5)):.1f}%", viol == 0 and same)
    # 2. drop one level on frames 10-19
    dp = json.loads(json.dumps(base))
    by = {m["stem"]: m for m in metas}
    dropped = 0
    for m in metas:
        if m["frame"] in drop_frames:
            vs = dp[m["stem"]]["vertebrae"]
            keep = [v for v in vs if v["level"] != drop_level]
            dropped += len(vs) - len(keep)
            dp[m["stem"]]["vertebrae"] = keep
    n = r0["per_level"][drop_level]["truth"]
    r = run(dp, oracle_track(metas, dp))
    got = r["per_level"][drop_level]["recall"]
    fr = r["temporal"]["per_level"][drop_level]["frag"]
    row(f"drop {drop_level} on frames {drop_frames[0]}-{drop_frames[-1]}: {drop_level} recall, fragmentation",
        f"(n-{dropped})/n = {(n - dropped) / n:.4f} (n = {n}), frag 1", f"{got}, frag {fr}",
        abs(got - round((n - dropped) / n, 4)) < 1e-9 and fr == 1 and dropped == len(drop_frames))
    # 3. two levels' track ids swapped from frame 50 on
    r = run(base, oracle_track(metas, base, swap=swap, swap_at=swap_at))
    sw = r["temporal"]["overall"]["idsw"]
    row(f"swap the track ids of {swap[0]} and {swap[1]} at frame {swap_at}: IDSW", "2", f"{sw}", sw == 2)
    # 4. every level renamed one step caudal
    r = run(perfect_preds(metas, rename=1))
    o = r["overall"]
    row("rename every level one step caudal: exact, within-1", "0.0, 1.0", f"{o['exact']}, {o['within1']}",
        o["exact"] == 0.0 and o["within1"] == 1.0)
    # 5./6. a false box in the ignore region, one below every truth
    fb = json.loads(json.dumps(base))
    n_ign = 0
    first = None
    for m in metas:
        tr = prep_truth(m)
        ig = [t for t in tr if t["role"] == "ignore" and t["gt_id"] == ignore_level]
        h = body_height(tr) or 40.0
        if ig:
            cx, cy = _centre(ig[0]["box"])
            fb[m["stem"]]["vertebrae"].append(dict(box=[cx - h / 2, cy - h / 2, cx + h / 2, cy + h / 2], level="C1",
                                                   level_prob=0.9, abstain=False, det_conf=0.9,
                                                   posterior=posterior_for("C1"), corners=None))
            n_ign += 1
        if first is None:
            first = m
    r = run(fb)
    row(f"a false box in the {ignore_level} ignore region (every frame that has one): FP", "0",
        f"{r['overall']['fp']} ({r['overall']['ignored']} dropped as ignored; {n_ign} placed)",
        r["overall"]["fp"] == 0 and r["overall"]["ignored"] == n_ign and n_ign > 0)
    fb2 = json.loads(json.dumps(base))
    tr = prep_truth(first)
    h = body_height(tr) or 40.0
    low = max(t["box"][3] for t in tr)
    sc = [t for t in tr if t["role"] == "score"]
    cx = _centre(max(sc, key=lambda t: t["box"][3])["box"])[0]
    y0 = min(low + h, 1023 - h)
    fbox = [cx - h / 2, y0, cx + h / 2, y0 + h]
    outside = all(not _inside(_centre(fbox), t["box"]) for t in tr)
    fb2[first["stem"]]["vertebrae"].append(dict(box=fbox, level="T2", level_prob=0.9, abstain=False, det_conf=0.9,
                                                posterior=posterior_for("T2"), corners=None))
    r = run(fb2)
    row("a false box below the lowest level, outside any ignore region (one frame): FP", "1",
        f"{r['overall']['fp']}", r["overall"]["fp"] == 1 and outside)
    # 7. the same R-facing sequence as-is and mirrored
    if flip_metas:
        fm = sorted(flip_metas, key=lambda m: m["frame"])
        fp_ = perfect_preds(fm, noise=1.5, seed=7)
        e1 = evaluate([(m["stem"], m, fp_[m["stem"]]) for m in fm])[2]
        fm2 = [flip_meta(m, width) for m in fm]
        fp2 = {k: flip_rec(v, width) for k, v in fp_.items()}
        e2 = evaluate([(m["stem"], m, fp2[m["stem"]]) for m in fm2])[2]
        a1 = {(x["stem"], x["gt_id"]): x for x in e1 if x.get("corner_px")}
        a2 = {(x["stem"], x["gt_id"]): x for x in e2 if x.get("corner_px")}
        dmax, dan, nn = 0.0, 0.0, 0
        for k, x in a1.items():
            y = a2.get(k)
            if y is None:
                dmax = float("inf"); continue
            for s in range(4):
                u, v = x["corner_px"][s], y["corner_px"][FLIP_SLOT[s]]
                if (u is None) != (v is None):
                    dmax = float("inf")
                elif u is not None:
                    dmax = max(dmax, abs(u - v)); nn += 1
            if set(x.get("corner_anat") or {}) != set(y.get("corner_anat") or {}):
                dan = float("inf")
            for nm_, u in (x.get("corner_anat") or {}).items():
                dan = max(dan, abs(u - (y.get("corner_anat") or {}).get(nm_, float("inf"))))
        fac = {x.get("facing") for x in [prep_truth(fm[0])[0], prep_truth(fm2[0])[0]]}
        row("same R-facing sequence, as-is and mirrored: slot-mapped corner errors (slot k <-> slot [1,0,3,2][k]), "
            "and per anatomical corner", "identical",
            f"max |diff| {dmax:.1e} over {nn} corner errors, anatomical {dan:.1e}; facings {sorted(f for f in fac if f)}",
            nn > 0 and len(a1) == len(a2) and dmax < 1e-9 and dan < 1e-9)
    # the real tracker on the perfect predictions (not the plan's table: a check on the tracker itself)
    mh = int(cfg["min_consecutive_hits"])
    ma = max(1, int(round(float(cfg["max_age_s"]) * fps)))

    def tracked(preds):
        seqs = [(m["frame"], m["stem"], preds[m["stem"]]) for m in metas]
        tf = run_tracker(seqs, cfg, fps)
        return {f["stem"]: f["tracks"] for f in tf}
    r = run(base, tracked(base))
    t = r["temporal"]["overall"]
    f0 = [m for m in metas if m["frame"] < metas[0]["frame"] + mh - 1]
    fn0 = sum(len([x for x in prep_truth(m) if x["role"] != "ignore"]) for m in f0)
    exp_mota = round(1 - fn0 / t["gt"], 4) if t["gt"] else None
    tn = r["overall"].get("tracked_naming", {})
    row("real tracker on the unperturbed predictions: IDSW / frag / FN (the confirmation delay) / MOTA / tracked "
        "naming exact", f"0 / 0 / {fn0} / {exp_mota} / {round(1 - fn0 / max(1, t['gt']), 4)}",
        f"{t['idsw']} / {t['frag']} / {t['fn']} / {t['mota']} / {tn.get('exact')}",
        t["idsw"] == 0 and t["frag"] == 0 and t["fn"] == fn0 and t["mota"] == exp_mota
        and tn.get("exact") is not None and abs(tn["exact"] - round(1 - fn0 / max(1, t["gt"]), 4)) < 1e-9)
    r = run(dp, tracked(dp))
    tl = r["temporal"]["per_level"][drop_level]
    k = len(drop_frames)
    exp_sw = 1 if k >= ma else 0
    row(f"real tracker, {drop_level} dropped for {k} frames (max_age {ma} frames at {fps:g} fps): {drop_level} IDSW, "
        "frag", f"{exp_sw}, 1", f"{tl['idsw']}, {tl['frag']}", tl["idsw"] == exp_sw and tl["frag"] == 1)
    return rows


def synthetic_sequence(n=120, facing="L", W=1024, seed=0):
    """A made-up cervical sequence in the cine schema (anatomical corners): C0 and C1 and T1 ignore, C2 caudal-only,
    C3-C7 scored, every body rocking about a point below the stack."""
    rng = np.random.default_rng(seed)
    levels = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "T1"]
    role = dict(C0="ignore", C1="ignore", C2="caudal_only", T1="ignore")
    metas = []
    for k in range(n):
        th = math.radians(12 * math.sin(2 * math.pi * k / n))
        boxes = []
        for i, lv in enumerate(levels):
            cx0, cy0, w, h = 480.0 + 3 * i, 250.0 + 62 * i, 56.0, 44.0
            cx = 480 + (cx0 - 480) * math.cos(th) - (cy0 - 820) * math.sin(th)
            cy = 820 + (cx0 - 480) * math.sin(th) + (cy0 - 820) * math.cos(th)
            ang = th * (1 - i / 12) + rng.normal(0, 0.002)
            ca, sa = math.cos(ang), math.sin(ang)
            s = -1 if facing == "L" else 1                  # anterior toward -x when facing L
            loc = [(s * w / 2, -h / 2), (s * w / 2, h / 2), (-s * w / 2, h / 2), (-s * w / 2, -h / 2)]   # AS AI PI PS
            q = [[cx + u * ca - v * sa, cy + u * sa + v * ca] for u, v in loc]
            q = [[round(x, 3), round(y, 3)] for x, y in q]
            xs, ys = [p[0] for p in q], [p[1] for p in q]
            boxes.append(dict(gt_id=lv, cls=0, level=lv, box=[min(xs), min(ys), max(xs), max(ys)], corners=q,
                              role=role.get(lv, "score")))
        metas.append(dict(case="synthetic", stem=f"synth{facing}_f{k:04d}", seq=f"synth{facing}", frame=k, view="LAT",
                          px_mm=None, corner_order="anatomical", boxes=boxes,
                          extras=dict(facing=facing, angle_deg=math.degrees(th))))
    return metas


def print_table(rows, title):
    print(f"\n{title}")
    w1 = max(len(r["test"]) for r in rows)
    for r in rows:
        print(f"  [{'PASS' if r['ok'] else 'FAIL'}] {r['test']:<{w1}}  expected {r['expected']}  |  actual {r['actual']}")
    bad = [r for r in rows if not r["ok"]]
    print(f"  {len(rows) - len(bad)}/{len(rows)} passed", flush=True)
    return not bad


def cmd_self_test(a):
    ok = True
    # the committed tracker constants are the plan's
    if TRACKER_CONFIG.exists():
        cfg = json.loads(TRACKER_CONFIG.read_text(encoding="utf-8"))
        diff = {k: (cfg.get(k), v) for k, v in TRACKER_DEFAULTS.items() if cfg.get(k) != v}
        print(f"tracker_config.json {'matches' if not diff else 'DIFFERS FROM'} the plan's constants"
              + (f": {diff}" if diff else ""))
        ok &= not diff
    else:
        print(f"note: {TRACKER_CONFIG} not present; the battery uses the plan's constants")
    metas = synthetic_sequence(120, "L")
    rows = battery(metas, fps=15.0, flip_metas=synthetic_sequence(60, "R", seed=1))
    ok &= print_table(rows, "cine_eval self-test: synthetic 120-frame sequence (C2 caudal-only, C3-C7 scored, "
                            "C0/C1/T1 ignore)")
    # the CLI path end to end, on disk: track -> score (the gate carried as declared) -> video
    out = Path(os.path.expanduser(a.out)) if a.out else Path(os.environ.get("TMP", "/tmp")) / "cine_eval_selftest"
    shutil.rmtree(out, ignore_errors=True)
    (out / "meta").mkdir(parents=True); (out / "pred").mkdir(parents=True)
    for m in metas:
        json.dump(m, open(out / "meta" / f"{m['stem']}.json", "w"))
    preds = perfect_preds(metas)
    json.dump(list(preds.values()), open(out / "pred" / "prototype_results.json", "w"))
    json.dump(dict(level_order=LEVEL_ORDER, dump_posterior=True, dump_corners=True,
                   eval_gate=dict(gate_version=EG.GATE_VERSION, held_out=False, n_checks=0, checks=[],
                                  not_held_out_reason="cine_eval self-test: synthetic predictions made from the truth")),
              open(out / "pred" / "prototype_meta.json", "w"))
    rc = main(["track", "--pred", str(out / "pred"), "--meta", str(out / "meta"), "--fps", "15",
               "--out", str(out / "track.json"), "--config", str(TRACKER_CONFIG) if TRACKER_CONFIG.exists() else
               _write_cfg(out)])
    rc |= main(["score", "--pred", str(out / "pred"), "--meta", str(out / "meta"), "--track", str(out / "track.json"),
                "--corpus-hint", "synthetic", "--bins", "angle:-15,-5,5,15", "--level-group", "primary=C3,C4,C5,C6",
                "--out", str(out / "score.json")])
    S = json.load(open(out / "score.json"))
    cli = [dict(test="CLI score: eval_gate first, held_out false with the declared reason",
                expected="eval_gate, False", actual=f"{list(S)[0]}, {S['eval_gate'].get('held_out')}",
                ok=list(S)[0] == "eval_gate" and S["eval_gate"].get("held_out") is False),
           dict(test="CLI score: primary group recall / exact", expected="1.0 / 1.0",
                actual=f"{S['groups']['primary']['recall']} / {S['groups']['primary']['exact']}",
                ok=S["groups"]["primary"]["recall"] == 1.0 and S["groups"]["primary"]["exact"] == 1.0),
           dict(test="CLI score: every frame row carries its corpus hint", expected="synthetic",
                actual=str(sorted({r['hint'] for r in S['frames']})), ok={r["hint"] for r in S["frames"]} == {"synthetic"}),
           dict(test="CLI score: tracked IDSW (real tracker)", expected="0",
                actual=str(S["temporal"]["overall"]["idsw"]), ok=S["temporal"]["overall"]["idsw"] == 0)]
    ok &= print_table(cli, "cine_eval self-test: the command line, on disk") and rc == 0
    print(f"\ncine_eval self-test: {'ALL PASSED' if ok else 'FAILED'} (outputs in {out})", flush=True)
    return 0 if ok else 1


def _write_cfg(out):
    p = Path(out) / "tracker_config.json"
    json.dump(TRACKER_DEFAULTS, open(p, "w"), indent=1)
    return str(p)


# ================================================================================================ main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["score", "track", "video", "self-test"])
    ap.add_argument("--pred", default=None, help="a tools/level_prototype.py output directory, or a directory of them "
                                                 "(one per sequence)")
    ap.add_argument("--meta", default=None, help="truth metas in the cine schema: <dir>/<stem>.json")
    ap.add_argument("--out", default=None)
    ap.add_argument("--tag", default="")
    ap.add_argument("--track", default=None, help="score / video: the track.json of `track` over the same --pred")
    ap.add_argument("--corpus-hint", default=None,
                    help="score: the corpus the scored cases key in (tools/patient_keys.key_any): bournemouth, "
                         "carmlspine, ctsp, ...; written into every frame row so a later carry keys them the same way")
    ap.add_argument("--bins", nargs="*", default=None,
                    help="score: bin variables from the meta (or its extras; NAME or NAME_deg): NAME (10-unit bins) "
                         "or NAME:e0,e1,...; every metric is also reported per bin")
    ap.add_argument("--level-group", action="append", default=[], metavar="NAME=L1,L2",
                    help="score: a named group of levels reported on its own (e.g. primary=C3,C4,C5,C6 c7=C7 c2=C2)")
    ap.add_argument("--mm-per-px", type=float, default=None,
                    help="score: pixel spacing for corner errors in mm (else the meta's px_mm; null: px only)")
    ap.add_argument("--caudal-ref", choices=["lower", "mean"], default="lower",
                    help="score: a caudal-only truth's inferior edge: the lower of its two caudal corners (default: the "
                         "inferior edge of a min/max box of the true corners), or their mean (the plan's wording, "
                         "under which a perfect C2 box fails on 17.7%% of Bournemouth frames; see match_frame)")
    ap.add_argument("--allow-unpredicted", action="store_true",
                    help="score: a truth frame with no prediction record scores every truth on it as a miss (default: "
                         "such frames are left out and counted)")
    ap.add_argument("--fps", type=float, default=None, help="track / video: frames per second of the sequence")
    ap.add_argument("--config", default=None, help=f"track: tracker constants (default {TRACKER_CONFIG})")
    ap.add_argument("--stem-regex", default=STEM_RE,
                    help="track / video: sequence and frame from a stem that has no meta")
    ap.add_argument("--images", default=None, help="video: directory searched recursively for <stem>.png")
    ap.add_argument("--seq", action="append", default=[], help="video: only these sequences")
    ap.add_argument("--hud-angle", default="auto", help="video: meta/extras key shown in the HUD (auto: machine angle, "
                                                         "then lat_signed_deg)")
    ap.add_argument("--latency", default=None, help="video: a JSON with per_frame {stem: ms} shown in the HUD")
    ap.add_argument("--scale", type=float, default=1.0, help="video: output scale")
    ap.add_argument("--ffmpeg", default=None, help="video: ffmpeg binary")
    EG.add_args(ap)
    a = ap.parse_args(argv)
    return {"score": cmd_score, "track": cmd_track, "video": cmd_video, "self-test": cmd_self_test}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
