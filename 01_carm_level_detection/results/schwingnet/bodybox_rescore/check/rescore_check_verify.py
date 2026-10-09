#!/usr/bin/env python
"""Adversarial re-derivation for RESCORE_CHECK.md. Independent implementation: no imports from
spinesurg-ct-nnunet/tools. Re-derives, from the raw dumps and the truth meta dirs alone:

  1. C_cobra_ar_pooled_real (sweeps/pooled__cobra_test.json): body truth 0.74/0.25, WV truth 0.74/0.25,
     WV-on-body-subset (outline convention inside the body meta), with own case-clustered bootstrap CIs.
  2. A1 (sweeps/lodo_carm__carm_test.json vs carmlspine meta): outline + body at 0.74 and 0.25, own CIs.
  3. Convention difference: IoU(body box, outline/WV box) distributions for both truth banks.
  4. Truth-bank audit: per-case body counts, D152, totals 855/893, body meta vs released WV meta.

Prints one JSON to stdout.
"""
import json
import sys
from pathlib import Path

import numpy as np

RS = "/rs/rs_grp_oschome/go2432/data"
TRUTH_META = f"{RS}/or_ready/bodybox_rescore/truth/cobra_elekta/meta"
WV_META = f"{RS}/realxray/cobra_elekta/meta"
CARM_META = f"{RS}/realxray/carmlspine/meta"
POOLED_DUMP = f"{RS}/or_ready/lodo/sweeps/pooled__cobra_test.json"
A1_DUMP = f"{RS}/or_ready/lodo/sweeps/lodo_carm__carm_test.json"


def iou(a, b):
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    i = ix * iy
    u = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - i
    return i / u if u > 0 else 0.0


def greedy_match(preds, truth_boxes):
    """preds: [(conf, box)] any order. Returns per-truth matched confidence (None if unmatched).
    Rule: descending confidence, each prediction takes the unused truth of highest IoU if IoU >= 0.5."""
    used = set()
    tconf = [None] * len(truth_boxes)
    for conf, box in sorted(preds, key=lambda q: -q[0]):
        bj, best = -1, 0.0
        for j, t in enumerate(truth_boxes):
            if j in used:
                continue
            o = iou(box, t)
            if o >= 0.5 and o > best:
                best, bj = o, j
        if bj >= 0:
            used.add(bj)
            tconf[bj] = conf
    return tconf


def boot_ci(per_case, seed, n_boot=2000):
    """per_case: ordered [(case, k, n)]. Cluster bootstrap of sum k / sum n, percentile 95%."""
    k = np.array([q[1] for q in per_case], float)
    n = np.array([q[2] for q in per_case], float)
    C = len(k)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, C, size=(n_boot, C))
    den = n[idx].sum(1)
    den[den == 0] = np.nan
    r = k[idx].sum(1) / den
    r = r[~np.isnan(r)]
    return [float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))]


def load_meta(meta_dir, stem):
    p = Path(meta_dir) / f"{stem}.json"
    if not p.exists():
        return None
    return json.load(open(p))


def score_dump(dump_path, meta_dir, confs=(0.74, 0.25), fallback_beside_image=False):
    S = json.load(open(dump_path))
    frames = []
    missing = 0
    missing_stems = []
    for r in S["frames"]:
        m = load_meta(meta_dir, r["stem"])
        if m is None and fallback_beside_image and r["stem"] == "case118_LAT":
            # the frame the dump calls case118_LAT is case118_OBL in the repaired meta (2026-09-23 rename)
            m = load_meta(meta_dir, "case118_OBL")
        if m is None and fallback_beside_image and r.get("image"):
            img = Path(r["image"])
            split = img.parent.name
            for cand in (img.parents[2] / "meta", img.parents[2] / "meta" / split,
                         img.parents[2] / split / "meta"):
                m = load_meta(cand, r["stem"])
                if m is not None:
                    break
        if m is None:
            missing += 1
            missing_stems.append(r["stem"])
            continue
        boxes = [b for b in m.get("boxes", []) if b.get("kept", True)]
        verts = [b for b in boxes if b["cls"] == 0]
        preds = [(float(c3), [float(x) for x in b]) for c0, b, c3 in r["raw"] if c0 == 0]
        case = str(r.get("case") or m.get("case") or r["stem"].split("_")[0])
        body_tc = greedy_match(preds, [v["box"] for v in verts])
        out_boxes = [v.get("outline_box") or v["box"] for v in verts]
        outline_tc = greedy_match(preds, out_boxes)
        frames.append(dict(case=case, stem=r["stem"], n_vert=len(verts),
                           body=body_tc, outline=outline_tc,
                           has_outline=any("outline_box" in v for v in verts)))
    res = dict(dump=dump_path, meta=str(meta_dir), frames=len(frames), missing_meta=missing, missing_stems=missing_stems,
               truth_vertebrae=sum(f["n_vert"] for f in frames),
               cases=len({f["case"] for f in frames}), at={})
    for conv in ("body", "outline"):
        for t in confs:
            acc = {}
            order = []
            for f in frames:
                h = sum(1 for c in f[conv] if c is not None and c >= t)
                if f["case"] not in acc:
                    acc[f["case"]] = [0, 0]
                    order.append(f["case"])
                acc[f["case"]][0] += h
                acc[f["case"]][1] += len(f[conv])
            per_case = [(c, acc[c][0], acc[c][1]) for c in order]
            K = sum(q[1] for q in per_case)
            N = sum(q[2] for q in per_case)
            res["at"][f"{conv}@{t}"] = dict(
                k=K, n=N, pct=round(100.0 * K / N, 2) if N else None,
                ci_seed0=[round(100 * x, 2) for x in boot_ci(per_case, 0)],
                ci_seed1234=[round(100 * x, 2) for x in boot_ci(per_case, 1234)])
    # per-case truth counts (body convention denominators)
    pc = {}
    for f in frames:
        pc[f["case"]] = pc.get(f["case"], 0) + f["n_vert"]
    res["per_case_truth"] = dict(sorted(pc.items()))
    return res


def convention_gap(dump_path, meta_dir):
    """IoU(body `box`, `outline_box`) for every vertebra of the dump's frames in this meta dir."""
    S = json.load(open(dump_path))
    vals = []
    n_no_outline = 0
    for r in S["frames"]:
        m = load_meta(meta_dir, r["stem"])
        if m is None:
            continue
        for b in m.get("boxes", []):
            if b["cls"] != 0 or not b.get("kept", True):
                continue
            ob = b.get("outline_box")
            if ob is None:
                n_no_outline += 1
                continue
            vals.append(iou(b["box"], ob))
    v = np.array(vals)
    if not len(v):
        return dict(n=0, n_without_outline=n_no_outline)
    return dict(n=len(v), n_without_outline=n_no_outline,
                median=round(float(np.median(v)), 4), p90=round(float(np.percentile(v, 90)), 4),
                max=round(float(v.max()), 4), min=round(float(v.min()), 4),
                n_ge_05=int((v >= 0.5).sum()), n_ge_09=int((v >= 0.9).sum()))


def body_vs_wv_meta(dump_path, body_meta, wv_meta):
    """Pair each body-truth box with the WV box of the same level in the same frame; IoU distribution."""
    S = json.load(open(dump_path))
    vals = []
    unpaired = 0
    for r in S["frames"]:
        bm = load_meta(body_meta, r["stem"])
        wm = load_meta(wv_meta, r["stem"])
        if bm is None or wm is None:
            continue
        wv_by_level = {}
        for b in wm.get("boxes", []):
            if b["cls"] == 0 and b.get("kept", True) and b.get("level"):
                wv_by_level[b["level"]] = b["box"]
        for b in bm.get("boxes", []):
            if b["cls"] != 0 or not b.get("kept", True):
                continue
            lv = b.get("level")
            if lv in wv_by_level:
                vals.append(iou(b["box"], wv_by_level[lv]))
            else:
                unpaired += 1
    v = np.array(vals)
    return dict(n=len(v), unpaired=unpaired, median=round(float(np.median(v)), 4),
                p90=round(float(np.percentile(v, 90)), 4), max=round(float(v.max()), 4),
                min=round(float(v.min()), 4), n_ge_05=int((v >= 0.5).sum()), n_ge_09=int((v >= 0.9).sum()))


def main():
    out = {}
    out["pooled_vs_bodytruth"] = score_dump(POOLED_DUMP, TRUTH_META)
    out["pooled_vs_wv"] = score_dump(POOLED_DUMP, WV_META)
    out["a1_lodo_carm_vs_carm_meta"] = score_dump(A1_DUMP, CARM_META, fallback_beside_image=True)
    out["gap_carmlspine_body_vs_outline"] = convention_gap(A1_DUMP, CARM_META)
    out["gap_cobra_bodytruth_vs_wv_level_paired"] = body_vs_wv_meta(POOLED_DUMP, TRUTH_META, WV_META)
    json.dump(out, sys.stdout, indent=1)
    print()


if __name__ == "__main__":
    main()
