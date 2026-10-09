#!/bin/bash
#SBATCH --job-name=dp_preflight
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --no-requeue
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G
#SBATCH --time=12:00:00
#SBATCH --output=logs/%x_%j.out
# Read-only pre-flight for one batch (or ALL): for every item, whether it exists, what it is, its apparent and
# allocated size, file count, symlinks (absolute, dangling, relative ones that leave the item) and files with more
# than one hard link; whether the destination already exists; plus the quotas and your running jobs that name any
# item (advisory: command lines, work dirs, logs and batch scripts, in the usual spellings of the path). Writes
# preflight/<BATCH>.tsv and preflight/<BATCH>.jobs.txt.
#
#   cd ~/spinesurg-ct-nnunet/data_platform/plan && mkdir -p logs
#   sbatch -D "$PWD" --export=ALL,BATCH=B02 preflight.sbatch
#   sbatch -D "$PWD" --export=ALL,BATCH=ALL preflight.sbatch
set -uo pipefail
if [ -z "${SLURM_JOB_ID:-}" ]; then echo "refusing: run this with sbatch, never on the login node"; exit 2; fi
case "$(hostname)" in warrior*) echo "refusing on the login node"; exit 2;; esac
BATCH=${BATCH:?set BATCH=Bxx or ALL}
PLAN=${PLAN:-$PWD}
PY=${PY:-python3}
OUT="$PLAN/preflight"; mkdir -p "$OUT" logs
if [ "$BATCH" = "ALL" ]; then FILES=("$PLAN"/batch_items/B*.tsv); else FILES=("$PLAN/batch_items/$BATCH.tsv"); fi
T="$OUT/$BATCH.tsv"
printf 'batch\tsrc\tdst\texists\ttype\tapparent_bytes\tallocated_kb\tfiles\tsymlinks\tabs_symlinks\tdangling_symlinks\trel_symlinks_leaving_item\tmultilink_files\tdst_exists\tflags\n' > "$T"
{ echo "== quotas $(date '+%F %T')"; command -v pan_quota >/dev/null && pan_quota; command -v df-ceph >/dev/null && df-ceph oschome; } > "$OUT/$BATCH.quota.txt" 2>&1
for f in "${FILES[@]}"; do
  b=$(basename "$f" .tsv)
  grep -v '^#' "$f" | tr '\t' '\037' | while IFS=$'\037' read -r src dst gb flags; do
    [ -z "$src" ] && continue
    for s in $( [[ "$flags" == *glob* ]] && echo $src || echo "$src" ); do
      d="$dst"; [[ "$flags" == *glob* ]] && d="$(dirname "$dst")/$(basename "$s")"
      dx=$([ -e "$d" ] && echo yes || echo no)
      if [ ! -e "$s" ] && [ ! -L "$s" ]; then printf '%s\t%s\t%s\tno\t-\t\t\t\t\t\t\t\t\t%s\t%s\n' "$b" "$s" "$d" "$dx" "$flags" >> "$T"; continue; fi
      if [ -L "$s" ]; then typ="symlink->$(readlink "$s")"; elif [ -d "$s" ]; then typ=dir; else typ=file; fi
      app=$(du -s --apparent-size -B1 "$s" 2>/dev/null | cut -f1); alloc=$(du -s -k "$s" 2>/dev/null | cut -f1)
      nf=$(find "$s" -type f 2>/dev/null | wc -l); nl=$(find "$s" -type l 2>/dev/null | wc -l)
      na=$(find "$s" -type l -lname '/*' 2>/dev/null | wc -l); nd=$(find "$s" -xtype l 2>/dev/null | wc -l)
      nr=0; [ "$nl" -gt 0 ] && [ -d "$s" ] && nr=$("$PY" "$PLAN/verify_transfer.py" --links-only --src "$s" 2>/dev/null | awk '{print $5}')
      nh=$(find "$s" -type f -links +1 2>/dev/null | wc -l)
      printf '%s\t%s\t%s\tyes\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$b" "$s" "$d" "$typ" "$app" "$alloc" "$nf" "$nl" "$na" "$nd" "${nr:-?}" "$nh" "$dx" "$flags" >> "$T"
    done
  done
done
# running or pending jobs of yours that name an item (advisory: a path built at run time is not seen)
J="$OUT/$BATCH.jobs.txt"; : > "$J"
squeue -u "$USER" -h -t R,PD -o '%i %j' 2>/dev/null | while read -r jid jname; do
  info=$( { scontrol show job "$jid" 2>/dev/null | grep -E 'Command=|WorkDir=|StdOut=|StdErr='; scontrol write batch_script "$jid" - 2>/dev/null; } )
  cut -f2 "$T" | tail -n +2 | while read -r s; do
    rel="${s#$HOME/}"
    if printf '%s' "$info" | grep -qF -e "$s" -e "~/$rel" -e "\$HOME/$rel" -e "\${HOME}/$rel" -e "\$H/$rel"; then echo "$jid $jname names $s" >> "$J"; fi
  done
done
echo "DP_PREFLIGHT done $(date '+%F %T'): $(($(wc -l < "$T") - 1)) items, $(sort -u "$J" | wc -l) job references -> $T"
