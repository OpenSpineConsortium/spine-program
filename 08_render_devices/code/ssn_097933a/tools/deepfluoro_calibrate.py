#!/usr/bin/env python
"""Calibrate the device terms of image formation on DeepFluoro's pairs, leave-one-specimen-out.

WHAT IS FITTED, AND WHY ONLY THIS. Exact geometry plus the repo's polyenergetic attenuation explains
81 % of a real frame's attenuation variance with no detector term at all (deepfluoro_residual_all.py).
The residual has a shape that a few parameters describe -- a radial field with one sign in 89 % of
frames, a lateral gradient that reverses with rot-180-for-up, an unsharp-mask halo on every cortical
edge, a scatter pedestal -- and a per-frame remainder that no published learned model has turned into
a downstream gain (docs/DEEPFLUORO_FORMATION.md, section 3). So this fits the parametric part and
stops. Every term is a property of the beam or the detector, never of the anatomy, which is what
applying it to a thoracic or cervical volume requires. Nothing here can move a label.

THE FORWARD MODEL, in the order the physics imposes it, on the water/bone path maps the ray-caster
already produced:

    T      = polyenergetic transmission, with a bone-path scale kb (spectrum hardness in one number)
    T_s    = (1 - s) T + s G[sigma_s] T                    scatter pedestal
    T_d    = G[sigma_r] T_s                                receptor blur
    T_d    = T_d + alpha (T_d - G[sigma_u] T_d)            vendor edge enhancement
    T_f    = T_d (1 + b r^2 + c u' + d v)                  vignette, heel (u' flips with rot-180), tilt
    a_hat  = k_f (-log T_f) + c_f                          PER-FRAME linear display match, as the baseline

Nine global parameters. The display match is per frame because the C-arm windows each frame on its
own; a global curve cannot fit an arbitrary per-acquisition scale, and the baseline uses the same
per-frame match, so any gain is the nine device terms and nothing else. Fitted by least squares on
pixels that are exposed, away from the collimator ring,
and NOT truncated -- a ray that entered or left the CT's bounding box through tissue is a hole in the
volume, not a formation term, and both of the worst-agreeing frames were exactly that.

LEAVE-ONE-SPECIMEN-OUT, because the literature's one documented collapse was on the specimen whose
poses lay outside the others' cluster. The number that matters is the held-out specimen's explained
variance against the uncalibrated baseline (81 %), and the spread of each fitted parameter across
folds: a device-fixed term should come out the same whichever specimen is held out.

    python tools/deepfluoro_calibrate.py --pairs ~/model_night/deepfluoro/pairs --fit-frames 60
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

# Nine GLOBAL parameters, all properties of the beam or the detector. The display curve is NOT among
# them: the C-arm windows every frame on its own, so the real image's intensity scale is arbitrary per
# acquisition and a global curve cannot fit it -- the first dry run put explained variance at
# -498,295 % and slammed the curve's parameters into their bounds. The match is therefore per frame
# and linear, exactly as the uncalibrated baseline's is, so any gain is attributable to these nine.
NAMES = ["kb", "s", "sigma_s", "sigma_r", "alpha", "sigma_u", "b", "c", "d"]
LO = np.array([0.5, 0.00, 4.0, 0.3, 0.0, 1.0, -0.6, -0.3, -0.3])
HI = np.array([2.5, 0.70, 60.0, 3.0, 2.0, 8.0, 0.6, 0.3, 0.3])   # kb was pinned at 1.6 in every fold
X0 = np.array([1.0, 0.25, 20.0, 0.8, 0.3, 3.0, 0.0, 0.0, 0.0])
# --fix NAME=value takes a term out of the optimiser at that value; --bounds NAME=lo:hi narrows or widens
# its box. The first fit left the scatter width anywhere from 5 to 60 px across folds and kb at its
# upper bound in every one: the first is the term to constrain, the second the term to let run so the
# bone model's defect can be sized.
FREE = np.ones(len(NAMES), dtype=bool)
_FRAMES = []          # inherited by forked workers, so only theta and an index cross the pipe


def gauss(a, s):
    from scipy.ndimage import gaussian_filter
    return gaussian_filter(a, s, mode="nearest") if s > 0.05 else a


# HOW THE STORED REAL FRAME IS READ. The stored DeepFluoro intensity was taken to be transmission-like and
# converted with -log. Measured on every pair (tools/deepfluoro_transfer.py, 2026-09-21): the stored intensity is
# a nearly straight, slightly concave DECREASING function of the model attenuation (exp(-B a) fits only with
# B = 0.15, where transmission would give B = 1), i.e. the device stores a log-compressed display image. -log of
# it is a log of a log, and every term was fitted against that bent target -- the symptom was a display exponent
# of two lifting held-out variance by three points. "linear" reads the stored frame as attenuation with a sign
# flip; "log" is the old reading, kept so that every earlier number can be reproduced. Set by --conversion on
# the calibration or by the environment variable DF_CONVERSION for every tool that imports this module.
CONVERSION = os.environ.get("DF_CONVERSION", "log")


def real_to_atten(rd, field=None, floor=0.02):
    """The stored REAL frame as attenuation, by the reading CONVERSION names; the synthetic side never comes here."""
    if CONVERSION == "linear":
        f = rd[field] if field is not None and field.any() else rd
        p2, p98 = np.percentile(f, (2, 98))
        return (p98 - rd) / max(p98 - p2, 1e-6)
    if CONVERSION != "log":
        raise SystemExit(f"unknown conversion {CONVERSION!r}: log or linear")
    return raw_to_atten(rd, field, floor)


def synth_to_atten(T, field=None, floor=0.02, photons=None):
    """A SYNTHETIC frame's transmission as attenuation, matched to how the real frame is read.

    Under the "log" reading the real frame goes through raw_to_atten, so the synthetic one did too (its own
    2nd-percentile transmission subtracted before the log, a 2 % floor). Under the "linear" reading the real
    frame is the device's log image read linearly, so the synthetic counterpart is the plain -log of the
    transmission -- exactly what forward() returns and what the terms were fitted on. Subtracting the frame's
    own low percentile of TRANSMISSION before the log bends the pixels near that percentile (in a pelvis, the
    thickest bone) and so changes thin-bone contrast relative to thick after a window. Suspected cause of the
    displayed thin-bone deficit (+57/+65 grey at 0.5-1.5 cm of bone) that survived the fix to the real side
    while the attenuation-domain deficit vanished; tested by rebuilding the pairs roots under this conversion.
    A pixel that counted zero photons is floored at half a count, so it is a bounded black, not 13.8.
    """
    if CONVERSION == "linear":
        tfloor = 0.5 / photons if photons else 1e-6
        return -np.log(np.clip(T, tfloor, None))
    return raw_to_atten(T, field, floor)


def raw_to_atten(rd, field=None, floor=0.02):
    """A device's transmission-like output as attenuation, ONE way for real and synthetic frames.

    The frame's own 2nd percentile is its black level and is subtracted, so the attenuation always spans
    the frame's own raw range -- the thinnest tissue at zero, the densest bone at the top -- which is
    what a C-arm's automatic window does and what makes soft tissue dark and bone bright on a real
    frame; the floor at `floor` of the p2-p98 range bounds a zero-count pixel to the same black it is on
    the device. The real test frames and the calibration pairs were always converted this way; the
    synthetic frames were not, and came out a hundred grey levels brighter than the frames they are
    tested against, with a whole frame white when the body filled it.
    """
    f = rd[field] if field is not None and field.any() else rd
    p2, p98 = np.percentile(f, (2, 98))
    rng_ = max(p98 - p2, 1e-6)
    return -np.log(np.clip(rd - p2 + floor * rng_, floor * rng_, None))


def load_pair(p):
    z = np.load(p)
    real = z["real"].astype(np.float64); hit = z["hit"].astype(bool)
    trunc = z["trunc"].astype(bool) if "trunc" in z else np.zeros_like(hit)
    p2 = np.percentile(real[hit], 2)
    atten = real_to_atten(real, hit)
    from scipy.ndimage import binary_erosion
    m = binary_erosion(hit & (real > p2), iterations=max(6, int(0.06 * min(hit.shape)))) & ~trunc
    h, w = hit.shape
    yy, xx = np.mgrid[0:h, 0:w]
    u = (xx - w / 2) / (w / 2); v = (yy - h / 2) / (h / 2)
    stem = Path(p).stem.replace("pair_", ""); spec, pid = stem.rsplit("_", 1)
    return dict(spec=spec, pid=pid, water=z["water_cm"].astype(np.float64), bone=z["bone_cm"].astype(np.float64),
                atten=atten, m=m, u=u, v=v, r2=u * u + v * v, rot=int(z["rot"]) if "rot" in z else 0,
                trunc_frac=float(trunc.mean()))


def matched(x, d, m=None):
    """Per-frame linear match of the model attenuation x onto the real attenuation scale."""
    mm = d["m"] if m is None else m
    xs, ys = x[mm], d["atten"][mm]
    k, c0 = np.linalg.lstsq(np.c_[xs, np.ones_like(xs)], ys, rcond=None)[0]
    return k * x + c0


def forward(theta, d, RP):
    """The model attenuation -log T_f under theta, BEFORE the per-frame display match."""
    kb, s, sg_s, sg_r, alpha, sg_u, b, c, dd = theta
    E, S, muw, mub = RP
    T = np.zeros_like(d["water"])
    for k in range(len(E)):
        T += S[k] * E[k] * np.exp(-(muw[k] * d["water"] + kb * mub[k] * d["bone"]))
    T /= (S * E).sum()
    T = (1 - s) * T + s * gauss(T, sg_s)
    T = gauss(T, sg_r)
    T = T + alpha * (T - gauss(T, sg_u))
    up = -d["u"] if d["rot"] else d["u"]
    T = T * (1.0 + b * d["r2"] + c * up + dd * d["v"])
    return -np.log(np.clip(T, 1e-6, None))


def forward_noisy(theta, d, RP, photons, rng, floor=0.02, hit=None):
    """The model attenuation with a quantum draw IN THE PLACE THE PHYSICS PUTS IT.

    Photons are counted at the detector entrance, after scatter and before the receptor's own blur, so
    the grain in a real frame is Poisson noise smoothed by sigma_r and then sharpened by the vendor's
    edge enhancement -- which is why the noise-floor tool reads the stochastic share from the 0-2 px band
    and not the 0-1 px band. spine_project.py first drew the noise on the finished frame instead, white
    noise on top of a blurred image, and that is a grain no fluoroscope produces. `photons` is the count
    per rendered pixel at unit transmission, at whatever downsampling the water/bone maps were cast at.

    With `floor` > 0 the device's transmission is converted by raw_to_atten, the SAME function that
    converts a real frame: its own black level subtracted, a 2 % floor. A pixel that counted zero
    photons is then the same bounded black it is on the device, not an attenuation of 13.8 that wrecks
    every percentile window downstream (the first synthetic set had featureless white and black frames
    for exactly that reason), and the display spans the frame's own range as a C-arm's does.
    """
    kb, s, sg_s, sg_r, alpha, sg_u, b, c, dd = theta
    E, S, muw, mub = RP
    T = np.zeros_like(d["water"])
    for k in range(len(E)):
        T += S[k] * E[k] * np.exp(-(muw[k] * d["water"] + kb * mub[k] * d["bone"]))
    T /= (S * E).sum()
    T = (1 - s) * T + s * gauss(T, sg_s)
    T = rng.poisson(np.clip(T, 1e-6, None) * photons).astype(np.float64) / photons
    T = gauss(T, sg_r)
    T = T + alpha * (T - gauss(T, sg_u))
    up = -d["u"] if d["rot"] else d["u"]
    T = T * (1.0 + b * d["r2"] + c * up + dd * d["v"])
    if floor and floor > 0:
        return synth_to_atten(T, hit, floor, photons)
    return -np.log(np.clip(T, 1e-6, None))


def _sse_one(args):
    i, theta, RP = args
    d = _FRAMES[i]
    a_hat = matched(forward(theta, d, RP), d)
    m = d["m"]; r = d["atten"][m] - a_hat[m]
    return float((r * r).sum()), float(((d["atten"][m] - d["atten"][m].mean()) ** 2).sum())


def explained(theta, frames, RP, sub=None):
    num = den = 0.0
    for d in frames:
        a_hat = matched(forward(theta, d, RP), d)
        m = d["m"]
        if sub is not None:
            m = m & sub[d["spec"], d["pid"]]
        r = d["atten"][m] - a_hat[m]
        num += float((r * r).sum()); den += float(((d["atten"][m] - d["atten"][m].mean()) ** 2).sum())
    return 1.0 - num / max(den, 1e-12)


def baseline_explained(frames):
    """Uncalibrated physics with a least-squares intensity match: the 81 % number, on these pixels."""
    import render_physics_drr as RP_
    RP = (RP_.ENERGIES.numpy(), RP_.SPECTRUM.numpy(), RP_.MU_WATER.numpy(), RP_.MU_BONE.numpy())
    num = den = 0.0
    for d in frames:
        th = X0.copy(); th[[1, 4, 6, 7, 8]] = 0.0; th[3] = 0.0     # no scatter, blur, halo or field
        x = matched(forward(th, d, RP), d)
        m = d["m"]; ys = d["atten"][m]; r = ys - x[m]
        num += float((r * r).sum()); den += float(((ys - ys.mean()) ** 2).sum())
    return 1.0 - num / max(den, 1e-12)


def fit(train_idx, RP, workers=8, seed=0, maxiter=60):
    """Minimise the per-frame-matched residual over the nine device parameters.

    Frames are inherited by forked workers through _FRAMES; each evaluation ships only theta and an
    index, so a 40-frame loss costs one forward per frame across the pool, not a 200 MB pickle.
    """
    from multiprocessing import get_context
    from scipy.optimize import minimize
    ctx = get_context("fork")
    # optimise in z in [0,1]^9 with theta = LO + z (HI - LO): the first run left sigma_s exactly at its
    # start in all six folds because eps = 1e-3 on a parameter of scale 20 px moved nothing, while the
    # same eps on the scatter fraction (scale 0.7) was a large step. One scale for every parameter.
    F = FREE
    span = np.where(F, HI - LO, 1.0)

    def to_th(z):
        th = X0.copy()
        th[F] = LO[F] + np.asarray(z) * span[F]
        return th
    z0 = ((X0 - LO) / span)[F]
    with ctx.Pool(workers) as pool:
        def loss(z):
            th = to_th(z)
            out = pool.map(_sse_one, [(i, th, RP) for i in train_idx])
            return float(sum(a for a, _ in out) / max(sum(b for _, b in out), 1e-12))
        l0 = loss(z0)
        res = minimize(loss, z0, method="L-BFGS-B", bounds=[(0.0, 1.0)] * int(F.sum()),
                       options=dict(maxiter=maxiter, eps=1e-2))
    return to_th(res.x), float(res.fun), int(res.nit), l0


def apply_overrides(fixes, bounds):
    """--fix NAME=value pins a term at value (X0 holds it, FREE drops it); --bounds NAME=lo:hi resets its box."""
    for spec in bounds or []:
        n, rng_ = spec.split("="); lo, hi = (float(t) for t in rng_.split(":"))
        i = NAMES.index(n); LO[i] = lo; HI[i] = hi; X0[i] = float(np.clip(X0[i], lo, hi))
    for spec in fixes or []:
        n, v = spec.split("="); i = NAMES.index(n)
        X0[i] = float(v); FREE[i] = False
    if fixes or bounds:
        print("terms:", "  ".join(f"{n}={X0[i]:g}(fixed)" if not FREE[i] else f"{n}[{LO[i]:g},{HI[i]:g}]"
                                  for i, n in enumerate(NAMES)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", default="~/model_night/deepfluoro/pairs")
    ap.add_argument("--fit-frames", type=int, default=60, help="frames drawn from the training specimens per fold")
    ap.add_argument("--out", default="~/model_night/deepfluoro/calibration.json")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--workers", type=int, default=int(os.environ.get("SLURM_CPUS_PER_TASK", 8)))
    ap.add_argument("--maxiter", type=int, default=60)
    ap.add_argument("--poses", default="~/model_night/deepfluoro/poses.json",
                    help="per-frame lateral tilt, for the held-out-by-view-angle folds")
    ap.add_argument("--angle-folds", action="store_true",
                    help="also fit on |lateral tilt| <= 8 deg and test on >= 15 deg, and the reverse. "
                         "DeepFluoro is near-AP; a spine sweep is lateral. This measures whether the "
                         "calibration extrapolates in view angle rather than assuming it.")
    ap.add_argument("--angle-bins", action="store_true",
                    help="fit the terms separately inside |lateral tilt| bins (<=8, 8-15, >=15 deg) and "
                         "report each term's slope per degree, and whether per-angle terms beat the "
                         "global ones on held-out frames of the same bin. The regression of the device "
                         "terms on view angle, measured rather than assumed.")
    ap.add_argument("--global-theta", default="~/model_night/deepfluoro/calibration.json",
                    help="the LOSO calibration whose median terms the per-angle terms are scored against")
    ap.add_argument("--fix", action="append", metavar="NAME=VALUE", help="pin a term (repeatable)")
    ap.add_argument("--bounds", action="append", metavar="NAME=LO:HI", help="reset a term's box (repeatable)")
    ap.add_argument("--skip-loso", action="store_true", help="only the angle analyses")
    ap.add_argument("--conversion", choices=["log", "linear"], default=None,
                    help="how the stored real frame is read as attenuation (see CONVERSION); default DF_CONVERSION or log")
    a = ap.parse_args()
    global CONVERSION
    if a.conversion:
        CONVERSION = a.conversion
    print(f"real frames read as attenuation by the {CONVERSION!r} conversion")
    apply_overrides(a.fix, a.bounds)
    import render_physics_drr as RP_
    RP = (RP_.ENERGIES.numpy(), RP_.SPECTRUM.numpy(), RP_.MU_WATER.numpy(), RP_.MU_BONE.numpy())

    files = sorted(glob.glob(os.path.expanduser(a.pairs) + "/pair_*.npz"))
    frames = [load_pair(p) for p in files]
    _FRAMES.extend(frames)
    specs = sorted({d["spec"] for d in frames})
    print(f"{len(frames)} pairs, {len(specs)} specimens; truncated pixels masked: "
          f"median {100 * np.median([d['trunc_frac'] for d in frames]):.1f}% per frame")
    base_all = baseline_explained(frames)
    print(f"uncalibrated physics + linear match, all frames: {100 * base_all:.1f}% explained\n")

    rng = np.random.RandomState(a.seed)
    folds = []
    print(f"{'held out':10s} {'n':>4s} {'baseline':>9s} {'calibrated':>11s} {'gain':>7s}   " + " ".join(f"{n:>7s}" for n in NAMES))
    for held in ([] if a.skip_loso else specs):
        train_all = [i for i, d in enumerate(frames) if d["spec"] != held]
        test = [d for d in frames if d["spec"] == held]
        train_idx = [int(i) for i in rng.choice(train_all, size=min(a.fit_frames, len(train_all)), replace=False)]
        theta, fval, nit, l0 = fit(train_idx, RP, workers=a.workers, seed=a.seed, maxiter=a.maxiter)
        base = baseline_explained(test); cal = explained(theta, test, RP)
        folds.append(dict(held=held, n=len(test), baseline=base, calibrated=cal, theta=theta.tolist(), nit=nit,
                          train_unexplained_start=l0, train_unexplained_end=fval))
        print(f"{held:10s} {len(test):4d} {100 * base:8.1f}% {100 * cal:10.1f}% {100 * (cal - base):+6.1f}   "
              + " ".join(f"{t:7.3f}" for t in theta), flush=True)
    if a.angle_folds and os.path.exists(os.path.expanduser(a.poses)):
        pj = json.load(open(os.path.expanduser(a.poses)))
        lat = {(r["spec"], r["pid"]): abs(float(r["lat_deg"])) for r in pj["poses"]}
        L = np.array([lat.get((d["spec"], d["pid"]), np.nan) for d in frames])
        print(f"\nheld out by VIEW ANGLE (|lateral tilt|): {int((L <= 8).sum())} near-AP frames <= 8 deg, "
              f"{int((L >= 15).sum())} lateral frames >= 15 deg")
        for name, tr_m, te_m in (("AP -> lateral", L <= 8, L >= 15), ("lateral -> AP", L >= 15, L <= 8)):
            tr_all = [i for i in range(len(frames)) if tr_m[i]]; test = [frames[i] for i in range(len(frames)) if te_m[i]]
            if len(tr_all) < 10 or len(test) < 5:
                print(f"  {name}: too few frames"); continue
            train_idx = [int(i) for i in rng.choice(tr_all, size=min(a.fit_frames, len(tr_all)), replace=False)]
            theta, fval, nit, l0 = fit(train_idx, RP, workers=a.workers, seed=a.seed, maxiter=a.maxiter)
            base = baseline_explained(test); cal = explained(theta, test, RP)
            folds.append(dict(held=name, n=len(test), baseline=base, calibrated=cal, theta=theta.tolist(), nit=nit,
                              train_unexplained_start=l0, train_unexplained_end=fval))
            print(f"  {name:14s} n={len(test):3d}  baseline {100 * base:5.1f}%  calibrated {100 * cal:5.1f}%  "
                  f"gain {100 * (cal - base):+5.1f}   " + " ".join(f"{n}={t:.3f}" for n, t in zip(NAMES, theta)), flush=True)
    bins = None
    if a.angle_bins and os.path.exists(os.path.expanduser(a.poses)):
        # The regression of the terms on view angle. Each bin's terms are fitted on fit-frames drawn from
        # that bin and scored on the bin's REMAINING frames against the global terms scored on the same
        # frames, so the comparison is between per-angle and global calibration on identical held-out
        # pixels. The slope is a least-squares line through the bins' medians; its excursion over the
        # full 36.5 deg is compared with the LOSO spread of the same term, which is the noise it must beat.
        pj = json.load(open(os.path.expanduser(a.poses)))
        lat = {(r["spec"], r["pid"]): abs(float(r["lat_deg"])) for r in pj["poses"]}
        L = np.array([lat.get((d["spec"], d["pid"]), np.nan) for d in frames])
        edges = ((0.0, 8.0), (8.0, 15.0), (15.0, 90.0))
        glob_th = np.array(json.load(open(os.path.expanduser(a.global_theta)))["theta_median"]) \
            if a.global_theta and os.path.exists(os.path.expanduser(a.global_theta)) else None
        print(f"\nterms fitted INSIDE |lateral tilt| bins; scored on that bin's remaining frames")
        print(f"{'bin':10s} {'n_fit':>5s} {'n_test':>6s} {'ang':>5s} {'baseline':>9s} {'per-bin':>8s} {'global':>7s}   "
              + " ".join(f"{n:>7s}" for n in NAMES))
        bins = []
        for lo, hi in edges:
            idx = [i for i in range(len(frames)) if lo <= L[i] < hi]
            if len(idx) < 20:
                print(f"  {lo:g}-{hi:g}: {len(idx)} frames, too few"); continue
            tr = [int(i) for i in rng.choice(idx, size=min(a.fit_frames, len(idx) - 10), replace=False)]
            te = [frames[i] for i in idx if i not in set(tr)]
            theta, fval, nit, l0 = fit(tr, RP, workers=a.workers, seed=a.seed, maxiter=a.maxiter)
            base = baseline_explained(te); cal = explained(theta, te, RP)
            glo = explained(glob_th, te, RP) if glob_th is not None else float("nan")
            ang = float(np.median(L[idx]))
            bins.append(dict(lo=lo, hi=hi, n_fit=len(tr), n_test=len(te), angle_median=ang, baseline=base,
                             per_bin=cal, global_terms=glo, theta=theta.tolist()))
            print(f"{lo:3g}-{hi:<5g} {len(tr):5d} {len(te):6d} {ang:5.1f} {100 * base:8.1f}% {100 * cal:7.1f}% "
                  f"{100 * glo:6.1f}%   " + " ".join(f"{t:7.3f}" for t in theta), flush=True)
        if len(bins) >= 2:
            A = np.array([b_["angle_median"] for b_ in bins]); T = np.array([b_["theta"] for b_ in bins])
            print(f"\n{'term':10s} {'slope/deg':>10s} {'over 36.5':>10s}   (compare with the LOSO spread below)")
            for i, n in enumerate(NAMES):
                sl = np.polyfit(A, T[:, i], 1)[0] if FREE[i] else 0.0
                print(f"{n:10s} {sl:10.4f} {36.5 * sl:10.3f}")
                for b_ in bins:
                    b_.setdefault("slope_per_deg", {})[n] = float(sl)
            d_ = np.array([b_["per_bin"] - b_["global_terms"] for b_ in bins])
            if np.all(np.isfinite(d_)):
                print(f"per-angle terms over global terms, on the same held-out frames: "
                      + ", ".join(f"{100 * x:+.1f}" for x in d_) + " points by bin")
    TH = np.array([f["theta"] for f in folds if "->" not in f["held"]]) if folds else np.zeros((0, len(NAMES)))
    if len(TH):
        print(f"\n{'parameter':10s} {'median':>8s} {'spread(p90-p10)':>16s}   stable across folds = a property of the device")
        for i, n in enumerate(NAMES):
            print(f"{n:10s} {np.median(TH[:, i]):8.3f} {np.percentile(TH[:, i], 90) - np.percentile(TH[:, i], 10):16.3f}"
                  + ("" if FREE[i] else "   fixed"))
    g = np.array([f["calibrated"] - f["baseline"] for f in folds]) if folds else np.zeros(0)
    if len(g):
        print(f"\nheld-out gain over uncalibrated physics: median {100 * np.median(g):+.1f} points, "
              f"min {100 * g.min():+.1f}, max {100 * g.max():+.1f}")
        if np.median(g) < 1.0 / 100:
            print("The calibrated terms buy less than a point on the held-out specimen. The per-frame remainder "
                  "dominates what is left, and the literature says a learned model does not recover it either.")
    o = os.path.expanduser(a.out); os.makedirs(os.path.dirname(o), exist_ok=True)
    json.dump(dict(conversion=CONVERSION, names=NAMES, folds=folds, baseline_all=base_all, free=FREE.tolist(), lo=LO.tolist(), hi=HI.tolist(),
                   fixed=X0.tolist(), angle_bins=bins,
                   theta_median=(np.median(TH, 0).tolist() if len(TH) else None)), open(o, "w"), indent=1)
    print("wrote", o)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
