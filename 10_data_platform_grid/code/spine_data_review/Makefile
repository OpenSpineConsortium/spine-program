# spine_data_review/Makefile — every stage of the review as one target, in pipeline order.
#
# Run inside WSL (the network stages must; PROTOCOL.md section 15), from this directory:
#   make all RUN_DATE=2026-09-21          the full review into runs/2026-09-21 (or: bash run_all.sh --run-date ...)
#   make smoke RUN_DATE=2026-09-21        --limit 5 through every stage into runs/smoke; nothing under
#                                         charting/, analysis/, tables/, figures/, manuscript/, recipe/ is touched
#                                         (any LIMIT run keeps chart-check's outputs under its run directory)
#   make <stage> RUN_DATE=... [LIMIT=N]   one stage; stages: protocol-check search check-run replay-check dedup
#                                         chart-check availability quality stats figures manuscript recipe
#   make replay-check RUN_DATE=...        replay the run from its own raw cache into <run>-replay and diff the two
#   make <stage> RUN_DATE=... REPLAY=1   the same stage served from its own raw/ cache (--replay), offline
# RUN_DATE=YYYY-MM-DD is required by every stage (PROTOCOL.md section 15: the run date is --run-date,
# never the wall clock); only help, creds-check and clean-smoke run without it. Other variables:
# PY (the venv python), RUN_DIR (default runs/$(RUN_DATE)), LIMIT, REPLAY, and the output locations below,
# which the smoke target points into runs/smoke/. AVAIL_FLAGS=--apply copies an agreed access route
# into the charting records on the second probe pass (>= 48 h after the first); AVAIL_FLAGS=--from-known-items
# probes screen/known_items.csv before any record is charted.
# Three defaults follow LIMIT, because a --limit run cannot satisfy what the full run must:
#   MANUSCRIPT_FLAGS  --strict unless LIMIT is set, so the real run's build fails on a pending or unused
#                     macro (PROTOCOL.md 13(b)) while a limited chain, whose analyses are pending by
#                     construction, still reaches the recipe stage. MANUSCRIPT_FLAGS=--strict forces it back.
#   STATS_FLAGS       --check-flow unless LIMIT is set, so a PRISMA flow identity that does not hold stops
#                     the real run before the manuscript prints it (statistical_analysis_plan.md A1). A
#                     --limit run legitimately fails that identity: prescreen_audit.csv and the chase
#                     records it counts are not produced by a limited search.
#   SDR_MAX_ATTEMPTS  2 HTTP attempts per request instead of the five of PROTOCOL.md 15, so a source that
#                     times out is logged and skipped in seconds, not minutes.
# PIPELINE.md states what each stage reads and writes.
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
PY ?= $(HOME)/sdr_venv/bin/python
RUN_DATE ?=
RUN_DIR ?= runs/$(RUN_DATE)
LIMIT ?=
LIMIT_FLAG = $(if $(LIMIT),--limit $(LIMIT),)
# REPLAY=1 serves every request from <run>/raw/ and fails on a miss: the offline reproduction of a run.
REPLAY ?=
COMMON = --run-dir $(RUN_DIR) --run-date $(RUN_DATE) $(LIMIT_FLAG) $(if $(REPLAY),--replay,)
ANALYSIS_DIR ?= analysis
TABLES_DIR ?= tables
FIGURES_DIR ?= figures
MAIN_OUT ?= manuscript/main.tex
PROBES_DIR ?= charting/probes
RECIPE_OUT ?= recipe
# A LIMIT run of chart-check writes its two outputs under $(RUN_DIR)/charting/ (sdr.chart slices by
# --limit, so the committed charting/datasets.jsonl is only ever written by an unlimited run).
CHART_FLAGS ?= $(if $(LIMIT),--out $(RUN_DIR)/charting/datasets.jsonl --report $(RUN_DIR)/charting/validation_report.json,)
AVAIL_FLAGS ?=
QUALITY_FLAGS ?=
STATS_FLAGS ?= $(if $(LIMIT),,--check-flow)
MANUSCRIPT_FLAGS ?= $(if $(LIMIT),,--strict)
RECIPE_FLAGS ?=
SEARCH_SOURCES ?= all
# HTTP attempts per request (sdr.common.RateLimitedSession.get): 2 on a LIMIT run, else the protocol's 5.
export SDR_MAX_ATTEMPTS = $(if $(LIMIT),2,5)

.PHONY: all smoke run-date protocol-check creds-check search search-literature search-repositories check-run \
        replay-check dedup chart-check availability quality stats figures manuscript recipe clean-smoke help

all: protocol-check search check-run dedup chart-check availability quality stats figures manuscript recipe
	@echo "== all stages done for run $(RUN_DIR) (run date $(RUN_DATE))"

help:
	@sed -n '/^# spine_data_review/,/^SHELL/p' Makefile | sed '$$d'

# Every stage depends on this: no default date, and the form is checked before anything is written.
run-date:
	@[[ "$(RUN_DATE)" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$$ ]] || { echo "RUN_DATE=YYYY-MM-DD is required (got '$(RUN_DATE)'); the run date is never the wall clock" >&2; exit 2; }

# Offline checks that the frozen protocol files and the code agree: the verbatim query strings load
# from information_sources.md and both YAML files, the schema parses, every self-test passes, every
# module's --dry-run plan prints. Creates <run>/run_meta.json (`sdr.common init`: run date, package
# versions, credential NAMES present, redacted argv) and then runs creds-check, whose keyed probes need
# the network; a failed probe is printed, not fatal, because every query records its own credential_mode.
protocol-check: run-date
	$(PY) -c "import json; from sdr.common import load_queries as L, review_root as R; \
	  n = (len(L()), len(L('queries/literature.yaml')), len(L('queries/repositories.yaml'))); \
	  s = json.load(open(R() / 'charting_schema.json', encoding='utf-8')); \
	  print('queries: markdown %d, literature.yaml %d, repositories.yaml %d; schema properties %d, x-requires-quote %d' % (*n, len(s['properties']), len(s['x-requires-quote'])))"
	$(PY) -m sdr.dedup_prescreen --selftest --run-dir $(RUN_DIR) --run-date $(RUN_DATE) | tail -1
	$(PY) -m sdr.quality --selftest --run-dir $(RUN_DIR) --run-date $(RUN_DATE)
	$(PY) -m sdr.stats --selftest --run-dir $(RUN_DIR) --run-date $(RUN_DATE)
	$(PY) recipe/prepare_splits.py --self-test
	$(PY) tests/test_queries_yaml.py --run-dir $(RUN_DIR) | tail -1
	$(PY) -m sdr.search_literature $(COMMON) --dry-run >/dev/null && echo "search_literature: dry-run plan ok"
	$(PY) -m sdr.search_repositories $(COMMON) --dry-run | tail -1
	$(PY) -m sdr.chart $(COMMON) $(CHART_FLAGS) --dry-run | tail -1
	$(PY) -m sdr.recipe $(COMMON) --dry-run | tail -1
	$(PY) -m sdr.manuscript $(COMMON) --dry-run --analysis-dir $(ANALYSIS_DIR) --tables-dir $(TABLES_DIR) --figures-dir $(FIGURES_DIR) --main-out $(MAIN_OUT) | head -1
	$(PY) -m sdr.common init --run-dir $(RUN_DIR) --run-date $(RUN_DATE)
	$(MAKE) --no-print-directory creds-check || echo "creds-check: a keyed probe did not answer 200 (above); the key is still used where present -- queries.json records the mode actually used per query"

# Credential names present and one harmless keyed request per service (network; never prints a value).
creds-check:
	$(PY) -m sdr.common check

search: search-literature search-repositories

search-literature: run-date
	$(PY) -m sdr.search_literature $(COMMON)

# `all` runs the twenty adapters and ends with the mention harvests, which read the other records.
search-repositories: run-date
	$(PY) -m sdr.search_repositories $(COMMON) --source $(SEARCH_SOURCES)

# Audit of the run directory after the search (tests/check_run.py): log fields and redaction, log
# against raw cache, no credential value anywhere, the verbatim-string rule (queries.json[qid].query_string
# equals queries/*.yaml), a source that did not answer saying so in its notes, paging, wall-clock dates.
# Exit 1 on secrets, log-cache, log-fields, strings, no-answer or wallclock; paging is printed only.
check-run: run-date
	$(PY) tests/check_run.py --run-dir $(RUN_DIR) --run-date $(RUN_DATE) $(LIMIT_FLAG)

# The byte-identity claim of README: replay $(RUN_DIR) from its own raw cache into $(RUN_DIR)-replay and
# diff records, queries and counts. No network (a cache miss raises ReplayMiss), so it also proves the cache
# is complete - which it was not while failed requests wrote no envelope.
replay-check: run-date
	rm -rf $(RUN_DIR)-replay && mkdir -p $(RUN_DIR)-replay
	cp -r $(RUN_DIR)/raw $(RUN_DIR)-replay/raw
	$(PY) -m sdr.common init --run-dir $(RUN_DIR)-replay --run-date $(RUN_DATE)
	$(PY) -m sdr.search_repositories --run-dir $(RUN_DIR)-replay --run-date $(RUN_DATE) $(LIMIT_FLAG) --replay --source $(SEARCH_SOURCES)
	$(PY) tests/diff_runs.py $(RUN_DIR) $(RUN_DIR)-replay

dedup: run-date
	$(PY) -m sdr.dedup_prescreen $(COMMON)

# Exit 1 on any invalid charting record: the gate before every stage that reads charting/datasets/.
# With LIMIT the outputs go under $(RUN_DIR)/charting/ (CHART_FLAGS above); an explicit CHART_FLAGS
# that keeps the default --out with a LIMIT is refused, because it would truncate the committed file.
chart-check: run-date
	$(if $(and $(LIMIT),$(if $(findstring --out,$(CHART_FLAGS)),,x)),$(error chart-check with LIMIT=$(LIMIT) would truncate charting/datasets.jsonl; CHART_FLAGS must carry --out and --report under a run directory))$(PY) -m sdr.chart $(COMMON) $(CHART_FLAGS)

availability: run-date
	$(PY) -m sdr.availability $(COMMON) --probes-dir $(PROBES_DIR) $(AVAIL_FLAGS)

quality: run-date
	$(PY) -m sdr.quality $(COMMON) --probes-dir $(PROBES_DIR) --out $(ANALYSIS_DIR)/quality.json --tex $(TABLES_DIR)/quality.tex $(QUALITY_FLAGS)

stats: run-date
	$(PY) -m sdr.stats $(COMMON) --quality $(ANALYSIS_DIR)/quality.json --analysis-dir $(ANALYSIS_DIR) --tables-dir $(TABLES_DIR) $(STATS_FLAGS)

figures: run-date
	$(PY) -m sdr.figures $(COMMON) --analysis-dir $(ANALYSIS_DIR) --figures-dir $(FIGURES_DIR)

# Render main.tex and the tables, then build the PDF; build.sh prints pages, unresolved references,
# pending macros/tables/figures and fails on an undefined macro or reference. The bare-digit rule
# (PROTOCOL.md 13(c)) reads manuscript/allowed_literals.txt; MANUSCRIPT_FLAGS (--strict on an unlimited run) adds 13(b).
manuscript: run-date
	$(PY) -m sdr.manuscript $(COMMON) --analysis-dir $(ANALYSIS_DIR) --tables-dir $(TABLES_DIR) --figures-dir $(FIGURES_DIR) --main-out $(MAIN_OUT) --check
	TABLES_DIR="$$(realpath --relative-to=$(dir $(MAIN_OUT)) $(TABLES_DIR))" FIGURES_DIR="$$(realpath --relative-to=$(dir $(MAIN_OUT)) $(FIGURES_DIR))" \
	  bash manuscript/build.sh $(MANUSCRIPT_FLAGS) $(dir $(MAIN_OUT))

recipe: run-date
	$(PY) -m sdr.recipe $(COMMON) --quality $(ANALYSIS_DIR)/quality.json --out $(RECIPE_OUT) $(RECIPE_FLAGS)

# End to end with --limit 5 in runs/smoke: probes the known items (no charting records are needed),
# generates the demo recipe, and keeps every output, the chart-check outputs included, under runs/smoke/
# so the real run's files are untouched (RUN_DIR is explicit, so the LIMIT defaults of CHART_FLAGS,
# STATS_FLAGS and MANUSCRIPT_FLAGS land there too; smoke clears no flag of its own).
smoke: run-date clean-smoke
	$(MAKE) all RUN_DIR=runs/smoke RUN_DATE=$(RUN_DATE) LIMIT=5 \
	  ANALYSIS_DIR=runs/smoke/analysis TABLES_DIR=runs/smoke/tables FIGURES_DIR=runs/smoke/figures \
	  MAIN_OUT=runs/smoke/manuscript/main.tex PROBES_DIR=runs/smoke/charting_probes RECIPE_OUT=runs/smoke/recipe \
	  AVAIL_FLAGS=--from-known-items RECIPE_FLAGS=--demo
	@echo "== smoke ok: runs/smoke (requests.log.jsonl, records/, merged.jsonl, charting/, analysis/, figures/, manuscript/main.pdf, recipe/)"

clean-smoke:
	rm -rf runs/smoke
