"""
SpineSurg-CT -- Augmentation Visualization & Quality Assessment
src/utils/augmentation_qc.py

Bug fixes vs original
---------------------
1. splits.json fallback: generates and saves the split when the file doesn't
   exist, using the already-loaded all_records and lstv_indices.

2. CopyPasteLSTVTransform now returns a CopyPasteResult namedtuple. QC code
   unpacks result.data (the augmented dict) and result.trajectory_lbl
   (the trajectory array) directly -- no more reading stale instance state
   from last_trajectory_lbl, which was unsafe across calls.

3. stem_to_record was built but never used. Removed.

4. Lumbarization/sacralization classification in QC now uses the
   stem_to_type mapping returned by classify_cases (no re-scan of label
   files, consistent with the cache).

5. Import of split_records and stem_to_type forwarded from pipeline import
   block so all pipeline symbols are imported in one place.

6. _label_inventory() added: computes per-class voxel counts and produces
   a one-line summary string used in logs, plot titles, and the quality
   CSV. Called for every preprocessed case (original, template, synthetic)
   so the output clearly shows what structures each study contains.

Author: Gregory Schwing, MD, PhD
"""

import argparse
import json
import logging
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import nibabel as nib
import numpy as np
import torch

log = logging.getLogger("spinesurg.augmentation_qc")

try:
    from src.utils.viz3d import render_3d_comparison
    _VIZ3D_AVAILABLE = True
except ImportError:
    _VIZ3D_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

LABEL_COLORS = {
    0: (0.0, 0.0, 0.0, 0.0),
    1: (0.2, 0.6, 1.0, 0.6),
    2: (0.2, 0.8, 1.0, 0.6),
    3: (0.2, 1.0, 0.8, 0.6),
    4: (0.2, 1.0, 0.4, 0.6),
    5: (0.6, 1.0, 0.2, 0.6),
    6: (1.0, 0.2, 0.2, 0.8),
    7: (1.0, 0.6, 0.0, 0.6),
    8: (0.8, 0.0, 0.8, 0.6),
    9: (0.6, 0.0, 1.0, 0.6),
}
CLASS_NAMES = {
    0: "bg", 1: "L1", 2: "L2", 3: "L3", 4: "L4", 5: "L5",
    6: "L6", 7: "sacrum", 8: "LH", 9: "RH",
}


# =============================================================================
# Label inventory
# =============================================================================

def _label_inventory(
    label_np: np.ndarray,
    has_pelvic_mask: bool = False,
    lstv_type: str = "normal",
    case_id: str = "",
    min_voxels: int = 50,
) -> Tuple[Dict[int, int], str]:
    """
    Compute per-class voxel counts for a label volume and return a
    structured dict plus a compact one-line summary string.

    Parameters
    ----------
    label_np        : (D, H, W) integer array, unified 10-class space
    has_pelvic_mask : whether pelvic fusion was attempted for this case
    lstv_type       : "normal", "lumbarization", or "sacralization"
    case_id         : short string used in the summary (display only)
    min_voxels      : threshold below which a class is considered absent

    Returns
    -------
    counts  : dict mapping class_id -> voxel_count (present classes only)
    summary : one-line string, e.g.
              "[0023] lumbarization | pelvic:YES | L1(23k) L2(22k) L3(25k)
               L4(21k) L5(20k) L6(15k) sacrum(140k) LH(77k) RH(70k)"
    """
    counts: Dict[int, int] = {}
    for cls in range(1, 10):
        n = int((label_np == cls).sum())
        if n >= min_voxels:
            counts[cls] = n

    def _fmt(n: int) -> str:
        return f"{n // 1000}k" if n >= 1000 else str(n)

    spine_parts  = [f"{CLASS_NAMES[c]}({_fmt(counts[c])})" for c in range(1, 7)  if c in counts]
    pelvic_parts = [f"{CLASS_NAMES[c]}({_fmt(counts[c])})" for c in range(7, 10) if c in counts]

    pelv_tag = "pelvic:YES" if pelvic_parts else ("pelvic:attempted(empty)" if has_pelvic_mask else "pelvic:NO")

    parts = [f"[{case_id}]", lstv_type, "|", pelv_tag, "|"]
    if spine_parts:
        parts += spine_parts
    else:
        parts.append("(no spine labels)")
    if pelvic_parts:
        parts += pelvic_parts

    return counts, " ".join(parts)


def _log_inventory(
    label_np: np.ndarray,
    role: str,
    has_pelvic_mask: bool = False,
    lstv_type: str = "normal",
    case_id: str = "",
) -> Tuple[Dict[int, int], str]:
    """
    Compute and log the label inventory for one case.

    role : "Original", "Template", "Synthetic", etc.
    Returns (counts, summary_string).
    """
    counts, summary = _label_inventory(
        label_np, has_pelvic_mask=has_pelvic_mask,
        lstv_type=lstv_type, case_id=case_id,
    )
    log.info("  [inventory] %-12s %s", role + ":", summary)
    return counts, summary


# =============================================================================
# Visualisation helpers
# =============================================================================

def _match_shapes(a: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    min_shape = tuple(min(sa, sb) for sa, sb in zip(a.shape, b.shape))
    slices    = tuple(slice(0, s) for s in min_shape)
    return a[slices], b[slices]


def _label_to_rgba(label_slice: np.ndarray) -> np.ndarray:
    H, W  = label_slice.shape
    rgba  = np.zeros((H, W, 4), dtype=np.float32)
    for cls, color in LABEL_COLORS.items():
        mask = (label_slice == cls)
        if mask.any():
            rgba[mask] = color
    return rgba


def _find_lumbosacral_center(label_vol: np.ndarray) -> Tuple[int, int, int]:
    """
    Find a display center slice in the lumbosacral region.

    PIR orientation: axis-1 is I->S (inferior to superior). We look for
    the inferior-most extent of the lumbosacral region on axis-1 and step
    65% up the SI span, which consistently lands around L4-S1 regardless
    of volume height.
    """
    D, H, W = label_vol.shape
    region  = None
    for classes in [[4, 5, 6, 7], [3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7]]:
        mask = np.isin(label_vol, classes)
        if mask.any():
            region = mask
            break
    if region is None:
        fg     = label_vol > 0
        region = fg if fg.any() else np.ones(label_vol.shape, dtype=bool)
    coords = np.argwhere(region)
    cy = int(np.clip(coords[:, 1].mean(), 0, H - 1))
    cx = W // 2
    cz = int(np.clip(coords[:, 0].mean(), 0, D - 1))
    return cz, cy, cx


def _tight_crop(image_vol: np.ndarray, label_vol: np.ndarray,
                pad: int = 30) -> Tuple[np.ndarray, np.ndarray]:
    fg = label_vol > 0
    if not fg.any():
        fg = image_vol > image_vol.min() + 1e-3
    if not fg.any():
        return image_vol, label_vol
    coords = np.argwhere(fg)
    lo     = np.maximum(coords.min(axis=0) - pad, 0)
    hi     = np.minimum(coords.max(axis=0) + pad + 1, np.array(image_vol.shape))
    slices = tuple(slice(lo[i], hi[i]) for i in range(3))
    return image_vol[slices], label_vol[slices]


def _inventory_subtitle(counts: Dict[int, int]) -> str:
    """
    Build a compact subtitle string from a counts dict for embedding in
    plot titles.  Shows present classes with voxel counts in thousands.
    """
    def _fmt(n):
        return f"{n // 1000}k" if n >= 1000 else str(n)
    parts = []
    for cls in range(1, 10):
        if cls in counts:
            parts.append(f"{CLASS_NAMES[cls]}:{_fmt(counts[cls])}")
    return "  ".join(parts) if parts else "(empty)"


def plot_case_grid(image_vol: np.ndarray, label_vol: np.ndarray, title: str,
                   output_path: Path, lstv_type: str = "",
                   inventory_counts: Optional[Dict[int, int]] = None,
                   hu_window: Tuple[float, float] = (-200, 800)) -> None:
    image_vol, label_vol = _tight_crop(image_vol, label_vol, pad=30)
    cz, cy, cx = _find_lumbosacral_center(label_vol)
    img_norm   = np.clip(image_vol, hu_window[0], hu_window[1])
    img_norm   = (img_norm - hu_window[0]) / (hu_window[1] - hu_window[0])
    slices = {
        "Axial":    (img_norm[cz, :, :],    label_vol[cz, :, :]),
        "Coronal":  (img_norm[:, cy, :],    label_vol[:, cy, :]),
        "Sagittal": (img_norm[:, :, cx].T,  label_vol[:, :, cx].T),
    }

    inv_str = _inventory_subtitle(inventory_counts) if inventory_counts else ""

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle(f"{title}\n{lstv_type}\n{inv_str}", fontsize=11, fontweight="bold")
    for col, (plane, (img_sl, lbl_sl)) in enumerate(slices.items()):
        axes[0, col].imshow(img_sl, cmap="gray", origin="lower", aspect="equal")
        axes[0, col].set_title(f"{plane} (image)", fontsize=10)
        axes[0, col].axis("off")
        axes[1, col].imshow(img_sl, cmap="gray", origin="lower", aspect="equal")
        axes[1, col].imshow(_label_to_rgba(lbl_sl), origin="lower", aspect="equal")
        axes[1, col].set_title(f"{plane} (+ labels)", fontsize=10)
        axes[1, col].axis("off")
    patches = [mpatches.Patch(color=LABEL_COLORS[c][:3], label=CLASS_NAMES[c], alpha=0.8)
               for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]]
    fig.legend(handles=patches, loc="lower center", ncol=9, fontsize=8,
               bbox_to_anchor=(0.5, 0.01))
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close()
    log.info("  Saved: %s", output_path.name)


def plot_comparison_grid(real_image: np.ndarray, real_label: np.ndarray, real_title: str,
                         synth_image: np.ndarray, synth_label: np.ndarray, synth_title: str,
                         output_path: Path, lstv_type: str = "",
                         real_counts: Optional[Dict[int, int]] = None,
                         synth_counts: Optional[Dict[int, int]] = None) -> None:
    real_image,  real_label  = _tight_crop(real_image,  real_label,  pad=30)
    synth_image, synth_label = _tight_crop(synth_image, synth_label, pad=30)

    def _prep(img, lbl):
        img_n = (np.clip(img, -200, 800) + 200) / 1000
        _, cy, _ = _find_lumbosacral_center(lbl)
        return img_n[:, cy, :], lbl[:, cy, :]

    r_img, r_lbl = _prep(real_image,  real_label)
    s_img, s_lbl = _prep(synth_image, synth_label)

    r_inv = _inventory_subtitle(real_counts)  if real_counts  else ""
    s_inv = _inventory_subtitle(synth_counts) if synth_counts else ""

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f"Real vs Synthetic -- {lstv_type}", fontsize=13, fontweight="bold")
    for col, (img, lbl, t, inv) in enumerate([
        (r_img, r_lbl, real_title,  r_inv),
        (s_img, s_lbl, synth_title, s_inv),
    ]):
        axes[0, col].imshow(img, cmap="gray", origin="lower")
        axes[0, col].set_title(f"{t}\n{inv}", fontsize=9)
        axes[0, col].axis("off")
        axes[1, col].imshow(img, cmap="gray", origin="lower")
        axes[1, col].imshow(_label_to_rgba(lbl), origin="lower")
        axes[1, col].set_title(f"{t} + labels", fontsize=9)
        axes[1, col].axis("off")
    patches = [mpatches.Patch(color=LABEL_COLORS[c][:3], label=CLASS_NAMES[c], alpha=0.8)
               for c in [1, 2, 3, 4, 5, 6, 7]]
    fig.legend(handles=patches, loc="lower center", ncol=7, fontsize=9,
               bbox_to_anchor=(0.5, 0.01))
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close()


# =============================================================================
# Quality metrics
# =============================================================================

def compute_ms_ssim(img_a: np.ndarray, img_b: np.ndarray,
                    hu_min: float = -1000, hu_max: float = 1000) -> float:
    try:
        from skimage.metrics import structural_similarity as ssim
    except ImportError:
        return float("nan")
    img_a, _ = _tight_crop(img_a, img_a > img_a.min())
    img_b, _ = _tight_crop(img_b, img_b > img_b.min())
    img_a, img_b = _match_shapes(img_a, img_b)
    a = (np.clip(img_a, hu_min, hu_max) - hu_min) / (hu_max - hu_min)
    b = (np.clip(img_b, hu_min, hu_max) - hu_min) / (hu_max - hu_min)
    if a.shape[0] < 2:
        return float("nan")
    cz     = a.shape[0] // 2
    scores = []
    for dz in [-5, 0, 5]:
        z = int(np.clip(cz + dz, 0, a.shape[0] - 1))
        if a[z].shape == b[z].shape and min(a[z].shape) > 1:
            scores.append(ssim(a[z], b[z], data_range=1.0))
    return float(np.mean(scores)) if scores else float("nan")


def compute_ncc(img_a: np.ndarray, img_b: np.ndarray) -> float:
    img_a, img_b = _match_shapes(img_a, img_b)
    a = img_a.ravel().astype(np.float64)
    b = img_b.ravel().astype(np.float64)
    a -= a.mean()
    b -= b.mean()
    denom = np.sqrt((a**2).sum() * (b**2).sum())
    return float(np.dot(a, b) / denom) if denom >= 1e-8 else 0.0


def _extract_radiomics_features(image_vol: np.ndarray, label_vol: np.ndarray,
                                 roi_classes: List[int] = None) -> Optional[np.ndarray]:
    if roi_classes is None:
        roi_classes = [4, 5, 6, 7]
    try:
        from skimage.feature import graycomatrix, graycoprops
    except ImportError:
        return None
    roi_mask = np.isin(label_vol, roi_classes)
    if not roi_mask.any():
        return None
    roi_voxels = np.clip(image_vol[roi_mask], -200, 800)
    feats = [
        roi_voxels.mean(), roi_voxels.std(),
        np.percentile(roi_voxels, 10), np.percentile(roi_voxels, 25),
        np.percentile(roi_voxels, 50), np.percentile(roi_voxels, 75),
        np.percentile(roi_voxels, 90),
        float(np.sum((roi_voxels - roi_voxels.mean())**3) /
              max((roi_voxels.std()**3 * len(roi_voxels)), 1e-8)),
        float(np.sum((roi_voxels - roi_voxels.mean())**4) /
              max((roi_voxels.std()**4 * len(roi_voxels)), 1e-8)),
        roi_mask.sum(),
    ]
    coords = np.argwhere(roi_mask)
    cz     = int(coords[:, 0].mean())
    sl     = np.clip(image_vol[cz], -200, 800)
    sl_q   = ((sl + 200) / 1000 * 63).astype(np.uint8).clip(0, 63)
    glcm   = graycomatrix(sl_q, distances=[1, 3], angles=[0, np.pi / 4],
                          levels=64, symmetric=True, normed=True)
    for prop in ["contrast", "dissimilarity", "homogeneity", "energy", "correlation"]:
        feats.append(float(graycoprops(glcm, prop).mean()))
    return np.array(feats, dtype=np.float64)


def compute_one_to_all_nn_distance(synth_features: np.ndarray,
                                    real_features_list: List[np.ndarray],
                                    ) -> Dict[str, float]:
    from scipy.spatial.distance import cosine
    distances = []
    for rf in real_features_list:
        try:
            distances.append(cosine(synth_features, rf))
        except Exception:
            continue
    if not distances:
        return {"mean_nn_dist": float("nan"), "min_nn_dist": float("nan"),
                "nearest_real_idx": -1}
    distances = np.array(distances)
    return {
        "mean_nn_dist":     float(distances.mean()),
        "min_nn_dist":      float(distances.min()),
        "nearest_real_idx": int(np.argmin(distances)),
    }


def check_label_plausibility(label_vol: np.ndarray, lstv_type: str,
                              min_voxels: int = 50) -> Dict[str, object]:
    l6_vox = int((label_vol == 6).sum())
    l5_vox = int((label_vol == 5).sum())
    l4_vox = int((label_vol == 4).sum())
    l3_vox = int((label_vol == 3).sum())
    checks: Dict[str, object] = {}
    if lstv_type == "lumbarization":
        checks["l6_present"]     = l6_vox >= min_voxels
        checks["l6_voxel_count"] = l6_vox
        checks["l5_present"]     = l5_vox >= min_voxels
        checks["l4_present"]     = l4_vox >= min_voxels
        checks["plausible"]      = (checks["l6_present"] and
                                    checks["l5_present"] and
                                    checks["l4_present"])
    elif lstv_type == "sacralization":
        checks["l5_absent"]      = l5_vox < min_voxels
        checks["l5_voxel_count"] = l5_vox
        checks["l4_present"]     = l4_vox >= min_voxels
        checks["l3_present"]     = l3_vox >= min_voxels
        checks["plausible"]      = (checks["l5_absent"] and
                                    checks["l4_present"] and
                                    checks["l3_present"])
    return checks


# =============================================================================
# Main QC runner
# =============================================================================

def run_augmentation_qc(
    raw_dir: Path,
    splits_path: Path,
    output_dir: Path,
    n_examples: int = 5,
    n_synthetic_per_real: int = 3,
    transform_type: str = "Affine",
    sacralization_registration_cache_dir: Optional[Path] = None,
    enable_3d: bool = True,
) -> None:
    from src.data.pipeline import (
        CaseRecord, PreprocessedCase,
        load_dataset, classify_cases,
        load_splits_from_json, split_records,
        preprocess_entry, CopyPasteLSTVTransform,
    )

    output_dir   = Path(output_dir)
    vis_lumb     = output_dir / "visuals"   / "lumbarization"
    vis_sacral   = output_dir / "visuals"   / "sacralization"
    viz3d_lumb   = output_dir / "visuals3d" / "lumbarization"
    viz3d_sacral = output_dir / "visuals3d" / "sacralization"
    metrics_dir  = output_dir / "metrics"
    for d in [vis_lumb, vis_sacral, viz3d_lumb, viz3d_sacral, metrics_dir]:
        d.mkdir(parents=True, exist_ok=True)

    log.info("=== Augmentation QC ===")
    log.info("Output: %s", output_dir)

    matched_json = raw_dir / "matched" / "colonog_matched_pairs.json"
    all_records  = load_dataset(
        raw_dir / "ctspine1k",
        matched_pairs_json=matched_json if matched_json.exists() else None,
    )
    lstv_indices, normal_indices, stem_to_type = classify_cases(
        all_records, cache_path=raw_dir / "lstv_scan_cache.json")

    lstv_stems = {Path(all_records[i].image).stem for i in lstv_indices}

    splits_path = Path(splits_path)
    if splits_path.exists():
        splits, _ = load_splits_from_json(splits_path, lstv_stems=lstv_stems)
    else:
        log.info("splits.json not found at %s -- generating and saving.", splits_path)
        splits, _ = split_records(all_records, lstv_indices, splits_path=splits_path)
    train_stems = {Path(r.image).stem for r in splits["train"]}

    lumb_records:   List[CaseRecord] = []
    sacral_records: List[CaseRecord] = []
    for i in lstv_indices:
        rec        = all_records[i]
        label_stem = Path(rec.label).stem
        if Path(rec.image).stem not in train_stems:
            continue
        t = stem_to_type.get(label_stem, "normal")
        if t == "lumbarization":
            lumb_records.append(rec)
        elif t == "sacralization":
            sacral_records.append(rec)

    normal_train_records: List[CaseRecord] = [
        all_records[i] for i in normal_indices
        if all_records[i].dataset == "spine"
        and Path(all_records[i].image).stem in train_stems
    ]

    log.info("Found: %d lumbarization, %d sacralization, %d normal training cases",
             len(lumb_records), len(sacral_records), len(normal_train_records))

    # Print a per-case inventory summary for ALL LSTV training cases
    log.info("=" * 70)
    log.info("LSTV case inventory (training split only):")
    log.info("=" * 70)
    for rec in lumb_records:
        pid = Path(rec.image).stem.split(".")[-1] if "." in Path(rec.image).stem else Path(rec.image).stem[-6:]
        log.info("  lumbarization  patient=%-6s  pelvic=%-3s  %s",
                 rec.patient_id,
                 "YES" if rec.pelvic_mask else "NO",
                 Path(rec.image).name)
    for rec in sacral_records:
        log.info("  sacralization  patient=%-6s  pelvic=%-3s  %s",
                 rec.patient_id,
                 "YES" if rec.pelvic_mask else "NO",
                 Path(rec.image).name)
    log.info("Normal training cases with pelvic mask: %d / %d",
             sum(1 for r in normal_train_records if r.pelvic_mask),
             len(normal_train_records))
    log.info("=" * 70)

    quality_rows = []
    # inventory_rows collects per-case inventory for the detailed report
    inventory_rows = []

    # -------------------------------------------------------------------------
    # LUMBARIZATION: CopyPaste QC
    # -------------------------------------------------------------------------
    log.info("--- Lumbarization (CopyPaste) QC ---")

    pool: List[PreprocessedCase] = []
    for rec in lumb_records[:n_examples]:
        try:
            pc = preprocess_entry(rec)
            counts, summary = _log_inventory(
                pc.label.squeeze(0).numpy(),
                role="Template",
                has_pelvic_mask=pc.has_pelvic_mask,
                lstv_type="lumbarization",
                case_id=rec.patient_id,
            )
            pool.append(pc)
            inventory_rows.append({
                "role": "template_lumb",
                "case_id": rec.patient_id,
                "lstv_type": "lumbarization",
                "has_pelvic_mask": rec.pelvic_mask is not None,
                **{f"cls_{c}": counts.get(c, 0) for c in range(1, 10)},
                "inventory": summary,
            })
        except Exception as exc:
            log.warning("  Could not preprocess %s: %s", rec.image, exc)

    real_lumb_features = []
    for pc in pool:
        f = _extract_radiomics_features(
            pc.image.squeeze(0).numpy(), pc.label.squeeze(0).numpy(),
            roi_classes=[4, 5, 6, 7])
        if f is not None:
            real_lumb_features.append(f)

    cp_transform  = CopyPasteLSTVTransform(lstv_pool=pool, apply_prob=1.0)
    rng           = random.Random(42)
    normal_sample = rng.sample(normal_train_records,
                               min(n_examples * n_synthetic_per_real,
                                   len(normal_train_records)))
    done_lumb = 0
    for normal_rec in normal_sample:
        if done_lumb >= n_examples:
            break

        try:
            normal_pc = preprocess_entry(normal_rec)
        except Exception:
            continue

        # Log inventory of original (normal destination) case
        orig_counts, orig_summary = _log_inventory(
            normal_pc.label.squeeze(0).numpy(),
            role="Original",
            has_pelvic_mask=normal_pc.has_pelvic_mask,
            lstv_type="normal",
            case_id=normal_rec.patient_id,
        )
        inventory_rows.append({
            "role": "original_lumb_dest",
            "case_id": normal_rec.patient_id,
            "lstv_type": "normal",
            "has_pelvic_mask": normal_rec.pelvic_mask is not None,
            **{f"cls_{c}": orig_counts.get(c, 0) for c in range(1, 10)},
            "inventory": orig_summary,
        })

        cp_result      = cp_transform({"image": normal_pc.image.clone(),
                                        "label": normal_pc.label.clone()})
        synth          = cp_result.data
        trajectory_lbl = cp_result.trajectory_lbl

        if (synth["label"] == 6).sum() < 50:
            continue

        n_img        = normal_pc.image.squeeze(0).numpy()
        n_lbl        = normal_pc.label.squeeze(0).numpy()
        s_img        = synth["image"].squeeze(0).numpy()
        s_lbl        = synth["label"].squeeze(0).numpy()
        normal_stem  = Path(normal_rec.image).stem[:20]

        # Log inventory of synthetic result
        synth_counts, synth_summary = _log_inventory(
            s_lbl,
            role="Synthetic",
            has_pelvic_mask=normal_pc.has_pelvic_mask,
            lstv_type="lumbarization",
            case_id=normal_rec.patient_id,
        )
        inventory_rows.append({
            "role": "synthetic_lumb",
            "case_id": normal_rec.patient_id,
            "lstv_type": "lumbarization",
            "has_pelvic_mask": normal_rec.pelvic_mask is not None,
            **{f"cls_{c}": synth_counts.get(c, 0) for c in range(1, 10)},
            "inventory": synth_summary,
        })

        # Template inventory for comparison panel
        tmpl_counts = {}
        if pool:
            tmpl_pc = pool[done_lumb % len(pool)]
            tmpl_counts, _ = _label_inventory(
                tmpl_pc.label.squeeze(0).numpy(),
                has_pelvic_mask=tmpl_pc.has_pelvic_mask,
                lstv_type="lumbarization",
                case_id=Path(tmpl_pc.source_record.image).stem.split(".")[-1],
            )

        plot_case_grid(s_img, s_lbl,
                       f"Synthetic Lumbarization (from {normal_stem})",
                       vis_lumb / f"synth_{done_lumb:02d}.png",
                       lstv_type="Lumbarization (CopyPaste)",
                       inventory_counts=synth_counts)

        if pool:
            tmpl_pc = pool[done_lumb % len(pool)]
            plot_comparison_grid(
                tmpl_pc.image.squeeze(0).numpy(),
                tmpl_pc.label.squeeze(0).numpy(),
                f"Real: {Path(tmpl_pc.source_record.image).stem[:20]}",
                s_img, s_lbl,
                f"Synthetic from: {normal_stem}",
                vis_lumb / f"comparison_{done_lumb:02d}.png",
                lstv_type="Lumbarization",
                real_counts=tmpl_counts,
                synth_counts=synth_counts,
            )

        plaus      = check_label_plausibility(s_lbl, "lumbarization")
        ms_ssim    = compute_ms_ssim(n_img, s_img)
        ncc        = compute_ncc(n_img, s_img)
        nn_scores  = {}
        synth_feat = _extract_radiomics_features(s_img, s_lbl, roi_classes=[4, 5, 6, 7])
        if synth_feat is not None and real_lumb_features:
            nn_scores = compute_one_to_all_nn_distance(synth_feat, real_lumb_features)

        quality_rows.append({
            "lstv_type":    "lumbarization",
            "augmentation": "copy_paste",
            "case_id":      normal_stem,
            "ms_ssim":      ms_ssim,
            "ncc":          ncc,
            "l6_voxels":    plaus.get("l6_voxel_count", 0),
            "plausible":    plaus.get("plausible", False),
            "mean_nn_dist": nn_scores.get("mean_nn_dist", float("nan")),
            "min_nn_dist":  nn_scores.get("min_nn_dist", float("nan")),
            "has_pelvic_orig":  normal_rec.pelvic_mask is not None,
            "orig_inventory":   orig_summary,
            "synth_inventory":  synth_summary,
        })

        if enable_3d and _VIZ3D_AVAILABLE and pool:
            tmpl_pc = pool[done_lumb % len(pool)]
            traj_lbl        = trajectory_lbl if trajectory_lbl is not None else np.zeros_like(n_lbl)
            s_lbl_with_traj = s_lbl.copy()
            if traj_lbl is not None and traj_lbl.any():
                s_lbl_with_traj[traj_lbl == 6] = 9
                for c in [1, 2, 3, 4, 5]:
                    s_lbl_with_traj[traj_lbl == c] = 8
                s_lbl_with_traj[traj_lbl == 7] = 7
            try:
                from src.utils.viz3d import render_3d_comparison
                tmpl_stem = Path(tmpl_pc.source_record.image).stem[:14]
                tmpl_inv  = _inventory_subtitle(tmpl_counts)
                orig_inv  = _inventory_subtitle(orig_counts)
                synth_inv = _inventory_subtitle(synth_counts)
                render_3d_comparison(
                    panels=[
                        (n_img, n_lbl,
                         f"Original: {normal_stem[:15]}\n{orig_inv}"),
                        (s_img, s_lbl_with_traj,
                         f"Synth+spline (9=curve 8=tips 7=pred)\n{synth_inv}"),
                        (tmpl_pc.image.squeeze(0).numpy(),
                         tmpl_pc.label.squeeze(0).numpy(),
                         f"Template: {tmpl_stem}\n{tmpl_inv}"),
                        (n_img, traj_lbl,
                         "Trajectory only (1-5=dst tips 6=curve 7=pred)"),
                    ],
                    output_path=viz3d_lumb / f"compare3d_{done_lumb:02d}.html",
                    title=f"Lumbarization 3D -- {normal_stem}",
                    lstv_type="Lumbarization (CopyPaste)",
                )
            except Exception as exc:
                log.debug("3D render failed (lumbarization): %s", exc)

        done_lumb += 1
        log.info("  Lumbarization example %d/%d done.", done_lumb, n_examples)

    # -------------------------------------------------------------------------
    # SACRALIZATION: Registration-based QC
    # -------------------------------------------------------------------------
    log.info("--- Sacralization (Registration) QC ---")

    try:
        from src.augmentation.sacralization_synthesis import (
            build_sacralization_field_pool, SacralizationSynthTransform,
        )
        has_ants = True
    except ImportError:
        log.warning("antspyx not available -- using DeleteL5 fallback.")
        has_ants = False

    real_sacral_features = []
    for rec in sacral_records:
        try:
            pc = preprocess_entry(rec)
            counts, summary = _log_inventory(
                pc.label.squeeze(0).numpy(),
                role="Real-sacral",
                has_pelvic_mask=pc.has_pelvic_mask,
                lstv_type="sacralization",
                case_id=rec.patient_id,
            )
            inventory_rows.append({
                "role": "real_sacral",
                "case_id": rec.patient_id,
                "lstv_type": "sacralization",
                "has_pelvic_mask": rec.pelvic_mask is not None,
                **{f"cls_{c}": counts.get(c, 0) for c in range(1, 10)},
                "inventory": summary,
            })
            f = _extract_radiomics_features(
                pc.image.squeeze(0).numpy(), pc.label.squeeze(0).numpy(),
                roi_classes=[4, 7])
            if f is None:
                f = _extract_radiomics_features(
                    pc.image.squeeze(0).numpy(), pc.label.squeeze(0).numpy(),
                    roi_classes=[3, 4, 5])
            if f is not None:
                real_sacral_features.append(f)
        except Exception:
            continue

    sacral_field_pool = []
    if has_ants and sacral_records:
        if (sacralization_registration_cache_dir and
                Path(sacralization_registration_cache_dir).exists()):
            effective_cache = Path(sacralization_registration_cache_dir)
            log.info("  Reusing training registration cache: %s", effective_cache)
        else:
            effective_cache = output_dir / "sacral_reg_cache_qc"
            if sacralization_registration_cache_dir:
                log.warning("  Training cache %s not found -- recomputing.",
                            sacralization_registration_cache_dir)

        all_dicts    = [{"image": r.image, "label": r.label,
                          "dataset": r.dataset, "pelvic_mask": r.pelvic_mask}
                         for r in all_records]
        train_global = [i for i, r in enumerate(all_records)
                        if Path(r.image).stem in train_stems]
        sacral_field_pool = build_sacralization_field_pool(
            data_list=all_dicts,
            lstv_indices=lstv_indices,
            normal_indices=normal_indices,
            train_global_indices=train_global,
            cache_dir=effective_cache,
            transform_type=transform_type,
            reference_per_sacral=1,
            raw_dir=raw_dir,
        )

    if sacral_field_pool:
        sacral_transform = SacralizationSynthTransform(
            field_pool=sacral_field_pool, apply_prob=1.0)
    else:
        from src.data.pipeline import DeleteL5Transform
        sacral_transform = DeleteL5Transform(apply_prob=1.0)
        log.warning("Using DeleteL5 fallback -- install antspyx for registration-based QC.")

    matched_normals   = [r for r in normal_train_records if r.pelvic_mask is not None]
    unmatched_normals = [r for r in normal_train_records if r.pelvic_mask is None]
    n_sacral_needed   = min(n_examples * n_synthetic_per_real, len(normal_train_records))

    if len(matched_normals) >= n_sacral_needed:
        sacral_sample = rng.sample(matched_normals, n_sacral_needed)
        log.info("Sacralization QC: %d matched cases", n_sacral_needed)
    elif matched_normals:
        extra         = min(n_sacral_needed - len(matched_normals), len(unmatched_normals))
        sacral_sample = matched_normals + rng.sample(unmatched_normals, extra)
        log.info("Sacralization QC: %d matched + %d unmatched", len(matched_normals), extra)
    else:
        sacral_sample = rng.sample(unmatched_normals,
                                   min(n_sacral_needed, len(unmatched_normals)))
        log.info("Sacralization QC: no matched cases -- using unmatched")

    done_sacral = 0
    for normal_rec in sacral_sample:
        if done_sacral >= n_examples:
            break

        try:
            normal_pc = preprocess_entry(normal_rec)
        except Exception:
            continue

        # Inventory of the original normal case going into sacralization synth
        orig_counts, orig_summary = _log_inventory(
            normal_pc.label.squeeze(0).numpy(),
            role="Original",
            has_pelvic_mask=normal_pc.has_pelvic_mask,
            lstv_type="normal",
            case_id=normal_rec.patient_id,
        )
        inventory_rows.append({
            "role": "original_sacral_dest",
            "case_id": normal_rec.patient_id,
            "lstv_type": "normal",
            "has_pelvic_mask": normal_rec.pelvic_mask is not None,
            **{f"cls_{c}": orig_counts.get(c, 0) for c in range(1, 10)},
            "inventory": orig_summary,
        })

        synth = sacral_transform({
            "image":           normal_pc.image.clone(),
            "label":           normal_pc.label.clone(),
            "has_pelvic_mask": normal_pc.has_pelvic_mask,
        })

        n_img       = normal_pc.image.squeeze(0).numpy()
        n_lbl       = normal_pc.label.squeeze(0).numpy()
        s_img       = synth["image"].squeeze(0).numpy()
        s_lbl       = synth["label"].squeeze(0).numpy()
        normal_stem = Path(normal_rec.image).stem[:20]

        synth_counts, synth_summary = _log_inventory(
            s_lbl,
            role="Synthetic",
            has_pelvic_mask=normal_pc.has_pelvic_mask,
            lstv_type="sacralization",
            case_id=normal_rec.patient_id,
        )
        inventory_rows.append({
            "role": "synthetic_sacral",
            "case_id": normal_rec.patient_id,
            "lstv_type": "sacralization",
            "has_pelvic_mask": normal_rec.pelvic_mask is not None,
            **{f"cls_{c}": synth_counts.get(c, 0) for c in range(1, 10)},
            "inventory": synth_summary,
        })

        plot_case_grid(s_img, s_lbl,
                       f"Synthetic Sacralization (from {normal_stem})",
                       vis_sacral / f"synth_{done_sacral:02d}.png",
                       lstv_type="Sacralization (Registration-based)",
                       inventory_counts=synth_counts)

        real_counts = {}
        if sacral_records:
            real_rec = sacral_records[done_sacral % len(sacral_records)]
            try:
                real_pc = preprocess_entry(real_rec)
                real_counts, _ = _label_inventory(
                    real_pc.label.squeeze(0).numpy(),
                    has_pelvic_mask=real_pc.has_pelvic_mask,
                    lstv_type="sacralization",
                    case_id=real_rec.patient_id,
                )
                plot_comparison_grid(
                    real_pc.image.squeeze(0).numpy(),
                    real_pc.label.squeeze(0).numpy(),
                    f"Real: {Path(real_rec.image).stem[:20]}",
                    s_img, s_lbl,
                    f"Synthetic from: {normal_stem}",
                    vis_sacral / f"comparison_{done_sacral:02d}.png",
                    lstv_type="Sacralization",
                    real_counts=real_counts,
                    synth_counts=synth_counts,
                )
            except Exception:
                pass

        plaus      = check_label_plausibility(s_lbl, "sacralization")
        ms_ssim    = compute_ms_ssim(n_img, s_img)
        ncc        = compute_ncc(n_img, s_img)
        nn_scores  = {}
        synth_feat = _extract_radiomics_features(s_img, s_lbl, roi_classes=[4, 7])
        if synth_feat is None:
            synth_feat = _extract_radiomics_features(s_img, s_lbl, roi_classes=[3, 4, 5, 6, 7])
        if synth_feat is not None and real_sacral_features:
            nn_scores = compute_one_to_all_nn_distance(synth_feat, real_sacral_features)

        quality_rows.append({
            "lstv_type":    "sacralization",
            "augmentation": "registration" if sacral_field_pool else "delete_l5",
            "case_id":      normal_stem,
            "ms_ssim":      ms_ssim,
            "ncc":          ncc,
            "l5_voxels":    plaus.get("l5_voxel_count", -1),
            "plausible":    plaus.get("plausible", False),
            "mean_nn_dist": nn_scores.get("mean_nn_dist", float("nan")),
            "min_nn_dist":  nn_scores.get("min_nn_dist", float("nan")),
            "has_pelvic_orig":  normal_rec.pelvic_mask is not None,
            "orig_inventory":   orig_summary,
            "synth_inventory":  synth_summary,
        })

        if enable_3d and _VIZ3D_AVAILABLE and sacral_field_pool:
            field       = (getattr(sacral_transform, "last_field", None) or sacral_field_pool[0])
            pair_name   = field.get("pair_name", "")
            sacral_stem = pair_name.split("_TO_")[0][:14] if "_TO_" in pair_name else pair_name
            orig_inv  = _inventory_subtitle(orig_counts)
            synth_inv = _inventory_subtitle(synth_counts)
            try:
                from src.utils.viz3d import preprocess_for_3d, render_3d_comparison
                tmpl_img_path = field.get("sacral_image_path")
                tmpl_lbl_path = field.get("sacral_label_path")
                if tmpl_img_path and tmpl_lbl_path:
                    t_img_3d, t_lbl_3d = preprocess_for_3d(tmpl_img_path, tmpl_lbl_path)
                else:
                    t_img_3d = field["sacral_img_np"]
                    t_lbl_3d = field["sacral_lbl_np"].astype(np.int32)
                tmpl_inv = _inventory_subtitle(real_counts)
                render_3d_comparison(
                    panels=[
                        (n_img, n_lbl,
                         f"Original: {normal_stem[:15]}\n{orig_inv}"),
                        (s_img, s_lbl,
                         f"Synthetic Sacralization\n{synth_inv}"),
                        (t_img_3d, t_lbl_3d,
                         f"Template: {sacral_stem[:14]}\n{tmpl_inv}"),
                    ],
                    output_path=viz3d_sacral / f"compare3d_{done_sacral:02d}.html",
                    title=f"Sacralization 3D -- {normal_stem}",
                    lstv_type="Sacralization (Registration-based)",
                )
            except Exception as exc:
                log.debug("3D render failed (sacralization): %s", exc)

        done_sacral += 1
        log.info("  Sacralization example %d/%d done.", done_sacral, n_examples)

    # -------------------------------------------------------------------------
    # Write metrics + inventory report
    # -------------------------------------------------------------------------
    import pandas as pd

    df       = pd.DataFrame(quality_rows)
    csv_path = metrics_dir / "augmentation_quality_report.csv"
    df.to_csv(csv_path, index=False)
    log.info("Quality report -> %s", csv_path)

    # Detailed per-case inventory CSV
    if inventory_rows:
        inv_df      = pd.DataFrame(inventory_rows)
        inv_csv     = metrics_dir / "case_inventory.csv"
        inv_df.to_csv(inv_csv, index=False)
        log.info("Case inventory -> %s", inv_csv)

    # Per-case inventory text block for the summary
    inv_lines = ["", "Per-case label inventory:", "-" * 64]
    for row in inventory_rows:
        inv_lines.append(f"  {row['role']:<26} {row['inventory']}")
    inv_lines.append("-" * 64)

    summary_lines = [
        "=" * 64,
        " SpineSurg-CT -- Augmentation Quality Summary",
        "=" * 64, "",
        "Metrics:",
        "  MS-SSIM     : structural similarity vs pre-augmentation normal (0-1)",
        "  NCC         : normalized cross-correlation vs pre-augmentation normal",
        "  mean_nn_dist: cosine dist in ROI feature space to all real LSTV cases",
        "  plausible   : label anatomy check (L6 present / L5 absent etc.)",
        "",
    ]
    for lstv_type, grp in df.groupby("lstv_type"):
        summary_lines += [
            f"  {lstv_type.upper()} (augmentation={grp['augmentation'].iloc[0]})",
            f"    n examples        : {len(grp)}",
            f"    MS-SSIM mean      : {grp['ms_ssim'].mean():.3f}",
            f"    NCC mean          : {grp['ncc'].mean():.3f}",
            f"    mean_nn_dist mean : {grp['mean_nn_dist'].mean():.3f}",
            f"    min_nn_dist mean  : {grp['min_nn_dist'].mean():.3f}",
            f"    plausible (%)     : {grp['plausible'].mean() * 100:.0f}%",
            f"    pelvic mask (orig): {grp['has_pelvic_orig'].sum()}/{len(grp)} cases",
            "",
        ]
    summary_lines += inv_lines
    summary_lines.append("=" * 64)
    summary_text = "\n".join(summary_lines)
    (metrics_dir / "augmentation_quality_summary.txt").write_text(summary_text)
    print(summary_text)
    log.info("Summary  -> %s", metrics_dir / "augmentation_quality_summary.txt")
    log.info("Visuals  -> %s", output_dir / "visuals")
    if enable_3d and _VIZ3D_AVAILABLE:
        log.info("3D HTML  -> %s", output_dir / "visuals3d")
    else:
        log.info("3D HTML  : skipped (pip install plotly to enable)")


# =============================================================================
# CLI
# =============================================================================

def _parse():
    p = argparse.ArgumentParser(description="Augmentation QC -- visuals + metrics.")
    p.add_argument("--raw_dir",            required=True)
    p.add_argument("--splits",             required=True)
    p.add_argument("--output_dir",         default="data/augmentation")
    p.add_argument("--n_examples",         type=int, default=5)
    p.add_argument("--n_per_real",         type=int, default=3)
    p.add_argument("--transform",          default="Affine",
                   choices=["Affine", "SyNRA", "SyN"])
    p.add_argument("--sacralization_registration_cache_dir", default=None)
    p.add_argument("--no_3d",             action="store_true")
    return p.parse_args()


if __name__ == "__main__":
    args = _parse()
    run_augmentation_qc(
        raw_dir=Path(args.raw_dir),
        splits_path=Path(args.splits),
        output_dir=Path(args.output_dir),
        n_examples=args.n_examples,
        n_synthetic_per_real=args.n_per_real,
        transform_type=args.transform,
        sacralization_registration_cache_dir=(
            Path(args.sacralization_registration_cache_dir)
            if args.sacralization_registration_cache_dir else None
        ),
        enable_3d=not args.no_3d,
    )
