"""
SpineSurg-CT -- Pelvic Alignment Grid Panel
src/utils/pelvic_grid_panel.py

Renders a single publication-quality PNG showing all fused cases
in a grid layout.  Each cell shows a coronal slice centred on the
lumbosacral junction, rotated into standard anatomical orientation
(superior up, left on right), with semi-transparent label overlay,
per-case pass/fail badge, and sacrum/hip voxel counts.

CACHE KEY ALIGNMENT
===================
Uses record.cache_stem  (<image_stem>__<match_type>__<label_role>) to look up
.pt files.  For fused cases this produces keys of the form:
  1.3.6.1.4.1.9328.50.4.4__fused__spineimg

Outputs
-------
<output_dir>/pelvic_alignment_grid.png
<output_dir>/pelvic_alignment_grid_fails.png  (if any FAILs)

Usage
-----
python -m src.utils.pelvic_grid_panel \\
    --raw_dir    /data \\
    --splits     /data/splits.json \\
    --cache_dir  /data/precache \\
    --output_dir /data/pelvic_alignment_qc \\
    --split      all   \\
    --cols       6     \\
    --slice_axis coronal   # coronal | sagittal | axial

FIX HISTORY
===========
v3 (2026-04):
  Cache key fix -- load_cache() now takes a CaseRecord and uses
    record.cache_stem instead of a local _stem(image_path) helper.
    This ensures the correct __fused__spineimg suffix is used.

  LSTV subtitle fix -- the LSTV count in the subtitle previously
    called _stem(record.image) to look up in lstv_stems.  Now it
    calls Path(record.image).stem directly (matching how lstv_stems
    is built in run_pipeline / run_grid_panel).

v2 (2026-04):
  Fix 3 -- PASS/FAIL gap lower bound: rejects gap outside [-20, 30] mm.
  Sagittal slice fix -- uses AP centroid (axis 0) as slice index.
  Gap annotation -- gap_mm printed in each cell.

Author: Gregory Schwing, MD, PhD
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import matplotlib.gridspec as gridspec
import numpy as np
import torch

log = logging.getLogger("spinesurg.pelvic_grid")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ── Colour palette ─────────────────────────────────────────────────────────────

RGBA_MAP = {
    0: (0.00, 0.00, 0.00, 0.00),
    1: (0.20, 0.60, 1.00, 0.65),  # L1
    2: (0.20, 0.80, 1.00, 0.65),  # L2
    3: (0.20, 1.00, 0.80, 0.65),  # L3
    4: (0.20, 1.00, 0.40, 0.65),  # L4
    5: (0.60, 1.00, 0.20, 0.70),  # L5
    6: (1.00, 0.20, 0.20, 0.82),  # L6
    7: (1.00, 0.60, 0.00, 0.80),  # Sacrum
    8: (0.85, 0.00, 0.85, 0.75),  # L-Hip
    9: (0.60, 0.00, 1.00, 0.75),  # R-Hip
}

CLASS_NAMES = {
    1: "L1", 2: "L2", 3: "L3", 4: "L4", 5: "L5", 6: "L6",
    7: "Sacrum", 8: "L-Hip", 9: "R-Hip",
}

SPINE_IDS  = [1, 2, 3, 4, 5, 6]
PELVIC_IDS = [7, 8, 9]

# Design constants
BG_COLOR     = "#0a0a12"
PANEL_COLOR  = "#10101e"
GRID_COLOR   = "#1a1a2e"
TEXT_PRIMARY = "#e8e8f0"
TEXT_MUTED   = "#7070a0"
PASS_COLOR   = "#00e676"
FAIL_COLOR   = "#ff1744"
WARN_COLOR   = "#ffab00"
ACCENT       = "#4040c0"

MIN_VOXELS = 50

# Anatomically valid gap range (mm).
# Positive = true disc gap; negative = sacrum cranially overlaps L5.
# -20 mm permits normal S1/L5 superior endplate articulation.
GAP_MM_MIN = -20.0
GAP_MM_MAX =  30.0


# ─────────────────────────────────────────────────────────────────────────────
# Cache helpers  — uses record.cache_stem (unambiguous key)
# ─────────────────────────────────────────────────────────────────────────────

def _to_plain(t: torch.Tensor) -> torch.Tensor:
    return t.as_tensor() if hasattr(t, "as_tensor") else t


def load_cache(record, cache_dir: Path) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    """
    Load (image_np, label_np) from the training cache.

    Uses record.cache_stem to derive the exact filename written by precache.py.
    For fused cases this resolves to <stem>__fused__spineimg.
    """
    stem     = record.cache_stem
    img_path = cache_dir / f"{stem}_image.pt"
    lbl_path = cache_dir / f"{stem}_label.pt"
    if not img_path.exists() or not lbl_path.exists():
        return None
    try:
        image = _to_plain(
            torch.load(img_path, map_location="cpu", weights_only=False)
        ).float().squeeze(0).numpy()
        label = _to_plain(
            torch.load(lbl_path, map_location="cpu", weights_only=False)
        ).long().squeeze(0).numpy().astype(np.int32)
        return image, label
    except Exception as exc:
        log.warning("Cache load failed for %s: %s", stem, exc)
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Slice extraction
# ─────────────────────────────────────────────────────────────────────────────

def _lumbosacral_centre(lbl: np.ndarray) -> Tuple[int, int, int]:
    """
    Centroid of the L4/L5/L6/sacrum cluster.
    Returns (ap_idx, is_idx, lr_idx) i.e. (axis-0, axis-1, axis-2) in PIR.
    """
    D, H, W = lbl.shape
    for classes in [[4, 5, 6, 7], [3, 4, 5, 7], [1, 2, 3, 4, 5, 6, 7]]:
        m = np.isin(lbl, classes)
        if m.any():
            c = np.argwhere(m)
            return int(c[:, 0].mean()), int(c[:, 1].mean()), int(c[:, 2].mean())
    return D // 2, H // 2, W // 2


def _label_rgba(lbl_slice: np.ndarray) -> np.ndarray:
    H, W  = lbl_slice.shape
    rgba  = np.zeros((H, W, 4), dtype=np.float32)
    for cls, color in RGBA_MAP.items():
        m = lbl_slice == cls
        if m.any():
            rgba[m] = color
    return rgba


def extract_coronal(
    image_np: np.ndarray,
    label_np: np.ndarray,
    margin_vox: int = 40,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    PIR volume -> coronal slice at lumbosacral junction, cropped and
    flipped into standard anatomical orientation (superior up, left on right).

    PIR axes: 0=P->A  1=I->S  2=R->L
    Coronal: fix axis 0 (AP) at AP centroid of LS cluster.
    Display: axis-1 (I->S) on Y (flipped superior-up), axis-2 (R->L) on X.
    """
    cz, cy, cx = _lumbosacral_centre(label_np)

    img_slice = image_np[cz, :, :]   # shape: H(I->S) x W(R->L)
    lbl_slice = label_np[cz, :, :]

    fg = np.argwhere(np.isin(label_np[cz], list(range(1, 10))))
    if len(fg) > 0:
        r0 = max(0,                  fg[:, 0].min() - margin_vox)
        r1 = min(img_slice.shape[0], fg[:, 0].max() + margin_vox)
        c0 = max(0,                  fg[:, 1].min() - margin_vox)
        c1 = min(img_slice.shape[1], fg[:, 1].max() + margin_vox)
        img_slice = img_slice[r0:r1, c0:c1]
        lbl_slice = lbl_slice[r0:r1, c0:c1]

    # Superior up, radiological convention (patient left on right)
    img_slice = np.fliplr(np.flipud(img_slice))
    lbl_slice = np.fliplr(np.flipud(lbl_slice))
    return img_slice, lbl_slice


def extract_sagittal(
    image_np: np.ndarray,
    label_np: np.ndarray,
    margin_vox: int = 35,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Mid-sagittal slice through the lumbosacral centroid.

    PIR axes: 0=P->A  1=I->S  2=R->L
    Sagittal: fix axis 2 (R->L) at LR centroid of LS cluster.
    """
    cz, cy, cx = _lumbosacral_centre(label_np)

    img_slice = image_np[:, :, cx]   # shape: D(P->A) x H(I->S)
    lbl_slice = label_np[:, :, cx]

    fg = np.argwhere(np.isin(label_np[:, :, cx], list(range(1, 10))))
    if len(fg) > 0:
        r0 = max(0,                  fg[:, 0].min() - margin_vox)
        r1 = min(img_slice.shape[0], fg[:, 0].max() + margin_vox)
        c0 = max(0,                  fg[:, 1].min() - margin_vox)
        c1 = min(img_slice.shape[1], fg[:, 1].max() + margin_vox)
        img_slice = img_slice[r0:r1, c0:c1]
        lbl_slice = lbl_slice[r0:r1, c0:c1]

    # Transpose + flipud -> rows=I->S (superior up), cols=P->A
    img_slice = np.flipud(img_slice.T)
    lbl_slice = np.flipud(lbl_slice.T)
    return img_slice, lbl_slice


SLICE_FN = {
    "coronal":  extract_coronal,
    "sagittal": extract_sagittal,
}


# ─────────────────────────────────────────────────────────────────────────────
# Per-case metrics
# ─────────────────────────────────────────────────────────────────────────────

def case_metrics(label_np: np.ndarray) -> Dict:
    """
    Compute QC metrics for a fused label volume.

    gap_mm = l5_inferior_IS - sacrum_superior_IS
      positive -> true anatomical disc gap (normal: ~2-5 mm)
      negative -> sacrum superior surface cranial to L5 inferior surface.
        |gap| < 20 mm: normal S1/L5 articular overlap -> PASS
        |gap| >= 20 mm: catastrophic misalignment -> FAIL
    """
    spine  = np.isin(label_np, SPINE_IDS)
    sac    = label_np == 7
    lhip   = label_np == 8
    rhip   = label_np == 9
    l5     = label_np == 5
    l6     = label_np == 6

    sw_viol = int((l5 & sac).sum())
    l6_viol = int((l6 & sac).sum())
    sac_vox = int(sac.sum())

    gap_mm  = float("nan")
    if l5.any() and sac.any():
        l5_inf  = float(np.argwhere(l5)[:, 1].min())
        sac_sup = float(np.argwhere(sac)[:, 1].max())
        gap_mm  = float(l5_inf - sac_sup)

    gap_plausible = (
        np.isnan(gap_mm)
        or (GAP_MM_MIN <= gap_mm <= GAP_MM_MAX)
    )

    plausible = (
        sac_vox >= MIN_VOXELS
        and sw_viol == 0
        and l6_viol == 0
        and gap_plausible
    )
    return {
        "plausible":   plausible,
        "sac_vox":     sac_vox,
        "lhip_vox":    int(lhip.sum()),
        "rhip_vox":    int(rhip.sum()),
        "sw_viol":     sw_viol,
        "l6_viol":     l6_viol,
        "gap_mm":      gap_mm,
        "has_l6":      int(l6.sum()) >= MIN_VOXELS,
        "has_pelvic":  sac_vox >= MIN_VOXELS,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Grid renderer
# ─────────────────────────────────────────────────────────────────────────────

def _draw_orientation_labels(ax, slice_axis: str) -> None:
    kw = dict(fontsize=5, color=TEXT_MUTED, fontfamily="monospace",
              path_effects=[pe.withStroke(linewidth=1.2, foreground="black")])
    if slice_axis == "coronal":
        ax.text(0.02, 0.97, "S", transform=ax.transAxes, va="top",   ha="left",  **kw)
        ax.text(0.02, 0.03, "I", transform=ax.transAxes, va="bottom",ha="left",  **kw)
        ax.text(0.98, 0.50, "L", transform=ax.transAxes, va="center",ha="right", **kw)
        ax.text(0.02, 0.50, "R", transform=ax.transAxes, va="center",ha="left",  **kw)
    elif slice_axis == "sagittal":
        ax.text(0.02, 0.97, "S", transform=ax.transAxes, va="top",   ha="left",  **kw)
        ax.text(0.02, 0.03, "I", transform=ax.transAxes, va="bottom",ha="left",  **kw)
        ax.text(0.98, 0.50, "A", transform=ax.transAxes, va="center",ha="right", **kw)
        ax.text(0.02, 0.50, "P", transform=ax.transAxes, va="center",ha="left",  **kw)


def _draw_pass_fail_badge(ax, plausible: bool) -> None:
    label = "PASS" if plausible else "FAIL"
    color = PASS_COLOR if plausible else FAIL_COLOR
    ax.text(0.98, 0.97, label,
            transform=ax.transAxes, va="top", ha="right",
            fontsize=5.5, fontweight="bold", color=color,
            fontfamily="monospace",
            path_effects=[pe.withStroke(linewidth=1.5, foreground="black")])


def _draw_case_label(ax, pid: str, metrics: Dict) -> None:
    stroke = [pe.withStroke(linewidth=1.5, foreground="black")]

    ax.text(0.02, 0.97, f"#{pid}",
            transform=ax.transAxes, va="top", ha="left",
            fontsize=5.0, color=TEXT_PRIMARY, fontfamily="monospace",
            path_effects=stroke)

    sac  = metrics["sac_vox"]
    info = f"Sac:{sac:,}"
    if metrics["lhip_vox"] > 0:
        info += f"  LH:{metrics['lhip_vox']:,}"
    if metrics["rhip_vox"] > 0:
        info += f"  RH:{metrics['rhip_vox']:,}"
    ax.text(0.02, 0.03, info,
            transform=ax.transAxes, va="bottom", ha="left",
            fontsize=4.0, color=TEXT_MUTED, fontfamily="monospace",
            path_effects=stroke)

    if not np.isnan(metrics["gap_mm"]):
        gap_val = metrics["gap_mm"]
        if GAP_MM_MIN <= gap_val <= GAP_MM_MAX:
            gap_color = TEXT_MUTED
        elif gap_val < GAP_MM_MIN:
            gap_color = FAIL_COLOR
        else:
            gap_color = WARN_COLOR
        ax.text(0.50, 0.13, f"gap:{gap_val:+.0f}mm",
                transform=ax.transAxes, va="bottom", ha="center",
                fontsize=4.0, color=gap_color, fontfamily="monospace",
                path_effects=stroke)

    violations = []
    if metrics["sw_viol"] > 0:
        violations.append(f"⚠ L5↔Sac:{metrics['sw_viol']}vx")
    if metrics["l6_viol"] > 0:
        violations.append(f"⚠ L6↔Sac:{metrics['l6_viol']}vx")
    if not np.isnan(metrics["gap_mm"]) and metrics["gap_mm"] >= GAP_MM_MAX:
        violations.append(f"⚠ gap:{metrics['gap_mm']:.0f}mm")
    if not np.isnan(metrics["gap_mm"]) and metrics["gap_mm"] < GAP_MM_MIN:
        violations.append(f"⚠ gap:{metrics['gap_mm']:.0f}mm")
    if not metrics["has_pelvic"]:
        violations.append("⚠ NO PELVIS")
    if violations:
        ax.text(0.50, 0.03, "  ".join(violations),
                transform=ax.transAxes, va="bottom", ha="center",
                fontsize=4.0, color=WARN_COLOR, fontfamily="monospace",
                path_effects=stroke)

    if metrics["has_l6"]:
        ax.text(0.98, 0.03, "L6✓",
                transform=ax.transAxes, va="bottom", ha="right",
                fontsize=4.5, color="#ff4444", fontweight="bold",
                fontfamily="monospace", path_effects=stroke)


def _spine_label_bar(ax_bar, classes_present: List[int]) -> None:
    bar = np.zeros((1, 9, 4), dtype=np.float32)
    for i, cls in enumerate(range(1, 10)):
        if cls in classes_present:
            bar[0, i] = RGBA_MAP[cls][:3] + (1.0,)
        else:
            bar[0, i] = (0.15, 0.15, 0.25, 1.0)
    ax_bar.imshow(bar, aspect="auto")
    ax_bar.set_xticks([])
    ax_bar.set_yticks([])
    for spine_side in ax_bar.spines.values():
        spine_side.set_visible(False)


def render_grid(
    cases: List[Dict],
    output_path: Path,
    cols: int = 6,
    slice_axis: str = "coronal",
    title: str = "Pelvic Alignment QC — Training Cache",
    subtitle: str = "",
) -> None:
    n      = len(cases)
    rows   = (n + cols - 1) // cols
    cell_w = 2.2
    cell_h = 2.5
    bar_h  = 0.08

    fig_w = cols * cell_w + 1.2
    fig_h = rows * cell_h + 1.6

    fig = plt.figure(figsize=(fig_w, fig_h), facecolor=BG_COLOR)

    n_pass   = sum(1 for c in cases if c["metrics"]["plausible"])
    n_fail   = n - n_pass
    n_miss   = sum(1 for c in cases if c.get("cache_miss"))
    n_nopelv = sum(1 for c in cases if not c["metrics"]["has_pelvic"])

    fig.text(0.5, 0.985, title,
             ha="center", va="top",
             fontsize=14, fontweight="bold", color=TEXT_PRIMARY,
             fontfamily="DejaVu Sans")

    status_str = (
        f"{n} cases  ·  "
        f"{n_pass} PASS  ·  "
        f"{n_fail} FAIL  ·  "
        f"{n_miss} cache-miss  ·  "
        f"{n_nopelv} no-pelvic"
        + (f"  ·  {subtitle}" if subtitle else "")
    )
    fig.text(0.5, 0.972, status_str,
             ha="center", va="top", fontsize=7.5, color=TEXT_MUTED,
             fontfamily="monospace")

    fig.text(0.5, 0.962,
             f"gap plausible: {GAP_MM_MIN:+.0f} ≤ gap ≤ {GAP_MM_MAX:+.0f} mm  "
             f"(negative = sacrum cranial to L5 inferior endplate)  "
             f"[direct voxel overlay — confirmed same-scan pairs only]",
             ha="center", va="top", fontsize=6.0, color=TEXT_MUTED,
             fontfamily="monospace")

    line_ax = fig.add_axes([0.04, 0.950, 0.92, 0.0015])
    line_ax.set_facecolor(ACCENT)
    line_ax.set_xticks([]); line_ax.set_yticks([])
    for s in line_ax.spines.values(): s.set_visible(False)

    top_margin    = 0.055
    bottom_margin = 0.060
    left_margin   = 0.015
    right_margin  = 0.015

    gs_outer = gridspec.GridSpec(
        rows, cols,
        figure=fig,
        top=1.0 - top_margin,
        bottom=bottom_margin,
        left=left_margin,
        right=1.0 - right_margin,
        hspace=0.04,
        wspace=0.03,
    )

    extract_fn = SLICE_FN.get(slice_axis, extract_coronal)

    for idx, case in enumerate(cases):
        row = idx // cols
        col = idx  % cols

        pid     = case["pid"]
        metrics = case["metrics"]

        inner = gridspec.GridSpecFromSubplotSpec(
            2, 1,
            subplot_spec=gs_outer[row, col],
            height_ratios=[1 - bar_h, bar_h],
            hspace=0.0,
        )
        ax_img = fig.add_subplot(inner[0])
        ax_bar = fig.add_subplot(inner[1])

        for ax in (ax_img, ax_bar):
            ax.set_facecolor(PANEL_COLOR)
            for s in ax.spines.values():
                s.set_edgecolor(GRID_COLOR)
                s.set_linewidth(0.6)

        if case.get("cache_miss"):
            ax_img.set_facecolor("#0d0d1a")
            ax_img.text(0.5, 0.55, "CACHE", ha="center", va="center",
                        fontsize=7, color=FAIL_COLOR, fontfamily="monospace",
                        fontweight="bold", transform=ax_img.transAxes)
            ax_img.text(0.5, 0.40, "MISS",  ha="center", va="center",
                        fontsize=7, color=FAIL_COLOR, fontfamily="monospace",
                        fontweight="bold", transform=ax_img.transAxes)
            ax_img.text(0.5, 0.22, f"#{pid}", ha="center", va="center",
                        fontsize=5, color=TEXT_MUTED, fontfamily="monospace",
                        transform=ax_img.transAxes)
            ax_img.set_xticks([]); ax_img.set_yticks([])
            ax_bar.set_facecolor("#0d0d1a")
            ax_bar.set_xticks([]); ax_bar.set_yticks([])
            continue

        image_np = case["image_np"]
        label_np = case["label_np"]

        img_sl, lbl_sl = extract_fn(image_np, label_np)
        lbl_rgba       = _label_rgba(lbl_sl)

        ax_img.imshow(img_sl, cmap="gray", origin="upper",
                      aspect="equal", interpolation="bicubic",
                      vmin=0.0, vmax=1.0)
        ax_img.imshow(lbl_rgba, origin="upper", aspect="equal",
                      interpolation="nearest")
        ax_img.set_xticks([])
        ax_img.set_yticks([])

        if not metrics["plausible"]:
            for s in ax_img.spines.values():
                s.set_edgecolor(FAIL_COLOR)
                s.set_linewidth(1.2)

        _draw_orientation_labels(ax_img, slice_axis)
        _draw_pass_fail_badge(ax_img, metrics["plausible"])
        _draw_case_label(ax_img, pid, metrics)

        present = [cls for cls in range(1, 10) if int((label_np == cls).sum()) >= 10]
        _spine_label_bar(ax_bar, present)

    # Blank unused cells
    for idx in range(n, rows * cols):
        row = idx // cols
        col = idx  % cols
        ax  = fig.add_subplot(gs_outer[row, col])
        ax.set_facecolor(BG_COLOR)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_visible(False)

    # Legend footer
    legend_ax = fig.add_axes([0.04, 0.005, 0.92, 0.048])
    legend_ax.set_facecolor(GRID_COLOR)
    legend_ax.set_xticks([]); legend_ax.set_yticks([])
    for s in legend_ax.spines.values():
        s.set_edgecolor(ACCENT)
        s.set_linewidth(0.8)

    patches = []
    for cls in range(1, 10):
        r, g, b, _ = RGBA_MAP[cls]
        patches.append(
            mpatches.Patch(facecolor=(r, g, b), edgecolor=(1,1,1,0.2),
                           linewidth=0.5, label=CLASS_NAMES[cls])
        )
    patches += [
        mpatches.Patch(facecolor=BG_COLOR, edgecolor=PASS_COLOR,
                       linewidth=1.5, label="PASS border"),
        mpatches.Patch(facecolor=BG_COLOR, edgecolor=FAIL_COLOR,
                       linewidth=1.5, label="FAIL border"),
    ]

    legend_ax.legend(
        handles=patches, loc="center", ncol=11, fontsize=6.5, frameon=False,
        labelcolor=TEXT_PRIMARY, handlelength=1.2, handletextpad=0.4,
        columnspacing=0.9, prop={"family": "monospace", "size": 6.5},
    )

    fig.text(0.98, 0.027,
             f"view: {slice_axis.upper()}  ·  S↑  {'L→' if slice_axis == 'coronal' else 'A→'}",
             ha="right", va="center", fontsize=5.5, color=TEXT_MUTED,
             fontfamily="monospace")
    fig.text(0.02, 0.027,
             "SpineSurg-CT  ·  Wayne State / DMC  ·  Schwing MD PhD",
             ha="left", va="center", fontsize=5.5, color=TEXT_MUTED,
             fontfamily="monospace")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200, bbox_inches="tight",
                facecolor=BG_COLOR, edgecolor="none")
    plt.close(fig)
    log.info("Grid PNG -> %s", output_path)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def run_grid_panel(
    raw_dir:     Path,
    splits_path: Path,
    cache_dir:   Path,
    output_dir:  Path,
    split:       str = "all",
    cols:        int = 6,
    slice_axis:  str = "coronal",
    max_cases:   int = 0,
) -> None:
    from src.data.pipeline import (
        load_splits_from_json,
        load_dataset,
        classify_cases,
    )

    raw_dir      = Path(raw_dir)
    splits_path  = Path(splits_path)
    cache_dir    = Path(cache_dir)
    output_dir   = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not cache_dir.exists():
        log.error("cache_dir not found: %s", cache_dir)
        sys.exit(1)

    n_pt = len(list(cache_dir.glob("*__*__*_image.pt")))
    log.info("Cache: %s  (%d versioned tensors)", cache_dir, n_pt)

    matched_json = raw_dir / "matched" / "colonog_matched_pairs.json"
    all_records  = load_dataset(
        raw_dir / "ctspine1k",
        matched_pairs_json=matched_json if matched_json.exists() else None,
    )
    lstv_indices, _, _ = classify_cases(
        all_records, cache_path=raw_dir / "lstv_scan_cache.json"
    )
    # Build lstv_stems using the same method as run_pipeline
    lstv_stems = {Path(all_records[i].image).stem for i in lstv_indices}

    if not splits_path.exists():
        log.error("splits.json not found: %s", splits_path)
        sys.exit(1)
    splits, _ = load_splits_from_json(splits_path, lstv_stems=lstv_stems)

    split_names = list(splits.keys()) if split == "all" else [split]
    candidates  = [
        r
        for sn in split_names
        for r in splits.get(sn, [])
        if r.pelvic_mask is not None
    ]

    if max_cases > 0:
        import random; random.seed(42)
        random.shuffle(candidates)
        candidates = candidates[:max_cases]

    log.info("Fused pairs: %d  (split=%s)", len(candidates), split)
    if not candidates:
        log.error("No fused cases found.")
        sys.exit(1)

    cases = []
    for idx, record in enumerate(candidates):
        pid = record.patient_id
        log.info("[%d/%d] Loading %s  (stem=%s) ...",
                 idx + 1, len(candidates), pid, record.cache_stem)

        result = load_cache(record, cache_dir)
        if result is None:
            log.warning("  CACHE MISS: %s", record.cache_stem)
            cases.append({
                "pid":        pid,
                "cache_miss": True,
                "image_np":   None,
                "label_np":   None,
                "metrics":    {
                    "plausible": False, "sac_vox": 0, "lhip_vox": 0,
                    "rhip_vox": 0, "sw_viol": 0, "l6_viol": 0,
                    "gap_mm": float("nan"), "has_l6": False, "has_pelvic": False,
                },
            })
            continue

        image_np, label_np = result
        metrics = case_metrics(label_np)
        cases.append({
            "pid":        pid,
            "cache_miss": False,
            "image_np":   image_np,
            "label_np":   label_np,
            "metrics":    metrics,
        })
        log.info("  [%s] sac=%d  lhip=%d  rhip=%d  gap=%s mm",
                 "PASS" if metrics["plausible"] else "FAIL",
                 metrics["sac_vox"], metrics["lhip_vox"], metrics["rhip_vox"],
                 f"{metrics['gap_mm']:+.1f}" if not np.isnan(metrics["gap_mm"]) else "nan")

    # Sort: FAIL first, then PASS, both alphabetical
    cases.sort(key=lambda c: (int(c["metrics"]["plausible"]), c["pid"]))

    n_pass = sum(1 for c in cases if c["metrics"]["plausible"])
    n_fail = len(cases) - n_pass

    subtitle = f"{split.upper()} split"
    if lstv_stems:
        # Count LSTV among the candidates (use image stem directly)
        n_lstv = sum(
            1 for r in candidates
            if Path(r.image).stem in lstv_stems
        )
        if n_lstv:
            subtitle += f"  ·  {n_lstv} LSTV"

    grid_path = output_dir / "pelvic_alignment_grid.png"
    render_grid(
        cases       = cases,
        output_path = grid_path,
        cols        = cols,
        slice_axis  = slice_axis,
        title       = "Pelvic Alignment QC — Training Cache",
        subtitle    = subtitle,
    )

    fail_cases = [c for c in cases if not c["metrics"]["plausible"]]
    if fail_cases:
        fail_path = output_dir / "pelvic_alignment_grid_fails.png"
        render_grid(
            cases       = fail_cases,
            output_path = fail_path,
            cols        = min(cols, len(fail_cases)),
            slice_axis  = slice_axis,
            title       = "Pelvic Alignment QC — FAIL Cases Only",
            subtitle    = subtitle,
        )
        log.info("FAIL-only grid -> %s", fail_path)

    log.info("Done.  %d PASS  /  %d FAIL  /  %d total", n_pass, n_fail, len(cases))
    log.info("Grid  -> %s", grid_path)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def _parse():
    p = argparse.ArgumentParser(
        description="Render all fused pelvic cases as a 2-D anatomical grid panel."
    )
    p.add_argument("--raw_dir",    required=True)
    p.add_argument("--splits",     required=True)
    p.add_argument("--cache_dir",  required=True)
    p.add_argument("--output_dir", default="data/pelvic_alignment_qc")
    p.add_argument("--split",      default="all",
                   choices=["train", "val", "test", "all"])
    p.add_argument("--cols",       type=int, default=6)
    p.add_argument("--slice_axis", default="coronal",
                   choices=["coronal", "sagittal"])
    p.add_argument("--max_cases",  type=int, default=0)
    return p.parse_args()


if __name__ == "__main__":
    args = _parse()
    run_grid_panel(
        raw_dir     = Path(args.raw_dir),
        splits_path = Path(args.splits),
        cache_dir   = Path(args.cache_dir),
        output_dir  = Path(args.output_dir),
        split       = args.split,
        cols        = args.cols,
        slice_axis  = args.slice_axis,
        max_cases   = args.max_cases,
    )
