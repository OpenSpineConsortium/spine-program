#!/usr/bin/env python3
# source-of-copy: spinesurg-ct-nnunet repository (private), branch L6_Class, path benchmark/run_spineps_patched.py; untracked on 2026-10-08 (not in 097933a)
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
"""benchmark/run_spineps_retry.py with the `spineps` command swapped for benchmark/spineps_cc3d_patched.py.

Same case table, same ladder and rungs, same harvest, same output names, same resume rule, same *_failed.json
record; the only difference is the executable, which removes the one TPTBox/cc3d crash documented there
("Statistics can only be computed on volumes containing labels with values lower than the number of voxels").
Each produced case also gets a <case>_cc3dpatch.json saying the mask came from the patched command, so a mask
from this runner is never mistaken for one from the stock SPINEPS.

    python benchmark/run_spineps_patched.py --selftest
    python benchmark/run_spineps_patched.py --cases <csv> --out_dir <dir> --work <dir> [run_spineps_retry args]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_spineps_retry as R  # noqa: E402

PATCHED = str(HERE / "spineps_cc3d_patched.py")


def run_spineps(ct: str, models: dict, timeout: int, extra: str = ""):
    cmd = [sys.executable, PATCHED, "sample", "-i", ct,
           "--model-semantic", models["semantic"], "--model-instance", models["instance"],
           "--model-labeling", models["labeling"], "--ignore-inference-compatibility", "--no-n4"]
    if extra:
        cmd += extra.split()
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def selftest() -> int:
    """the patched cc3d call must return what np.bincount says, on the array shape that crashes the stock one"""
    import numpy as np
    sys.path.insert(0, str(HERE))
    import spineps_cc3d_patched as P
    import TPTBox.core.np_utils as nu
    arr = np.zeros((2, 3, 1), np.uint16)
    arr[0, 1, 0] = 22
    arr[1, 2, 0] = 7
    stock_raises = False
    try:
        nu._cc3dstats(arr)
    except ValueError as e:
        stock_raises = "lower than the number of voxels" in str(e)
    P._install()

    def plain(d):
        return {int(k): int(v) for k, v in d.items()}
    got = plain(nu.np_volume(arr))
    want = {int(i): int(c) for i, c in enumerate(np.bincount(arr.ravel())) if c > 0 and i != 0}
    got0 = plain(nu.np_volume(arr, include_zero=True))
    want0 = {int(i): int(c) for i, c in enumerate(np.bincount(arr.ravel())) if c > 0}
    big = np.zeros((30, 30, 30), np.uint16)
    big[3:6, 4:9, 2:3] = 5
    big[10:12, 1:2, 7:9] = 22
    ok_big = plain(nu.np_volume(big)) == {5: 15, 22: 4}
    ok = (got == want) and (got0 == want0) and ok_big
    print(json.dumps({"stock_cc3d_raises_on_tiny_array": stock_raises, "patched": got, "bincount": want,
                      "patched_with_zero": got0, "bincount_with_zero": want0, "large_array_unchanged": ok_big,
                      "fired": P._FIRED[0], "ok": ok}), flush=True)
    return 0 if ok else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    R.run_spineps = run_spineps
    out_dir = None
    if "--out_dir" in sys.argv:
        out_dir = Path(sys.argv[sys.argv.index("--out_dir") + 1])
    before = set(os.listdir(out_dir)) if out_dir and out_dir.is_dir() else set()
    rc = R.main()
    if out_dir and out_dir.is_dir():
        for f in sorted(set(os.listdir(out_dir)) - before):
            if f.endswith("_seg-vert_msk.nii.gz"):
                case = f[: -len("_seg-vert_msk.nii.gz")]
                json.dump({"case": case, "command": "benchmark/spineps_cc3d_patched.py",
                           "why": "stock SPINEPS crashed in TPTBox cc3dstatistics on a tiny array; the patched "
                                  "command pads that array with zeros past its last index and re-counts"},
                          open(out_dir / f"{case}_cc3dpatch.json", "w"), indent=1)
    return rc


if __name__ == "__main__":
    sys.exit(main())
