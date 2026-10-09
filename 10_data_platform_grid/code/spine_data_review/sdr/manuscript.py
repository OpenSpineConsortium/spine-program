"""Render manuscript/main.tex and every table it inputs from the review's outputs; no number is typed.

WHAT. `manuscript/template.tex` is the PRISMA-ScR skeleton with `@@MARKER@@` placeholders. This
module writes `tables/*.tex` (the renderers are in sdr.manuscript_tables) from the protocol files,
the run's queries, the charting records and `analysis/*.json`; writes `tables/numbers.tex` (one
`\\num<Name>` macro per manuscript number and a `\\numword<Name>` twin that spells out integers under
ten); replaces each marker with an `\\input`, a date, a commit or the appendix; and reports bare
digits in the Abstract and Results, unreplaced markers and the abstract length (`--check` makes
them fatal; `--scan <main.tex>` runs the same check on a rendered file for build.sh).

WHY. PROTOCOL.md section 13 requires every manuscript number to trace to a file: a typed count
survives a rerun that changes it. So the .tex the author edits holds no data; a value missing from
`analysis/` renders as a red `\\pending{Name}` instead of a guess, and build.sh counts them. The
pooled LSTV macros are pending whenever a pooled block exists that the file does not attribute to the
SAP's primary estimator (the logit GLMM of sdr.meta) -- naming a sensitivity estimator and naming none
are both pending, with the reason saying which -- so neither a DerSimonian-Laird value nor an
unattributed one can be printed as the pre-specified result. \\numSourcesRun counts sources that
returned at least one record (Retrieved > 0, from the flow where it has an entry), which is the claim
the Results sentence makes and the number Table 2's rows add up to. Rendering is deterministic: sorted
inputs, no wall-clock values; the git commit is recorded once into <run-dir>/run_meta.json and read
back from there, so a re-render on a later commit with the same inputs produces the same main.tex.

ASSUMED SHAPES of files other modules own (every accessor accepts a value written bare or as the
SAP envelope {value, derived_from, rule}). Queries: <run-dir>/queries.json (information_sources.md,
"What is recorded for every query") with queries/*.yaml (id -> {string, markdown_string?, source_code,
source_name, source, role, endpoint, coverage, credential_mode_expected, ...}) merged underneath,
counts.json as sdr.search_* write it ({source: {n_items, ..., queries: {qid: {hit_count_api,
n_retrieved, ...}}}}; a flat {qid: ...} form is accepted) and the pilot record appended. Charting:
charting/datasets/<id>.json per charting_schema.json. The dotted paths in NUMBER_MACROS are the
number contract; the table contracts are: quality.json per_dataset.{id: {items.Q1..Q10 (score or
{score, rule}), total, fit_level_id, fit_level_id_fail_rule, fit_stitching}} and reliability {n,
icc_total: {value, ci}, per_item_kappa: {Q1..Q10}}; descriptives.json by_<stratifier>.{stratum:
{n_datasets, n_subjects_sum, n_subjects_median, n_images_sum}}; availability.json
route_distribution.overall and described_public_downloads.{primary, file_url, recipe_eligible}.
{numerator, denominator, proportion, ci}; pooled_variants.json {L6,T13,LSTV}.{per_dataset: [{id,
modality, x, n, p, ci_low, ci_high, selection, ascertainment, definition_class}], k_eligible, pooled:
{estimate, ci_low, ci_high, pi_low, pi_high, estimator} | null} and estimator_note;
pooled_agreement.json per_dataset: [{id, statistic, value, ci, n, comparator, n_categories, group}];
grid_coverage.json per_dataset: [{id, status, path, n_subjects_on_grid}] and recipe_order: [{id,
quality_total}]; flow.json per_source.{source: {n_identified}}; build_info.json git_commit.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from sdr import PROTOCOL_VERSION
from sdr.common import add_common_args, dump_json, load_queries, resolve_run_dir, review_root
from sdr.manuscript_tables import (SEARCH_ROLES, dig, esc, executed, fmt, is_primary_estimator, md_tables, pending_table,  # noqa: F401 (re-exported)
                                   planned_key, planned_sources, pooled_estimator, source_key, sources_run, t_agreement, t_availability, t_counts,
                                   t_data_items, t_datasets_main, t_eligibility, t_grid, t_md, t_pooled_variants, t_quality,
                                   t_search_strings, t_sources)

ROOT = review_root()
PILOT_DIR = ROOT / "runs" / "pilot-2026-09-19"
ANALYSES = ("flow", "descriptives", "availability", "quality", "pooled_variants", "pooled_agreement",
            "grid_coverage", "screening_reliability", "search_validation", "build_info")
FIGURES = ("prisma_flow", "datasets_by_year", "quality", "availability", "variants")
# Template figure name -> the files sdr/figures.py writes (several for the forest plots; each that exists is included).
FIGURE_FILES = {"prisma_flow": ["fig1_prisma_flow"], "datasets_by_year": ["fig2_datasets_per_year"], "availability": ["fig3_access_by_modality"],
                "quality": ["fig4_quality"], "variants": ["fig5_forest_L6", "fig5_forest_T13", "fig5_forest_LSTV"]}
# The template's numbers: file -> kind -> {macro name: dotted path}. kind: int | pct | dec | p | text.
NUMBER_MACROS: dict[str, dict[str, dict[str, str]]] = {
    "flow": {"int": {"Identified": "search_arm.identified", "AfterMerge": "search_arm.after_merge", "Screened": "search_arm.screened",
                     "SoughtFullText": "search_arm.sought_for_full_text", "IncludedRecordsSearch": "search_arm.included_records",
                     "IncludedRecordsOther": "other_arm.included_records", "KnownItems": "other_arm.known_items", "Datasets": "datasets.total",
                     "DatasetsDerived": "datasets.derived", "DatasetsFigureDerived": "datasets.figure_derived"}},
    "descriptives": {"int": {"DatasetsCT": "by_modality.CT.n_datasets", "DatasetsXR": "by_modality.radiograph.n_datasets",
                             "DatasetsFluoro": "by_modality.fluoroscopy.n_datasets", "DatasetsDXA": "by_modality.DXA-VFA.n_datasets",
                             "DatasetsWholeSpine": "by_region.whole-spine.n_datasets", "DatasetsThoracic": "by_region.thoracic.n_datasets",
                             "SubjectsTotal": "totals.n_subjects_sum", "LevelNamesYes": "by_level_names.yes.n_datasets",
                             "CountingInferred": "by_annotation_origin.counting-inferred.n_datasets", "VariantExplicit": "by_variant_labelling.explicit-label.n_datasets"}},
    "availability": {"int": {"OpenDownload": "route_distribution.overall.open-download", "Registration": "route_distribution.overall.registration",
                             "DUA": "route_distribution.overall.data-use-agreement", "RequestToAuthors": "route_distribution.overall.request-to-authors",
                             "Unavailable": "route_distribution.overall.unavailable", "Commercial": "route_distribution.overall.commercial",
                             "DescribedPublic": "described_public_downloads.primary.denominator", "DescribedPublicDownloads": "described_public_downloads.primary.numerator",
                             "VerifierOverrides": "verifier_overrides.n", "ProbeChanged": "probe_agreement.n_changed"},
                     "pct": {"PctDescribedPublicDownloads": "described_public_downloads.primary.proportion"}},
    "quality": {"dec": {"QualityMedian": "summary.total.median", "QualityQOne": "summary.total.q1", "QualityQThree": "summary.total.q3",
                        "RhoQualityYear": "total_vs_year.annotated.rho", "ICCTotal": "reliability.icc_total.value",
                        "ICCTotalLow": "reliability.icc_total.ci.0", "ICCTotalHigh": "reliability.icc_total.ci.1"},
                "int": {"FitLevelId": "fitness.fit_level_id.n", "FitStitching": "fitness.fit_stitching.n", "FitVariant": "fitness.fit_variant.n",
                        "UsableTraining": "fitness.usable_for_training.n", "ReliabilitySample": "reliability.n"}, "p": {"PKruskalRoute": "total_vs_route.annotated.p"}},
    "pooled_variants": {"int": {"PoolableLSix": "L6.k_eligible", "PoolableTThirteen": "T13.k_eligible", "PoolableLSTV": "LSTV.k_eligible"},
                        "pct": {"PooledLSTV": "LSTV.pooled.estimate", "PooledLSTVLow": "LSTV.pooled.ci_low", "PooledLSTVHigh": "LSTV.pooled.ci_high",
                                "PiLSTVLow": "LSTV.pooled.pi_low", "PiLSTVHigh": "LSTV.pooled.pi_high"},
                        "text": {"PooledEstimator": "LSTV.pooled.estimator"}},
    "pooled_agreement": {"int": {"AgreementDatasets": "n_datasets_with_statistic"}},
    "grid_coverage": {"int": {"OnGrid": "overall.n_on_grid", "ReachableNotOnGrid": "overall.n_reachable_not_on_grid"}},
    "screening_reliability": {"int": {"DualSample": "dual_sample.n", "LLMCovered": "llm.n_covered"},
                              "dec": {"KappaDual": "dual_sample.kappa_binary.value", "KappaDualLow": "dual_sample.kappa_binary.ci.0",
                                      "KappaDualHigh": "dual_sample.kappa_binary.ci.1", "KappaLLM": "llm.kappa_binary.value"}},
    "search_validation": {"pct": {"RecallKnownItems": "known_item_recall.overall.recall"},
                          "int": {"KnownRetrieved": "known_item_recall.overall.retrieved", "KnownRecallDenominator": "known_item_recall.overall.denominator"}}}
# Macros that report the pre-specified primary pooled estimate (SAP A5.2): pending unless the file names the GLMM.
PRIMARY_POOLED = {"PooledLSTV", "PooledLSTVLow", "PooledLSTVHigh", "PiLSTVLow", "PiLSTVHigh", "PooledEstimator"}
WORDS = "zero one two three four five six seven eight nine".split()
QUERY_ID_RE = re.compile(r"^(pilot_)?[a-z0-9-]+_")
ANNOTATED_RE = re.compile(r"\(verify|template:|   \(")  # a markdown string with a comment attached, not a sent string


# ----------------------------------------------------------------------------- inputs
def _merge_counts(path: Path, recs: dict[str, dict]) -> None:
    """counts.json as sdr.search_* write it, {source: {..., queries: {qid: rec}}}; a source block without
    `queries` ran nothing and is skipped; a top-level key shaped like a query id is the flat legacy form."""
    for k, v in json.loads(path.read_text(encoding="utf-8")).items():
        if isinstance(v, dict) and "queries" in v:
            for qid, rec in (v.get("queries") or {}).items():
                recs.setdefault(qid, {}).update(rec if isinstance(rec, dict) else {"hit_count_api": rec})
        elif re.match(r"^[a-z0-9-]+_[a-z0-9]", k):
            recs.setdefault(k, {}).update(v if isinstance(v, dict) else {"hit_count_api": v})


def load_query_records(run_dir: Path) -> dict[str, dict]:
    """queries.json of the run, with queries/*.yaml and counts.json merged underneath and the pilot rows
    added. The printed `query_string` is the YAML's operational `string` wherever the YAML defines the
    id (the run's annotated markdown forms are not sent strings); a run string that genuinely differs
    is kept as `query_string_run`; a pilot row that only names another id is filled from the verbatim
    markdown ("as written") or marked derived. Raises on an id that is not a query id."""
    recs: dict[str, dict] = {}
    qdir, yaml_recs = ROOT / "queries", {}
    for y in sorted(qdir.glob("*.y*ml")) if qdir.exists() else []:
        yaml_recs.update(load_queries(y))
    for k, v in yaml_recs.items():
        recs[k] = {"query_string": v.get("string"), **{a: b for a, b in v.items() if a != "string"}}
    for c in (run_dir / "counts.json", qdir / "counts.json"):
        if c.exists():
            _merge_counts(c, recs)
    for q in sorted({run_dir / "queries.json", PILOT_DIR / "queries.json"}):
        if q.exists():
            for k, v in json.loads(q.read_text(encoding="utf-8")).items():
                if not k.startswith("_") and isinstance(v, dict):
                    recs.setdefault(k, {}).update(v)
    verbatim = load_queries()
    for k, r in recs.items():
        if not QUERY_ID_RE.match(k):
            raise ValueError(f"{k!r} is not a query id (source-keyed counts.json block leaked into the query records?)")
        r.setdefault("source", k.split("_")[0])
        r.setdefault("role", "search")
        # credential_mode is what the run recorded; an unrun id keeps credential_mode_expected only, and Appendix A says "not run"
        sent = str(r.get("query_string") or "")
        if (m := re.match(r"^([a-z0-9]+_\d+[a-z]?) (as written|with )", sent)) and m.group(1) in verbatim:
            if m.group(2) == "as written":
                r["query_string"] = verbatim[m.group(1)]["string"]
            else:
                r["form"], r["derived_from_query"] = "derived", m.group(1)
        elif (y := yaml_recs.get(k)) and y.get("string"):
            if sent and sent not in (y["string"], y.get("markdown_string")) and not ANNOTATED_RE.search(sent):
                r["query_string_run"] = sent
            r["query_string"] = y["string"]
    return dict(sorted(recs.items()))


def load_analyses(adir: Path) -> dict[str, Any]:
    return {n: json.loads((adir / f"{n}.json").read_text(encoding="utf-8")) if (adir / f"{n}.json").exists() else None for n in ANALYSES}


def load_charting(cdir: Path) -> list[dict]:
    return sorted((json.loads(p.read_text(encoding="utf-8")) for p in cdir.glob("*.json")), key=lambda d: d.get("id", ""))


# ----------------------------------------------------------------------------- numbers
def numbers_tex(an: dict, extra: dict[str, Any]) -> tuple[str, list[str]]:
    """The macro file: \\num<Name> and \\numword<Name> per entry; a missing value becomes \\pending.
    `extra` maps a name to an int, or to (value, kind). One rounding serves both forms, so a
    non-integer count never prints as one number and spells out another."""
    lines, pend = ["% generated by sdr.manuscript; do not edit"], []
    # The guard is keyed on the pooled block, not on a named estimator: a block that names none is exactly the case in
    # which an unattributed prevalence would otherwise print as the pre-specified primary result.
    pooled, est = dig(an.get("pooled_variants"), "LSTV.pooled"), pooled_estimator(an.get("pooled_variants"))
    entries = [(n, dig(an.get(f), p), k) for f, kinds in NUMBER_MACROS.items() for k, names in kinds.items() for n, p in names.items()]
    entries += [(n, *(v if isinstance(v, tuple) else (v, "int"))) for n, v in extra.items()]
    for name, v, kind in entries:
        assert re.fullmatch(r"[A-Za-z]+", name), name
        s = fmt(v, kind)
        if name in PRIMARY_POOLED and pooled is not None and not is_primary_estimator(est):
            s, reason = None, (f"{name}: primary GLMM (sdr.meta, SAP A5.2) not run; the file names "
                               + ("a sensitivity estimator" if est else "no estimator"))
        else:
            reason = name
        if s is None:
            pend.append(name)
            s = w = rf"\pending{{{reason}}}"
        else:
            n = int(round(float(v))) if kind == "int" else None
            s = esc(s)
            w = WORDS[n] if n is not None and 0 <= n < 10 else s
        lines += [rf"\newcommand{{\num{name}}}{{{s}}}", rf"\newcommand{{\numword{name}}}{{{w}}}"]
    return "\n".join(lines) + "\n", pend


# ----------------------------------------------------------------------------- render
def git_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True, timeout=20).stdout.strip() or "unknown"
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def render_commit(run_dir: Path, an: dict, run_date: str, dry_run: bool) -> str:
    """The commit printed in main.tex: build_info.json when sdr writes it; else the one recorded in
    <run-dir>/run_meta.json at the first render, so later renders of the same run on later commits do
    not change the text. Read only on --dry-run."""
    if c := dig(an.get("build_info"), "git_commit"):
        return str(c)
    meta_p = run_dir / "run_meta.json"
    meta = json.loads(meta_p.read_text(encoding="utf-8")) if meta_p.exists() else {"run_date": run_date, "protocol_version": PROTOCOL_VERSION, "invocations": []}
    if not meta.get("render_commit"):
        meta["render_commit"] = git_commit()
        if not dry_run and meta["render_commit"] != "unknown":
            dump_json(meta_p, meta)
    return str(meta["render_commit"])


def check(main: str, allowed: set[str]) -> list[str]:
    """Bare digits in the Abstract and Results outside macros, citations, labels, ids (P15, I3, S1, L6) and
    the allow-list; unreplaced markers; abstract length (each \\num macro counts as one word). Returns
    the problems (PROTOCOL.md section 13)."""
    probs = [f"unreplaced marker {m}" for m in sorted(set(re.findall(r"@@[A-Z_:a-z]+@@", main)))]
    ok = re.compile(r"^\W*[A-Z]{1,2}\d{1,2}\W*$|^\$.*\$\W*$")
    for name, pat in (("abstract", r"\\begin\{abstract\}(.*?)\\end\{abstract\}"), ("results", r"\\section\{Results\}(.*?)\\section\{Discussion\}")):
        if not (m := re.search(pat, main, re.S)):
            probs.append(f"{name}: section not found")
            continue
        body = re.sub(r"(?m)%.*$", "", m.group(1))
        if name == "abstract":
            words = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})?", " ", re.sub(r"\\num[A-Za-z]+(\{\})?", " N ", body)).split()
            if len(words) > 300:
                probs.append(f"abstract has about {len(words)} words (limit 300)")
        body = re.sub(r"\\(cite[tp]?|ref|label|input|includegraphics|num[A-Za-z]*|pending|tabref|figref|yearRange|url)\*?(\[[^\]]*\])?(\{[^}]*\})*", " ", body)
        probs += [f"{name}: bare digit in '{t}'" for t in sorted(set(re.findall(r"[^\s~]*\d[^\s~]*", body))) if t not in allowed and not ok.match(t)]
    return probs


def allowed_literals(mdir: Path) -> set[str]:
    """manuscript/allowed_literals.txt: one literal per line followed by its reason; # comments."""
    p = mdir / "allowed_literals.txt"
    return {ln.split()[0] for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")} if p.exists() else set()


def scan(path: Path) -> int:
    """`--scan <main.tex>`: the check() of a rendered file, for build.sh (PROTOCOL.md section 13 (c))."""
    probs = check(path.read_text(encoding="utf-8"), allowed_literals(ROOT / "manuscript"))
    print(*(f"scan: {p}" for p in probs), sep="\n") if probs else print(f"scan: {path.name} has no bare digit in Abstract or Results")
    return 1 if probs else 0


def _rel(target: Path, start: Path) -> str:
    """POSIX relative path from the directory `start` to `target`, for \\input and \\includegraphics."""
    return os.path.relpath(target, start).replace(os.sep, "/")


def render(a: argparse.Namespace) -> int:
    run_dir, mdir = resolve_run_dir(a.run_dir), ROOT / "manuscript"
    main_out = (Path(a.main_out) if Path(a.main_out).is_absolute() else ROOT / a.main_out).resolve()
    tdir, fdir = (ROOT / a.tables_dir).resolve(), (ROOT / a.figures_dir).resolve()
    if ROOT not in main_out.parents or ROOT not in tdir.parents:
        raise ValueError("main.tex and tables must be written under spine_data_review/")
    trel, frel = _rel(tdir, main_out.parent), _rel(fdir, main_out.parent)
    qs, an, ch = load_query_records(run_dir), load_analyses(ROOT / a.analysis_dir), load_charting(ROOT / a.charting_dir)
    if a.limit:
        qs, ch = dict(list(qs.items())[:a.limit]), ch[:a.limit]
    searches = {k: r for k, r in qs.items() if r.get("role") in SEARCH_ROLES and executed(r)}
    # Planned search-role ids whose request never went out: a source with no adapter in this version
    # (credential_mode not-run) or a credential-gated id that was skipped. \numQueries counts only the
    # ids that did go out, so the two numbers have to be printed together or the Methods sentence
    # silently loses thirteen planned queries and two planned sources.
    # "<" in an id is a template with a placeholder (openalex_03_<openalex_id>), not an addressable query.
    unsent = {k: r for k, r in qs.items() if r.get("role") in SEARCH_ROLES and not executed(r) and "<" not in k}
    planned, by_name = planned_sources()
    searched_keys = {source_key(k, r) for k, r in searches.items()}
    # A planned source is unsearched when no executed query carries its key -- the same test t_sources
    # uses to seed a row, so the macro and the table's "not run" rows are one set. Counting source keys
    # instead would have added O1, the citation-chasing arm, which is not a planned source.
    extra = {"SourcesPlanned": len(planned), "SourcesRun": sources_run(searches, an["flow"]), "Queries": len(searches),
             "QueriesNotSent": len(unsent),
             "SourcesNotSearched": sum(1 for pl in planned if (planned_key(pl["code"], by_name) or f"~{pl['code']}") not in searched_keys),
             "DatasetsCharted": len(ch), "DatasetsVerified": sum(1 for d in ch if d.get("verified_by"))}
    tables = {"eligibility": t_eligibility(), "items": t_data_items(), "sources": t_sources(qs, an["flow"]), "search_strings": t_search_strings(qs),
              "datasets_main": t_datasets_main(ch, an["quality"]) if ch else pending_table("datasets_main", f"no charting records in {a.charting_dir}"),
              "quality": t_quality(an["quality"]), "counts": t_counts(an["descriptives"]), "availability": t_availability(an["availability"]),
              "pooled_variants": t_pooled_variants(an["pooled_variants"]), "agreement": t_agreement(an["pooled_agreement"]), "grid": t_grid(an["grid_coverage"]),
              "deviations": t_md("deviations", "Deviations from protocol (PROTOCOL.md section 19, verbatim).", ROOT / "PROTOCOL.md", r"^## 19\. ",
                                 [0, 1, 2, 3, 4, 5, 6], (0.105, 0.12, 0.15, 0.15, 0.145, 0.12, 0.07)),
              "checklist": t_md("checklist", "PRISMA-ScR checklist with the location of each item.", ROOT / "PRISMA-ScR_checklist.md", r"^# PRISMA-ScR checklist",
                                [0, 1, 2, 3, 4], (0.05, 0.11, 0.12, 0.25, 0.34))}
    numbers, pend = numbers_tex(an, extra)
    reg = re.search(r"10\.17605/OSF\.IO/[A-Z0-9]+", (ROOT / "PROTOCOL.md").read_text(encoding="utf-8"), re.I)
    subs = {"RUN_DATE": esc(a.run_date), "PROTOCOL_VERSION": esc(PROTOCOL_VERSION), "NUMBERS": rf"\input{{{trel}/numbers.tex}}",
            "LAST_SEARCH_DATE": esc(max([str(r["run_date"]) for r in searches.values() if r.get("run_date")] or [a.run_date])),
            "GIT_COMMIT": esc(render_commit(run_dir, an, a.run_date, a.dry_run)), "PENDING_LIST": esc(", ".join(pend) if pend else "none"),
            "REGISTRATION_DOI": rf"\url{{https://doi.org/{reg.group(0)}}}" if reg else r"\pending{registration DOI}"}

    def sub(m: re.Match) -> str:
        kind, arg = m.group(1), m.group(2)
        if kind == "TABLE":
            return rf"\input{{{trel}/{arg}.tex}}" if arg in tables else rf"\pendingtable{{{arg}}}{{no such table}}"
        if kind == "FIGURE":
            present = [f for f in FIGURE_FILES.get(arg, [arg]) if (fdir / f"{f}.pdf").exists()]
            return "\n".join(rf"\includegraphics[width=\linewidth]{{{frel}/{f}.pdf}}" for f in present) if present else rf"\pendingfigure{{{arg}}}"
        return subs.get(kind, m.group(0))
    main = re.sub(r"@@([A-Z_]+)(?::([a-z_]+))?@@", sub, (mdir / "template.tex").read_text(encoding="utf-8"))
    probs = check(main, allowed_literals(mdir))
    print(f"tables: {len(tables)}; charting records: {len(ch)}; queries: {len(qs)} ({len(searches)} search, executed); pending macros: {len(pend)}"
          + (f" ({', '.join(pend[:8])}{'...' if len(pend) > 8 else ''})" if pend else ""))
    print(*(f"check: {p}" for p in probs), sep="\n") if probs else None
    if a.dry_run:
        print("dry run: would write", ", ".join(f"{a.tables_dir}/{k}.tex" for k in tables), f"{a.tables_dir}/numbers.tex, {a.main_out}")
        return 1 if (a.check and probs) else 0  # the Makefile's dry-run target reads this: a dry run is not clean because it wrote nothing
    tdir.mkdir(parents=True, exist_ok=True)
    main_out.parent.mkdir(parents=True, exist_ok=True)
    for k, body in tables.items():
        (tdir / f"{k}.tex").write_text(f"% generated by sdr.manuscript; do not edit\n{body}", encoding="utf-8", newline="\n")
    if not (a.keep_numbers and (tdir / "numbers.tex").exists()):
        (tdir / "numbers.tex").write_text(numbers, encoding="utf-8", newline="\n")
    header = (f"% generated by sdr.manuscript from template.tex; do not edit. run-dir {run_dir.relative_to(ROOT)}, run-date {a.run_date}, "
              f"analysis {a.analysis_dir}, charting {a.charting_dir}, limit {a.limit}\n% pending macros: {', '.join(pend) if pend else 'none'}\n")
    main_out.write_text(header + main, encoding="utf-8", newline="\n")
    print(f"wrote {len(tables)} tables, {a.tables_dir}/numbers.tex and {a.main_out}")
    return 1 if (a.check and probs) else 0


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["--scan"] and len(argv) == 2:
        return scan(Path(argv[1]))
    ap = add_common_args(argparse.ArgumentParser(prog="python -m sdr.manuscript", description=__doc__.split("\n")[0],
                                                 epilog="python -m sdr.manuscript --scan <main.tex>: only the bare-digit check on a rendered file (build.sh)"))
    ap.add_argument("--analysis-dir", default="analysis", help="directory of analysis/*.json (relative to spine_data_review/, or absolute)")
    ap.add_argument("--charting-dir", default="charting/datasets", help="directory of charting records (relative or absolute)")
    ap.add_argument("--tables-dir", default="tables", help="where the generated tables go (relative to spine_data_review/)")
    ap.add_argument("--figures-dir", default="figures", help="where the figures are read from (relative to spine_data_review/)")
    ap.add_argument("--main-out", default="manuscript/main.tex", help="the rendered main.tex (its directory needs refs.bib for the build)")
    ap.add_argument("--keep-numbers", action="store_true", help="do not overwrite an existing tables/numbers.tex (sdr.numbers owns it)")
    ap.add_argument("--check", action="store_true", help="exit 1 on bare digits in Abstract/Results, unreplaced markers or a long abstract")
    return render(ap.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
