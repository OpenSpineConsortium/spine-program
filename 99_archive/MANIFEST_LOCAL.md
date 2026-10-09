# MANIFEST_LOCAL for 99_archive

**This record is history, not a dependency.** The laptop paths below say where each copy came from on 2026-10-08.
Nothing in this folder depends on a laptop path; the only outside references of this folder are grid paths
(`MANIFEST_GRID.md`) and code repositories at stated commits (`MANIFEST_CODE.md`). Copied historical documents carry the
prefix keys of their day (`ssn:`, `ctsp:`, `mem:`, `Desktop/`), which `docs/handoff/PREFIX_KEY.md` resolves to the
repositories in `MANIFEST_CODE.md` and to grid paths; full laptop roots remain only inside the eight unedited HANDOFF copies
(listed in section 3), and the checkpoints and memory notes carry `[laptop ... of the day]` tokens or the `Desktop/` key
where a laptop root stood. Row ids such as `ssn r110`, `carm r30`, `ctsp r13`, `desk r40`, `inv3 r87`, `mem r88` and
`grid r84` are rows of `../_plan/DISPOSITION.tsv` and of the seven inventory TSVs in `../_plan/inventories/` (row N = TSV
row N counted from 1 after the header).

Copy rules applied (`spine-program/_plan/PLAN.md` section 2 rule 6): nothing over 25 MB, no imaging data, weights, `.git`,
environments, caches, logs over 2 MB, credentials or personal material; symlinks and junctions never followed; every
copy and every refusal recorded. Result: 79 files, 7,223,620 bytes, nothing refused by the size or kind rules. Every
file in the copy table was checked for the banned word after copy (none remains) and for e-mail addresses, usernames and
student names (the redactions column), and re-checked in the fix pass of the same day for e-mail addresses, telephone
patterns, street addresses, postal codes, citizenship statements and laptop roots (section 3).

## 1. Files copied (source path as it was on 2026-10-08; commit where tracked; redactions by kind, never by value)

| destination in this folder | source path on 2026-10-08 | commit | bytes (copy) | redactions and notes |
|---|---|---|---|---|
| `code/fuc/ULTIMATE_EXPLANATION_FOR_LLM.md` | `C:\Users\grego\OneDrive\Desktop\FUC\ULTIMATE_EXPLANATION_FOR_LLM.md` | not a repository | 10,299 | none. inv3 r87: a 2026-02-14 DICOM dual-view crosshair bug note |
| `code/fuc/viewer_dual_ACTUALLY_FIXED.js` | `C:\Users\grego\OneDrive\Desktop\FUC\viewer_dual_ACTUALLY_FIXED.js` | not a repository | 30,705 | none. inv3 r87: the fixed viewer JS, 30,705 B |
| `docs/checkpoints/DAILY_REPORT_2026-09-22.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\docs\DAILY_REPORT_2026-09-22.md` | 9f2af48 (tree 097933a) | 4,190 | none. ssn r110 / carm r111 |
| `docs/checkpoints/FLUOROCAP_MORNING_2026-09-14.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\docs\FLUOROCAP_MORNING_2026-09-14.md` | 0439616 (tree 097933a) | 17,857 | none. ssn r110 / carm r110: the dated FluoroCap overnight report |
| `docs/checkpoints/HANDOFF_2026-09-21_PM.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\docs\HANDOFF_2026-09-21_PM.md` | fb14892 (tree 097933a) | 66,554 | four researcher e-mail addresses withheld (4); one laptop session path tokenised (1) (fix pass). carm r30 / ssn r110: the C-ArmLSpine entry document and the OR-readiness adversarial programme; 66,295 B |
| `docs/checkpoints/HANDOFF_2026-09-21_PM_ctsp_audit_track.md` | `C:\Users\grego\OneDrive\Desktop\CTSpinoPelvic1K-1\docs\HANDOFF_2026-09-21_PM.md` | untracked 2026-10-08 | 1,551 | none. ctsp r13: the 2026-09-22 05:30 audit-track block (1,551 B); a different file from the spinesurg one (md5 812a2a00 vs babaa09c), so both are kept |
| `docs/checkpoints/MORNING_BRIEF_2026-09-16.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\docs\MORNING_BRIEF_2026-09-16.md` | 6984446 (tree 097933a) | 10,550 | none. ssn r110 / carm r111 |
| `docs/checkpoints/RESUME_2026-09-22.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\docs\RESUME_2026-09-22.md` | 9f2af48 (tree 097933a) | 4,526 | none. ssn r110 / carm r111 |
| `docs/checkpoints/RESUME_2026-09-22_PM.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\docs\RESUME_2026-09-22_PM.md` | 465bec6 (tree 097933a) | 365,793 | banned word rewritten (2); Greg's e-mail withheld (1); HF username withheld (1); three first names struck (a collaborator; fix pass: a TTO officer, a deck recipient); fix pass: the personal data of line 351 withheld (home address, telephone, citizenship, inventorship, employment-agreement reading), PhysioNet username withheld (1), laptop roots tokenised (section 3). carm r31 / ssn r109: the last session checkpoint, 2026-09-22 to 2026-09-27, 366,958 B |
| `docs/early_scratch_2026-05/EXAMPLE_CASTELVII_4.jpg` | `C:\Users\grego\OneDrive\Desktop\NextPaper\EXAMPLE_CASTELVII_4.jpg` | not a repository | 214,305 | none. inv3 r30: one coronal CT render with a label overlay, called a Castellvi IV example by its name; no identifier on it (`docs/early_scratch_2026-05/README.md`), 214,305 B |
| `docs/early_scratch_2026-05/Image20260517150105.png` | `C:\Users\grego\OneDrive\Desktop\NextPaper\Image20260517150105.png` | not a repository | 354,877 | none. inv3 r30: a render of 2026-05-17 (sagittal CT slice with per-level wedge angles; on-image id "token 408"; `docs/early_scratch_2026-05/README.md`), 354,877 B |
| `docs/early_scratch_2026-05/action_items.txt` | `C:\Users\grego\OneDrive\Desktop\NextPaper\action_items.txt` | not a repository | 4,227 | first name struck (1); first name struck (1). inv3 r6: fifteen-step plan of 2026-05-15 around the 45 VerSe L6 cases and the NeurIPS merge; superseded by the v10/v11 build |
| `docs/early_scratch_2026-05/meeting_agenda.docx` | `C:\Users\grego\OneDrive\Desktop\NextPaper\meeting_agenda.docx` | not a repository | 14,146 | none. inv3 r30: 2026-05 lab meeting agenda (student show-and-tell as Student 1-4, the Moeller naming discussion); no student names inside |
| `docs/early_scratch_2026-05/newplot.png` | `C:\Users\grego\OneDrive\Desktop\NextPaper\newplot.png` | not a repository | 170,643 | none. inv3 r30: a render of 2026-05-31 (Plotly 3-D segmentation mesh; on-image case id 413910863, dataset not recorded; `docs/early_scratch_2026-05/README.md`), 170,643 B |
| `docs/fluorocap/FLUOROCAP_PROTOCOL.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\docs\FLUOROCAP_PROTOCOL.md` | a6e36b3 (tree 097933a) | 13,347 | none. ssn r114 / carm r110 |
| `docs/fluorocap/FLUOROCAP_QC_2026-09-14.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\docs\FLUOROCAP_QC_2026-09-14.md` | 351808c (tree 097933a) | 12,646 | none. ssn r114 / carm r110 |
| `docs/fluorocap/FLUOROCAP_README.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\docs\FLUOROCAP_README.md` | 116b6ef (tree 097933a) | 4,242 | none. ssn r114 / carm r110 |
| `docs/fluorocap/PATHOLOGY_SOURCE_SWEEP_2026-09-14.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\docs\PATHOLOGY_SOURCE_SWEEP_2026-09-14.md` | b1469ae (tree 097933a) | 452,578 | named vendor contact address withheld (1); named society contact address withheld (1) (fix pass; the same replacement as the JSON twin). ssn r114 / carm r110: 366 sources, 534 queries; 454,660 B |
| `docs/fluorocap/pathology_source_sweep_2026-09-14.json` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\docs\pathology_source_sweep_2026-09-14.json` | b1469ae (tree 097933a) | 1,334,714 | named vendor contact withheld (1); named society contact withheld (1); banned word rewritten as origin (2). ssn r114: the machine form of the sweep, 1,345,233 B (the row's name PATHOLOGY_SOURCE_SWEEP_2026-09-14.json does not exist; this is the file) |
| `docs/handoff/DATASET_USAGE.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\DATASET_USAGE.md` | 097933a | 37,254 | none. PLAN.md section 2 rule 3: the eight student-readable HANDOFF files are copied whole into every folder |
| `docs/handoff/GLOSSARY.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\GLOSSARY.md` | 097933a | 25,368 | none. PLAN.md section 2 rule 3: the eight student-readable HANDOFF files are copied whole into every folder |
| `docs/handoff/INFRASTRUCTURE.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\INFRASTRUCTURE.md` | 097933a | 48,550 | none. PLAN.md section 2 rule 3: the eight student-readable HANDOFF files are copied whole into every folder |
| `docs/handoff/LEAKAGE.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\LEAKAGE.md` | 097933a | 25,299 | none. PLAN.md section 2 rule 3: the eight student-readable HANDOFF files are copied whole into every folder |
| `docs/handoff/OPEN_QUESTIONS.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\OPEN_QUESTIONS.md` | 097933a | 28,532 | none. PLAN.md section 2 rule 3: the eight student-readable HANDOFF files are copied whole into every folder |
| `docs/handoff/README.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\README.md` | 097933a | 42,567 | none. PLAN.md section 2 rule 3: the eight student-readable HANDOFF files are copied whole into every folder |
| `docs/handoff/RECIPES.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\RECIPES.md` | 097933a | 73,585 | none. PLAN.md section 2 rule 3: the eight student-readable HANDOFF files are copied whole into every folder |
| `docs/handoff/RESULTS_CATALOG.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\RESULTS_CATALOG.md` | 097933a | 110,438 | none. PLAN.md section 2 rule 3: the eight student-readable HANDOFF files are copied whole into every folder |
| `docs/mans_talk/Deck_Outline.html` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Deck_Outline.html` | not a repository | 45,814 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/Deck_Outline.md` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Deck_Outline.md` | not a repository | 24,815 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/Field_Guide.html` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Field_Guide.html` | not a repository | 110,677 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/Field_Guide.md` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Field_Guide.md` | not a repository | 79,074 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/Image_Catalogue.html` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Image_Catalogue.html` | not a repository | 17,501 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/MRI_Sequences_Figure.html` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\MRI_Sequences_Figure.html` | not a repository | 14,912 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/Neuroradiology_Anatomic_Checkpoints.html` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Neuroradiology_Anatomic_Checkpoints.html` | not a repository | 31,877 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/Neuroradiology_Cord_Compression.html` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Neuroradiology_Cord_Compression.html` | not a repository | 50,738 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/Neuroradiology_Lumbar_Stenosis.html` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Neuroradiology_Lumbar_Stenosis.html` | not a repository | 49,241 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/Neuroradiology_Nerve_Root_Foramen.html` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Neuroradiology_Nerve_Root_Foramen.html` | not a repository | 39,810 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/Outline.txt` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Outline.txt` | not a repository | 20,475 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/Outline_for_MANS_Talk.docx` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Outline for MANS Talk.docx` | not a repository | 15,562 | none. ctsp r136: the docx outline (15,562 B) |
| `docs/mans_talk/PERMISSIONS.html` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\PERMISSIONS.html` | not a repository | 22,974 | banned word rewritten (1). ctsp r136 |
| `docs/mans_talk/PERMISSIONS.md` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\PERMISSIONS.md` | not a repository | 7,497 | banned word rewritten (1). ctsp r136: figure-permission notes; publisher permission addresses are institutional and kept |
| `docs/mans_talk/Scope_and_Priorities.html` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Scope_and_Priorities.html` | not a repository | 26,569 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/Scope_and_Priorities.md` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Scope_and_Priorities.md` | not a repository | 15,923 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/Slides_Cord_Compression.html` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Slides_Cord_Compression.html` | not a repository | 40,014 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/Slides_Findings.html` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Slides_Findings.html` | not a repository | 20,999 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/Syllabus.html` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Syllabus.html` | not a repository | 28,748 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/Syllabus.md` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Syllabus.md` | not a repository | 19,501 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/Timeline_Figure.html` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\Timeline_Figure.html` | not a repository | 96,332 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/asia_radiopedia_resources.txt` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\asia_radiopedia_resources.txt` | not a repository | 315 | none. ctsp r136: August 2026 teaching-talk outline |
| `docs/mans_talk/style.css` | `C:\Users\grego\OneDrive\Desktop\MANS_Talk\style.css` | not a repository | 2,581 | none. ctsp r136: August 2026 teaching-talk outline |
| `manuscripts/talks/TechFair_LSTV_Schwing.pptx` | `C:\Users\grego\OneDrive\Desktop\CTSpinoPelvic1K-1\TechFair_LSTV_Schwing.pptx` | untracked 2026-10-08 | 2,861,510 | none. ctsp r94: AACA 2026 Tech Fair deck, 15 slides, 2,861,510 B, md5 7d7ccd86; byte-identical twins at the Desktop root and in NextPaper (desk r40, inv3 r28) are not copied |
| `memory/bash-heredoc-backslashes.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\bash-heredoc-backslashes.md` | 097933a | 1,304 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/cns-deck-v2-2026-09-25.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\cns-deck-v2-2026-09-25.md` | 097933a | 13,468 | `~/OneDrive/Desktop/` replaced by the `Desktop/` key (5); the deck recipient's first name struck as `[deck recipient]` (1) (fix pass). the archive cut list, `../_plan/inventories/memory_and_handoff_map.md` section "archive" |
| `memory/ct-volumes-are-pir-not-ras.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\ct-volumes-are-pir-not-ras.md` | 097933a | 2,296 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/data-directives-2026-09-23.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\data-directives-2026-09-23.md` | 097933a | 2,428 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/figure-captions-terse.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\figure-captions-terse.md` | 097933a | 1,572 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/fluoro-panel-gap-diagnosed.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\fluoro-panel-gap-diagnosed.md` | 097933a | 4,126 | none. the archive cut list, `../_plan/inventories/memory_and_handoff_map.md` section "archive" |
| `memory/fluorocap-dataset.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\fluorocap-dataset.md` | 097933a | 16,813 | none. the archive cut list, `../_plan/inventories/memory_and_handoff_map.md` section "archive" |
| `memory/fluorocap-prototype-and-lstv-arm.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\fluorocap-prototype-and-lstv-arm.md` | 097933a | 13,812 | none. the archive cut list, `../_plan/inventories/memory_and_handoff_map.md` section "archive" |
| `memory/fluorocap-repo-private.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\fluorocap-repo-private.md` | 097933a | 1,717 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/fluorogen-synthetic.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\fluorogen-synthetic.md` | 097933a | 4,496 | none. the archive cut list, `../_plan/inventories/memory_and_handoff_map.md` section "archive" |
| `memory/grid-access.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\grid-access.md` | 097933a | 1,703 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/grid-bash-4-2-quoting.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\grid-bash-4-2-quoting.md` | 097933a | 1,692 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/grid-ceph-volume-oschome.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\grid-ceph-volume-oschome.md` | 097933a | 1,578 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/grid-local-singularity-is-broken.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\grid-local-singularity-is-broken.md` | 097933a | 2,663 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/key-patients-from-metadata-not-filenames.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\key-patients-from-metadata-not-filenames.md` | 097933a | 2,454 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/label-scheme-v4-vs-ostk.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\label-scheme-v4-vs-ostk.md` | 097933a | 2,718 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/morphology-deformation-feasibility.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\morphology-deformation-feasibility.md` | 097933a | 2,562 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/never-reorient-when-writing-labels.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\never-reorient-when-writing-labels.md` | 097933a | 2,187 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/no-jobs-on-login-node.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\no-jobs-on-login-node.md` | 097933a | 2,443 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/no-unexplained-subsets-fix-not-disclose.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\no-unexplained-subsets-fix-not-disclose.md` | 097933a | 2,392 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/publication-roadmap.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\publication-roadmap.md` | 097933a | 4,397 | none. the archive cut list, `../_plan/inventories/memory_and_handoff_map.md` section "archive" |
| `memory/scratchpad-shadows-stdlib.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\scratchpad-shadows-stdlib.md` | 097933a | 1,659 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/submit-and-sleep-orchestration.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\submit-and-sleep-orchestration.md` | 097933a | 2,183 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/user-affiliation-general-surgery.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\user-affiliation-general-surgery.md` | 097933a | 1,811 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/windows-junction-worktree-trap.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\windows-junction-worktree-trap.md` | 097933a | 1,761 | one laptop path replaced by `Desktop/ashley/extension` (fix pass). the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/writing-preferences.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\writing-preferences.md` | 097933a | 1,083 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/wsl-for-network.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\wsl-for-network.md` | 097933a | 1,727 | the WSL mount of the laptop replaced by `/mnt/c/<laptop Desktop root>/CTSpinoPelvic1K-1` (fix pass). the 22 standing-rule notes (PLAN.md section 2 rule 2a) |
| `memory/wsu-library-access-cutoff.md` | `C:\Users\grego\OneDrive\Desktop\spinesurg-ct-nnunet\HANDOFF\context\wsu-library-access-cutoff.md` | 097933a | 1,773 | none. the 22 standing-rule notes (PLAN.md section 2 rule 2a) |

Total: 79 files, 7,223,620 bytes (recomputed after the fix pass). Byte counts are of the copies (after redaction); the source sizes of the redacted and tokenised text files differ from these by a few bytes to a few hundred bytes.

## 2. Valuable files NOT copied, with the reason (DISPOSITION rows with action reference or exclude)

### 2.1 Twins and byte-identical copies (one copy exists in this repository; recorded so nothing is lost)

| file | reason |
|---|---|
| `C:/Users/grego/OneDrive/Desktop/TechFair_LSTV_Schwing.pptx` and `C:/Users/grego/OneDrive/Desktop/NextPaper/TechFair_LSTV_Schwing.pptx` (2,861,510 B each) | byte-identical to the copy in `manuscripts/talks/` (md5 7d7ccd86 on all three; desk r40, inv3 r28) |
| `C:/Users/grego/OneDrive/Desktop/CNS2026_Schwing_SchwingNet_CNStemplate.pptx` (13,608,401 B, 2026-09-26) | byte-identical to `_v10.pptx` (md5 aa8df26fb2), which is copied into `01_carm_level_detection/manuscripts/talks/` (desk r4, r20); private, never public |
| `C:/Users/grego/OneDrive/Desktop/FUC.zip` (10,918 B, 2026-02-14) | the zip twin of `Desktop/FUC`, whose two files are copied into `code/fuc/` (desk r30) |
| `C:/Users/grego/OneDrive/Desktop/MDPA.pdf` (1,467,927 B, 2026-09-12) | superseded by `CTSpinoPelvic1K-1/MDPA.pdf` (2026-09-16) and by `Desktop/MDPA_FINAL.pdf` (962,263 B, 2026-09-21, the submission, owned by 03); desk r34 |

### 2.2 Superseded decks, manuscripts, builds and scaffolds kept by path

| file | reason |
|---|---|
| `C:/Users/grego/OneDrive/Desktop/CNS2026_Schwing_Spine_v2.pptx` (6,918,724 B, 2026-09-25, 21 slides) | v2 "results only" deck, superseded by v10 and v12; a same-size copy sits in `private_ip/TTO_package_2026-09-25/followup/` (desk r22) |
| `C:/Users/grego/OneDrive/Desktop/CNS2026_Schwing_SchwingNet.pptx` (10,972,555 B, 2026-09-25, 21 slides) | v3 "SchwingNet results only" deck before the CNS template; superseded by v10; discloses Part B; private (desk r19) |
| `C:/Users/grego/OneDrive/Desktop/CNS2026_Schwing_SchwingNet_CNStemplate_v9.pptx` (13,806,896 B, 2026-09-25) | v9 of the CNS-template deck, superseded by v10; private (desk r21) |
| `C:/Users/grego/OneDrive/Desktop/CNS2026_Schwing_NotAllSpines_public_v11.pptx` (6,181,487 B, 2026-09-26, 15 slides) | superseded the same day by v12 (6,945,073 B, 17 slides, copied into 03) (desk r18) |
| `C:/Users/grego/OneDrive/Desktop/GREG_PRES.pptx` (804,321 B, 2025-06-20, 6 slides) | a lumbar spinal stenosis teaching deck; clinical teaching, not research (desk r31) |
| `C:/Users/grego/OneDrive/Desktop/SPINAL_AVM.pptx` (3,720,980 B, 2025-06-20, 8 slides) | a spinal arteriovenous malformation teaching deck; clinical teaching, not research (desk r37) |
| `C:/Users/grego/OneDrive/Desktop/MANS_Talk/MANS_Schwing.pptx` (12,194,006 B) and `Degenerative Cervical Myelopathy Case.pptx` (1,105,967 B) | the August 2026 teaching talk itself and a clinical case deck; the row copies the md and html outlines only; the case deck may hold patient images and was not opened (ctsp r136) |
| `C:/Users/grego/OneDrive/Desktop/MANS_Talk/DCM_Review.pdf` and 19 further literature PDFs (cervical myelopathy, lumbar stenosis, foraminal stenosis grading; listed in `LITERATURE_BY_PATH.md` section 6) | third-party literature; copyright; by path |
| `C:/Users/grego/OneDrive/Desktop/MANS_Talk/MANS_Talk.code-workspace` (80 B), `figures/` (empty) | an editor file and an empty folder |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/MDPA.pdf` (2026-09-16), `MDPA_OL.zip` (2026-09-06), `GPTZero AI Scan - CTSpinoPelvic1K_single_column.docx.pdf` | earlier builds and an AI-scan report; superseded by `MDPA_FINAL.pdf` (ctsp r91; `EXCLUDED.md` section 6) |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K_overleaf/`, `CTSpinoPelvic1K_MDPA_overleaf/`, `CTSpinoPelvic1K_overleaf.zip`, `CTSpinoPelvic1K_MDPA_overleaf.zip`, `CTSpinoPelvic1K_arxiv.tar.gz`, `CTSpinoPelvic1K_submission/` | overleaf exports and source bundles of 2026-09-04 to 09-10, older and smaller than their `paper/mpda` and `dist/` counterparts; nothing unique (2,398 and 501 diff lines against the current tex; git history holds them) (ctsp r116, r117; desk r27, r28) |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/dist/` | build outputs of `make_submission.py`; regenerable (ctsp r65; owned by 03 as a reference) |
| spinesurg-ct-nnunet `SchwingNet/packet/`, `packet_cameraready/` (89 MB each), the 16 earlier `packet_build` PDFs | regenerable submission packets; the two 2026-09-27 PDFs are copied into 01 (carm r47; `EXCLUDED.md` section 6) |
| `C:/Users/grego/OneDrive/Desktop/new_repo/` and `new_repo.zip` (84,504 B, 2026-04-18) | the scaffold of spinesurg-ct-nnunet (README, Makefile, `download_dataset.py`, `spinesurg-ct.def`, the three docs); superseded by the private repository at L6_Class 097933a (ctsp r144, desk r141) |
| `C:/Users/grego/OneDrive/Desktop/CTSP1K_private/CTSpinoPelvic1K_prepurge_20260911.bundle` (97,808,303 B) | the full git history of the public repository before the 2026-09-11 purge of personal material; over 25 MB and holds purged personal material: reference only, never push, never copy (ctsp r111) |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K/` (the older clone, 4fb4a62, 2026-04-28) | an ancestor of 7ddfe38 in git (`EXCLUDED.md` section 6) |
| `C:/Users/grego/OneDrive/Desktop/AshleyBridge-6.0.0-tester-package.zip`, `Ashley Bridge for testers/` | superseded by Beethoven release 14.0.0; Beethoven is owned by 11 (`EXCLUDED.md` section 6) |
| spinesurg-ct-nnunet `paper/rsnai/web/index.html` (65,805 B) | a styled web rendering of the first C-arm draft; in the repository at 097933a (ssn r180) |
| spinesurg-ct-nnunet `paper/rsnai/` (`main.tex`, `main_v2.tex`, `claims.tex`, `refs.bib`, `graveyard.tex`, `figures/`) and `paper/focused/main.tex` | superseded drafts; copied once into `01_carm_level_detection/manuscripts/superseded/` (carm r57, r58); `main_v2.tex` says Neurosurgery |
| spinesurg-ct-nnunet `docs/RSNAI_PLAN.md`, `RSNAI_CLAIMS.json`, `FEASIBILITY_REPRODUCE.md`, `FLAGSHIP_PLAN.md` | superseded plans kept in 01 as history flagged superseded (carm r15, r16, r41) |
| spinesurg-ct-nnunet `docs/PATENT_PACKAGE.md` and the disclosure package | excluded from the whole repository (`EXCLUDED.md` section 4; carm r29) |
| spinesurg-ct-nnunet `docs/PIPELINE_RESUME.md`, `pipeline.md`, `troubleshooting.md` | copied into `01_carm_level_detection/docs/` (DISPOSITION line 1273); carm r111 names them as old notes; one copy in the repository |
| spinesurg-ct-nnunet `docs/ablations.md`, `xrsp1k_seg.md` | copied into `03_ctspinopelvic1k_dataset/docs/` (DISPOSITION line 1280) |
| spinesurg-ct-nnunet `LICENSE` (11,313 B), `NOTICE` (166 B), `.gitignore` (3,040 B), `.github/workflows/ci.yml` (964 B) | in the repository at 097933a (ssn r5, r6, r9, r11); nothing to copy |
| spinesurg-ct-nnunet `tools/fluorocap_*.py` (73), `tools/fluorocap.py`, `validate_sources.py`, the five `make_*` / `finetune_level_fluoro.py`, `hunt_*.py` (11), `slurm/fluorocap_*.sh` (12), `benchmark/data/fluorocap_v0.1/` (12 files) | dormant code and the frozen release record, in the repository at 097933a (ssn r143; `MANIFEST_CODE.md` section 1) |

### 2.3 Third-party literature and saved pages (by path; `LITERATURE_BY_PATH.md` carries the identifiers)

| file | reason |
|---|---|
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/` root: `COBRA.pdf`, `RIBSEG.pdf`, `TS_DS.pdf`, `PANJABI_1991_FULL.pdf`, `PANJABI_1991_FULL_fixed.pdf`, `panjabi_1976.pdf`, `Sun_2021_Phys._Med._Biol._66_175002.pdf`, `PG-Net_*.pdf`, `Development_and_Evaluation_of_a_Robotic_System_*.pdf`, `CaseReports_T12_hypoplastic_rib.pdf`, `AITR-2002-001.pdf`, `Protocols for Reproducible Machine Learning Research.pdf`, `Spine chapters.zip`, `AI_Imaging_Workshop.pdf`, `2D-3D-GS_UG.pdf`, `PIG/PIG_LEVELCHECK.pdf` | copyright; available from the publishers; cited by identifier from the bib files (ctsp r100) |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/MANUAL_REFS/` (`ACR.pdf`, `NASS.pdf`, `BENZEL_CH_1.pdf`, `KONIN_WALZ.pdf`, `VERIDAH.pdf`, `panjabi1991.pdf`, `panjabi1992.pdf`) | guideline and textbook sources for the manual reference checks of `paper/mpda/_schehr` (ctsp r101). **The folder also holds two Cerner `.ica` session files (2,119 B and 2,118 B): credential-like; never copied; Greg deletes them (`PLAN.md` section 6)** |
| `C:/Users/grego/OneDrive/Desktop/SpineSurg-CT/*.pdf` (the 2024-2025 segmentation and LSTV literature, the two editorial PDFs, the ML4H 2025 dataset paper, `fmed-12-1511487.pdf`, the pelvic-fragment challenge paper) and `SpineSurg-CT/irb/` (three WSU exempt / expedited guidance PDFs) | third-party literature and IRB guidance (ctsp r124) |
| `C:/Users/grego/OneDrive/Desktop/Panjabi_1976_JBJS_thoracic.pdf`, `STUMP_RIBS.pdf`, `venetti.pdf` (18,840,219 B), `ACQUIFER.pdf`, `ACQUIFER_2.pdf` | Desktop-root literature; by path |
| `C:/Users/grego/OneDrive/Desktop/nsurg/AACA/` literature (`LSTV Vertebrae Labeling Manual.pdf`, `Deep Learning for Automated Spinopelvic Parameter Measurement Fro.pdf`, `Bullspine.pdf`, the AACA 2023-2025 programmes, `EBM Starter Document_Jan2026.pdf`) | the AACA 2026 LSTV MRI project's reading; by path (`EXCLUDED.md` section 9); the rest of `nsurg/` is personal or another study |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/docs/ajnr.html` (5,387 B), `docs/ukb.html` (250,341 B), `docs/ids.txt` (36 B), `sp_978-3-030-00937-3_12.html` (3,038 B), `sp_978-3-030-87240-3_28.html` (3,038 B) | saved web pages (an AJNR page, a UK Biobank page, two Springer chapter pages) and a 36-byte id list; not copied (ctsp r14) |
| `C:/Users/grego/OneDrive/Desktop/2026 AACA_0377.jpg` in the CTSpinoPelvic1K-1 root (10,328,744 B, 2026-07-29) | the AACA 2026 abstract 0377 image; an image, not opened; by path (ctsp r98) |

### 2.4 Memory notes not copied

| note | reason |
|---|---|
| `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/overnight-2026-09-15-chains.md` (2,317 B) | RECORD ONLY history-only entry point; the markers it names are on the grid under `/wsu/home/go/go24/go2432/FluoroCap` (mem r88) |
| `.../memory/resume-2026-09-21-pm.md` (5,938 B) | RECORD ONLY; names a researcher and an e-mail (Balgrist); never copied unredacted; the document it points at is `docs/checkpoints/HANDOFF_2026-09-21_PM.md` (mem r105) |
| `.../memory/resume-2026-09-22.md` (4,605 B) | RECORD ONLY; `docs/checkpoints/RESUME_2026-09-22.md` holds the record (mem r106) |
| `.../memory/resume-2026-09-22-pm.md` (1,772 B) | RECORD ONLY; `docs/checkpoints/RESUME_2026-09-22_PM.md` holds the record (mem r107) |
| `.../memory/resume-2026-09-24.md` (2,119 B) | RECORD ONLY; history (mem r108) |
| `.../memory/resume-2026-09-26-handoff.md` (3,791 B) | RECORD ONLY; half U251 (another study); the spine half points at the resume file (mem r109) |
| `.../memory/MEMORY.md` (the live index) | Greg-only, never copied: its one-liners carry leaked numbers and link notes that were not copied |

### 2.5 Other items this folder's plan section names, kept out

| item | reason |
|---|---|
| `C:/Users/grego/OneDrive/Desktop/FluoroCap_reading/` (12 MB) and `FluoroCap_screening/` (13 MB) | 3 of 64 reading pages and 2 of 104 screening pages, HTML with embedded licence-bearing panel PNGs from the grid `~/FluoroCap/annotate`; partial and image-bearing; referenced from 02 (inv3 r57, carm r69) |
| spinesurg-ct-nnunet `HANDOFF/GREG_ONLY/` (`PRIVATE_STATE.md`, `context/`, `context_beethoven/`) | Greg-only: credential locations, personal and contact data, the commercial stance, the disclosure state (`EXCLUDED.md` section 4) |
| `/rs/rs_grp_oschome/go2432/data/rsna_2022_cspine/raw` | imaging data on the grid (`MANIFEST_GRID.md`) |
| `C:/Users/grego/OneDrive/Desktop/private_ip/` (incl. `TTO_package_2026-09-25/followup/` deck twins) | Greg's private records (`EXCLUDED.md` section 4) |

## 3. Redactions and edits, by kind (values never written here)

Two passes: the build of 2026-10-08 and the fix pass of the same day (verifier issues 1 to 4, 10 and 11). Every edit is
to a copy in this folder; no source was touched. Line numbers are those of the copies (no edit added or removed a line
in the checkpoints).

- `docs/checkpoints/RESUME_2026-09-22_PM.md`. Build pass: the two mentions of the banned word rewritten (both were
  statements of the rule itself); Greg's WSU e-mail address withheld (1); one Hugging Face username withheld (1); one
  collaborator's first name struck (1). Fix pass: Greg's citizenship statement, home street address with postal code,
  telephone number, inventorship statement and the reading of his employment agreement's intellectual-property terms
  replaced by one `[personal data withheld: ...]` token (line 351); Greg's PhysioNet username withheld (line 352); the
  TTO officer's first name struck as `[TTO officer]` (lines 286, 320, 347) and a deck recipient's first name as
  `[deck recipient]` (3 occurrences, lines 280, 282, 286), the same way as the first name struck in
  the build pass; 8 laptop session and transcript roots with session identifiers replaced by
  `[laptop session folder of the day]`, 2 scratchpad roots by `[laptop scratchpad of the day]`,
  1 laptop home path by `[laptop home of the day]`, `~/OneDrive/Desktop/` by the `Desktop/` key
  (5) and the session-directory tokens `C--Users-grego-OneDrive-Desktop-...` of the workflow
  tables by `Desktop--...` (22). Kept: the institutional office addresses of the WSU IRB and
  invention-disclosure offices (not personal); "Dr Tech" (a placeholder, not a name; OQ A18); a faculty sponsor's surname
  and the two resident co-authors (the public NeurIPS author list); relative `scratchpad/...` paths without a root (they
  name the session's temporary folder of the day, which is swept; nothing depends on them).
- `docs/checkpoints/HANDOFF_2026-09-21_PM.md` (fix pass): four researchers' e-mail addresses (the Balgrist, UCLA, Fudan
  and SJTU corresponding-author contacts; lines 176, 228, 229, 231) replaced by `[address withheld; <institution and
  paper or set>]`; one laptop session path with a session identifier (line 23) replaced by
  `[laptop session folder of the day]`. The build pass had recorded this file as naming no person; that was wrong.
- `docs/fluorocap/pathology_source_sweep_2026-09-14.json` (build pass) and `PATHOLOGY_SOURCE_SWEEP_2026-09-14.md` (fix
  pass; the build pass had left the Markdown twin unredacted and recorded it as "none"): the two named vendor and
  society contact addresses (lines 1254 and 1257 of the `.md`) replaced by `<domain> (named contact address withheld)`;
  the banned word rewritten as origin (2, JSON only; the `.md` had none). Kept: generic addresses (licence@, sales@,
  info@, editor@, support@, subscribe@), institutional telephone numbers and street addresses of organisations, and the
  vendor contact's name and title as published on the vendor's own page.
- `docs/mans_talk/PERMISSIONS.md` and `.html`: the banned word rewritten as origin (1 each); publisher permission
  addresses kept (institutional).
- `docs/early_scratch_2026-05/action_items.txt`: two collaborators' first names struck (inv3 r6).
- `memory/writing-preferences.md` is the redacted HANDOFF copy (788 B), not the live note (730 B), because the live note
  spells the banned word.
- Memory notes, fix pass: `memory/cns-deck-v2-2026-09-25.md`, `~/OneDrive/Desktop/` replaced by the `Desktop/` key (5) and the
  deck recipient's first name struck as `[deck recipient]` (line 18; the same person as in the checkpoint; the copy in
  `03_ctspinopelvic1k_dataset/memory/` still carries it);
  `memory/windows-junction-worktree-trap.md`, one laptop path replaced by `Desktop/ashley/extension`;
  `memory/wsl-for-network.md`, the WSL mount of the laptop replaced by `/mnt/c/<laptop Desktop root>/CTSpinoPelvic1K-1`
  (the recipe still reads: substitute the clone's path). The words "scratchpad" and "transcript" in
  `memory/bash-heredoc-backslashes.md`, `memory/fluorocap-prototype-and-lstv-arm.md`, `memory/scratchpad-shadows-stdlib.md`,
  `MEMORY.md`, `docs/checkpoints/RESUME_2026-09-22.md` and five lines of `HANDOFF_2026-09-21_PM.md` are not laptop paths
  and were left.
- The eight HANDOFF copies in `docs/handoff/` are unedited (PLAN.md section 2 rule 3: copied whole). The laptop roots
  they spell (`README.md` lines 34-42; `RESULTS_CATALOG.md` lines 12-14 and 637; `INFRASTRUCTURE.md` lines 5 and 114;
  `RECIPES.md` lines 29 and 76-77; `OPEN_QUESTIONS.md` lines 143 and 161) are history, keyed to repositories and grid
  paths by `docs/handoff/PREFIX_KEY.md`, written in the fix pass; one shared key for all thirteen folders is `TODO.md`
  step 16.
- `docs/early_scratch_2026-05/meeting_agenda.docx` names a collaborating researcher by surname and "Student 1-4" without
  names: copied as is; its title says "Neurosurgical Department Conference" (historical). The three images beside it
  are single renders with a numeric case id at most (`docs/early_scratch_2026-05/README.md`), not imaging data.
- Seen and kept on purpose, pending Greg's decision (verifier issue 11; none of the rules settles them): the C&IT
  administrator's AccessID (`docs/handoff/INFRASTRUCTURE.md` line 97; `memory/grid-ceph-volume-oschome.md` line 12); the
  co-PI's Hugging Face username (`docs/handoff/RECIPES.md` line 402; she is a person and a co-author); the two resident
  co-authors of the NeurIPS paper (`docs/handoff/README.md` line 343; `docs/checkpoints/RESUME_2026-09-22_PM.md` lines
  372 and 660; a public author list); Greg's grid account `go2432` and the public dataset URL that carries his Hugging
  Face username (`docs/handoff/INFRASTRUCTURE.md` line 403). None of the eleven annotator usernames or surnames appears
  anywhere in this folder (grep of 2026-10-08).

## 4. Affiliation notes on copies and references

The Tech Fair deck (`manuscripts/talks/TechFair_LSTV_Schwing.pptx`) title slide says "Department of Neurosurgery" and
"NIH F30 Fellow"; the superseded `paper/rsnai/main_v2.tex` (in 01) says Department of Neurosurgery; the QI protocol draft
(in 09) and the Balgrist request draft (in 01) say Neurosurgery (`docs/handoff/GREG_ONLY_SECTION_EXTRACTS.md`, C5). None is
edited; every new sentence here says General Surgery.


## Final pass of 2026-10-08 (after the critic's check of the whole tree)

Rows added by the final pass; the sections above are the first build and the verifier's fix pass as they were. Sources are laptop paths of 2026-10-08 (history, not dependencies). sha1 is the first 16 hex digits of the copy.

### Written, not copied: the presentations record

| file | source | what | redaction |
|---|---|---|---|
| `manuscripts/talks/PRESENTATIONS_RECORD_2026-08-17.md` | `<laptop:Desktop>/Schwing_Presentations.docx` (39,491 B, 2026-08-17; inventory 4 row r174 had classified it from its file name as application material and did not open it) | the dated list of the programme's talks and posters: venue, date, placing; the only file giving the Hickey symposium placings (first and third place, 2026-08-07) and the CNS 2026 abstract numbers beside their titles | an extract, not a copy: the four non-spine items left out; every student name struck to `[student]` / `[n students]`; Schwing G and Schehr A kept (a published co-author, a person) |

### Redaction made the same in every folder

The one Hugging Face handle quoted beside a published co-author's name was withheld in some folders and kept in others for the same source line (the critic's finding). It now reads `(HF username withheld)` everywhere (one occurrence per file below); the person's name stays (a person, never renamed). Greg may restore it; it is his decision (PLAN.md section 5).

- `docs/handoff/RECIPES.md`

### E-mail address withheld

`memory/wsu-library-access-cutoff.md`: the library contact address replaced by `[library e-mail withheld]` (the library's public phone numbers kept), the same as 08's copy already read.

### Laptop paths rewritten to markers (self-containment)

The critic's tree-wide scan still found laptop spellings in copied files of this folder outside `MANIFEST_LOCAL.md`. They are now the markers the other folders use: `<laptop:Desktop>` for the Desktop root that held every repository checkout (`<laptop:Desktop>/spinesurg-ct-nnunet` = spinesurg-ct-nnunet at 097933a, `<laptop:Desktop>/CTSpinoPelvic1K-1` = CTSpinoPelvic1K at 7ddfe38, `<laptop:Desktop>/OpenSpineToolkit` = OpenSpineToolkit at cb43197, `<laptop:Desktop>/XRaySpinoPelvic1K` = XRSpinoPelvic1K at 4f22935), `<laptop:Temp scratchpad>` for the swept session scratchpad (nothing there is a dependency), `<laptop memory folder>` for the live memory notes (copied redacted into `memory/`), `<laptop vendor folder, never read>` and `<laptop home>`. The marker is a spelling of where the file came from, not a path to resolve; the repository and commit are the dependency. Scripts among these copies (`.py`, `.sh`) hard-coded laptop roots and did not run anywhere else before this change either; they are records of how a document was built.

| file | laptop spellings rewritten | left |
|---|---:|---:|
| `docs/handoff/INFRASTRUCTURE.md` | 4 | 0 |
| `docs/handoff/README.md` | 14 | 0 |
| `docs/handoff/RECIPES.md` | 4 | 0 |
| `docs/handoff/RESULTS_CATALOG.md` | 8 | 0 |
| `memory/windows-junction-worktree-trap.md` | 1 | 0 |

### The TechFair deck: core properties emptied

`manuscripts/talks/TechFair_LSTV_Schwing.pptx` was re-written in place in the final pass with `docProps/core.xml` creator and lastModifiedBy emptied (they carried Greg's name, kept nowhere else in metadata for uniformity). The deck's slide text carries Greg's institutional address (a recorded keep: his own corresponding address) and no student name.
