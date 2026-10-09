#!/bin/bash
#SBATCH --job-name=dedup_apply
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --no-requeue
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=1-00:00:00
#SBATCH --signal=B:TERM@120
#SBATCH --output=logs/%x_%j.out
# Replace byte-identical duplicates (kind a) by symlinks to their canonical copy, one group at a time, re-hashing both
# sides of every file immediately before its swap. Deletes nothing else and moves nothing else.
#
#   cd ~/spinesurg-ct-nnunet/data_platform/dedup && mkdir -p logs
#   sbatch -D "$PWD" --export=ALL,GROUP_IDS=A17,DRY=1 dedup_apply.sbatch          # say what it would do
#   sbatch -D "$PWD" --export=ALL,GROUP_IDS=A17 dedup_apply.sbatch                # link
#   sbatch -D "$PWD" --export=ALL,GROUP_IDS=A17,ROLLBACK=1 dedup_apply.sbatch     # put the bytes back
#
# Refuses (the whole group) when: the group is not kind (a); the plan holds it (hold column; ALLOW_HOLD="<gid> ..."
# releases it after Greg's decision); hash_results/<gid>.json is missing, its verdict is not "identical", or the
# plan rows changed since it was hashed; squeue cannot be read; any member root, as spelled or as resolved, is not
# under $RS_ROOT, is on HOME or is a .pre-ceph copy; the duplicate root is Ceph-native (no batch covers it); a covering
# batch item is not VERIFIED, not cut over, or (REQUIRE_FINALIZED=1, the default) not finalized: a symlink made
# before FINALIZE makes verify_transfer.py see a kind change and FINALIZE then keeps the .pre-ceph copy for ever;
# a migrate or cut-over job is writing that batch; any running or pending job names a member, its batch dst or its
# HOME src (absolute, ~/, $HOME/ or relative to the job's WorkDir), or works inside it; an interrupted earlier apply
# left .dedup_old / .dedup_hold / .dedup_tmp artefacts under it; a ledger copy cannot be written.
# Refuses one file when: it or its canonical passes through a symlinked directory below its member root, or resolves
# onto HOME, into a .pre-ceph copy or outside $RS_ROOT; the duplicate is not a regular file or has other hard links
# (nlink > 1: a symlink would free nothing and rollback could not rebuild the link); the canonical is a symlink, or the
# canonical of any pair in any hash_results/*.tsv or ledger (no link chains); the two are one inode; re-hashed now,
# they differ, or differ from the hash job's record; either changed while it was being hashed.
#
# File mode, in this order: (1) the canonical is made read-only (PROTECT=1: every canonical, batch copy or Ceph-native;
# its mode goes to the ledger first); (2) a hard link <dup>.dedup_hold.<job> keeps the duplicate's inode, and both
# sides are stat'ed (dev:ino, size, mtime and ctime to the nanosecond); (3) both are hashed; (4) the symlink is made
# under a temporary name (ln -sT) and both sides are stat'ed again, unchanged or refused; (5) the ledger row is written
# to applied/<gid>.ledger.tsv and to $LEDGER2_DIR/<gid>.ledger.tsv, and a failed write stops the group; (6) mv -fT puts
# the link over the duplicate (atomic); (7) the link must resolve to the canonical's recorded inode, the hold must still
# carry the duplicate's recorded inode, size and mtime, and the canonical must be unchanged, or mv -fT puts the hold
# back over the link (the original returns, with any late write) and the file is refused; (8) the hold is removed.
# What no check can close: a process that holds the duplicate open and writes after step 7 writes into an unlinked
# inode. The gates (no running or pending job names the member) are the only defence against that.
# Tree mode (TREE=1, the default): a relpath row whose duplicate tree has exactly the canonical tree's files and folders,
# every file verified. The tree is recorded entry by entry (type, path, size, mtime, ctime, inode, nlink) before the
# hashing, moved aside, replaced by one symlink (ln -sT), walked again and compared with the record; any new, missing
# or changed entry, or a file that does not resolve to its canonical's inode, puts the original tree back and refuses
# the row. Only then is the moved-aside tree removed.
# Jobs and gates are scanned again before every tree swap and, in file mode, whenever REGATE_SECS (default 60) have
# passed. A TERM (the --signal above, preemption, scancel) finishes the swap in flight and stops before the next one.
# ROLLBACK=1 reads the ledger (the primary or its Ceph copy; refused when they disagree beyond one being a prefix of the
# other), puts back trees left moved aside by a killed apply, replaces tree links by folders, copies each canonical back
# over its link (verifying the recorded sha256), restores file modes and full-precision mtimes, then folder modes and
# mtimes deepest first, and returns a canonical its first recorded mode only when no ledger of any group still has a
# live link to it. Owner, group, ACLs and xattrs: a copy made in the same folder gets what the batch copy got (rsync
# -aH --no-g into setgid folders, no -A or -X: plan/migrate_batch.sbatch L51), so nothing is recorded for them.
# Output: applied/<gid>.json (the last real apply), applied/<gid>.dry.<job>.json, applied/<gid>.refused.<job>.json,
# applied/<gid>.rollback.<job>.json; applied/<gid>.ledger.tsv and $LEDGER2_DIR/<gid>.ledger.tsv (append only, the same
# rows); CANONICAL_ROOTS.tsv in both places. dedup_guard.sh reads the ledgers before any deletion.
set -uo pipefail
if [ -z "${SLURM_JOB_ID:-}" ]; then echo "refusing: run this with sbatch, never on the login node"; exit 2; fi
case "$(hostname)" in warrior*) echo "refusing on the login node"; exit 2;; esac
DEDUP_DIR=${DEDUP_DIR:-$PWD}
# shellcheck source=dedup_lib.sh
. "$DEDUP_DIR/dedup_lib.sh" || { echo "no $DEDUP_DIR/dedup_lib.sh"; exit 2; }
GROUP_IDS=${GROUP_IDS:?set GROUP_IDS="<gid> ..." (no default: every group is applied by name)}
DRY=${DRY:-0}
ROLLBACK=${ROLLBACK:-0}
TREE=${TREE:-1}
PROTECT=${PROTECT:-1}
REQUIRE_FINALIZED=${REQUIRE_FINALIZED:-1}
ALLOW_HOLD=${ALLOW_HOLD:-}
REGATE_SECS=${REGATE_SECS:-60}
JOB=$SLURM_JOB_ID
mkdir -p "$APPLIED" "$DEDUP_DIR/logs"
setup_tmpdir || { echo "refusing: no writable TMPDIR under /dev/shm or logs/"; exit 2; }
STOP=0
on_term() { STOP=1; echo "TERM at $(now_utc): finishing the swap in flight, then stopping"; }
trap on_term TERM INT
trap cleanup_tmpdir EXIT
RC=0
echo "DEDUP_APPLY start $(now_utc) host $(hostname) job $JOB groups [$GROUP_IDS] dry=$DRY rollback=$ROLLBACK"

LEDGER_FAIL=
ledger_row() {   # ledger_row <gid> <action> <dup> <canon> <bytes> <sha> <mode> <mtime> <note>; 1 when either copy failed
  local line f
  line=$(printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' "$JOB" "$(now_utc)" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "${9:-}")
  for f in "$APPLIED/$1.ledger.tsv" "$LEDGER2_DIR/$1.ledger.tsv"; do
    if ! { printf '%s\n' "$line" >> "$f"; } 2>/dev/null; then LEDGER_FAIL="cannot append to $f"; echo "LEDGER WRITE FAILED: $f"; return 1; fi
  done
  sync -- "$APPLIED/$1.ledger.tsv" "$LEDGER2_DIR/$1.ledger.tsv" 2>/dev/null || true
  return 0
}

register_root() {   # register_root <gid> <canonical root>: once per group and root, in both CANONICAL_ROOTS.tsv
  local f line
  [ -z "${REGISTERED[$2]:-}" ] || return 0
  line=$(printf '%s\t%s\t%s\t%s' "$2" "$1" "$JOB" "$(now_utc)")
  for f in "$APPLIED/CANONICAL_ROOTS.tsv" "$LEDGER2_DIR/CANONICAL_ROOTS.tsv"; do
    if ! { printf '%s\n' "$line" >> "$f"; } 2>/dev/null; then LEDGER_FAIL="cannot append to $f"; return 1; fi
  done
  REGISTERED[$2]=1
}

json_value() {   # json_value <file> <key>: the string value of a top-level "key": "value" line
  local line
  while IFS= read -r line; do
    if [[ $line =~ ^[[:space:]]*\"$2\":[[:space:]]*\"([^\"]*)\" ]]; then printf '%s' "${BASH_REMATCH[1]}"; return 0; fi
  done < "$1"
  return 1
}

holder_gone() {   # 0 only on positive evidence that job $1 is over: squeue says the id is invalid, or sacct says it ended
  local h=$1 out rc st
  out=$(squeue -h -j "$h" -o '%T' 2>&1); rc=$?
  if [ "$rc" -ne 0 ]; then [[ $out == *"Invalid job id"* ]] && return 0; return 1; fi
  [ -n "$out" ] && return 1
  command -v sacct >/dev/null 2>&1 || return 1
  st=$(sacct -n -X -P -j "$h" -o State 2>/dev/null) || return 1
  st=${st%%$'\n'*}; st=${st%% *}
  case "$st" in COMPLETED|FAILED|CANCELLED|CANCELLED+|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|PREEMPTED|BOOT_FAIL|DEADLINE) return 0;; esac
  return 1
}

lock_group() {   # one apply or rollback per group at a time; a lock is taken over only from a job proven finished
  local l="$APPLIED/.lock.$1" holder
  if mkdir "$l" 2>/dev/null; then printf '%s' "$JOB" > "$l/job"; return 0; fi
  holder=$(cat "$l/job" 2>/dev/null)
  if [ -n "$holder" ] && command -v squeue >/dev/null 2>&1 && holder_gone "$holder" && mkdir "$l/takeover.$holder" 2>/dev/null; then
    printf '%s' "$JOB" > "$l/job"; echo "  took over the lock of finished job $holder"; return 0; fi
  return 1
}
unlock_group() { [ "$(cat "$APPLIED/.lock.$1/job" 2>/dev/null)" = "$JOB" ] && rm -rf -- "$APPLIED/.lock.$1"; }

declare -a S_LINKED=() S_REFUSED=()
SUMMARY_OUT=
summary() {      # summary <gid> <state> <reason> <bytes>
  local out i sep=""
  case "$2" in
    dry_run) out="$APPLIED/$1.dry.$JOB.json" ;;
    refused) out="$APPLIED/$1.refused.$JOB.json" ;;
    *)       out=${SUMMARY_OUT:-$APPLIED/$1.json} ;;
  esac
  {
    printf '{\n  "group_id": "%s",\n  "state": "%s",\n  "reason": "%s",\n' "$(json_esc "$1")" "$2" "$(json_esc "$3")"
    printf '  "job": "%s",\n  "finished": "%s",\n  "dry_run": %s,\n  "rollback": %s,\n' "$JOB" "$(now_utc)" \
      "$([ "$DRY" = 1 ] && echo true || echo false)" "$([ "$ROLLBACK" = 1 ] && echo true || echo false)"
    printf '  "bytes": %s,\n  "ledger": "%s",\n  "ledger_copy": "%s",\n' "${4:-0}" "$(json_esc "$APPLIED/$1.ledger.tsv")" "$(json_esc "$LEDGER2_DIR/$1.ledger.tsv")"
    printf '  "done": [\n'
    for i in "${!S_LINKED[@]}"; do printf '%s    "%s"' "$sep" "$(json_esc "${S_LINKED[i]}")"; sep=$',\n'; done
    printf '\n  ],\n  "refused": [\n'; sep=""
    for i in "${!S_REFUSED[@]}"; do printf '%s    "%s"' "$sep" "$(json_esc "${S_REFUSED[i]}")"; sep=$',\n'; done
    printf '\n  ]\n}\n'
  } > "$out.tmp" && mv -f "$out.tmp" "$out"
  echo "GROUP $1 $2: $3 (done ${#S_LINKED[@]}, refused ${#S_REFUSED[@]}, bytes ${4:-0})"
  echo "SUMMARY $1 $out"
}

refuse_group() { summary "$1" refused "$2" 0; RC=1; }

declare -A PROTECTED=() REGISTERED=()
protect_canon() {   # chmod a-w a canonical file once, after a checked ledger row; 2 = the ledger write failed
  local gid=$1 c=$2 m
  [ "$PROTECT" = "1" ] || return 0
  [ -n "${PROTECTED[$c]:-}" ] && return 0
  [ -L "$c" ] && return 1
  m=$(stat -c '%a' -- "$c") || return 1
  if [ $(( 8#$m & 8#222 )) -ne 0 ]; then
    ledger_row "$gid" protect "-" "$c" "-" "-" "$m" "-" "chmod a-w" || return 2
    chmod a-w -- "$c" || return 1
  fi
  PROTECTED[$c]=1
  return 0
}

# ------------------------------------------------------------------------------------------------ gates, again
declare -a DROOTS=() CROOTS=() MODES=() FIRSTC=()
LAST_GATE=0 REGATE_WHY=
regate() {       # the user's jobs and every member gate, again
  local r bad=""
  jobs_scan || { REGATE_WHY="squeue/scontrol not available: cannot check running jobs"; return 1; }
  for r in "${DROOTS[@]}"; do gate "$r" dup apply || bad+="; $r: $GATE"; done
  for r in "${CROOTS[@]}"; do gate "$r" canon apply || bad+="; $r: $GATE"; done
  LAST_GATE=$SECONDS
  [ -z "$bad" ] || { REGATE_WHY="gate: ${bad#; }"; return 1; }
  return 0
}
regate_if_due() { [ $(( SECONDS - LAST_GATE )) -ge "$REGATE_SECS" ] || return 0; regate; }

tree_record() {  # tree_record <root>: one sorted line per entry below the root (type, path, size, mtime, ctime, inode, nlink)
  find "$1" -mindepth 1 -printf '%y\t%P\t%s\t%T@\t%C@\t%i\t%n\n' 2>/dev/null | LC_ALL=C sort
}

# ------------------------------------------------------------------------------------------------ apply
apply_group() {
  local gid=$1 line hres="$RESULTS/$1.json" htsv="$RESULTS/$1.tsv" v sha_now sha_then f r arr bad=""
  S_LINKED=(); S_REFUSED=(); PROTECTED=(); REGISTERED=(); LEDGER_FAIL=
  DROOTS=(); CROOTS=(); MODES=(); FIRSTC=()
  local -a ROWS=()
  while IFS= read -r line; do ROWS+=("$line"); done < <(plan_rows "$gid")
  [ "${#ROWS[@]}" -gt 0 ] || { refuse_group "$gid" "not in $PLAN_TSV"; return; }
  split_tab "${ROWS[0]}"
  [ "${F[1]}" = "a" ] || { refuse_group "$gid" "kind ${F[1]}: only kind (a) is ever linked"; return; }
  local hold=${F[12]:-}
  if [[ -n $hold && $hold != - && " $ALLOW_HOLD " != *" $gid "* ]]; then refuse_group "$gid" "held by the plan ($hold); ALLOW_HOLD=$gid releases it"; return; fi
  [ -f "$hres" ] && [ -f "$htsv" ] || { refuse_group "$gid" "no hash_results/$gid.json and .tsv: run dedup_hash.sbatch first"; return; }
  v=$(json_value "$hres" verdict) || v=""
  [ "$v" = "identical" ] || { refuse_group "$gid" "hash verdict is '${v:-none}', not identical"; return; }
  sha_then=$(json_value "$hres" plan_rows_sha256) || sha_then=""
  sha_now=$(plan_rows_sha "$gid")
  [ "$sha_then" = "$sha_now" ] || { refuse_group "$gid" "the plan rows changed since the hash (hash again)"; return; }
  jobs_scan || { refuse_group "$gid" "squeue/scontrol not available: cannot check running jobs"; return; }

  # gates on every member root
  for line in "${ROWS[@]}"; do
    split_tab "$line"
    local rmode=${F[2]} rdup=${F[3]} rcan=${F[5]}
    gate "$rdup" dup apply || bad+="; $rdup: $GATE"
    DROOTS+=("$rdup"); MODES+=("$rmode"); FIRSTC+=("${rcan%%|*}")
    IFS='|' read -r -a arr <<< "$rcan"
    for r in "${arr[@]}"; do gate "$r" canon apply || bad+="; $r: $GATE"; CROOTS+=("$r"); done
  done
  [ -z "$bad" ] || { refuse_group "$gid" "gate: ${bad#; }"; return; }
  LAST_GATE=$SECONDS

  # artefacts of an interrupted apply or rollback
  local -a LEFT=()
  local x
  for r in "${DROOTS[@]}"; do
    for x in "$r".dedup_old.*; do { [ -e "$x" ] || [ -L "$x" ]; } && LEFT+=("$x"); done
    if [ -d "$r" ] && [ ! -L "$r" ]; then
      while IFS= read -r -d '' x; do LEFT+=("$x"); done < <(find "$r" \( -name '*.dedup_hold.*' -o -name '*.dedup_tmp.*' -o -name '*.dedup_restore.*' \) -print0 2>/dev/null)
    fi
  done
  [ "${#LEFT[@]}" -eq 0 ] || { refuse_group "$gid" "an interrupted apply left ${#LEFT[*]} artefact(s), e.g. ${LEFT[0]}: run ROLLBACK=1 or look first"; return; }

  if [ "$DRY" != "1" ]; then
    mkdir -p -- "$LEDGER2_DIR" 2>/dev/null && [ -w "$LEDGER2_DIR" ] || { refuse_group "$gid" "the ledger copy folder $LEDGER2_DIR cannot be written"; return; }
  fi

  # no link chains: every canonical named by any hash result or any ledger
  local -A IS_CANON=()
  for f in "$RESULTS"/*.tsv; do
    [ -f "$f" ] || continue
    while IFS= read -r line || [ -n "$line" ]; do
      [[ -z $line || $line == \#* ]] && continue
      split_tab "$line"
      case "${F[0]}" in identical|unhashed_size_equal) [ -n "${F[2]:-}" ] && IS_CANON[${F[2]}]=1 ;; esac
    done < "$f"
  done
  while IFS= read -r f; do
    while IFS= read -r line || [ -n "$line" ]; do
      [[ -z $line || $line == \#* ]] && continue
      split_tab "$line"
      case "${F[2]:-}" in link_file|tree_member|link_tree) [ -n "${F[4]:-}" ] && IS_CANON[${F[4]}]=1 ;; esac
    done < "$f"
  done < <(ledger_files)

  # candidates from the hash result (hashed again below, file by file)
  local -a C_DUP=() C_CAN=() C_SIZE=() C_SHA=() C_ROW=() C_CROOT=()
  local -A ROOT_NOTED=()
  local st dp cp sz shd k cr
  while IFS= read -r line || [ -n "$line" ]; do
    [[ -z $line || $line == \#* ]] && continue
    split_tab "$line"
    st=${F[0]}; dp=${F[1]}; cp=${F[2]}; sz=${F[3]}; shd=${F[4]:-}
    [ "$st" = "identical" ] || [ "$st" = "unhashed_size_equal" ] || continue
    k=-1; cr=
    for r in "${!DROOTS[@]}"; do under "$dp" "${DROOTS[r]}" && { k=$r; break; }; done
    for r in "${CROOTS[@]}"; do under "$cp" "$r" && { cr=$r; break; }; done
    if [ "$k" -lt 0 ] || [ -z "$cr" ]; then S_REFUSED+=("$dp: outside the group's gated roots"); continue; fi
    if [ -L "${DROOTS[k]}" ]; then          # the whole duplicate root is already a link (an earlier tree swap)
      if [ -z "${ROOT_NOTED[$k]:-}" ]; then
        ROOT_NOTED[$k]=1
        if [ "$(readlink -- "${DROOTS[k]}")" = "${FIRSTC[k]}" ]; then S_LINKED+=("${DROOTS[k]} (already linked as a tree)")
        else S_REFUSED+=("${DROOTS[k]}: the duplicate root is a symlink to $(readlink -- "${DROOTS[k]}")"); fi
      fi
      continue
    fi
    if [ -n "${IS_CANON[$dp]:-}" ]; then S_REFUSED+=("$dp: it is the canonical file of a pair (no link chains)"); continue; fi
    if [ "$dp" = "$cp" ]; then S_REFUSED+=("$dp: duplicate and canonical are one path"); continue; fi
    C_DUP+=("$dp"); C_CAN+=("$cp"); C_SIZE+=("$sz"); C_SHA+=("$shd"); C_ROW+=("$k"); C_CROOT+=("$cr")
  done < "$htsv"

  # tree mode candidates: relpath rows whose duplicate tree is exactly the canonical tree
  local -A TREE_ROW=() FALLBACK=()
  local i rec
  if [ "$TREE" = "1" ]; then
    for r in "${!DROOTS[@]}"; do
      [ "${MODES[r]}" = "relpath" ] || continue
      local droot=${DROOTS[r]} croot=${FIRSTC[r]} n_c=0
      [ "$droot" != "$croot" ] || continue
      local -A crel_set=() drel=() crel=()
      for i in "${!C_DUP[@]}"; do [ "${C_ROW[i]}" = "$r" ] && { crel_set[${C_DUP[i]#"$droot"/}]=1; n_c=$((n_c + 1)); }; done
      [ "$n_c" -gt 0 ] || { unset crel_set drel crel; continue; }
      local same=1
      while IFS= read -r -d '' rec; do drel[$rec]=1; done < <(find "$droot" -mindepth 1 -printf '%y:%P\0')
      while IFS= read -r -d '' rec; do crel[$rec]=1; done < <(find "$croot" -mindepth 1 -printf '%y:%P\0')
      [ "${#drel[@]}" -eq "${#crel[@]}" ] || same=0
      for rec in "${!drel[@]}"; do
        [ -n "${crel[$rec]:-}" ] || { same=0; break; }
        case "$rec" in d:*) ;; f:*) [ -n "${crel_set[${rec#f:}]:-}" ] || { same=0; break; } ;; *) same=0; break ;; esac
      done
      [ "$same" = "1" ] && TREE_ROW[$r]=1
      unset crel_set drel crel
    done
  fi

  local total=0 stopped=""
  # ---------------------------------------------------------------- tree rows
  for r in "${!TREE_ROW[@]}"; do
    [ "$STOP" = "1" ] && { stopped="TERM"; break; }
    local droot=${DROOTS[r]} croot=${FIRSTC[r]} old="${DROOTS[r]}.dedup_old.$JOB" rec1 rec2 okv=1
    local -a M=()
    for i in "${!C_DUP[@]}"; do [ "${C_ROW[i]}" = "$r" ] && M+=("$i"); done
    rec1=$(tree_record "$droot")
    # every file of the duplicate tree is a plain single-link file, every path clean
    for i in "${M[@]}"; do
      dp=${C_DUP[i]}; cp=${C_CAN[i]}
      if [ -L "$dp" ] || [ ! -f "$dp" ] || [ "$(nlink_of "$dp")" != "1" ] || ! clean_below "$droot" "$dp" || ! clean_below "$croot" "$cp" \
         || [ -L "$cp" ] || [ ! -f "$cp" ] || ! safe_resolved "$cp"; then okv=0; break; fi
    done
    [ "$okv" = "1" ] || { FALLBACK[$r]=1; continue; }
    local -A CST=()
    if [ "$DRY" != "1" ]; then
      for i in "${M[@]}"; do
        protect_canon "$gid" "${C_CAN[i]}"; case $? in 0) ;; 2) stopped="ledger: $LEDGER_FAIL"; break 2 ;; *) okv=0 ;; esac
      done
    fi
    for i in "${M[@]}"; do
      dp=${C_DUP[i]}; cp=${C_CAN[i]}; sz=${C_SIZE[i]}
      CST[$i]=$(stat -c '%d:%i|%s|%y' -- "$cp" 2>/dev/null)
      local h1 h2
      [ "$(size_of "$dp")" = "$sz" ] && [ "$(size_of "$cp")" = "$sz" ] || { okv=0; break; }
      h1=$(sha_of "$dp"); h2=$(sha_of "$cp")
      if [ -z "$h1" ] || [ "$h1" != "$h2" ] || { [ -n "${C_SHA[i]}" ] && [ "$h1" != "${C_SHA[i]}" ]; }; then okv=0; break; fi
      C_SHA[i]=$h1
    done
    [ "$okv" = "1" ] || { FALLBACK[$r]=1; unset CST; continue; }
    if [ "$DRY" = "1" ]; then
      for i in "${M[@]}"; do S_LINKED+=("would link (tree $droot): ${C_DUP[i]}"); total=$(( total + C_SIZE[i] )); done
      unset CST; continue
    fi
    if ! regate; then stopped="$REGATE_WHY"; unset CST; break; fi
    [ "$STOP" = "1" ] && { stopped="TERM"; unset CST; break; }
    # ledger first: every member, every folder, the root
    local lok=1 dmode dmt
    for i in "${M[@]}"; do
      ledger_row "$gid" tree_member "${C_DUP[i]}" "${C_CAN[i]}" "${C_SIZE[i]}" "${C_SHA[i]}" \
        "$(stat -c '%a' -- "${C_DUP[i]}")" "$(mtime_of "${C_DUP[i]}")" "$droot" || { lok=0; break; }
    done
    if [ "$lok" = "1" ]; then
      while IFS= read -r -d '' rec; do
        ledger_row "$gid" tree_dir "$droot/$rec" "$croot/$rec" - - "$(stat -c '%a' -- "$droot/$rec")" "$(mtime_of "$droot/$rec")" "$droot" || { lok=0; break; }
      done < <(find "$droot" -mindepth 1 -type d -printf '%P\0')
    fi
    dmode=$(stat -c '%a' -- "$droot"); dmt=$(mtime_of "$droot")
    [ "$lok" = "1" ] && ledger_row "$gid" link_tree "$droot" "$croot" - - "$dmode" "$dmt" "whole tree" || lok=0
    [ "$lok" = "1" ] && register_root "$gid" "$croot" || lok=0
    [ "$lok" = "1" ] || { stopped="ledger: $LEDGER_FAIL"; unset CST; break; }
    if ! mv -T -- "$droot" "$old"; then S_REFUSED+=("$droot: could not move aside"); unset CST; continue; fi
    if ! ln -sT -- "$croot" "$droot"; then mv -T -- "$old" "$droot"; S_REFUSED+=("$droot: could not create the link; restored"); unset CST; continue; fi
    rec2=$(tree_record "$old")
    local why=""
    [ "$rec2" = "$rec1" ] || why="the duplicate tree changed between the record and the swap"
    if [ -z "$why" ]; then
      for i in "${M[@]}"; do
        [ "$(stat -L -c '%d:%i|%s|%y' -- "${C_DUP[i]}" 2>/dev/null)" = "${CST[$i]}" ] || { why="${C_DUP[i]} does not resolve to its canonical's recorded inode"; break; }
        [ "$(stat -c '%d:%i|%s|%y' -- "${C_CAN[i]}" 2>/dev/null)" = "${CST[$i]}" ] || { why="${C_CAN[i]} changed since it was hashed"; break; }
      done
    fi
    if [ -n "$why" ]; then
      [ -L "$droot" ] && [ "$(readlink -- "$droot")" = "$croot" ] && rm -f -- "$droot"
      if mv -T -- "$old" "$droot"; then
        ledger_row "$gid" undo_tree "$droot" "$croot" - - "$dmode" "$dmt" "$why" || true
        S_REFUSED+=("$droot: $why; the original tree is back")
      else
        S_REFUSED+=("$droot: $why; COULD NOT move $old back (do it by hand)"); RC=1
      fi
      unset CST; continue
    fi
    find "$old" -type d ! -perm -u+w -exec chmod u+w {} + 2>/dev/null
    rm -rf -- "$old"
    [ -e "$old" ] && { S_REFUSED+=("$droot: linked, but $old could not be removed completely"); RC=1; }
    for i in "${M[@]}"; do total=$(( total + C_SIZE[i] )); done
    S_LINKED+=("$droot -> $croot (tree, ${#M[@]} files)")
    unset CST
  done

  # ---------------------------------------------------------------- file rows, one file at a time
  if [ -z "$stopped" ]; then
    for i in "${!C_DUP[@]}"; do
      [ -n "${TREE_ROW[${C_ROW[i]}]:-}" ] && [ -z "${FALLBACK[${C_ROW[i]}]:-}" ] && continue
      [ "$STOP" = "1" ] && { stopped="TERM"; break; }
      if [ "$DRY" != "1" ] && ! regate_if_due; then stopped="$REGATE_WHY"; break; fi
      local d=${C_DUP[i]} c=${C_CAN[i]} sz=${C_SIZE[i]} droot=${DROOTS[${C_ROW[i]}]} croot=${C_CROOT[i]} tmp hld D0 C0 D1 C1 h1 h2 dmode dmt
      if [ -L "$d" ]; then
        if [ "$(readlink -- "$d")" = "$c" ]; then S_LINKED+=("$d (already linked)"); else S_REFUSED+=("$d: now a symlink to $(readlink -- "$d")"); fi
        continue; fi
      if ! clean_below "$droot" "$d"; then S_REFUSED+=("$d: reached through a symlinked directory (resolves to $(readlink -f -- "$d"))"); continue; fi
      if ! clean_below "$croot" "$c"; then S_REFUSED+=("$d: its canonical $c is reached through a symlink (resolves to $(readlink -f -- "$c"))"); continue; fi
      if ! safe_resolved "$d"; then S_REFUSED+=("$d: $SAFE_WHY"); continue; fi
      if ! safe_resolved "$c"; then S_REFUSED+=("$d: its canonical $SAFE_WHY"); continue; fi
      if [ ! -f "$d" ] || [ ! -f "$c" ] || [ -L "$c" ]; then S_REFUSED+=("$d: a side is missing or not a regular file"); continue; fi
      if [ "$(nlink_of "$d")" != "1" ]; then S_REFUSED+=("$d: has $(nlink_of "$d") hard links; a symlink frees nothing"); continue; fi
      if [ "$(ino_of "$d")" = "$(ino_of "$c")" ]; then S_REFUSED+=("$d: same inode as $c"); continue; fi
      if [ "$DRY" = "1" ]; then
        if [ "$(size_of "$d")" != "$sz" ] || [ "$(size_of "$c")" != "$sz" ]; then S_REFUSED+=("$d: size changed since the hash"); continue; fi
        h1=$(sha_of "$d"); h2=$(sha_of "$c")
        if [ -z "$h1" ] || [ "$h1" != "$h2" ]; then S_REFUSED+=("$d: differs from $c now"); continue; fi
        if [ -n "${C_SHA[i]}" ] && [ "$h1" != "${C_SHA[i]}" ]; then S_REFUSED+=("$d: changed since the hash"); continue; fi
        S_LINKED+=("would link: $d -> $c"); total=$(( total + sz )); continue
      fi
      protect_canon "$gid" "$c"
      case $? in 0) ;; 2) stopped="ledger: $LEDGER_FAIL"; break ;; *) S_REFUSED+=("$d: could not make $c read-only"); continue ;; esac
      hld="$d.dedup_hold.$JOB"; tmp="$d.dedup_tmp.$JOB"
      if ! ln -T -- "$d" "$hld" 2>/dev/null; then S_REFUSED+=("$d: could not take a hold link"); continue; fi
      D0=$(fstate "$d"); C0=$(fstate "$c")
      IFS='|' read -r _ dsz _ <<< "$D0"; IFS='|' read -r _ csz _ <<< "$C0"
      if [ "$dsz" != "$sz" ] || [ "$csz" != "$sz" ]; then rm -f -- "$hld"; S_REFUSED+=("$d: size changed since the hash"); continue; fi
      h1=$(sha_of "$d"); h2=$(sha_of "$c")
      if [ -z "$h1" ] || [ "$h1" != "$h2" ]; then rm -f -- "$hld"; S_REFUSED+=("$d: differs from $c now (sha256 $h1 vs $h2)"); continue; fi
      if [ -n "${C_SHA[i]}" ] && [ "$h1" != "${C_SHA[i]}" ]; then rm -f -- "$hld"; S_REFUSED+=("$d: changed since the hash"); continue; fi
      if ! ln -sT -- "$c" "$tmp"; then rm -f -- "$hld" "$tmp"; S_REFUSED+=("$d: could not make the link"); continue; fi
      D1=$(fstate "$d"); C1=$(fstate "$c")
      if [ "$D1" != "$D0" ] || [ "$C1" != "$C0" ]; then
        rm -f -- "$tmp" "$hld"
        S_REFUSED+=("$d: $([ "$D1" != "$D0" ] && echo "the duplicate" || echo "the canonical") changed while it was hashed; left as it was"); continue; fi
      dmode=$(stat -c '%a' -- "$d"); dmt=$(mtime_of "$d")
      if ! ledger_row "$gid" link_file "$d" "$c" "$sz" "$h1" "$dmode" "$dmt" "-" || ! register_root "$gid" "$croot"; then
        rm -f -- "$tmp" "$hld"; stopped="ledger: $LEDGER_FAIL"; break; fi
      if ! mv -fT -- "$tmp" "$d"; then rm -f -- "$tmp" "$hld"; S_REFUSED+=("$d: could not swap in the link (file left as it was)"); continue; fi
      local why=""
      [ "$(readlink -- "$d")" = "$c" ] || why="the link does not name $c"
      [ -z "$why" ] && [ "$(stat -L -c '%d:%i' -- "$d" 2>/dev/null)" != "${C0%%|*}" ] && why="the link does not resolve to the canonical's recorded inode"
      [ -z "$why" ] && [ "$(stat -c '%d:%i|%s|%y' -- "$hld" 2>/dev/null)" != "${D0%|*}" ] && why="the duplicate was written during the swap"
      [ -z "$why" ] && [ "$(fstate "$c")" != "$C0" ] && why="the canonical changed during the swap"
      if [ -n "$why" ]; then
        if mv -fT -- "$hld" "$d"; then
          ledger_row "$gid" undo_file "$d" "$c" "$sz" "$h1" "$dmode" "$dmt" "$why" || true
          S_REFUSED+=("$d: $why; the original is back")
        else
          S_REFUSED+=("$d: $why; COULD NOT put $hld back (do it by hand; ROLLBACK=1 also restores from the canonical)"); RC=1
        fi
        continue
      fi
      rm -f -- "$hld"
      S_LINKED+=("$d -> $c"); total=$(( total + sz ))
    done
  fi
  if [ -n "$stopped" ]; then
    S_REFUSED+=("stopped before the remaining files: $stopped"); RC=1
  fi
  if [ "$DRY" = "1" ]; then summary "$gid" dry_run "re-verified ${#S_LINKED[@]} file(s); nothing changed" "$total"; return; fi
  local state=applied
  [ "${#S_REFUSED[@]}" -gt 0 ] && state=partial
  [ -n "$stopped" ] && state=stopped
  [ "${#S_LINKED[@]}" -eq 0 ] && [ -n "$stopped" ] && [[ $stopped == ledger:* ]] && state=refused
  if [ "$state" = "refused" ]; then refuse_group "$gid" "$stopped"; return; fi
  summary "$gid" "$state" "linked ${#S_LINKED[@]} file(s) or tree(s)" "$total"
}

# ------------------------------------------------------------------------------------------------ rollback
ledger_pick() {  # the ledger to read: the primary or its Ceph copy (append-only copies of one another)
  local a="$APPLIED/$1.ledger.tsv" b="$LEDGER2_DIR/$1.ledger.tsv" na nb
  if [ -f "$a" ] && [ -f "$b" ]; then
    na=$(wc -l < "$a"); nb=$(wc -l < "$b")
    if [ "$na" -le "$nb" ] && [ "$(sha256sum < "$a")" = "$(head -n "$na" "$b" | sha256sum)" ]; then printf '%s' "$b"; return 0; fi
    if [ "$nb" -le "$na" ] && [ "$(sha256sum < "$b")" = "$(head -n "$nb" "$a" | sha256sum)" ]; then printf '%s' "$a"; return 0; fi
    return 1
  fi
  [ -f "$a" ] && { printf '%s' "$a"; return 0; }
  [ -f "$b" ] && { printf '%s' "$b"; return 0; }
  return 2
}

touch_to() {     # touch_to <mtime as recorded> <path>: stat %y (nanoseconds) or epoch seconds (older ledgers)
  if [[ $1 =~ ^[0-9]+(\.[0-9]+)?$ ]]; then touch -m -d "@$1" -- "$2"; else touch -m -d "$1" -- "$2"; fi
}

sweep_artefacts() {  # sweep_artefacts <gid>: resolve the .dedup_hold / .dedup_tmp / .dedup_restore files a killed job left
  local gid=$1 line r x base ok=0
  local -a R=()
  while IFS= read -r line; do split_tab "$line"; R+=("${F[3]}"); done < <(plan_rows "$gid")
  for r in "${R[@]}"; do
    [ -d "$r" ] && [ ! -L "$r" ] || continue
    under "$r" "$RS_ROOT" && ! on_home "$r" && ! is_preceph "$r" || continue
    while IFS= read -r -d '' x; do
      case "$x" in
        *.dedup_tmp.*|*.dedup_restore.*)
          base=${x%.dedup_*}
          if [ "$DRY" = "1" ]; then S_LINKED+=("would remove $x"); continue; fi
          if [ -L "$x" ] || [[ $x == *.dedup_restore.* ]]; then rm -f -- "$x" && S_LINKED+=("removed $x (a temporary of an interrupted job)"); fi ;;
        *.dedup_hold.*)
          base=${x%.dedup_hold.*}
          if [ "$DRY" = "1" ]; then S_LINKED+=("would resolve $x"); continue; fi
          if [ -f "$base" ] && [ ! -L "$base" ] && [ "$(ino_of "$base")" = "$(ino_of "$x")" ]; then
            rm -f -- "$x" && S_LINKED+=("removed $x (a second name of $base, which was never swapped)")
          elif [ -L "$base" ] || [ ! -e "$base" ]; then
            if mv -fT -- "$x" "$base"; then S_LINKED+=("$base: the original inode is back from $x"); else S_REFUSED+=("$base: could not put $x back"); RC=1; fi
          else
            S_REFUSED+=("$x: $base is another file; left alone"); RC=1
          fi ;;
      esac
      ok=1
    done < <(find "$r" \( -name '*.dedup_hold.*' -o -name '*.dedup_tmp.*' -o -name '*.dedup_restore.*' \) -print0 2>/dev/null)
  done
  [ "$ok" = "1" ]
}

rollback_group() {
  local gid=$1 led line act d c sz sha mode mtime restored=0 total=0 rc_pick swept=0
  S_LINKED=(); S_REFUSED=()
  SUMMARY_OUT="$APPLIED/$gid.rollback.$JOB.json"
  sweep_artefacts "$gid" && swept=1
  led=$(ledger_pick "$gid"); rc_pick=$?
  if [ "$rc_pick" = "2" ]; then
    if [ "$swept" = "1" ]; then summary "$gid" "$([ "${#S_REFUSED[@]}" -gt 0 ] && echo rollback_partial || echo rolled_back)" "no ledger; artefacts of an interrupted job resolved" 0
    else refuse_group "$gid" "no ledger ($APPLIED/$gid.ledger.tsv or its copy in $LEDGER2_DIR): nothing was linked"; fi
    SUMMARY_OUT=; return; fi
  if [ "$rc_pick" != "0" ]; then refuse_group "$gid" "the two ledger copies disagree: compare $APPLIED/$gid.ledger.tsv with $LEDGER2_DIR/$gid.ledger.tsv"; SUMMARY_OUT=; return; fi
  local -a L=()
  while IFS= read -r line || [ -n "$line" ]; do [[ -z $line || $line == \#* ]] || L+=("$line"); done < "$led"
  local -A tree_done=() tree_whole=() canons=()
  # 1) trees: a tree left moved aside by a killed apply comes back whole; a tree link becomes a folder (files: step 2)
  for line in "${L[@]}"; do
    split_tab "$line"; act=${F[2]}; d=${F[3]}; c=${F[4]}
    [ "$act" = "link_tree" ] || continue
    local old="$d.dedup_old.${F[0]}"
    if ! under "$d" "$RS_ROOT" || on_home "$d" || is_preceph "$d"; then S_REFUSED+=("$d: not a Ceph path; refused"); continue; fi
    if [ -L "$d" ]; then
      if [ "$(readlink -- "$d")" = "$c" ] && [ -d "$old" ] && [ ! -L "$old" ]; then
        # killed after the link and before the moved-aside tree was removed: the original tree comes back whole
        if [ "$DRY" = "1" ] || { rm -f -- "$d" && mv -T -- "$old" "$d"; }; then tree_whole[$d]=1; S_LINKED+=("$d: the moved-aside tree is back whole")
        else S_REFUSED+=("$d: could not move $old back"); RC=1; fi
      elif [ "$(readlink -- "$d")" = "$c" ]; then
        [ "$DRY" = "1" ] || { rm -f -- "$d" && mkdir -p -- "$d"; }
        tree_done[$d]=1
      else
        S_REFUSED+=("$d: the tree root links elsewhere ($(readlink -- "$d")), not to $c; left alone"); RC=1
      fi
    elif [ ! -e "$d" ] && [ -d "$old" ]; then
      if [ "$DRY" = "1" ] || mv -T -- "$old" "$d"; then tree_whole[$d]=1; S_LINKED+=("$d: the moved-aside tree is back whole")
      else S_REFUSED+=("$d: could not move $old back"); RC=1; fi
    elif [ -d "$d" ] && [ -e "$old" ]; then
      S_REFUSED+=("$d and $old both exist: look first"); RC=1
    elif [ ! -e "$d" ]; then
      S_REFUSED+=("$d: the tree root is missing and no moved-aside copy exists"); RC=1
    fi
  done
  for line in "${L[@]}"; do
    split_tab "$line"; act=${F[2]}; d=${F[3]}
    [ "$act" = "tree_dir" ] && [ -n "${tree_done[${F[9]}]:-}" ] || continue
    [ "$DRY" = "1" ] || mkdir -p -- "$d"
  done
  # 2) files
  for line in "${L[@]}"; do
    [ "$STOP" = "1" ] && { S_REFUSED+=("stopped by TERM before the remaining files"); RC=1; break; }
    split_tab "$line"; act=${F[2]}; d=${F[3]}; c=${F[4]}; sz=${F[5]}; sha=${F[6]}; mode=${F[7]}; mtime=${F[8]}
    case "$act" in protect) canons[$c]=1; continue ;; link_file|tree_member) canons[$c]=1 ;; *) continue ;; esac
    if [ "$act" = "tree_member" ] && [ -n "${tree_whole[${F[9]}]:-}" ]; then
      [ "$DRY" = "1" ] || [ "$(sha_of "$d")" = "$sha" ] || { S_REFUSED+=("$d: back with its tree, but not with the recorded bytes"); RC=1; }
      continue; fi
    if ! under "$d" "$RS_ROOT" || on_home "$d" || is_preceph "$d"; then S_REFUSED+=("$d: not a Ceph path; refused"); continue; fi
    if ! clean_below "$RS_ROOT" "${d%/*}"; then S_REFUSED+=("$d: a parent folder is a symlink (resolves to $(readlink -f -- "${d%/*}")); left alone"); RC=1; continue; fi
    if [ -f "$d" ] && [ ! -L "$d" ]; then
      [ "$(sha_of "$d")" = "$sha" ] && continue          # already restored (or never linked)
      S_REFUSED+=("$d: a regular file with other bytes; left alone"); continue
    fi
    if [ -L "$d" ] && [ "$(readlink -- "$d")" != "$c" ]; then S_REFUSED+=("$d: links elsewhere ($(readlink -- "$d")); left alone"); continue; fi
    if [ ! -f "$c" ]; then S_REFUSED+=("$d: canonical $c is gone; cannot restore"); RC=1; continue; fi
    if [ "$(sha_of "$c")" != "$sha" ]; then S_REFUSED+=("$d: canonical $c no longer has the recorded bytes"); RC=1; continue; fi
    if [ "$DRY" = "1" ]; then S_LINKED+=("would restore $d from $c"); total=$(( total + sz )); continue; fi
    local tmp="$d.dedup_restore.$JOB"
    if cp -- "$c" "$tmp" && chmod "$mode" -- "$tmp" && touch_to "$mtime" "$tmp" && [ "$(sha_of "$tmp")" = "$sha" ] && mv -fT -- "$tmp" "$d"; then
      S_LINKED+=("$d restored"); restored=$((restored + 1)); total=$(( total + sz ))
    else
      rm -f -- "$tmp"; S_REFUSED+=("$d: copy back failed"); RC=1
    fi
  done
  # 3) folder modes and mtimes, deepest first, after their contents are back
  if [ "$DRY" != "1" ]; then
    local -A DMODE=() DMT=()
    local dl s
    for line in "${L[@]}"; do
      split_tab "$line"
      case "${F[2]}" in
        tree_dir)  [ -n "${tree_done[${F[9]}]:-}" ] || continue ;;
        link_tree) [ -n "${tree_done[${F[3]}]:-}" ] || continue ;;
        *) continue ;;
      esac
      DMODE[${F[3]}]=${F[7]}; DMT[${F[3]}]=${F[8]}
    done
    while IFS=$'\t' read -r _ dl; do
      [ -n "$dl" ] || continue
      chmod "${DMODE[$dl]}" -- "$dl" 2>/dev/null || S_REFUSED+=("$dl: could not restore mode ${DMODE[$dl]}")
      [ "${DMT[$dl]}" = "-" ] || touch_to "${DMT[$dl]}" "$dl" 2>/dev/null || true
    done < <(for dl in "${!DMODE[@]}"; do s=${dl//[!\/]/}; printf '%d\t%s\n' "${#s}" "$dl"; done | LC_ALL=C sort -t$'\t' -k1,1nr)
  fi
  # 4) canonical modes: the first recorded mode, only when no ledger of any group still has a live link to it
  if [ "$DRY" != "1" ]; then
    local -A first_mode=() first_utc=() live=()
    local lf cc dd
    while IFS= read -r lf; do
      while IFS= read -r line || [ -n "$line" ]; do
        [[ -z $line || $line == \#* ]] && continue
        split_tab "$line"; cc=${F[4]:-}
        [ -n "${canons[$cc]:-}" ] || continue
        case "${F[2]}" in
          protect) if [ -z "${first_utc[$cc]:-}" ] || [[ ${F[1]} < ${first_utc[$cc]} ]]; then first_utc[$cc]=${F[1]}; first_mode[$cc]=${F[7]}; fi ;;
          link_file|tree_member)
            dd=${F[3]}
            if [ -z "${live[$cc]:-}" ] && [ "$dd" != "$cc" ] && [ "$(readlink -f -- "$dd" 2>/dev/null)" = "$(readlink -f -- "$cc" 2>/dev/null)" ]; then live[$cc]=$dd; fi ;;
        esac
      done < "$lf"
    done < <(ledger_files)
    for cc in "${!first_mode[@]}"; do
      if [ -n "${live[$cc]:-}" ]; then S_LINKED+=("$cc stays read-only: ${live[$cc]} still links to it"); continue; fi
      if [ -L "$cc" ]; then S_REFUSED+=("$cc: the canonical is now a symlink; its mode was not touched"); continue; fi
      [ -e "$cc" ] && { chmod "${first_mode[$cc]}" -- "$cc" || S_REFUSED+=("$cc: could not restore mode ${first_mode[$cc]}"); }
    done
  fi
  local state=rolled_back; [ "${#S_REFUSED[@]}" -gt 0 ] && state=rollback_partial; [ "$DRY" = "1" ] && state=dry_run
  summary "$gid" "$state" "restored $restored file(s) from the ledger $led" "$total"
  SUMMARY_OUT=
}

for gid in $GROUP_IDS; do
  [ "$STOP" = "1" ] && { echo "GROUP $gid: not started (TERM)"; RC=1; continue; }
  if ! lock_group "$gid"; then echo "GROUP $gid: another dedup_apply holds $APPLIED/.lock.$gid"; RC=1; continue; fi
  if [ "$ROLLBACK" = "1" ]; then rollback_group "$gid"; else apply_group "$gid"; fi
  unlock_group "$gid"
done
echo "DEDUP_APPLY end $(now_utc) rc=$RC"
exit $RC
