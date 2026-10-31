#!/bin/bash
#SBATCH --cpus-per-task=32
#SBATCH --mem=128G
#SBATCH --time=02:00:00
# Calibration run: the engine copy under $W/engine over the sample list; writes $W/runs/<tag>/.
set -uo pipefail
W=/rs/rs_grp_oschome/go2432/cns-profile/cal
TAG=${CAL_TAG:?}
M=/rs/rs_grp_oschome/go2432/morphometry
D=/rs/rs_grp_oschome/go2432/data
TS=$D/totalsegmentator_v300/raw/TotalSegmentator_v3/Totalsegmentator_dataset_v300
cd "$W"
if [ ! -s sample2.tsv ]; then
  for f in $(ls "$M"/enhance/masks/*.nii.gz | awk 'NR % 33 == 1' | head -48); do
    id=$(basename "$f" .nii.gz); printf '%s\tenhance\tenhance\t%s\n' "$f" "$D/aws_enhance_pet_ct/raw/$id.nii.gz"
  done > sample2.tsv
  for s in $(awk -F, '$2=="verse"{print $4}' "$M"/covariates/40902924/persons.csv); do
    [ -f "$M/verse/masks/$s.nii.gz" ] && printf '%s\tverse\tverse\t\n' "$M/verse/masks/$s.nii.gz" >> sample2.tsv
  done
  for f in $(ls "$M"/verse/totalseg/masks/*.nii.gz | awk 'NR % 8 == 1' | head -20); do
    id=$(basename "$f" .nii.gz); printf '%s\tverse\ttotalseg\t%s\n' "$f" "$TS/$id/ct.nii.gz"
  done >> sample2.tsv
fi
export PYTHONPATH=$W/engine PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=$HOME/mambaforge/envs/spineps/bin/python
"$PY" cal.py run --list sample2.tsv --out "runs/$TAG/out" --workers "${SLURM_CPUS_PER_TASK:-32}"
"$PY" cal.py summary --out "runs/$TAG/out" --panjabi panjabi.csv
ls "runs/$TAG/out" | grep -c '\.err$' || true
