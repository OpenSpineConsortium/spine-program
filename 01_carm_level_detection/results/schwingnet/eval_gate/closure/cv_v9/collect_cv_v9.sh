#!/bin/bash
#SBATCH --job-name=cv9icollect
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=/wsu/home/go/go24/go2432/logs/cv9icollect_%j.out
# CPU stage after slurm/carmlspine_cv_v9init.sh, slurm/carmlspine_cv_day_v9init.sh (training + the repaired-truth
# evaluation) and slurm/carmlspine_cv_v9init_prerepair.sh (the shipped-truth evaluation). For each truth -- pre (the
# pre-repair export, on which every quoted number was scored) and rep (the export as it stands today):
#  (1) the four coupler passes of SchwingNet/slurm/coupling_eval.sh over that truth's coupling prototypes;
#  (2) SchwingNet/tools/coupling_report.py over them (coupling.json + COUPLING.md, written under coupling_<truth>/);
#  (3) tools/rigor_fixes.py a4 / a7 / a9 over the re-run (drop-in twins of results/a4.json, a7.json, a9.json, written
#      under rigor_<truth>/);
# then (4) closure_cv_v9.py: every quoted row, shipped beside both re-runs, one code path, the gate on every new input.
#   sbatch -D ~/logs --dependency=afterany:<arrays> SchwingNet/results/eval_gate/closure/cv_v9/collect_cv_v9.sh
set -u
export PYTHONNOUSERSITE=1
export TMPDIR=/dev/shm/go2432_cv9icollect_${SLURM_JOB_ID:-local}; mkdir -p "$TMPDIR"; trap 'rm -rf "$TMPDIR"' EXIT
cd "$HOME/spinesurg-ct-nnunet"
PY=$HOME/mambaforge/envs/fluorogen/bin/python
CP=/rs/rs_grp_oschome/go2432/data/carmlspine
RX=/rs/rs_grp_oschome/go2432/data/realxray
D=$HOME/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9
VARIANT="case42=L6,case121=L6,case136=L6"
echo "CV9I_COLLECT_START $(date) host=$(hostname) jobs=${JOBS:-}"
$PY tools/alphabet_couple.py --self-test > "$TMPDIR/st.log" 2>&1 || { echo "SELF_TEST_FAILED"; tail -5 "$TMPDIR/st.log"; exit 1; }
for TR in pre rep; do
  if [ $TR = pre ]; then ROOT=$CP/proto_post_v9init_prerepair; NEW=$CP/proto_v9init_prerepair; CVR=$RX/carmlspine_cv_prerepair
  else ROOT=$CP/proto_post_v9init; NEW=$CP/proto_v9init; CVR=$RX/carmlspine_cv; fi
  for K in 0 1 2 3 4; do for b in det oracle; do for k in full 5; do
    P=$ROOT/cv_fold$K/$b/k$k; M=$CVR/fold$K/k$k/meta
    [ -f $P/prototype_meta.json ] || { echo "MISSING $P (fold $K not run?)"; continue; }
    SM=""; [ $b = oracle ] && SM="--sacrum-from-meta"
    $PY tools/alphabet_couple.py --pred $P --meta $M --out $P/couple     --truth-variant "$VARIANT" $SM | tail -1
    $PY tools/alphabet_couple.py --pred $P --meta $M --out $P/couple_ns  --truth-variant "$VARIANT" $SM --exclude-named-sacrum | tail -1
    $PY tools/alphabet_couple.py --pred $P --meta $M --out $P/couple_ext --truth-variant "$VARIANT" $SM --alphabets ext | tail -1
    if [ $b = det ]; then
      $PY tools/alphabet_couple.py --pred $P --meta $M --out $P/couple_c74 --truth-variant "$VARIANT" --sacrum-min-conf 0.74 | tail -1
    fi
  done; done; done
  mkdir -p $D/coupling_$TR $D/rigor_$TR
  $PY SchwingNet/tools/coupling_report.py --root $ROOT --orig $NEW --sweep-calls SchwingNet/results/sweep_variant_calls.json \
      --out $D/coupling_$TR --jobs "${JOBS:-}" 2>&1 | tail -3
  echo "COUPLING_REPORT_$TR done"
  for it in a4 a7 a9; do
    $PY tools/rigor_fixes.py $it --inputs $NEW --results $D/rigor_$TR 2>&1 | tail -2
  done
done
$PY SchwingNet/results/eval_gate/closure/cv_v9/closure_cv_v9.py --out $D/cv_v9.json \
    --coupling-pre $D/coupling_pre/coupling.json --coupling-rep $D/coupling_rep/coupling.json 2>&1 | tail -40
echo "CV9I_COLLECT_DONE $(date)"
