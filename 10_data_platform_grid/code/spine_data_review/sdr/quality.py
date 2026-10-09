"""Rubric scoring (quality_rubric.md): ten items 0/1/2 from charted fields, the fit booleans, analysis/quality.json.

WHY A SCORE IS A PURE FUNCTION OF THE CHART. The rubric exists so that a dataset's usability can
be ranked and argued about; the only way that ranking stays auditable is if every point traces
to a charted field, and every charted field to a quote or an API value. So this module reads
`charting/datasets/<id>.json` and nothing else: no network, no disk on the grid, no reviewer
judgement. A score changes only when a chart changes, the blind re-charting sample (protocol
section 8) is scored by the same code on its own directory (`--charting-dir`), and the rule that
fired is written next to every item so a reader can dispute the rule rather than the number.

Each `q<N>` function below carries its rule text verbatim from quality_rubric.md and returns
(score, rule_fired). Interpretations the rubric leaves implicit are stated at the rule and in
the summary: an `explicit-label` variant without both counts scores Q4 = 1 (row 1 names only
derivable-from-labels, reported-in-text and excluded-by-design; the reading "a label scheme
that could carry it" is recorded in PIPELINE.md stage 6 and is owed a deviations-log row in
PROTOCOL.md section 19, which the rule string says); a level-name origin entry missing from
`annotation_origin_by_type` fails F2 (the schema requires the entry, so its absence is a charting
defect, not expert origin); Q7 treats a 2xx status, or an API-method probe whose class is a
repository state, as "answered", and takes the file confirmation from the file probes (entries
whose url equals `file_url_probed`, plus `file_probes[]` of charting/probes/<id>.json) answering
200/206 on **two distinct dates**, or from a rule that requires file evidence by definition
(P1, P13, P14, P15, P20) on both probes. `file_url_confirmed()` is the one implementation of
that rule; sdr/stats.py imports it for the SAP A3.2 file-URL row so the two cannot drift.

Output `analysis/quality.json`: {per_dataset: {id: {items: {Q1..Q10: {score, rule}}, total,
total_without_q7, total_without_q6_q7_q8, band, annotated, q2_type_read, fit_level_id,
fit_level_id_fail_rule, usable_for_training, usable_for_training_fail_rule, fit_variant,
fit_stitching, fit_stitching_fail_rule, verified, derived_from}}, summary, derived_from, rule,
scores_sha1} and, unless --no-tex, tables/quality.tex (one row per dataset, ten item columns and
the total). sdr/stats.py later merges its A4 blocks (summary.total, fitness, total_vs_year,
total_vs_route, total_vs_modality, analysis_derived_from) into the same file for the manuscript;
when this module rewrites the file and `scores_sha1` is unchanged those blocks are carried over,
so the two modules can run in either order; when the scores changed they are dropped and the
message says stats must be rerun.
CLI: python -m sdr.quality --run-dir R --run-date D [--charting-dir charting/datasets]
[--out analysis/quality.json] [--verified-only] [--limit N] [--dry-run] [--selftest]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from sdr.common import add_common_args, dump_json, init_run_dir, review_root

# Order in which Q2 reads the annotation types (quality_rubric.md Q2; the annotation_type enum order).
Q2_TYPE_ORDER = ("per-vertebra-level-names", "segmentation-3d", "segmentation-2d", "landmarks", "bounding-boxes",
                 "centroids", "pathology-labels", "fracture-grade", "measurements", "radiology-reports",
                 "image-level-labels")
EXPERT = {"expert-manual", "expert-corrected-model"}
# Probe classes that a repository API reports as a state without an HTTP 2xx on the landing page (Q7).
API_STATE = {"open-download", "registration", "data-use-agreement", "request-to-authors", "commercial"}
# Rules whose definition requires a file URL to have answered 200/206 (PROTOCOL.md section 10).
FILE_EVIDENCE_RULES = {"P1", "P13", "P14", "P15", "P20"}
BANDS = ((6, "low"), (13, "medium"), (20, "high"))


def _unannotated(d: dict) -> bool:
    return d.get("annotation_types") == ["none"]


def q1_documentation(d: dict) -> tuple[int, str]:
    """Q1. 0: article_or_preprint = false and (repository_record_or_readme = false or
    description_at_least_100_words = false). 2: article and repository record and states_population
    and states_acquisition and (states_annotation_protocol or unannotated) and
    states_file_layout_and_label_scheme. 1: otherwise."""
    doc = d["documentation"]
    if not doc["article_or_preprint"] and (not doc["repository_record_or_readme"]
                                           or not doc["description_at_least_100_words"]):
        return 0, "Q1=0: no article and (no repository record or description under 100 words)"
    if (doc["article_or_preprint"] and doc["repository_record_or_readme"] and doc["states_population"]
            and doc["states_acquisition"] and (doc["states_annotation_protocol"] or _unannotated(d))
            and doc["states_file_layout_and_label_scheme"]):
        return 2, "Q1=2: article and repository record; population, acquisition, annotation protocol and file layout stated"
    return 1, "Q1=1: neither the 0 nor the 2 condition holds (partial documentation)"


def q2_type_read(d: dict) -> str | None:
    """The first annotation type present in Q2_TYPE_ORDER; None when the dataset is unannotated."""
    types = set(d.get("annotation_types") or [])
    return next((t for t in Q2_TYPE_ORDER if t in types), None)


def q2_origin(d: dict) -> tuple[int, str]:
    """Q2. 0: annotation_types = [none] or the origin read is [unknown]. 2: the origin read contains
    expert-manual or expert-corrected-model and annotator_qualification_stated. 1: otherwise (no
    expert category, or expert without a stated qualification). The origin read is
    annotation_origin_by_type[first type in Q2_TYPE_ORDER]; a missing entry (a schema violation)
    falls back to the union field annotation_origin and says so."""
    t = q2_type_read(d)
    if t is None:
        return 0, "Q2=0: unannotated"
    origin = d.get("annotation_origin_by_type", {}).get(t)
    note = ""
    if origin is None:
        origin, note = d.get("annotation_origin", []), " (entry missing; union field read)"
    if not origin or set(origin) == {"unknown"}:
        return 0, f"Q2=0: origin of {t} is unknown{note}"
    if EXPERT & set(origin) and d.get("annotator_qualification_stated"):
        return 2, f"Q2=2: {t} has an expert origin and the annotator qualification is stated{note}"
    if EXPERT & set(origin):
        return 1, f"Q2=1: {t} has an expert origin but annotator_qualification_stated = false{note}"
    return 1, f"Q2=1: origin of {t} is {'/'.join(sorted(origin))}, not expert{note}"


def q3_validation(d: dict) -> tuple[int, str]:
    """Q3. 0: unannotated or described = false. 2: inter_rater_statistic != none, value and n not
    null, (ci not null or per_structure_breakdown), and not (fraction_of_items < 0.10 and n < 30).
    1: described and not 2. fraction_of_items = null counts as not < 0.10."""
    v = d["annotation_validation"]
    if _unannotated(d) or not v["described"]:
        return 0, "Q3=0: unannotated or no validation described"
    frac, n = v.get("fraction_of_items"), v.get("inter_rater_n")
    small = frac is not None and n is not None and frac < 0.10 and n < 30
    if (v["inter_rater_statistic"] != "none" and v["inter_rater_value"] is not None and n is not None
            and (v["inter_rater_ci"] is not None or v["per_structure_breakdown"]) and not small):
        return 2, "Q3=2: statistic with n and (interval or per-structure breakdown), not on a small subset"
    if small:
        return 1, "Q3=1: statistic computed on under 10 % of items and fewer than 30 items"
    if v["inter_rater_statistic"] != "none" and n is None and v["inter_rater_ci"] is None:
        return 1, "Q3=1: statistic without n and without an interval"
    return 1, "Q3=1: validation described (qa_process or statistic) but the 2 condition does not hold"


def q4_variants(d: dict) -> tuple[int, str]:
    """Q4. 2: any variant with how_labelled = explicit-label and n_subjects_with and
    n_subjects_assessed non-null. 1: any variant with how_labelled in {derivable-from-labels,
    reported-in-text, excluded-by-design}, or explicit-label without both counts (a label scheme
    that could carry it). 0: all three status = unknown, or every how_labelled in {not-labelled,
    unknown}."""
    vl = d["variant_labels"]
    hows = {v: vl[v]["how_labelled"] for v in ("L6", "T13", "LSTV")}
    for v, how in hows.items():
        if how == "explicit-label" and vl[v]["n_subjects_with"] is not None and vl[v]["n_subjects_assessed"] is not None:
            return 2, f"Q4=2: {v} labelled per subject with a computable prevalence"
    ack = [v for v, how in hows.items() if how in {"derivable-from-labels", "reported-in-text", "excluded-by-design"}]
    if ack:
        return 1, f"Q4=1: variant acknowledged without a computable prevalence ({', '.join(ack)})"
    if "explicit-label" in hows.values():
        return 1, ("Q4=1: explicit-label without both counts (interpretation of rubric row 1, "
                   "PROTOCOL.md section 19 deviations log, row dated 2026-09-19 'quality_rubric.md row 1 (Q4)')")
    return 0, "Q4=0: no variant labelled or acknowledged"


def q5_metadata(d: dict) -> tuple[int, str]:
    """Q5. 0: 0-1 metadata elements; 1: 2-4; 2: 5-6."""
    n = len(set(d.get("metadata_elements") or []))
    return (0 if n <= 1 else 1 if n <= 4 else 2), f"Q5={0 if n <= 1 else 1 if n <= 4 else 2}: {n} metadata elements"


def q6_licence(d: dict) -> tuple[int, str]:
    """Q6. 0: tier = unknown. 2: standard = true and stated_in in {repository, both} and consistent in
    {yes, single-source}. 1: otherwise (non-standard terms, inconsistent, or stated only in the article)."""
    li = d["licence"]
    if li["tier"] == "unknown":
        return 0, "Q6=0: licence tier unknown"
    if li["standard"] and li["stated_in"] in {"repository", "both"} and li["consistent"] in {"yes", "single-source"}:
        return 2, "Q6=2: standard licence, visible on the repository, consistent"
    why = "non-standard terms" if not li["standard"] else "inconsistent" if li["consistent"] == "no" else f"stated_in = {li['stated_in']}"
    return 1, f"Q6=1: {why}"


def _answered(p: dict) -> bool:
    s = p.get("http_status")
    return p.get("method") != "none" and ((s is not None and 200 <= s < 300)
                                           or (p.get("method") == "API" and p.get("classification_machine") in API_STATE))


def load_file_probes(probes_dir: Path, d: dict) -> None:
    """Attach `_file_probes` (the file_probes[] of charting/probes/<id>.json, [] when absent) to a
    charting record in place. sdr/availability.py keeps the file-URL probes there, not in the
    record's access_probe[], so every reader of file evidence goes through this one loader."""
    pf = probes_dir / f"{d['id']}.json"
    d["_file_probes"] = (json.loads(pf.read_text(encoding="utf-8")).get("file_probes") or []) if pf.exists() else []


def file_probe_dates_ok(d: dict) -> set[str]:
    """The distinct probe dates on which the file URL answered 200 or 206: access_probe entries whose
    url equals `file_url_probed` plus `_file_probes` (load_file_probes). Same-day repeats count once."""
    file_url = d.get("file_url_probed")
    files = [p for p in d.get("access_probe") or [] if file_url and p.get("url") == file_url] + list(d.get("_file_probes") or [])
    return {str(p.get("date")) for p in files if p.get("http_status") in (200, 206)}


def file_url_confirmed(d: dict) -> bool:
    """SAP A3.2 second row and rubric Q7: the file URL answered 200/206 on both probes, read as two
    distinct dates (two probes on one day are one probe for the 48 h rule of protocol section 10)."""
    return len(file_probe_dates_ok(d)) >= 2


def q7_probe(d: dict) -> tuple[int, str]:
    """Q7. Scoring probes = the first two landing probes, or the two that agree on
    classification_machine when a third was run. 0: neither answered (non-2xx, no response, or
    method = none throughout). 2: both answered with the same classification_machine and the file
    URL answered 200/206 on both (file probes on two distinct dates, or a file-evidence rule on
    both scoring probes). 1: otherwise."""
    file_url = d.get("file_url_probed")
    landing = [p for p in d["access_probe"] if not (file_url and p.get("url") == file_url)]
    scoring = landing[:2]
    if len(landing) >= 3:
        for i in range(len(landing)):
            for j in range(i + 1, len(landing)):
                if landing[i]["classification_machine"] == landing[j]["classification_machine"]:
                    scoring = [landing[i], landing[j]]
                    break
            else:
                continue
            break
    answered = [_answered(p) for p in scoring]
    if not any(answered):
        return 0, "Q7=0: no scoring probe answered (P22/P23 or method none)"
    if sum(answered) == 1 or len(scoring) < 2:
        return 1, "Q7=1: exactly one scoring probe answered"
    if scoring[0]["classification_machine"] != scoring[1]["classification_machine"]:
        return 1, "Q7=1: the scoring probes disagree on the classification"
    file_ok = file_url_confirmed(d) or all(p.get("rule") in FILE_EVIDENCE_RULES for p in scoring)
    if file_ok:
        return 2, "Q7=2: both probes answered with the same classification and a file URL answered 200/206 on both (two dates)"
    return 1, "Q7=1: both probes agree but no file URL was confirmed on two distinct dates"


def q8_versioning(d: dict) -> tuple[int, str]:
    """Q8. 0: dataset_doi, version_identifier both null and versions empty. 2: dataset_doi resolving
    to a dataset record and (version_identifier or versions) and changelog_or_versioned_records. 1: otherwise."""
    v, versions = d["versioning"], d.get("versions") or []
    if v["dataset_doi"] is None and v["version_identifier"] is None and not versions:
        return 0, "Q8=0: no dataset DOI, version identifier or named versions"
    if (v["dataset_doi"] is not None and v["doi_resolves_to"] == "dataset-record"
            and (v["version_identifier"] is not None or versions) and v["changelog_or_versioned_records"]):
        return 2, "Q8=2: dataset DOI resolving to a record, a version, and a change log"
    return 1, "Q8=1: partial versioning (see rubric Q8 examples)"


def q9_split(d: dict) -> tuple[int, str]:
    """Q9. 0: split_defined in {no, unknown} and patient_level_dedup in {no, unknown}. 2: split_defined
    = yes and ((patient_level_dedup = yes and grouping_variable_released) or patient_level_dedup = NA).
    1: otherwise."""
    split, dedup, grp = d["split_defined"], d["patient_level_dedup"], d["grouping_variable_released"]
    if split in {"no", "unknown"} and dedup in {"no", "unknown"}:
        return 0, "Q9=0: no split and no patient-level de-duplication stated"
    if split == "yes" and ((dedup == "yes" and grp) or dedup == "NA"):
        return 2, "Q9=2: released split, patient-grouped (or one image per subject)"
    return 1, "Q9=1: split or de-duplication but not both with a released grouping variable"


def q10_quality(d: dict) -> tuple[int, str]:
    """Q10. 2: yes-quantitative; 1: yes-qualitative; 0: no or unknown."""
    iq = d["image_quality_reported"]
    return {"yes-quantitative": (2, "Q10=2: quantitative quality metrics released"),
            "yes-qualitative": (1, "Q10=1: qualitative quality statement or exclusions")}.get(iq, (0, f"Q10=0: image_quality_reported = {iq}"))


ITEMS = (("Q1", q1_documentation), ("Q2", q2_origin), ("Q3", q3_validation), ("Q4", q4_variants), ("Q5", q5_metadata),
         ("Q6", q6_licence), ("Q7", q7_probe), ("Q8", q8_versioning), ("Q9", q9_split), ("Q10", q10_quality))


def fitness(d: dict) -> dict:
    """The fit booleans of quality_rubric.md, each with the first failing rule (F1-F4), plus
    fit_variant (any variant status = yes) and fit_stitching (region meets {thoracic, whole-spine})."""
    origin = set(d.get("annotation_origin_by_type", {}).get("per-vertebra-level-names") or [])
    n = d.get("n_subjects")
    rules = {"F1": d["per_vertebra_level_names"] in {"yes", "partial"},
             "F2": bool(EXPERT & origin) and "counting-inferred" not in origin,
             "F3": d["access_route"] in {"open-download", "registration", "data-use-agreement"},
             "F4": n is not None and n >= 20}
    first_fail = next((r for r, ok in rules.items() if not ok), None)
    usable_fail = next((r for r in ("F1", "F3", "F4") if not rules[r]), None)
    fit = first_fail is None
    variant = fit and any(d["variant_labels"][v]["status"] == "yes" for v in ("L6", "T13", "LSTV"))
    region_ok = bool({"thoracic", "whole-spine"} & set(d.get("region") or []))
    return {"fit_level_id": fit, "fit_level_id_fail_rule": first_fail, "usable_for_training": usable_fail is None,
            "usable_for_training_fail_rule": usable_fail, "fit_variant": variant,
            "fit_stitching": fit and region_ok,
            "fit_stitching_fail_rule": first_fail or (None if region_ok else "region lacks thoracic/whole-spine"),
            "rules": rules}


def score_record(d: dict, path: str | None = None) -> dict:
    """Score one charting record: items, totals, band, fitness, derived_from."""
    items = {q: dict(zip(("score", "rule"), fn(d))) for q, fn in ITEMS}
    total = sum(v["score"] for v in items.values())
    out = {"items": items, "total": total, "total_without_q7": total - items["Q7"]["score"],
           "total_without_q6_q7_q8": total - sum(items[q]["score"] for q in ("Q6", "Q7", "Q8")),
           "band": next(b for hi, b in BANDS if total <= hi), "annotated": not _unannotated(d),
           "q2_type_read": q2_type_read(d), "verified": d.get("verified_by") is not None,
           "derived_from": [path] if path else []}
    out.update({k: v for k, v in fitness(d).items() if k != "rules"})
    return out


def scores_sha1(per_dataset: dict) -> str:
    """SHA-1 over the sorted JSON of per_dataset: the value stored as `scores_sha1`, which
    sdr/stats.py recomputes to refuse a hand-edited quality.json."""
    return hashlib.sha1(json.dumps(per_dataset, sort_keys=True).encode("utf-8")).hexdigest()


def load_records(charting_dir: Path, limit: int | None = None) -> list[tuple[str, dict]]:
    """(relative path, record) for every *.json under charting_dir, sorted by file name."""
    files = sorted(charting_dir.glob("*.json"))[: limit or None]
    return [(str(p.relative_to(review_root())) if review_root() in p.parents else str(p),
             json.loads(p.read_text(encoding="utf-8"))) for p in files]


def summarise(scored: dict[str, dict]) -> dict:
    """Counts the manuscript needs at a glance; the full A4 analysis lives in sdr/stats.py."""
    totals = sorted(v["total"] for v in scored.values())
    return {"n_datasets": len(scored), "n_verified": sum(v["verified"] for v in scored.values()),
            "n_annotated": sum(v["annotated"] for v in scored.values()),
            "n_fit_level_id": sum(v["fit_level_id"] for v in scored.values()),
            "n_usable_for_training": sum(v["usable_for_training"] for v in scored.values()),
            "n_fit_variant": sum(v["fit_variant"] for v in scored.values()),
            "n_fit_stitching": sum(v["fit_stitching"] for v in scored.values()),
            "bands": {b: sum(v["band"] == b for v in scored.values()) for _, b in BANDS},
            "item_share": {q: {str(s): sum(v["items"][q]["score"] == s for v in scored.values()) for s in (0, 1, 2)}
                           for q, _ in ITEMS},
            "total_min": totals[0] if totals else None, "total_max": totals[-1] if totals else None}


def render_tex(scored: dict[str, dict]) -> str:
    """tables/quality.tex: booktabs rows id, Q1..Q10, total, band, fit; sorted by total desc then id."""
    rows = sorted(scored.items(), key=lambda kv: (-kv[1]["total"], kv[0]))
    head = ("\\begin{tabular}{l" + "r" * 10 + "rll}\n\\toprule\nDataset & " + " & ".join(q for q, _ in ITEMS)
            + " & Total & Band & Fit \\\\\n\\midrule\n")
    body = "".join(f"{k.replace('_', '\\_')} & " + " & ".join(str(v['items'][q]['score']) for q, _ in ITEMS)
                   + f" & {v['total']} & {v['band']} & {'yes' if v['fit_level_id'] else v['fit_level_id_fail_rule']} \\\\\n"
                   for k, v in rows)
    return "% generated by sdr/quality.py from analysis/quality.json; do not edit\n" + head + body + "\\bottomrule\n\\end{tabular}\n"


def _selftest() -> int:
    """Score the worked example of quality_rubric.md (total 15, high band, fit_level_id true) from a
    minimal record; no file is read or written."""
    ex = {"annotation_types": ["segmentation-3d", "per-vertebra-level-names"],
          "annotation_origin_by_type": {"segmentation-3d": ["expert-corrected-model"], "per-vertebra-level-names": ["expert-manual"]},
          "annotator_qualification_stated": True, "annotation_origin": ["expert-manual", "expert-corrected-model"],
          "documentation": {k: True for k in ("article_or_preprint", "repository_record_or_readme", "description_at_least_100_words",
                                              "states_population", "states_acquisition", "states_annotation_protocol",
                                              "states_file_layout_and_label_scheme")},
          "annotation_validation": {"described": True, "qa_process": "double-read", "inter_rater_statistic": "dice",
                                    "inter_rater_value": 0.93, "inter_rater_ci": None, "inter_rater_sd": None, "inter_rater_n": 20,
                                    "fraction_of_items": 0.2, "per_structure_breakdown": True, "n_raters": 2,
                                    "comparator": "rater-vs-rater", "n_categories": None, "comparable_group": "dice-vertebra-3d"},
          "variant_labels": {v: {"status": "unknown", "how_labelled": "derivable-from-labels" if v == "L6" else "not-labelled",
                                 "n_subjects_with": None, "n_subjects_assessed": None, "unit": "subject", "definition": "",
                                 "definition_class": "count-based", "ascertainment": "unknown", "selection": "unknown"}
                             for v in ("L6", "T13", "LSTV")},
          "metadata_elements": ["age-sex", "scanner-or-acquisition-parameters", "spacing-or-dicom-headers", "site-and-country"],
          "licence": {"text": "CC BY-SA 4.0", "tier": "open", "url": None, "spdx": "CC-BY-SA-4.0", "standard": True,
                      "stated_in": "both", "consistent": "yes"},
          "file_url_probed": "https://example.org/f.zip",
          "access_probe": [{"url": "https://example.org/d", "method": "HEAD", "http_status": 200, "classification_machine": "open-download", "rule": "P20"},
                           {"url": "https://example.org/d", "method": "HEAD", "http_status": 200, "classification_machine": "open-download", "rule": "P20"},
                           {"url": "https://example.org/f.zip", "method": "GET-range", "http_status": 206, "classification_machine": "open-download", "rule": "P15"},
                           {"url": "https://example.org/f.zip", "method": "GET-range", "http_status": 206, "classification_machine": "open-download", "rule": "P15"}],
          "versioning": {"dataset_doi": "10.5281/zenodo.1", "doi_resolves_to": "dataset-record", "version_identifier": "v1",
                         "changelog_or_versioned_records": False}, "versions": [],
          "split_defined": "yes", "patient_level_dedup": "yes", "grouping_variable_released": True,
          "image_quality_reported": "no", "per_vertebra_level_names": "yes", "access_route": "open-download",
          "n_subjects": 160, "region": ["thoracic", "lumbar"], "verified_by": "R2"}
    s = score_record(ex)
    expect = {"Q1": 2, "Q2": 2, "Q3": 2, "Q4": 1, "Q5": 1, "Q6": 2, "Q7": 2, "Q8": 1, "Q9": 2, "Q10": 0}
    got = {q: s["items"][q]["score"] for q in expect}
    ok = got == expect and s["total"] == 15 and s["band"] == "high" and s["fit_level_id"] and not s["fit_variant"] and s["fit_stitching"]
    # Q7 file confirmation needs two distinct dates: the example's file probes carry none, so the 2
    # there comes from the P20 file-evidence rule; two same-day 206 probes alone must not confirm.
    same_day = {"file_url_probed": "https://x/f.zip", "access_probe": [], "_file_probes": [
        {"url": "https://x/f.zip", "http_status": 206, "date": "2026-09-10"}, {"url": "https://x/f.zip", "http_status": 206, "date": "2026-09-10"}]}
    two_days = {**same_day, "_file_probes": same_day["_file_probes"][:1] + [{"url": "https://x/f.zip", "http_status": 200, "date": "2026-09-13"}]}
    ok &= not file_url_confirmed(same_day) and file_url_confirmed(two_days)
    print("selftest worked example and file-URL two-date rule:", "ok" if ok else f"FAIL got {got} total {s['total']}")
    return 0 if ok else 1


MERGED_BY_STATS = ("fitness", "total_vs_year", "total_vs_route", "total_vs_modality", "analysis_derived_from")


def carry_over(previous: dict | None, out: dict) -> str:
    """Keep the A4 blocks sdr/stats.py merged into an existing quality.json when the scores are
    unchanged (same scores_sha1); drop them otherwise and say so. Returns a one-line message."""
    if not previous:
        return "no previous quality.json; stats blocks absent until sdr.stats runs"
    if previous.get("scores_sha1") != out["scores_sha1"]:
        return "scores changed since the previous quality.json; the stats blocks were dropped, rerun sdr.stats"
    kept = [k for k in MERGED_BY_STATS if k in previous]
    for k in kept:
        out[k] = previous[k]
    if "total" in previous.get("summary", {}):
        out["summary"]["total"] = previous["summary"]["total"]
        kept.append("summary.total")
    return ("scores unchanged; carried over the stats blocks " + ", ".join(kept)) if kept else "scores unchanged; no stats block to carry over"


def main(argv: list[str] | None = None) -> int:
    ap = add_common_args(argparse.ArgumentParser(prog="python -m sdr.quality", description=__doc__.split("\n")[0]))
    ap.add_argument("--charting-dir", default="charting/datasets", help="directory of charting records, relative to spine_data_review/")
    ap.add_argument("--probes-dir", default=None, help="sdr/availability.py probe histories (<id>.json with file_probes[]) for Q7; "
                    "default: the `probes` directory beside --charting-dir (charting/probes)")
    ap.add_argument("--out", default="analysis/quality.json")
    ap.add_argument("--tex", default="tables/quality.tex")
    ap.add_argument("--no-tex", action="store_true")
    ap.add_argument("--verified-only", action="store_true", help="skip records with verified_by = null")
    ap.add_argument("--selftest", action="store_true", help="score the rubric's worked example and exit")
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    root = review_root()
    cdir = Path(a.charting_dir) if Path(a.charting_dir).is_absolute() else root / a.charting_dir
    recs = load_records(cdir, a.limit)
    if a.verified_only:
        recs = [(p, d) for p, d in recs if d.get("verified_by") is not None]
    if a.dry_run:
        print(f"would score {len(recs)} record(s) from {cdir} -> {a.out}" + ("" if a.no_tex else f", {a.tex}"))
        for p, d in recs:
            print(f"  {d.get('id', '?'):32s} {p}")
        return 0
    init_run_dir(a.run_dir, a.run_date, argv)
    scored, pdir = {}, (cdir.parent / "probes" if a.probes_dir is None else Path(a.probes_dir) if Path(a.probes_dir).is_absolute() else root / a.probes_dir)
    for p, d in recs:
        load_file_probes(pdir, d)
        scored[d["id"]] = score_record(d, p)
    out = {"per_dataset": scored, "summary": summarise(scored), "run_date": a.run_date, "rule": "quality_rubric.md (protocol 1.0)",
           "derived_from": sorted(p for p, _ in recs), "scores_sha1": scores_sha1(scored)}
    out_path = root / a.out
    previous = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else None
    carried = carry_over(previous, out)
    dump_json(out_path, out)
    if not a.no_tex:
        tex = root / a.tex
        tex.parent.mkdir(parents=True, exist_ok=True)
        tex.write_text(render_tex(scored), encoding="utf-8", newline="\n")
    n_unverified = sum(not v["verified"] for v in scored.values())
    print(f"scored {len(scored)} dataset(s) -> {root / a.out}; unverified: {n_unverified}; "
          f"fit_level_id: {out['summary']['n_fit_level_id']}; fit_stitching: {out['summary']['n_fit_stitching']}; {carried}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
