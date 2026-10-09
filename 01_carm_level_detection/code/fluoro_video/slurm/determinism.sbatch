#!/bin/bash
# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/slurm/determinism.sbatch [untracked at 097933a (laptop copy of 2026-10-08)]
#SBATCH -J fvdet
#SBATCH -p reqp
#SBATCH --qos=requeue
#SBATCH -c 8
#SBATCH --mem=32G
#SBATCH -t 04:00:00
#SBATCH -o logs/fvdet_%j.out
# The pipeline twice, in one job (one node), on real videos: auto:4 = the shortest included videos of >= 20 s,
# taking the sources (commons, pmc, youtube) in turn. Compares every clip digest and manifest (timestamps, host, wall time excluded).
source /rs/rs_grp_oschome/go2432/data/external/fluoro_video/work/code/tools/fluoro_video/slurm/env.sh
rm -rf "$FV_WORK/determinism" "$FV_WORK"/det_run1 "$FV_WORK"/det_run2
$PY -m tools.fluoro_video.cli determinism --work "$FV_WORK" --out "$FV_WORK/determinism" --videos "${FV_DET_VIDEOS:-auto:4}"
