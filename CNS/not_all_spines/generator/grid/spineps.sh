#!/bin/bash
#SBATCH --cpus-per-task=32
#SBATCH --mem=128G
#SBATCH --time=02:00:00
W=/rs/rs_grp_oschome/go2432/cns-profile/cal
H=/rs/rs_grp_oschome/go2432/data/anomaly_harvest
cd "$W"
{ ls $H/tcia_fdg_pet_ct_lesions/spineps/*_seg-vert_msk.nii.gz | awk 'NR % 20 == 1' | head -40
  ls $H/totalsegmentator/spineps/*_seg-vert_msk.nii.gz | awk 'NR % 50 == 1' | head -20
  ls $H/abdomenatlas3_mini/spineps/*_seg-vert_msk.nii.gz | awk 'NR % 50 == 1' | head -20; } > spineps_sample.txt
wc -l spineps_sample.txt
export PYTHONPATH=$W/engine PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=$HOME/mambaforge/envs/spineps/bin/python
"$PY" spineps_cal.py spineps_sample.txt runs/spineps2/out 32
ls runs/spineps2/out | grep -c err
"$PY" cal.py summary --out runs/spineps2/out --panjabi panjabi.csv
