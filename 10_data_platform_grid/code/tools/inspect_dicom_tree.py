#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/inspect_dicom_tree.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""What a directory of DICOM cases actually holds: modality, device, geometry, intensity form, per case.

Built for C-ArmLSpine (Zenodo 22768651: 149 intraoperative spine cases, each with two C-arm frames and a CBCT from
one FIRST Surgio-B51), but general. For every case folder: the 2-D frames' size, pixel spacing, bit depth, the
Pixel Intensity Relationship (LIN or LOG) and its sign, photometric interpretation, kVp and exposure, positioner
angles, source-to-detector and source-to-patient distances, detector type, any frame-of-reference UID shared with
the 3-D volume, and every private or geometry tag present; for the volume: size, spacing, orientation, HU range.
Whether the frames can be tied to the volume -- a shared frame of reference, a registration object, or stored
geometry -- decides whether vertebra labels can be projected onto real intraoperative frames.

    python tools/inspect_dicom_tree.py --root /rs/rs_grp_oschome/go2432/data/carmlspine --cases 5 --out carm_inspect.json
"""
from __future__ import annotations

import argparse
import glob
import json
import os
from collections import Counter

TAGS2D = ["Modality", "Manufacturer", "ManufacturerModelName", "Rows", "Columns", "PixelSpacing", "ImagerPixelSpacing",
          "BitsStored", "PhotometricInterpretation", "PixelIntensityRelationship", "PixelIntensityRelationshipSign",
          "KVP", "XRayTubeCurrent", "ExposureTime", "Exposure", "DistanceSourceToDetector", "DistanceSourceToPatient",
          "PositionerPrimaryAngle", "PositionerSecondaryAngle", "DetectorType", "FieldOfViewShape", "FieldOfViewDimensions",
          "ImageType", "FrameOfReferenceUID", "StudyInstanceUID", "SeriesDescription", "ViewPosition", "BodyPartExamined",
          "WindowCenter", "WindowWidth", "RescaleSlope", "RescaleIntercept", "EstimatedRadiographicMagnificationFactor",
          "PatientSex", "PatientAge"]
TAGS3D = ["Modality", "Manufacturer", "ManufacturerModelName", "Rows", "Columns", "PixelSpacing", "SliceThickness",
          "ImageOrientationPatient", "FrameOfReferenceUID", "StudyInstanceUID", "RescaleSlope", "RescaleIntercept", "KVP",
          "SeriesDescription", "BodyPartExamined"]


def val(ds, k):
    v = getattr(ds, k, None)
    if v is None:
        return None
    try:
        if hasattr(v, "__iter__") and not isinstance(v, (str, bytes)):
            return [str(x) for x in v]
        return str(v)
    except Exception:  # noqa: BLE001
        return repr(v)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True); ap.add_argument("--cases", type=int, default=5)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    import numpy as np
    import pydicom
    cases = sorted({os.path.dirname(os.path.dirname(p)) for p in glob.glob(os.path.join(a.root, "**", "C-arm", "*.dcm"), recursive=True)})
    print(f"{len(cases)} case folders with a C-arm/ subfolder under {a.root}")
    report = dict(n_cases=len(cases), cases=[])
    fam = Counter()
    for c in cases[: a.cases]:
        rec = dict(case=os.path.basename(c), frames=[], volume=None)
        for p in sorted(glob.glob(os.path.join(c, "C-arm", "*.dcm"))):
            ds = pydicom.dcmread(p)
            f = {k: val(ds, k) for k in TAGS2D}
            arr = ds.pixel_array.astype(np.float64)
            f["pixel_min_p1_p50_p99_max"] = [float(x) for x in np.percentile(arr, (0, 1, 50, 99, 100))]
            f["private_or_geometry_tags"] = [f"{el.tag} {el.keyword or el.name}" for el in ds if el.tag.is_private or "Geometry" in (el.name or "") or "Positioner" in (el.name or "")][:60]
            rec["frames"].append(dict(file=os.path.basename(p), **f))
            fam[(f["Manufacturer"], f["ManufacturerModelName"], f["PixelIntensityRelationship"], f["PhotometricInterpretation"])] += 1
        vols = sorted(glob.glob(os.path.join(c, "CBCT", "*")))
        if vols:
            ds = pydicom.dcmread(vols[0])
            v = {k: val(ds, k) for k in TAGS3D}
            v["n_slices"] = len(vols)
            v["first_slice_hu_p1_p99"] = [float(x) for x in np.percentile(ds.pixel_array * float(getattr(ds, "RescaleSlope", 1)) + float(getattr(ds, "RescaleIntercept", 0)), (1, 99))]
            rec["volume"] = v
        fr = {x["FrameOfReferenceUID"] for x in rec["frames"]}
        # a MISSING uid on both sides is not a shared frame of reference (C-ArmLSpine: None == None read as "shared")
        vfr = rec["volume"]["FrameOfReferenceUID"] if rec["volume"] else None
        rec["frames_share_volume_frame_of_reference"] = bool(vfr not in (None, "", "None") and vfr in fr)
        report["cases"].append(rec)
        print(f"\n== {rec['case']}: {len(rec['frames'])} frames, volume {rec['volume']['n_slices'] if rec['volume'] else 0} slices; shared frame of reference: {rec['frames_share_volume_frame_of_reference']}")
        for fr_ in rec["frames"]:
            keys = ["Modality", "Manufacturer", "ManufacturerModelName", "Rows", "Columns", "PixelSpacing", "ImagerPixelSpacing", "BitsStored",
                    "PhotometricInterpretation", "PixelIntensityRelationship", "PixelIntensityRelationshipSign", "KVP", "XRayTubeCurrent",
                    "ExposureTime", "DistanceSourceToDetector", "DistanceSourceToPatient", "PositionerPrimaryAngle", "PositionerSecondaryAngle",
                    "DetectorType", "ViewPosition", "ImageType"]
            print("  frame", fr_["file"], {k: fr_[k] for k in keys if fr_.get(k) is not None})
            print("    pixels min/p1/p50/p99/max", [round(x, 1) for x in fr_["pixel_min_p1_p50_p99_max"]], "| private/geometry tags:", len(fr_["private_or_geometry_tags"]))
        if rec["volume"]:
            print("  volume", {k: rec["volume"][k] for k in ("Modality", "Manufacturer", "ManufacturerModelName", "Rows", "Columns", "PixelSpacing", "SliceThickness", "ImageOrientationPatient", "n_slices", "first_slice_hu_p1_p99")})
    report["families"] = [dict(key=list(k), n=n) for k, n in fam.items()]
    json.dump(report, open(a.out, "w"), indent=1)
    print("\nframe families (manufacturer, model, intensity relationship, photometric):", dict(fam))
    print("wrote", a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
