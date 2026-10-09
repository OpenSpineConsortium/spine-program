#!/bin/bash
# source-of-copy: spinesurg-ct-nnunet repository (private), branch L6_Class, commit 097933a, path scripts/export_env.sh
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
# Export the EXACT environment the results were produced in, from the machine that produced them.
#
# WHY NOT JUST requirements.txt. That file says what the project depends on; it does not say what ran. A
# reader who installs from it gets whatever those ranges resolve to today, which is not what produced the
# numbers in the paper. This writes a lock -- exact versions, the CUDA build, the driver, the Python -- from
# the grid environment the jobs actually use, and stamps it with the commit and the date so a mismatch is
# visible rather than silent.
#
# The probe is piped to the remote shell on STDIN rather than embedded in the ssh argument. Quoting a python
# -c through wsl -> ssh -> bash needs three levels of escaping, and the first version of this script got it
# wrong in the quiet way: the pip list came back fine and the python, torch and GPU lines came back EMPTY, so
# the lock looked complete and was missing the part that pip cannot reconstruct.
#
# Runs against the grid over WSL, because Windows sockets flake here and the environment being described is
# the grid's, not this laptop's.
set -u
cd "$(dirname "$0")/.."
OUT=env
mkdir -p "$OUT"
REMOTE=${REMOTE:-go2432@grid.wayne.edu}
STAMP=$(date -Is)
GIT=$(git rev-parse --short HEAD 2>/dev/null || echo unknown)
# The probe lives in the repository and is handed to the remote shell on stdin. Its path has to cross the
# Git-Bash/WSL boundary, and those two do not share /tmp -- the first version wrote the probe to mktemp and
# WSL could not see it, so the lock came back with one line in it.
HERE=$(pwd)
WSLPATH=$(printf '%s' "$HERE" | sed 's#^/\([a-zA-Z]\)/#/mnt/\1/#')
PROBE="$WSLPATH/scripts/_env_probe.sh"
BODY=$(wsl -e bash -lc "ssh -o BatchMode=yes $REMOTE 'bash -s' < \"$PROBE\"" 2>/dev/null)

n=$(printf '%s\n' "$BODY" | grep -cv '^#')
if [ "${n:-0}" -lt 20 ]; then
  echo "only ${n:-0} packages captured -- the grid was not reachable, so the lock was NOT written"
  echo "the previous lock is left in place rather than replaced with a stub"
  exit 1
fi
if ! printf '%s\n' "$BODY" | grep -q '^# torch'; then
  echo "the probe returned packages but no torch/CUDA line -- refusing to write a lock that omits the"
  echo "one thing pip cannot restore. Check ssh to $REMOTE and re-run."
  exit 1
fi

{
  echo "# The environment the grid jobs run in, as it was on $STAMP"
  echo "# repository commit: $GIT"
  echo "# host: $REMOTE   interpreter: ~/mambaforge/envs/spineps/bin/python"
  echo "#"
  echo "# Regenerate with: make env-lock   (or bash scripts/export_env.sh)"
  echo "# Install with:    pip install -r env/spineps.lock.txt   into a matching Python"
  echo "#"
  echo "# Read the header before the list: the CUDA build is part of the answer, and pip cannot restore a"
  echo "# driver. A run on a different CUDA minor version is a different run and should say so."
  echo "#"
  printf '%s\n' "$BODY"
} > "$OUT/spineps.lock.txt"

echo "wrote $OUT/spineps.lock.txt  ($n packages)"
grep '^#' "$OUT/spineps.lock.txt" | sed -n '1,12p'
