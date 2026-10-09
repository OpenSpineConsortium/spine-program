# PIPELINE.md — the contract between the stages

One line per stage: the module, what it reads, what it writes, and the fields the next stage
depends on. This is the file to change first when a field moves; the modules' docstrings repeat
their own side of it. Paths are relative to `spine_data_review/`; `<run>` is `runs/<run-date>`.
Every module is `python -m sdr.<module> --run-dir <run> --run-date <date> [--limit N] [--dry-run]
[--replay]` (`sdr.common.add_common_args`), and `Makefile` runs them in this order.

## Module names against PROTOCOL.md

The protocol (section 14) was written before the code and names stages, not files. What exists:

| protocol name | module here | note |
|---|---|---|
| one module per source | `sdr/search_literature.py` (L1–L7), `sdr/search_repositories.py` (R1–R8, the data archives), `sdr/search_platforms.py` (R9–R14, the code and model hosts), `sdr/search_figure_routes.py` (F1, F4–F8, the two mention harvests), `sdr/repo_run.py` (the `Run` state, helpers and binary GET the three repository modules share) | F2 MultiCaRe and F3 Open-PMC-18M are charting-time routes (figure-derived parents) and have no search adapter; `search_repositories --source all` runs R1–R8, R9–R14, then the figure routes, then the mention harvests in one process |
| `prescreen.py` | `sdr/dedup_prescreen.py` | merge (7.1) and prescreen (7.2) in one pass so the flow identity holds by construction |
| `validate.py` | `sdr/chart.py` | schema, quote rule, cross-field rules, "what is missing" |
| `probe.py` | `sdr/availability.py` | section 10 |
| `quality` | `sdr/quality.py` | rubric |
| `analyse.py`, `stats.py`, `meta.py` | `sdr/stats.py` (A3, A4, A5, A7 and the CLI), `sdr/flow_counts.py` (A1), `sdr/descriptives.py` (the general counting rules and A2), `sdr/estimators.py` (the formulae and their self-test) | one command, `python -m sdr.stats`, runs them all; the A5 primary GLMM (`meta.py`) is **not written** |
| `figure_counts.py`, `report.py`, `numbers.py` | `sdr/figures.py`, `sdr/manuscript.py`, `sdr/manuscript_tables.py` | manuscript.py owns `tables/numbers.tex`, `main.tex` and the checks; manuscript_tables.py the `tables/*.tex` renderers |
| recipe | `sdr/recipe.py`, `recipe/prepare_splits.py` | |
| `screen.py`, `enrich.py`, `sampling.py`, `reliability.py`, `trace`, `tests/` | **not written** | see "What is not built" |

## Stages

### 0. protocol-check — offline checks, then one keyed probe per service
Reads `information_sources.md`, `queries/literature.yaml`, `queries/repositories.yaml`,
`charting_schema.json`; runs the four self-tests (`dedup_prescreen --selftest`, `quality
--selftest`, `stats --selftest`, `recipe/prepare_splits.py --self-test`) and every `--dry-run`
(a dry run writes nothing). Then `sdr.common init` creates `<run>/` and writes
`<run>/run_meta.json` (`init_run_dir`: run_date, protocol_version, python, packages, credential
**names**, invocations with redacted argv and the `max_attempts` in force), printing the names
present, and `make creds-check` (`sdr.common check`) sends one harmless keyed request per
credentialed service. A failed probe is printed, not fatal: the service runs credential-free and
every `queries.json` entry records its own `credential_mode`. `RUN_DATE` has no default; the
`run-date` prerequisite of every stage rejects a missing or malformed one before anything is written.

### 1. search — `sdr.search_literature`, `sdr.search_repositories`, `sdr.search_platforms`, `sdr.search_figure_routes` (network, WSL)
Reads the verbatim strings: the literature module through `sdr.common.load_queries()` (229 ids
from the markdown), the three repository modules through `sdr.repo_run.load_repo_queries()`
(`queries/repositories.yaml` + `queries/literature.yaml`, the 346 materialised entries the
appendix prints, byte-checked against the markdown by `tests/test_queries_yaml.py`; the YAML
strips the markdown's inline annotations such as "(verify; fallback ...)", so `query_string`
is what was sent). Credentials by name from `~/.fluorocap/credentials.env`.
Writes, per source:
- `<run>/records/<source>.jsonl` — one line per unique item, sorted by `record_id`:
  `{record_id, canonical, source, query_id, query_ids[], retrieved_at, ids{doi,pmid,pmcid,arxiv,url,repo_id},
  title, abstract_or_description, year, type, raw}`. `record_id` is `lit:`/`repo:` + 12 hex of
  SHA-1 over `canonical` (`sdr.ids`); `query_id` is the first sorted query that found the item,
  `query_ids` all of them. **File stem = `source`** and the stems in use are: pubmed, epmc, openalex,
  s2, arxiv, biorxiv (both servers; query ids `biorxiv_01`/`medrxiv_01`), crossref, zenodo,
  figshare, dryad, osf, mendeley, datacite, physionet, tcia, kaggle, hf, gc, github, pwc, odl,
  openi, commons, jstage, koreamed, scielo, redalyc, kaggle-mention, hf-mention.
- `<run>/queries.json[query_id]` — `source, role, endpoint, method, query_string, intervals,
  n_requests, n_failed_requests, partial, params (secret-stripped), grammar, coverage, run_date,
  first_request_ts, last_request_ts, hit_count_api, unit, n_retrieved, n_fetched, n_pages, cap_hit,
  limit, date_filter, credential_mode, raw_cache_published, raw_cache_note, notes`; run-time sub-ids appear
  (`pubmed_01a-d`, `openalex_01_g01..g35`, `crossref_12a/b/c`); Open-i's two image types are
  recorded under the one yaml id `openi_NN` (`n_requests` counts both, `notes.hit_count_by_it` the
  totals). `date_filter` is stated by the adapter at every call (`repo_run.Run.query` has no default:
  `api` when the request carried the 2000-2026 limit, `local` when the limit is left to the screen,
  `none` when nothing was sent) and `raw_cache_published` is the summary table's cell; neither is
  copied from `queries/*.yaml` any more, so `tests/test_queries_yaml.py --run-dir <run>` compares two
  independently produced values and can fail. A disagreement with the plan is recorded beside the
  observation as `date_filter_planned` / `raw_cache_published_planned` and printed by the run;
  `n_fetched` (literature) is the count before any local filter.
  `n_failed_requests` counts the requests of the query that never answered (status 0, a 5xx, or a 429
  that outlived every attempt), written by `repo_run.Run.note_status`, and `partial` is true when more
  of them failed than the adapter declared through `Run.expect_failure` (only Figshare declares one:
  the body it sends to test the ~11-term ceiling). `partial` means the counts of that query are lower
  bounds, because every paging loop reads a failure as end-of-results; Table 2 daggers the row and
  `flow.json` per-source lists the query ids.
  A yaml id whose source has no adapter (`multicare_*`, `openpmc_*`, `not_run_reason` in the yaml) is
  written by `repo_run.write_not_run` (end of `search_repositories --source all`, which is what the
  Makefile runs, and of `search_figure_routes --source all`) with
  `credential_mode: not-run`, `hit_count_api: null`, `date_filter: none` and no `first_request_ts`,
  so Table 2 and Appendix A agree on what was searched. Table 2 counts a query only where a request
  went out (`manuscript_tables.executed`: a request timestamp, a total the source reported, or the
  role of a local harvest -- never the run date, which every not-run record also carries); such an id
  is counted in the table's "Not sent" column, dates nothing, and `\numQueries` excludes it while
  `\numQueriesNotSent` and `\numSourcesNotSearched` name what was left out. Appendix A prints every
  id, an unrun one as "not run" with its `not_run_reason` or the `condition` that would have sent it.
  `springer_01` (S1) runs in `sdr.search_literature`: `needs-credentials`, no request, when
  `SPRINGER_API_META_KEY` is absent.
  **Units and totals** (the repository modules): `n_fetched` is what the source handed over before
  any local filter and `n_retrieved` the distinct items kept per query (a record found by two
  queries counts once in each; `n_records_unique` counts it once); `n_requests` counts calls through `Run.get`
  (cache hits included; a retry adds a log line, not a call); `hit_count_api` is the API's own
  total or null when the API reports none (Kaggle, Hugging Face, Figshare, Mendeley: the
  retrieved count is never copied into it); `unit` names what the total counts: `records`
  (deposits, repositories, articles), `figures` (Open-i, each string run twice), `files`
  (Commons), `harvest` (PhysioNet, TCIA, grand-challenge, the PwC dump, the mention harvests:
  the size of a listing filtered locally). A consumer that adds hit counts across sources adds
  `unit == "records"` and `role == "search"` only. For a list source `endpoint` is the endpoint
  actually requested (the REST list, or the HTML fallback when it answered 404) and
  `notes.endpoint_used` repeats it; `query_string` stays the YAML string.
  **Verbatim-string rule** (PROTOCOL.md 6.3; checked by stage 1b): `query_string` is the string of
  the query's entry in `queries/*.yaml`, character for character, and a sub-id inherits its base
  id's string. Anything the adapter adds at run time — a fallback taken, an endpoint verified, a
  local filter, a template's interval — goes into `notes`, never into `query_string`; a run-time id
  with no YAML entry (`odl_03` at integration) needs one. `sdr.manuscript.load_query_records` prints
  `query_string` in Appendix A, so an annotated string there is a mismatch with the frozen file.
  Every run-time fact that changes what a source answered (a timeout after `max_attempts`, a
  non-JSON body, a retired endpoint) is a `notes` entry, so Table 2 can show the source as "no answer".
  `coverage`, `raw_cache_published` and `raw_cache_note` are read at run time from the summary table
  of `information_sources.md` (`sdr.common.source_table`), never typed in an adapter; `date_filter` is
  what the adapter did (`api` everywhere in `sdr.search_literature` except `biorxiv_01`/`medrxiv_01`,
  whose `query_string` is the template, whose intervals stop at the run date and whose bounds are
  stated in `notes`; `local` wherever the year limit is left to the screen). `role` is the adapter's
  word too (`search`, or `supplementary` for `springer_01`), and `tests/test_queries_yaml.py` checks
  both against the plan.
  `n_fetched` is the number of items fetched before a local filter (Crossref pass (a), the bioRxiv
  dumps) and equals `n_retrieved` elsewhere, so a `--limit` check reads it first. `params` records
  the page size actually sent (`retmax`, `pageSize`, `rows` shrink under `--limit`).
  **Resuming in the same run dir** (`sdr.search_literature`): a query whose cached first page carries
  session state (PubMed WebEnv, Crossref cursor, Semantic Scholar token) that leads to an uncached page
  is restarted live under `cache_salt resume<n>` and says so in `notes`; `--replay` follows the same
  salted chain. Exit status is 1 when a fallback the protocol names could not be sent (OpenAlex 400
  with no grid strings in either query file); the source's records are still written.
- `<run>/counts.json[source]` — merged by all three modules: `queries{qid: {hit_count_api, unit,
  role, n_retrieved, n_requests, cap_hit, credential_mode}}`, `n_records_unique`, `n_unusable_ids`
  (items with no usable identifier), `n_requests`, `hit_count_api_total` (sum over
  `unit == records` and `role == search` only) and `hit_count_by_unit{unit: sum}`.
- The mention harvests (`kaggle-mention`, `hf-mention`; role `supplement`, unit `harvest`) scan
  the records still in memory plus every `records/<source>.jsonl` on disk that is not in memory;
  both lists are in the query's `notes` (`scanned_in_memory_sources`, `scanned_files`).
- `<run>/requests.log.jsonl`, `<run>/raw/<source>/<sha1>.json` (section 15; `--replay` serves from it).
  HTTP attempts per request are `sdr.common.max_attempts()`: five, or `SDR_MAX_ATTEMPTS` from the
  environment, which the Makefile exports as 2 on any `LIMIT` run (recorded per invocation in
  `run_meta.json`).

### 1b. check-run — `tests/check_run.py` (offline)
Reads `<run>/requests.log.jsonl`, `<run>/raw/`, `<run>/queries.json`, `queries/*.yaml`,
`information_sources.md`, the credential store (values held in memory only, for the scan) and every
text file under `<run>/` and the output directories. Prints PASS/FAIL for log-fields, log-cache,
strings (the rule above), no-answer, paging, secrets and wallclock; exit 1 on all of them except
`paging`, which is printed only (a source that reports a total it does not serve is the source's
behaviour, not the run's). `no-answer`: a query whose requests were mostly transport errors or 5xx
must say so in its `notes`, counted from the request log rather than from the notes themselves, so a
source that never answered cannot be read as a source that answered zero. `wallclock` exempts a
query's own `intervals` and any date its intervals or its frozen string already contain (a bioRxiv
note restating its monthly bounds is not a wall clock). Writes nothing. `make all` and `make smoke`
run it directly after `search`.

### 2. dedup — `sdr.dedup_prescreen` (offline)
Reads every `<run>/records/*.jsonl`, `screen/known_items.csv`, optional
`screen/prescreen_rules.yaml` (absent: the Appendix A literals, sha1 recorded).
Writes:
- `<run>/merged.jsonl` — one row per unique record, no `raw`: `record_id` (representative), `ids`
  (union, except `repo_id`, taken only from members whose DOI is the representative's or absent),
  `title`, `abstract_or_description` (longest), `year`, `type`, `first_author`, `sources[]`,
  `query_ids[]`, `found_by[{source, query_id, record_id}]`, `member_record_ids[]` (distinct),
  `n_members` (over distinct ids), `member_dois[]`, `concept_doi` (Zenodo), `related_dois[]`
  (every DOI a repository member links to, merged or not, for the 7.6 mapping), `merge_rules[]`,
  `source_class`, `source_classes[]`, `prescreen_outcome`, `prescreen_rule`, `flags[]`,
  `lang_flags[]`, `known_item` (a DOI-keyed item also matches through `concept_doi` and
  `member_dois`), `to_screen`. No two rows share a `record_id`: the same canonical string found by
  two sources (github and pwc, hf and hf-mention) is one row, counted under merge rule 0.
- `<run>/screening_sheet.csv` — the reviewer's sheet, columns `record_id, to_screen,
  prescreen_outcome, rule_fired, source_class, sources, query_ids, n_members, merge_rules, flags,
  lang_flags, known_item, title, year, type, doi, pmid, pmcid, arxiv, url, first_author,
  abstract_or_description, member_record_ids`.
- `<run>/prisma_counts.json` — `identified` (after within-source dedup and `--limit`),
  `merge{rule_0_identical_canonical, rule_1_doi..rule_6_related_identifier,
  rule_6_skipped_many_dois, rule_6_skipped_derived_context}` (rule 6 links a repository record to
  a `lit:` article only, never repo to repo, and skips a DOI cited in a derived-from context),
  `duplicates_removed` (rules 0-6),
  `after_merge`, `identity_check`, `prescreen{outcome: n}`, `prescreen_uncertain_no_abstract`
  (the `uncertain` rows decided by 7.2's no-abstract rule: found only by literature sources and
  with no abstract in any of them, so they reach the reviewer instead of being recorded as a
  modality or dataset failure they were never tested for), `prescreen_by_source_class`,
  `to_screen`, `flags`, `known_items{n_in_file, n_matched, matched}`, `rules{sha1, origin}`.

### 3. screening — reviewers (no module yet)
Reads `<run>/screening_sheet.csv`. Writes `data/screening/decisions.csv` (protocol 7.3 columns +
`full_text_retrieved`, `arm`; header in place) and, under `screen/`, `prescreen_audit.csv`
(`record_id, stratum, decision`), `dual_sample.csv`, `chase_manual.csv`, `llm/outputs.jsonl`.
`sdr.stats` looks for each CSV under `data/screening/` first and `screen/` second.

### 4. charting — reviewers + `sdr.chart` (offline gate)
Reads `charting/datasets/<id>.json` (schema `charting_schema.json`), `licence_tiers.csv`,
`charting/aliases.csv`, `charting/dataset_sources.csv` (`dataset_id, record_id, role`),
`screen/known_items.csv` (`recall` rows are expected datasets), `<run>/merged.jsonl` (record ids
are checked against representatives and members), optional `--rechart-dir`.
Writes `charting/datasets.jsonl` (valid records only) and `charting/validation_report.json`
(`datasets{id: {errors, warnings, valid, q2_type_read}}, expected_not_charted` (recall known
items plus alias-table ids, minus the `I1-test` and `excluded-I4` known items, listed as
`not_expected_known_items`), `charted_without_alias_row, n_unverified, n_use_records_written`);
fills `n_use_records` from `dataset_sources.csv` and writes a changed value back into
`charting/datasets/<id>.json` (not on `--dry-run`), since downstream stages read those files.
Relative `--charting-dir`, `--rechart-dir`, `--out`, `--report` and `--schema` resolve against
`spine_data_review/`. Exit 1 on any error unless `--allow-invalid`; exit 2 when an explicit
`--charting-dir` does not exist (the default absent is a warning: an empty gate). A CC-BY family
licence takes its version from `licence.text` (3.0 charts as `CC-BY-3.0`; 4.0 is the default).
`--limit N` validates the first N files and writes only those to `--out`, so on a `LIMIT` run the
Makefile's `CHART_FLAGS` default sends `--out` and `--report` to `<run>/charting/` and an explicit
`CHART_FLAGS` without `--out` is refused; the committed `charting/datasets.jsonl` is only ever
written by an unlimited run.
`data/charting/README.md` is the reviewer procedure. Downstream stages read
`charting/datasets/*.json` directly, so this gate must pass first.

### 5. availability — `sdr.availability` (network, WSL)
Reads `charting/datasets/<id>.json` (`access_url`, `file_url_probed`, `checksums[].url`,
`versioning.dataset_doi`, `source_record.doi`, `notes`, `quotes[].text`) and optional
`charting/enrichment/<id>.json` (`file_url_probed` or `files[].url`); or, with
`--from-known-items`, `screen/known_items.csv` (`item, url, doi, note`).
Writes `charting/probes/<id>.json` (`--probes-dir`): `{id, access_url, host_type, file_url_probed,
probes[] (one per date in the schema's probe shape: date, url, method, http_status, final_url,
content_type, classification_machine, rule, evidence, ...), file_probes[] (same shape, on the file
URL), agreement{status, route, rule, dates}}`; `<run>/probes/<run-date>.jsonl` and
`<run>/probes/summary.json`. With `--apply` and two agreeing probes it writes `access_probe`,
`host_type`, `access_route`, `access_route_rule` into the charting record (never over a
`verifier:` rule). Run twice, ≥ 48 h apart; `sdr.chart` enforces the gap.

### 6. quality — `sdr.quality` (offline)
Reads `charting/datasets/<id>.json` and `charting/probes/<id>.json` (`file_probes[]`, the Q7 file
evidence; `--probes-dir`, default the `probes` directory beside `--charting-dir`, so a fixture
laid out as `<dir>/charting` + `<dir>/probes` needs no flag). Writes `analysis/quality.json`:
`{per_dataset{id: {items{Q1..Q10: {score, rule}}, total, total_without_q7, total_without_q6_q7_q8,
band, annotated, q2_type_read, fit_level_id, fit_level_id_fail_rule, usable_for_training,
usable_for_training_fail_rule, fit_variant, fit_stitching, fit_stitching_fail_rule, verified,
derived_from}}, summary{n_datasets, n_verified, n_annotated, n_fit_*, bands, item_share, total_min,
total_max}, run_date, rule, derived_from, scores_sha1}` and `tables/quality.tex`; the invocation
goes to `<run>/run_meta.json`.
- `scores_sha1` is SHA-1 over `json.dumps(per_dataset, sort_keys=True)` (`quality.scores_sha1()`);
  stage 7 recomputes it and refuses a file whose hash does not match.
- Q7's file confirmation is `quality.file_url_confirmed()`: the file URL answered 200/206 on **two
  distinct probe dates** (`file_probes[]` plus `access_probe[]` entries on that url); stage 7 uses
  the same function for SAP A3.2.
- Q4 interpretation (rubric row 1 names derivable-from-labels, reported-in-text and
  excluded-by-design only): an `explicit-label` variant without both counts scores 1, on the
  reading "a label scheme that could carry it". The rule string cites the deviations-log row in
  PROTOCOL.md section 19 dated 2026-09-19, section `quality_rubric.md row 1 (Q4)`.
- Order independence with stage 7: when the file exists and its `scores_sha1` equals the new one,
  the blocks stage 7 merged (`summary.total`, `fitness`, `total_vs_year`, `total_vs_route`,
  `total_vs_modality`, `analysis_derived_from`) are carried over; when the scores changed they are
  dropped and the message says to rerun `sdr.stats`.

### 7. stats — `sdr.stats` (offline; A1 in `sdr.flow_counts`, A2 and the counting rules in `sdr.descriptives`, formulae in `sdr.estimators`)
Reads `charting/datasets/*.json`, `charting/probes/<id>.json` (`--probes-dir`, default the
`probes` directory beside `--charting-dir`), `analysis/quality.json`, `<run>/queries.json`,
`<run>/records/*.jsonl` (+ `records/chase.jsonl` when the chase adapter exists),
`<run>/merged.jsonl`, `<run>/prisma_counts.json`, `<run>/screening_sheet.csv` (or
`screen/prescreen.csv`), the reviewer CSVs (stage 3), `charting/dataset_sources.csv`,
`screen/known_items.csv`, `charting_schema.json` (the enums every count table is seeded with).
Absent inputs are listed in `flow.missing_inputs`, never guessed. Before anything runs,
`analysis/quality.json` must hold exactly the ids of the charting records and a `scores_sha1`
that matches its `per_dataset`; otherwise the module prints the difference and exits 1
(allowed, and said so, under `--limit`; printed under `--dry-run`). The invocation goes to
`<run>/run_meta.json`. General rules applied everywhere (`sdr.descriptives`): a zero is a row
(every enum value present, `n_datasets` 0, null sums), a `subject_overlap` pair is collected
from either record (frozenset of the two ids, the larger `n_shared` when both list it) and
subtracted once, multi-modal datasets contribute `n_per_modality` to modality rows.
Writes `analysis/<name>.json` as `{value, derived_from, rule, run_date}`:
- `flow.json` — `per_source{source: {hit_count_api, n_retrieved, n_identified, credential_mode, cap_hit}}`
  (search-arm sources only: a source whose queries.json roles hold no `search`, and the `chase`
  file, are not rows; `n_identified` excludes chase rows), `search_arm{identified, after_merge,
  merged_rows, duplicates_removed, merge_rules (keys `rule_0_`..`rule_6_`, never `rule_6_skipped_*`),
  prisma_counts_present, prescreen{pass, uncertain, uncertain_no_abstract (the share of
  `uncertain` carrying 7.2's no-abstract rule, read from the sheet's `rule_fired`),
  non_english_route, fail{}, fail_total, by_source_class}, audit{sampled, included, excluded, by_stratum}, screened,
  screen_excluded_by_code, use_only, unclear_to_full_text, include_to_full_text,
  sought_for_full_text, not_retrieved, full_text_excluded_by_code, included_records,
  included_records_search}`, `other_arm{known_items (int), known_items_by_role_retrieved,
  chase_backward, chase_forward (null with a missing-input note when no chase record exists),
  chase_manual, screened, excluded, included_records}`, `datasets{total, derived, figure_derived,
  non_derived_non_figure, n_use_records_per_dataset, source_records_per_dataset,
  mapped_from_included_records[], included_records_unmapped[], not_mapped_from_included[],
  dataset_sources_present}`, `identities{}` (nine SAP A1 checks: the three prisma_counts
  comparisons, the four screening-chain sums, the two dataset identities including
  `datasets = |map(included_records_search U included_records_other)|`, which is True/False
  whenever dataset_sources.csv exists; `--check-flow` exits 1 on any False), `missing_inputs`.
- `descriptives.json` — `table[]`, `totals{n_subjects_sum, n_images_sum, n_datasets, n_datasets_in_totals}`,
  `totals_rule{keep, excluded, subtract, subtracted_pairs}`, `by_<stratum>{value: {n_datasets,
  n_subjects_sum, n_subjects_median, n_subjects_iqr, n_subjects_n_known, n_subjects_n_unknown,
  n_images_*}}` for modality (per `n_per_modality`), region, projection_radiography,
  annotation_type, annotation_origin, access_route, licence_tier, year, year_band, country,
  **country_top_ten** (ten rows plus `other`), pediatric, format, flags, level_names,
  variant_labelling; the cross-tabs `year_x_modality`, `cumulative_subjects_by_year_modality`
  (same per-modality rule as `by_modality`; `--selftest` asserts they agree), `origin_x_modality`,
  `variant_x_level_origin`, `level_names_x_modality`, `region_x_projection_radiography`,
  `route_x_licence`, `public_charted_x_regex`.
- `availability.json` — `route_distribution{overall (all six routes), by_modality, by_year_band, by_host_type}`,
  `route_x_modality`, `route_x_year_band`, `route_x_host_type`, `described_public_downloads{primary,
  file_url (two distinct dates, from charting/probes/<id>.json), recipe_eligible: {numerator,
  denominator, proportion, ci}, file_url_rule}`, `verifier_overrides{n, ...}`,
  `route_rule_distribution`, `probe_agreement{changed_between_probes (classification **or** HTTP
  status class), n_changed, n_third_probe, rule}`, `figure_pool{per_query, per_source, note}` (SAP
  A3.4, from queries.json), `unavailable_x_year_band`, `trend_unavailable_by_band`.
- `quality_analysis.json` — `total{all, annotated, unannotated, median, q1, q3}`, `item_share`,
  `total_vs_modality`, `total_vs_route`, `total_vs_route_without_q7`, `..._without_q6_q7_q8`
  (each `{annotated, all}`; `epsilon2` and `dunn_holm` on `annotated` only, `all` carries a note),
  `total_vs_year{annotated, all: {rho, p, ci, n}}` (None with a note on a constant input, never
  NaN), `total_vs_log10_subjects`, `scatter[]`, `fitness{fit_level_id, usable_for_training,
  fit_variant, fit_stitching: {n, ids, by_modality}, subjects_fit_level_id, fail_rule (F1–F4 all
  present)}`. The `total`, `fitness`, `total_vs_year`, `total_vs_route`, `total_vs_modality`
  blocks are also merged into `analysis/quality.json` (`summary.total`, top level), which is where
  `sdr.manuscript` reads them; stage 6 carries them over on a rerun with unchanged scores.
- `pooled_variants.json` — per variant `{per_dataset[{id, year, modality, x, n, p, ci_low, ci_high,
  selection, ascertainment, definition_class, poolable, enriched, ineligible_reasons}], k_eligible,
  pooled (DL on the logit scale: estimate, ci_low, ci_high, pi_low, pi_high, tau2, I2, I2_ci, k, ...)
  | null, note, enriched{k, ids, pooled, note}, totals_rule (family/overlap rule with that
  variant's n_subjects_assessed as n_i)}`, `estimator_note`.
- `grid_coverage.json` — `overall{n_on_grid, n_partial, n_reachable, n_reachable_not_on_grid,
  n_datasets}`, `status_x_modality`, `status_x_region` (seeded), `subjects_on_grid_over_reachable`,
  `fit_level_id_on_grid`, `per_dataset[{id, status, path, n_subjects_on_grid, access_route,
  fit_level_id}]`, `recipe_order[{id, quality_total, access_route, n_subjects}]`.
- `tables/<analysis>_<key>.csv` for the dataset table, the `by_*` strata and numeric cross-tabs
  (integer cells, never `6.0`).

### 8. figures — `sdr.figures` (offline)
Reads only `analysis/{flow, pooled_variants, descriptives, availability, quality_analysis}.json`
(no fallback to `prisma_counts.json`, whose shape is different; an absent file is a skip with a
message and exit 1). Writes `figures/fig1_prisma_flow.pdf`, `fig2_datasets_per_year.pdf`,
`fig3_access_by_modality.pdf`, `fig4_quality.pdf`, `fig5_forest_<L6|T13|LSTV>.pdf` (+ PNG twins;
the source JSON's sha1 in the PDF Subject; **no CreationDate/ModDate**, so two runs on the same
JSON are byte-identical and `--selftest` checks that in memory); the invocation goes to
`<run>/run_meta.json`. `--only` is validated against the five names (exit 2 otherwise); under
`--limit` the forest rows are truncated and the footer says so while the diamonds stay pooled
over every eligible row; each stratum's diamond is drawn directly under its own rows.
`sdr.manuscript.FIGURE_FILES` maps the template's `@@FIGURE:name@@` markers (the SAP's names
prisma_flow, datasets_by_year, availability, quality, variants) to these files; a marker whose
files are all absent renders as a red placeholder.

### 9. manuscript — `sdr.manuscript` + `sdr.manuscript_tables` + `manuscript/build.sh`
Reads `manuscript/template.tex`, `PROTOCOL.md`, `PRISMA-ScR_checklist.md`, `information_sources.md`,
`charting_schema.json`, `queries/*.yaml`, `<run>/queries.json`, `<run>/counts.json` (source-keyed,
as `sdr.search_*` write it: `{source: {n_items, …, queries: {qid: {hit_count_api, n_retrieved, …}}}}`;
a flat `{qid: …}` form is accepted; any other top-level id raises), `runs/pilot-2026-09-19/queries.json`,
`charting/datasets/*.json`, `analysis/*.json` (the ten names in `ANALYSES`; four of them —
`pooled_agreement`, `screening_reliability`, `search_validation`, `build_info` — have no producer
yet and render as `\pending`). Two contracts on files other modules will write: `quality.json`
`reliability {n, icc_total: {value, ci: [lo, hi]}, per_item_kappa: {Q1..Q10}}` (SAP A4.5,
`sdr.reliability`) fills the quality table's note and `\numICCTotal*`/`\numReliabilitySample`, pending
until present; `pooled_variants.json` `<variant>.pooled.estimator` must name the GLMM (SAP A5.2,
`sdr.meta`) before `\numPooledLSTV*` and `\numPooledEstimator` render — while it names
DerSimonian–Laird (what `sdr.stats` writes) they stay pending and the pooled row is labelled a
sensitivity estimator, so the sensitivity value cannot be printed as the primary one. The guard is
on the presence of `LSTV.pooled`, not on a named estimator: a pooled block that names none is
pending too, with the reason distinguishing "the file names a sensitivity estimator" from "the file
names no estimator", so an unattributed prevalence cannot print as the pre-specified primary result.
Table 2 has one row per planned source of `information_sources.md`'s summary table — every row whose
code has the shape of a search series (`[LRFS]\d+`) and that the table does not mark as not a search
source (S2, Unpaywall) — so its rows and `\numSourcesPlanned` are one set; a planned source no query
was sent to keeps its row, says `not run`, prints `--` in every count column and has its recorded
`not_run_reason` in the note. Rows are ordered naturally on the code (R2 after R1, R10 after R9).
Arms that are not numbered sources carry a code of their own: the chase is `O1`, and the Kaggle and
Hugging Face mention harvests are `R9a` and `R10a`, because they belong to R9 and R10 and would
otherwise print a second row under a duplicated code. Counted queries are those that ran (a record
with no request timestamp, reported total or supplementary role is a template: the chase templates,
the Open-i grid heads). Hits are summed per-query totals (stated in the note); `Retrieved` comes from
`flow.json`'s per-source `n_retrieved` where the flow has an entry, so it and `Identified` trace to
one file, and the note carries a warning when the flow identifies more records than it retrieved.
`\numSourcesRun` is the number of sources with `Retrieved > 0` — what the Results sentence claims,
and what Table 2's own rows add up to — not the number that reported an API total.
Appendix A prints the YAML `string` for every id the YAML defines, then the markdown form when it
differs, then the run's sent string when that differs from both. The git commit in `main.tex` comes
from `build_info.json` or, until that exists, from `render_commit` in `<run>/run_meta.json`, written
once at the first non-dry render so re-renders of one run do not move with HEAD.
Writes `tables/*.tex` (13 tables), `tables/numbers.tex` (`\num<Name>`/`\numword<Name>`, dotted
paths in `NUMBER_MACROS`) and `manuscript/main.tex`; `--tables-dir/--figures-dir/--main-out`
relocate them (the smoke run uses `runs/smoke/…`) and the `\input` paths are computed relative
to `main.tex`. `--dry-run` writes nothing but still exits 1 under `--check`, so a dry run that found
an unreplaced marker, a bare digit or an over-long abstract is not read as clean. `build.sh [--strict] [DIR]` builds the PDF and fails on an undefined macro or
reference and on a bare digit in Abstract or Results (`python -m sdr.manuscript --scan main.tex`,
the renderer's own `--check` on the rendered file, outside the allow-list
`manuscript/allowed_literals.txt`: first token per line, then the reason; PROTOCOL.md 13(c)).
PROTOCOL.md 13(b), a defined-but-unused macro fails the build, any pending macro, table or figure,
and an overfull box wider than `OVERFULL_MAX_PT` (default 6.0 pt; a table cell printing into its
neighbour or the margin), are enforced by `--strict`, which the Makefile passes on an unlimited run
(`MANUSCRIPT_FLAGS ?= $(if $(LIMIT),,--strict)`); any `LIMIT` run clears it, because a `--limit` run
leaves analyses pending by construction and would otherwise die one stage short of `recipe`. `build.sh`
also runs `tests/test_queries_yaml.py` twice: the YAML-against-markdown checks are fatal (the
appendix is printed from those files), and the run-against-YAML checks (`--run-dir`, the run named
in `main.tex`'s header) are printed and fatal only under `--strict`, because a mismatch there is an
adapter defect the check-run stage reports, not a manuscript defect.

### 10. recipe — `sdr.recipe` (offline)
Reads `charting/datasets/*.json` (`access_route`, `access_route_rule`, `host_type`, `access_url`,
`file_url_probed`, `checksums[]`, `licence`, `on_grid.status`, `versioning.dataset_doi`,
`source_record.doi`, `access_probe[].http_status`), `analysis/quality.json` (`per_dataset.<id>.total`,
`fit_level_id`), optional `charting/enrichment/<id>.json` (`files[]`). Writes `recipe/download_all.sh`,
`recipe/datasets/<id>.sh`, `recipe/manifest.csv` (columns in `MANIFEST_COLUMNS`); `--demo` writes
three built-in records to `--out`. `recipe/prepare_splits.py` reads `manifest.csv` and
`$DATA_ROOT/<id>/.recipe_status`.

## Reconciliations made at integration (2026-09-19)

1. `sdr.stats._selftest` indexed `wilson()` as `lo/hi`; the function returns `ci=[lo, hi]` and
   `clopper_pearson()` returns `ci_low/ci_high`. Fixed; the selftest now runs (DL matches statsmodels).
2. `sdr.stats.flow` read `screen/prescreen.csv` and `merged_from[]`, which nothing writes. It now
   takes `identified` and the merge-rule counts from `<run>/prisma_counts.json` and the prescreen
   outcomes from `<run>/screening_sheet.csv` (`prescreen_outcome`), keeping `screen/prescreen.csv`
   as an alternative; reviewer CSVs are looked up under `data/screening/` then `screen/`
   (`--decisions-dir`, `--screen-dir`).
3. `sdr.manuscript` asked `descriptives.json` for `per_vertebra_level_names.yes.n_datasets` and
   `variant_by_origin.explicit_label.total`, and `grid_coverage.json` for `overall.*`; `sdr.stats`
   now writes `by_level_names`, `by_variant_labelling` and `grid_coverage.overall`, and the macro
   paths point at them.
4. `sdr.quality` Q7 looked for file probes inside `access_probe`; `sdr.availability` keeps them in
   `charting/probes/<id>.json` `file_probes[]`. quality now reads that file (`--probes-dir`).
5. `sdr.manuscript` and `build.sh` gained output-location flags so the smoke run writes under
   `runs/smoke/` and never overwrites the real `tables/`, `figures/`, `manuscript/main.tex`.
6. `sdr/__init__.py` names the modules that exist. PROTOCOL.md (frozen) still uses its own names;
   the table above is the map.
7. The template's figure markers used the SAP's figure names; `sdr.figures` writes `fig1_…fig5_…`.
   `sdr.manuscript.FIGURE_FILES` maps one to the other (the three forest plots under `variants`),
   and `build.sh` counts pending figures from the rendered `main.tex`.
8. `sdr.manuscript.check` flagged the digit in `fig1_…` inside `\includegraphics` as a typed number;
   `\includegraphics[...]{...}` is now stripped like `\input` before the bare-digit scan.
9. A pending table now carries its `\label{tab:<name>}`, so `\tabref` resolves and `build.sh`
   reports OK once the PDF builds with every reference defined; `--strict` still fails on any
   pending macro, table or figure.
10. Stats-module review (2026-09-19): `sdr/stats.py` (659 lines) was split into `sdr/estimators.py`,
    `sdr/descriptives.py`, `sdr/flow_counts.py` and `sdr/stats.py`; the fixes listed in stages 6–8
    above were made (file probes read from `charting/probes/`, symmetric overlaps, per-modality
    sums, seeded zeros, prisma_counts comparisons, chase as a missing input, quality.json
    consistency check, integer CSV cells, dated-free PDFs, run_meta invocations). Two
    consequences for `tests/test_stats_module.py` on `tests/fixtures/stats`: the seeded tables now
    carry zero rows (`by_level_names.partial`, the three unused routes), which its exact-dict
    checks did not expect; and the new record-to-dataset identity is False on that fixture (twelve
    datasets, five included records mapping to four), so `--check-flow` exits 1 there. That is the
    correct report for the fixture, not a defect; the test's expectations are the reviewer's to
    update. `per_source.n_identified` no longer counts `openalex_03*` chase rows as search hits
    (openalex 3, not 5, on the fixture).
10. `make smoke` ran `chart-check --limit 5` against the default `--out`, so once charting records
    exist it would have truncated the committed `charting/datasets.jsonl` to five rows. Any `LIMIT`
    run now writes both chart outputs under `<run>/charting/` (the `CHART_FLAGS` default),
    `chart-check` refuses a `LIMIT` run whose explicit `CHART_FLAGS` lacks `--out`, and `sdr.chart`
    itself exits 2 when `--limit` is given with the default `--out`/`--report`, so the protection
    holds for a module invoked by hand as well as through the Makefile.
11. `RUN_DATE` defaulted to the wall clock (`date -u +%F`), against PROTOCOL.md 15; it is now
    required and checked by the `run-date` prerequisite of every stage.
12. `protocol-check` created no run directory (every step was a self-test or dry run) while this
    file said it wrote `run_meta.json`; it now ends with `sdr.common init` and `creds-check`.
13. `tests/check_run.py` runs as the `check-run` stage after `search`. The verbatim-string rule now
    passes on a fresh chain (the adapters record `Q[qid]["string"]`, and `odl_03` has an entry in
    `queries/repositories.yaml`), so `strings` is fatal rather than narrated, as are `no-answer` and
    `wallclock`. A run directory made before 2026-09-20 (`runs/smoke`, if kept) still reports the old
    mismatches: re-run `make smoke` rather than reading them as live.
14. `sdr.common.RateLimitedSession.get` takes its attempt count from `max_attempts()`
    (`SDR_MAX_ATTEMPTS`, exported as 2 by the Makefile on a `LIMIT` run) after api.osf.io answered
    20 s read timeouts on all five attempts of every query and stalled a reviewer chain for minutes.
15. `data/screening/decisions.csv` (two columns beyond PROTOCOL.md 7.3 and a different directory)
    is now a row in the PROTOCOL.md section 19 deviations table, as is the `--strict` point of item 9.
16. `.gitignore` covers `runs/review_*`, the relocated build artefacts under `runs/*/manuscript/`
    and `tests/_out/`; README.md states which run-directory files are committed.
17. Two run-diff tools exist: `tests/diff_runs.py` (records, queries, counts) and
    `tests/diff_run_dirs.py` (the whole chain through the recipe and the request sequence). Both are
    kept; README names them.
18. Literature-module review (2026-09-20). Semantic Scholar elides the abstract of every
    closed-access paper (406 of the 1,000 records on the first `s2_01` page; 405 of them fail the
    three regexes on their title alone), which no parameter can undo, so 7.2 gained the no-abstract
    rule above and the flow gained a row for it. Europe PMC's `resultType=core` abstracts are
    stripped of their JATS markup before being stored, because the merge keeps the longest member
    abstract and the marked-up copy was displacing the clean PubMed one. `run_arxiv` retries an
    empty feed on the empty feed alone while nothing has been retrieved, not on
    `start < totalResults`: arXiv's transient form also zeroes `totalResults`, and a query that
    ends there now records `hit_count_api` null with a note instead of a bare zero, so a source's
    whole row cannot go missing silently. `queries/literature.yaml` held a second copy of the
    summary table's `coverage` and `raw_cache_published` cells that had drifted for six of the
    eight literature sources; the copies are aligned and
    `tests/test_search_literature_fixture.py` now compares them.
19. The 150-450 line rule is not held by `sdr/search_literature.py` (632),
    `sdr/availability.py` (817), `sdr/common.py` (573) or `sdr/dedup_prescreen.py` (556). Lifting
    `Query` and its cache/resume bookkeeping into `sdr.common` would move lines between two files
    that are both over the rule rather than bring either under it, so it is recorded here rather
    than done. What the rule is protecting - one CLI, one docstring that says why, no framework -
    holds in each of them.

## Smoke run (2026-09-19)

`make smoke RUN_DATE=2026-09-19` ran the chain with `--limit 5` into `runs/smoke/`: 29 record
files from the search (773 logged requests; the log carries credential names only), 97 merged
records (no duplicate at this size), chart-check with zero records (exit 0, the 29 expected
datasets listed), five known items probed (four registration, one data-use-agreement), quality and
stats on zero datasets, four figures (the forest plots skip without rows), a 21-page PDF with no
undefined reference, and the three demo recipe scripts. In `flow.json` the audit and chase CSVs are
listed as missing inputs, and the identity `screened = pass + uncertain + non_english +
audit_included` is False because `data/screening/decisions.csv` holds only its header: that is the
correct report for an unscreened run, and `STATS_FLAGS=--check-flow` would make it fatal. The
manuscript stage failed twice on the way (items 8 and 9) and was rerun on the same run directory
after each fix; the earlier stages were not rerun because their code did not change.

## What is not built (stated so it is not mistaken for done)

`sdr/screen.py` (the reviewer CLI; decisions are typed into `data/screening/decisions.csv`),
`sdr/enrich.py` (API enrichment into `charting/enrichment/`; `availability` and `recipe` accept its
output when present), `sdr/sampling.py` (the seeded draws of 7.8), `sdr/reliability.py` (A4.5, A8
→ `screening_reliability.json`), `sdr/meta.py` (A5 primary GLMM; `pooled_agreement.json` A6),
`search_validation.json` (known-item recall, 6.4), `build_info.json` and `tests/`. Each renders as
a pending marker or a missing-input note rather than a number.

## Shared layer contract (`sdr.common`, `sdr.creds`, `sdr.ids`; review of 2026-09-19)

What every adapter may rely on, fixed by the 2026-09-19 review of the shared layer
(`tests/test_common_review.py`, `tests/test_ids.py`, `tests/live_common_probe.py`):

- **A query string inside `url` is merged into `params`** by `RateLimitedSession.get` and
  `cache_path` before hashing or logging (explicit `params` win on a clash). A server-supplied
  next-page URL may be passed straight through and gets its own cache key and log line;
  `search_repositories._split` is no longer load-bearing.
- **Cache key** = SHA-1 over `method`, canonical secret-stripped URL, sorted secret-stripped
  `params`, POST body, `cache_salt`, plus the line `keyed` when `keyed=True`. Anonymous keys are
  byte-identical to protocol-v1.0 (every fixture and run replays unchanged); keyed answers (HF
  gated datasets, NCBI, Springer) are stored apart from anonymous ones, so a keyed request cached
  before this change misses once and is refetched.
- **Redaction by value everywhere**: `redact_text` (plain, `quote`, `quote_plus` and lower-cased
  spellings of every loaded credential of six or more characters) is applied to the logged url,
  every string-valued parameter (`strip_params`), the error text, the final url, the response
  body before it is cached or returned, and run_meta argv. Name-based stripping of
  `SECRET_PARAMS` still applies first. A body is therefore never bit-identical to the wire when
  it echoed a credential; that is the intended difference.
- **`get` also serves the probe**: `method="HEAD"`, `allow_redirects=False` (hops followed one at
  a time up to `session.s.max_redirects`, statuses in `Resp.chain`, answering URL in
  `Resp.final_url`, both in the envelope), `stream_cap=N` (at most N bytes read, `stream=True`)
  and `full_headers=True` (every header, not the logged subset). `availability.probe_fetch` can
  now delegate to `get` and drop its private attempt loop; until it does, its three-attempt
  ladder and envelope are a documented duplicate.
- **Retry-After** is honoured in delta-seconds and HTTP-date form (`email.utils`), raising the
  1/2/4/8/16 s ladder step, capped at 120 s. Attempts per request default to `max_attempts()`
  (five; `SDR_MAX_ATTEMPTS`).
- **Run dirs** must be a strict descendant of `runs/` (PROTOCOL.md section 14) or of `tests/`
  (fixture runs); `resolve_run_dir` raises for the review root, `runs/` itself or anything else.
- **CLI**: `python -m sdr.common init --dry-run` prints the layout and writes nothing;
  `check` takes `--limit N` (first N probes), `--dry-run` (secret-stripped probe list, no
  network) and an optional `--run-dir R --run-date D` pair (probes logged and cached there).
- **`sdr.ids`**: `norm_pmid` and `norm_pmcid` are anchored (the whole value must be a PMID/PMCID
  or a pubmed/PMC URL; `0`, a DOI or a title yield None); `norm_title` keeps every Unicode
  alphanumeric after NFKC, not only ASCII (PROTOCOL.md 7.1 "alphanumerics only" read literally),
  so non-English titles compare as themselves. Worked examples are frozen in `tests/test_ids.py`.
