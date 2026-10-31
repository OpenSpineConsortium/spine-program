#!/bin/bash
#SBATCH --cpus-per-task=32
#SBATCH --mem=192G
#SBATCH --time=08:00:00
set -uo pipefail
W=/rs/rs_grp_oschome/go2432/cns-profile/cal
cd "$W"
PY=$HOME/mambaforge/envs/spineps/bin/python
[ -s full.tsv ] || "$PY" full_list.py full.tsv
wc -l full.tsv
export PYTHONPATH=$W/engine PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 CAL_LEAN=1
"$PY" cal.py run --list full.tsv --out runs/full/out --workers "${SLURM_CPUS_PER_TASK:-32}"
ls runs/full/out | grep -c '\.err$' || true
