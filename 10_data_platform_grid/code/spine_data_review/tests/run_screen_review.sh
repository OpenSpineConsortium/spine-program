#!/usr/bin/env bash
# Adversarial smoke of the 'screen' module (sdr.dedup_prescreen + sdr.chart) on hand-built fixtures.
# Run inside WSL from spine_data_review/:  bash tests/run_screen_review.sh
# Steps: build fixtures; py_compile; selftest; --dry-run; two real runs into runs/review_screen with a
# planted fake credential in the environment; byte-diff of the outputs between the runs (retrieved_at
# ignored, though this module writes none); hand-count comparison; chart validation on the fixtures
# twice with a diff; grep every output for the planted value.
set -u
PY=${PY:-$HOME/sdr_venv/bin/python}
RUN=runs/review_screen
DATE=2026-09-19
FAKE=ZZFAKESECRET0001XX
export NCBI_API_KEY=$FAKE            # planted: must never appear in any file the module writes
cd "$(dirname "$0")/.."
mkdir -p tests/_out
echo "== fixtures"
$PY tests/make_screen_fixture.py && $PY tests/make_chart_fixture.py || exit 1
echo "== py_compile"
$PY -m py_compile sdr/dedup_prescreen.py sdr/chart.py && echo compile ok
echo "== selftest"
$PY -m sdr.dedup_prescreen --selftest --run-dir $RUN --run-date $DATE | tail -1
echo "== dry-run (no files may be written)"
rm -rf $RUN; mkdir -p $RUN/records; cp tests/fixtures/screen_run/records/*.jsonl $RUN/records/
$PY -m sdr.dedup_prescreen --run-dir $RUN --run-date $DATE --dry-run | head -3
ls $RUN
echo "== run 1"
$PY -m sdr.dedup_prescreen --run-dir $RUN --run-date $DATE > tests/_out/dedup_run1.log; echo "exit $?"
mkdir -p tests/_out/run1; cp $RUN/merged.jsonl $RUN/screening_sheet.csv $RUN/prisma_counts.json tests/_out/run1/
echo "== run 2"
$PY -m sdr.dedup_prescreen --run-dir $RUN --run-date $DATE > tests/_out/dedup_run2.log; echo "exit $?"
echo "== determinism diff (empty = identical)"
for f in merged.jsonl screening_sheet.csv prisma_counts.json; do
  diff <(grep -v retrieved_at tests/_out/run1/$f) <(grep -v retrieved_at $RUN/$f) > /dev/null && echo "  $f identical" || { echo "  $f DIFFERS"; diff tests/_out/run1/$f $RUN/$f | head; }
done
echo "== --limit 2 run into a second dir"
rm -rf ${RUN}_lim; mkdir -p ${RUN}_lim/records; cp tests/fixtures/screen_run/records/*.jsonl ${RUN}_lim/records/
$PY -m sdr.dedup_prescreen --run-dir ${RUN}_lim --run-date $DATE --limit 2 | head -4
echo "== hand-count comparison"
$PY tests/check_screen_counts.py --run-dir $RUN; echo "check exit $?"
echo "== chart: dry-run then two real runs on the fixtures"
$PY -m sdr.chart --run-dir $RUN --run-date $DATE --charting-dir tests/fixtures/chart_screen --dry-run > tests/_out/chart_dry.log; echo "dry exit $?"
$PY -m sdr.chart --run-dir $RUN --run-date $DATE --charting-dir tests/fixtures/chart_screen --out tests/_out/chart_datasets.jsonl --report tests/_out/chart_report.json --allow-invalid > tests/_out/chart_run1.log; echo "run1 exit $?"
cp tests/_out/chart_report.json tests/_out/chart_report_run1.json; cp tests/_out/chart_datasets.jsonl tests/_out/chart_datasets_run1.jsonl
$PY -m sdr.chart --run-dir $RUN --run-date $DATE --charting-dir tests/fixtures/chart_screen --out tests/_out/chart_datasets.jsonl --report tests/_out/chart_report.json > tests/_out/chart_run2.log; echo "run2 exit (expected 1: invalid fixtures present) $?"
diff tests/_out/chart_report_run1.json tests/_out/chart_report.json > /dev/null && echo "  chart report identical" || echo "  chart report DIFFERS"
diff tests/_out/chart_datasets_run1.jsonl tests/_out/chart_datasets.jsonl > /dev/null && echo "  chart datasets identical" || echo "  chart datasets DIFFERS"
$PY tests/check_chart_report.py --report tests/_out/chart_report.json; echo "chart check exit $?"
echo "== planted credential scan (no line may print)"
grep -rl "$FAKE" $RUN ${RUN}_lim tests/_out 2>/dev/null && echo "  LEAK" || echo "  no leak"
echo "== run_meta credential names"
grep -A6 credentials_present $RUN/run_meta.json | head -8
