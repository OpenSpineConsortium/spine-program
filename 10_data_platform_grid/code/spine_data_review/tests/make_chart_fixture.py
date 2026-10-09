"""Build the charting fixture for sdr.chart (review of the 'screen' module).

One record that should validate cleanly (a VerSe-like chart with every required field and a quote
for every x-requires-quote field), and a set of single-defect variants each expected to fail on
one named rule. The expected error substrings are typed here by hand; tests/check_chart_report.py
compares them with charting validation_report.json.

Usage: ~/sdr_venv/bin/python tests/make_chart_fixture.py   (writes tests/fixtures/chart_screen/<id>.json
       and tests/expected_chart_errors.json)
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "fixtures" / "chart_screen"
VERSE_DOI = "10.1016/j.media.2021.102166"
VERSE_TITLE = "VerSe: A Vertebrae labelling and segmentation benchmark for multi-detector CT images"


def probe(date: str, rule: str = "P13", cls: str = "open-download", method: str = "API") -> dict:
    return {"url": "https://osf.io/nqjyw", "final_url": "https://osf.io/nqjyw", "method": method, "http_status": 200,
            "status_chain": [200], "content_type": "application/json", "content_length": None, "content_disposition": None,
            "www_authenticate": None, "date": date, "attempts": 1, "classification_machine": cls, "rule": rule,
            "evidence": "public: true; files listed", "raw_sha1": "a" * 40, "error": None}


def variant(status: str, n: int | None, assessed: int | None) -> dict:
    known = status == "yes"
    return {"status": status, "how_labelled": "explicit-label" if known else "unknown", "n_subjects_with": n,
            "n_subjects_assessed": assessed, "unit": "subject" if known else "unknown",
            "definition": "class id in the label scheme" if known else "", "definition_class": "count-based" if known else "not-defined",
            "ascertainment": "count-from-c2" if known else "unknown", "selection": "consecutive-or-unselected" if known else "unknown"}


def quote(field: str, text: str) -> dict:
    return {"field": field, "text": text, "source": VERSE_DOI, "locator": "Methods"}


QUOTED = ["n_subjects", "annotation_origin", "annotation_validation.qa_process", "variant_labels.L6", "variant_labels.T13",
          "licence.text", "per_vertebra_level_names", "described_as_public", "documentation.states_population",
          "documentation.states_acquisition", "documentation.states_annotation_protocol",
          "documentation.states_file_layout_and_label_scheme", "documentation.description_at_least_100_words",
          "metadata_elements.age-sex", "metadata_elements.scanner-or-acquisition-parameters", "split_defined",
          "patient_level_dedup", "image_quality_reported"]


def valid_record(rid_lit: str) -> dict:
    return {
        "schema_version": "1.0", "id": "verse", "name": "VerSe", "aliases": ["VerSe'19", "VerSe'20"],
        "versions": [{"label": "VerSe 2019", "year": 2019}, {"label": "VerSe 2020", "year": 2020}], "charted_version": "VerSe 2020",
        "modality": ["CT"], "projection": ["NA"], "region": ["cervical", "thoracic", "lumbar", "mixed"],
        "n_subjects": 355, "n_subjects_basis": "reported", "n_images_or_volumes": 374, "n_images_unit": "volumes",
        "pediatric_included": "no",
        "annotation_types": ["per-vertebra-level-names", "segmentation-3d", "centroids"],
        "annotation_origin": ["expert-manual", "expert-corrected-model"],
        "annotation_origin_by_type": {"per-vertebra-level-names": ["expert-manual"], "segmentation-3d": ["expert-corrected-model"],
                                      "centroids": ["expert-manual"]},
        "annotator_qualification_stated": True,
        "annotation_validation": {"described": True, "qa_process": "double-read", "inter_rater_statistic": "dice", "inter_rater_value": 0.95,
                                  "inter_rater_ci": None, "inter_rater_sd": 0.03, "inter_rater_n": 20, "fraction_of_items": 0.05,
                                  "per_structure_breakdown": True, "n_raters": 2, "comparator": "rater-vs-rater", "n_categories": None,
                                  "comparable_group": None},
        "variant_labels": {"L6": variant("yes", 12, 355), "T13": variant("yes", 6, 355), "LSTV": variant("unknown", None, None)},
        "per_vertebra_level_names": "yes",
        "documentation": {"article_or_preprint": True, "repository_record_or_readme": True, "description_at_least_100_words": True,
                          "states_population": True, "states_acquisition": True, "states_annotation_protocol": True,
                          "states_file_layout_and_label_scheme": True},
        "metadata_elements": ["age-sex", "scanner-or-acquisition-parameters"],
        "licence": {"text": "CC BY-SA 4.0", "tier": "open", "url": "https://creativecommons.org/licenses/by-sa/4.0/", "spdx": "CC-BY-SA-4.0",
                    "standard": True, "stated_in": "both", "consistent": "yes"},
        "described_as_public": "yes", "described_as_public_regex": True,
        "access_url": "https://osf.io/nqjyw", "access_url_basis": "given-in-record", "host_type": "repository-api", "file_url_probed": None,
        "access_probe": [probe("2026-09-10"), probe("2026-09-13")], "access_route": "open-download", "access_route_rule": "P13",
        "subject_overlap": [], "year": 2021, "year_basis": "article", "cohort_year_range": None, "country": ["DE"],
        "source_record": {"doi": VERSE_DOI, "pmid": "34340104", "pmcid": None, "arxiv": None, "url": "https://osf.io/nqjyw",
                          "title": VERSE_TITLE, "record_type": "journal-article", "record_ids": [rid_lit]},
        "size_gb": 12.5, "format": ["NIfTI"],
        "versioning": {"dataset_doi": None, "doi_resolves_to": "none", "version_identifier": "2020", "changelog_or_versioned_records": False},
        "superset_of_version": None, "split_defined": "yes", "patient_level_dedup": "yes", "grouping_variable_released": True,
        "image_quality_reported": "no", "resolution_summary": None,
        "flags": {"figure_derived": False, "derived": False, "parent_ids": [], "multi_modal": False, "challenge": True,
                  "authors_own": False, "maintainer_authors": [], "superseded": False},
        "checksums": [], "on_grid": {"status": "yes", "path": "~/VerSeFusion/data/unified", "checked_date": "2026-09-19", "n_subjects_on_grid": 355},
        "field_sources": {"described_as_public_regex": "api:code"}, "notes": "",
        "quotes": [quote(f, f"Verbatim sentence supporting {f} in the fixture.") for f in QUOTED],
        "charted_by": "GS", "charted_date": "2026-09-15", "verified_by": "AB", "verified_date": "2026-09-18",
        "eligibility": {"decision": "included", "criteria_met": ["I1", "I2", "I3", "I4", "I5", "I6"], "found_via": ["search", "known-item"]},
    }


def variants(base: dict) -> dict[str, tuple[dict, list[str]]]:
    """id -> (record, expected error substrings). Empty list = expected valid."""
    out: dict[str, tuple[dict, list[str]]] = {"verse": (base, [])}

    def mk(name: str, expect: list[str], edit):
        r = copy.deepcopy(base)
        r["id"] = name
        edit(r)
        out[name] = (r, expect)

    mk("bad-licence-spdx", ["rule licence"], lambda r: r["licence"].update({"spdx": "CC-BY-4.0"}))
    mk("bad-route-rule", ["rule access_route_rule"], lambda r: r.update({"access_route_rule": "P15"}))
    mk("bad-missing-quote", ["quote: 'n_subjects'"], lambda r: r.update({"quotes": [q for q in r["quotes"] if q["field"] != "n_subjects"]}))
    mk("bad-comparable-group", ["rule comparable_group"], lambda r: r["annotation_validation"].update({"comparable_group": "dice-vertebra-3d"}))
    mk("bad-id-mismatch", ["differs from file name"], lambda r: r.update({"id": "verse"}))
    mk("bad-probe-gap", ["rule probes"], lambda r: r.update({"access_probe": [probe("2026-09-10"), probe("2026-09-11")]}))
    mk("bad-derived-flag", ["parent_ids", "I8"], lambda r: r["flags"].update({"derived": True}))
    mk("bad-extra-key", ["unexpected key 'extra'"], lambda r: r.update({"extra": 1}))
    mk("bad-figure-basis", ["rule figure_derived"], lambda r: (r["flags"].update({"figure_derived": True}),
                                                                r["eligibility"]["criteria_met"].append("I7")))
    mk("bad-origin-by-type", ["rule origin_by_type"], lambda r: r["annotation_origin_by_type"].pop("centroids"))
    mk("bad-host-type", ["rule host_type"], lambda r: r.update({"host_type": "institutional"}))
    mk("bad-authors-own", ["rule authors_own"], lambda r: r["flags"].update({"authors_own": True, "maintainer_authors": ["AB"]}))
    mk("bad-year", ["maximum 2026"], lambda r: r.update({"year": 2031}))
    # Not a defect by the schema, a probe of the validator: 'CC BY 3.0' text -> what spdx does the table force?
    mk("probe-ccby3", [], lambda r: r["licence"].update({"text": "CC BY 3.0", "spdx": "CC-BY-3.0", "tier": "open", "standard": True}))
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.json"):
        old.unlink()
    # The lit: id of the pubmed VerSe record in the screen fixture, so the merged.jsonl check has a hit.
    recs = HERE / "fixtures" / "screen_run" / "records" / "pubmed.jsonl"
    rid = "lit:000000000000"
    if recs.exists():
        rid = next(json.loads(l)["record_id"] for l in recs.read_text(encoding="utf-8").splitlines() if "34340104" in l)
    expected = {}
    for name, (rec, errs) in variants(valid_record(rid)).items():
        (OUT / f"{name}.json").write_text(json.dumps(rec, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
        expected[name] = errs
    (HERE / "expected_chart_errors.json").write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {len(expected)} charting fixtures to {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
