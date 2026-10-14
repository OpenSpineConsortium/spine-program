#!/bin/bash
#SBATCH --job-name=check_app_inputs
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:10:00
#SBATCH --output=%x_%j.out
# Issue #25 (CT-2): can this account read the v11 release and import what the APP fit needs?
# Read-only; safe to resubmit. Submit from your own Ceph folder:
#   sbatch -D /rs/rs_grp_oschome/$USER/ct2 /rs/rs_grp_oschome/$USER/ct2/check_app_inputs.sbatch
export PYTHONNOUSERSITE=1
PY=/rs/rs_grp_oschome/go2432/envs/spineps212/bin/python
REL=/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K

echo "== release"
ls -ld "$REL" "$REL/labels" "$REL/ct"
echo "labels: $(ls "$REL/labels" | wc -l)  ct: $(ls "$REL/ct" | wc -l)"
ls "$REL/labels" | head -3

echo "== python"
"$PY" -c "import sys, numpy, scipy, nibabel; print(sys.version.split()[0], 'numpy', numpy.__version__, 'scipy', scipy.__version__, 'nibabel', nibabel.__version__)"
echo "exit=$?"

echo "== ostk in the shared environment"
"$PY" -c "import ostk, ostk.labels; print('ostk at', ostk.__file__)"
echo "exit=$?"

echo "== one label volume"
F=$(ls "$REL/labels" | head -1)
"$PY" -c "
import sys, nibabel as nib, numpy as np
img = nib.load(sys.argv[1])
d = np.asarray(img.dataobj)
print('file', sys.argv[1].split('/')[-1], 'shape', d.shape, 'axcodes', nib.aff2axcodes(img.affine), 'zooms', img.header.get_zooms())
print('ids', sorted(int(i) for i in np.unique(d)))
" "$REL/labels/$F"
echo "exit=$?"
