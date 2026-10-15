#!/usr/bin/env bash
# Make the Overleaf project of the AIDaS packet: a zip with main.tex, its figures, contacts.tex and the two
# biosketches at its root, which Overleaf's Upload Project takes as it is and compiles with pdfLaTeX to the
# 10-page submission.
#
# The zip holds the tracked files under latex/ as the working tree holds them (an uncommitted edit is in, LaTeX's
# own outputs and other untracked files are out) and the three local files beside main.tex, which git never holds
# (root CLAUDE.md rule 12). The script refuses while one of the three is missing or a biosketch is not two pages,
# then unzips a copy and compiles it twice with pdflatex, as Overleaf will, and writes the zip to its path only
# once that copy is 10 pages: a run that fails or is interrupted leaves nothing there, and a zip left by an earlier
# run is removed first. Unlike a submission build of build_pdf.sh, it does not refuse a [DATA NEEDED] mark: the
# zip is where the marks get filled, on Overleaf, and the PDF built from it says in red what is still missing.
#
# Usage: bash make_overleaf_zip.sh [zip path], a path that ends in .zip. The default is
# AIDaS_SEED_2027_overleaf.zip under $TMPDIR, or /tmp, outside the tree; git ignores a zip written anywhere in the
# tree (the root .gitignore's *.zip, repeated in this folder's), since it carries e-mail addresses.
# Needs git, zip, unzip, pdflatex and pdfinfo. Run from any directory, on a laptop or as an sbatch job, never on
# the grid's login node.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
latex="$here/latex"
contacts="$latex/contacts.tex"
biosketches=("$latex/biosketch_han.pdf" "$latex/biosketch_schwiebert.pdf")
out="${1:-${TMPDIR:-/tmp}/AIDaS_SEED_2027_overleaf.zip}"
expected=10

fail() {
  echo "$1" >&2
  exit 1
}

pages_of() {
  pdfinfo "$1" | awk '/^Pages:/ {print $2}'
}

# A relative zip path is taken from where the script was called, not from the temporary directory. The name must
# end in .zip, since zip itself adds .zip to a name whose last part has no dot and would write another file than
# the one checked and reported here.
case "$out" in
  /*) ;;
  *) out="$PWD/$out" ;;
esac
[[ "$out" == *.zip ]] || fail "the zip path must end in .zip: $out"
# Nothing stays at the path but a zip this run has checked, so one left by an earlier run goes before the checks.
rm -f "$out"

missing=()
for file in "$contacts" "${biosketches[@]}"; do
  [[ -f "$file" ]] || missing+=("$(basename "$file")")
done
if (( ${#missing[@]} )); then
  fail "the zip needs contacts.tex and both biosketches beside main.tex; missing: ${missing[*]}"
fi
for sketch in "${biosketches[@]}"; do
  [[ "$(pages_of "$sketch")" == 2 ]] || fail "$(basename "$sketch") is not two pages; the call allows two each"
done

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
mkdir -p "$work/stage" "$work/test"
# The tracked files, with the latex/ prefix dropped so that main.tex sits at the zip's root, where Overleaf looks.
git -C "$here" ls-files -z -- latex | while IFS= read -r -d '' path; do
  file="${path#latex/}"
  mkdir -p "$work/stage/$(dirname "$file")"
  cp "$here/$path" "$work/stage/$file"
done
rm -f "$work/stage/.gitignore"
cp "$contacts" "${biosketches[@]}" "$work/stage/"
(cd "$work/stage" && zip -q -r -X "$work/out.zip" .)

# What Overleaf does with the upload: unzip it and run pdfLaTeX, twice for the references. The zip is still in the
# temporary directory, which the trap removes, so a failure or an interruption here writes nothing to the path.
(cd "$work/test" && unzip -q "$work/out.zip")
for pass in 1 2; do
  if ! (cd "$work/test" && pdflatex -interaction=nonstopmode -halt-on-error main.tex > build.log 2>&1); then
    tail -n 40 "$work/test/build.log" >&2
    fail "pdflatex failed on pass $pass; no zip was written"
  fi
done
# A box that runs into the margin or a reference LaTeX could not resolve is shown, not hidden.
grep -E "^Overfull|LaTeX Warning: (Reference|Citation)" "$work/test/main.log" || true
pages="$(pages_of "$work/test/main.pdf")"
if [[ "$pages" != "$expected" ]]; then
  fail "the zip's copy built $pages pages where $expected were expected; no zip was written"
fi
mv "$work/out.zip" "$out"
files="$(unzip -Z -1 "$out" | grep -c -v '/$')"
echo "wrote $out: $files files; its copy builds $pages pages"
