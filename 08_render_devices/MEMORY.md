# MEMORY: the notes under memory/ and their status

Forty dated notes, copied from the redacted handoff copies (spinesurg-ct-nnunet 097933a, `HANDOFF/context/`,
copy time 2026-10-08 16:39, `docs/handoff/context_COPIED_AT.txt`), each with a header line carrying the status of
`docs/handoff/context_INDEX.md` verbatim. A note is a dated record from the session that did the work, not an
instruction; where a note and a result file or `docs/handoff/RESULTS_CATALOG.md` disagree, the file and the catalog
win. Status words: CURRENT, DATED (a state at its date), PARTLY SUPERSEDED, SUPERSEDED (replaced by the number
named), LEAKED (measured on a bank with a known leak), RECORD ONLY (history, not quotable), DORMANT.

Nineteen notes carry the family tag `render_devices` in the memory map (`../_plan/inventories/memory_and_handoff_map.tsv`,
column `project_families`: 19 `mem:` rows; the family tally of `memory_and_handoff_map.md` and `../_plan/PLAN.md`
section 3 project 08 both say 19). Eighteen of them are listed in section 1, as the map's section "03 render_devices"
lists them; the nineteenth, `morphology-deformation-feasibility`, is tagged `render_devices+all` and the map placed
it with the standing notes, so it sits in section 2. Twenty-one further notes are the standing rules and laptop traps
every project folder carries (tag `all`): section 2 holds 22 and the folder 40, and both counts, 18 and 19, are right
once that is said. Three memory notes were redacted on copy, one of them again in the fix pass of 2026-10-08, and two
standing notes had laptop paths rewritten as prefixes (`MANIFEST_LOCAL.md` section 3). Five Greg-only notes and the
six Beethoven notes are never copied; the U251 and LITT notes belong to another study.

## 1. The project's notes (18)

| note | one line | status (context_INDEX.md) | replacement or caveat |
|---|---|---|---|
| `acquisition-space-saturation` | the fluoroscopy plateau follows where frames sit in acquisition space, not N (tested 2026-09-25, Figure 5 b-d); the claim wording | CURRENT | the finding behind A11.1 and A11.5 |
| `deepfluoro-convention` | DeepFluoro file layout and projection convention (0.00 px reprojection); (z, y, x) volume; focal -5257.7 kept signed | CURRENT | |
| `device-sampling-audit` | the card clip saturates (95-98 % of the joint lost); the typicality gate; Cios kVp recoverable | CURRENT | open defect A12.6; the clip is still the default |
| `drr-row-spacing-defect` | A-P voxel size written as S-I row spacing; pre-sweep_v3 sweeps on the wrong field size | CURRENT | why only `sweep_v3` counts |
| `drr-to-fluoro-levers` | three measured levers for DRR to fluoroscopy; CycleGAN and ADDA refuted; the honest ceiling | CURRENT | what to build and what not to |
| `film-fluoro-boundary-not-transferable` | devices separate pairwise; film vs fluoroscopy does not transfer to an unseen corpus | CURRENT | the manifold finding (A13.4) |
| `fluorogen-synthetic` | SDXL + ControlNet + LoRA synthetic C-arm frames; img2img dead at every strength; CUT v2 is not a lever | DATED | the verdicts stand; its login-node download line is against rule 7 |
| `k-devices-one-network` | per-device parameter sets, styled renders, LODO; where the pipeline lives | CURRENT | the device pipeline map |
| `learned-formation-refuted-calibrate-instead` | CT to fluoroscopy formation calibrated on DeepFluoro; the first real-fluoro recall; the 2026-09-21 deliverables | CURRENT; redacted copy | a staff contact withheld by the handoff; two clinicians' names struck here; a staff member (the body-bequest contact) and a faculty member (the eProtocol template) named by role here (fix pass 2026-10-08); the IRB and grant drafts it names exist only in a scratchpad and as claude.ai artifacts |
| `oblique-angles-and-sweep-vision` | the detector must work at any angle; synthetic AP to lateral arcs; AR vision is preview only | CURRENT | the pose-pool rule and the case134 spin |
| `physics-three-defects-measured` | only the AEC defect changed an image; the display window hides the lateral spine | CURRENT | supersedes the causal claim of `sweep-physics-no-bone` |
| `polypose-decision` | morphology augmentation = PolyPose within published ROM; fused junctions zero motion | CURRENT | Greg's decision on synthesis (2026-09-23) |
| `polypose-generator-build` | where the generator lives; six traps | CURRENT | its "never pushed" is outdated on the laptop's evidence (`STATUS.md` section 8); `VALIDATION.{json,md}` still not written (G.6) |
| `pooled-vs-lodo-device-designs` | pooled and LODO both reported; the list builder refuses split subjects | CURRENT | design rule for device arms; only design P refuses |
| `sweep-physics-no-bone` | physics-perturbed sweeps rendered with no bone; fix `--paths2-only` | CURRENT | render-before-believing record; causal claim superseded by `physics-three-defects-measured` |
| `synthetic-real-ratio-evidence` | no DRR paper swept the ratio; adjacent sweeps flatten at 4:1-10:1 | CURRENT | the project's own ratio was never swept (A10.11; OQ A9) |
| `ts-sacrum-excludes-s1` | TotalSegmentator `sacrum` excludes S1; whole sacrum = union | CURRENT | the trap behind NeurIPS defect A (F.47) |
| `vf813-drops-c1-t9-use-raw-verse-for-whole-spine` | `~/vf_813` maps C1-T9 to ignore; read raw VerSeFusion for whole-spine work | CURRENT | render-source rule |

## 2. The standing rules and laptop traps every folder carries (22)

| note | one line | status (context_INDEX.md) | replacement or caveat |
|---|---|---|---|
| `bash-heredoc-backslashes` | heredocs collapse backslashes; write scripts with Write, run by path | CURRENT | |
| `ct-volumes-are-pir-not-ras` | volumes are (P, I, R) on disk; decide by reading the affine | CURRENT | |
| `data-directives-2026-09-23` | D1-D9: fix or justify every truncation; FluoroCap dropped; use all | CURRENT | |
| `figure-captions-terse` | captions short, argument in text; float spacing | CURRENT | |
| `fluorocap-repo-private` | spinesurg private since 2026-09-14; never push level-ID code public | CURRENT | |
| `grid-access` | login, project root, where CTs and labels lived, ITK-SNAP launch | PARTLY SUPERSEDED (alias; data paths, section 13 rows 3-4) | aliases now resolve (`wsl-for-network`, `windows-ssh-to-grid`); data moved to Ceph (`grid-ceph-volume-oschome`) |
| `grid-bash-4-2-quoting` | the grid runs bash 4.2.46: a quoted replacement in `${var/pat/"$new"}` keeps its quotes | CURRENT (new 2026-10-08) | write grid jobs for bash 4.2 |
| `grid-ceph-volume-oschome` | 20 TB Ceph volume, working tree, `df-ceph oschome` | CURRENT | the administrator's username replaced by role on copy |
| `grid-local-singularity-is-broken` | use the conda singularity + a pre-unpacked sandbox + a specific bind | CURRENT | |
| `key-patients-from-metadata-not-filenames` | identity order: DICOM, manifest, annotation fields, filename last | CURRENT | |
| `label-scheme-v4-vs-ostk` | two live maps; `labels_for(volume)`; what the mix-up cost | CURRENT | |
| `morphology-deformation-feasibility` | literature first; no bespoke CT warp | CURRENT | tagged `render_devices+all` in the map: the nineteenth render_devices note, carried here among the standing notes; the rule that led to the PolyPose decision |
| `never-reorient-when-writing-labels` | `as_closest_canonical` + `nib.save` transposes a label | CURRENT | |
| `no-jobs-on-login-node` | every computation via sbatch; compute nodes have internet; the C&IT addendum | CURRENT | |
| `no-unexplained-subsets-fix-not-disclose` | use all of a dataset; describe each in prose; fix leaks, do not disclose them | CURRENT | |
| `scratchpad-shadows-stdlib` | stdlib-named scratch scripts hijack Python | CURRENT | |
| `submit-and-sleep-orchestration` | submit, estimate, record, stop | CURRENT | |
| `user-affiliation-general-surgery` | General Surgery, not Neurosurgery | CURRENT | |
| `windows-junction-worktree-trap` | `git worktree remove` deletes junction targets | CURRENT | two laptop paths rewritten as prefixes on copy (`MANIFEST_LOCAL.md` section 3) |
| `writing-preferences` | the banned word; no fractional versions | CURRENT | the redacted copy (the live note spells the word) |
| `wsl-for-network` | network commands via WSL | CURRENT | one laptop path rewritten as a prefix on copy (`MANIFEST_LOCAL.md` section 3) |
| `wsu-library-access-cutoff` | WSU Libraries dropped DMC residents 2026-06-30 | CURRENT | a library contact e-mail withheld on copy |

## 3. Notes this project cites but does not carry (they live in the folder named)

`ts-bench-inside-v9-bank` (project 07 and 10: `ts_drr` is not held out from v9); `film-ncurve-ablation-result`
(project 07; SUPERSEDED reading: trust `READ.md`, 7 of 9 cells); `detection-is-the-binding-constraint`,
`carm-plateau-is-the-denominator`, `carmlspine-level-experiment`, `sweep-map-replaces-registration`,
`guided-acquisition-loop` (project 01); `panjabi-1991-page-892` (project 05; the Table 3 ranges the sampling
spec cites); `identity-audit-findings`, `split-leak-cross-naming`, `nhanes-double-inclusion`,
`grid-quota-and-deleted-banks`, `dataset813-image-links-are-container-paths`, `versefusion-t13-flag-wrong`
(project 10); `two-mechanisms-thesis`, `lstv-tltv-detection-goal`, `l6-sample-count-and-counting-decoder`
(project 02). Their statuses are in `docs/handoff/context_INDEX.md`.
