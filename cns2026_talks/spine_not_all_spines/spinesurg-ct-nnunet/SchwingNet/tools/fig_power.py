#!/usr/bin/env python
"""Figure 5 of the SchwingNet manuscript: transitional persons needed; naming against training persons on plain film
and on one C-arm separated by view; same-device detection against real frames with one-view arms; and render-only
detectors at matched N read along the lateral angle.

Four components; every curve and point is read from a results file or computed here and written to
results/power/power.json, and every number on the page is listed with its file and pointer in
figures/figure5.record.json. Rebuilt 2026-09-25 (afternoon) from the 10:26 build: panels (c) (the matched-N arm dot
plot) and (d) (the pooled fit scatter) are replaced by the same-device detection curve with its one-view arms and by
the arms' recall against angle; the pooled fit's numbers stay in the text and in power.json ("pooled_fit").

(a) Wilson 95 % lower bound of exact-level accuracy against the number of transitional test persons n, for
    k = 0, 1, 2 and 5 errors, with the two pre-stated G6 targets as lines (90 % exact level, 85 % variant
    sensitivity; results/power_table.json#targets_pct); markers where each k clears each line, the k = 0 crossings
    labelled (35 and 22). Every n is a count of PERSONS (independent spines), never of frames.
(b) Naming against training persons. Film (results/coverage/film_ncurve/film_ncurve.json): exact-level naming on
    the fixed v9 VAL films of each corpus against N training persons of that corpus, the film-free render-only
    encoder fine-tuned per cell; seed mean, bars over the per-seed range where three seeds ran; N = 0 is the
    render-only encoder, drawn left of a break. C-arm (results/indomain/name_fill.json#figure5b, whole frame):
    the v9 encoder and head fine-tuned per case-grouped fold on N C-ArmLSpine persons of ONE view protocol and read
    on that protocol (solid: lateral, anteroposterior), the lateral-trained cells read on the anteroposterior test
    frames (dashed), and the both-protocol cells at all persons (x). N = all is the fold mean (87.6 persons).
(c) Same-device detection (results/indomain/det_fill.json): vertebra recall on the C-ArmLSpine test split (body
    boxes, confidence 0.74, the reported convention) against N real frames of the device added to a fixed
    background, both views of N/2 patients (curves per test view, seeds pooled, case-clustered intervals), and the
    one-view arms: 25 or 50 frames of one protocol alone, read on that protocol (filled triangles) and on the other
    (open), two seeds pooled (det_fill.json#protocol).
(d) The coverage arms along the angle (results/coverage/experiment/runs/<arm>/unseen/recall_vs_angle.json):
    render-only detectors of the Surgio-B51 card at matched N (2,646 renders) whose training poses are the device's
    real anteroposterior and lateral poses (low), an arc of poses (high), or twice the real poses (low, 2N), read at
    confidence 0.25 on renders of 40 unseen subjects at 19 lateral angles (tilt 0); seed mean with the per-seed range
    shaded; dotted verticals at the three trained angles of the low arms. The Surgio card renders thick laterals
    photon-starved (recall_vs_angle.md), so the +-90 degree bins conflate geometry with synthetic underexposure.

Journal rules (SchwingNet/RSNA_AI_REQUIREMENTS.md): four components a-d with bare bold letters; Arial, every text
>= 12 pt at the 7.0 in print width (audited from the PDF after writing); sans-serif; grid on both axes; degree
sign, not deg; graphs as TIF at 1,200 dpi, LZW. Palette: Okabe-Ito blue / green / vermillion (validated with the
dataviz checks, all pairs, 2026-09-25: CVD dE >= 11.0, normal-vision dE >= 18.7, contrast >= 3:1) plus two
deliberate neutrals (ink, grey) that carry a marker shape of their own; in (b) and (c) the C-arm's two views are
the neutrals (lateral ink, anteroposterior grey) so the film corpora keep the three colours.

    python SchwingNet/tools/fig_power.py
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator

REPO = Path(__file__).resolve().parents[2]
SN = REPO / "SchwingNet"
RES = SN / "results"
FIG = SN / "figures"
OUTDIR = RES / "power"
POWER_TABLE = RES / "power_table.json"
RECOMPUTE = RES / "stats_review" / "recompute.json"
POOLED = RES / "coverage" / "pooled_fit.json"
FILM_JSON = RES / "coverage" / "film_ncurve" / "film_ncurve.json"
NAME_FILL = RES / "indomain" / "name_fill.json"
DET_FILL = RES / "indomain" / "det_fill.json"
SCORES = RES / "coverage" / "experiment" / "scores.json"
RUNS = RES / "coverage" / "experiment" / "runs"
SENS_074 = RES / "coverage" / "sensitivity" / "pooled_fit_conf074.json"
SENS_TRAINED = RES / "coverage" / "sensitivity" / "pooled_fit_trained_only.json"

Z95 = 1.959963984540054
BOOT = 1000
BOOT_SEED = 0

# palette (Okabe-Ito; validated 2026-09-25 with the dataviz six checks, all pairs: blue/green/vermillion PASS,
# worst CVD dE 11.0 deutan, worst normal-vision dE 18.7, every contrast >= 3:1; ink and grey are deliberate neutrals
# that always carry their own marker shape)
INK, SOFT, GRID = "#1f2d3d", "#5d6b7c", "#d9dee5"
C_BLUE, C_GREEN, C_VERM = "#0072B2", "#009E73", "#D55E00"
K_LIST = [0, 1, 2, 5]
K_RAMP = ["#1f2d3d", "#46546a", "#6f7b8b", "#9aa4b0"]
K_MARK = ["o", "s", "^", "v"]
FILM = {"nhanes": ("NHANES II", C_BLUE, "o"), "buu_full": ("BUU-LSPINE", C_VERM, "s"), "csxa": ("CSXA", C_GREEN, "^")}
FILM_ORDER = ["nhanes", "buu_full", "csxa"]
VIEW = {"LAT": ("lateral", INK, "o"), "AP": ("anteroposterior", SOFT, "s")}   # the C-arm's two views: the neutrals
DEVICE_D = "surgio_b51_dr"
ARMS_D = [("low", "anteroposterior and lateral poses, N", C_VERM, "o"),
          ("high", "arc of poses, N", C_BLUE, "^"),
          ("low2n", "anteroposterior and lateral poses, 2N", C_GREEN, "s")]
TRAINED_LATS = (-90.0, 0.0, 90.0)
ARM_CONF = 0.25
ARM_TILT = "0.0"
DET_CONV, DET_CONF = "body", "0.74"

FS = 12.0            # every text on the page
FS_LETTER = 14.0     # panel letters, bold
W_IN = 7.0
H_IN = 9.4


# ---------------------------------------------------------------------------------------------------------------
# statistics
# ---------------------------------------------------------------------------------------------------------------
def wilson(s: int, n: int, z: float = Z95) -> tuple[float, float]:
    """Wilson score interval for s successes in n trials."""
    if n <= 0:
        return (float("nan"), float("nan"))
    p = s / n
    centre = p + z * z / (2 * n)
    half = z * math.sqrt(max(p * (1 - p) / n + z * z / (4 * n * n), 0.0))
    d = 1 + z * z / n
    return (max(0.0, (centre - half) / d), min(1.0, (centre + half) / d))


def meets(lb: float, thr: float, strict: bool) -> bool:
    return lb > thr if strict else lb >= thr


def wilson_n_min(k: int, thr: float, strict: bool, n_max: int = 100000) -> int | None:
    """Smallest n at which n - k successes put the Wilson lower bound on thr."""
    for n in range(k + 1, n_max):
        if meets(wilson(n - k, n)[0], thr, strict):
            return n
    return None


def wilson_min_successes(n: int, thr: float, strict: bool) -> int | None:
    if not meets(wilson(n, n)[0], thr, strict):
        return None
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if meets(wilson(mid, n)[0], thr, strict):
            hi = mid
        else:
            lo = mid + 1
    return lo


def wilson_power(n: int, p_true: float, thr: float, strict: bool) -> float:
    s = wilson_min_successes(n, thr, strict)
    return 0.0 if s is None else float(stats.binom.sf(s - 1, n, p_true))


# ---------------------------------------------------------------------------------------------------------------
# inputs
# ---------------------------------------------------------------------------------------------------------------
def rel(p: Path) -> str:
    return str(p.relative_to(REPO)).replace("\\", "/")


def file_tag(p: Path) -> dict:
    b = p.read_bytes()
    return {"file": rel(p), "sha256": hashlib.sha256(b).hexdigest(),
            "mtime": dt.datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")}


def load_json(p: Path) -> dict:
    return json.load(open(p, encoding="utf-8"))


def run_checks(pt: dict) -> dict:
    """The Wilson numbers of panel (a) against the independent implementation and the pre-stated table."""
    out = {}
    rc = load_json(RECOMPUTE)["R4_wilson"]
    mine = {"bound85": wilson_n_min(0, 0.85, False), "bound90": wilson_n_min(0, 0.90, False)}
    assert mine == rc["min_n_zero_errors"], (mine, rc["min_n_zero_errors"])
    for p, key in ((0.97, "true_97_bound90_power80"), (0.98, "true_98_bound90_power80")):
        n_ok = next(n for n in range(20, 1000) if wilson_power(n, p, 0.90, False) >= 0.80)
        assert n_ok == rc["smallest_n_for_80pct_power"][key], (key, n_ok)
    assert abs(wilson_power(60, 0.97, 0.90, False) - rc["probability_bound_met"]["n60_bound90"]["true_97"]) < 1e-9
    for k in ("0", "1", "2", "3", "5"):
        for n, v in pt["lower_bound_pct_by_k_then_n"][k].items():
            assert abs(wilson(int(n) - int(k), int(n))[0] * 100 - v) < 0.006, (k, n, v)
    out["stats_review_recompute"] = (f"min n {mine} (results/stats_review/recompute.json#R4_wilson), 80 %-power n "
                                     "and n60 probability reproduced")
    out["power_table_json"] = "all 30 Wilson cells reproduced to 0.01 pp"
    out["verdict"] = "PASS"
    return out


def load_film(pooled: dict) -> dict:
    """Film N-curve cells: seed mean and per-seed range per corpus and N key; the seed-0 cross-corpus transfer kept
    in the record (not drawn since the 2026-09-25 afternoon build)."""
    fn = load_json(FILM_JSON)
    assert fn["n_cells"] == fn["n_cells_scored"] == 48, (fn["n_cells"], fn["n_cells_scored"])
    out = {}
    for src in FILM_ORDER:
        curve = fn["curves"][src]
        fs = pooled["film_summary"][src]
        n_all = fs["N_all_persons"]
        pts = []
        for nkey, cell in curve.items():
            accs = [p["acc"] for p in cell["points"]]
            n_persons = {p["n_persons"] for p in cell["points"]}
            assert len(n_persons) == 1, (src, nkey, n_persons)
            n = n_persons.pop()
            if nkey == "all":
                assert n == n_all, (src, n, n_all)
            if nkey in fs["points"]:
                assert abs(np.mean(accs) * 100 - fs["points"][nkey]["mean_acc_pct"]) < 0.051, (src, nkey, accs)
            s0 = next(p for p in cell["points"] if p["seed"] == 0)
            pts.append({"Nkey": nkey, "N": n, "seeds": len(accs), "acc_mean": float(np.mean(accs)),
                        "acc_min": float(min(accs)), "acc_max": float(max(accs)),
                        "per_seed": [{"seed": p["seed"], "acc": p["acc"], "lo": p["lo"], "hi": p["hi"]}
                                     for p in cell["points"]],
                        "cross_seed0": dict(s0["cross"]),
                        "pointer": f"{rel(FILM_JSON)}#/curves/{src}/{nkey}/points"})
        pts.sort(key=lambda p: p["N"])
        out[src] = {"label": FILM[src][0], "N_all_persons": n_all, "points": pts,
                    "asymptote_pct": fs["ipl"]["asymptote_pct"], "plateau_reached": fs["plateau_reached"],
                    "first_grid_N_within_2pt": fs["first_grid_N_within_2pt_key"]}
    return {"corpora": out, "generated": fn["generated"], "tool": fn["tool"], "tag": file_tag(FILM_JSON)}


def load_carm_naming() -> dict:
    """C-ArmLSpine naming against training persons per view protocol, whole frame, from name_fill.json#figure5b."""
    nf = load_json(NAME_FILL)
    rows = nf["figure5b"]
    keep = {}
    for i, r in enumerate(rows):
        if r.get("k") != "full":
            continue
        assert r["complete"] is True and r["held_out"] == "gate + lists", (i, r.get("held_out"))
        key = (r["arm"], r["train_view"], r["test_view"])
        keep.setdefault(key, []).append({"i": i, "N": r["N"], "x": float(r["x_persons_mean"]), "pct": r["point_pct"],
                                         "ci": r["ci_pct"], "correct": r["correct"], "n": r["n"], "seeds": r["seeds"],
                                         "pointer": f"{rel(NAME_FILL)}#/figure5b/{i}"})
    for v in keep.values():
        v.sort(key=lambda p: p["x"])
    for tv, n_expected in (("LAT", 623), ("AP", 633)):
        for k, v in keep.items():
            if k[2] == tv:
                assert all(p["n"] == n_expected for p in v), (k, [p["n"] for p in v])
    out = {"own": {tv: keep[("indomain", tv, tv)] for tv in ("LAT", "AP")},
           "cross_lat_on_ap": keep[("indomain", "LAT", "AP")],
           "cross_ap_on_lat": keep[("indomain", "AP", "LAT")],
           "both": {tv: keep[("indomain", "BOTH", tv)] for tv in ("LAT", "AP")},
           "zeroshot": {tv: keep[("zeroshot", "BOTH", tv)] for tv in ("LAT", "AP")},
           "design": {k: nf["design"][k] for k in ("question", "folds", "N", "views", "recipe", "scoring", "held_out")},
           "tag": file_tag(NAME_FILL), "generated": nf["generated"]}
    for tv in ("LAT", "AP"):
        assert len(out["both"][tv]) == 1 and out["both"][tv][0]["N"] == "all", out["both"][tv]
        assert out["own"][tv][0]["N"] == "0" and out["own"][tv][-1]["N"] == "all"
    return out


def load_detection() -> dict:
    """Same-device detection against real frames (both-view arm, per test view) and the one-view arms."""
    df = load_json(DET_FILL)
    curves = {}
    for nkey, cur in df["curves"]["carm"].items():
        n = int(nkey)
        curves[n] = {}
        for view in ("ALL", "LAT", "AP"):
            b = cur["pooled"][view][DET_CONV][DET_CONF]
            assert abs(100 * b["k"] / b["n"] - b["pct"]) < 0.06, (nkey, view, b)
            curves[n][view] = {"pct": b["pct"], "ci": b["ci"], "k": b["k"], "n": b["n"], "clusters": b["clusters"],
                               "seeds": cur["seeds"],
                               "pointer": f"{rel(DET_FILL)}#/curves/carm/{nkey}/pooled/{view}/{DET_CONV}/{DET_CONF}"}
    one = {}
    for pk, pv in df["protocol"].items():
        for c in pv["cells"]:
            assert df["cells"][c]["status"] == "scored" and df["cells"][c]["arm"] == "carm_view", c
        tv = pv["trained_on"]
        other = "AP" if tv == "LAT" else "LAT"
        rec = {"trained_on": tv, "other": other, "n_frames": pv["n_frames"], "n_patients": pv["n_patients"],
               "cells": pv["cells"]}
        for view in ("ALL", "LAT", "AP"):
            b = pv["pooled"][view][DET_CONV][DET_CONF]
            assert abs(100 * b["k"] / b["n"] - b["pct"]) < 0.06, (pk, view, b)
            rec[view] = {"pct": b["pct"], "ci": b["ci"], "k": b["k"], "n": b["n"],
                         "pointer": f"{rel(DET_FILL)}#/protocol/{pk}/pooled/{view}/{DET_CONV}/{DET_CONF}"}
        rec["own"], rec["on_other"] = rec[tv], rec[other]
        one[pk] = rec
    own = [r["own"]["pct"] for r in one.values()]
    oth = [r["on_other"]["pct"] for r in one.values()]
    summary = {"oneview_own_min_pct": min(own), "oneview_own_max_pct": max(own),
               "oneview_other_min_pct": min(oth), "oneview_other_max_pct": max(oth),
               "oneview_arms": sorted(one.keys()),
               "rule": "min and max over the four one-view arms (25 and 50 frames x anteroposterior and lateral), "
                       "each pooled over its two seeds, body boxes at confidence 0.74; 'own' = read on the protocol "
                       "trained on, 'other' = read on the other protocol"}
    return {"curves": curves, "one_view": one, "summary": summary, "design": df["design"]["arms"],
            "caveats": df.get("caveats"), "tag": file_tag(DET_FILL), "generated": df.get("when")}


def load_angle(pooled: dict) -> dict:
    """Recall against lateral angle of the Surgio-B51 coverage arms on the unseen render sweep, per seed."""
    out = {}
    lats_ref = None
    for arm, _lab, _c, _m in ARMS_D:
        out[arm] = {"seeds": {}}
        for seed in (0, 1):
            key = f"cov_{DEVICE_D}_{arm}_s{seed}"
            p = RUNS / key / "unseen" / "recall_vs_angle.json"
            d = load_json(p)
            assert d["eval_gate"]["held_out"] is True and d["eval_gate"]["overlap"] == 0, key
            assert d["n_subjects"] == 40 and abs(d["iou"] - 0.5) < 1e-9 and ARM_CONF in d["confs"], key
            pts = d["curves"][key][DEVICE_D][str(ARM_CONF)]["body"][ARM_TILT]
            lats = [q["lat"] for q in pts]
            if lats_ref is None:
                lats_ref = lats
                assert lats == [float(v) for v in range(-90, 91, 10)], lats
            assert lats == lats_ref, key
            a = pooled["arms"][key]
            out[arm]["seeds"][seed] = {"key": key, "N_train": a["N_train"], "subjects_train": a["subjects_train"],
                                       "H_lat": a["H_lat"], "val_mAP50": a["val"]["mAP50"],
                                       "pooled_unseen_recall": a["unseen_by_conf"][str(ARM_CONF)][DEVICE_D]["recall"],
                                       "bins": [{"lat": q["lat"], "n": q["n"], "recall": q["recall"], "lo": q["lo"], "hi": q["hi"]}
                                                for q in pts],
                                       "pointer": f"{rel(p)}#/curves/{key}/{DEVICE_D}/{ARM_CONF}/body/{ARM_TILT}",
                                       "tag": file_tag(p)}
        ys = np.array([[q["recall"] for q in s["bins"]] for s in out[arm]["seeds"].values()]) * 100
        mean = ys.mean(axis=0)
        trained = [i for i, l in enumerate(lats_ref) if l in TRAINED_LATS]
        untrained = [i for i, l in enumerate(lats_ref) if l not in TRAINED_LATS]
        out[arm]["lats"] = lats_ref
        out[arm]["seed_mean_pct"] = [round(float(v), 2) for v in mean]
        out[arm]["seed_range_pct"] = [[round(float(v), 2) for v in ys.min(axis=0)], [round(float(v), 2) for v in ys.max(axis=0)]]
        out[arm]["trained_bins_mean_pct"] = round(float(mean[trained].mean()), 1)
        out[arm]["untrained_bins_mean_pct"] = round(float(mean[untrained].mean()), 1)
        out[arm]["per_seed_trained_bins_mean_pct"] = [round(float(ys[s][trained].mean()), 1) for s in range(len(ys))]
        out[arm]["per_seed_untrained_bins_mean_pct"] = [round(float(ys[s][untrained].mean()), 1) for s in range(len(ys))]
        out[arm]["all_bins_mean_pct"] = round(float(mean.mean()), 1)
        out[arm]["pooled_unseen_recall_pct_per_seed"] = [round(100 * s["pooled_unseen_recall"], 1) for s in out[arm]["seeds"].values()]
    return {"arms": out, "n_subjects": 40, "n_bins": len(lats_ref), "n_trained_bins": len(TRAINED_LATS),
            "n_untrained_bins": len(lats_ref) - len(TRAINED_LATS), "trained_lats": list(TRAINED_LATS),
            "conf": ARM_CONF, "tilt": ARM_TILT, "card": DEVICE_D,
            "rule": "bin value = body recall at confidence 0.25 on the unseen sweep (40 TotalSegmentator subjects, "
                    "Surgio-B51 geometry, styled per card), tilt 0; seed mean over seeds 0 and 1; 'trained bins' = "
                    "the three lateral angles the real anteroposterior-lateral pool occupies (-90, 0, +90); "
                    "'untrained bins' = the other 16; means are unweighted over bins",
            "exposure_caveat": "the Surgio card renders thick laterals photon-starved, so the +-90 degree bins "
                               "conflate geometry with synthetic underexposure (experiment/runs/*/unseen/recall_vs_angle.md)"}


# ---------------------------------------------------------------------------------------------------------------
# drawing helpers
# ---------------------------------------------------------------------------------------------------------------
def style(ax):
    ax.grid(True, which="major", color=GRID, lw=0.5)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(SOFT)
        ax.spines[s].set_linewidth(0.6)
    ax.tick_params(labelsize=FS, colors=INK, width=0.6, length=3)


def log_ticks(ax, ticks, labels=None):
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_major_formatter(FixedFormatter(labels or [f"{t:,}" for t in ticks]))
    ax.xaxis.set_minor_locator(NullLocator())


def axis_break(ax, x0, x1):
    for xb in (x0, x1):
        ax.plot([xb / 1.04, xb * 1.04], [-0.012, 0.012], "-", lw=1.0, color=SOFT, clip_on=False,
                transform=ax.get_xaxis_transform(), zorder=6)


# ---------------------------------------------------------------------------------------------------------------
# panels
# ---------------------------------------------------------------------------------------------------------------
def panel_a(ax, target_level: float, target_sens: float) -> dict:
    ns = np.unique(np.round(np.geomspace(3, 1000, 400)).astype(int))
    curves, cross = {}, {}
    k90, k85 = f"n_lower_bound_ge_{target_level:.0f}", f"n_lower_bound_ge_{target_sens:.0f}"
    for k, col, mk in zip(K_LIST, K_RAMP, K_MARK):
        nn = ns[ns > k]
        lb = np.array([wilson(int(n) - k, int(n))[0] * 100 for n in nn])
        ax.plot(nn, lb, "-", lw=1.6, color=col, solid_capstyle="round", zorder=3)
        n90 = wilson_n_min(k, target_level / 100, strict=False)
        n85 = wilson_n_min(k, target_sens / 100, strict=False)
        for nx in (n90, n85):
            ax.plot([nx], [wilson(nx - k, nx)[0] * 100], mk, ms=6, color=col, mfc=col if k == 0 else "white",
                    mew=1.2, zorder=5)
        cross[str(k)] = {k90: n90, k85: n85}
        curves[str(k)] = {"n": [int(v) for v in nn], "lower_bound_pct": [round(float(v), 4) for v in lb]}
    handles = [Line2D([], [], color=col, lw=1.6, marker=mk, ms=6, mfc=col if k == 0 else "white", mew=1.2,
                      label="no error" if k == 0 else f"{k} error" + ("s" if k > 1 else ""))
               for k, col, mk in zip(K_LIST, K_RAMP, K_MARK)]
    ax.legend(handles=handles, loc="lower right", fontsize=FS, frameon=False, handlelength=1.6,
              handletextpad=0.5, labelspacing=0.25, borderaxespad=0.15)
    ax.axhline(target_level, color=INK, lw=1.0, ls=(0, (4, 2)), zorder=2)
    ax.axhline(target_sens, color=SOFT, lw=1.0, ls=(0, (4, 2)), zorder=2)
    ax.text(3.35, target_level + 0.6, f"{target_level:.0f} %", fontsize=FS, color=INK, ha="left", va="bottom")
    ax.text(3.35, target_sens - 0.8, f"{target_sens:.0f} %", fontsize=FS, color=INK, ha="left", va="top")
    n90, n85 = cross["0"][k90], cross["0"][k85]
    ax.text(n90 * 0.90, target_level + 0.6, f"{n90}", fontsize=FS, color=INK, ha="right", va="bottom")
    ax.text(n85 * 0.90, target_sens + 0.6, f"{n85}", fontsize=FS, color=INK, ha="right", va="bottom")
    ax.set_xscale("log")
    log_ticks(ax, [3, 10, 30, 100, 300, 1000])
    ax.set_xlim(3, 1000)
    ax.set_ylim(40, 102)
    ax.yaxis.set_major_locator(FixedLocator([40, 50, 60, 70, 80, 90, 100]))
    ax.set_xlabel("transitional test persons, n", fontsize=FS, color=INK)
    ax.set_ylabel("95 % lower bound, %", fontsize=FS, color=INK)
    style(ax)
    return {"curves": curves, "crossings_n": cross, "targets_pct": [target_level, target_sens]}


X0_LOG = 2.0   # where N = 0 sits on the log axes of (b) and (c)


def panel_b(ax, film: dict, carm: dict) -> tuple[dict, list]:
    drawn = {"film": {}, "carm": {}}
    for src in FILM_ORDER:
        lab, col, mk = FILM[src]
        pts = film["corpora"][src]["points"]
        xs = np.array([max(p["N"], X0_LOG) for p in pts])
        ys = np.array([p["acc_mean"] * 100 for p in pts])
        ax.plot(xs, ys, "-", lw=1.3, color=col, zorder=3)
        ax.plot(xs, ys, mk, ms=5, color=col, mfc=col, mew=1.0, zorder=4)
        for p, x in zip(pts, xs):
            if p["seeds"] > 1:
                ax.plot([x, x], [p["acc_min"] * 100, p["acc_max"] * 100], "-", lw=1.2, color=col, zorder=4)
        drawn["film"][src] = {"x_persons": [p["N"] for p in pts], "mean_pct": [round(float(v), 2) for v in ys],
                              "range_pct": [[round(p["acc_min"] * 100, 2), round(p["acc_max"] * 100, 2)] if p["seeds"] > 1 else None
                                            for p in pts],
                              "pointers": [p["pointer"] for p in pts]}
    # the C-arm: own view solid (seed mean where three seeds ran; interval bars omitted for legibility, in the record)
    for tv in ("LAT", "AP"):
        lab, col, mk = VIEW[tv]
        pts = carm["own"][tv]
        xs = np.array([max(p["x"], X0_LOG) for p in pts])
        ys = np.array([p["pct"] for p in pts])
        ax.plot(xs, ys, "-", lw=2.0, color=col, zorder=5)
        ax.plot(xs, ys, mk, ms=6.5, color=col, mfc=col, mew=1.0, zorder=6)
        drawn["carm"][f"own_{tv}"] = {"x_persons": [p["x"] for p in pts], "pct": [p["pct"] for p in pts],
                                      "ci_pct": [p["ci"] for p in pts], "pointers": [p["pointer"] for p in pts]}
    pts = carm["cross_lat_on_ap"]
    xs = np.array([max(p["x"], X0_LOG) for p in pts])
    ys = np.array([p["pct"] for p in pts])
    ax.plot(xs, ys, ls=(0, (3, 1.6)), lw=1.6, color=VIEW["LAT"][1], zorder=4)
    ax.plot(xs, ys, VIEW["LAT"][2], ms=5, color=VIEW["LAT"][1], mfc="white", mew=1.2, zorder=5)
    drawn["carm"]["lat_trained_on_ap"] = {"x_persons": [p["x"] for p in pts], "pct": [p["pct"] for p in pts],
                                          "ci_pct": [p["ci"] for p in pts], "pointers": [p["pointer"] for p in pts]}
    for tv in ("LAT", "AP"):
        p = carm["both"][tv][0]
        ax.plot([p["x"]], [p["pct"]], "x", ms=9, mew=2.2, color=VIEW[tv][1], zorder=7)
        drawn["carm"][f"both_{tv}"] = {"x_persons": p["x"], "pct": p["pct"], "ci_pct": p["ci"], "pointer": p["pointer"]}
    axis_break(ax, 2.75, 3.0)
    ax.set_xscale("log")
    log_ticks(ax, [X0_LOG, 5, 25, 100, 1000, 5000], ["0", "5", "25", "100", "1,000", "5,000"])
    ax.set_xlim(1.7, 6500)
    ax.set_ylim(0, 102)
    ax.yaxis.set_major_locator(FixedLocator([0, 20, 40, 60, 80, 100]))
    ax.set_xlabel("training persons, N", fontsize=FS, color=INK)
    ax.set_ylabel("exact level, %", fontsize=FS, color=INK)
    style(ax)
    handles = [Line2D([], [], color=FILM[s][1], lw=1.3, marker=FILM[s][2], ms=5, label=FILM[s][0]) for s in FILM_ORDER]
    handles += [Line2D([], [], color=VIEW[tv][1], lw=2.0, marker=VIEW[tv][2], ms=6.5, label=f"C-arm, {VIEW[tv][0]}")
                for tv in ("LAT", "AP")]
    handles.append(Line2D([], [], color=VIEW["LAT"][1], lw=1.6, ls=(0, (3, 1.6)), marker="o", ms=5, mfc="white",
                          mew=1.2, label="lateral-trained, read on anteroposterior"))
    handles.append(Line2D([], [], ls="", marker="x", ms=9, mew=2.2, color=INK, label="both views, all persons"))
    return drawn, handles


def panel_c(ax, det: dict) -> tuple[dict, list]:
    drawn = {"both_view_arm": {}, "one_view_arms": {}}
    Ns = sorted(det["curves"])
    xs = np.array([max(n, X0_LOG) for n in Ns])
    for tv in ("LAT", "AP"):
        lab, col, mk = VIEW[tv]
        ys = np.array([det["curves"][n][tv]["pct"] for n in Ns])
        ax.plot(xs, ys, "-", lw=2.0, color=col, zorder=4)
        ax.plot(xs, ys, mk, ms=6.5, color=col, mfc=col, mew=1.0, zorder=5)
        for n, x in zip(Ns, xs):
            ci = det["curves"][n][tv]["ci"]
            ax.plot([x, x], [ci[0], ci[1]], "-", lw=1.1, color=col, zorder=3)
        drawn["both_view_arm"][tv] = {"x_frames": Ns, "pct": [det["curves"][n][tv]["pct"] for n in Ns],
                                      "ci_pct": [det["curves"][n][tv]["ci"] for n in Ns],
                                      "pointers": [det["curves"][n][tv]["pointer"] for n in Ns]}
    for pk, r in sorted(det["one_view"].items()):
        tv = r["trained_on"]
        col = VIEW[tv][1]
        x = r["n_frames"] * (0.90 if tv == "LAT" else 1.11)
        own, oth = r["own"], r["on_other"]
        ax.plot([x, x], [own["ci"][0], own["ci"][1]], "-", lw=1.1, color=col, zorder=5)
        ax.plot([x], [own["pct"]], "^", ms=9, color=col, mfc=col, mew=1.0, zorder=7)
        ax.plot([x, x], [oth["ci"][0], oth["ci"][1]], "-", lw=1.1, color=col, zorder=5)
        ax.plot([x], [oth["pct"]], "v", ms=8, color=col, mfc="white", mew=1.4, zorder=7)
        drawn["one_view_arms"][pk] = {"x_frames": r["n_frames"], "trained_on": tv, "own_pct": own["pct"], "own_ci": own["ci"],
                                      "other_pct": oth["pct"], "other_ci": oth["ci"],
                                      "pointers": [own["pointer"], oth["pointer"]]}
    axis_break(ax, 2.75, 3.0)
    ax.set_xscale("log")
    log_ticks(ax, [X0_LOG, 4, 10, 24, 50, 100, 200], ["0", "4", "10", "24", "50", "100", "200"])
    ax.set_xlim(1.7, 260)
    ax.set_ylim(0, 102)
    ax.yaxis.set_major_locator(FixedLocator([0, 20, 40, 60, 80, 100]))
    ax.set_xlabel("real frames of the device, N", fontsize=FS, color=INK)
    ax.set_ylabel("vertebra recall, %", fontsize=FS, color=INK)
    style(ax)
    handles = [Line2D([], [], color=VIEW[tv][1], lw=2.0, marker=VIEW[tv][2], ms=6.5,
                      label=f"both views, read on {VIEW[tv][0]}") for tv in ("LAT", "AP")]
    handles += [Line2D([], [], ls="", marker="^", ms=9, color=INK, mfc=INK, label="one view, read on it"),
                Line2D([], [], ls="", marker="v", ms=8, color=INK, mfc="white", mew=1.4, label="one view, read on the other")]
    return drawn, handles


def panel_d(ax, ang: dict) -> tuple[dict, list]:
    drawn = {}
    for arm, lab, col, mk in ARMS_D:
        a = ang["arms"][arm]
        lats = np.array(a["lats"])
        mean = np.array(a["seed_mean_pct"])
        lo, hi = np.array(a["seed_range_pct"][0]), np.array(a["seed_range_pct"][1])
        ax.fill_between(lats, lo, hi, color=col, alpha=0.18, lw=0, zorder=2)
        ax.plot(lats, mean, "-", lw=1.8, color=col, zorder=4)
        ax.plot(lats, mean, mk, ms=5, color=col, mfc=col, mew=1.0, zorder=5)
        drawn[arm] = {"lats": a["lats"], "seed_mean_pct": a["seed_mean_pct"], "seed_range_pct": a["seed_range_pct"],
                      "trained_bins_mean_pct": a["trained_bins_mean_pct"],
                      "untrained_bins_mean_pct": a["untrained_bins_mean_pct"],
                      "pointers": [s["pointer"] for s in a["seeds"].values()]}
    for l in TRAINED_LATS:
        ax.axvline(l, color=SOFT, lw=1.0, ls=(0, (2, 2)), zorder=1)
    ax.set_xlim(-95, 95)
    ax.set_ylim(0, 102)
    ax.xaxis.set_major_locator(FixedLocator([-90, -45, 0, 45, 90]))
    ax.xaxis.set_major_formatter(FixedFormatter(["−90°", "−45°", "0°", "45°", "90°"]))
    ax.yaxis.set_major_locator(FixedLocator([0, 20, 40, 60, 80, 100]))
    ax.set_xlabel("lateral angle of the render", fontsize=FS, color=INK)
    ax.set_ylabel("vertebra recall, %", fontsize=FS, color=INK)
    style(ax)
    handles = [Line2D([], [], color=col, lw=1.8, marker=mk, ms=5, label=lab) for _a, lab, col, mk in ARMS_D]
    return drawn, handles


# ---------------------------------------------------------------------------------------------------------------
def audit_pdf(pdf: Path) -> dict:
    import fitz
    doc = fitz.open(pdf)
    sizes, fonts, spans = [], set(), 0
    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    if not s["text"].strip():
                        continue
                    spans += 1
                    sizes.append(s["size"])
                    fonts.add(s["font"])
    w_in = doc[0].rect.width / 72.0
    h_in = doc[0].rect.height / 72.0
    small = min(sizes) if sizes else None
    ok = small is not None and small >= 11.95 and all("Arial" in f for f in fonts) and abs(w_in - W_IN) < 0.01
    return {"spans": spans, "smallest_pt": round(small, 2) if small else None, "fonts": sorted(fonts),
            "page_in": [round(w_in, 3), round(h_in, 3)], "pass": ok}


CAPTION = ("Persons, views, angles. (a) Wilson 95 % lower bound by errors against transitional test persons; lines, "
           "targets. (b) Naming against training persons: film corpora and one C-arm by view (dashed, lateral-trained "
           "read on anteroposterior; x, both views). (c) Same-device detection against real frames; triangles, "
           "one-view arms (open, other view). (d) Render-only detectors at matched N against lateral angle.")


def caption_tex(cap: str) -> str:
    """The legend as main.tex carries it: '95 %' -> '95\\,\\%'."""
    return cap.replace(" %", "\\,\\%")


def main() -> int:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial"]
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["axes.unicode_minus"] = True

    pt = load_json(POWER_TABLE)
    target_level = float(pt["targets_pct"]["exact_level_lower_bound"])       # 90
    target_sens = float(pt["targets_pct"]["variant_sensitivity_lower_bound"])  # 85
    checks = run_checks(pt)
    pooled = load_json(POOLED)
    assert pooled["experiment_status"] == "scored" and str(pooled["arm_conf"]) == str(ARM_CONF), (
        pooled["experiment_status"], pooled["arm_conf"])
    film = load_film(pooled)
    carm = load_carm_naming()
    det = load_detection()
    ang = load_angle(pooled)

    # ---- layout, inches -----------------------------------------------------------------------------------------
    fig = plt.figure(figsize=(W_IN, H_IN))

    def ax_in(x, y, w, h):
        return fig.add_axes([x / W_IN, y / H_IN, w / W_IN, h / H_IN])

    top_y, top_h = 6.40, 2.55
    bot_y, bot_h = 1.70, 2.55
    ax_a = ax_in(0.84, top_y, 2.42, top_h)
    ax_b = ax_in(4.28, top_y, 2.52, top_h)
    ax_c = ax_in(0.84, bot_y, 2.42, bot_h)
    ax_d = ax_in(4.28, bot_y, 2.52, bot_h)

    ra = panel_a(ax_a, target_level, target_sens)
    rb, hb = panel_b(ax_b, film, carm)
    rc, hc = panel_c(ax_c, det)
    rd, hd = panel_d(ax_d, ang)
    fig.legend(handles=hb, loc="lower left", bbox_to_anchor=(0.30 / W_IN, 5.02 / H_IN), ncol=2, fontsize=FS,
               frameon=False, handlelength=1.8, handletextpad=0.5, labelspacing=0.2, columnspacing=1.2,
               borderaxespad=0.0)
    fig.legend(handles=hc, loc="lower left", bbox_to_anchor=(0.15 / W_IN, 0.22 / H_IN), ncol=1, fontsize=FS,
               frameon=False, handlelength=1.8, handletextpad=0.5, labelspacing=0.2, borderaxespad=0.0)
    fig.legend(handles=hd, loc="lower left", bbox_to_anchor=(3.62 / W_IN, 0.22 / H_IN), ncol=1, fontsize=FS,
               frameon=False, handlelength=1.8, handletextpad=0.5, labelspacing=0.2, borderaxespad=0.0)

    for letter, (x, y) in (("a", (0.02, top_y + top_h + 0.30)), ("b", (3.55, top_y + top_h + 0.30)),
                           ("c", (0.02, bot_y + bot_h + 0.32)), ("d", (3.55, bot_y + bot_h + 0.32))):
        fig.text(x / W_IN, y / H_IN, letter, fontsize=FS_LETTER, fontweight="bold", color="black", ha="left", va="top")

    FIG.mkdir(parents=True, exist_ok=True)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    pdf, png, tif = FIG / "figure5.pdf", FIG / "figure5.png", FIG / "figure5.tif"
    fig.savefig(pdf)
    fig.savefig(png, dpi=300)
    fig.savefig(tif, dpi=1200, pil_kwargs={"compression": "tiff_lzw"})
    plt.close(fig)
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(tif)
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bg.paste(im, mask=im.split()[3] if im.mode == "RGBA" else None)
    bg.save(tif, compression="tiff_lzw", dpi=(1200, 1200))
    tif_px = list(bg.size)
    png_px = list(Image.open(png).size)
    audit = audit_pdf(pdf)
    if not audit["pass"]:
        raise SystemExit(f"figure5.pdf fails the text audit: {audit}")

    n_words = len(CAPTION.split())
    if n_words > 60:
        raise SystemExit(f"caption is {n_words} words, over 60")
    (FIG / "figure5.caption.txt").write_text(CAPTION + "\n", encoding="utf-8")

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    s074, strn = load_json(SENS_074)["comparison"], load_json(SENS_TRAINED)["comparison"]
    sens = {"conf_0.74": {"delta_aicc_M0_minus_M1": s074["delta_aicc_M0_minus_M1"], "lr_p": s074["lr_p"],
                          "g_pp": s074["g"]["per_unit_H_in_pp"], "g_ci95_pp": [v * 100 for v in s074["g"]["ci95"]],
                          "file": rel(SENS_074)},
            "trained_only": {"delta_aicc_M0_minus_M1": strn["delta_aicc_M0_minus_M1"], "lr_p": strn["lr_p"],
                             "g_pp": strn["g"]["per_unit_H_in_pp"], "g_ci95_pp": [v * 100 for v in strn["g"]["ci95"]],
                             "file": rel(SENS_TRAINED)}}
    k90, k85 = f"n_lower_bound_ge_{target_level:.0f}", f"n_lower_bound_ge_{target_sens:.0f}"
    arms_d = ang["arms"]
    power_json = {
        "what": "Figure 5: (a) Wilson 95 % score interval (z = 1.959964), 'meets the bound' = lower bound >= target "
                "(inclusive), against transitional test PERSONS; (b) naming against training persons on plain film and "
                "on one C-arm per view protocol; (c) same-device detection against real frames, both-view arm and "
                "one-view arms; (d) the matched-N coverage arms read along the lateral angle on the unseen render sweep. "
                "The pooled nested fit (M0 vs M1) is no longer drawn; its comparison numbers are under 'pooled_fit'.",
        "generated": now,
        "tool": rel(Path(__file__)),
        "pre_stated_targets_pct": {"exact_level_lower_bound": target_level,
                                   "variant_sensitivity_lower_bound": target_sens,
                                   "source": rel(POWER_TABLE) + "#targets_pct (docs/FLAGSHIP_PLAN.md G6 item 4)"},
        "n_needed_zero_errors": {"G6_level_wilson_90": ra["crossings_n"]["0"][k90],
                                 "G6_sensitivity_wilson_85": ra["crossings_n"]["0"][k85]},
        "unit_of_evidence": "persons (independent spines) in (a); training persons in (b), C-ArmLSpine cases counted as "
                            "persons; real training frames of the device in (c), scored on the 28 test cases; training "
                            "renders at matched N in (d), scored on 40 unseen subjects' renders per angle bin",
        "panel_a": ra,
        "panel_b_film": {"inputs": film["tag"] | {"generated": film["generated"], "tool": film["tool"]},
                         "corpora": film["corpora"], "drawn": rb["film"],
                         "transfer_note": "the seed-0 cross-corpus transfer of each cell is kept per point "
                                          "(corpora.<src>.points[].cross_seed0) and is quoted in the text; it is no "
                                          "longer drawn"},
        "panel_b_carm": {"inputs": carm["tag"] | {"generated": carm["generated"]}, "design": carm["design"],
                         "own": carm["own"], "cross_lat_on_ap": carm["cross_lat_on_ap"],
                         "cross_ap_on_lat_not_drawn": carm["cross_ap_on_lat"], "both": carm["both"],
                         "zeroshot_not_drawn": carm["zeroshot"], "drawn": rb["carm"],
                         "interval_rule": "case-clustered percentile bootstrap, 2,000 resamples, in name_fill.json; "
                                          "the per-point intervals are in the record and are not drawn"},
        "panel_c_detection": {"inputs": det["tag"] | {"generated": det["generated"]}, "design": det["design"],
                              "convention": DET_CONV, "conf": DET_CONF, "curves": det["curves"], "one_view": det["one_view"],
                              "summary": det["summary"], "drawn": rc, "caveats": det["caveats"],
                              "interval_rule": "case-clustered percentile bootstrap over the 28 test patients, seeds "
                                               "summed within a patient, 2,000 resamples (det_fill.json)"},
        "panel_d_angle": {k: ang[k] for k in ("n_subjects", "n_bins", "n_trained_bins", "n_untrained_bins", "trained_lats",
                                              "conf", "tilt", "card", "rule", "exposure_caveat")}
                         | {"arms": arms_d, "drawn": rd,
                            "summary": {arm: {"trained_bins_mean_pct": arms_d[arm]["trained_bins_mean_pct"],
                                              "untrained_bins_mean_pct": arms_d[arm]["untrained_bins_mean_pct"],
                                              "per_seed_trained_bins_mean_pct": arms_d[arm]["per_seed_trained_bins_mean_pct"],
                                              "per_seed_untrained_bins_mean_pct": arms_d[arm]["per_seed_untrained_bins_mean_pct"],
                                              "all_bins_mean_pct": arms_d[arm]["all_bins_mean_pct"],
                                              "pooled_unseen_recall_pct_per_seed": arms_d[arm]["pooled_unseen_recall_pct_per_seed"],
                                              "N_train": arms_d[arm]["seeds"][0]["N_train"],
                                              "subjects_train": arms_d[arm]["seeds"][0]["subjects_train"]}
                                        for arm in arms_d}},
        "pooled_fit": {"inputs": file_tag(POOLED) | {"generated": pooled["generated"], "tool": pooled["tool"]},
                       "M0": {k: pooled["M0"][k] for k in ("model", "k_params", "weighted_rss", "aicc", "rmse_pp", "exponent_C")},
                       "M1": {k: pooled["M1"][k] for k in ("model", "k_params", "weighted_rss", "aicc", "rmse_pp", "exponent_C")},
                       "comparison": pooled["comparison"], "verdict": pooled["verdict"],
                       "g_identified_by": pooled["g_identified_by"], "admissibility": pooled["admissibility"],
                       "sensitivities": sens, "n_points": len(pooled["points"]),
                       "note": "not drawn since the 2026-09-25 afternoon build; quoted in Results"},
        "independent_check": checks,
    }
    (OUTDIR / "power.json").write_text(json.dumps(power_json, indent=1), encoding="utf-8")

    # ---- the record: every number on the figure and its file ----------------------------------------------------
    numbers = []
    for k, v in ra["crossings_n"].items():
        numbers.append({"panel": "a", "quantity": f"n at which {k} errors put the Wilson lower bound on the targets",
                        "value": v, "source": "computed here (results/power/power.json#panel_a); 22 and 35 equal "
                                              "results/stats_review/recompute.json#R4_wilson/min_n_zero_errors"})
    numbers.append({"panel": "a", "quantity": "target lines, %", "value": [target_level, target_sens],
                    "source": rel(POWER_TABLE) + "#targets_pct"})
    for src, d in rb["film"].items():
        numbers.append({"panel": "b", "quantity": f"{FILM[src][0]}: seed-mean accuracy (%) at N persons, per-seed range",
                        "value": d, "source": d["pointers"]})
    for k, d in rb["carm"].items():
        numbers.append({"panel": "b", "quantity": f"C-ArmLSpine naming, whole frame, {k}: accuracy (%) at N persons with "
                                                  "case-clustered 95 % intervals",
                        "value": d, "source": d["pointers"] if "pointers" in d else d["pointer"]})
    for tv, d in rc["both_view_arm"].items():
        numbers.append({"panel": "c", "quantity": f"both-view arm read on {tv}: recall (%) at N real frames, 95 % intervals",
                        "value": d, "source": d["pointers"]})
    for pk, d in rc["one_view_arms"].items():
        numbers.append({"panel": "c", "quantity": f"one-view arm {pk}: recall (%) on the trained protocol and on the other",
                        "value": d, "source": d["pointers"]})
    numbers.append({"panel": "c", "quantity": "one-view arms: min and max on own / other protocol (quoted in Results)",
                    "value": det["summary"], "source": rel(OUTDIR / "power.json") + "#/panel_c_detection/summary"})
    for arm, d in rd.items():
        numbers.append({"panel": "d", "quantity": f"{arm} arm: seed-mean recall (%) per lateral angle, per-seed range, "
                                                  "means over trained and untrained bins",
                        "value": d, "source": d["pointers"]})
    fc = film["corpora"]
    own = carm["own"]
    record = {
        "figure": "figure5",
        "title": "Persons, views and angles: what accuracy follows in acquisition space",
        "generated": now,
        "tool": rel(Path(__file__)),
        "outputs": {"pdf": rel(pdf), "tif": rel(tif), "tif_px": tif_px, "tif_dpi": 1200, "png": rel(png), "png_px": png_px,
                    "png_dpi": 300, "caption": rel(FIG / "figure5.caption.txt"), "numbers": rel(OUTDIR / "power.json")},
        "caption": CAPTION, "caption_tex": caption_tex(CAPTION), "caption_words": n_words,
        "text_audit": audit,
        "palette": {"blue": C_BLUE, "green": C_GREEN, "vermillion": C_VERM, "ink": INK, "grey": SOFT,
                    "validation": "dataviz six checks (Python twin of scripts/validate_palette.js, light surface, "
                                  "all pairs) 2026-09-25: blue/green/vermillion PASS (worst CVD dE 11.0 deutan; "
                                  "worst normal-vision dE 18.7; contrast >= 3:1); ink and grey are neutrals with "
                                  "their own marker shape (in b and c: lateral = ink circle, anteroposterior = grey "
                                  "square)"},
        "components": {
            "a": "Wilson 95 % lower bound vs n for k = 0, 1, 2, 5 errors; dashed lines at the pre-stated 90 % "
                 "(exact level) and 85 % (variant sensitivity) targets; markers where each k clears each line; the "
                 f"k = 0 crossings labelled ({ra['crossings_n']['0'][k90]}, {ra['crossings_n']['0'][k85]}).",
            "b": "Naming against training persons on one log axis (N = 0 at x = 2 left of a break). Film: exact-level "
                 "naming on the v9 VAL films of the corpus against N training persons, render-only encoder fine-tuned "
                 "per cell, seed mean with bars over the per-seed range (three seeds at N <= 25). C-arm: the v9 "
                 "encoder and head fine-tuned per case-grouped fold on N C-ArmLSpine persons of one protocol and read "
                 "on that protocol (lateral ink, anteroposterior grey, solid); the lateral-trained cells read on the "
                 "anteroposterior test frames (ink dashed, open); the both-protocol cells at all persons (x). Reading: "
                 "separated by view, each C-arm curve rises like film; the view not trained on stays where it was; "
                 "training both views costs neither.",
            "c": "Same-device detection: vertebra recall (body boxes, confidence 0.74) on the 28 C-ArmLSpine test "
                 "cases against N real frames of the device added to a fixed background, both views of N/2 patients, "
                 "read on the lateral (ink) and anteroposterior (grey) test frames with case-clustered intervals; "
                 "one-view arms of 25 and 50 frames of one protocol read on it (filled triangles) and on the other "
                 "(open triangles), two seeds pooled. Reading: the plateau from 24 frames is the same pooled or "
                 "separated; frames of one view buy that view and not the other.",
            "d": "Render-only detectors of the Surgio-B51 card at matched N (2,646 renders of 125 subjects) whose "
                 "training poses are the real anteroposterior-lateral pool (vermillion), an arc (blue) or the real "
                 "pool doubled (green), read at confidence 0.25 on 40 unseen subjects' renders per lateral angle "
                 "(tilt 0); seed mean, per-seed range shaded; dotted verticals at the three trained angles. Reading: "
                 "accuracy sits where the training poses sit; doubling the same poses raises those bins and not the "
                 "gaps; the same N spread over the arc holds at every angle.",
        },
        "numbers_on_figure": numbers,
        "discrepancies_stated": [
            "Panel (b) mixes evaluation sets: film cells are scored on the corpus's fixed VAL films (persons never in "
            "any cell's training), C-arm cells on five case-grouped test folds pooled (148 lateral / 149 "
            "anteroposterior cases; 623 / 633 vertebrae); a C-ArmLSpine case is an acquisition session, counted as a "
            "person. The C-arm N = 0 cell is the fine-tune recipe with no C-arm crop; the zero-shot run (no C-arm "
            f"image at all: lateral {carm['zeroshot']['LAT'][0]['pct']:.1f} %, anteroposterior "
            f"{carm['zeroshot']['AP'][0]['pct']:.1f} %) is in power.json and not drawn.",
            "Panel (b) draws no C-arm interval (the per-point case-clustered intervals are in power.json and the "
            "record; at N <= 25 three seeds are averaged, above one seed). The anteroposterior-trained cells read on "
            "the lateral test frames (93.4-95.3 %, not drawn) sit on the lateral own-view curve.",
            "Panel (c): under the body rule the N = 0 floor (lateral 0.2 %, anteroposterior 15.2 %) is a "
            "box-convention artefact (det_fill.json 'reading'): arms without C-ArmLSpine frames draw whole-vertebra "
            "boxes, which the body rule scores as misses; the convention-free centre rule reads 70.5 % at N = 0. The "
            "curve from N = 4 upward is unaffected in shape.",
            "Panel (c): the one-view arms at 25 frames use the same patients as the both-view arm at 50 frames and the "
            "same frame count as the both-view arm at 24; at 50 frames, the patients of the both-view 100 and the "
            "frame count of the both-view 50. Paired contrasts against both are in det_fill.json#contrasts.",
            "Panel (d): the Surgio card renders thick laterals photon-starved (recall_vs_angle.md), so the +-90 degree "
            "bins conflate geometry with synthetic underexposure; the +-30 to 60 degree bins carry the comparison. "
            "Every subject is placed on one anchor, so another subject's truth boxes already score about 0.64-0.68 "
            "at every angle (supplement); the bins are read against that floor, not zero.",
            "Panel (d) is renders at confidence 0.25 (the operating point every arm evaluator reports at), not the "
            "manuscript's detectors at 0.74; every render-only arm scores under 15 % on any real test set. The "
            "six Elekta XVI arms did not train (val mAP50 0.13-0.22) and are not drawn.",
            f"The pooled nested fit (delta AICc {pooled['comparison']['delta_aicc_M0_minus_M1']:.1f}, g "
            f"{pooled['comparison']['g']['per_unit_H_in_pp']:+.1f} points per unit H*; at confidence 0.74 g "
            f"{sens['conf_0.74']['g_pp']:+.1f}, delta AICc {sens['conf_0.74']['delta_aicc_M0_minus_M1']:+.1f}; "
            f"trained-only g {sens['trained_only']['g_pp']:+.1f}) is quoted in Results and no longer drawn; g is "
            "identified by the Surgio arms alone.",
            "Film asymptotes: NHANES II and BUU-LSPINE are still rising at N = all (3.2 and 3.1 points below their "
            "fitted asymptotes); only CSXA plateaus (within 2 points from N = 200). The film cross-corpus transfer "
            "(dashed in the 10:26 build) is quoted in Results and no longer drawn.",
        ],
        "reading": (
            f"At zero errors, {ra['crossings_n']['0'][k90]} transitional persons put the Wilson lower bound at 90 % "
            f"and {ra['crossings_n']['0'][k85]} at 85 %. Film: NHANES II {fc['nhanes']['points'][1]['acc_mean'] * 100:.1f} % "
            f"at N = 5 and {fc['nhanes']['points'][-1]['acc_mean'] * 100:.1f} % at all {fc['nhanes']['N_all_persons']}; "
            f"BUU-LSPINE {fc['buu_full']['points'][1]['acc_mean'] * 100:.1f} -> {fc['buu_full']['points'][-1]['acc_mean'] * 100:.1f} % "
            f"({fc['buu_full']['N_all_persons']}); CSXA {fc['csxa']['points'][1]['acc_mean'] * 100:.1f} -> "
            f"{fc['csxa']['points'][-1]['acc_mean'] * 100:.1f} % ({fc['csxa']['N_all_persons']}). C-arm naming: lateral "
            f"{own['LAT'][0]['pct']:.1f} % at N = 0 -> {own['LAT'][-2]['pct']:.1f} % at 50; anteroposterior "
            f"{own['AP'][0]['pct']:.1f} -> {own['AP'][1]['pct']:.1f} % at 5 -> {own['AP'][-1]['pct']:.1f} % at all; "
            f"lateral-trained on anteroposterior {carm['cross_lat_on_ap'][-1]['pct']:.1f} % at all; both views "
            f"{carm['both']['LAT'][0]['pct']:.1f} / {carm['both']['AP'][0]['pct']:.1f} %. Detection (body, 0.74): "
            f"both-view arm lateral {det['curves'][24]['LAT']['pct']:.1f} / anteroposterior {det['curves'][24]['AP']['pct']:.1f} % "
            f"at 24 frames, {det['curves'][200]['LAT']['pct']:.1f} / {det['curves'][200]['AP']['pct']:.1f} % at 200; "
            f"one-view arms {det['summary']['oneview_own_min_pct']:.1f}-{det['summary']['oneview_own_max_pct']:.1f} % on "
            f"their own view, {det['summary']['oneview_other_min_pct']:.1f}-{det['summary']['oneview_other_max_pct']:.1f} % "
            f"on the other. Angle (renders, 0.25): low arm {arms_d['low']['trained_bins_mean_pct']:.1f} % at the trained "
            f"angles and {arms_d['low']['untrained_bins_mean_pct']:.1f} % over the 16 others; 2N "
            f"{arms_d['low2n']['trained_bins_mean_pct']:.1f} / {arms_d['low2n']['untrained_bins_mean_pct']:.1f} %; arc "
            f"{arms_d['high']['trained_bins_mean_pct']:.1f} / {arms_d['high']['untrained_bins_mean_pct']:.1f} %."),
    }
    (FIG / "figure5.record.json").write_text(json.dumps(record, indent=1), encoding="utf-8")

    print(f"wrote {rel(pdf)}, .tif {tif_px} px, .png {png_px} px, caption ({n_words} words), "
          f"{rel(OUTDIR / 'power.json')}, figure5.record.json")
    print(f"text audit: {audit}")
    print("checks:", checks["verdict"])
    print("panel a crossings:", ra["crossings_n"])
    print("caption tex:", record["caption_tex"])
    print(record["reading"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
