# spine-program/04_openspinetoolkit: copied 2026-10-08 from the NextPaper working folder on the laptop
# (untracked, in no repository; file dated 2026-05-17). The copy's source path and hash are recorded in
# 04_openspinetoolkit/MANIFEST_LOCAL.md. Superseded by OpenSpineToolkit (main, cb43197); kept as dated lineage.
# Reads the CTSpinoPelvic1K-Sample export of May 2026 under the legacy label map (L1 = 1 ... femur_right = 12);
# never run it on a v11 volume without ostk.labels.labels_for(volume).
"""
spine_analysis_v316.py  —  TRALL Lumbar Lordosis (Chernukha method)
==============================================================

LANDMARK STRATEGY (this version):
-----------------------------------
Instead of trying to extract the "posterior cortex" (which requires knowing
the AP direction convention and is sensitive to process voxels), we use the
3-D CENTROID of each vertebral body as the arc landmark.

Rationale:
  - The centroid is unambiguous: no sign/direction assumptions needed
  - It always sits inside the vertebra — never outside
  - For the Chernukha TRALL, the arc traces the POSTERIOR VERTEBRAL BODY
    WALL.  In a segmentation mask the centroid of the posterior half of
    each vertebra is a robust proxy for this wall, and the TRALL angle
    is insensitive to small AP offsets of the landmark (it measures
    curvature, not absolute AP position)
  - Produces consistent results across all cases regardless of orientation

For endpoints A and B we use the superior centroid of L1 and the inferior
centroid of the Sacrum respectively, which cleanly represent the arc ends.

TRALL METHOD (Chernukha et al.):
---------------------------------
  arc  = centroids of L1, L2, L3, L4, L5, Sacrum  (sorted superior→inferior)
  A    = centroid of superior half of L1
  B    = centroid of inferior half of Sacrum
  C    = arc point with max perpendicular distance from chord A→B
  TRALL = angle at C between rays C→A and C→B

All geometry in world mm (RAS).  Visualisation in mid-sagittal slice pixels.

Usage
-----
  python spine_analysis.py --hub_repo anonymous-neurips-ED/CTSpinoPelvic1K-Sample
  python spine_analysis.py --dataset_root C:\\path\\to\\repo
  [--output results.csv] [--visualize] [--vis_dir figures]
  [--split all|trainval|test] [--cases 0071 0468 0761]

Dependencies: nibabel numpy scipy matplotlib huggingface_hub
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys
import threading
import time

# ── Windows cp1252 console fix ────────────────────────────────────────────────
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
# ─────────────────────────────────────────────────────────────────────────────
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np

# ── tqdm with graceful fallback ───────────────────────────────────────────────
try:
    from tqdm import tqdm as _tqdm_real
    _TQDM_AVAILABLE = True
except ImportError:
    _TQDM_AVAILABLE = False

def _make_pbar(total: int, desc: str = "", disable: bool = False):
    """Return a tqdm progress bar, or a no-op shim if tqdm is unavailable."""
    if _TQDM_AVAILABLE and not disable:
        return _tqdm_real(
            total=total, desc=desc, unit="case",
            dynamic_ncols=True, leave=True,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
        )
    class _NullBar:
        def update(self, n=1): pass
        def set_postfix_str(self, s, refresh=True): pass
        def close(self): pass
        def __enter__(self): return self
        def __exit__(self, *a): pass
    return _NullBar()
# ─────────────────────────────────────────────────────────────────────────────

# ── Logging setup ─────────────────────────────────────────────────────────────
_LOG_LOCK = threading.Lock()

def _setup_logging(log_path: Path, file_level: int = logging.DEBUG) -> logging.Logger:
    """
    File handler  — DEBUG level (full per-case detail).
    Console handler — WARNING level only (keeps tqdm bar clean).
    Thread-safe: Python logging serialises handler writes internally.
    """
    logger = logging.getLogger("spine")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    fmt = logging.Formatter(
        fmt="%(asctime)s  %(levelname)-7s  [%(threadName)s]  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    fh = logging.FileHandler(str(log_path), mode="w", encoding="utf-8")
    fh.setLevel(file_level)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.WARNING)
    ch.setFormatter(logging.Formatter("%(levelname)-7s  %(message)s"))
    logger.addHandler(ch)

    return logger

log = logging.getLogger("spine")
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# Label constants
# ─────────────────────────────────────────────────────────────────────────────

LABEL_MAP: Dict[int, str] = {
    1: "L1", 2: "L2", 3: "L3", 4: "L4", 5: "L5", 6: "L6", 7: "Sacrum",
}
HIP_LABELS     = {8, 9}
L1_LABEL       = 1
SACRUM_LABEL   = 7
ARC_LABELS     = [1, 2, 3, 4, 5]      # L1–L5 only; Sacrum not in arc
ALL_SPINE_LBLS = list(LABEL_MAP.keys())


# ─────────────────────────────────────────────────────────────────────────────
# Matplotlib compat
# ─────────────────────────────────────────────────────────────────────────────

def _get_cmap(name: str):
    try:
        return matplotlib.colormaps[name]
    except AttributeError:
        return plt.cm.get_cmap(name)


# ─────────────────────────────────────────────────────────────────────────────
# Case wrapper — reads directly from ct/ and labels/ NIfTI folders
# ─────────────────────────────────────────────────────────────────────────────

class NiftiCase:
    """
    Wraps one entry from the manifest JSON.
    Reads ct/<token>_ct.nii.gz and labels/<token>_label.nii.gz directly.
    """
    def __init__(self, token: str, config: str, split: str,
                 ct_path: Path, label_path: Path):
        self.token      = token
        self.config     = config
        self.split      = split
        self._ct_path   = ct_path
        self._label_path = label_path

    def load_label(self):
        import nibabel as nib
        img = nib.load(str(self._label_path))
        return np.asarray(img.dataobj).astype(np.int16),                np.array(img.affine, dtype=np.float64)

    def load_ct(self):
        import nibabel as nib
        img = nib.load(str(self._ct_path))
        return np.asarray(img.dataobj).astype(np.int16),                np.array(img.affine, dtype=np.float64)


def build_dataset(args) -> list:
    """
    Read the manifest JSON files from the snapshot directory and build a
    list of NiftiCase objects pointing at the ct/ and labels/ NIfTI files.
    No downloading — the data is already on disk.
    """
    snap = Path(args.dataset_root)

    # Determine which splits to include
    split_arg = getattr(args, "split", "all").lower()
    if split_arg == "all":
        wanted_splits = {"train", "validation", "test"}
    elif split_arg == "trainval":
        wanted_splits = {"train", "validation"}
    elif split_arg == "test":
        wanted_splits = {"test"}
    else:
        wanted_splits = {"train", "validation", "test"}

    # Map split name -> manifest file
    manifest_files = {
        "train":      snap / "manifest_train.json",
        "validation": snap / "manifest_validation.json",
        "test":       snap / "manifest_test.json",
    }

    ct_dir    = snap / "ct"
    label_dir = snap / "labels"

    if not ct_dir.exists():
        raise FileNotFoundError(
            f"ct/ folder not found under {snap}.\n"
            f"Point --dataset_root at the snapshot folder that contains "
            f"ct/, labels/, and manifest_*.json files.\n"
            f"e.g. /path/to/D:/hf_cache/datasets--anonymous-mlhc--"
            f"CTSpinoPelvic1K/snapshots/<hash>")

    cases = []
    split_counts = {}
    for split_name, mf in manifest_files.items():
        if split_name not in wanted_splits:
            continue
        if not mf.exists():
            log.warning("Manifest not found, skipping split '%s': %s", split_name, mf)
            continue
        with open(mf) as fh:
            entries = json.load(fh)
        for e in entries:
            config = e.get("config", "unknown")
            token  = str(e.get("token", ""))
            ct_file    = snap / e["ct_file"]
            label_file = snap / e["label_file"]
            if not ct_file.exists() or not label_file.exists():
                log.warning("Missing files for token %s, skipping.", token)
                continue
            cases.append(NiftiCase(
                token      = token,
                config     = config,
                split      = split_name,
                ct_path    = ct_file,
                label_path = label_file,
            ))
        split_counts[split_name] = sum(1 for c in cases if c.split == split_name)

    log.info("%d cases loaded from manifests: %s", len(cases), split_counts)
    return cases


# ─────────────────────────────────────────────────────────────────────────────
# Case loading  (thin wrapper — NpzCase.load_label() handles the actual I/O)
# ─────────────────────────────────────────────────────────────────────────────

def load_label_and_affine(case) -> Tuple[np.ndarray, np.ndarray]:
    mask, affine = case.load_label()
    return mask.astype(np.int16), affine.astype(np.float64)


def _setup_hf_cache(args):
    """Kept for CLI compatibility — no-op in local mode."""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# Affine helpers
# ─────────────────────────────────────────────────────────────────────────────

def axis_for_world_dim(affine: np.ndarray, world_dim: int) -> Tuple[int, int]:
    """Which voxel axis aligns best with RAS dim (0=LR,1=AP,2=SI)?"""
    row = affine[:3, :3][world_dim, :]
    ax  = int(np.argmax(np.abs(row)))
    return ax, (1 if row[ax] > 0 else -1)


def voxels_to_world(ijk: np.ndarray, affine: np.ndarray) -> np.ndarray:
    h = np.hstack([ijk, np.ones((len(ijk), 1))])
    return (affine @ h.T).T[:, :3]


# ─────────────────────────────────────────────────────────────────────────────
# Vertebral centroid landmarks  (world mm)
# ─────────────────────────────────────────────────────────────────────────────

def _posterior_world_ap(world: np.ndarray, ap_sgn: int = -1,
                         frac: float = 0.20) -> np.ndarray:
    """
    Return the posterior `frac` fraction of voxels.
    ap_sgn < 0: posterior = LARGEST Y (keep top frac)
    ap_sgn > 0: posterior = SMALLEST Y (keep bottom frac)
    """
    ap = world[:, 1]
    ap_min, ap_max = ap.min(), ap.max()
    ap_range = ap_max - ap_min
    if ap_range < 1.0:
        return np.ones(len(ap), dtype=bool)
    if ap_sgn < 0:
        thr  = ap_max - frac * ap_range
        keep = ap >= thr
    else:
        thr  = ap_min + frac * ap_range
        keep = ap <= thr
    return keep if keep.sum() >= 3 else np.ones(len(ap), dtype=bool)


def posterior_centroid(mask: np.ndarray,
                        label: int,
                        affine: np.ndarray,
                        ap_sgn: int = 1,
                        si_frac_lo: float = 0.0,
                        si_frac_hi: float = 1.0,
                        post_frac: float = 0.25,
                        sl=None) -> Optional[np.ndarray]:
    """
    Centroid of the POSTERIOR wall of a vertebra in a SI height band.

    When `sl` (SagittalSlice) is provided, posterior is determined using
    the display column: in the SagittalSlice, col=0 is guaranteed to be the
    most posterior direction (enforced by col_order sorting in __init__).
    We pick the rear `post_frac` of AP columns in the mid-sagittal slice.

    Without sl, falls back to world-AP minimum (RAS: min-Y = posterior).

    Returns (AP_mm, SI_mm) or None.
    """
    if sl is not None:
        return _posterior_centroid_slice(sl, label, si_frac_lo, si_frac_hi,
                                          post_frac)
    # Fallback: world space
    coords = np.argwhere(mask == label).astype(np.float64)
    if coords.shape[0] < 10:
        return None
    world = voxels_to_world(coords, affine)
    si    = world[:, 2]
    si_min, si_max = si.min(), si.max()
    si_lo  = si_min + si_frac_lo * (si_max - si_min)
    si_hi  = si_min + si_frac_hi * (si_max - si_min)
    si_keep = (si >= si_lo) & (si <= si_hi)
    if si_keep.sum() < 5:
        si_keep = np.ones(len(si), dtype=bool)
    world_band = world[si_keep]
    post_keep  = _posterior_world_ap(world_band, frac=post_frac)
    final      = world_band[post_keep] if post_keep.sum() >= 3 else world_band
    return np.array([float(final[:, 1].mean()), float(final[:, 2].mean())])


def get_endplate_point(sl, label: int, endplate: str) -> Optional[np.ndarray]:
    """
    Posterior point on superior or inferior endplate of a vertebral body.

    Approach:
    1. For each row compute the horizontal span (max_col - min_col).
       Body rows are wide; spinous process rows are narrow.
       Threshold: keep rows with span >= 30% of max span = body rows.
    2. Endplate row = topmost (superior) or bottommost (inferior) body row.
    3. At that endplate row, posterior col = min_col (leftmost pixel).
       At the true endplate level the spinous process does not appear,
       so min_col is always the posterior body wall.
    4. For the SACRUM inferior endplate (B): first isolate the largest
       connected blob of sacrum pixels to ignore the small S-shaped tail.
    """
    img   = sl.img
    nrows = sl.nrows
    ncols = sl.ncols

    locs = np.argwhere(img == label)
    if len(locs) < 5:
        return None

    # For sacrum inferior endplate: keep only the LARGEST connected component
    if label == SACRUM_LABEL and endplate == 'inferior':
        from scipy import ndimage as _ndi
        sacrum_mask = (img == label).astype(np.uint8)
        labeled, n  = _ndi.label(sacrum_mask)
        if n > 1:
            sizes = [np.sum(labeled == i) for i in range(1, n + 1)]
            largest = int(np.argmax(sizes)) + 1
            locs    = np.argwhere(labeled == largest)

    rows = locs[:, 0]
    cols = locs[:, 1]

    unique_rows = np.unique(rows)

    # Per-row span and min col
    row_span_d   = {}
    row_mincol_d = {}
    for r in unique_rows:
        rc = cols[rows == r]
        row_span_d[r]   = int(rc.max() - rc.min())
        row_mincol_d[r] = int(rc.min())

    max_span  = max(row_span_d.values())
    threshold = 0.30 * max_span

    body_rows = np.array([r for r in unique_rows
                          if row_span_d[r] >= threshold])
    if len(body_rows) == 0:
        body_rows = unique_rows

    body_rows = np.sort(body_rows)

    # Endplate row — set after superior branch to allow clean-band clamping
    if endplate != 'superior':
        endplate_row = int(body_rows.min())

    # ── Posterior col computation ─────────────────────────────────────────
    # Use the centroid col as the body/arch divider (arch is left of centroid).
    all_body_cols = []
    for r in body_rows:
        rc = cols[rows == r]
        all_body_cols.extend(rc.tolist())
    centroid_col = float(np.mean(all_body_cols))

    if endplate == 'superior':
        # Two-step Point A (v316):
        #
        # Step 1 — AP col from INFERIOR body band (20–50% from bottom), widest-run.
        #   T12 overlap and L1 spinous contamination only appear at the TOP of the
        #   L1 label. The inferior 20–50% of body rows is always clean body tissue.
        #   At each row, find all contiguous pixel runs and take the WIDEST one —
        #   the vertebral body is always the widest run; any spinous/T12 fragment
        #   is a narrow separate run.  Leftmost col of widest run = posterior wall.
        #   IQR filter + min of clean set gives the most posterior stable value.
        #
        # Step 2 — SI row: topmost row among body rows whose span is consistent
        #   with the clean body (IQR filter on per-row spans).
        #   T12-contaminated rows at the top of the L1 label often have an
        #   anomalously large horizontal span (two overlapping vertebrae merged).
        #   Rows whose span exceeds Q75 + 1.5*IQR of the body-row span
        #   distribution are excluded before taking body_rows.max().
        #   This keeps Point A on the L1 superior endplate rather than T12.
        #
        # Confined to this branch only — arc logic untouched.

        def _widest_run_min_col_A(row_cols):
            """Min col of the widest contiguous pixel run in sorted row_cols."""
            rc = np.sort(row_cols)
            runs, run = [], [int(rc[0])]
            for c in rc[1:]:
                if int(c) - run[-1] <= 2:   # gap <= 2px = same run
                    run.append(int(c))
                else:
                    runs.append(run)
                    run = [int(c)]
            runs.append(run)
            widest = max(runs, key=len)
            return int(widest[0])           # leftmost col of widest run

        br_min = int(body_rows.min())
        br_max = int(body_rows.max())
        br_span = br_max - br_min

        # Use the INFERIOR 20-50% of body rows for AP reference.
        # T12 overlap and L1 spinous contamination always appear at the TOP
        # of the L1 label (high row = superior). The inferior body is clean.
        mid_lo = br_min + int(0.20 * br_span)
        mid_hi = br_min + int(0.50 * br_span)
        mid_band = body_rows[(body_rows >= mid_lo) & (body_rows <= mid_hi)]
        if len(mid_band) == 0:
            mid_band = body_rows  # fallback: use all body rows

        mid_body_cols = []
        for r in mid_band:
            rc = cols[rows == r]
            if len(rc) > 0:
                mid_body_cols.append(_widest_run_min_col_A(rc))

        if len(mid_body_cols) >= 3:
            arr = np.array(mid_body_cols)
            q25, q75 = np.percentile(arr, [25, 75])
            iqr = max(q75 - q25, 1.0)
            ok  = arr <= q75 + 1.5 * iqr   # remove only anterior outliers
            posterior_col = int(arr[ok].min() if ok.sum() >= 1 else arr.min())
        elif mid_body_cols:
            posterior_col = int(min(mid_body_cols))
        else:
            posterior_col = int(centroid_col)

        # --- SI row: use IQR filter on per-row spans to exclude T12 contamination ---
        # T12 overlap rows are anomalously wide; spinous rows are narrow (already
        # filtered by the 30% threshold above). Rows with span > Q75+1.5*IQR are
        # likely merged T12 voxels — exclude them, then take the highest remaining row.
        row_spans = np.array([row_span_d[r] for r in body_rows])
        sp_q25, sp_q75 = np.percentile(row_spans, [25, 75])
        sp_iqr = max(sp_q75 - sp_q25, 1.0)
        sp_hi_limit = sp_q75 + 1.5 * sp_iqr
        clean_rows = body_rows[row_spans <= sp_hi_limit]
        if len(clean_rows) == 0:
            clean_rows = body_rows  # fallback
        endplate_row = int(clean_rows.max())
        log.debug("    PointA SI: body_rows.max=%d, clean_rows.max=%d (span IQR filter, sp_hi_limit=%.1f)",
                  br_max, endplate_row, sp_hi_limit)

    else:
        # For Point B (inferior endplate): use mid-body stable posterior wall
        mid_lo2 = body_rows[len(body_rows)//4]
        mid_hi2 = body_rows[3*len(body_rows)//4]
        mid_body_cols = []
        for r in body_rows[(body_rows >= mid_lo2) & (body_rows <= mid_hi2)]:
            rc = cols[rows == r]
            bc = rc[rc >= centroid_col]
            if len(bc) > 0:
                mid_body_cols.append(int(bc.min()))
        posterior_col = int(np.median(mid_body_cols)) if mid_body_cols else int(centroid_col)

    c_idx = int(np.clip(posterior_col, 0, ncols - 1))
    r_idx = int(np.clip(endplate_row,  0, nrows - 1))

    return np.array([float(sl._col_to_ap_mm[c_idx]),
                     float(sl._row_to_si_mm[r_idx])])


def get_s2_inferior_endplate(sl, ct_vol=None) -> Optional[np.ndarray]:
    """
    Posterior point of the S2 inferior endplate (S2-S3 junction).

    S2-S3 consistently falls at 30% down from the top of the sacrum label
    (validated on gold-standard cases 71, 468, 761).

    Point B posterior col uses a WIDEST-RUN strategy: at each row in the
    S2/S3 band, find all contiguous pixel runs and select the widest one.
    The sacral body always produces the widest run; the sacral spinous
    process produces a narrow separate run to the left. Taking the minimum
    col of the widest run gives the posterior body wall, not the spinous tip.
    """
    from scipy import ndimage as _ndi

    img   = sl.img
    nrows = sl.nrows
    ncols = sl.ncols

    sacrum_mask = (img == SACRUM_LABEL).astype(np.uint8)
    labeled, n  = _ndi.label(sacrum_mask)
    if n == 0:
        return None

    sizes   = [np.sum(labeled == i) for i in range(1, n + 1)]
    largest = int(np.argmax(sizes)) + 1
    locs    = np.argwhere(labeled == largest)
    rows    = locs[:, 0]
    cols    = locs[:, 1]

    row_top  = int(rows.max())
    row_bot  = int(rows.min())
    row_span = row_top - row_bot

    centroid_col = float(cols.mean())

    s2s3_row = row_top - int(0.30 * row_span)
    log.debug("    S2-S3 junction (anat 30%%): row=%d", s2s3_row)

    def _widest_run_min_col(row_cols):
        """Min col of the widest contiguous pixel run in sorted row_cols."""
        rc = np.sort(row_cols)
        runs, run = [], [int(rc[0])]
        for c in rc[1:]:
            if int(c) - run[-1] <= 2:   # gap <= 2px = same run
                run.append(int(c))
            else:
                runs.append(run)
                run = [int(c)]
        runs.append(run)
        widest = max(runs, key=len)
        return int(widest[0])           # leftmost col = posterior body wall

    band_posterior_cols = []
    for rr in range(max(int(rows.min()), s2s3_row - 5),
                    min(int(rows.max()), s2s3_row + 5) + 1):
        rc_r = cols[rows == rr]
        if len(rc_r) == 0:
            continue
        band_posterior_cols.append(_widest_run_min_col(rc_r))

    if band_posterior_cols:
        arr = np.array(band_posterior_cols)
        # Remove only anterior outliers, then take the most posterior value
        q25, q75 = np.percentile(arr, [25, 75])
        iqr = max(q75 - q25, 1.0)
        ok  = arr <= q75 + 1.5 * iqr
        posterior_col = int(arr[ok].min() if ok.sum() >= 1 else arr.min())
    else:
        dists = np.abs(rows - s2s3_row)
        nearest = rows[np.argmin(dists)]
        rc = cols[rows == nearest]
        posterior_col = int(rc.min()) if len(rc) > 0 else int(centroid_col)

    c_idx = int(np.clip(posterior_col, 0, ncols - 1))
    r_idx = int(np.clip(s2s3_row,     0, nrows - 1))

    return np.array([float(sl._col_to_ap_mm[c_idx]),
                     float(sl._row_to_si_mm[r_idx])])


def _posterior_centroid_slice(sl, label: int,
                               si_frac_lo: float = 0.0,
                               si_frac_hi: float = 1.0,
                               post_frac:  float = 0.25) -> Optional[np.ndarray]:
    """
    Mid-body posterior wall for arc points.
    Same logic as get_endplate_point: find centroid, scan left from centroid
    at the centroid row to find the body's left (posterior) edge.
    Returns that posterior col at the centroid SI height.
    """
    img   = sl.img
    nrows = sl.nrows
    ncols = sl.ncols
    si_mm = sl._row_to_si_mm

    si_lo = si_mm[0] + si_frac_lo * (si_mm[-1] - si_mm[0])
    si_hi = si_mm[0] + si_frac_hi * (si_mm[-1] - si_mm[0])
    row_in_band = np.where((si_mm >= si_lo) & (si_mm <= si_hi))[0]
    if len(row_in_band) == 0:
        row_in_band = np.arange(nrows)

    locs = []
    for r in row_in_band:
        for c in np.where(img[r, :] == label)[0]:
            locs.append((r, c))

    if len(locs) < 5:
        return None

    locs = np.array(locs)
    centroid_row = int(round(float(locs[:, 0].mean())))
    centroid_col = float(locs[:, 1].mean())

    # Arc point = left edge of body at centroid row.
    # Body cols = those >= centroid_col (right half, no spinous process).
    # Posterior wall = minimum of those body cols.
    row_cols = locs[locs[:, 0] == centroid_row][:, 1]
    if len(row_cols) == 0:
        # fallback: use all rows near centroid
        near = locs[np.abs(locs[:, 0] - centroid_row) <= 3][:, 1]
        row_cols = near if len(near) > 0 else locs[:, 1]

    # Use per-row min-col >= centroid_col, median across all band rows
    # for a stable posterior wall (same method as Point A)
    per_row_left = []
    for rr in np.unique(locs[:, 0]):
        rc = locs[locs[:, 0] == rr][:, 1]
        bc = rc[rc >= centroid_col]
        if len(bc) > 0:
            per_row_left.append(int(bc.min()))
    if per_row_left:
        posterior_col = int(np.median(per_row_left))
    else:
        posterior_col = int(centroid_col)

    c_idx = int(np.clip(posterior_col, 0, ncols - 1))
    r_idx = int(np.clip(centroid_row,  0, nrows - 1))

    return np.array([float(sl._col_to_ap_mm[c_idx]),
                     float(sl._row_to_si_mm[r_idx])])

def get_l5_posterior_midpoint(sl) -> Optional[np.ndarray]:
    """
    Midpoint of the posterior cortical border of L5.

    Steps:
    1. Isolate L5 label pixels.
    2. Use centroid_col as body/arch divider.
    3. For each row, find the minimum col >= centroid_col (posterior body wall).
    4. Find the SUPERIOR endpoint: topmost row with a valid posterior body col.
    5. Find the INFERIOR endpoint: bottommost row with a valid posterior body col.
    6. Return the midpoint (average row, average col) of those two endpoints.
    """
    img   = sl.img
    nrows = sl.nrows
    ncols = sl.ncols

    locs = np.argwhere(img == 5)  # L5
    if len(locs) < 5:
        return None

    rows = locs[:, 0]
    cols = locs[:, 1]

    # Centroid col — body interior anchor
    centroid_col = float(cols.mean())

    # Per-row posterior body col (min col >= centroid_col)
    valid_rows = []
    valid_cols = []
    for r in np.unique(rows):
        rc = cols[rows == r]
        bc = rc[rc >= centroid_col]
        if len(bc) > 0:
            valid_rows.append(r)
            valid_cols.append(int(bc.min()))

    if len(valid_rows) < 3:
        return None

    valid_rows = np.array(valid_rows)
    valid_cols = np.array(valid_cols)

    # Remove outlier cols (osteophytes = isolated extreme values)
    q25, q75 = np.percentile(valid_cols, [25, 75])
    iqr = max(q75 - q25, 1.0)
    ok  = (valid_cols >= q25 - 1.5*iqr) & (valid_cols <= q75 + 1.5*iqr)
    if ok.sum() >= 3:
        valid_rows = valid_rows[ok]
        valid_cols = valid_cols[ok]

    # Superior endpoint = topmost row, inferior endpoint = bottommost row
    sup_idx = int(np.argmax(valid_rows))   # highest row = most superior
    inf_idx = int(np.argmin(valid_rows))   # lowest row  = most inferior

    sup_row, sup_col = valid_rows[sup_idx], valid_cols[sup_idx]
    inf_row, inf_col = valid_rows[inf_idx], valid_cols[inf_idx]

    # Midpoint
    mid_row = int(round((sup_row + inf_row) / 2.0))
    mid_col = int(round((sup_col + inf_col) / 2.0))

    c_idx = int(np.clip(mid_col, 0, ncols - 1))
    r_idx = int(np.clip(mid_row, 0, nrows - 1))

    return np.array([float(sl._col_to_ap_mm[c_idx]),
                     float(sl._row_to_si_mm[r_idx])])


def vertebra_centroid_world(mask: np.ndarray,
                             label: int,
                             affine: np.ndarray,
                             si_frac_lo: float = 0.0,
                             si_frac_hi: float = 1.0) -> Optional[np.ndarray]:
    """Full-width centroid (used for coronal deviation and arc ordering)."""
    coords = np.argwhere(mask == label).astype(np.float64)
    if coords.shape[0] < 5:
        return None
    world  = voxels_to_world(coords, affine)
    si     = world[:, 2]
    si_min, si_max = si.min(), si.max()
    si_lo  = si_min + si_frac_lo * (si_max - si_min)
    si_hi  = si_min + si_frac_hi * (si_max - si_min)
    keep   = (si >= si_lo) & (si <= si_hi)
    if keep.sum() < 3:
        keep = np.ones(len(si), dtype=bool)
    return np.array([float(world[keep, 1].mean()),
                     float(world[keep, 2].mean())])


def endplate_centroid(mask: np.ndarray,
                      label: int,
                      affine: np.ndarray,
                      which: str = "superior",
                      frac: float = 0.12,
                      ap_sgn: int = 1,
                      sl=None) -> Optional[np.ndarray]:
    """
    Centroid of the POSTERIOR edge of an endplate surface.
    Uses slice-based posterior detection (col=0 = posterior) when sl is provided.
    """
    si_frac_lo = (1.0 - frac) if which == "superior" else 0.0
    si_frac_hi = 1.0           if which == "superior" else frac
    if sl is not None:
        return _posterior_centroid_slice(sl, label,
                                          si_frac_lo=si_frac_lo,
                                          si_frac_hi=si_frac_hi,
                                          post_frac=0.30)
    coords = np.argwhere(mask == label).astype(np.float64)
    if coords.shape[0] < 10:
        return None
    world  = voxels_to_world(coords, affine)
    si     = world[:, 2]
    si_min, si_max = si.min(), si.max()
    height = si_max - si_min
    if height < 1.0:
        return None
    si_lo = si_min + si_frac_lo * height
    si_hi = si_min + si_frac_hi * height
    keep  = (si >= si_lo) & (si <= si_hi)
    if keep.sum() < 3:
        keep = np.ones(len(si), dtype=bool)
    ep_world  = world[keep]
    post_keep = _posterior_world_ap(ep_world, frac=0.30)
    final     = ep_world[post_keep] if post_keep.sum() >= 3 else ep_world
    return np.array([float(final[:, 1].mean()), float(final[:, 2].mean())])


# ─────────────────────────────────────────────────────────────────────────────
# Mid-sagittal slice for visualisation
# ─────────────────────────────────────────────────────────────────────────────

class SagittalSlice:
    """
    Extracts the mid-sagittal 2-D slice and provides bidirectional mapping
    between world (AP_mm, SI_mm) and display pixel (col, row).

    Orientation guarantee:
      row 0   = most inferior  → displayed at bottom with origin='lower'
      row N-1 = most superior  → displayed at top
      col 0   = left edge of display  (nominal posterior)
      col N-1 = right edge
    """

    def __init__(self, mask: np.ndarray, affine: np.ndarray):
        self.mask   = mask
        self.affine = affine

        self.lr_ax, self.lr_sgn = axis_for_world_dim(affine, 0)
        self.ap_ax, self.ap_sgn = axis_for_world_dim(affine, 1)
        self.si_ax, self.si_sgn = axis_for_world_dim(affine, 2)

        # Mid-sagittal = slice with most spine-label voxels
        spine = np.isin(mask, ALL_SPINE_LBLS).astype(np.float32)
        prof  = spine.sum(axis=tuple(i for i in range(3) if i != self.lr_ax))
        self.lr_idx = int(np.argmax(prof))

        # Extract 2-D slice
        slicer             = [slice(None)] * 3
        slicer[self.lr_ax] = self.lr_idx
        raw                = mask[tuple(slicer)]     # shape (dim_a, dim_b)

        free      = [d for d in range(3) if d != self.lr_ax]
        ap_local  = free.index(self.ap_ax)
        si_local  = free.index(self.si_ax)

        # Transpose → (SI_vox, AP_vox)
        arr = raw.copy() if (si_local == 0 and ap_local == 1) else raw.T.copy()

        # Build per-row SI world mm lookup (row → SI mm)
        n_si = arr.shape[0]
        si_vox_range = np.arange(n_si)

        si_ijks = np.zeros((n_si, 3))
        si_ijks[:, self.lr_ax] = self.lr_idx
        si_ijks[:, self.ap_ax] = 0
        si_ijks[:, self.si_ax] = si_vox_range
        si_world_vals = voxels_to_world(si_ijks, affine)[:, 2]   # Z = SI

        # Sort rows so row 0 = minimum SI = most inferior
        row_order = np.argsort(si_world_vals)
        arr = arr[row_order, :]
        self._row_to_si_mm = si_world_vals[row_order]

        # Build per-col AP world mm lookup (col → AP mm)
        n_ap = arr.shape[1]
        ap_vox_range = np.arange(n_ap)

        ap_ijks = np.zeros((n_ap, 3))
        ap_ijks[:, self.lr_ax] = self.lr_idx
        ap_ijks[:, self.ap_ax] = ap_vox_range
        ap_ijks[:, self.si_ax] = 0
        ap_world_vals = voxels_to_world(ap_ijks, affine)[:, 1]   # Y = AP

        # Sort cols so col 0 = minimum AP = most posterior (in RAS, smaller Y = more posterior)
        col_order = np.argsort(ap_world_vals)
        arr = arr[:, col_order]
        self._col_to_ap_mm = ap_world_vals[col_order]

        self.img        = arr
        self.nrows      = arr.shape[0]
        self.ncols      = arr.shape[1]
        # Store transform orders so CT can use the same reordering
        self._row_order = row_order
        self._col_order = col_order
        self._si_local  = si_local
        self._ap_local  = ap_local

    def world_to_pix(self, ap_mm: float, si_mm: float) -> Tuple[float, float]:
        """World (AP_mm, SI_mm) → display (col, row). Always on-image."""
        col = float(np.argmin(np.abs(self._col_to_ap_mm - ap_mm)))
        row = float(np.argmin(np.abs(self._row_to_si_mm - si_mm)))
        return col, row

    def slice_to_world(self, col: float, row: float) -> Tuple[float, float]:
        """Display (col, row) → world (AP_mm, SI_mm) via lookup tables."""
        c = int(np.clip(round(col), 0, self.ncols - 1))
        r = int(np.clip(round(row), 0, self.nrows - 1))
        return float(self._col_to_ap_mm[c]), float(self._row_to_si_mm[r])

    def get_ct_slice(self, ct_vol: np.ndarray) -> np.ndarray:
        """
        Extract and orient the CT mid-sagittal slice using the IDENTICAL
        row/col transforms applied to the label slice.  This guarantees
        pixel-perfect alignment between CT underlay and label overlay.
        Returns a 2-D float32 array (nrows, ncols).
        """
        slicer             = [slice(None)] * 3
        slicer[self.lr_ax] = self.lr_idx
        raw                = ct_vol[tuple(slicer)].astype(np.float32)

        # Same transpose as label
        if self._si_local == 0 and self._ap_local == 1:
            arr = raw.copy()
        else:
            arr = raw.T.copy()

        # Same row and col reordering as label
        arr = arr[self._row_order, :]
        arr = arr[:, self._col_order]
        return arr

    def oriented_rgba(self, vtx_colors: Dict) -> np.ndarray:
        """Build RGBA from self.img using provided colour dict."""
        rgba = np.zeros((*self.img.shape, 4), dtype=float)
        for lbl, col in vtx_colors.items():
            rgba[self.img == lbl] = (*col[:3], 0.88)
        for h in HIP_LABELS:
            rgba[self.img == h] = (0.5, 0.5, 0.5, 0.4)
        return rgba

    def build_rgba(self) -> Tuple[np.ndarray, Dict]:
        cmap       = _get_cmap("tab10")
        vtx_colors = {lbl: cmap(i / 10) for i, lbl in enumerate(LABEL_MAP)}
        rgba       = np.zeros((*self.img.shape, 4), dtype=float)
        for lbl, col in vtx_colors.items():
            rgba[self.img == lbl] = (*col[:3], 0.88)
        for h in HIP_LABELS:
            rgba[self.img == h] = (0.5, 0.5, 0.5, 0.4)
        return rgba, vtx_colors


# ─────────────────────────────────────────────────────────────────────────────
# TRALL computation — Chernukha method
# ─────────────────────────────────────────────────────────────────────────────

def compute_trall(mask: np.ndarray,
                  affine: np.ndarray,
                  sl: SagittalSlice,
                  ct_vol: Optional[np.ndarray] = None) -> Dict:
    """
    TRALL (Chernukha method):
      A     = posterior wall of L1 superior endplate
      B     = posterior wall of sacrum at S2/S3 level
      arc   = smooth curve through posterior body walls L1→L2→L3→L4→L5→Sacrum
      chord = straight line A→B
      C     = point on arc with greatest perpendicular distance from chord
      TRALL = angle at C in triangle A-C-B

    All arc points use the SAME LR-width method as A and B, computed on the
    full vertebra height (not just endplate bands), so the spline control
    points are consistent and the curve is smooth.
    """
    from scipy.interpolate import make_interp_spline

    out = dict(trall_deg=None, A=None, B=None, C=None,
               arc_pts=None, arc_pix=None,
               upper_vec=None, lower_vec=None,
               arc_spline_pts=None)

    ap_sgn = sl.ap_sgn

    # ── Step 1: compute posterior body-wall point for every vertebra ──────
    # Use the FULL vertebra height (si_frac 0→1) for intermediate arc points.
    # Use TOP 25% for A (L1 superior endplate) and
    #     MIDDLE of sacrum for B (S2/S3 level ≈ 45-65% from top of sacrum).
    # All use _posterior_centroid_slice (LR-width profile method).

    LABELS_ARC = [1, 2, 3, 4, 5]   # L1–L5 only; Sacrum excluded (B covers it)

    # A = posterior point on the SUPERIOR endplate of L1
    A = get_endplate_point(sl, L1_LABEL, 'superior')

    # B = posterior point of S2 inferior endplate (S2-S3 junction)
    # Use CT intensity to find the S2-S3 cortical line if available,
    # otherwise fall back to anatomical proportions.
    B = get_s2_inferior_endplate(sl, ct_vol=ct_vol)
    if B is None:
        B = get_endplate_point(sl, SACRUM_LABEL, 'inferior')

    # Intermediate arc points: full-height posterior wall of each vertebra
    arc_world, arc_pix_list, arc_lbl = [], [], []
    for lbl in LABELS_ARC:
        if lbl == 5:
            # L5 is wedge-shaped and tilted. Strategy:
            #   SI position (row): use the MID-BODY band (20%–80% of L5 height)
            #     centroid, so the dot lands inside the vertebral body, NOT in
            #     the disc space below it.
            #   AP position (col): for each row in the MIDDLE 50% of L5 height
            #     (25%–75%), find the leftmost col of the rightmost contiguous
            #     pixel run (= posterior cortex of body, excluding spinous process).
            #     Use the median across rows — robust against the wedge tilt.
            img_s = sl.img
            nrows = sl.nrows
            ncols = sl.ncols

            all_locs = np.array([(r, c)
                                  for r in range(nrows)
                                  for c in np.where(img_s[r, :] == 5)[0]])
            if len(all_locs) < 5:
                pt = None
            else:
                all_rows = all_locs[:, 0]
                row_min = int(all_rows.min())
                row_max = int(all_rows.max())
                row_span_l5 = max(row_max - row_min, 1)

                # --- SI: centroid of mid-body band 20%–80% ---
                si_lo = row_min + int(0.20 * row_span_l5)
                si_hi = row_min + int(0.80 * row_span_l5)
                si_band_mask = (all_rows >= si_lo) & (all_rows <= si_hi)
                si_band_locs = all_locs[si_band_mask]
                if len(si_band_locs) < 3:
                    si_band_locs = all_locs
                centroid_row = int(round(float(si_band_locs[:, 0].mean())))

                # --- AP: rightmost-run posterior edge in middle 25%–75% band ---
                ap_lo = row_min + int(0.25 * row_span_l5)
                ap_hi = row_min + int(0.75 * row_span_l5)
                ap_band_mask = (all_rows >= ap_lo) & (all_rows <= ap_hi)
                ap_band_locs = all_locs[ap_band_mask]
                if len(ap_band_locs) < 5:
                    ap_band_locs = all_locs

                ap_rows = ap_band_locs[:, 0]
                per_row_left = []
                for rr in np.unique(ap_rows):
                    rc = np.sort(ap_band_locs[ap_rows == rr, 1])
                    if len(rc) < 2:
                        continue
                    # Find rightmost contiguous run (gap <= 3px) = vertebral body
                    runs, run = [], [int(rc[0])]
                    for c in rc[1:]:
                        if int(c) - run[-1] <= 3:
                            run.append(int(c))
                        else:
                            runs.append(run)
                            run = [int(c)]
                    runs.append(run)
                    body_run = runs[-1]  # rightmost run = body (not spinous process)
                    per_row_left.append(min(body_run))

                if per_row_left:
                    arr = np.array(per_row_left)
                    q25, q75 = np.percentile(arr, [25, 75])
                    iqr = max(q75 - q25, 1.0)
                    ok  = (arr >= q25 - 1.5*iqr) & (arr <= q75 + 1.5*iqr)
                    clean = arr[ok] if ok.sum() >= 3 else arr
                    # Median across the mid-body rows = stable posterior wall col
                    posterior_col = int(np.median(clean))
                    c_idx = int(np.clip(posterior_col, 0, ncols - 1))
                    r_idx = int(np.clip(centroid_row,  0, nrows - 1))
                    pt = np.array([float(sl._col_to_ap_mm[c_idx]),
                                   float(sl._row_to_si_mm[r_idx])])
                else:
                    pt = None
        else:
            pt = _posterior_centroid_slice(sl, lbl,
                                            si_frac_lo=0.10, si_frac_hi=0.90)
        if pt is not None:
            arc_world.append(pt)
            arc_pix_list.append(sl.world_to_pix(pt[0], pt[1]))
            arc_lbl.append(lbl)
            log.debug("    post.cent %s: AP=%.1f mm  SI=%.1f mm", LABEL_MAP.get(lbl, str(lbl)), pt[0], pt[1])
        else:
            log.debug("    post.cent %s: NOT FOUND", LABEL_MAP.get(lbl, str(lbl)))

    if len(arc_world) < 3:
        log.warning("Too few arc landmarks for TRALL.")
        return out

    arc_world   = np.array(arc_world)
    arc_pix_arr = np.array(arc_pix_list)

    # Sort superior → inferior (descending SI)
    order       = np.argsort(arc_world[:, 1])[::-1]
    arc_world   = arc_world[order]
    arc_pix_arr = arc_pix_arr[order]
    arc_lbl     = [arc_lbl[i] for i in order]

    # Fallbacks if A or B failed
    if A is None:
        A = arc_world[0].copy()
    if B is None:
        B = arc_world[-1].copy()

    out["arc_pts"] = arc_world
    out["arc_pix"] = arc_pix_arr
    out["A"]       = A
    out["B"]       = B
    out["A_pix"]   = sl.world_to_pix(A[0], A[1])
    out["B_pix"]   = sl.world_to_pix(B[0], B[1])

    log.debug("    A (L1 sup.): AP=%.1f  SI=%.1f", A[0], A[1])
    log.debug("    B (S2/S3 jct): AP=%.1f  SI=%.1f", B[0], B[1])

    # ── Step 2: chord A→B ─────────────────────────────────────────────────
    chord     = B - A
    chord_len = np.linalg.norm(chord)
    if chord_len < 1e-6:
        return out
    chord_u = chord / chord_len

    # ── Step 3: build spline through A → arc_intermediates → B ───────────
    # Collect all control points, replacing the arc endpoints with A and B
    # so the spline is anchored to the true endplate positions.
    ctrl_pts = []
    ctrl_pts.append(A)
    for pt in arc_world:
        # Include intermediate arc points that aren't duplicates of A or B
        if np.linalg.norm(pt - A) > 2.0 and np.linalg.norm(pt - B) > 2.0:
            ctrl_pts.append(pt)
    ctrl_pts.append(B)

    ctrl_arr = np.array(ctrl_pts)

    # Sort by SI ascending and deduplicate (spline needs strictly increasing x)
    ctrl_arr = ctrl_arr[np.argsort(ctrl_arr[:, 1])]
    _, uid   = np.unique(np.round(ctrl_arr[:, 1], 1), return_index=True)
    ctrl_arr = ctrl_arr[uid]

    C              = None
    arc_spline_pts = None

    if len(ctrl_arr) >= 3:
        try:
            k        = min(3, len(ctrl_arr) - 1)
            si_vals  = ctrl_arr[:, 1]   # ascending SI mm
            ap_vals  = ctrl_arr[:, 0]
            spl      = make_interp_spline(si_vals, ap_vals, k=k)

            si_fine  = np.linspace(si_vals[0], si_vals[-1], 600)
            ap_fine  = spl(si_fine)
            dense    = np.column_stack([ap_fine, si_fine])   # [AP, SI]

            # Perpendicular distances from chord A→B
            PA_d     = dense - A
            proj_d   = PA_d @ chord_u
            perp_d   = PA_d - np.outer(proj_d, chord_u)
            dists_d  = np.linalg.norm(perp_d, axis=1)

            # Exclude first/last 3% (near A and B)
            margin   = max(1, int(0.03 * len(si_fine)))
            masked   = dists_d.copy()
            masked[:margin]  = -1
            masked[-margin:] = -1

            c_idx        = int(np.argmax(masked))
            C            = dense[c_idx].copy()
            arc_spline_pts = dense

            log.debug("    C (spline): AP=%.1f  SI=%.1f  dev=%.1f mm", C[0], C[1], dists_d[c_idx])
        except Exception as e:
            log.debug("    Spline failed: %s", e)

    # Fallback: C from discrete arc points
    if C is None:
        PA    = arc_world - A
        proj  = PA @ chord_u
        perp  = PA - np.outer(proj, chord_u)
        dists = np.linalg.norm(perp, axis=1)
        excl  = [i for i, pt in enumerate(arc_world)
                 if np.linalg.norm(pt - A) < 5 or np.linalg.norm(pt - B) < 5]
        masked2 = dists.copy()
        for i in excl: masked2[i] = -1
        if masked2.max() < 0: masked2 = dists.copy()
        c_idx = int(np.argmax(masked2))
        C     = arc_world[c_idx].copy()
        log.debug("    C (discrete): AP=%.1f  SI=%.1f  dev=%.1f mm", C[0], C[1], dists[c_idx])

    out["C"]             = C
    out["C_pix"]         = sl.world_to_pix(C[0], C[1])
    out["arc_spline_pts"] = arc_spline_pts
    log.debug("    C pix=%s", out['C_pix'])

    # ── Step 4: TRALL angle at C ──────────────────────────────────────────
    CA  = A - C;  CB  = B - C
    nCA = np.linalg.norm(CA);  nCB = np.linalg.norm(CB)
    if nCA < 1e-6 or nCB < 1e-6:
        return out

    out["upper_vec"] = CA / nCA
    out["lower_vec"] = CB / nCB
    cos_t = float(np.clip(np.dot(out["upper_vec"], out["lower_vec"]), -1.0, 1.0))
    out["trall_deg"] = float(np.degrees(np.arccos(abs(cos_t))))
    log.debug("    cos=%.3f  TRALL=%.1f deg", cos_t, out['trall_deg'])

    return out




# ─────────────────────────────────────────────────────────────────────────────
# Coronal curvature
# ─────────────────────────────────────────────────────────────────────────────

def max_coronal_deviation(mask: np.ndarray, affine: np.ndarray) -> Optional[float]:
    def cw(lbl):
        c = np.argwhere(mask == lbl).astype(np.float64)
        return voxels_to_world(c.mean(axis=0, keepdims=True), affine)[0] if c.size else None
    centroids = {l: cw(l) for l in ALL_SPINE_LBLS}
    centroids = {k: v for k, v in centroids.items() if v is not None}
    if L1_LABEL not in centroids or SACRUM_LABEL not in centroids:
        return None
    def cor(c): return np.array([c[1], c[2]])
    p1, p2 = cor(centroids[L1_LABEL]), cor(centroids[SACRUM_LABEL])
    ref = p2 - p1
    rlen = np.linalg.norm(ref)
    if rlen < 1e-6:
        return 0.0
    ru = ref / rlen
    devs = [float(np.linalg.norm(cor(c) - p1 - np.dot(cor(c) - p1, ru) * ru))
            for l, c in centroids.items() if l not in (L1_LABEL, SACRUM_LABEL)]
    return max(devs, default=0.0)


# ─────────────────────────────────────────────────────────────────────────────
# Visualisation
# ─────────────────────────────────────────────────────────────────────────────

def visualise_case(mask, affine, token, trall, sl, output_dir, ct_vol=None):
    cmap       = _get_cmap("tab10")
    vtx_colors = {lbl: cmap(i / 10) for i, lbl in enumerate(LABEL_MAP)}
    rgba = np.zeros((*sl.img.shape, 4), dtype=float)
    for lbl, col in vtx_colors.items():
        rgba[sl.img == lbl] = (*col[:3], 0.85)
    for h in HIP_LABELS:
        rgba[sl.img == h] = (0.5, 0.5, 0.5, 0.4)

    spine_rows = np.where(np.isin(sl.img, list(LABEL_MAP.keys())).any(axis=1))[0]
    spine_cols = np.where(np.isin(sl.img, list(LABEL_MAP.keys())).any(axis=0))[0]
    pad = 30
    r0 = max(0, spine_rows.min() - pad)
    r1 = min(sl.nrows, spine_rows.max() + pad)
    c0 = max(0, spine_cols.min() - pad)
    c1 = min(sl.ncols, spine_cols.max() + pad * 3)

    fig, (ax, ax_leg) = plt.subplots(1, 2, figsize=(9, 12),
                                      gridspec_kw={"width_ratios": [3, 1]})
    fig.patch.set_facecolor("#0d0d0d")

    if ct_vol is not None:
        try:
            ct_2d = sl.get_ct_slice(ct_vol)
            ct_2d = np.clip(ct_2d, -200, 1000)
            ct_2d = (ct_2d - ct_2d.min()) / (ct_2d.max() - ct_2d.min() + 1e-6)
            ax.imshow(ct_2d[r0:r1, c0:c1], origin="lower", aspect="auto",
                      cmap="gray", interpolation="bilinear", alpha=0.65, zorder=0)
            label_alpha = 0.70
        except Exception:
            label_alpha = 1.0
    else:
        ax.set_facecolor("#111111")
        label_alpha = 1.0

    ax.imshow(rgba[r0:r1, c0:c1], origin="lower", aspect="auto",
              interpolation="nearest", alpha=label_alpha, zorder=1)

    w2p = sl.world_to_pix
    def crop(pix):
        if pix is None: return None
        return (pix[0] - c0, pix[1] - r0)

    arc_pix = trall.get("arc_pix")
    A_pix   = crop(trall.get("A_pix"))
    B_pix   = crop(trall.get("B_pix"))
    C_pix   = crop(trall.get("C_pix"))
    A_world = trall.get("A")
    B_world = trall.get("B")
    C_world = trall.get("C")
    uv      = trall.get("upper_vec")
    lv      = trall.get("lower_vec")
    td      = trall.get("trall_deg")
    arc_spline_pts = trall.get("arc_spline_pts")   # dense (AP,SI) world-mm curve

    # ── Draw the arc (yellow curve) ────────────────────────────────────────
    # Prefer the dense spline sampled in world-mm (converted to pixels).
    # Fall back to re-spline from the sparse pixel landmarks.
    if arc_spline_pts is not None and len(arc_spline_pts) > 2:
        # Convert each dense world point to pixel and crop
        arc_cols = []
        arc_rows = []
        for pt in arc_spline_pts:
            px = crop(sl.world_to_pix(pt[0], pt[1]))
            arc_cols.append(px[0])
            arc_rows.append(px[1])
        ax.plot(arc_cols, arc_rows, color="#FFD700", lw=2.5, zorder=7, alpha=0.95)
    else:
        # Fallback: build spline from sparse landmark pixels
        spline_pix = []
        if A_pix is not None: spline_pix.append(A_pix)
        if arc_pix is not None:
            for p in arc_pix:
                cp = crop(p)
                if A_pix is not None and np.hypot(cp[0]-A_pix[0], cp[1]-A_pix[1]) < 8: continue
                if B_pix is not None and np.hypot(cp[0]-B_pix[0], cp[1]-B_pix[1]) < 8: continue
                spline_pix.append(cp)
        if B_pix is not None: spline_pix.append(B_pix)
        spline_pix.sort(key=lambda p: -p[1])
        if len(spline_pix) >= 3:
            from scipy.interpolate import make_interp_spline as _mks
            sp_r = np.array([p[1] for p in spline_pix], dtype=float)
            sp_c = np.array([p[0] for p in spline_pix], dtype=float)
            _, uid = np.unique(sp_r, return_index=True)
            sp_r, sp_c = sp_r[uid], sp_c[uid]
            if len(sp_r) >= 3:
                try:
                    spl = _mks(sp_r, sp_c, k=min(3, len(sp_r)-1))
                    t_fine = np.linspace(sp_r.min(), sp_r.max(), 500)
                    ax.plot(spl(t_fine), t_fine, color="#FFD700", lw=2.5, zorder=7, alpha=0.95)
                except Exception:
                    ax.plot([p[0] for p in spline_pix], [p[1] for p in spline_pix],
                            color="#FFD700", lw=2.5, zorder=7)

    if A_pix is not None and B_pix is not None:
        dx = B_pix[0]-A_pix[0]; dy = B_pix[1]-A_pix[1]; d = np.hypot(dx, dy)
        if d > 0.5:
            ux, uy = dx/d, dy/d
            ax.plot([A_pix[0]-ux*80, B_pix[0]+ux*80],
                    [A_pix[1]-uy*80, B_pix[1]+uy*80],
                    color="#ff4444", lw=1.8, ls="--", zorder=6, alpha=0.85)

    pix_uv = pix_lv = None
    if A_pix is not None and B_pix is not None and C_pix is not None:
        dx_u = A_pix[0]-C_pix[0]; dy_u = A_pix[1]-C_pix[1]
        dx_l = B_pix[0]-C_pix[0]; dy_l = B_pix[1]-C_pix[1]
        du = np.hypot(dx_u, dy_u); dl = np.hypot(dx_l, dy_l)
        if du > 0.5: pix_uv = (dx_u/du, dy_u/du)
        if dl > 0.5: pix_lv = (dx_l/dl, dy_l/dl)
        ext_past = 180; ext_back = 60
        for pv, ep in [(pix_uv, A_pix), (pix_lv, B_pix)]:
            if pv is None or ep is None: continue
            dist = np.hypot(ep[0]-C_pix[0], ep[1]-C_pix[1])
            ax.plot([C_pix[0]-pv[0]*ext_back, C_pix[0]+pv[0]*(dist+ext_past)],
                    [C_pix[1]-pv[1]*ext_back, C_pix[1]+pv[1]*(dist+ext_past)],
                    color="white", lw=2.0, zorder=9, alpha=0.90)

    if arc_pix is not None:
        ARC_LABELS_FULL = [1, 2, 3, 4, 5, 7]
        for i, p in enumerate(arc_pix):
            cp = crop(p)
            ax.plot(cp[0], cp[1], "o", color="#FFEE00", markersize=9,
                    markeredgecolor="black", markeredgewidth=1.2, zorder=10)
            lbl = ARC_LABELS_FULL[i] if i < len(ARC_LABELS_FULL) else 0
            ax.text(cp[0]+5, cp[1], LABEL_MAP.get(lbl, ""), color="#FFEE00",
                    fontsize=7, fontweight="bold", zorder=11)

    for pix, lbl_txt in [(A_pix, "A  (L1 sup.)"), (B_pix, "B  (S2/S3)")]:
        if pix is None: continue
        ax.plot(*pix, "D", color="white", markersize=8, markeredgecolor="black", zorder=12)
        ax.text(pix[0]+7, pix[1], lbl_txt, color="white", fontsize=7,
                fontweight="bold", va="center",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="black", alpha=0.65), zorder=13)

    if C_pix is not None:
        ax.plot(*C_pix, "o", color="limegreen", markersize=12,
                markeredgecolor="black", markeredgewidth=1.5, zorder=11)
        ax.text(C_pix[0]+7, C_pix[1]+3, "C  (apex)", color="limegreen", fontsize=7,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="black", alpha=0.6), zorder=13)

    if C_world is not None and A_world is not None and B_world is not None:
        cv = B_world - A_world; cl = np.linalg.norm(cv)
        if cl > 1e-6:
            cu = cv / cl
            t  = float(np.dot(C_world - A_world, cu))
            fp = A_world + t * cu
            fp_pix = crop(w2p(fp[0], fp[1]))
            ax.plot([C_pix[0], fp_pix[0]], [C_pix[1], fp_pix[1]],
                    color="limegreen", lw=1.4, ls=":", alpha=0.85, zorder=9)
            ax.plot(*fp_pix, "s", color="limegreen", markersize=5, zorder=10)

    arc_radius = (r1 - r0) * 0.06
    if C_pix is not None and td is not None and pix_uv is not None and pix_lv is not None:
        ang_u = float(np.degrees(np.arctan2(pix_uv[1], pix_uv[0]))) % 360
        ang_l = float(np.degrees(np.arctan2(pix_lv[1], pix_lv[0]))) % 360
        cands = [(ang_u,(ang_l-ang_u)%360),(ang_l,(ang_u-ang_l)%360),
                 ((ang_u+180)%360,(ang_l-ang_u-180)%360),
                 ((ang_l+180)%360,(ang_u-ang_l-180)%360)]
        valid = [(t1,sp) for t1,sp in cands if 0 < sp <= 180]
        if not valid: valid = cands
        t1b, spb = min(valid, key=lambda x: x[1])
        ax.add_patch(mpatches.Wedge((C_pix[0],C_pix[1]), r=arc_radius,
                                     theta1=t1b, theta2=t1b+spb,
                                     facecolor="orange", alpha=0.40,
                                     edgecolor="orange", lw=2.0, zorder=12))
        mar = np.radians(t1b + spb/2)
        tr  = arc_radius * 2.2
        ax.text(C_pix[0]+tr*np.cos(mar), C_pix[1]+tr*np.sin(mar),
                f"{td:.1f}\u00b0", color="orange", fontsize=10, fontweight="bold",
                ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#0a0a0a",
                          alpha=0.82, edgecolor="orange", lw=1.2), zorder=15)

    ax.set_xlim(0, c1-c0); ax.set_ylim(0, r1-r0)
    ax.set_xlabel("P \u2192 A  (Posterior \u2192 Anterior)", fontsize=9, color="white")
    ax.set_ylabel("I \u2192 S  (Inferior \u2192 Superior)", fontsize=9, color="white")
    ax.tick_params(colors="white")
    ax.set_facecolor("#0d0d0d")
    for sp in ax.spines.values(): sp.set_edgecolor("#444444")

    ax_leg.set_facecolor("#0d0d0d")
    ax_leg.axis("off")
    patches = [mpatches.Patch(color=vtx_colors[l], label=n) for l,n in LABEL_MAP.items()]
    patches += [mpatches.Patch(color=(0.5,0.5,0.5), label="Hip"),
                mlines.Line2D([],[],color="#FFD700",lw=2.5,label="Arc (post. bodies)"),
                mlines.Line2D([],[],color="#ff4444",lw=1.8,ls="--",label="Chord A\u2192B"),
                mlines.Line2D([],[],color="#FFEE00",lw=0,marker="o",markersize=8,
                              markeredgecolor="black",label="Vertebral landmark"),
                mlines.Line2D([],[],color="limegreen",lw=0,marker="o",markersize=9,label="C (apex)"),
                mlines.Line2D([],[],color="white",lw=2.0,label="Lines C\u2192A / C\u2192B"),
                mlines.Line2D([],[],color="limegreen",lw=1.4,ls=":",label="Max deviation \u22a5"),
                mpatches.Patch(facecolor="orange",alpha=0.4,edgecolor="orange",label="TRALL angle")]
    leg = ax_leg.legend(handles=patches, loc="upper left", fontsize=7.5,
                       framealpha=0.0)
    for text in leg.get_texts():
        text.set_color("white")

    td_str = f"{td:.1f}" if td is not None else "N/A"
    a_str  = f"({A_world[0]:.1f}, {A_world[1]:.1f})" if A_world is not None else "N/A"
    b_str  = f"({B_world[0]:.1f}, {B_world[1]:.1f})" if B_world is not None else "N/A"
    c_str  = f"({C_world[0]:.1f}, {C_world[1]:.1f})" if C_world is not None else "N/A"
    stats  = "TRALL\n\n" + td_str + "\u00b0\n\nLandmarks\n\nA: " + a_str
    stats += "\nB: " + b_str + "\nC: " + c_str + "\n\n[AP mm, SI mm]"
    ax_leg.text(0.0, 0.28, stats, transform=ax_leg.transAxes, fontsize=8,
                color="white", va="top",
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#1a1a1a",
                          edgecolor="#444444", alpha=0.9))

    title = f"Case: {token}  \u2014  TRALL Lumbar Lordosis\nTRALL = {td_str}\u00b0"
    fig.suptitle(title, fontsize=11, color="white", y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.97])

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    out_path = Path(output_dir) / f"{token}_sagittal.png"
    fig.savefig(str(out_path), dpi=100, facecolor=fig.get_facecolor())
    plt.close(fig)
    plt.close('all')  # force-close any stray figures to prevent memory leak
    import gc; gc.collect()
    log.debug("[%s] figure saved -> %s", token, out_path)


# ─────────────────────────────────────────────────────────────────────────────
# Per-case pipeline
# ─────────────────────────────────────────────────────────────────────────────

def process_case(case, visualize=False, vis_dir=".") -> Dict:
    t_start = time.time()
    mask, affine = load_label_and_affine(case)
    token  = case.token
    config = case.config
    split  = case.split

    log.debug("[%s] config=%s  split=%s", token, config, split)
    log.debug("[%s] mask shape=%s  dtype=%s", token, mask.shape, mask.dtype)

    sl = SagittalSlice(mask, affine)
    log.debug("[%s] axes: LR=ax%d(%+d) AP=ax%d(%+d) SI=ax%d(%+d)",
              token, sl.lr_ax, sl.lr_sgn, sl.ap_ax, sl.ap_sgn, sl.si_ax, sl.si_sgn)
    log.debug("[%s] mid-sag: ax=%d idx=%d img=%s",
              token, sl.lr_ax, sl.lr_idx, sl.img.shape)

    present = [l for l in ALL_SPINE_LBLS if np.any(mask == l)]
    log.debug("[%s] labels present: %s", token, [LABEL_MAP[l] for l in present])

    # ── Sacrum presence check ─────────────────────────────────────────────────
    sacrum_voxels = int(np.sum(mask == SACRUM_LABEL))
    if sacrum_voxels == 0:
        log.warning("[%s] SKIP — no sacrum label in mask (config=%s). "
                    "TRALL cannot be computed.", token, config)
        return {
            "token":  token,
            "split":  split,
            "config": config,
            "trall_angle_deg":            "NO_SACRUM",
            "max_coronal_deviation_mm":   "",
            "landmark_A_AP_SI_mm":        "N/A",
            "landmark_B_AP_SI_mm":        "N/A",
            "landmark_C_AP_SI_mm":        "N/A",
        }
    log.debug("[%s] sacrum voxels: %d", token, sacrum_voxels)
    # ─────────────────────────────────────────────────────────────────────────

    ct_vol_trall = None
    try:
        ct_arr, _ = case.load_ct()
        ct_vol_trall = ct_arr
    except Exception as exc:
        log.debug("[%s] CT load failed (label-only mode): %s", token, exc)

    trall = compute_trall(mask, affine, sl, ct_vol=ct_vol_trall)
    td = trall["trall_deg"]

    def fmt(pt): return f"({pt[0]:.1f},{pt[1]:.1f})" if pt is not None else "N/A"

    if td is not None:
        log.debug("[%s] TRALL=%.2f deg", token, td)
    else:
        log.warning("[%s] TRALL could not be computed.", token)

    cd = max_coronal_deviation(mask, affine)
    if cd is not None:
        log.debug("[%s] coronal dev=%.2f mm", token, cd)

    if visualize:
        visualise_case(mask, affine, token, trall, sl, vis_dir,
                       ct_vol=ct_vol_trall)

    log.debug("[%s] done in %.1f s", token, time.time() - t_start)

    return {
        "token":  token,
        "split":  split,
        "config": config,
        "trall_angle_deg": round(td, 4) if td is not None else "",
        "max_coronal_deviation_mm": round(cd, 4) if cd is not None else "",
        "landmark_A_AP_SI_mm": fmt(trall.get("A")),
        "landmark_B_AP_SI_mm": fmt(trall.get("B")),
        "landmark_C_AP_SI_mm": fmt(trall.get("C")),
    }


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

_pbar_lock = threading.Lock()
_pbar_ref  = None   # set to the active tqdm bar in main()


def _process_case_worker(case, visualize=False, vis_dir=".") -> dict:
    """Thread-safe wrapper: runs process_case and ticks the progress bar."""
    result = process_case(case, visualize=visualize, vis_dir=vis_dir)
    with _pbar_lock:
        if _pbar_ref is not None:
            td = result.get("trall_angle_deg", "")
            status = f"{td:.1f}°" if isinstance(td, float) else str(td)
            _pbar_ref.set_postfix_str(f"{case.token} -> {status}", refresh=True)
            _pbar_ref.update(1)
    return result


def main(argv=None):
    global _pbar_ref, log

    ap = argparse.ArgumentParser(
        description="TRALL Lordosis (Chernukha) \u2014 CTSpinoPelvic1K",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--dataset_root", metavar="DIR",
                     help="Path to the snapshot folder containing ct/, "
                          "labels/, and manifest_*.json")
    src.add_argument("--hub_repo", metavar="REPO_ID", default=None,
                     help="(deprecated for local use) HuggingFace repo id")
    ap.add_argument("--cache_dir", default=None)
    ap.add_argument("--output", default="spine_results.csv")
    ap.add_argument("--split", default="all",
                    choices=["all", "trainval", "test"])
    ap.add_argument("--visualize", action="store_true")
    ap.add_argument("--vis_dir", default="figures")
    ap.add_argument("--cases", nargs="*", default=None, metavar="TOKEN")
    ap.add_argument("--log_level", default="DEBUG",
                    choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                    help="Verbosity written to the log file "
                         "(console always shows WARNING+ only).")

    args = ap.parse_args(argv)

    # ── Logging ───────────────────────────────────────────────────────────────
    _op      = Path(args.output)
    log_path = _op.parent / (_op.stem + ".log")
    log = _setup_logging(log_path, file_level=getattr(logging, args.log_level))
    log.info("=" * 70)
    log.info("spine_analysis v314  —  TRALL Lumbar Lordosis (Chernukha)")
    log.info("=" * 70)
    log.info("args: %s", vars(args))
    # ─────────────────────────────────────────────────────────────────────────

    all_cases = build_dataset(args)

    EXCLUDED_CONFIGS = {"pelvic_native"}
    fused = [c for c in all_cases if c.config not in EXCLUDED_CONFIGS]

    if args.cases:
        wanted = set(args.cases)
        fused  = [c for c in fused if c.token in wanted]

    config_counts = {}
    for c in fused:
        config_counts[c.config] = config_counts.get(c.config, 0) + 1

    log.info("%d case(s) selected (excluded: %s)", len(fused), EXCLUDED_CONFIGS)
    log.info("Config breakdown: %s", config_counts)
    print(f"\n[info] {len(fused)} case(s) selected | configs: {config_counts}")
    print(f"[info] Log file: {log_path.resolve()}")

    if not fused:
        log.warning("No eligible cases found.")
        print("[warn] No eligible cases found.")
        sys.exit(0)

    fields = ["token", "split", "config", "trall_angle_deg",
              "max_coronal_deviation_mm",
              "landmark_A_AP_SI_mm", "landmark_B_AP_SI_mm", "landmark_C_AP_SI_mm"]
    rows, n_err = [], 0

    n_workers = int(os.environ.get("SPINE_WORKERS", os.cpu_count() or 1))
    if args.visualize:
        n_workers = 1
        log.info("Visualization mode: single worker to avoid OOM.")
        print("[info] Visualization mode: forcing single worker.")
    log.info("Parallel workers: %d", n_workers)
    print(f"[info] Workers: {n_workers}")

    t_start = time.time()

    pbar = _make_pbar(total=len(fused), desc="Processing")
    _pbar_ref = pbar

    if n_workers == 1:
        for case in fused:
            try:
                result = process_case(case, visualize=args.visualize,
                                      vis_dir=args.vis_dir)
                rows.append(result)
            except Exception as exc:
                import traceback as _tb
                log.error("[%s] unhandled exception: %s\n%s",
                          case.token, exc, _tb.format_exc())
                rows.append({f: ("ERROR" if f != "token" else case.token)
                             for f in fields})
                n_err += 1
            finally:
                td = rows[-1].get("trall_angle_deg", "")
                status = f"{td:.1f}°" if isinstance(td, float) else str(td)
                with _pbar_lock:
                    pbar.set_postfix_str(f"{case.token} -> {status}", refresh=True)
                    pbar.update(1)
    else:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        import functools

        _worker = functools.partial(_process_case_worker,
                                    visualize=args.visualize,
                                    vis_dir=args.vis_dir)
        futures = {}
        with ThreadPoolExecutor(max_workers=n_workers,
                                thread_name_prefix="spine") as pool:
            for case in fused:
                futures[pool.submit(_worker, case)] = case.token

        result_map = {}
        for fut in as_completed(futures):
            tok = futures[fut]
            try:
                result_map[tok] = fut.result()
            except Exception as exc:
                import traceback as _tb
                log.error("[%s] unhandled exception: %s\n%s",
                          tok, exc, _tb.format_exc())
                result_map[tok] = {f: ("ERROR" if f != "token" else tok)
                                   for f in fields}
                n_err += 1

        for case in fused:
            rows.append(result_map[case.token])

    pbar.close()
    _pbar_ref = None

    elapsed      = time.time() - t_start
    per_case_avg = elapsed / max(len(rows), 1)

    # ── Write CSV ─────────────────────────────────────────────────────────────
    csv_path = Path(args.output)
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    n_no_sacrum = sum(1 for r in rows if r.get("trall_angle_deg") == "NO_SACRUM")
    n_ok        = sum(1 for r in rows if isinstance(r.get("trall_angle_deg"), float))
    summary_line = (
        f"{len(rows)} cases | {n_ok} computed | "
        f"{n_no_sacrum} NO_SACRUM | {n_err} errors | "
        f"{elapsed:.0f}s total ({per_case_avg:.1f}s/case)"
    )
    log.info("Run complete: %s", summary_line)
    log.info("Results CSV -> %s", csv_path.resolve())
    if args.visualize:
        log.info("Figures     -> %s", Path(args.vis_dir).resolve())

    print(f"\n{'='*60}")
    print(f"  {summary_line}")
    print(f"  Results  -> {csv_path.resolve()}")
    if args.visualize:
        print(f"  Figures  -> {Path(args.vis_dir).resolve()}")
    print(f"  Log      -> {log_path.resolve()}")

    # ── Summary statistics ────────────────────────────────────────────────────
    import csv as _csv

    def _nums(key):
        return [r[key] for r in rows if isinstance(r.get(key), (int, float))]

    def _stats_line(label, vals, unit=""):
        if not vals:
            return f"  {label}: no valid data"
        a = np.array(vals)
        p25, p50, p75 = np.percentile(a, [25, 50, 75])
        ci95_lo = a.mean() - 1.96 * a.std(ddof=1) / np.sqrt(len(a))
        ci95_hi = a.mean() + 1.96 * a.std(ddof=1) / np.sqrt(len(a))
        return (f"  {label:35s} n={len(a):4d} | "
                f"mean={a.mean():7.2f}{unit}  std={a.std(ddof=1):6.2f}{unit}  "
                f"median={p50:7.2f}{unit}  IQR=[{p25:.2f},{p75:.2f}]{unit}  "
                f"range=[{a.min():.2f},{a.max():.2f}]{unit}  "
                f"95%CI=[{ci95_lo:.2f},{ci95_hi:.2f}]{unit}")

    td_v = _nums("trall_angle_deg")
    cd_v = _nums("max_coronal_deviation_mm")

    a_si_v, b_si_v, c_si_v = [], [], []
    chord_v, c_dev_v = [], []
    for r in rows:
        try:
            A = r.get("landmark_A_AP_SI_mm", "")
            B = r.get("landmark_B_AP_SI_mm", "")
            C = r.get("landmark_C_AP_SI_mm", "")
            if "," in str(A) and "," in str(B) and "," in str(C):
                def _parse(s):
                    return [float(x) for x in s.strip("()").split(",")]
                ap_a, si_a = _parse(A)
                ap_b, si_b = _parse(B)
                ap_c, si_c = _parse(C)
                a_si_v.append(si_a); b_si_v.append(si_b); c_si_v.append(si_c)
                chord = np.sqrt((ap_b - ap_a)**2 + (si_b - si_a)**2)
                chord_v.append(chord)
                ab = np.array([ap_b - ap_a, si_b - si_a])
                ac = np.array([ap_c - ap_a, si_c - si_a])
                ab_norm = np.linalg.norm(ab)
                if ab_norm > 0:
                    c_dev_v.append(abs(float(np.cross(ab, ac))) / ab_norm)
        except Exception:
            pass

    stat_block = "\n".join([
        "", "=" * 80, "  SUMMARY STATISTICS", "=" * 80,
        _stats_line("TRALL angle",              td_v,    " deg"),
        _stats_line("Max coronal deviation",    cd_v,    " mm"),
        _stats_line("Chord length A->B",        chord_v, " mm"),
        _stats_line("Apex deviation (C|chord)", c_dev_v, " mm"),
        _stats_line("Landmark A  SI position",  a_si_v,  " mm"),
        _stats_line("Landmark B  SI position",  b_si_v,  " mm"),
        _stats_line("Landmark C  SI position",  c_si_v,  " mm"),
        "=" * 80,
    ])
    log.info(stat_block)
    print(stat_block)

    _op2 = Path(args.output)
    summary_path = _op2.parent / (_op2.stem + "_summary" + _op2.suffix)
    summary_rows = []
    for label, vals, unit in [
        ("trall_angle_deg",           td_v,    "deg"),
        ("max_coronal_deviation_mm",  cd_v,    "mm"),
        ("chord_length_AB_mm",        chord_v, "mm"),
        ("apex_deviation_C_mm",       c_dev_v, "mm"),
        ("landmark_A_SI_mm",          a_si_v,  "mm"),
        ("landmark_B_SI_mm",          b_si_v,  "mm"),
        ("landmark_C_SI_mm",          c_si_v,  "mm"),
    ]:
        if not vals:
            continue
        a = np.array(vals)
        p25, p50, p75 = np.percentile(a, [25, 50, 75])
        ci95_lo = a.mean() - 1.96 * a.std(ddof=1) / np.sqrt(len(a))
        ci95_hi = a.mean() + 1.96 * a.std(ddof=1) / np.sqrt(len(a))
        summary_rows.append({
            "metric": label, "unit": unit, "n": len(a),
            "mean":    round(float(a.mean()), 4),
            "std":     round(float(a.std(ddof=1)), 4),
            "median":  round(float(p50), 4),
            "p25":     round(float(p25), 4), "p75": round(float(p75), 4),
            "min":     round(float(a.min()), 4), "max": round(float(a.max()), 4),
            "ci95_lo": round(float(ci95_lo), 4),
            "ci95_hi": round(float(ci95_hi), 4),
        })
    s_fields = ["metric", "unit", "n", "mean", "std", "median",
                "p25", "p75", "min", "max", "ci95_lo", "ci95_hi"]
    with open(summary_path, "w", newline="") as fh:
        w = _csv.DictWriter(fh, fieldnames=s_fields)
        w.writeheader()
        w.writerows(summary_rows)
    log.info("Summary CSV -> %s", summary_path.resolve())
    print(f"  Summary  -> {summary_path.resolve()}\n")


if __name__ == "__main__":
    main()
