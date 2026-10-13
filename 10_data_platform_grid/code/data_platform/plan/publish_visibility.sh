#!/bin/bash
#SBATCH --job-name=dp_visibility
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --no-requeue
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=12:00:00
#SBATCH --output=logs/%x_%j.out
# Student visibility (Greg, 2026-10-08: "i want students to be able to see all of this data"). Approved
# students pass the gate on the volume root (their named ACL entry, kept by tools/grid_access.sh); below it,
# what they can read is decided by the "other" bits. This job sets them for the Ceph data folders:
#   open   = every source folder under $RS/data that is not a restricted folder: directories o+rx, files o+r
#            (execute kept where it exists), default ACL o::r-x so new content inherits;
#   closed = restricted sources (a named-person DUA or an EULA that forbids redistribution: VinDr-SpineXR,
#            BUU-LSPINE, and every bank that holds their pixels): mode 0700 throughout. A restricted bank that
#            lives inside an otherwise open folder (multisource_banks, spine_detector_corpus) is closed by its
#            own path after the folder is opened, so its neighbours stay readable.
# Which items are restricted comes from the plan: the `restricted` flag in plan/batch_items/*.tsv (exact
# destination paths) plus the fixed folder list below for folders that were on Ceph before the plan. Nothing
# is moved or deleted; only modes and default ACLs change. Idempotent. Run after each cut-over for that
# batch's folders (FOLDERS="deepfluoro_h5 ...") or once over everything (FOLDERS=ALL).
#
#   cd ~/spinesurg-ct-nnunet/data_platform/plan && mkdir -p logs
#   sbatch -D "$PWD" --export=ALL,FOLDERS=ALL publish_visibility.sh
#   sbatch -D "$PWD" --export=ALL,FOLDERS="deepfluoro_h5 versefusion" publish_visibility.sh
#   DRY=1 prints what would change and changes nothing.
set -u
RS=/rs/rs_grp_oschome/go2432
DATA=$RS/data
HERE=$(pwd)
FOLDERS=${FOLDERS:-ALL}
DRY=${DRY:-0}
case "$(hostname -s)" in warrior*) echo "REFUSING: not on the login node"; exit 97;; esac
[ -n "${SLURM_JOB_ID:-}" ] || { echo "REFUSING: run as an sbatch job"; exit 98; }
# whole folders closed whatever the plan says (on Ceph before the plan; VinDr's DUA and BUU's EULA)
# Until 2026-10-11 the BUU-LSPINE folders, VinDr-SpineXR, mendeley_5jdfdgp762 (a redistribution of BUU and VinDr,
# dedup/DEDUP_PLAN.md C08) and spine_detector_corpus (holds BUU films, dedup A21) were owner-only under the BUU EULA and
# the PhysioNet DUA. On 2026-10-11 Greg stated that all approved students hold the PhysioNet credential and these
# agreements ("all the students also have credentials for these"), so they open to the approved-student gate like the
# rest; the gate (named-user ACL entries on the volume root) still keeps every other grid user out. Put a folder back
# in this list to close it again.
FIXED_RESTRICTED=""
# exact paths closed whatever the plan says. On 2026-10-12 Greg stated "anyone can read anything, dont worry about
# tokens", so s1v11 (the v11 build workspace with its Zenodo upload scripts) is open without the token check.
# One path stays owner-only:
#  build_archive_private  its one file, annotator_map.json, maps annotator usernames to people: students' personal
#                         data (no student name or username is shared), not a dataset and not a token.
FIXED_RESTRICTED_PATHS="$DATA/ctspinopelvic1k_build_tree/derived/build_archive_private"
# The plan's `restricted` flag (LAYOUT.md rule 8) marks VinDr-SpineXR, BUU-LSPINE and every bank that holds their
# pixels (33 rows across B04, B05, B10, B11 and B14 on 2026-10-08). On 2026-10-11 Greg stated that every approved student
# holds the PhysioNet credential and the VinDr and BUU agreements, so the flag no longer closes anything. Until
# 2026-10-12 it still did, at item level, which left vindr/raw, buu_full and the VinDr/BUU banks owner-only inside
# folders that were already open. Set HONOUR_PLAN_RESTRICTED=1 to close the flagged items again.
HONOUR_PLAN_RESTRICTED=${HONOUR_PLAN_RESTRICTED:-0}
restricted_paths_from_plan() { # the exact destination path of every item flagged restricted, when honoured
  [ "$HONOUR_PLAN_RESTRICTED" = 1 ] || return 0
  awk -F'\t' 'FNR>1 && $0 !~ /^#/ && $4 ~ /restricted/ { print $2 }' "$HERE"/batch_items/B*.tsv 2>/dev/null | sort -u
}
RESTRICTED_PATHS=$( { restricted_paths_from_plan; printf '%s
' $FIXED_RESTRICTED_PATHS; } | sort -u)
echo "== dp_visibility $(date -Is) on $(hostname -s); FOLDERS=$FOLDERS DRY=$DRY"
echo "restricted folders (closed whole): $FIXED_RESTRICTED"
echo "restricted items inside open folders (closed after the folder is opened): $(printf '%s\n' "$RESTRICTED_PATHS" | grep -c .)"
is_restricted_folder() { printf '%s\n' $FIXED_RESTRICTED | grep -qx -- "$1"; }
under_restricted_path() { # FILE -> 0 when it lies inside a restricted item
  local rp
  while IFS= read -r rp; do [ -n "$rp" ] || continue; case "$1" in "$rp"|"$rp"/*) return 0;; esac; done <<< "$RESTRICTED_PATHS"
  return 1
}
if [ "$FOLDERS" = ALL ]; then LIST=$(ls -1 "$DATA"); else LIST=$FOLDERS; fi
open_tree() { # DIR: readable by others, traversable directories, new content inherits
  if [ "$DRY" = 1 ]; then echo "  would open  $1"; return 0; fi
  chmod o+rX "$1" || return 1
  find "$1" -type d ! -perm -o=rx -exec chmod o+rx {} + 2>/dev/null
  find "$1" -type f ! -perm -o=r -exec chmod o+r {} + 2>/dev/null
  command -v setfacl >/dev/null 2>&1 && find "$1" -type d -exec setfacl -d -m o::r-x {} + 2>/dev/null
  return 0
}
close_tree() { # DIR or FILE: owner only
  if [ "$DRY" = 1 ]; then echo "  would close $1"; return 0; fi
  chmod -R go-rwx "$1" 2>/dev/null
  if command -v setfacl >/dev/null 2>&1 && [ -d "$1" ]; then
    find "$1" -type d -exec setfacl -d -m o::---,g::--- {} + 2>/dev/null
    setfacl -R -m g::---,o::--- "$1" 2>/dev/null
  fi
  return 0
}
for p in "$RS" "$DATA"; do
  if [ "$DRY" = 1 ]; then echo "  would ensure o+rx on $p"; else chmod o+rx "$p"; fi
done
n_open=0; n_closed=0; n_absent=0
for f in $LIST; do
  d="$DATA/$f"
  [ -e "$d" ] || { echo "  absent      $d"; n_absent=$((n_absent+1)); continue; }
  [ -L "$d" ] && { echo "  link        $d (left alone)"; continue; }
  if is_restricted_folder "$f"; then
    close_tree "$d"; echo "  closed      $d"; n_closed=$((n_closed+1))
  else
    open_tree "$d" && { echo "  open        $d"; n_open=$((n_open+1)); } || echo "  FAILED      $d"
    while IFS= read -r rp; do
      [ -n "$rp" ] || continue
      case "$rp" in "$d"/*) [ -e "$rp" ] && { close_tree "$rp"; echo "  closed      $rp (restricted item)"; n_closed=$((n_closed+1)); };; esac
    done <<< "$RESTRICTED_PATHS"
  fi
done
for extra in "$DATA/index" "$DATA/inventory"; do [ -d "$extra" ] && open_tree "$extra" && echo "  open        $extra"; done
echo "== done $(date -Is): opened $n_open, closed $n_closed, absent $n_absent"
# a check a student would make: one regular file per opened folder must be readable by others
for f in $LIST; do
  d="$DATA/$f"; [ -d "$d" ] || continue; is_restricted_folder "$f" && continue
  one=$(find "$d" -type f ! -name '.*' -print -quit 2>/dev/null); [ -n "$one" ] || continue
  under_restricted_path "$one" && continue
  m=$(stat -c %A "$one"); case "$m" in ???????r*) ;; *) echo "  CHECK: $one is $m (not readable by others)";; esac
done
