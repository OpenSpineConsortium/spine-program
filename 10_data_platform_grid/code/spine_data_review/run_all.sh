#!/usr/bin/env bash
# One-command reproduction of the review: bash run_all.sh --run-date YYYY-MM-DD [make variables]
#
# Runs `make all RUN_DATE=<date>` from spine_data_review/. Every network stage must go through WSL
# (PROTOCOL.md section 15; Windows sockets are unreliable here), so when this script is started
# from Git Bash on Windows it re-executes itself inside WSL; inside WSL or on Linux it runs make
# directly. Extra arguments are passed to make, e.g. `bash run_all.sh --run-date 2026-09-21
# LIMIT=5` or `... AVAIL_FLAGS=--apply` for the second probe pass. --replay (or REPLAY=1) re-runs
# the chain offline from runs/<date>/raw/ and fails on a cache miss: the reproduction of a run that
# sends nothing. The run date is the only date written into outputs; the run directory is runs/<date>.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_DATE=""; ARGS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --run-date) RUN_DATE=$2; shift 2;;
    --run-date=*) RUN_DATE=${1#*=}; shift;;
    --replay) ARGS+=("REPLAY=1"); shift;;
    -h|--help) sed -n '2,10p' "$0"; exit 0;;
    *) ARGS+=("$1"); shift;;
  esac
done
[[ "$RUN_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || { echo "usage: bash run_all.sh --run-date YYYY-MM-DD [VAR=value ...]" >&2; exit 2; }

if [ -z "${WSL_DISTRO_NAME:-}" ] && command -v wsl.exe >/dev/null 2>&1; then
  # Git Bash on Windows: <laptop drive>/Users/... -> <laptop drive>/Users/... and hand over to WSL.
  WPATH=$(printf '%s' "$HERE" | sed -E 's#^/([A-Za-z])/#/mnt/\L\1/#')
  exec wsl.exe -e bash -lc "cd '$WPATH' && make all RUN_DATE='$RUN_DATE' ${ARGS[*]:-}"
fi
cd "$HERE"
exec make all RUN_DATE="$RUN_DATE" "${ARGS[@]}"
