#!/bin/bash
# Build manuscript/main.pdf with latexmk and refuse to pretend a build succeeded: LaTeX emits a PDF
# on top of a broken table, so the page count, the unresolved references and citations, the pending
# macros and the three macro checks of PROTOCOL.md section 13 -- (a) every \num… used is defined,
# (b) every defined macro is used, (c) no bare digit in the Abstract or Results outside a macro,
# citation, label, reference or manuscript/allowed_literals.txt -- are printed from the log and the
# sources, and the exit code reflects them. (c) is `python -m sdr.manuscript --scan main.tex`, the
# same check the renderer's --check runs, so the two cannot drift. Run from anywhere; render first with
#   python -m sdr.manuscript --run-dir runs/<date> --run-date <date>
# Flags: --strict also fails on defined-but-unused macros, on any pending macro, table or figure, on an
# overfull box wider than OVERFULL_MAX_PT (a table cell printing into its neighbour or the margin), and on
# a run whose recorded query metadata disagrees with queries/*.yaml (the Makefile passes it for the real
# run and clears it for the smoke run).
# Usage: bash manuscript/build.sh [--strict] [DIR]   DIR holds main.tex (default: this directory;
# the Makefile's smoke target renders into runs/smoke/manuscript). TABLES_DIR and FIGURES_DIR
# (relative to DIR; default ../tables and ../figures) name where sdr.manuscript put the tables and
# where the figures are, matching its --tables-dir / --figures-dir. refs.bib is copied in when absent.
# PY names the python with the sdr package importable (default ~/sdr_venv/bin/python, else python3);
# it runs the query-file check before the build and the bare-digit scan after it.
set -u
strict=0; dir=""; here="$(cd "$(dirname "$0")" && pwd)"; root="$(cd "$here/.." && pwd)"
for arg in "$@"; do case "$arg" in --strict) strict=1;; *) dir=$arg;; esac; done
cd "${dir:-$here}" || exit 2
TABLES="${TABLES_DIR:-../tables}"; FIGURES="${FIGURES_DIR:-../figures}"
# The widest overfull box the tables are allowed to produce, in points. Recorded, not guessed: the builds
# that set it had 6 and 11 boxes, widest 4.38pt, a \texttt{RateLimitedSession.} token in the deviations log
# that no column width will hold. Raise it only with the cell that needs it named in the commit; the count
# alone is not the gate, because one wide box can replace two narrow ones and read as an improvement.
OVERFULL_MAX_PT="${OVERFULL_MAX_PT:-5.0}"; over_bad=0
[ -f main.tex ] || { echo "main.tex missing in $PWD: run python -m sdr.manuscript first"; exit 2; }
[ -f "$TABLES/numbers.tex" ] || { echo "$TABLES/numbers.tex missing: run python -m sdr.manuscript first"; exit 2; }
[ -f refs.bib ] || cp "$here/refs.bib" .

# ---- the query files the appendix prints must match information_sources.md (tests/test_queries_yaml.py;
# fatal). The same test's verdict on the run's recorded metadata against the YAML (the run dir is read
# from the header sdr.manuscript wrote into main.tex) is the check-run stage's business: printed here,
# fatal only under --strict, so a smoke run's adapter mismatches do not stop a build of its manuscript.
PY="${PY:-$HOME/sdr_venv/bin/python}"; command -v "$PY" >/dev/null 2>&1 || PY=python3
run_dir=$(sed -n '1s/.*run-dir \([^,]*\),.*/\1/p' main.tex)
if "$PY" "$root/tests/test_queries_yaml.py" >query_check.log 2>&1; then
  echo "queries: $(tail -1 query_check.log)"
else
  echo "queries: FAIL ($(tail -1 query_check.log)); see manuscript/query_check.log"; exit 2
fi
run_q_rc=0
if [ -n "$run_dir" ]; then
  "$PY" "$root/tests/test_queries_yaml.py" --run-dir "$root/$run_dir" >>query_check.log 2>&1 || run_q_rc=$?
  echo "queries vs run $run_dir: $(tail -1 query_check.log)$([ $run_q_rc -ne 0 ] && echo ' (advisory; fatal under --strict; see query_check.log)')"
fi

if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -file-line-error -halt-on-error main.tex >build.log 2>&1
elif command -v pdflatex >/dev/null 2>&1; then
  { pdflatex -interaction=nonstopmode main.tex && bibtex main && pdflatex -interaction=nonstopmode main.tex \
    && pdflatex -interaction=nonstopmode main.tex; } >build.log 2>&1
else
  echo "no TeX engine (latexmk / pdflatex) on this host"; exit 2
fi
rc=$?
echo "----- build rc=$rc (full log: manuscript/build.log, manuscript/main.log)"
[ $rc -ne 0 ] && grep -m 5 -E '^\./main\.tex:[0-9]+:|^!|\.tex:[0-9]+: ' main.log

# ---- what the log says
if [ -f main.log ]; then
  echo "pages: $(grep -o 'Output written on main.pdf ([0-9]* pages' main.log | grep -o '[0-9]* pages')"
  undef_ref=$(grep -c 'Reference .* undefined' main.log)
  undef_cit=$(grep -c 'Citation .* undefined' main.log)
  echo "undefined references: $undef_ref   undefined citations: $undef_cit"
  grep -oE "(Reference|Citation) \`[^']*'" main.log | sort -u | sed 's/^/  /'
  # An overfull box is a cell whose longest word does not fit its column: the word prints into the
  # neighbouring column or into the margin. The count alone let the widest box drift upwards unnoticed,
  # so the widest is measured and compared with OVERFULL_MAX_PT (recorded here, raised only deliberately).
  n_over=$(grep -c 'Overfull' main.log)
  over_pt=$(grep -o 'Overfull \\[hv]box ([0-9.]*pt' main.log | grep -o '[0-9.]*' | sort -g | tail -1)
  over_pt=${over_pt:-0}
  echo "overfull boxes: $n_over   widest: ${over_pt}pt (limit ${OVERFULL_MAX_PT}pt)   unicode errors: $(grep -c 'Unicode character' main.log)"
  if awk -v a="$over_pt" -v b="$OVERFULL_MAX_PT" 'BEGIN{exit !(a+0 > b+0)}'; then
    over_bad=1
    grep -A1 'Overfull' main.log | grep -m 3 -A1 "Overfull ..box ($over_pt" | sed 's/^/  WIDEST: /'
  fi
fi

# ---- macro consistency (PROTOCOL.md section 13 (a), (b)): every \num… used is defined; every defined is used.
# \numX and \numwordX are two forms of one number, so both are compared by the base name numX.
defined=$(grep -o '\\newcommand{\\num[A-Za-z]*}' "$TABLES/numbers.tex" | sed 's/\\newcommand{\\//; s/}//; s/^numword/num/' | sort -u)
used=$(cat main.tex "$TABLES"/*.tex | grep -v '^%' | grep -o '\\num[A-Za-z]*' | sed 's/^\\//; s/^numword/num/' | grep -v '^num$' | sort -u)
undef=$(comm -13 <(echo "$defined") <(echo "$used"))
unused=$(comm -23 <(echo "$defined") <(echo "$used"))
n_undef=$(echo "$undef" | grep -c .); n_unused=$(echo "$unused" | grep -c .)
echo "macros: defined $(echo "$defined" | grep -c .)  used $(echo "$used" | grep -c .)  undefined-used $n_undef  defined-unused $n_unused"
[ "$n_undef" -gt 0 ] && echo "$undef" | sed 's/^/  UNDEFINED: /'
[ "$n_unused" -gt 0 ] && echo "$unused" | sed 's/^/  unused: /' | head -20

# ---- bare digits (PROTOCOL.md section 13 (c)), by the renderer's own check on the rendered file
main_abs="$PWD/main.tex"
(cd "$root" && "$PY" -m sdr.manuscript --scan "$main_abs"); scan_rc=$?
[ "$scan_rc" -eq 0 ] || echo "bare-digit scan failed (rc=$scan_rc); allow-list: manuscript/allowed_literals.txt"

# ---- pending markers (values not yet produced by the analysis run)
n_pending=$(grep -o '\\pending{[^}]*}' "$TABLES/numbers.tex" | sort -u | grep -c .)
n_ptab=$(cat "$TABLES"/*.tex main.tex | grep -c '\\pendingtable{')
n_pfig=$(grep -c '\\pendingfigure{' main.tex)
echo "pending: macros $n_pending  tables $n_ptab  figures $n_pfig"

fail=0
[ $rc -ne 0 ] && fail=1
[ "$n_undef" -gt 0 ] && fail=1
[ "$scan_rc" -ne 0 ] && fail=1
[ "${undef_ref:-0}" -gt 0 ] || [ "${undef_cit:-0}" -gt 0 ] && fail=1
if [ $strict -eq 1 ]; then
  { [ "$n_unused" -gt 0 ] || [ "$n_pending" -gt 0 ] || [ "$n_ptab" -gt 0 ] || [ "$n_pfig" -gt 0 ] || [ "$run_q_rc" -ne 0 ] \
    || [ "$over_bad" -ne 0 ]; } && fail=1
fi
echo "----- result: $([ $fail -eq 0 ] && echo OK || echo FAIL)"
exit $fail
