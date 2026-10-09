#!/bin/bash
#SBATCH --job-name=dp_index
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --requeue
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=2-00:00:00
#SBATCH --output=logs/%x_%j.out
# Build or refresh the SQLite index of the CephFS layout (build_index.py). Incremental: unchanged files are not re-read,
# so a requeue or a rerun is cheap. Writes $DB (default /rs/rs_grp_oschome/go2432/data/_index/holding.sqlite).
#   cd ~/spinesurg-ct-nnunet/data_platform/db && mkdir -p logs     # Slurm opens --output before this script runs
#   sbatch -D "$PWD" build_index.sbatch                                   # every folder with a README.yaml
#   sbatch -D "$PWD" --export=ALL,FOLDERS="ctspinopelvic1k vindr_spinexr" build_index.sbatch
#   sbatch -D "$PWD" --export=ALL,HASH=small build_index.sbatch            # also sha256 of files under 64 MB
set -uo pipefail
mkdir -p logs
ROOT=${ROOT:-/rs/rs_grp_oschome/go2432/data}
DB=${DB:-$ROOT/_index/holding.sqlite}
HASH=${HASH:-none}
FOLDERS=${FOLDERS:-}
# a Python with sqlite3 >= 3.8 and, when present, pydicom (DICOM headers); the spineps env has both
PY=${PY:-$HOME/mambaforge/envs/spineps/bin/python}
[ -x "$PY" ] || PY=python3
export PYTHONNOUSERSITE=1
echo "DP_INDEX start $(date '+%F %T') on $(hostname) root=$ROOT db=$DB hash=$HASH folders=${FOLDERS:-all}"
# shellcheck disable=SC2086
"$PY" "$HOME/spinesurg-ct-nnunet/data_platform/db/build_index.py" --root "$ROOT" --db "$DB" --hash "$HASH" ${FOLDERS:+--folders $FOLDERS}
rc=$?
echo "DP_INDEX_RC=$rc $(date '+%F %T')"
exit $rc
