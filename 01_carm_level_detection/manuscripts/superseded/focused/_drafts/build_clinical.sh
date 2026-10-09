#!/bin/bash
# Build the focused clinical paper (clinical.tex). Copied from paper/rsnai/build.sh and given its own name
# because several drafts share this directory and a shared build.sh gets overwritten. Uses whatever TeX
# engine the host has, and refuses to pretend a build succeeded: the page count and the unresolved-reference
# count are printed from the log, because a LaTeX run emits a PDF on top of a broken table.
set -u
cd "$(dirname "$0")"
DOC=clinical
if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error "$DOC.tex"
elif command -v pdflatex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode "$DOC.tex" && bibtex "$DOC" && pdflatex -interaction=nonstopmode "$DOC.tex" && pdflatex -interaction=nonstopmode "$DOC.tex"
elif command -v tectonic >/dev/null 2>&1; then
  tectonic "$DOC.tex"
else
  echo "no TeX engine (latexmk / pdflatex / tectonic) on this host"; exit 2
fi
rc=$?
echo "----- build rc=$rc"
[ -f "$DOC.log" ] && {
  echo "pages: $(grep -o "Output written on $DOC.pdf ([0-9]* pages" "$DOC.log" | grep -o '[0-9]* pages')"
  echo "undefined references: $(grep -c 'Reference .* undefined\|Citation .* undefined' "$DOC.log")"
  echo "overfull boxes: $(grep -c 'Overfull' "$DOC.log")"
}
exit $rc
