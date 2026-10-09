# spine-program/04_openspinetoolkit: copied 2026-10-08 (read on the grid 2026-10-09 00:12 UTC with `cat`, read-only).
# Source: grid HOME /wsu/home/go/go24/go2432/ostk_run/pedicle_dev.py, dated 2026-09-10 05:59; in no repository. Hash of the file as read: sha256 59b7c3655879c7718cfdf4883c8c9808db664df5258d6588a9fb47fc206db9f6.
# The development function (isthmus_width, erosion neck) behind the 118-pedicle-per-level table of job 40183964; ostk.morphometry.pedicle_widths
# at cb43197 is a different implementation (isthmus as the section of least area). See 04_openspinetoolkit/STATUS.md G.4.
"""Pedicle width as the NARROWEST NECK between body and arch, measured by erosion.

WHY THE PREVIOUS THREE ATTEMPTS FAILED, in order, because each failure narrowed the problem:

  1. "everything that is not body, split at the midline" -- the principal axis followed the
     lamina and transverse process, which outweigh an upper lumbar pedicle. Read 17 mm at
     L1 against a published 8.6.
  2. "the part lateral to the canal, in the anterior half of its span" -- took the wrong end
     of the canal, after a comment warning not to assume which end was anterior. Read a flat
     7 mm with none of the caudal widening a pedicle has.
  3. "the thin bridge between two thick cores", after Yao 2006 -- right in principle, wrong
     in its constant. A filled lumbar pedicle is 8 to 18 mm across, so its inscribed radius
     EXCEEDS the 4 mm core threshold and it joins the cores rather than bridging them. That
     threshold is tuned for thoracic pedicles. Found nothing at all.

WHAT ACTUALLY DEFINES THE MEASUREMENT. Panjabi's PDW is the transverse diameter of the
pedicle at its isthmus, and the isthmus is the narrowest cross-section of the strut joining
body to arch. That is a NECK, and a neck does not have to be segmented to be measured:
erode the side's bone until body and arch stop being connected through it, and the erosion
count is the neck's half-width. It is the same quantity as the largest sphere that passes
through the pedicle, which is why it is also the limiting screw diameter.

Two things make it trustworthy rather than approximate:

  HOLES ARE FILLED FIRST. The basivertebral channel and marrow voids are background here,
  and erosion eats from every interior edge, so an unfilled body separates from its arch
  for the wrong reason.

  THE GRID IS INTERPOLATED FIRST. An 8 mm pedicle on a 0.8 mm grid is quantised at 10%, and
  a staircase edge measured across an oblique strut reads systematically wide because the
  steps protrude perpendicular to the direction being measured. The mask becomes a signed
  distance field, is resampled linearly to 0.35 mm isotropic and re-thresholded -- the
  standard level-set resampling, which recovers sub-voxel boundary position. A
  nearest-neighbour zoom would only make the staircase finer.

    python pedicle_dev.py <ct_dir> <lab_dir> <out_dir> [case ...]
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import nibabel as nib
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent / "OpenSpineToolkit"))
from ostk.vertebral_body import body_mask, canal_mask     # noqa: E402
from ostk.geometry import principal_axes, unit            # noqa: E402

LV = {20: "L1", 22: "L3", 24: "L5"}
PAN_W = {"L1": 8.6, "L3": 10.15, "L5": 18.6}
TARGET = 0.35


def _fill(m):
    out = np.zeros_like(m)
    for k in range(m.shape[2]):
        if m[:, :, k].any():
            out[:, :, k] = ndimage.binary_fill_holes(m[:, :, k])
    return out


def _resample(mask, sp, box, target=TARGET):
    """Signed-distance resample onto the grid defined by `box`, with sub-voxel edges."""
    lo, hi = box
    sub = np.asarray(mask, bool)[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
    if not sub.any():
        return None
    sdf = (ndimage.distance_transform_edt(sub, sampling=sp)
           - ndimage.distance_transform_edt(~sub, sampling=sp))
    return ndimage.zoom(sdf, np.asarray(sp, float) / target, order=1, mode="nearest") > 0.0


def isthmus_width(vert, body, sp, canal=None, margin=6, target=TARGET, max_mm=30.0):
    """PDW per side, by the published convention.

    Written against the literature after four attempts failed. Two things it settles that
    guessing did not:

    THE REGION IS BOUNDED BEFORE ANYTHING IS MINIMISED. Kumar et al. (Int J Med Robot 2025,
    doi:10.1002/rcs.70049) define an Initial Pedicle Region per axial slice, between the
    vertebral-body boundary and the spinal-canal boundary, split left and right by the line
    joining the canal centre to the body centre. The pars is posterior to the canal, so it
    is never a candidate -- which is the whole of my min-cut failure, where the narrowest
    route from body to lamina ran through the pars instead of the pedicle.

    PDW IS THE TRANSVERSE EXTENT, NOT THE INSCRIBED CIRCLE. This is the error that made
    every previous version read flat across levels. A maximum inscribed circle measures
    min(width, height). At L1 the pedicle is 8.6 wide and about 16 tall, so the circle is
    the width and the answer looks right; by L5 it is about 18.6 wide and the height is
    limiting, so the same code returns the height and the caudal widening disappears.
    Makino et al. (Eur Spine J 2012) show the flip directly: transverse 5.5 to 12.9 mm from
    L1 to L5 while sagittal runs 11.9 down to 9.0. So the cross-section is measured along
    the vertebra's own transverse direction.

    Isthmus is the section of least area perpendicular to the pedicle's own axis, after
    Li et al. (Spine 2004;29:2438) and Sugisaki et al. (Spine 2009;34:2599). Outer
    cortical, to match Panjabi and Zindrick.
    """
    vfill = _fill(np.asarray(vert, bool))
    idx = np.argwhere(vfill)
    if not len(idx) or canal is None:
        return {}, None, None
    lo = np.maximum(idx.min(0) - margin, 0)
    hi = np.minimum(idx.max(0) + margin + 1, np.array(vfill.shape))
    V = _resample(vfill, sp, (lo, hi), target)
    B = _resample(_fill(np.asarray(body, bool)), sp, (lo, hi), target)
    C = _resample(canal, sp, (lo, hi), target)
    if V is None or C is None or B is None or not C.any():
        return {}, V, None
    B = B & V

    # ---- the Initial Pedicle Region, per axial section -------------------------------
    ipr = {"l": np.zeros_like(V), "r": np.zeros_like(V)}
    for k in range(V.shape[2]):
        cs, vs, bs = C[:, :, k], V[:, :, k], B[:, :, k]
        if cs.sum() < 20 or not bs.any():
            continue
        cx = np.nonzero(cs.any(axis=1))[0]
        cy = np.nonzero(cs.any(axis=0))[0]
        bx = np.nonzero(bs.any(axis=1))[0]
        band = np.zeros_like(vs)
        band[:, cy.min():cy.max() + 1] = True          # anterior to the canal's back wall
        for name, lat in (("l", slice(int(bx.min()), int(cx.min()))),
                          ("r", slice(int(cx.max()) + 1, int(bx.max()) + 1))):
            if lat.start is None or lat.stop is None or lat.stop <= lat.start:
                continue
            reg = np.zeros_like(vs)
            reg[lat] = vs[lat]
            reg &= band & ~bs                          # bone, not body, lateral of canal
            if reg.sum() < 15:
                continue
            lab, n = ndimage.label(reg)
            if n:
                sizes = ndimage.sum(reg, lab, range(1, n + 1))
                ipr[name][:, :, k] = lab == (int(np.argmax(sizes)) + 1)

    marks = np.zeros_like(V, np.uint8)
    out = {}
    lat_dir = np.array([1.0, 0.0, 0.0])                # array x is left-right after canon.
    for name in ("l", "r"):
        pts_i = np.argwhere(ipr[name])
        if len(pts_i) < 200:
            continue
        pts = pts_i.astype(float) * target
        axes, _, cen = principal_axes(pts)
        axis = unit(np.asarray(axes)[:, 0])            # the pedicle's own long axis
        t = pts @ axis
        lo_t, hi_t = np.quantile(t, [0.15, 0.85])
        best = None
        for c in np.linspace(lo_t, hi_t, 25):
            sec = pts[np.abs(t - c) <= target]
            if len(sec) < 25:
                continue
            area = len(sec) * target ** 2               # section of least area = isthmus
            if best is None or area < best[0]:
                best = (area, c, sec)
        if best is None:
            continue
        sec = best[2]
        # transverse extent within that section, in the vertebra's own left-right
        u = lat_dir - (lat_dir @ axis) * axis
        if np.linalg.norm(u) < 1e-6:
            continue
        u = unit(u)
        proj = sec @ u
        out[name] = float(proj.max() - proj.min())
        kk = int(round(float(np.median(sec[:, 2])) / target))
        if 0 <= kk < marks.shape[2]:
            marks[:, :, kk] |= (ipr[name][:, :, kk]).astype(np.uint8) * (1 if name == "l" else 2)
    if "l" in out and "r" in out:
        out["mean"] = 0.5 * (out["l"] + out["r"])
    return out, V, marks


def main():
    lab_dir, out_dir = Path(sys.argv[2]), Path(sys.argv[3])
    out_dir.mkdir(parents=True, exist_ok=True)
    cases = sys.argv[4:] or [p.name.split("_")[0] for p in
                             sorted(lab_dir.glob("*_label.nii.gz"))[:3]]
    for case in cases:
        lp = lab_dir / f"{case}_label.nii.gz"
        if not lp.exists():
            continue
        limg = nib.as_closest_canonical(nib.load(str(lp)))
        lab = np.asanyarray(limg.dataobj)
        sp = np.asarray(limg.header.get_zooms()[:3], float)
        aff = limg.affine

        fig, axes = plt.subplots(1, len(LV), figsize=(4.3 * len(LV), 4.6))
        for col, (vid, name) in enumerate(LV.items()):
            ax = axes[col]
            vert = lab == vid
            if vert.sum() < 500:
                ax.axis("off"); continue
            body = body_mask(vert, aff)
            if body is None:
                ax.axis("off"); continue
            w, V, seps = isthmus_width(vert, body, sp, canal_mask(vert, aff))
            txt = [f"{case} {name}"]
            if V is None:
                txt.append("resample failed")
            else:
                z = (int(np.argmax((seps == 3).sum(axis=(0, 1))))
                     if seps is not None and (seps == 3).any()
                     else (int(np.argmax((seps > 0).sum(axis=(0, 1))))
                           if seps is not None and (seps > 0).any() else V.shape[2] // 2))
                ax.imshow(V[:, :, z].T, cmap="Greys", origin="lower",
                          interpolation="nearest")
                if seps is not None and (seps > 0).any():
                    m = np.ma.masked_where(seps[:, :, z].T == 0, seps[:, :, z].T)
                    ax.imshow(m, cmap="autumn", alpha=0.9, origin="lower",
                              interpolation="nearest")
                txt.append("  ".join(f"PDW_{k} {v:.1f}" for k, v in sorted(w.items()))
                           or "no separation found")
                txt.append(f"Panjabi PDW {PAN_W[name]}")
            ax.set_xticks([]); ax.set_yticks([])
            ax.set_title("\n".join(txt), fontsize=8, loc="left")
            print(f"  {case} {name}: " + " | ".join(txt[1:]), flush=True)
        fig.tight_layout(pad=0.4)
        fig.savefig(out_dir / f"{case}_pedicle.png", dpi=140)
        plt.close(fig)


if __name__ == "__main__":
    main()
