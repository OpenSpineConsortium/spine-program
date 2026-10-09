# BUILD_RECORD: how this tree was built on 2026-10-08

## 1. Sources and inventories

The tree was cut from the laptop folders, the memory notes and one read-only pass over the grid, as `PLAN.md` "Sources"
lists them: spinesurg-ct-nnunet `L6_Class` 097933a (private), CTSpinoPelvic1K `master` 7ddfe38 (working tree modified),
OpenSpineToolkit `main` cb43197, XRSpinoPelvic1K `main` 4f22935 (private), the other spine folders of the Desktop, the loose
Desktop files, the memory folder (newest note 2026-10-08 16:43) and its redacted copies in `spinesurg-ct-nnunet/HANDOFF/context/`
with the statuses of `HANDOFF/context/INDEX.md`, and the grid (HOME `/wsu/home/go/go24/go2432`, Ceph `/rs/rs_grp_oschome/go2432`)
read with `ls`, `cat` of small files and `squeue` at 22:20 UTC; nothing was written on the grid and nothing heavy ran on the
login node.

Seven inventories were written first, between 18:28 and 18:50, in the build session's scratchpad and copied into
`inventories/` (one `.md` and one `.tsv` each; `inventories/README.md` names them): the spinesurg-ct-nnunet repository, the
CTSpinoPelvic1K repository root and its 28 sibling folders, the other spine folders, the loose Desktop files, the grid, the
C-arm hospital path, and the memory-and-handoff map. Their 1,385 rows merged to 1,369 after 16 exact duplicates and were
dispositioned one by one into `DISPOSITION.tsv` (83 row-level overrides; `PLAN.md` section 1 gives the per-folder copy /
reference / not-copied counts).

## 2. The plan

Two independent proposals of the division arrived at the same twelve projects and one archive; `PLAN.md` section 4 records
where they disagreed (order, where the HANDOFF lives, the archive's number, a dozen rows) and what was decided. `PLAN.md`
(111,189 B, 19:39), `ROOT_FILES.md` (19:40) and `EXCLUDED.md` (19:43) were written before any folder was built;
`DISPOSITION.tsv` was last written at 21:37 and `GRID_MANIFEST_2026-10-08.md` at 21:35.

## 3. The first run (workflow run wf_e27ebb09-038) and its interruption

The first run built the folders in parallel from the plan: twelve of the thirteen project builds returned (every folder but
`01_carm_level_detection`; 01's folder is complete on disk with its eight documents, 3,549 lines in all, last written 21:41,
but its build result never reached the cache), seven verifications returned (02, 05, 06, 08, 09, 11, 12; each verdict
`needs-changes`) and one fix returned (12) before the account's session limit cut the run off. The returned results are in
`CACHED_RESULTS_2026-10-08.json` (keys `plan`, `builds[folder]`, `verifies[folder]`, `fixes[folder]`), redacted in the final
pass of the identities its own verify text quoted.

Build counts from the cache (files copied / bytes copied / files written / skipped as too large / unknowns recorded):
02: 416 / 41,059,871 / 8 / 6 / 14; 03: 1,020 / 133,268,961 / 9 / 2 / 13; 04: 68 / 6,997,442 / 14 / 0 / 9;
05: 390 / 66,823,778 / 8 / 1 / 11; 06: 1,239 / 63,636,987 / 13 / 5 / 14; 07: 204 / 80,732,741 / 10 / 0 / 12;
08: 293 / 36,351,975 / 9 / 4 / 12; 09: 111 / 25,317,393 / 10 / 8 / 9; 10: 687 / 47,288,380 / 19 / 5 / 10;
11: 187 / 10,887,624 / 9 / 0 / 12; 12: 67 / 5,575,308 / 12 / 0 / 10; 99: 79 / 7,224,703 / 17 / 0 / 12; 01: not cached
(its `MANIFEST_LOCAL.md` section 1 gives its own counts).

Verifiers' verdicts and what they found (the cache; the problems are summarised, each verify lists 7 to 10 issues):
- 02: student co-author names copied into two handoff files; A1.2 / A1.5 cited to a file that does not hold the numbers;
  laptop paths in 40 files; abbreviated grid paths; a miscount of redacted addresses (27 against 23); the one Hugging Face
  handle; 58 preview PNGs copied as evidence.
- 05: laptop paths in the copied handoff files; a voxel count cited to two scripts that do not contain it; 21 graded III / IV
  records quoted against 25 in the folder's own csv.
- 06: "546 review cases" cited to a file that holds 446 + 103 = 549; six citations to Greg-only files not in the folder;
  40 laptop paths inside `registry.json`; bare `Desktop/` locations; a CC-BY PDF with eleven author addresses; a
  collaborator's first name in a file name; a json count of 375 explained as 374; `$RS` abbreviations.
- 08: 162 laptop-path hits in 36 handoff copies; numbers cited to an inventory not yet in the repository; a `code_sha`
  attributed to card files that lack it; `SAMPLE_MODE` described as the gate when `clip` is the default; the untracked
  `polypose_cine.sh` unrecorded; two sizes for `anchor_drr` left unreconciled; a staff name and a faculty surname kept; no URL
  for spine-detector; 18 against 19 memory notes.
- 09: the eleven student usernames with counts in topic 6 and the handle in two more files; a PDF with the wrong affiliation.
- 11: laptop paths in 25 copies; `~` grid paths; a university address in the JEEHP draft and 16 student co-authors in two
  decks; stale-document claims attributed to the wrong file; a release ladder cited to a note that lacks it; "two" for three
  dated entries; four scripts without their copy-record line.
- 12: "13 .bin meshes under gallery/data/" against 12 under `assets/gallery/` in the clone; a CV in an application folder
  named in a student-safe file.

Although only 12's fix returned to the cache, the fixes of 02, 05, 06, 08, 09 and 11 had reached the disk before the cut:
each folder's `MANIFEST_LOCAL.md` carries "second pass" or "fix pass 2026-10-08" rows, and the final pass found their
corrections in place (02's author lists withheld; 05's step 8 reading 25 rows and F.7 cited to the script line and job log;
06's count 446 + 103 = 549 and `registry.json` free of laptop paths; 08's banners, names and `SAMPLE_MODE` wording; 09's
tally withheld; 11's `~` paths spelled out, the JEEHP address struck, the deck properties emptied). What those fixes left
undone is listed in section 4 below. 01, 03, 04, 07, 10 and 99 were never verified by the first run.

## 4. The critic's check and the final pass (this run)

A critic then read the whole tree (19,455 files checked) against the inventories and the plan and reported six left-behind
items and eight cross-project defects. The final pass performed only the calls that never returned; nothing already built was
rebuilt.

**Salvaged (six items, 33 files copied, one record written).** The AACA 2026 LSTV fusion pipeline (lstv-fusion 3c8f5c1, nine
tracked files) into `06/code/aaca_lstv_mri/lstv_fusion/`; the March-April 2026 sacralisation-synthesis line (SpineSurg-CT
0051074, five scripts) into `08/code/spinesurg_ct_0051074/` with its laptop-only QC result in
`08/results/superseded/sacralization_synthesis_2026-04/`; the untracked `slurm/polypose_cine.sh` and `tools/polypose/cine_render.py`
into `08/code/ssn_untracked_2026-10-08/`; the May 2026 NeurIPS submission source (anonymised) into
`03/manuscripts/neurips_as_submitted_2026-05/`; the two co-author review files and their PDF into `03/manuscripts/mpda/coauthor_review/`
(docx metadata emptied, one AccessID address struck); and a redacted extract of the presentations list into
`99/manuscripts/talks/PRESENTATIONS_RECORD_2026-08-17.md` with a row in `11/STATUS.md` section E. Every copy is recorded with
source, bytes and sha1 in the owning folder's `MANIFEST_LOCAL.md` under "Final pass of 2026-10-08".

**Defects fixed.** (1) Duplicates: eight files held by 01 against rule 2d were removed from 01 (owners 08, 09, 10; sha1
verified before removal; citations in 01's `STATUS.md` and `MANIFEST_GRID.md` redirected); the remaining shared copies
(01 / 02, 01 / 08 `overlap.json`, 03 / 06 one figure, 03 / 12 the visual-abstract files) are recorded as shared on both sides.
(2) Grid ownership: `model_registry` and `registry.jsonl` to 10 (01 appends, 12 reads), `split_final.json` and `patient_keys*`
to 10, `bench` declared shared by 01 and 03, `physics_rare` to 08; written into the four manifests and `PLAN.md` section 9.
(3) Rule 3: the Greg-only working notes topic 6 (03), topic 2 (06) and `literature_state/` (10, ten files) removed, with
pointers to 01 and 09. (4) The one Hugging Face handle withheld in every folder (`(HF username withheld)`). (5) The nine
scripts `PLAN.md` promised copied into `08/code/ssn_097933a/`. (6) `11/TODO.md` names project 10 and the Ceph access gate as
its dependency. (7) Of the verifies left unfixed by the cache, what was still open on disk was fixed: the ten student
co-author names and the four abstract rows with student presenters withheld in 07 and 08 (and 01) as 02 had them; the
username tally in 08's topic 6; the student list in the twelve CNS deck generators of 03; the library address in six memory
copies; an example account in two Beethoven documents; a mailing-list poster's address in one 11 note. (8) The triage order
was checked and found right; no change.

**Root files written.** `README.md`, `CLAUDE.md`, `INDEX.md`, `.gitignore` (with three negations for files whose names collide
with its patterns) and this record. `PLAN.md` gained section 9 (the corrections).

**Self-containment.** 74 copied text files in 01, 03, 08, 10, 11 and 99 still spelled laptop paths; they now carry the
markers the other folders already used (`<laptop:Desktop>`, `<laptop:Temp scratchpad>`, `<laptop memory folder>`, `<laptop
vendor folder, never read>`, `<laptop home>`), each folder's `MANIFEST_LOCAL.md` lists the files and counts, and the root
`CLAUDE.md` gives the key. Only `MANIFEST_LOCAL.md` files and `_plan/` keep the laptop spellings, as the record of where
each copy came from.

**Final scan (whole tree).** The banned word: 0 files (one occurrence in the salvaged May tex rewritten to "lineage" and
recorded). Token-shaped strings: none (the one `AIza…` match sits inside a base64 PNG in four SVGs). E-mail addresses of
persons: none outside three recorded kinds of keep (Greg's own institutional corresponding-author address in his manuscript
sources and package metadata; the maintainer addresses printed in the third-party `neurips_2026.sty` and `medphy.bst`;
role mailboxes). Laptop paths outside `MANIFEST_LOCAL.md` and `_plan/`: 0 files. Files over 25 MB: none. Stray files
(`*.stackdump`, `Thumbs.db`, `.DS_Store`, `~$*`, `*.pyc`, `__pycache__`, `.git`): none after the two `__pycache__` folders
in 10 were removed. Student names and usernames outside the manuscript sources: none; the author lists inside submitted or
public manuscript sources (`03/manuscripts/mpda/*.tex`, the `.bib` files, `ARXIV_SUBMISSION.md`, `REVIEWER_CRITIQUES.txt`)
and inside the accepted-abstract decks of 11 and the public CNS decks of 03 are kept as the record of authorship, a keep
reserved to Greg (`PLAN.md` section 5) and recorded in those folders' manifests.

**Size.** After the pass: 01 298.0 MB (1,970 files), 02 39.5, 03 131.9, 04 6.8, 05 63.9, 06 59.2, 07 16.7, 08 35.4, 09 24.3,
10 45.4, 11 10.6, 12 5.4, 99 7.1, `_plan` 1.5; 745.5 MB and 6,879 files in all (byte sizes, `find`, 2026-10-08). Folder 01
was 385 MB by `du` before the pass; the rule for shedding size allows only bulk per-run files over 2 MB that are byte-identical
to a file tracked in a repository, and 16 such files (81.0 MB: the per-seed `a5_rows.csv` tables, the two persons json files)
were removed and recorded by repository path and commit in `01/MANIFEST_LOCAL.md`. 01 stays above the 150 MB cap and the tree
above 600 MB because what remains is figures (45 MB), manuscripts (the two 2026-09-27 packet PDFs, 12.0 MB each, untracked in
the working tree so no commit holds them; the private CNS deck v10, 13.0 MB), the IRB letter and about 1,100 result files
under 2 MB each, all of which the rule keeps. The next lever (`PLAN.md` section 8: figure PNGs by path, regenerable from their
`.record.json` sidecars) is Greg's call. Every file is under GitHub's 100 MB limit.

## 5. What this record does not know

Whether the lstv-fusion remote on GitHub exists and is reachable (no network in this pass). Whether the CTSpinoPelvic1K git
history holds the May 2026 NeurIPS tex. The branch of SpineSurg-CT at 0051074. Whether the CNS 2026 items of the presentations
record were presented (the file predates the meeting). Whether Greg wants the author lists kept in the manuscript sources and
the decks, the 58 preview PNGs kept in 02, the one Hugging Face handle restored, and the SchwingNet figure PNGs moved to
reference-by-path to bring 01 under the cap. Those are listed as open in the final report and in each folder's `TODO.md`.
