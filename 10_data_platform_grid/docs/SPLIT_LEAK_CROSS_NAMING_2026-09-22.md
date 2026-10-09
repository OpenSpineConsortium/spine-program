# One person, two names, two independent splits — measured in the shipped level banks

Found 2026-09-22, after the NHANES defect, by asking the same question of every other source pair.

## The rule that caused it

`tools/make_context_crops.py` drew its split PER SOURCE DIRECTORY: for each `--drr` root it shuffled that root's
groups and took a validation fraction. Two roots holding the same person under different names are therefore
shuffled separately, and the person lands in training through one root and in validation through the other. No
score can show this: both sides look like ordinary held-out cases.

## The two instances, measured

**NHANES II** (`docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md`). `~/films_drr` carries the annotated subset as source
`nhanes` with `patient_id` `nhanes_00160`; `~/nhanes_drr` carries the same 543 films as `NH_00160_c` / `NH_00160_l`.
In banks v2, v6 and v7: 48 of the 54 NHANES validation patients had their other copy in training.

**CTSpinoPelvic1K.** `~/ctsp_drr` names a case `CTSP_COLONOG_<n>` (the Dataset813 stem). `~/physics_drr` and
`~/physics_rare` name the same patient `ctsp_<release id>_<view>_p<k>`. The two names are tied only by the
Dataset813 symlink `imagesTr/COLONOG_<n>_0000.nii.gz -> <release id>_ct.nii.gz`. Resolving that crosswalk over the
802 links and re-keying every case of every render bank:

| bank | people in validation | people in training | people on BOTH sides | of those, split only by the naming |
|---|---:|---:|---:|---:|
| allspine_v7_fov96_ctx | 620 | 3,240 | 371 | **357** |
| allspine_v6_fov96_ctx | 620 | 3,240 | 371 | **357** |

Every one of the 357 is a CTSpinoPelvic1K patient whose CT render was validation and whose physics render was
training, or the reverse. v2 was built by the same rule, so it has the same defect.

Not affected by this instance: the film corpora (BUU, CSXA, Mendeley, VinDr are different people from the CT
collections), and every C-arm result, which is scored on a device held out whole.

## What was also checked and is CLEAN

**Synthetic frames stay with their CT.** The device corpus styles each render with several cards and several
geometries. Its split is drawn on the TotalSegmentator subject, and all five styled corpora
(`cios_fusion__cios_fusion`, `cios_fusion__elekta_xvi`, `cios_fusion__surgio_b51_dr`, `elekta_xvi__elekta_xvi`,
`surgio_b51_dr__surgio_b51_dr`) record the SAME 17 validation subjects in their `STYLE_INFO.json`. A subject is
therefore on the same side of the split in every geometry and under every noise card: geometries are not mixed
across training and test, and a synthetic frame never sits opposite the CT it came from.

**Pose duplicates within a bank.** `--group-regex` already collapses the several poses of one CT into one split
group (physics_drr: 7,045 cases in 2,201 groups).

## The fix

`tools/patient_keys.py` writes one key per PERSON across every naming scheme, resolving the Dataset813 crosswalk
and the NHANES pair; `tools/test_patient_keys.py` asserts that the two defects collapse. `make_context_crops.py`
takes `--patient-json` and then draws ONE split over people across all sources, refuses a case it cannot key
(`--allow-unkeyed` to override), records the key file in the bank's `meta.json`, and fails if any person still
appears on both sides.

The clean rebuild is `slurm/allspine_v8_clean.sh` -> `allspine_v8_bank.sh` -> `allspine_v8_train.sh`: the v2 source
list without the redundant `~/nhanes_drr` copy, one split over people, then the encoder and the mixed-length head
at three seeds, scored per source. Until it lands, no pooled real-film number from v2, v6 or v7 should be quoted;
the per-source CSXA and BUU-LSPINE figures the manuscript uses are unaffected by both instances.
