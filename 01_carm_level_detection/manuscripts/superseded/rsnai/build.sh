#!/bin/bash
# Build the RSNA-structure manuscript. Run from paper/rsnai/. Uses whatever TeX engine the host has, in
# order of preference, and refuses to pretend a build succeeded: the page count and the unresolved-reference
# count are printed from the log, because a LaTeX run emits a PDF on top of a broken table.
set -u
cd "$(dirname "$0")"
if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
elif command -v pdflatex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode main.tex && bibtex main && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex
elif command -v tectonic >/dev/null 2>&1; then
  tectonic main.tex
else
  echo "no TeX engine (latexmk / pdflatex / tectonic) on this host"; exit 2
fi
rc=$?
echo "----- build rc=$rc"
[ -f main.log ] && {
  echo "pages: $(grep -o 'Output written on main.pdf ([0-9]* pages' main.log | grep -o '[0-9]* pages')"
  echo "undefined references: $(grep -c 'Reference .* undefined\|Citation .* undefined' main.log)"
  echo "overfull boxes: $(grep -c 'Overfull' main.log)"
}
exit $rc
