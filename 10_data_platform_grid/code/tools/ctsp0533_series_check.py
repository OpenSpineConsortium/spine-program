# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/ctsp0533_series_check.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Does the downloaded series match what the manifest says this record was acquired with?

The bone-fraction gate tests the CT against the LABEL. This tests the DICOM against the
MANIFEST, which is a separate source: the release records the scanner, the model, the
reconstruction kernel, the slice thickness, the kVp, the sex and the age of every record. A
series that agrees on all of them is the one the crosswalk names; a redirected or substituted
download would have to match seven independent fields by accident.

It prints only those fields. No patient identifier is read out of the file or written anywhere.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pydicom

FIELDS = [
    ("manufacturer", "Manufacturer", lambda v: str(v).strip().upper()),
    ("manufacturer_model", "ManufacturerModelName", lambda v: str(v).strip()),
    ("convolution_kernel", "ConvolutionKernel", lambda v: str(v).strip()),
    ("slice_thickness", "SliceThickness", lambda v: round(float(v), 3)),
    ("kvp", "KVP", lambda v: round(float(v), 1)),
    ("sex", "PatientSex", lambda v: {"M": "male", "F": "female"}.get(str(v).strip().upper(), str(v))),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dicom-dir", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--case", default="0533")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    files = sorted(Path(a.dicom_dir).rglob("*.dcm"))
    if not files:
        print("  no DICOM found")
        return 2
    d = pydicom.dcmread(str(files[len(files) // 2]), stop_before_pixels=True)

    recs = json.loads(Path(a.manifest).read_text(encoding="utf-8"))
    recs = recs if isinstance(recs, list) else recs.get("records", list(recs.values()))
    rec = next((r for r in recs if str(r.get("volume_id")) == a.case), None)
    if rec is None:
        print(f"  {a.case} is not in the manifest")
        return 2

    out = {"case": a.case, "n_dicom": len(files), "checks": {}}
    ok = True
    for key, tag, norm in FIELDS:
        want = rec.get(key)
        raw = getattr(d, tag, None)
        got = None
        if raw is not None:
            try:
                got = norm(raw)
            except Exception:                                           # noqa: BLE001
                got = str(raw)
        want_n = None
        if want is not None:
            try:
                want_n = norm(want)
            except Exception:                                           # noqa: BLE001
                want_n = want
        agree = (want_n is None) or (got is not None and str(got).upper() == str(want_n).upper())
        ok = ok and agree
        out["checks"][key] = {"manifest": want, "dicom": got, "agree": bool(agree)}
        print(f"  [{'ok ' if agree else 'NO '}] {key}: manifest {want!r} vs series {got!r}")

    # age is banded in the report so the row stays coarse
    age = getattr(d, "PatientAge", None)
    if age is not None and rec.get("age") is not None:
        try:
            years = int(str(age).rstrip("Yy").lstrip("0") or 0)
        except ValueError:
            years = None
        agree = years is not None and abs(years - int(rec["age"])) <= 1
        ok = ok and agree
        out["checks"]["age"] = {"manifest_band": rec.get("age_band"), "agree": bool(agree)}
        print(f"  [{'ok ' if agree else 'NO '}] age: manifest band {rec.get('age_band')}, series agrees={agree}")

    out["series_uid_matches_manifest"] = (
        str(getattr(d, "SeriesInstanceUID", "")) == str(rec.get("spine_series_uid")))
    print(f"  [{'ok ' if out['series_uid_matches_manifest'] else 'NO '}] the series identifier in the "
          f"files is the one the manifest names for this record")
    ok = ok and out["series_uid_matches_manifest"]
    out["all_agree"] = bool(ok)

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"SERIES_CHECK_0533 all_agree={ok} fields={len(out['checks'])}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
