# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/ctsp0533_verify.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Verify a rebuilt CTSpinoPelvic1K CT against its released label, from OUTSIDE the rebuild.

Written for record 0533, whose released CT is a truncated gzip (17,301,504 B) on the grid and
on HuggingFace alike. A rebuild that "looks fine" is exactly the failure mode this project
keeps hitting, so nothing here is checked against the rebuild's own bookkeeping:

  * gzip integrity              -- the defect being repaired, tested directly
  * shape and affine            -- taken from labels/0533_label.nii.gz, not from the manifest
  * orientation                 -- axis codes reported, never rewritten (labels are PIR here)
  * dtype and file size         -- compared to the neighbouring released CTs, so the repaired
                                   file is the same KIND of object as the other 801
  * bone fraction under the mask -- compared to manifest.spine_bone_pct, which was computed by
                                   the release from the file this one replaces. This is the
                                   check that catches the wrong CT series: every patient in
                                   this cohort was scanned twice.

`spine_bone_pct` is the fraction under the VERTEBRA identifiers, not under every label. That was
not documented and was established by measuring it on ten records whose released CT is not in
question (job 40416604, `tools/ctsp0533_bone_check.py`): over all labels they sit two to four
points off their own recorded value, over the vertebrae they reproduce it to about a fifth of a
point. Comparing the all-label fraction to it reads a correct volume as a wrong one, which is
what the first run of this verifier did.

Exit 0 only if every gate passes. The caller swaps the file in on exit 0 and on nothing else.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import nibabel as nib

BONE_HU = 200.0
# C1..L6 and T13 -- the identifiers `spine_bone_pct` is computed over (established on controls)
VERTEBRA_IDS = list(range(1, 26)) + [28]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def gzip_ok(path: Path) -> tuple[bool, str]:
    r = subprocess.run(["gzip", "-t", str(path)], capture_output=True, text=True)
    if r.returncode == 0:
        return True, "gzip -t clean"
    return False, (r.stderr.strip() or r.stdout.strip())[:200]


def gzip_bytes(path: Path) -> int:
    """Decompressed length, read the long way (ISIZE is only the low 32 bits)."""
    n = 0
    with gzip.open(path, "rb") as fh:
        while True:
            b = fh.read(1 << 22)
            if not b:
                break
            n += len(b)
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ct", required=True, help="the rebuilt CT to judge")
    ap.add_argument("--label", required=True, help="released *_label.nii.gz")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--case", default="0533")
    ap.add_argument("--neighbours", nargs="*", default=[],
                    help="released CTs of other records, for dtype/size comparison")
    ap.add_argument("--old-ct", default=None, help="the file this one would replace")
    ap.add_argument("--min-bone", type=float, default=0.5)
    ap.add_argument("--bone-tol", type=float, default=1.0,
                    help="allowed points of difference from manifest spine_bone_pct, measured over "
                         "the vertebra identifiers. Ten control records reproduce their own recorded "
                         "value to between +0.20 and +0.25 points, so 1.0 is loose.")
    ap.add_argument("--out", required=True, help="where to write the JSON report")
    a = ap.parse_args()

    ct_p, lab_p = Path(a.ct), Path(a.label)
    rep: dict = {"case": a.case, "ct": str(ct_p), "label": str(lab_p), "gates": {}}
    gates = rep["gates"]

    def gate(name, ok, detail):
        gates[name] = {"pass": bool(ok), "detail": detail}
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)

    if not ct_p.exists():
        print(f"  no rebuilt CT at {ct_p}")
        return 2

    rep["size_bytes"] = ct_p.stat().st_size
    rep["sha256_new"] = sha256(ct_p)
    if a.old_ct and Path(a.old_ct).exists():
        op = Path(a.old_ct)
        rep["old_size_bytes"] = op.stat().st_size
        rep["sha256_old"] = sha256(op)
        ok_old, why_old = gzip_ok(op)
        rep["old_gzip_ok"] = ok_old
        print(f"  the file being replaced: {rep['old_size_bytes']} B, sha256 "
              f"{rep['sha256_old']}, gzip -t -> {'clean' if ok_old else why_old}")

    ok, why = gzip_ok(ct_p)
    gate("gzip_integrity", ok, why)
    if ok:
        try:
            rep["decompressed_bytes"] = gzip_bytes(ct_p)
        except Exception as e:                                          # noqa: BLE001
            gate("gzip_integrity", False, f"{type(e).__name__}: {e}")

    ref = nib.load(str(lab_p))
    try:
        img = nib.load(str(ct_p))
        data = np.asanyarray(img.dataobj)
    except Exception as e:                                              # noqa: BLE001
        gate("loads", False, f"{type(e).__name__}: {e}")
        Path(a.out).write_text(json.dumps(rep, indent=1), encoding="utf-8")
        return 1
    gate("loads", True, f"shape {tuple(img.shape)} dtype {data.dtype}")

    rep["shape"] = list(map(int, img.shape[:3]))
    rep["label_shape"] = list(map(int, ref.shape[:3]))
    gate("shape_matches_label", tuple(img.shape[:3]) == tuple(ref.shape[:3]),
         f"CT {tuple(img.shape[:3])} vs label {tuple(ref.shape[:3])}")

    rep["axcodes"] = "".join(nib.aff2axcodes(img.affine))
    rep["label_axcodes"] = "".join(nib.aff2axcodes(ref.affine))
    gate("orientation_matches_label", rep["axcodes"] == rep["label_axcodes"],
         f"CT {rep['axcodes']} vs label {rep['label_axcodes']} (never reoriented on write)")

    dmax = float(np.abs(np.asarray(img.affine) - np.asarray(ref.affine)).max())
    rep["affine"] = np.asarray(img.affine).tolist()
    rep["affine_max_abs_diff"] = dmax
    gate("affine_matches_label", dmax <= 1e-4, f"max |delta| = {dmax:.3e}")

    # bone fraction under the mask -- the wrong-series detector
    lab = np.asanyarray(ref.dataobj)
    m = (lab > 0) & (lab != 255)
    rep["label_fg_voxels"] = int(m.sum())
    if m.any() and tuple(img.shape[:3]) == tuple(ref.shape[:3]):
        frac = float((np.asarray(data, dtype=np.float32)[m] >= BONE_HU).mean())
    else:
        frac = float("nan")
    rep["bone_fraction"] = frac
    gate("bone_fraction_min", frac == frac and frac >= a.min_bone,
         f"{frac * 100:.1f}% of labelled voxels >= {BONE_HU:.0f} HU (floor {a.min_bone * 100:.0f}%)")

    # the same quantity restricted to the vertebrae, which is what the release recorded
    mv = np.isin(lab, VERTEBRA_IDS)
    rep["vertebra_voxels"] = int(mv.sum())
    if mv.any() and tuple(img.shape[:3]) == tuple(ref.shape[:3]):
        vfrac = float((np.asarray(data, dtype=np.float32)[mv] >= BONE_HU).mean())
    else:
        vfrac = float("nan")
    rep["bone_fraction_vertebrae"] = vfrac

    recs = json.loads(Path(a.manifest).read_text(encoding="utf-8"))
    recs = recs if isinstance(recs, list) else recs.get("records", list(recs.values()))
    mrec = next((r for r in recs if str(r.get("volume_id")) == a.case), None)
    rep["manifest"] = {k: mrec.get(k) for k in
                       ("volume_id", "token", "config", "match_type", "position",
                        "spine_series_uid", "spine_bone_pct", "n_voxels_fg")} if mrec else None
    if mrec is not None:
        want = mrec.get("spine_bone_pct")
        if want is not None and vfrac == vfrac:
            d = abs(vfrac * 100 - float(want))
            gate("bone_fraction_matches_release", d <= a.bone_tol,
                 f"{vfrac * 100:.2f}% of vertebra voxels rebuilt vs {float(want):.1f}% recorded in "
                 f"the release (delta {d:.2f} pts, tolerance {a.bone_tol}); over ALL labels it is "
                 f"{frac * 100:.2f}%, which is NOT what that field means")
        # advisory, not a gate: manifest.n_voxels_fg is a broken column (0 in 340 of 802 records)
        # and describes neither label version on disk for this record
        nfg = mrec.get("n_voxels_fg")
        if nfg:
            rep["label_fg_vs_manifest"] = {"label_on_disk": rep["label_fg_voxels"],
                                           "manifest": int(nfg),
                                           "agree": int(nfg) == rep["label_fg_voxels"]}
            print(f"  [note] manifest n_voxels_fg {int(nfg)} vs {rep['label_fg_voxels']} in the "
                  f"label on disk -- advisory: that column is 0 in 340 of 802 records")

    # the other 801 released CTs: same dtype, plausible size
    sizes, dtypes = [], []
    for n in a.neighbours:
        p = Path(n)
        if not p.exists():
            continue
        try:
            sizes.append(p.stat().st_size)
            dtypes.append(str(nib.load(str(p)).get_data_dtype()))
        except Exception:                                               # noqa: BLE001
            continue
    rep["neighbour_sizes"] = sizes
    rep["neighbour_dtypes"] = dtypes
    if dtypes:
        gate("dtype_matches_neighbours", str(img.get_data_dtype()) in set(dtypes),
             f"{img.get_data_dtype()} vs neighbours {sorted(set(dtypes))}")
    if sizes:
        lo, hi = min(sizes) * 0.25, max(sizes) * 4.0
        gate("size_plausible", lo <= rep["size_bytes"] <= hi,
             f"{rep['size_bytes'] / 1e6:.1f} MB vs neighbours "
             f"{min(sizes) / 1e6:.0f}-{max(sizes) / 1e6:.0f} MB")

    rep["all_pass"] = all(g["pass"] for g in gates.values())
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(rep, indent=1), encoding="utf-8")
    print(f"VERIFY_0533 all_pass={rep['all_pass']} gates={len(gates)} "
          f"failed={[k for k, g in gates.items() if not g['pass']]}", flush=True)
    return 0 if rep["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
