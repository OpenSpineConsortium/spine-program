#!/bin/bash
#SBATCH --job-name=dedup_guard
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=01:00:00
#SBATCH --output=logs/%x_%j.out
# dedup_guard.sh -- run before deleting or moving any folder or file on Ceph (or its HOME spelling). It exits 1 and
# lists the links when any dedup ledger (applied/<gid>.ledger.tsv or its copy in $LEDGER2_DIR) records a symlink that
# is still live (it resolves to its canonical) and whose canonical file lies in a path to be deleted. Deleting such a
# path would leave every one of those links dangling and remove the only bytes of their duplicates. Read-only.
#
#   cd ~/spinesurg-ct-nnunet/data_platform/dedup && mkdir -p logs
#   sbatch -D "$PWD" --wrap 'bash dedup_guard.sh /rs/rs_grp_oschome/go2432/data/versefusion/raw/VerSeFusion_data/canonical'
#   (or call it at the top of any deletion job: bash dedup_guard.sh <path>... || exit 1)
#
# exit 0: nothing links into the paths; 1: live links found (listed); 2: usage, or no ledger folder readable.
# A ledger row whose link was rolled back or replaced is not live and does not block. ROLLBACK=1 of the groups named
# (dedup_apply.sbatch) clears the block.
set -uo pipefail
if [ -n "${SLURM_JOB_ID:-}" ] || [ "${DEDUP_GUARD_ANYWHERE:-0}" = "1" ]; then :; else
  case "$(hostname)" in warrior*) echo "refusing on the login node: run it in a job (or from a deletion job)"; exit 2;; esac
fi
[ "$#" -ge 1 ] || { echo "usage: dedup_guard.sh <path> [<path> ...]"; exit 2; }
DEDUP_DIR=${DEDUP_DIR:-$(cd "$(dirname "$0")" && pwd)}
# shellcheck source=dedup_lib.sh
. "$DEDUP_DIR/dedup_lib.sh" || { echo "no $DEDUP_DIR/dedup_lib.sh"; exit 2; }
[ -d "$APPLIED" ] || [ -d "$LEDGER2_DIR" ] || { echo "no ledger folder ($APPLIED, $LEDGER2_DIR)"; exit 2; }

declare -a T=()
for t in "$@"; do
  t=${t%/}
  T+=("$t")
  r=$(readlink -f -- "$t" 2>/dev/null) && [ "$r" != "$t" ] && T+=("$r")
done
declare -A seen=()
n=0
while IFS= read -r lf; do
  while IFS= read -r line || [ -n "$line" ]; do
    [[ -z $line || $line == \#* ]] && continue
    split_tab "$line"
    case "${F[2]:-}" in link_file|tree_member|link_tree) ;; *) continue ;; esac
    d=${F[3]}; c=${F[4]}
    hit=""
    for t in "${T[@]}"; do under "$c" "$t" && { hit=$t; break; }; done
    if [ -z "$hit" ]; then
      cr=$(readlink -f -- "$c" 2>/dev/null) || cr=$c
      for t in "${T[@]}"; do under "$cr" "$t" && { hit=$t; break; }; done
    fi
    [ -n "$hit" ] || continue
    [ -n "${seen[$d]:-}" ] && continue
    # live: the duplicate path (a symlink, or a file below a tree link) still resolves to the canonical
    if [ "$d" != "$c" ] && [ "$(readlink -f -- "$d" 2>/dev/null)" = "$(readlink -f -- "$c" 2>/dev/null)" ]; then
      seen[$d]=1; n=$((n + 1))
      [ "$n" -le 50 ] && printf 'LIVE %s -> %s  (ledger %s, group %s)\n' "$d" "$c" "$lf" "$(basename "$lf" .ledger.tsv)"
    fi
  done < "$lf"
done < <(ledger_files)
if [ "$n" -gt 0 ]; then
  echo "REFUSE: $n live link(s) have their canonical in [$*]; run dedup_apply.sbatch ROLLBACK=1 for the groups listed first"
  exit 1
fi
echo "OK: no dedup link has its canonical in [$*]"
exit 0
