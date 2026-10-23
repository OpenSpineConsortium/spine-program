#!/usr/bin/env bash
# Upload the posterior pipeline and submit fetch -> predict (transitional records first, one GPU; the rest on six)
# -> analyze (once after the transitional records, once after everything). Run from WSL.
set -euo pipefail
L=/mnt/c/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/paper/cns2026/posterior
V=/mnt/c/Users/grego/OneDrive/Desktop/NextPaper/spinopelvic-seg/tools/nnunet_wandb_variant.py
W=/rs/rs_grp_oschome/go2432/cns2026_posterior
sed -i 's/\r$//' "$L"/*.sbatch "$L"/*.py
ssh -o BatchMode=yes go2432@grid.wayne.edu "mkdir -p $W/src $W/logs $W/pred"
rsync -t -e "ssh -o BatchMode=yes" "$L"/fetch.sbatch "$L"/predict.sbatch "$L"/analyze.sbatch "$L"/analyze.py "$V" "go2432@grid.wayne.edu:$W/src/"
ssh -o BatchMode=yes go2432@grid.wayne.edu 'bash -s' <<'REMOTE'
set -euo pipefail
W=/rs/rs_grp_oschome/go2432/cns2026_posterior
RAW=$HOME/spinesurg-ct-nnunet/nnunet/raw/Dataset803_SpineSurgCTFullMerged
FIRST="COLONOG_699 COLONOG_149 COLONOG_261_r1 COLONOG_615 COLONOG_4_r1 COLONOG_6_r1 COLONOG_555_r1 COLONOG_666_r1 COLONOG_721_r1"
rm -rf "$W/in_lstv" "$W/in_rest"; mkdir -p "$W/in_lstv" "$W/in_rest"
for l in "$RAW"/imagesTs/*_0000.nii.gz; do
  f=$(basename "$l"); case=${f%_0000.nii.gz}; t=$(basename "$(readlink "$l")")
  d=in_rest; for c in $FIRST; do [ "$c" = "$case" ] && d=in_lstv; done
  ln -s "/data/hf_export/ct/$t" "$W/$d/$f"
done
echo "in_lstv $(ls $W/in_lstv | wc -l)  in_rest $(ls $W/in_rest | wc -l)"
cd "$W"
A=$(sbatch --parsable src/fetch.sbatch)
B=$(sbatch --parsable --dependency=afterok:$A --export=ALL,INPUT=in_lstv,NPARTS=1 src/predict.sbatch)
C=$(sbatch --parsable --dependency=afterok:$A --array=0-5 --export=ALL,INPUT=in_rest,NPARTS=6 src/predict.sbatch)
D=$(sbatch --parsable --dependency=afterany:$B --export=ALL,OUT=analysis_lstv src/analyze.sbatch)
E=$(sbatch --parsable --dependency=afterany:$B:$C --export=ALL,OUT=analysis_all src/analyze.sbatch)
echo "SUBMITTED fetch=$A pred_lstv=$B pred_rest=$C analyze_lstv=$D analyze_all=$E"
REMOTE
