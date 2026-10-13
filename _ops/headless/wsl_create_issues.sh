#!/bin/bash
# Create the board issues from the drafts: wsl_create_issues.sh <issues dir with INDEX.tsv> [<extra dir>]
# Each draft file is the Task form's body (### Goal / ### Acceptance / ### Files likely touched); title from INDEX.tsv or,
# for extras, from the first line "TITLE: ..." of a sidecar .title file. Writes CREATED.tsv (file, issue number, url).
set -u
export PATH=~/.local/bin:$PATH
tok=$(printf 'protocol=https\nhost=github.com\n' | git credential fill 2>/dev/null | sed -n 's/^password=//p')
export GH_TOKEN="$tok"; unset tok
T=OpenSpineConsortium/spine-program
DIR=$1; EXTRA=${2:-}
OUT=$DIR/CREATED.tsv; touch "$OUT"
# Folders the tree marks Greg-only (01, 02, 07, 08, 09, 99) or Greg-only until confirmed (10, 11): their -02/-03 tasks are
# created WITHOUT the todo label, so the board's queue does not offer them to a student before Greg confirms a hand-out
# (he adds the label to release one). Every -01 start-here issue gets todo and is claimed at once by Greg's own sessions.
GREG_ONLY="01_carm_level_detection 02_transitional_naming_truth 07_plain_film_level_id 08_render_devices 09_wrong_level_clinical_qi 99_archive 10_data_platform_grid 11_students_grid_access"
label_for() { # file -> "todo" or ""
  local b=$(basename "$1") folder; folder=${b%-0[0-9].md}
  case "$b" in *-0[1].md) echo todo; return;; esac
  for g in $GREG_ONLY; do [ "$g" = "$folder" ] && { echo ""; return; }; done
  echo todo
}
create() { # file title
  local f=$1 title=$2 lab
  if grep -q -F "$(basename "$f")	" "$OUT"; then echo "skip (created before): $(basename "$f")"; return; fi
  lab=$(label_for "$f"); labopt=(); [ -n "$lab" ] && labopt=(--label "$lab")
  url=$(gh issue create --repo $T --title "$title" "${labopt[@]}" --body-file "$f" 2>&1) || { echo "FAILED $f: $url"; return; }
  n=${url##*/}
  printf '%s\t%s\t%s\n' "$(basename "$f")" "$n" "$url" >> "$OUT"
  echo "#$n  [${lab:-no label}]  $title"
  sleep 2
}
if [ -n "$EXTRA" ]; then
  for f in "$EXTRA"/*.md; do
    [ -f "$f" ] || continue
    t=$(cat "${f%.md}.title" 2>/dev/null); [ -n "$t" ] || { echo "no .title for $f"; continue; }
    create "$f" "$t"
  done
fi
# INDEX.tsv: file, folder, title, labels, order
[ -f "$DIR/INDEX.tsv" ] && tail -n +2 "$DIR/INDEX.tsv" | sort -t$'\t' -k5,5n -k1,1 | while IFS=$'\t' read -r file folder title labels order; do
  [ -f "$DIR/$file" ] || { echo "missing $file"; continue; }
  create "$DIR/$file" "$title"
done
echo "---- created so far: $(wc -l < "$OUT")"
