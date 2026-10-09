#!/bin/bash
# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/slurm/report.sbatch [untracked at 097933a (laptop copy of 2026-10-08)]
#SBATCH -J fvrep
#SBATCH -p reqp
#SBATCH --qos=requeue
#SBATCH -c 2
#SBATCH --mem=8G
#SBATCH -t 00:30:00
#SBATCH -o logs/fvrep_%j.out
source /rs/rs_grp_oschome/go2432/data/external/fluoro_video/work/code/tools/fluoro_video/slurm/env.sh
$PY -m tools.fluoro_video.cli report --work "$FV_WORK" --out "$FV_OUT"
$PY -m tools.fluoro_video.cli export --out "$FV_OUT" --dest "$FV_WORK/qc_export"
