#!/bin/bash
#SBATCH --job-name=zs9kfield
#SBATCH --partition=gmsap,gvohp,galhp
#SBATCH --qos=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=/wsu/home/go/go24/go2432/logs/zs9kfield_%A_%a.out
# EVAL_LEAKS U1 closure, the zero-shot k-in-field ladder: the lineage-complete allspine_v9 encoder with its recurrent head
# (no C-ArmLSpine frame in training; head_allspine_v9_mixed_kmax4_seed0), on the k = 1..5-vertebra crops of every case
# fold (array task = fold), on both truths: the pre-repair mirror (the replacement) and the repaired export. No training.
# Whole-frame zero-shot on the same folds was scored by slurm/carmlspine_cv_v9init.sh (kfull); this fills the
# "three and one in field, zero-shot" cell of Table 4 and Results, which existed only for the UNRESOLVED zeroshot2 run.
# Every run goes through tools/eval_gate.py inside level_prototype.py (no declaration); a refusal is recorded, not hidden.
#   sbatch -D ~/logs --array=0-4 SchwingNet/results/eval_gate/closure/cv_v9/zs_v9_kfield.sh
set -u
export PYTHONNOUSERSITE=1
export TMPDIR=/dev/shm/go2432_zs9kfield_${SLURM_JOB_ID:-local}_${SLURM_ARRAY_TASK_ID:-0}
mkdir -p "$TMPDIR"; trap 'rm -rf "$TMPDIR"' EXIT
cd "$HOME/spinesurg-ct-nnunet"
PY=$HOME/mambaforge/envs/fluorogen/bin/python
K=${SLURM_ARRAY_TASK_ID:-0}
RX=/rs/rs_grp_oschome/go2432/data/realxray
CP=/rs/rs_grp_oschome/go2432/data/carmlspine
INIT=$HOME/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt
V9HEAD=$HOME/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt
for f in "$INIT" "$V9HEAD"; do [ -f "$f" ] || { echo "MISSING $f"; exit 2; }; done
echo "ZS9KFIELD_START fold=$K host=$(hostname) $(date)"
FAIL=0
run() {
  local tag=$1; shift
  "$@" > "$TMPDIR/run.log" 2>&1; local rc=$?
  grep -viE "warn|deprecat" "$TMPDIR/run.log" | grep -E "^done:|exact" | tail -2
  grep -E "eval_gate: .*(HELD OUT|DECLARED)" "$TMPDIR/run.log" | grep -E "model_rung|head" | tail -2 | cut -c1-200
  if [ $rc -ne 0 ]; then echo "RUN_FAILED rc=$rc [$tag]"; grep -E "Error|eval_gate" "$TMPDIR/run.log" | tail -6; FAIL=1; fi
  return $rc
}
for TR in pre rep; do
  if [ $TR = pre ]; then CV=$RX/carmlspine_cv_prerepair/fold$K; ZS=$CP/proto_v9init_prerepair/zs_fold$K
  else CV=$RX/carmlspine_cv/fold$K; ZS=$CP/proto_v9init/zs_fold$K; fi
  for k in 1 2 3 4 5; do
    [ -d "$CV/k$k/images" ] || { echo "MISSING $CV/k$k"; FAIL=1; continue; }
    run "zs v9head $TR fold$K k$k" $PY -u tools/level_prototype.py --image $CV/k$k/images --out $ZS/v9head/det/k$k --no-orient --model "$INIT" --head "$V9HEAD" \
      && run "zs v9head score $TR fold$K k$k" $PY -u tools/carmlspine_eval.py score --pred $ZS/v9head/det/k$k --meta $CV/k$k/meta --out $ZS/v9head/det_score_k$k.json --tag "zs v9head $TR fold$K det k=$k"
  done
done
echo "ZS9KFIELD_DONE fold=$K fail=$FAIL $(date)"
exit $FAIL
