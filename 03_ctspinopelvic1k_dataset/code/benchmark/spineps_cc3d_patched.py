#!/usr/bin/env python3
# source-of-copy: spinesurg-ct-nnunet repository (private), branch L6_Class, path benchmark/spineps_cc3d_patched.py; untracked on 2026-10-08 (not in 097933a)
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
"""The `spineps` command with one TPTBox crash removed -- the same CLI, the same models, the same arguments.

THE CRASH. 53 of the TotalSegmentator v3 CTs that SPINEPS returned no vertebra mask for, and 23 of the 24 that
still failed the fifth (cropped) attempt, die in TPTBox with

    cc3d/fastcc3d.pyx statistics: ValueError: Statistics can only be computed on volumes containing labels with
    values lower than the number of voxels. Max: 22
    <- TPTBox/core/np_utils.py cc3dstatistics <- np_volume

cc3d refuses to count the voxels of a label map that has fewer voxels than its largest label value. TPTBox reaches
it with a tiny array (its own bounding-box crop of one object, and then the same small array again in the
fallback), so the refusal is about the array's size, not about the anatomy or the segmentation.

THE PATCH. `TPTBox.core.np_utils._cc3dstats` is wrapped: on exactly that ValueError the array is padded with zeros
AFTER its last index along axis 0 until it has more voxels than its largest label, cc3d is called on the padded
array, and the zeros added are subtracted from the background count. Padding at the far end moves no existing
voxel, so every label's voxel count, bounding box and centroid is the one cc3d would have returned if it had
agreed to count; only label 0's box and centroid can differ, and nothing in the count path reads them. Any other
exception is re-raised unchanged. The number of times the patch fired is printed on stderr as CC3D_PATCH_FIRED.

ONLY WITH --cpu, a second guard: SPINEPS's own `--cpu` flag dies in TPTBox before the first prediction
(`nnUnet_utils/predictor.py get_gpu_util` calls torch.cuda.mem_get_info on the cpu device: "Expected a cuda device,
but got: cpu"). That function only decides whether to WAIT for a busy GPU (predictor.py line 622); on the cpu device
it now reports 0.0 (idle) and get_gpu_memory_MB reports no limit. No prediction path changes. Without --cpu nothing
here is touched.

    python benchmark/spineps_cc3d_patched.py sample -i <ct> --model-semantic ... (exactly the `spineps` arguments)
"""
from __future__ import annotations

import sys

import numpy as np

_FIRED = [0]


def _install() -> None:
    import TPTBox.core.np_utils as nu

    orig = nu._cc3dstats

    def cc3dstats_padded(arr, *args, **kwargs):
        try:
            return orig(arr, *args, **kwargs)
        except ValueError as e:
            if "lower than the number of voxels" not in str(e) or arr.ndim < 1 or arr.size == 0:
                raise
            mx = int(arr.max())
            per_slab = int(np.prod(arr.shape[1:])) if arr.ndim > 1 else 1
            if per_slab == 0:
                raise
            need = mx + 2 - arr.size
            n_pad = max(1, -(-need // per_slab))
            pad = [(0, n_pad)] + [(0, 0)] * (arr.ndim - 1)
            padded = np.pad(np.ascontiguousarray(arr), pad, mode="constant", constant_values=0)
            out = orig(padded, *args, **kwargs)
            added = padded.size - arr.size
            vc = out.get("voxel_counts") if isinstance(out, dict) else None
            if vc is not None and len(vc) > 0:
                vc = np.array(vc, copy=True)
                vc[0] = max(0, int(vc[0]) - added)
                out["voxel_counts"] = vc
            _FIRED[0] += 1
            return out

    nu._cc3dstats = cc3dstats_padded


def _install_cpu_guard() -> None:
    import torch
    import TPTBox.segmentation.nnUnet_utils.predictor as pr

    util0, mem0 = pr.get_gpu_util, pr.get_gpu_memory_MB

    def is_cpu(device):
        return str(getattr(device, "type", device)).startswith("cpu") or not torch.cuda.is_available()

    def get_gpu_util(device):
        return 0.0 if is_cpu(device) else util0(device)

    def get_gpu_memory_MB(device):
        return float("inf") if is_cpu(device) else mem0(device)

    pr.get_gpu_util = get_gpu_util
    pr.get_gpu_memory_MB = get_gpu_memory_MB


def main() -> int:
    _install()
    if "--cpu" in sys.argv:
        _install_cpu_guard()
    from spineps.entrypoint import entry_point

    sys.argv[0] = "spineps"
    try:
        rc = entry_point()
    finally:
        print(f"CC3D_PATCH_FIRED {_FIRED[0]}", file=sys.stderr, flush=True)
    return int(rc or 0)


if __name__ == "__main__":
    sys.exit(main())
