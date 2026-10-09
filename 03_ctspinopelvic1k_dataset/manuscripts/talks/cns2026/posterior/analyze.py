#!/usr/bin/env python
"""Posterior figure, step 3: per-voxel softmax of the released model against the ground truth.

For every held-out record with a prediction:
  * reproduction first: per-class Dice and the junction Dice exactly as spinopelvic-seg tools/eval_full.py defines
    them (ignore label 9 masked; junction = 40 mm slab along the IS axis centred between the mean IS positions of
    GT last_lumbar and GT sacrum; mean Dice over L4 / last_lumbar / sacrum present in the slab). The paper reports,
    for the five-fold ensemble, junction 0.950 on the scorable lumbarization record and sacrum 0.970 over the
    held-out records with a sacral mask; those are the checks.
  * orientation check: argmax of the saved probabilities must equal nnU-Net's saved segmentation.
  * junction window: for GT background / L4 / last_lumbar / sacrum voxels, histograms of the posterior of each of
    those classes (50 bins on [0, 1]) and the summed posterior mass (a soft confusion matrix).
  * sacrum: posterior of sacrum on GT-sacrum voxels, and on the non-sacrum voxels of a 3-voxel shell around it.
  * example slices (sagittal, through the junction) for the scorable lumbarization record and for the normal
    record whose junction Dice is the median of the normals.
"""
import argparse
import csv
import json
import os
import pickle
from concurrent.futures import ProcessPoolExecutor

import nibabel as nib
import numpy as np
from scipy import ndimage

IGN, BG, L4, LL, SAC = 9, 0, 4, 5, 6
NAMES = {0: "background", 1: "L1", 2: "L2", 3: "L3", 4: "L4", 5: "last_lumbar", 6: "sacrum", 7: "left_hip", 8: "right_hip"}
JX = [BG, L4, LL, SAC]
BINS = np.linspace(0, 1, 51)


def is_axis(aff):
    ax = nib.aff2axcodes(aff)
    i = next((k for k, c in enumerate(ax) if c in ("I", "S")), 2)
    return i, float(np.linalg.norm(aff[:3, i]))


def dice(p, g, c):
    gm, pm = g == c, p == c
    n = gm.sum()
    if n == 0:
        return None
    return 2.0 * (gm & pm).sum() / (n + pm.sum())


def window(gt, aff):
    ax, sp = is_axis(aff)
    if not (gt == LL).any() or not (gt == SAC).any():
        return None
    other = tuple(i for i in range(3) if i != ax)
    j = (np.where((gt == LL).any(axis=other))[0].mean() + np.where((gt == SAC).any(axis=other))[0].mean()) / 2
    h = max(1, int(round(20.0 / sp)))
    lo, hi = max(0, int(round(j - h))), min(gt.shape[ax], int(round(j + h)) + 1)
    if hi <= lo:
        return None
    sl = [slice(None)] * 3
    sl[ax] = slice(lo, hi)
    return tuple(sl), ax, int(round(j))


def one(args):
    case, pred_dir, lab_dir, ct_path, want_slice = args
    g_img = nib.load(os.path.join(lab_dir, case + ".nii.gz"))
    gt = np.asarray(g_img.dataobj).astype(np.int16)
    p_img = nib.load(os.path.join(pred_dir, case + ".nii.gz"))
    pred = np.asarray(p_img.dataobj).astype(np.int16)
    assert gt.shape == pred.shape and np.allclose(g_img.affine, p_img.affine, atol=1e-3), case
    prob = np.load(os.path.join(pred_dir, case + ".npz"))["probabilities"]
    # nnU-Net stores (C, z, y, x) in SimpleITK order; nibabel arrays are (x, y, z)
    prob = np.transpose(prob, (0, 3, 2, 1))
    assert prob.shape[1:] == gt.shape, (case, prob.shape, gt.shape)
    am = np.argmax(prob, 0)
    agree = float((am == pred).mean())
    out = {"case": case, "argmax_agrees": agree, "dtype": str(prob.dtype)}
    valid = gt != IGN
    pv, gv = pred[valid], gt[valid]
    for c in range(1, 9):
        d = dice(pv, gv, c)
        out["dice_" + NAMES[c]] = None if d is None else float(d)
    res = {"row": out}

    w = window(gt, g_img.affine)
    if w is not None:
        sl, ax, jidx = w
        gw, pw = gt[sl], pred[sl]
        m = gw != IGN
        ds = [dice(pw[m], gw[m], c) for c in (L4, LL, SAC)]
        ds = [d for d in ds if d is not None]
        out["junction_dsc"] = float(np.mean(ds)) if ds else None
        prw = prob[(slice(None),) + sl]
        hist, mass, count = {}, {}, {}
        for gc in JX:
            sel = (gw == gc) & m
            n = int(sel.sum())
            count[gc] = n
            if n == 0:
                continue
            for pc in JX:
                v = prw[pc][sel].astype(np.float32)
                hist[(gc, pc)] = np.histogram(v, BINS)[0]
                mass[(gc, pc)] = float(v.sum())
            mass[(gc, "other")] = float(n - sum(mass[(gc, pc)] for pc in JX))
        res["jx"] = {"hist": hist, "mass": mass, "count": count}
        if want_slice:
            # sagittal = fix the left-right axis, read from the label's own affine (these volumes are P,I,R)
            codes = nib.aff2axcodes(g_img.affine)
            lr = next(k for k, c in enumerate(codes) if c in ("L", "R"))
            sag = int(np.median(np.where(gt == LL)[lr]))
            ct = np.asarray(nib.load(ct_path).dataobj)
            tk = lambda v: np.take(v, sag, axis=lr)
            crop = {"ct": tk(ct), "gt": tk(gt), "pred": tk(pred),
                    "p_L4": tk(prob[L4]), "p_LL": tk(prob[LL]), "p_sac": tk(prob[SAC]), "p_bg": tk(prob[BG]),
                    "is_axis": ax, "lr_axis": lr, "junction_idx": jidx, "sag_index": sag,
                    "spacing": np.array(g_img.header.get_zooms()[:3]), "axcodes": "".join(nib.aff2axcodes(g_img.affine))}
            res["slice"] = crop
    else:
        out["junction_dsc"] = None

    if (gt == SAC).any():
        sac = gt == SAC
        bb = ndimage.find_objects(sac.astype(np.int8))[0]
        bb = tuple(slice(max(0, s.start - 6), s.stop + 6) for s in bb)
        s_in = sac[bb]
        shell = ndimage.binary_dilation(s_in, iterations=3) & ~s_in & (gt[bb] != IGN)
        ps = prob[SAC][bb].astype(np.float32)
        res["sac"] = {"in": np.histogram(ps[s_in], BINS)[0], "shell": np.histogram(ps[shell], BINS)[0],
                      "n_in": int(s_in.sum()), "n_shell": int(shell.sum()),
                      "in_mass_to": {NAMES[c]: float(prob[c][bb][s_in].astype(np.float64).sum()) for c in range(9)}}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred", required=True)
    ap.add_argument("--labels", required=True)
    ap.add_argument("--images", required=True, help="imagesTs folder of symlinks (resolved via --ctdir)")
    ap.add_argument("--ctdir", required=True)
    ap.add_argument("--lstv", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    sub = json.load(open(a.lstv))["case_to_subtype"]
    cases = sorted(f[:-7] for f in os.listdir(a.pred) if f.endswith(".nii.gz") and os.path.exists(os.path.join(a.pred, f[:-7] + ".npz")))
    ctp = {c: os.path.join(a.ctdir, os.path.basename(os.readlink(os.path.join(a.images, c + "_0000.nii.gz")))) for c in cases}
    slice_cases = {c for c in cases if sub.get(c) == "lumb"}
    jobs = [(c, a.pred, a.labels, ctp[c], c in slice_cases) for c in cases]
    rows, JH, JM, JC, SH, SI = [], {}, {}, {}, {}, {}
    slices = {}
    with ProcessPoolExecutor(a.workers) as ex:
        for r in ex.map(one, jobs):
            row = r["row"]
            st = sub.get(row["case"], "normal")
            row["subtype"] = st
            rows.append(row)
            if "jx" in r:
                for k, v in r["jx"]["hist"].items():
                    JH.setdefault(st, {}).setdefault(k, np.zeros(50, np.int64))
                    JH[st][k] += v
                for k, v in r["jx"]["mass"].items():
                    JM.setdefault(st, {}).setdefault(k, 0.0)
                    JM[st][k] += v
                for k, v in r["jx"]["count"].items():
                    JC.setdefault(st, {}).setdefault(k, 0)
                    JC[st][k] += v
            if "sac" in r:
                grp = "all"
                SH.setdefault(grp, {"in": np.zeros(50, np.int64), "shell": np.zeros(50, np.int64)})
                SH[grp]["in"] += r["sac"]["in"]
                SH[grp]["shell"] += r["sac"]["shell"]
                SI[row["case"]] = r["sac"]["in_mass_to"]
            if "slice" in r:
                slices[row["case"]] = r["slice"]
            print(row["case"], st, "argmax=%.5f" % row["argmax_agrees"], "jx=%s" % row.get("junction_dsc"), "sac=%s" % row.get("dice_sacrum"), flush=True)

    # normal example: the fused normal record whose junction Dice is the median of the normals, re-run for its slice
    nj = sorted((r["junction_dsc"], r["case"]) for r in rows if r["subtype"] == "normal" and r.get("junction_dsc") is not None)
    if nj:
        med = nj[len(nj) // 2][1]
        slices[med] = one((med, a.pred, a.labels, ctp[med], True))["slice"]

    keys = sorted({k for r in rows for k in r})
    with open(os.path.join(a.out, "per_case.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)

    def mean(xs):
        xs = [x for x in xs if x is not None]
        return (float(np.mean(xs)), len(xs)) if xs else (None, 0)

    summ = {"n_cases": len(rows), "min_argmax_agreement": float(min(r["argmax_agrees"] for r in rows)),
            "prob_dtype": rows[0]["dtype"] if rows else None,
            "reproduction": {
                "sacrum_dice_all": mean([r.get("dice_sacrum") for r in rows]),
                "junction_lumb": [(r["case"], r["junction_dsc"]) for r in rows if r["subtype"] == "lumb" and r.get("junction_dsc") is not None],
                "junction_normal": mean([r.get("junction_dsc") for r in rows if r["subtype"] == "normal"]),
                "paper": {"sacrum_ensemble": 0.970, "sacrum_n": 113, "junction_lumb_ensemble": 0.950, "junction_normal_5fold_mean": 0.907, "junction_normal_n": 50}},
            "junction_mass": {st: {f"{NAMES[g]}->{NAMES[p] if isinstance(p, int) else p}": v for (g, p), v in d.items()} for st, d in JM.items()},
            "junction_counts": {st: {NAMES[g]: n for g, n in d.items()} for st, d in JC.items()},
            "sacrum_in_mass_to_by_case": SI}
    json.dump(summ, open(os.path.join(a.out, "summary.json"), "w"), indent=1)
    np.savez_compressed(os.path.join(a.out, "hist.npz"), bins=BINS,
                        **{f"jx|{st}|{g}|{p}": v for st, d in JH.items() for (g, p), v in d.items()},
                        **{f"sac|{grp}|{k}": v for grp, d in SH.items() for k, v in d.items()})
    with open(os.path.join(a.out, "slices.pkl"), "wb") as fh:
        pickle.dump(slices, fh)
    print(json.dumps(summ["reproduction"], indent=1))
    print("min argmax agreement", summ["min_argmax_agreement"])


if __name__ == "__main__":
    main()
