# TODO: what is not on the grid, or not done, and remains

Ordered. Each step carries its gate, the pre-stated number where one exists, the dependency and who decides.
Sources: `../_plan/PLAN.md` section 3 project 08 "First five steps" (steps 1 to 5); `docs/handoff/OPEN_QUESTIONS.md`
(OQ rows); `docs/handoff/RESEARCH_DIRECTIONS.md` (RD); `docs/handoff/RECIPES.md` sections 5 and 6; the data-platform
cards quoted in `MANIFEST_GRID.md`. "Engineering" means a student or a Claude session may do it under the standing
rules; "Greg" means Greg decides before it starts. Nothing runs on the login node; every step is an `sbatch` job
submitted with `sbatch -D`. Every quoted score goes through `tools/eval_gate.py`.

## The first five steps (the plan's order)

| # | step | gate and number | depends on | decides |
|---|---|---|---|---|
| 1 | Read `$RS/data/or_ready/devices_refit`, `devices_refit_constrained`, `devices_refit_v2` and `~/spine-detector/runs/devcorpus/*/scores.json` in a job: answer OQ B9 (were the cards refitted under `DF_CONVERSION=linear`) and OQ B10 (which of the three box conventions of `rescore_outline.md` the `scores.json` rows use; why `dc_B_held_cios_fusion_s1` has no row) | `MODEL_CARD.md` section 4.6 reconciled with `scores.json`; the convention named; both answers written into `STATUS.md` section 4 with the file | nothing | engineering |
| 2 | PolyPose validation: the chain was started (the 22-case inspection and one smoke variant `pp_ctsp_0874_v000`, generated 2026-09-23 with sampler commit 1001a82, sit in `results/polypose/validation/`) and never reported; run `slurm/polypose_validate_submit.sh` (gen, fin, render, collect) on `reqp` or a GPU partition, write `results/polypose/VALIDATION.{json,md}` through `tools/polypose/validation_report.py`; record whether any training bank ever used a PolyPose variant; commit `rom_cine.json`, `tools/polypose/cine_render.py` and its job script `slurm/polypose_cine.sh` (all three untracked on 2026-10-08; `MANIFEST_CODE.md` section 1) and confirm 1f4418f on GitHub when network is available | the file exists with the Dice and range-of-motion checks; the invariant self-test fails when a fold, a moved fusion or a shifted pelvis is injected; fused junctions zero motion confirmed (OQ C18; G.6) | nothing | engineering; Greg pushes |
| 3 | The primary C7 criterion: paired bootstrap of each styled-corpus arm (designs A and B, both seeds) against the LODO real-frame baseline on the same held-out device (OQ C14); then the exposure-clip A/B on real frames with `slurm/device_spread_arm.sh` (OQ C17) | "improves" only with an interval excluding zero; otherwise the sentence "not met" with the number; the default sampler changes from `SPREAD = 0.2` to the typicality gate only if that interval excludes zero (`docs/DEVICE_SPREAD_SWEEP.md` last paragraph) | step 1 (the convention); project 10 batches B10 and B11 if the banks have moved | engineering |
| 4 | Correct paper 1's Table 1 TotalSegmentator rows and the 4,093-render footnote from the v9 build roots; correct `DATASHEET.md` and `MODEL_CARD.md` where they call the device corpus "v2" (OQ F6); correct the MODEL_CARD 4.6 sentence "two of the three" to "none of the three" (A6.13 [WORDING]) and the "scored zero" wording of A11.2 | `ts_drr` and `ts_drr_v3` counted out; `physics_drr` and `physics_rare` counted in; numbers re-enter through the manifest key, never typed | step 1 | engineering (paper 1 is held in project 01) |
| 5 | The synthetic:real ratio array: real share 0.1 to 0.9, N 25 and all, three seeds, about 45 cells, L6 scored separately, on the clean encoder of project 02 (OQ A9, C5; `memory/synthetic-real-ratio-evidence.md` "the experiment this project can be first to publish") | a cell counts if it raises held-out L6 recall without lowering ordinary film naming by more than the seed spread (1.0 point at full size); the plateau reported as a curve, never one ratio; the sentence says whether it is joint mixing or pretrain-then-fine-tune | project 02 step 5 (the clean encoder); Greg's yes | Greg |

## Open questions and defects of this folder (OQ rows not covered above)

| # | step | gate and number | depends on | decides |
|---|---|---|---|---|
| 6 | OQ B12: list `~/physics_drr/ann` in a job and settle 7,045 against 7,048; record the per-prefix counts | one count, with the listing's date, written into `STATUS.md` section 1 and into the `physics_drr` card | nothing | engineering |
| 7 | OQ B22: per-source render counts inside `allspine_v9_fov96_ctx` (`meta.json`, case arrays) and whether the 1,321 implant renders come from `implant_ct` (deleted), `implant_ts` or both | counts per source with the file | nothing (the bank is on HOME) | engineering |
| 8 | OQ C15: the leakage audit over every device-corpus training list (`tools/leak_check.py check`); add design P's refusal to designs A and B in `tools/devcorpus_build.py lists` | zero subjects on two sides in every list, or the arms that fail named | nothing | engineering |
| 9 | OQ E5: write the criterion for why the 2,293 DeepFluoro vendor frames and `~/fluorogen/synth_rare` (12,929 renders, 9.0 GB) are unused; use all or justify in writing (rule 9) | a written criterion in `docs/`; a bank either admitted through `tools/realxray_banks.json` or excluded with the reason | nothing | Greg (a data directive) |
| 10 | C4.3: if step 1 finds no linear-conversion refit, refit the DeepFluoro-derived cards with `slurm/device_fit.sh` (`CMD=fit`, `DEVICE=cios_fusion`) after copying the shipped card aside; every refit must pass its own acceptance gate | held-out R^2 at or above A12.1's 0.905 on 40 frames; the gate of `sn:figures/figS2.record.json` panel d | step 1 | engineering |
| 11 | Recover Cios Fusion kVp by a per-frame join of the 366 registered frames to the 2,654 vendor DICOMs (`memory/device-sampling-audit.md`); add kVp to the Cios copula | the term enters the card with its census file; the card's coverage statistic unchanged or better | nothing | engineering |
| 12 | Register the device-corpus detectors (`~/spine-detector/runs/devcorpus/dc_*`, no alias on 2026-10-08) in `~/model_registry` with `tools/model_registry.py` | every `dc_*` arm has an alias and a sha in `registry.jsonl` | nothing | engineering |

## Bank hygiene (the cards' "known defects and gaps"; RECIPES 5)

| # | step | gate and number | depends on | decides |
|---|---|---|---|---|
| 13 | `verse_drr`: delete the 13 `glgl*` byte twins, fix the prefix logic, rerun `make_drr_dataset.py --scheme verse` (card `verse_drr`; dedup group A04 `removal_preferred`) | 374 annotations, no duplicate sha | project 10 (B06 cut over; dedup apply) | engineering |
| 14 | `ts_drr`: delete `path/*.npy` and rerun `slurm/path_render.sh` against the v2 root (card `ts_drr`, defect 19) | 1,170 path files whose source string is v2.0.1 | B07 landed | engineering |
| 15 | `ts_drr_v3`, `verse_soft_drr`, `ctsp_drr_obl`, `ctsp_drr_obl2`, the smoke directories (`physics_smoke`, `render_smoke`, `implant_ct_smoke`, `implant_verse_smoke`), `$RS/data/morphdef` (three empty folders): retire or delete per the deletion-candidate table | Greg's per-item decision recorded in `MIGRATION_PLAN.md` section 8 | nothing | Greg |
| 16 | `physics_rare`: resubmit the rare_v arm for the 9 missing VerSe series (2 of the 6 T13 scans among them); `physics_drr`: add CTSP 0721, 0919 and 1020 (lost to an unwritten `--min-levels 2` rule) and the VerSe and implant people lost to crashes (282 of 374 and 558 of 799 covered) | 1,482 + 9 series; the three CTSP ids present; a written rule for `--min-levels` | B10/B11 if the banks have moved | engineering |
| 17 | `implant_ts`: finish the 355 subjects never processed (`tools/make_implant_ct.py`, resume guard) or record the decision not to; `implant_verse` (187 GB) is regenerable and a deletion candidate | a count of subjects processed, or Greg's decision | B07 | Greg for deletion, engineering for the run |
| 18 | `anchor_drr`: fix the split seed to `cid.split('_v')[0]` before any reuse (301 of 801 people on both sides); never quote a number scored on it until then | the leak check passes on the rebuilt split | nothing | engineering |

## Migration (project 10 owns the batches; this folder's banks)

| # | step | gate and number | depends on | decides |
|---|---|---|---|---|
| 19 | B07 (TotalSegmentator v2.0.1 82.0 GB, v3.0.0 89.8 GB, `implant_ts`, `ts_drr`, `ts_drr_v3`) was copying at 22:20 UTC on 2026-10-08 with no STATUS file; then cut over | `plan/runs/B07/STATUS` VERIFIED on every item | the running `dp_migrate` job | engineering |
| 20 | B10 (`ctsp_drr`, `ctsp_drr_film`, `exp3_*`, `physics_smoke`, `~/polypose`) and B11 (`physics_drr`, `physics_drr_film`, `physics_rare`, `physics_rare_film`, `cut_physics*`, `film_style_ds`) not started; every script that names a HOME bank keeps working through the symlink the cut-over leaves | STATUS VERIFIED; the v9 bank's `meta.json` roots still resolve | B04, B06, B07 landed | engineering; FINALIZE (deleting the `.pre-ceph` copies) is Greg's call per batch |
| 21 | `$RS/data/polypose` holds the venv, the sif, the HF DeepFluoro re-host and the cohort together (87.713 GB in the census); the cohort's own size and item count are not recorded until the census reports the subfolders | subfolder sizes in the census; a README.yaml per subfolder for the holding index | the census job | engineering |

## Support this folder owes other projects

| # | step | gate and number | depends on | decides |
|---|---|---|---|---|
| 22 | PAR-2 for project 05: projected morphometry at exact pose on the 802 v11 volumes; fifty records, lateral and AP, T12 to L4, as a two-hour smoke test on `reqp` with job ids and ETA written to the resume file; then all 802 and the arc | per-feature ICC tiers 0.75 and 0.50; junction AUC tiers 0.97 and 0.90 (RD section 6 rank 2) | PAR-1's feature list (project 05); the v11 tree on the grid (project 03); `tools/render_physics_drr.py` | engineering |
| 23 | COBRA Varian (225 cases): the geometry map was solved 2026-09-23 and the acceptance render is pending; without it the Varian Halcyon card has no real-frame test and COBRA stays at 145 of 692 cases in any bank | an acceptance render with the gantry geometry agreeing with the RTK file; then `realxray/cobra_varian` admitted through `tools/realxray_banks.json` | nothing | engineering |
| 24 | For project 01: when the hospital's C-arm make and model are known (not recorded), decide whether a card can be fitted from its own frames (needs paired CT and pose or a phantom) or whether the pooled design P detector is used uncarded | a card fitted on at least 40 frames with held-out R^2 above uncalibrated physics, or the written decision to go uncarded | project 01 S3 and S4 (the device and the sponsor) | Greg |

## Record-keeping (a read-only grid pass; nothing runs)

| # | step | gate and number | depends on | decides |
|---|---|---|---|---|
| 25 | In the next read-only grid pass (`ls` and `cat` of small files only, through `wsl -e bash -lc 'ssh grid ...'`): `cat ~/spine-detector/.git/HEAD` and the ref it names, and write the commit into `MANIFEST_CODE.md` section 5; `ls $RS/data/or_ready/devices` and write its eight entry names into `MANIFEST_GRID.md` section 2 (the project 10 listing of 2026-10-08 shows the count 8 and no names; the C-arm inventory's own `ls` named `surgio_b51_dr/raw`, `surgio_b51_dr/display` and `varian_halcyon`); `ls ~/spine-detector/runs/devcorpus` to settle 19 runs (C-arm inventory) against 21 arms (grid inventory) | the commit, the eight names and the run count written with the date of the listing | nothing | engineering |

## Do not do (refuted or ruled out; `STATUS.md` section 9)

CycleGAN, ADDA, CUT v3, SDXL img2img at any strength, a learned formation refiner, a bespoke CT warp, a render bank
keyed on identifier 29, any number from `anchor_drr`'s own split, any physics number measured before the bone-path
fix, any sweep number before `sweep_v3`, quoting `ts_drr` as held out from v9.
