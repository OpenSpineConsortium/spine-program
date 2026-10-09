#!/bin/bash
# The synthetic flexion-extension CINE (tools/polypose/cine_render.py; docs/CINE_DEMO_BUILD_PLAN_2026-09-26.md
# section 4, with the source changed to a whole-spine VerSe CT, verse823 by default). One script, five stages, one
# sequence directory, chained with afterany (a stage that exits non-zero for one frame must not strand the rest; every
# stage reads what is on disk and says what is missing):
#
#   plan    CPU (reqp), fluorogen env       frames.json, the re-keyed body mask, the corners          pp_cine_plan
#   warp    GPU array 0-(N-1)%8, container  one frame per task: volumes/f###_*.nii.gz + checks/        pp_cine_warp
#   rgt     CPU (reqp), frame 0 FIRST, then 1-(N-1): render (fixes the pose, isocentre and exposure
#           from frame 0 in render_state.json) + gt: images/, images_logor/, render/, meta/             pp_cine_rgt
#   check   CPU (reqp)                      qc/contact_sheet.png + qc/check.json -- LOOK before scoring pp_cine_check
#
# NOT HELD OUT: every VerSe CT is inside the v9 training renders. The inference over these frames (slurm/cine_eval.sh)
# must pass --not-held-out "demo on a VerSe CT; VerSe renders are in v9 training".
#
#   bash slurm/polypose_cine.sh submit --region lumbar --case verse823 [--frac 0.5] [--frames 60]   (login node: sbatch only)
#   sbatch -D ~/spinesurg-ct-nnunet -J pp_cine_plan -p reqp -q requeue --cpus-per-task=4 --mem=64G \
#       slurm/polypose_cine.sh plan --region lumbar --case verse823 --frac 0.5                 (one stage by hand)
# A stage by hand takes the stage's -J name (pp_cine_plan / pp_cine_warp / pp_cine_rgt / pp_cine_check): the
# #SBATCH name below is only a fallback, and tools/pipeline_state.py sees a stage as running by its -J name.
#
# The lumbar region moves T10-T11 .. L4-L5 with L5 fixed (verse823 has no sacrum label, so L5-S1 cannot move).
# A warp task skips its frame only when checks/f###.json carries the CURRENT plan's frame_key; after a re-plan
# into the same sequence directory every frame is re-warped, and render / gt / check refuse stale volumes.
#
# The cervical and whole regions are REFUSED until their rows in SchwingNet/results/polypose/rom_cine.json are filled
# from a verified extraction: `submit` runs `cine_render.py rom-check` (reads one JSON file, no volume) before it
# queues anything, and `plan` refuses again on the source's own chain.
#
# Estimates (not measured on this source yet): plan ~10-15 min (9.3 min for the dry run on a workstation); warp
# 3-8 min per frame on one GPU (0874 took 192 s at 151 M voxels; the lumbar slab of verse823 is 512 x 512 x 716 =
# 188 M voxels, 8 rigid bodies), so 60 frames at 8 in parallel ~ 40-60 min of GPU time after the queue; render + gt
# ~4-8 min per frame on CPU (measured on a workstation with a stand-in CT: render 110-280 s, gt 100-190 s); check
# ~2 min. The warp has NOT run anywhere yet: its first frame is its first test.
#
#SBATCH --job-name=pp_cine
#SBATCH --output=logs/pp_cine_%x_%A_%a.out
set -uo pipefail
REPO=${REPO:-$HOME/spinesurg-ct-nnunet}
SCRIPT=$REPO/slurm/polypose_cine.sh
PY=${PY:-$HOME/mambaforge/envs/fluorogen/bin/python}
LOGS=${LOGS:-$REPO/logs}
OUTROOT=${OUTROOT:-/rs/rs_grp_oschome/go2432/data/polypose/cine}
STAGE=${1:-}
[ $# -gt 0 ] && shift
REGION=lumbar; CASE=verse823; FRAC=0.5; NFRAMES=60; WARP_PAR=8
while [ $# -gt 0 ]; do
  case "$1" in
    --region) REGION=$2; shift 2;;
    --case) CASE=$2; shift 2;;
    --frac) FRAC=$2; shift 2;;
    --frames) NFRAMES=$2; shift 2;;
    --warp-parallel) WARP_PAR=$2; shift 2;;
    *) echo "unknown argument: $1"; exit 2;;
  esac
done
case "$REGION" in lumbar|cervical|whole) ;; *) echo "--region must be lumbar, cervical or whole"; exit 2;; esac
# the sequence directory is decided HERE and passed to every stage, so the shell and the python never disagree on it
FTAG=$(awk -v f="$FRAC" 'BEGIN{printf "f%03d", int(f * 100 + 0.5)}')
SEQ=$OUTROOT/${CASE}_${REGION}_fe_${FTAG}
ARGS="--region $REGION --case $CASE --frac $FRAC --frames $NFRAMES"
export PYTHONPATH=$HOME/OpenSpineToolkit:$REPO/tools OSTK_DIR=$HOME/OpenSpineToolkit
export PYTHONNOUSERSITE=1 MPLBACKEND=Agg HF_HUB_OFFLINE=1 OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-4}
export TMPDIR=$HOME/tmp; mkdir -p "$TMPDIR"
CR=tools/polypose/cine_render.py
cd "$REPO" || exit 2
[ "$STAGE" = submit ] || echo "== pp_cine $STAGE $SEQ task ${SLURM_ARRAY_TASK_ID:-} host $(hostname) job ${SLURM_JOB_ID:-} $(date -Is)"

case "$STAGE" in
  plan)
    "$PY" -u $CR plan $ARGS --seq-dir "$SEQ"
    exit $?;;
  warp)
    T=${SLURM_ARRAY_TASK_ID:?the warp runs as an array task, one frame each}
    source "$REPO/slurm/polypose_env.sh"
    pp_setup_ok || { echo "PolyPose setup not OK"; exit 2; }
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo "no GPU: device ${PP_DEVICE:-auto}"
    pp_run --nv "$PP_PY" -u $CR warp --seq-dir "$SEQ" --frame "$T" 2>&1 | grep -v -i -E "warn|deprecat|tqdm"
    R=${PIPESTATUS[0]}
    echo "== warp f$(printf %03d "$T") rc $R $(date -Is)"
    exit $R;;
  rgt)
    T=${SLURM_ARRAY_TASK_ID:?render + gt run as an array task, one frame each}
    "$PY" -u $CR render --seq-dir "$SEQ" --frame "$T" || exit $?
    "$PY" -u $CR gt --seq-dir "$SEQ" --frame "$T"
    exit $?;;
  check)
    "$PY" -u $CR check --seq-dir "$SEQ"
    exit $?;;
  submit)
    "$PY" $CR rom-check --region "$REGION" || { echo "nothing submitted"; exit 3; }
    mkdir -p "$LOGS" "$OUTROOT"
    N1=$((NFRAMES - 1))
    P=$(sbatch --parsable -D "$REPO" -J pp_cine_plan -p reqp -q requeue --cpus-per-task=4 --mem=64G --time=01:30:00 \
        -o "$LOGS/pp_cine_plan_%j.out" "$SCRIPT" plan $ARGS) || exit 4
    W=$(sbatch --parsable -D "$REPO" -J pp_cine_warp -q gpu -p galhp,gvohp,gmsap --gres=gpu:1 --cpus-per-task=8 \
        --mem=120G --time=01:30:00 --array=0-$N1%$WARP_PAR --dependency=afterany:$P \
        -o "$LOGS/pp_cine_warp_%A_%a.out" "$SCRIPT" warp $ARGS) || exit 4
    # frame 0 alone first: it fixes the pose, the isocentre, the exposure terms and the field for every other frame
    R0=$(sbatch --parsable -D "$REPO" -J pp_cine_rgt -p reqp -q requeue --cpus-per-task=4 --mem=32G --time=01:00:00 \
         --array=0 --dependency=afterany:$W -o "$LOGS/pp_cine_rgt_%A_%a.out" "$SCRIPT" rgt $ARGS) || exit 4
    R=$(sbatch --parsable -D "$REPO" -J pp_cine_rgt -p reqp -q requeue --cpus-per-task=4 --mem=32G --time=01:00:00 \
        --array=1-$N1 --dependency=afterany:$R0 -o "$LOGS/pp_cine_rgt_%A_%a.out" "$SCRIPT" rgt $ARGS) || exit 4
    C=$(sbatch --parsable -D "$REPO" -J pp_cine_check -p reqp -q requeue --cpus-per-task=2 --mem=16G --time=00:30:00 \
        --dependency=afterany:$R -o "$LOGS/pp_cine_check_%j.out" "$SCRIPT" check $ARGS) || exit 4
    echo "plan $P  warp $W (0-$N1%$WARP_PAR)  rgt0 $R0  rgt $R (1-$N1)  check $C  -> $SEQ"
    printf 'plan=%s\nwarp=%s\nrgt0=%s\nrgt=%s\ncheck=%s\nseq=%s\nregion=%s\ncase=%s\nfrac=%s\nframes=%s\nsubmitted=%s\n' \
      "$P" "$W" "$R0" "$R" "$C" "$SEQ" "$REGION" "$CASE" "$FRAC" "$NFRAMES" "$(date -Is)" > "$SEQ.jobs.txt"
    exit 0;;
  *)
    echo "usage: polypose_cine.sh {submit|plan|warp|rgt|check} [--region lumbar|cervical|whole] [--case verse823]" \
         "[--frac 0.5] [--frames 60] [--warp-parallel 8]"
    exit 2;;
esac
