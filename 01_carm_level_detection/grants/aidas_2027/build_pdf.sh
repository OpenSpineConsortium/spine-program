#!/usr/bin/env bash
# Build the AIDaS packet from latex/main.tex with pdflatex, in a temporary directory so the tree stays clean.
#
# With nothing beside main.tex it writes the committed draft, AIDaS_SEED_2027_packet.pdf: 8 pages, the cover, the
# three-page narrative, the alignment page, the budget page and one placeholder page for each biosketch.
# With latex/contacts.tex and both biosketches (latex/biosketch_han.pdf, latex/biosketch_schwiebert.pdf) it writes
# AIDaS_SEED_2027_submission.pdf: 10 pages, the same six and the two biosketches of two pages each, the one PDF the
# call asks for. A submission build refuses to start while any of the three files is missing, while a biosketch is
# not two pages, or while main.tex or contacts.tex still holds a [DATA NEEDED] mark (\tbd); it writes the PDF only
# once every check has passed, so a failed build never leaves a PDF that looks finished. That file carries faculty
# e-mail addresses, so .gitignore keeps it out of git (root CLAUDE.md rule 12). Overleaf builds the same main.tex
# with no script and none of these checks.
#
# Needs pdflatex (TeX Live with helvet, sansmath, pdfpages, tabularx, booktabs, enumitem, titlesec, caption,
# multicol, microtype and hyperref) and pdfinfo. Run from any directory, on a laptop or as an sbatch job, never on
# the grid's login node.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
latex="$here/latex"
biosketches=("$latex/biosketch_han.pdf" "$latex/biosketch_schwiebert.pdf")

fail() {
  echo "$1" >&2
  exit 1
}

pages_of() {
  pdfinfo "$1" | awk '/^Pages:/ {print $2}'
}

# Any one of the three files beside main.tex makes this a submission build, which needs all three.
check_submission_inputs() {
  local missing=()
  [[ -f "$latex/contacts.tex" ]] || missing+=("contacts.tex")
  for sketch in "${biosketches[@]}"; do
    [[ -f "$sketch" ]] || missing+=("$(basename "$sketch")")
  done
  if (( ${#missing[@]} )); then
    fail "a submission build needs contacts.tex and both biosketches beside main.tex; missing: ${missing[*]}"
  fi
  for sketch in "${biosketches[@]}"; do
    [[ "$(pages_of "$sketch")" == 2 ]] || fail "$(basename "$sketch") is not two pages; the call allows two each"
  done
  if grep -n '\\tbd{' "$latex/contacts.tex"; then
    fail "contacts.tex still holds the [DATA NEEDED] marks above; fill them first"
  fi
  # The fallback contact lines main.tex provides are replaced by contacts.tex, and a comment prints nothing, so
  # neither counts.
  if grep -n '\\tbd{' "$latex/main.tex" | grep -v -E '\\providecommand|^[0-9]+:[[:space:]]*%'; then
    fail "main.tex still holds the [DATA NEEDED] marks above; fill them first (RECORD.md section 3)"
  fi
}

submission=0
for input in "$latex/contacts.tex" "${biosketches[@]}"; do
  [[ -f "$input" ]] && submission=1
done
if (( submission )); then
  check_submission_inputs
  name="AIDaS_SEED_2027_submission.pdf"
  expected=10
else
  name="AIDaS_SEED_2027_packet.pdf"
  expected=8
fi

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
cp -r "$latex/." "$work/"
cd "$work"
for pass in 1 2; do
  if ! pdflatex -interaction=nonstopmode -halt-on-error main.tex > build.log 2>&1; then
    tail -n 40 build.log >&2
    fail "pdflatex failed on pass $pass"
  fi
done
# A box that runs into the margin or a reference LaTeX could not resolve is shown, not hidden.
grep -E "^Overfull|LaTeX Warning: (Reference|Citation)" main.log || true

pages="$(pages_of main.pdf)"
if [[ "$pages" != "$expected" ]]; then
  fail "built $pages pages where $expected were expected: a section has spilled onto a page of its own; shorten it"
fi
mv main.pdf "$here/$name"
echo "wrote $here/$name: $pages pages"
