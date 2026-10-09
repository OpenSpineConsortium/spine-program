# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/panels.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""Panel detection on one frame: where is a greyscale, textured (fluoroscopic) image inside a composite frame.

Per frame (at the analysis scale, an integer block-mean downscale of the native frame):
  grey      = chroma (max - min of R, G, B after the block mean) <= chroma_max
  nonblack  = luma > black_max
  textured  = local standard deviation of luma over a texture_window square >= texture_min
  seed      = grey & nonblack & textured, opened by open_px (removes text strokes and 1-2 px lines)
  core      = seed closed by close_px, holes filled (bridges smooth soft tissue inside the image); opening, closing
              and dilation use square structuring elements (separable running max/min: O(N) per frame)
  region    = grey & nonblack within snap_px of a core component (box edges follow the exact greyscale edge,
              not the texture filter's blurred edge)
  XY-cut    = a region box is split along full-height / full-width gutters (runs of >= gutter_min_px columns or
              rows whose region occupancy <= gutter_occ): two images side by side separated by a black gutter
  features  = purity (grey fraction of the box), chroma_p90 (90th percentile of the residual chroma of its grey
              non-black pixels: fluoroscopy is greyscale at source), texture (median local std over grey non-black box
              pixels),
              entropy (bits, 64-bin luma histogram over the same pixels), fill (region fraction of the box),
              aspect, area fraction; circle fit (Kasa least squares on the region boundary) for round
              image-intensifier fields
  circle    = circle COMPLETION: a round field that is partly flat inside (saturated air, collimator shading) is
              partly textured, so its region covers part of the disk; the region boundary pixels touching black
              (the rim) are fitted with a circle, and when the rim is round, long and the disk is bright the box
              becomes the disk's bounding box (clipped to the frame)
  score     = mean of the four features normalised between their gate and a 'typical fluoroscopy' level
  accepted  = every gate passes; non-maximum suppression drops a candidate lying >= nms_contain inside a better one
"""
from __future__ import annotations

import math

import numpy as np
from scipy import ndimage as ndi


def disk(r):
    r = int(r)
    if r <= 0:
        return np.ones((1, 1), bool)
    y, x = np.mgrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y) <= r * r


def sq_dilate(m, r):
    """Binary dilation by a (2r+1) square: a separable running maximum (O(N), independent of r)."""
    return ndi.maximum_filter(m.astype(np.uint8), size=2 * r + 1, mode="constant", cval=0).astype(bool)


def sq_erode(m, r):
    return ndi.minimum_filter(m.astype(np.uint8), size=2 * r + 1, mode="constant", cval=0).astype(bool)


def sq_open(m, r):
    return sq_dilate(sq_erode(m, r), r)


def sq_close(m, r):
    """Closing by a square; the frame border is padded so a panel touching the border is not eroded there."""
    p = r + 1
    mm = np.pad(m, p, mode="edge")
    return sq_erode(sq_dilate(mm, r), r)[p:-p, p:-p]


def analysis_factor(w, h, max_side):
    return max(1, int(math.ceil(max(w, h) / float(max_side))))


def block_mean(a, f):
    """Integer block mean (exact, deterministic) of an HxW[xC] uint8 array; the trailing partial block is dropped.
    Summed as f*f strided slices (fast for the small integer factors used here)."""
    if f == 1:
        return a.astype(np.float32)
    H, W = a.shape[:2]
    h, w = H // f, W // f
    acc = np.zeros((h, w) + a.shape[2:], np.uint32)
    for i in range(f):
        for j in range(f):
            acc += a[i:h * f:f, j:w * f:f]
    return (acc.astype(np.float64) / (f * f)).astype(np.float32)


def maps_from_rgb(rgb, f, P):
    """Analysis maps of one RGB uint8 frame (native), at scale 1/f."""
    sm = block_mean(rgb, f)                                  # h x w x 3 float32
    r, g, b = sm[..., 0], sm[..., 1], sm[..., 2]
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    chroma = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    w = int(P["texture_window"])
    m1 = ndi.uniform_filter(luma.astype(np.float64), w, mode="reflect")
    m2 = ndi.uniform_filter(luma.astype(np.float64) ** 2, w, mode="reflect")
    lstd = np.sqrt(np.clip(m2 - m1 * m1, 0, None)).astype(np.float32)
    grey = chroma <= float(P["chroma_max"])
    nonblack = luma > float(P["black_max"])
    return dict(luma=luma.astype(np.float32), chroma=chroma, lstd=lstd, grey=grey, nonblack=nonblack,
                textured=lstd >= float(P["texture_min"]), f=f, shape=luma.shape)


def _norm(v, lo, hi):
    if v is None or not np.isfinite(v):
        return 0.0
    return float(np.clip((v - lo) / (hi - lo), 0.0, 1.0)) if hi != lo else float(v >= lo)


def box_features(M, box, region=None):
    """Features of a fixed analysis-scale box [x0, y0, x1, y1) (exclusive ends). region: the candidate's own region
    mask (analysis scale); None for a fixed box (fill = grey & non-black fraction)."""
    x0, y0, x1, y1 = [int(v) for v in box]
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(M["shape"][1], x1), min(M["shape"][0], y1)
    if x1 - x0 < 2 or y1 - y0 < 2:
        return dict(purity=0.0, texture=0.0, entropy=0.0, fill=0.0, aspect=None, n=0, chroma_p90=99.0)
    g = M["grey"][y0:y1, x0:x1]
    nb = M["nonblack"][y0:y1, x0:x1]
    gm = g & nb
    purity = float(g.mean())
    if gm.sum() >= 16:
        tex = float(np.median(M["lstd"][y0:y1, x0:x1][gm]))
        chp90 = float(np.percentile(M["chroma"][y0:y1, x0:x1][gm], 90))
        hist = np.histogram(M["luma"][y0:y1, x0:x1][gm], bins=64, range=(0, 256))[0].astype(np.float64)
        p = hist / hist.sum()
        p = p[p > 0]
        ent = float(-(p * np.log2(p)).sum())
    else:
        tex, ent, chp90 = 0.0, 0.0, 99.0
    if region is not None:
        fill = float(region[y0:y1, x0:x1].mean())
    else:
        fill = float(gm.mean())
    return dict(purity=purity, texture=tex, entropy=ent, fill=fill, aspect=(x1 - x0) / float(y1 - y0),
                n=int(gm.sum()), chroma_p90=chp90)


def score_features(feat, P, area_frac=None):
    """(score in [0, 1], {gate: passed}, first failing gate or None)."""
    S = P["score"]
    parts = [_norm(feat["purity"], S["purity"][0], S["purity"][1]),
             _norm(feat["texture"], S["texture"][0], S["texture"][1]),
             _norm(feat["entropy"], S["entropy"][0], S["entropy"][1]),
             _norm(feat["fill"], S["fill"][0], S["fill"][1])]
    score = float(np.mean(parts))
    gates = dict(purity=feat["purity"] >= P["purity_min"], chroma=feat["chroma_p90"] <= P["chroma_p90_max"],
                 texture=feat["texture"] >= P["texture_box_min"],
                 entropy=feat["entropy"] >= P["entropy_min_bits"], fill=feat["fill"] >= P["fill_min"])
    if feat.get("aspect") is not None:
        gates["aspect"] = P["aspect_range"][0] <= feat["aspect"] <= P["aspect_range"][1]
    if area_frac is not None:
        gates["area"] = area_frac >= P["min_area_frac"]
    fail = next((k for k, ok in gates.items() if not ok), None)
    return score, gates, fail


def _runs(mask1d):
    """[(start, end_exclusive)] of True runs."""
    m = np.concatenate([[False], mask1d, [False]])
    d = np.diff(m.astype(np.int8))
    return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))


def xy_cut(region, box, P, depth=0):
    """Split a box along full gutters of the region mask; returns a list of tight boxes."""
    x0, y0, x1, y1 = box
    sub = region[y0:y1, x0:x1]
    if sub.size == 0 or not sub.any():
        return []
    ys, xs = np.where(sub)
    x0, x1 = x0 + int(xs.min()), x0 + int(xs.max()) + 1          # tighten
    y0, y1 = y0 + int(ys.min()), y0 + int(ys.max()) + 1
    sub = region[y0:y1, x0:x1]
    if depth >= int(P["xy_cut_depth"]):
        return [(x0, y0, x1, y1)]
    gmin, gocc = int(P["gutter_min_px"]), float(P["gutter_occ"])
    for axis in (0, 1):                                            # 0: split columns (vertical gutters), 1: rows
        occ = sub.mean(axis=axis)
        gaps = [(a, b) for a, b in _runs(occ <= gocc) if b - a >= gmin and a > 0 and b < occ.size]
        if gaps:
            cuts = [0] + [int((a + b) // 2) for a, b in gaps] + [occ.size]
            out = []
            for a, b in zip(cuts[:-1], cuts[1:]):
                nb = (x0 + a, y0, x0 + b, y1) if axis == 0 else (x0, y0 + a, x1, y0 + b)
                out += xy_cut(region, nb, P, depth + 1)
            return out
    return [(x0, y0, x1, y1)]


def refine_box(support, region, box, trim_support, band, n_iter=2):
    """Peel off box edges while the outer `band` lines of an edge are < trim_support 'panel-like' (support = grey
    and (textured or black): the pixels a fluoroscopy panel is made of), then tighten the box to the grey
    non-black region inside it; twice. Removes the room-camera pixels and flat grey bars/frame lines that the
    closing joined to a panel; the band (not a single line) makes a 1-2 px texture spill onto a flat bar count as
    what it is."""
    x0, y0, x1, y1 = box
    for _ in range(n_iter):
        while x1 - x0 > 2 * band and y1 - y0 > 2 * band:
            e = dict(top=float(support[y0:y0 + band, x0:x1].mean()), bottom=float(support[y1 - band:y1, x0:x1].mean()),
                     left=float(support[y0:y1, x0:x0 + band].mean()), right=float(support[y0:y1, x1 - band:x1].mean()))
            k = min(sorted(e), key=lambda n: e[n])
            if e[k] >= trim_support:
                break
            if k == "top":
                y0 += 1
            elif k == "bottom":
                y1 -= 1
            elif k == "left":
                x0 += 1
            else:
                x1 -= 1
        sub = region[y0:y1, x0:x1]
        if sub.size == 0 or not sub.any():
            return None
        ys, xs = np.where(sub)
        x0, x1, y0, y1 = x0 + int(xs.min()), x0 + int(xs.max()) + 1, y0 + int(ys.min()), y0 + int(ys.max()) + 1
    return (x0, y0, x1, y1)


def fit_circle(mask):
    """Kasa algebraic circle fit to the boundary pixels of a mask: (cx, cy, r, rms_rel)."""
    er = ndi.binary_erosion(mask)
    b = mask & ~er
    ys, xs = np.where(b)
    if xs.size < 20:
        return None
    x = xs.astype(np.float64) + 0.5
    y = ys.astype(np.float64) + 0.5
    A = np.stack([x, y, np.ones_like(x)], 1)
    rhs = x * x + y * y
    sol, *_ = np.linalg.lstsq(A, rhs, rcond=None)
    cx, cy = sol[0] / 2, sol[1] / 2
    r2 = sol[2] + cx * cx + cy * cy
    if r2 <= 0:
        return None
    r = math.sqrt(r2)
    res = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) - r
    return float(cx), float(cy), float(r), float(np.sqrt(np.mean(res ** 2)) / r)


def complete_circle(M, region, box, P):
    """A round image-intensifier field whose inside is partly flat (saturated air, collimator shading) is only
    partly textured, so its region covers part of the disk. Its rim against the black surround is still there:
    fit a circle (Kasa) to the region boundary pixels that touch black, and accept it when the rim is round
    (rms / r <= circle_rms_max), covers >= circle_min_arc_deg of arc, has a plausible radius, and the disk is
    >= circle_disk_nonblack non-black. Returns (cx, cy, r, rms_rel, disk bbox) at analysis scale, or None."""
    h, w = M["shape"]
    x0, y0, x1, y1 = box
    pad = int(0.6 * max(x1 - x0, y1 - y0))
    X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(w, x1 + pad), min(h, y1 + pad)
    reg = region[Y0:Y1, X0:X1]
    blk = ~M["nonblack"][Y0:Y1, X0:X1]
    rim = reg & ~sq_erode(reg, 1) & sq_dilate(blk, 1)
    ys, xs = np.where(rim)
    if xs.size < int(P["circle_min_rim_px"]):
        return None
    x = xs.astype(np.float64) + 0.5
    y = ys.astype(np.float64) + 0.5
    A = np.stack([x, y, np.ones_like(x)], 1)
    sol, *_ = np.linalg.lstsq(A, x * x + y * y, rcond=None)
    cx, cy = sol[0] / 2, sol[1] / 2
    r2 = sol[2] + cx * cx + cy * cy
    if r2 <= 0:
        return None
    r = math.sqrt(r2)
    rms = float(np.sqrt(np.mean((np.sqrt((x - cx) ** 2 + (y - cy) ** 2) - r) ** 2)) / r)
    if rms > float(P["circle_rms_max"]):
        return None
    if not (0.5 * min(x1 - x0, y1 - y0) <= r <= 0.75 * max(w, h)):
        return None
    ang = np.degrees(np.arctan2(y - cy, x - cx))
    occ = np.unique(np.floor((ang + 180.0) / 10.0).astype(int)).size * 10.0
    if occ < float(P["circle_min_arc_deg"]):
        return None
    cxa, cya = cx + X0, cy + Y0
    bx = (int(max(0, math.floor(cxa - r))), int(max(0, math.floor(cya - r))),
          int(min(w, math.ceil(cxa + r))), int(min(h, math.ceil(cya + r))))
    yy, xx = np.mgrid[bx[1]:bx[3], bx[0]:bx[2]]
    disk = (xx + 0.5 - cxa) ** 2 + (yy + 0.5 - cya) ** 2 <= r * r
    if disk.sum() == 0 or M["nonblack"][bx[1]:bx[3], bx[0]:bx[2]][disk].mean() < float(P["circle_disk_nonblack"]):
        return None
    return cxa, cya, r, rms, bx, occ


def iou(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    u = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / u if u > 0 else 0.0


def contain(a, b):
    """Fraction of box a inside box b."""
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    area = (a[2] - a[0]) * (a[3] - a[1])
    return ix * iy / area if area > 0 else 0.0


def detect(rgb, P):
    """All candidate boxes of one native RGB frame, accepted and rejected, with features and scores.
    Boxes are returned at native scale as [x0, y0, x1, y1) integers (x1, y1 exclusive)."""
    H, W = rgb.shape[:2]
    f = analysis_factor(W, H, P["analysis_max_side"])
    M = maps_from_rgb(rgb, f, P)
    h, w = M["shape"]
    seed = M["grey"] & M["nonblack"] & M["textured"]
    if P["open_px"] > 0:
        seed = sq_open(seed, int(P["open_px"]))
    core = sq_close(seed, int(P["close_px"]))
    core = ndi.binary_fill_holes(core)
    lab, n = ndi.label(core)
    sl = ndi.find_objects(lab)
    gm = M["grey"] & M["nonblack"]
    support = M["grey"] & (M["textured"] | ~M["nonblack"])
    min_side = int(P["min_side_px"])
    out = []
    for k, s in enumerate(sl, start=1):
        if s is None:
            continue
        hh, ww = s[0].stop - s[0].start, s[1].stop - s[1].start
        if hh < min_side or ww < min_side:
            continue
        pad = int(P["snap_px"]) + 1
        ys0, ys1 = max(0, s[0].start - pad), min(h, s[0].stop + pad)
        xs0, xs1 = max(0, s[1].start - pad), min(w, s[1].stop + pad)
        comp = lab[ys0:ys1, xs0:xs1] == k
        reg_local = gm[ys0:ys1, xs0:xs1] & sq_dilate(comp, int(P["snap_px"]))
        reg_local = ndi.binary_fill_holes(reg_local)
        region = np.zeros((h, w), bool)
        region[ys0:ys1, xs0:xs1] = reg_local
        for bx in xy_cut(region, (xs0, ys0, xs1, ys1), P):
            bx = refine_box(support, region, bx, float(P["trim_support"]), int(P["trim_band"]))
            if bx is None:
                continue
            completed = None
            if (bx[2] - bx[0]) >= min_side and (bx[3] - bx[1]) >= min_side:
                completed = complete_circle(M, region, bx, P)
            reg_f = region
            if completed is not None:
                cxa, cya, rr = completed[0], completed[1], completed[2]
                yy, xx = np.mgrid[0:h, 0:w]
                dmask = (xx + 0.5 - cxa) ** 2 + (yy + 0.5 - cya) ** 2 <= rr * rr
                rb = region[bx[1]:bx[3], bx[0]:bx[2]]
                inside = float((rb & dmask[bx[1]:bx[3], bx[0]:bx[2]]).sum()) / max(1, int(rb.sum()))
                # the disk must explain the region: >= circle_region_inside of it lies in the disk (burned-in title
                # text beside the field, joined by the closing, is then left out of the box)
                if inside >= float(P["circle_region_inside"]):
                    bx = completed[4]
                    reg_f = dmask & M["nonblack"]
                else:
                    completed = None
            bx0, by0, bx1, by1 = bx
            if (bx1 - bx0) < min_side or (by1 - by0) < min_side:
                continue
            feat = box_features(M, bx, reg_f)
            area_frac = (bx1 - bx0) * (by1 - by0) / float(w * h)
            score, gates, fail = score_features(feat, P, area_frac)
            shape, circle = "rect", None
            if completed is not None:
                shape = "circle"
                circle = [completed[0] * f, completed[1] * f, completed[2] * f, completed[3]]
            elif feat["fill"] < float(P["circle_fill_max"]):
                c = fit_circle(region[by0:by1, bx0:bx1])
                if c is not None and c[3] <= float(P["circle_rms_max"]):
                    shape = "circle"
                    circle = [(c[0] + bx0) * f, (c[1] + by0) * f, c[2] * f, c[3]]
            if shape == "circle" and gates.get("fill") is False and feat["fill"] >= float(P["circle_fill_min"]):
                gates["fill"] = True                      # a round field fills pi/4 of its box
                fail = next((kk for kk, ok in gates.items() if not ok), None)
            out.append(dict(box=[bx0 * f, by0 * f, bx1 * f, by1 * f], box_a=[bx0, by0, bx1, by1], f=f,
                            circle_completed=completed is not None,
                            area_frac=area_frac, score=score, gates=gates, reject=fail, accepted=fail is None,
                            shape=shape, circle=circle, **{k: feat[k] for k in ("purity", "texture", "entropy",
                                                                                 "fill", "aspect", "chroma_p90")}))
    # suppression among accepted candidates: a candidate lying >= nms_contain inside a LARGER accepted one is a
    # fragment of it (or text inside it)
    def _area(b):
        return (b[2] - b[0]) * (b[3] - b[1])
    acc = sorted([c for c in out if c["accepted"]], key=lambda c: (-_area(c["box"]), -c["score"], c["box"]))
    kept = []
    for c in acc:
        if any(contain(c["box"], k["box"]) >= float(P["nms_contain"]) for k in kept):
            c["accepted"] = False
            c["reject"] = "inside"
            continue
        kept.append(c)
    out.sort(key=lambda c: (not c["accepted"], -c["score"], c["box"]))
    return out[:int(P["max_candidates_kept"])], M


def fixed_box_score(rgb_crop, P, f):
    """The panel score of a FIXED box (the layout box) on one native frame: the crop at the same analysis scale."""
    M = maps_from_rgb(rgb_crop, f, P)
    h, w = M["shape"]
    feat = box_features(M, (0, 0, w, h), None)
    score, gates, fail = score_features(feat, P, None)
    gates.pop("aspect", None)
    fail = next((k for k, ok in gates.items() if not ok), None)
    return score, fail is None, fail, feat
