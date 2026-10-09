#!/usr/bin/env bash
#SBATCH --job-name=augmentation_qc
#SBATCH -q primary
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=logs/augmentation_qc_%j.out
#SBATCH --error=logs/augmentation_qc_%j.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=gregory.schwing@med.wayne.edu

set -euo pipefail

# FIX 3: $(pwd) is evaluated at job-runtime, not submission time. SLURM sets
# SLURM_SUBMIT_DIR to the directory sbatch was invoked from, which is the
# reliable anchor here.  Fall back to HOME/SpineSurg-CT for interactive runs.
PROJECT_ROOT="${SLURM_SUBMIT_DIR:-${HOME}/SpineSurg-CT}"

DATA_DIR="${PROJECT_ROOT}/data"
OUTPUT_DIR="${DATA_DIR}/augmentation"

# FIX 3 (cont.): SIF_PATH default was a bare relative path; anchor it.
SIF_PATH="${SIF_PATH:-${PROJECT_ROOT}/containers/spinesurg-ct.sif}"

SPLITS_PATH="${DATA_DIR}/splits.json"
N_EXAMPLES="${N_EXAMPLES:-1}"
TRANSFORM="${TRANSFORM:-Affine}"

# Path to the sacral registration cache produced by the training job.
# When this directory exists, the QC job reuses the pre-computed deformation
# fields instead of recomputing them (~45 min saved).
# Override at submission time:
#   SACRALIZATION_REGISTRATION_CACHE_DIR=/path/to/cache sbatch slurm/run_augmentation_qc.sh
SACRALIZATION_REGISTRATION_CACHE_DIR="${SACRALIZATION_REGISTRATION_CACHE_DIR:-${PROJECT_ROOT}/checkpoints/sacral_registration_cache}"

mkdir -p logs "${OUTPUT_DIR}"

echo "======================================================"
echo " SpineSurg-CT Augmentation QC"
echo " SLURM Job ID  : ${SLURM_JOB_ID:-interactive}"
echo " Project root  : ${PROJECT_ROOT}"
echo " Output dir    : ${OUTPUT_DIR}"
echo " N examples    : ${N_EXAMPLES}"
echo " Transform     : ${TRANSFORM}"
echo " Sacral reg cache: ${SACRALIZATION_REGISTRATION_CACHE_DIR}"
if [[ -d "${SACRALIZATION_REGISTRATION_CACHE_DIR}" ]]; then
    echo " Cache status  : FOUND — will reuse training registrations"
else
    echo " Cache status  : NOT FOUND — will recompute registrations"
fi
echo " Started       : $(date)"
echo "======================================================"

# =============================================================================
# Singularity environment
# =============================================================================
export SINGULARITY_TMPDIR="/tmp/${USER}_job_${SLURM_JOB_ID}"
export XDG_RUNTIME_DIR="$SINGULARITY_TMPDIR/runtime"
export NXF_SINGULARITY_CACHEDIR="${HOME}/singularity_cache"
mkdir -p "$SINGULARITY_TMPDIR" "$XDG_RUNTIME_DIR" "$NXF_SINGULARITY_CACHEDIR"
trap 'rm -rf "$SINGULARITY_TMPDIR"' EXIT
export CONDA_PREFIX="${HOME}/mambaforge/envs/nextflow"
export PATH="${CONDA_PREFIX}/bin:${PATH}"
unset JAVA_HOME
which singularity
export NXF_SINGULARITY_HOME_MOUNT=true
unset LD_LIBRARY_PATH PYTHONPATH R_LIBS R_LIBS_USER R_LIBS_SITE

# FIX 4: OUTPUT_DIR is a subdirectory of DATA_DIR, so it's already covered by
# the DATA_DIR bind — listing it separately created a redundant mount entry.
# Build bind list without the duplicate.
BINDS="${DATA_DIR}:${DATA_DIR},${PROJECT_ROOT}:/opt/spinesurg-ct"
if [[ -d "${SACRALIZATION_REGISTRATION_CACHE_DIR}" ]]; then
    BINDS="${BINDS},${SACRALIZATION_REGISTRATION_CACHE_DIR}:${SACRALIZATION_REGISTRATION_CACHE_DIR}"
fi

singularity exec \
    --env PYTHONPATH="/opt/spinesurg-ct" \
    --bind "${BINDS}" \
    "${SIF_PATH}" \
    bash -c "cd /opt/spinesurg-ct && python -m src.utils.augmentation_qc \
        --raw_dir              ${DATA_DIR} \
        --splits               ${SPLITS_PATH} \
        --output_dir           ${OUTPUT_DIR} \
        --n_examples           ${N_EXAMPLES} \
        --transform            ${TRANSFORM} \
        --sacralization_registration_cache_dir   ${SACRALIZATION_REGISTRATION_CACHE_DIR}"

echo ""
echo "QC complete at $(date)."
echo "Visuals → ${OUTPUT_DIR}/visuals/"
echo "Metrics → ${OUTPUT_DIR}/metrics/augmentation_quality_summary.txt"
