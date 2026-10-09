# source-of-copy: CTSpinoPelvic1K repository (public, master; head 7ddfe38 on 2026-10-08), path _verify_0816/va/spine_qc_0068.py; gitignored there, so not in any commit; copied 2026-10-08 from the working tree
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
# laptop path on line 5: set before running (MANIFEST_LOCAL.md section 3.6)
import sys, nibabel as nib, numpy as np
sys.path.insert(0, r'<laptop:Desktop>\CTSpinoPelvic1K-1\scripts')
import review_anatomy_qc as RA
for rev in ['v5', 'v6']:
    ni = nib.load(f'0068_label_{rev}.nii.gz')
    lab = np.asanyarray(ni.dataobj).astype(np.int16)
    print('=' * 60, flush=True)
    print(' 0068', rev, 'ids:', sorted(int(x) for x in np.unique(lab) if x), flush=True)
    for nm in ['spine_sanity', 'class_mixing_qc', 'spine_extend_qc']:
        try:
            ok, msgs = getattr(RA, nm)(lab, ni.affine)
            print(f'  [{"PASS" if ok else "FAIL"}] {nm}', flush=True)
            for m in msgs:
                if m.startswith('X'):
                    print('       ', m[:160], flush=True)
        except Exception as e:
            print(f'  [ERR] {nm}: {type(e).__name__} {str(e)[:110]}', flush=True)
