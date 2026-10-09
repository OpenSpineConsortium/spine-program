#!/usr/bin/env python
"""Style a rendered path map as one device's frame, from that device's fitted card alone (docs/devices/<device>.json).

The forward model is device_fit.forward, the one the card was fitted with; nothing is learned here. A styled frame is
one DRAW from the device's distribution: the global terms (kb, sigma_s, sigma_u, b, c, d) at their fitted medians,
the per-exposure terms (photons, s, sigma_r, alpha, win_A, win_B, field fraction, penumbra, halo) drawn from the
card's Gaussian copula -- conditioned on the render's own water-equivalent thickness so that exposure follows the
automatic exposure control the frames showed -- and the field (blades or iris) drawn from the card's border
quantiles. Pixel terms are stored in mm on the card and converted to the render's pitch here, so a render at any
pitch gets the same physical blur, penumbra and photon fluence.

    stage                                 term source on the card
    polyenergetic transmission            physics_terms.fitted.kb
    scatter pedestal                       s (copula), sigma_s (fitted, mm)
    collimator field + penumbra            border.{shape, left/right/top/bottom | centre, radius} (quantiles), sigma_p (mm)
    quantum draw                           photons_per_mm2 (copula, log10)
    receptor blur                          sigma_r (copula, mm)
    edge enhancement                       alpha (copula), sigma_u (fitted, mm)
    vignette / heel / tilt                 b, c, d (fitted); orientation from device.rot180_share
    display                                the device's monotone transfer, then the OR window on the exposed field
                                           (percentile targets 27/47/126/216/239, jittered by the card's stored spread);
                                           the collimated region is painted at the black level through the penumbra

    python tools/device_style.py demo --device cios_fusion --n 6 --draws 3      # real | draws, and the NPS / histogram / halo distances
    python tools/device_style.py stats --device elekta_xvi --n 40                # unpaired-path validation numbers only

Any device whose card has a copula can be sampled; a device without pairs can be given a card from the census and
physics defaults (tools/device_physics), which is the unpaired path this tool exists for.
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
import device_fit as DF  # noqa: E402
import device_physics as PH  # noqa: E402

DOCS = Path(__file__).resolve().parents[1] / "docs" / "devices"
OR_TARGETS = np.array([27.0, 47.0, 126.0, 216.0, 239.0]); OR_PCT = np.array([1.0, 5.0, 50.0, 95.0, 99.0])
GLOBAL = ["kb", "sigma_s", "sigma_u", "b", "c", "d"]


def load_device(name):
    p = DOCS / f"{name}.json"
    if not p.exists():
        raise SystemExit(f"no card {p}; run device_fit.py fit --device {name} (or write a census + physics-defaults card)")
    return json.load(open(p))


def _q(qd, key, default):
    return float(qd[key]) if qd and qd.get(key) is not None and np.isfinite(qd[key]) else default


def _draw_q(qd, rng, default):
    """One draw between a quantile dict's p10 and p90 (uniform), or the default when the card has none."""
    if not qd or qd.get("median") is None:
        return default
    lo, hi = _q(qd, "p10", qd["median"]), _q(qd, "p90", qd["median"])
    return float(rng.uniform(min(lo, hi), max(lo, hi))) if hi > lo else float(qd["median"])


def rp_tables():
    import render_physics_drr as RP_
    return (RP_.ENERGIES.numpy(), RP_.SPECTRUM.numpy(), RP_.MU_WATER.numpy(), RP_.MU_BONE.numpy())


AEC_MODE = "hold_detector"   # "hold_detector" | "off". See aec_gain() -- this is a knob, never a silent default.
AEC_MAX_GAIN = 30.0          # the most a real C-arm can raise output before it saturates, as a FACTOR on quanta
MU_WATER_EFF = 0.193         # 1/cm at ~70 keV, the same effective value the renderer and the cards use


def aec_gain(dev, thickness_cm):
    """How much to multiply the drawn photon count when the render is THICKER than anything the card was fitted on.

    WHY. A card's exposure model is a regression of log10 photons on water-equivalent thickness, fitted over the
    thicknesses its paired frames happened to contain: 9.3-11.5 cm for the PIXIUM 4600 (n=18) and 9.7-19.7 cm for
    the Cios Fusion (n=366), with R^2 0.19 and 0.15 -- and the PIXIUM slope is NEGATIVE. Sampled at a lateral
    abdomen (28-38 cm of water) that regression hands a thick patient FEWER photons, about a dozen quanta per
    pixel survive the path, and the vertebral bodies' 19 % primary modulation sits under the quantum noise. Frames
    drawn that way showed no spine at all (docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md, tools/diag_card_lateral.py).

    WHAT A REAL C-ARM DOES. Its automatic exposure control does not extrapolate a regression: it raises output
    until the DETECTOR sees enough signal. So outside the fitted range the photon count here is multiplied by
    exp(mu_water * (thickness - fitted_max)), which holds the transmitted quanta at the level the card was fitted
    at, capped at AEC_MAX_GAIN because a real tube saturates. Inside the fitted range nothing changes.

    This is an EXTRAPOLATION and is flagged as one: the returned terms carry aec_extrapolated and aec_gain, and
    any figure or number drawn from such a frame must say so. Set AEC_MODE = "off" to get the raw draw.
    """
    if AEC_MODE == "off" or thickness_cm is None or not np.isfinite(thickness_cm):
        return 1.0, None
    r = (((dev.get("distribution") or {}).get("aec") or {}).get("log10_photons_on_thickness") or {})
    rng_ = r.get("x_range")
    if not rng_ or len(rng_) != 2 or not all(np.isfinite(rng_)):
        return 1.0, None
    x_max = float(rng_[1])
    if thickness_cm <= x_max:
        return 1.0, x_max
    g = float(np.exp(MU_WATER_EFF * (thickness_cm - x_max)))
    return float(min(g, AEC_MAX_GAIN)), x_max


SPREAD = 0.2        # per-exposure draws are clipped to the card's [SPREAD, 1-SPREAD] quantiles; 0 = the full fitted spread
# HOW AN IMPLAUSIBLE DRAW IS REJECTED. "clip" holds every term to its central band; "typicality" keeps every marginal
# and rejects only draws the device itself would not produce. They are not equivalent, and the difference is large:
# the clip is applied to 8-11 correlated terms at once, so a styled frame is drawn from 1.7-5.1 % of the card's fitted
# JOINT distribution (tools/device_spread_sweep.py, docs/DEVICE_SPREAD_SWEEP.md), while the gate reaches 99 % of it.
# The clip remains the default until the A/B on real frames says otherwise (slurm/device_spread_arm.sh): a sampler
# that reaches more of the distribution is not automatically better training data, and this project does not adopt a
# change on the strength of the argument for it.
SAMPLE_MODE = os.environ.get("DEVICE_SAMPLE_MODE", "clip")   # clip | typicality | full
TYPICALITY_Q = 99.0  # the card's own percentile, the one device_fit.coverage validates each card against
WINDOW_JITTER = 2.5  # grey levels, on the OR-window percentile targets


def _clip_draws(cop, draws, spread):
    """The per-frame fits carry outliers (photons spanned three decades on the Cios card, p10 107 to p90 58,088 per mm²)
    and the copula reproduces them faithfully, so a draw can pair an extreme count with an extreme blur; the first
    demo sheets showed pure grain beside pure smear. Clipping each term to the central quantile band keeps the draws
    on the part of the distribution the frames actually occupy; `sweep` measures what that costs or buys."""
    if not cop or spread <= 0:
        return draws
    lv = np.array(cop["levels"])
    for nm in cop["names"]:
        q = np.array(cop["quantiles"][nm]); lo = float(np.interp(spread, lv, q)); hi = float(np.interp(1.0 - spread, lv, q))
        draws[nm] = np.clip(draws[nm], min(lo, hi), max(lo, hi))
    return draws


def _copula_z(cop, n, rng, cond=None):
    """The normal scores `device_fit.copula_sample` would draw, before they are mapped through the marginals.

    Mirrors that function exactly: a conditional Gaussian when `cond` fixes columns, the fitted correlation otherwise.
    The gate works here rather than on the mapped values because the mapping is a 41-point piecewise-linear inverse
    CDF, and where a term is discrete -- a tube that runs at four mAs settings, a kVp that takes a handful of values --
    that inverse is not unique. Reading a value back through it biases the score, which is what the first version of
    this gate did: it shifted one card's marginal median by 0.55 SD while every other check passed.
    """
    from scipy.stats import norm
    names = cop["names"]; C = np.array(cop["corr"]); lv = np.array(cop["levels"]); k = len(names)
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
    return Z


def _z_to_values(cop, Z):
    """Normal scores through the card's marginals, the same mapping `copula_sample` ends with."""
    from scipy.stats import norm
    lv = np.array(cop["levels"]); U = norm.cdf(Z)
    out = {nm: np.interp(U[:, j], lv, cop["quantiles"][nm]) for j, nm in enumerate(cop["names"])}
    for nm, v in (cop.get("constants") or {}).items():
        out[nm] = np.full(Z.shape[0], np.nan if v is None else v)
    return out


def _typicality_draws(cop, n, rng, cond=None, q=TYPICALITY_Q, oversample=4, max_rounds=12, return_z=False):
    """n draws from the FULL copula with only the atypical COMBINATIONS rejected.

    A draw is atypical when the Mahalanobis distance of its copula normal scores exceeds the qth percentile of that
    distance over the card's own draws -- the statistic `device_fit.coverage` scores each card on against held-out
    real frames. Every marginal is untouched, so the sampler still reaches the tails of each term; what it cannot
    produce is a COMBINATION the device never produced, which is what the clip was aimed at and what it missed by
    shrinking the marginals instead.
    """
    names = cop["names"]; C = np.array(cop["corr"], float); k = len(names)
    Ci = np.linalg.inv(C + 1e-6 * np.eye(k))
    Zref = rng.multivariate_normal(np.zeros(k), C, size=40000)
    thr = float(np.percentile(np.einsum("ij,jk,ik->i", Zref, Ci, Zref), q))
    kept, have = [], 0
    for _ in range(max_rounds):
        Z = _copula_z(cop, max(n * oversample, 256), rng, cond)
        ok = np.einsum("ij,jk,ik->i", Z, Ci, Z) <= thr
        idx = np.flatnonzero(ok)
        if idx.size:
            take = idx[: n - have]
            kept.append(Z[take]); have += take.size
        if have >= n:
            break
    if have < n:              # a conditional slice can be mostly atypical; say so rather than pad silently
        print(f"typicality gate: only {have}/{n} draws accepted after {max_rounds} rounds; the remainder comes from "
              "the ungated copula", flush=True)
        kept.append(_copula_z(cop, n - have, rng, cond))
    Z = np.concatenate(kept)[:n]
    return (_z_to_values(cop, Z), Z, thr) if return_z else _z_to_values(cop, Z)


def sample_terms(dev, n, rng, cond=None, spread=None, mode=None):
    """n term sets for one device. `cond` may fix copula columns (thickness_cm, lat_deg, kvp ...).

    `mode` selects how an implausible draw is rejected: "clip" (each term to its central band), "typicality" (full
    marginals, atypical combinations rejected) or "full" (no rejection). See SAMPLE_MODE.
    """
    fitted = dev["physics_terms"]["fitted"]; pitch_fit = float(dev["device"]["fit_pitch_mm"])
    cop = dev.get("distribution", {}).get("copula")
    md = (mode or SAMPLE_MODE).lower()
    if not cop:
        draws = {}
    elif md == "typicality":
        draws = _typicality_draws(cop, n, rng, cond)
    elif md == "full":
        draws = DF.copula_sample(cop, n, rng, cond)
    else:
        draws = _clip_draws(cop, DF.copula_sample(cop, n, rng, cond), SPREAD if spread is None else spread)
    out = []
    for i in range(n):
        t = {}
        for g in GLOBAL:
            t[g] = float(fitted[g]["median"])
        for g in ("sigma_s", "sigma_u"):
            t[g + "_mm"] = t[g] * pitch_fit
        def dr(col, fallback):
            v = draws.get(col)
            return float(v[i]) if v is not None and np.isfinite(v[i]) else fallback
        t["s"] = float(np.clip(dr("s", _q(dev["physics_terms"]["scatter_fraction_per_frame"], "median", fitted["s"]["median"])), 0.0, 0.85))
        t["sigma_r_mm"] = float(np.clip(dr("sigma_r", fitted["sigma_r"]["median"]), 0.0, 8.0)) * pitch_fit
        t["alpha"] = float(np.clip(dr("alpha", fitted["alpha"]["median"]), 0.0, 3.0))
        lp = dr("log10_photons", np.log10(_q(dev["physics_terms"]["photons_per_fit_px"], "median", 1000.0)))
        t["photons_per_mm2"] = float(10 ** lp) / pitch_fit ** 2
        # AEC OUTSIDE THE FITTED THICKNESS RANGE: hold the detector's quanta instead of extrapolating the
        # regression, and say so in the terms (see aec_gain).
        thick_cond = (cond or {}).get("thickness_cm")
        g, x_max = aec_gain(dev, thick_cond if thick_cond is not None else t.get("thickness_cm"))
        t["aec_gain"] = round(float(g), 3)
        t["aec_fit_thickness_max_cm"] = (round(float(x_max), 2) if x_max is not None else None)
        t["aec_extrapolated"] = bool(g > 1.0)
        if g > 1.0:
            t["photons_per_mm2"] *= g
        t["win_A"] = dr("win_A", np.nan); t["win_B"] = dr("win_B", np.nan)
        t["thickness_cm"] = dr("thickness_cm", np.nan); t["lat_deg"] = dr("lat_deg", np.nan)
        sp = dr("sigma_p_px", np.nan)
        b = dev.get("border", {})
        t["sigma_p_mm"] = (sp if np.isfinite(sp) else _q(b.get("penumbra_sigma_px"), "median", 2.0)) * pitch_fit
        t["halo"] = dr("halo", _q(b.get("halo"), "median", 0.0))
        t["field_frac"] = dr("field_frac", _q(b.get("field_frac"), "median", 0.8))
        t["rot180"] = bool(rng.uniform() < float(dev["device"].get("rot180_share") or 0.0))
        t["sample_mode"] = md
        out.append(t)
    return out


def field_mask(dev, shape, rng, t=None):
    """A collimator field for a frame of `shape`, drawn from the card's border quantiles (blades or iris)."""
    H, W = shape; b = dev.get("border", {}); yy, xx = np.mgrid[0:H, 0:W]
    u = (xx - W / 2) / (W / 2); v = (yy - H / 2) / (H / 2)
    if (b.get("shape") or dev["device"].get("field_shape")) == "circle":
        cu = _draw_q(b.get("centre_u"), rng, 0.0); cv = _draw_q(b.get("centre_v"), rng, 0.0); r = _draw_q(b.get("radius"), rng, 0.98)
        return ((u - cu) ** 2 + (v - cv) ** 2) <= r * r
    l = _draw_q(b.get("left"), rng, -1.0); r_ = _draw_q(b.get("right"), rng, 1.0); tp = _draw_q(b.get("top"), rng, -1.0); bt = _draw_q(b.get("bottom"), rng, 1.0)
    return (u >= l) & (u <= r_) & (v >= tp) & (v <= bt)


def style(water_cm, bone_cm, hit, dev, t, rng, pitch_mm, field=None, RP=None, out8=True, window_region="field"):
    """One styled frame (uint8, bone bright, OR window) from water / bone path maps in cm at `pitch_mm` per pixel.

    window_region (A31): "field" reproduces the shipped corpora (percentiles over the exposed field within the
    render's hit mask -- which on an oblique or lateral render includes the air beside the patient). "body" takes
    them over attenuation >= 0.25 inside that region, the treatment realxray_cobra_export.py --window-region body
    gives the real frames; a styled set paired with cobra_elekta_v3 must pass "body" so real and styled frames get
    identical display treatment. Same fallback guard as the exporter."""
    RP = RP or rp_tables()
    H, W = water_cm.shape
    field = field_mask(dev, (H, W), rng, t) if field is None else field
    yy, xx = np.mgrid[0:H, 0:W]
    u = (xx - W / 2) / (W / 2); v = (yy - H / 2) / (H / 2)
    d = dict(water=np.asarray(water_cm, np.float64), bone=np.asarray(bone_cm, np.float64), fieldf=field.astype(np.float64), u=u, v=v, r2=u * u + v * v,
             rot=int(t["rot180"]))
    th = dict(kb=t["kb"], s=t["s"], sigma_s=t["sigma_s_mm"] / pitch_mm, sigma_r=t["sigma_r_mm"] / pitch_mm, alpha=t["alpha"], sigma_u=t["sigma_u_mm"] / pitch_mm,
              b=t["b"], c=t["c"], d=t["d"], sigma_p=t["sigma_p_mm"] / pitch_mm, s_t=0.0, b4=0.0)
    N = max(t["photons_per_mm2"] * pitch_mm ** 2, 2.0)
    a = DF.forward(th, d, RP, noisy=(N, rng))                      # attenuation, noise drawn where the detector counts
    if not out8:
        return a, field
    # display: the device's monotone transfer, then the OR window on the exposed field
    soft = PH.__dict__.get("gaussian_filter", None)
    from scipy.ndimage import gaussian_filter
    fsoft = gaussian_filter(field.astype(np.float64), max(th["sigma_p"], 0.3))
    inside = fsoft > 0.5
    stored = a if dev["device"]["reading"] != "neg_log_offset" else a
    wm = inside & hit if (inside & hit).any() else inside
    if window_region == "body":
        body = (stored >= 0.25) & wm
        if int(body.sum()) >= max(2000, int(0.02 * wm.sum())):
            wm = body
    vals = stored[wm]
    if vals.size < 50:
        vals = stored.ravel()
    src = np.percentile(vals, OR_PCT)
    # the card's stored spread jitters the window: a device whose 5-95 spread varies frame to frame gets that variation
    tgt = OR_TARGETS + rng.normal(0, WINDOW_JITTER, size=5); tgt = np.sort(np.clip(tgt, 1, 254))
    img = np.interp(stored, src, tgt, left=tgt[0], right=tgt[-1])
    black = float(rng.uniform(2, 14))
    img = fsoft * img + (1.0 - fsoft) * black
    if t.get("halo", 0.0):
        # processing overshoot at the border, as measured: a bright / dark rim inside the field of the border's own width
        rim = gaussian_filter(field.astype(np.float64), 2.0 * max(th["sigma_p"], 0.6)) - fsoft
        img = img + t["halo"] * 60.0 * rim
    if t["rot180"]:
        img = img[::-1, ::-1]
    return np.clip(np.rint(img), 0, 255).astype(np.uint8), field


def style_paths(water_cm, bone_cm, dev, rng, pitch_mm, hit=None, spread=None, RP=None):
    """Convenience for figure tools: one styled 8-bit frame from path maps, terms drawn conditioned on the thickness."""
    hit = np.ones(np.asarray(water_cm).shape, bool) if hit is None else hit
    H, W = hit.shape
    yy, xx = np.mgrid[0:H, 0:W]; disc = ((yy - H / 2) ** 2 + (xx - W / 2) ** 2 <= (0.06 * min(H, W)) ** 2) & hit
    thick = float(np.median(np.asarray(water_cm)[disc])) if disc.any() else float("nan")
    t = sample_terms(dev, 1, rng, cond={"thickness_cm": thick} if np.isfinite(thick) else None, spread=spread)[0]
    t["rot180"] = False                                  # figure frames keep the orientation the layout gives them
    img, field = style(np.asarray(water_cm, np.float64), np.asarray(bone_cm, np.float64), hit, dev, t, rng, pitch_mm, field=np.ones((H, W), bool), RP=RP)
    return img, t


def style_uint8(img8, dev, rng, pitch_mm, a_max=6.0, spread=None, RP=None):
    """APPROXIMATE styling of an 8-bit render that has no path maps: the stored value is read as a linear window of
    attenuation (0..a_max), split into water-equivalent path (bone share from the brightest tenth), and pushed through
    the same forward model. Documented as approximate; used only where a corpus stores images and not path maps."""
    x = np.asarray(img8, np.float64) / 255.0
    a = x * a_max
    bone = np.clip((x - np.percentile(x, 90)) / max(1e-6, 1.0 - np.percentile(x, 90)), 0, 1) * a * 0.35
    water = np.clip(a - bone, 0, None) / 0.2            # cm of water at mu 0.2 / cm (the repo's water basis at ~70 keV)
    bone_cm = bone / 0.5
    img, t = style_paths(water, bone_cm, dev, rng, pitch_mm, spread=spread, RP=RP)
    return img, t


def _pairs_of(dev_name):
    d = DF.DEVICES[dev_name]
    return sorted(glob.glob(os.path.join(os.path.expanduser(d["pairs"]), "pair_*.npz")))


def real_display(z, dev_name):
    """The real frame of a pair through the same OR window, bone bright, for the side-by-side."""
    d = DF.DEVICES[dev_name]; real = z["real"].astype(np.float64); hit = z["hit"].astype(bool)
    field = PH.exposed_field(real, hit)
    att = DF.stored_to_atten(real, field, d["reading"], 0.0)
    vals = att[field & hit] if (field & hit).any() else att.ravel()
    img = np.interp(att, np.percentile(vals, OR_PCT), OR_TARGETS, left=OR_TARGETS[0], right=OR_TARGETS[-1])
    img = np.where(field, img, 6.0)
    return np.clip(np.rint(img), 0, 255).astype(np.uint8), field


def cmd_demo(a):
    from PIL import Image, ImageDraw
    dev = load_device(a.device); rng = np.random.default_rng(a.seed); RP = rp_tables()
    pairs = _pairs_of(a.device)
    if not pairs:
        raise SystemExit("no pairs")
    idx = rng.choice(len(pairs), min(a.n, len(pairs)), replace=False)
    pitch = float(dev["device"]["fit_pitch_mm"])
    tiles = []; dist = []
    for i in idx:
        z = np.load(pairs[i]); water = z["water_cm"].astype(np.float64); bone = z["bone_cm"].astype(np.float64); hit = z["hit"].astype(bool)
        real8, rfield = real_display(z, a.device)
        # statistics inside the field AND the CT's own rays: outside `hit` the render has no anatomy (a truncated CT
        # renders as air) while the real frame does, and the histogram distance was reading that, not the styling
        rs = PH.image_stats(real8, rfield & hit)
        thick = float(np.median(water[hit])) if hit.any() else np.nan
        row = [real8]
        for k in range(a.draws):
            t = sample_terms(dev, 1, rng, cond={"thickness_cm": thick} if np.isfinite(thick) else None)[0]
            img, fld = style(water, bone, hit, dev, t, rng, pitch, field=rfield if a.keep_field else None, RP=RP)
            row.append(img)
            m_s = (fld & hit) if not t["rot180"] else (fld & hit)[::-1, ::-1]
            ss = PH.image_stats(img, m_s)
            dist.append(PH.stat_distance(rs, ss))
        tiles.append(row)
    H, W = tiles[0][0].shape; s = 256 / max(H, W)
    sheet = Image.new("L", (int(W * s) * (a.draws + 1), int(H * s) * len(tiles)), 0)
    for r, row in enumerate(tiles):
        for c, im in enumerate(row):
            sheet.paste(Image.fromarray(im).resize((int(W * s), int(H * s))), (c * int(W * s), r * int(H * s)))
    out = Path(a.out or (DF.ROOT + f"/{a.device}")); out.mkdir(parents=True, exist_ok=True)
    sheet.save(out / "fig_style_demo.png")
    med = {k: float(np.median([d[k] for d in dist if k in d])) for k in dist[0]} if dist else {}
    json.dump(dict(device=a.device, n=len(tiles), draws=a.draws, distances_median=med, distances=dist), open(out / "style_demo.json", "w"), indent=1)
    print(f"{a.device}: wrote {out / 'fig_style_demo.png'}; real-vs-styled distances (median over draws): {med}", flush=True)
    return 0


def _stats_for(dev, dev_name, pairs, idx, seed, spread, RP, fixed=None):
    """Pooled statistics of the real frames and of one styled draw per pair; `fixed` overrides drawn terms."""
    rng = np.random.default_rng(seed); pitch = float(dev["device"]["fit_pitch_mm"]); R = []; S = []
    for i in idx:
        z = np.load(pairs[i]); water = z["water_cm"].astype(np.float64); bone = z["bone_cm"].astype(np.float64); hit = z["hit"].astype(bool)
        real8, rfield = real_display(z, dev_name); R.append(PH.image_stats(real8, rfield & hit))
        thick = float(np.median(water[hit])) if hit.any() else np.nan
        t = sample_terms(dev, 1, rng, cond={"thickness_cm": thick} if np.isfinite(thick) else None, spread=spread)[0]
        if fixed:
            t.update(fixed)
        img, fld = style(water, bone, hit, dev, t, rng, pitch, RP=RP)
        m_s = (fld & hit) if not t["rot180"] else (fld & hit)[::-1, ::-1]
        S.append(PH.image_stats(img, m_s))
    pr, ps = PH.pool_stats(R), PH.pool_stats(S)
    h = len(R) // 2
    ref = PH.stat_distance(PH.pool_stats(R[:h]), PH.pool_stats(R[h:])) if h >= 3 else None
    return PH.stat_distance(pr, ps), ref, pr, ps


def cmd_stats(a):
    """Unpaired-path validation: styled draws vs the device's real frames, statistics only (no side-by-side)."""
    dev = load_device(a.device); rng = np.random.default_rng(a.seed); RP = rp_tables()
    pairs = _pairs_of(a.device)
    idx = rng.choice(len(pairs), min(a.n, len(pairs)), replace=False)
    d, ref, pr, ps = _stats_for(dev, a.device, pairs, idx, a.seed, a.spread, RP)
    out = Path(a.out or (DF.ROOT + f"/{a.device}")); out.mkdir(parents=True, exist_ok=True)
    json.dump(dict(device=a.device, n=len(idx), spread=a.spread if a.spread is not None else SPREAD, real_vs_styled=d, real_vs_real_reference=ref, real=pr, styled=ps),
              open(out / "style_stats.json", "w"), indent=1)
    print(f"{a.device}: real vs styled {d}; real-vs-real floor {ref}", flush=True)
    return 0


def cmd_sweep(a):
    """Which knob closes the real-vs-styled gap: the draw spread (0.5 = every term at its median, 0 = the full fitted
    spread), then one term at a time held at its median while the others are drawn. Ratios to the real-vs-real floor."""
    dev = load_device(a.device); rng = np.random.default_rng(a.seed); RP = rp_tables()
    pairs = _pairs_of(a.device)
    idx = rng.choice(len(pairs), min(a.n, len(pairs)), replace=False)
    rows = []
    fitted = dev["physics_terms"]["fitted"]; pitch_fit = float(dev["device"]["fit_pitch_mm"])
    med = dict(s=float(fitted["s"]["median"]), sigma_r_mm=float(fitted["sigma_r"]["median"]) * pitch_fit, alpha=float(fitted["alpha"]["median"]),
               photons_per_mm2=float(_q(dev["physics_terms"]["photons_per_fit_px"], "median", 1000.0)) / pitch_fit ** 2)
    configs = [("spread 0.5 (all medians)", 0.5, None), ("spread 0.35", 0.35, None), ("spread 0.2", 0.2, None), ("spread 0.1", 0.1, None), ("spread 0 (full)", 0.0, None)]
    configs += [(f"spread 0 but {k} at median", 0.0, {k: v}) for k, v in med.items()]
    configs += [("spread 0.2, photons x4", 0.2, {"photons_per_mm2": med["photons_per_mm2"] * 4}), ("spread 0.2, photons /4", 0.2, {"photons_per_mm2": med["photons_per_mm2"] / 4}),
                ("spread 0.2, sigma_r x2", 0.2, {"sigma_r_mm": med["sigma_r_mm"] * 2}), ("spread 0.2, sigma_r /2", 0.2, {"sigma_r_mm": med["sigma_r_mm"] / 2}),
                ("spread 0.2, alpha x2", 0.2, {"alpha": med["alpha"] * 2}), ("spread 0.2, alpha 0", 0.2, {"alpha": 0.0})]
    ref = None
    for name, spread, fixed in configs:
        d, ref, _, _ = _stats_for(dev, a.device, pairs, idx, a.seed, spread, RP, fixed)
        rows.append(dict(config=name, spread=spread, fixed=fixed, distances=d, ratio_to_floor={k: (d[k] / ref[k] if ref and ref.get(k) else None) for k in d}))
        print(f"{name:34s} " + "  ".join(f"{k} {d[k]:.3f} ({d[k] / ref[k]:.1f}x)" for k in d if ref and ref.get(k)), flush=True)
    out = Path(a.out or (DF.ROOT + f"/{a.device}")); out.mkdir(parents=True, exist_ok=True)
    json.dump(dict(device=a.device, n=len(idx), floor=ref, rows=rows), open(out / "style_sweep.json", "w"), indent=1)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["demo", "stats", "sweep"])
    ap.add_argument("--device", required=True); ap.add_argument("--n", type=int, default=6); ap.add_argument("--draws", type=int, default=3)
    ap.add_argument("--seed", type=int, default=0); ap.add_argument("--out", default=None)
    ap.add_argument("--spread", type=float, default=None, help="clip per-exposure draws to the card's [spread, 1-spread] quantiles (default SPREAD)")
    ap.add_argument("--keep-field", action="store_true", help="demo: use the real frame's own field instead of a drawn one")
    a = ap.parse_args()
    return dict(demo=cmd_demo, stats=cmd_stats, sweep=cmd_sweep)[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
