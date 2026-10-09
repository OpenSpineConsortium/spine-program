#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/export_vindr_identity.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Re-export the VinDr-SpineXR image -> study map from the release's own annotation csvs.

The release (PhysioNet vindr-spinexr 1.0.0) carries no PatientID in any DICOM header; the only
identity unit it publishes is study_id in annotations/{train,test}.csv (study_id, series_id, image_id
per row, one row per lesion box or "No finding"). tools/patient_keys.py needs this map to key VinDr by
study rather than by image (open item C13: the per-image key leaks 77.8 % of vindrps validation).

Writes {image_id: {"study_id", "series_id", "split"}} and prints the counts that must match the release:
10,466 images, 5,000 studies (8,389 train / 2,077 test images). Exits non-zero if they do not.
"""
import argparse, csv, json, sys
from collections import Counter, defaultdict
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=str(Path.home() / "spine-detector/data/raw/vindr/1.0.0"))
    ap.add_argument("--out", required=True, nargs="+", help="one or more json paths to write")
    a = ap.parse_args()
    raw = Path(a.raw)
    m, rows = {}, Counter()
    conflicts = 0
    for split in ("train", "test"):
        with open(raw / "annotations" / f"{split}.csv", newline="") as fh:
            for r in csv.DictReader(fh):
                rows[split] += 1
                rec = {"study_id": r["study_id"], "series_id": r["series_id"], "split": split}
                prev = m.get(r["image_id"])
                if prev is not None and prev != rec:
                    conflicts += 1
                m[r["image_id"]] = rec
    studies = defaultdict(set)
    for iid, rec in m.items():
        studies[rec["study_id"]].add(iid)
    per_split = Counter(rec["split"] for rec in m.values())
    on_disk = {p.stem for d in ("train_images", "test_images") for p in (raw / d).glob("*.dicom")}
    imgs_per_study = Counter(len(v) for v in studies.values())
    summary = {
        "csv_rows": dict(rows),
        "images": len(m), "images_per_split": dict(per_split),
        "studies": len(studies), "images_per_study_hist": dict(sorted(imgs_per_study.items())),
        "image_to_study_conflicts": conflicts,
        "dicoms_on_disk": len(on_disk),
        "csv_images_without_dicom": sorted(set(m) - on_disk)[:20],
        "n_csv_images_without_dicom": len(set(m) - on_disk),
        "dicoms_without_csv_row": sorted(on_disk - set(m))[:20],
        "n_dicoms_without_csv_row": len(on_disk - set(m)),
        "studies_split_across_train_test": sum(1 for v in studies.values() if len({m[i]["split"] for i in v}) > 1),
    }
    print(json.dumps(summary, indent=1))
    for o in a.out:
        Path(o).parent.mkdir(parents=True, exist_ok=True)
        json.dump({"_summary": summary, "images": m}, open(o, "w"), indent=0, sort_keys=True)
        print("wrote", o)
    ok = (len(m) == 10466 and len(studies) == 5000 and conflicts == 0
          and summary["n_csv_images_without_dicom"] == 0 and summary["n_dicoms_without_csv_row"] == 0)
    print("VINDR_IDENTITY_OK" if ok else "VINDR_IDENTITY_MISMATCH")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
