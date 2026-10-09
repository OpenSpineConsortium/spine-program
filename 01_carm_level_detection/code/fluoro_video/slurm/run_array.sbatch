#!/bin/bash
# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/slurm/run_array.sbatch [untracked at 097933a (laptop copy of 2026-10-08)]
#SBATCH -J fvrun
#SBATCH -p reqp
#SBATCH --qos=requeue
#SBATCH -c 4
#SBATCH --mem=16G
#SBATCH -t 16:00:00
#SBATCH -o logs/fvrun_%A_%a.out
# One video per array task, in video_id order of work/inventory.json (the included entries).
# N=$(grep -c '"include": true' $FV_WORK/inventory.json); sbatch -D $FV_WORK --array=0-$((N-1)) run_array.sbatch
# A requeued task starts its video from scratch (outputs of that video are removed first).
source /rs/rs_grp_oschome/go2432/data/external/fluoro_video/work/code/tools/fluoro_video/slurm/env.sh
$PY -m tools.fluoro_video.cli run --work "$FV_WORK" --out "$FV_OUT" --index "$SLURM_ARRAY_TASK_ID" --skip-done
