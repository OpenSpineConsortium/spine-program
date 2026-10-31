"""Calibration harness: the engine's Panjabi chords and candidate readings on a sample of real masks.

    python cal.py run --list sample.tsv --out out/ --workers 32
    python cal.py summary --out out/ --panjabi panjabi.csv

sample.tsv: path<TAB>scheme<TAB>source per line. Writes out/<study>.csv (level, key, value) and
the summary prints per-level means of each key beside Panjabi's.
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import sys
import traceback
from concurrent.futures import ProcessPoolExecutor

import numpy as np

NAN = float("nan")


def hole_extents(hole: np.ndarray, pixel: float):
    """The hole's widest row (x extent) and deepest column (y extent), in mm."""
    if hole is None or len(hole) < 3:
        return NAN, NAN
    rows = np.round((hole[:, 1] - hole[:, 1].min()) / pixel).astype(int)
    cols = np.round((hole[:, 0] - hole[:, 0].min()) / pixel).astype(int)
    w = max(np.ptp(hole[rows == r, 0]) for r in np.unique(rows)) + pixel
    d = max(np.ptp(hole[cols == c, 1]) for c in np.unique(cols)) + pixel
    return float(w), float(d)


def slabs_of(G, body, wall, grid, frame):
    fx, fy, fz = grid.footprint(frame.ex), grid.footprint(frame.ey), grid.footprint(frame.ez)
    core = body[G.central(body[:, 0], body[:, 1])]
    core = core if len(core) >= G.MIN_CHORD_POINTS else body
    height = float(core[:, 2].max() - core[:, 2].min()) + fz
    t = min(max(G.ENDPLATE_SHARE * height, G.ENDPLATE_MM[0]), G.ENDPLATE_MM[1])
    t = max(t, fz)
    inner = G.central(body[:, 0], body[:, 1])
    top = G.plate(body, inner, max(fx, fy), t, True, fz)
    bot = G.plate(body, inner, max(fx, fy), t, False, fz)
    return top, bot, fx, fy, fz


def width_front(G, slab, wall, depth, share, fx):
    keep = slab[slab[:, 1] >= wall + share * depth]
    return G.extent(keep[:, 0], fx) if len(keep) >= G.MIN_CHORD_POINTS else NAN


def profile_width(slab, wall, pixel, q):
    """The run of x-bins about the body's middle whose depth (front surface to the wall) is at
    least q of the middle's: the body's own sides, not what stands thin beside it."""
    if len(slab) < 20:
        return NAN
    x = slab[:, 0]
    xm = 0.5 * (x.min() + x.max())
    bins = np.floor((x - xm) / pixel).astype(int)
    depth = {}
    for b in np.unique(bins):
        ys = slab[bins == b, 1]
        depth[b] = ys.max() - max(ys.min(), wall)
    mid = [depth[b] for b in depth if abs(b) <= 1]
    if not mid:
        return NAN
    ref = float(np.median(mid))
    lo = hi = 0
    while (lo - 1) in depth and depth[lo - 1] >= q * ref:
        lo -= 1
    while (hi + 1) in depth and depth[hi + 1] >= q * ref:
        hi += 1
    return float((hi - lo + 1) * pixel)


def row_widths(slab, pixel, fx):
    """Each row's (y bin centre, width of the run of x-bins holding the row's middle), in the slab."""
    out = []
    yb = np.floor((slab[:, 1] - slab[:, 1].min()) / pixel).astype(int)
    for b in np.unique(yb):
        xs = np.sort(slab[yb == b, 0])
        if len(xs) < 2:
            continue
        xm = 0.5 * (xs.min() + xs.max())
        bins = set(np.floor((xs - xm) / pixel).astype(int))
        lo = hi = 0
        if 0 not in bins and -1 not in bins:
            continue
        lo = hi = 0 if 0 in bins else -1
        while lo - 1 in bins:
            lo -= 1
        while hi + 1 in bins:
            hi += 1
        out.append((float(slab[yb == b, 1].mean()), (hi - lo + 1) * pixel))
    return out


def plate_widths(slab, wall, pixel, fx, prefix, out):
    if len(slab) < 20:
        return
    front = slab[:, 1].max()
    depth = front - wall
    rows = row_widths(slab, pixel, fx)
    for f in (0.5, 0.6, 0.7, 0.8):
        ws = [w for y, w in rows if y >= front - f * depth]
        out["%s_rowmax_ant%02d" % (prefix, int(100 * f))] = max(ws) if ws else NAN
    mid = slab[np.abs(slab[:, 1] - (wall + 0.5 * depth)) <= max(1.5, 0.5 * pixel)]
    out["%s_midband" % prefix] = (np.ptp(mid[:, 0]) + fx) if len(mid) >= 3 else NAN
    ws = sorted(w for y, w in rows)
    if ws:
        out["%s_rowmax" % prefix] = ws[-1]
    near = slab[np.abs(slab[:, 0] - 0.5 * (slab[:, 0].min() + slab[:, 0].max())) <= 3.0]
    out["%s_depth_mid" % prefix] = (near[:, 1].max() - wall + 0.5 * pixel) if len(near) else NAN


# ---- the canal on the CT itself: canal contents flood-filled from a seed behind the body, bounded by
# bone at the half-maximum between the canal's level and the bone's (the relative 50 per cent edge rule;
# the soft-tissue window and flood fill of Radnostics US 8,891,848 and Yao 2006), sampled at STEP mm in
# the vertebra's frame ----
STEP = 0.25


def ct_plane(ct, inv, frame, z, xs, ys):
    from scipy import ndimage
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    world = frame.origin + X[..., None] * frame.ex + Y[..., None] * frame.ey + z * frame.ez
    ijk = world.reshape(-1, 3) @ inv[:3, :3].T + inv[:3, 3]
    vals = ndimage.map_coordinates(ct, ijk.T, order=1, mode="nearest")
    return vals.reshape(X.shape)


def canal_in_plane(img, seed, thr):
    """The canal at one threshold: the region below thr holding the seed, its widest row through the
    seed's column and its depth along that column, or the reason it is not read."""
    from scipy import ndimage
    soft = img < thr
    if not soft[seed]:
        return "seed in bone"
    lab, n = ndimage.label(soft)
    reg = lab == lab[seed]
    if reg[0, :].any() or reg[-1, :].any() or reg[:, 0].any() or reg[:, -1].any():
        return "open"
    area = reg.sum() * STEP * STEP
    if not (40.0 <= area <= 700.0):
        return "size"
    c = seed[0]
    depth = reg[c, :].sum() * STEP
    best = 0.0
    for j in np.flatnonzero(reg[c, :]):
        r = reg[:, j]
        lo = hi = c
        while lo - 1 >= 0 and r[lo - 1]:
            lo -= 1
        while hi + 1 < len(r) and r[hi + 1]:
            hi += 1
        best = max(best, (hi - lo + 1) * STEP)
    return best, depth


def ct_canal(v, ct, inv):
    rings = v.full_rings() or v.slabs
    if not rings:
        return {}
    B = v.body_pts
    zb = (float(B[:, 2].min()), float(B[:, 2].max()))
    zs = np.arange(zb[0], zb[1] + 1e-6, 0.5)
    mid, wall = v.midline, v.wall
    xs = np.arange(mid - 22.0, mid + 22.0 + 1e-9, STEP)
    ys = np.arange(wall - 32.0, wall + 4.0 + 1e-9, STEP)
    seed = (int(round((mid - xs[0]) / STEP)), int(round((wall - 5.0 - ys[0]) / STEP)))
    out, why = {}, {}
    for name, rule in (("t150", lambda c, b: 150.0), ("t200", lambda c, b: 200.0), ("half", lambda c, b: 0.5 * (c + b))):
        widths, depths = [], []
        for z in zs:
            img = ct_plane(ct, inv, v.frame, z, xs, ys)
            canal_level = float(np.median(img[max(seed[0] - 6, 0):seed[0] + 7, max(seed[1] - 6, 0):seed[1] + 7]))
            bone_level = float(np.percentile(img, 99))
            got = canal_in_plane(img, seed, rule(canal_level, bone_level))
            if isinstance(got, str):
                why[got] = why.get(got, 0) + 1
                continue
            widths.append(got[0])
            depths.append(got[1])
        if widths:
            out["ct_%s_scw" % name] = float(np.median(widths))
            out["ct_%s_scw_max" % name] = float(np.max(widths))
            out["ct_%s_scd" % name] = float(np.median(depths))
            out["ct_%s_slabs" % name] = float(len(widths))
        else:
            out["ct_%s_slabs" % name] = 0.0
    for k, n in why.items():
        out["ct_why_" + k.replace(" ", "_")] = float(n)
    return out

def candidates(A, G, CANAL, v, vals):
    out = {}
    B = A.square_to_wall(v, v.body_pts)
    wall = v.wall_y0
    if len(B) >= G.MIN_BODY_VOXELS:
        top, bot, fx, fy, fz = slabs_of(G, B, wall, v.grid, v.frame)
        depth = G.surface(B[:, 1], True, fy) - wall
        for share in (0.15, 0.25, 0.35, 0.5):
            out["epw_front%02d" % int(100 * share)] = width_front(G, top, wall, depth, share, fx)
        for q in (0.4, 0.5, 0.6, 0.7):
            out["epw_prof%02d" % int(100 * q)] = profile_width(top, wall, v.pixel, q)
        plate_widths(top, wall, v.pixel, fx, "epu", out)
        plate_widths(bot, wall, v.pixel, fx, "epl", out)
        for name, slab_top in (("u", True), ("l", False)):
            inner = G.central(B[:, 0], B[:, 1])
            c = G.plate_plane(B, inner, max(fx, fy), slab_top, fz)
            d = B[:, 2] - (c[0] + c[1] * B[:, 0] + c[2] * B[:, 1])
            if not slab_top:
                d = -d
            t = max(min(max(G.ENDPLATE_SHARE * (np.ptp(B[:, 2]) + fz), G.ENDPLATE_MM[0]), G.ENDPLATE_MM[1]), fz)
            for up, label in ((0.5 * fz, "half"), (1.0, "1mm"), (2.0, "2mm"), (max(fz, 2.0), "layer")):
                band = B[(d >= -t - 1e-6) & (d <= up + 1e-6)]
                out["ep%s_band_%s" % (name, label)] = G.extent(band[:, 0], fx) if len(band) >= G.MIN_CHORD_POINTS else NAN
                plate_widths(band, wall, v.pixel, fx, "ep%s_band_%s" % (name, label), out)
                if len(band) >= 20:
                    for q in (0.5, 0.6):
                        out["ep%s_band_%s_prof%02d" % (name, label, int(100 * q))] = profile_width(band, wall, v.pixel, q)
        mid = B[np.abs(B[:, 2] - 0.5 * (B[:, 2].min() + B[:, 2].max())) <= max(0.5 * fz, 1.0)]
        for q in (0.4, 0.5, 0.6, 0.7):
            out["mid_prof%02d" % int(100 * q)] = profile_width(mid, wall, v.pixel, q)
    if v.level.startswith("C"):
        front = G.connected_front(v.idx, A.square_to_wall(v, v.loc), v.wall_y0, v.grid.shape)
        F = A.square_to_wall(v, v.loc[front])
        if len(F) >= G.MIN_BODY_VOXELS:
            top, bot, fx, fy, fz = slabs_of(G, F, wall, v.grid, v.frame)
            out["epw_unclipped"] = G.extent(top[:, 0], fx)
            for q in (0.4, 0.5, 0.6, 0.7):
                out["epwfront_prof%02d" % int(100 * q)] = profile_width(top, wall, v.pixel, q)
                mid = F[np.abs(F[:, 2] - np.median(F[:, 2])) <= max(fz, 1.0)]
                out["midfront_prof%02d" % int(100 * q)] = profile_width(mid, wall, v.pixel, q)
    zb = CANAL.body_span(v)
    q = 0.25 * (zb[1] - zb[0])
    rings = [s for s in v.full_rings() if zb[0] + q <= s.z <= zb[1] - q] or v.full_rings()
    ext = [hole_extents(s.hole, v.pixel) for s in rings]
    if ext:
        out["hole_max_w"] = float(np.median([e[0] for e in ext]))
        out["hole_max_ap"] = float(np.median([e[1] for e in ext]))
        out["hole_max_w_max"] = float(np.max([e[0] for e in ext]))
        out["ring_ap_max"] = float(np.max([s.ap for s in rings]))
        out["ring_w_max"] = float(np.max([s.width for s in rings]))
        out["n_rings"] = float(len(rings))
    return out


def lean_candidates(A, G, v, ct, inv):
    """The fixed readings: each end plate's width over the front half of its plate, below anything that
    rises beyond the plate's plane (uncinates, lips), and its depth at the midline; the canal on the CT
    at 200 HU, median over the enclosed slabs."""
    out = {}
    B = A.square_to_wall(v, v.body_pts)
    wall = v.wall_y0
    if len(B) >= G.MIN_BODY_VOXELS:
        fx, fy, fz = v.grid.footprint(v.frame.ex), v.grid.footprint(v.frame.ey), v.grid.footprint(v.frame.ez)
        inner = G.central(B[:, 0], B[:, 1])
        t = max(min(max(G.ENDPLATE_SHARE * (np.ptp(B[:, 2]) + fz), G.ENDPLATE_MM[0]), G.ENDPLATE_MM[1]), fz)
        for name, top in (("u", True), ("l", False)):
            c = G.plate_plane(B, inner, max(fx, fy), top, fz)
            d = B[:, 2] - (c[0] + c[1] * B[:, 0] + c[2] * B[:, 1])
            d = d if top else -d
            band = B[(d >= -t - 1e-6) & (d <= 0.5 * fz + 1e-6)]
            got = {}
            plate_widths(band, wall, v.pixel, fx, "x", got)
            out["plate_w_" + name] = got.get("x_rowmax_ant50", NAN)
            out["plate_d_" + name] = got.get("x_depth_mid", NAN)
    if ct is not None:
        got = ct_canal_lean(v, ct, inv)
        out.update(got)
    return out


def ct_canal_lean(v, ct, inv):
    B = v.body_pts
    if not len(B):
        return {}
    zs = np.arange(float(B[:, 2].min()), float(B[:, 2].max()) + 1e-6, 0.5)
    mid, wall = v.midline, v.wall
    xs = np.arange(mid - 22.0, mid + 22.0 + 1e-9, STEP)
    ys = np.arange(wall - 32.0, wall + 4.0 + 1e-9, STEP)
    seed = (int(round((mid - xs[0]) / STEP)), int(round((wall - 5.0 - ys[0]) / STEP)))
    widths, depths = [], []
    for z in zs:
        got = canal_in_plane(ct_plane(ct, inv, v.frame, z, xs, ys), seed, 200.0)
        if not isinstance(got, str):
            widths.append(got[0])
            depths.append(got[1])
    if not widths:
        return {"ct_slabs": 0.0}
    return {"ct_scw": float(np.median(widths)), "ct_scd": float(np.median(depths)), "ct_slabs": float(len(widths))}


def one(job):
    path, scheme, source, ctpath, outdir = job
    study = os.path.basename(path).split(".")[0]
    dest = os.path.join(outdir, "%s-%s.csv" % (source, study))
    if os.path.exists(dest):
        return dest
    try:
        from scanimport import volume as V
        from scanimport import geometry as G
        from morphometry import measure as M
        from morphometry import anatomy as A
        from morphometry import canal as CANAL
        vol, grid, names, problems, _ = V.read_labels(path, scheme)
        ct = inv = None
        if ctpath:
            import nibabel as nib
            img = nib.load(ctpath)
            ct = np.asarray(img.dataobj, dtype=np.float32)
            inv = np.linalg.inv(img.affine)
        keep = {}
        rows = M.measure_volume(vol, grid, names, study, pelvis=False, keep=keep)
        flags = {}
        for r in rows:
            if str(r["key"]).startswith("flag:"):
                flags.setdefault(r["level"], set()).add(r["key"][5:])
        out = []
        for lv, v in keep.get("verts", {}).items():
            vals = keep["values"][lv]
            for k in ("endplate", "endplate_depth", "endplate_lower", "endplate_lower_depth", "canal_w", "canal_ap",
                      "interpedicular", "interpedicular_max", "canal_ap_min", "body_w_mid", "body_d_mid"):
                out.append((lv, k, vals.get(k, NAN)))
            try:
                if os.environ.get("CAL_LEAN"):
                    for k, x in lean_candidates(A, G, v, ct, inv).items():
                        out.append((lv, k, x))
                else:
                    for k, x in candidates(A, G, CANAL, v, vals).items():
                        out.append((lv, k, x))
                    if ct is not None:
                        for k, x in ct_canal(v, ct, inv).items():
                            out.append((lv, k, x))
            except Exception as exc:  # noqa: BLE001
                out.append((lv, "candidate_error:" + type(exc).__name__ + ":" + str(exc)[:60].replace(",", ";"), NAN))
            for f in sorted(flags.get(lv, ())):
                out.append((lv, "flag:" + f, 1.0))
        with open(dest + ".tmp", "w", newline="") as h:
            w = csv.writer(h)
            w.writerow(["source", "study", "level", "key", "value"])
            for lv, k, x in out:
                w.writerow([source, study, lv, k, "" if x is None or (isinstance(x, float) and not math.isfinite(x)) else "%.4f" % x])
        os.replace(dest + ".tmp", dest)
    except Exception:  # noqa: BLE001
        with open(dest + ".err", "w") as h:
            h.write(traceback.format_exc())
    return dest


def run(a):
    os.makedirs(a.out, exist_ok=True)
    jobs = []
    for line in open(a.list):
        if line.strip():
            parts = line.rstrip("\n").split("\t")
            path, scheme, source = parts[:3]
            ctpath = parts[3] if len(parts) > 3 else ""
            jobs.append((path, scheme, source, ctpath, a.out))
    with ProcessPoolExecutor(a.workers) as pool:
        for k, done in enumerate(pool.map(one, jobs), 1):
            if k % 10 == 0:
                print(k, "of", len(jobs), flush=True)


def summary(a):
    pan = {}
    for r in csv.DictReader(l for l in open(a.panjabi) if not l.startswith("#")):
        pan[(r["measure"], r["level"])] = float(r["mean"])
    vals = {}
    for name in os.listdir(a.out):
        if not name.endswith(".csv"):
            continue
        for r in csv.DictReader(open(os.path.join(a.out, name))):
            if r["value"]:
                vals.setdefault((r["key"], r["level"]), []).append(float(r["value"]))
                vals.setdefault((r["key"] + "@" + r["source"], r["level"]), []).append(float(r["value"]))
    levels = ["C2", "C3", "C4", "C5", "C6", "C7"] + ["T%d" % i for i in range(1, 13)] + ["L%d" % i for i in range(1, 6)]
    keys = sorted({k for k, _ in vals})
    with open(os.path.join(a.out, "..", "summary.tsv"), "w") as h:
        h.write("key\t" + "\t".join(levels) + "\n")
        for k in keys:
            h.write(k + "\t" + "\t".join("%.2f|%d" % (np.mean(vals[(k, l)]), len(vals[(k, l)])) if (k, l) in vals else ""
                                        for l in levels) + "\n")
        for m in ("endplate", "endplate_depth", "canal_w", "canal_ap"):
            h.write("PANJABI_" + m + "\t" + "\t".join("%.2f" % pan[(m, l)] if (m, l) in pan else "" for l in levels) + "\n")
    print("summary written")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--list", required=True)
    r.add_argument("--out", required=True)
    r.add_argument("--workers", type=int, default=32)
    s = sub.add_parser("summary")
    s.add_argument("--out", required=True)
    s.add_argument("--panjabi", required=True)
    a = p.parse_args()
    {"run": run, "summary": summary}[a.cmd](a)


if __name__ == "__main__":
    main()
