"""Hand-calculated fixture for sdr.manuscript: formatting, macro generation, table aggregation, the
bare-digit check and the counts.json shape. Every expected value below was computed by hand and is
written next to the rule it tests. Writes only under tests/_out/. Run in WSL:
  ~/sdr_venv/bin/python tests/test_manuscript_fixture.py
Exit 1 on any failed assertion; each failure is printed with the observed value.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sdr import manuscript as M  # noqa: E402
from sdr.manuscript_tables import code_sort_key  # noqa: E402

OUT = ROOT / "tests" / "_out" / "manuscript_fixture"
FAILS: list[str] = []


def eq(name: str, got, want) -> None:
    if got != want:
        FAILS.append(f"{name}: got {got!r}, want {want!r}")


def dump(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=1, sort_keys=True), encoding="utf-8")


# ---------------------------------------------------------------- 1. fmt / numbers (hand values)
eq("int 1234.0 -> thousands", M.fmt(1234.0, "int"), "1,234")
eq("int bool ignored", M.fmt(True, "int"), None)
eq("pct proportion 2/3 -> 66.7%", M.fmt(2 / 3, "pct"), "66.7%")
eq("pct 0.125 -> 12.5%", M.fmt(0.125, "pct"), "12.5%")
eq("pct 0.1235 half-even -> 12.4% (12.35 -> 12.4)", M.fmt(0.1235, "pct"), "12.4%")
# 0.1245 * 100 = 12.450000000000001 in binary floating point, so Decimal(str(...)) is above the half and
# rounds UP to 12.5; a true half-to-even rule on 12.45 would give 12.4. This records what the code does.
print("fmt(0.1245,'pct') =", M.fmt(0.1245, "pct"), "(half-even on the exact decimal would be 12.4%)")
eq("pct 1.0 -> 100.0%", M.fmt(1.0, "pct"), "100.0%")
eq("pct 45.0 (already a percentage) -> 45.0%", M.fmt(45.0, "pct"), "45.0%")
eq("p 0.0004 -> <0.001", M.fmt(0.0004, "p"), "<0.001")
eq("p 0.0234 -> 0.023", M.fmt(0.0234, "p"), "0.023")
eq("dec 3.14159 -> 3.14", M.fmt(3.14159, "dec"), "3.14")
eq("dig envelope", M.dig({"a": {"value": {"b": [10, {"value": 7}]}}}, "a.b.1"), 7)
eq("dig missing", M.dig({"a": 1}, "a.b"), None)
eq("dig literal value key beside ci ({value, ci} is a block, not an envelope)", M.dig({"k": {"value": 0.8, "ci": [0.7, 0.9]}}, "k.ci.1"), 0.9)
eq("dig literal value key read as itself", M.dig({"k": {"value": 0.8, "ci": [0.7, 0.9]}}, "k.value"), 0.8)

tex, pend = M.numbers_tex({"flow": {"search_arm": {"identified": {"value": 7, "derived_from": [], "rule": "x"}}}}, {"Extra": 12})
eq("numword 7 -> seven", re.search(r"\\newcommand\{\\numwordIdentified\}\{(.*?)\}", tex).group(1), "seven")
eq("num 7 -> 7", re.search(r"\\newcommand\{\\numIdentified\}\{(.*?)\}", tex).group(1), "7")
eq("numword 12 -> 12", re.search(r"\\newcommand\{\\numwordExtra\}\{(.*?)\}", tex).group(1), "12")
eq("pending includes AfterMerge", "AfterMerge" in pend, True)
eq("pending macro form", r"\newcommand{\numAfterMerge}{\pending{AfterMerge}}" in tex, True)
tex2, _ = M.numbers_tex({"flow": {"search_arm": {"identified": 9.7}}}, {})
eq("9.7 rounds once: num 10", re.search(r"\\newcommand\{\\numIdentified\}\{(.*?)\}", tex2).group(1), "10")
eq("9.7 rounds once: numword 10 (not 'nine')", re.search(r"\\newcommand\{\\numwordIdentified\}\{(.*?)\}", tex2).group(1), "10")
tex3, _ = M.numbers_tex({"flow": {"search_arm": {"identified": 8.5}}}, {"Est": ("DL, logit", "text")})
eq("8.5 half-even -> 8 / eight", re.search(r"\\newcommand\{\\numwordIdentified\}\{(.*?)\}", tex3).group(1), "eight")
eq("extra text macro", re.search(r"\\newcommand\{\\numEst\}\{(.*?)\}", tex3).group(1), "DL, logit")
# SAP A5.2: the pooled LSTV macros stay pending while the file names DL, and render once it names the GLMM
pv_dl = {"LSTV": {"k_eligible": 6, "pooled": {"estimate": 0.12, "ci_low": 0.1, "ci_high": 0.15, "pi_low": 0.05, "pi_high": 0.25,
                                             "estimator": "DerSimonian-Laird, logit scale (SAP A5.3a)"}}}
tex4, pend4 = M.numbers_tex({"pooled_variants": pv_dl}, {})
eq("DL estimator -> PooledLSTV pending with reason", r"\newcommand{\numPooledLSTV}{\pending{PooledLSTV: primary GLMM" in tex4, True)
eq("DL estimator -> PooledEstimator pending", "PooledEstimator" in pend4, True)
eq("DL estimator -> PoolableLSTV still printed (6)", r"\newcommand{\numPoolableLSTV}{6}" in tex4, True)
# A pooled block that names no estimator at all is the same failure with the attribution missing, so it is
# pending too: the guard is keyed on the pooled block, not on a named estimator.
pv_none = {"LSTV": {"k_eligible": 6, "pooled": {k: v for k, v in pv_dl["LSTV"]["pooled"].items() if k != "estimator"}}}
tex_n, pend_n = M.numbers_tex({"pooled_variants": pv_none}, {})
eq("unattributed pooled estimate -> PooledLSTV pending, not 12.0%", r"\newcommand{\numPooledLSTV}{12.0\%}" in tex_n, False)
eq("unattributed pooled estimate -> reason says the file names no estimator",
   r"\newcommand{\numPooledLSTV}{\pending{PooledLSTV: primary GLMM (sdr.meta, SAP A5.2) not run; the file names no estimator}}" in tex_n, True)
eq("unattributed pooled estimate -> every primary pooled macro pending", sorted(p for p in pend_n if p in M.PRIMARY_POOLED),
   sorted(M.PRIMARY_POOLED))
tex_k, pend_k = M.numbers_tex({"pooled_variants": {"LSTV": {"k_eligible": 3, "pooled": None}}}, {})
eq("nothing pooled (k < 5) -> plain pending, no estimator reason", r"\newcommand{\numPooledLSTV}{\pending{PooledLSTV}}" in tex_k, True)
pv_glmm = {"LSTV": {"k_eligible": 6, "pooled": dict(pv_dl["LSTV"]["pooled"], estimator="logit random-intercept GLMM, adaptive Gauss-Hermite (SAP A5.2)")}}
tex5, pend5 = M.numbers_tex({"pooled_variants": pv_glmm}, {})
eq("GLMM estimator -> PooledLSTV 12.0%", r"\newcommand{\numPooledLSTV}{12.0\%}" in tex5, True)
eq("GLMM estimator -> nothing pooled pending", [p for p in pend5 if "Pooled" in p or "PiLSTV" in p], [])

# ---------------------------------------------------------------- 2. esc / tt
eq("esc specials", M.esc("a_b&c%d"), r"a\_b\&c\%d")
eq("esc CJK -> code point", M.esc("脊椎"), "[U+810A][U+690E]")
eq("esc unicode arrows", M.esc("a → b"), r"a $\rightarrow$ b")

# ---------------------------------------------------------------- 3. t_sources aggregation by hand
qs = {"pubmed_01": {"source": "pubmed", "role": "search", "hit_count_api": 10, "n_retrieved": 3, "credential_mode": "keyed",
                    "run_date": "2026-09-19", "coverage": "1946-"},
      "pubmed_02": {"source": "pubmed", "role": "search", "hit_count_api": 15, "n_retrieved": 4, "credential_mode": "keyed",
                    "run_date": "2026-09-18", "cap_hit": True},
      "zenodo_01": {"source": "zenodo", "role": "enrich", "hit_count_api": 99},
      "openalex_03_x": {"source": "openalex", "role": "chase", "hit_count_api": 5, "n_retrieved": 5, "source_name": "OpenAlex works API", "source_code": "L3"},
      "openalex_03_<openalex_id>": {"source": "openalex", "role": "chase", "form": "template", "source_name": "OpenAlex works API", "source_code": "L3"},
      "openi_01": {"source": "openi", "role": "search", "form": "grid"},  # never executed: no run date, no timestamp, no total
      "openi_01_c": {"source": "openi", "role": "search", "hit_count_api": 4, "n_retrieved": 1, "run_date": "2026-09-19"}}
t = M.t_sources(qs)
cells = lambda r: [c.strip() for c in r.rstrip(" \\").split("&")]  # noqa: E731
row = next(r for r in t.splitlines() if "PubMed" in r)
eq("sources row: PubMed name, coverage, credential mode", cells(row)[1:4], ["PubMed", "1946-", "keyed"])
eq("sources row: PubMed 2 queries", cells(row)[5], "2")
eq("sources row: PubMed 25 hits with the cap star, 7 fetched, 7 retrieved, identified -- without flow",
   cells(row)[-4:], ["25*", "7", "7", "--"])
eq("sources: enrich role excluded (Zenodo is planned, so its row is 'not run', not a count of the enrich query)",
   [c for c in cells(next(r for r in t.splitlines() if "Zenodo" in r)) if c == "99"], [])
chase_row = next(r for r in t.splitlines() if "citation chasing" in r)
eq("sources: chase is its own row O1, blank date", cells(chase_row)[:5], ["O1", "OpenAlex citation chasing", "unknown", "unknown", ""])
eq("sources: chase counts 1 executed query, the template skipped", cells(chase_row)[5], "1")
eq("sources: chase 5 hits, 5 fetched, 5 retrieved, identified --", cells(chase_row)[-4:], ["5", "5", "5", "--"])
eq("sources: the executed OpenAlex arm is the chase row; L3 itself printed as planned-but-not-run",
   [cells(r)[0] for r in t.splitlines() if "OpenAlex" in r and r.rstrip().endswith("\\\\")], ["L3", "O1"])
openi_row = next(r for r in t.splitlines() if "Open-i" in r)
eq("sources: Open-i grid head not counted, its executed sub-id is", [cells(openi_row)[5]] + cells(openi_row)[-4:], ["1", "4", "1", "1", "--"])
eq("sources: run date never substituted for a blank date", "2026-09-19" in chase_row, False)
t_flow = M.t_sources(qs, {"per_source": {"value": {"pubmed": {"n_identified": 6, "n_retrieved": 9}, "openi": {"n_identified": 1}}}})
eq("sources: Identified column from flow.json per_source", cells(next(r for r in t_flow.splitlines() if "PubMed" in r))[-1], "6")
eq("sources: Retrieved column also from flow.json where it has one (9, not the query sum 7)",
   cells(next(r for r in t_flow.splitlines() if "PubMed" in r))[-2], "9")
eq("sources: Retrieved and Identified are adjacent, so the reader compares two numbers from one file",
   cells(next(r for r in t_flow.splitlines() if "PubMed" in r))[-2:], ["9", "6"])
eq("sources: overlap stated in the note", "queries overlap" in t_flow, True)
eq("sources: a flow that identifies more than it retrieved is warned about, not printed in silence",
   "WARNING, inconsistent upstream counts" in M.t_sources(qs, {"per_source": {"pubmed": {"n_identified": 99, "n_retrieved": 7}}}), True)

# \numSourcesRun says "returned records": a source that reported a total and retrieved nothing does not count,
# and a source whose adapter reports no total but retrieved records does. One of these two counts, so the answer is 1.
sr = {"dryad_01": {"source": "dryad", "role": "search", "hit_count_api": 40, "n_retrieved": 0, "run_date": "2026-09-19"},
      "figshare_01": {"source": "figshare", "role": "search", "n_retrieved": 10, "run_date": "2026-09-19"}}
eq("SourcesRun counts records returned, not totals reported", M.sources_run(sr), 1)
eq("SourcesRun reads the flow's n_retrieved where the flow has one (dryad 3 in, figshare 0 out: still 1)",
   M.sources_run(sr, {"per_source": {"dryad": {"n_retrieved": 3}, "figshare": {"n_retrieved": 0}}}), 1)

# Table 2's rows and \numSourcesPlanned are one set: every planned code has a row, a planned source that never ran
# says so, and the codes run in natural order (R2 directly after R1, R10 after R9).
codes = [cells(r)[0] for r in t.splitlines() if r.rstrip().endswith("\\\\") and re.fullmatch(r"[A-Z]+\d+[a-z]?", cells(r)[0])]
planned, _ = M.planned_sources()
eq("Table 2 has a row for every planned source", [p["code"] for p in planned if p["code"] not in codes], [])
eq("Table 2 codes are in natural order", codes, sorted(codes, key=code_sort_key))
zen = next(r for r in t.splitlines() if "Zenodo" in r)
eq("sources: a planned source with no executed query is a 'not run' row, not a silent absence",
   [cells(zen)[3]] + cells(zen)[-5:], ["not run", "--", "--", "--", "--", "--"])
eq("sources: the note states the SourcesRun rule and the planned denominator",
   "Sources returning at least one record (Retrieved $>$ 0): 3 of %d planned." % len(planned) in t, True)

# ---------------------------------------------------------------- 4. t_availability CI string by hand
av = {"route_distribution": {"overall": {"value": {"open-download": 2, "unavailable": 1}}},
      "described_public_downloads": {"primary": {"numerator": 2, "denominator": 3, "proportion": 2 / 3, "ci": [0.2077, 0.9385]}}}
t = M.t_availability(av)
eq("availability: 66.7% (20.8% to 93.8%)", "66.7\\% (20.8\\% to 93.8\\%)" in t, True)
eq("availability: open-download 2", "open-download & 2" in t, True)

# ---------------------------------------------------------------- 5. check(): bare digits
doc = (r"\begin{abstract} We found \numDatasets{} datasets and 12 films; L6 and P15 are ids; \cite{a2021b} \end{abstract}"
       r"\section{Results} n = 3 here. \section{Discussion} 99 typed here is allowed.")
probs = M.check(doc, set())
eq("check: '12' flagged in abstract", any("abstract: bare digit in '12'" in p for p in probs), True)
eq("check: '3' flagged in results", any("results: bare digit in '3'" in p for p in probs), True)
eq("check: L6 / P15 / cite / macro not flagged", any(x in " ".join(probs) for x in ("L6", "P15", "a2021b", "numDatasets")), False)
eq("check: discussion digit not scanned", any("99" in p for p in probs), False)
eq("check: unreplaced marker", M.check("@@TABLE:foo@@ \\begin{abstract}\\end{abstract}\\section{Results}\\section{Discussion}", set())[0],
   "unreplaced marker @@TABLE:foo@@")

# ---------------------------------------------------------------- 6. counts.json shape: source-keyed top level (as sdr.search_* write it)
shutil.rmtree(OUT, ignore_errors=True)
run = OUT / "run"
dump(run / "queries.json", {"fx_01": {"source": "pubmed", "role": "search", "query_string": "spine AND dataset", "hit_count_api": 3,
                                      "n_retrieved": 3, "run_date": "2026-09-19", "credential_mode": "keyed"}})
dump(run / "counts.json", {"pubmedfixture": {"n_items": 3, "n_records_after_within_source_dedup": 3,
                                             "queries": {"fx_01": {"hit_count_api": 3, "n_retrieved": 3}}}})
recs = M.load_query_records(run)
eq("counts.json source key does not become a query record", "pubmedfixture" in recs, False)
eq("counts.json queries{} merged under the query id", recs["fx_01"].get("n_retrieved"), 3)
eq("every loaded id is a query id", [k for k in recs if not re.match(r"^(pilot_)?[a-z0-9-]+_", k)], [])
dump(run / "counts.json", {"fx_01": {"hit_count_api": 3}, "fx_02": 9, "arxiv": {"n_items": 0}})  # legacy flat form; an empty source block is skipped
recs2 = M.load_query_records(run)
eq("legacy flat counts.json: bare count becomes hit_count_api", recs2["fx_02"].get("hit_count_api"), 9)
eq("legacy flat counts.json: empty source block skipped", "arxiv" in recs2, False)
dump(run / "queries.json", {"fx_01": {"source": "pubmed", "role": "search"}, "pubmed": {"role": "search"}})
try:
    M.load_query_records(run)
    FAILS.append("a non-query id in queries.json did not raise")
except ValueError as e:
    eq("non-query id raises and names it", "'pubmed'" in str(e), True)
dump(run / "queries.json", {"fx_01": {"source": "pubmed", "role": "search", "query_string": "spine AND dataset", "hit_count_api": 3,
                                      "n_retrieved": 3, "run_date": "2026-09-19", "credential_mode": "keyed"}})
dump(run / "counts.json", {"pubmedfixture": {"n_items": 3, "n_records_after_within_source_dedup": 3,
                                             "queries": {"fx_01": {"hit_count_api": 3, "n_retrieved": 3}}}})

# ---------------------------------------------------------------- 7. end-to-end render on a tiny analysis + charting fixture
an = OUT / "analysis"
dump(an / "flow.json", {"search_arm": {"identified": {"value": 120, "derived_from": [], "rule": "r"}, "after_merge": 100, "screened": 90,
                                       "sought_for_full_text": 20, "included_records": 8}, "other_arm": {"included_records": 2, "known_items": 30},
                        "datasets": {"total": 7, "derived": 1, "figure_derived": 1}})
dump(an / "descriptives.json", {"by_modality": {"CT": {"n_datasets": 4, "n_subjects_sum": 1500, "n_subjects_median": 300.0, "n_images_sum": None},
                                                "radiograph": {"n_datasets": 3, "n_subjects_sum": 2500, "n_subjects_median": 800, "n_images_sum": 9000}},
                                "totals": {"n_subjects_sum": 4000}})
dump(an / "availability.json", av)
dump(an / "quality.json", {"per_dataset": {"ds_a": {"items": {f"Q{k}": {"score": 2, "rule": "x"} for k in range(1, 11)}, "total": 20,
                                                    "fit_level_id": True, "fit_stitching": False}},
                           "summary": {"total": {"median": 12.5, "q1": 9.0, "q3": 15.0}}})
ch = OUT / "charting"
dump(ch / "ds_a.json", {"id": "ds_a", "name": "Fixture A", "year": 2021, "country": ["US"], "modality": ["CT"], "region": ["lumbar"],
                        "n_subjects": 1234, "annotation_types": ["per-vertebra-level-names"], "annotation_origin": ["expert-manual"],
                        "variant_labels": {"L6": {"status": "yes"}, "T13": {"status": "unknown"}, "LSTV": {"status": "no"}},
                        "licence": {"tier": "open"}, "access_route": "open-download", "verified_by": "x"})
rc = M.main(["--run-dir", str(run), "--run-date", "2026-09-19", "--analysis-dir", str(an), "--charting-dir", str(ch),
             "--tables-dir", "tests/_out/manuscript_fixture/tables", "--figures-dir", "tests/_out/manuscript_fixture/figures",
             "--main-out", "tests/_out/manuscript_fixture/manuscript/main.tex", "--check"])
eq("render rc (check passes on the template)", rc, 0)
num = (OUT / "tables" / "numbers.tex").read_text(encoding="utf-8")
eq("numIdentified 120", r"\newcommand{\numIdentified}{120}" in num, True)
eq("numwordDatasets seven", r"\newcommand{\numwordDatasets}{seven}" in num, True)
eq("numDatasetsCT 4 / numword four", r"\newcommand{\numwordDatasetsCT}{four}" in num, True)
eq("numPctDescribedPublicDownloads 66.7%", r"\newcommand{\numPctDescribedPublicDownloads}{66.7\%}" in num, True)
eq("numQualityMedian 12.50", r"\newcommand{\numQualityMedian}{12.50}" in num, True)
eq("numSubjectsTotal 4,000", r"\newcommand{\numSubjectsTotal}{4,000}" in num, True)
eq("numDatasetsCharted 1", r"\newcommand{\numDatasetsCharted}{1}" in num, True)
main_tex = (OUT / "manuscript" / "main.tex").read_text(encoding="utf-8")
eq("no marker left", re.findall(r"@@[A-Z_:a-z]+@@", main_tex), [])
eq("relative input path from manuscript/ to tables/", r"\input{../tables/numbers.tex}" in main_tex, True)
dm = (OUT / "tables" / "datasets_main.tex").read_text(encoding="utf-8")
eq("datasets_main: variants YN? and 1,234 subjects and Q 20", all(s in dm for s in ["Y?N", "1,234", "& 20 &", "& yes"]), True)
cn = (OUT / "tables" / "counts.tex").read_text(encoding="utf-8")
print("counts.tex CT row:", next((r for r in cn.splitlines() if "CT" in r), None))
q = (OUT / "tables" / "quality.tex").read_text(encoding="utf-8")
eq("quality: per-item scores from {score, rule}", "ds\\_a} & 2 & 2 & 2" in q.replace("\\allowbreak{}", ""), True)
eq("quality: reliability note is a pending marker while quality.json has no reliability block",
   "\\noindent{\\footnotesize \\pending{Rubric reliability" in q, True)
eq("numICCTotal pending without the reliability block", r"\newcommand{\numICCTotal}{\pending{ICCTotal}}" in num, True)
rel = M.t_quality({"per_dataset": {"ds_a": {"items": {}, "total": 1}}, "reliability": {"n": 25, "icc_total": {"value": 0.8123, "ci": [0.7, 0.9]},
                                                                                        "per_item_kappa": {"Q1": 0.5, "Q2": "not estimable"}}})
eq("quality: reliability note from the block (n, ICC, CI, per-item kappa)",
   all(s in rel for s in ["(n = 25)", "ICC(2,1) on the total 0.81 (0.70 to 0.90)", "Q1 0.50", "Q2 not estimable", "Q3 --"]), True)
pvt = (OUT / "tables" / "pooled_variants.tex").read_text(encoding="utf-8") if (OUT / "tables" / "pooled_variants.tex").exists() else ""
eq("pooled_variants table pending in the fixture (no file)", "\\pendingtable{pooled_variants}" in pvt, True)
pv_tex = M.t_pooled_variants({"value": {"LSTV": {"k_eligible": 6, "per_dataset": [], "pooled": pv_dl["LSTV"]["pooled"]},
                                        "L6": {"k_eligible": 0, "pooled": None}, "T13": {"k_eligible": 0, "pooled": None},
                                        "estimator_note": "DL is the sensitivity estimator"}})
eq("pooled row names the estimator and flags it as sensitivity", "DerSimonian-Laird, logit scale (SAP A5.3a); sensitivity estimator, primary GLMM (SAP A5.2) pending (k = 6)" in pv_tex, True)
eq("pooled table note carries the file's estimator note", "Estimator note recorded in the analysis file: DL is the sensitivity estimator" in pv_tex, True)
mt = M.check(r"\begin{abstract} " + " ".join([r"\numX{}"] * 301) + r" \end{abstract}\section{Results}\section{Discussion}", set())
eq("check: every \\num macro counts as one abstract word", any("abstract has about 301 words" in p for p in mt), True)
items_tex = (OUT / "tables" / "items.tex").read_text(encoding="utf-8")
eq("items: underscores in prose cells are breakable", "states\\_\\allowbreak{}file" in items_tex.replace("\\_\\allowbreak{}", "\\_\\allowbreak{}"), True)
ss = (OUT / "tables" / "search_strings.tex").read_text(encoding="utf-8")
eq("appendix: no '(no string recorded)' block", ss.count("(no string recorded)"), 0)
eq("appendix: markdown form printed beside the YAML string where it differs", "as written in information\\_sources.md:" in ss, True)
eq("appendix: pilot 'as written' row carries the verbatim epmc_01 string", "TITLE:" in ss.split("pilot\\_\\allowbreak{}epmc\\_\\allowbreak{}fielded")[1][:3000], True)
eq("appendix: pilot unfielded row is marked derived", "derived from \\texttt{epmc\\_\\allowbreak{}01}" in ss, True)
eq("appendix: chase block says no request ran", "no request recorded in this run" in ss, True)
meta_p = run / "run_meta.json"
eq("render commit recorded once in run_meta.json", json.loads(meta_p.read_text(encoding="utf-8")).get("render_commit") not in (None, "", "unknown"), True)
eq("main.tex carries the recorded commit", json.loads(meta_p.read_text(encoding="utf-8"))["render_commit"] in main_tex, True)

# --limit 1 must be deterministic and keep the first sorted query only
rc2 = M.main(["--run-dir", str(run), "--run-date", "2026-09-19", "--analysis-dir", str(an), "--charting-dir", str(ch), "--limit", "1",
              "--tables-dir", "tests/_out/manuscript_fixture/tables_l1", "--figures-dir", "tests/_out/manuscript_fixture/figures",
              "--main-out", "tests/_out/manuscript_fixture/manuscript_l1/main.tex"])
eq("limit run rc", rc2, 0)

print("\n".join(FAILS) if FAILS else "ALL FIXTURE ASSERTIONS PASSED")
sys.exit(1 if FAILS else 0)
