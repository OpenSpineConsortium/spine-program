#!/bin/bash
# Ship spine-program's record material from git history to the grid: _ops/ship_archive.sh
#
# Run once, from the top folder of a clone, on a computer with ssh to the grid (on Windows inside WSL:
# wsl -e bash -lc 'cd /mnt/c/.../spine-program && _ops/ship_archive.sh'). It ships the results/, figures/, manuscripts/
# and regulatory/ folders of the thirteen numbered folders as they stood at the commit ARCHIVE.md records, never the
# working tree, by the route of RECIPES.md section 0 item 2: git archive piped to tar over ssh. The extraction runs tar
# on the login node, one of the commands the Beethoven deploy runs there; it was tested for a subfolder only, and this
# tree is 673 MB in 4,379 files. If the login node kills it partway, run the script again: tar overwrites what it
# already wrote. The read bits are then opened by a short job, as job 40602926 opened the python environment, so
# that approved students (the named-user entries on the volume root) can read the copy.
#
# Nothing here names a token, a password or an AccessID: ssh uses the host alias and the key it already has.
set -eu

COMMIT=55971971cd6bba0bd2dda034665f415162924c90   # main on 2026-10-13, the last commit that holds the files in its tree
HOST=${GRID_HOST:-wsu-grid}                        # the ssh alias of grid.wayne.edu (RECIPES.md); override with GRID_HOST
DEST=/rs/rs_grp_oschome/shared/spine-program/archive

cd "$(git rev-parse --show-toplevel)"
git cat-file -e "$COMMIT^{commit}" 2>/dev/null || git fetch -q origin main

paths=()
for folder in $(git ls-tree --name-only "$COMMIT" | grep -E '^[0-9]{2}_'); do
    for sub in results figures manuscripts regulatory; do
        if git cat-file -e "$COMMIT:$folder/$sub" 2>/dev/null; then paths+=("$folder/$sub"); fi
    done
done
echo "shipping ${#paths[@]} folders from $COMMIT to $HOST:$DEST"

ssh "$HOST" "mkdir -p '$DEST'"
git archive --format=tar "$COMMIT" "${paths[@]}" \
    | ssh "$HOST" "tar -xf - -C '$DEST' && echo '$COMMIT' >> '$DEST/SHIPPED_COMMITS.txt'"
ssh "$HOST" "cd '$DEST' && sbatch --partition=reqp --qos=requeue --time=00:15:00 -D '$DEST' -o open_read_bits.out \
    --wrap 'chmod -R u+rwX,go+rX $DEST && find $DEST -type f | wc -l > FILE_COUNT.txt'"
echo "shipped; the job writes FILE_COUNT.txt in $DEST when the read bits are open (expected 4379 files plus the two records)"
