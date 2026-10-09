# data/ — what the reviewers type

Everything else in `spine_data_review/` is written by code. This directory holds the two kinds of
input a person produces, so that a diff of `data/` is a diff of human decisions.

## data/screening/decisions.csv

One row per screening decision (PROTOCOL.md 7.3), appended by the reviewer (or by `sdr/screen.py`
once it exists); `sdr/stats.py` reads it for the PRISMA flow, looking here first and under
`screen/` second.

| column | values |
|---|---|
| `record_id` | the merged record id from `<run-dir>/screening_sheet.csv` (`lit:` or `repo:` + 12 hex) |
| `stage` | `title-abstract`, `full-text`, `dual`, `resolution` |
| `reviewer` | initials |
| `date` | YYYY-MM-DD |
| `decision` | `include`, `exclude`, `unclear` |
| `primary_code` | first failing criterion in the order I1, I2, I3, I4, I5, E1, E2, E3, E4, E5, E6, E8, `use-only`; equal to the first entry of `codes`; empty on an include |
| `codes` | `;`-separated: I1–I8, E1–E6, E8, `use-only`, `prescreen-override` |
| `reason_text` | one sentence |
| `llm_suggestion` | the LLM's decision when the 7.4 step ran, else empty |
| `llm_agreed` | `yes` / `no` / empty |
| `prescreen_outcome` | copied from the screening sheet (`pass`, `uncertain`, `pass:non-english-route`, `fail:S|M|D` with `prescreen-override`) |
| `full_text_retrieved` | `yes` / `no` on a `full-text` row (a `no` is charted from the abstract and counted "not retrieved") |
| `arm` | `search` (default) or `other` (known items and citation chasing, the second PRISMA arm) |

The flow takes the `resolution` row as final when one exists, else the first `full-text` row, else
the `title-abstract` row. `dual` rows are the second reviewer's sample (SAP A8) and never decide.

## data/charting — how a charting record is made

Charting records themselves live where PROTOCOL.md section 14 and every module expect them,
`charting/datasets/<id>.json`, one file per dataset, `id` = file stem = the slug that names
`recipe/datasets/<id>.sh`. This README is the reviewer's procedure; the schema is the contract.

1. **Map records to a dataset** (7.6): add the dataset's aliases to `charting/aliases.csv`
   (`dataset_id, alias, source`) and one row per included record to
   `charting/dataset_sources.csv` (`dataset_id, record_id, role` with role in
   `primary-description`, `repository`, `version`, `use`, `derived-from`, `challenge-page`).
   `use` rows are counted into `n_use_records` by `sdr/chart.py`; they are not included records.
2. **Draft the record** against `charting_schema.json`. Every field listed in the schema's
   `x-requires-quote` needs either a `quotes[]` entry whose `field` is the dotted path (verbatim
   sentence, source, locator) or a `field_sources` entry that starts with `api:` (the value came
   from a repository API, kept in `charting/enrichment/<id>.json`). An LLM may draft a chart
   (7.4; prompts under `screen/llm/prompts/`, outputs under `screen/llm/`); a drafted chart is
   unverified until each field has its quote or API source.
3. **Probe access** (section 10): `make availability` writes `charting/probes/<id>.json`; run it
   again at least 48 hours later with `AVAIL_FLAGS=--apply` to copy the agreed `access_route`,
   `access_route_rule`, `host_type` and `access_probe[]` into the record. A `verifier:` rule in
   `access_route_rule` is never overwritten.
4. **Licence, host, comparable group** are checked by rule: `licence.tier/spdx/standard` must be
   the first matching row of `licence_tiers.csv`; `host_type` the section-10 host table value for
   `access_url`; `annotation_validation.comparable_group` the SAP A6.0 lookup. `make chart-check`
   prints the exact expected value on a mismatch.
5. **Blind re-chart** (section 8): the second reviewer's copies go to `charting/rechart/<id>.json`
   with their own `charted_date`; pass `--rechart-dir charting/rechart` to `sdr.chart` and the
   build asserts each re-chart predates `verified_date`.
6. **Verify**: fill `verified_by` and `verified_date`. Unverified records validate with a warning
   and are excluded from analysis by `make quality QUALITY_FLAGS=--verified-only`.
7. `make chart-check` (exit 1 on any error) gates `quality`, `stats`, `figures`, `manuscript` and
   `recipe`; all of them read `charting/datasets/*.json` directly, so a record that fails
   validation must be fixed or removed before those targets are meaningful.
   Never run it with `LIMIT` expecting the committed `charting/datasets.jsonl`: `sdr.chart --limit N`
   keeps the first N records only, so the Makefile sends a `LIMIT` run's outputs to `<run>/charting/`.
