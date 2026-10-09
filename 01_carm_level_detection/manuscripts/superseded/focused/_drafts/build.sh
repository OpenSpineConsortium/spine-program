#!/bin/bash
# Build the focused deployment paper. Run from paper/focused/_drafts/. Uses whatever TeX engine the host has, in
# order of preference, and refuses to pretend a build succeeded: the page count and the unresolved-reference
# count are printed from the log, because a LaTeX run emits a PDF on top of a broken table.
set -u
cd "$(dirname "$0")"
if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error deployment.tex
elif command -v pdflatex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode deployment.tex && bibtex deployment && pdflatex -interaction=nonstopmode deployment.tex && pdflatex -interaction=nonstopmode deployment.tex
elif command -v tectonic >/dev/null 2>&1; then
  tectonic deployment.tex
else
  echo "no TeX engine (latexmk / pdflatex / tectonic) on this host"; exit 2
fi
rc=$?
echo "----- build rc=$rc"
[ -f deployment.log ] && {
  echo "pages: $(grep -o 'Output written on deployment.pdf ([0-9]* pages' deployment.log | grep -o '[0-9]* pages')"
  echo "undefined references: $(grep -c 'Reference .* undefined\|Citation .* undefined' deployment.log)"
  echo "overfull boxes: $(grep -c 'Overfull' deployment.log)"
}
exit $rc
