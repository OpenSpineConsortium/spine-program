#!/bin/bash
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:30:00
cd /rs/rs_grp_oschome/go2432/cns-profile/cal
P=/rs/rs_grp_oschome/go2432/morphometry/covariates/40902924/persons.csv
$HOME/mambaforge/envs/spineps/bin/python reweight.py runs/full/out panjabi_specimens.csv $P runs/full/reweighted.json
