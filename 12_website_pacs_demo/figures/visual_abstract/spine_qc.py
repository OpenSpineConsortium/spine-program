# spine-program copy 2026-10-08: from CTSpinoPelvic1K poster/spine_qc.py (untracked in that repository at head 7ddfe38),
# one laptop-path line replaced (marked 'spine-program edit'); the inputs it reads (case CTs and label revisions
# as .nii.gz) are imaging data and are not in this folder. Recorded in MANIFEST_LOCAL.md.
import sys, nibabel as nib, numpy as np
sys.path.insert(0, 'scripts')  # spine-program edit: was a laptop path; scripts/ is the folder of that name in the CTSpinoPelvic1K repository at 7ddfe38 (review_anatomy_qc.py)
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
