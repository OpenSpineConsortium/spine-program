#!/bin/bash
#SBATCH --job-name=dp_migrate
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --no-requeue
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=4-00:00:00
#SBATCH --output=logs/%x_%j.out
# Copy one migration batch from HOME to the CephFS layout, then verify every item. Never deletes or renames the
# source: the cut-over is a separate step (cutover.sh) that runs only on a verified batch.
#
#   cd ~/spinesurg-ct-nnunet/data_platform/plan && mkdir -p logs      # Slurm opens --output before the script runs
#   sbatch -D "$PWD" --export=ALL,BATCH=B00 migrate_batch.sbatch            # copy + verify
#   sbatch -D "$PWD" --export=ALL,BATCH=B02,DRY=1 migrate_batch.sbatch      # rsync --dry-run only
#   sbatch -D "$PWD" --export=ALL,BATCH=B01,SAMPLE=500 migrate_batch.sbatch
#
# Inputs: batch_items/$BATCH.tsv (src, dst, est_gb, flags; written by build_plan.py). Flags: hardlink_group (copied in
# the batch's one group rsync), restricted (owner-only on Ceph), irreplaceable (cutover FINALIZE hashes every file),
# candidate, glob.
# Outputs: runs/$BATCH/<n>.rsync.log, runs/$BATCH/<n>.verify.json, runs/$BATCH/STATUS (one line per item:
# tag, state, src, dst, verify summary, flags).
# Re-running the same batch resumes: rsync skips what is already equal and --partial keeps half-copied files. A
# hard-link group is re-entered: copies already moved into place are renamed back into the staging tree, the group
# rsync refreshes them from HOME, and they are moved into place again.
# A destination that already exists and was not written by an earlier run of the same item is refused (DST_EXISTS):
# runs/markers/ records which source each destination was copied from.
# Rules from CLAUDE.md: rsync never on the login node (warrior); output goes under the submit directory (-D).
set -uo pipefail
if [ -z "${SLURM_JOB_ID:-}" ]; then echo "refusing: run this with sbatch, never on the login node"; exit 2; fi
case "$(hostname)" in warrior*) echo "refusing on the login node"; exit 2;; esac
BATCH=${BATCH:?set BATCH=Bxx}
DRY=${DRY:-0}
SAMPLE=${SAMPLE:-200}
PLAN=${PLAN:-$PWD}
ITEMS="$PLAN/batch_items/$BATCH.tsv"
RUN="$PLAN/runs/$BATCH"
MARK="$PLAN/runs/markers"
PY=${PY:-python3}
STAGING=${STAGING:-/rs/rs_grp_oschome/go2432/data/_staging/$BATCH}
ALLOW_NLINK_LOSS=${ALLOW_NLINK_LOSS:-0}
mkdir -p "$RUN" "$MARK" logs
STATUS="$RUN/STATUS.${SLURM_JOB_ID}"; ln -sfn "$(basename "$STATUS")" "$RUN/STATUS"
[ -f "$ITEMS" ] || { echo "no $ITEMS"; exit 2; }
echo "DP_MIGRATE start $(date '+%F %T') host $(hostname) batch $BATCH dry=$DRY"
command -v df-ceph >/dev/null 2>&1 && df-ceph oschome | tail -3
command -v pan_quota >/dev/null 2>&1 && pan_quota 2>/dev/null | tail -2
# -aH keeps links, hard links, modes and times; --no-g lets files take the group of the setgid CephFS folder
# (oschome) instead of their HOME group, and --chmod=Dg+s keeps that setgid bit on every copied directory (rsync -a
# would otherwise give each directory its HOME mode, which has no setgid, and files below would take go2432's group).
RSYNC_OPTS=(-aH --no-g --chmod=Dg+s --partial --numeric-ids --info=progress2,stats2)
[ "$DRY" = "1" ] && RSYNC_OPTS+=(--dry-run --itemize-changes)
VOPTS=()
[ "$ALLOW_NLINK_LOSS" = "1" ] && VOPTS+=(--allow-nlink-loss)

markfile() { printf '%s/%s' "$MARK" "$(printf '%s' "$1" | md5sum | cut -c1-32)"; }
marked_for() { local m; m=$(markfile "$1"); [ -f "$m" ] && [ "$(cat "$m")" = "$2" ]; }   # dst $1 written from src $2
mark() { printf '%s' "$2" > "$(markfile "$1")"; }
nonempty() { [ -L "$1" ] || { [ -d "$1" ] && [ -n "$(ls -A "$1" 2>/dev/null)" ]; } || [ -f "$1" ]; }

# expand glob rows (src ending in *) into one row per match
expand() {
  grep -v '^#' "$ITEMS" | tr '\t' '\037' | while IFS=$'\037' read -r src dst gb flags; do   # \037 keeps empty fields (a tab IFS collapses them)
    [ -z "$src" ] && continue
    if [[ "$flags" == *glob* ]]; then
      parent=$(dirname "$src"); pat=$(basename "$src")
      for m in "$parent"/$pat; do [ -e "$m" ] && printf '%s\t%s\t%s\t%s\n' "$m" "$(dirname "$dst")/$(basename "$m")" "" "${flags/glob/}"; done
    else
      printf '%s\t%s\t%s\t%s\n' "$src" "$dst" "$gb" "$flags"
    fi
  done
}

# ---------------------------------------------------------------- the hard-link group
# Items flagged hardlink_group are copied in ONE rsync call into the staging tree, so links between them survive
# (hard links cannot span two rsync runs), then renamed into place on CephFS (same filesystem, instant).
# Items already cut over (the HOME path is a symlink) are not in the group any more.
GROUP_FAIL=""
HL=$(expand | awk -F'\t' '$4 ~ /hardlink_group/' | while IFS=$'\t' read -r s d g f; do [ -e "$s" ] && [ ! -L "$s" ] && printf '%s\t%s\n' "$s" "$d"; done)
if [ -n "$HL" ] && [ "$DRY" != "1" ]; then
  mkdir -p "$STAGING"
  LIST="$STAGING/.group_items"
  want=$(echo "$HL" | cut -f1 | sort)
  if [ -f "$LIST" ] && [ "$(cat "$LIST")" != "$want" ]; then
    echo "refusing: $STAGING holds leftovers of a different group (compare $LIST with batch_items/$BATCH.tsv)" | tee -a "$STATUS"
    exit 2
  fi
  if [ ! -f "$LIST" ] && [ -n "$(ls -A "$STAGING" 2>/dev/null)" ]; then
    echo "refusing: $STAGING is not empty and has no .group_items record; inspect it before rerunning" | tee -a "$STATUS"
    exit 2
  fi
  echo "$want" > "$LIST"
  # bring copies that an earlier run already moved into place back into staging, so the group rsync refreshes them
  while IFS=$'\t' read -r s d; do
    staged="$STAGING/${s#$HOME/}"
    if [ -e "$d" ] || [ -L "$d" ]; then
      if ! marked_for "$d" "$s"; then GROUP_FAIL="$GROUP_FAIL $d(DST_EXISTS)"; continue; fi
      if [ -e "$staged" ]; then GROUP_FAIL="$GROUP_FAIL $d(BOTH_STAGED_AND_PLACED)"; continue; fi
      mkdir -p "$(dirname "$staged")" && mv -- "$d" "$staged" || GROUP_FAIL="$GROUP_FAIL $d(BRING_BACK_FAILED)"
    fi
  done <<< "$HL"
  if [ -n "$GROUP_FAIL" ]; then
    echo "refusing the hard-link group:$GROUP_FAIL" | tee -a "$STATUS"
  else
    echo "== hard-link group: $(echo "$HL" | wc -l) roots -> $STAGING"
    while IFS=$'\t' read -r s d; do mark "$d" "$s"; done <<< "$HL"
    # --relative with /./ keeps each root's path below $HOME inside the staging tree; --delete drops files that left HOME
    mapfile -t HLR < <(echo "$HL" | cut -f1 | sed "s#^$HOME/#$HOME/./#")
    rsync "${RSYNC_OPTS[@]}" --delete --relative "${HLR[@]}" "$STAGING/" > "$RUN/hardlink_group.rsync.log" 2>&1
    grc=$?
    echo "hard-link rsync rc=$grc" | tee -a "$STATUS"
    if [ "$grc" -eq 0 ]; then
      while IFS=$'\t' read -r s d; do
        staged="$STAGING/${s#$HOME/}"
        mkdir -p "$(dirname "$d")" && mv -- "$staged" "$d" || GROUP_FAIL="$GROUP_FAIL $d(MOVE_FAILED)"
      done <<< "$HL"
    else
      GROUP_FAIL=" rsync rc=$grc"
    fi
  fi
fi

# ---------------------------------------------------------------- per item
n=0
expand | tr '\t' '\037' | while IFS=$'\037' read -r src dst gb flags; do
  n=$((n + 1)); tag=$(printf '%03d' "$n")
  if [ ! -e "$src" ] && [ ! -L "$src" ]; then
    printf '%s\tABSENT\t%s\t%s\t-\t%s\n' "$tag" "$src" "$dst" "$flags" | tee -a "$STATUS"; continue
  fi
  if [ -L "$src" ]; then
    printf '%s\tALREADY_SYMLINK\t%s\t-> %s\t-\t%s\n' "$tag" "$src" "$(readlink "$src")" "$flags" | tee -a "$STATUS"; continue
  fi
  restricted=0; [[ "$flags" == *restricted* ]] && restricted=1
  opts=("${RSYNC_OPTS[@]}")
  [ "$restricted" = "1" ] && opts=("${opts[@]/--chmod=Dg+s/--chmod=Dg+s,go-rwx}")
  if [[ "$flags" == *hardlink_group* ]] && [ "$DRY" != "1" ]; then
    rc=0
    if [ -n "$GROUP_FAIL" ]; then rc=96; fi
    if [ ! -e "$dst" ]; then rc=97; fi
  else
    if nonempty "$dst" && ! marked_for "$dst" "$src"; then
      printf '%s\tDST_EXISTS\t%s\t%s\tnot written by an earlier run of this item: refused\t%s\n' "$tag" "$src" "$dst" "$flags" | tee -a "$STATUS"; continue
    fi
    mkdir -p "$(dirname "$dst")"
    [ "$DRY" = "1" ] || mark "$dst" "$src"
    if [ -d "$src" ]; then
      rsync "${opts[@]}" "$src/" "$dst/" > "$RUN/$tag.rsync.log" 2>&1; rc=$?
    else
      rsync "${opts[@]}" "$src" "$dst" > "$RUN/$tag.rsync.log" 2>&1; rc=$?
    fi
  fi
  if [ "$DRY" = "1" ]; then
    printf '%s\tDRYRUN rc=%s\t%s\t%s\t%s changes\t%s\n' "$tag" "$rc" "$src" "$dst" "$(grep -c '^[<>ch.*]' "$RUN/$tag.rsync.log" 2>/dev/null)" "$flags" | tee -a "$STATUS"; continue
  fi
  if [ "$rc" -ne 0 ]; then printf '%s\tRSYNC_FAILED rc=%s\t%s\t%s\t-\t%s\n' "$tag" "$rc" "$src" "$dst" "$flags" | tee -a "$STATUS"; continue; fi
  [ "$restricted" = "1" ] && chmod -R go-rwx "$dst"
  "$PY" "$PLAN/verify_transfer.py" --src "$src" --dst "$dst" --sample "$SAMPLE" ${VOPTS[@]+"${VOPTS[@]}"} --out "$RUN/$tag.verify.json" > "$RUN/$tag.verify.txt" 2>&1
  vrc=$?
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$tag" "$([ $vrc -eq 0 ] && echo VERIFIED || echo VERIFY_FAILED)" "$src" "$dst" "$(tail -1 "$RUN/$tag.verify.txt")" "$flags" | tee -a "$STATUS"
done
# the staging tree must end empty: remove its empty folders, then say if anything is left
if [ -d "$STAGING" ]; then
  find "$STAGING" -depth -mindepth 1 -type d -empty -delete 2>/dev/null
  if [ -z "$(find "$STAGING" -mindepth 1 ! -name .group_items -print -quit 2>/dev/null)" ]; then
    rm -f "$STAGING/.group_items"; rmdir "$STAGING" 2>/dev/null
  else
    echo "STAGING_NOT_EMPTY $STAGING (left for the rerun; nothing in it is lost)" | tee -a "$STATUS"
  fi
fi
echo "DP_MIGRATE end $(date '+%F %T')"
grep -c $'\tVERIFIED\t' "$STATUS" | sed 's/^/verified items: /'
grep -qE 'FAILED|DST_EXISTS|refusing|STAGING_NOT_EMPTY' "$STATUS" && exit 1
exit 0
