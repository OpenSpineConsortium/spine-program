# spine-program: the root working context

This is one private repository that seeds a set of Claude Code projects, one per numbered folder; each folder is
self-contained (its own `CLAUDE.md`, `README.md`, `STATUS.md`, `TODO.md`, `MEMORY.md` + `memory/`, three manifests and the
salvaged material). Open the folder's `CLAUDE.md` first: the rules below bind everywhere, and the folder adds its own
traps. Nothing here is imaging data or a weight; the grid and the named repositories hold those. Since 2026-10-13 the salvaged record, each folder's `results/`, `figures/`, `manuscripts/` and `regulatory/`, lives on the grid too, under `/rs/rs_grp_oschome/shared/spine-program/archive/`, and the folders in the tree are symlinks to it: `ARCHIVE.md` says how a session reads a file from either place and how a task brings one back into its branch (issue #87).

## Read first

- `_plan/PLAN.md` sections 1-2 (the division and the builders' rules) and section 9 (the corrections of the final pass).
- The folder's `CLAUDE.md`, `README.md`, `STATUS.md`, `TODO.md`.
- `<folder>/docs/handoff/README.md` section 5 (the ten rules as the handoff wrote them) and
  `<folder>/docs/handoff/RESULTS_CATALOG.md` "How to read a row" (every folder carries the student-readable handoff files).
- `<folder>/DATA.md` (every grid path the folder uses, who may read it, a read-only check line); its access facts of
  2026-10-11 supersede older statements in the `docs/handoff` copies.

## The map

```
01_carm_level_detection      Greg-only   the C-arm path to a hospital test (SchwingNet as it stands -> service -> PREREG -> real fluoroscopy)
02_transitional_naming_truth Greg-only   the transitional truth file, reader protocol, power table (paper 2); feeds 01's PREREG
03_ctspinopelvic1k_dataset   student     release v11, the dataset article, the NeurIPS camera-ready, Zenodo and HF
04_openspinetoolkit          student     ostk's v11 defects and their one-hour tests; blocks 05
05_ct_morphometry_parity     student     the spinopelvic estimator, the level atlas, 3-D to 2-D parity
06_transitional_ct_census    student     the harvest over 21,622 CTs, the registry, ruleclass arms, the review tree
07_plain_film_level_id       Greg-only   the radiograph corner detector, XRSpinoPelvic1K, the film-naming line
08_render_devices            Greg-only   DRR banks, device cards, PolyPose, synthetic-to-real; serves 01 and 05
09_wrong_level_clinical_qi   Greg-only   the iliac-crest paper, the scoping review, the QI protocol (01's per-case form)
10_data_platform_grid        student     211 sources, the Ceph migration, identity and leakage, the registry, grid rules; the dependency of all
11_students_grid_access      mixed       Beethoven, onboarding, the lab recipe, the med-ed record; waits on 10
12_website_pacs_demo         student     the public site, the PACS demo, the level-service client; waits on 01 S2, 04, 05
13_aidas_program             mixed       the AIDaS program map: workflow, IRB, data and literature mining, C-arm training, recruitment, the LLM; REFORMS
99_archive                   Greg-only   superseded, refuted, dormant; never run, never quoted
_plan/                                   the division, the disposition of every row, the exclusions, the inventories, the build record
```
Every Write holder may read all 13 folders (Greg's answer of 2026-10-12 to `OPEN_QUESTIONS.md` A29, issue #68); the
label governs claiming and hand-outs, not reading. `Greg-only` means Greg works the folder first, and a student takes an
issue there only after Greg hands it out (his comment on the issue naming the student's login, or the label
`greg-first` removed); `student` means a hand-out can be cut from the folder after the redactions it records. The
repository itself is private whatever the label.

**How the folders relate.** 10 is the dependency of all (data, identity tables, the registry, the access gate). 04 blocks
05. 02 feeds 01's PREREG and consumes 06. 08 serves 01 and 05. 09's per-case form is 01's S5 / S8 scaffold. 12 waits on 01
S2, 04 and 05. 11 waits on 10. 99 is never run. The one circularity is stated on both sides: 01 depends on 12 for the
service client while 12 waits on 01 S2.

## The standing rules (every folder's CLAUDE.md restates these in its own words)

1. **Words and style.** Never the banned word, the French-derived word for where data came from: write origin, lineage,
   source, where it came from. No fractional version numbers; fold a change into the next integer version. Figure captions
   at most 60 words, the argument in the text. Plain sentences. Matrix tables in solid black with at most one outlined mark;
   slides never use sideways bar charts. The affiliation is General Surgery (Wayne State University School of Medicine /
   Detroit Medical Center), never Neurosurgery. Ashley Schehr is a person (senior scientist, co-PI, a published co-author),
   never a product name; the product is Beethoven. (`ctsp:CLAUDE.md`, `memory/writing-preferences.md`,
   `memory/user-affiliation-general-surgery.md`.)
2. **Every number carries its file.** A count, date, path or claim names the file it comes from; what no file records is
   written "not recorded"; say plainly what is not known rather than guess. (`ctsp:CLAUDE.md` "How to be useful here".)
3. **Check outside the computation.** The recurring failure in this programme is a number that is wrong but plausible:
   three estimators produced finite, reasonable values from the wrong bone, the wrong surface or the wrong label map, and
   internal consistency (PI = SS + PT) held throughout because both sides shared one bad landmark. Compare with published
   values, an independent implementation, the spread of the distribution (not its median), a published prevalence; render
   the mask; when a tidy explanation presents itself, test it before believing it. (`ctsp:CLAUDE.md`,
   `ctsp:docs/SPINOPELVIC_ESTIMATOR.md`, `ctsp:docs/LEVEL_MORPHOMETRY.md`.)
4. **Labels and orientation.** Two label schemes exist and mixing them does not raise: release v11 is VerSe-native
   (L1 = 20 ... L5 = 24, sacrum 26, hips 30 / 31, femurs 32 / 33); the legacy map puts L1 at 1 and the femurs at 11 / 12,
   and "femur_left" resolved against the wrong one comes back T4. Call `ostk.labels.labels_for(volume)`; never import a
   fixed map. Identifier 29 (the carved S1) is retired in v11 and dissolved into 26; code that gates on 29 is retired with
   it. Case ids are zero-padded (`zfill(4)`) in the release and were not in the old CSVs. Canonicalise to RAS to analyse;
   never reorient when writing a label (`as_closest_canonical` + `nib.save` transposes a label away from its CT); CT volumes
   are stored P, I, R. (`ctsp:CLAUDE.md`, `memory/label-scheme-v4-vs-ostk.md`, `memory/never-reorient-when-writing-labels.md`.)
5. **Held out.** Held out means the person was never seen by the checkpoint or any ancestor; a render inherits its CT's
   person; unknown is not clean. Every quoted score goes through `ssn:tools/eval_gate.py`. Never quote the leaked banks
   (allspine v2, v6, v7, v8 for VerSe, `anchor_drr`, `vindrps`) or any number marked LEAKED, SUPERSEDED or RECORD ONLY in
   `docs/handoff/RESULTS_CATALOG.md`. (`docs/handoff/LEAKAGE.md`.)
6. **Pre-register, then score.** Write the rule and its success criterion before the run, hash it, stamp every output row
   with the hash; a number produced before the freeze is calibration; comparators are pre-specified from the literature and
   never tuned; manuscript numbers enter through a manifest key, never typed. (`docs/handoff/RECIPES.md`.)
7. **The login node runs nothing.** Every computation, render, plot and download is an `sbatch` job; warrior kills python,
   rsync, node, pip and conda by name; no container command on warrior and nothing of ours under its `/tmp`. `sbatch -D <dir>`
   (a relative `--output` resolves against the submit directory); `afterany`, not `afterok`; IPC under `/dev/shm` (compute-node
   `/tmp` is swept); large outputs on Ceph `/rs/rs_grp_oschome/go2432/`, not HOME; record a job before cancelling it; write grid
   bash for bash 4.2; partition `reqp --qos=requeue` for CPU, `gmsap` / `gvohp` for GPU; Greg's python with nibabel and
   scipy is `~/mambaforge/envs/spineps/bin/python`, in his HOME, which students cannot read; a student's environment is
   `11_students_grid_access/STUDENT_ENV.md` (written by issue #66). Submit, estimate the wall time, write the job ids and
   the ETA to the resume file, stop. (`ctsp:CLAUDE.md` "Grid", `memory/no-jobs-on-login-node.md`,
   `memory/submit-and-sleep-orchestration.md`.)
8. **What stays private.** SchwingNet and all level-identification code, text, figures and weights; FluoroCap; the
   `spinesurg-ct-nnunet` and `XRSpinoPelvic1K` repositories; this repository. Nothing about them goes public until Greg says
   so; run `ssn:tools/disclosure_audit.py` before any talk, upload or submission; for the CNS talk use only
   `CNS2026_Schwing_NotAllSpines_public_v12.pptx`. (`memory/fluorocap-repo-private.md`, `memory/schwingnet-disclosure-scrub.md`.)
9. **Data directives.** Use all of a public dataset; a download budget is not a criterion; every truncation is fixed or
   justified in writing before a rerun; a leaked initialisation is fixed by retraining, never disclosed as a caveat;
   FluoroCap is out of training (a test set at most); identity comes from metadata first and the file name last; the IRB
   umbrella (HPR 2026-269) covers only public, de-identified data downloadable without an agreement.
   (`memory/no-unexplained-subsets-fix-not-disclose.md`, `memory/data-directives-2026-09-23.md`.)
10. **Git, network, credentials.** In spine-program the worker doing the work, a person's sessions under the person's
    GitHub login, commits and pushes only its own branch `claude/<issue>`, as `docs/agents/PROTOCOL.md` says; it never
    commits to or pushes `main`; a session of Greg's merges its own pull request once the required checks are green, never waiting for him (his word of 2026-10-31 03:45 UTC: "REMOVE ALL OWNER REQUIRED PERMISSION FOR MERGING PRS"), while a student's or another collaborator's pull request still waits for Greg to merge it. The claim push
    is a plain `git push -u origin claude/<N>` in the Bash tool, never wrapped in `wsl`. In the code repositories
    (`CTSpinoPelvic1K`, `OpenSpineToolkit`, `spinesurg-ct-nnunet`, `XRSpinoPelvic1K`, `openspineconsortium.github.io`,
    `beethoven`) and on Greg's laptop: commit only when Greg asks; `CTSpinoPelvic1K` commits directly to master, no
    feature branches, and pushes to `origin` and `osc`; `OpenSpineToolkit`: branch `main`, both remotes. The WSL network rule is Greg's Windows laptop's: there, network (git push, ssh, rsync, Hugging Face)
    goes through `wsl -e bash -lc '...'`, and `ctsp:paper/mpda/make_submission.py` is the one exception and runs from
    Windows. The git clauses of the folder `CLAUDE.md` files mean the repositories those folders name, never this one.
    Tokens are read from files, never echoed, never on a command line or in
    `sbatch --export`; nothing under the laptop vendor folder is read. Write scripts as files and run them by path (inline
    heredocs collapse backslashes); never name a scratch script `numbers.py`, `io.py` or `pdb.py`.
    (`memory/wsl-for-network.md`, `memory/bash-heredoc-backslashes.md`, `memory/scratchpad-shadows-stdlib.md`.)
11. **The page limit** of the dataset article is 10 published pages and only `build.sh --reprint` measures it; read the
    whole build output, because LaTeX emits a PDF and a page count on top of a broken table. (`ctsp:CLAUDE.md`.)
12. **Personal data.** No student name or username, no researcher or personal e-mail address enters any file of this
    repository; where a source carries one, the redacted copy is used and `MANIFEST_LOCAL.md` records the redaction by kind.
    Three kinds of keep are recorded, not hidden: the author lists inside submitted or public manuscript sources (the record
    of authorship; Greg's to confirm, `_plan/PLAN.md` section 5), Greg's own institutional corresponding-author address in
    his manuscript sources and package metadata, and the maintainer addresses printed in third-party template files
    (`neurips_2026.sty`, `medphy.bst`). Role mailboxes (`hpc@`, `IRBQuestions@`) and the ssh login `go2432@grid.wayne.edu` are
    not personal data and stay. The worker name the claim protocol needs (the `worker:<login>` label, the claim file's
    `- Worker:` line, the board) is working metadata like commit authorship, not the personal data this rule is about.

## Prefixes and markers in the copied documents

`ssn:` = spinesurg-ct-nnunet at 097933a; `ctsp:` = CTSpinoPelvic1K at 7ddfe38; `ostk:` = OpenSpineToolkit at cb43197;
`xr:` = XRSpinoPelvic1K at 4f22935; `bth:` = OpenSpineConsortium/beethoven at 2f90319. Copied files spell where they came
from with markers, never with a laptop path: `<laptop:Desktop>` (the Desktop root that held every checkout, so
`<laptop:Desktop>/spinesurg-ct-nnunet` is `ssn:`), `<laptop:Temp scratchpad>` (a swept session folder; nothing there is a
dependency), `<laptop memory folder>` (the live memory notes, copied redacted into each `memory/`), `<laptop vendor folder,
never read>`, `<laptop home>`. Only `MANIFEST_LOCAL.md` files and `_plan/` keep the laptop spellings, as the record of
where each copy came from. A marker is history; the repository and commit are the dependency.

## How to be useful here

Check against something outside the computation. When a tidy explanation presents itself, test it before believing it.
Say plainly what is not known; `ctsp:docs/SPINOPELVIC_ESTIMATOR.md` records an unexplained failure in 128 records rather
than a guess at its cause, and that is the preferred form. Render the mask: twice in this programme one render settled
what two or three rounds of reasoning from numbers got wrong.

## What a cloud session reaches

A claude.ai Project thread or a cloud session has this clone and GitHub, through its proxy, and nothing else: no grid,
no ssh, no `sbatch`, no `wsl`, no access to Greg's HOME and no clone of the other repositories. The record folders the symlinks
point at are on the grid, so such a session reads one of their files from git history (`ARCHIVE.md`). Grid steps run from the
Beethoven worker or by Greg, and their job ids and outputs come back to the claim branch. A change to another repository
lands as `<folder>/patches/<N>-<slug>.patch` (`git format-patch` against the commit `MANIFEST_CODE.md` names) in the
claim's pull request, and Greg applies it.

## Continuing locally

Since 2026-10-31 the owner runs this project from a local Claude Code session instead of claude.ai project threads. Start every local session the same way:

1. Clone the four private repositories side by side and keep them current: `git clone git@github.com:OpenSpineConsortium/<name>.git` for SchwingNet, bordercall, symphony-template and spine-program, then `git fetch origin` before any work.
2. Read SchwingNet's docs/checkpoints/2026-10-31-final/README.md (the latest handoff: every thread's state, open pull requests, grid jobs and next steps) and the project memory beside it in memory/MEMORY.md.
3. Work one piece at a time on its own branch, open a pull request, and merge it yourself once CI is green: no merge waits for the owner (his word of 2026-10-31 03:45 UTC). Test what you change before pushing.
4. Grid work: ssh to the grid and run `cd ~/SchwingNet && git pull && bash grid/gate.sh <word>`, or dispatch symphony-template's grid-accounts.yml (action=job, job=schwingnet-<word>); the size rule holds; the login node only submits jobs.
5. Never public, sign nothing about the provisional, no usage credits, never run archived code, and be frugal with tokens.

## How work is claimed

@docs/agents/PROTOCOL.md

@docs/memory/MEMORY.md

Before any work: fetch, read the board with `git fetch origin +refs/heads/board:refs/remotes/origin/board && git show origin/board:STATE.md` (or `/board`), and check the claim on the issue you mean to take. One issue, one branch `claude/<issue>`, one pull request. Never push to the default branch or to another worker's claim branch. The required check "check" (`.github/workflows/ci.yml`, `bash scripts/check.sh`) holds every pull request to the claim protocol and the review record (`CONTRIBUTING.md`); run it before a pull request. The push guard is the symphony plugin's and runs in local sessions only.

The protocol is the release of OpenSpineConsortium/symphony-protocol that `tools/VENDORED` records, vendored under `tools/sdlc_protocol`; `.github/workflows/protocol.yml` brings each later release in, weekly and by hand, as a pull request from the branch `symphony-protocol/sync` (or an issue linking one where GitHub Actions may not open a pull request), and nobody vendors by hand. Every worker here is a person's sessions, named by the GitHub login: the registry under `.github/symphony/workers/`, the workers' and the coordinator's workflows that PROTOCOL.md names are the template's and are not here; the board's own run releases idle claims and tells overlapping work.
