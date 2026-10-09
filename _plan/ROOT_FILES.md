# ROOT_FILES: what the root README.md, CLAUDE.md and INDEX.md must say

Written 2026-10-08 for `C:/Users/grego/OneDrive/Desktop/spine-program/`. The builders write the three root files from this
specification; `PLAN.md` is the source of every folder name, title, reader label and first step quoted below.

---

## README.md (the repository's front page)

1. **What this is.** One private repository that seeds a set of Claude Code projects, one per folder, dividing the spine
   programme of the Open Spine Consortium (Wayne State University School of Medicine / Detroit Medical Center, Department of
   General Surgery) into self-contained units. Built 2026-10-08 from the laptop folders, the memory notes and one read-only
   pass over the grid; nothing on the grid was written and nothing here is imaging data or a model weight.
2. **The one-paragraph programme** (from `HANDOFF/README.md` section 1, in the root's own words): a CT dataset of 802
   abdominopelvic records (CTSpinoPelvic1K, release v11, Zenodo 10.5281/zenodo.22797014) built to ask whether local
   morphology can name a vertebra without counting from C2; a public measurement toolkit (OpenSpineToolkit); a private
   convolutional-recurrent network (SchwingNet) that names lumbar levels on intraoperative C-arm exposures, held out on one
   unseen C-arm at 595 of 617 lateral vertebrae (96.4 %; `HANDOFF/RESULTS_CATALOG.md` A2.1); a census of transitional anatomy
   across 21,622 public CTs; a data platform of 211 sources migrating to Ceph; and the student framework (Beethoven, the lab
   recipe) that lets medical students work on the grid.
3. **The table of folders**, exactly the table of `PLAN.md` section 1 (rank, folder, title, reader, likelihood in one line,
   depends on), followed by one sentence per folder giving its goal (the first sentence of each "Goal" paragraph in
   `PLAN.md` section 3) and its first step.
4. **How to start a project from a folder.** Open the folder as a Claude Code project; read `CLAUDE.md`, then `README.md`,
   `STATUS.md`, `TODO.md`; `MEMORY.md` indexes `memory/` with every note's status (CURRENT, DATED, PARTLY SUPERSEDED,
   SUPERSEDED, LEAKED, RECORD ONLY, DORMANT); `MANIFEST_GRID.md`, `MANIFEST_CODE.md` and `MANIFEST_LOCAL.md` say where
   everything the folder does not hold lives (grid path with migration state, repository with URL / branch / commit / files,
   laptop file kept by path with the reason). The only references outside a folder are grid paths, code repositories and
   sibling folders of this repository.
5. **What is deliberately not here.** Imaging data, arrays and weights (on the grid, Zenodo, Hugging Face or in their public
   sources; every item recorded by path in the owning folder's manifest); anything under `.git`, environments, caches, logs
   over 2 MB, files over 25 MB; credentials (a rotation list in `_plan/PLAN.md` section 6, paths only); personal and
   administrative material; the U251 and LITT studies; `HANDOFF/GREG_ONLY/`, `private_ip/` and the invention-disclosure
   material (referenced by path from 01); student names and usernames, researcher and personal e-mail addresses (redacted
   copies where the research content matters). The full list with reasons is `_plan/EXCLUDED.md`.
6. **Readers.** Which folders are student-safe (03, 04, 05, 12; 06, 10 and the guides of 11 after redaction and after Greg
   confirms `HANDOFF/OPEN_QUESTIONS.md` A29, A30) and which are Greg-only (01, 02, 07, 08, 09, the Beethoven notes of 11, 99);
   the repository itself is private and the label is about hand-outs.
7. **Where the plan is.** `_plan/PLAN.md` (the division, the rules, the projects, where the two proposals disagreed, the
   decisions reserved to Greg, the unknowns), `_plan/DISPOSITION.tsv` (every inventory row and where it went),
   `_plan/EXCLUDED.md`, `_plan/ROOT_FILES.md` (this specification).
8. **The grid in one paragraph** (from `_plan/PLAN.md` section 3, folder 10): HOME `/wsu/home/go/go24/go2432` at 4,050.75 GB of a
   4,294.97 GB soft limit on 2026-10-08; Ceph `/rs/rs_grp_oschome/go2432` at 7 of 20 TB; batches B00, B02, B06, B08, B14 verified
   and cut over, B01 and B03 absent or meta-only, B04, B07, B09 copying at 22:20 UTC, B10 and B11 not started, B12 dropped, B13
   not run, no batch finalized; the per-batch truth is `~/spinesurg-ct-nnunet/data_platform/plan/runs/<B>/STATUS`. Known losses:
   the TCIA CT Colonography raw and NIfTI trees (1,057 GB) are on neither volume; CTPelvic1K datasets 1-5 absent; the
   `allspine_v2..v5c` banks deleted 2026-09-20.
9. **Dates and commits** of the sources this seed was cut from: `spinesurg-ct-nnunet` `L6_Class` 097933a; `CTSpinoPelvic1K`
   `master` 7ddfe38 (working tree modified); `OpenSpineToolkit` `main` cb43197; `XRSpinoPelvic1K` `main` 4f22935;
   `OpenSpineConsortium/beethoven` 2f90319; `beethoven-vscode` 8d7fc65; `openspineconsortium.github.io` local c1800f8 behind origin
   a17ea39; the memory folder's newest note 2026-10-08 16:43; the grid pass 2026-10-08 22:20 UTC.

The README never uses the banned word, names no student or username, carries no e-mail address, and states the affiliation
as General Surgery.

---

## CLAUDE.md (the working context every project inherits; each folder's own CLAUDE.md restates these rules in its own words
and adds its folder-specific traps)

**Opening paragraph.** What the repository is (one sentence), that each numbered folder is a self-contained project, and
that the reader must open the folder's `CLAUDE.md` first because the root rules bind everywhere and the folder adds its own.

**Read first.** `_plan/PLAN.md` sections 1-2; the folder's `CLAUDE.md`, `README.md`, `STATUS.md`, `TODO.md`; `docs/handoff/README.md`
section 5 (the ten rules as the handoff wrote them) and `docs/handoff/RESULTS_CATALOG.md` "How to read a row".

**The standing rules** (every one restated, in the root's own words, with the file it comes from):

1. Words and style: never the banned word (the French-derived word for where data came from): write origin, lineage, source,
   where it came from; no fractional version numbers, fold a change into the next integer version; figure captions at most 60
   words, the argument in the text; plain sentences; matrix tables in solid black with at most one outlined mark; slides never
   use sideways bar charts. Affiliation is General Surgery (Wayne State University School of Medicine / Detroit Medical Center),
   never Neurosurgery. Ashley Schehr is a person, never a product name; the product is Beethoven.
2. Every number carries its file. A count, date, path or claim names the file it comes from; what no file records is written
   "not recorded"; say plainly what is not known rather than guess.
3. Check outside the computation. The recurring failure in this programme is a number that is wrong but plausible: three
   estimators produced finite, reasonable values from the wrong bone, the wrong surface or the wrong label map, and internal
   consistency (PI = SS + PT) held throughout. Compare with published values, an independent implementation, the spread of the
   distribution (not its median), a published prevalence; render the mask; test a tidy explanation before believing it.
4. Labels and orientation. Two label schemes exist (release v11: L1 = 20 ... L5 = 24, sacrum 26, hips 30 / 31, femurs 32 / 33;
   the legacy map: L1 = 1, femurs 11 / 12) and mixing them does not raise: "femur_left" comes back T4. Call
   `ostk.labels.labels_for(volume)`, never import a fixed map. Identifier 29 (the carved S1) is retired in v11 and dissolved
   into 26; any code that gates on 29 goes with it. Case ids are zero-padded (`zfill(4)`) in the release and were not in the old
   CSVs. Canonicalise to RAS to analyse; never reorient when writing a label (`as_closest_canonical` + `nib.save` transposes a
   label away from its CT). CT volumes are stored P, I, R.
5. Held out means the person was never seen by the checkpoint or any ancestor; a render inherits its CT's person; unknown is
   not clean. Every quoted score goes through `ssn:tools/eval_gate.py`. Never quote the leaked banks (allspine v2, v6, v7, v8
   for VerSe, `anchor_drr`, `vindrps`) or the numbers marked LEAKED, SUPERSEDED or RECORD ONLY in `docs/handoff/RESULTS_CATALOG.md`.
6. Pre-register, then score. Write the rule and its success criterion before the run, hash it, stamp every output row with
   the hash; a number produced before the freeze is calibration; comparators are pre-specified from the literature and never
   tuned; manuscript numbers enter through a manifest key, never typed.
7. The grid's login node runs nothing. Every computation, render, plot and download is an `sbatch` job; warrior kills python,
   rsync, node, pip and conda by name; no container command on warrior and nothing of ours under its `/tmp`. `sbatch -D <dir>`
   (a relative `--output` resolves against the submit directory); `afterany`, not `afterok`; IPC under `/dev/shm` (compute-node
   `/tmp` is swept); large outputs on Ceph `/rs/rs_grp_oschome/go2432/`, not HOME; record a job before cancelling it; write grid
   bash for bash 4.2; partition `reqp --qos=requeue` for CPU, `gmsap` / `gvohp` for GPU; the python with nibabel and scipy is
   `~/mambaforge/envs/spineps/bin/python`. Submit, estimate the wall time, write the job ids and ETA to the resume file, stop.
8. What stays private. SchwingNet and all level-identification code, text, figures and weights, FluoroCap, and the
   `spinesurg-ct-nnunet` and `XRSpinoPelvic1K` repositories; nothing about them goes public until Greg says so; run
   `ssn:tools/disclosure_audit.py` before any talk, upload or submission; for the CNS talk use only
   `CNS2026_Schwing_NotAllSpines_public_v12.pptx`.
9. Data directives. Use all of a public dataset; a download budget is not a criterion; every truncation is fixed or justified
   in writing before a rerun; a leaked initialisation is fixed by retraining, never disclosed as a caveat; FluoroCap is out of
   training; identity comes from metadata first and the file name last; the IRB umbrella (HPR 2026-269) covers only public,
   de-identified data downloadable without an agreement.
10. Git, network and credentials. `CTSpinoPelvic1K`: commit directly to master, push to `origin` and `osc`; `OpenSpineToolkit`:
    branch `main`, both remotes; this repository: commit only when Greg asks and Greg pushes. Network (git push, ssh, rsync,
    Hugging Face) goes through `wsl -e bash -lc '...'`; `ctsp:paper/mpda/make_submission.py` is the one exception and runs from
    Windows. Tokens are read from files, never echoed, never put on a command line or in `sbatch --export`; nothing under
    `C:/Users/grego/.beethoven-vendor` is read. Write scripts as files and run them by path (heredocs collapse backslashes);
    never name a scratch script `numbers.py`, `io.py` or `pdb.py`.
11. The page limit of the dataset article is 10 published pages and only `build.sh --reprint` measures it; read the whole
    build output, because LaTeX emits a PDF and a page count on top of a broken table.
12. Personal data. No student name or username, no researcher or personal e-mail address enters any file of this
    repository; where a source carries one, the redacted copy is used and `MANIFEST_LOCAL.md` records the redaction by kind.

**How the folders relate.** One line each: 10 is the dependency of all; 04 blocks 05; 02 feeds 01's PREREG and consumes 06;
08 serves 01 and 05; 09's per-case form is 01's S5 / S8 scaffold; 12 waits on 01 S2, 04 and 05; 11 waits on 10; 99 is never run.

**How to be useful here** (from `ctsp:CLAUDE.md`, restated): check against something outside the computation; when a tidy
explanation presents itself, test it before believing it; say plainly what is not known; render the mask.

---

## INDEX.md (one line per folder, machine-friendly)

A table with columns rank, folder, title, reader, goal (one sentence), first step (the step 1 of `PLAN.md` section 3 with
its gate), links to the folder's `README.md`, `STATUS.md`, `TODO.md`, `MANIFEST_GRID.md`, and the counts of its `DISPOSITION.tsv`
rows (copy / reference / not copied) from `PLAN.md` section 1. After the table: one line pointing at `_plan/` and one line
giving the build date (2026-10-08) and the source commits listed in README item 9. Nothing else.
