#!/bin/bash
# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/anomaly_rules_array.sh; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
# anomaly_rules_array.sh -- Slurm array for tools/transitional_review/anomaly_rules.py over one tier list.
#
# PURPOSE   Score every CT of a tier list with the PREREG_rules.md screen (rule 1 count, rule 3 stump, rule 2 / 1b / 4
#           features, comparators), one JSON + one row per CT, resumable. CPU only, 2 cores, 8 G (masks are read on the
#           SPINEPS grid; the CT is opened for its header only).
# INPUTS    LIST      a tier list (RS/ruleclass/tiers/tier1.tsv | tier2.tsv | untiered.tsv; columns in TIERS.md section 3)
#           OUT_ROOT  output tree (default RS/ruleclass/rules/<list stem>)
#           CODE      the checked-out tools/transitional_review directory on the grid (default
#                     $HOME/spinesurg-ct-nnunet/tools/transitional_review; pull/rsync it first, the array does not)
#           EXTRA     extra anomaly_rules.py arguments (e.g. --limit 50, --reverse, --retry-failed, --force)
# OUTPUTS   $OUT_ROOT/<coll>/<case>.rules.json, <case>.row.tsv, _failed/, _claims/ (atomic mkdir per case exactly like
#           RS/ruleclass/code/ts_arm_run.py: a claim untouched for 2 h is taken over; a live task touches its claim every
#           5 min; a case marked failed is retaken only with --retry-failed); logs in RS/ruleclass/logs.
# RUN       (NOT submitted by the tool that wrote this; submit from the login node when the list is final)
#   RC=/rs/rs_grp_oschome/go2432/ruleclass
#   sbatch -D $RC/rules --array=0-63 --export=ALL,LIST=$RC/tiers/tier1.tsv $HOME/spinesurg-ct-nnunet/tools/transitional_review/anomaly_rules_array.sh
#   afterwards:  $PY anomaly_rules.py collect --out $RC/rules/tier1
#   Every task walks the SAME list, so any array size works and a re-submission resumes (cases with a rules.json are skipped).
#   Chain later steps with afterany, never afterok (CLAUDE.md: a trivial non-zero exit strands an afterok chain).
#SBATCH --job-name=tr_rules
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=1-00:00:00
#SBATCH --output=/rs/rs_grp_oschome/go2432/ruleclass/logs/%x_%A_%a.out
set -uo pipefail
RC=/rs/rs_grp_oschome/go2432/ruleclass
LIST=${LIST:?set LIST to a tier list (tier1.tsv / tier2.tsv / untiered.tsv)}
STEM=$(basename "$LIST" .tsv)
OUT_ROOT=${OUT_ROOT:-$RC/rules/$STEM}
CODE=${CODE:-$HOME/spinesurg-ct-nnunet/tools/transitional_review}
PY=${PY:-$HOME/mambaforge/envs/spineps/bin/python}          # nibabel 5.4, scipy 1.15, numpy 2.2, pandas 2.3
# ostk (labels_for) and tools/spineps_ids.py are imported from the checkouts, never from a copied map
export PYTHONPATH=$HOME/OpenSpineToolkit:$HOME/spinesurg-ct-nnunet/tools:$HOME/spinesurg-ct-nnunet${PYTHONPATH:+:$PYTHONPATH}
export PYTHONNOUSERSITE=1 OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-2} MKL_NUM_THREADS=${SLURM_CPUS_PER_TASK:-2} OPENBLAS_NUM_THREADS=${SLURM_CPUS_PER_TASK:-2}
W=/dev/shm/${USER}_tr_rules_${SLURM_JOB_ID:-x}_${SLURM_ARRAY_TASK_ID:-0}      # /tmp is node-local and swept
mkdir -p "$W" "$OUT_ROOT" "$RC/logs"
export TMPDIR=$W
trap 'rm -rf "$W"' EXIT
echo "TR_RULES_START job=${SLURM_ARRAY_JOB_ID:-${SLURM_JOB_ID:-}} task=${SLURM_ARRAY_TASK_ID:-} host=$(hostname) $(date) list=$LIST out=$OUT_ROOT code=$CODE"
"$PY" -c "from ostk.labels import labels_for; import spineps_ids, nibabel, scipy; print('imports ok')" || { echo "TR_RULES_ABORT: imports failed (PYTHONPATH=$PYTHONPATH)"; exit 3; }
"$PY" -u "$CODE/anomaly_rules.py" run --list "$LIST" --out "$OUT_ROOT" --claim --stale-h 2 \
    --moller-root "$RC/arms/moller_fast" --ts-root "$RC/arms/ts" --pelvis-root "$RC/arms/pelvis" ${EXTRA:-}
rc=$?
echo "TR_RULES_EXIT rc=$rc $(date)"
exit $rc
