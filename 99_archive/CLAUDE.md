# 99_archive: working context

Written 2026-10-08 for `spine-program/99_archive/`. Reader: Greg only (this folder holds SchwingNet deck history and
private draft history). Nothing in this folder is run, trained, scored or quoted.

## The goal in one paragraph

Keep, dated and never as a source of a quotable number, the work that was superseded, refuted or left dormant, with the
reason each item is here and what replaced it, so that nobody repeats it. That means: FluoroCap (the harvest of
published fluoroscopy figures; 4,979 figures, 10,281 panels, 72.8 % of panels with zero pixel residual, so reproductions
of printed figures, not fluoroscopy; out of training by directive D1; a test set at most; `memory/fluorocap-dataset.md`,
`docs/handoff/DATASET_USAGE.md` section 2.1 row "FluoroCap literature panels"), the generative translation routes
(SDXL img2img, CUT, CycleGAN, ADDA; all refuted; `memory/fluorogen-synthetic.md`, `docs/handoff/RESULTS_CATALOG.md` C4.11),
the refuted losses and rules (Star Temporal Classification, C1.7; R + C = 22, D.24; the pelvic Castellvi cues, D.21;
sacral foramina counting, F.39), one page `SUPERSEDED_NUMBERS.md` that lists every v2-lineage, leaked or wrong-bank number
with its replacement, the dated session checkpoints under `docs/checkpoints/`, the superseded manuscripts, builds,
scaffolds and decks by path in `MANIFEST_LOCAL.md`, the teaching-talk outlines under `docs/mans_talk/`, the early scratch of
May 2026, and `LITERATURE_BY_PATH.md`, the list of every third-party PDF kept by path with its identifier (library access
was cut on 2026-06-30, so the paths matter).

## Where things are

- This folder: `README.md` (what is here, the superseded-by-what chains, the five do-not-carry-forward lists),
  `STATUS.md` (the record-only, superseded, leaked and refuted results with their catalog ids and rigor marks),
  `SUPERSEDED_NUMBERS.md`, `LITERATURE_BY_PATH.md`, `TODO.md` (the few decisions that remain; nothing to run),
  `MEMORY.md` + `memory/` (28 notes with their status headers), `MANIFEST_GRID.md`, `MANIFEST_CODE.md`,
  `MANIFEST_LOCAL.md`, `docs/checkpoints/` (the dated handoffs and resumes of 2026-09-14 to 2026-09-27),
  `docs/fluorocap/` (protocol, README, QC and the pathology-source sweep), `docs/handoff/` (the eight student-readable
  files of the 2026-10-08 handoff, whole, plus the extracts of the Greg-only sections assigned to this folder),
  `docs/mans_talk/`, `docs/early_scratch_2026-05/`, `manuscripts/talks/` (the one copy of the AACA Tech Fair deck),
  `code/fuc/` (a 2026-02-14 DICOM viewer bug note and its fixed JavaScript; a record, not a tool).
- The grid: HOME `/wsu/home/go/go24/go2432` and Ceph `/rs/rs_grp_oschome/go2432`; every path this folder names, with
  what it holds, its size where a file records one, its migration state and whether a job verified it, is in
  `MANIFEST_GRID.md`. The grid is read only with `ls`, `stat`, `cat` of small files and `squeue`, through
  `wsl -e bash -lc 'ssh grid ...'`; never `du`, `find` over trees, python or anything heavy on the login node.
- The repositories: `MANIFEST_CODE.md` (URL, branch, commit, the files that matter). The prefixes the copied records use
  (`ssn:`, `sn:`, `ctsp:`, `ostk:`, `xrsp:`, `mem:`) resolve to those repositories at the stated commits
  (spinesurg-ct-nnunet L6_Class 097933a; CTSpinoPelvic1K master 7ddfe38; OpenSpineToolkit main cb43197; XRSpinoPelvic1K
  main 4f22935), never to a laptop. Laptop paths appear only in `MANIFEST_LOCAL.md`, as a record of where each copy came
  from, and inside the copied historical documents, where they are the paths of their day and nothing depends on them.
  The copied handoff's own prefix table is keyed for this repository in `docs/handoff/PREFIX_KEY.md`; the seven
  inventories of 2026-10-08 that the manifests cite by short name (`carm_hospital_path`, `memory_and_handoff_map`,
  `grid_manifest`, ...) are in `../_plan/inventories/`, one `.md` and one `.tsv` each (row N = TSV row N after the header).

## The traps that bind this folder

1. **Nothing here is a source of a quotable number.** Every number in `docs/checkpoints/`, `docs/fluorocap/`, the decks and
   the dormant memory notes is RECORD ONLY, SUPERSEDED, LEAKED or REFUTED unless `docs/handoff/RESULTS_CATALOG.md` says
   CURRENT. Before any number leaves this folder, read `SUPERSEDED_NUMBERS.md` and the catalog row it names.
2. **The dated checkpoints contradict later files on purpose.** `docs/checkpoints/DAILY_REPORT_2026-09-22.md` prints
   98.2 % lateral exact level (the v2-lineage cross-validation, A3.11); the current number is 601 / 617 = 97.4 % (A3.1).
   `docs/checkpoints/HANDOFF_2026-09-21_PM_ctsp_audit_track.md` prints "DeepFluoro 100 % / 95.2 %" (a same-device number).
   Read them as history.
3. **FluoroCap is figures of published articles.** 72.8 % of panels have zero pixel residual against the printed figure;
   the panel accuracy of 19.7 % (C1.11) is an agreement with weak labels, not an accuracy. FluoroCap is out of every
   training set by directive D1 (`memory/data-directives-2026-09-23.md`), and 2,100 FluoroCap crops still sit in the
   C-ArmLSpine fold banks (`docs/handoff/DATASET_USAGE.md` sections 0 and 3.2); that is 01's problem, recorded in `TODO.md`.
4. **The decks.** The v3, v9 and v10 CNS 2026 decks disclose SchwingNet and the unfiled sweep: private, never shown
   (`manuscripts/talks/README.md`). The Tech Fair deck's title slide says "Department of Neurosurgery" and "NIH F30 Fellow":
   historical, and wrong under the standing affiliation rule; nothing is reused from it without saying General Surgery.
5. **Two label schemes, identifier 29, zero-padding, orientation.** The CT work this archive refers to uses the v11
   VerSe-native scheme (L1 = 20 ... L5 = 24, sacrum 26, hips 30 / 31, femora 32 / 33); the legacy ostk map puts L1 at 1
   and resolving a name against the wrong map returns a finite wrong answer ("femur_left" comes back T4). Call
   `ostk.labels.labels_for(volume)`; never import a fixed map. Identifier 29 (the v10 carved S1) is retired in v11 and
   any code that gates on it goes with it. Case ids are zero-padded (`0001`) in the release and were not in old CSVs:
   `zfill(4)` before diffing. Volumes are canonicalised to RAS to analyse and never reoriented when written. Old
   documents in this folder predate some of these rules; they are not corrected.

## The standing rules, in this folder's words

- Never the banned word (the French-derived word for where data came from); write origin, lineage, source, or where it
  came from. The two mentions in the copied `RESUME_2026-09-22_PM.md` were rewritten; a grep over this folder finds none.
- No fractional version numbers of our own; a change folds into the next integer version. Release names that exist on
  disk are spelled as they are.
- Figure captions at most 60 words; the argument goes in the text. Plain sentences.
- Every count, date, path and claim names the file it came from; what no file records is written "not recorded".
- Check outside the computation: the recurring failure in this programme is a number that is wrong but plausible, and
  internal identities (PI = SS + PT) did not catch a shared bad landmark. Published values, an independent implementation,
  the spread rather than the median, a published prevalence, a rendered mask.
- Held out means the person was never seen by the checkpoint or any ancestor; a render inherits its CT's person; unknown
  is not clean. Every quoted score goes through `tools/eval_gate.py` in spinesurg-ct-nnunet. Nothing is quoted from the
  leaked banks (allspine v2, v6, v7, v8 for VerSe, `anchor_drr`, `vindrps`); most of what is in this folder was measured
  on them.
- Pre-register, then score: the rule and its success number are written and hashed before the run; a number produced
  before the freeze is calibration; manuscript numbers enter through a manifest key, never typed.
- Nothing runs on the grid's login node. Every computation is an `sbatch` job with `sbatch -D <dir>`, chains use
  `afterany`, IPC goes under `/dev/shm`, large outputs go to Ceph, grid bash is written for bash 4.2. This folder submits
  nothing.
- SchwingNet and all level-identification code, text, figures and weights stay private, as do FluoroCap, the
  spinesurg-ct-nnunet and XRSpinoPelvic1K repositories and the decks named in trap 4.
- Use all of a public dataset; every truncation is fixed or justified in writing before a rerun; a leaked initialisation
  is fixed by retraining, never disclosed as a caveat.
- On Greg's laptop, network (git push, ssh, rsync, Hugging Face) goes through `wsl -e bash -lc '...'`. Tokens are read
  from files only, never echoed or put on a command line; nothing under the vendor key folder is read.
- In the code repositories this folder names, commit only when Greg asks; CTSpinoPelvic1K commits go directly to master
  and are pushed to both remotes. In spine-program itself the account doing the work pushes only its claim branch
  `claude/<issue>` and Greg merges (root `CLAUDE.md` rule 10).
- Ashley Schehr is a person (a published co-author), never a product name; the student product is Beethoven.
- The affiliation is the Department of General Surgery, Wayne State University School of Medicine / Detroit Medical
  Center, never Neurosurgery. Four historical documents named in `MANIFEST_LOCAL.md` say Neurosurgery; they are not edited.
