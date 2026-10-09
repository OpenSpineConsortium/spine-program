#!/bin/bash
# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/slurm/env.sh [untracked at 097933a (laptop copy of 2026-10-08)]
# Sourced by every launcher: the pinned environment, the fixed locations, single-threaded numerics (bit-stable
# results), and temporary files under /dev/shm (never /tmp, which is swept on the grid).
export FV_ENV=${FV_ENV:-/rs/rs_grp_oschome/go2432/envs/fluoroclip}
export FV_ROOT=${FV_ROOT:-/rs/rs_grp_oschome/go2432/data/external/fluoro_video}
export FV_WORK=${FV_WORK:-$FV_ROOT/work}
export FV_OUT=${FV_OUT:-$FV_ROOT/clips}
export FV_CODE=${FV_CODE:-$FV_WORK/code}
export PATH=$FV_ENV/bin:$PATH
export PY=$FV_ENV/bin/python
export OMP_THREAD_LIMIT=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export MPLBACKEND=Agg PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
export TMPDIR=/dev/shm/$USER/fv_${SLURM_JOB_ID:-$$}_${SLURM_ARRAY_TASK_ID:-0}
mkdir -p "$TMPDIR"
trap 'rm -rf "$TMPDIR"' EXIT
cd "$FV_CODE" || exit 2
echo "host $(hostname) job ${SLURM_JOB_ID:-} task ${SLURM_ARRAY_TASK_ID:-} code $FV_CODE env $FV_ENV"
