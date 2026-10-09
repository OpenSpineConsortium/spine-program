# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/timing.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""Timing inside a crop: duplicate frames, acquisition cadence, liveness, hard cuts, replays, clock fits.

Per native frame k of a segment the crop is reduced to a <= thumb_side greyscale thumbnail T_k (integer block
mean) and a 32x32 signature S_k (PIL box filter). Then
  d_k   = mean |T_k - T_{k-1}|                       (the image-change magnitude, grey levels)
  ncc_k = normalised cross-correlation of S_k and S_{k-1}
  phash = 64-bit DCT hash of S_k

DUPLICATES. The d_k of one segment are split in two classes by Otsu's threshold on log10(d + 0.01). The split is
accepted (the segment shows repeated frames between image updates) when the lower class median is <= dup_abs_max,
the upper median is >= dup_sep_ratio x the lower, and each class holds >= dup_min_class frames. Otherwise: if the
median d <= dup_abs_max the segment is static (every frame a duplicate except isolated jumps above
max(dup_abs_max, dup_outlier_k x median)), else every frame is a new image. The lower-class median is the
segment's noise floor (codec requantisation of a repeated image). An update that falls on a key frame and is
smaller than keyframe_guard x the threshold is re-labelled a duplicate: an I-frame refresh re-quantises a held image
and would otherwise read as a new pulse at the GOP period.

CADENCE. Intervals between consecutive image updates (pts, ms); the modal number of frames per image, the modal and
median interval, images per video second, and the run-length pattern.

LIVENESS. Fraction of 1-second pts windows holding >= 1 update: >= live_window_frac -> live, <= held_window_frac
-> held, else mixed.

CUTS. A hard cut before frame k when ncc_k < cut_ncc_max and d_k >= cut_min_d.

REPLAYS. Among image-update frames (first frame of each distinct image) of the whole video, in time order: a
pair (j, i), i < j, matches when the pHash Hamming distance <= replay_hamming_max AND the signature difference
mean |S_j - S_i| <= replay_rel_max x the median signature difference between consecutive updates of i's clip (a
replayed image is closer to its first showing than two successive pulses are to each other). A replay is a run of
>= replay_min_images consecutive updates matching consecutive earlier updates at a constant offset, starting >=
replay_min_gap_s after the matched run ends.
"""
from __future__ import annotations

import math

import numpy as np
from PIL import Image
from scipy.fft import dct

from .panels import block_mean


# ------------------------------------------------------------------------------------------------ signatures
def thumb(grey, side):
    f = max(1, int(math.ceil(max(grey.shape) / float(side))))
    return block_mean(grey, f)


def signature32(grey):
    im = Image.fromarray(grey).resize((32, 32), Image.BOX)
    return np.asarray(im, dtype=np.uint8)


def phash64(sig):
    d = dct(dct(sig.astype(np.float64), axis=0, norm="ortho"), axis=1, norm="ortho")[:8, :8].ravel()
    med = np.median(d[1:])
    bits = (d > med).astype(np.uint8)
    bits[0] = 0
    v = 0
    for b in bits:
        v = (v << 1) | int(b)
    return v


def ncc(a, b):
    a = a.astype(np.float64).ravel()
    b = b.astype(np.float64).ravel()
    a -= a.mean()
    b -= b.mean()
    den = math.sqrt(float((a * a).sum() * (b * b).sum()))
    if den <= 1e-9:
        return 1.0 if float(np.abs(a - b).max()) < 1e-9 else 0.0
    return float((a * b).sum() / den)


# ------------------------------------------------------------------------------------------------ duplicates
def otsu_1d(x, nbins=128):
    x = np.asarray(x, float)
    lo, hi = float(x.min()), float(x.max())
    if hi - lo < 1e-12:
        return None
    hist, edges = np.histogram(x, bins=nbins, range=(lo, hi))
    centres = 0.5 * (edges[:-1] + edges[1:])
    w0 = np.cumsum(hist)
    w1 = w0[-1] - w0
    m0 = np.cumsum(hist * centres)
    mt = m0[-1]
    with np.errstate(divide="ignore", invalid="ignore"):
        mu0 = m0 / w0
        mu1 = (mt - m0) / w1
        between = w0 * w1 * (mu0 - mu1) ** 2
    between[~np.isfinite(between)] = -1
    k = int(np.argmax(between))
    return float(edges[k + 1])


def classify_duplicates(d, key, P):
    """d: per-frame change magnitudes (d[0] is ignored: first frame of a clip is always an update).
    Returns (is_dup bool array, info dict)."""
    d = np.asarray(d, float)
    n = d.size
    is_dup = np.zeros(n, bool)
    info = dict(method=None, threshold=None, noise_floor=None, bimodal=False, lower_median=None, upper_median=None)
    if n < 2:
        info["method"] = "single frame"
        return is_dup, info
    x = d[1:]
    lx = np.log10(x + 0.01)
    thr_l = otsu_1d(lx)
    accepted = False
    if thr_l is not None:
        lo = x[lx <= thr_l]
        hi = x[lx > thr_l]
        if lo.size >= int(P["dup_min_class"]) and hi.size >= int(P["dup_min_class"]):
            mlo, mhi = float(np.median(lo)), float(np.median(hi))
            info.update(lower_median=mlo, upper_median=mhi)
            if mlo <= float(P["dup_abs_max"]) and mhi >= float(P["dup_sep_ratio"]) * max(mlo, 0.01):
                accepted = True
                thr = float(10 ** thr_l - 0.01)
                is_dup[1:] = x <= thr
                info.update(method="otsu-bimodal", threshold=thr, noise_floor=mlo, bimodal=True)
    if not accepted:
        med = float(np.median(x))
        if med <= float(P["dup_abs_max"]):
            thr = max(float(P["dup_abs_max"]), float(P["dup_outlier_k"]) * med)
            is_dup[1:] = x <= thr
            info.update(method="static: isolated jumps only", threshold=thr, noise_floor=med)
        else:
            info.update(method="every frame a new image (no duplicate class)", threshold=None, noise_floor=None)
    # key-frame guard
    key = np.asarray(key, bool)
    if info["threshold"] is not None:
        g = float(P["keyframe_guard"]) * info["threshold"]
        fix = (~is_dup) & key & (d <= g)
        fix[0] = False
        info["keyframe_relabelled"] = int(fix.sum())
        is_dup |= fix
    else:
        info["keyframe_relabelled"] = 0
    return is_dup, info


def cadence(pts_s, is_dup, key, P):
    """Acquisition cadence from the duplicate flags of one clip."""
    t = np.asarray(pts_s, float)
    upd = np.where(~np.asarray(is_dup, bool))[0]
    n = t.size
    out = dict(n_frames=int(n), n_updates=int(upd.size), n_duplicates=int(n - upd.size))
    if n == 0:
        return out
    runs = np.diff(np.concatenate([upd, [n]]))            # frames per distinct image
    out["frames_per_image_hist"] = {str(int(k)): int(v) for k, v in zip(*np.unique(runs, return_counts=True))}
    out["pattern_head"] = ",".join(str(int(r)) for r in runs[:48])
    if upd.size >= 2:
        iv = np.diff(t[upd]) * 1000.0
        runs_c = runs[:-1]                                 # the last run is truncated by the clip end
        vals, cnts = np.unique(runs_c, return_counts=True)
        modal_run = int(vals[np.argmax(cnts)])
        out["modal_frames_per_image"] = modal_run
        out["modal_frames_per_image_share"] = float(cnts.max() / cnts.sum())
        sel = iv[runs_c == modal_run]
        out["modal_interval_ms"] = float(np.median(sel)) if sel.size else None
        out["median_interval_ms"] = float(np.median(iv))
        out["mean_interval_ms"] = float(np.mean(iv))
        # the rate over the whole run of updates (robust to alternating patterns such as 2,3 for 12 images/s at
        # 30 fps, where the median interval flips between two values); the median-based rate is reported beside it
        tu = t[upd[-1]] - t[upd[0]]
        out["images_per_video_s"] = (upd.size - 1) / tu if tu > 0 else None
        out["images_per_video_s_from_median"] = 1000.0 / float(np.median(iv)) if np.median(iv) > 0 else None
        k = np.asarray(key, bool)
        out["updates_on_keyframes_frac"] = float(k[upd[1:]].mean()) if upd.size > 1 else None
        # the shortest regular pattern: the run lengths repeat with period p if they equal their shift by p on
        # >= 80% of positions (e.g. '4' for 7.5 images/s at 30 fps; '2,3' for 12 images/s at 30 fps)
        pat = None
        rc = runs_c.astype(int)
        for p in range(1, 7):
            if rc.size >= 3 * p and np.mean(rc[p:] == rc[:-p]) >= 0.8:
                # the most frequent p-run cycle, written from its smallest rotation (4 -> '4'; 3,2,3,2 -> '2,3')
                grams = {}
                for i in range(rc.size - p + 1):
                    g = tuple(int(v) for v in rc[i:i + p])
                    grams[g] = grams.get(g, 0) + 1
                best = max(sorted(grams), key=lambda g: grams[g])
                canon = min(best[k:] + best[:k] for k in range(p))
                pat = ",".join(str(v) for v in canon)
                break
        out["repeat_pattern"] = pat
    else:
        out.update(modal_frames_per_image=None, modal_interval_ms=None, median_interval_ms=None,
                   images_per_video_s=None, repeat_pattern=None, updates_on_keyframes_frac=None)
    # liveness
    if n >= 2 and t[-1] > t[0]:
        edges = np.arange(t[0], t[-1] + 1e-9, 1.0)
        if edges.size >= 2:
            has = []
            for a, b in zip(edges[:-1], edges[1:]):
                has.append(bool(np.any((t[upd[1:]] >= a) & (t[upd[1:]] < b))) if upd.size > 1 else False)
            frac = float(np.mean(has))
        else:
            frac = 1.0 if upd.size > 1 else 0.0
    else:
        frac = 0.0
    out["update_window_frac"] = frac
    if frac >= float(P["live_window_frac"]):
        out["liveness"] = "live"
    elif frac <= float(P["held_window_frac"]):
        out["liveness"] = "held"
    else:
        out["liveness"] = "mixed"
    return out


# ------------------------------------------------------------------------------------------------ replays
def popcount64(x):
    x = x.astype(np.uint64)
    c = np.zeros(x.shape, np.uint64)
    for s in range(0, 64, 8):
        c += _POP8[((x >> np.uint64(s)) & np.uint64(0xFF)).astype(np.intp)]
    return c.astype(np.int32)


_POP8 = np.array([bin(i).count("1") for i in range(256)], np.uint64)


def find_replays(upd, P):
    """upd: [dict(clip, u (update index within clip), t (pts_s), phash, sig (32x32 uint8), ref (median consecutive
    signature difference of its clip))] in time order. Returns a list of runs:
    dict(replay=[(clip, u)...], original=[(clip, u)...], n, offset)."""
    n = len(upd)
    if n < 2 * int(P["replay_min_images"]):
        return []
    H = np.array([u["phash"] for u in upd], dtype=np.uint64)
    S = np.stack([u["sig"].astype(np.float32) for u in upd])
    T = np.array([u["t"] for u in upd])
    ref = np.array([u["ref"] if u["ref"] else np.nan for u in upd], float)
    # a clip with fewer than two updates has no reference difference: the video-wide median stands in, and with
    # none at all only identical signatures can match (never a free pass)
    fill = float(np.nanmedian(ref)) if np.isfinite(ref).any() else 0.0
    ref[~np.isfinite(ref)] = fill
    hmax = int(P["replay_hamming_max"])
    rel = float(P["replay_rel_max"])
    match = {}
    for j in range(1, n):
        hd = popcount64(H[:j] ^ H[j])
        cand = np.where(hd <= hmax)[0]
        if cand.size == 0:
            continue
        dd = np.abs(S[cand] - S[j]).mean(axis=(1, 2))
        ok = dd <= rel * ref[cand]
        for i in cand[ok]:
            match.setdefault(int(j - i), set()).add(int(j))
    runs = []
    used = set()
    for off in sorted(match):
        js = sorted(match[off])
        cur = [js[0]]
        for j in js[1:] + [None]:
            if j is not None and j == cur[-1] + 1:
                cur.append(j)
                continue
            if len(cur) >= int(P["replay_min_images"]):
                i0, i1 = cur[0] - off, cur[-1] - off
                gap = T[cur[0]] - T[i1]
                if gap >= float(P["replay_min_gap_s"]) and not (set(cur) & used):
                    runs.append(dict(replay=[(upd[j]["clip"], upd[j]["u"]) for j in cur],
                                     original=[(upd[j - off]["clip"], upd[j - off]["u"]) for j in cur],
                                     n=len(cur), offset=off, t_replay=(float(T[cur[0]]), float(T[cur[-1]])),
                                     t_original=(float(T[i0]), float(T[i1]))))
                    used |= set(cur)
            if j is not None:
                cur = [j]
    runs.sort(key=lambda r: r["t_replay"])
    return runs


# ------------------------------------------------------------------------------------------------ clock fits
def theil_sen(x, y, min_dx):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    sl = []
    for i in range(x.size):
        dx = x[i + 1:] - x[i]
        ok = dx >= min_dx
        if ok.any():
            sl.append((y[i + 1:][ok] - y[i]) / dx[ok])
    if not sl:
        return None
    s = np.concatenate(sl)
    slope = float(np.median(s))
    icpt = float(np.median(y - slope * x))
    return dict(slope=slope, intercept=icpt, slope_p05=float(np.percentile(s, 5)),
                slope_p95=float(np.percentile(s, 95)), n_pairs=int(s.size))


def fit_clock(pts_s, clock_s, P, groups=None):
    """Clock seconds vs pts seconds. groups: a group label per point (clips); pairwise slopes are taken within a
    group only (a pooled fit with a free intercept per clip). Returns the fit or None with the reason."""
    x = np.asarray(pts_s, float)
    y = np.asarray(clock_s, float)
    g = np.asarray(groups if groups is not None else np.zeros(x.size, int))
    ok = np.isfinite(x) & np.isfinite(y)
    x, y, g = x[ok], y[ok], g[ok]
    if x.size < int(P["clock_min_points"]):
        return None, f"{x.size} clock readings < clock_min_points {P['clock_min_points']}"
    min_dx = float(P["clock_min_pair_dt_s"])
    slopes = []
    for gg in sorted(set(g.tolist())):
        m = g == gg
        xs, ys = x[m], y[m]
        for i in range(xs.size):
            dx = xs[i + 1:] - xs[i]
            sel = dx >= min_dx
            if sel.any():
                slopes.append((ys[i + 1:][sel] - ys[i]) / dx[sel])
    if not slopes:
        return None, "no reading pair spans clock_min_pair_dt_s"
    s = np.concatenate(slopes)
    slope = float(np.median(s))
    icpt = {gg: float(np.median(y[g == gg] - slope * x[g == gg])) for gg in sorted(set(g.tolist()))}
    res = y - slope * x - np.array([icpt[gg] for gg in g])
    inl = np.abs(res) <= float(P["clock_inlier_s"])
    span_clock = max((float(y[(g == gg) & inl].max() - y[(g == gg) & inl].min()) if ((g == gg) & inl).any() else 0.0)
                     for gg in set(g.tolist()))
    distinct = len(set(np.round(y[inl], 3).tolist()))
    fit = dict(slope=slope, slope_p05=float(np.percentile(s, 5)), slope_p95=float(np.percentile(s, 95)),
               n_points=int(x.size), n_inliers=int(inl.sum()), inlier_frac=float(inl.mean()),
               distinct_clock_values=distinct, clock_span_s=span_clock, n_pairs=int(s.size),
               residual_rms_s=float(np.sqrt(np.mean(res[inl] ** 2))) if inl.any() else None)
    why = None
    if inl.mean() < float(P["clock_min_inlier_frac"]):
        why = f"inlier fraction {inl.mean():.2f} < {P['clock_min_inlier_frac']}"
    elif distinct < int(P["clock_min_distinct"]):
        why = f"{distinct} distinct clock values < {P['clock_min_distinct']}"
    elif span_clock < float(P["clock_min_span_s"]):
        why = f"clock span {span_clock:.1f} s < {P['clock_min_span_s']}"
    elif not (float(P["speed_range"][0]) <= slope <= float(P["speed_range"][1])):
        why = f"slope {slope:.3f} outside speed_range {P['speed_range']}"
    fit["accepted"] = why is None
    return fit, why
