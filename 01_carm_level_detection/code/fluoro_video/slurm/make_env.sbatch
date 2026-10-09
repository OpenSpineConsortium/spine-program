#!/bin/bash
# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/slurm/make_env.sbatch [untracked at 097933a (laptop copy of 2026-10-08)]
#SBATCH -J fvenv
#SBATCH -p reqp
#SBATCH --qos=requeue
#SBATCH -c 4
#SBATCH --mem=16G
#SBATCH -t 02:00:00
#SBATCH -o logs/fvenv_%j.out
# Re-creates the pinned environment from the exact lock (every package, URL and md5).
# sbatch -D $FV_WORK $FV_CODE/tools/fluoro_video/slurm/make_env.sbatch
set -euo pipefail
ENV=${FV_ENV:-/rs/rs_grp_oschome/go2432/envs/fluoroclip}
CODE=${FV_CODE:-/rs/rs_grp_oschome/go2432/data/external/fluoro_video/work/code}
export CONDA_PKGS_DIRS=/rs/rs_grp_oschome/go2432/tmp/conda_pkgs TMPDIR=/dev/shm/$USER/fvenv
mkdir -p "$CONDA_PKGS_DIRS" "$TMPDIR"
rm -rf "$ENV"
~/mambaforge/bin/conda create -y -p "$ENV" --file "$CODE/tools/fluoro_video/explicit_lock.txt"
"$ENV/bin/python" -c "import numpy, scipy, PIL, yaml, matplotlib, av; print('ok', av.__version__)"
"$ENV/bin/ffmpeg" -hide_banner -version | head -1
"$ENV/bin/tesseract" --version | head -1
