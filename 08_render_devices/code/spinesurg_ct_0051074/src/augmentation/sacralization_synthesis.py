"""
SpineSurg-CT — On-the-fly Registration-Based Sacralization Synthesis
src/augmentation/sacralization_synthesis.py

How it works:
  Phase 1 (startup, runs once): For each real sacralization training case,
    PREPROCESS it to 256³ 1mm isotropic (same space as training tensors),
    then register to one reference normal case — also preprocessed.
    Store the deformation field in preprocessed/unit coordinate space.

  Phase 2 (training, on-the-fly): SacralizationSynthTransform picks a
    random stored field and applies it to the incoming preprocessed tensor.
    Because both the field and the tensor live in the same 256³ unit space,
    the warp is anatomically correct.

    9 stored fields × 533 normal training cases = ~4,800 unique synthetic
    sacralization variants per epoch.

  Key fix vs v1: registration is done in PREPROCESSED space (256³, 1mm
    isotropic, unit coords), not in original NIfTI space. Applying a field
    computed in original NIfTI space to a preprocessed tensor produces
    content in a tiny corner of the output — because the coordinate frames
    are incompatible. Working entirely in preprocessed space eliminates
    this mismatch.

Author: Gregory Schwing, MD, PhD
"""

import json
import logging
import random
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch

log = logging.getLogger("spinesurg.sacralization_synth")

L5_UNIFIED     = 5
SACRUM_UNIFIED = 7
MIN_VOXELS     = 50

# Unit coordinate system shared by all preprocessed 256³ tensors.
# Every tensor coming out of build_preprocessing_transforms() lives here.
_UNIT_ORIGIN    = (0.0, 0.0, 0.0)
_UNIT_SPACING   = (1.0, 1.0, 1.0)
_UNIT_DIRECTION = np.eye(3)


def _check_ants() -> bool:
    try:
        import ants
        return True
    except ImportError:
        log.warning("antspyx not installed — sacralization synthesis will fall back "
                    "to DeleteL5. Install with: pip install antspyx")
        return False


def _tensor_to_ants(arr: np.ndarray):
    """
    Convert a preprocessed 3D numpy array to an ANTs image in unit space.
    All preprocessed tensors share the same 1mm isotropic unit coordinate
    system so deformation fields computed between them are directly reusable.
    """
    import ants
    return ants.from_numpy(
        arr.astype(np.float32).copy(),
        origin=_UNIT_ORIGIN,
        spacing=_UNIT_SPACING,
        direction=_UNIT_DIRECTION,
    )


def _preprocess_nifti(image_path: str, label_path: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Preprocess a NIfTI pair to 256³ 1mm isotropic using the same pipeline
    transforms used during training. Returns (image_np, label_np).
    """
    from src.data.pipeline import build_preprocessing_transforms, CTSPINE1K_TO_UNIFIED
    preprocess = build_preprocessing_transforms(CTSPINE1K_TO_UNIFIED)
    result = preprocess({"image": image_path, "label": label_path, "dataset": "spine"})
    img_np = result["image"].squeeze(0).numpy()
    lbl_np = result["label"].squeeze(0).numpy().astype(np.float32)
    return img_np, lbl_np


def _fuse_l5_to_sacrum(label_arr: np.ndarray) -> np.ndarray:
    """
    Relabel L5 voxels adjacent to sacrum as sacrum (class 7).
    If >50% of L5 is adjacent, fuse all remaining L5 too (complete sacralization).
    """
    from scipy.ndimage import binary_dilation

    lbl         = label_arr.copy()
    l5_mask     = (lbl == L5_UNIFIED)
    sacrum_mask = (lbl == SACRUM_UNIFIED)

    if not l5_mask.any() or not sacrum_mask.any():
        # No sacrum label present (sacralization training cases lack pelvic GT).
        # Fall back: fuse all L5 into class 7.
        if l5_mask.any():
            lbl[l5_mask] = SACRUM_UNIFIED
        return lbl

    sacrum_dilated = binary_dilation(sacrum_mask, iterations=8)
    l5_to_fuse     = l5_mask & sacrum_dilated

    if not l5_to_fuse.any():
        # Dilation didn't reach L5 — fuse all L5 anyway (anatomically correct
        # for complete sacralization where L5 merges fully with S1).
        lbl[l5_mask] = SACRUM_UNIFIED
        return lbl

    lbl[l5_to_fuse] = SACRUM_UNIFIED

    # Complete sacralization: if >50% of L5 already fused, absorb the rest.
    fused_fraction = l5_to_fuse.sum() / max(l5_mask.sum(), 1)
    if fused_fraction > 0.5:
        lbl[lbl == L5_UNIFIED] = SACRUM_UNIFIED

    return lbl


def _register_preprocessed_pair(
    sacral_img_np: np.ndarray,
    ref_img_np: np.ndarray,
    cache_dir: Path,
    pair_name: str,
    transform_type: str = "SyNRA",
) -> Optional[Dict]:
    """
    Register preprocessed sacralization image to preprocessed reference image,
    both in unit coordinate space (256³, 1mm isotropic).

    Returns dict with paths to cached transform files, or None on failure.
    Caches to disk — subsequent runs load from cache instantly.
    """
    import ants

    pair_dir = cache_dir / pair_name
    pair_dir.mkdir(parents=True, exist_ok=True)
    prefix = str(pair_dir / "reg_")

    # ── Cache check ────────────────────────────────────────────────────────
    fwd_warp = pair_dir / "reg_1Warp.nii.gz"
    inv_warp = pair_dir / "reg_1InverseWarp.nii.gz"
    aff      = pair_dir / "reg_0GenericAffine.mat"

    if fwd_warp.exists() and aff.exists():
        log.info("  Using cached registration: %s", pair_name)
        return {
            "fwdtransforms": [str(fwd_warp), str(aff)],
            "invtransforms": [str(inv_warp), str(aff)],
            "pair_name":     pair_name,
        }

    # Affine-only cache (no warp file)
    if aff.exists() and not fwd_warp.exists():
        log.info("  Using cached affine registration: %s", pair_name)
        return {
            "fwdtransforms": [str(aff)],
            "invtransforms": [str(aff)],
            "pair_name":     pair_name,
        }

    # ── Register ───────────────────────────────────────────────────────────
    log.info("  Registering %s → reference (%s, preprocessed space) …",
             pair_name, transform_type)
    t0 = time.time()
    try:
        fixed  = _tensor_to_ants(ref_img_np)
        moving = _tensor_to_ants(sacral_img_np)

        result = ants.registration(
            fixed=fixed, moving=moving,
            type_of_transform=transform_type,
            outprefix=prefix,
            verbose=False,
        )
        log.info("  Done in %.1f s.", time.time() - t0)

        # Build return dict from actual output files
        ret = {"pair_name": pair_name}
        if (pair_dir / "reg_1Warp.nii.gz").exists():
            ret["fwdtransforms"] = [
                str(pair_dir / "reg_1Warp.nii.gz"),
                str(pair_dir / "reg_0GenericAffine.mat"),
            ]
            ret["invtransforms"] = [
                str(pair_dir / "reg_1InverseWarp.nii.gz"),
                str(pair_dir / "reg_0GenericAffine.mat"),
            ]
        else:
            # Affine-only (no warp file produced)
            ret["fwdtransforms"] = [str(pair_dir / "reg_0GenericAffine.mat")]
            ret["invtransforms"] = [str(pair_dir / "reg_0GenericAffine.mat")]
        return ret

    except Exception as e:
        log.error("  Registration failed (%s): %s", pair_name, e)
        return None


def build_sacralization_field_pool(
    data_list: List[Dict],
    lstv_indices: List[int],
    normal_indices: List[int],
    train_global_indices: List[int],
    cache_dir: Path,
    transform_type: str = "SyNRA",
    reference_per_sacral: int = 1,
    raw_dir: Optional[Path] = None,
) -> List[Dict]:
    """
    Phase 1: Preprocess each sacralization training case + reference normals,
    register them in 256³ unit space, and cache the deformation fields.

    Called ONCE at training startup. Returns a list of field dicts that
    SacralizationSynthTransform uses on-the-fly.

    Parameters
    ----------
    reference_per_sacral : how many normal cases to pair with each sacral case.
    transform_type : "SyNRA" (recommended), "SyN", or "Affine" (fastest).
    raw_dir : used to locate lstv_scan_cache.json.

    Returns
    -------
    List of dicts: {fwdtransforms, sacral_img_np, sacral_lbl_np, pair_name}
    """
    if not _check_ants():
        return []

    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    train_set = set(train_global_indices)

    # ── Identify sacralization training cases ──────────────────────────────
    stem_to_type = {}
    cache_path   = (Path(raw_dir) / "lstv_scan_cache.json"
                    if raw_dir else cache_dir.parent.parent / "lstv_scan_cache.json")
    if cache_path.exists():
        try:
            with open(cache_path) as f:
                cached = json.load(f)
            stem_to_type = cached.get("stem_to_type", {})
            log.info("  Using LSTV scan cache (%d entries) from %s",
                     len(stem_to_type), cache_path)
        except Exception as e:
            log.warning("  Could not load LSTV cache: %s — will scan NIfTIs.", e)

    import nibabel as nib
    sacral_cases = []
    for i in lstv_indices:
        if i not in train_set:
            continue
        d = data_list[i]
        if d.get("dataset") != "spine":
            continue
        stem = Path(d["label"]).stem
        if stem_to_type:
            if stem_to_type.get(stem) == "sacralization":
                sacral_cases.append(i)
            continue
        try:
            arr    = nib.load(d["label"]).get_fdata(dtype=np.float32).ravel()
            unique = set(arr.astype(int).tolist())
            if 24 not in unique and bool(unique - {0}):
                sacral_cases.append(i)
        except Exception:
            continue

    log.info("Sacralization field pool: %d sacral cases found.", len(sacral_cases))
    if not sacral_cases:
        return []

    # ── Pick reference normal cases ─────────────────────────────────────────
    # Prefer matched cases (those with a pelvic_mask) as registration references.
    # A matched reference has complete sacrum + hip labels, so the deformed
    # label in every synthetic case will have a full sacrum (class 7) including
    # the inferior sacral body — not just the fused L5 fragment.
    # Falls back to unmatched normals if no matched cases are in the training split.
    normal_train = [i for i in normal_indices
                    if i in train_set and data_list[i].get("dataset") == "spine"]
    matched_normal_train   = [i for i in normal_train
                              if data_list[i].get("pelvic_mask")]
    unmatched_normal_train = [i for i in normal_train
                              if not data_list[i].get("pelvic_mask")]

    ref_pool = matched_normal_train if matched_normal_train else unmatched_normal_train
    log.info(
        "Reference pool: %d matched (pelvic mask) + %d unmatched normals — "
        "using %s (%d available).",
        len(matched_normal_train), len(unmatched_normal_train),
        "matched" if matched_normal_train else "unmatched (fallback)",
        len(ref_pool),
    )

    rng = random.Random(42)

    field_pool = []
    for sacral_idx in sacral_cases:
        sacral_data = data_list[sacral_idx]
        sacral_stem = Path(sacral_data["image"]).stem

        # Preprocess the sacralization case once (or load from npy cache)
        sacral_cache_img = cache_dir / f"{sacral_stem}_img.npy"
        sacral_cache_lbl = cache_dir / f"{sacral_stem}_lbl.npy"
        if sacral_cache_img.exists() and sacral_cache_lbl.exists():
            sacral_img_np = np.load(str(sacral_cache_img))
            sacral_lbl_np = np.load(str(sacral_cache_lbl))
        else:
            try:
                sacral_img_np, sacral_lbl_np = _preprocess_nifti(
                    sacral_data["image"], sacral_data["label"])
                np.save(str(sacral_cache_img), sacral_img_np)
                np.save(str(sacral_cache_lbl), sacral_lbl_np)
            except Exception as e:
                log.error("  Could not preprocess sacral case %s: %s",
                          sacral_stem, e)
                continue

        refs = rng.sample(ref_pool,
                          min(reference_per_sacral, len(ref_pool)))

        for ref_idx in refs:
            ref_data = data_list[ref_idx]
            ref_stem = Path(ref_data["image"]).stem
            pair_name = f"{sacral_stem}_TO_{ref_stem}"

            # Preprocess the reference normal case
            ref_cache_img = cache_dir / f"{ref_stem}_img.npy"
            if ref_cache_img.exists():
                ref_img_np = np.load(str(ref_cache_img))
            else:
                try:
                    ref_img_np, _ = _preprocess_nifti(
                        ref_data["image"], ref_data["label"])
                    np.save(str(ref_cache_img), ref_img_np)
                except Exception as e:
                    log.error("  Could not preprocess reference %s: %s",
                              ref_stem, e)
                    continue

            result = _register_preprocessed_pair(
                sacral_img_np=sacral_img_np,
                ref_img_np=ref_img_np,
                cache_dir=cache_dir,
                pair_name=pair_name,
                transform_type=transform_type,
            )
            if result:
                field_pool.append({
                    "fwdtransforms":    result["fwdtransforms"],
                    "sacral_img_np":    sacral_img_np,   # label-crop space (for training)
                    "sacral_lbl_np":    sacral_lbl_np,   # label-crop space (for training)
                    "pair_name":        pair_name,
                    # Store source paths so QC can re-preprocess all panels
                    # with a consistent image-based crop for 3D visualization.
                    "sacral_image_path": sacral_data["image"],
                    "sacral_label_path": sacral_data["label"],
                    "ref_image_path":    ref_data["image"],
                    "ref_label_path":    ref_data["label"],
                    "ref_pelvic_mask":   ref_data.get("pelvic_mask"),
                })

    log.info(
        "Field pool ready: %d deformation fields from %d sacralization cases.",
        len(field_pool), len(sacral_cases),
    )
    return field_pool


class SacralizationSynthTransform:
    """
    On-the-fly sacralization synthesis using pre-computed deformation fields.

    At each call (on a preprocessed normal training tensor):
      1. Pick a random field from the pool (computed in same 256³ unit space)
      2. Apply the forward transform (normal → sacralization morphology)
      3. Post-process label: fuse L5 into sacrum

    Because both the incoming tensor and the deformation field live in the
    same 256³ 1mm isotropic unit coordinate space, the warp lands correctly.

    Parameters
    ----------
    field_pool  : output of build_sacralization_field_pool()
    apply_prob  : probability of applying per normal training sample (0.25)
    """

    def __init__(self, field_pool: List[Dict], apply_prob: float = 0.25,
                 matched_stems: Optional[set] = None):
        self.pool          = field_pool
        self.apply_prob    = apply_prob
        self.matched_stems = matched_stems   # if set, only augment matched cases
        self._has_ants     = _check_ants()
        self.last_field    = None   # set after each _apply_field call; used by QC

        if not self._has_ants or not self.pool:
            log.warning(
                "SacralizationSynthTransform: %s — using DeleteL5 fallback.",
                "no ANTs" if not self._has_ants else "empty pool",
            )
        if self.matched_stems is not None:
            log.info(
                "SacralizationSynthTransform: matched-only mode enabled "
                "(has_pelvic_mask flag) — apply_prob=%.2f. "
                "Unmatched normals will be skipped at call time.",
                self.apply_prob,
            )

    def __call__(self, data: dict) -> dict:
        # If restricted to matched cases, check the has_pelvic_mask flag that
        # _PerSampleTransform sets on every sample before calling us.
        # This is unambiguous — no stem extraction from MONAI tensors needed.
        # Unmatched normals (has_pelvic_mask=False) have no sacrum/hip labels,
        # so synthetic sacralization would produce an incomplete class-7 mask
        # (fused L5 fragment only, missing the full sacral body).
        if self.matched_stems is not None:
            if not data.get("has_pelvic_mask", False):
                return data

        if random.random() > self.apply_prob:
            return data
        if not self._has_ants or not self.pool:
            return self._delete_l5_fallback(data)
        return self._apply_field(data)

    def _apply_field(self, data: dict) -> dict:
        """
        Apply a random pre-computed deformation field to this preprocessed scan.

        Both the incoming tensor and the stored field are in 256³ unit space
        (1mm isotropic, zero origin, identity direction), so no coordinate
        conversion is needed — just wrap in ANTs and apply.
        """
        import ants

        field           = random.choice(self.pool)
        self.last_field  = field   # expose for QC logging
        img_t: torch.Tensor = data["image"]   # (1, D, H, W)
        lbl_t: torch.Tensor = data["label"]   # (1, D, H, W)

        try:
            img_np = img_t.squeeze(0).numpy()
            lbl_np = lbl_t.squeeze(0).numpy().astype(np.float32)

            # Both moving and fixed are in unit space — no coordinate tricks needed
            moving_img = _tensor_to_ants(img_np)
            moving_lbl = _tensor_to_ants(lbl_np)

            # Fixed: use the preprocessed sacralization image as anatomical target
            fixed_img  = _tensor_to_ants(field["sacral_img_np"])

            # Forward transform: warp normal → sacralization appearance
            warped_img = ants.apply_transforms(
                fixed=fixed_img, moving=moving_img,
                transformlist=field["fwdtransforms"],
                interpolator="linear",
            )
            warped_lbl = ants.apply_transforms(
                fixed=fixed_img, moving=moving_lbl,
                transformlist=field["fwdtransforms"],
                interpolator="nearestNeighbor",
            )

            # Post-process: fuse L5 into sacrum
            lbl_fused = _fuse_l5_to_sacrum(
                warped_lbl.numpy().astype(np.int32))

            data["image"] = torch.from_numpy(
                warped_img.numpy()).float().unsqueeze(0)
            data["label"] = torch.from_numpy(
                lbl_fused).long().unsqueeze(0)

        except Exception as e:
            log.debug("SacralizationSynthTransform field application failed "
                      "(%s): %s — using DeleteL5 fallback.",
                      field.get("pair_name", "?"), e)
            return self._delete_l5_fallback(data)

        return data

    def _delete_l5_fallback(self, data: dict) -> dict:
        """Simple fallback: zero L5 voxels in label only."""
        lbl    = data["label"]
        l5_vox = int((lbl == L5_UNIFIED).sum().item())
        if l5_vox >= MIN_VOXELS:
            lbl           = lbl.clone()
            lbl[lbl == L5_UNIFIED] = 0
            data["label"] = lbl
        return data


# =============================================================================
# CLI — standalone pre-computation of registration fields
# =============================================================================
# Called by slurm/run_sacral_registration.sh before training:
#   python -m src.augmentation.sacralization_synthesis \
#       --raw_dir data/ --splits data/splits.json \
#       --output_dir checkpoints/sacral_registration_cache \
#       --transform SyNRA --n_per_real 1
#
# After this completes, sbatch slurm/train.sh will find the cached fields
# and skip registration entirely at training startup.
# =============================================================================

def _parse():
    import argparse
    p = argparse.ArgumentParser(
        description="Pre-compute sacralization deformation fields in preprocessed "
                    "space. Run once before training; fields are cached to disk.")
    p.add_argument("--raw_dir",    required=True,
                   help="Root data dir containing ctspine1k/ and ctpelvic1k/")
    p.add_argument("--splits",     required=True,
                   help="Path to splits.json")
    p.add_argument("--output_dir", required=True,
                   help="Cache dir for deformation fields "
                        "(e.g. checkpoints/sacral_registration_cache)")
    p.add_argument("--transform",  default="SyNRA",
                   choices=["SyNRA", "SyN", "Affine"],
                   help="ANTs transform type. SyNRA=recommended, Affine=fastest.")
    p.add_argument("--n_per_real", type=int, default=1,
                   help="Reference normals per sacralization case.")
    return p.parse_args()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    args     = _parse()
    raw_dir  = Path(args.raw_dir)
    out_dir  = Path(args.output_dir)

    from src.data.pipeline import scan_both_datasets, identify_lstv_cases, load_splits_from_json

    log.info("=== Sacralization Registration (standalone) ===")
    log.info("  raw_dir    : %s", raw_dir)
    log.info("  output_dir : %s", out_dir)
    log.info("  transform  : %s", args.transform)
    log.info("  n_per_real : %d", args.n_per_real)

    data_list = scan_both_datasets(raw_dir / "ctspine1k", raw_dir / "ctpelvic1k")
    lstv_indices, normal_indices = identify_lstv_cases(
        data_list, cache_path=raw_dir / "lstv_scan_cache.json")

    splits      = load_splits_from_json(data_list, args.splits)
    train_stems = {Path(d["image"]).stem for d in splits["train"]}
    train_global = [i for i, d in enumerate(data_list)
                    if Path(d["image"]).stem in train_stems]

    field_pool = build_sacralization_field_pool(
        data_list=data_list,
        lstv_indices=lstv_indices,
        normal_indices=normal_indices,
        train_global_indices=train_global,
        cache_dir=out_dir,
        transform_type=args.transform,
        reference_per_sacral=args.n_per_real,
        raw_dir=raw_dir,
    )

    log.info("=== Done: %d fields cached to %s ===", len(field_pool), out_dir)
