# 03_ctspinopelvic1k_dataset — working context

Project 03 of the spine programme (`../_plan/PLAN.md` section 3, rank 3; reader: student-safe after the
redactions recorded in `MANIFEST_LOCAL.md`). Written 2026-10-08. Every number here names the file it
comes from; "not recorded" means no file on the laptop or the grid records it.

## The goal, in one paragraph

Close out CTSpinoPelvic1K, the public CT dataset of 802 abdominopelvic records with per-level vertebrae,
ribs, sacrum, hips and femora, released as v11 (VerSe-native ids, identifier 29 retired; Zenodo
10.5281/zenodo.22797014, published 2026-09-18 per `docs/handoff/RESULTS_CATALOG.md` Part F header and
`manuscripts/mpda/cover_letter.md`). Three deliverables remain: (1) the Medical Physics Dataset and
Software Article (`manuscripts/mpda/main.tex`; third packet built 2026-09-25; whether it was uploaded is
not recorded, `TODO.md` step 1); (2) the accepted NeurIPS 2026 Evaluations and Datasets paper 3474
(`manuscripts/neurips_camera_ready/`; 134 `[pending]` slots and headline defects A and B still in the main
text, `CAMERA_READY_CHANGES.md` items 19-21); (3) the release documents brought to v11 and the Hugging
Face mirror, still v10 with id 29 on 2026-09-27 (`memory/hf-mirror-is-v10.md`), either moved to v11 or
dropped from the text. Everything else in this folder (QC tables, review records, the earlier manuscript
lineage, the CNS 2026 deck) is the record that makes those three defensible.

## Read first

1. `README.md` (state on 2026-10-08, success criteria, how this folder relates to 04, 05, 06, 10).
2. `TODO.md` (ordered steps with gate, number, dependency, decider) and `STATUS.md` (every result in
   hand with its id, file and rigor mark).
3. `manuscripts/mpda/REPRODUCE.md`: the pipeline from labels to article, and its traps. Its section 0
   still says "v10 ... S1=29"; that line is stale (`TODO.md` step 4).
4. `docs/ctsp/SPINOPELVIC_ESTIMATOR.md` and `docs/ctsp/LEVEL_MORPHOMETRY.md`: how the numbers are
   computed, the defects found, and the ones still open.
5. `docs/handoff/RECIPES.md` section 9 (the measurement, figure and article chain) and section 0 (how
   work reaches the grid).
6. `MEMORY.md`, then the notes in `memory/` it points at; each note carries its status on its first
   line, and a result file always wins over a note.

## Where things are

- **This folder.** `manuscripts/` (the article, the camera-ready, the as-submitted packages, the earlier
  drafts, the CNS 2026 decks and generators), `docs/` (`ctsp/` the repository's working knowledge,
  `ctsp_root/` the repository's root documents, `release/` the deposit sidecars and ITK-SNAP descriptors,
  `handoff/` the eight student-readable HANDOFF files of 2026-10-08 plus the topic-6 working note and
  `EXTRACTS.md`), `results/` (QC tables, review records, the May 2026 NeurIPS benchmark outputs),
  `code/` (case-fix scripts, the LSTV review tool, the CT competitor benchmark, container build files),
  `memory/` (55 notes), `figures/`. The manifests `MANIFEST_GRID.md`, `MANIFEST_CODE.md`,
  `MANIFEST_LOCAL.md` say what is on the grid, in which repository, and what was copied or left out.
- **The grid** (`MANIFEST_GRID.md`). HOME = `/wsu/home/go/go24/go2432`; Ceph = `/rs/rs_grp_oschome/go2432`.
  The only grid copy of the 802 CTs and the v11 labels is
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` (196,195,055,488 B, 2,417
  files, batch B02 VERIFIED). The v11 build workspace with the Zenodo upload state is
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` (restricted). The public
  repository checkout `/wsu/home/go/go24/go2432/CTSpinoPelvic1K` is at a0c5139, behind the laptop's
  7ddfe38.
- **Repositories** (`MANIFEST_CODE.md`). `CTSpinoPelvic1K` (public; `origin` =
  github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K, `osc` = github.com/OpenSpineConsortium/CTSpinoPelvic1K;
  master 7ddfe38) holds every script, slurm wrapper, test and deposit tool; nothing tracked there was
  copied here except the documents a reader opens first. `spinesurg-ct-nnunet` (private, L6_Class
  097933a) holds the nnU-Net tools, the benchmark and the HANDOFF. `OpenSpineToolkit` (public, main
  cb43197) is the measurement library. `OpenSpineConsortium/spinopelvic-seg` (main c105981) is the
  public pseudolabeller the camera-ready cites.

## The rules that bind this folder (the programme's standing rules, in this folder's words)

1. **Words.** Never the French-derived word for where data came from; write origin, lineage, source,
   or "where it came from" (`memory/writing-preferences.md`). No fractional version numbers: a changed
   deposit is the next integer Zenodo version (`docs/handoff/RECIPES.md` section 9 item 9). Figure
   captions at most 60 words; the argument goes in the text (`memory/figure-captions-terse.md`). Matrix
   tables in solid black with at most one outlined mark; slides never sideways bars. Plain sentences.
   The affiliation is the Department of General Surgery, Wayne State University School of Medicine /
   Detroit Medical Center, never Neurosurgery (`memory/user-affiliation-general-surgery.md`; the March
   2026 draft `manuscripts/spinesurgct_arxiv_2026-03/SpineSurgCT_arxiv.tex` line 56 still says
   Neurosurgery and is kept as history, `MANIFEST_LOCAL.md`). Ashley Schehr is a person, never a
   product name.
2. **Every number carries its file.** A count, a date, a path, a claim names the file it comes from;
   what no file records is written "not recorded". Manuscript numbers enter through the audit chain
   (`manuscripts/mpda/audit_ms.py` checks every number in the text against its CSV), never typed.
3. **Check outside the computation.** The recurring failure in this dataset is a number that is wrong
   but plausible: three estimators returned finite, reasonable values from the wrong bone, the wrong
   surface or the wrong label map, and PI = SS + PT held throughout an error that moved sacral slope
   by 9 degrees and lordosis by 12 (`docs/ctsp/SPINOPELVIC_ESTIMATOR.md` sections 1-4). Compare with
   published values (Veilleux, Hasegawa, Panjabi), an independent implementation (ostk against the
   extraction scripts, `docs/ctsp/OSTK_VS_EXTRACTION.md`), the spread not the median (21 % of L3 canal
   depths below any living value while the median sat on the published mean,
   `docs/ctsp/LEVEL_MORPHOMETRY.md`), a published prevalence; and render the mask (three analytically
   reasonable L5 end-plate fixes were all wrong until one render showed what was retained).
4. **Labels and orientation.** Two label schemes exist and mixing them does not raise: the release is
   VerSe-native (L1 = 20 ... L5 = 24, sacrum 26, hips 30/31, femurs 32/33) and the legacy map puts L1 at
   1 and the femurs at 11/12; "femur_left" resolved against the wrong map comes back T4. Call
   `ostk.labels.labels_for(volume)`, never import a fixed map (`memory/label-scheme-v4-vs-ostk.md`).
   Identifier 29 (the carved S1) is retired in v11: dissolved back into 26, never renumbered, and code
   that gates on 29 must go (`memory/s1-carve-changed-spinopelvic.md`; `select_anchor_cases.py` once
   swapped a Figure 2 case silently on a stale check). Case ids are zero-padded in the release and were
   not in the old CSVs: `zfill(4)` before any diff. Canonicalise to RAS to analyse; never reorient when
   writing a label (`as_closest_canonical` + `nib.save` transposes a label away from its CT,
   `memory/never-reorient-when-writing-labels.md`; volumes on disk are P,I,R,
   `memory/ct-volumes-are-pir-not-ras.md`).
5. **Held out means the person was never seen.** A score counts only if the patient key was in neither
   the training nor the validation set of the checkpoint or any ancestor; every quoted score goes
   through the evaluation gate (`ssn:tools/eval_gate.py`); the leaked banks (allspine v2, v6, v7, v8 for
   VerSe, `anchor_drr`, `vindrps`; `docs/handoff/GLOSSARY.md`) are never quoted. In this folder the
   relevant case is the NeurIPS segmentation numbers: all computed on the April 2026 release with a
   record-level split, not on v11 (`STATUS.md` F.46).
6. **Pre-register, then score.** The rule and its success number are written and hashed before the
   run; a number produced before the freeze is calibration. The dataset article allows no hypothesis
   test (`manuscripts/mpda/PLAN.md`); counts only.
7. **The login node runs nothing.** Every computation, render, plot and download is an `sbatch` job
   (warrior kills python, rsync, node, md5sum and others by name); `sbatch -D <dir>` (a relative
   `--output` resolves against the submit directory); chain with `afterany`, never `afterok`; IPC under
   `/dev/shm`, never `/tmp`; large outputs on Ceph; grid bash is 4.2 (`memory/grid-bash-4-2-quoting.md`);
   no container command on warrior and nothing of ours under its `/tmp`. The `ctsp:slurm/*.sh` wrappers
   still point at `data/v5_final` and use `-q primary`: edit before reuse (`docs/handoff/RECIPES.md`
   section 9 item 3).
8. **What stays private.** SchwingNet and all level-identification code, text, figures and weights stay
   private; nothing of them is in this folder, and nothing about them goes into any document here.
   For the CNS talk only `manuscripts/talks/cns2026/CNS2026_Schwing_NotAllSpines_public_v12.pptx` may be
   shown (`memory/cns-deck-v2-2026-09-25.md`). The talk generators in `manuscripts/talks/cns2026/` are
   excluded from the public repository and must never be pushed to it.
9. **Use all of a public dataset.** Every truncation is fixed or justified in writing before a rerun; a
   leaked initialisation is retrained, never disclosed as a caveat (`memory/data-directives-2026-09-23.md`,
   `memory/no-unexplained-subsets-fix-not-disclose.md`). Identity comes from metadata first and the
   file name last (`memory/key-patients-from-metadata-not-filenames.md`).
10. **Git, network, credentials.** In CTSpinoPelvic1K, commit directly to master, no feature branches,
    and push to both `origin` and `osc` (`memory/commit-directly-to-master.md`,
    `memory/push-both-github-remotes.md`); commit only when Greg asks. In spine-program itself the account
    doing the work pushes only its claim branch `claude/<issue>` and Greg merges (root `CLAUDE.md` rule 10).
    On Greg's laptop, network (git push, ssh, Hugging Face, Zenodo) goes through
    `wsl -e bash -lc '...'`; the one exception is `manuscripts/mpda/make_submission.py`, which shells out
    to `wsl` and runs from Windows. Tokens are read from files only (`~/.zenodo_token`, the Hugging Face
    token files), never echoed, never on a command line. Write scripts as files and run them by path;
    inline heredocs collapse backslashes (`memory/bash-heredoc-backslashes.md`).

## Traps specific to this folder

- **The page limit is 10 published pages and only `build.sh --reprint` measures it.** The submission
  form is about 25 pages because it is double-spaced. Read the whole build output: LaTeX prints a PDF
  and a page count on top of a broken table (`manuscripts/mpda/REPRODUCE.md`; `memory/journal-figure-and-style-rules.md`).
- **The laptop deposit sidecars are v10.** `docs/release/dataset_labels.json` names the scheme "v10" and
  maps `S1` to 29; `docs/release/KNOWN_ISSUES.md` is headed v10. The v11 deposit staging is only on the
  grid (`MANIFEST_GRID.md`, `s1v11`). Do not read these sidecars as the v11 state.
- **Four morphometric CSVs were written on v10 labels** (`pelvic_shape.csv`, `transition_morphometrics.csv`,
  `degenerative.csv`, `opportunistic.csv`; `STATUS.md` F.44): recompute on v11 with project 05 before any
  new sacral or lumbosacral number.
- **ostk on v11 labels silently falls back to the whole sacrum for S1** (`docs/handoff/RESULTS_CATALOG.md`
  G.3) and its canal mask carries the 1b7005c regression (G.2): do not trust an ostk PI or posterior body
  height computed after 2026-09-10 until project 04 has fixed both.
- **`spine_tampering.csv`, `morphometrics/annotator_names.csv` and the review ledgers carry student
  identities.** They are not in this folder; the review tables that are here carry `annotator_NN` tokens
  (`MANIFEST_LOCAL.md`). Never copy a ledger from `anonymous-mlhc/CTSpinoPelvic1K-reviews-*` into this
  folder.
- **The HANDOFF copies use path prefixes** (`ctsp:`, `ssn:`, `sn:`, `mem:`, `Desktop/`) defined in
  `docs/handoff/README.md` section 0 as laptop folders. `docs/handoff/PREFIXES.md` resolves each one to a
  repository at the commit named in `MANIFEST_CODE.md`, to a path in this folder, or to the grid. The copied
  notes and scripts that still quote a laptop path are listed in `MANIFEST_LOCAL.md` section 3.6 with the
  line to change; this folder depends on no laptop path.
- **NeurIPS numbers are April-release numbers.** The camera-ready's segmentation results come from the
  1,153-record April 2026 release with a ten-class scheme merged to nine and a record-level split; the
  v11 summaries (Appendix J) were never produced because their jobs were cancelled on 2026-09-27
  (`STATUS.md` F.46, F.49).
- **Case 0500 sits in the lumbarization stratum on a phantom L6** (no id 25 in its label; `STATUS.md`
  F.17) and the splitter never read the lumbar count. Say so wherever the splits are described.

## How to be useful here

Ask Greg the six questions in `TODO.md` step 1 before editing either manuscript. Then work the steps in
order; each has a gate and a pre-stated number. When a tidy explanation presents itself, test it before
believing it: the 128 low pelvic incidences had an innocent reading (anteverted pelvis, lost sign) that
was wrong, and the distribution showed a second surface (`docs/ctsp/SPINOPELVIC_ESTIMATOR.md`). Say
plainly what is not known; `OPEN_QUESTIONS.md` rows D3-D5 and E2-E19 are the preferred form.
