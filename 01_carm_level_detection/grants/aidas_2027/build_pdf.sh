#!/usr/bin/env bash
# Build the AIDaS packet from latex/main.tex with pdflatex, in a temporary directory so the tree stays clean.
#
# Without contacts.tex or a biosketch beside main.tex it writes the committed draft, AIDaS_SEED_2027_packet.pdf:
# 7 pages, the cover, the three-page narrative, the alignment page, the budget page and the biosketch placeholder.
# With latex/contacts.tex and both biosketches (latex/biosketch_han.pdf, latex/biosketch_schwiebert.pdf) it writes
# AIDaS_SEED_2027_submission.pdf: 10 pages, the same six and the two biosketches of two pages each, the one PDF the
# call asks for. That file carries faculty e-mail addresses, so .gitignore keeps it out of git (root CLAUDE.md
# rule 12). Overleaf builds the same main.tex with no script.
#
# Needs pdflatex (TeX Live with helvet, sansmath, pdfpages, tabularx, booktabs, enumitem, titlesec, caption,
# multicol, microtype and hyperref) and pdfinfo. Run from any directory, on a laptop or as an sbatch job, never on
# the grid's login node.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
latex="$here/latex"

han=0; schwiebert=0; contacts=0
[[ -f "$latex/biosketch_han.pdf" ]] && han=1
[[ -f "$latex/biosketch_schwiebert.pdf" ]] && schwiebert=1
[[ -f "$latex/contacts.tex" ]] && contacts=1
if (( han != schwiebert )); then
  echo "put both biosketches beside main.tex, or neither: the call wants the PI's and the Co-PI's" >&2
  exit 1
fi

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
cp -r "$latex/." "$work/"
cd "$work"
for pass in 1 2; do
  if ! pdflatex -interaction=nonstopmode -halt-on-error main.tex > build.log 2>&1; then
    tail -n 40 build.log >&2
    echo "pdflatex failed on pass $pass" >&2
    exit 1
  fi
done
# A box that runs into the margin or a reference LaTeX could not resolve is shown, not hidden.
grep -E "^Overfull|LaTeX Warning: (Reference|Citation)" main.log || true

if (( contacts || han )); then
  name="AIDaS_SEED_2027_submission.pdf"
else
  name="AIDaS_SEED_2027_packet.pdf"
fi
expected=$(( han ? 10 : 7 ))
cp main.pdf "$here/$name"
pages="$(pdfinfo "$here/$name" | awk '/^Pages:/ {print $2}')"
echo "wrote $here/$name: $pages pages"
if [[ "$pages" != "$expected" ]]; then
  echo "expected $expected pages: a section has spilled onto a page of its own; shorten it" >&2
  exit 1
fi
