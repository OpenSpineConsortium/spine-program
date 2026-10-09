#!/bin/bash
# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/slurm/inventory.sbatch [untracked at 097933a (laptop copy of 2026-10-08)]
#SBATCH -J fvinv
#SBATCH -p reqp
#SBATCH --qos=requeue
#SBATCH -c 2
#SBATCH --mem=8G
#SBATCH -t 01:00:00
#SBATCH -o logs/fvinv_%j.out
# Inputs by rule, input sha256, ffprobe, and the source texts (fetched once, cached in work/source_text).
source /rs/rs_grp_oschome/go2432/data/external/fluoro_video/work/code/tools/fluoro_video/slurm/env.sh
$PY -m tools.fluoro_video.cli inventory --work "$FV_WORK"
