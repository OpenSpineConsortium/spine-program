# spine_data_review

A protocol-driven scoping review (PRISMA-ScR, JBI structure, Cochrane-style search reporting) of
publicly described datasets of human spine imaging in CT and projection radiography (plain
radiograph, fluoroscopy, DXA vertebral fracture assessment, EOS), with or without annotations.
It asks what exists, how each dataset is annotated and where the annotations came from, whether
variant anatomy (L6, T13, lumbosacral transitional vertebra) is labelled, under what licence, and
whether it can be obtained today, the last established by code on two dates. Second to that it
scores each dataset on a predefined rubric, pools what can be pooled, and generates a download
recipe for everything that downloads.

The review exists because the authors' level-identification project kept discovering datasets
late, and no published enumeration states annotation origin, variant coverage and live
availability. Whole-spine radiographs and thoracic images are the scarcest and the most valuable
to it.

Everything a person decided is in `PROTOCOL.md` and its companions, frozen before the search:
`information_sources.md` (every verbatim query string), `charting_schema.json`,
`quality_rubric.md`, `statistical_analysis_plan.md`, `PRISMA-ScR_checklist.md`,
`licence_tiers.csv`, `screen/known_items.csv`, `grid_inventory.csv`. Everything else is produced
by `sdr/` from those files, and every number in the manuscript is generated into
`analysis/*.json` and `tables/numbers.tex`; none is typed.

## Reproduce

Once, on the WSL host (the network stages must run there; `PROTOCOL.md` section 15):

```
python3.12 -m venv ~/sdr_venv && ~/sdr_venv/bin/pip install -r requirements.txt
# credentials, by name only, in ~/.fluorocap/credentials.env (KEY=value lines, chmod 600):
# NCBI_API_KEY, S2_API_KEY, FLUOROCAP_CONTACT_EMAIL, SPRINGER_API_META_KEY; optional HF_TOKEN,
# GITHUB_TOKEN, OSF_TOKEN, ~/.kaggle/kaggle.json.
```

Every route degrades to credential-free without its key and says so: `make protocol-check` prints
the names present (never a value) at the start of every run and probes each keyed service once,
`run_meta.json` records the names, and each entry of `queries.json` records its `credential_mode`
(a Semantic Scholar run without `S2_API_KEY` paces at one request per five seconds instead of one
per second; the appendix table reports the mode per source). The reproduction is therefore the
same command with or without keys; only the pace and the recorded mode differ.

Then one command, from Git Bash on Windows (it hands over to WSL) or from a WSL shell:

```
bash run_all.sh --run-date 2026-09-21
```

which is `make all RUN_DATE=2026-09-21` in this directory: protocol-check → search → check-run →
dedup → chart-check → availability → quality → stats → figures → manuscript → recipe, into
`runs/2026-09-21/` and the output directories. `RUN_DATE` is required by every stage and is the
only date written into outputs; there is no wall-clock default. `make smoke RUN_DATE=...` runs
the same chain with `--limit 5` into `runs/smoke/` and touches nothing under `charting/`,
`analysis/`, `tables/`, `figures/`, `manuscript/` or `recipe/`. Any `LIMIT` run writes the two
outputs of `chart-check` under its run directory (`<run>/charting/`), because `sdr.chart` slices
by `--limit` and would otherwise truncate the committed `charting/datasets.jsonl` to the first N
records, and caps HTTP attempts at two (`SDR_MAX_ATTEMPTS`) so a source that times out costs
seconds. `make <stage>` runs one stage, `make <stage> REPLAY=1` serves it from the run's own
`raw/` cache (`--replay`, offline, fails on a miss), and `make help` lists the variables.
`run_all.sh --replay` passes the same switch through. `PIPELINE.md` states what each stage reads
and writes.

`check-run` (`tests/check_run.py`) audits the run directory after the search: log fields and
redaction, log against raw cache, no credential value anywhere, the verbatim-string rule, a source
that did not answer saying so in its notes rather than reading as zero records, and wall-clock
dates. All six are fatal; `paging` is printed only, because a source that reports a total it does
not serve is the source's behaviour, not the run's. Two defaults follow `LIMIT` instead of the
smoke target: `MANUSCRIPT_FLAGS` is `--strict` on an unlimited run, so the real run's manuscript
build fails on a pending or unused macro (`PROTOCOL.md` 13(b)), and `STATS_FLAGS` is `--check-flow`,
so a PRISMA flow identity that does not hold stops the run before the manuscript prints it. A
`LIMIT` run clears both, because a limited search cannot satisfy either and would otherwise die one
stage short of `recipe`. `manuscript/allowed_literals.txt`
carries the bare literals the 13(c) digit rule allows, one reason per line, and `build.sh` runs that
rule itself (`python -m sdr.manuscript --scan main.tex`).

Two stages need a person between them: after `dedup`, screening decisions go into
`data/screening/decisions.csv` and charting records into `charting/datasets/<id>.json`
(`data/charting/README.md`); `availability` is run twice at least 48 hours apart, the second time
with `AVAIL_FLAGS=--apply`. A run is replayable offline from its own cache (`--replay`: every
request is cached, a failed one with its `error`, so a replay reproduces what the run observed), and
a rerun on the same records is byte-identical. `make replay-check RUN_DIR=<run> RUN_DATE=...` checks
exactly that: it replays the run from its own `raw/` into `<run>-replay` with no network and diffs
the two (`tests/diff_runs.py` compares records, queries and counts of two runs; `tests/diff_run_dirs.py`
compares whole chains through the recipe).

## Layout

```
sdr/            the code: common (HTTP with limits, log, cache; run dir; JSONL), creds, ids,
                search_literature, the four repository modules (repo_run, the shared Run state;
                search_repositories R1-R8; search_platforms R9-R14; search_figure_routes F1,
                F4-F8 and the mention harvests), dedup_prescreen, chart, availability, quality,
                the four analysis modules (descriptives, estimators, flow_counts, stats),
                figures, manuscript, manuscript_tables, recipe
queries/        the 346 materialised query entries (generated from information_sources.md)
runs/<date>/    requests.log.jsonl, raw/ (not committed), records/, queries.json, counts.json,
                merged.jsonl, screening_sheet.csv, prisma_counts.json, probes/
data/           what reviewers type: screening/decisions.csv; charting/README.md (procedure)
screen/         known_items.csv (frozen), audit and dual-sample CSVs, llm/prompts
charting/       datasets/<id>.json, aliases.csv, dataset_sources.csv, enrichment/, probes/
analysis/       every number, with derived_from       tables/  figures/  manuscript/  recipe/
tests/          check_run.py (the check-run stage), fixtures and the two run-diff tools
```

What is committed from a run directory: `run_meta.json`, `requests.log.jsonl`, `records/*.jsonl`
(the sources' own fields under `raw`, which the protocol keeps), `queries.json`, `counts.json`,
`merged.jsonl`, `screening_sheet.csv`, `prisma_counts.json` and `probes/`. Not committed:
`runs/*/raw/` (response bodies; `queries.json` says per source whether they may be published),
`runs/smoke*/` and `runs/review_*/` (throwaway smoke and reviewer chains), and LaTeX build
artefacts anywhere. The dated run directory of the review run is the only one kept.

How big `raw/` gets, measured per record in the cached envelopes of the review run: Europe PMC
about 9 kB (`resultType=core` carries the full record; `lite` would be a few hundred bytes, but
carries no abstract, which the prescreen needs), Semantic Scholar 2.6 kB, Crossref 2.2 kB,
bioRxiv/medRxiv 2.5 kB, OpenAlex and PubMed in between. Europe PMC therefore dominates: `epmc_02`
alone reports 152,589 hits and pages at 1,000 with no cap, so a full literature run writes roughly
1.4 GB of Europe PMC envelopes and something over 2 GB in total. `runs/*/raw/` is gitignored, but
this directory is inside OneDrive, which syncs it: exclude `spine_data_review/runs/` from sync, or
run with `--run-dir` under a path OneDrive does not watch, before the first unlimited search.

## Venue

Target: **Systematic Reviews** (BMC). It publishes protocol-driven scoping reviews reported under
PRISMA-ScR, expects the protocol and the deviations log to be cited, has no appendix limit (the
verbatim query strings for thirty sources are long), and accepts code and run logs as
supplementary material, which is what this review's evidence is. BMJ Open and JBI Evidence
Synthesis are the alternatives if the editors judge a dataset review out of scope; Scientific Data
(Analysis) would take it only if the download recipe and the pooled statistics were the main
result, which the protocol says they are not.

## Status

**The full search ran for run date 2026-09-23.** Every stage after it ran on 2026-09-24. The account is
`SchwingNet/results/transitional_registry/acquisition/REVIEW_RUN.md` in the parent repository, and the
deviations are the 2026-09-24 rows of PROTOCOL.md section 19.

- **Where it stops.** 26,176 records wait for screening.
- **Recall.** Known-item recall is 9 of 21 (0.43), under the 0.80 at which 6.4 requires a revision of the query
  strings.
- **Where the files are.** The small run files are in `runs/2026-09-23/`. The large ones (`records/`,
  `merged.jsonl`, `screening_sheet.csv`, `raw/`) stay in the WSL working copy.
- **Re-observation.** A request that did not answer can now be re-observed inside a run dir under a label
  (`SDR_REOBSERVE`, `SDR_REOBSERVE_SOURCES`; `tests/test_reobserve.py`).
- **Another host.** A source run on another host is merged back with `tests/merge_reobservation.py`.

Before that run, the pipeline ran end to end on the smoke path only. No record has been screened or charted, and the
modules the protocol names for screening,
enrichment, sampling, reliability and the primary GLMM are not written (`PIPELINE.md`, "What is not
built"). Every value those would produce renders as a red pending marker, not a number. The
`check-run` stage passes the verbatim-string rule on a fresh chain -- the adapters record the
frozen `queries/*.yaml` string and `odl_03` has an entry there -- so `strings` is now fatal, along
with `no-answer` and `wallclock`. A run directory made before 2026-09-20 still reports the old
mismatches; re-run `make smoke` rather than reading them as live.
