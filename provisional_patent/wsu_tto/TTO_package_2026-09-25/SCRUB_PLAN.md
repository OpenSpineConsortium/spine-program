# SCRUB_PLAN.md: removing public disclosures of Parts A and B from git

Prepared 26 Sep 2026. Consolidates the searchers' findings, with my own spot checks. This is general practice, not legal advice. Decide the history-rewrite and purge steps with the TTO before taking them.

## What scrubbing can and cannot do

- Nothing below withdraws a disclosure that has already happened. Anything that was public stays prior art from its first public date. For the inventor's own disclosures that date also starts the US one-year grace period; in absolute-novelty jurisdictions it counts against the application at once. Scrubbing does three things only:
  1. It stops new copies (forks, clones, crawlers, CNS attendees who follow a link).
  2. It stops the repos from inviting more public work on the inventions (the student project menu, the roadmaps).
  3. It keeps the claim-relevant specifics (C-arm results, coupling, stop rule, device terms, sweep) that are **not yet public** out of public view. On that last point git is currently clean: I found no B3-B5, B8 architecture, B10, B12, B14, B17, B19 specifics or B20 in any public repo, tree or history. The live risk is local working copies (section 3).
- Three copies are immutable and no git action reaches them:
  - arXiv 2609.22760 v1
  - the NeurIPS 2026 E&D paper and its OpenReview page
  - the Zenodo records: 22139642 (v10 and v11), and build archive 22647933, public 7 Sep, which I opened. It carries `paper/clinical/main.tex` with the iliac-crest and rib-free results, and no Part B.
- A third-party fork (`usmnashd1/CTSpinoPelvic1K`, snapshot of 13 Sep) holds every CTSpinoPelvic1K hit dated before 13 Sep. The owner cannot delete or rewrite it.

## 0. Order of operations

1. **Keep private evidence before any change.** The TTO relies on dated commits as conception evidence. For every repo in section 2:
   - Create the mirror and bundle: `git clone --mirror <url> X.git` then `git -C X.git bundle create X.bundle --all`.
   - Include the orphaned objects:
     - CTSpinoPelvic1K: `git fetch origin a959ff7da5703ff9ea3c28cfe7ec2b71cc6a4f95:refs/preserved/pre_purge`.
     - Site: `git fetch origin 5559d87947c13983a01e6f8f04dc88de0cec4339:refs/preserved/pre_rewrite`.
   - Write a sha256 manifest for the bundles.
   - Save the GitHub Events JSON already collected in `scratchpad\patent_review\ctsp_work\ev_*.json`, and a screenshot of each repo's Settings > Security log (`repo.create` / `repo.access`), especially for XRSpinoPelvic1K.
   - Store all of this privately, outside every repo working tree. Commit dates are self-asserted, and push events are the third-party record. The Events API drops entries after about 90 days: the 27 Aug events expire around 25 Nov, and the 4 Sep proposals push events around 3 Dec. Insights > Traffic keeps 14 days.
2. **Protect the local clones before touching anything** (section 3). One `git add -A` in the Desktop CTSpinoPelvic1K clone today would publish C-arm results.
3. **Commit the current-tree changes** (section 2), directly to master/main, and push to both remotes via WSL, for example: `wsl -e bash -lc 'cd /mnt/c/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1 && git push origin master && git push osc master'`.
4. **XRSpinoPelvic1K:** after the bundle, make it private (recommended), or apply the redactions in 2.3.
5. **File GitHub Support "remove sensitive data / cached views" requests**, one per object network:
   - (a) `Gregory-Schwing-MD-PhD/CTSpinoPelvic1K`, whose network includes the fork `usmnashd1`. List the 190 orphaned commits be4f419..a959ff7 and the paths `proposals/**`.
   - (b) `OpenSpineConsortium/CTSpinoPelvic1K`, same list. It is a separate network.
   - (c) `OpenSpineConsortium/openspineconsortium.github.io`. List the old SHAs from the Desktop clone's `.git/filter-repo/commit-map`: the first changed commit is 4f7987e and the old head is 5559d87. Name the five `pacs/models/*.onnx` paths.
6. **Verify.** Each of these must return 404:
   - `https://raw.githubusercontent.com/OpenSpineConsortium/openspineconsortium.github.io/45ae8f14223a0a78b7e10de7fcdf3274d4183543/pacs/models/v11m_640_v4_fp16.onnx`
   - `.../4f7987e0b8ec681079394de91c896aaff0a8506b/pacs/models/v11n_640.onnx`
   - `https://raw.githubusercontent.com/<owner>/CTSpinoPelvic1K/a959ff7da5703ff9ea3c28cfe7ec2b71cc6a4f95/proposals/xr_fracture_detector.md` for each of Gregory-Schwing-MD-PhD, OpenSpineConsortium and usmnashd1.

   On 26 Sep 2026 all of these returned **HTTP 200**. After GitHub confirms the purge, also check jsDelivr (`cdn.jsdelivr.net/gh/...@<sha>/...`). I did not probe it, because a request would itself create a cache copy.

## 1. Summary

| Repository | Current-tree action | History | Priority |
|---|---|---|---|
| Gregory-Schwing-MD-PhD/CTSpinoPelvic1K + OpenSpineConsortium/CTSpinoPelvic1K | Delete: `paper/cns2026/` (tracked part), the six-lumbar, shift and reading-sheet scripts and results, three design docs, `paper/clinical/`, the email doc. Redact: RIB_REVIEW_GUIDE, ROADMAP, DATASETS_ROADMAP, one code comment, .gitignore and CAMERA_READY_CHANGES | `proposals/` orphans: Support purge. **Do not rewrite reachable history.** | High |
| OpenSpineConsortium/openspineconsortium.github.io | One commit across `pacs/remote.js`, `pacs/xr.js` and `pacs/index.html`. Delete `gallery/data/distributions.json` | 5 detector ONNX files still downloadable by SHA: Support purge, or delete and recreate the repo | High |
| Gregory-Schwing-MD-PhD/XRSpinoPelvic1K | Make private (recommended), or delete `localize.py` and `train_localizer.py` and redact README, ROADMAP and metadata. Delete the `.ica` and `.crdownload` files either way | e1a7918-era README and ROADMAP, a 91 MB BUU `.crdownload`: rewrite only if it stays public | High |
| OpenSpineConsortium/Student_Projects | Redact IDEAS.md B6 and E2 | Leave | Medium |
| Gregory-Schwing-MD-PhD/OpenSpineToolkit + OSC mirror | Redact three code comments | Leave | Low |
| All others (section 2.6) | None for the patent | None | n/a |

---

## 2. Per repository

### 2.1 CTSpinoPelvic1K (origin `Gregory-Schwing-MD-PhD` and mirror `OpenSpineConsortium`; apply identical commits, push to both)

State:
- master is 38b0cb9 on both remotes.
- Branch PIR (01de136) is an ancestor of master.
- Tag `v10-build-archive` points to f9b5c84 (7 Sep). **Zenodo 22647933 cites it as "Code state cited by the build archive."**
- Origin has an open PR #1 from `usmnashd1`, with no element content.
- One fork, `usmnashd1`, with master at 6dbc561 (13 Sep).
- Licence is Apache-2.0 (see section 5).
- No releases, no gists, and no issue text with element content.

#### Current tree: delete

Move the local copies first, so nothing is lost and nothing is re-added. `paper/cns2026/**` is already covered by `.git/info/exclude`, so `git rm --cached` is enough for it. Every other path must be moved out of the working tree before `git rm`, or a later `git add -A` re-stages it.

| Path | Elements | First public (origin, UTC) | Breaks / how to avoid |
|---|---|---|---|
| `paper/cns2026/make_cns_deck.py` + `paper/cns2026/figs/*.png` (10 tracked files) | Concept-level B1, B2, B7, B13 ("Aim: the level named on the intraoperative film, from local shape, before the incision, with a probability attached", "4,000 rendered radiographs … corners exact by construction", "class-agnostic corner detector"); on CT: A3-A6, A2 readings, a posterior over readings | 7 Sep 23:57 (pre-purge twin 68619fb; re-pushed as fba94ca on 11 Sep). **public_record says 11 Sep; the correct date is 7 Sep.** | Nothing references `paper/cns2026` (I checked README, Makefile, CI and the site). Use `git rm -r --cached paper/cns2026`: the local files stay and remain ignored by `.git/info/exclude` (`/paper/cns2026/*`, `/paper/cns2026/figs/*`). The dataset-article figures have their own copies in `paper/mpda/figures`. |
| `scripts/six_lumbar_readings.py`, `results/six_lumbar_readings/` (report.txt, csv, png, pdf) | A2 (rule-based call per record: true L6 / lumbarized S1 / aplastic-rib T12), A3-A6, A8 (the call printed with the scores that drove it, "needs a reader"), A9 partial, A10 (z-scores against 643 normal records) | Script 7 Sep 18:41; results 19:13 | Only the deck generator reads them. Delete together with the next row. |
| `scripts/shift_hypothesis_test.py`, `results/six_lumbar_readings/shift_hypothesis.csv`, `shift_hypothesis_report.txt` | A2 (detects the one-level label shift from shape), A1 partial, A6 | 7 Sep 19:13 | `six_lumbar_readings.py` reads `shift_hypothesis.csv` by default, so delete them together. |
| `scripts/render_reading_sheet.py`, `results/reading_sheets/` (0068, 0376, 1053) | A8, A3, A5, A6 | 7 Sep 20:06 | None. |
| `docs/ANCHOR_ORDINAL_DESIGN.md` | On CT: A3-A6, B2 (T12 vs L1 from morphology), and the B9-B11 analogue: "Neither head suffices", "At inference the disagreement is the output" | By 27 Aug 12:46 | Only cross-references COUNTING_PRIOR_ART. It stays readable in the fork, the tag and history. |
| `docs/SEGMENTATION_ARCHITECTURE.md` | A1 partial ("Classes contain no vertebral identity"), A3, A4, A9 ("ambiguous with both readings") | By 27 Aug; ambiguity wording 7 Sep 16:59 | Referenced only by COUNTING_PRIOR_ART.md:74. |
| `docs/COUNTING_PRIOR_ART.md` | A1 partial, A3, A4 | By 27 Aug | Referenced only by ANCHOR_ORDINAL_DESIGN. |
| `paper/clinical/main.tex`, `paper/clinical/iliac_crest_landmark.pdf` | A7, A4 | By 27 Aug. **Also inside Zenodo 22647933** (`08_grid_worktree` → `untracked_files.tar.zst`, public 7 Sep), so deleting it retracts nothing. | Nothing references it. Keep it locally for the SSRR submission. Optional for the patent; reasonable as an unpublished manuscript. |
| `docs/EMAIL_CM_SPINE_REQUEST.md` | B1 interest only | 10 Sep 04:49 | None. It also lists eleven third-party email addresses. |

#### Current tree: redact (keep the files, because they are linked)

1. **`docs/RIB_REVIEW_GUIDE.md`** (B1, B6, B13, B15 at concept level; since 30 Jun, public by 27 Aug). `README.md:38`, `reviewtool/README.md:8` and `reviewtool/cli.py:657` link to this file, so keep the path.
   - Replace lines 15-33 with:
     `## Why this matters` / (blank) / `Every rib in the CT must be complete and correctly numbered. A rib left in two pieces, or two ribs sharing one number, is a defect in the labels the dataset exists to provide, and it carries into every measurement built on them. Your correction is what makes the label right.`
   - Keep the image at line 35.
   - Replace the caption at lines 37-39 with `*A rib cage in the dataset, each rib coloured by its number (the flagged rib is ringed).*`
2. **`docs/ROADMAP.md`** (B7, B9 anchor on a positively identified S1, B11 fail loudly; 26 Aug). Delete lines 120-185 inclusive, from `## Landmark model (XR) — generalization gap…` through the `---` rule before `## Prone/supine as a design constraint`. `docs/email_update.md:72` links the file but not this section.
   - Optional: soften Paper 4 Aim 3 (lines 63-65) to `- **Aim 3:** transitional-anatomy evaluation on the v4 labels + VerSeFusion augmentation (~50 more LSTV/TLTV; n=33 → ~83, annotated in the v3 scheme); publish v4.`
3. **`docs/DATASETS_ROADMAP.md`** (B13, and B1/B6 at concept level; 25 Jun). Nothing links to it.
   - Line 76: `as: (a) a transitional-rib **evaluation set**, (b) extra rib`.
   - Lines 101-102: `**Phase 0 — deadline (FOV-limited, own data only):** CTSpinoPelvic1K spine + pelvis + T12-anchored ribs. *No external data required.*`
   - Lines 110-112: `**Phase 3 — transitional anatomy:** add the **stump-rib cohort** as a transitional/LSTV evaluation track + rib-morphology supervision; report results on transitional cases separately.`
   - Line 125: end the line at `…Cobb/spinopelvic (ostk).` by dropping `Clinical thread = **miscount → wrong-level surgery**.`
4. **`scripts/relabel_ribs.py:377`** (comment only): `    downstream use, where every rib must be kept, fragment or whole.`
5. **`.gitignore:91-95`** (shows that a TTO package and an unpublished manuscript exist; 25 Sep).
   - First move `TTO_package_2026-09-25/`, any `TTO_package_*.zip`, `WSU_Invention_Disclosure_*.docx` **and `Modified WSU invention_disclosure_form 2026.docx`** (which the current pattern does not match) and `idf_work/` out of the repo folder, for example to `C:\Users\grego\OneDrive\Desktop\private_ip\`.
   - Then delete the comment and the four patterns.
   - If they are deleted before the files move, the next `git add -A` stages the TTO package.
6. **`CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md:63-64`**: end the sentence at `…(5F30GM147909, ended 31 May 2026).` by dropping `is also named in the WSU invention disclosure`.
7. Optional, not patent-related: delete `CAMERA_READY_NEURIPS/REVIEWER_CRITIQUES.pdf/.txt` for review confidentiality; nothing depends on them.

#### Current tree: leave (with reason)

- **`paper/mpda/**` (including `_others/`, `_[student A]/`, `_upd/` drafts), `CLAUDE.md` lines 3-5, `zenodo/**`, `docs/dataset_card.md`, `_README_hf.md`, README iliac-crest rows 172-173 and 190.** These match arXiv v1 and the immutable Zenodo README. The only intraoperative content is the LevelCheck and Otake prior-art discussion. Removing them breaks the article build and REPRODUCE.md. If wanted, soften the "Naming a level without counting to it" paragraph (`zenodo/README.md` 205-217) in the next integer Zenodo version only.
- **`scripts/test_morphometric_separability.py`.** It reproduces the arXiv AUC 0.990.
- **Castellvi screens, TP and ala measurement, `extract_transition_morphometrics.py`, `render_phenotype_plate.py`, `fig_countfree.pdf`, `morphometrics/*.csv`, `docs/LAB_JOURNAL.md`.** These build released CSVs, figures and re-read queues. `fig_countfree.pdf` is included by `reprint_check.tex` and `typeset_preview.tex`. If the TTO wants A5 narrowed, `scripts/screen_missed_castellvi.py` (the learned ranking) is the only one worth removing.
- **Bicoxofemoral axis in `SPINOPELVIC_ESTIMATOR.md` and the femur scripts.** This is the standard pelvic-incidence construction on CT, not B15.
- **`LICENSE` (Apache-2.0).** It cannot be withdrawn for copies already distributed; see section 5.

#### History

- **Orphaned `proposals/` (be4f419..a959ff7, 190 commits).** Pushed 4 Sep 06:23 UTC to both remotes. Refs removed by git-filter-repo on 11 Sep 13:11 UTC. Still served by SHA from origin, osc and the fork (verified 26 Sep, HTTP 200).
  - `xr_fracture_detector.md` / `.docx`: B1, B2, B9 (in-view sacral-base anchor), B11 (explicit transitional flag), B13, B15 concept, "naming head on DRRs".
  - `lab_update_email_2026-09-07.md`: 7 Sep 18:16 UTC.
  - `irb/*`, `irb_amendment_draft.md`, `andreea_email.md`, `annotator_email.md`: B7 corpus size, B19 same-visit CT truth and silent prospective evaluation, A2 concept. These also carry staff email addresses.
  - **This is the most explicit public Part B concept statement, and it is missing from public_record.json.**
  - Action: Support purge requests (a) and (b). No ref points into the orphans: the tag, PR #1 and the fork's branches all sit on post-purge history, so a purge breaks nothing.
- **Do NOT rewrite master.**
  - The hits above sit in reachable history from 21 Aug onward. Rewriting would change f9b5c84, which Zenodo 22647933 cites through the tag. The NeurIPS paper and arXiv v1 cite the repo as the code of record.
  - The fork's 13 Sep snapshot, the Zenodo build archive and the papers would keep the same content anyway.
  - A rewrite would also strand PR #1 and every student and grid clone.
- Commit messages that stay regardless: 2c0def3 (names the invention-disclosure package) and fae8e09 (the readings). Low weight: they show that the documents exist, not what they say.

### 2.2 OpenSpineConsortium/openspineconsortium.github.io (Pages → openspineconsortium.com)

State:
- master is a3f7474. No forks, stars, issues or PRs. Apache-2.0.
- History was rewritten 14 Sep (filter-repo) to remove `pacs/models/*.onnx`.

#### History (highest priority on this repo)

- The five detector ONNX files (B7, enabling weights of the film-trained class-agnostic YOLO11m-pose vertebra and corner detector, plus the earlier v11n pair) are **still downloadable today** by SHA. I verified HTTP 200 for v11n_640 and v11n_1024 at 4f7987e, and for v11m_640_v4_fp16 at 45ae8f1. The site itself now returns 404 for `/pacs/models/…`.
  - Added: 4f7987e (9 Aug), 97df16a (pushed 11 Sep 22:50Z), b459213 (12 Sep 10:26Z), 45ae8f1 (13 Sep 00:56Z).
  - **public_record.json and the TTO form say the weights stopped being public on 14 Sep. That is wrong.**
- Action, option (a): Support purge request (c). Breaks nothing.
- Action, option (b): delete the repository and recreate it under the same name. Push master from a **fresh clone of the current remote**. Never push from the Desktop clone's pack or from the scratch clone `scratchpad\patent_review\repos\osc_site`, which holds `refs/old/pre_rewrite`; delete that scratch clone after review. Option (b) takes the site offline until Pages is re-enabled on master root with the custom domain (the CNAME file is in the tree; the certificate can take up to 24 h).
- Commits ea0086c, 8f854d5 and a3f7474 (14-22 Sep) carry the "level model / level NAMES" text below. They are reachable, so they can be removed only by another rewrite. Recommended: do not rewrite for that. The statements are existence-level, with no method or results.

#### Current tree (one commit; the files share ES-module imports)

Bump the cache-busters to `?v=20260926a`:
- `pacs/index.html:283`, which currently loads `xr.js?v=20260911b`;
- `xr.js:21`, which imports `remote.js?v=20260914a`;
- `xr.js:19-20`, the `infer.js` import, if `infer.js` is edited.

1. **`pacs/remote.js`** (B1/B2/B8 at existence level; B7).
   - Replace the header (lines 1-13) with: `/* Remote detector: the model runs on a server and this page only sends pixels. Anything a browser loads a visitor can save, so no model file is delivered to this page. Each detection is a vertebra box with four corner keypoints; the service does not name levels. Level names come only from the region chain chosen on the page (infer.js assignLevels). Endpoint: ?service=URL, then localStorage, then SERVICE_DEFAULT. The service answers GET /health and POST /infer (multipart image, conf, imgsz). */`
   - Line 15: change `SERVICE_DEFAULT` from `https://level-id.openspineconsortium.org` (NXDOMAIN today) to a neutral host name, or an empty string.
   - Delete `modelLevels` (lines 71-78).
   - Optional: in `infer()`, drop `level`, `level_conf`, `level_run` and `top3` from each detection.
   - If the localStorage key `"levelIdService"` is renamed, change both `setItem` (line 19) and `getItem` (line 20).
2. **`pacs/xr.js`** (B1/B8 at existence level, B7, B9-adjacent).
   - Line 21: `import { RemoteDetector, serviceURL } from "./remote.js?v=20260926a";`.
   - Lines 40-46: `// THE MODEL DOES NOT SHIP WITH THE PAGE. The detector runs behind one endpoint (see remote.js); this page sends pixels and receives vertebra boxes and corners. Level names come only from the region chain chosen under Model. The 640 px working size is kept: measured on the same film it finds the same vertebrae as 1024 at a quarter of the compute.` This also drops the sentence saying the weights "were, in effect, published".
   - Lines 411-414: `// The detector names nothing; the reader chooses the chain.` / `const region = els.regionSel ? els.regionSel.value : "none";` / `const levelled = assignLevels(dets, region);`.
   - Line 584: `` `Re-inferred by the detector service at ${detImgsz}px and confidence ` ``.
   - Lines 622-628: set the engine title to `"The detector runs on a server, not in this browser: the page sends the image and receives boxes and corner landmarks. No model parameters are delivered to the page."` and delete the registry / `level_model` lines and the `modelName` assignment that reads `reg.level_model`.
   - Lines 764-770: keep only the two region branches, `Unnamed. Looks like a ${region} film — ${why}. Choose a region to apply names.` and `Named as ${current} by counting. …`. Delete `modelNamed`.
   - Lines 24-39 (fp16 vs int8, v3/v4 AP50 and PCK) can stay: they describe the detector, which is already public.
3. **`pacs/index.html`** (a privacy statement that has been false since 14 Sep; B7 training corpus).
   - Lines 11-14: `RIGHT  your own film. It is sent to the detector service, which returns vertebra boxes and four corners per vertebra.`
   - Lines 120-122: `The film is sent to the detector service for this analysis.` Add a retention statement only once it is true.
   - Lines 170-171 tooltip: `YOLO11m-Pose keypoint detector.`
   - Keep the element ids `regionSel`, `modelName`, `regionNote` and `dropzone`.
   - Leave the DRR, bicoxofemoral and counting teaching text (lines 206-258). It is public through ostk (2 Aug) and XRSpinoPelvic1K.
4. **Delete `gallery/data/distributions.json`.** It is a stale duplicate that nothing references; the live page reads `assets/gallery/distributions.json`.
5. Optional softening. These are already public in arXiv v1 and Zenodo, so the edits do not retract anything:
   - `assets/js/gallery.js:99-101`: delete "Morphology is the better hint than counting here…".
   - `assets/gallery/distributions.json`, Castellvi caption: replace "Height and gap carry most of the grading without naming the level." with "Type I is defined on craniocaudal height at nineteen millimetres, marked here."
6. Optional housekeeping:
   - `pacs/infer.js` header lines 10-13: `The model has ONE class. It finds vertebrae; it does not name them, and the level names this file assigns come from a chain the caller chooses (see assignLevels).`
   - Delete the dead `SpineDetector` class (lines 370-466). Do **not** delete `infer.js`: xr.js and `tools/test_decode.mjs` import from it.
   - `pacs/README.md` lines 71-89: `The detector is not distributed with this site; the page sends the film to a detector service and receives boxes and corners.`
   - Remove the committed `pacs/tools/__pycache__/*.pyc`.

Leave:
- `pacs/tools/export_xr_demo_case.py` and `pacs/data/xr/**`: deleting them blanks the reference pane.
- `pacs/tools/*` decode and test scripts.
- `spine-mri/*`: clinical teaching about the problem, not the solution.
- `contributions/manifest.json`: the CNS title only.
- `index.html` dataset text.
- `MANS_Schwing.pptx`, `AI_Imaging_Workshop.pdf`, `atlas/level_atlas.pdf`: I scanned them and found no element text. MANS_Schwing.pptx is a separate privacy issue (section 5).

### 2.3 Gregory-Schwing-MD-PhD/XRSpinoPelvic1K

State: main is 4f22935. No forks, releases, issues or tags. Apache-2.0. Created 24 Jun 2026; last push 15 Aug. Whether it was public from creation is **not established**; check the Security log.

**Recommended: bundle, then make private.**
- Nothing public depends on it. CTSpinoPelvic1K `RIB_REVIEW_GUIDE` and `ostk/drr.py` name it without a link.
- The Docker image `go2432/xrspinopelvic` does not copy the code.
- The HF Space `spinesurg-ct-annotator` deploys independently.
- Going private also removes the side issues below.
- It does not undo B1 (concept plus scaffold) or B15 (enabling code). If it was public from creation they have been public since 24 Jun and 4 Aug, and B15 is public anyway through ostk (2 Aug) and the HF Space.

If it must stay public, apply the following in one commit.

1. **Delete `xrsp/localize.py`** (B1, B13: "name the vertebral level under a query point (e.g. the C-arm centre…) — the intra-op 'wrong-level surgery' guard. Trained on the DRR dataset"), **and `scripts/train_localizer.py`**. Then:
   - In `xrsp/__init__.py`, remove line 6 (the `.localize` import) and `"gaussian_heatmaps", "level_at_point", "points_from_heatmaps",` from `__all__` (line 13).
   - In `tests/test_drr.py`, remove `level_at_point` from the import at lines 6-8, remove lines 53-55, and delete `test_heatmap_roundtrip` (or point it at `xrsp.heatmaps`, whose signature differs).
   - Update README line 203 (`14 tests`) to the new count.
   - The Makefile, slurm, YOLO and unified scripts do not import `localize`.
2. **`README.md`.**
   - Line 3: `**An open spinal-radiograph (DRR) dataset with amodal endplate-corner and spinopelvic landmarks — generated from segmented CT.**`
   - Line 5: start with `> Spinopelvic alignment is measured on lateral radiographs, but there is **no open spinal X-ray dataset with vertebra-level labels**…` and keep the rest.
   - Lines 114-115: `        ▼  train_landmarks.py / train_unified.py  (heatmap targets → U-Net → endplate corners + hip point)` / `  PI · SS · PT · LL  (xrsp/measure.py)`.
3. **`docs/ROADMAP.md`.**
   - Replace §1 (lines 26-31) with `## 1. Train the landmark model` / `- Targets: xrsp.heatmaps.gaussian_heatmaps (4 corners per level + hip point); model xrsp.model (MONAI U-Net); trainer scripts/train_landmarks.py.`
   - Line 40: end at `…behind the same \`projection_plan\` interface.`
   - Line 44: `- Report landmark error and SS/LL/PI agreement on real data.`
   - Delete §4 (lines 46-48).
   - Line 52: `- Model I/O: image → per-landmark heatmaps → points → xrsp.measure angles.`
   - Keep the DeepDRR sentences. They are evidence that per-device image formation (B14/B17) was **not** public.
4. **Metadata and small edits.**
   - `pyproject.toml` L8: `description = "XRSpinoPelvic1K — open spinal-radiograph (DRR) dataset with amodal spinopelvic landmarks, generated from segmented CT."`; L13: `keywords = ["spine", "radiograph", "DRR", "landmark detection", "spinopelvic"]`.
   - `xrsp/__init__.py` docstring: the same wording as the description.
   - `docs/dataset_card.md` L14-17: `Training/evaluation of radiograph models for spinopelvic landmark detection and DRR→real-radiograph domain adaptation. **Research/education only — not a medical device.**`
   - `docs/PIPELINE.md` L126-127: `Six specimens is a domain-gap probe, not a cohort.`
   - `docs/RESULTS.md` L207-209: `* the padding is uniform grey. A real standing film's margins contain thoracic vertebrae — distractors that look exactly like the objects being detected.`
   - `xrsp/labels.py` L34-36, comment only: `# Vertebral levels projected as per-level landmarks (cranio-caudal), VerSe ids; T13 sits between T12 and L1; absent levels are skipped.` Keep the list; `project_labels.py` and `__init__` use it.
   - `tests/test_drr.py` docstring: `DRR engine + label projection — on a synthetic CT so it runs with no data. Checks the DRR/label projections are aligned.`
5. **Leave**, because they are core generator code and already public elsewhere:
   - `xrsp/oblique.py`, `build_dataset.py`, `project_labels.py`, `drr.py`, `drr_to_yolo.py`, `unified.py`, the YOLO scripts, `splits.py`, `RESULTS.md` (the negative sim-to-real results teach against B16/B17), and the example and figure PNGs.
   - Removing them breaks PI generation, the tests and README images.
6. **Delete regardless (side issues).**
   - `Q2VybmVyNzE1LlBvd2VyQ2hhcnQgRHJhZ29uIFByb2Q-.ica`: a Cerner PowerChart Citrix launch file with LogonTicket/ClearPassword fields. Tell DMC IT if policy requires.
   - `Unconfirmed 31234.crdownload`: BUU radiographs.
   - Add `*.ica`, `*.crdownload` and `cookies.txt` to `.gitignore`.

**History, only if the repo stays public.**
- Items: the e1a7918 README (L45-50, L67-83, "Real-time fluoroscopy inference loop (frame → level overlay)"), the e1a7918 ROADMAP ("real-time fluoro loop"), the `.ica` file, both `.crdownload` files (the 91 MB `Unconfirmed 213265.crdownload` holds 215 BUU AP films and CSVs), and the deleted oblique and corner PNGs.
- Method: `git filter-repo --invert-paths --path <ica> --path "Unconfirmed 213265.crdownload" --path "Unconfirmed 31234.crdownload"`, plus `--replace-text` for the README and ROADMAP lines. Then force-push and file a Support purge.
- With 0 forks, the only breakage is the grid clone (`git fetch && git reset --hard origin/main`).
- Privatising makes all of this unnecessary.

### 2.4 OpenSpineToolkit (Gregory-Schwing-MD-PhD and OpenSpineConsortium; main cb43197 on both)

Apply as one commit and push to both remotes. None of these edits breaks anything, because they are comments only.
- `ostk/vertebral_body.py` 336-338: `# pass the CALLER's axes through -- defaulting silently to the world axes made this correct only when the caller happened to use them`.
- `ostk/vertebral_body.py` 600-601: `# !! initial scale is not set by the contamination. The live path is endplate_corners_body.`
- `ostk/metrics.py` 175-178: `It is also the only anchor derivable from landmarks visible on a lateral radiograph, which keeps CT- and radiograph-derived PI on one definition.`

Leave:
- `ostk/drr.py`, `ostk/project2d.py`, `tests/test_drr.py`, `tests/test_project2d.py` (B13 generic, B15).
  - Deleting them breaks `import ostk` (`__init__.py` lines 3, 5, 27 and 46), XRSpinoPelvic1K `annot/make_reference.py` and the site's `export_xr_demo_case.py`.
  - They have been public since PR #5, **opened 2 Aug 2026 18:04 UTC** (public_record says 4 Aug), and possibly earlier on the student fork `[student A]/OpenSpineToolbox` (commits 24 Jul).
  - Four student forks hold copies. The code was written by [student A], which matters for inventorship if a claim covers it.
- `labels.py`, `SPEC.md` and `cli.py` (the published label scheme), `morphometry.py` (Panjabi-style per-level morphometry that the released level atlas depends on) and `projects/spinal-stenosis/README.md` (textbook background).
- No history action.

### 2.5 OpenSpineConsortium/Student_Projects (main fd60c58; PR #1 open, based before IDEAS.md)

Redact `IDEAS.md` and keep the entry ids. F1 refers only to B2 and B3, and `/onboard` and `/new-project` read the file generically. The purpose is to stop a public student project from building the Part A phenotype reader or crop-based identity learning (B2/B8); the redaction does not retract anything.
- Lines 84-88, **B6**: `**B6. The eighteen L6 records, described.** Eighteen records carry an L6. Tabulate their age, sex, position, Castellvi grade and lumbar-rib status from the manifest, and render each in the gallery viewer. Source: paper, introduction. Difficulty 1.`
- Lines 138-141, **E2**: `**E2. Segmentation quality by field of view.** Evaluate the released checkpoints on spine-only against pelvic records and report per-class Dice by record type. Source: paper, future directions.`
- Optional, B1 (line 52): delete `all normalised by the patient's own median across levels`.

History (`projects/IDEAS.md` in 44ccdbc, 7 Sep 17:54 UTC): do not rewrite. The content is in arXiv v1 and in CTSpinoPelvic1K. A rewrite would break every student clone and the grid clone.

### 2.6 Repositories with no scrub action for the patent

| Repository | Finding | Reason to leave |
|---|---|---|
| OpenSpineConsortium/spinopelvic-seg; anonymous-neurips-ED/spinopelvic-seg | nnU-Net code of the NeurIPS paper. Its docstring argues that local shape cannot separate L5 from L6. | It teaches against B2/B3, which is worth keeping. The paper and the HF checkpoint card point to it. |
| **anonymous-mlhc/CTSpinoPelvic1K, anonymous-mlhc/spinopelvic-seg** (not in the searchers' list) | One commit each, 8-9 Jun 2026. Scanned: no element hits ("sweep" is a hyperparameter sweep; "wrong-level" is background). | Nothing to scrub. |
| lstv-detector, spine-level-ai, lstv-uncertainty-detection, lstv-fusion, spineps-segmentation, VerSeFusion | MRI or label-based weak analogues of A1-A10, all from Feb to Jun 2026. | Pre-conception; the inventor's own prior art to **disclose to the TTO**, not scrub. Deletion changes nothing and breaks the AACA slide link and the NeurIPS D&B companion. Grace for the February items runs to about 9-12 Feb 2027. |
| lstv-annotation-tool, spinesurg-ct-annotator (GitHub) | No element hits. | See section 5 for the RSNA DICOMs in history. |
| Gregory-Schwing-MD-PhD.github.io, Gregory-Schwing-MD-PhD/OpenSpineConsortium | Generic LSTV MRI card; placeholder template. | See section 5 for the API key and CV. |
| Forks spineps, totalspineseg, CTSpine1K, d2D, RSNATemplate (not in the searchers' list) | The user's own commits are dependency pins (spineps), `--save-uncertainties` (totalspineseg, 19 Feb, MRI), or unrelated. | No hits. |
| u251-*, cphmd_myc_max, omomyc_myc_rfbe, SmallMoleculeResearch, paralleledmondsblossom, transcriptionfactorsimulation, SpineNerveModelGenerator | Unrelated topics. The HEAD trees of the four largest contain no spine terms. | n/a |
| Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet | Private (API 404). Part B code lives here. | **Keep it private.** See section 5 on the broken commit citations; do not "fix" them by pushing this history to a public repo. |

### 2.7 Non-GitHub public copies found (git-backed or distribution)

- **HF Space `gregoryschwingmdphd/spinesurg-ct-annotator`** (public, 44 commits, femoral-head annotator deployed 13-15 Aug). Its README says "The hip point in XRSpinoPelvic1K is learned from **synthetic DRRs**, where the ground truth is a 3-D sphere fitted to the femoral head and projected" (B15). It survives privatising XRSpinoPelvic1K. Leave it for the patent, since B15 is public through ostk. It also hosts BUU film PNGs (`pilot_review/*.png`, `calib_film.jpg`); see section 5.
- **HF models.** The only public weights are the nnU-Net segmentation checkpoints (`OpenSpineConsortium`, `anonymous-mlhc`, `anonymous-neurips-ED` /spinopelvic-seg-checkpoints). There is **no** level model or detector on HF publicly.
- **HF datasets** (`OpenSpineConsortium`, `gregoryschwingmdphd`, `anonymous-mlhc`, `anonymous-neurips-ED` /CTSpinoPelvic1K). The cards contain no Part B text. The OSC card still says "You cannot tell L5 from L6 by looking at one vertebra. Level identity is a counting problem", which teaches against B2. Leave.
- **Docker Hub `go2432`** (24 images). The only related images are `xrspinopelvic` (environment only) and the Feb MRI images. No level or detector image.
- **Zenodo 22647933 build archive.** I scanned all 493 files in `08_grid_worktree`: no Part B, but it carries `paper/clinical/main.tex` (A7/A4 results) and the Zenodo README. It is immutable.

---

## 3. Local working copies: the real ongoing risk

The Desktop clone `C:\Users\grego\OneDrive\Desktop\CTSpinoPelvic1K-1` (public remotes origin and osc) has **518 untracked entries**, and most of them are **not ignored**. A single `git add -A` or `git add .` would publish:

- **Undisclosed Part B specifics:**
  - `docs/HANDOFF_2026-09-21_PM.md`: C-arm LODO results, the nine image-formation terms, the rx_* detectors, C-ArmLSpine and DeepFluoro numbers.
  - `C-Arm Validation Research Plan.pdf`, `Spine Fluoroscopy Image Datasets.pdf`.
  - `scratchpad/REPORT_final.md`, `scratchpad/REPORT_interim.md`, `scratchpad/drr/`, `scratchpad/schwing_det_p1.png`, `p2.png`.
  - `scratchpad_resweep_*`, `scratchpad_sweep*.log`, `scratchpad_spine_sweep.txt`.
  - `_desc.py`, `BIBM/…/conference_101719.tex`, `docs/ukb.html`.
- **Invention-disclosure material:** `Modified WSU invention_disclosure_form 2026.docx` (not matched by the `.gitignore` pattern).
- **Other:** the decks `TechFair_LSTV_Schwing.pptx`, `Med_Ed_CNS*.pptx` and `2026 CNS AM Speaker Powerpoint Template.pptx`.
- **Credentials and third-party data:** 10 Citrix `.ica` files (Cerner/Tenet), `cookies.txt`, `ckpt_mirror/` (11 MB), `BUU-LSPINE_400/`, IRB and personal PDFs.

The CNS deck generators (`paper/cns2026/make_cns_deck_v2..v10.py`, **`make_cns_deck_v11_public.py`**, `prep_v*_figs.py`, `figs_public/`, `abs418_tables.json`) are ignored only by `.git/info/exclude`, which exists in this clone only.

Actions (no commit needed):

1. Move everything that is not repository content out of the repo folder, for example into `Desktop\private_ip\` and `Desktop\papers\`. This includes the TTO package and all the files listed above. The repo folder should hold only the repo.
2. Set a global excludes file (`git config --global core.excludesFile ~/.gitignore_global`) containing `*.ica`, `*.crdownload`, `cookies.txt`, `*invention*`, `TTO_package*` and `idf_work/`. That applies to every repo on this machine, the case that already leaked into XRSpinoPelvic1K.
3. Add a `pre-commit` hook to each public clone (append; `.git/hooks` has only the git-lfs hooks). It should reject a commit whose staged diff (`git diff --cached -U0`) matches `C-?arm|fluoroscop|SchwingNet|alphabet|image[- ]formation|level[ _-]model|abstain|LODO|DeepFluoro|C-ArmLSpine|\.onnx|invention`, with an explicit override flag.
4. `openspineconsortium.github.io` Desktop clone: `pacs/sllp/` (single / fullwidth / band test outputs), `pacs/testimgs/` (BUU films) and `pacs/webtest/` are untracked. Add them to `.git/info/exclude` or move them out.
5. Slides (git side only): the CNS deck, including any "disclosure-friendly" version (`make_cns_deck_v11_public.py`, `prep_v16_public_figs.py`), should never enter git. Deliver it to CNS directly, after the TTO has cleared the content. Tracked `paper/cns2026` files go with `git rm -r --cached` (2.1). The exclude rules keep the local generators ignored afterwards.

---

## 4. What a history rewrite would and would not achieve

**It would:**
- stop GitHub from serving blobs by SHA and remove them from the compare, archive and blame views, but only after a GitHub Support purge. A force-push alone leaves orphans fetchable, as shown by the proposals and ONNX commits that still returned 200 on 26 Sep;
- stop casual discovery by anyone who clones afterwards.

**It would not:**
- reach existing clones: the grid clones, student clones, the searchers' scratch clones, and anyone's `git clone` since June;
- reach third-party forks: `usmnashd1/CTSpinoPelvic1K` (13 Sep snapshot), the four `OpenSpineToolbox` student forks, and `[student A]`'s 3d-to-2d branch;
- reach caches: jsDelivr or githack mirrors if someone requested them, GitHub's Events API (it lists SHAs for about 90 days), or search-engine caches;
- reach immutable records: arXiv 2609.22760 v1, the NeurIPS/OpenReview paper, Zenodo 22139642 (v10/v11 README) and 22647933 (build archive with `paper/clinical`), and the HF dataset cards and Space;
- change any first-public date. Everything public stays prior art from that date.

**It would break:**
- CTSpinoPelvic1K: the `v10-build-archive` tag cited by Zenodo 22647933, the NeurIPS and arXiv code citations, PR #1 and every student and grid clone. **Do not rewrite CTSpinoPelvic1K reachable history**; purge only the already-unreferenced `proposals/` orphans.
- The site: nothing further, because the rewrite is already done; only the purge is outstanding.
- XRSpinoPelvic1K: only the grid clone (0 forks), if it stays public and is rewritten.

**Before any rewrite or purge:** keep the private full backup bundles and the push-event evidence from step 0.1. The TTO relies on dated commits as conception evidence, and a purge destroys the only server-side copy of the orphaned commits.

---

## 5. Side issues found (not patent)

- **Apache-2.0 patent grant (section 3).** It covers CTSpinoPelvic1K, XRSpinoPelvic1K (`localize.py`, `oblique.py`, `build_dataset.py`), OpenSpineToolkit (`drr.py`, `project2d.py`, a student contribution), the site repo (detector code, and the ONNX weights distributed from it) and spinopelvic-seg. Student_Projects is MIT. The grant cannot be withdrawn for copies already distributed. Flag it to the TTO, and keep future inventive code out of Apache-2.0 repositories.
- **Broken citations.**
  - The NeurIPS camera-ready says "trained with github.com/OpenSpineConsortium/spinopelvic-seg at commit 50b209f". That commit does not exist there: the repo has fd8d565 and c105981 only. 50b209f (2 May 2026) is in the private spinesurg-ct-nnunet.
  - arXiv v1 cites spinesurg-ct-nnunet at 50b209f, which now returns 404.
  - Fix the citation text. Do not push spinesurg-ct-nnunet refs to a public repo. If a public copy of 50b209f is ever needed, push only a tag at that commit, after checking that its ancestry holds nothing dated after 2 May.
- **Privacy and credentials.**
  - XRSpinoPelvic1K: the `.ica` EHR launch file, and BUU films in `.crdownload` files and figure montages.
  - HF Space `spinesurg-ct-annotator`: BUU films. Its own `app.py` says "redistribution is not ours to grant."
  - The site: `MANS_Schwing.pptx` ("Internal Use Only", with a patient case).
  - Personal site: a hardcoded Gemini API key at `index.html:508` since Aug 2025 (rotate it), and a CV with home address, phone and USMLE ID.
  - lstv-annotation-tool: RSNA 2024 DICOMs in history.
  - Staff emails in the purged `proposals/` and in `docs/EMAIL_CM_SPINE_REQUEST.md`.
- **Content accuracy.**
  - lstv-uncertainty-detection `AACA_ABSTRACT.md` states sensitivity, specificity and AUROC that were written before the inference code existed, lists other authors, and gives a Neurosurgery affiliation. Correct to "Results pending radiologist audit; none measured" and to the Department of General Surgery.
  - The site onboarding line 219 still describes retired identifier 29.

## 6. Corrections owed to public_record.json and the TTO package

1. Add the `proposals/` disclosure: public 4 Sep 06:23 UTC, removed 11 Sep, still fetchable. It covers B1, B2, B9 (sacral-base anchor), B11 (transitional flag), B13, B15 (concept) and B19 (same-visit CT truth, silent evaluation), plus the lab email of 7 Sep.
2. The CNS deck generator was first public **7 Sep 23:57 UTC**, not 11 Sep. The six-lumbar scripts were first public 7 Sep 18:41-20:08 UTC and should be their own item (A2, A8, A10 implementation).
3. The site detector weights were **not** withdrawn on 14 Sep. They remain downloadable by SHA until purged.
4. ostk `drr.py` and `project2d.py` were visible from 2 Aug 18:04 UTC (PR #5).
5. Zenodo build archive 22647933 (7 Sep) carries `paper/clinical/main.tex` (A7/A4 results).
6. spine-level-ai, default branch, 11-12 Feb 2026: an MRI analogue of A3 (ribs traced from image intensity because "SPINEPS labels alone miss 30-40% of T12 ribs") and weak A9 ("EXTEND FIELD OF VIEW").
7. The HF Space README states the B15 hip-point construction.
8. Apache-2.0 applies to XRSpinoPelvic1K, the site and ostk as well as CTSpinoPelvic1K.

## What the searchers missed (spot checks)

I spot-checked the searchers' high-risk findings myself (26 Sep 2026). Three were confirmed with live network checks:
- the purged proposals/xr_fracture_detector.md still returns HTTP 200 by SHA from origin, osc and the usmnashd1 fork;
- the site's detector ONNX files (v11n_640 and v11n_1024 at 4f7987e, v11m_640_v4_fp16 at 45ae8f1) still return HTTP 200 on raw.githubusercontent.com, while openspineconsortium.com/pacs/models returns 404;
- spinesurg-ct-nnunet is private (API 404).

The file contents were confirmed by reading them: make_cns_deck.py, XRSpinoPelvic1K localize.py and its README, the .ica file in XRSpinoPelvic1K's current tree, and the site's remote.js, xr.js and index.html.

What the searchers missed:

1. **Local working copies are the largest live risk.** The Desktop CTSpinoPelvic1K-1 clone (public remotes) has 518 untracked entries, and most are not ignored. They include:
   - docs/HANDOFF_2026-09-21_PM.md, with undisclosed C-arm LODO results, the nine image-formation terms and the rx_* detector generations;
   - "C-Arm Validation Research Plan.pdf";
   - scratchpad/REPORT_*.md, scratchpad/drr/ and schwing_det_p*.png;
   - "Modified WSU invention_disclosure_form 2026.docx", which the .gitignore pattern WSU_Invention_Disclosure_*.docx does not match;
   - 10 Citrix .ica files, cookies.txt, ckpt_mirror/ and BUU-LSPINE_400/.

   One `git add -A` would publish them. The CNS deck generators (v2..v10 and make_cns_deck_v11_public.py) are protected only by .git/info/exclude in this one clone. In the site clone, pacs/sllp/out (single/fullwidth/band outputs), pacs/testimgs (BUU) and pacs/webtest are untracked and unignored.

2. **Two public GitHub repos were in no searcher's list:** anonymous-mlhc/CTSpinoPelvic1K and anonymous-mlhc/spinopelvic-seg (8-9 Jun 2026). I scanned both: no element hits. Also unassigned were five public forks (spineps, totalspineseg, CTSpine1K, d2D, RSNATemplate). The user's own commits in them are dependency pins or a Feb 2026 MRI --save-uncertainties flag, with no hits. The unrelated repos (u251 etc.) have no spine terms in their HEAD trees.

3. **Hugging Face (git-backed) was not searched.**
   - The public Space gregoryschwingmdphd/spinesurg-ct-annotator states the B15 construction ("hip point … learned from synthetic DRRs, where the ground truth is a 3-D sphere fitted to the femoral head and projected"). It survives privatising XRSpinoPelvic1K, and it hosts BUU film PNGs.
   - The only public HF weights are the nnU-Net segmentation checkpoints. There is no level model or detector on HF.
   - The HF dataset cards have no Part B text; the OSC card argues that level identity is a counting problem.
   - Docker Hub go2432 has no level or detector image. There are no gists, no releases on any main repo, and no issue or PR text with element content.

4. **Zenodo build archive 22647933** (public 7 Sep; I downloaded and scanned all 493 files) contains paper/clinical/main.tex with the iliac-crest and rib-free results (A7/A4). Deleting paper/clinical from git therefore retracts nothing. The archive has no Part B content.

5. **The v10-build-archive tag (f9b5c84) is cited by Zenodo 22647933** as the code state of record. That is a concrete reason never to rewrite CTSpinoPelvic1K reachable history; purge only the unreferenced proposals/ orphans.

6. **The NeurIPS camera-ready cites a commit that does not exist.** It says "OpenSpineConsortium/spinopelvic-seg at commit 50b209f", but that repo has only fd8d565 and c105981. 50b209f (2 May 2026) is in the private spinesurg-ct-nnunet, and arXiv v1 cites that private repo. Fix the text. Pushing spinesurg-ct-nnunet refs publicly would expose Part B code.

7. **Apache-2.0 covers more than CTSpinoPelvic1K.** XRSpinoPelvic1K (localize.py, oblique.py), the site repo (detector code and the historical ONNX weights), OpenSpineToolkit and spinopelvic-seg are Apache-2.0 too.

8. **Implementation details that would break or leak the site edit.** remote.js stores the endpoint under the localStorage key "levelIdService" (lines 19-20), so any rename must change both lines. xr.js imports modelLevels, so remote.js and xr.js must change in one commit with the ?v= cache-busters bumped. For CTSpinoPelvic1K, `git rm -r --cached paper/cns2026` keeps the local deck files, which stay ignored by the existing exclude rules. The other deleted scripts must be moved out of the working tree before `git rm`, or `git add -A` re-stages them.

9. **Commit messages that stay in history:** 2c0def3 names the invention-disclosure package; the site's ea0086c/5559d87 says "the model runs behind the level service". Both are existence-level only.

Not verified: whether XRSpinoPelvic1K was public from creation (needs the owner's Security log), and whether jsDelivr holds cached copies. I did not probe jsDelivr, because a request would create a cached copy. My own background full-history -G search of CTSpinoPelvic1K did not finish; I relied on the searcher's reachable-history scan (removed_strong.json), which I reviewed and which shows no Part B content outside the items listed.
