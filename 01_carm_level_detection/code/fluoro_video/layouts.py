# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/layouts.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""Stable panel layouts across a video, and coarse segments.

Clustering (deterministic leader clustering, two refinement passes): every accepted candidate box of every sample,
normalised by the frame width / height, is visited in order of decreasing score (ties: sample index, box). It joins
the first cluster whose centre is within cluster_eps (Chebyshev distance over the four normalised coordinates),
else it founds a cluster. Centres are then replaced by the per-coordinate median of the members and every candidate
is reassigned to the nearest centre within eps (twice). A layout's crop box is the outer envelope of its members at
native scale (x0, y0 at the 10th, x1, y1 at the 90th percentile: box_outer_q), because detection errors mostly
shrink a panel. Layouts whose boxes overlap with IoU >= layout_merge_iou are merged (the same panel with edge
jitter), and so is a layout lying >= layout_nest_contain inside another whose member samples interleave with its
own over >= layout_nest_overlap of the shorter span (the same panel, detected smaller on some frames). A candidate belongs to exactly one layout (the one with the highest IoU, which must be >=
member_iou).

Segments: for each layout, the samples with a member are runs; runs separated by gaps <= max_gap_s are merged; a
run shorter than min_segment_s is dropped (rule recorded). Duration of a run = (last - first sample time) + one
sample interval.
"""
from __future__ import annotations

import numpy as np

from .panels import iou


def _norm_box(b, W, H):
    return np.array([b[0] / W, b[1] / H, b[2] / W, b[3] / H], float)


def cluster(cands, W, H, eps, n_iter=2):
    """cands: [(sample_idx, box_native, score)]. Returns labels (list of int) and centres (k x 4 normalised)."""
    if not cands:
        return [], np.zeros((0, 4))
    X = np.stack([_norm_box(c[1], W, H) for c in cands])
    order = sorted(range(len(cands)), key=lambda i: (-cands[i][2], cands[i][0], tuple(cands[i][1])))
    centres = []
    lab = [-1] * len(cands)
    for i in order:
        best, bd = -1, None
        for k, c in enumerate(centres):
            d = float(np.max(np.abs(X[i] - c)))
            if d <= eps and (bd is None or d < bd):
                best, bd = k, d
        if best < 0:
            centres.append(X[i].copy())
            best = len(centres) - 1
        lab[i] = best
    C = np.array(centres)
    for _ in range(n_iter):
        C = np.array([np.median(X[[i for i in range(len(lab)) if lab[i] == k]], axis=0)
                      if any(l == k for l in lab) else C[k] for k in range(len(C))])
        D = np.max(np.abs(X[:, None, :] - C[None, :, :]), axis=2)
        new = []
        for i in range(len(cands)):
            k = int(np.argmin(D[i]))
            new.append(k if D[i, k] <= eps else lab[i])
        lab = new
    return lab, C


def outer_box(B, q):
    """Outer envelope of member boxes: x0, y0 at the (1-q) quantile, x1, y1 at the q quantile."""
    B = np.asarray(B, float)
    lo = np.quantile(B[:, :2], 1.0 - q, axis=0, method="lower")
    hi = np.quantile(B[:, 2:], q, axis=0, method="higher")
    return [int(round(v)) for v in list(lo) + list(hi)]


def build_layouts(samples, W, H, P):
    """samples: [{i, t, cands: [candidate dict]}]. Returns layouts (list of dict) and the per-sample membership."""
    sidx = {s["i"]: s for s in samples}
    flat = []
    for s in samples:
        for j, c in enumerate(s["cands"]):
            if c["accepted"]:
                flat.append((s["i"], c["box"], c["score"], j))
    lab, _ = cluster([(a, b, c) for a, b, c, _ in flat], W, H, float(P["cluster_eps"]))
    groups = {}
    for (si, box, sc, j), k in zip(flat, lab):
        groups.setdefault(k, []).append((si, box, sc, j))
    q = float(P["box_outer_q"])
    lays = []
    for k, mem in groups.items():
        box = outer_box([m[1] for m in mem], q)
        lays.append(dict(box=box, members=mem, first=min(m[0] for m in mem)))
    # merge near-identical layouts (same panel, edge jitter beyond eps on one side)
    lays.sort(key=lambda L: (-len(L["members"]), L["first"], L["box"]))
    merged = []
    for L in lays:
        tgt = next((M for M in merged if iou(M["box"], L["box"]) >= float(P["layout_merge_iou"])), None)
        if tgt is None:
            merged.append(dict(box=L["box"], members=list(L["members"]), first=L["first"]))
        else:
            tgt["members"] += L["members"]
            tgt["box"] = outer_box([m[1] for m in tgt["members"]], q)
            tgt["first"] = min(tgt["first"], L["first"])
    # nested layouts that interleave in time are one panel whose extent was detected smaller on some frames
    from .panels import contain
    changed = True
    while changed:
        changed = False
        merged.sort(key=lambda L: (-(L["box"][2] - L["box"][0]) * (L["box"][3] - L["box"][1]), L["first"], L["box"]))
        for a in range(len(merged)):
            for b in range(len(merged)):
                if a == b:
                    continue
                big, small = merged[a], merged[b]
                if contain(small["box"], big["box"]) < float(P["layout_nest_contain"]):
                    continue
                s0, s1 = min(m[0] for m in small["members"]), max(m[0] for m in small["members"])
                b0, b1 = min(m[0] for m in big["members"]), max(m[0] for m in big["members"])
                ov = min(s1, b1) - max(s0, b0) + 1
                if ov >= float(P["layout_nest_overlap"]) * (min(s1 - s0, b1 - b0) + 1):
                    big["members"] += small["members"]
                    big["box"] = outer_box([m[1] for m in big["members"]], q)
                    big["first"] = min(big["first"], small["first"])
                    big.setdefault("merged_nested", 0)
                    big["merged_nested"] += 1
                    del merged[b]
                    changed = True
                    break
            if changed:
                break
    merged = [L for L in merged if len(L["members"]) >= int(P["min_layout_members"])]
    merged.sort(key=lambda L: (L["first"], L["box"]))
    for n, L in enumerate(merged):
        L["id"] = f"L{n:02d}"
        B = np.array([m[1] for m in L["members"]], float)
        L["box_mad"] = [float(v) for v in np.median(np.abs(B - np.median(B, axis=0)), axis=0)]
        L["n_members"] = len(L["members"])
        shapes = [sidx[m[0]]["cands"][m[3]]["shape"] for m in L["members"]]
        L["shape"] = max(set(shapes), key=lambda s: (shapes.count(s), s))
        circ = [sidx[m[0]]["cands"][m[3]]["circle"] for m in L["members"]
                if sidx[m[0]]["cands"][m[3]]["circle"] is not None]
        L["circle"] = [float(v) for v in np.median(np.array(circ), axis=0)] if (circ and L["shape"] == "circle") else None
    # exclusive membership: every accepted candidate -> the layout with the highest IoU (>= member_iou)
    member = {L["id"]: {} for L in merged}
    for s in samples:
        for j, c in enumerate(s["cands"]):
            if not c["accepted"]:
                continue
            best = max(merged, key=lambda L: (iou(c["box"], L["box"]), L["id"]), default=None)
            if best is not None and iou(c["box"], best["box"]) >= float(P["member_iou"]):
                prev = member[best["id"]].get(s["i"])
                if prev is None or c["score"] > prev[1]:
                    member[best["id"]][s["i"]] = (j, c["score"])
    for L in merged:
        L["member_samples"] = sorted(member[L["id"]])
        del L["members"]
    return merged, member


def runs_for_layout(L, samples, P, dt):
    """Coarse runs of one layout: (first sample, last sample) merged across gaps <= max_gap_s; each run is
    kept or dropped with the rule that fired."""
    t_of = {s["i"]: s["t"] for s in samples}
    ms = L["member_samples"]
    if not ms:
        return []
    order = [s["i"] for s in samples]
    pos = {i: k for k, i in enumerate(order)}
    runs = []
    cur = [ms[0], ms[0], 1]
    for i in ms[1:]:
        gap = t_of[i] - t_of[cur[1]] - dt
        if gap <= float(P["max_gap_s"]) + 1e-9:
            cur[1] = i
            cur[2] += 1
        else:
            runs.append(cur)
            cur = [i, i, 1]
    runs.append(cur)
    out = []
    for a, b, n in runs:
        dur = t_of[b] - t_of[a] + dt
        k0, k1 = pos[a], pos[b]
        span = k1 - k0 + 1
        rule = None
        if dur < float(P["min_segment_s"]) - 1e-9:
            rule = f"dropped: coarse duration {dur:.2f} s < min_segment_s {P['min_segment_s']}"
        elif n / span < float(P["min_member_frac"]):
            rule = f"dropped: member fraction {n / span:.2f} < min_member_frac {P['min_member_frac']}"
        out.append(dict(layout=L["id"], first_sample=a, last_sample=b, t_first=t_of[a], t_last=t_of[b],
                        coarse_duration_s=dur, n_member_samples=n, n_span_samples=span,
                        prev_sample=order[k0 - 1] if k0 > 0 else None,
                        next_sample=order[k1 + 1] if k1 + 1 < len(order) else None,
                        kept=rule is None, rule=rule or "kept: member run >= min_segment_s with enough members"))
    return out
