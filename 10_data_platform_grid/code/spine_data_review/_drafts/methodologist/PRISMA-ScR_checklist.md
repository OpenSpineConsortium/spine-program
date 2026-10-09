# PRISMA-ScR checklist, extended to 27 items, with where each is reported

Protocol version 1.0, 2026-09-19.

PRISMA-ScR (Tricco et al., Ann Intern Med 2018) has 22 numbered items: 20 essential and two
optional (12 and 16, critical appraisal). This review pools numbers and ships code, so five
items are added from PRISMA 2020 (Page et al., BMJ 2021) that PRISMA-ScR does not carry:
registration and protocol amendments (PRISMA 2020 item 24), tabulation and visual display
methods (13c), heterogeneity exploration (13e), competing interests (26), and availability of
data, code and other materials (27). The five are marked *added*. Reporting locations use the
manuscript's section names; file paths are relative to `spine_data_review/`.

| # | Section | Item | Reporting requirement | Where reported |
|---|---|---|---|---|
| 1 | Title | Title | Identify the report as a scoping review. | Title: "… : a scoping review with programmatic access verification" |
| 2 | Abstract | Structured summary | Background, objectives, eligibility, sources, charting, results, conclusions. | Structured Abstract (≤ 300 words), every count from `results/numbers.json` |
| 3 | Introduction | Rationale | Why a scoping review; the gap (no enumeration with annotation origin, variant coverage, live availability). | Introduction ¶1–2; protocol §1 |
| 4 | Introduction | Objectives | Questions with PCC elements. | Introduction, final ¶ (RQ1–RQ5, SO1–SO4); protocol §2 |
| 5 | Methods | Protocol and registration | Protocol exists, where it can be accessed, registration number. | Methods 2.1 "Protocol and registration": OSF DOI; `protocol/` in the repository, git tag `protocol-v1.0` |
| 6 | Methods | Eligibility criteria | Characteristics used as criteria with rationale. | Methods 2.2, Table 1 (I1–I8, E1–E8); protocol §4 |
| 7 | Methods | Information sources | All sources, dates of coverage, date last searched. | Methods 2.3, Table 2 (29 sources with coverage and query date); Appendix A; `runs/<run-date>/counts.json` |
| 8 | Methods | Search | Full electronic search strategy for at least one source, such that it can be repeated. | Appendix A: verbatim string for **every** source, with endpoint, date and hit count; `information_sources.md`; `runs/<run-date>/requests.log.jsonl` |
| 9 | Methods | Selection of sources of evidence | Process: prescreen, screening, dual sample, LLM step. | Methods 2.4; Figure 1 flow; `screening/decisions.csv`, `screening/dual_sample.csv`, `screening/prescreen_sample.csv`, `screening/llm/` |
| 10 | Methods | Data charting process | Form, pilot, independent charting and verification, author contact. | Methods 2.5; `charting_schema.json`; `charting/<id>.json` |
| 11 | Methods | Data items | Variables and definitions. | Methods 2.6, Table 3 (field, definition, allowed values); protocol §4.3, §9 |
| 12 | Methods | Critical appraisal of individual sources (optional) | Rationale, instrument, process. | Methods 2.7; `quality_rubric.md`; `results/quality_scores.csv` |
| 13 | Methods | Synthesis of results | Methods of handling and summarising data. | Methods 2.8 (points to the SAP); `statistical_analysis_plan.md` |
| 13c *added* | Methods | Tabulation and visual display | Which tables and figures, and how they are generated. | Methods 2.8.1; SAP §8; `sdr/report.py` |
| 13e *added* | Methods | Heterogeneity exploration | Subgroups (modality, ascertainment) and I² for the pooled prevalences. | Methods 2.8.3; SAP §5.4 |
| 14 | Results | Selection of sources of evidence | Numbers screened, assessed, included, excluded with reasons; flow diagram. | Results 3.1; Figure 1 (PRISMA 2020 two-arm flow); `results/flow.json` |
| 15 | Results | Characteristics of sources of evidence | Characteristics of each included dataset and citations. | Results 3.2; Table 4 (one row per dataset, 11 columns); full charting in Supplement S1 (generated from `charting/`) |
| 16 | Results | Critical appraisal within sources (optional) | Per-dataset scores. | Results 3.3; Table 5; Figure 4 (score distribution by route); `results/quality_scores.csv` |
| 17 | Results | Results of individual sources of evidence | Data charted per dataset relating to the questions. | Results 3.2 and Supplement S1; annotation origin and variant labels per dataset in Table 4 |
| 18 | Results | Synthesis of results | Summaries relating to questions and objectives. | Results 3.4–3.8: counts (Tables 6–7), availability (Table 8), pooled prevalence (Figure 5 forest plots), agreement (Table 9), grid coverage (Table 10) |
| 19 | Discussion | Summary of evidence | Main results linked to questions and to the intended use. | Discussion ¶1–3 |
| 20 | Discussion | Limitations | Of the process (single screener with 10 % dual, prescreen false negatives, probe date, LLM assistance, author-maintained datasets). | Discussion "Limitations" |
| 21 | Discussion | Conclusions | Interpretation and next steps. | Discussion, final ¶ |
| 22 | Funding | Funding | Sources of funding and the funders' role. | Funding section |
| 24 *added* | Methods | Registration, protocol and amendments | Where the protocol and registration are, and every amendment with its reason. | Methods 2.1 and Table S2 (deviations log copied verbatim from protocol §17) |
| 26 *added* | Other | Competing interests | Authors' interests, including authorship of datasets under review. | Competing interests section; charting rule that own datasets are verified by another author |
| 27 *added* | Other | Availability of data, code and other materials | Where the search logs, raw responses, screening decisions, charts, scores, code and recipe are. | Data and code availability: repository URL, git commit, Zenodo DOI of the archived run; `runs/`, `screening/`, `charting/`, `results/`, `recipe/` |

## Items PRISMA-ScR includes that need a stated non-applicability

- Item 12/16 (critical appraisal) are optional in PRISMA-ScR; they are done here (protocol §10)
  and reported in full.
- PRISMA 2020 items on risk of bias in studies, certainty of evidence and reporting bias are not
  applicable to a review of datasets; this is stated in Methods 2.8 with one sentence each, so a
  reader looking for them finds the reason rather than an omission.

## Checklist maintenance

`sdr/report.py --checklist` regenerates this table with the manuscript's section numbers and
the file paths resolved, and fails the build if any "Where reported" location does not exist.
