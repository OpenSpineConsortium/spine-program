# PRISMA-ScR checklist, extended to 27 items, with where each is reported

Protocol 1.0, frozen 2026-09-19 after the count-only pilot search and before the full search.

**Design statement.** This is a scoping review under PRISMA-ScR and the JBI chapter. JBI
scoping reviews map evidence and do not pool by meta-analysis; here the variant prevalence and
inter-rater statistics are reported as per-dataset tables (primary), and the pooled summaries
of SAP A5 and A6 are secondary, illustrative, and named as a departure from the JBI design in
Methods and Limitations (`PROTOCOL.md` section 3). Two further departures are stated up front:
access requests are never sent, so `request-to-authors` and `unavailable` are unrequested
outcomes; and one reviewer screens the full title/abstract set, with dual screening on a
stratified sample and on the whole description-review stage.

PRISMA-ScR (Tricco et al., Ann Intern Med 2018) has 22 numbered items: 20 essential and two
optional (12 and 16, critical appraisal). This review reports pooled summaries, registers a
protocol and ships code, so five items are added from PRISMA 2020 (Page et al., BMJ 2021) that
PRISMA-ScR does not carry: tabulation and visual display (13c), heterogeneity exploration (13e),
registration, protocol access and amendments (24a–c), competing interests (26), and
availability of data, code and other materials (27). The five are marked *added*. Near-miss
exclusions (PRISMA 2020 item 16b) are reported under item 14, which already requires
exclusions with reasons. "Where" names a manuscript section (`main.tex` label) and the file it
is generated from; nothing in that column is a hand-typed number: source counts, table and
figure numbers are macros (`\numSources`, `\tabref{…}`, `\figref{…}`) that
`python -m sdr.report --checklist` fills from `analysis/build_info.json`.

| # | Section | Item | Reporting requirement | Where reported |
|---|---|---|---|---|
| 1 | Title | Title | Identify the report as a scoping review. | Title: "…: a scoping review with programmatic access verification" |
| 2 | Abstract | Structured summary | Background, objectives, eligibility, sources, charting, results, conclusions. | Structured Abstract (≤ 300 words); every count a macro from `tables/numbers.tex` |
| 3 | Introduction | Rationale | Why a scoping review; the gap (no enumeration with annotation origin, variant coverage, live availability). | `sec:rationale`; `PROTOCOL.md` section 1 |
| 4 | Introduction | Objectives | Questions with PCC elements. | `sec:objectives` (RQ1–RQ5, SO1–SO4); `PROTOCOL.md` sections 2–3 |
| 5 | Methods | Protocol and registration | Protocol exists, where it can be accessed, registration number. | `sec:protocol`: OSF DOI read from the deviations log; registration after the count-only pilot search (`runs/pilot-2026-09-19/`) and before the full search; `PROTOCOL.md` at git tag `protocol-v1.0`, commit hash in `analysis/build_info.json` |
| 6 | Methods | Eligibility criteria | Characteristics used as criteria with rationale. | `sec:eligibility`, `\tabref{eligibility}` (I1–I8, E1–E8 with the Rationale column of `PROTOCOL.md` section 4: the 10-subject floor, the year-2000 start, CBCT inclusion); `screen/prescreen_rules.yaml` |
| 7 | Methods | Information sources | All sources, dates of coverage, date last searched. | `sec:sources`, `\tabref{sources}` (`\numSources` search sources — L1–L7, R1–R14, F1–F8, S1 — with the `coverage` column from `information_sources.md` and `queries.json`, query date; Unpaywall listed under charting tools, not as a source; excluded sources with reasons); `queries.json` |
| 8 | Methods | Search | Full electronic search strategy for at least one source, such that it can be repeated. | Appendix A: verbatim string, endpoint, date and hit count for **every** `query_id` (`tables/search_strings.tex` from `queries.json`); `information_sources.md`; `runs/<run-date>/requests.log.jsonl` |
| 9 | Methods | Selection of sources of evidence | Process: de-duplication, prescreen, screening, dual sample, LLM step, description review. | `sec:selection`; `PROTOCOL.md` section 7; `screen/decisions.csv`, `screen/dual_sample.csv`, `screen/prescreen_audit.csv`, `screen/llm/` |
| 10 | Methods | Data charting process | Form, pilot, independent charting and verification, author contact. | `sec:charting`; `charting_schema.json`; `charting/datasets/<id>.json`; `charting/dataset_sources.csv` |
| 11 | Methods | Data items | Variables and definitions. | `sec:items`, Table 3 (field, definition, allowed values, generated from the schema); `PROTOCOL.md` sections 4.3, 9 |
| 12 | Methods | Critical appraisal of individual sources (optional) | Rationale, instrument, process. | `sec:appraisal`; `quality_rubric.md`; `sdr/quality.py` |
| 13 | Methods | Synthesis of results | Methods of handling and summarising data. | `sec:synthesis`; `statistical_analysis_plan.md` |
| 13c *added* | Methods | Tabulation and visual display | Which tables and figures, and how they are generated. | `sec:synthesis`; SAP A10; `sdr/report.py` |
| 13e *added* | Methods | Heterogeneity exploration | Subgroups (modality, ascertainment, definition), I², τ², prediction intervals. | `sec:synthesis`; SAP A5.2, A5.4 |
| 14 | Results | Selection of sources of evidence | Numbers screened, assessed, included, excluded with reasons; flow diagram; near-miss exclusions cited. | `sec:flow`; `\figref{flow}` (`figures/prisma_flow.pdf` from `analysis/flow.json`, totals only; per-source rows in `\tabref{sources}`); `tables/exclusions.tex` by `primary_code`; Supplement S2 (`tables/near_miss.tex` from `screen/decisions.csv`, stage full-text, decision exclude) |
| 15 | Results | Characteristics of sources of evidence | Characteristics of each included dataset and citations. | `sec:characteristics`; `\tabref{datasets_main}` (`tables/datasets_main.tex`); Supplement S1 (full charting rendered) |
| 16 | Results | Critical appraisal within sources (optional) | Per-dataset scores. | `sec:appraisal_results`; `\tabref{quality}` (`tables/quality.tex`); `\figref{quality}`; reliability from SAP A4.5 |
| 17 | Results | Results of individual sources of evidence | Data charted per dataset relating to the questions. | `sec:individual`; `\tabref{datasets_main}` and `tables/datasets_annotation.tex` (annotation origin, variant labels, access route per dataset) |
| 18 | Results | Synthesis of results | Summaries relating to questions and objectives. | `sec:synthesis_results`: counts (`\tabref{counts}`, `\tabref{totals}`), availability (`\tabref{availability}`, `\figref{availability}`), per-dataset prevalence with the illustrative pooled summary (`\figref{variants}`, `tables/pooled_variants.tex`), agreement (`\tabref{agreement}`), grid coverage (`\tabref{grid}`, labelled author-specific) |
| 19 | Discussion | Summary of evidence | Main results linked to questions and to the intended use. | `sec:summary` |
| 20 | Discussion | Limitations | Of the process: the pooled summaries are not part of the JBI scoping design (secondary, illustrative); access requests are never sent, so `request-to-authors` and `unavailable` are unrequested outcomes measured on two days; single primary screener with a stratified dual sample and full dual description review (a stated departure from JBI); prescreen false negatives per audit stratum; probe dates; undocumented endpoints and html fallbacks; LLM assistance; author-maintained datasets; SO4 not reproducible by a second team; withheld raw caches; index coverage (SAP A9). | `sec:limitations`; `PROTOCOL.md` section 16 standing limitations |
| 21 | Discussion | Conclusions | Interpretation and next steps. | `sec:conclusions` |
| 22 | Funding | Funding | Sources of funding and the funders' role. | `sec:funding` |
| 24 *added* | Methods | Registration, protocol access and amendments | Where the protocol and registration are; every amendment with its reason. | `sec:protocol`; Appendix B (deviations log copied verbatim from `PROTOCOL.md` section 19) |
| 26 *added* | Other | Competing interests | Authors' interests, including authorship of datasets under review. | `sec:competing`; the rule that own datasets (CTSpinoPelvic1K, FluoroCap) are charted, verified and scored by another author |
| 27 *added* | Other | Availability of data, code and other materials | Where the search logs, raw responses, screening decisions, charts, scores, code and recipe are. | `sec:availability`: repository directory `spine_data_review/`, git commit, Zenodo DOI of the archived run; `runs/`, `screen/`, `charting/`, `analysis/`, `tables/`, `recipe/` |

## Items that need a stated non-applicability

- Items 12 and 16 are optional in PRISMA-ScR; they are done here (protocol section 11) and
  reported in full.
- PRISMA 2020 items on risk of bias in studies, certainty of evidence and reporting bias are
  not applicable to a review of datasets; this is stated in `sec:synthesis` with one sentence
  each, so a reader looking for them finds the reason rather than an omission.

## Reporting rules that apply to every item

- Counts in items 2, 14, 15 and 18 are macros from `tables/numbers.tex`; `build.sh` fails on
  any bare digit in the Abstract or Results outside a macro, citation, label or the allow-list.
- Items 7 and 8 are generated from `<run-dir>/queries.json` (with the pilot record's rows
  marked "pilot" and the chase keys collapsed to one row); the appendix is not edited by hand.
- Item 14's flow diagram carries totals; the per-source rows, including `needs-credentials`,
  `html-fallback`, `no-public-api` and `retired` sources with their hits and the reason, are
  in the sources table.
- Table and figure numbers in this file are `\tabref`/`\figref` macros resolved by
  `python -m sdr.report --checklist` from `analysis/build_info.json`; none is typed.
- The p-word banned by the project style guide is not used anywhere; the concepts are
  "annotation origin" and "where the data came from".

## Checklist maintenance

`python -m sdr.report --checklist` regenerates this table with the manuscript's section
numbers and file paths resolved, and fails the build if any "Where reported" location does not
exist.
