#!/bin/bash
#SBATCH --job-name=v8_close
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G
#SBATCH --time=03:00:00
#SBATCH --output=v8_close_%j.out
#SBATCH --error=v8_close_%j.out
# Closure item 2: why allspine_v8 holds 192 persons in both train and val (by today's patient key), read from the
# bank's case/split arrays and the key file it was built with; plus the v8/v9 exposure the G3 split plan quotes.
set -uo pipefail
export PYTHONNOUSERSITE=1
export TMPDIR=/dev/shm/go2432_v8c_${SLURM_JOB_ID:-x}; mkdir -p "$TMPDIR"
trap 'rm -rf "$TMPDIR"' EXIT
H=/wsu/home/go/go24/go2432
cd "$H/spinesurg-ct-nnunet"
PY=$H/mambaforge/envs/spineps/bin/python
O=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure/v8_overlap
mkdir -p "$O"
echo "V8_CLOSE_START $(date) on $(hostname)"
md5sum tools/eval_gate.py tools/patient_keys.py "$H/patient_keys.json" "$H/patient_keys_v9.json" "$H/split_final.json"
"$PY" -u SchwingNet/results/eval_gate/closure/v8_overlap_cause.py \
    --bank "$H/allspine_v8_fov96_ctx" --keys "$H/patient_keys.json" \
    --also-bank "v9=$H/allspine_v9_fov96_ctx=$H/patient_keys_v9.json" \
    --stratify "$O/stratify.json" --split-final "$H/split_final.json" \
    --out "$O/v8_overlap.json"
rc=$?
echo "V8_CLOSE_RC=$rc $(date)"
exit $rc
