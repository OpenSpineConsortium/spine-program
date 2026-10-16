#!/usr/bin/env bash
# Build the AIDaS packet twice in the scratchpad: build3 with the example contact lines, build4 with the real ones
# (contacts.tex and the biosketches, never committed), and print each build's pages, overfull lines and slack.
set -euo pipefail
here=/home/user/spine-program/01_carm_level_detection/grants/aidas_2027
sp=/tmp/claude-0/-home-user/e6d88dbd-5c62-5bda-9b36-249fae0bf6ea/scratchpad
for build in build3 build4; do
  dir="$sp/$build"
  rm -rf "$dir/figures" "$dir"/main.*
  mkdir -p "$dir/figures"
  cp "$here/latex/main.tex" "$here/latex/contacts.example.tex" "$dir/"
  cp "$here/latex/figures/"*.pdf "$dir/figures/"
  cp "$here/latex/biosketch_han.pdf" "$here/latex/biosketch_schwiebert.pdf" "$dir/"
  if [[ "$build" == build4 ]]; then cp "$here/latex/contacts.tex" "$dir/"; else rm -f "$dir/contacts.tex"; fi
  for pass in 1 2; do
    (cd "$dir" && pdflatex -interaction=nonstopmode -halt-on-error main.tex > build.log 2>&1) || { tail -30 "$dir/build.log"; exit 1; }
  done
  echo "== $build: $(pdfinfo "$dir/main.pdf" | awk '/^Pages:/ {print $2}') pages; overfull: $(grep -c 'Overfull' "$dir/main.log" || true); marks: $(pdftotext "$dir/main.pdf" - | grep -o 'DATA NEEDED' | wc -l)"
  python3 "$here/review/page_slack.py" "$dir/main.pdf" > "$dir/slack.txt"; sed -n 1,6p "$dir/slack.txt"
done
