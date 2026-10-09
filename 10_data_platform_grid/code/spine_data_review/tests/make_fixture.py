"""Write the tiny fixture the stats-module review runs quality -> stats -> figures on.

Everything here is chosen by hand so that every number the three modules produce can be
recomputed on paper (tests/test_stats_module.py holds the hand calculations). Twelve charting
records under tests/fixtures/stats/charting/, their probe histories under tests/fixtures/stats/probes/,
the reviewer CSVs under tests/fixtures/stats/screening/, charting/dataset_sources.csv beside the records, and
the run-dir inputs of the flow (queries.json, records/*.jsonl, merged.jsonl, prisma_counts.json,
screening_sheet.csv) under runs/review_stats/. Nothing is downloaded and no credential is read.

The design, so the hand calculations are readable:
  ds01  CT lumbar, open-download, n=100, LSTV 12/100 unselected, L6 3/100        rubric 16
  ds02  CT whole-spine, open-download, n=200, LSTV 30/200 ENRICHED               rubric 19
  ds03  radiograph lumbar, registration, n=150, LSTV 0/150 (zero cell)            rubric 14
  ds04  CT thoracic+lumbar, open-download, n=80, DERIVED from ds01 (family dup)   rubric 13
  ds05  radiograph whole-spine, registration, n=60, LSTV 5/60, model-generated    rubric 16
  ds06  fluoroscopy lumbar, unavailable, n=40, FIGURE-DERIVED                     rubric 11
  ds07  CT+radiograph mixed, open-download, n=300 (CT 200 / XR 120), LSTV 45/300  rubric 14
  ds08  CT lumbar, registration, n=500, LSTV 60/500, overlaps ds01 by 50 (one-sided) rubric 15
  ds09  radiograph cervical, open-download, n=25, UNANNOTATED, LSTV 2/25          rubric 12
  ds10  CT lumbar, registration, n=15 (F4 fails), LSTV 3/15 (n<20)                rubric 15
  ds11  DXA-VFA thoracic+lumbar, open-download, n=90 ESTIMATED, variants unknown  rubric 13
  ds12  CT lumbar, registration, n=70, UNVERIFIED, LSTV 8/70                      rubric 15
Run: ~/sdr_venv/bin/python tests/make_fixture.py   (from spine_data_review/)
"""
from __future__ import annotations

import copy
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIX = ROOT / "tests" / "fixtures" / "stats"
RUN = ROOT / "runs" / "review_stats"


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_csv(path: Path, header: list[str], rows: list[list]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def variant(status="unknown", how="not-labelled", x=None, n=None, selection="unknown", ascert="unknown", defn="not-defined"):
    return {"status": status, "how_labelled": how, "n_subjects_with": x, "n_subjects_assessed": n, "unit": "subject",
            "definition": "", "definition_class": defn, "ascertainment": ascert, "selection": selection}


def probe(url, date, status=200, cls="open-download", rule="P20", method="HEAD"):
    return {"url": url, "final_url": url, "method": method, "http_status": status, "status_chain": [status], "content_type": "text/html",
            "content_length": None, "content_disposition": None, "www_authenticate": None, "date": date, "attempts": 1,
            "classification_machine": cls, "rule": rule, "evidence": None, "raw_sha1": None, "error": None}


def base(i: int, year: int, modality: list[str], region: list[str], route: str, n: int, **over) -> dict:
    did = f"ds{i:02d}"
    url = f"https://example.org/{did}"
    d = {"schema_version": "1.0", "id": did, "name": f"Dataset {i:02d}", "aliases": [], "versions": [],
         "modality": modality, "projection": ["lateral"] if set(modality) & {"radiograph", "fluoroscopy", "DXA-VFA", "EOS"} else ["NA"],
         "region": region, "n_subjects": n, "n_subjects_basis": "reported", "n_images_or_volumes": 2 * n, "n_images_unit": "volumes",
         "pediatric_included": "no",
         "annotation_types": ["segmentation-3d", "per-vertebra-level-names"],
         "annotation_origin": ["expert-manual"],
         "annotation_origin_by_type": {"segmentation-3d": ["expert-manual"], "per-vertebra-level-names": ["expert-manual"]},
         "annotator_qualification_stated": True,
         "annotation_validation": {"described": True, "qa_process": "double-read", "inter_rater_statistic": "dice", "inter_rater_value": 0.9,
                                   "inter_rater_ci": None, "inter_rater_sd": None, "inter_rater_n": 20, "fraction_of_items": 0.2,
                                   "per_structure_breakdown": True, "n_raters": 2, "comparator": "rater-vs-rater", "n_categories": None,
                                   "comparable_group": "dice-vertebra-3d"},
         "variant_labels": {"L6": variant(), "T13": variant(), "LSTV": variant()},
         "per_vertebra_level_names": "yes",
         "documentation": {k: True for k in ("article_or_preprint", "repository_record_or_readme", "description_at_least_100_words",
                                             "states_population", "states_acquisition", "states_annotation_protocol",
                                             "states_file_layout_and_label_scheme")},
         "metadata_elements": ["age-sex", "scanner-or-acquisition-parameters", "spacing-or-dicom-headers", "site-and-country"],
         "licence": {"text": "CC BY 4.0", "tier": "open", "url": None, "spdx": "CC-BY-4.0", "standard": True, "stated_in": "both", "consistent": "yes"},
         "described_as_public": "yes", "described_as_public_regex": True,
         "access_url": url, "access_url_basis": "article", "host_type": "repository-api",
         "file_url_probed": f"{url}/f.zip",
         "access_probe": [probe(url, "2026-09-10", cls=route if route != "unavailable" else "unavailable", rule="P20" if route == "open-download" else "P3"),
                          probe(url, "2026-09-13", cls=route if route != "unavailable" else "unavailable", rule="P20" if route == "open-download" else "P3")],
         "access_route": route, "access_route_rule": "P20" if route == "open-download" else "P3",
         "subject_overlap": [], "year": year, "year_basis": "article", "country": ["DE"],
         "source_record": {"doi": f"10.1000/{did}", "pmid": None, "pmcid": None, "arxiv": None, "url": None, "title": f"Dataset {i:02d} article",
                           "record_type": "journal-article", "record_ids": [f"lit:{i:012d}"]},
         "size_gb": 1.0, "format": ["NIfTI"],
         "versioning": {"dataset_doi": f"10.5281/zenodo.{i}", "doi_resolves_to": "dataset-record", "version_identifier": "v1",
                        "changelog_or_versioned_records": False},
         "split_defined": "yes", "patient_level_dedup": "yes", "grouping_variable_released": True,
         "image_quality_reported": "no", "resolution_summary": None,
         "flags": {"figure_derived": False, "derived": False, "parent_ids": [], "multi_modal": len(modality) > 1, "challenge": False,
                   "authors_own": False, "maintainer_authors": [], "superseded": False},
         "checksums": [], "on_grid": {"status": "no", "path": None, "checked_date": None, "n_subjects_on_grid": None},
         "field_sources": {}, "notes": "", "quotes": [], "charted_by": "R1", "charted_date": "2026-09-15", "verified_by": "R2",
         "verified_date": "2026-09-16", "eligibility": {"decision": "included", "criteria_met": ["I1", "I2", "I3", "I4", "I5", "I6"], "found_via": ["search"]}}
    d.update(over)
    return d


def lstv(x, n, selection="consecutive-or-unselected"):
    return variant("yes", "explicit-label", x, n, selection, "count-from-c2", "castellvi-II-IV")


def records() -> list[dict]:
    ds = []
    d = base(1, 2015, ["CT"], ["lumbar"], "open-download", 100)
    d["variant_labels"]["LSTV"] = lstv(12, 100)
    d["variant_labels"]["L6"] = variant("yes", "explicit-label", 3, 100, "consecutive-or-unselected", "count-from-c2", "count-based")
    d["on_grid"] = {"status": "yes", "path": "~/data/ds01", "checked_date": "2026-09-15", "n_subjects_on_grid": 100}
    ds.append(d)                                                                       # 16

    d = base(2, 2017, ["CT"], ["whole-spine"], "open-download", 200)
    d["variant_labels"]["LSTV"] = lstv(30, 200, "enriched")
    d["variant_labels"]["L6"] = variant("yes", "explicit-label", 20, 200, "enriched", "count-from-c2", "count-based")
    d["image_quality_reported"] = "yes-quantitative"                                    # Q10 2
    d["versioning"]["changelog_or_versioned_records"] = True                            # Q8 2
    ds.append(d)                                                                       # 19

    d = base(3, 2019, ["radiograph"], ["lumbar"], "registration", 150)
    d["variant_labels"]["LSTV"] = lstv(0, 150)
    d["licence"]["stated_in"] = "article"                                               # Q6 1
    d["file_url_probed"] = None                                                         # Q7 1 (no file evidence, rule P3)
    ds.append(d)                                                                       # 14

    d = base(4, 2020, ["CT"], ["thoracic", "lumbar"], "open-download", 80)
    d["variant_labels"]["LSTV"] = lstv(10, 80)
    d["flags"].update({"derived": True, "parent_ids": ["ds01"]})
    d["eligibility"]["criteria_met"].append("I8")
    d["documentation"]["article_or_preprint"] = False                                   # Q1 1
    d["annotation_validation"].update({"described": False, "qa_process": "none", "inter_rater_statistic": "none",
                                       "inter_rater_value": None, "inter_rater_n": None, "fraction_of_items": None,
                                       "per_structure_breakdown": False, "comparable_group": None})  # Q3 0
    ds.append(d)                                                                       # 13

    d = base(5, 2021, ["radiograph"], ["whole-spine"], "registration", 60)
    d["variant_labels"]["LSTV"] = lstv(5, 60)
    d["annotation_origin"] = ["model-generated"]
    d["annotation_origin_by_type"] = {"segmentation-3d": ["model-generated"], "per-vertebra-level-names": ["model-generated"]}  # Q2 1, F2 fails
    d["metadata_elements"] = ["age-sex", "scanner-or-acquisition-parameters", "spacing-or-dicom-headers", "site-and-country",
                              "inclusion-exclusion-criteria", "clinical-status-per-subject"]              # Q5 2
    ds.append(d)                                                                       # 16

    d = base(6, 2022, ["fluoroscopy"], ["lumbar"], "unavailable", 40)
    d["variant_labels"]["LSTV"] = variant("yes", "reported-in-text", 4, 40, "consecutive-or-unselected", "report-or-text", "castellvi-unspecified")  # Q4 1
    d["flags"]["figure_derived"] = True
    d["eligibility"]["criteria_met"].append("I7")
    d["access_probe"] = [probe(d["access_url"], "2026-09-10", 404, "unavailable", "P22"), probe(d["access_url"], "2026-09-13", 404, "unavailable", "P22")]  # Q7 0
    d["access_route_rule"] = "P22"
    d["licence"] = {"text": "not stated", "tier": "unknown", "url": None, "spdx": None, "standard": False, "stated_in": "none", "consistent": "unknown"}  # Q6 0
    d["described_as_public"] = "no"
    d["file_url_probed"] = None
    ds.append(d)                                                                       # 11

    d = base(7, 2023, ["CT", "radiograph"], ["mixed"], "open-download", 300)
    d["variant_labels"]["LSTV"] = lstv(45, 300)
    d["n_per_modality"] = {"CT": {"n_subjects": 200, "n_images_or_volumes": 200}, "radiograph": {"n_subjects": 120, "n_images_or_volumes": 400}}
    d["split_defined"], d["patient_level_dedup"], d["grouping_variable_released"] = "no", "no", False   # Q9 0
    ds.append(d)                                                                       # 14

    d = base(8, 2018, ["CT"], ["lumbar"], "registration", 500)
    d["variant_labels"]["LSTV"] = lstv(60, 500)
    d["subject_overlap"] = [{"dataset_id": "ds01", "n_shared": 50, "basis": "stated"}]  # listed on ds08 only
    d["annotation_validation"].update({"inter_rater_statistic": "kappa", "inter_rater_value": 0.8, "inter_rater_n": 10,
                                       "fraction_of_items": 0.02, "comparable_group": "kappa-level-names"})  # Q3 1 (small subset)
    ds.append(d)                                                                       # 15

    d = base(9, 2012, ["radiograph"], ["cervical"], "open-download", 25)
    d["variant_labels"]["LSTV"] = lstv(2, 25)
    d.update({"annotation_types": ["none"], "annotation_origin": ["none"], "annotation_origin_by_type": {},
              "annotator_qualification_stated": False, "per_vertebra_level_names": "no"})   # Q2 0, Q3 0, F1 fails
    d["documentation"]["states_annotation_protocol"] = False
    d["annotation_validation"].update({"described": False, "qa_process": "none", "inter_rater_statistic": "none", "inter_rater_value": None,
                                       "inter_rater_n": None, "fraction_of_items": None, "per_structure_breakdown": False, "comparable_group": None})
    ds.append(d)                                                                       # 12

    d = base(10, 2016, ["CT"], ["lumbar"], "registration", 15)
    d["variant_labels"]["LSTV"] = lstv(3, 15)
    d["metadata_elements"] = ["age-sex"]                                                # Q5 0
    ds.append(d)                                                                       # 15

    d = base(11, 2024, ["DXA-VFA"], ["thoracic", "lumbar"], "open-download", 90)
    d["n_subjects_basis"] = "estimated"
    d["versioning"] = {"dataset_doi": None, "doi_resolves_to": "none", "version_identifier": None, "changelog_or_versioned_records": False}  # Q8 0
    ds.append(d)                                                                       # 13 (Q4 0)

    d = base(12, 2009, ["CT"], ["lumbar"], "registration", 70)
    d["variant_labels"]["LSTV"] = lstv(8, 70)
    d["annotator_qualification_stated"] = False                                         # Q2 1
    d["verified_by"], d["verified_date"] = None, None
    ds.append(d)                                                                       # 15
    return ds


def probes_files(ds: list[dict]) -> None:
    """charting/probes/<id>.json as sdr/availability.py writes it: file_probes[] on the file URL, two dates."""
    for d in ds:
        fps = []
        if d["file_url_probed"]:
            fps = [probe(d["file_url_probed"], dt, 206, "open-download", "P15", "GET-range") for dt in ("2026-09-10", "2026-09-13")]
        dump(FIX / "probes" / f"{d['id']}.json", {"id": d["id"], "access_url": d["access_url"], "host_type": d["host_type"],
                                                   "file_url_probed": d["file_url_probed"], "probes": d["access_probe"], "file_probes": fps,
                                                   "agreement": {"status": "agree", "route": d["access_route"], "rule": d["access_route_rule"],
                                                                 "dates": ["2026-09-10", "2026-09-13"]}})


def screening_and_run() -> None:
    """Counts chosen so every A1 identity has a hand value: identified 15, after_merge 12, prescreen
    pass 7 / uncertain 1 / non-english 1 / fail 3, audit 2 (1 included), screened 10, TA decisions
    include 4 / unclear 2 / exclude 4 (one use-only), full text 6 -> include 4 / exclude 2 (one not
    retrieved); other arm 2 screened, 1 included; chase forward 1 / backward 1; 3 known items.
    dataset_sources.csv maps all twelve datasets onto the five included records, so the A1 mapping
    identity is True here; the False branch is exercised in tests/test_stats_module.py."""
    rid = [f"lit:{i:012d}" for i in range(1, 16)]
    queries = {"pubmed_01": {"source": "pubmed", "role": "search", "hit_count_api": 10, "n_retrieved": 6, "credential_mode": "keyed", "cap_hit": False},
               "zenodo_01": {"source": "zenodo", "role": "search", "hit_count_api": 5, "n_retrieved": 4, "credential_mode": "credential-free", "cap_hit": False},
               "openalex_01": {"source": "openalex", "role": "search", "hit_count_api": 4, "n_retrieved": 3, "credential_mode": "credential-free", "cap_hit": True},
               "openalex_03_W1": {"source": "openalex", "role": "chase", "hit_count_api": 1, "n_retrieved": 1, "credential_mode": "credential-free", "cap_hit": False},
               "openalex_03r_W2": {"source": "openalex", "role": "chase", "hit_count_api": 1, "n_retrieved": 1, "credential_mode": "credential-free", "cap_hit": False}}
    dump(RUN / "queries.json", queries)
    rec = lambda r, src, qid: {"record_id": r, "canonical": r, "source": src, "query_id": qid, "query_ids": [qid], "retrieved_at": "2026-09-19T00:00:00Z",
                               "ids": {}, "title": f"title {r}", "abstract_or_description": "", "year": 2020, "type": "article", "raw": {}}
    files = {"pubmed": [rec(rid[i], "pubmed", "pubmed_01") for i in range(6)],
             "zenodo": [rec(rid[i], "zenodo", "zenodo_01") for i in range(6, 10)],
             "openalex": [rec(rid[i], "openalex", "openalex_01") for i in range(10, 13)]
             + [rec(rid[13], "openalex", "openalex_03_W1"), rec(rid[14], "openalex", "openalex_03r_W2")]}
    for src, rows in files.items():
        p = RUN / "records" / f"{src}.jsonl"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows), encoding="utf-8", newline="\n")
    outcomes = ["pass"] * 7 + ["uncertain", "pass:non-english-route", "fail:S", "fail:S", "fail:M"]
    merged = [{"record_id": rid[i], "title": f"title {rid[i]}", "prescreen_outcome": outcomes[i], "source_class": "literature", "n_members": 1}
              for i in range(12)]
    (RUN / "merged.jsonl").write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in merged), encoding="utf-8", newline="\n")
    dump(RUN / "prisma_counts.json", {"identified": 15, "after_merge": 12, "duplicates_removed": 3,
                                      "merge": {"rule_1_doi": 2, "rule_2_pmid": 1, "rule_6_skipped_many_dois": 0}})
    write_csv(RUN / "screening_sheet.csv", ["record_id", "to_screen", "prescreen_outcome", "source_class", "title"],
              [[m["record_id"], "yes" if m["prescreen_outcome"] in ("pass", "uncertain", "pass:non-english-route") else "no",
                m["prescreen_outcome"], "literature", m["title"]] for m in merged])
    scr = FIX / "screening"
    write_csv(scr / "prescreen_audit.csv", ["record_id", "stratum", "decision"], [[rid[9], "literature", "include"], [rid[10], "literature", "exclude"]])
    hdr = ["record_id", "stage", "reviewer", "date", "decision", "primary_code", "codes", "reason_text", "llm_suggestion", "llm_agreed",
           "prescreen_outcome", "full_text_retrieved", "arm"]
    ta = [(rid[0], "include", "", ""), (rid[1], "include", "", ""), (rid[2], "include", "", ""), (rid[3], "include", "", ""),
          (rid[4], "unclear", "", ""), (rid[5], "unclear", "", ""),
          (rid[6], "exclude", "E1", "E1"), (rid[7], "exclude", "E1", "E1"), (rid[8], "exclude", "I3", "I3"), (rid[9], "exclude", "I2", "I2;use-only")]
    rows = [[r, "title-abstract", "R1", "2026-09-17", dec, code, codes, "", "", "", "", "", "search"] for r, dec, code, codes in ta]
    ft = [(rid[0], "include", "", "yes"), (rid[1], "include", "", "yes"), (rid[2], "include", "", "no"), (rid[3], "include", "", "yes"),
          (rid[4], "exclude", "E2", "yes"), (rid[5], "exclude", "I5", "no")]
    rows += [[r, "full-text", "R1", "2026-09-18", dec, code, code, "", "", "", "", got, "search"] for r, dec, code, got in ft]
    rows += [[rid[13], "title-abstract", "R1", "2026-09-17", "include", "", "", "", "", "", "", "", "other"],
             [rid[14], "title-abstract", "R1", "2026-09-17", "exclude", "E1", "E1", "", "", "", "", "", "other"],
             [rid[13], "full-text", "R1", "2026-09-18", "include", "", "", "", "", "", "", "yes", "other"]]
    write_csv(scr / "decisions.csv", hdr, rows)
    write_csv(scr / "known_items.csv", ["item", "role", "url", "doi", "note", "retrieved"],
              [["verse", "recall", "", "", "", "yes"], ["ctspine1k", "recall", "", "", "", "no"], ["mri-only", "excluded-I4", "", "", "", ""]])
    write_csv(scr / "chase_manual.csv", ["record_id", "source", "note"], [[rid[14], "manual", ""]])
    # Every charted dataset must be reachable from an INCLUDED record, or the A1 identity
    # `datasets = |map(included_records_search U included_records_other)|` is false by construction:
    # the included records are rid[0..3] (search arm) and rid[13] (other arm), while ds05-ds12 carry
    # source_record.record_ids rid[4..11], which this fixture excludes at prescreen or at screening.
    # So each of ds05-ds12 is listed here against one of the five included records, with rid[0] and
    # rid[1] each describing three datasets (a companion article covering a family of releases) and
    # rid[13] two. tests/test_stats_module.py holds the matching negative case.
    src_rows = [["ds01", rid[0], "source"], ["ds01", rid[1], "use"], ["ds02", rid[2], "source"], ["ds03", rid[3], "source"],
                ["ds03", rid[13], "use"], ["ds03", rid[1], "use"]]
    src_rows += [[did, rid[j], "source"] for did, j in
                 (("ds04", 3), ("ds05", 0), ("ds06", 1), ("ds07", 2), ("ds08", 3), ("ds09", 13), ("ds10", 0), ("ds11", 1), ("ds12", 13))]
    write_csv(FIX / "dataset_sources.csv", ["dataset_id", "record_id", "role"], sorted(src_rows))


def main() -> int:
    ds = records()
    for d in ds:
        dump(FIX / "charting" / f"{d['id']}.json", copy.deepcopy(d))
    probes_files(ds)
    screening_and_run()
    print(f"fixture written: {len(ds)} charting records under {FIX}, run inputs under {RUN}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
