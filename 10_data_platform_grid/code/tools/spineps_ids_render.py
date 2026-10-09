#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/spineps_ids_render.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Render a relabelled SPINEPS mask (and, when given, the reader's label map of the same CT) on a mid-sagittal CT
slice, with each instance's NAME written at its centroid -- so the relabel is LOOKED at, not only counted.

Panels per case: [raw ids as they were read] [ctd-relabelled names] [reader / reference labels, when given].
Everything is taken to world space through the affines: the CT is resampled onto the mask's grid (linear), the
reference labels likewise (nearest). Arrays are canonicalised to RAS for display only; nothing is written back.

    python tools/spineps_ids_render.py --case COLONOG_1 --raw <raw mask> --new <relabelled mask> --ct <ct> \
        [--ref <label map> --ref-names verse|oneshot:<dataset.json>] --out <png>
"""
from __future__ import annotations

import argparse
import json

import numpy as np

VERSE = {**{i: f"C{i}" for i in range(1, 8)}, **{7 + i: f"T{i}" for i in range(1, 13)},
         **{19 + i: f"L{i}" for i in range(1, 7)}, 26: "S", 27: "Co", 28: "T13"}


def canon(img):
    import nibabel as nib
    return nib.as_closest_canonical(img)                     # display only; never saved


def main() -> int:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import nibabel as nib
    from nibabel.processing import resample_from_to

    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--ct", required=True)
    ap.add_argument("--ref", default=None)
    ap.add_argument("--ref-names", default="verse")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    new_img = canon(nib.load(a.new))
    raw_img = canon(nib.load(a.raw))
    new = np.asanyarray(new_img.dataobj).astype(np.int32)
    raw = np.asanyarray(resample_from_to(raw_img, new_img, order=0).dataobj).astype(np.int32)
    ct = np.asanyarray(resample_from_to(canon(nib.load(a.ct)), new_img, order=1).dataobj).astype(np.float32)
    panels = [("raw ids read as VerSe names", raw, VERSE), ("ctd-relabelled (tools/spineps_ids.py)", new, VERSE)]
    if a.ref:
        ref = np.asanyarray(resample_from_to(canon(nib.load(a.ref)), new_img, order=0).dataobj).astype(np.int32)
        if a.ref_names.startswith("oneshot:"):
            lab = json.load(open(a.ref_names.split(":", 1)[1]))["labels"]
            rn = {int(v): k for k, v in lab.items() if not isinstance(v, list)}
        else:
            rn = VERSE
        panels.append(("reader / reference labels", ref, rn))
    fg = np.nonzero((new > 0) & (new < 100))
    x = int(np.median(fg[0])) if len(fg[0]) else new.shape[0] // 2
    zooms = new_img.header.get_zooms()[:3]
    fig, axs = plt.subplots(1, len(panels), figsize=(4.2 * len(panels), 8))
    for ax, (title, lab, names) in zip(np.atleast_1d(axs), panels):
        sl_ct = ct[x, :, :].T[::-1, :]                       # rows S -> I, cols P -> A
        sl = lab[x, :, :].T[::-1, :]
        ax.imshow(np.clip(sl_ct, -200, 1200), cmap="gray", aspect=zooms[2] / zooms[1], interpolation="nearest")
        ax.imshow(np.ma.masked_where((sl == 0) | (sl >= 100), sl % 20), cmap="tab20", alpha=0.45,
                  aspect=zooms[2] / zooms[1], interpolation="nearest", vmin=0, vmax=19)
        for i in [int(v) for v in np.unique(sl) if 0 < v < 100]:
            ys, xs = np.nonzero(sl == i)
            if len(ys) < 30:
                continue
            ax.text(xs.mean(), ys.mean(), names.get(i, str(i)), fontsize=8, ha="center", va="center", color="k",
                    bbox=dict(fc="w", alpha=0.75, lw=0, pad=1))
        ax.set_title(title, fontsize=9)
        ax.set_axis_off()
    fig.suptitle(f"{a.case}  (mid-sagittal, x = {x})", fontsize=10)
    fig.savefig(a.out, dpi=110, bbox_inches="tight")
    print("wrote", a.out, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
