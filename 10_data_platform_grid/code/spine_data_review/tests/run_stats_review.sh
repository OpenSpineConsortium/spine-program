#!/usr/bin/env bash
# Review driver for the stats module: build the fixture, run quality -> stats -> figures twice
# (runs/review_stats/a and /b), diff the two runs, then run the hand-calculation test.
# Run inside WSL from spine_data_review/:  bash tests/run_stats_review.sh
set -uo pipefail
PY=${PY:-$HOME/sdr_venv/bin/python}
RD=runs/review_stats
COMMON="--run-dir $RD --run-date 2026-09-19"
$PY tests/make_fixture.py || exit 1
for tag in a b; do
  out=$RD/$tag
  rm -rf "$out"
  echo "== quality ($tag)"
  $PY -m sdr.quality $COMMON --charting-dir tests/fixtures/stats/charting --probes-dir tests/fixtures/stats/probes \
     --out $out/analysis/quality.json --tex $out/tables/quality.tex || echo "quality rc=$?"
  echo "== stats ($tag)"
  $PY -m sdr.stats $COMMON --charting-dir tests/fixtures/stats/charting --quality $out/analysis/quality.json \
     --screen-dir tests/fixtures/stats/screening --decisions-dir tests/fixtures/stats/screening \
     --analysis-dir $out/analysis --tables-dir $out/tables --check-flow; echo "stats rc=$?"
  echo "== figures ($tag)"
  $PY -m sdr.figures $COMMON --analysis-dir $out/analysis --figures-dir $out/figures; echo "figures rc=$?"
done
echo "== diff a vs b (byte-level, all outputs)"
diff -rq $RD/a $RD/b && echo "identical" || true
echo "== diff a vs b (PDF, ignoring CreationDate/ModDate lines)"
for f in $RD/a/figures/*.pdf; do
  g=$RD/b/figures/$(basename "$f")
  if cmp -s <(grep -av 'CreationDate\|ModDate' "$f") <(grep -av 'CreationDate\|ModDate' "$g"); then echo "  same modulo dates: $(basename "$f")"; else echo "  DIFFERS beyond dates: $(basename "$f")"; fi
done
echo "== --limit 3 and --dry-run"
$PY -m sdr.quality $COMMON --charting-dir tests/fixtures/stats/charting --probes-dir tests/fixtures/stats/probes --limit 3 --dry-run
$PY -m sdr.stats $COMMON --charting-dir tests/fixtures/stats/charting --quality $RD/a/analysis/quality.json --limit 3 --dry-run
$PY -m sdr.figures $COMMON --analysis-dir $RD/a/analysis --figures-dir $RD/limit3/figures --limit 3 --only forest
echo "== hand-calculation test"
$PY tests/test_stats_module.py; echo "test rc=$?"
