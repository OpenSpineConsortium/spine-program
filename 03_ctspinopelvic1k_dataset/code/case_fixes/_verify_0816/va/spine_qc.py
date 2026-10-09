# source-of-copy: CTSpinoPelvic1K repository (public, master; head 7ddfe38 on 2026-10-08), path _verify_0816/va/spine_qc.py; gitignored there, so not in any commit; copied 2026-10-08 from the working tree
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
# laptop path on line 5: set before running (MANIFEST_LOCAL.md section 3.6)
import sys, nibabel as nib, numpy as np
sys.path.insert(0, r'<laptop:Desktop>\CTSpinoPelvic1K-1\scripts')
import review_anatomy_qc as RA
for rev in ['v4', 'v6']:
    ni = nib.load(f'0231_label_{rev}.nii.gz')
    lab = np.asanyarray(ni.dataobj).astype(np.int16)
    print('=' * 60, flush=True)
    print(' ', rev, flush=True)
    for nm in ['spine_sanity', 'class_mixing_qc', 'spine_extend_qc']:
        try:
            ok, msgs = getattr(RA, nm)(lab, ni.affine)
            print(f'  [{"PASS" if ok else "FAIL"}] {nm}', flush=True)
            for m in msgs:
                if m.startswith('X'):
                    print('       ', m[:150], flush=True)
        except Exception as e:
            print(f'  [ERR] {nm}: {type(e).__name__} {str(e)[:100]}', flush=True)
