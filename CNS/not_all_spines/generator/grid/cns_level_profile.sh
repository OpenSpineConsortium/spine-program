#!/bin/bash
#SBATCH --cpus-per-task=32
#SBATCH --mem=64G
#SBATCH --time=06:00:00
# The Benzel slide's second line (Greg, 2026-10-31): bordercall's morphometry engine, as SchwingNet's
# grid/bordercall pins it at SchwingNet a82dfd7 (bordercall 9c85de1, the engine that measured the gold
# tier 3 rows), over the gold tier 4 TotalSegmentator maps that grid/level_profile.py links, then the
# profile by level over those rows and the gold tier 3 rows. Queued by hand through hpcworker's job
# submit (batch class) from /rs/rs_grp_oschome/go2432/cns-profile, where code/ holds this folder's copy;
# writes only under cns-profile/<job>/. The rows stay on the grid; profile.json, aggregates alone, leaves it.
set -uo pipefail
HERE=/rs/rs_grp_oschome/go2432/cns-profile
OUT=$HERE/${SLURM_JOB_ID:-$$}
GOLD4=/rs/rs_grp_oschome/go2432/gold4-totalseg
MORPH=/rs/rs_grp_oschome/go2432/morphometry
PERSONS=$MORPH/covariates/40902924/persons.csv
ENGINE_COMMIT=a82dfd7f
PY=$HOME/mambaforge/envs/spineps/bin/python
CPUS=${SLURM_CPUS_PER_TASK:-32}
umask 077
mkdir -p "$OUT/engine"
export PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
echo "$(date -u '+%F %T') UTC job ${SLURM_JOB_ID:-none} on $(hostname -s)"
git -C "$HOME/SchwingNet" archive "$ENGINE_COMMIT" grid/bordercall | tar -x -C "$OUT/engine" || { echo "no engine copy"; exit 2; }
export PYTHONPATH=$OUT/engine/grid/bordercall
"$PY" "$HERE/code/level_profile.py" links --records "$GOLD4/records.jsonl" --labels-root "$GOLD4" --masks "$OUT/masks" || exit 2
"$PY" -m morphometry run --masks "$OUT/masks" --scheme verse --out "$OUT/gold4" --workers "$CPUS" --lines > "$OUT/run.log" 2>&1
echo "morphometry run: exit $?; $(tail -n 2 "$OUT/run.log" | tr '\n' ' ')"
"$PY" "$HERE/code/level_profile.py" profile --morphometry "$MORPH" --persons "$PERSONS" --gold4 "$OUT/gold4/rows.csv" \
  --out "$OUT/profile.json" || exit 1
echo "$(date -u '+%F %T') UTC done"
