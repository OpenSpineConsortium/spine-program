#!/bin/bash
# test_dedup.sh -- dedup_hash.sbatch, dedup_apply.sbatch and dedup_guard.sh on a synthetic tree (run it in WSL or on any
# Linux box; it never touches the grid, HOME data or Ceph). Fake Slurm: squeue/scontrol/sacct stubs on PATH,
# SLURM_JOB_ID set by hand. The fake layout mirrors the real one: a Ceph root, a HOME root, plan/batch_items +
# plan/runs/<B>/STATUS + CUTOVER logs, and the HOME src of each batch item cut over to its Ceph dst.
#
#   DEDUP_TEST_ROOT=<folder> bash test_dedup.sh     # the tree goes in a fresh folder under it (default: .test_tmp next
#                                                   # to this script; never /tmp, which the grid sweeps); KEEP=1 keeps it
#
# Cases: T01 identical trees -> one tree symlink, then ROLLBACK restores the bytes; T02 a one-byte difference ->
# verdict different, apply refuses; T03a/T03b a HOME path (spelled, and resolved through a Ceph-spelled link) ->
# refused; T04 a file changed after the hash -> that file refused, the rest linked file by file; T05 a batch not
# finalized (.pre-ceph present) -> refused; T06 sampled coverage -> apply re-hashes and links; T07 content pairing
# across names; T07b same bytes under another series token -> review, refused; T08 explicit pairs + read-only
# canonical blocks a write through the link, rollback restores; T09 a running job names the path -> refused;
# T10 a .pre-ceph member -> refused; T11 a held group -> refused until ALLOW_HOLD; T12 a literal '(1)' rename
# pattern written as a bracket expression pairs only the '(1)' file; TB1 kind (b) never linked.
# Review cases (2026-10-08): X1 a pairs-mode duplicate through a directory symlink onto HOME; X2 a relpath canonical
# through a directory symlink onto HOME; X3 the duplicate written between its hash and its swap; X4 a file written into
# a duplicate tree while it is swapped; X5a a Ceph-native canonical rewritten in place (blocked by the read-only bit);
# X5b the same by a writer that restores the write bit first (caught by the re-stat); X6 a batch re-run after its
# cut-over (ALREADY_SYMLINK); X7 the ledger cannot be written; X8 a hard-linked duplicate; X9 rollback restores the
# recorded mtime; X10 rollback refuses a tree root that links elsewhere; X11 a canonical shared by two groups stays
# read-only until the last rollback, and dedup_guard.sh refuses its deletion while links are live; X12 no link chain
# across groups; X13 GL003 (raw spelling) pairs with gl003; X14 a job naming the member relative to its WorkDir;
# X15 a DRY run does not overwrite the last real summary; X16 a stale lock is taken over only on proof the holder
# ended; X17 artefacts of a killed apply refuse the group until ROLLBACK resolves them; X18 TERM finishes the swap in
# flight and stops.
set -u
SRC=$(cd "$(dirname "$0")" && pwd)
ROOT=${DEDUP_TEST_ROOT:-$SRC/.test_tmp}
mkdir -p "$ROOT"
T=$(mktemp -d "$ROOT/dedup_test.XXXXXX")
[ "${KEEP:-0}" = "1" ] || trap 'chmod -R u+w "$T" 2>/dev/null; rm -rf "$T"; rmdir "$ROOT" 2>/dev/null' EXIT
RS=$T/rs/rs_grp_oschome/go2432
HM=$T/wsu/home/go/go24/go2432
PLAN=$T/plan
D=$T/dedup
BIN=$T/bin
WRAP=$T/wrap
mkdir -p "$RS/data" "$HM" "$PLAN/batch_items" "$PLAN/runs/BT1" "$PLAN/runs/BT2" "$PLAN/runs/BT3" "$D" "$BIN" "$WRAP"
cp "$SRC/dedup_lib.sh" "$SRC/dedup_hash.sbatch" "$SRC/dedup_apply.sbatch" "$SRC/dedup_guard.sh" "$D/"
PASS=0; FAIL=0
ok()   { PASS=$((PASS + 1)); echo "  ok   $1"; }
bad()  { FAIL=$((FAIL + 1)); echo "  FAIL $1"; }
check(){ local d=$1; shift; if "$@"; then ok "$d"; else bad "$d"; fi; }
sha()  { local h; h=$(sha256sum -- "$1"); printf '%s' "${h%% *}"; }

# ---------------------------------------------------------------- fake Slurm
cat > "$BIN/squeue" <<'EOS'
#!/bin/bash
prev=
for a in "$@"; do
  if [ "$prev" = "-j" ]; then
    [ -f "${STUB_DIR:-/nonexistent}/sq_j_$a.err" ] && { cat "$STUB_DIR/sq_j_$a.err" >&2; exit 1; }
    [ -f "${STUB_DIR:-/nonexistent}/sq_j_$a.out" ] && cat "$STUB_DIR/sq_j_$a.out"
    exit 0
  fi
  prev=$a
done
[ -f "${STUB_SQUEUE:-/nonexistent}" ] && cat "$STUB_SQUEUE"
exit 0
EOS
cat > "$BIN/scontrol" <<'EOS'
#!/bin/bash
if [ "$1" = "show" ] && [ "$2" = "job" ]; then f="${STUB_DIR:-/nonexistent}/job_$3.txt"; [ -f "$f" ] && cat "$f"; fi
exit 0
EOS
chmod +x "$BIN/squeue" "$BIN/scontrol"
export PATH="$BIN:$PATH" RS_ROOT="$RS" HOME_ROOTS="$T/wsu/home" PLAN_DIR="$PLAN" DEDUP_DIR="$D" STUB_DIR="$T" \
       STUB_SQUEUE="$T/squeue.out" DEDUP_GUARD_ANYWHERE=1
unset LEDGER2_DIR DEDUP_TMP
: > "$T/squeue.out"
run_hash()  { (cd "$D" && HOME=$HM SLURM_JOB_ID=h$RANDOM bash "$D/dedup_hash.sbatch") > "$T/last_hash.log" 2>&1; }
run_apply() { (cd "$D" && HOME=$HM SLURM_JOB_ID=a$RANDOM PATH="${XPATH:-}$PATH" bash "$D/dedup_apply.sbatch") > "$T/last_apply.log" 2>&1; }
verdict()   { local l; while IFS= read -r l; do [[ $l =~ \"verdict\":\ \"([a-z_]+)\" ]] && { printf '%s' "${BASH_REMATCH[1]}"; return; }; done < "$D/hash_results/$1.json"; }
sumfile()   { grep "^SUMMARY $1 " "${2:-$T/last_apply.log}" | tail -1 | cut -d' ' -f3-; }
state()     { local f l; f=$(sumfile "$1" "${2:-}"); [ -n "$f" ] && [ -f "$f" ] || { printf 'none'; return; }
              while IFS= read -r l; do [[ $l =~ \"state\":\ \"([a-z_]+)\" ]] && { printf '%s' "${BASH_REMATCH[1]}"; return; }; done < "$f"; }
forge()     { # forge <gid> <dup> <canonical> <bytes>: an identical verdict the hash job would not give
  printf '{\n  "group_id": "%s",\n  "verdict": "identical",\n  "plan_rows_sha256": "%s"\n}\n' "$1" "$(cd "$D" && PLAN_TSV="$P" DEDUP_DIR="$D" bash -c '. ./dedup_lib.sh; plan_rows_sha "$0"' "$1")" > "$D/hash_results/$1.json"
  printf 'identical\t%s\t%s\t%s\t\t\t\n' "$2" "$3" "$4" > "$D/hash_results/$1.tsv"; }

# ---------------------------------------------------------------- the holding
# batch BT1: ~/t -> $RS/data/t, VERIFIED, cut over, FINALIZED.  batch BT2: ~/t5 -> $RS/data/t5, cut over, not finalized
# batch BT3: ~/t3 -> $RS/data/t3, re-run after the cut-over (latest STATUS ALREADY_SYMLINK, an earlier one VERIFIED)
C=$RS/data/t
mkf() { mkdir -p "$(dirname "$1")"; printf '%s' "$2" > "$1"; }
for r in canA dupA; do mkf "$C/$r/a.bin" "alpha-0123456789"; mkf "$C/$r/sub/b.bin" "bravo-bytes"; mkf "$C/$r/sub/c.txt" "charlie"; done
mkf "$C/canB/x.bin" "same-length-AAAA"; mkf "$C/dupB/x.bin" "same-length-AAAB"; mkf "$C/canB/y.bin" "yy"; mkf "$C/dupB/y.bin" "yy"
for r in canD dupD; do mkf "$C/$r/x" "xxxxxxxx"; mkf "$C/$r/y" "yyyyyyyy"; mkf "$C/$r/z" "zzzzzzzz"; done
mkf "$C/dupD/only_in_dup" "extra"                              # forces file mode for T04
for r in canF dupF; do for i in 1 2 3 4 5 6; do mkf "$C/$r/s$((i % 2))/f$i" "file-$i-content"; done; done
mkf "$C/canE/verse019_CT-iso.nii.gz" "CT-019"; mkf "$C/canE/verse019_CT-iso_seg.nii.gz" "SEG-019"; mkf "$C/canE/gl003_CT-iso.nii.gz" "CT-gl3"
mkf "$C/dupE/rawdata/verse019.nii.gz" "CT-019"; mkf "$C/dupE/rawdata/verse019_seg.nii.gz" "SEG-019"; mkf "$C/dupE/rawdata/gl003.nii.gz" "CT-gl3"
mkf "$C/dupE/rawdata/verse019_ctd.json" "ctd-asl-space"         # no twin: stays a file
mkf "$C/canE2/verse021_CT-iso.nii.gz" "CT-shared"; mkf "$C/dupE2/verse020.nii.gz" "CT-shared"
mkf "$C/bank/rung_2.npz" "rung-bytes-identical"; mkf "$C/bank/rung_3.npz" "rung-bytes-identical"; mkf "$C/bank/rung_4.npz" "rung-bytes-identical"
for r in canJ dupJ; do mkf "$C/$r/j.bin" "jjj"; done
for r in canK dupK; do mkf "$C/$r/k.bin" "kkk"; done
for r in canH dupH; do mkf "$C/$r/h.bin" "hhh"; done
mkf "$C/paren/x.jpg" "xjpg"; mkf "$C/paren/x(1).jpg" "xjpg"; mkf "$C/paren/y1.jpg" "y1"; mkf "$C/paren/z11.jpg" "zz"
mkdir -p "$C/old.pre-ceph"; mkf "$C/old.pre-ceph/p.bin" "ppp"; mkf "$C/canP/p.bin" "ppp"
mkf "$HM/homecopy/a.bin" "alpha-0123456789"; mkf "$HM/homecopy/sub/b.bin" "bravo-bytes"; mkf "$HM/homecopy/sub/c.txt" "charlie"
ln -s "$HM/homecopy" "$C/homelink"                              # a Ceph spelling that resolves onto HOME
mkf "$RS/data/t5/dup/q.bin" "qqq"; mkf "$RS/data/t5/can/q.bin" "qqq"
# review holdings
mkdir -p "$HM/homedir"; mkf "$HM/homedir/f.bin" "same-bytes-X1"; mkdir -p "$C/bankP"; ln -s "$HM/homedir" "$C/bankP/sub"; mkf "$C/canX1/f.bin" "same-bytes-X1"
mkf "$C/dupR/sub/f.bin" "same-bytes-X2"; mkdir -p "$HM/homedir2" "$C/canR"; mkf "$HM/homedir2/f.bin" "same-bytes-X2"; ln -s "$HM/homedir2" "$C/canR/sub"
mkf "$C/bankT/r2.npz" "rung-bytes"; mkf "$C/bankT/r3.npz" "rung-bytes"
for r in canW dupW; do mkf "$C/$r/a.bin" "aaaa"; mkf "$C/$r/s/b.bin" "bbbb"; done
mkf "$RS/data/native/c.bin" "native-0001"; mkf "$C/dupN/c.bin" "native-0001"; mkf "$C/dupN/extra" "forces-file-mode"
mkf "$RS/data/native2/c.bin" "native-0002"; mkf "$C/dupN2/c.bin" "native-0002"; mkf "$C/dupN2/extra" "forces-file-mode"
C3=$RS/data/t3; mkf "$C3/dup/q.bin" "qqq"; mkf "$C3/can/q.bin" "qqq"
mkf "$C/canL/l.bin" "llll"; mkf "$C/dupL/l.bin" "llll"; mkf "$C/dupL/extra" "keeps-file-mode"
mkf "$C/canHL/h.bin" "hhhh"; mkf "$C/dupHL/h.bin" "hhhh"; mkdir -p "$C/other"; ln "$C/dupHL/h.bin" "$C/other/h_hardlink.bin"
mkf "$C/canM/m.bin" "mmmm"; mkf "$C/dupM/m.bin" "mmmm"; mkf "$C/dupM/extra" "file-mode"; touch -m -d '2026-01-02 03:04:05.123456789' "$C/dupM/m.bin"
for r in canQ dupQ canQ2; do mkf "$C/$r/q1.bin" "q1"; mkf "$C/$r/d/q2.bin" "q2"; done
mkf "$C/canS/s.bin" "shared-canonical"; mkf "$C/dupS1/s.bin" "shared-canonical"; mkf "$C/dupS2/s.bin" "shared-canonical"
mkf "$C/dupS1/extra1" "e1"; mkf "$C/dupS2/extra2" "e2"
mkf "$C/chainA/x" "chain-bytes"; mkf "$C/chainB/x" "chain-bytes"; mkf "$C/chainC/x" "chain-bytes"
mkf "$C/chainA/extraA" "a"; mkf "$C/chainB/extraB" "b"
mkf "$C/dupG/GL003/GL003.nii.gz" "gl-bytes"; mkf "$C/canG/gl003_CT-iso.nii.gz" "gl-bytes"
for r in canJ2 dupJ2; do mkf "$C/$r/j.bin" "j2j2"; done
for r in canV dupV; do mkf "$C/$r/v.bin" "vvvv"; done; mkf "$C/dupV/extra" "x"; ln "$C/dupV/v.bin" "$C/dupV/v.bin.dedup_hold.123"
for r in canZ dupZ; do for i in 1 2 3; do mkf "$C/$r/z$i.bin" "zzz-$i"; done; done; mkf "$C/dupZ/extra" "file-mode"
ln -s "$C" "$HM/t"; ln -s "$RS/data/t5" "$HM/t5"; mkdir -p "$HM/t5.pre-ceph"; ln -s "$C3" "$HM/t3"
printf '# src\tdst\test_gb\tflags\n%s\t%s\t\t-\n' "$HM/t" "$C" > "$PLAN/batch_items/BT1.tsv"
printf '# src\tdst\test_gb\tflags\n%s\t%s\t\t-\n' "$HM/t5" "$RS/data/t5" > "$PLAN/batch_items/BT2.tsv"
printf '# src\tdst\test_gb\tflags\n%s\t%s\t\t-\n' "$HM/t3" "$C3" > "$PLAN/batch_items/BT3.tsv"
printf '001\tVERIFIED\t%s\t%s\tok\t-\n' "$HM/t" "$C" > "$PLAN/runs/BT1/STATUS.100"; ln -s STATUS.100 "$PLAN/runs/BT1/STATUS"
printf '001 CUT %s -> %s (original kept at %s.pre-ceph)\n001 FINALIZED (compared in full, deleted %s.pre-ceph)\n' "$HM/t" "$C" "$HM/t" "$HM/t" > "$PLAN/runs/BT1/CUTOVER.101"
printf '001\tVERIFIED\t%s\t%s\tok\t-\n' "$HM/t5" "$RS/data/t5" > "$PLAN/runs/BT2/STATUS.200"; ln -s STATUS.200 "$PLAN/runs/BT2/STATUS"
printf '001\tVERIFIED\t%s\t%s\tok\t-\n' "$HM/t3" "$C3" > "$PLAN/runs/BT3/STATUS.299"
printf '001\tALREADY_SYMLINK\t%s\t-> %s\t-\t-\n' "$HM/t3" "$C3" > "$PLAN/runs/BT3/STATUS.300"; ln -s STATUS.300 "$PLAN/runs/BT3/STATUS"
printf '001 FINALIZED (compared in full, deleted %s.pre-ceph)\n' "$HM/t3" > "$PLAN/runs/BT3/CUTOVER.301"

# gid kind mode dup_root dup_include canon_roots canon_include exclude key rename pairs allow_unpaired hold est_gb
P=$D/dedup_plan.tsv
rel() { printf '%s\ta\trelpath\t%s\t*\t%s\t-\t-\t-\t-\t-\t%s\t-\t0\n' "$1" "$2" "$3" "${4:-0}"; }
{
  printf '# test plan\n'
  rel T01 "$C/dupA" "$C/canA"
  rel T02 "$C/dupB" "$C/canB"
  rel T03a "$HM/homecopy" "$C/canA"
  rel T03b "$C/homelink" "$C/canA"
  rel T04 "$C/dupD" "$C/canD" 1
  rel T05 "$RS/data/t5/dup" "$RS/data/t5/can"
  rel T06 "$C/dupF" "$C/canF"
  printf 'T07\ta\tcontent\t%s\t*\t%s\t*\t-\t(verse|gl)[0-9]{3}\t-\t-\t0\t-\t0\n' "$C/dupE" "$C/canE"
  printf 'T07b\ta\tcontent\t%s\t*\t%s\t*\t-\t(verse|gl)[0-9]{3}\t-\t-\t0\t-\t0\n' "$C/dupE2" "$C/canE2"
  printf 'T08\ta\tpairs\t%s\t-\t%s\t-\t-\t-\t-\trung_3.npz=>rung_2.npz|rung_4.npz=>rung_2.npz\t0\t-\t0\n' "$C/bank" "$C/bank"
  rel T09 "$C/dupJ" "$C/canJ"
  rel T10 "$C/old.pre-ceph" "$C/canP"
  printf 'T11\ta\trelpath\t%s\t*\t%s\t-\t-\t-\t-\t-\t0\tremoval_preferred\t0\n' "$C/dupH" "$C/canH"
  printf 'T12\ta\trename\t%s\t*[(]1[)]*\t%s\t-\t-\t-\t(1)=>\t-\t0\t-\t0\n' "$C/paren" "$C/paren"
  printf 'TB1\tb\t-\t%s\t-\t%s\t-\t-\t-\t-\t-\t0\t-\t0\n' "$C/dupK" "$C/canK"
  printf 'X1\ta\tpairs\t%s\t-\t%s\t-\t-\t-\t-\tsub/f.bin=>f.bin\t0\t-\t0\n' "$C/bankP" "$C/canX1"
  rel X2 "$C/dupR" "$C/canR"
  printf 'X3\ta\tpairs\t%s\t-\t%s\t-\t-\t-\t-\tr3.npz=>r2.npz\t0\t-\t0\n' "$C/bankT" "$C/bankT"
  rel X4 "$C/dupW" "$C/canW"
  rel X5a "$C/dupN" "$RS/data/native" 1
  rel X5b "$C/dupN2" "$RS/data/native2" 1
  rel X6 "$C3/dup" "$C3/can"
  rel X7 "$C/dupL" "$C/canL" 1
  rel X8 "$C/dupHL" "$C/canHL"
  rel X9 "$C/dupM" "$C/canM" 1
  rel X10 "$C/dupQ" "$C/canQ"
  rel X11a "$C/dupS1" "$C/canS" 1
  rel X11b "$C/dupS2" "$C/canS" 1
  rel X12a "$C/chainA" "$C/chainB" 1
  rel X12b "$C/chainB" "$C/chainC" 1
  printf 'X13\ta\tcontent\t%s\t*\t%s\t*\t-\t(verse|gl)[0-9]{3}\t-\t-\t0\t-\t0\n' "$C/dupG" "$C/canG"
  rel X14 "$C/dupJ2" "$C/canJ2"
  rel X17 "$C/dupV" "$C/canV" 1
  rel X18 "$C/dupZ" "$C/canZ" 1
} > "$P"
declare -A ORIG=()
for f in a.bin sub/b.bin sub/c.txt; do ORIG[$f]=$(sha "$C/dupA/$f"); done

echo "== hash (all kind-a groups)"
run_hash; grep '^GROUP' "$T/last_hash.log" | cut -c1-200 | sed 's/^/   /'
check "T01 identical trees: verdict identical"            [ "$(verdict T01)" = identical ]
check "T02 one-byte difference: verdict different"        [ "$(verdict T02)" = different ]
check "T03a HOME path: hash not_ready"                    [ "$(verdict T03a)" = not_ready ]
check "T03b Ceph spelling resolving to HOME: not_ready"   [ "$(verdict T03b)" = not_ready ]
check "T04 before the change: verdict identical"          [ "$(verdict T04)" = identical ]
check "T05 cut over, not finalized: hash allowed"         [ "$(verdict T05)" = identical ]
check "T07 content pairs across names: identical"         [ "$(verdict T07)" = identical ]
check "T07b same bytes, other series token: review"       [ "$(verdict T07b)" = review ]
check "T08 explicit pairs: identical"                     [ "$(verdict T08)" = identical ]
check "T10 .pre-ceph member: not_ready"                   [ "$(verdict T10)" = not_ready ]
check "kind (b) group is never hashed"                    [ ! -e "$D/hash_results/TB1.json" ]
check "X1 duplicate through a dir symlink: via_link, not paired" bash -c "grep -q '^via_link' '$D/hash_results/X1.tsv' && ! grep -q '^identical' '$D/hash_results/X1.tsv'"
check "X2 canonical through a dir symlink: via_link, not paired" bash -c "grep -q '^via_link' '$D/hash_results/X2.tsv' && ! grep -q '^identical' '$D/hash_results/X2.tsv'"
check "X6 batch re-run after cut-over (ALREADY_SYMLINK): hash allowed" [ "$(verdict X6)" = identical ]
check "X13 GL003 pairs with gl003 (lowercased key): identical" [ "$(verdict X13)" = identical ]
(cd "$D" && HOME=$HM SLURM_JOB_ID=h1 FULL_HASH_GB=0 SAMPLE_N=2 GROUP_IDS=T06 bash "$D/dedup_hash.sbatch") > "$T/h6.log" 2>&1
check "T06 sampled: coverage sample, verdict identical"   bash -c "grep -q '\"coverage\": \"sample\"' '$D/hash_results/T06.json' && grep -q '\"verdict\": \"identical\"' '$D/hash_results/T06.json' && grep -q unhashed_size_equal '$D/hash_results/T06.tsv'"
check "hash job leaves no TMPDIR behind"                  bash -c "! ls -d /dev/shm/dedup.h1 '$D'/logs/tmp.h1 >/dev/null 2>&1"

echo "== T01 identical trees are symlinked, then rolled back"
GROUP_IDS=T01 run_apply
check "T01 apply state applied"                           [ "$(state T01)" = applied ]
check "T01 dup tree is now one symlink to canA"           eval '[ -L "$C/dupA" ] && [ "$(readlink "$C/dupA")" = "$C/canA" ]'
check "T01 files read the same bytes through the link"    [ "$(sha "$C/dupA/sub/b.bin")" = "${ORIG[sub/b.bin]}" ]
check "T01 canonical made read-only"                      [ ! -w "$C/canA/a.bin" ]
check "T01 no leftover .dedup_old tree"                   bash -c "! ls -d '$C'/dupA.dedup_old.* >/dev/null 2>&1"
check "T01 ledger written twice (primary and Ceph copy)"  bash -c "cmp -s '$D/applied/T01.ledger.tsv' '$RS/dedup_ledgers/T01.ledger.tsv' && grep -q link_tree '$RS/dedup_ledgers/T01.ledger.tsv'"
check "T01 canonical root registered"                     grep -q "^$C/canA"$'\t'"T01" "$RS/dedup_ledgers/CANONICAL_ROOTS.tsv"
GROUP_IDS=T01 ROLLBACK=1 run_apply
check "T01 rollback state rolled_back"                    [ "$(state T01)" = rolled_back ]
check "T01 rollback: dup is a real folder again"          eval '[ -d "$C/dupA" ] && [ ! -L "$C/dupA" ]'
rb=1; for f in a.bin sub/b.bin sub/c.txt; do [ -f "$C/dupA/$f" ] && [ ! -L "$C/dupA/$f" ] && [ "$(sha "$C/dupA/$f")" = "${ORIG[$f]}" ] || rb=0; done
check "T01 rollback restores every file's bytes"          [ "$rb" = 1 ]
check "T01 rollback gives canonical its write bit back"   [ -w "$C/canA/a.bin" ]

echo "== T02 one-byte difference"
GROUP_IDS=T02 run_apply
check "T02 apply refused"                                 [ "$(state T02)" = refused ]
check "T02 dup files untouched"                           eval '[ -f "$C/dupB/x.bin" ] && [ ! -L "$C/dupB/x.bin" ] && [ ! -L "$C/dupB/y.bin" ]'

echo "== T03 HOME paths"
for g in T03a T03b; do
  forge "$g" "$(grep "^$g"$'\t' "$P" | cut -f4)/a.bin" "$C/canA/a.bin" 16
  GROUP_IDS=$g run_apply
  check "$g apply refused even with a forged identical verdict" [ "$(state $g)" = refused ]
done
check "T03a HOME copy untouched"                          eval '[ -f "$HM/homecopy/a.bin" ] && [ ! -L "$HM/homecopy/a.bin" ]'
check "T03b reason names HOME"                            grep -q 'HOME' "$(sumfile T03b)"

echo "== T04 a file changed after the hash"
printf 'X' | dd of="$C/dupD/x" bs=1 seek=3 conv=notrunc status=none
GROUP_IDS=T04 run_apply
check "T04 apply state partial"                           [ "$(state T04)" = partial ]
check "T04 changed file refused, still a regular file"    eval '[ -f "$C/dupD/x" ] && [ ! -L "$C/dupD/x" ]'
check "T04 unchanged files linked file by file"           eval '[ -L "$C/dupD/y" ] && [ -L "$C/dupD/z" ] && [ ! -L "$C/dupD" ]'
check "T04 file outside the pairing untouched"            eval '[ -f "$C/dupD/only_in_dup" ] && [ ! -L "$C/dupD/only_in_dup" ]'
check "T04 no hold or tmp names left"                     bash -c "! find '$C/dupD' -name '*.dedup_*' | grep -q ."

echo "== T05 batch not finalized"
GROUP_IDS=T05 run_apply
check "T05 apply refused (not finalized)"                 grep -q 'not finalized' "$(sumfile T05)"
check "T05 dup untouched"                                 [ ! -L "$RS/data/t5/dup/q.bin" ]

echo "== T06 sampled coverage: apply re-hashes every file"
GROUP_IDS=T06 run_apply
check "T06 every file linked (tree)"                      [ -L "$C/dupF" ]
echo "== X15 a DRY run after a real apply"
GROUP_IDS=T06 DRY=1 run_apply
check "X15 DRY summary written to its own file"           bash -c "ls '$D'/applied/T06.dry.*.json >/dev/null 2>&1"
check "X15 applied/T06.json still records the real apply" grep -q '"state": "applied"' "$D/applied/T06.json"

echo "== T07 content pairing"
GROUP_IDS=T07 run_apply
check "T07 renamed twins linked to their canonical"       [ "$(readlink "$C/dupE/rawdata/verse019.nii.gz")" = "$C/canE/verse019_CT-iso.nii.gz" ]
check "T07 file without a twin stays"                     eval '[ -f "$C/dupE/rawdata/verse019_ctd.json" ] && [ ! -L "$C/dupE/rawdata/verse019_ctd.json" ]'
GROUP_IDS=T07b run_apply
check "T07b review verdict refused"                       [ "$(state T07b)" = refused ]

echo "== T08 explicit pairs, read-only canonical, rollback"
GROUP_IDS=T08 run_apply
check "T08 rung_3 and rung_4 link to rung_2"              eval '[ "$(readlink "$C/bank/rung_3.npz")" = "$C/bank/rung_2.npz" ] && [ -L "$C/bank/rung_4.npz" ]'
( printf 'overwrite' > "$C/bank/rung_3.npz" ) 2>/dev/null
check "T08 a write through the link fails (canonical intact)" [ "$(cat "$C/bank/rung_2.npz")" = "rung-bytes-identical" ]
GROUP_IDS=T08 ROLLBACK=1 run_apply
check "T08 rollback: rung_3 is a file with the original bytes" eval '[ ! -L "$C/bank/rung_3.npz" ] && [ "$(cat "$C/bank/rung_3.npz")" = "rung-bytes-identical" ]'
check "T08 rollback: rung_2 writable again"              [ -w "$C/bank/rung_2.npz" ]

echo "== T09 a running job names the path"
echo "777 train_level R" > "$T/squeue.out"; printf '   Command=/x/train.sh --data %s\n' "$C/dupJ" > "$T/job_777.txt"
GROUP_IDS=T09 run_apply
check "T09 apply refused (a running job names it)"       grep -q 'job names it' "$(sumfile T09)"
: > "$T/squeue.out"
echo "== X14 a job names the member relative to its WorkDir"
echo "778 build R" > "$T/squeue.out"; printf '   WorkDir=%s\n   Command=python src/build.py --out t/dupJ2\n' "$HM" > "$T/job_778.txt"
GROUP_IDS=X14 run_apply
check "X14 apply refused (relative to the job's WorkDir)" grep -q 't/dupJ2 relative to its WorkDir' "$(sumfile X14)"
check "X14 dup untouched"                                 eval '[ ! -L "$C/dupJ2" ] && [ ! -L "$C/dupJ2/j.bin" ]'
: > "$T/squeue.out"

echo "== T10 .pre-ceph member"
forge T10 "$C/old.pre-ceph/p.bin" "$C/canP/p.bin" 3
GROUP_IDS=T10 run_apply
check "T10 apply refused (.pre-ceph)"                     grep -q 'pre-ceph' "$(sumfile T10)"
check "T10 .pre-ceph file untouched"                      [ ! -L "$C/old.pre-ceph/p.bin" ]
echo "== T11 held group"
GROUP_IDS=T11 run_apply
check "T11 held: refused"                                 [ "$(state T11)" = refused ]
GROUP_IDS=T11 ALLOW_HOLD=T11 run_apply
check "T11 released by ALLOW_HOLD: linked"                [ -L "$C/dupH" ]
echo "== T12 a literal '(1)' rename pattern (bash [[ == ]] reads patterns as extglob)"
n12=0; while IFS= read -r l; do [[ $l == identical$'\t'* ]] && n12=$((n12 + 1)); done < "$D/hash_results/T12.tsv"
check "T12 hash pairs only the (1) file"                  [ "$n12" = 1 ]
GROUP_IDS=T12 run_apply
check "T12 x(1).jpg links to x.jpg"                       [ "$(readlink "$C/paren/x(1).jpg")" = "$C/paren/x.jpg" ]
check "T12 names with a 1 but no parentheses untouched"   eval '[ ! -L "$C/paren/y1.jpg" ] && [ ! -L "$C/paren/z11.jpg" ] && [ ! -L "$C/paren/x.jpg" ]'
echo "== TB1 kind (b) is never linked"
forge TB1 "$C/dupK/k.bin" "$C/canK/k.bin" 3
GROUP_IDS=TB1 run_apply
check "TB1 kind (b): refused"                             [ "$(state TB1)" = refused ]

echo "== X1 a pairs-mode duplicate through a directory symlink onto HOME"
forge X1 "$C/bankP/sub/f.bin" "$C/canX1/f.bin" 13
GROUP_IDS=X1 run_apply
check "X1 the HOME original is still a regular file"      eval '[ -f "$HM/homedir/f.bin" ] && [ ! -L "$HM/homedir/f.bin" ]'
check "X1 refused as resolving through a symlink"         grep -q 'symlink' "$(sumfile X1)"
echo "== X2 a relpath canonical through a directory symlink onto HOME"
m2=$(stat -c %a "$HM/homedir2/f.bin")
forge X2 "$C/dupR/sub/f.bin" "$C/canR/sub/f.bin" 13
GROUP_IDS=X2 run_apply
check "X2 the Ceph duplicate is still a regular file"     eval '[ -f "$C/dupR/sub/f.bin" ] && [ ! -L "$C/dupR/sub/f.bin" ]'
check "X2 the HOME file was not chmodded"                 [ "$(stat -c %a "$HM/homedir2/f.bin")" = "$m2" ]

echo "== X3 the duplicate is written between its hash and its swap"
cat > "$WRAP/ln" <<'EOS'
#!/bin/bash
last=${!#}
case "$last" in *.dedup_tmp.*) d=${last%.dedup_tmp.*}; printf 'UNIQUE-LATE-WRITE' >> "$d";; esac
exec /bin/ln "$@"
EOS
chmod +x "$WRAP/ln"
GROUP_IDS=X3 XPATH="$WRAP:" run_apply; rm -f "$WRAP/ln"
check "X3 refused: the duplicate changed while it was hashed" grep -q 'duplicate changed while it was hashed' "$(sumfile X3)"
check "X3 the late bytes survive in the duplicate"        eval '[ ! -L "$C/bankT/r3.npz" ] && grep -q UNIQUE-LATE-WRITE "$C/bankT/r3.npz"'
check "X3 no hold or tmp names left"                      bash -c "! find '$C/bankT' -name '*.dedup_*' | grep -q ."

echo "== X4 a file lands in a duplicate tree while it is swapped"
cat > "$WRAP/mv" <<'EOS'
#!/bin/bash
last=${!#}
case "$last" in *.dedup_old.*) n=$#; src=${@:$((n-1)):1}; printf 'UNIQUE-TREE-LATE' > "$src/late.bin";; esac
exec /bin/mv "$@"
EOS
chmod +x "$WRAP/mv"
GROUP_IDS=X4 XPATH="$WRAP:" run_apply; rm -f "$WRAP/mv"
check "X4 refused: the tree changed during the swap"      grep -q 'tree changed' "$(sumfile X4)"
check "X4 the original tree is back, with the late file"  eval '[ -d "$C/dupW" ] && [ ! -L "$C/dupW" ] && [ "$(cat "$C/dupW/late.bin")" = UNIQUE-TREE-LATE ]'
check "X4 no leftover .dedup_old tree"                    bash -c "! ls -d '$C'/dupW.dedup_old.* >/dev/null 2>&1"

echo "== X5 a Ceph-native canonical rewritten in place before the swap"
cat > "$WRAP/ln" <<EOS
#!/bin/bash
last=\${!#}
case "\$last" in *.dedup_tmp.*) ( printf 'native-9999' > "$RS/data/native/c.bin" ) 2>/dev/null;; esac
exec /bin/ln "\$@"
EOS
chmod +x "$WRAP/ln"
GROUP_IDS=X5a XPATH="$WRAP:" run_apply; rm -f "$WRAP/ln"
check "X5a the Ceph-native canonical was made read-only"  [ ! -w "$RS/data/native/c.bin" ]
check "X5a its bytes survived the writer"                 [ "$(cat "$RS/data/native/c.bin")" = native-0001 ]
check "X5a the duplicate links to the intact canonical"   eval '[ -L "$C/dupN/c.bin" ] && [ "$(cat "$C/dupN/c.bin")" = native-0001 ]'
cat > "$WRAP/ln" <<EOS
#!/bin/bash
last=\${!#}
case "\$last" in *.dedup_tmp.*) chmod u+w "$RS/data/native2/c.bin"; printf 'native-9999' > "$RS/data/native2/c.bin";; esac
exec /bin/ln "\$@"
EOS
chmod +x "$WRAP/ln"
GROUP_IDS=X5b XPATH="$WRAP:" run_apply; rm -f "$WRAP/ln"
check "X5b refused: the canonical changed while it was hashed" grep -q 'canonical changed while it was hashed' "$(sumfile X5b)"
check "X5b the duplicate keeps the original bytes"        eval '[ ! -L "$C/dupN2/c.bin" ] && [ "$(cat "$C/dupN2/c.bin")" = native-0002 ]'

echo "== X6 batch re-run after its cut-over (ALREADY_SYMLINK)"
GROUP_IDS=X6 run_apply
check "X6 apply allowed and linked"                       [ -L "$C3/dup" ]

echo "== X7 the ledger cannot be written"
mkdir -p "$D/applied/X7.ledger.tsv"
GROUP_IDS=X7 run_apply
check "X7 refused before any write"                       [ "$(state X7)" = refused ]
check "X7 the duplicate is still a regular file"          eval '[ -f "$C/dupL/l.bin" ] && [ ! -L "$C/dupL/l.bin" ]'
check "X7 the canonical was not chmodded"                 [ -w "$C/canL/l.bin" ]
rmdir "$D/applied/X7.ledger.tsv"

echo "== X8 a hard-linked duplicate"
GROUP_IDS=X8 run_apply
check "X8 refused (hard links)"                           grep -q 'hard links' "$(sumfile X8)"
check "X8 both names still one inode"                     [ "$(stat -c %i "$C/dupHL/h.bin")" = "$(stat -c %i "$C/other/h_hardlink.bin")" ]

echo "== X9 rollback restores the recorded mtime"
mt9=$(stat -c %y "$C/dupM/m.bin")
GROUP_IDS=X9 run_apply
check "X9 linked"                                         [ -L "$C/dupM/m.bin" ]
GROUP_IDS=X9 ROLLBACK=1 run_apply
check "X9 mtime after rollback equals the original ($mt9)" [ "$(stat -c %y "$C/dupM/m.bin")" = "$mt9" ]

echo "== X10 rollback refuses a tree root that links elsewhere"
GROUP_IDS=X10 run_apply
check "X10 tree linked"                                   eval '[ -L "$C/dupQ" ] && [ "$(readlink "$C/dupQ")" = "$C/canQ" ]'
rm "$C/dupQ"; ln -s "$C/canQ2" "$C/dupQ"
GROUP_IDS=X10 ROLLBACK=1 run_apply
check "X10 rollback partial, not rolled_back"             [ "$(state X10)" = rollback_partial ]
check "X10 the foreign link is left alone"                [ "$(readlink "$C/dupQ")" = "$C/canQ2" ]
rm "$C/dupQ"; ln -s "$C/canQ" "$C/dupQ"; GROUP_IDS=X10 ROLLBACK=1 run_apply

echo "== X11 a canonical shared by two groups; dedup_guard.sh"
GROUP_IDS="X11a X11b" run_apply
check "X11 both duplicates linked"                        eval '[ -L "$C/dupS1/s.bin" ] && [ -L "$C/dupS2/s.bin" ]'
(cd "$D" && bash dedup_guard.sh "$C/canS") > "$T/guard.log" 2>&1; g1=$?
check "X11 guard refuses deleting the canonical folder"   eval '[ "$g1" = 1 ] && grep -q "LIVE $C/dupS1/s.bin" "$T/guard.log"'
(cd "$D" && bash dedup_guard.sh "$HM/t/canS") > /dev/null 2>&1; g1h=$?
check "X11 guard refuses it by its HOME spelling too"     [ "$g1h" = 1 ]
GROUP_IDS=X11a ROLLBACK=1 run_apply
check "X11 after one rollback the canonical stays read-only" [ ! -w "$C/canS/s.bin" ]
GROUP_IDS=X11b ROLLBACK=1 run_apply
check "X11 after the last rollback it is writable again"  [ -w "$C/canS/s.bin" ]
(cd "$D" && bash dedup_guard.sh "$C/canS") > /dev/null 2>&1; g2=$?
check "X11 guard allows the deletion once nothing links"  [ "$g2" = 0 ]

echo "== X12 no link chain across groups"
GROUP_IDS=X12b run_apply
check "X12 chainB/x (canonical of X12a) is never replaced" eval '[ -f "$C/chainB/x" ] && [ ! -L "$C/chainB/x" ]'
GROUP_IDS=X12a run_apply
check "X12 chainA/x links to the plain file chainB/x"     eval '[ -L "$C/chainA/x" ] && [ ! -L "$C/chainB/x" ]'

echo "== X16 a stale lock"
mkdir -p "$D/applied/.lock.T02"; printf '999' > "$D/applied/.lock.T02/job"
GROUP_IDS=T02 run_apply
check "X16 squeue prints nothing, no sacct: lock kept"    grep -q 'another dedup_apply holds' "$T/last_apply.log"
printf 'slurm_load_jobs error: Invalid job id specified\n' > "$T/sq_j_999.err"
GROUP_IDS=T02 run_apply
check "X16 squeue says invalid job id: lock taken over"   grep -q 'took over the lock of finished job 999' "$T/last_apply.log"
rm -f "$T/sq_j_999.err"
mkdir -p "$D/applied/.lock.T02"; printf '998' > "$D/applied/.lock.T02/job"
printf '#!/bin/bash\nfor a; do [ "$p" = -j ] && { [ -f "%s/sacct_$a" ] && cat "%s/sacct_$a"; exit 0; }; p=$a; done\n' "$T" "$T" > "$BIN/sacct"; chmod +x "$BIN/sacct"
printf 'RUNNING\n' > "$T/sacct_998"
GROUP_IDS=T02 run_apply
check "X16 sacct says RUNNING: lock kept"                 grep -q 'another dedup_apply holds' "$T/last_apply.log"
printf 'CANCELLED by 123\n' > "$T/sacct_998"
GROUP_IDS=T02 run_apply
check "X16 sacct says CANCELLED: lock taken over"         grep -q 'took over the lock of finished job 998' "$T/last_apply.log"
rm -f "$BIN/sacct"

echo "== X17 artefacts of a killed apply"
GROUP_IDS=X17 run_apply
check "X17 refused while a .dedup_hold name exists"       grep -q 'interrupted apply left' "$(sumfile X17)"
GROUP_IDS=X17 ROLLBACK=1 run_apply
check "X17 rollback resolves the hold name"               eval '[ ! -e "$C/dupV/v.bin.dedup_hold.123" ] && [ -f "$C/dupV/v.bin" ] && [ "$(cat "$C/dupV/v.bin")" = vvvv ]'
GROUP_IDS=X17 run_apply
check "X17 then the apply links"                          [ -L "$C/dupV/v.bin" ]

echo "== X18 TERM finishes the swap in flight and stops"
cat > "$WRAP/sha256sum" <<'EOS'
#!/bin/bash
sleep 1
exec /usr/bin/sha256sum "$@"
EOS
chmod +x "$WRAP/sha256sum"
( cd "$D" && HOME=$HM SLURM_JOB_ID=aterm GROUP_IDS=X18 PATH="$WRAP:$PATH" exec bash "$D/dedup_apply.sbatch" ) > "$T/term.log" 2>&1 &
apid=$!
# TERM once the first file is in flight (its hold name exists; the slowed sha256sum keeps it there for two seconds)
for _ in $(seq 1 600); do compgen -G "$C/dupZ/*.dedup_hold.*" >/dev/null && break; sleep 0.1; done
kill -TERM "$apid" 2>/dev/null; wait "$apid"
rm -f "$WRAP/sha256sum"
nl=0; for i in 1 2 3; do [ -L "$C/dupZ/z$i.bin" ] && nl=$((nl + 1)); done
check "X18 state stopped"                                 [ "$(state X18 "$T/term.log")" = stopped ]
check "X18 the file in flight linked, the next ones not ($nl of 3 linked)" [ "$nl" = 1 ]
check "X18 no hold or tmp names left"                     bash -c "! find '$C/dupZ' -name '*.dedup_*' | grep -q ."

echo
echo "passed $PASS, failed $FAIL   (tree: $T$([ "${KEEP:-0}" = 1 ] || echo ', removed'))"
[ "$FAIL" -eq 0 ]
