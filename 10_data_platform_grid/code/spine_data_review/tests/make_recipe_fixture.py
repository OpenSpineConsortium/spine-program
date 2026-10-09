#!/usr/bin/env python3
"""Write tests/fixtures/recipe/: twenty-one minimal charting records covering every route and host
family sdr.recipe branches on, a quality.json in the SHAPE sdr.quality writes (scalar `total`,
boolean `fit_level_id` under `per_dataset`), a second quality.json in the `{value: ...}` shape the
recipe docstring describes, and one enrichment record. Deterministic; rerun to regenerate.

The records carry only the fields the recipe reads; they are NOT schema-valid charting records
and must never be copied into charting/datasets/.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FX = HERE / "fixtures" / "recipe"


def rec(id_, route, rule, url, **kw):
    base = {"schema_version": "1.0", "id": id_, "name": f"Fixture {id_}", "modality": ["CT"], "region": ["lumbar"],
            "n_subjects": 50, "size_gb": None, "checksums": [], "licence": {"text": "CC BY 4.0", "tier": "open"},
            "on_grid": {"status": "no", "path": None, "checked_date": None, "n_subjects_on_grid": None},
            "access_probe": [{"date": "2026-09-19", "http_status": 200}, {"date": "2026-09-21", "http_status": 200}],
            "file_url_probed": None, "versioning": {"dataset_doi": None}, "source_record": {"doi": None},
            "access_route": route, "access_route_rule": rule, "host_type": "repository-api", "access_url": url}
    base.update(kw)
    return base


RECORDS = [
    # open-download, files known from checksums[] (sha256 + md5 + size) -> method files
    rec("fx-files", "open-download", "P15", "https://example.org/data/index.html",
        host_type="institutional",
        checksums=[{"file": "vol_001.nii.gz", "from": "published-readme", "url": "https://example.org/data/vol_001.nii.gz",
                    "size_bytes": 1234, "sha256": "a" * 64},
                   {"file": "vol_002.nii.gz", "from": "published-readme", "url": "https://example.org/data/vol_002.nii.gz",
                    "md5": "b" * 32}]),
    # open-download on Zenodo by DOI only (no record id in the URL) -> zenodo-api
    rec("fx-zenodo", "open-download", "P1", "https://doi.org/10.5281/zenodo.10079370",
        versioning={"dataset_doi": "10.5281/zenodo.10079370"}),
    rec("fx-figshare", "open-download", "P13", "https://figshare.com/articles/dataset/x/12345678"),
    rec("fx-dryad", "open-download", "P13", "https://datadryad.org/stash/dataset/doi:10.5061/dryad.abc123"),
    rec("fx-osf", "open-download", "P13", "https://osf.io/ab1cd/"),
    rec("fx-physionet-open", "open-download", "P7", "https://physionet.org/content/ptb-xl/1.0.3/",
        modality=["radiograph"]),
    rec("fx-tcia", "open-download", "P10", "https://www.cancerimagingarchive.net/collection/no-such-collection-xyz/"),
    rec("fx-hf-open", "open-download", "P4", "https://huggingface.co/datasets/owner/spine-ct"),
    rec("fx-github", "open-download", "P14", "https://github.com/owner/spine-repo"),
    # open-download elsewhere with a file_url_probed -> files (one URL)
    rec("fx-generic-fileurl", "open-download", "P20", "https://example.org/spine/",
        host_type="institutional", file_url_probed="https://example.org/spine/all.zip"),
    # open-download elsewhere, nothing recorded -> browser (manual, exit 10)
    rec("fx-generic-browser", "open-download", "P20", "https://example.org/other/", host_type="institutional"),
    # open-download on Mendeley Data (protocol host table row; mendeley-api lists files at run time)
    rec("fx-mendeley", "open-download", "P13", "https://data.mendeley.com/datasets/5jdfdgp762/1",
        versioning={"dataset_doi": "10.17632/5jdfdgp762.1"}),
    # the same dataset with NO version anywhere: the landing URL is /datasets/<id> and no dataset DOI is
    # charted, so the script must resolve the latest available version before it can list the files
    # (live 2026-09-19: /versions answers [{"version":1,...,"available":true}], and the same files URL
    # without a version answers HTTP 200 with the body {"error":400})
    rec("fx-mendeley-nover", "open-download", "P13", "https://data.mendeley.com/datasets/5jdfdgp762"),
    rec("fx-kaggle", "registration", "P12", "https://www.kaggle.com/datasets/owner/spine-xr",
        host_type="challenge-platform", licence={"text": "CC BY-NC-SA 4.0", "tier": "non-commercial"}),
    rec("fx-hf-gated", "registration", "P5", "https://huggingface.co/datasets/owner/gated-spine"),
    rec("fx-gc", "registration", "P12", "https://spine-challenge.grand-challenge.org/", host_type="challenge-platform"),
    rec("fx-dua", "data-use-agreement", "P8", "https://physionet.org/content/vindr-spinexr/1.0.0/",
        licence={"text": "PhysioNet Credentialed Health Data License 1.5.0", "tier": "restricted"}),
    rec("fx-request", "request-to-authors", "P24", None, host_type="unknown",
        access_probe=[{"date": "2026-09-19", "method": "none"}], source_record={"doi": "10.1000/example.1"}),
    rec("fx-commercial", "commercial", "P17", "https://vendor.example.com/spine", host_type="unknown"),
    rec("fx-unavailable", "unavailable", "P23", "https://gone.example.org/spine", host_type="institutional",
        access_probe=[{"date": "2026-09-19", "http_status": 404}, {"date": "2026-09-21", "http_status": 404}]),
    # reachable, fit, but already on the grid -> tier 1 not tier 0
    rec("fx-on-grid", "open-download", "P1", "https://zenodo.org/records/1234567",
        on_grid={"status": "yes", "path": "~/data/x", "checked_date": "2026-09-19", "n_subjects_on_grid": 50}),
]

# Quality in the shape sdr.quality writes: scalar total, boolean fit_level_id.
QUALITY_REAL = {"per_dataset": {
    "fx-files": {"total": 14, "fit_level_id": True},
    "fx-zenodo": {"total": 17, "fit_level_id": True},
    "fx-figshare": {"total": 9, "fit_level_id": False},
    "fx-dryad": {"total": 9, "fit_level_id": False},
    "fx-osf": {"total": 8, "fit_level_id": False},
    "fx-physionet-open": {"total": 12, "fit_level_id": True},
    "fx-tcia": {"total": 11, "fit_level_id": False},
    "fx-hf-open": {"total": 6, "fit_level_id": False},
    "fx-github": {"total": 5, "fit_level_id": False},
    "fx-generic-fileurl": {"total": 7, "fit_level_id": False},
    "fx-generic-browser": {"total": 4, "fit_level_id": False},
    "fx-mendeley": {"total": 10, "fit_level_id": False},
    "fx-mendeley-nover": {"total": 15, "fit_level_id": False},
    "fx-kaggle": {"total": 14, "fit_level_id": True},
    "fx-hf-gated": {"total": 3, "fit_level_id": False},
    "fx-gc": {"total": 13, "fit_level_id": False},
    "fx-dua": {"total": 16, "fit_level_id": True},
    "fx-request": {"total": 2, "fit_level_id": False},
    "fx-commercial": {"total": 1, "fit_level_id": False},
    "fx-unavailable": {"total": 0, "fit_level_id": False},
    "fx-on-grid": {"total": 18, "fit_level_id": True},
}, "summary": {}, "run_date": "2026-09-19"}


def main() -> None:
    d = FX / "datasets"
    d.mkdir(parents=True, exist_ok=True)
    for r in RECORDS:
        (d / f"{r['id']}.json").write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    (FX / "quality_real_shape.json").write_text(json.dumps(QUALITY_REAL, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    wrapped = {"per_dataset": {k: {"total": {"value": v["total"]}, "fit_level_id": {"value": v["fit_level_id"]}}
                               for k, v in QUALITY_REAL["per_dataset"].items()}}
    (FX / "quality_value_shape.json").write_text(json.dumps(wrapped, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    e = FX / "enrichment"
    e.mkdir(exist_ok=True)
    # enrichment adds a third file to fx-files and repeats one URL (must be de-duplicated by URL)
    (e / "fx-files.json").write_text(json.dumps({"files": [
        {"name": "vol_003.nii.gz", "url": "https://example.org/data/vol_003.nii.gz", "size_bytes": 99},
        {"name": "vol_001.nii.gz", "url": "https://example.org/data/vol_001.nii.gz", "size_bytes": 1234}]}, indent=2) + "\n",
        encoding="utf-8", newline="\n")
    print(f"wrote {len(RECORDS)} records, two quality files and one enrichment record under {FX}")


if __name__ == "__main__":
    main()
