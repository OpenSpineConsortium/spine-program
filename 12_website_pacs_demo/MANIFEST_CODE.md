# MANIFEST_CODE.md — the repositories this project works in or depends on

Everything that lives in a repository is referenced here, not copied. Commits are those read on 2026-10-08. "Files that
matter" are the ones a maintainer of the site opens; the rest of each tree is listed by the repository's own README.

## 1. The site: `OpenSpineConsortium/openspineconsortium.github.io` (public)

- URL `https://github.com/OpenSpineConsortium/openspineconsortium.github.io`; branch `master`; GitHub Pages from `/`;
  custom domain `openspineconsortium.com` (`CNAME`). First commit 4e49f5f on 2026-05-18; origin head a17ea39 (2026-10-07),
  221 commits (`git rev-list --count origin/master`, 2026-10-08).
- The clone this seed was read from was at **c1800f8 (2026-10-02), ten commits behind origin**. The ten (newest first):
  a17ea39 merge of PR #3; 22b77ce "Admin page: the grid token kept nowhere, the page's own dates for 90 s only"; 602486f
  "Admin page: the grid's token, made, saved as a file and withdrawn"; 6623191 merge of PR #2; 1b4b337 "Site rebuilt: the
  lab storage page, the admin section, and the products' current texts"; 7d89acf "Lab storage pages: the folder box
  follows the tick again after Back"; 32e8059 "Lab storage: 'All of the lab storage' on the request page and the admin
  page"; 9b7cd8a "Site build: the VS Code edition's texts may name its earlier product"; d07e809 merge of PR #1; 480545a
  "Lab storage, read only: the request page and the admin section". Pull before any edit (`TODO.md` step 1).
- 420 tracked files at c1800f8 (`git ls-files | wc -l`). No `.pt` or `.onnx` anywhere in the tree (`git ls-files '*.pt'
  '*.onnx'` returns nothing); the only `.bin` files are the 12 gallery meshes under `assets/gallery/` (874,636 to
  1,327,480 B; `git ls-files '*.bin'` at c1800f8, 2026-10-08; `gallery/data/` holds `distributions.json`, 1,368,004 B,
  and no mesh); the only `.nii.gz` are the four demo volumes of case 0003 (292,542 to 1,682,039 B; `git ls-files
  '*.nii.gz'`, same day). An earlier inventory said 13 meshes under `gallery/data/` and five volumes; both counts were
  wrong and are withdrawn. The history was rewritten on 2026-09-14 to remove a 121 MB ONNX (new head ea0086c then;
  `memory/level-service-serving.md`). The site `README.md` (lines 185-186) says the Beethoven 7.0.0 packages are still
  in history at 816e9c4; 816e9c4 is not an object in the clone on 2026-10-08 (`git cat-file -t`, checked on c1800f8 and
  origin/master a17ea39), so that claim is unverified.
- **Untracked in the clone, never to be added**: `pacs/testimgs/` (8 BUU films, not redistributable), `pacs/webtest/`
  (2 cervical JPGs), `pacs/sllp/` (4 figure JPGs and an `out` folder), `headshots/*.jpg.orig` (`git status`, 2026-10-08).

| file | role |
|---|---|
| `README.md` (17,525 B) | the publishing rules: rebuild once, push once; the 600 s HTML cache; `/ashley/` redirects and kept files; the body-fragment convention; Beethoven's two editions; local preview; deploy settings ("Enforce HTTPS") |
| `tools/build_site.py` (76,916 B) | the one build: `SITE` (the site map, the only place navigation is defined), `REDIRECTS`, `KEPT_FILES` (SHA-256 pinned), `MODULE_EDGES` (content hashes for ES-module imports such as `xr.js` to `infer.js` and `remote.js`), `BEETHOVEN_REPO` and `BEETHOVEN_VSCODE_REPO` (sibling-folder lookup, overridable by environment), `VSCODE_STORE_URL` (None), `BROWSERS` (Chrome only), `PRIVATE_LISTING`, `OTHER_BROWSERS`; `--check-only`, `--external`, `--out DIR` |
| `tools/pages/**/body.html` | 25 body fragments at c1800f8: index; beethoven (admin, privacy, request, reviewers, support, terms; vscode index, privacy, terms, terms-full, third-party); data (index, datasets, gallery, hardware); onboarding; people (index, education, organization); research (index, conferences, goals, outside, workshop) |
| `tools/templates/` | `head.html`, `header.html`, `footer.html`, `page.html`, `request-form.html`, `browser-card.html` |
| `tools/square_headshot.py`, `tools/stamp_assets.py` | headshot cropping; the pre-build stamper, superseded by the build (site `README.md`, "Caching") |
| `pacs/index.html`, `pacs/ct.html`, `pacs/xr.html` | the demo's pages (`kind="app"` in `SITE`: header only) |
| `pacs/pacs.js` (40,364 B), `pacs/pacs.css` | the NiiVue CT viewer and the measurement animation driven by `metrics.json` |
| `pacs/xr.js` (40,468 B), `pacs/remote.js` (3,878 B), `pacs/infer.js` (23,030 B) | the X-ray tab; `remote.js` holds `SERVICE_DEFAULT`, `serviceURL()`, `RemoteDetector` (`GET /health`, `POST /infer` multipart image, conf, imgsz) and `modelLevels()`; `infer.js` is the former in-browser decode path kept for the reference pane |
| `pacs/coi-serviceworker.js`, `pacs/package.json`, `pacs/measure_live.py` | the COOP/COEP shim of the in-browser era; the latency probe (`--film X --headed --channel chrome`, enters through the github.io host on purpose) |
| `pacs/README.md` (7,001 B) | the demo's own notes; its X-ray section is stale (describes in-browser ONNX with `pacs/models/`, removed 2026-09-14) |
| `pacs/data/manifest.json`, `pacs/data/0003/` | one case: `ct.nii.gz` 1,411,849 B, `seg.nii.gz` 292,542 B, `postop_ct.nii.gz` 1,682,039 B, `postop_seg.nii.gz` 294,920 B, `metrics.json` 16,242 B |
| `pacs/data/xr/` | the DRR reference pane: `manifest.json`, `0003/`, `femoral_head_reference.png` |
| `pacs/tools/` | `export_xr_demo_case.py`, `reference_angles_from_corners.py`, `reference_corners_decode.mjs`, `reference_corners_from_net.py`, `test_buu_live.py`, `test_decode.mjs`, `test_page.py`, `test_webgpu.py`, `truth_corners.py` |
| `atlas/level_atlas.csv` (2,786 B), `atlas/build_table.py`, `atlas/index.html`, `atlas/level_atlas.pdf`, `atlas/level_atlas.png` | the per-level atlas: 47 data rows, measures `canal_ap, canal_w, disc, endplate, h_ant, h_post, hu, pedicle` at T11-L5 and the discs L1L2-L5S1 (counted 2026-10-08); the CSV is rendered into the page so no number is typed |
| `tutorials/` | six Markdown tutorials with their HTML, `_build.py`, `README.md`, `tutorial.css`, `index.html` (the AI Imaging Workshop, WSUSOM) |
| `onboard.sh`, `onboard.ps1`, `onboarding/` | the one-line onboarding (`11_students_grid_access` owns the text) |
| `beethoven/` | the product pages; `services.json` and `killlist.json` are never hand-edited (both editions fetch them); `vscode/`; the two agreement texts as `.txt` |
| `ashley/` | the old address: `REDIRECTS` and `KEPT_FILES` only; the build fails on any other file there |
| `contributions/manifest.json` (11,064 B) | `meta`, `abstracts`, `people` (20 entries on 2026-10-08); the People grid and the CNS 2026 list render from it; names by design; not copied here |
| `meded/summarize_survey.py`, `meded/survey-summary.json`, `meded/README.md` | the de-identified survey summary the Education Outcomes chart reads; the raw CSV is excluded by `.gitignore` |
| `assets/gallery/` | the 12 `.bin` meshes: cases 0004, 0033, 0068, 0231, 0268, 0349, 0378, 0431, 0631, 1035, 1090, 1153 (874,636 to 1,327,480 B; `git ls-files '*.bin'` at c1800f8, 2026-10-08) |
| `gallery/data/distributions.json` (1,368,004 B) | the gallery's distribution data; the only file under `gallery/data/`; no mesh lives there |
| `data/`, `people/`, `research/`, `spine-mri/` (79 files), `celebrate-life/`, `headshots/` | generated pages and sub-sites |
| `sitemap.xml` (41 `<loc>` entries on 2026-10-08), `robots.txt`, `CNAME`, `.nojekyll`, `.gitignore`, `LICENSE`, `NOTICE` | site plumbing |
| `googlec3911e7fb095977e.html` (54 B) | the Google site-verification file; tracked here, never edited, never copied elsewhere |
| `AI_Imaging_Workshop.pdf` (90,116 B), `MANS_Schwing.pptx` (12,194,006 B), `MANS_agenda.pdf`, the conference images and the two videos (`LA_QUINTA_VIDEO.mp4` 21,244,960 B, `BATON_ROUGE_VIDEO.mp4` 7,806,000 B) | conference material served by the site; the workshop agenda also exists as a Word source and two near-identical PDFs elsewhere (routed to `11_students_grid_access`) |

## 2. The toolkit: `OpenSpineToolkit` (public)

- URLs `https://github.com/Gregory-Schwing-MD-PhD/OpenSpineToolkit` (origin) and
  `https://github.com/OpenSpineConsortium/OpenSpineToolkit` (osc); branch `main`; commit **cb43197** (2026-09-25, "A
  one-element array is indexed before it becomes a float"). Push to both remotes.
- Files that matter here: `tools/export_demo_case.py` (the only file under `tools/`): crops to the label bounding box plus
  margin, optional bone mask and downsample, keeps the affine, writes `ct.nii.gz`, `seg.nii.gz`, `metrics.json` and
  appends to `manifest.json`; usage `python tools/export_demo_case.py --ct <case>_ct.nii.gz --label <case>_label.nii.gz
  --case-id <case> --out-dir <site>/pacs/data --crop-margin 25 --mask-bone --downsample 2`; `--geometry-only` re-emits
  `metrics.json` (`memory/pacs-demo-and-ostk-params.md`). It imports `lid` from `ostk.labels` (a fixed-map lookup), not
  `labels_for`. `ostk/labels.py` (`labels_for`, `lid`, `LABELS_V4`, `LABELS_V10`; `LABELS_V10` still maps `"S1": 29`, catalog
  G.3); `ostk/spine.py`; `ostk/surgery.py` (the post-operative synthesis the demo's post-op tab shows, catalog G.5);
  `tests/` (94 test functions, catalog G.1; one failing test on 2026-10-08, `OPEN_QUESTIONS.md` F18). `SPEC.md`, `README.md`
  and `CLAUDE.md` of that repository still describe the legacy scheme and a "27 tests" count (`docs/handoff/INFRASTRUCTURE.md`
  section 7): stale. The open defects G.2 and G.3 belong to `04_openspinetoolkit`.

## 3. The service code: `spinesurg-ct-nnunet` (private, never public)

- URL `https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet`; branch `L6_Class`; commit **097933a** (2026-10-08).
- `service/`: `app.py` (3,580 B; FastAPI, `GET /health`, `POST /infer`), `model_defs.py` (6,661 B; self-contained),
  `Dockerfile` (CPU torch), `modal_app.py` (1,941 B; one-command Modal deploy, L4, scale-to-zero), `requirements.txt`,
  `README.md`; all dated 2026-09-14. `tools/deploy_service.py`: hashes the three weight files, writes `registry.json`,
  uploads to the private weights repository and refuses a public one; tokens from files only. `HANDOFF/` (2026-10-08): the
  eight student-readable files are copied into `docs/handoff/` here; the rest is Greg-only.
- Nothing of this repository is public, and nothing from it is copied here beyond the handoff files and the redacted notes.

## 4. The dataset repository: `CTSpinoPelvic1K` (public)

- URLs `https://github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K` (origin) and
  `https://github.com/OpenSpineConsortium/CTSpinoPelvic1K` (osc); branch `master`; commit **7ddfe38** (working tree
  modified on 2026-10-08). Push to both remotes; commit directly to master.
- Files that matter here: `assets/` (the consortium mark: `osc_logo.py`, `osc_logo.svg`, six PNGs; tracked at 7af09ed "a
  mark for the consortium that survives being 40 pixels wide"; copied into `figures/logo/assets/`); `poster/` (the med-ed
  visual abstract and its scripts; **untracked** in that repository on 2026-10-08; copied into `figures/visual_abstract/`);
  `morphometrics/level_atlas.csv` (the source of `atlas/level_atlas.csv`; owned by `05_ct_morphometry_parity`);
  `scripts/review_anatomy_qc.py` (the three spine checks `spine_qc.py` runs); `docs/survey_protocol.md` (the med-ed survey
  protocol); `Student_Projects/BOARD.md` card `meded`; `CLAUDE.md` (the standing rules in their original words).

## 5. `XRSpinoPelvic1K` (private)

- URL `https://github.com/Gregory-Schwing-MD-PhD/XRSpinoPelvic1K`; branch `main`; commit **4f22935**. No file of it is used
  by this project. It is listed because every folder of this seed names the four repositories, and because its films
  must never reach the site (no radiograph is committed there).

## 6. Beethoven (private; owned by `11_students_grid_access`)

- `OpenSpineConsortium/beethoven` (the browser edition; local folder name `beethoven` or `ashley-bridge`; `main` 2f90319,
  2026-10-03, 32 commits) and `OpenSpineConsortium/beethoven-vscode` (the VS Code edition and the access service; local
  folder `beethoven-vscode` or `ashley`; `main` 8d7fc65, 2026-10-02, 56 commits) (inventory of the other spine folders,
  2026-10-08, section 2.8). `tools/build_site.py` renders their `LICENSE.txt`, `PRIVACY.md`, `extension/package.json`
  (the version) and the VS Code edition's `extension/LICENSE*.txt`, `PRIVACY.md`, `THIRD_PARTY_NOTICES.md` into
  `/beethoven/`; the build finds them as sibling folders or through `BEETHOVEN_REPO` / `BEETHOVEN_VSCODE_REPO`. No local
  remote is configured in either clone; they are pushed with `tools/push_org.sh`. The product is Beethoven; Ashley Schehr
  is a person.

## 7. Weight stores (never public; names only)

- Hugging Face `gregoryschwingmdphd/level-id-weights` (private: `detector.pt` = detect_v5z epoch 25, `level_model.pt`,
  `recurrent_head.pt`, `registry.json` with SHA-256) and `OpenSpineConsortium/level-id-weights` (private, empty), both as
  of 2026-09-14 (`memory/level-service-serving.md`). Live state not re-checked. The site never links to either.
