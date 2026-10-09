#!/bin/bash
# Functional test of migrate_batch.sbatch, verify_transfer.py, cutover.sh and preflight.sbatch on a synthetic tree
# under $TMPDIR (Linux or WSL; needs rsync and python3; no network, no grid, no Slurm: SLURM_JOB_ID is faked).
# Checks: the generated B02 batch puts every item in the hard-link group; hard links survive the group copy; a rerun
# of a group after a source change refreshes it and leaves no staging behind; symlinks stay symlinks; a relative link
# that leaves its item fails verification; an existing destination not written by this item is refused; restricted
# items are owner-only and directories keep setgid; a source changed after the copy blocks the cut-over; cut-over
# leaves a symlink and a .pre-ceph copy; rollback restores; finalize refuses a .pre-ceph written after the cut-over
# and a missing Ceph copy, and deletes only after comparing. B14 (2026-10-08): the generated B14 batch closes
# ~/dis_renders and ~/s1v11 and lists nothing that stays on HOME; a single file under a new leaf name and a folder
# under a new parent folder copy, verify and cut over; a file hard-linked to a partner outside its item fails
# verification and passes with ALLOW_NLINK_LOSS=1.
#   bash data_platform/plan/test_migration.sh
set -u
SRCPLAN="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
T="${TMPDIR:-/tmp}/dptest_$$"; rm -rf "$T"; mkdir -p "$T/home" "$T/rs/data" "$T/plan/batch_items"
for f in migrate_batch.sbatch verify_transfer.py cutover.sh preflight.sbatch; do tr -d '\r' < "$SRCPLAN/$f" > "$T/plan/$f"; done
export HOME="$T/home" SLURM_JOB_ID=999 PLAN="$T/plan" STAGING="$T/rs/data/_staging/BT"
H=$HOME; D="$T/rs/data"
chmod g+s "$D"
cd "$T/plan"
fail=0; chk() { if eval "$1"; then echo "ok   $2"; else echo "FAIL $2"; fail=1; fi; }

# --- the generated B02 batch file: every item is in the hard-link group
chk '[ "$(grep -v "^#" "$SRCPLAN/batch_items/B02.tsv" | awk -F"\t" "\$4 !~ /hardlink_group/" | wc -l)" = 0 ]' "generated B02.tsv flags every item hardlink_group"
chk 'grep -q $'"'"'\thardlink_group,restricted,glob$'"'"' "$SRCPLAN/batch_items/B04.tsv"' "generated B04.tsv: the yolo* banks copy as one restricted group"

# --- synthetic HOME
mkdir -p "$H/data/CTSpinoPelvic1K/ct" "$H/CTSpinoPelvic1K/data/hf_export_osc/ct" "$H/deepfluoro/data" "$H/deepfluoro/unpacked_full"
for i in 1 2 3; do head -c $((i * 1000)) /dev/urandom > "$H/CTSpinoPelvic1K/data/hf_export_osc/ct/000${i}_ct.nii.gz"; done
for i in 1 2 3; do ln "$H/CTSpinoPelvic1K/data/hf_export_osc/ct/000${i}_ct.nii.gz" "$H/data/CTSpinoPelvic1K/ct/000${i}_ct.nii.gz"; done
echo '{"a":1}' > "$H/data/CTSpinoPelvic1K/manifest.json"
head -c 5000 /dev/urandom > "$H/deepfluoro/unpacked_full/ipcai.h5"; echo lic > "$H/deepfluoro/unpacked_full/LICENSE"
head -c 300 /dev/urandom > "$H/deepfluoro/data/x.zip"; mkdir -p "$H/deepfluoro/data/sub"; echo s > "$H/deepfluoro/data/sub/s.txt"
ln -s "$H/deepfluoro/data" "$H/deepfluoro/rel_link_abs"; ln -s ../data/x.zip "$H/deepfluoro/unpacked_full/rel_link"
mkdir -p "$H/user"; ln -s "$H/deepfluoro/data" "$H/user/diffdrr_data"
printf '# src\tdst\test_gb\tflags\n%s\t%s\t0.1\thardlink_group,irreplaceable\n%s\t%s\t0.1\thardlink_group,candidate\n' \
  "$H/data/CTSpinoPelvic1K" "$D/ctspinopelvic1k/converted/CTSpinoPelvic1K" \
  "$H/CTSpinoPelvic1K/data/hf_export_osc" "$D/ctspinopelvic1k_build_tree/derived/hf_export_osc" > "$T/plan/batch_items/BT.tsv"
printf '# src\tdst\test_gb\tflags\n%s\t%s\t0.01\t-\n%s/missing_dir\t%s/x\t\t-\n' "$H/deepfluoro" "$D/deepfluoro_h5/raw/deepfluoro" "$H" "$D" > "$T/plan/batch_items/BP.tsv"

BATCH=BP bash migrate_batch.sbatch > bp.log 2>&1; echo "migrate BP rc=$?"
BATCH=BT bash migrate_batch.sbatch > bt.log 2>&1; echo "migrate BT rc=$?"
chk '[ "$(stat -c %i "$D/ctspinopelvic1k/converted/CTSpinoPelvic1K/ct/0001_ct.nii.gz")" = "$(stat -c %i "$D/ctspinopelvic1k_build_tree/derived/hf_export_osc/ct/0001_ct.nii.gz")" ]' "hard link kept across the two B02 items"
chk '[ -L "$D/deepfluoro_h5/raw/deepfluoro/rel_link_abs" ]' "symlink copied as a symlink"
chk 'grep -q ABSENT runs/BP/STATUS' "absent item reported"
chk '[ "$(grep -c $'"'"'\tVERIFIED\t'"'"' runs/BP/STATUS)" = 1 ] && [ "$(grep -c $'"'"'\tVERIFIED\t'"'"' runs/BT/STATUS)" = 2 ]' "all present items verified"
chk '[ ! -e "$STAGING" ]' "staging removed after a clean group run"
chk '[ "$(stat -c %A "$D/deepfluoro_h5/raw/deepfluoro/data" | cut -c7)" = s ]' "copied directories keep setgid (group oschome below the item root)"

# --- P2: rerun of the group after a source file changed (new inode in one item): refreshed, verified, no leftovers
head -c 777 /dev/urandom > "$H/data/CTSpinoPelvic1K/ct/0002.new"; mv "$H/data/CTSpinoPelvic1K/ct/0002.new" "$H/data/CTSpinoPelvic1K/ct/0002_ct.nii.gz"
SLURM_JOB_ID=1000 BATCH=BT bash migrate_batch.sbatch > bt2.log 2>&1; echo "migrate BT rerun rc=$?"   # a new job, a new STATUS
chk '[ "$(grep -c $'"'"'\tVERIFIED\t'"'"' runs/BT/STATUS)" = 2 ] && [ "$(stat -c %s "$D/ctspinopelvic1k/converted/CTSpinoPelvic1K/ct/0002_ct.nii.gz")" = 777 ]' "group rerun picks up a changed source and verifies"
chk '[ ! -e "$STAGING" ]' "group rerun leaves no staging copy"

# --- a destination that exists and was not written by this item is refused
mkdir -p "$H/fluorogen/sub"; echo a > "$H/fluorogen/sub/f"; mkdir -p "$D/fluorogen_synthetic/derived/fluorogen"; echo theirs > "$D/fluorogen_synthetic/derived/fluorogen/other"
printf '# src\tdst\test_gb\tflags\n%s\t%s\t\t-\n' "$H/fluorogen" "$D/fluorogen_synthetic/derived/fluorogen" > batch_items/BX.tsv
BATCH=BX bash migrate_batch.sbatch > bx.log 2>&1
chk 'grep -q DST_EXISTS runs/BX/STATUS && [ ! -e "$D/fluorogen_synthetic/derived/fluorogen/sub" ]' "an existing destination not written by this item is refused"

# --- P3: a relative link that leaves its item fails verification; restricted items are owner-only
mkdir -p "$H/verse_drr/img" "$H/allspine_v9_fov96_ctx" "$H/vindr_det_drr/ann"; echo x > "$H/verse_drr/img/a.npy"; echo y > "$H/vindr_det_drr/ann/a.json"
ln -s ../verse_drr/img/a.npy "$H/allspine_v9_fov96_ctx/a.npy"
printf '# src\tdst\test_gb\tflags\n%s\t%s\t\t-\n%s\t%s\t\trestricted\n' "$H/allspine_v9_fov96_ctx" "$D/multisource_banks/derived/allspine_v9_fov96_ctx" \
  "$H/vindr_det_drr" "$D/vindr_spinexr/derived/vindr_det_drr" > batch_items/BY.tsv
BATCH=BY bash migrate_batch.sbatch > by.log 2>&1
chk 'grep $'"'"'\tVERIFY_FAILED\t'"'"' runs/BY/STATUS | grep -q allspine_v9' "a relative link leaving the item fails verification"
chk '[ "$(stat -c %a "$D/vindr_spinexr/derived/vindr_det_drr/ann/a.json")" = 600 ] && [ "$(stat -c %A "$D/vindr_spinexr/derived/vindr_det_drr" | cut -c5-10)" = "--S---" ]' "restricted item copied owner-only (setgid kept, no group or other access)"

# --- B14 (identified 2026-10-08): the generated batch file, and the item shapes it introduces
chk 'awk -F"\t" "\$1 ~ /\/dis_renders\$/ {print \$4}" "$SRCPLAN/batch_items/B14.tsv" | grep -q restricted' "generated B14.tsv: ~/dis_renders (BUU film names) copies owner-only"
chk 'awk -F"\t" "\$1 ~ /\/s1v11\$/ {print \$4}" "$SRCPLAN/batch_items/B14.tsv" | grep -q "restricted,irreplaceable"' "generated B14.tsv: ~/s1v11 owner-only and hashed in full at finalize"
chk '[ -z "$(awk -F"\t" "\$1 ~ /\/(github|docs|ada|output|3|6|v|Multi-View-Vertebra)\$/" "$SRCPLAN/batch_items/B14.tsv")" ]' "generated B14.tsv: nothing that stays on HOME is an item"
head -c 2000 /dev/urandom > "$H/qc.tar.gz"; mkdir -p "$H/pitest"; head -c 100 /dev/urandom > "$H/pitest/0024_label.nii.gz"
printf '# src\tdst\test_gb\tflags\n%s\t%s\t\t-\n%s\t%s\t\tcandidate\n' "$H/qc.tar.gz" "$D/ctspinopelvic1k_build_tree/derived/qc_2026-06-12.tar.gz" \
  "$H/pitest" "$D/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/pitest" > batch_items/BZ.tsv
BATCH=BZ bash migrate_batch.sbatch > bz.log 2>&1
chk '[ "$(grep -c $'"'"'\tVERIFIED\t'"'"' runs/BZ/STATUS)" = 2 ] && cmp -s "$H/qc.tar.gz" "$D/ctspinopelvic1k_build_tree/derived/qc_2026-06-12.tar.gz"' "a file under a new leaf name and a folder under a new parent folder copy and verify"
BATCH=BZ bash cutover.sh > cutbz.log 2>&1
chk '[ "$(readlink "$H/qc.tar.gz")" = "$D/ctspinopelvic1k_build_tree/derived/qc_2026-06-12.tar.gz" ] && [ -f "$H/qc.tar.gz.pre-ceph" ] && [ -L "$H/pitest" ] && [ -f "$H/pitest/0024_label.nii.gz" ]' "cut-over of a renamed file item and a nested folder item"
echo lbl > "$H/release_label.nii.gz"; mkdir -p "$H/pdwtest"; ln "$H/release_label.nii.gz" "$H/pdwtest/0010_label.nii.gz"
printf '# src\tdst\test_gb\tflags\n%s\t%s\t\tcandidate\n' "$H/pdwtest" "$D/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/pdwtest" > batch_items/BW.tsv
BATCH=BW bash migrate_batch.sbatch > bw.log 2>&1
chk 'grep -q $'"'"'\tVERIFY_FAILED\t'"'"' runs/BW/STATUS' "a file hard-linked to a partner outside its item fails verification"
SLURM_JOB_ID=1001 ALLOW_NLINK_LOSS=1 BATCH=BW bash migrate_batch.sbatch > bw2.log 2>&1
chk 'grep -q $'"'"'\tVERIFIED\t'"'"' runs/BW/STATUS' "the same item verifies with ALLOW_NLINK_LOSS=1 (after review)"

# --- cut-over, rollback, finalize
BATCH=BP DRY=1 bash migrate_batch.sbatch > bpdry.log 2>&1; chk 'grep -q DRYRUN runs/BP/STATUS' "dry run itemizes"
BATCH=BP bash migrate_batch.sbatch > bp2.log 2>&1   # re-run resumes (no-op) and refreshes STATUS
echo extra > "$H/deepfluoro/data/new_file"          # a change after the copy must block the cut-over
BATCH=BP bash cutover.sh > cut1.log 2>&1; chk 'grep -q REFUSED_CHANGED_SINCE_COPY runs/BP/CUTOVER.999' "cut-over refuses a source changed after the copy"
rm "$H/deepfluoro/data/new_file"
BATCH=BP bash cutover.sh > cut2.log 2>&1; chk '[ -L "$H/deepfluoro" ] && [ -d "$H/deepfluoro.pre-ceph" ]' "cut-over: symlink at the old path, original kept"
chk '[ -f "$H/user/diffdrr_data/x.zip" ]' "an existing symlink into the moved tree still resolves"
BATCH=BP ROLLBACK=1 bash cutover.sh > rb.log 2>&1; chk '[ -d "$H/deepfluoro" ] && [ ! -L "$H/deepfluoro" ] && [ ! -e "$H/deepfluoro.pre-ceph" ]' "rollback restores the original"
BATCH=BP bash cutover.sh > cut3.log 2>&1
echo "late result" > "$H/deepfluoro.pre-ceph/written_after_cutover.txt"      # P4: a write into .pre-ceph after the cut-over
BATCH=BP FINALIZE=1 bash cutover.sh > fin1.log 2>&1
chk '[ -f "$H/deepfluoro.pre-ceph/written_after_cutover.txt" ] && grep -q REFUSED_PRE runs/BP/CUTOVER.999' "finalize refuses a .pre-ceph that differs from the copy"
mv "$H/deepfluoro.pre-ceph/written_after_cutover.txt" "$D/deepfluoro_h5/raw/deepfluoro/"   # reconcile: the late file goes to the copy
touch -r "$H/deepfluoro.pre-ceph/LICENSE" "$D/deepfluoro_h5/raw/deepfluoro/written_after_cutover.txt" 2>/dev/null
mv "$D/deepfluoro_h5/raw/deepfluoro" "$D/deepfluoro_h5/raw/deepfluoro.away"            # the Ceph copy vanishes
BATCH=BP FINALIZE=1 bash cutover.sh > fin2.log 2>&1
chk '[ -d "$H/deepfluoro.pre-ceph" ] && grep -q REFUSED_DST_MISSING runs/BP/CUTOVER.999' "finalize refuses when the Ceph copy is missing (the .pre-ceph copy is kept)"
mv "$D/deepfluoro_h5/raw/deepfluoro.away" "$D/deepfluoro_h5/raw/deepfluoro"
BATCH=BP FINALIZE=1 bash cutover.sh > fin3.log 2>&1
chk '[ -L "$H/deepfluoro" ] && [ ! -e "$H/deepfluoro.pre-ceph" ] && [ -f "$H/deepfluoro/unpacked_full/ipcai.h5" ]' "finalize compares, then deletes the .pre-ceph copy; data reachable through the symlink"
BATCH=BT bash cutover.sh > cutbt.log 2>&1; chk '[ -L "$H/data/CTSpinoPelvic1K" ] && [ -f "$H/data/CTSpinoPelvic1K/ct/0002_ct.nii.gz" ]' "B02-style cut-over"
BATCH=BT FINALIZE=1 bash cutover.sh > finbt.log 2>&1
chk 'grep -q "FINALIZED (compared in full" runs/BT/CUTOVER.999' "an irreplaceable item is hashed in full before its .pre-ceph copy is deleted"
BATCH=BT bash preflight.sbatch > pre.log 2>&1; chk '[ -s preflight/BT.tsv ]' "preflight writes its table"
BATCH=BY bash preflight.sbatch > prey.log 2>&1; chk 'awk -F"\t" "\$2 ~ /allspine_v9/ {print \$12}" preflight/BY.tsv | grep -qx 1' "preflight counts relative links that leave an item"
unset SLURM_JOB_ID; BATCH=BP bash migrate_batch.sbatch > nojob.log 2>&1; chk 'grep -q refusing nojob.log' "refuses outside a Slurm job"
echo "RESULT fail=$fail"
if [ "${KEEP:-0}" = 1 ]; then echo "kept $T"; else rm -rf "$T"; fi
exit $fail
