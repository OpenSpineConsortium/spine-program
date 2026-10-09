#!/usr/bin/env python
"""Fit one device's image-formation parameter set from its paired (CT render, real frame) data, in one schema.

WHAT A DEVICE IS HERE. The map from projected volume to stored frame decomposes into exact geometry, polyenergetic
attenuation, and device terms (docs/DEEPFLUORO_FORMATION.md). The device terms were fitted once, on DeepFluoro's
Siemens Cios Fusion, as nine numbers (tools/deepfluoro_calibrate.py). This tool fits the SAME forward model, with the
same optimiser and the same per-frame linear display match, on every device the project holds pairs for, and then
goes further than a point estimate: every exposure-dependent term is fitted PER FRAME, the automatic exposure control
is learned as a conditional on the patient's thickness, the per-frame vector is stored as a Gaussian copula so that a
sampler can draw whole frames, and a coverage check says how much of the held-out real frames that sampler covers.
Beside every fitted term sits a physics default that needs no pairs (tools/device_physics.py), so the gap between
them says which terms an unpaired device can be given by physics alone.

THE FORWARD MODEL (tools/deepfluoro_calibrate.forward, unchanged when the extra terms are zero):
    T    = polyenergetic transmission of the water / bone path maps, bone scaled by kb
    T_s  = (1 - s) T + s G[sigma_s] T                 scatter pedestal (s may follow thickness: s (1 - exp(-water / s_t)))
    T_p  = T_s . G[sigma_p] field                      collimator penumbra (the field edge rolls off, then is blurred)
    T_n  = Poisson(N T_p) / N                          quantum draw, in the place the detector counts it (fits only)
    T_d  = G[sigma_r] T_n                              receptor blur
    T_d  = T_d + alpha (T_d - G[sigma_u] T_d)          edge enhancement
    T_f  = T_d (1 + b r^2 + c u' + d v + b4 r^4)       vignette, heel (u' flips with rot-180), tilt, quartic vignette
    a    = -log T_f ;  a_hat = k_f a + c_f             per-frame linear display match, the same for the baseline

HOW EACH DEVICE'S STORED FRAME IS READ AS ATTENUATION (its `reading`): a log display is read linearly, (p98 - r) /
(p98 - p2) over the exposed field (DeepFluoro, C-ArmLSpine DR); a linear detector signal by -log(r - offset) (COBRA
Elekta raw projections, the C-ArmLSpine raw sweep twins, Geneva's intensifier with its per-frame glare offset). The
transfer test (tools/deepfluoro_transfer.py) is run on every device and reported beside the reading chosen.

    python tools/device_fit.py pairs --device elekta_xvi            # build the pairs a device does not have yet
    python tools/device_fit.py fit   --device cios_fusion           # everything -> docs/devices/<device>.json etc.
    python tools/device_fit.py display                              # C-ArmLSpine raw -> processed display stage
    python tools/device_fit.py cobra-thickness                      # AP / lateral water thickness of every Elekta case

Outputs: /rs/rs_grp_oschome/go2432/data/or_ready/devices/<device>/ (pairs, figures, per-frame json) and the schema
JSON + frames.csv in docs/devices/. Nothing here can move a label.
"""
from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import device_physics as PH  # noqa: E402
import eval_gate as EG  # noqa: E402

ROOT = "/rs/rs_grp_oschome/go2432/data/or_ready/devices"
DOCS = Path(__file__).resolve().parents[1] / "docs" / "devices"
NAMES9 = ["kb", "s", "sigma_s", "sigma_r", "alpha", "sigma_u", "b", "c", "d"]
EXTRAS = ["sigma_p", "s_t", "b4"]
PX_TERMS = ["sigma_s", "sigma_r", "sigma_u", "sigma_p"]
# The boxes, in physical units, with where each came from. A fitted value within 1 % of a box edge is reported "at bound".
BOX_MM = dict(sigma_s=(4.5, 12.5), sigma_r=(0.2, 2.4), sigma_u=(0.75, 6.2), sigma_p=(0.0, 6.0))
BOX = dict(kb=(0.5, 2.5), s=(0.0, 0.75), alpha=(0.0, 2.0), b=(-0.6, 0.6), c=(-0.3, 0.3), d=(-0.3, 0.3), s_t=(2.0, 40.0), b4=(-0.6, 0.6))
BOX_SOURCE = dict(
    kb="0.5-2.5: the bone-path scale a 60-150 kVp Kramers spectrum needs against the repo's ~100 kVp six-energy spectrum spans ~0.6-1.6 (device_physics.kb_default); the box is opened to 2.5 because DeepFluoro under the old reading pinned at 2.5 and under the linear reading sits at 2.0",
    s="0-0.75: scatter fraction s = SPR/(1+SPR) for SPR 0-3 (gridless pelvis, Siewerdsen & Jaffray 2001)",
    sigma_s="4.5-12.5 mm: the box that made the term identifiable on DeepFluoro (6-16 px at 0.776 mm); wider boxes ran 5-60 px across folds",
    sigma_r="0.2-2.4 mm: scintillator + binning blur of CsI / GOS panels and intensifiers (device_physics.SCINT_SIGMA_MM), up to a 2x2-binned II",
    alpha="0-2: unsharp-mask gain, none to twice the high-pass",
    sigma_u="0.75-6.2 mm: unsharp radius 1-40 px at 0.15-0.2 mm native pitch",
    b="-0.6..0.6: radial gain at the field corner, from -60 % (an intensifier's vignetting is ~-25 %) to +60 %",
    c="-0.3..0.3: anode-heel gradient across the field, |c| ~0.07 physically", d="-0.3..0.3: cranio-caudal tilt gradient",
    sigma_p="0-6 mm: geometric penumbra of a 0.3-1 mm focal spot at 100-300 mm collimator distance is 0.5-5 mm",
    s_t="2-40 cm: the water thickness at which scatter build-up saturates", b4="quartic vignette, II only",
    photons="0.05x-20x the mAs-derived count (device_physics.photons_default), or the observed p1-p99 where mAs is unknown",
    kvp="mobile C-arm 40-125 kV (spec sheets); COBRA Elekta XVI 70-150", ma="0.2-30 mA pulsed fluoroscopy, higher for a DR spot", pulse_ms="4-100 ms",
    sid_mm="900-1200 mm mobile C-arms; 1536 mm Elekta XVI", pitch_mm="0.1-0.4 mm native", window="percentiles inside [0, 100], OR targets 27/47/126/216/239 at the centre")

# ---------------------------------------------------------------------------------------------------------- devices
DEVICES = {
    "cios_fusion": dict(make="Siemens", model="Cios Fusion", dataset="DeepFluoro (Grupp et al. 2020), 6 cadaveric pelves, 366 frames",
                        detector_type="csi_fpd", pixel_pitch_mm=0.194, image_size=[1536, 1536], panel_mm=[298.0, 298.0], sid_mm=1020.0, sod_mm=None,
                        stored_form="log_display", reading="log_display", down=4, group="spec", grid=False, focal_mm=0.5, coll_mm=150.0,
                        pairs=os.path.expanduser("~/model_night/deepfluoro/pairs"), cios_exact=True,
                        orientation="the stored frame is the camera image of K (focal -5257.7 px kept signed, (col, row)); no rotation is applied to the render; "
                                    "rot-180-for-up is set on 160/366 frames (all 24 of 17-1905) and the heel sign follows it"),
    "surgio_b51_dr": dict(make="Yiying (FIRST)", model="Surgio-B51", dataset="C-ArmLSpine (Zenodo 10.5281/zenodo.22768651), 149 intraoperative cases, AP + lateral DR frames + CBCT",
                          detector_type="unknown_fpd", pixel_pitch_mm=0.15, image_size=[2048, 2048], panel_mm=[307.2, 307.2], sid_mm=1140.0, sod_mm=745.0,
                          stored_form="processed_display", reading="log_display", down=4, group="case", grid=None, focal_mm=0.5, coll_mm=150.0,
                          pairs=f"{ROOT}/surgio_b51_dr/pairs",
                          orientation="AP: dir(0,-1,0)_rot180_m-1 (beam posterior->anterior, image turned 180 deg, mirrored: K focal negative); LAT: dir(1,0,0)_rot180_m-1 "
                                      "(tools/carmlspine_pose.py consensus over 148 cases; laterals bounded 5/5/25 mm 6 deg, tag _ref2)"),
    "surgio_b51_raw": dict(make="Yiying (FIRST)", model="Surgio-B51", dataset="C-ArmLSpine raw CBCT sweeps case39 and case134: 301 XA frames each with a near-raw twin in private tag (0037,0020)",
                           detector_type="unknown_fpd", pixel_pitch_mm=0.30, image_size=[1024, 1024], panel_mm=[307.2, 307.2], sid_mm=1140.0, sod_mm=745.0,
                           stored_form="linear", reading="neg_log", down=2, group="case", grid=None, focal_mm=0.5, coll_mm=150.0,
                           pairs=f"{ROOT}/surgio_b51_raw/pairs",
                           orientation="the private raw frame is stored turned 180 deg relative to the processed main frame (verified by NCC per frame, see pairs meta)"),
    "elekta_xvi": dict(make="Elekta", model="XVI kV imager (four European centres A-D)", dataset="COBRA2026 (Thummerer et al.), living pelvic radiotherapy patients, raw kV CBCT projections + registered planning CT",
                       detector_type="unknown_fpd", pixel_pitch_mm=0.8, image_size=[504, 504], panel_mm=[403.2, 403.2], sid_mm=1536.0, sod_mm=1000.0,
                       stored_form="linear", reading="neg_log", down=1, group="case", grid=False, focal_mm=0.6, coll_mm=200.0,
                       pairs=f"{ROOT}/elekta_xvi/pairs",
                       orientation="RTK world->detector matrices; patient LPS -> RTK world by rtk_x=+pat_y, rtk_y=-pat_z, rtk_z=+pat_x (settled by edges against the authors' simulated projections)"),
    "pixium_4600": dict(make="Trixell (Ljubljana 2D-3D-GS)", model="PIXIUM 4600 flat panel, fixed radiograph on a turntable (not a C-arm)",
                        dataset="Ljubljana 2D-3D gold standard (Tomazevic 2002): cadaver L1-L5 in a water tube, 18 radiographs at 20 deg steps, CT with fiducial gold standard",
                        detector_type="csi_fpd", pixel_pitch_mm=0.286, image_size=[1560, 1560], panel_mm=[446.2, 446.2], sid_mm=1009.6, sod_mm=None,
                        stored_form="linear", reading="neg_log", down=3, group="frame", grid=None, focal_mm=0.6, coll_mm=150.0,
                        pairs="/rs/rs_grp_oschome/go2432/data/ljubljana/pairs", group_by_pid=True,
                        orientation="detector axes (n, s) handedness settled per frame by NCC over the four sign choices (tools/ljubljana_pairs.py); supplied frames are 2x subsampled, 3x3 median filtered"),
    "varian_halcyon": dict(make="Varian", model="Halcyon / TrueBeam-class kV imager (COBRA centre G)", dataset="COBRA2026 centre G: living pelvic radiotherapy patients, kV CBCT projections normalised against an air scan with a kernel scatter correction, + registered planning CT",
                           detector_type="unknown_fpd", pixel_pitch_mm=0.388, image_size=[768, 1024], panel_mm=[298.0, 397.3], sid_mm=1540.0, sod_mm=1000.0,
                           stored_form="linear", reading="neg_log", down=1, group="case", grid=True, focal_mm=0.6, coll_mm=200.0,
                           pairs=f"{ROOT}/varian_halcyon/pairs", cobra_manufacturer="Varian", cobra_cases=["G000", "G001", "G003", "G004", "G007", "G008", "G009", "G010", "G011", "G012", "G014", "G015"],
                           orientation="RTK world->detector matrices as for the Elekta cases; the patient->RTK map settled on Elekta is used first and the per-case NCC decides whether Varian needs its own (tools/cobra_handedness.py)"),
    "bv_pulsera": dict(make="Philips", model="BV Pulsera", dataset="Geneva hip gold standard (D'Isidoro et al. 2021): one resin phantom, 19 poses, 116 image-intensifier frames at 62-110 kV",
                       detector_type="ii", pixel_pitch_mm=0.2904, image_size=[1000, 1000], panel_mm=[290.4, 290.4], sid_mm=968.2, sod_mm=None,
                       stored_form="linear", reading="neg_log_offset", down=1000.0 / 372.0, group="view", grid=False, focal_mm=0.6, coll_mm=150.0,
                       pairs=f"{ROOT}/bv_pulsera/pairs", field="circle",
                       orientation="K with positive focal in ITK pixel indices; the intensifier's S-distortion is corrected in the source; frames were turned 180 deg on export where superior pointed down"),
}
_G = {}


# ---------------------------------------------------------------------------------------------------------- reading
def gauss(a, s):
    from scipy.ndimage import gaussian_filter
    return gaussian_filter(a, s, mode="nearest") if s > 0.05 else a


def stored_to_atten(raw, field, reading, offset=0.0):
    f = raw[field] if field is not None and field.any() else raw
    if reading == "log_display":
        p2, p98 = np.percentile(f, (2, 98))
        return (p98 - raw) / max(p98 - p2, 1e-6)
    if reading in ("neg_log", "neg_log_offset"):
        p98 = np.percentile(f, 98)
        fl = max(1.0, 1e-3 * (p98 - offset))
        return -np.log(np.clip(raw - offset, fl, None))
    raise SystemExit(f"unknown reading {reading}")


def make_frame(real, hit, trunc, rot, water, bone, dev, meta, px_mm, spec, pid, offset=0.0, sat=None, excl=None):
    from scipy.ndimage import binary_erosion
    real = np.asarray(real, np.float64); hit = np.asarray(hit, bool); trunc = np.asarray(trunc, bool)
    h, w = real.shape
    field = PH.exposed_field(real, hit)
    iters = max(6, int(0.06 * min(h, w)))
    if dev.get("cios_exact"):
        # exactly tools/deepfluoro_calibrate.load_pair, so the DeepFluoro numbers reproduce
        p2 = np.percentile(real[hit], 2)
        atten = stored_to_atten(real, hit, "log_display")
        m = binary_erosion(hit & (real > p2), iterations=iters) & ~trunc
    else:
        p2 = np.percentile(real[field], 2) if field.any() else real.min()
        atten = stored_to_atten(real, field, dev["reading"], offset)
        m = binary_erosion(field & (real > p2), iterations=iters) & ~trunc & hit
    m_full = binary_erosion(field, iterations=3) & ~trunc & hit
    if sat is not None:
        m &= ~sat; m_full &= ~sat
    if excl is not None:
        m &= ~excl; m_full &= ~excl
    yy, xx = np.mgrid[0:h, 0:w]
    u = (xx - w / 2) / (w / 2); v = (yy - h / 2) / (h / 2)
    return dict(spec=str(spec), pid=str(pid), water=np.asarray(water, np.float64), bone=np.asarray(bone, np.float64), atten=atten, raw=real,
                m=m, m_full=m_full, field=field, fieldf=field.astype(np.float64), u=u, v=v, r2=u * u + v * v, rot=int(rot),
                trunc_frac=float(trunc.mean()), px_mm=float(px_mm), meta=dict(meta or {}), hit=hit)


def load_frames(dev, limit=0):
    files = sorted(glob.glob(os.path.join(dev["pairs"], "pair_*.npz")))
    if limit:
        files = files[:limit]
    poses = {}
    if dev.get("cios_exact"):
        pj = os.path.expanduser("~/model_night/deepfluoro/poses.json")
        if os.path.exists(pj):
            poses = {(r["spec"], r["pid"]): r for r in json.load(open(pj))["poses"]}
    out = []; skipped = 0
    for p in files:
        z = np.load(p)
        stem = Path(p).stem.replace("pair_", ""); spec, pid = stem.rsplit("_", 1)
        subject_spec = spec                              # the imaged subject, before any regrouping below
        if dev.get("group_by_pid"):
            spec = pid                                   # one subject: hold frames out, not specimens (folds of frames)
        sc = p[:-4] + ".json"
        meta = json.load(open(sc)) if os.path.exists(sc) else {}
        if dev.get("cios_exact"):
            r = poses.get((spec, pid), {})
            meta = dict(lat_deg=r.get("lat_deg"), rot=int(z["rot"]), kvp=None, ma=None, ms=None, mas=None)
        sat = z["sat"].astype(bool) if "sat" in z.files else None
        excl = z["excl"].astype(bool) if "excl" in z.files else None
        off = float(meta.get("offset_c", 0.0) or 0.0)
        d = make_frame(z["real"], z["hit"], z["trunc"] if "trunc" in z.files else np.zeros(z["hit"].shape, bool), int(z["rot"]) if "rot" in z.files else 0,
                       z["water_cm"], z["bone_cm"], dev, meta, float(z["px_mm"]), spec, pid, offset=off, sat=sat, excl=excl)
        if d["m"].sum() < 200:
            # the CT does not cover this frame (COBRA B000: 41 of 41 frames with hit_frac 0-0.09, a registration that
            # never landed); nothing here can be fitted and the per-frame percentiles of an empty mask raised
            skipped += 1; continue
        d["subject_spec"] = subject_spec
        out.append(d)
    if skipped:
        print(f"  {skipped} pairs skipped: fewer than 200 fittable pixels (CT does not cover the frame)", flush=True)
    return out


# ---------------------------------------------------------------------------------------------------------- forward
def poly_T(water, bone, kb, RP):
    E, S, muw, mub = RP
    T = np.zeros_like(water)
    for k in range(len(E)):
        T += S[k] * E[k] * np.exp(-(muw[k] * water + kb * mub[k] * bone))
    return T / (S * E).sum()


def forward(th, d, RP, noisy=None):
    T = poly_T(d["water"], d["bone"], th["kb"], RP)
    s = th["s"]
    if th.get("s_t", 0.0) > 0:
        s = s * (1.0 - np.exp(-d["water"] / th["s_t"]))
    T = (1.0 - s) * T + s * gauss(T, th["sigma_s"])
    if th.get("sigma_p", 0.0) > 0.05:
        T = T * gauss(d["fieldf"], th["sigma_p"])
    if noisy is not None:
        N, rng = noisy
        T = rng.poisson(np.clip(T, 1e-6, None) * N).astype(np.float64) / N
    T = gauss(T, th["sigma_r"])
    T = T + th["alpha"] * (T - gauss(T, th["sigma_u"]))
    up = -d["u"] if d["rot"] else d["u"]
    T = T * (1.0 + th["b"] * d["r2"] + th["c"] * up + th["d"] * d["v"] + th.get("b4", 0.0) * d["r2"] ** 2)
    return -np.log(np.clip(T, 1e-6, None))


def matched(x, d, m):
    xs, ys = x[m], d["atten"][m]
    k, c0 = np.linalg.lstsq(np.c_[xs, np.ones_like(xs)], ys, rcond=None)[0]
    return k * x + c0, float(k), float(c0)


def sse_sst(th, d, RP, mkey="m"):
    m = d[mkey]
    if m.sum() < 50:
        return 0.0, 0.0
    a_hat, _, _ = matched(forward(th, d, RP), d, m)
    r = d["atten"][m] - a_hat[m]
    return float((r * r).sum()), float(((d["atten"][m] - d["atten"][m].mean()) ** 2).sum())


def explained(th, frames, RP, mkey="m"):
    num = den = 0.0
    for d in frames:
        a, b = sse_sst(th, d, RP, mkey); num += a; den += b
    return 1.0 - num / max(den, 1e-12)


def baseline_theta(x0):
    th = dict(x0); th.update(s=0.0, alpha=0.0, b=0.0, c=0.0, d=0.0, sigma_r=0.0, sigma_p=0.0, s_t=0.0, b4=0.0); th["kb"] = 1.0
    return th


def _sse_one(args):
    i, th, mkey = args
    return sse_sst(th, _G["frames"][i], _G["RP"], mkey)


def fit_terms(train_idx, free, box, x0, workers=8, maxiter=60, mkey="m"):
    """L-BFGS-B in [0,1]^k over the free terms, the frames inherited by forked workers (tools/deepfluoro_calibrate.fit)."""
    from multiprocessing import get_context
    from scipy.optimize import minimize
    lo = np.array([box[n][0] for n in free]); hi = np.array([box[n][1] for n in free]); span = hi - lo

    def to_th(z):
        th = dict(x0)
        for n, zi, l, sp in zip(free, z, lo, span):
            th[n] = float(l + zi * sp)
        return th
    z0 = np.array([(x0[n] - box[n][0]) / (box[n][1] - box[n][0]) for n in free])
    with get_context("fork").Pool(workers) as pool:
        def loss(z):
            th = to_th(np.clip(z, 0, 1))
            out = pool.map(_sse_one, [(i, th, mkey) for i in train_idx])
            return float(sum(a for a, _ in out) / max(sum(b for _, b in out), 1e-12))
        l0 = loss(z0)
        res = minimize(loss, z0, method="L-BFGS-B", bounds=[(0.0, 1.0)] * len(free), options=dict(maxiter=maxiter, eps=1e-2))
    th = to_th(res.x)
    at_bound = {n: bool(abs(res.x[j]) < 0.01 or abs(res.x[j] - 1) < 0.01) for j, n in enumerate(free)}
    return th, float(res.fun), int(res.nit), l0, at_bound


def px_box(dev, extra=None):
    """The fit box in this device's fit pixels (mm boxes / fit pitch), plus the starting point."""
    pitch = dev["pixel_pitch_mm"] * dev["down"]
    if dev.get("cios_exact"):
        box = dict(kb=(0.5, 2.5), s=(0.0, 0.7), sigma_s=(6.0, 16.0), sigma_r=(0.3, 3.0), alpha=(0.0, 2.0), sigma_u=(1.0, 8.0), b=(-0.6, 0.6), c=(-0.3, 0.3), d=(-0.3, 0.3))
        x0 = dict(kb=1.0, s=0.25, sigma_s=16.0, sigma_r=0.8, alpha=0.3, sigma_u=3.0, b=0.0, c=0.0, d=0.0)
    else:
        box = dict(BOX)
        for n in ("sigma_s", "sigma_r", "sigma_u"):
            box[n] = (BOX_MM[n][0] / pitch, BOX_MM[n][1] / pitch)
        x0 = dict(kb=1.0, s=0.25, sigma_s=float(np.clip(12.0 / pitch, *box["sigma_s"])), sigma_r=float(np.clip(0.6 / pitch, *box["sigma_r"])), alpha=0.3,
                  sigma_u=float(np.clip(2.3 / pitch, *box["sigma_u"])), b=0.0, c=0.0, d=0.0)
    box["sigma_p"] = (BOX_MM["sigma_p"][0] / pitch, BOX_MM["sigma_p"][1] / pitch); box["s_t"] = BOX["s_t"]; box["b4"] = BOX["b4"]
    x0.update(sigma_p=0.0, s_t=0.0, b4=0.0)
    return box, x0, pitch


def run_loso(frames, groups, free, box, x0, workers, maxiter, fit_frames, seed=0, label="", log=print):
    """Leave-one-group-out fits: theta per fold, held-out explained variance on the fit mask and on the full field."""
    rng = np.random.RandomState(seed)
    folds = []
    log(f"{'held out':12s} {'n':>4s} {'base':>6s} {'cal':>6s} {'gain':>6s} {'base_f':>7s} {'cal_f':>6s}   " + " ".join(f"{n:>7s}" for n in free))
    for held in groups:
        train_all = [i for i, d in enumerate(frames) if d["spec"] != held]
        test = [d for d in frames if d["spec"] == held]
        if len(train_all) < 5 or not test:
            continue
        train_idx = [int(i) for i in rng.choice(train_all, size=min(fit_frames, len(train_all)), replace=False)]
        th, fval, nit, l0, ab = fit_terms(train_idx, free, box, x0, workers, maxiter)
        base = explained(baseline_theta(x0), test, _G["RP"]); cal = explained(th, test, _G["RP"])
        base_f = explained(baseline_theta(x0), test, _G["RP"], "m_full"); cal_f = explained(th, test, _G["RP"], "m_full")
        folds.append(dict(held=held, n=len(test), n_fit=len(train_idx), baseline=base, calibrated=cal, baseline_full=base_f, calibrated_full=cal_f,
                          theta=th, nit=nit, train_unexplained_start=l0, train_unexplained_end=fval, at_bound=ab, train_idx=train_idx))
        log(f"{held:12s} {len(test):4d} {100 * base:6.1f} {100 * cal:6.1f} {100 * (cal - base):+6.1f} {100 * base_f:7.1f} {100 * cal_f:6.1f}   "
            + " ".join(f"{th[n]:7.3f}" for n in free) + ("  AT BOUND: " + ",".join(n for n, v in ab.items() if v) if any(ab.values()) else ""), flush=True)
    return folds


def theta_for_group(folds, g):
    m = [f for f in folds if f["held"] == g]
    return m[0]["theta"] if m else None


def fold_summary(folds, names):
    TH = {n: np.array([f["theta"][n] for f in folds]) for n in names}
    out = {}
    for n in names:
        v = TH[n]
        out[n] = dict(median=float(np.median(v)), spread_p90_p10=float(np.percentile(v, 90) - np.percentile(v, 10)), min=float(v.min()), max=float(v.max()),
                      at_bound_folds=int(sum(1 for f in folds if f.get("at_bound", {}).get(n))))
    return out


# --------------------------------------------------------------------------------------------------- per-frame terms
def fine(x):
    return x - gauss(x, 2.0)


def photons_one(d, th, RP, n1=2000.0, n2=8000.0, draws=2, seed=0):
    """tools/deepfluoro_photons.one with this forward: the count whose quantum draw reproduces the real fine-band grain."""
    m = d["m"]
    det = forward(th, d, RP)
    k, c0 = np.linalg.lstsq(np.c_[det[m], np.ones(int(m.sum()))], d["atten"][m], rcond=None)[0]
    struct = np.abs(gauss(k * det, 1.0) - gauss(k * det, 4.0))
    flat = m & (struct <= np.percentile(struct[m], 20))
    v_real = float(fine(d["atten"])[flat].var()); v_det = float(fine(k * det)[flat].var())

    def v_at(n):
        return float(np.mean([fine(k * forward(th, d, RP, noisy=(n, np.random.RandomState(seed + j))))[flat].var() for j in range(draws)]))
    v1, v2 = v_at(n1), v_at(n2)
    a_ = (v1 - v2) / (1.0 / n1 - 1.0 / n2); v0 = v1 - a_ / n1
    excess = v_real - v0
    N = a_ / excess if (excess > 0 and a_ > 0) else float("nan")
    return dict(photons=float(N), v_real=v_real, v_det=v_det, v0=v0, grain_sd=float(np.sqrt(max(v_real, 0.0))), n_flat=int(flat.sum()))


def thickness_at_centre(d, frac=0.06):
    """Water-equivalent thickness (cm) at the field centre (median in a disc of radius frac x image), and its mean over the field."""
    h, w = d["water"].shape
    ys, xs = np.nonzero(d["field"])
    cy, cx = (ys.mean(), xs.mean()) if len(ys) else (h / 2, w / 2)
    yy, xx = np.mgrid[0:h, 0:w]
    disc = ((yy - cy) ** 2 + (xx - cx) ** 2 <= (frac * min(h, w)) ** 2) & d["hit"]
    f = d["field"] & d["hit"]
    return (float(np.median(d["water"][disc])) if disc.any() else float("nan"), float(d["water"][f].mean()) if f.any() else float("nan"),
            float(d["bone"][f].mean()) if f.any() else float("nan"))


def _perframe(i):
    from scipy.optimize import minimize
    from deepfluoro_transfer import curve, fit_forms
    d = _G["frames"][i]; RP = _G["RP"]; th0 = dict(_G["theta_of"][d["spec"]]); box = _G["box"]
    if d["m"].sum() < 50:                                   # belt and braces: load_frames already drops these
        nan = float("nan")
        return dict(spec=d["spec"], pid=d["pid"], r2_global=nan, r2_frame=nan, s=th0["s"], sigma_r=th0["sigma_r"], alpha=th0["alpha"], photons=nan, grain_sd=nan,
                    kf=nan, cf=nan, win_A=nan, win_B=nan, I0=None, B_trans=None, C_trans=None,
                    transfer=dict(linear_r2=None, transmission_r2=None, transmission_B=None, power_r2=None, power_gamma=None),
                    stored_p1=nan, stored_p5=nan, stored_p50=nan, stored_p95=nan, stored_p99=nan, thickness_cm=nan, thickness_mean_cm=nan, bone_mean_cm=nan,
                    field_frac=float(d["field"].mean()), trunc_frac=d["trunc_frac"], rot=d["rot"], shape=None, border=None, meta=d["meta"], px_mm=d["px_mm"])
    free = list(_G.get("pf_free", ["s", "sigma_r", "alpha"]))
    lo = np.array([box[n][0] for n in free]); hi = np.array([box[n][1] for n in free])

    def loss(z):
        th = dict(th0)
        for n, zi, l, h_ in zip(free, np.clip(z, 0, 1), lo, hi):
            th[n] = float(l + zi * (h_ - l))
        a, b = sse_sst(th, d, RP)
        return a / max(b, 1e-12)
    z0 = np.array([(th0[n] - box[n][0]) / (box[n][1] - box[n][0]) for n in free])
    l_glob = loss(z0)
    if free:
        res = minimize(loss, z0, method="L-BFGS-B", bounds=[(0, 1)] * len(free), options=dict(maxiter=int(_G.get("pf_maxiter", 40)), eps=1e-2))
        res_x, res_fun = np.clip(res.x, 0, 1), float(res.fun)
    else:
        # PHOTONS-ONLY per-frame fit: the fold's terms stay, only the quantum count is estimated per frame. With three free
        # terms per frame the first cards put alpha and sigma_r at their bounds on most frames (not identifiable from one
        # frame's residual) and the photon spread reached four decades; see docs/RSNAI_PLAN.md C4.
        res_x, res_fun = z0, l_glob
    th = dict(th0)
    for n, zi, l, h_ in zip(free, res_x, lo, hi):
        th[n] = float(l + zi * (h_ - l))
    ph = photons_one(d, th, RP)
    a_model = forward(th, d, RP)
    _, kf, cf = matched(a_model, d, d["m"])
    # the device window in STORED units: raw ~ A + B a (log display) or raw ~ A exp(-B a) + C (linear signal).
    # Guarded as a whole: on C-ArmLSpine case frames whose masked stored values collapse to one bin, curve() returned
    # empty arrays and fit_forms took the minimum of nothing (the Surgio fit died there, 2026-09-22 08:xx).
    none_forms = dict(linear=dict(r2=None), transmission=dict(r2=None, B=None), power=dict(r2=None, gamma=None))
    try:
        xs, ys, ws = curve(a_model, d["raw"], d["m"])
        if len(xs) < 8:
            raise ValueError("transfer curve has fewer than 8 bins")
        forms, _ = fit_forms(xs, ys, ws)
        A_ = np.c_[xs, np.ones_like(xs)] * np.sqrt(ws / ws.sum())[:, None]
        coef = np.linalg.lstsq(A_, ys * np.sqrt(ws / ws.sum()), rcond=None)[0]
    except Exception:  # noqa: BLE001
        forms = none_forms; coef = np.array([np.nan, np.nan]); xs = ys = np.zeros(0)
    try:
        from scipy.optimize import curve_fit
        if len(xs) < 8:
            raise ValueError("no curve")
        pr, _ = curve_fit(lambda t, a_, b_, c_: a_ * np.exp(-b_ * t) + c_, xs, ys, p0=(max(ys.max(), 1.0), 1.0, 0.0), maxfev=4000,
                          bounds=((0, 0.02, -1e5), (1e9, 20, 1e5)))
        trans_raw = dict(I0=float(pr[0]), B=float(pr[1]), C=float(pr[2]))
    except Exception:  # noqa: BLE001
        trans_raw = dict(I0=None, B=None, C=None)
    fld = d["raw"][d["field"]]
    pct = np.percentile(fld, (1, 5, 50, 95, 99)) if fld.size else [np.nan] * 5
    tc, tm, bm = thickness_at_centre(d)
    shape = PH.field_shape(d["field"])
    border = PH.border_profile(d["raw"], d["field"])
    return dict(spec=d["spec"], pid=d["pid"], r2_global=1.0 - l_glob, r2_frame=1.0 - res_fun, s=th["s"], sigma_r=th["sigma_r"], alpha=th["alpha"],
                photons=ph["photons"], grain_sd=ph["grain_sd"], kf=kf, cf=cf, win_A=float(coef[1]), win_B=float(coef[0]),
                I0=trans_raw["I0"], B_trans=trans_raw["B"], C_trans=trans_raw["C"],
                transfer=dict(linear_r2=forms["linear"].get("r2"), transmission_r2=forms["transmission"].get("r2"), transmission_B=forms["transmission"].get("B"),
                              power_r2=forms["power"].get("r2"), power_gamma=forms["power"].get("gamma")),
                stored_p1=float(pct[0]), stored_p5=float(pct[1]), stored_p50=float(pct[2]), stored_p95=float(pct[3]), stored_p99=float(pct[4]),
                thickness_cm=tc, thickness_mean_cm=tm, bone_mean_cm=bm, field_frac=float(d["field"].mean()), trunc_frac=d["trunc_frac"], rot=d["rot"],
                shape=shape, border=border, meta=d["meta"], px_mm=d["px_mm"])


def per_frame_all(frames, theta_of, box, workers):
    from multiprocessing import get_context
    _G["theta_of"] = theta_of; _G["box"] = box
    with get_context("fork").Pool(workers) as pool:
        rows = pool.map(_perframe, list(range(len(frames))))
    return rows


# --------------------------------------------------------------------------------------------- distributions, sampler
COP_COLS = ["log10_photons", "s", "sigma_r", "alpha", "thickness_cm", "kvp", "log10_mas", "win_A", "win_B", "log10_I0", "lat_deg", "field_frac", "sigma_p_px", "halo"]


def frame_vector(r):
    m = r.get("meta", {}) or {}
    kv = m.get("kvp"); mas = m.get("mas")
    if mas is None and m.get("ma") is not None and m.get("ms") is not None:
        mas = float(m["ma"]) * float(m["ms"]) / 1000.0
    lat = m.get("lat_deg", m.get("lat_from_ap_deg"))
    return dict(log10_photons=(np.log10(r["photons"]) if r.get("photons") and np.isfinite(r["photons"]) and r["photons"] > 0 else np.nan),
                # .get with NaN: physics_defaults is also called (term tests) on rows that carry only meta / thickness /
                # field_frac / photons before the per-frame fit exists; the first smoke run died here on KeyError 's'
                s=r.get("s", np.nan), sigma_r=r.get("sigma_r", np.nan), alpha=r.get("alpha", np.nan), thickness_cm=r.get("thickness_cm", np.nan),
                kvp=(float(kv) if kv is not None else np.nan),
                log10_mas=(np.log10(mas) if mas else np.nan), win_A=r.get("win_A", np.nan), win_B=r.get("win_B", np.nan),
                log10_I0=(np.log10(r["I0"]) if r.get("I0") else np.nan), lat_deg=(abs(float(lat)) if lat is not None else np.nan),
                field_frac=r.get("field_frac", np.nan), sigma_p_px=(r["border"]["sigma_p_px"] if r.get("border") else np.nan),
                halo=(r["border"]["halo"] if r.get("border") else np.nan))


def copula_fit(rows, cols=None, nq=41):
    from scipy.stats import norm
    cols = list(cols) if cols is not None else list(_G.get("cop_cols", COP_COLS))
    V = np.array([[frame_vector(r)[c] for c in cols] for r in rows], np.float64)
    keep = [j for j, c in enumerate(cols) if np.isfinite(V[:, j]).sum() >= 8 and np.nanstd(V[:, j]) > 1e-9]
    const = {cols[j]: (float(np.nanmedian(V[:, j])) if np.isfinite(V[:, j]).any() else None) for j in range(len(cols)) if j not in keep}
    X = V[:, keep]; ok = np.all(np.isfinite(X), 1)
    X = X[ok]
    names = [cols[j] for j in keep]
    levels = np.linspace(0, 1, nq)
    q = {n: np.quantile(X[:, j], levels).tolist() for j, n in enumerate(names)}
    n = len(X)
    Z = np.zeros_like(X)
    for j in range(X.shape[1]):
        r = np.argsort(np.argsort(X[:, j])) + 1
        Z[:, j] = norm.ppf((r - 0.5) / n)
    C = np.corrcoef(Z, rowvar=False) if n > 3 else np.eye(len(names))
    C = np.atleast_2d(C); C = 0.98 * C + 0.02 * np.eye(len(names))
    return dict(names=names, levels=levels.tolist(), quantiles=q, corr=C.round(5).tolist(), n=int(n), constants=const)


def copula_sample(cop, n, rng, cond=None):
    """Draw n frame vectors; `cond` fixes some columns (e.g. thickness_cm) and the rest follow the conditional Gaussian."""
    from scipy.stats import norm
    names = cop["names"]; C = np.array(cop["corr"]); lv = np.array(cop["levels"])
    k = len(names)
    cond = cond or {}
    ci = [names.index(c) for c in cond if c in names]; fi = [j for j in range(k) if j not in ci]
    Z = np.zeros((n, k))
    if ci:
        zc = np.array([norm.ppf(np.clip(np.interp(cond[names[j]], cop["quantiles"][names[j]], lv), 0.005, 0.995)) for j in ci])
        Ccc = C[np.ix_(ci, ci)]; Cfc = C[np.ix_(fi, ci)]; Cff = C[np.ix_(fi, fi)]
        A = Cfc @ np.linalg.inv(Ccc)
        mu = A @ zc; cov = Cff - A @ Cfc.T
        cov = 0.5 * (cov + cov.T) + 1e-6 * np.eye(len(fi))
        Z[:, ci] = zc[None]; Z[:, fi] = rng.multivariate_normal(mu, cov, size=n)
    else:
        Z = rng.multivariate_normal(np.zeros(k), C, size=n)
    U = norm.cdf(Z)
    out = {}
    for j, nm in enumerate(names):
        out[nm] = np.interp(U[:, j], lv, cop["quantiles"][nm])
    for nm, v in cop.get("constants", {}).items():
        out[nm] = np.full(n, np.nan if v is None else v)
    return out


def coverage(train_rows, test_rows, n_draw=1000, seed=0):
    """Share of held-out frames whose per-frame terms fall inside the 1st-99th percentile of the sampler's draws, conditioned on
    each frame's own thickness; per term and jointly; plus the unconditional check."""
    cop = copula_fit(train_rows)
    rng = np.random.RandomState(seed)
    names = cop["names"]
    inside = {n: [] for n in names}; joint = []; inside_u = {n: [] for n in names}; joint_u = []
    for r in test_rows:
        v = frame_vector(r)
        cond = {"thickness_cm": v["thickness_cm"]} if ("thickness_cm" in names and np.isfinite(v["thickness_cm"])) else {}
        S = copula_sample(cop, n_draw, rng, cond); Su = copula_sample(cop, n_draw, rng, {})
        ok_all = True; ok_all_u = True
        for n in names:
            if n in cond or not np.isfinite(v[n]):
                continue
            lo, hi = np.percentile(S[n], (1, 99)); lou, hiu = np.percentile(Su[n], (1, 99))
            i = bool(lo <= v[n] <= hi); iu = bool(lou <= v[n] <= hiu)
            inside[n].append(i); inside_u[n].append(iu); ok_all &= i; ok_all_u &= iu
        joint.append(ok_all); joint_u.append(ok_all_u)
    # JOINT COVERAGE AS TYPICALITY, not as a product of boxes. "Inside every term's 1-99 %" over 14 terms is a 14-fold
    # product (0.99^14 = 0.87 even for the sampler's own draws) and read 0.03 on the first fit. The joint statistic
    # here is the copula's own: each held-out frame's normal-score vector z (its marginal quantiles through the
    # fitted quantile tables) and its Mahalanobis distance d2 = z' C^-1 z on the terms it has, against the 99th
    # percentile of d2 over the sampler's draws on the same terms. Coverage = share of held-out frames with
    # d2 <= d2_99: a frame the sampler would produce 99 % of the time counts as covered.
    mahal = _mahalanobis_coverage(cop, test_rows, rng)
    return dict(n_test=len(test_rows), conditional=dict(per_term={n: (float(np.mean(v)) if v else None) for n, v in inside.items()}, joint=float(np.mean(joint)) if joint else None),
                unconditional=dict(per_term={n: (float(np.mean(v)) if v else None) for n, v in inside_u.items()}, joint=float(np.mean(joint_u)) if joint_u else None),
                joint_boxes_note="'joint' above = inside every term's 1-99 % box at once (a product over terms; not the statistic to quote)",
                typicality=mahal, copula_n=cop["n"])


def _mahalanobis_coverage(cop, test_rows, rng, n_draw=4000, q=99.0):
    from scipy.stats import norm
    names = cop["names"]; C = np.array(cop["corr"]); lv = np.array(cop["levels"])
    Zs = rng.multivariate_normal(np.zeros(len(names)), C, size=n_draw)      # the sampler's own normal scores
    inside = []; d2s = []; dims = []
    for r in test_rows:
        v = frame_vector(r)
        idx = [j for j, n in enumerate(names) if np.isfinite(v.get(n, np.nan))]
        if len(idx) < 2:
            continue
        z = np.array([norm.ppf(np.clip(np.interp(v[names[j]], cop["quantiles"][names[j]], lv), 0.005, 0.995)) for j in idx])
        Ci = np.linalg.inv(C[np.ix_(idx, idx)] + 1e-6 * np.eye(len(idx)))
        d2 = float(z @ Ci @ z)
        Zd = Zs[:, idx]; d2_ref = np.einsum("ij,jk,ik->i", Zd, Ci, Zd)
        thr = float(np.percentile(d2_ref, q))
        inside.append(d2 <= thr); d2s.append(d2 / max(thr, 1e-9)); dims.append(len(idx))
    return dict(coverage_99=(float(np.mean(inside)) if inside else None), n=len(inside), d2_over_threshold_median=(float(np.median(d2s)) if d2s else None),
                d2_over_threshold_p90=(float(np.percentile(d2s, 90)) if d2s else None), terms_per_frame_median=(float(np.median(dims)) if dims else None),
                how=f"Mahalanobis distance of the frame's copula normal scores against the {q:.0f}th percentile of the sampler's own draws on the same terms")


def regress(x, y):
    x = np.asarray(x, np.float64); y = np.asarray(y, np.float64)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 6 or np.std(x[ok]) < 1e-9 or np.std(y[ok]) < 1e-9:
        return dict(n=int(ok.sum()), slope=None, intercept=None, resid_sd=None, r2=None,
                    note=("constant" if ok.sum() >= 6 else "too few frames"))
    k, c = np.polyfit(x[ok], y[ok], 1)
    res = y[ok] - (k * x[ok] + c)
    return dict(n=int(ok.sum()), slope=float(k), intercept=float(c), resid_sd=float(res.std()), r2=float(1 - res.var() / y[ok].var()),
                x_range=[float(x[ok].min()), float(x[ok].max())])


def aec_fit(rows):
    V = [frame_vector(r) for r in rows]
    t = [v["thickness_cm"] for v in V]
    out = {}
    for y in ("kvp", "log10_mas", "log10_photons", "s", "win_B", "log10_I0"):
        out[f"{y}_on_thickness"] = regress(t, [v[y] for v in V])
    out["log10_photons_on_kvp"] = regress([v["kvp"] for v in V], [v["log10_photons"] for v in V])
    out["kvp_on_lat_deg"] = regress([v["lat_deg"] for v in V], [v["kvp"] for v in V])
    return out


# ----------------------------------------------------------------------------------------------- residual by region
def partition(bone_cm, trunc, m, close_px=12, edge_px=2):
    from scipy.ndimage import binary_closing, binary_dilation, binary_erosion, binary_fill_holes
    bone = (bone_cm >= 0.3) & m
    edge = binary_dilation(bone, iterations=edge_px) & ~binary_erosion(bone, iterations=edge_px) & m
    interior = bone & ~edge
    enclosed = binary_fill_holes(binary_closing(bone, iterations=close_px)) & m & ~bone & ~edge
    outside = m & ~bone & ~edge & ~enclosed
    t = trunc & m
    return dict(truncated=t, bone_edge=edge & ~t, bone_interior=interior & ~t, enclosed_soft=enclosed & ~t, outside_soft=outside & ~t)


REGIONS = ["truncated", "bone_edge", "bone_interior", "enclosed_soft", "outside_soft", "field_border"]


def regions_one(d, th, RP):
    a_hat, _, _ = matched(forward(th, d, RP), d, d["m"])
    mf = d["m_full"]
    p1, p99 = np.percentile(d["atten"][mf], (1, 99)); g = 255.0 / max(p99 - p1, 1e-9)       # attenuation -> grey levels of a 1-99 window
    res = (d["atten"] - a_hat) * g
    regs = partition(d["bone"], ~d["hit"], d["m"]); regs["field_border"] = mf & ~d["m"]
    tot = float((res[mf] ** 2).sum())
    out = dict(explained_full=1.0 - float(res[mf].var()) / max(float((d["atten"][mf] * g).var()), 1e-9), rms=float(np.sqrt((res[mf] ** 2).mean())))
    for k, r in regs.items():
        n = int(r.sum())
        out[k] = dict(area=n / float(mf.sum()), energy=(float((res[r] ** 2).sum()) / max(tot, 1e-9)) if n else 0.0, bias=(float(res[r].mean()) if n else 0.0),
                      rms=(float(np.sqrt((res[r] ** 2).mean())) if n else 0.0))
    return out, res, a_hat


def _regions(i):
    d = _G["frames"][i]
    out, _, _ = regions_one(d, _G["theta_of"][d["spec"]], _G["RP"])
    return out


def regions_pooled(rows):
    if not rows:
        return None
    o = dict(n=len(rows), explained_full_median=float(np.median([r["explained_full"] for r in rows])), rms_median=float(np.median([r["rms"] for r in rows])))
    for k in REGIONS:
        o[k] = dict(area=float(np.median([r[k]["area"] for r in rows])), energy=float(np.median([r[k]["energy"] for r in rows])),
                    bias=float(np.median([r[k]["bias"] for r in rows])), bias_p10=float(np.percentile([r[k]["bias"] for r in rows], 10)),
                    bias_p90=float(np.percentile([r[k]["bias"] for r in rows], 90)), rms=float(np.median([r[k]["rms"] for r in rows])))
    return o


# ------------------------------------------------------------------------------------------------- physics defaults
def physics_defaults(dev, frames, rows, summ, folds, pitch):
    RP = _G["RP"]
    kvs = [r["meta"].get("kvp") for r in rows if r.get("meta", {}).get("kvp") is not None]
    kv_med = float(np.median(kvs)) if kvs else None
    w = np.concatenate([d["water"][d["m"]][::7] for d in frames[:40]]); b = np.concatenate([d["bone"][d["m"]][::7] for d in frames[:40]])
    out = {}
    if kv_med is not None:
        kb, mis = PH.kb_default(kv_med, w, b, RP)
        out["kb"] = dict(default=kb, rms_mismatch=mis, how=f"Kramers spectrum at the median kVp {kv_med:.0f} with 2.5 mm Al, NIST water / cortical bone, through these frames' paths")
    else:
        vals = {str(k): PH.kb_default(k, w, b, RP)[0] for k in (70, 90, 110)}
        out["kb"] = dict(default=None, range_by_kvp=vals, how="kVp not recorded for this device; the default at 70 / 90 / 110 kVp is given instead")
    tk = [r["thickness_cm"] for r in rows if np.isfinite(r["thickness_cm"])]
    thick = float(np.median(tk)) if tk else 20.0
    field_cm = float(np.median([r["field_frac"] for r in rows])) ** 0.5 * dev["panel_mm"][0] / 10.0 * (dev["sod_mm"] or 0.65 * dev["sid_mm"]) / dev["sid_mm"]
    spr, s_ = PH.spr_default(thick, field_cm, bool(dev.get("grid")))
    out["s"] = dict(default=s_, spr=spr, how=f"SPR {spr:.2f} for {thick:.0f} cm water, {field_cm:.0f} cm field at the patient, grid={dev.get('grid')} (Siewerdsen & Jaffray 2001, order of magnitude)")
    out["sigma_r"] = dict(default=PH.sigma_r_default(dev["detector_type"], dev["pixel_pitch_mm"], dev["down"]), how=f"{dev['detector_type']} scintillator sigma + binning box, in fit px")
    mas = [frame_vector(r)["log10_mas"] for r in rows]; mas = [10 ** v for v in mas if np.isfinite(v)]
    ph = PH.photons_default(kv_med, float(np.median(mas)) if mas else None, dev["sid_mm"], pitch, dev["detector_type"])
    out["photons"] = dict(default=ph, how="fluence(kVp) x mAs x (1 m/SID)^2 x pixel area x DQE" if ph else "kVp or mAs not recorded")
    sp_px, sp_mm = PH.penumbra_default(dev["focal_mm"], dev["sid_mm"], dev["coll_mm"], pitch)
    out["sigma_p"] = dict(default=sp_px, width_mm=sp_mm, how=f"focal {dev['focal_mm']} mm, collimator {dev['coll_mm']} mm from the source (assumed), SID {dev['sid_mm']}")
    out["c"] = dict(default=PH.heel_default(), how="|c| ~0.07 across a 30 cm field at 1 m; sign not predictable")
    if dev["detector_type"] == "ii":
        out["b"] = dict(default=PH.ii_defaults()["b"], how="intensifier vignetting ~25 % at the edge"); out["glare_frac"] = dict(default=PH.ii_defaults()["glare_frac"], how="veiling glare ~8 % of the mean")
    else:
        out["b"] = dict(default=0.0, how="flat panel with vendor flat-field: no vignette expected")
    out["alpha"] = dict(default=None, how="display unsharp gain: from the images alone (edge halo), see display_stage.from_images")
    out["sigma_u"] = dict(default=None, how="display unsharp radius: from the images alone (edge halo), see display_stage.from_images")
    # the gap: fitted median minus default, in units of the fold spread where there is one
    for n in list(out):
        if n in summ and out[n].get("default") is not None:
            gap = summ[n]["median"] - out[n]["default"]; sp = summ[n]["spread_p90_p10"]
            out[n]["fitted_median"] = summ[n]["median"]; out[n]["gap"] = float(gap); out[n]["gap_over_fold_spread"] = (float(abs(gap) / sp) if sp > 1e-9 else None)
    if out["photons"].get("default") and any(np.isfinite(r["photons"]) for r in rows):
        pm = float(np.nanmedian([r["photons"] for r in rows]))
        out["photons"].update(fitted_median=pm, gap_log10=float(np.log10(pm) - np.log10(out["photons"]["default"])))
    return out


# -------------------------------------------------------------------------------------------------- display stage
def display_from_images(frames, theta_of, RP, n=40):
    """Edge halo, NPS, histogram and gradient statistics of the real 8-bit display (OR window of the attenuation), the same for
    the calibrated render, restricted to cortical edges the CT names. What an unpaired device would be described by."""
    import deepfluoro_anchor as DA
    from scipy.ndimage import binary_dilation, binary_erosion
    S_real, S_rend = [], []
    for d in frames[:: max(1, len(frames) // n)]:
        f = d["field"] & d["hit"]
        real8 = np.clip(DA.window_or(d["atten"], f), 0, 255)
        a_hat, _, _ = matched(forward(theta_of[d["spec"]], d, RP), d, d["m"])
        rend8 = np.clip(DA.window_or(a_hat, f), 0, 255)
        bone = (d["bone"] >= 0.3)
        em = binary_dilation(bone, iterations=2) & ~binary_erosion(bone, iterations=2) & d["m"]
        S_real.append(PH.image_stats(real8, d["m"], edge_mask=em)); S_rend.append(PH.image_stats(rend8, d["m"], edge_mask=em))
    pr, pd = PH.pool_stats(S_real), PH.pool_stats(S_rend)
    return dict(real=pr, render_calibrated=pd, distance_render_vs_real=(PH.stat_distance(pd, pr) if pr and pd else None))


# ------------------------------------------------------------------------------------------------------------ figures
def fig_regions(dev, frames, theta_of, RP, pooled, path, n_show=3):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "sans-serif"})
    picks = frames[:: max(1, len(frames) // n_show)][:n_show]
    fig, axs = plt.subplots(n_show, 3, figsize=(12, 3.9 * n_show))
    axs = np.atleast_2d(axs)
    for i, d in enumerate(picks):
        out, res, a_hat = regions_one(d, theta_of[d["spec"]], RP)
        mf = d["m_full"]; lo, hi = np.percentile(d["atten"][mf], (1, 99))
        for j, (im, t) in enumerate(((d["atten"], "real, as attenuation"), (a_hat, "calibrated model, matched"))):
            axs[i, j].imshow(np.clip((im - lo) / max(hi - lo, 1e-9), 0, 1) * mf, cmap="gray", vmin=0, vmax=1); axs[i, j].set_title(f"{d['spec']}/{d['pid']}: {t}", fontsize=8)
        axs[i, 2].imshow(np.where(mf, res, 0), cmap="RdBu_r", vmin=-60, vmax=60); axs[i, 2].set_title(f"signed residual, grey of a 1-99 window (red: model too dark); explained {100 * out['explained_full']:.0f} %", fontsize=8)
        for a in axs[i]:
            a.set_xticks([]); a.set_yticks([])
    txt = "region          area  energy   bias    rms\n" + "\n".join(f"{k:15s} {100 * pooled[k]['area']:5.1f}% {100 * pooled[k]['energy']:6.1f}% {pooled[k]['bias']:+6.1f} {pooled[k]['rms']:6.1f}" for k in REGIONS)
    fig.text(0.01, 0.005, txt, family="monospace", fontsize=7, va="bottom")
    fig.suptitle(f"{dev['make']} {dev['model']}: residual by region over {pooled['n']} held-out frames (pooled medians below)", fontsize=10)
    fig.tight_layout(rect=(0, 0.12, 1, 0.97)); fig.savefig(path, dpi=110); plt.close(fig)


def fig_coverage(dev, rows, folds_of, cop_all, path, seed=0):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "sans-serif", "axes.grid": True, "grid.alpha": 0.3})
    rng = np.random.RandomState(seed)
    V = [frame_vector(r) for r in rows]
    S = copula_sample(cop_all, 4000, rng, {})
    pairs = [("thickness_cm", "kvp"), ("thickness_cm", "log10_photons"), ("win_A", "win_B"), ("thickness_cm", "s"), ("sigma_r", "alpha"), ("lat_deg", "log10_mas")]
    pairs = [(a, b) for a, b in pairs if a in S and b in S and np.isfinite(S[a]).any() and np.isfinite(S[b]).any()]
    if not pairs:
        return
    fig, axs = plt.subplots(2, 3, figsize=(14, 8)); axs = axs.ravel()
    for ax, (a, b) in zip(axs, pairs):
        ax.scatter(S[a], S[b], s=4, color="#b7c1cc", alpha=0.35, label="sampler (unconditional)")
        xa = [v[a] for v in V]; xb = [v[b] for v in V]
        ax.scatter(xa, xb, s=12, color="#c0392b", alpha=0.85, label="real frames (every fold held out)")
        ax.set_xlabel(a); ax.set_ylabel(b)
    axs[0].legend(fontsize=7)
    for ax in axs[len(pairs):]:
        ax.axis("off")
    fig.suptitle(f"{dev['make']} {dev['model']}: the sampled cloud and the real frames", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.96)); fig.savefig(path, dpi=110); plt.close(fig)


def fig_frames(dev, frames, theta_of, RP, path, n=6):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import deepfluoro_anchor as DA
    picks = frames[:: max(1, len(frames) // n)][:n]
    fig, axs = plt.subplots(2, len(picks), figsize=(2.6 * len(picks), 5.6))
    axs = np.atleast_2d(axs)
    for j, d in enumerate(picks):
        f = d["field"] & d["hit"]
        if os.environ.get("DF_WINDOW_REGION") == "body":
            # A31 display fix, panels only (the fit and its statistics are untouched): on a small specimen in a
            # large exposed field -- the Ljubljana turntable frames -- air sets p1/p5 and crushes the body's greys.
            # The region comes from the REAL frame's attenuation and is applied to both tiles: identical treatment.
            f = DA.window_region_body(d["atten"], f)[0]
        a_hat, _, _ = matched(forward(theta_of[d["spec"]], d, RP), d, d["m"])
        axs[0, j].imshow(DA.window_or(d["atten"], f), cmap="gray", vmin=0, vmax=255); axs[0, j].set_title(f"real {d['spec']}/{d['pid']}", fontsize=7)
        axs[1, j].imshow(DA.window_or(a_hat, f) * d["field"], cmap="gray", vmin=0, vmax=255); axs[1, j].set_title("calibrated render", fontsize=7)
        for a in axs[:, j]:
            a.set_xticks([]); a.set_yticks([])
    fig.suptitle(f"{dev['make']} {dev['model']}: real frames (top) and the calibrated model (bottom), both through the OR window", fontsize=9)
    fig.tight_layout(); fig.savefig(path, dpi=110); plt.close(fig)


def fig_transfer(dev, rows, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "sans-serif", "axes.grid": True, "grid.alpha": 0.3})
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
    B = [r["transfer"]["transmission_B"] for r in rows if r["transfer"]["transmission_B"]]
    g = [r["transfer"]["power_gamma"] for r in rows if r["transfer"]["power_gamma"]]
    ax[0].hist(B, bins=30, color="#2a78d6"); ax[0].set_title("transmission-form decay B per frame (1 = linear signal)", fontsize=8)
    ax[1].hist(g, bins=30, color="#eb6834"); ax[1].set_title("power-form gamma per frame (1 = log display read linearly)", fontsize=8)
    r2 = np.array([[r["transfer"]["transmission_r2"] or 0, r["transfer"]["linear_r2"] or 0, r["transfer"]["power_r2"] or 0] for r in rows])
    ax[2].boxplot([r2[:, 0], r2[:, 1], r2[:, 2]], tick_labels=["transmission", "linear", "power"]); ax[2].set_title("R2 of each form, per frame", fontsize=8)
    fig.suptitle(f"{dev['make']} {dev['model']}: what function of the model attenuation the stored value is", fontsize=9)
    fig.tight_layout(); fig.savefig(path, dpi=110); plt.close(fig)


def fig_border(dev, rows, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "sans-serif", "axes.grid": True, "grid.alpha": 0.3})
    bs = [r["border"] for r in rows if r.get("border")]
    if not bs:
        return
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
    for b in bs[:200]:
        ax[0].plot(b["t"], b["profile"], color="#8a949d", alpha=0.08, lw=0.8)
    ax[0].plot(bs[0]["t"], np.median(np.array([b["profile"] for b in bs]), 0), color="#1b3a6b", lw=2, label="median")
    ax[0].set_xlabel("px from the border (inward +)"); ax[0].set_ylabel("stored value, normalised"); ax[0].legend(fontsize=7); ax[0].set_title("border profile", fontsize=8)
    ax[1].hist([b["sigma_p_px"] * rows[0]["px_mm"] for b in bs], bins=25, color="#2a78d6"); ax[1].set_title("penumbra sigma, mm", fontsize=8)
    ax[2].hist([b["halo"] for b in bs], bins=25, color="#eb6834"); ax[2].set_title("processing halo at the border (fraction of the interior level)", fontsize=8)
    fig.suptitle(f"{dev['make']} {dev['model']}: the collimator border over {len(bs)} frames", fontsize=9)
    fig.tight_layout(); fig.savefig(path, dpi=110); plt.close(fig)


# ------------------------------------------------------------------------------------------------------- schema out
def qdist(vals):
    v = np.array([x for x in vals if x is not None and np.isfinite(x)], np.float64)
    if v.size == 0:
        return None
    return dict(n=int(v.size), median=float(np.median(v)), p1=float(np.percentile(v, 1)), p10=float(np.percentile(v, 10)), p90=float(np.percentile(v, 90)),
                p99=float(np.percentile(v, 99)), min=float(v.min()), max=float(v.max()))


def write_frames_csv(rows, path):
    cols = ["spec", "pid", "kvp", "ma", "ms", "mas", "window_center", "window_width", "angle", "lat_deg", "view", "r2_global", "r2_frame", "s", "sigma_r", "alpha", "photons",
            "grain_sd", "kf", "cf", "win_A", "win_B", "I0", "B_trans", "C_trans", "transfer_linear_r2", "transfer_transmission_r2", "transfer_transmission_B", "transfer_power_r2",
            "transfer_power_gamma", "stored_p1", "stored_p5", "stored_p50", "stored_p95", "stored_p99", "thickness_cm", "thickness_mean_cm", "bone_mean_cm", "field_frac", "field_shape",
            "field_left", "field_right", "field_top", "field_bottom", "field_radius", "sigma_p_px", "border_halo", "trunc_frac", "rot", "px_mm"]
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(cols)
        for r in rows:
            m = r.get("meta", {}) or {}; sh = r.get("shape") or {}; b = r.get("border") or {}
            mas = m.get("mas")
            if mas is None and m.get("ma") is not None and m.get("ms") is not None:
                mas = float(m["ma"]) * float(m["ms"]) / 1000.0
            w.writerow([r["spec"], r["pid"], m.get("kvp"), m.get("ma"), m.get("ms"), mas, m.get("window_center"), m.get("window_width"), m.get("angle"),
                        m.get("lat_deg", m.get("lat_from_ap_deg")), m.get("view"), r["r2_global"], r["r2_frame"], r["s"], r["sigma_r"], r["alpha"], r["photons"], r["grain_sd"],
                        r["kf"], r["cf"], r["win_A"], r["win_B"], r["I0"], r["B_trans"], r["C_trans"], r["transfer"]["linear_r2"], r["transfer"]["transmission_r2"],
                        r["transfer"]["transmission_B"], r["transfer"]["power_r2"], r["transfer"]["power_gamma"], r["stored_p1"], r["stored_p5"], r["stored_p50"], r["stored_p95"],
                        r["stored_p99"], r["thickness_cm"], r["thickness_mean_cm"], r["bone_mean_cm"], r["field_frac"], sh.get("shape"), sh.get("left"), sh.get("right"), sh.get("top"),
                        sh.get("bottom"), sh.get("radius"), b.get("sigma_p_px"), b.get("halo"), r["trunc_frac"], r["rot"], r["px_mm"]])


def code_sha():
    try:
        import subprocess
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=str(Path(__file__).resolve().parents[1])).decode().strip()
    except Exception:  # noqa: BLE001
        return None


# ----------------------------------------------------------------------------------------------------------- fit cmd
def cmd_reperframe(a):
    """Recompute the per-frame terms, the copula, the AEC and the coverage of an existing card from its own fold terms,
    with a chosen set of free per-frame terms (--perframe-free photons|s,sigma_r,alpha), without refitting the folds."""
    import render_physics_drr as RP_
    dev = DEVICES[a.device]
    RP = (RP_.ENERGIES.numpy(), RP_.SPECTRUM.numpy(), RP_.MU_WATER.numpy(), RP_.MU_BONE.numpy())
    card_p = DOCS / f"{a.device}.json"
    if not card_p.exists():
        raise SystemExit(f"no card {card_p}")
    card = json.load(open(card_p)); folds = card["physics_terms"]["folds"]; free9 = card["physics_terms"]["names"]
    out_dir = Path(ROOT) / a.device; out_dir.mkdir(parents=True, exist_ok=True)
    frames = load_frames(dev, a.limit)
    _G["frames"] = frames; _G["RP"] = RP
    groups = sorted({d["spec"] for d in frames})
    box, x0, pitch = px_box(dev)
    if len(groups) > a.max_folds:                       # the same fold assignment the fit used
        fold_of = {g: int(hashlib.md5(g.encode()).hexdigest(), 16) % a.max_folds for g in groups}
        for d in frames:
            d["spec_orig"] = d["spec"]; d["spec"] = f"fold{fold_of[d['spec']]}"
        groups = sorted({d["spec"] for d in frames})
    theta_of = {}
    med = {n: float(card["physics_terms"]["fitted"][n]["median"]) for n in free9}
    for g in groups:
        f = next((f for f in folds if f["held"] == g), None)
        base = dict(f["theta"]) if f else dict(med)
        for k in ("sigma_p", "s_t", "b4"):
            base.setdefault(k, 0.0)
        theta_of[g] = base
    pf = [] if a.perframe_free in ("photons", "none", "") else [x for x in a.perframe_free.split(",") if x]
    _G["pf_free"] = pf; _G["pf_maxiter"] = a.var_maxiter if pf else 0
    # terms that are fold constants are not per-frame draws: keep them out of the copula and the coverage
    _G["cop_cols"] = [c for c in COP_COLS if c in pf or c not in ("s", "sigma_r", "alpha")]
    print(f"{a.device}: {len(frames)} frames, {len(groups)} groups; per-frame free terms {pf or ['photons only']}; copula columns {_G['cop_cols']}", flush=True)
    rows = per_frame_all(frames, theta_of, box, a.workers)
    for r, d in zip(rows, frames):
        r["group"] = d.get("spec_orig", d["spec"]); r["fold"] = d["spec"]
    print(f"  photons: {qdist([r['photons'] for r in rows])}", flush=True)
    write_frames_csv(rows, DOCS / f"{a.device}.frames.csv")
    cop_all = copula_fit(rows); aec = aec_fit(rows)
    cov_folds = []
    for g in groups:
        tr = [r for r in rows if r["fold"] != g]; te = [r for r in rows if r["fold"] == g]
        if len(tr) >= 10 and te:
            c = coverage(tr, te, seed=a.seed); c["held"] = g; cov_folds.append(c)
    w = np.array([c["n_test"] for c in cov_folds], float) if cov_folds else None
    typ = [c["typicality"]["coverage_99"] for c in cov_folds]
    cov = dict(per_fold=cov_folds, typicality_99=(float(np.average([t if t is not None else np.nan for t in typ], weights=w)) if cov_folds else None),
               conditional=dict(joint=float(np.average([c["conditional"]["joint"] for c in cov_folds], weights=w)) if cov_folds else None),
               statistic_to_quote="typicality_99")
    card["distribution"].update(copula=cop_all, aec=aec, coverage=cov, per_frame_free=(pf or ["photons"]), reperframe_date=time.strftime("%Y-%m-%d %H:%M"))
    pt = card["physics_terms"]
    pt.update(photons_per_fit_px=qdist([r["photons"] for r in rows]), photons_per_mm2=qdist([r["photons"] / pitch ** 2 for r in rows]),
              scatter_fraction_per_frame=qdist([r["s"] for r in rows]), blur_sigma_per_frame_px=qdist([r["sigma_r"] for r in rows]), alpha_per_frame=qdist([r["alpha"] for r in rows]),
              per_frame_r2=qdist([r["r2_frame"] for r in rows]), per_frame_free=(pf or ["photons"]))
    dump = lambda o: None if isinstance(o, float) and not np.isfinite(o) else (o.tolist() if hasattr(o, "tolist") else str(o))  # noqa: E731
    json.dump(card, open(card_p, "w"), indent=1, default=dump)
    json.dump(dict(rows=rows), open(out_dir / "per_frame.json", "w"), default=dump)
    fig_coverage(dev, rows, None, cop_all, out_dir / "fig_coverage.png")
    print(f"{a.device}: typicality_99 {cov['typicality_99']}; photons per mm2 {pt['photons_per_mm2']}", flush=True)
    return 0


def cmd_recoverage(a):
    """Recompute the coverage block of docs/devices/<device>.json from the saved per-frame rows (the fits that ran before
    the typicality statistic existed), without refitting anything."""
    src = Path(ROOT) / a.device / "per_frame.json"
    if not src.exists():
        raise SystemExit(f"{a.device}: no {src}")
    rows = json.load(open(src))["rows"]
    groups = sorted({r["fold"] for r in rows})
    cov_folds = []
    for g in groups:
        tr = [r for r in rows if r["fold"] != g]; te = [r for r in rows if r["fold"] == g]
        if len(tr) >= 10 and te:
            c = coverage(tr, te, seed=a.seed); c["held"] = g; cov_folds.append(c)
    if not cov_folds:
        raise SystemExit("no fold with >= 10 training frames")
    w = np.array([c["n_test"] for c in cov_folds], float)
    names = copula_fit(rows)["names"]
    typ = [c["typicality"]["coverage_99"] for c in cov_folds]
    cov = dict(per_fold=cov_folds,
               conditional=dict(joint=float(np.average([c["conditional"]["joint"] for c in cov_folds], weights=w)),
                                per_term={n: float(np.mean([c["conditional"]["per_term"][n] for c in cov_folds if c["conditional"]["per_term"].get(n) is not None] or [np.nan])) for n in names}),
               unconditional=dict(joint=float(np.average([c["unconditional"]["joint"] for c in cov_folds], weights=w)),
                                  per_term={n: float(np.mean([c["unconditional"]["per_term"][n] for c in cov_folds if c["unconditional"]["per_term"].get(n) is not None] or [np.nan])) for n in names}),
               typicality_99=float(np.average([t if t is not None else np.nan for t in typ], weights=w)),
               statistic_to_quote="typicality_99 (Mahalanobis in copula normal scores against the sampler's own 99th percentile); 'joint' is a product of per-term boxes")
    card = DOCS / f"{a.device}.json"
    js = json.load(open(card)) if card.exists() else {}
    js.setdefault("distribution", {})["coverage"] = cov
    json.dump(js, open(card, "w"), indent=1, default=lambda o: None if isinstance(o, float) and not np.isfinite(o) else (o.tolist() if hasattr(o, "tolist") else str(o)))
    print(f"{a.device}: typicality_99 {cov['typicality_99']:.3f} over {int(w.sum())} held-out frames in {len(cov_folds)} folds; per-term (conditional) "
          + ", ".join(f"{n} {v:.2f}" for n, v in cov["conditional"]["per_term"].items() if np.isfinite(v)), flush=True)
    return 0


# WHOSE BODY each device's frames show, for the held-out gate (tools/eval_gate.py). A fold is patient-held-out only when
# the held group's subjects appear in no frame the fold fits on. Where a device's dataset is ONE subject, every frame is
# that subject and no fold can be (a view- or frame-held-out fit of one phantom or one cadaver).
SUBJECT_OF = {"cios_fusion": ("deepfluoro", None), "surgio_b51_dr": ("carmlspine", None), "surgio_b51_raw": ("carmlspine", None),
              "elekta_xvi": ("cobra", None), "varian_halcyon": ("cobra", None),
              "pixium_4600": ("ljubljana", "ljubljana:LJ-L1L5"),     # ONE cadaver L1-L5 (Tomazevic 2002)
              "bv_pulsera": ("geneva", "geneva:phantom")}             # ONE resin phantom (D'Isidoro 2021)


def fold_gate(device, frames, groups, not_held_out=None):
    """One eval_gate header per leave-one-group-out fold: the held group's subjects against the subjects of every frame
    the fold may fit on (the other groups; run_loso fits a subset of them, so this is the conservative side)."""
    hint, const = SUBJECT_OF.get(device, (None, None))
    def keys(ds):
        if const:
            return {const}
        k, _, unk = EG.key_items([dict(case=d["subject_spec"], hint=hint) for d in ds])
        return k | {f"unkeyed:{u[0]}" for u in unk}
    hdrs = []
    for g in groups:
        held = [d for d in frames if d["spec"] == g]; fit = [d for d in frames if d["spec"] != g]
        hk = keys(held)
        items = [k for k in hk if not k.startswith("unkeyed:")] + [dict(name=k[8:]) for k in hk if k.startswith("unkeyed:")]
        hdrs.append(EG.assert_unseen(items, None, f"tools/device_fit.py fit {device} fold held={g}", eval_set=f"{device} group {g}",
                                     also_seen={f"frames fitted with {g} held out": keys(fit)}, not_held_out=not_held_out))
    return EG.block(hdrs, not_held_out)


def cmd_gate(a):
    """The per-fold patient gate ALONE, from the pair file names (no fit, no pixels): the folds cmd_fit would build
    (the same groups, the same md5 folding), every held group's subjects against every other group's. Writes
    docs/devices/eval_gate/<device>.json -- the record leak_check CHK-9 reads for the card's quoted rows (a subdirectory,
    so nothing that globs docs/devices/*.json for cards reads it as one) -- whatever
    the verdict; exits 1 when a fold's held subjects were fitted on and nothing declared it."""
    dev = DEVICES[a.device]
    files = sorted(glob.glob(os.path.join(dev["pairs"], "pair_*.npz")))
    if not files:
        raise SystemExit(f"{a.device}: no pairs under {dev['pairs']}")
    frames = []
    for p in files:
        stem = Path(p).stem.replace("pair_", ""); spec, pid = stem.rsplit("_", 1)
        frames.append(dict(spec=(pid if dev.get("group_by_pid") else spec), subject_spec=spec))
    groups = sorted({d["spec"] for d in frames})
    if len(groups) > a.max_folds:
        fold_of = {g: int(hashlib.md5(g.encode()).hexdigest(), 16) % a.max_folds for g in groups}
        for d in frames:
            d["spec"] = f"fold{fold_of[d['spec']]}"
        groups = sorted({d["spec"] for d in frames})
    hint, const = SUBJECT_OF.get(a.device, (None, None))
    hdrs = []
    for g in groups:
        held = [d for d in frames if d["spec"] == g]; fit = [d for d in frames if d["spec"] != g]
        k = (lambda ds: {const} if const else EG.key_items([dict(case=d["subject_spec"], hint=hint) for d in ds])[0])
        hdrs.append(EG.assess(sorted(k(held)), None, f"tools/device_fit.py gate {a.device} fold held={g}",
                              eval_set=f"{a.device} group {g}", also_seen={f"frames fitted with {g} held out": k(fit)},
                              not_held_out=a.not_held_out))
    blk = EG.block(hdrs, a.not_held_out)
    blk.update(device=a.device, pairs_dir=dev["pairs"], n_pairs=len(files), n_folds=len(groups), group=dev["group"],
               subject_rule=(f"one subject ({const})" if const else f"the pair's group id, keyed as {hint}"))
    out = DOCS / "eval_gate" / f"{a.device}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    json.dump(blk, open(out, "w"), indent=1)
    seen = [h["eval_set"] for h in hdrs if h["overlap"]]
    print(f"{a.device}: {len(groups)} folds, {len(seen)} whose held subjects were fitted on "
          f"({', '.join(seen[:6])}); held_out={blk['held_out']} -> {out}", flush=True)
    return 1 if (seen and not a.not_held_out) else 0


def cmd_fit(a):
    import render_physics_drr as RP_
    dev = DEVICES[a.device]
    RP = (RP_.ENERGIES.numpy(), RP_.SPECTRUM.numpy(), RP_.MU_WATER.numpy(), RP_.MU_BONE.numpy())
    out_dir = Path(ROOT) / a.device; out_dir.mkdir(parents=True, exist_ok=True); DOCS.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    frames = load_frames(dev, a.limit)
    if not frames:
        raise SystemExit(f"{a.device}: no pairs under {dev['pairs']}")
    _G["frames"] = frames; _G["RP"] = RP
    groups = sorted({d["spec"] for d in frames})
    box, x0, pitch = px_box(dev)
    print(f"{a.device}: {len(frames)} frames, {len(groups)} groups ({dev['group']}), fit pitch {pitch:.4f} mm, truncated median {100 * np.median([d['trunc_frac'] for d in frames]):.1f} %", flush=True)
    # group folds: leave-one-group-out, or K folds of groups when there are many groups
    if len(groups) > a.max_folds:
        fold_of = {g: int(hashlib.md5(g.encode()).hexdigest(), 16) % a.max_folds for g in groups}
        for d in frames:
            d["spec_orig"] = d["spec"]; d["spec"] = f"fold{fold_of[d['spec']]}"
        groups = sorted({d["spec"] for d in frames})
        print(f"  {a.max_folds} folds of groups: " + ", ".join(f"{g}: {sum(1 for d in frames if d['spec'] == g)} frames" for g in groups), flush=True)
    # THE GATE, before any fold is fitted: a fold whose held subjects are also fitted on raises unless --not-held-out
    gate = fold_gate(a.device, frames, groups, a.not_held_out)
    base_all = explained(baseline_theta(x0), frames, RP)
    print(f"uncalibrated physics + linear match, all frames: {100 * base_all:.1f} % explained", flush=True)
    free9 = list(NAMES9)
    print("\n===== nine terms, leave-one-group-out", flush=True)
    folds = run_loso(frames, groups, free9, box, x0, a.workers, a.maxiter, a.fit_frames, a.seed)
    summ = fold_summary(folds, free9)
    theta_of = {g: theta_for_group(folds, g) for g in groups}
    for d in frames:
        if theta_of.get(d["spec"]) is None:
            theta_of[d["spec"]] = {n: summ[n]["median"] for n in free9} | dict(sigma_p=0.0, s_t=0.0, b4=0.0)
    gains = [f["calibrated"] - f["baseline"] for f in folds]
    print(f"\nheld-out gain: median {100 * np.median(gains):+.1f} (min {100 * min(gains):+.1f}, max {100 * max(gains):+.1f})", flush=True)
    for n in free9:
        print(f"  {n:8s} median {summ[n]['median']:8.3f}  spread {summ[n]['spread_p90_p10']:7.3f}  at bound in {summ[n]['at_bound_folds']} folds", flush=True)
    # the reproduction check against the shipped DeepFluoro calibration
    repro = None
    if dev.get("cios_exact"):
        cal = json.load(open(os.path.expanduser("~/model_night/deepfluoro/calibration_linear.json")))
        rows_ = []
        for f in folds:
            ref = [x for x in cal["folds"] if x["held"] == f["held"]]
            if ref:
                rt = dict(zip(cal["names"], ref[0]["theta"]))
                rows_.append(dict(held=f["held"], max_abs_theta_diff=float(max(abs(f["theta"][n] - rt[n]) for n in NAMES9)), calibrated_here=f["calibrated"], calibrated_shipped=ref[0]["calibrated"],
                                  shipped_theta_scored_here=explained({**rt, "sigma_p": 0.0, "s_t": 0.0, "b4": 0.0}, [d for d in frames if d["spec"] == f["held"]], RP)))
        repro = rows_
        print("\nreproduction of calibration_linear.json:", json.dumps(rows_, indent=0)[:1500], flush=True)
    # ---- the term tests (C): which physics-derived terms raise the held-out R2
    variants = {}
    if a.variants:
        print("\n===== term tests: each variant refitted leave-one-group-out (fit-frames %d, maxiter %d)" % (a.var_frames, a.var_maxiter), flush=True)
        defs = physics_defaults(dev, frames, [dict(meta=d["meta"], thickness_cm=thickness_at_centre(d)[0], field_frac=float(d["field"].mean()), photons=np.nan) for d in frames[:60]], summ, folds, pitch)
        vdefs = {"base9": (free9, dict(x0)),
                 "+penumbra": (free9 + ["sigma_p"], dict(x0, sigma_p=max(0.5, defs["sigma_p"]["default"]))),
                 "+scatter_follows_thickness": (free9 + ["s_t"], dict(x0, s_t=10.0)),
                 "sigma_r_fixed_physics": ([n for n in free9 if n != "sigma_r"], dict(x0, sigma_r=float(np.clip(defs["sigma_r"]["default"], *box["sigma_r"])))),
                 }
        if defs["kb"].get("default") is not None:
            vdefs["kb_fixed_from_kVp"] = ([n for n in free9 if n != "kb"], dict(x0, kb=float(np.clip(defs["kb"]["default"], *box["kb"]))))
        if dev["detector_type"] == "ii":
            vdefs["+quartic_vignette"] = (free9 + ["b4"], dict(x0, b4=0.0))
        for name, (fr, xv) in vdefs.items():
            print(f"\n--- {name}", flush=True)
            vf = run_loso(frames, groups, fr, box, xv, a.workers, a.var_maxiter, a.var_frames, a.seed)
            variants[name] = dict(free=fr, held_out_r2_median=float(np.median([f["calibrated"] for f in vf])), held_out_r2_full_median=float(np.median([f["calibrated_full"] for f in vf])),
                                  folds=[dict(held=f["held"], calibrated=f["calibrated"], calibrated_full=f["calibrated_full"], theta={n: f["theta"][n] for n in fr}, at_bound=f["at_bound"]) for f in vf],
                                  terms=fold_summary(vf, fr))
        b0 = variants["base9"]
        for name, v in variants.items():
            v["delta_r2_vs_base9"] = v["held_out_r2_median"] - b0["held_out_r2_median"]; v["delta_r2_full_vs_base9"] = v["held_out_r2_full_median"] - b0["held_out_r2_full_median"]
            print(f"{name:28s} held-out R2 {100 * v['held_out_r2_median']:5.1f} ({100 * v['delta_r2_vs_base9']:+.2f})   full field {100 * v['held_out_r2_full_median']:5.1f} ({100 * v['delta_r2_full_vs_base9']:+.2f})", flush=True)
    # ---- per-frame terms under each group's held-out theta
    print("\n===== per-frame terms", flush=True)
    rows = per_frame_all(frames, theta_of, box, a.workers)
    for r, d in zip(rows, frames):
        r["group"] = d.get("spec_orig", d["spec"]); r["fold"] = d["spec"]
    print(f"  photons: {qdist([r['photons'] for r in rows])}", flush=True)
    print(f"  s per frame: {qdist([r['s'] for r in rows])}", flush=True)
    write_frames_csv(rows, DOCS / f"{a.device}.frames.csv")
    # ---- distributions, AEC, coverage (copula fitted on the training folds, scored on each held-out fold)
    cop_all = copula_fit(rows)
    aec = aec_fit(rows)
    cov_folds = []
    for g in groups:
        tr = [r for r in rows if r["fold"] != g]; te = [r for r in rows if r["fold"] == g]
        if len(tr) >= 10 and te:
            c = coverage(tr, te, seed=a.seed); c["held"] = g; cov_folds.append(c)
    cov = None
    if cov_folds:
        names = cop_all["names"]
        cov = dict(per_fold=cov_folds,
                   conditional=dict(joint=float(np.average([c["conditional"]["joint"] for c in cov_folds if c["conditional"]["joint"] is not None], weights=[c["n_test"] for c in cov_folds if c["conditional"]["joint"] is not None])),
                                    per_term={n: float(np.mean([c["conditional"]["per_term"][n] for c in cov_folds if c["conditional"]["per_term"].get(n) is not None] or [np.nan])) for n in names}),
                   unconditional=dict(joint=float(np.average([c["unconditional"]["joint"] for c in cov_folds if c["unconditional"]["joint"] is not None], weights=[c["n_test"] for c in cov_folds if c["unconditional"]["joint"] is not None])),
                                      per_term={n: float(np.mean([c["unconditional"]["per_term"][n] for c in cov_folds if c["unconditional"]["per_term"].get(n) is not None] or [np.nan])) for n in names}))
        print("coverage (held-out frames inside the sampler's 1-99 %):", json.dumps(cov["conditional"])[:600], flush=True)
    # ---- residual by region, transfer summary, physics defaults, images-only display statistics
    from multiprocessing import get_context
    _G["theta_of"] = theta_of
    with get_context("fork").Pool(a.workers) as pool:
        reg_rows = pool.map(_regions, list(range(len(frames))))
    pooled = regions_pooled(reg_rows)
    print("\nresidual by region (pooled medians, grey levels of a 1-99 window, + = model too dark):", flush=True)
    for k in REGIONS:
        print(f"  {k:15s} area {100 * pooled[k]['area']:5.1f}%  energy {100 * pooled[k]['energy']:5.1f}%  bias {pooled[k]['bias']:+6.1f}  rms {pooled[k]['rms']:5.1f}", flush=True)
    tr_forms = {}
    for form in ("transmission", "linear", "power"):
        r2 = np.array([r["transfer"][f"{form}_r2"] for r in rows if r["transfer"][f"{form}_r2"] is not None])
        tr_forms[form] = dict(r2_median=float(np.median(r2)) if r2.size else None, r2_p10=float(np.percentile(r2, 10)) if r2.size else None)
    wins = [max(("transmission", "linear", "power"), key=lambda f: (r["transfer"][f"{f}_r2"] if r["transfer"][f"{f}_r2"] is not None else -9)) for r in rows]
    tr_forms["winner_share"] = {f: float(np.mean([w == f for w in wins])) for f in ("transmission", "linear", "power")}
    tr_forms["transmission_B_median"] = float(np.nanmedian([r["transfer"]["transmission_B"] or np.nan for r in rows]))
    tr_forms["power_gamma_median"] = float(np.nanmedian([r["transfer"]["power_gamma"] or np.nan for r in rows]))
    print("transfer test:", json.dumps(tr_forms), flush=True)
    defs = physics_defaults(dev, frames, rows, summ, folds, pitch)
    dimg = display_from_images(frames, theta_of, RP)
    # ---- figures
    fig_regions(dev, frames, theta_of, RP, pooled, out_dir / "fig_regions.png")
    fig_coverage(dev, rows, None, cop_all, out_dir / "fig_coverage.png")
    fig_frames(dev, frames, theta_of, RP, out_dir / "fig_frames.png")
    fig_transfer(dev, rows, out_dir / "fig_transfer.png")
    fig_border(dev, rows, out_dir / "fig_border.png")
    # ---- the schema JSON
    shapes = [r["shape"] for r in rows if r.get("shape") and r["shape"].get("shape")]
    borders = [r["border"] for r in rows if r.get("border")]
    kv = [r["meta"].get("kvp") for r in rows]; ma = [r["meta"].get("ma") for r in rows]; ms = [r["meta"].get("ms") for r in rows]
    mas = [frame_vector(r)["log10_mas"] for r in rows]
    at_bound_terms = [n for n in free9 if summ[n]["at_bound_folds"] >= max(1, len(folds) // 2)]
    js = dict(
        device=dict(name=a.device, make=dev["make"], model=dev["model"], dataset=dev["dataset"], detector_type=dev["detector_type"], pixel_pitch_mm=dev["pixel_pitch_mm"],
                    panel_mm=dev["panel_mm"], image_size=dev["image_size"], field_shape=(max(set(s["shape"] for s in shapes), key=[s["shape"] for s in shapes].count) if shapes else None),
                    field_shape_share_circle=(float(np.mean([s["shape"] == "circle" for s in shapes])) if shapes else None),
                    SID_mm=dev["sid_mm"], SOD_or_SAD_mm=dev["sod_mm"], stored_form=dev["stored_form"], reading=dev["reading"], orientation_convention=dev["orientation"],
                    rot180_share=float(np.mean([r["rot"] for r in rows])), grid=dev.get("grid"), fit_pitch_mm=pitch, fit_image_size=list(frames[0]["raw"].shape), fit_down=dev["down"]),
        exposure_range=dict(kvp=qdist(kv), ma=qdist(ma), ms=qdist(ms), mas=qdist([10 ** v if np.isfinite(v) else None for v in mas]),
                            window_center=qdist([r["meta"].get("window_center") for r in rows]), window_width=qdist([r["meta"].get("window_width") for r in rows]),
                            lat_from_ap_deg=qdist([frame_vector(r)["lat_deg"] for r in rows]), source="DICOM / metadata of the paired frames" if any(v is not None for v in kv) else "not recorded in this dataset",
                            documented_ranges=None),
        physics_terms=dict(names=free9, units={n: ("px at fit pitch" if n in PX_TERMS else "-") for n in free9 + ["sigma_p"]},
                           fitted={n: dict(summ[n], value_mm=(summ[n]["median"] * pitch if n in PX_TERMS else None), bounds=[box[n][0], box[n][1]],
                                           bounds_mm=([box[n][0] * pitch, box[n][1] * pitch] if n in PX_TERMS else None), bound_source=BOX_SOURCE.get(n),
                                           at_bound=(summ[n]["at_bound_folds"] >= max(1, len(folds) // 2))) for n in free9},
                           at_bound_terms=at_bound_terms,
                           folds=[dict(held=f["held"], n=f["n"], n_fit=f["n_fit"], baseline=f["baseline"], calibrated=f["calibrated"], baseline_full=f["baseline_full"], calibrated_full=f["calibrated_full"],
                                       theta={n: f["theta"][n] for n in free9}, at_bound=f["at_bound"]) for f in folds],
                           held_out_r2_median=float(np.median([f["calibrated"] for f in folds])), baseline_r2_median=float(np.median([f["baseline"] for f in folds])),
                           held_out_gain_median=float(np.median(gains)), held_out_r2_by_group={f["held"]: f["calibrated"] for f in folds},
                           photons_per_fit_px=qdist([r["photons"] for r in rows]), photons_per_mm2=qdist([r["photons"] / pitch ** 2 for r in rows]),
                           scatter_fraction_per_frame=qdist([r["s"] for r in rows]), blur_sigma_per_frame_px=qdist([r["sigma_r"] for r in rows]), alpha_per_frame=qdist([r["alpha"] for r in rows]),
                           per_frame_r2=qdist([r["r2_frame"] for r in rows]), global_theta_r2_per_frame=qdist([r["r2_global"] for r in rows]),
                           physics_defaults=defs, term_tests=variants, reproduction_of_shipped_calibration=repro),
        display_stage=dict(transfer=dict(form=("log display read linearly" if dev["reading"] == "log_display" else "linear detector signal, -log"), test=tr_forms),
                           unsharp=dict(radius_px=summ["sigma_u"]["median"], radius_mm=summ["sigma_u"]["median"] * pitch, gain=summ["alpha"]["median"], domain="transmission (the nine-term model)",
                                        gain_per_frame=qdist([r["alpha"] for r in rows])),
                           dynamic_range=dict(gamma=tr_forms["power_gamma_median"], compression=None),
                           window=dict(stored_percentiles={f"p{p}": qdist([r[f"stored_p{p}"] for r in rows]) for p in (1, 5, 50, 95, 99)},
                                       win_A=qdist([r["win_A"] for r in rows]), win_B=qdist([r["win_B"] for r in rows]), I0=qdist([r["I0"] for r in rows]), C_trans=qdist([r["C_trans"] for r in rows]),
                                       dicom_window_center=qdist([r["meta"].get("window_center") for r in rows]), dicom_window_width=qdist([r["meta"].get("window_width") for r in rows]),
                                       or_targets="27/47/126/216/239 at percentiles 1/5/50/95/99 (FluoroCap medians) for the 8-bit display"),
                           from_images=dimg),
        border=dict(shape=(max(set(s["shape"] for s in shapes), key=[s["shape"] for s in shapes].count) if shapes else None),
                    field_frac=qdist([s["field_frac"] for s in shapes]), left=qdist([s["left"] for s in shapes]), right=qdist([s["right"] for s in shapes]),
                    top=qdist([s["top"] for s in shapes]), bottom=qdist([s["bottom"] for s in shapes]), radius=qdist([s.get("radius") for s in shapes]),
                    centre_u=qdist([s.get("centre_u") for s in shapes]), centre_v=qdist([s.get("centre_v") for s in shapes]),
                    penumbra_sigma_px=qdist([b["sigma_p_px"] for b in borders]), penumbra_sigma_mm=qdist([b["sigma_p_px"] * pitch for b in borders]),
                    halo=qdist([b["halo"] for b in borders]), profile_median=(np.median(np.array([b["profile"] for b in borders]), 0).round(4).tolist() if borders else None),
                    profile_t=(borders[0]["t"] if borders else None), penumbra_default=defs.get("sigma_p"),
                    penumbra_fitted_term=(variants.get("+penumbra", {}).get("terms", {}).get("sigma_p") if variants else None),
                    collimator_style=("iris (circle)" if shapes and np.mean([s["shape"] == "circle" for s in shapes]) > 0.5 else "blades (rect)"),
                    measured_on="the real frames' borders (device_physics.border_profile), all frames; the penumbra term in the forward model is fitted in term_tests['+penumbra']"),
        distribution=dict(copula=cop_all, aec=aec, coverage=cov, columns=COP_COLS,
                          note="Gaussian copula over the per-frame vector (marginals as 41 quantiles, correlation of normal scores); sample with device_style.sample_terms; the conditional on thickness_cm is exact in normal-score space"),
        fit=dict(n_frames_fit=int(np.median([f["n_fit"] for f in folds])), n_frames_total=len(frames), n_frames_val=sum(f["n"] for f in folds), n_groups=len(groups), folds=len(folds),
                 R2_held_out=float(np.median([f["calibrated"] for f in folds])), R2_held_out_by_fold={f["held"]: f["calibrated"] for f in folds},
                 R2_baseline_held_out=float(np.median([f["baseline"] for f in folds])), R2_full_field_held_out=float(np.median([f["calibrated_full"] for f in folds])),
                 residual_by_region=pooled, date=time.strftime("%Y-%m-%d %H:%M"), code_sha=code_sha(), pairs_dir=dev["pairs"], seconds=int(time.time() - t0),
                 fit_frames=a.fit_frames, maxiter=a.maxiter, seed=a.seed),
        unknowns=[],
    )
    js = EG.stamp(js, gate)
    json.dump(js, open(DOCS / f"{a.device}.json", "w"), indent=1, default=lambda o: None if isinstance(o, float) and not np.isfinite(o) else (o.tolist() if hasattr(o, "tolist") else str(o)))
    json.dump(dict(rows=rows, regions=reg_rows), open(out_dir / "per_frame.json", "w"), default=lambda o: None if isinstance(o, float) and not np.isfinite(o) else (o.tolist() if hasattr(o, "tolist") else str(o)))
    print(f"\nwrote {DOCS / (a.device + '.json')}, {DOCS / (a.device + '.frames.csv')}, figures in {out_dir}  ({int(time.time() - t0)} s)", flush=True)
    return 0


# ---------------------------------------------------------------------------------------------------- pairs builders
def block_mean(x, k):
    if k == 1:
        return x.astype(np.float64)
    h, w = x.shape; h2, w2 = h // k, w // k
    return x[: h2 * k, : w2 * k].reshape(h2, k, w2, k).mean((1, 3))


def save_pair(out, case, pid, trans, water, bone, hit, trunc, real, rot, down, px_mm, meta, sat=None, excl=None):
    extra = {}
    if sat is not None:
        extra["sat"] = sat
    if excl is not None:
        extra["excl"] = excl
    np.savez_compressed(out / f"pair_{case}_{pid}.npz", drr_trans=trans.astype(np.float32), water_cm=water.astype(np.float32), bone_cm=bone.astype(np.float32),
                        real=real.astype(np.float32), hit=hit, trunc=trunc, rot=np.int64(rot), down=np.float64(down), px_mm=np.float64(px_mm), **extra)
    json.dump(meta, open(out / f"pair_{case}_{pid}.json", "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))


def _render_worker(args):
    """One frame: raycast d (volume inherited from the fork) and save the pair."""
    import deepfluoro_render as DR
    out, case, pid, K, ext, nr, nc, down, real, rot, px_mm, meta, sat, excl = args
    d = dict(K=K, ext=ext, T=np.eye(4), nr=nr, nc=nc, vol=_G["vol"], org=_G["org"], sp=_G["sp"])
    trans, water, bone, hit, trunc = DR.raycast(d, down=down)
    h = min(real.shape[0], trans.shape[0]); w = min(real.shape[1], trans.shape[1])
    real, trans, water, bone, hit, trunc = (x[:h, :w] for x in (real, trans, water, bone, hit, trunc))
    if sat is not None:
        sat = sat[:h, :w]
    if excl is not None:
        excl = excl[:h, :w]
    m = hit & ~trunc & (real > 0)
    c = float(np.corrcoef(np.log(np.clip(real[m], 1e-3, None)), np.log(np.clip(trans[m], 1e-6, 1)))[0, 1]) if m.sum() > 100 else float("nan")
    meta = dict(meta, ncc_log=c, hit_frac=float(hit.mean()), trunc_frac=float(trunc[hit].mean()) if hit.any() else 1.0)
    save_pair(Path(out), case, pid, trans, water, bone, hit, trunc, real, rot, down, px_mm, meta, sat, excl)
    return case, pid, c


def pairs_cobra(a):
    """Elekta XVI cases: frames within --max-deg of AP, every --every-th, at native 0.8 mm (down 1)."""
    import cobra_pairs as CP
    from realxray_cobra_export import view_of
    from multiprocessing import get_context
    import yaml
    dev = DEVICES[a.device]; maker = dev.get("cobra_manufacturer", "Elekta")
    out = Path(ROOT) / a.device / "pairs"; out.mkdir(parents=True, exist_ok=True)
    Pi = np.array([[0, 1, 0], [0, 0, -1], [1, 0, 0]], float)
    cases = a.cases.split(",") if a.cases else dev.get("cobra_cases", ["A002", "A004", "A005", "B000", "B002", "B005", "C000", "C005", "C012", "D002", "D009", "D018"])
    for case in cases:
        cdir = Path("/rs/rs_grp_oschome/go2432/data/cobra2026/cases") / case
        if list(out.glob(f"pair_{case}_*.npz")):
            print(case, "exists; skipped", flush=True); continue
        meta = yaml.safe_load(open(cdir / "metadata.yaml"))
        cb = meta.get("cbct", {})
        if cb.get("Manufacturer") != maker:
            print(case, f"not {maker}; skipped", flush=True); continue
        mats, angles, sid, sdd = CP.read_geometry(cdir / "geometry.xml")
        _, ph = CP.read_mha(cdir / "projections.mha", frames=[0]); (ox, oy, _), (sx, sy, _) = ph["_offset"], ph["_spacing"]
        nc, nr = ph["_dims"][0], ph["_dims"][1]
        vol, ch = CP.read_mha(cdir / "ct_def.mha")
        _G["vol"] = vol.astype(np.float32); _G["org"] = np.array(ch["_offset"], np.float64); _G["sp"] = np.array(ch["_spacing"], np.float64)
        fov, fh = CP.read_mha(cdir / "fov_cbct.mha", frames=[0])
        fdims = np.array(fh["_dims"], float); fsp = np.array(fh["_spacing"]); fdir = np.array(fh["_direction"]).reshape(3, 3)
        iso = np.array(fh["_offset"]) + fdir @ ((fdims - 1) / 2.0 * fsp)
        W = CP.world_map(Pi, iso)
        picks = []
        for k in range(0, len(mats), a.every):
            v = view_of(mats[k] @ W, iso)
            if v["lat_from_ap_deg"] <= a.max_deg:
                picks.append((k, v))
        if not picks:
            print(case, "no frames within", a.max_deg, "deg of AP", flush=True); continue
        reals, _ = CP.read_mha(cdir / "projections.mha", frames=[k for k, _ in picks])
        jobs = []
        for j, (k, v) in enumerate(picks):
            K, ext = CP.camera_from_matrix(mats[k] @ W, ox, oy, sx, sy)
            fm = dict(case=case, pid=f"{k:04d}", angle=float(angles[k]), lat_deg=v["lat_from_ap_deg"], cranial_caudal_deg=v["cranial_caudal_deg"], source_side=v["source_side"],
                      kvp=float(cb.get("TubeVoltage")), ma=float(cb.get("TubeCurrent")), ms=float(cb.get("PulseLength")), mas=float(cb.get("TubeCurrent")) * float(cb.get("PulseLength")) / 1000.0,
                      collimator=cb.get("Collimator"), fan=cb.get("Fan"), kv_filter=cb.get("KVFilter"), grid=cb.get("ScatterGrid"), detector_offset_x=cb.get("DetectorOffsetX"),
                      centre=case[0], view="AP" if v["lat_from_ap_deg"] <= 20 else "OBL", sid=sdd, sad=sid, px_native=sx)
            jobs.append((str(out), case, f"{k:04d}", K, ext, nr, nc, a.down, block_mean(reals[j].astype(np.float64), a.down), 0, sx * a.down, fm, None, None))
        with get_context("fork").Pool(a.workers) as pool:
            res = pool.map(_render_worker, jobs)
        print(f"{case}: {len(res)} pairs, NCC(log real, log DRR) median {np.nanmedian([r[2] for r in res]):+.3f}, mA {cb.get('TubeCurrent')} ms {cb.get('PulseLength')}", flush=True)
    return 0


def cobra_thickness(a):
    """AP and lateral water-equivalent thickness through the isocentre of EVERY downloaded Elekta case, with its preset (kV, mA, ms)."""
    import cobra_pairs as CP
    import yaml
    rows = []
    for cdir in sorted(Path("/rs/rs_grp_oschome/go2432/data/cobra2026/cases").glob("*")):
        mp = cdir / "metadata.yaml"
        if not mp.exists() or not (cdir / "ct_def.mha").exists():
            continue
        cb = yaml.safe_load(open(mp)).get("cbct", {})
        if cb.get("Manufacturer") != "Elekta":
            continue
        try:
            vol, ch = CP.read_mha(cdir / "ct_def.mha")
            fov, fh = CP.read_mha(cdir / "fov_cbct.mha", frames=[0])
            fdims = np.array(fh["_dims"], float); fsp = np.array(fh["_spacing"]); fdir = np.array(fh["_direction"]).reshape(3, 3)
            iso = np.array(fh["_offset"]) + fdir @ ((fdims - 1) / 2.0 * fsp)
            org = np.array(ch["_offset"]); sp = np.array(ch["_spacing"])
            idx = np.round((iso - org) / sp).astype(int)                  # (x, y, z) index of the isocentre
            w = np.clip((vol.astype(np.float32) + 1000.0) / 1000.0, 0, 1)
            r = 10
            zs = slice(max(idx[2] - r, 0), idx[2] + r); xs = slice(max(idx[0] - r, 0), idx[0] + r); ys = slice(max(idx[1] - r, 0), idx[1] + r)
            ap = float(w[zs, :, xs].sum(1).mean() * sp[1] / 10.0)          # along y (anterior-posterior), cm
            lat = float(w[zs, ys, :].sum(2).mean() * sp[0] / 10.0)          # along x
            rows.append(dict(case=cdir.name, centre=cdir.name[0], kvp=float(cb.get("TubeVoltage")), ma=float(cb.get("TubeCurrent")), ms=float(cb.get("PulseLength")),
                             mas=float(cb.get("TubeCurrent")) * float(cb.get("PulseLength")) / 1000.0, frames=cb.get("Frames"), collimator=cb.get("Collimator"), fan=cb.get("Fan"),
                             thickness_ap_cm=ap, thickness_lat_cm=lat))
            print(rows[-1], flush=True)
        except Exception as e:  # noqa: BLE001
            print(cdir.name, "failed", e, flush=True)
    out = Path(ROOT) / "elekta_xvi"; out.mkdir(parents=True, exist_ok=True)
    with open(out / "cases_thickness.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    reg = dict(log10_mas_on_thickness_ap=regress([r["thickness_ap_cm"] for r in rows], [np.log10(r["mas"]) for r in rows]),
               ma_on_thickness_ap=regress([r["thickness_ap_cm"] for r in rows], [r["ma"] for r in rows]),
               by_preset={str(k): dict(n=sum(1 for r in rows if (r["ma"], r["ms"]) == k), thickness_ap_median=float(np.median([r["thickness_ap_cm"] for r in rows if (r["ma"], r["ms"]) == k])))
                          for k in sorted({(r["ma"], r["ms"]) for r in rows})},
               by_centre={c: dict(n=sum(1 for r in rows if r["centre"] == c), presets=sorted({(r["ma"], r["ms"]) for r in rows if r["centre"] == c}, key=str)) for c in sorted({r["centre"] for r in rows})},
               n=len(rows))
    json.dump(reg, open(out / "cases_thickness_regression.json", "w"), indent=1, default=str)
    print(json.dumps(reg, indent=1, default=str))
    return 0


def read_frame_header(ds):
    def g(*names):
        for n in names:
            v = getattr(ds, n, None)
            if v is not None and v != "":
                try:
                    return float(v[0]) if isinstance(v, (list, tuple)) or hasattr(v, "__getitem__") and not isinstance(v, (str, bytes)) and len(v) else float(v)
                except Exception:  # noqa: BLE001
                    return None
        return None
    ma = g("XRayTubeCurrent", "XRayTubeCurrentInmA")
    pw = g("AveragePulseWidth")
    et = g("ExposureTimeInms"); et_ = g("ExposureTime")
    ms = pw if pw else (et if et and et < 1000 else et_)
    return dict(kvp=g("KVP"), ma=ma, ms=ms, pulse_ms=pw, exposure_time_ms=et, exposure_time=et_, exposure_mas=g("Exposure", "ExposureInmAs"),
                mas=((ma * ms / 1000.0) if (ma and ms) else None), window_center=g("WindowCenter"), window_width=g("WindowWidth"),
                angle=g("PositionerPrimaryAngle"), secondary_angle=g("PositionerSecondaryAngle"), sid=g("DistanceSourceToDetector"), sod=g("DistanceSourceToPatient"),
                shutter=[getattr(ds, n, None) for n in ("ShutterLeftVerticalEdge", "ShutterRightVerticalEdge", "ShutterUpperHorizontalEdge", "ShutterLowerHorizontalEdge")],
                photometric=str(getattr(ds, "PhotometricInterpretation", "")), pir=str(getattr(ds, "PixelIntensityRelationship", "")), bits=getattr(ds, "BitsStored", None),
                acquisition_time=str(getattr(ds, "AcquisitionTime", "")), station=str(getattr(ds, "StationName", "")))


def pairs_surgio_dr(a):
    """C-ArmLSpine DR frames (2048^2) at down 4 through their registered poses (_ref2 for laterals when present)."""
    import pydicom
    import SimpleITK as sitk
    import carmlspine_io as CIO
    from multiprocessing import get_context
    out = Path(ROOT) / "surgio_b51_dr" / "pairs"; out.mkdir(parents=True, exist_ok=True)
    root = "/rs/rs_grp_oschome/go2432/data/carmlspine/unpacked/C-ArmLSpine"; pose_dir = "/rs/rs_grp_oschome/go2432/data/carmlspine/pose"
    cases = a.cases.split(",") if a.cases else sorted([os.path.basename(p) for p in glob.glob(f"{root}/case*")], key=lambda c: int(c[4:]))
    n_done = 0
    for case in cases:
        nii = f"/rs/rs_grp_oschome/go2432/data/carmlspine/nifti/{case}_cbct.nii.gz"
        if not os.path.exists(nii):
            continue
        try:
            fr = CIO.read_frames(os.path.join(root, case, "C-arm"))
        except Exception as e:  # noqa: BLE001
            print(case, "no frames", e); continue
        jobs = []
        for p, ds in fr:
            view = CIO.view_of_angle(float(getattr(ds, "PositionerPrimaryAngle", 0) or 0))
            if view not in ("AP", "LAT"):
                continue
            pid = view
            if (out / f"pair_{case}_{pid}.npz").exists():
                continue
            pj = f"{pose_dir}/{case}_{view}_ref2.json"
            if not os.path.exists(pj):
                pj = f"{pose_dir}/{case}_{view}_ref.json"
            if not os.path.exists(pj):
                continue
            P = json.load(open(pj))
            if os.path.basename(p) != P.get("frame", os.path.basename(p)):
                continue                                   # the pose belongs to another frame of this view (case39 has three)
            dsf = pydicom.dcmread(p); img = dsf.pixel_array.astype(np.float64)
            hdr = read_frame_header(dsf)
            hdr.update(case=case, view=view, pid=pid, pose_file=os.path.basename(pj), edge_ncc=P.get("edge_ncc"), lat_deg=(0.0 if view == "AP" else 90.0), frame=os.path.basename(p))
            K = np.array(P["K"], float); ext = np.eye(4); ext[:3, :3] = np.array(P["R"]); ext[:3, 3] = np.array(P["t"])
            jobs.append((str(out), case, pid, K, ext, img.shape[0], img.shape[1], a.down, block_mean(img, a.down), 0, CIO.DET_MM / img.shape[1] * a.down, hdr, None, None))
        if not jobs:
            continue
        im = sitk.ReadImage(nii)
        if not np.allclose(im.GetDirection(), np.eye(3).ravel()):
            print(case, "CBCT direction not identity; skipped"); continue
        _G["vol"] = sitk.GetArrayFromImage(im).astype(np.float32); _G["org"] = np.array(im.GetOrigin()); _G["sp"] = np.array(im.GetSpacing())
        with get_context("fork").Pool(min(a.workers, len(jobs))) as pool:
            res = pool.map(_render_worker, jobs)
        n_done += len(res)
        print(case, [(r[1], round(r[2], 3)) for r in res], flush=True)
    print(f"wrote {n_done} pairs to {out}")
    return 0


def sweep_frames(case_dir):
    """The 1024-row XA files of a raw CBCT sweep, ordered by InstanceNumber, with the header, the main image and the private raw twin."""
    import pydicom
    out = []
    for sub in ("CBCT", "ori"):
        d = os.path.join(case_dir, sub)
        if not os.path.isdir(d):
            continue
        for p in sorted(glob.glob(os.path.join(d, "*"))):
            try:
                ds = pydicom.dcmread(p, stop_before_pixels=True)
            except Exception:  # noqa: BLE001
                continue
            if str(getattr(ds, "Modality", "")) == "XA" and int(getattr(ds, "Rows", 0) or 0) == 1024:
                out.append((int(getattr(ds, "InstanceNumber", 0) or 0), p))
    return [p for _, p in sorted(out)]


def read_sweep_frame(p):
    import pydicom
    ds = pydicom.dcmread(p)
    main = ds.pixel_array.astype(np.float64)
    raw = None
    if (0x0037, 0x0020) in ds:
        v = ds[(0x0037, 0x0020)].value
        if isinstance(v, bytes) and len(v) == 2 * 1024 * 1024:
            raw = np.frombuffer(v, "<u2").reshape(1024, 1024).astype(np.float64)
    return ds, main, raw


def sweep_start(theta_deg, sign, centre, sod):
    """The AP convention dir(0,-1,0)_rot180_m-1 turned about the patient's S-I axis by sign*theta."""
    from scipy.spatial.transform import Rotation
    th = np.radians(theta_deg) * sign
    d = np.array([np.sin(th), -np.cos(th), 0.0]); d /= np.linalg.norm(d)
    up = np.array([0, 0, 1.0]); x = np.cross(up, d); x /= np.linalg.norm(x); y = np.cross(d, x)
    Rcam = Rotation.from_euler("z", 180, degrees=True).as_matrix() @ np.stack([x, y, d])
    src = centre - d * sod
    return dict(R=Rcam, t=-Rcam @ src, mirror=-1, rot=180, dir=d.tolist())


def pairs_surgio_sweep(a):
    """The raw sweeps: pose per frame from the header angle refined by bounded edge registration (CPU), pairs of the near-raw
    private frame (real) with the CBCT render, the processed main frame kept beside it (real_main)."""
    import SimpleITK as sitk
    import carmlspine_io as CIO
    import carmlspine_pose as CPo
    import drr_register as DRG
    import deepfluoro_render as DR
    out = Path(ROOT) / "surgio_b51_raw" / "pairs"; out.mkdir(parents=True, exist_ok=True)
    root = "/rs/rs_grp_oschome/go2432/data/carmlspine/unpacked/C-ArmLSpine"
    cases = a.cases.split(",") if a.cases else ["case134", "case39"]
    px_native = CIO.DET_MM / 1024.0
    summary = {}
    for case in cases:
        files = sweep_frames(os.path.join(root, case))
        if not files:
            print(case, "no sweep frames"); continue
        nii = f"/rs/rs_grp_oschome/go2432/data/carmlspine/nifti/{case}_cbct.nii.gz"
        im = sitk.ReadImage(nii); hu = sitk.GetArrayFromImage(im).astype(np.float32)
        mu = np.clip((hu + 1000.0) / 1000.0, 0.0, None) * 0.02
        D = np.array(im.GetDirection()).reshape(3, 3); sp = np.array(im.GetSpacing()); org = np.array(im.GetOrigin())
        A = np.eye(4); A[:3, :3] = D @ np.diag(sp); A[:3, 3] = org
        rend = DRG.Renderer(mu, A, "cpu"); centre = rend.centre
        picks = files[:: a.every]
        sign = None; recs = []
        for j, p in enumerate(picks):
            ds, main, raw = read_sweep_frame(p)
            if raw is None:
                print(case, os.path.basename(p), "no private raw twin; skipped"); continue
            hdr = read_frame_header(ds); ang = hdr["angle"] or 0.0
            att = CPo.stored_to_atten(main)
            sid, sod = hdr["sid"] or 1140.0, hdr["sod"] or 745.0
            if sign is None:
                # decide the sign of the primary angle on the first frame far from AP, by the edge score of both starts
                cand = {}
                for sg in (1, -1):
                    res = DRG.register(mu, A, att, px_native, sid, sod, starts=[sweep_start(ang, sg, centre, sod)], device="cpu", work=a.work, topk=1,
                                       tc_bound=(15.0, 15.0, 40.0), rot_bound_deg=8.0, log=lambda s_: None)
                    cand[sg] = res
                sign = max(cand, key=lambda k: cand[k]["edge_ncc"])
                print(f"{case}: angle sign {sign:+d} chosen at {ang:.1f} deg (edge {cand[1]['edge_ncc']:+.3f} vs {cand[-1]['edge_ncc']:+.3f})", flush=True)
                res = cand[sign]
            else:
                res = DRG.register(mu, A, att, px_native, sid, sod, starts=[sweep_start(ang, sign, centre, sod)], device="cpu", work=a.work, topk=1,
                                   tc_bound=(15.0, 15.0, 40.0), rot_bound_deg=8.0, log=lambda s_: None)
            K = np.array(res["K"]); ext = np.eye(4); ext[:3, :3] = np.array(res["R"]); ext[:3, 3] = np.array(res["t"])
            # the private raw frame: turned 180 relative to the main frame? decide by correlation of ln(raw) with the main image
            r180 = raw[::-1, ::-1]
            c0 = np.corrcoef(np.log(np.clip(raw, 1, None)).ravel()[::13], main.ravel()[::13])[0, 1]
            c1 = np.corrcoef(np.log(np.clip(r180, 1, None)).ravel()[::13], main.ravel()[::13])[0, 1]
            raw_al = r180 if c1 > c0 else raw
            d = dict(K=K, ext=ext, T=np.eye(4), nr=1024, nc=1024, vol=hu, org=org, sp=sp)
            trans, water, bone, hit, trunc = DR.raycast(d, down=a.down)
            real = block_mean(raw_al, a.down); main_d = block_mean(main, a.down)
            pid = f"{int(getattr(ds, 'InstanceNumber', j) or j):04d}"
            hdr.update(case=case, view="SWEEP", pid=pid, lat_deg=float(abs(ang)), edge_ncc=res["edge_ncc"], raw_turned_180=bool(c1 > c0), corr_raw_main=float(max(c0, c1)),
                       angle_sign=sign, frame=os.path.basename(p), pose_from_header_shift_mm=None)
            np.savez_compressed(out / f"pair_{case}_{pid}.npz", drr_trans=trans.astype(np.float32), water_cm=water.astype(np.float32), bone_cm=bone.astype(np.float32),
                                real=real.astype(np.float32), real_main=main_d.astype(np.float32), hit=hit, trunc=trunc, rot=np.int64(0), down=np.float64(a.down), px_mm=np.float64(px_native * a.down))
            json.dump(hdr, open(out / f"pair_{case}_{pid}.json", "w"), indent=1, default=str)
            m = hit & ~trunc
            c = float(np.corrcoef(-np.log(np.clip(real[m], 1, None)), -np.log(np.clip(trans[m], 1e-6, 1)))[0, 1]) if m.sum() > 100 else float("nan")
            recs.append(dict(pid=pid, angle=ang, edge=res["edge_ncc"], ncc_atten=c, raw180=bool(c1 > c0)))
            print(f"  {case}/{pid} angle {ang:7.1f} edge {res['edge_ncc']:+.3f} NCC(-log raw, -log DRR) {c:+.3f} raw turned {bool(c1 > c0)}", flush=True)
        summary[case] = dict(sign=sign, n=len(recs), edge_median=float(np.median([r["edge"] for r in recs])) if recs else None,
                             ncc_median=float(np.median([r["ncc_atten"] for r in recs])) if recs else None, frames=recs)
    json.dump(summary, open(out.parent / "sweep_pose_summary.json", "w"), indent=1)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "frames"} for k, v in summary.items()}, indent=1))
    return 0


def pairs_geneva(a):
    """The Geneva frames as pairs from the exporter's work directory (drr/<view>.npz at 372 px, tif resized, glare offset per frame)."""
    import realxray_geneva_export as GV
    from PIL import Image
    out = Path(ROOT) / "bv_pulsera" / "pairs"; out.mkdir(parents=True, exist_ok=True)
    V = json.load(open(GV.WORK / "verify.json"))
    FR = GV.frames()
    n = 0
    for x in FR:
        z = np.load(GV.WORK / "drr" / f"{x['view']}.npz")
        real = np.asarray(Image.open(x["tif"])).astype(np.float64)
        rd = GV.resize(real); fov = GV.fov_mask(real)
        sat = GV.resize((real >= GV.SAT).astype(np.float64)) > 0.01
        lm = np.asarray(Image.open(x["mask"])); lm = (lm.max(-1) if lm.ndim == 3 else lm) > 0
        lmk = GV.resize(lm.astype(np.float64)) > 0.01
        vr = V["frames"][x["stem"]]
        meta = dict(case=x["view"], view=x["view"], pid=f"{x['kv']:03d}kv", kvp=float(x["kv"]), ma=None, ms=None, mas=None, offset_c=float(vr["offset_c"]),
                    local_slope_r2=vr["local_slope"]["r2"], bead_err_px=vr["bead_err_px_median"], lat_deg=None, field="circle")
        hit = z["hit"] & fov
        save_pair(out, x["view"], meta["pid"], z["trans"], z["water"], z["bone"], hit, z["trunc"], rd, 0, GV.NFULL / GV.WPX, GV.NFULL * 0.2904 / GV.WPX, meta, sat=sat, excl=lmk)
        n += 1
    print(f"wrote {n} Geneva pairs to {out}")
    return 0


# ------------------------------------------------------------------------------------------- C-ArmLSpine display stage
def display_model(L, params, mean_ref=None):
    """The processed frame from the log of the raw one: a (L + g (L - G_su L) - k (G_sd L - mean)) + b."""
    a_, b_, g, su, k, sd = params
    hp = L - gauss(L, su) if su > 0.05 else np.zeros_like(L)
    lp = gauss(L, sd) if sd > 0.05 else L
    mref = float(L.mean()) if mean_ref is None else mean_ref
    return a_ * (L + g * hp - k * (lp - mref)) + b_


def fit_display_twins(twins, su_grid=(1, 2, 3, 4, 6, 8, 12), sd_grid=(0, 24, 48, 96), off_grid=(0.0, 50.0, 150.0), sub=3):
    """Least squares over (a, b, g', k') for every (su, sd, off) on a subsample of pixels of every twin; the best triple by pooled R2."""
    best = None
    for off in off_grid:
        for su in su_grid:
            for sd in sd_grid:
                num = den = 0.0; coefs = []
                for raw, main in twins:
                    L = np.log(np.clip(raw - off, 1.0, None))
                    hp = L - gauss(L, su); lp = gauss(L, sd) - L.mean() if sd > 0 else np.zeros_like(L)
                    X = np.c_[L[::sub, ::sub].ravel(), hp[::sub, ::sub].ravel(), lp[::sub, ::sub].ravel(), np.ones(L[::sub, ::sub].size)]
                    y = main[::sub, ::sub].ravel()
                    co = np.linalg.lstsq(X, y, rcond=None)[0]
                    r = y - X @ co; num += float((r * r).sum()); den += float(((y - y.mean()) ** 2).sum()); coefs.append(co)
                r2 = 1 - num / max(den, 1e-12)
                if best is None or r2 > best["r2"]:
                    C = np.array(coefs)
                    best = dict(r2=r2, su=su, sd=sd, off=off, a=float(np.median(C[:, 0])), g=float(np.median(C[:, 1] / C[:, 0])), k=float(np.median(-C[:, 2] / C[:, 0])), b=float(np.median(C[:, 3])),
                                a_p10_p90=[float(np.percentile(C[:, 0], 10)), float(np.percentile(C[:, 0], 90))], g_p10_p90=[float(np.percentile(C[:, 1] / C[:, 0], 10)), float(np.percentile(C[:, 1] / C[:, 0], 90))],
                                k_p10_p90=[float(np.percentile(-C[:, 2] / C[:, 0], 10)), float(np.percentile(-C[:, 2] / C[:, 0], 90))])
    return best


def r2_display(twins, P, sub=3):
    num = den = 0.0
    for raw, main in twins:
        L = np.log(np.clip(raw - P["off"], 1.0, None))
        hp = L - gauss(L, P["su"]); lp = gauss(L, P["sd"]) - L.mean() if P["sd"] > 0 else np.zeros_like(L)
        X = np.c_[L[::sub, ::sub].ravel(), hp[::sub, ::sub].ravel(), lp[::sub, ::sub].ravel(), np.ones(L[::sub, ::sub].size)]
        y = main[::sub, ::sub].ravel()
        co = np.linalg.lstsq(X[:, [0, 3]], y, rcond=None)[0]          # only the per-frame window (a, b) refitted; g, k, su, sd carried
        pred = co[0] * (L + P["g"] * hp - P["k"] * lp)[::sub, ::sub].ravel() + co[1]
        r = y - pred; num += float((r * r).sum()); den += float(((y - y.mean()) ** 2).sum())
    return 1 - num / max(den, 1e-12)


def cmd_display(a):
    """C-ArmLSpine: (1) the transfer curve main-vs-raw per twin; (2) the display map fitted on case134's twins, validated on case39's;
    (3) the whole chain on the DR frames: physics terms (surgio_b51_raw fit) -> modelled raw -> display map -> against the stored DR."""
    import render_physics_drr as RP_
    from deepfluoro_transfer import fit_forms
    RP = (RP_.ENERGIES.numpy(), RP_.SPECTRUM.numpy(), RP_.MU_WATER.numpy(), RP_.MU_BONE.numpy())
    out = Path(ROOT) / "surgio_b51_display"; out.mkdir(parents=True, exist_ok=True)
    root = "/rs/rs_grp_oschome/go2432/data/carmlspine/unpacked/C-ArmLSpine"
    twins = {}
    curves = []
    for case in ("case134", "case39"):
        files = sweep_frames(os.path.join(root, case))[:: a.every]
        tw = []
        for p in files:
            ds, main, raw = read_sweep_frame(p)
            if raw is None:
                continue
            r180 = raw[::-1, ::-1]
            c0 = np.corrcoef(np.log(np.clip(raw, 1, None)).ravel()[::13], main.ravel()[::13])[0, 1]
            c1 = np.corrcoef(np.log(np.clip(r180, 1, None)).ravel()[::13], main.ravel()[::13])[0, 1]
            raw_al = r180 if c1 > c0 else raw
            k = a.down
            tw.append((block_mean(raw_al, k), block_mean(main, k)))
            # the transfer curve of this twin: main binned by raw, three forms on (ln raw -> main)
            L = np.log(np.clip(raw_al, 1, None)); q = np.quantile(L, np.linspace(0, 1, 41)); xs = []; ys = []; ws = []
            for i in range(40):
                sel = (L >= q[i]) & (L < q[i + 1]) if i < 39 else (L >= q[i])
                if sel.sum() > 50:
                    xs.append(float(np.median(L[sel]))); ys.append(float(np.median(main[sel]))); ws.append(float(sel.sum()))
            forms, _ = fit_forms(np.array(xs), np.array(ys), np.array(ws))
            curves.append(dict(case=case, frame=os.path.basename(p), raw_turned=bool(c1 > c0), corr=float(max(c0, c1)), forms=forms, kvp=read_frame_header(ds)["kvp"], ma=read_frame_header(ds)["ma"]))
        twins[case] = tw
        print(f"{case}: {len(tw)} twins; main-vs-ln(raw) linear R2 median {np.median([c['forms']['linear']['r2'] for c in curves if c['case'] == case]):.3f}, "
              f"power gamma median {np.median([c['forms']['power']['gamma'] for c in curves if c['case'] == case]):.2f}", flush=True)
    P = fit_display_twins(twins["case134"])
    print("display map fitted on case134:", json.dumps(P), flush=True)
    val = r2_display(twins["case39"], P); val_plain = r2_display(twins["case39"], dict(P, g=0.0, k=0.0))
    P39 = fit_display_twins(twins["case39"])
    print(f"validation on case39: R2 {val:.4f} with the map, {val_plain:.4f} as a plain log; case39's own fit: {json.dumps(P39)}", flush=True)
    # the chain on the DR frames
    chain = None
    dr_json = DOCS / "surgio_b51_dr.json"; raw_json = DOCS / "surgio_b51_raw.json"
    if raw_json.exists() and (Path(ROOT) / "surgio_b51_dr" / "pairs").exists():
        dev_dr = DEVICES["surgio_b51_dr"]; dev_raw = DEVICES["surgio_b51_raw"]
        frames = load_frames(dev_dr, a.limit)
        Rj = json.load(open(raw_json)); th_raw = {n: Rj["physics_terms"]["fitted"][n]["median"] for n in NAMES9}; th_raw.update(sigma_p=0.0, s_t=0.0, b4=0.0)
        pitch_dr = dev_dr["pixel_pitch_mm"] * dev_dr["down"]; pitch_raw = dev_raw["pixel_pitch_mm"] * dev_raw["down"]
        for n in PX_TERMS[:3]:
            th_raw[n] = th_raw[n] * pitch_raw / pitch_dr
        # kb at the DR kVp from the sweep's 111 kV by the spectrum model
        w = np.concatenate([d["water"][d["m"]][::9] for d in frames[:30]]); b = np.concatenate([d["bone"][d["m"]][::9] for d in frames[:30]])
        kb111 = PH.kb_default(111.0, w, b, RP)[0]
        rows = []
        for d in frames:
            kv = d["meta"].get("kvp") or 85.0
            th = dict(th_raw); th["kb"] = th_raw["kb"] * PH.kb_default(kv, w, b, RP)[0] / kb111
            T = np.exp(-forward(th, d, RP))
            L = np.log(np.clip(T * 10000.0, 1.0, None))
            pred = display_model(L, (1.0, 0.0, P["g"], P["su"] * pitch_raw / pitch_dr, P["k"], P["sd"] * pitch_raw / pitch_dr))
            plain = L
            m = d["m"]
            def r2_of(x):
                k_, c_ = np.polyfit(x[m], d["raw"][m], 1); r = d["raw"][m] - (k_ * x[m] + c_)
                return 1 - float(r.var() / d["raw"][m].var())
            th_dr = None
            if dr_json.exists():
                Dj = json.load(open(dr_json)); th_dr = {n: Dj["physics_terms"]["fitted"][n]["median"] for n in NAMES9}; th_dr.update(sigma_p=0.0, s_t=0.0, b4=0.0)
            rows.append(dict(case=d["spec"], pid=d["pid"], kvp=kv, r2_chain=r2_of(pred), r2_plain_log=r2_of(plain), r2_dr_terms=(r2_of(forward(th_dr, d, RP)) if th_dr else None),
                             r2_physics_only=r2_of(forward(baseline_theta(th_raw), d, RP))))
        chain = dict(n=len(rows), r2_chain_median=float(np.median([r["r2_chain"] for r in rows])), r2_plain_log_median=float(np.median([r["r2_plain_log"] for r in rows])),
                     r2_dr_terms_median=(float(np.median([r["r2_dr_terms"] for r in rows if r["r2_dr_terms"] is not None])) if any(r["r2_dr_terms"] is not None for r in rows) else None),
                     r2_physics_only_median=float(np.median([r["r2_physics_only"] for r in rows])), kb_sweep=th_raw["kb"], kb_scaled_median=float(np.median([th_raw["kb"] * PH.kb_default(r["kvp"], w, b, RP)[0] / kb111 for r in rows[:20]])),
                     rows=rows, note="R2 of the stored DR frame against each model after a per-frame line, on the fit mask; chain = sweep physics terms (kb rescaled to the frame's kVp) -> ln(raw) -> display map (g, su, k, sd from the twins)")
        print("DR chain:", json.dumps({k: v for k, v in chain.items() if k != "rows"}), flush=True)
    res = dict(transfer_curves=dict(n=len(curves), linear_r2_median=float(np.median([c["forms"]["linear"]["r2"] for c in curves])),
                                    power_gamma_median=float(np.median([c["forms"]["power"]["gamma"] for c in curves])),
                                    transmission_r2_median=float(np.median([c["forms"]["transmission"]["r2"] or 0 for c in curves])),
                                    raw_turned_share=float(np.mean([c["raw_turned"] for c in curves])), corr_median=float(np.median([c["corr"] for c in curves])), rows=curves),
               display_map=dict(fitted_on="case134", params=P, validation_case39=dict(r2_with_map=val, r2_plain_log=val_plain, own_fit=P39),
                                model="main = a (L + g (L - G_su L) - k (G_sd L - mean L)) + b, L = ln(raw - off); su, sd in px at %.3f mm" % (0.30 * a.down),
                                pitch_mm=0.30 * a.down),
               dr_chain=chain, date=time.strftime("%Y-%m-%d %H:%M"))
    json.dump(res, open(out / "display_stage.json", "w"), indent=1, default=lambda o: None if isinstance(o, float) and not np.isfinite(o) else str(o))
    # figure: one twin (raw | main | predicted | residual) and the transfer curve
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    raw, main = twins["case39"][len(twins["case39"]) // 2]
    L = np.log(np.clip(raw - P["off"], 1.0, None)); hp = L - gauss(L, P["su"]); lp = gauss(L, P["sd"]) - L.mean() if P["sd"] > 0 else 0 * L
    X = np.c_[(L + P["g"] * hp - P["k"] * lp).ravel(), np.ones(L.size)]; co = np.linalg.lstsq(X, main.ravel(), rcond=None)[0]
    pred = (X @ co).reshape(L.shape)
    fig, ax = plt.subplots(1, 4, figsize=(16, 4.2))
    for q, im, t in zip(ax, (np.log(np.clip(raw, 1, None)), main, pred, main - pred), ("ln(raw private frame)", "stored main frame", "predicted from raw", "residual")):
        lo, hi = np.percentile(im, (1, 99)); q.imshow(im, cmap="gray" if t != "residual" else "RdBu_r", vmin=lo if t != "residual" else -np.abs(hi), vmax=hi if t != "residual" else np.abs(hi)); q.set_title(t, fontsize=9); q.set_xticks([]); q.set_yticks([])
    fig.suptitle(f"C-ArmLSpine raw sweep twin (case39): display map from case134, g {P['g']:.2f} at su {P['su']} px, k {P['k']:.2f} at sd {P['sd']} px; R2 {val:.3f} (plain log {val_plain:.3f})", fontsize=9)
    fig.tight_layout(); fig.savefig(out / "fig_display_twin.png", dpi=110); plt.close(fig)
    print("wrote", out / "display_stage.json")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["pairs", "fit", "gate", "display", "cobra-thickness", "recoverage", "reperframe"])
    ap.add_argument("--perframe-free", default="s,sigma_r,alpha", help="per-frame free terms; 'photons' = only the quantum count per frame")
    ap.add_argument("--device", default=None, choices=list(DEVICES))
    ap.add_argument("--cases", default=None); ap.add_argument("--every", type=int, default=8); ap.add_argument("--down", type=int, default=None)
    ap.add_argument("--max-deg", type=float, default=45.0); ap.add_argument("--work", type=int, default=256)
    ap.add_argument("--workers", type=int, default=int(os.environ.get("SLURM_CPUS_PER_TASK", 8)))
    ap.add_argument("--fit-frames", type=int, default=40); ap.add_argument("--maxiter", type=int, default=60); ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--max-folds", type=int, default=6); ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--variants", action="store_true"); ap.add_argument("--var-frames", type=int, default=30); ap.add_argument("--var-maxiter", type=int, default=40)
    EG.add_args(ap)
    a = ap.parse_args()
    if a.cmd == "fit":
        return cmd_fit(a)
    if a.cmd == "gate":
        return cmd_gate(a)
    if a.cmd == "recoverage":
        return cmd_recoverage(a)
    if a.cmd == "reperframe":
        return cmd_reperframe(a)
    _G["pf_free"] = [] if a.perframe_free in ("photons", "none", "") else [x for x in a.perframe_free.split(",") if x]
    if a.cmd == "display":
        a.down = a.down or 2
        return cmd_display(a)
    if a.cmd == "cobra-thickness":
        return cobra_thickness(a)
    if a.device in ("elekta_xvi", "varian_halcyon"):
        a.down = a.down or 1; return pairs_cobra(a)
    if a.device == "surgio_b51_dr":
        a.down = a.down or 4; return pairs_surgio_dr(a)
    if a.device == "surgio_b51_raw":
        a.down = a.down or 2; return pairs_surgio_sweep(a)
    if a.device == "bv_pulsera":
        return pairs_geneva(a)
    raise SystemExit("pairs for cios_fusion exist at ~/model_night/deepfluoro/pairs")


if __name__ == "__main__":
    raise SystemExit(main())
