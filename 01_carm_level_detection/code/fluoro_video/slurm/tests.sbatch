#!/bin/bash
# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/slurm/tests.sbatch [untracked at 097933a (laptop copy of 2026-10-08)]
#SBATCH -J fvtest
#SBATCH -p reqp
#SBATCH --qos=requeue
#SBATCH -c 4
#SBATCH --mem=16G
#SBATCH -t 01:30:00
#SBATCH -o logs/fvtest_%j.out
# Unit tests + end-to-end tests on synthetic videos with known truth + a two-run determinism check on them.
# sbatch -D $FV_WORK $FV_CODE/tools/fluoro_video/slurm/tests.sbatch
source /rs/rs_grp_oschome/go2432/data/external/fluoro_video/work/code/tools/fluoro_video/slurm/env.sh
export FV_TEST_DIR=$TMPDIR/tests
$PY -m pytest -q -rA -p no:cacheprovider tools/fluoro_video/tests
rc=$?
# keep the synthetic run's QC for inspection
mkdir -p "$FV_WORK/test_artifacts" && cp -r "$FV_TEST_DIR"/*/out "$FV_WORK/test_artifacts/" 2>/dev/null
rm -rf "$FV_WORK/test_artifacts/out/"*/*/images
echo "pytest exit $rc"
exit $rc
