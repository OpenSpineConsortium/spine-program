# MANIFEST_LOCAL.md — what was copied into this folder, from where, and what was not

**This record is history, not a dependency.** The laptop paths below say where each copy came from on 2026-10-08 so the
lineage is auditable; nothing in this folder reads them, and a reader with only this folder, grid access and the
repositories in `MANIFEST_CODE.md` needs none of them. Laptop paths appear in this file only.

The sources: the public repository `CTSpinoPelvic1K` at 7ddfe38 (`assets/` tracked, `poster/` untracked), a loose
Desktop folder of logo renders, and `HANDOFF/` of the private repository `spinesurg-ct-nnunet` at 097933a (the eight
student-readable files and the redacted memory copies under `HANDOFF/context/`). The disposition rows this folder
executes are the twelve rows of `_plan/DISPOSITION.tsv` whose `project_folder` is `12_website_pacs_demo` (7 copy,
4 reference, 1 exclude).

## 1. Copied

Every file in this folder that was not authored for it. "Bytes" is the size of the copy; "state" says whether the copy
is byte-identical to its source or carries an edit listed in section 2.

| copy (this folder) | source (laptop, 2026-10-08) | bytes | state |
|---|---|---|---|
| `figures/logo/assets/osc_logo.py` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/assets/osc_logo.py` | 5,588 | byte-identical |
| `figures/logo/assets/osc_logo.svg` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/assets/osc_logo.svg` | 1,099 | byte-identical |
| `figures/logo/assets/osc_logo_1024.png` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/assets/osc_logo_1024.png` | 63,037 | byte-identical |
| `figures/logo/assets/osc_logo_256.png` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/assets/osc_logo_256.png` | 14,241 | byte-identical |
| `figures/logo/assets/osc_logo_40.png` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/assets/osc_logo_40.png` | 1,884 | byte-identical |
| `figures/logo/assets/osc_logo_512.png` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/assets/osc_logo_512.png` | 29,383 | byte-identical |
| `figures/logo/assets/osc_logo_64.png` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/assets/osc_logo_64.png` | 3,213 | byte-identical |
| `figures/logo/assets/osc_logo_preview.png` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/assets/osc_logo_preview.png` | 25,949 | byte-identical |
| `figures/logo/OpenSpineConsortium-logo/OpenSpineConsortium-logo-128.png` | `C:/Users/grego/OneDrive/Desktop/OpenSpineConsortium-logo/OpenSpineConsortium-logo-128.png` | 6,627 | byte-identical |
| `figures/logo/OpenSpineConsortium-logo/OpenSpineConsortium-logo-256.png` | `C:/Users/grego/OneDrive/Desktop/OpenSpineConsortium-logo/OpenSpineConsortium-logo-256.png` | 12,884 | byte-identical |
| `figures/logo/OpenSpineConsortium-logo/OpenSpineConsortium-logo-512-white.png` | `C:/Users/grego/OneDrive/Desktop/OpenSpineConsortium-logo/OpenSpineConsortium-logo-512-white.png` | 12,622 | byte-identical |
| `figures/logo/OpenSpineConsortium-logo/OpenSpineConsortium-logo-512.jpg` | `C:/Users/grego/OneDrive/Desktop/OpenSpineConsortium-logo/OpenSpineConsortium-logo-512.jpg` | 29,621 | byte-identical |
| `figures/logo/OpenSpineConsortium-logo/OpenSpineConsortium-logo-512.png` | `C:/Users/grego/OneDrive/Desktop/OpenSpineConsortium-logo/OpenSpineConsortium-logo-512.png` | 13,497 | byte-identical |
| `figures/logo/OpenSpineConsortium-logo/OpenSpineConsortium-logo-inverse-128.png` | `C:/Users/grego/OneDrive/Desktop/OpenSpineConsortium-logo/OpenSpineConsortium-logo-inverse-128.png` | 5,904 | byte-identical |
| `figures/logo/OpenSpineConsortium-logo/OpenSpineConsortium-logo-inverse-256.png` | `C:/Users/grego/OneDrive/Desktop/OpenSpineConsortium-logo/OpenSpineConsortium-logo-inverse-256.png` | 11,416 | byte-identical |
| `figures/logo/OpenSpineConsortium-logo/OpenSpineConsortium-logo-inverse-512-flat.png` | `C:/Users/grego/OneDrive/Desktop/OpenSpineConsortium-logo/OpenSpineConsortium-logo-inverse-512-flat.png` | 9,620 | byte-identical |
| `figures/logo/OpenSpineConsortium-logo/OpenSpineConsortium-logo-inverse-512.jpg` | `C:/Users/grego/OneDrive/Desktop/OpenSpineConsortium-logo/OpenSpineConsortium-logo-inverse-512.jpg` | 24,659 | byte-identical |
| `figures/logo/OpenSpineConsortium-logo/OpenSpineConsortium-logo-inverse-512.png` | `C:/Users/grego/OneDrive/Desktop/OpenSpineConsortium-logo/OpenSpineConsortium-logo-inverse-512.png` | 13,298 | byte-identical |
| `figures/visual_abstract/make_visual_abstract.py` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/poster/make_visual_abstract.py` | 16,429 | edited (section 2) |
| `figures/visual_abstract/ORIGINAL_center_Picture_6.png` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/poster/ORIGINAL_center_Picture_6.png` | 697,201 | byte-identical |
| `figures/visual_abstract/OSC_visual_abstract.pdf` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/poster/OSC_visual_abstract.pdf` | 734,374 | byte-identical |
| `figures/visual_abstract/OSC_visual_abstract.png` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/poster/OSC_visual_abstract.png` | 1,281,992 | byte-identical |
| `figures/visual_abstract/panels/0068_v5.png` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/poster/panels/0068_v5.png` | 418,402 | byte-identical |
| `figures/visual_abstract/panels/0068_v6.png` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/poster/panels/0068_v6.png` | 439,703 | byte-identical |
| `figures/visual_abstract/panels/0231_v4.png` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/poster/panels/0231_v4.png` | 614,169 | byte-identical |
| `figures/visual_abstract/panels/0231_v6.png` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/poster/panels/0231_v6.png` | 624,275 | byte-identical |
| `figures/visual_abstract/panels/markers.json` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/poster/panels/markers.json` | 839 | byte-identical |
| `figures/visual_abstract/panels/markers_0068.json` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/poster/panels/markers_0068.json` | 835 | byte-identical |
| `figures/visual_abstract/render_0068_panels.py` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/poster/render_0068_panels.py` | 4,277 | edited (section 2) |
| `figures/visual_abstract/render_0231_panels.py` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/poster/render_0231_panels.py` | 4,810 | edited (section 2) |
| `figures/visual_abstract/spine_qc.py` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/poster/spine_qc.py` | 1,203 | edited (section 2) |
| `figures/visual_abstract/spine_qc_0068.py` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/poster/spine_qc_0068.py` | 1,265 | edited (section 2) |
| `docs/handoff/DATASET_USAGE.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/DATASET_USAGE.md` | 37,254 | byte-identical |
| `docs/handoff/GLOSSARY.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/GLOSSARY.md` | 25,368 | byte-identical |
| `docs/handoff/INFRASTRUCTURE.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/INFRASTRUCTURE.md` | 48,552 | edited (section 2) |
| `docs/handoff/LEAKAGE.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/LEAKAGE.md` | 25,299 | byte-identical |
| `docs/handoff/OPEN_QUESTIONS.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/OPEN_QUESTIONS.md` | 28,544 | edited (section 2) |
| `docs/handoff/README.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/README.md` | 42,406 | edited (section 2) |
| `docs/handoff/RECIPES.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/RECIPES.md` | 73,560 | edited (section 2) |
| `docs/handoff/RESULTS_CATALOG.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/RESULTS_CATALOG.md` | 110,286 | edited (section 2) |
| `memory/bash-heredoc-backslashes.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/bash-heredoc-backslashes.md` | 1,495 | edited (section 2) |
| `memory/ct-volumes-are-pir-not-ras.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/ct-volumes-are-pir-not-ras.md` | 2,489 | edited (section 2) |
| `memory/data-directives-2026-09-23.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/data-directives-2026-09-23.md` | 2,621 | edited (section 2) |
| `memory/engine-swap-architecture.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/engine-swap-architecture.md` | 2,154 | edited (section 2) |
| `memory/figure-captions-terse.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/figure-captions-terse.md` | 1,760 | edited (section 2) |
| `memory/fluorocap-repo-private.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/fluorocap-repo-private.md` | 1,906 | edited (section 2) |
| `memory/grid-access.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-access.md` | 1,996 | edited (section 2) |
| `memory/grid-bash-4-2-quoting.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-bash-4-2-quoting.md` | 1,880 | edited (section 2) |
| `memory/grid-ceph-volume-oschome.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-ceph-volume-oschome.md` | 1,777 | edited (section 2) |
| `memory/grid-local-singularity-is-broken.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-local-singularity-is-broken.md` | 2,938 | edited (section 2) |
| `memory/hf-identity.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/hf-identity.md` | 1,154 | edited (section 2) |
| `memory/key-patients-from-metadata-not-filenames.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/key-patients-from-metadata-not-filenames.md` | 2,661 | edited (section 2) |
| `memory/label-scheme-v4-vs-ostk.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/label-scheme-v4-vs-ostk.md` | 2,908 | edited (section 2) |
| `memory/level-service-serving.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/level-service-serving.md` | 3,500 | edited (section 2) |
| `memory/morphology-deformation-feasibility.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/morphology-deformation-feasibility.md` | 2,763 | edited (section 2) |
| `memory/never-reorient-when-writing-labels.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/never-reorient-when-writing-labels.md` | 2,388 | edited (section 2) |
| `memory/no-jobs-on-login-node.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/no-jobs-on-login-node.md` | 2,631 | edited (section 2) |
| `memory/no-unexplained-subsets-fix-not-disclose.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/no-unexplained-subsets-fix-not-disclose.md` | 2,598 | edited (section 2) |
| `memory/pacs-demo-and-ostk-params.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/pacs-demo-and-ostk-params.md` | 2,477 | edited (section 2) |
| `memory/pacs-website-latency-root-cause.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/pacs-website-latency-root-cause.md` | 2,123 | edited (section 2) |
| `memory/scratchpad-shadows-stdlib.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/scratchpad-shadows-stdlib.md` | 1,851 | edited (section 2) |
| `memory/submit-and-sleep-orchestration.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/submit-and-sleep-orchestration.md` | 2,380 | edited (section 2) |
| `memory/user-affiliation-general-surgery.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/user-affiliation-general-surgery.md` | 2,010 | edited (section 2) |
| `memory/windows-junction-worktree-trap.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/windows-junction-worktree-trap.md` | 1,966 | edited (section 2) |
| `memory/writing-preferences.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/writing-preferences.md` | 1,326 | edited (section 2) |
| `memory/wsl-for-network.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/wsl-for-network.md` | 1,904 | edited (section 2) |
| `memory/wsu-library-access-cutoff.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/wsu-library-access-cutoff.md` | 1,965 | edited (section 2) |
| `docs/handoff/EXTRACT_MANUSCRIPTS_12.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/MANUSCRIPTS.md` (section 12 and section 21 item 7 only) | 1,910 | extract (section 2) |

67 files copied, 5,575,206 bytes in the copies (sizes read 2026-10-08 after the edits of section 2), plus the one extract.

## 2. Edits and redactions, by kind

| kind | where | what was done |
|---|---|---|
| laptop paths replaced by markers | `docs/handoff/README.md` (8 substitutions: 6 Desktop paths, the memory folder, the vendor folder), `docs/handoff/RECIPES.md` (3: the WSL mount path at line 29; the Desktop root at line 77, first to `<laptop home>/OneDrive/Desktop` and then reduced to `<laptop Desktop>` so no Windows folder name remains), `docs/handoff/RESULTS_CATALOG.md` (5: the three prefix definitions at lines 12-14; the F.48 scratchpad path at line 637, first its drive prefix and then the whole path reduced to `<laptop Temp scratchpad, swept>/neurips_fixes/cr_apply/`), `docs/handoff/INFRASTRUCTURE.md` (3 paths: lines 5, 114, 380); 19 substitutions in the four handoff files, the same counts as `docs/handoff/ABOUT_THESE_COPIES.md`; `memory/pacs-demo-and-ostk-params.md` (1), `memory/windows-junction-worktree-trap.md` (2), `memory/wsl-for-network.md` (1) | the absolute paths became `<laptop Desktop>/`, `<laptop home>/`, `<laptop memory folder>/`, `<laptop vendor folder, never read>`, `<laptop Temp scratchpad, swept>/` so that no text in this folder depends on a laptop; `docs/handoff/ABOUT_THESE_COPIES.md` says how the prefixes resolve to repositories |
| one staff username replaced by a role | `docs/handoff/INFRASTRUCTURE.md` section 2 (one occurrence), `memory/grid-ceph-volume-oschome.md` (one occurrence) | a C&IT administrator's AccessID became "a C&IT administrator" |
| another study's examples replaced by placeholders | `memory/grid-local-singularity-is-broken.md` | the job ids, the sandbox path and the R-library path of another study became generic placeholders; the rule the note states is unchanged |
| a CV reference reworded | `docs/handoff/EXTRACT_MANUSCRIPTS_12.md` (1), `docs/handoff/OPEN_QUESTIONS.md` (3, row A1: two phrases in the question and consequence columns, and the file column, which named a CV file inside an application folder and now reads "a CV in an application folder (laptop only, never copied)"), `docs/handoff/README.md` (1, section 7), `docs/handoff/RECIPES.md` (1, a laptop-only folder name) | phrases that cited a CV through its application system now say "a CV" or "an application folder"; application material is never copied or named (a grep of this folder for the application system's name returns nothing, 2026-10-08); the handoff copies name another study only in lines that say it is a different project and not part of the handoff, which stay |
| one laptop-path line patched, origin header added | `figures/visual_abstract/render_0068_panels.py`, `render_0231_panels.py` (the `SCHEME = Path(...)` line now reads `itksnap_v6_labels.txt` from beside the script, with the grid path in a comment), `spine_qc.py`, `spine_qc_0068.py` (`sys.path.insert` now names the repository's `scripts/` folder); `make_visual_abstract.py` (header only, no other change) | each edited line is marked `spine-program edit`; each script begins with a three-line origin header |
| one-line status header prepended | every file in `memory/` | the status from `HANDOFF/context/INDEX.md`, the source copy, and the rule that a note is a record, not an instruction |
| section extracted from a Greg-only file | `docs/handoff/EXTRACT_MANUSCRIPTS_12.md` | section 12 of `HANDOFF/MANUSCRIPTS.md` and item 7 of its section 21, verbatim apart from the two substitutions above |

Nothing was redacted in the figure files: the logo and poster files carry no name, address or username (checked by
grep on 2026-10-08), and the poster scripts' docstrings name cases by id only.

## 3. Not copied, and why

| source (laptop, 2026-10-08) | why not, and where it is instead |
|---|---|
| `C:/Users/grego/OneDrive/Desktop/googlec3911e7fb095977e.html` (53 B) | the disposition's one `exclude` row for this folder (desktop inventory r112): a Google site-verification token; the tracked copy in the site repository is the record and is never edited |
| `C:/Users/grego/OneDrive/Desktop/openspineconsortium.github.io/` (the clone, 127 MB, 449 files) | a repository: referenced in `MANIFEST_CODE.md` section 1 with URL, branch, commit and the files that matter (disposition rows inv3 r59 and carm r63) |
| `.../openspineconsortium.github.io/pacs/testimgs/` (8 BUU films), `pacs/webtest/` (2 cervical JPGs), `pacs/sllp/` (4 figure JPGs and `out/`), `headshots/*.jpg.orig` | untracked radiographs and originals in the clone: never copied anywhere, never added to the site (`TODO.md` step 2) |
| `.../openspineconsortium.github.io/contributions/manifest.json`, `headshots/` | student and contributor names and portraits, public on the site by design; not copied into this seed (by reference, `MANIFEST_CODE.md`) |
| `.../openspineconsortium.github.io/pacs/data/0003/*.nii.gz`, `gallery/data/*.bin` | imaging data and meshes, in the repository; by reference |
| `.../openspineconsortium.github.io/MANS_Schwing.pptx` (12.2 MB), `LA_QUINTA_VIDEO.mp4` (21.2 MB), `BATON_ROUGE_VIDEO.mp4` (7.8 MB) and the conference images | in the repository; by reference |
| `C:/Users/grego/OneDrive/Desktop/AI_Imaging_Workshop.pdf` and `.docx`, `CTSpinoPelvic1K-1/AI_Imaging_Workshop.pdf`, `CTSpinoPelvic1K-1/mlhc/AI_Imaging_Workshop.pdf` | the workshop agenda; a near-identical copy (90,116 B) is tracked in the site; routed to `11_students_grid_access` by reference (desktop inventory r14, r15; `_plan/DISPOSITION.tsv`) |
| `C:/Users/grego/OneDrive/Desktop/cureus.pdf`; `CTSpinoPelvic1K-1/Med_Ed_CNS.pptx`, `Med_Ed_CNS_visual_abstract.pptx`, `OSC MedEd Manuscript - JEEHP.docx` | the medical-education paper, its decks and the JEEHP draft: routed to `11_students_grid_access` (`manuscripts/`, `manuscripts/talks/`; disposition rows desk r5, ctsp r95); this folder holds the visual abstract's source only |
| `C:/Users/grego/OneDrive/Desktop/openspineconsortium.github.io/atlas/level_atlas.csv` and `CTSpinoPelvic1K-1/morphometrics/level_atlas.csv` | the atlas is `05_ct_morphometry_parity`'s (disposition row inv3 r60, by reference); the site copy is in the repository |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/data/itksnap_v6_labels.txt` (3,713 B, 2026-09-03, untracked) | a dataset artefact owned by `03_ctspinopelvic1k_dataset`; the grid copy at `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/itksnap_v6_labels.txt` is 5,421 B (2026-08-27): which the poster run used is not recorded |
| the volumes the poster scripts read (`0231_ct.nii.gz`, `0231_label_v4.nii.gz`, `0231_label_v6.nii.gz`, `0068_ct.nii.gz`, `0068_label_v5.nii.gz`, `0068_label_v6.nii.gz`) | imaging data; not found beside the scripts on 2026-10-08; where those review revisions live today is not recorded |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/MANUSCRIPTS.md` (whole), `CONTEXT_EXPORT.md`, `RESEARCH_DIRECTIONS.md`, `LITERATURE_STATE.md`, `literature_state/`, `working_notes/`, `GREG_ONLY/` | Greg-only handoff material (`_plan/PLAN.md` section 2 rule 3); this student-safe folder carries one section as an extract |
| `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/` (the live notes and `MEMORY.md`) | the redacted `HANDOFF/context/` copies were used instead; the live index is never copied; the Greg-only, Beethoven, other-study and history-only notes are never copied into a student-safe folder |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/service/`, `tools/deploy_service.py` | level-identification code in the private repository: by reference only (`MANIFEST_CODE.md` section 3) |
| `/wsu/home/go/go24/go2432/level_id_service/weights/` and the Hugging Face weights repositories | model weights: never copied (`MANIFEST_GRID.md`, `MANIFEST_CODE.md` section 7) |

## 4. Skipped by the copy rules

None. The three copied folders held no file over 25 MB, no imaging data, no archive, no log and no credential-like name
(the copy script checked each file; 0 skips). The largest copy is `figures/visual_abstract/OSC_visual_abstract.png`,
1,281,992 B.


## Final pass of 2026-10-08 (after the critic's check of the whole tree)

Rows added by the final pass; the sections above are the first build and the verifier's fix pass as they were. Sources are laptop paths of 2026-10-08 (history, not dependencies). sha1 is the first 16 hex digits of the copy.

### Shared copies, recorded as such

9 files of `figures/visual_abstract/` also sit, byte for byte, under `../03_ctspinopelvic1k_dataset/code/case_fixes/_verify_0816/va/` (03 lists them in its final-pass section); this folder is the owner of the visual abstract.

### Redaction made the same in every folder

The one Hugging Face handle quoted beside a published co-author's name was withheld in some folders and kept in others for the same source line (the critic's finding). It now reads `(HF username withheld)` everywhere (one occurrence per file below); the person's name stays (a person, never renamed). Greg may restore it; it is his decision (PLAN.md section 5).

- `docs/handoff/RECIPES.md`

### E-mail address withheld

`memory/wsu-library-access-cutoff.md`: the library contact address replaced by `[library e-mail withheld]` (the library's public phone numbers kept), the same as 08's copy already read.
