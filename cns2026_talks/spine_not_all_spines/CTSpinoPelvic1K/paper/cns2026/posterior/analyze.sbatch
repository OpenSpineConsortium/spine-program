#!/bin/bash
# Posterior figure, step 3: reproduction checks and posterior histograms over whatever predictions exist.
#   sbatch --export=ALL,OUT=analysis_all analyze.sbatch
#SBATCH --job-name=post_anal
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --time=06:00:00
#SBATCH --output=/rs/rs_grp_oschome/go2432/cns2026_posterior/logs/analyze_%j.out
set -euo pipefail
W=/rs/rs_grp_oschome/go2432/cns2026_posterior
RAW=$HOME/spinesurg-ct-nnunet/nnunet/raw/Dataset803_SpineSurgCTFullMerged
OUT=${OUT:-analysis}
unset PYTHONPATH
"$HOME/mambaforge/envs/spineps/bin/python" -u "$W/src/analyze.py" --pred "$W/pred" --labels "$RAW/labelsTs" \
  --images "$RAW/imagesTs" --ctdir "$W/hf_export/ct" --lstv "$RAW/lstv_cases.json" --out "$W/$OUT" --workers 6
ls -la "$W/$OUT"
