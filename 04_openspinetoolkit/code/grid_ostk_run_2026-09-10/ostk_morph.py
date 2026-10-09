# spine-program/04_openspinetoolkit: copied 2026-10-08 (read on the grid 2026-10-09 00:12 UTC with `cat`, read-only).
# Source: grid HOME /wsu/home/go/go24/go2432/ostk_run/ostk_morph.py, dated 2026-09-10 03:01; in no repository. Hash of the file as read: sha256 26b9f63ef24de387ea7f018ff14a08f31fe9e10909f07c54ab6d68cfaaf1ecd2.
# The 2026-09-10 shard run of ostk per-level morphometry; see 04_openspinetoolkit/STATUS.md G.4 and results/grid_run_2026-09-10/README.md.
"""Run ostk.morphometry over real cases and set it beside Panjabi.

This is the check that decides whether the frame-based estimator was worth building.
It reports the NEW measurement, the OLD one on the same masks, and the published value,
so the gap can be attributed rather than argued about:

  if new lands near Panjabi and old does not, the gap was the estimator;
  if both sit high, the gap is the population, and the release measures what it says.

Nothing here is tuned. The estimator was written against the published DEFINITION and
this is the first time its output is compared with the published NUMBERS.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import nibabel as nib
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parent / "OpenSpineToolkit"))
import ostk  # noqa: E402
from ostk.morphometry import level_morphometry  # noqa: E402

LUMBAR = {20: "L1", 21: "L2", 22: "L3", 23: "L4", 24: "L5"}

# Panjabi 1992, Tables 2-4, mean over twelve specimens
PAN = {
    "VBHp":  {"L1": 23.8, "L2": 24.3, "L3": 23.8, "L4": 24.1, "L5": 22.9},
    "EPWu":  {"L1": 41.2, "L2": 42.6, "L3": 44.1, "L4": 46.6, "L5": 47.3},
    "SCW":   {"L1": 23.7, "L2": 23.8, "L3": 24.3, "L4": 25.4, "L5": 27.1},
    "SCD":   {"L1": 19.0, "L2": 18.2, "L3": 17.5, "L4": 18.6, "L5": 19.7},
    "PDW":   {"L1":  8.6, "L2":  8.25, "L3": 10.15, "L4": 14.05, "L5": 18.6},
}


def old_post_height(lab, sp, vid):
    """The estimator being replaced: max column over the posterior half of a slab."""
    whole = lab == vid
    if whole.sum() < 500:
        return None
    zz = np.nonzero(whole.any(axis=(0, 1)))[0]
    fronts = []
    for z in zz[len(zz) // 3: 2 * len(zz) // 3 + 1]:
        sl = whole[:, :, z]
        if sl.sum() < 40:
            continue
        h = ndimage.binary_fill_holes(sl) & ~sl
        if h.any():
            fronts.append(int(np.nonzero(h.any(axis=0))[0].max()))
    if not fronts:
        return None
    m = np.zeros_like(whole)
    m[:, int(np.median(fronts)):, :] = whole[:, int(np.median(fronts)):, :]
    if m.sum() < 500:
        return None
    idx = np.argwhere(m)
    bx = float(np.median(idx[:, 0]))
    slab = m[max(0, int(round(bx - 5 / sp[0]))): int(round(bx + 5 / sp[0])) + 1]
    col = {}
    for y in np.nonzero(slab.any(axis=(0, 2)))[0]:
        c = slab[:, y, :]
        if c.sum() < 3:
            continue
        zc = np.nonzero(c.any(axis=0))[0]
        col[y] = (zc.max() - zc.min() + 1) * sp[2]
    if len(col) < 6:
        return None
    yy = np.array(sorted(col))
    hh = np.array([col[y] for y in yy])
    return float(hh[yy <= (yy.min() + yy.max()) / 2.0].max())


def main():
    root = Path(sys.argv[1])
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    files = sorted(root.glob("*_label.nii.gz"))[:n]
    print(f"ostk {getattr(ostk, '__version__', 'dev')} on {len(files)} case(s)\n", flush=True)
    new, old, dropped = {}, {}, 0
    for i, f in enumerate(files, 1):
        try:
            img = nib.as_closest_canonical(nib.load(str(f)))
            lab = np.asanyarray(img.dataobj)
            aff = img.affine
            sp = np.asarray(img.header.get_zooms()[:3], float)
            for vid, lv in LUMBAR.items():
                r = level_morphometry(lab, aff, vid)
                if r is None:
                    dropped += 1
                else:
                    for k, v in r.items():
                        new.setdefault((lv, k), []).append(v)
                o = old_post_height(lab, sp, vid)
                if o is not None:
                    old.setdefault(lv, []).append(o)
        except Exception as exc:
            print(f"  {f.name}: {type(exc).__name__}: {exc}", flush=True)
        if i % 10 == 0:
            print(f"  {i}/{len(files)}", flush=True)

    print(f"\nlevels dropped for a bad plate fit: {dropped}\n")
    for key in ("VBHp", "EPWu", "SCW", "SCD", "PDW"):
        src = {"EPWu": "EPWu", "PDW": "PDW"}.get(key, key)
        print(f"--- {key} ---")
        print(f"{'level':6s} {'n':>4s} {'ostk':>8s} {'old':>8s} {'Panjabi':>8s} "
              f"{'ostk-Pan':>9s} {'old-Pan':>9s}")
        for lv in LUMBAR.values():
            vals = new.get((lv, src), [])
            if not vals:
                print(f"{lv:6s} {0:4d} {'--':>8s}")
                continue
            nv = float(np.median(vals))
            pv = PAN[key][lv]
            ov = float(np.median(old[lv])) if (key == "VBHp" and old.get(lv)) else float("nan")
            od = f"{ov - pv:+9.1f}" if ov == ov else f"{'':>9s}"
            os_ = f"{ov:8.1f}" if ov == ov else f"{'':>8s}"
            print(f"{lv:6s} {len(vals):4d} {nv:8.1f} {os_} {pv:8.1f} {nv - pv:+9.1f} {od}")
        print()


if __name__ == "__main__":
    main()
