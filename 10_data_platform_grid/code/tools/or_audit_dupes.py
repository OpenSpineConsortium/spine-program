#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/or_audit_dupes.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Leakage and independence audit, part 2: near-duplicate images across splits and across corpora.

Similarity = zero-mean, unit-norm correlation of the 32x32 box-downsampled grey image (NCC32). It is coarse on
purpose: it finds the same frame twice (a re-export, a mirrored copy is NOT found, a figure reproduction is),
and it also fires on two different patients photographed the same way, so every flagged pair is classed
same-case / cross-case and the top cross-case pairs are drawn to a contact sheet for the eye. Pairs above the
threshold are re-scored at 64x64 (NCC64), which separates "same picture" from "same kind of picture" better.

Within each realxray dataset: every train+val frame against every test frame, and train against val.
Across corpora: every realxray frame (all splits) against the film detector's corpus (yolo_v3 + yolo_v4z, the
data.yaml chain of v5z), the FluoroCap literature panels (in the zero-shot level bank via fluorocap_fov96_ctx)
and yolo_v6f (FluoroCap-derived film-detector fine-tune set).

    python tools/or_audit_dupes.py --out <audit dir> --workers 32
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
from collections import Counter
from multiprocessing import Pool

import numpy as np
from PIL import Image

H = os.path.expanduser("~")
R = "/rs/rs_grp_oschome/go2432/data/realxray"
EXTS = (".png", ".jpg", ".jpeg")


def load_vec(args):
    p, n = args
    try:
        im = Image.open(p).convert("L")
        v = np.asarray(im.resize((n, n), Image.BOX), np.float32).ravel()
        v -= v.mean(); s = np.linalg.norm(v)
        return v / s if s > 1e-6 else None
    except Exception:
        return None


def vecs(paths, n, workers):
    with Pool(workers) as pool:
        out = pool.map(load_vec, [(p, n) for p in paths], chunksize=64)
    keep = [i for i, v in enumerate(out) if v is not None]
    return np.stack([out[i] for i in keep]) if keep else np.zeros((0, n * n), np.float32), [paths[i] for i in keep]


def stem(p):
    return os.path.splitext(os.path.basename(p))[0]


def case_of(ds, st):
    if ds == "carmlspine":
        m = re.match(r"^(case\d+)_", st); return m.group(1) if m else st
    return st.split("_")[0]


def top_pairs(A, B, thr, block=2048):
    """(i, j, r) for r >= thr, plus the max r per row of B (each test frame's nearest)."""
    pairs = []; bmax = np.full(len(B), -1.0, np.float32); barg = np.full(len(B), -1, np.int64)
    for j0 in range(0, len(B), block):
        Bb = B[j0:j0 + block]
        C = A @ Bb.T                                   # (nA, nb)
        if C.size:
            am = C.argmax(0); mx = C[am, np.arange(C.shape[1])]
            bmax[j0:j0 + len(Bb)] = mx; barg[j0:j0 + len(Bb)] = am
            ii, jj = np.nonzero(C >= thr)
            pairs.extend((int(i), int(j0 + j), float(C[i, j])) for i, j in zip(ii, jj))
    return pairs, bmax, barg


def ncc(p, q, n=64):
    a = load_vec((p, n)); b = load_vec((q, n))
    return float(a @ b) if a is not None and b is not None else None


def sheet(pairs, path, size=192, maxn=12):
    """Rows of (left, right) images with their score, for the eye."""
    from PIL import ImageDraw
    pairs = pairs[:maxn]
    if not pairs:
        return
    W = size * 2 + 8; Hh = size + 14
    canvas = Image.new("L", (W, Hh * len(pairs)), 40)
    d = ImageDraw.Draw(canvas)
    for r, (pa, pb, txt) in enumerate(pairs):
        for k, p in enumerate((pa, pb)):
            try:
                im = Image.open(p).convert("L").resize((size, size), Image.BILINEAR)
            except Exception:
                im = Image.new("L", (size, size), 0)
            canvas.paste(im, (k * (size + 8), r * Hh + 14))
        d.text((2, r * Hh + 1), txt[:110], fill=255)
    canvas.save(path)


def within(ds, thr, workers, out_dir, n=32):
    root = os.path.join(R, ds)
    paths = {s: sorted(p for p in glob.glob(os.path.join(root, "images", s, "*.png"))) for s in ("train", "val", "test")}
    V = {}
    for s, ps in paths.items():
        V[s] = vecs(ps, n, workers) if ps else (np.zeros((0, n * n), np.float32), [])
    res = dict(dataset=ds, n={s: len(V[s][1]) for s in V}, threshold=thr, comparisons={})
    for a_name, b_name in (("train+val", "test"), ("train", "val")):
        if a_name == "train+val":
            A = np.concatenate([V["train"][0], V["val"][0]]) if len(V["train"][1]) + len(V["val"][1]) else np.zeros((0, n * n), np.float32)
            Ap = V["train"][1] + V["val"][1]
        else:
            A, Ap = V["train"]
        B, Bp = V[b_name]
        if not len(A) or not len(B):
            res["comparisons"][f"{a_name}|{b_name}"] = dict(n_pairs=0, note="one side empty"); continue
        pairs, bmax, barg = top_pairs(A, B, thr)
        rows = []
        for i, j, r in pairs:
            sa, sb = stem(Ap[i]), stem(Bp[j]); ca, cb = case_of(ds, sa), case_of(ds, sb)
            rows.append(dict(a=sa, b=sb, case_a=ca, case_b=cb, same_case=(ca == cb), ncc32=round(r, 4)))
        cross = [r for r in rows if not r["same_case"]]
        cross.sort(key=lambda r: -r["ncc32"])
        for r in cross[:40]:
            r["ncc64"] = ncc(os.path.join(root, "images", "train" if os.path.exists(os.path.join(root, "images", "train", r["a"] + ".png")) else "val", r["a"] + ".png"),
                             os.path.join(root, "images", b_name, r["b"] + ".png"))
        hist = np.histogram(bmax, bins=[-1, 0.5, 0.8, 0.9, 0.95, 0.97, 0.98, 0.99, 1.001])[0].tolist()
        comp = dict(n_a=len(Ap), n_b=len(Bp), n_pairs=len(rows), n_same_case=sum(r["same_case"] for r in rows), n_cross_case=len(cross),
                    cross_case_pairs_involving_cases=len({r["case_b"] for r in cross}), max_ncc32=float(bmax.max()) if len(bmax) else None,
                    nearest_hist_bins=[-1, 0.5, 0.8, 0.9, 0.95, 0.97, 0.98, 0.99, 1.0], nearest_hist=hist,
                    n_ncc64_ge_thr=sum(1 for r in cross[:40] if r.get("ncc64") is not None and r["ncc64"] >= thr),
                    top_cross_case=cross[:20])
        res["comparisons"][f"{a_name}|{b_name}"] = comp
        if cross:
            def full(st, side):
                for s in (("train", "val") if side == "a" else (b_name,)):
                    p = os.path.join(root, "images", s, st + ".png")
                    if os.path.exists(p):
                        return p
                return p
            sheet([(full(r["a"], "a"), full(r["b"], "b"), f"{r['a']} | {r['b']}  ncc32 {r['ncc32']:.3f} ncc64 {r.get('ncc64', float('nan')):.3f}") for r in cross],
                  os.path.join(out_dir, f"dupes_{ds}_{a_name.replace('+', '')}_{b_name}.png"))
        print(f"{ds} {a_name} vs {b_name}: {len(rows)} pairs >= {thr} ({len(cross)} cross-case); max {comp['max_ncc32']}", flush=True)
    return res


def external_corpora():
    out = {}
    films = []
    for ds in ("yolo_v3", "yolo_v4z"):
        for s in ("train", "val", "test"):
            films += glob.glob(os.path.join(H, "spine-detector", "data", ds, "images", s, "*"))
    out["film_corpus_v3_v4z"] = [p for p in films if p.lower().endswith(EXTS)]
    pan = []
    for ext in EXTS:
        pan += glob.glob(os.path.join(H, "FluoroCap", "panels", "**", "*" + ext), recursive=True)
    out["fluorocap_panels"] = pan
    v6 = []
    for s in ("train", "val"):
        v6 += glob.glob(os.path.join(H, "spine-detector", "data", "yolo_v6f", "images", s, "*"))
    out["yolo_v6f"] = [p for p in v6 if p.lower().endswith(EXTS)]
    return out


def across(thr, workers, out_dir, n=32):
    internal = []
    for ds in ("carmlspine", "cobra_elekta", "deepfluoro", "geneva_hip"):
        for s in ("train", "val", "test"):
            internal += [(ds, s, p) for p in sorted(glob.glob(os.path.join(R, ds, "images", s, "*.png")))]
    IV, Ip = vecs([p for _, _, p in internal], n, workers)
    meta = {p: (ds, s) for ds, s, p in internal}
    res = dict(n_internal=len(Ip), threshold=thr, corpora={})
    for name, paths in external_corpora().items():
        if not paths:
            res["corpora"][name] = dict(n=0, note="no images found"); continue
        EV, Ep = vecs(paths, n, workers)
        pairs, imax, iarg = top_pairs(EV, IV, thr)       # rows = external, cols = internal
        rows = []
        for i, j, r in pairs:
            ds, s = meta[Ip[j]]
            rows.append(dict(external=os.path.relpath(Ep[i], H), internal=stem(Ip[j]), dataset=ds, split=s, ncc32=round(r, 4)))
        rows.sort(key=lambda r: -r["ncc32"])
        for r in rows[:40]:
            r["ncc64"] = ncc(os.path.join(H, r["external"]), os.path.join(R, r["dataset"], "images", r["split"], r["internal"] + ".png"))
        per_ds = Counter((r["dataset"], r["split"]) for r in rows)
        nearest = {}
        for ds in ("carmlspine", "cobra_elekta", "deepfluoro", "geneva_hip"):
            idx = [k for k, p in enumerate(Ip) if meta[p][0] == ds]
            if idx:
                m = imax[idx]
                nearest[ds] = dict(n=len(idx), median=float(np.median(m)), p90=float(np.percentile(m, 90)), max=float(m.max()),
                                   n_ge_0_9=int((m >= 0.9).sum()), n_ge_thr=int((m >= thr).sum()))
        res["corpora"][name] = dict(n=len(Ep), n_pairs=len(rows), pairs_per_dataset_split={f"{a}/{b}": c for (a, b), c in per_ds.items()},
                                    n_ncc64_ge_thr=sum(1 for r in rows[:40] if r.get("ncc64") is not None and r["ncc64"] >= thr),
                                    nearest_by_dataset=nearest, top=rows[:20])
        # the eye: the strongest match per dataset even when below threshold
        show = []
        for ds in ("carmlspine", "cobra_elekta", "deepfluoro", "geneva_hip"):
            idx = [k for k, p in enumerate(Ip) if meta[p][0] == ds]
            if idx:
                best = sorted(idx, key=lambda k: -imax[k])[:3]
                show += [(Ep[iarg[k]], Ip[k], f"{ds} {stem(Ip[k])} <- {os.path.basename(Ep[iarg[k]])[:40]} ncc32 {imax[k]:.3f}") for k in best]
        sheet(show, os.path.join(out_dir, f"xcorpus_{name}_nearest.png"))
        print(f"{name}: {len(Ep)} images; {len(rows)} pairs >= {thr}; nearest per dataset: " +
              ", ".join(f"{d} max {v['max']:.3f}" for d, v in nearest.items()), flush=True)
        del EV
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True); ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--thr", type=float, default=0.97)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    res = dict(threshold=a.thr, within={}, across=None)
    for ds in ("carmlspine", "cobra_elekta", "deepfluoro", "geneva_hip"):
        res["within"][ds] = within(ds, a.thr, a.workers, a.out)
    res["across"] = across(a.thr, a.workers, a.out)
    json.dump(res, open(os.path.join(a.out, "dupes.json"), "w"), indent=1)
    print("wrote", os.path.join(a.out, "dupes.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
