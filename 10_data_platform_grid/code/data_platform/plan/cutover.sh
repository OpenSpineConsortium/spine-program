#!/bin/bash
#SBATCH --job-name=dp_cutover
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --no-requeue
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=1-00:00:00
#SBATCH --output=logs/%x_%j.out
# Cut a VERIFIED batch over to CephFS: for each item, re-check that nothing changed since the copy, rename the HOME
# original to <src>.pre-ceph (same filesystem, instant, still restorable) and put a symlink at the old path, so every
# script that names the HOME path keeps working. A later FINALIZE=1 run deletes the .pre-ceph copies; that is the
# step that frees HOME quota, and it runs only after Greg has checked the batch (MIGRATION_PLAN.md, step 6).
#
#   cd ~/spinesurg-ct-nnunet/data_platform/plan && mkdir -p logs
#   sbatch -D "$PWD" --export=ALL,BATCH=B00 cutover.sh                  # rename + symlink
#   sbatch -D "$PWD" --export=ALL,BATCH=B00,FINALIZE=1 cutover.sh       # compare, then delete the .pre-ceph copies
#   sbatch -D "$PWD" --export=ALL,BATCH=B00,ROLLBACK=1 cutover.sh       # undo a cut-over that has not been finalized
#
# Refuses an item whose latest verify JSON is missing or not ok, or that changed after the copy. The running-job
# check is ADVISORY: it greps your running and pending jobs' command lines, work directories, logs and (when Slurm
# returns it) their batch script for the item's path in its usual spellings; a script that builds the path at run
# time is not seen. Check squeue yourself before a cut-over.
#
# FINALIZE deletes <src>.pre-ceph only when: the HOME path is a symlink to dst, dst exists, verify_transfer.py finds
# .pre-ceph and dst equal (every path, size, link target and hard-link group; every file hashed when the item is
# flagged irreplaceable or holds less than FULL_HASH_GB, a sample otherwise), and a size-and-mtime rsync dry run of
# .pre-ceph against dst itemizes nothing (a file written into .pre-ceph after the cut-over shows here).
# Modes, owner and group are left out of that comparison on purpose: publish_visibility.sh changes the Ceph
# copy's modes (students read it) and must not make the cut-over refuse an unchanged file.
set -uo pipefail
if [ -z "${SLURM_JOB_ID:-}" ]; then echo "refusing: run this with sbatch, never on the login node"; exit 2; fi
case "$(hostname)" in warrior*) echo "refusing on the login node"; exit 2;; esac
BATCH=${BATCH:?set BATCH=Bxx}
FINALIZE=${FINALIZE:-0}
ROLLBACK=${ROLLBACK:-0}
PLAN=${PLAN:-$PWD}
RUN="$PLAN/runs/$BATCH"
ITEMS="$PLAN/batch_items/$BATCH.tsv"
PY=${PY:-python3}
SAMPLE=${SAMPLE:-500}
FULL_HASH_GB=${FULL_HASH_GB:-50}
LOG="$RUN/CUTOVER.${SLURM_JOB_ID}"
STATUS="$RUN/STATUS"
[ -f "$STATUS" ] || { echo "no $STATUS: run migrate_batch.sbatch first"; exit 2; }
mkdir -p "$RUN"
echo "DP_CUTOVER start $(date '+%F %T') batch $BATCH finalize=$FINALIZE rollback=$ROLLBACK" | tee "$LOG"

# advisory: what your running and pending jobs name (command line, work dir, logs, batch script)
RUNNING=$(squeue -u "$USER" -h -t R,PD -o '%i' 2>/dev/null | while read -r j; do
  scontrol show job "$j" 2>/dev/null | grep -E 'Command=|WorkDir=|StdOut=|StdErr='
  scontrol write batch_script "$j" - 2>/dev/null
done)
names_item() {   # $1 = HOME path; true when a running job names it in any usual spelling
  local p="$1" rel="${1#$HOME/}"
  [ -n "$RUNNING" ] || return 1
  printf '%s' "$RUNNING" | grep -qF -e "$p" -e "~/$rel" -e "\$HOME/$rel" -e "\${HOME}/$rel" -e "\$H/$rel"
}

flags_of() {     # the flags column of the batch item that produced this src (glob rows match by pattern)
  local s="$1"
  [ -f "$ITEMS" ] || return 0
  grep -v '^#' "$ITEMS" | tr '\t' '\037' | while IFS=$'\037' read -r isrc idst igb iflags; do
    # shellcheck disable=SC2053
    if [ "$isrc" = "$s" ] || { [[ "$iflags" == *glob* ]] && [[ "$s" == $isrc ]]; }; then printf '%s' "$iflags"; break; fi
  done
}
restricted() {   # $1 = dst, $2 = flags. DUA/EULA folders are closed to the group (DATA_MANIFEST.md: VinDr DUA, BUU EULA)
  [[ "$2" == *restricted* ]] && return 0
  case "$1" in */vindr_spinexr/*|*/buu_lspine_3600/*|*/buu_lspine_2000/*|*/buu_lspine_v1_smoke/*) return 0;; esac; return 1; }

finalize_item() {  # $1 tag, $2 src, $3 dst, $4 flags
  local tag="$1" src="$2" dst="$3" flags="$4" pre="${2}.pre-ceph" all=() gb ch
  if ! { [ -L "$src" ] && [ "$(readlink "$src")" = "$dst" ]; }; then
    echo "$tag NOT_FINALIZED $src (not a symlink to $dst)" | tee -a "$LOG"; return; fi
  if [ ! -e "$pre" ]; then echo "$tag NOT_FINALIZED $src (no $pre)" | tee -a "$LOG"; return; fi
  if [ ! -e "$dst" ]; then echo "$tag REFUSED_DST_MISSING $dst (the .pre-ceph copy is the only one left; kept)" | tee -a "$LOG"; return; fi
  gb=$(du -s --apparent-size -B1G "$pre" 2>/dev/null | cut -f1)
  if [[ "$flags" == *irreplaceable* ]] || [ "${gb:-999999}" -lt "$FULL_HASH_GB" ]; then all=(--all); fi
  if ! "$PY" "$PLAN/verify_transfer.py" --src "$pre" --dst "$dst" --sample "$SAMPLE" ${all[@]+"${all[@]}"} \
        --out "$RUN/$tag.finalize.json" > "$RUN/$tag.finalize.txt" 2>&1; then
    echo "$tag REFUSED_PRE_DIFFERS $pre vs $dst: $(tail -1 "$RUN/$tag.finalize.txt") (see $tag.finalize.json)" | tee -a "$LOG"; return; fi
  if [ -d "$pre" ]; then ch=$(rsync -aHn --no-g --no-p --no-o --itemize-changes "$pre/" "$dst/" | grep -v '^\.d' | head -5)
  else ch=$(rsync -aHn --no-g --no-p --no-o --itemize-changes "$pre" "$dst" | head -5); fi
  if [ -n "$ch" ]; then echo "$tag REFUSED_PRE_CHANGED $pre: $ch" | tee -a "$LOG"; return; fi
  rm -rf -- "$pre" && echo "$tag FINALIZED (compared${all:+ in full}, deleted $pre)" | tee -a "$LOG"
}

grep -E $'\t(VERIFIED|ALREADY_SYMLINK|ABSENT)\t' "$STATUS" | tr '\t' '\037' | while IFS=$'\037' read -r tag state src dst summary flags; do
  pre="${src}.pre-ceph"
  flags=$(flags_of "$src")
  if [ "$ROLLBACK" = "1" ]; then
    if [ -L "$src" ] && [ -e "$pre" ]; then rm "$src" && mv "$pre" "$src" && echo "$tag ROLLED_BACK $src" | tee -a "$LOG"
    else echo "$tag NOTHING_TO_ROLL_BACK $src" | tee -a "$LOG"; fi
    continue
  fi
  if [ "$FINALIZE" = "1" ]; then
    [ "$state" = "ABSENT" ] && { echo "$tag SKIP ABSENT $src" | tee -a "$LOG"; continue; }
    finalize_item "$tag" "$src" "$dst" "$flags"
    continue
  fi
  [ "$state" = "VERIFIED" ] || { echo "$tag SKIP $state $src" | tee -a "$LOG"; continue; }
  if [ -L "$src" ]; then echo "$tag ALREADY_CUT $src -> $(readlink "$src")" | tee -a "$LOG"; continue; fi
  if names_item "$src"; then echo "$tag REFUSED_RUNNING_JOB $src (advisory check; see squeue)" | tee -a "$LOG"; continue; fi
  v="$RUN/$tag.verify.json"
  ok=$("$PY" -c "import json,sys; print(json.load(open(sys.argv[1])).get('ok'))" "$v" 2>/dev/null)
  [ "$ok" = "True" ] || { echo "$tag REFUSED_NOT_VERIFIED $src" | tee -a "$LOG"; continue; }
  # nothing may have changed since the copy: a quick rsync dry run (size + mtime) must itemize nothing
  if [ -d "$src" ]; then ch=$(rsync -aHn --no-g --no-p --no-o --itemize-changes "$src/" "$dst/" | grep -v '^\.d' | head -5)
  else ch=$(rsync -aHn --no-g --no-p --no-o --itemize-changes "$src" "$dst" | head -5); fi
  if [ -n "$ch" ]; then echo "$tag REFUSED_CHANGED_SINCE_COPY $src: $ch" | tee -a "$LOG"; continue; fi
  if restricted "$dst" "$flags"; then chmod -R go-rwx "$dst" && echo "$tag CLOSED_TO_GROUP $dst" | tee -a "$LOG"; fi
  mv -- "$src" "$pre" && ln -s -- "$dst" "$src" && echo "$tag CUT $src -> $dst (original kept at $pre)" | tee -a "$LOG" \
    || { echo "$tag CUT_FAILED $src" | tee -a "$LOG"; [ -e "$pre" ] && [ ! -e "$src" ] && mv -- "$pre" "$src"; }
done
echo "DP_CUTOVER end $(date '+%F %T')" | tee -a "$LOG"
command -v pan_quota >/dev/null 2>&1 && pan_quota 2>/dev/null | tail -2 | tee -a "$LOG"
grep -qE 'FAILED|REFUSED' "$LOG" && exit 1
exit 0
