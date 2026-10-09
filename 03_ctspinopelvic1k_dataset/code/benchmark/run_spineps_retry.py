#!/usr/bin/env python3
# source-of-copy: spinesurg-ct-nnunet repository (private), branch L6_Class, path benchmark/run_spineps_retry.py; committed at 097933a
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
"""SPINEPS over a shard of a case table, with further attempts for the cases the first one crashes on —
and the mask always returned on the CT's OWN grid.

WHY A SECOND RUNNER. `benchmark/run_spineps_cases.py` is the benchmark runner and is being used right now by
the CTSpinoPelvic1K job, so it is not edited. This one is a superset: same command, same harvest, same output
names, same resume rule, plus the ladder below and a per-case record of which attempt produced the mask.

THE FAILURES IT IS FOR. Of the 1,602 TotalSegmentator + VerSe cases, 118 came back without an instance mask.
Read out of the runner's own timing log, the exceptions fall into five classes; three of them are crashes
inside SPINEPS/TPTBox rather than statements about the anatomy:

    22 x  AssertionError: assert_affine failed with ['shape mismatch (129, 555, 77), (129, 555, 76)']
          spineps/phase_labeling.py:184 run_model_for_vert_labeling -> img.assert_affine(other=vert)
    21 x  ValueError: Statistics can only be computed on volumes containing labels with values lower than the
          number of voxels. Max: 8              cc3d/fastcc3d.pyx, reached from TPTBox np_volume
    15 x  ValueError: bbox_nd: img is empty, cannot calculate a bbox
          TPTBox nii_wrapper.py:867 compute_crop, called with VIBE_CROP_MARGIN_MM

THE FIRST EXPLANATION WAS WRONG, AND IT WAS TESTED BEFORE IT WAS BELIEVED. It looked as though all three
classes came from one place -- the body segmentation SPINEPS runs before the semantic model, whose crop is
what `compute_crop`/`VIBE_CROP_MARGIN_MM` is doing -- and that `--no-crop` would therefore clear all three.
It does not. `--no-crop` sets `proc_sem_crop_input`, which is a different crop: TSV3_s0122 raised the
identical `bbox_nd: img is empty` traceback with the flag and without it. And the shape mismatch is not in a
crop at all; it is in the VERIDAH labelling phase, comparing the image against the instance mask.

What does work on the shape mismatch is the isotropic resample: TSV3_s0001 and TSV3_s0208 both failed native
and `--no-crop` and both came back on the 1.5 mm grid. So the ladder keeps all four rungs and records which
one produced each mask, and the per-class answer is read off the result rather than argued for here.

Rungs 1 and 2 touch no voxel of the released CT. Rungs 3 and 4 resample it onto an axis-aligned 1.5 mm grid
and resample the instance and semantic masks BACK onto the original grid by nearest neighbour, keeping the
CT's own shape and affine. `resample_from_to` maps through the affines, so the mask stays on the CT it came
from, which is what `tools/body_masks.py` and `make_drr_dataset --body-mask-dir` both require (they refuse a
mask whose shape is not the label's).

Every attempt is recorded per case, so a mask from a resampled grid is never mistaken for a native one, and a
case that fails all four is written into <out>/<case>_failed.json with all four exceptions — what is still
absent is on disk, not only in a log.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_spineps_cases import harvest  # noqa: E402  same harvest rule, one definition

# cheapest and most faithful first: (name, resample the CT to an isotropic grid?, extra flags)
LADDER = [("native", False, ""),
          ("native_nocrop", False, "--no-crop"),
          ("iso", True, ""),
          ("iso_nocrop", True, "--no-crop")]


def iso_grid(img, mm: float = 1.5):
    """An axis-aligned grid at `mm` isotropic covering the volume: (shape, affine).

    The rotation is dropped deliberately -- one of the crashes this exists for is a rounding disagreement
    produced by cropping and uncropping an oblique stack -- and nothing is lost, because the masks are mapped
    back through the affines onto the original grid before anything downstream sees them.
    """
    import numpy as np

    A = img.affine
    s = img.shape[:3]
    corners = np.array([[i * (s[0] - 1), j * (s[1] - 1), k * (s[2] - 1), 1]
                        for i in (0, 1) for j in (0, 1) for k in (0, 1)], float)
    world = (A @ corners.T).T[:, :3]
    lo, hi = world.min(0), world.max(0)
    shape = tuple(int(np.ceil((hi[d] - lo[d]) / mm)) + 1 for d in range(3))
    aff = np.eye(4)
    aff[0, 0] = aff[1, 1] = aff[2, 2] = mm
    aff[:3, 3] = lo
    return shape, aff


def resample_ct_to_iso(src_ct: str, dst_ct: str, mm: float = 1.5) -> dict:
    import nibabel as nib
    from nibabel.processing import resample_from_to

    img = nib.load(src_ct)
    shape, aff = iso_grid(img, mm)
    out = resample_from_to(img, (shape, aff), order=1, cval=-1024.0)
    out.set_data_dtype("int16")
    nib.save(out, dst_ct)
    return {"orig_shape": [int(x) for x in img.shape[:3]],
            "orig_zooms": [round(float(z), 4) for z in img.header.get_zooms()[:3]],
            "iso_shape": [int(x) for x in shape], "iso_mm": mm}


def masks_back_to_native(files: dict, ref_ct: str) -> dict:
    """Put each harvested label mask back on the reference CT's grid, in place, by nearest neighbour."""
    import nibabel as nib
    import numpy as np
    from nibabel.processing import resample_from_to

    ref = nib.load(ref_ct)
    moved = {}
    for key, p in files.items():
        p = str(p)
        if not p.endswith(".nii.gz"):
            # the centroid json SPINEPS wrote is in the isotropic grid's voxel coordinates, not the CT's;
            # it is renamed rather than left under the name a native run would have written
            if p.endswith("_ctd.json") and os.path.exists(p):
                q = p.replace("_ctd.json", "_ctd_isogrid.json")
                os.replace(p, q)
                moved[key] = {"renamed": os.path.basename(q),
                              "why": "centroids are in the isotropic grid, not the CT's"}
            continue
        m = nib.load(p)
        back = resample_from_to(m, (ref.shape[:3], ref.affine), order=0, cval=0)
        arr = np.asanyarray(back.dataobj).round().astype(np.int16)
        # a fresh image on the CT's own affine; no as_closest_canonical, nothing transposed
        nib.save(nib.Nifti1Image(arr, ref.affine), p)
        moved[key] = {"shape": [int(x) for x in arr.shape],
                      "n_labels": int((np.unique(arr) > 0).sum())}
    return moved


def run_spineps(ct: str, models: dict, timeout: int, extra: str = ""):
    cmd = ["spineps", "sample", "-i", ct,
           "--model-semantic", models["semantic"], "--model-instance", models["instance"],
           "--model-labeling", models["labeling"], "--ignore-inference-compatibility", "--no-n4"]
    if extra:
        cmd += extra.split()
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", required=True, type=Path)
    ap.add_argument("--out_dir", required=True, type=Path)
    ap.add_argument("--work", required=True, type=Path)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--n_shards", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--model_semantic", default="ct")
    ap.add_argument("--model_instance", default="CT_instance")
    ap.add_argument("--model_labeling", default="ct_labeling")
    ap.add_argument("--extra", default="")
    ap.add_argument("--timeout", type=int, default=5400)
    ap.add_argument("--iso-mm", type=float, default=1.5)
    ap.add_argument("--attempts", type=int, default=len(LADDER),
                    help="how far down the ladder to go; 1 makes this the base runner")
    ap.add_argument("--rungs", default="",
                    help="comma-separated rung names to use instead of the ladder prefix, e.g. 'iso'. Only for "
                         "the controlled comparison of one rung against another on the same CT.")
    a = ap.parse_args()

    models = {"semantic": a.model_semantic, "instance": a.model_instance, "labeling": a.model_labeling}
    a.out_dir.mkdir(parents=True, exist_ok=True)
    a.work.mkdir(parents=True, exist_ok=True)
    with open(a.cases) as fh:
        rows = [r for i, r in enumerate(csv.DictReader(fh)) if i % a.n_shards == a.shard]
    if a.limit:
        rows = rows[: a.limit]
    print(f"shard {a.shard}/{a.n_shards}: {len(rows)} cases", flush=True)
    log = open(a.out_dir / f"retry_timing_shard{a.shard}.jsonl", "a")
    if a.rungs:
        want = [x.strip() for x in a.rungs.split(",") if x.strip()]
        by_name = {r[0]: r for r in LADDER}
        missing = [w for w in want if w not in by_name]
        if missing:
            raise SystemExit(f"unknown rung(s) {missing}; known: {sorted(by_name)}")
        ladder = [by_name[w] for w in want]
    else:
        ladder = LADDER[: max(1, a.attempts)]
    print(f"rungs: {[r[0] for r in ladder]}", flush=True)
    n_skip = n_fail = 0
    attempts: dict = {}

    for r in rows:
        case, src = r["case"], r["ct"]
        if (a.out_dir / f"{case}_seg-vert_msk.nii.gz").exists():
            n_skip += 1
            continue
        if not os.path.exists(src):
            rec = {"case": case, "ok": False, "attempt": "none", "error": f"CT missing: {src}"}
            log.write(json.dumps(rec) + os.linesep)
            log.flush()
            n_fail += 1
            continue

        t0 = time.time()
        errs: dict = {}
        done: dict | None = None

        for name, iso, extra in ladder:
            stage = a.work / f"{case}__{name}"
            shutil.rmtree(stage, ignore_errors=True)
            stage.mkdir(parents=True)
            staged = stage / f"{case}_ct.nii.gz"
            geo = None
            try:
                if iso:
                    geo = resample_ct_to_iso(src, str(staged), a.iso_mm)
                else:
                    os.symlink(src, staged)
                proc = run_spineps(str(staged), models, a.timeout, (a.extra + " " + extra).strip())
                if proc.returncode != 0:
                    raise RuntimeError(f"spineps exited {proc.returncode}: {proc.stderr[-700:]}")
                got = harvest(stage, case, a.out_dir)
                if "vert" not in got:
                    raise RuntimeError("no seg-vert mask produced; stage tree: " +
                                       ", ".join(q.name for q in stage.rglob("*") if q.is_file())[:400])
                done = {"case": case, "ok": True, "attempt": name,
                        "seconds": round(time.time() - t0, 1), "files": got,
                        "earlier_failures": errs}
                if iso:
                    done["geometry"] = geo
                    done["back_on_native_grid"] = masks_back_to_native(got, src)
                    done["note"] = ("run on a 1.5 mm axis-aligned resample because the released grid crashed "
                                    "SPINEPS; the masks were resampled back onto the CT's own shape and "
                                    "affine, nearest neighbour, nothing reoriented")
                if name != "native":
                    json.dump(done, open(a.out_dir / f"{case}_retry.json", "w"), indent=1)
            except Exception as e:  # noqa: BLE001
                errs[name] = repr(e)[:900]
            finally:
                shutil.rmtree(stage, ignore_errors=True)
            if done is not None:
                break

        if done is not None:
            attempts[done["attempt"]] = attempts.get(done["attempt"], 0) + 1
            log.write(json.dumps(done) + os.linesep)
            log.flush()
            print({k: done[k] for k in ("case", "ok", "attempt", "seconds")}, flush=True)
        else:
            n_fail += 1
            rec = {"case": case, "ok": False, "attempt": "all", "seconds": round(time.time() - t0, 1),
                   "errors": errs}
            json.dump(rec, open(a.out_dir / f"{case}_failed.json", "w"), indent=1)
            log.write(json.dumps(rec) + os.linesep)
            log.flush()
            print(f"{case}: FAILED every attempt {sorted(errs)}", flush=True)

    made = ", ".join(f"{k} {v}" for k, v in sorted(attempts.items())) or "none"
    print(f"SPINEPS_RETRY_SHARD{a.shard}: produced by attempt [{made}]; skipped {n_skip}, failed {n_fail}",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
