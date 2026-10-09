#!/usr/bin/env bash
# copy record: source OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path tools/grid.sh; copied 2026-10-08 into spine-program/11_students_grid_access; redactions: none
# tools/grid.sh — the handful of remote calls a project needs, with one layer of quoting.
#
#   tools/grid.sh run "squeue -u \$USER"           run a short command on the login node
#   tools/grid.sh sync                              git pull the grid clone to match origin
#   tools/grid.sh submit templates/slurm_job.sh projects/me/measure.py --data ~/data/CTSpinoPelvic1K --out projects/me/results
#   tools/grid.sh wait 40056610                     poll a job every 30 s, then print its logs
#   tools/grid.sh pull projects/me/results projects/me/results     rsync a folder back
#
# Set GRID_HOST (default "grid", the ~/.ssh/config alias) and GRID_REPO (default
# ~/Student_Projects on the grid) if yours differ. On Windows run this from WSL.
#
# Why this file exists: every attempt to inline scripts or multi-argument commands through
# wsl -> ssh -> heredoc or sbatch --wrap got mangled by quoting. Job scripts are files in
# the repo; this helper only ever sends short, single-layer commands.
set -euo pipefail

HOST="${GRID_HOST:-grid}"
REPO="${GRID_REPO:-Student_Projects}"
SSH=(ssh -o BatchMode=yes -o ConnectTimeout=20 "$HOST")

cmd="${1:-}"; shift || true
case "$cmd" in
  run)
    "${SSH[@]}" "$*" ;;
  sync)
    "${SSH[@]}" "cd ~/$REPO && git pull -q && git log --oneline -1 && if [ -d projects/.git ]; then (cd projects && git pull -q && git log --oneline -1); fi" ;;
  submit)
    script="${1:?job script, e.g. templates/slurm_job.sh}"; shift
    out=$("${SSH[@]}" "cd ~/$REPO && mkdir -p logs && sbatch $script $*")
    echo "$out"
    echo "$out" | grep -o '[0-9]\+$' > .last_jobid 2>/dev/null || true ;;
  wait)
    job="${1:-$(cat .last_jobid 2>/dev/null)}"; [ -n "$job" ] || { echo "no job id"; exit 1; }
    echo "waiting on job $job"
    for i in $(seq 1 720); do
      st=$("${SSH[@]}" "squeue -j $job -h -o %T" 2>/dev/null || true)
      [ -z "$st" ] && break
      printf '  %s %s\n' "$(date +%H:%M)" "$st"
      sleep 30
    done
    "${SSH[@]}" "cd ~/$REPO && sacct -j $job --format=JobID,State,Elapsed,MaxRSS -n | head -3; echo '--- stdout tail'; tail -n 40 logs/*_$job.out 2>/dev/null; echo '--- stderr tail'; tail -n 20 logs/*_$job.err 2>/dev/null" ;;
  pull)
    remote="${1:?remote path relative to the repo}"; local_="${2:?local destination}"
    mkdir -p "$local_"
    rsync -avz --exclude '*.nii.gz' "$HOST:~/$REPO/$remote/" "$local_/" ;;
  *)
    sed -n '2,15p' "$0"; exit 1 ;;
esac
