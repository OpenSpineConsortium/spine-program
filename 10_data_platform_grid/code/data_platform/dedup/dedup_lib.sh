# dedup_lib.sh -- sourced by dedup_hash.sbatch, dedup_apply.sbatch and dedup_guard.sh. Bash only: it needs find,
# sha256sum and coreutils (stat, readlink, cp, mv, ln, chmod, touch, sort); no python, jq, awk or sed.
#
# Paths and gates come from data_platform/plan (batch_items/<B>.tsv written by build_plan.py; runs/<B>/STATUS written
# by migrate_batch.sbatch; runs/<B>/CUTOVER.<job> written by cutover.sh). A member is a Ceph path. It is
#   "covered"    when a batch item's dst is the member or one of its parents (the member is a batch copy of HOME data);
#   "verified"   when that item's STATUS row (this run or an earlier one) says VERIFIED;
#   "cut over"   when the item's HOME src is a symlink whose target is exactly dst;
#   "finalized"  when <src>.pre-ceph is gone and a CUTOVER log records "FINALIZED (..., deleted <src>.pre-ceph)".
# A member no batch item covers is Ceph-native (for example $RS/data/thoracic_xr): it may be read and linked TO,
# never replaced.
#
# Every path test is made twice: on the path as spelled and on the path as resolved (readlink -f). A file is acted on
# only when it lies under its member root with no symlink component below the root (clean_below): a directory
# symlink inside a member tree can lead onto HOME or into a .pre-ceph copy, and a prefix test on the spelling cannot
# see that.

RS_ROOT=${RS_ROOT:-/rs/rs_grp_oschome/go2432}
RS_ROOT_R=$(readlink -f -- "$RS_ROOT" 2>/dev/null) || RS_ROOT_R=$RS_ROOT
[ -n "$RS_ROOT_R" ] || RS_ROOT_R=$RS_ROOT
HOME_ROOTS=${HOME_ROOTS:-"/wsu/home ${HOME:-/nonexistent-home}"}
DEDUP_DIR=${DEDUP_DIR:-$PWD}
PLAN_DIR=${PLAN_DIR:-$DEDUP_DIR/../plan}
PLAN_TSV=${PLAN_TSV:-$DEDUP_DIR/dedup_plan.tsv}
RESULTS=${RESULTS:-$DEDUP_DIR/hash_results}
APPLIED=${APPLIED:-$DEDUP_DIR/applied}
# the second copy of every ledger, next to the data on Ceph (outside data/, so no indexer walks it), and the registry
# of canonical roots that dedup_guard.sh reads before any deletion
LEDGER2_DIR=${LEDGER2_DIR:-$RS_ROOT/dedup_ledgers}
US=$'\037'

now_utc() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }

json_esc() {   # escape a string for a JSON value
  local s=$1
  s=${s//\\/\\\\}; s=${s//\"/\\\"}; s=${s//$'\t'/\\t}; s=${s//$'\n'/\\n}; s=${s//$'\r'/\\r}
  printf '%s' "$s"
}

split_tab() {  # split_tab "<line>" -> fills array F (empty fields kept; IFS=tab would collapse them)
  IFS="$US" read -r -a F <<< "${1//$'\t'/$US}"
}

under() { [[ $1 == "$2" || $1 == "$2"/* ]]; }        # literal prefix test: $1 is $2 or below it

on_home() {    # true when the path, as spelled or resolved, is on HOME
  local p=$1 r h
  r=$(readlink -m -- "$p" 2>/dev/null) || r=$p
  for h in $HOME_ROOTS; do
    under "$p" "$h" && return 0
    under "$r" "$h" && return 0
  done
  return 1
}

is_preceph() { [[ $1 == *.pre-ceph || $1 == *.pre-ceph/* ]]; }

clean_below() {  # clean_below <root> <path>: <path> is <root> or below it and no component below <root> is a symlink
  local root=$1 p=$2 rr pr
  under "$p" "$root" || return 1
  rr=$(readlink -f -- "$root" 2>/dev/null) || return 1
  pr=$(readlink -f -- "$p" 2>/dev/null) || return 1
  if [ "$p" = "$root" ]; then [ "$pr" = "$rr" ]; return; fi
  [ "$pr" = "$rr/${p#"$root"/}" ]
}

SAFE_WHY=
safe_resolved() {  # the path AS RESOLVED is under $RS_ROOT, not on HOME and not inside a .pre-ceph copy
  local r
  SAFE_WHY=
  r=$(readlink -f -- "$1" 2>/dev/null) || { SAFE_WHY="cannot be resolved"; return 1; }
  under "$r" "$RS_ROOT_R" || { SAFE_WHY="resolves outside $RS_ROOT ($r)"; return 1; }
  on_home "$r" && { SAFE_WHY="resolves onto HOME ($r)"; return 1; }
  is_preceph "$r" && { SAFE_WHY="resolves into a .pre-ceph copy ($r)"; return 1; }
  return 0
}

sha_of() {     # sha256 of one file (sha256sum prefixes a backslash when the name needs escaping)
  local h
  h=$(sha256sum -- "$1" 2>/dev/null) || return 1
  h=${h%% *}; h=${h#\\}
  printf '%s' "$h"
}

ino_of() { stat -c '%d:%i' -- "$1" 2>/dev/null; }
size_of() { stat -c '%s' -- "$1" 2>/dev/null; }
nlink_of() { stat -c '%h' -- "$1" 2>/dev/null; }
# full-precision identity of a file at one moment: dev:ino|size|mtime|ctime (stat %y/%z carry nanoseconds)
fstate() { stat -c '%d:%i|%s|%y|%z' -- "$1" 2>/dev/null; }
mtime_of() { stat -c '%y' -- "$1" 2>/dev/null; }

match_any() {  # match_any <rel> <pat1|pat2|...>; '-' or empty matches nothing. Patterns are bash globs, * crosses /
  local rel=$1 pats=$2 pat arr
  [[ -z $pats || $pats == - ]] && return 1
  IFS='|' read -r -a arr <<< "$pats"
  for pat in "${arr[@]}"; do
    # shellcheck disable=SC2053
    [[ $rel == $pat ]] && return 0
  done
  return 1
}

setup_tmpdir() {   # here-strings are temp files on bash < 5.1: keep them off the node's swept /tmp (CLAUDE.md)
  local d
  for d in "${DEDUP_TMP:-}" "/dev/shm/dedup.${SLURM_JOB_ID:-$$}" "$DEDUP_DIR/logs/tmp.${SLURM_JOB_ID:-$$}"; do
    [ -n "$d" ] || continue
    if mkdir -p -- "$d" 2>/dev/null && [ -w "$d" ]; then export TMPDIR=$d; DEDUP_TMPDIR_MADE=$d; return 0; fi
  done
  return 1
}
cleanup_tmpdir() { [ -n "${DEDUP_TMPDIR_MADE:-}" ] && rm -rf -- "$DEDUP_TMPDIR_MADE"; }

# ------------------------------------------------------------------------------------------------ the plan
plan_rows() {  # plan_rows <gid>: the plan lines of one group, in file order
  local line
  [ -f "$PLAN_TSV" ] || return 1
  while IFS= read -r line || [ -n "$line" ]; do
    [[ -z $line || $line == \#* ]] && continue
    [[ $line == "$1"$'\t'* ]] && printf '%s\n' "$line"
  done < "$PLAN_TSV"
}

plan_gids() {  # every kind-(a) group id in the plan, in file order, once each
  local line seen=" "; local -a F
  while IFS= read -r line || [ -n "$line" ]; do
    [[ -z $line || $line == \#* ]] && continue
    split_tab "$line"
    [ "${F[1]}" = "a" ] || continue
    [[ $seen == *" ${F[0]} "* ]] && continue
    seen+="${F[0]} "; printf '%s\n' "${F[0]}"
  done < "$PLAN_TSV"
}

plan_rows_sha() { local h; h=$(plan_rows "$1" | sha256sum); printf '%s' "${h%% *}"; }

ledger_files() {   # every ledger on disk: applied/<gid>.ledger.tsv and its Ceph copy
  local f
  for f in "$APPLIED"/*.ledger.tsv "$LEDGER2_DIR"/*.ledger.tsv; do [ -f "$f" ] && printf '%s\n' "$f"; done
}

# ------------------------------------------------------------------------------------------------ batch gates
CB_BATCH= CB_SRC= CB_DST= CB_TAG= CB_STATE=
batch_cover() {  # batch_cover <ceph path>; sets CB_*; returns 0 when a batch item covers the path
  local p=$1 f b line best=0 n; local -a F      # a local F: the caller's split_tab fields survive
  CB_BATCH= CB_SRC= CB_DST= CB_TAG= CB_STATE=
  for f in "$PLAN_DIR"/batch_items/*.tsv; do
    [ -f "$f" ] || continue
    b=${f##*/}; b=${b%.tsv}
    while IFS= read -r line || [ -n "$line" ]; do
      [[ -z $line || $line == \#* ]] && continue
      split_tab "$line"
      local src=${F[0]:-} dst=${F[1]:-} flags=${F[3]:-}
      [ -n "$dst" ] || continue
      if [[ $flags == *glob* ]]; then
        # shellcheck disable=SC2053
        [[ $p == $dst || $p == $dst/* ]] || continue
      else
        under "$p" "$dst" || continue
      fi
      n=${#dst}
      if [ "$n" -gt "$best" ]; then best=$n; CB_BATCH=$b; CB_SRC=$src; CB_DST=$dst; fi
    done < "$f"
  done
  [ -n "$CB_BATCH" ] || return 1
  status_of "$p"
  return 0
}

status_of() {    # fill CB_STATE, CB_TAG, CB_SRC, CB_DST from runs/<B>/STATUS (glob rows are expanded there)
  local p=$1 st="$PLAN_DIR/runs/$CB_BATCH/STATUS" line best=0 n state f fdst; local -a F
  CB_STATE=NO_STATUS
  [ -e "$st" ] || return 0
  while IFS= read -r line || [ -n "$line" ]; do
    split_tab "$line"
    [ "${#F[@]}" -ge 4 ] || continue
    # migrate_batch.sbatch writes an ALREADY_SYMLINK row with field 4 = "-> <readlink of src>" (L131)
    fdst=${F[3]#-> }
    under "$p" "$fdst" || continue
    n=${#fdst}
    if [ "$n" -gt "$best" ]; then best=$n; CB_TAG=${F[0]}; state=${F[1]}; CB_STATE=${state%% *}; CB_SRC=${F[2]}; CB_DST=$fdst; fi
  done < "$st"
  # a rerun of migrate_batch after the cut-over writes ALREADY_SYMLINK; the item counts as verified when an
  # earlier run of the same batch verified the same dst
  if [ "$CB_STATE" = "ALREADY_SYMLINK" ]; then
    for f in "$PLAN_DIR/runs/$CB_BATCH"/STATUS.*; do
      [ -f "$f" ] || continue
      while IFS= read -r line || [ -n "$line" ]; do
        split_tab "$line"
        [ "${#F[@]}" -ge 4 ] || continue
        if [ "${F[1]}" = "VERIFIED" ] && [ "${F[3]}" = "$CB_DST" ]; then CB_STATE=VERIFIED; CB_SRC=${F[2]}; CB_TAG=${F[0]}; return 0; fi
      done < "$f"
    done
  fi
  return 0
}

cut_over() { [ -n "$CB_SRC" ] && [ -L "$CB_SRC" ] && [ "$(readlink -- "$CB_SRC")" = "$CB_DST" ]; }

finalized() {
  local f line
  [ -e "$CB_SRC.pre-ceph" ] || [ -L "$CB_SRC.pre-ceph" ] && return 1
  for f in "$PLAN_DIR/runs/$CB_BATCH"/CUTOVER.*; do
    [ -f "$f" ] || continue
    while IFS= read -r line || [ -n "$line" ]; do
      [[ $line == *" FINALIZED "* && $line == *"deleted $CB_SRC.pre-ceph)"* ]] && return 0
    done < "$f"
  done
  return 1
}

# ------------------------------------------------------------------------------------------------ running jobs
RUN_TEXT= RUNNING_BATCH_JOBS= PENDING_MIGRATE=0 JOBS_OK=0
declare -a JOB_IDS=()
declare -A JOB_TXT=() JOB_WD=()
jobs_scan() {    # what the user's running and pending jobs name (command, work dir, logs, batch script)
  local jid jname jstate out txt l wd
  RUN_TEXT= RUNNING_BATCH_JOBS= PENDING_MIGRATE=0 JOBS_OK=0
  JOB_IDS=(); JOB_TXT=(); JOB_WD=()
  command -v squeue >/dev/null 2>&1 || return 1
  out=$(squeue -u "${USER:-$(id -un)}" -h -t R,PD -o '%i %j %T' 2>/dev/null) || return 1
  while read -r jid jname jstate; do
    [ -n "$jid" ] || continue
    [ "$jid" = "${SLURM_JOB_ID:-}" ] && continue
    txt= wd=
    while IFS= read -r l; do
      case "$l" in
        *WorkDir=*) txt+="$l"$'\n'; wd=${l#*WorkDir=}; wd=${wd%% *} ;;
        *Command=*|*StdOut=*|*StdErr=*) txt+="$l"$'\n' ;;
      esac
    done < <(scontrol show job "$jid" 2>/dev/null)
    txt+=$(scontrol write batch_script "$jid" - 2>/dev/null)$'\n'
    JOB_IDS+=("$jid"); JOB_TXT[$jid]=$txt; JOB_WD[$jid]=$wd
    RUN_TEXT+=$txt
    case "$jname" in
      dp_migrate|dp_cutover)
        if [ "$jstate" = "PENDING" ]; then PENDING_MIGRATE=1; else RUNNING_BATCH_JOBS+=" $jid"; fi ;;
    esac
  done <<< "$out"
  JOBS_OK=1
  return 0
}

batch_busy() {   # a migrate or cut-over job is writing batch $1 (or one is pending, batch unknown)
  local j
  [ "$PENDING_MIGRATE" = "1" ] && return 0
  for j in $RUNNING_BATCH_JOBS; do
    [ -e "$PLAN_DIR/runs/$1/STATUS.$j" ] || [ -e "$PLAN_DIR/runs/$1/CUTOVER.$j" ] && return 0
  done
  return 1
}

NAMED_BY=
names_member() { # names_member <member> [<batch src> <batch dst>]: a running or pending job names the member, its
  # HOME spelling, its batch dst or the batch's HOME src, as an absolute path, as ~/ or $HOME/, or as a path relative
  # to the job's WorkDir (sd:src/build_dataset.py writes data/interim from WorkDir ~/spine-detector); or the job's
  # WorkDir lies inside the member
  local p=$1 s=${2:-} d=${3:-} hs="" j txt wd x rel
  NAMED_BY=
  [ "${#JOB_IDS[@]}" -gt 0 ] || return 1
  if [ -n "$s" ] && [ -n "$d" ] && under "$p" "$d"; then hs="$s${p#"$d"}"; fi
  for j in "${JOB_IDS[@]}"; do
    txt=${JOB_TXT[$j]:-}; wd=${JOB_WD[$j]:-}
    for x in "$p" "$hs" "$d" "$s"; do
      [ -n "$x" ] || continue
      if [[ $txt == *"$x"* ]]; then NAMED_BY="job $j names $x"; return 0; fi
      if [ -n "${HOME:-}" ] && under "$x" "$HOME" && [ "$x" != "$HOME" ]; then
        rel=${x#"$HOME"/}
        if [[ $txt == *"~/$rel"* || $txt == *"\$HOME/$rel"* || $txt == *"\${HOME}/$rel"* ]]; then NAMED_BY="job $j names ~/$rel"; return 0; fi
      fi
      if [ -n "$wd" ]; then
        if under "$wd" "$x"; then NAMED_BY="job $j works inside $x (WorkDir $wd)"; return 0; fi
        if under "$x" "$wd" && [ "$x" != "$wd" ]; then
          rel=${x#"$wd"/}
          if [[ $txt == *"$rel"* ]]; then NAMED_BY="job $j names $rel relative to its WorkDir $wd"; return 0; fi
        fi
      fi
    done
  done
  return 1
}

# gate <path> <role: dup|canon> <level: hash|apply>; sets GATE (ok or the reason) and returns 0 when ok
GATE=
gate() {
  local p=$1 role=$2 level=$3
  GATE=ok
  if ! under "$p" "$RS_ROOT"; then GATE="not under $RS_ROOT (not a Ceph copy)"; return 1; fi
  if on_home "$p"; then GATE="on HOME (spelled or resolved)"; return 1; fi
  if is_preceph "$p"; then GATE="a .pre-ceph copy"; return 1; fi
  if [ ! -e "$p" ]; then GATE="missing"; return 1; fi
  if ! safe_resolved "$p"; then GATE="$SAFE_WHY"; return 1; fi
  if batch_cover "$p"; then
    if [ "$CB_STATE" != "VERIFIED" ]; then GATE="batch $CB_BATCH item $CB_DST is $CB_STATE, not VERIFIED"; return 1; fi
    if ! cut_over; then GATE="batch $CB_BATCH item not cut over ($CB_SRC is not a symlink to $CB_DST)"; return 1; fi
    if [ "$level" = "apply" ] && [ "${REQUIRE_FINALIZED:-1}" = "1" ] && ! finalized; then
      GATE="batch $CB_BATCH item not finalized ($CB_SRC.pre-ceph present or no FINALIZED line): a link now would make FINALIZE refuse"; return 1; fi
    if [ "$JOBS_OK" = "1" ] && batch_busy "$CB_BATCH"; then GATE="a migrate or cut-over job is writing batch $CB_BATCH (or one is pending)"; return 1; fi
  else
    if [ "$level" = "apply" ] && [ "$role" = "dup" ]; then GATE="Ceph-native (no batch item covers it): never replaced"; return 1; fi
  fi
  if [ "$level" = "apply" ] && names_member "$p" "$CB_SRC" "$CB_DST"; then GATE="a running or pending job names it ($NAMED_BY)"; return 1; fi
  return 0
}
