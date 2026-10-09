# PRISMA-ScR checklist, with where each item will be reported

Protocol 1.0, 2026-09-19. Items 1–22 are the PRISMA-ScR checklist (Tricco et al., Ann Intern
Med 2018), which has 20 essential items and two optional ones (12 and 16). PRISMA-ScR does not
have 27 items; to reach the 27 requested, items 23–27 are taken from PRISMA 2020 (Page et al.,
BMJ 2021) and are marked as such. They cover protocol access, amendments, competing interests,
data/code availability and near-miss exclusions, all of which this review reports anyway.

"Where" names a manuscript section (`main.tex` label) or a generated file. Nothing in the
"Where" column is a hand-typed number.

| # | Section / topic | Item | Where reported |
|---|---|---|---|
| 1 | Title | Identify the report as a scoping review | Title: "... : a scoping review with programmatic availability probing" |
| 2 | Structured summary | Background, objectives, eligibility, sources, charting, results, conclusions | Abstract (structured; counts from `tables/numbers.tex`) |
| 3 | Rationale | Describe the rationale in the context of what is already known | Introduction, paragraph 1–2 (`sec:rationale`) |
| 4 | Objectives | Questions and objectives, with PCC elements | Introduction, `sec:objectives`; PROTOCOL.md section 2 |
| 5 | Protocol and registration | Whether a protocol exists, where it can be accessed, registration number | Methods `sec:protocol`; OSF DOI from `analysis/registration.json`; PROTOCOL.md in the repository |
| 6 | Eligibility criteria | Characteristics used as eligibility criteria, with rationale | Methods `sec:eligibility`; PROTOCOL.md section 3; `screen/prescreen_rules.yaml` |
| 7 | Information sources | All sources, date of last search | Methods `sec:sources`; Appendix A (`tables/sources.tex` from `queries.json`) |
| 8 | Search | Full electronic search strategy for at least one source, reproducible | Appendix A: verbatim string, endpoint, date, hit count for EVERY source (`tables/search_strings.tex` from `queries.json`); `information_sources.md` |
| 9 | Selection of sources of evidence | Process for selecting sources | Methods `sec:selection`; PROTOCOL.md section 8; `screen/decisions.csv` |
| 10 | Data charting process | Methods of charting, calibration, independence, verification | Methods `sec:charting`; PROTOCOL.md section 9; `charting/dataset_sources.csv` |
| 11 | Data items | List and define all variables | Methods `sec:items`; `charting_schema.json`; Supplementary Table S1 (`tables/data_items.tex` generated from the schema) |
| 12 | Critical appraisal of individual sources (optional) | Rationale and methods for appraisal | Methods `sec:appraisal`; `quality_rubric.md`; `sdr/quality.py` |
| 13 | Synthesis of results | Methods of handling and summarising data | Methods `sec:synthesis`; `statistical_analysis_plan.md` |
| 14 | Selection of sources of evidence (results) | Numbers screened, assessed, included, excluded with reasons; flow diagram | Results `sec:flow`; Figure 1 (`figures/prisma_flow.pdf` from `analysis/flow.json`); `tables/exclusions.tex` |
| 15 | Characteristics of sources of evidence | Characteristics for which data were charted, with citations | Results `sec:characteristics`; Table 1 (`tables/datasets_main.tex`); Supplementary Table S2 (full charting) |
| 16 | Critical appraisal within sources (optional) | Appraisal results | Results `sec:appraisal_results`; Table 3 (`tables/quality.tex`); Figure 4 |
| 17 | Results of individual sources of evidence | Relevant data charted for each source, related to the questions | Results `sec:individual`; Table 2 (annotation origin, variant labels, access route per dataset, `tables/datasets_annotation.tex`) |
| 18 | Synthesis of results | Summary and/or charted results as they relate to the questions | Results `sec:synthesis_results`; Figures 2–5; `tables/pooled_*.tex` |
| 19 | Summary of evidence | Main results linked to objectives, relevance to key groups | Discussion `sec:summary` |
| 20 | Limitations | Limitations of the scoping review process | Discussion `sec:limitations` (index coverage, undocumented endpoints, single-day probe, single primary reviewer) |
| 21 | Conclusions | Interpretation and implications | Discussion `sec:conclusions` |
| 22 | Funding | Sources of funding, role of funders | `sec:funding` |
| 23 (PRISMA 2020 24b) | Protocol access | Where the protocol can be accessed | `sec:protocol`; Data and code availability; PROTOCOL.md path and commit hash in `analysis/build_info.json` |
| 24 (PRISMA 2020 24c) | Protocol amendments | Amendments with reasons | Appendix C: deviations log reproduced verbatim from PROTOCOL.md section 14 |
| 25 (PRISMA 2020 26) | Competing interests | Competing interests of authors | `sec:competing`; the authors created CTSpinoPelvic1K and FluoroCap, charted by the second reviewer |
| 26 (PRISMA 2020 27) | Availability of data, code and other materials | Where charting forms, extracted data, analysis code are available | `sec:availability`; repository directory `spine_data_review/`, run directory frozen with its `requests.log.jsonl` and `raw/` cache |
| 27 (PRISMA 2020 16b) | Near-miss exclusions | Cite records that appeared to meet criteria but were excluded, with reasons | Supplementary Table S3 (`tables/near_miss.tex` from `screen/decisions.csv` where `decision=exclude` after full text) |

## Reporting rules that apply to every item

- Counts in items 2, 14, 15, 18 are LaTeX macros from `tables/numbers.tex`; `build.sh` fails on
  a bare literal.
- Items 7 and 8 are generated from `<run-dir>/queries.json`; the appendix is not edited by hand.
- Item 14's flow diagram has one row per source and reports `needs-credentials` sources as
  searched-with-zero-hits, with the reason.
- The banned p-word from the project style guide is not used anywhere; the concepts are
  "annotation origin" and "where the data came from".
