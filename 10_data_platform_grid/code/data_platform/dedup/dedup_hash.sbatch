#!/bin/bash
#SBATCH --job-name=dedup_hash
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --requeue
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=2-00:00:00
#SBATCH --output=logs/%x_%j.out
# Hash the byte-identical candidates (kind a) of dedup_plan.tsv on their Ceph copies and write a verdict per group.
# Read-only: it never writes outside hash_results/ and logs/. Bash, find, sha256sum and coreutils only.
#
#   cd ~/spinesurg-ct-nnunet/data_platform/dedup && mkdir -p logs        # Slurm opens --output before the script runs
#   sbatch -D "$PWD" dedup_hash.sbatch                                      # every kind-(a) group of the plan
#   sbatch -D "$PWD" --export=ALL,GROUP_IDS="A05 A17" dedup_hash.sbatch    # named groups
#
# A group is hashed only when every member root is under $RS_ROOT, not on HOME (as spelled or resolved), not a
# .pre-ceph copy, and, when a migration batch covers it, that batch item is VERIFIED and cut over and no migrate or
# cut-over job is writing the batch. Otherwise the group's result says not_ready and why.
#
# Modes (dedup_plan.tsv column 3):
#   relpath  the canonical of <dup_root>/<rel> is <canon_root>/<rel>
#   rename   the same, with the basename rewritten by rename_map (old=>new;...)  e.g. glgl003.npy -> gl003.npy
#   pairs    explicit dup_rel=>canon_rel pairs
#   content  pairing BY BYTES: a dup file is paired with the first canonical file (canonical roots in priority order)
#            of equal size and equal sha256; key_regex, when set, must find a shared token in both relative paths
#            (BASENAME = equal basenames). Names never decide a content pair (TotalSegmentator renumbered 24 ids).
#            The token test runs on lowercased paths (raw VerSe'20 spells GL003/GL003.nii.gz, staging spells gl003), so
#            a key_regex is written in lowercase.
# A pair whose dup or canonical path passes through a symlinked directory below its member root is reported as
# via_link and never paired: such a link can lead onto HOME or into a .pre-ceph copy.
# Depth: sizes first. relpath/rename/pairs groups whose paired bytes are under FULL_HASH_GB are hashed in full;
# larger ones get a sample stratified by first directory (SAMPLE_N files) plus every pair whose sizes differ, and
# the result says coverage=sample (dedup_apply.sbatch re-hashes every file it touches anyway). content groups hash
# every same-size candidate, because the hash is the pairing.
#
# Output: hash_results/<gid>.json (verdict, counts, one record per file) and hash_results/<gid>.tsv (the same
# records, read by dedup_apply.sbatch). Verdicts: identical | different | missing | review (a content twin under a
# different series token) | none (no pair) | not_ready (a gate failed). via_link records do not change the verdict:
# they are never paired, and dedup_apply.sbatch re-checks every path it touches anyway.
# Rules from CLAUDE.md: never on the login node; output under the submit directory (-D); no /tmp (TMPDIR, which bash
# older than 5.1 uses for here-strings, is set to /dev/shm/dedup.<job> or logs/tmp.<job> and removed at exit).
set -uo pipefail
if [ -z "${SLURM_JOB_ID:-}" ]; then echo "refusing: run this with sbatch, never on the login node"; exit 2; fi
case "$(hostname)" in warrior*) echo "refusing on the login node"; exit 2;; esac
DEDUP_DIR=${DEDUP_DIR:-$PWD}
# shellcheck source=dedup_lib.sh
. "$DEDUP_DIR/dedup_lib.sh" || { echo "no $DEDUP_DIR/dedup_lib.sh"; exit 2; }
mkdir -p "$DEDUP_DIR/logs"
setup_tmpdir || { echo "refusing: no writable TMPDIR under /dev/shm or logs/"; exit 2; }
trap cleanup_tmpdir EXIT
FULL_HASH_GB=${FULL_HASH_GB:-50}
SAMPLE_N=${SAMPLE_N:-200}
mkdir -p "$RESULTS" "$DEDUP_DIR/logs"
[ -f "$PLAN_TSV" ] || { echo "no $PLAN_TSV"; exit 2; }
echo "DEDUP_HASH start $(now_utc) host $(hostname) job $SLURM_JOB_ID"
if jobs_scan; then echo "running/pending jobs scanned"; else echo "WARNING: squeue not available; batch-busy check skipped (read-only job)"; fi
GIDS=${GROUP_IDS:-$(plan_gids | tr '\n' ' ')}

# ---------------------------------------------------------------- per-group state
declare -a E_STATUS E_DUP E_CAN E_SIZE E_SHAD E_SHAC E_NOTE
add() { E_STATUS+=("$1"); E_DUP+=("$2"); E_CAN+=("$3"); E_SIZE+=("$4"); E_SHAD+=("${5:-}"); E_SHAC+=("${6:-}"); E_NOTE+=("${7:-}"); }

listing() {    # listing <root> <include> <exclude>: "type<TAB>size<TAB>rel" per non-directory entry, NUL-terminated
  local root=$1 inc=$2 exc=$3 rec ty sz rel
  while IFS= read -r -d '' rec; do
    ty=${rec%%$'\t'*}; rec=${rec#*$'\t'}; sz=${rec%%$'\t'*}; rel=${rec#*$'\t'}
    match_any "$rel" "$inc" || continue
    match_any "$rel" "$exc" && continue
    printf '%s\t%s\t%s\0' "$ty" "$sz" "$rel"
  done < <(find "$root" -mindepth 1 ! -type d -printf '%y\t%s\t%P\0' 2>/dev/null)
}

tokens() {     # every match of regex $2 in $1, space-separated
  local s=$1 re=$2 out=" " m
  while [[ $s =~ $re ]]; do
    m=${BASH_REMATCH[0]}; [ -n "$m" ] || break
    out+="$m "; s=${s#*"$m"}
  done
  printf '%s' "$out"
}

key_ok() {     # key_ok <dup rel> <canon rel> <key_regex>: compared in lowercase (GL003 in raw/verse20, gl003 in staging)
  local a=${1,,} b=${2,,} re=$3 t
  [[ -z $re || $re == - ]] && return 0
  if [ "$re" = "BASENAME" ]; then [ "${a##*/}" = "${b##*/}" ]; return; fi
  local ta tb; ta=$(tokens "$a" "$re"); tb=$(tokens "$b" "$re")
  for t in $ta; do [[ $tb == *" $t "* ]] && return 0; done
  return 1
}

renamed() {    # renamed <rel> <map old=>new;...>: dir/<basename with the first matching rule applied>
  local rel=$1 map=$2 base dir rule old new arr
  base=${rel##*/}; dir=; [[ $rel == */* ]] && dir=${rel%/*}/
  IFS=';' read -r -a arr <<< "$map"
  for rule in "${arr[@]}"; do
    old=${rule%%=>*}; new=${rule#*=>}
    [ -n "$old" ] || continue
    if [[ $base == *"$old"* ]]; then printf '%s%s' "$dir" "${base/"$old"/$new}"; return 0; fi
  done
  printf '%s' "$rel"
}

# ---------------------------------------------------------------- pairing by name (relpath, rename, pairs)
# P_* hold candidate pairs before hashing
declare -a P_DUP P_CAN P_SD P_SC
pair_by_name() {   # pair_by_name <mode> <dup_root> <dup_include> <canon_root> <exclude> <rename_map> <pairs> <allow_unpaired>
  local mode=$1 droot=$2 dinc=$3 croot=$4 exc=$5 map=$6 pairs=$7 allow=$8 rec ty sz rel crel cp arr pr
  if [ -L "$droot" ]; then add already_link "$droot" "$croot" "" "" "" "-> $(readlink -- "$droot") (the whole root)"; return; fi
  if [ "$mode" = "pairs" ]; then
    IFS='|' read -r -a arr <<< "$pairs"
    for pr in "${arr[@]}"; do
      rel=${pr%%=>*}; crel=${pr#*=>}
      local dp="$droot/$rel"; cp="$croot/$crel"
      if [ -L "$dp" ]; then add already_link "$dp" "$cp" "" "" "" "-> $(readlink -- "$dp")"; continue; fi
      if [ -e "$dp" ] && ! clean_below "$droot" "$dp"; then add via_link "$dp" "$cp" "" "" "" "the duplicate is reached through a symlinked directory (resolves to $(readlink -f -- "$dp"))"; continue; fi
      if [ -e "$cp" ] && ! clean_below "$croot" "$cp"; then add via_link "$dp" "$cp" "" "" "" "the canonical is reached through a symlinked directory (resolves to $(readlink -f -- "$cp"))"; continue; fi
      if [ ! -f "$dp" ]; then
        if [ "$allow" = "1" ]; then add unpaired "$dp" "$cp" "" "" "" "declared duplicate absent"; else add missing_duplicate "$dp" "$cp"; fi
        continue; fi
      if [ ! -f "$cp" ] || [ -L "$cp" ]; then add missing_canonical "$dp" "$cp" "$(size_of "$dp")"; continue; fi
      P_DUP+=("$dp"); P_CAN+=("$cp"); P_SD+=("$(size_of "$dp")"); P_SC+=("$(size_of "$cp")")
    done
    return
  fi
  while IFS= read -r -d '' rec; do
    ty=${rec%%$'\t'*}; rec=${rec#*$'\t'}; sz=${rec%%$'\t'*}; rel=${rec#*$'\t'}
    crel=$rel; [ "$mode" = "rename" ] && crel=$(renamed "$rel" "$map")
    cp="$croot/$crel"
    if [ "$ty" = "l" ]; then add already_link "$droot/$rel" "$cp" "" "" "" "-> $(readlink -- "$droot/$rel")"; continue; fi
    [ "$ty" = "f" ] || { add unpaired "$droot/$rel" "" "$sz" "" "" "not a regular file (type $ty)"; continue; }
    if [ "$droot/$rel" = "$cp" ]; then continue; fi
    if { [ -e "$cp" ] || [ -L "$cp" ]; } && ! clean_below "$croot" "$cp"; then
      add via_link "$droot/$rel" "$cp" "$sz" "" "" "the canonical is reached through a symlinked directory (resolves to $(readlink -f -- "$cp"))"; continue; fi
    if [ ! -f "$cp" ] || [ -L "$cp" ]; then
      if [ "$allow" = "1" ]; then add unpaired "$droot/$rel" "$cp" "$sz" "" "" "no canonical counterpart"; else add missing_canonical "$droot/$rel" "$cp" "$sz"; fi
      continue; fi
    P_DUP+=("$droot/$rel"); P_CAN+=("$cp"); P_SD+=("$sz"); P_SC+=("$(size_of "$cp")")
  done < <(listing "$droot" "$dinc" "$exc")
}

hash_pairs() {     # hash_pairs <coverage all|sample>: resolve P_* into E_* records
  local cov=$1 n=${#P_DUP[@]} i hd hc
  local -A pick=()
  if [ "$cov" = "sample" ] && [ "$n" -gt 0 ]; then
    local -A members=() count=()
    local s rel
    for ((i = 0; i < n; i++)); do
      rel=${P_DUP[i]#"$CUR_DROOT"/}; s=${rel%%/*}; [[ $rel == */* ]] || s=.
      members[$s]+="$i "; count[$s]=$(( ${count[$s]:-0} + 1 ))
    done
    for s in "${!members[@]}"; do
      local idx=(${members[$s]}) ns=${count[$s]} q j k
      q=$(( (SAMPLE_N * ns + n - 1) / n )); [ "$q" -lt 2 ] && q=2; [ "$q" -gt "$ns" ] && q=$ns
      if [ "$q" -le 1 ]; then pick[${idx[0]}]=1; continue; fi
      for ((j = 0; j < q; j++)); do k=$(( j * (ns - 1) / (q - 1) )); pick[${idx[k]}]=1; done
    done
  fi
  for ((i = 0; i < n; i++)); do
    local dp=${P_DUP[i]} cp=${P_CAN[i]} sd=${P_SD[i]} sc=${P_SC[i]}
    if [ "$(ino_of "$dp")" = "$(ino_of "$cp")" ]; then add same_inode "$dp" "$cp" "$sd" "" "" "already one file (hard link)"; continue; fi
    if [ "$sd" != "$sc" ]; then
      hd=$(sha_of "$dp"); hc=$(sha_of "$cp")
      add size_differs "$dp" "$cp" "$sd" "$hd" "$hc" "canonical size $sc"; continue; fi
    if [ "$cov" = "sample" ] && [ -z "${pick[$i]:-}" ]; then add unhashed_size_equal "$dp" "$cp" "$sd"; continue; fi
    hd=$(sha_of "$dp") || { add missing_duplicate "$dp" "$cp" "$sd" "" "" "unreadable"; continue; }
    hc=$(sha_of "$cp") || { add missing_canonical "$dp" "$cp" "$sd" "" "" "unreadable"; continue; }
    if [ "$hd" = "$hc" ]; then add identical "$dp" "$cp" "$sd" "$hd" "$hc"; else add different "$dp" "$cp" "$sd" "$hd" "$hc"; fi
  done
}

# ---------------------------------------------------------------- pairing by content
pair_by_content() {  # pair_by_content <dup_root> <dup_include> <canon_roots a|b> <canon_include> <exclude> <key_regex>
  local droot=$1 dinc=$2 croots=$3 cinc=$4 exc=$5 key=$6 rec ty sz rel cr arr cp
  if [ -L "$droot" ]; then add already_link "$droot" "" "" "" "" "-> $(readlink -- "$droot") (the whole root)"; return; fi
  local -A by_size=() chash=() crel_of=()
  IFS='|' read -r -a arr <<< "$croots"
  for cr in "${arr[@]}"; do
    while IFS= read -r -d '' rec; do
      ty=${rec%%$'\t'*}; rec=${rec#*$'\t'}; sz=${rec%%$'\t'*}; rel=${rec#*$'\t'}
      [ "$ty" = "f" ] || continue
      by_size[$sz]+="$cr/$rel"$'\n'; crel_of["$cr/$rel"]=$rel
    done < <(listing "$cr" "$cinc" "$exc")
  done
  while IFS= read -r -d '' rec; do
    ty=${rec%%$'\t'*}; rec=${rec#*$'\t'}; sz=${rec%%$'\t'*}; rel=${rec#*$'\t'}
    local dp="$droot/$rel"
    if [ "$ty" = "l" ]; then add already_link "$dp" "" "" "" "" "-> $(readlink -- "$dp")"; continue; fi
    [ "$ty" = "f" ] || continue
    local cands=${by_size[$sz]:-}
    if [ -z "$cands" ]; then add unpaired "$dp" "" "$sz" "" "" "no canonical file of the same size"; continue; fi
    local hd twin="" cpath
    hd=$(sha_of "$dp") || { add missing_duplicate "$dp" "" "$sz" "" "" "unreadable"; continue; }
    while IFS= read -r cpath; do
      [ -n "$cpath" ] || continue
      [ "$cpath" = "$dp" ] && continue
      [ -n "${chash[$cpath]:-}" ] || chash[$cpath]=$(sha_of "$cpath")
      if [ "${chash[$cpath]}" = "$hd" ]; then twin=$cpath; break; fi
    done <<< "$cands"
    if [ -z "$twin" ]; then add unpaired "$dp" "" "$sz" "$hd" "" "no canonical file with the same sha256"; continue; fi
    if [ "$(ino_of "$dp")" = "$(ino_of "$twin")" ]; then add same_inode "$dp" "$twin" "$sz" "$hd" "$hd" "already one file (hard link)"; continue; fi
    if ! key_ok "$rel" "${crel_of[$twin]}" "$key"; then add key_mismatch "$dp" "$twin" "$sz" "$hd" "$hd" "same bytes under another key ($key)"; continue; fi
    add identical "$dp" "$twin" "$sz" "$hd" "$hd"
  done < <(listing "$droot" "$dinc" "$exc")
}

# ---------------------------------------------------------------- one group
write_result() {   # write_result <gid> <verdict> <reason> <coverage> <rows_json> <mode>
  local gid=$1 verdict=$2 reason=$3 cov=$4 rows=$5 mode=$6 out="$RESULTS/$1.json" tsv="$RESULTS/$1.tsv" i
  local -A c=(); local bytes_ident=0
  for i in "${!E_STATUS[@]}"; do
    c[${E_STATUS[i]}]=$(( ${c[${E_STATUS[i]}]:-0} + 1 ))
    [ "${E_STATUS[i]}" = "identical" ] && bytes_ident=$(( bytes_ident + ${E_SIZE[i]:-0} ))
  done
  {
    printf '# group %s  job %s  %s  verdict %s\n' "$gid" "$SLURM_JOB_ID" "$(now_utc)" "$verdict"
    printf '#status\tdup\tcanonical\tbytes\tsha256_dup\tsha256_canonical\tnote\n'
    for i in "${!E_STATUS[@]}"; do
      printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "${E_STATUS[i]}" "${E_DUP[i]}" "${E_CAN[i]}" "${E_SIZE[i]}" "${E_SHAD[i]}" "${E_SHAC[i]}" "${E_NOTE[i]}"
    done
  } > "$tsv.tmp" && mv -f "$tsv.tmp" "$tsv"
  {
    printf '{\n'
    printf '  "group_id": "%s",\n' "$(json_esc "$gid")"
    printf '  "verdict": "%s",\n' "$verdict"
    printf '  "verdict_reason": "%s",\n' "$(json_esc "$reason")"
    printf '  "mode": "%s",\n' "$mode"
    printf '  "coverage": "%s",\n' "$cov"
    printf '  "plan_rows_sha256": "%s",\n' "$(plan_rows_sha "$gid")"
    printf '  "generated": "%s",\n' "$(now_utc)"
    printf '  "job": "%s",\n' "$SLURM_JOB_ID"
    printf '  "host": "%s",\n' "$(hostname)"
    printf '  "full_hash_gb": %s,\n  "sample_n": %s,\n' "$FULL_HASH_GB" "$SAMPLE_N"
    printf '  "bytes_identical": %s,\n' "$bytes_ident"
    printf '  "counts": {'
    local first=1 k
    for k in identical different size_differs missing_canonical missing_duplicate unpaired key_mismatch already_link same_inode unhashed_size_equal via_link; do
      [ $first = 1 ] || printf ', '; first=0; printf '"%s": %s' "$k" "${c[$k]:-0}"
    done
    printf '},\n'
    printf '  "rows": [%s],\n' "$rows"
    printf '  "files": [\n'
    local sep=""
    for i in "${!E_STATUS[@]}"; do
      printf '%s    {"status": "%s", "dup": "%s", "canonical": "%s", "bytes": %s, "sha256_dup": "%s", "sha256_canonical": "%s", "note": "%s"}' \
        "$sep" "${E_STATUS[i]}" "$(json_esc "${E_DUP[i]}")" "$(json_esc "${E_CAN[i]}")" "${E_SIZE[i]:-null}" \
        "${E_SHAD[i]}" "${E_SHAC[i]}" "$(json_esc "${E_NOTE[i]}")"
      sep=$',\n'
    done
    printf '\n  ]\n}\n'
  } > "$out.tmp" && mv -f "$out.tmp" "$out"
  printf 'GROUP %s verdict=%s coverage=%s identical=%s different=%s size_differs=%s missing=%s unpaired=%s key_mismatch=%s via_link=%s bytes_identical=%s %s\n' \
    "$gid" "$verdict" "$cov" "${c[identical]:-0}" "${c[different]:-0}" "${c[size_differs]:-0}" \
    "$(( ${c[missing_canonical]:-0} + ${c[missing_duplicate]:-0} ))" "${c[unpaired]:-0}" "${c[key_mismatch]:-0}" "${c[via_link]:-0}" "$bytes_ident" "$reason"
}

hash_group() {
  local gid=$1 line rows_json="" sep="" not_ready="" mode="" kind cov=all
  E_STATUS=(); E_DUP=(); E_CAN=(); E_SIZE=(); E_SHAD=(); E_SHAC=(); E_NOTE=()
  local -a ROWS=()
  while IFS= read -r line; do ROWS+=("$line"); done < <(plan_rows "$gid")
  if [ "${#ROWS[@]}" -eq 0 ]; then echo "GROUP $gid: not in $PLAN_TSV"; return; fi
  # gates first, for every row
  for line in "${ROWS[@]}"; do
    split_tab "$line"
    kind=${F[1]}; mode=${F[2]}
    local droot=${F[3]} croots=${F[5]} r g arr
    [ "$kind" = "a" ] || { not_ready+="; kind $kind is never hashed"; continue; }
    gate "$droot" dup hash; g=$GATE
    rows_json+="$sep{\"dup_root\": \"$(json_esc "$droot")\", \"dup_gate\": \"$(json_esc "$g")\", \"canonical_roots\": ["
    sep=", "
    [ "$g" = "ok" ] || not_ready+="; $droot: $g"
    IFS='|' read -r -a arr <<< "$croots"
    local s2=""
    for r in "${arr[@]}"; do
      gate "$r" canon hash
      rows_json+="$s2{\"path\": \"$(json_esc "$r")\", \"gate\": \"$(json_esc "$GATE")\"}"; s2=", "
      [ "$GATE" = "ok" ] || not_ready+="; $r: $GATE"
    done
    rows_json+="]}"
  done
  if [ -n "$not_ready" ]; then write_result "$gid" not_ready "${not_ready#; }" none "$rows_json" "$mode"; return; fi
  # pair and hash, row by row
  for line in "${ROWS[@]}"; do
    split_tab "$line"
    local mode=${F[2]} droot=${F[3]} dinc=${F[4]} croots=${F[5]} cinc=${F[6]} exc=${F[7]} key=${F[8]} map=${F[9]} pairs=${F[10]} allow=${F[11]}
    CUR_DROOT=$droot
    if [ "$mode" = "content" ]; then
      pair_by_content "$droot" "$dinc" "$croots" "$cinc" "$exc" "$key"
    else
      P_DUP=(); P_CAN=(); P_SD=(); P_SC=()
      pair_by_name "$mode" "$droot" "$dinc" "${croots%%|*}" "$exc" "$map" "$pairs" "$allow"
      local tot=0 i
      for i in "${!P_SD[@]}"; do tot=$(( tot + P_SD[i] )); done
      local rowcov=all
      [ "$tot" -ge $(( FULL_HASH_GB * 1000000000 )) ] && rowcov=sample
      [ "$rowcov" = "sample" ] && cov=sample
      hash_pairs "$rowcov"
    fi
  done
  local -A c=(); local i
  for i in "${!E_STATUS[@]}"; do c[${E_STATUS[i]}]=$(( ${c[${E_STATUS[i]}]:-0} + 1 )); done
  local verdict reason
  if [ $(( ${c[different]:-0} + ${c[size_differs]:-0} )) -gt 0 ]; then verdict=different; reason="$(( ${c[different]:-0} + ${c[size_differs]:-0} )) paired file(s) differ"
  elif [ $(( ${c[missing_canonical]:-0} + ${c[missing_duplicate]:-0} )) -gt 0 ]; then verdict=missing; reason="a declared file has no counterpart"
  elif [ "${c[key_mismatch]:-0}" -gt 0 ]; then verdict=review; reason="${c[key_mismatch]} byte twin(s) under another key: look before linking"
  elif [ $(( ${c[identical]:-0} + ${c[unhashed_size_equal]:-0} )) -gt 0 ]; then verdict=identical; reason="every paired file matched"
  else verdict=none; reason="no pair found"; fi
  [ "$mode" = "content" ] && cov=all
  write_result "$gid" "$verdict" "$reason" "$cov" "$rows_json" "$mode"
}

for gid in $GIDS; do hash_group "$gid"; done
echo "DEDUP_HASH end $(now_utc)"
exit 0
