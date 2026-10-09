"""
SpineSurg-CT -- Pelvic Alignment 3-D QC  (Cache Edition)
src/utils/pelvic_alignment_qc.py

Validates the ACTUAL tensors stored in /data/precache -- i.e. exactly what
the neural network trains on -- rather than re-running preprocessing from raw
NIfTIs.

For every fused-pair case whose .pt files exist in --cache_dir, renders:
  Panel 1 -- Spine labels only (L1-L6 colour-coded)
  Panel 2 -- Pelvic labels only (sacrum / L-hip / R-hip)
  Panel 3 -- Fused result (all 10 classes as stored)

CACHE KEY ALIGNMENT
===================
Uses record.cache_stem  (<image_stem>__<match_type>__<label_role>) to look up
.pt files.  For fused cases this produces keys of the form:
  1.3.6.1.4.1.9328.50.4.4__fused__spineimg_image.pt
This matches exactly what precache.py writes.

Outputs
-------
<output_dir>/
  html/  <patient_id>_alignment.html
  png/   <patient_id>_alignment.png
  pelvic_alignment_summary.csv
  pelvic_alignment_report.txt

Usage
-----
python -m src.utils.pelvic_alignment_qc \\
    --raw_dir    /data \\
    --splits     /data/splits.json \\
    --cache_dir  /data/precache \\
    --output_dir /data/pelvic_alignment_qc \\
    --split      train          # train | val | test | all  (default: all)
    --max_cases  0              # 0 = no limit

Author: Gregory Schwing, MD, PhD
"""

from __future__ import annotations

import argparse
import logging
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import torch

log = logging.getLogger("spinesurg.pelvic_qc")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ── label meta ────────────────────────────────────────────────────────────────

SPINE_COLORS = {
    1: "#3399FF", 2: "#33CCFF", 3: "#33FFCC",
    4: "#33FF66", 5: "#99FF33", 6: "#FF3333",
}
PELVIC_COLORS = {
    7: "#FF9900",   # sacrum
    8: "#CC00CC",   # left hip
    9: "#9900FF",   # right hip
}
ALL_COLORS = {**SPINE_COLORS, **PELVIC_COLORS}

CLASS_NAMES = {
    1: "L1", 2: "L2", 3: "L3", 4: "L4", 5: "L5", 6: "L6",
    7: "Sacrum", 8: "L-Hip", 9: "R-Hip",
}

RGBA_MAP = {
    0: (0.0, 0.0, 0.0, 0.0),
    1: (0.20, 0.60, 1.00, 0.60),
    2: (0.20, 0.80, 1.00, 0.60),
    3: (0.20, 1.00, 0.80, 0.60),
    4: (0.20, 1.00, 0.40, 0.60),
    5: (0.60, 1.00, 0.20, 0.60),
    6: (1.00, 0.20, 0.20, 0.80),
    7: (1.00, 0.60, 0.00, 0.75),
    8: (0.80, 0.00, 0.80, 0.70),
    9: (0.60, 0.00, 1.00, 0.70),
}

MIN_VOXELS = 50

SPINE_CLASS_IDS  = [1, 2, 3, 4, 5, 6]
PELVIC_CLASS_IDS = [7, 8, 9]


# ─────────────────────────────────────────────────────────────────────────────
# Cache loading  — uses record.cache_stem (unambiguous key)
# ─────────────────────────────────────────────────────────────────────────────

def _to_plain_tensor(t: torch.Tensor) -> torch.Tensor:
    """Strip MONAI MetaTensor wrapper -> plain torch.Tensor."""
    if hasattr(t, "as_tensor"):
        return t.as_tensor()
    return t


def load_from_cache(
    record,            # CaseRecord
    cache_dir: Path,
) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    """
    Load (image_np, label_np) from the training cache using record.cache_stem.

    Returns
    -------
    (image_np float32 D×H×W, label_np int32 D×H×W)  or  None on miss.
    """
    stem     = record.cache_stem
    img_path = cache_dir / f"{stem}_image.pt"
    lbl_path = cache_dir / f"{stem}_label.pt"

    if not img_path.exists() or not lbl_path.exists():
        return None

    try:
        image = torch.load(img_path, map_location="cpu", weights_only=False)
        label = torch.load(lbl_path, map_location="cpu", weights_only=False)
        image = _to_plain_tensor(image).float().squeeze(0).numpy()
        label = _to_plain_tensor(label).long().squeeze(0).numpy().astype(np.int32)
        return image, label
    except Exception as exc:
        log.warning("Cache load failed for %s: %s", stem, exc)
        return None


def derive_panels(fused_np: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Derive spine-only and pelvic-only label arrays from the fused label.

      spine_np : classes 1-6 preserved, everything else -> 0
      pelv_np  : classes 7-9 preserved, everything else -> 0
    """
    spine_np = np.where(np.isin(fused_np, SPINE_CLASS_IDS),  fused_np, 0).astype(np.int32)
    pelv_np  = np.where(np.isin(fused_np, PELVIC_CLASS_IDS), fused_np, 0).astype(np.int32)
    return spine_np, pelv_np


# ─────────────────────────────────────────────────────────────────────────────
# Alignment metrics
# ─────────────────────────────────────────────────────────────────────────────

def compute_alignment_metrics(
    spine_lbl: np.ndarray,
    fused_lbl: np.ndarray,
) -> Dict[str, object]:
    l5_mask     = spine_lbl == 5
    l6_mask     = spine_lbl == 6
    sac_in_fuse = fused_lbl == 7
    lhip_fuse   = fused_lbl == 8
    rhip_fuse   = fused_lbl == 9

    spine_wins_violation = int((l5_mask & sac_in_fuse).sum())
    l6_wins_violation    = int((l6_mask & sac_in_fuse).sum())

    sac_vox  = int(sac_in_fuse.sum())
    lhip_vox = int(lhip_fuse.sum())
    rhip_vox = int(rhip_fuse.sum())

    gap_mm = float("nan")
    if l5_mask.any() and sac_in_fuse.any():
        l5_inf  = float(np.argwhere(l5_mask)[:, 1].min())
        sac_sup = float(np.argwhere(sac_in_fuse)[:, 1].max())
        gap_mm  = float(l5_inf - sac_sup)

    l5_sac_overlap_mm = max(0.0, -gap_mm) if not np.isnan(gap_mm) else float("nan")

    plausible = (
        sac_vox >= MIN_VOXELS
        and spine_wins_violation == 0
        and l6_wins_violation    == 0
        and (np.isnan(gap_mm) or gap_mm < 30.0)
    )

    return {
        "sacrum_voxels":         sac_vox,
        "l_hip_voxels":          lhip_vox,
        "r_hip_voxels":          rhip_vox,
        "spine_wins_violation":  spine_wins_violation,
        "l6_wins_violation":     l6_wins_violation,
        "l5_sacrum_gap_mm":      round(gap_mm,   1) if not np.isnan(gap_mm)           else "nan",
        "l5_sacrum_overlap_mm":  round(l5_sac_overlap_mm, 1) if not np.isnan(gap_mm) else "nan",
        "plausible":             plausible,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 2-D PNG summary
# ─────────────────────────────────────────────────────────────────────────────

def _label_to_rgba(lbl_slice: np.ndarray) -> np.ndarray:
    H, W  = lbl_slice.shape
    rgba  = np.zeros((H, W, 4), dtype=np.float32)
    for cls, color in RGBA_MAP.items():
        m = lbl_slice == cls
        if m.any():
            rgba[m] = color
    return rgba


def _lumbosacral_center(lbl: np.ndarray) -> Tuple[int, int, int]:
    D, H, W = lbl.shape
    for classes in [[4, 5, 6, 7], [3, 4, 5, 7], [1, 2, 3, 4, 5, 6, 7]]:
        m = np.isin(lbl, classes)
        if m.any():
            coords = np.argwhere(m)
            return (int(coords[:, 0].mean()), int(coords[:, 1].mean()), W // 2)
    return D // 2, H // 2, W // 2


def save_2d_summary(
    image_np:   np.ndarray,
    spine_lbl:  np.ndarray,
    pelv_lbl:   np.ndarray,
    fused_lbl:  np.ndarray,
    patient_id: str,
    metrics:    Dict,
    output_path: Path,
) -> None:
    cz, cy, cx = _lumbosacral_center(fused_lbl)
    img_n      = np.clip(image_np, 0.0, 1.0)   # pipeline already normalises to [0,1]

    def _cor(lbl):  return lbl[:, cy, :]
    def _ax(lbl):   return lbl[cz, :, :]
    def _img_cor(): return img_n[:, cy, :]
    def _img_ax():  return img_n[cz, :, :]

    rows = [
        ("Spine only",  _img_cor(), _cor(spine_lbl), _img_ax(), _ax(spine_lbl)),
        ("Pelvic only", _img_cor(), _cor(pelv_lbl),  _img_ax(), _ax(pelv_lbl)),
        ("Fused",       _img_cor(), _cor(fused_lbl), _img_ax(), _ax(fused_lbl)),
    ]

    fig, axes = plt.subplots(3, 4, figsize=(16, 12))
    status    = "✓ PASS" if metrics["plausible"] else "✗ FAIL"
    violation = ""
    if metrics["spine_wins_violation"] > 0:
        violation = f"  ⚠ L5↔Sacrum overlap: {metrics['spine_wins_violation']} vx"
    if metrics["l6_wins_violation"] > 0:
        violation += f"  ⚠ L6↔Sacrum: {metrics['l6_wins_violation']} vx"

    fig.suptitle(
        f"Pelvic Alignment QC (CACHE)  —  Patient {patient_id}  {status}\n"
        f"Sacrum: {metrics['sacrum_voxels']:,} vx  "
        f"L-Hip: {metrics['l_hip_voxels']:,} vx  "
        f"R-Hip: {metrics['r_hip_voxels']:,} vx  "
        f"L5-Sacrum gap: {metrics['l5_sacrum_gap_mm']} mm"
        f"{violation}",
        fontsize=11, fontweight="bold",
        color="green" if metrics["plausible"] else "red",
    )

    col_titles = ["Coronal (image)", "Coronal (+ labels)", "Axial (image)", "Axial (+ labels)"]
    for ci, ct in enumerate(col_titles):
        axes[0, ci].set_title(ct, fontsize=9)

    for ri, (row_title, img_cor, lbl_cor, img_ax, lbl_ax) in enumerate(rows):
        axes[ri, 0].imshow(img_cor, cmap="gray", origin="lower", aspect="equal")
        axes[ri, 0].set_ylabel(row_title, fontsize=9)
        axes[ri, 0].axis("off")

        axes[ri, 1].imshow(img_cor, cmap="gray", origin="lower", aspect="equal")
        axes[ri, 1].imshow(_label_to_rgba(lbl_cor), origin="lower", aspect="equal")
        axes[ri, 1].axis("off")

        axes[ri, 2].imshow(img_ax, cmap="gray", origin="lower", aspect="equal")
        axes[ri, 2].axis("off")

        axes[ri, 3].imshow(img_ax, cmap="gray", origin="lower", aspect="equal")
        axes[ri, 3].imshow(_label_to_rgba(lbl_ax), origin="lower", aspect="equal")
        axes[ri, 3].axis("off")

    patches = [
        mpatches.Patch(color=RGBA_MAP[c][:3], label=CLASS_NAMES[c], alpha=0.85)
        for c in range(1, 10)
    ]
    fig.legend(handles=patches, loc="lower center", ncol=9,
               fontsize=8, bbox_to_anchor=(0.5, 0.005))
    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    plt.savefig(output_path, dpi=110, bbox_inches="tight")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
# 3-D Plotly HTML
# ─────────────────────────────────────────────────────────────────────────────

def _mesh_traces(
    image_vol:    np.ndarray,
    label_vol:    np.ndarray,
    label_colors: Dict[int, str],
    bone_opacity: float = 0.08,
    lbl_opacity:  float = 0.82,
    downsample:   int   = 2,
    showlegend:   bool  = True,
    bone_thr:     float = 0.55,
    min_voxels:   int   = MIN_VOXELS,
):
    try:
        from skimage.measure import marching_cubes
        from scipy.ndimage import gaussian_filter
        import plotly.graph_objects as go
    except ImportError as exc:
        log.warning("3-D render unavailable: %s", exc)
        return []

    orig_H = image_vol.shape[1]
    ds     = downsample

    def _tr(verts, faces, color, opacity, name, flat=False):
        v = verts * ds
        return go.Mesh3d(
            x=v[:, 2], y=v[:, 0], z=(orig_H - v[:, 1]),
            i=faces[:, 0], j=faces[:, 1], k=faces[:, 2],
            color=color, opacity=opacity,
            name=name, legendgroup=name,
            showlegend=showlegend, hoverinfo="name",
            flatshading=flat,
            lighting=dict(ambient=0.45, diffuse=0.8, specular=0.2,
                          roughness=0.5, fresnel=0.1),
            lightposition=dict(x=100, y=200, z=150),
        )

    traces = []

    img_ds = gaussian_filter(image_vol[::ds, ::ds, ::ds].astype("float32"), sigma=0.8)
    if img_ds.max() > bone_thr:
        try:
            vv, ff, _, _ = marching_cubes(img_ds, level=bone_thr)
            traces.append(_tr(vv, ff, "#c8c8c8", bone_opacity, "Bone (CT)", flat=True))
        except Exception as exc:
            log.debug("bone isosurface: %s", exc)

    lbl_ds = label_vol[::ds, ::ds, ::ds].astype("int32")
    for cls, color in label_colors.items():
        if int((label_vol == cls).sum()) < min_voxels:
            continue
        mask = (lbl_ds == cls).astype("float32")
        if mask.sum() < 10:
            continue
        try:
            vv, ff, _, _ = marching_cubes(mask, level=0.5)
            traces.append(_tr(vv, ff, color, lbl_opacity, CLASS_NAMES[cls]))
        except Exception as exc:
            log.debug("label mesh cls %d: %s", cls, exc)

    return traces


def _scene_layout() -> dict:
    ax = dict(showgrid=False, zeroline=False,
              showticklabels=False, showbackground=False)
    return dict(
        xaxis={**ax, "title": "R→L"},
        yaxis={**ax, "title": "P→A"},
        zaxis={**ax, "title": "I→S"},
        camera=dict(
            up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0),
            eye=dict(x=0.9, y=-2.0, z=0.1),
        ),
        aspectmode="data",
        bgcolor="rgb(18,18,28)",
    )


_SCENE_KEYS = ["scene", "scene2", "scene3"]


def save_3d_html(
    image_np:    np.ndarray,
    spine_lbl:   np.ndarray,
    pelv_lbl:    np.ndarray,
    fused_lbl:   np.ndarray,
    patient_id:  str,
    metrics:     Dict,
    output_path: Path,
    downsample:  int = 2,
) -> None:
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
    except ImportError:
        log.warning("plotly not installed -- skipping 3-D render for %s.", patient_id)
        return

    panels = [
        (spine_lbl,  SPINE_COLORS,  "Spine only (L1-L6)"),
        (pelv_lbl,   PELVIC_COLORS, "Pelvic mask (cached)"),
        (fused_lbl,  ALL_COLORS,    "Fused  [as trained]"),
    ]

    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{"type": "scene"}] * 3],
        subplot_titles=[p[2] for p in panels],
        horizontal_spacing=0.01,
    )

    for col, (lbl, colors, _) in enumerate(panels):
        for tr in _mesh_traces(
            image_np, lbl, colors,
            downsample=downsample,
            showlegend=(col == 0),
        ):
            fig.add_trace(tr, row=1, col=col + 1)

    fig.update_layout(**{_SCENE_KEYS[i]: _scene_layout() for i in range(3)})

    status    = "✓ PASS" if metrics["plausible"] else "✗ FAIL"
    violation = ""
    if metrics["spine_wins_violation"] > 0:
        violation = f"  ⚠ L5/Sacrum overlap: {metrics['spine_wins_violation']} vx"
    if metrics["l6_wins_violation"] > 0:
        violation += f"  ⚠ L6/Sacrum: {metrics['l6_wins_violation']} vx"

    fig.update_layout(
        title=dict(
            text=(
                f"Patient {patient_id}  —  Pelvic Alignment QC (CACHE)  {status}<br>"
                f"<sup>Sacrum: {metrics['sacrum_voxels']:,} vx  "
                f"L-Hip: {metrics['l_hip_voxels']:,} vx  "
                f"R-Hip: {metrics['r_hip_voxels']:,} vx  "
                f"L5-Sacrum gap: {metrics['l5_sacrum_gap_mm']} mm"
                f"{violation}</sup>"
            ),
            x=0.5, xanchor="center",
            font=dict(size=13, color="white"),
        ),
        height=680,
        paper_bgcolor="rgb(12,12,22)",
        font=dict(color="white"),
        legend=dict(
            x=0.003, y=0.97,
            bgcolor="rgba(30,30,50,0.85)",
            bordercolor="rgba(255,255,255,0.15)", borderwidth=1,
            font=dict(size=10),
            title=dict(text="Structure", font=dict(size=11)),
        ),
        margin=dict(l=5, r=5, t=95, b=30),
    )
    fig.add_annotation(
        text="Drag=rotate  Scroll=zoom  Shift+drag=pan  Click legend=toggle",
        x=0.5, y=-0.04, xref="paper", yref="paper",
        showarrow=False, font=dict(size=9, color="rgba(255,255,255,0.45)"),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path), include_plotlyjs="cdn")
    log.info("  3-D HTML -> %s", output_path.name)


# ─────────────────────────────────────────────────────────────────────────────
# Main QC runner
# ─────────────────────────────────────────────────────────────────────────────

def run_pelvic_alignment_qc(
    raw_dir:     Path,
    splits_path: Path,
    cache_dir:   Path,
    output_dir:  Path,
    split:       str  = "all",
    max_cases:   int  = 0,
    downsample:  int  = 2,
    no_3d:       bool = False,
) -> None:
    from src.data.pipeline import (
        load_splits_from_json,
        load_dataset,
        classify_cases,
    )

    raw_dir     = Path(raw_dir)
    splits_path = Path(splits_path)
    cache_dir   = Path(cache_dir)
    output_dir  = Path(output_dir)

    html_dir = output_dir / "html"
    png_dir  = output_dir / "png"
    html_dir.mkdir(parents=True, exist_ok=True)
    png_dir.mkdir(parents=True, exist_ok=True)

    if not cache_dir.exists():
        log.error("cache_dir does not exist: %s", cache_dir)
        sys.exit(1)

    n_pt = len(list(cache_dir.glob("*__*__*_image.pt")))
    log.info("=== Pelvic Alignment QC (Cache Edition) ===")
    log.info("Cache:  %s  (%d versioned tensors)", cache_dir, n_pt)
    log.info("Output: %s", output_dir)

    # ── load splits ───────────────────────────────────────────────────────────
    matched_json = raw_dir / "matched" / "colonog_matched_pairs.json"
    all_records  = load_dataset(
        raw_dir / "ctspine1k",
        matched_pairs_json=matched_json if matched_json.exists() else None,
    )
    lstv_indices, _, stem_to_type = classify_cases(
        all_records, cache_path=raw_dir / "lstv_scan_cache.json"
    )
    lstv_stems = {Path(all_records[i].image).stem for i in lstv_indices}

    if splits_path.exists():
        splits, _ = load_splits_from_json(splits_path, lstv_stems=lstv_stems)
    else:
        log.error("splits.json not found: %s", splits_path)
        sys.exit(1)

    # ── collect fused cases (those with pelvic_mask) ──────────────────────────
    split_names = list(splits.keys()) if split == "all" else [split]
    candidates = [
        r
        for sn in split_names
        for r in splits.get(sn, [])
        if r.pelvic_mask is not None
    ]

    if max_cases > 0:
        import random
        random.seed(42)
        random.shuffle(candidates)
        candidates = candidates[:max_cases]

    log.info("Fused cases to QC: %d  (split=%s  max_cases=%s)",
             len(candidates), split, max_cases if max_cases > 0 else "unlimited")

    if not candidates:
        log.error("No fused cases found (pelvic_mask is not None).")
        sys.exit(1)

    # ── per-case loop ─────────────────────────────────────────────────────────
    rows    = []
    n_pass  = n_fail = 0
    n_miss  = 0
    n_no_pelv = 0

    for idx, record in enumerate(candidates):
        pid  = record.patient_id
        stem = record.cache_stem
        log.info("[%d/%d] %s  (stem=%s)", idx + 1, len(candidates), pid, stem)

        result = load_from_cache(record, cache_dir)

        if result is None:
            log.warning("  CACHE MISS: %s_image.pt not found.", stem)
            rows.append({
                "patient_id":      pid,
                "plausible":       False,
                "cache_hit":       False,
                "pelvic_in_cache": False,
                "error":           "CACHE_MISS",
                "split":           split,
                "image":           record.image,
                "pelvic":          record.pelvic_mask,
            })
            n_fail += 1
            n_miss += 1
            continue

        image_np, fused_np = result

        pelvic_in_cache = bool(np.any(np.isin(fused_np, PELVIC_CLASS_IDS)))
        if not pelvic_in_cache:
            log.warning("  PELVIC_ABSENT: no classes 7-9 in cached label for %s.", pid)
            n_no_pelv += 1

        spine_np, pelv_np = derive_panels(fused_np)
        metrics = compute_alignment_metrics(spine_np, fused_np)
        metrics["patient_id"]      = pid
        metrics["split"]           = split
        metrics["image"]           = record.image
        metrics["pelvic"]          = record.pelvic_mask
        metrics["cache_hit"]       = True
        metrics["pelvic_in_cache"] = pelvic_in_cache
        rows.append(metrics)

        tag = "PASS" if metrics["plausible"] else "FAIL"
        log.info(
            "  [%s] sacrum=%d  l_hip=%d  r_hip=%d  gap=%s mm  "
            "spine_wins_viol=%d  l6_viol=%d",
            tag,
            metrics["sacrum_voxels"],
            metrics["l_hip_voxels"],
            metrics["r_hip_voxels"],
            metrics["l5_sacrum_gap_mm"],
            metrics["spine_wins_violation"],
            metrics["l6_wins_violation"],
        )

        if metrics["plausible"]: n_pass += 1
        else:                    n_fail += 1

        try:
            png_path = png_dir / f"{pid}_alignment.png"
            save_2d_summary(image_np, spine_np, pelv_np, fused_np,
                            pid, metrics, png_path)
            log.info("  PNG -> %s", png_path.name)
        except Exception as exc:
            log.warning("  PNG failed for %s: %s", pid, exc)

        if not no_3d:
            try:
                html_path = html_dir / f"{pid}_alignment.html"
                save_3d_html(image_np, spine_np, pelv_np, fused_np,
                             pid, metrics, html_path, downsample=downsample)
            except Exception as exc:
                log.warning("  HTML failed for %s: %s", pid, exc)

    # ── write summary ─────────────────────────────────────────────────────────
    import pandas as pd

    df       = pd.DataFrame(rows)
    csv_path = output_dir / "pelvic_alignment_summary.csv"
    df.to_csv(csv_path, index=False)

    fail_pids = df[~df["plausible"].astype(bool)]["patient_id"].tolist()

    summary_lines = [
        "=" * 72,
        " SpineSurg-CT — Pelvic Alignment QC Report  [CACHE EDITION]",
        "=" * 72,
        "",
        f"  Cache dir        : {cache_dir}",
        f"  Total cases QC'd : {len(rows)}",
        f"  PASS             : {n_pass}  ({100*n_pass/max(1,len(rows)):.0f}%)",
        f"  FAIL             : {n_fail}  ({100*n_fail/max(1,len(rows)):.0f}%)",
        f"  Cache miss       : {n_miss} cases",
        f"  Pelvic absent    : {n_no_pelv} cases (cache hit but 0 pelvic voxels)",
        "",
        "  NOTE: These labels are the EXACT tensors fed to the model.",
        "        A FAIL here means the training data itself is wrong.",
        "        Fused cases use direct voxel-wise overlay (no spatial alignment).",
        "        If pelvic_absent > 0, check that series_match is correct in",
        "        colonog_matched_pairs.json (only uid_confirmed / affine_confirmed",
        "        cases should be fused).",
        "",
        "  Failure criteria (any one triggers FAIL):",
        "    • sacrum voxels < 50",
        "    • L5 voxels overwritten by sacrum  (Spine-Wins violation)",
        "    • L6 voxels overwritten by sacrum  (Spine-Wins violation)",
        "    • L5-sacrum gap > 30 mm",
        "",
    ]
    if n_miss > 0:
        miss_pids = (df[df["cache_hit"] == False]["patient_id"].tolist()
                     if "cache_hit" in df.columns else [])
        summary_lines += [
            "  CACHE MISS cases (run precache.py to fix):",
            *[f"    • {p}" for p in miss_pids],
            "",
        ]
    if n_fail > 0:
        summary_lines += [
            "  FAIL cases:",
            *[f"    • {p}" for p in fail_pids],
            "",
        ]
    ok = df[df["plausible"].astype(bool)] if "plausible" in df.columns else df.iloc[0:0]
    if len(ok) > 0 and "sacrum_voxels" in ok.columns:
        summary_lines += [
            "  Statistics (PASS cases only):",
            f"    sacrum voxels  — mean: {ok['sacrum_voxels'].mean():.0f}  "
            f"min: {ok['sacrum_voxels'].min():.0f}  max: {ok['sacrum_voxels'].max():.0f}",
            f"    L-hip voxels   — mean: {ok['l_hip_voxels'].mean():.0f}  "
            f"min: {ok['l_hip_voxels'].min():.0f}  max: {ok['l_hip_voxels'].max():.0f}",
            f"    R-hip voxels   — mean: {ok['r_hip_voxels'].mean():.0f}  "
            f"min: {ok['r_hip_voxels'].min():.0f}  max: {ok['r_hip_voxels'].max():.0f}",
            f"    L5-sacrum gap  — mean: {pd.to_numeric(ok['l5_sacrum_gap_mm'], errors='coerce').mean():.1f} mm",
            "",
        ]
    summary_lines += [
        f"  CSV      -> {csv_path}",
        f"  PNG dir  -> {png_dir}",
        f"  HTML dir -> {html_dir}  ({'enabled' if not no_3d else 'disabled'})",
        "=" * 72,
    ]
    summary_text = "\n".join(summary_lines)
    (output_dir / "pelvic_alignment_report.txt").write_text(summary_text)
    print(summary_text)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def _parse():
    p = argparse.ArgumentParser(
        description="QC pelvic alignment by reading the TRAINING CACHE (.pt tensors)."
    )
    p.add_argument("--raw_dir",    required=True)
    p.add_argument("--splits",     required=True)
    p.add_argument("--cache_dir",  required=True)
    p.add_argument("--output_dir", default="data/pelvic_alignment_qc")
    p.add_argument("--split",      default="all",
                   choices=["train", "val", "test", "all"])
    p.add_argument("--max_cases",  type=int, default=0)
    p.add_argument("--downsample", type=int, default=2)
    p.add_argument("--no_3d",      action="store_true")
    return p.parse_args()


if __name__ == "__main__":
    args = _parse()
    run_pelvic_alignment_qc(
        raw_dir     = Path(args.raw_dir),
        splits_path = Path(args.splits),
        cache_dir   = Path(args.cache_dir),
        output_dir  = Path(args.output_dir),
        split       = args.split,
        max_cases   = args.max_cases,
        downsample  = args.downsample,
        no_3d       = args.no_3d,
    )
