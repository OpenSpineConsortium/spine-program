#!/bin/bash
#SBATCH --cpus-per-task=2
#SBATCH --mem=16G
#SBATCH --time=01:00:00
# The profile again over the rows job 40906591 measured, with the canal keys added (the slide's second panel,
# Benzel Fig. 1.9); measures nothing, writes cns-profile/<job>/profile.json.
HERE=/rs/rs_grp_oschome/go2432/cns-profile
M=/rs/rs_grp_oschome/go2432/morphometry
OUT=$HERE/${SLURM_JOB_ID:-$$}
umask 077; mkdir -p "$OUT"
"$HOME/mambaforge/envs/spineps/bin/python" "$HERE/code/level_profile.py" profile --morphometry "$M" \
  --persons "$M/covariates/40902924/persons.csv" --gold4 "$HERE/40906591/gold4/rows.csv" --out "$OUT/profile.json"
