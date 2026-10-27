# spine-program

`HANDOFF.md` gives any Claude session the state of this repository, the board and the grid on 2026-10-12; read it first.

`data_mining/` holds the Fluoroscopy Data Atlas of 2026-10-17: 217 fluoroscopy, spine radiograph, paired CT and X-ray,
CBCT projection and DRR datasets with what is on the grid and how to get the rest, and the 16 ready request letters
(read `data_mining/CATALOG.md` on GitHub).

`provisional_patent/` holds the SchwingNet provisional packet of 2026-09-18 and the WSU invention disclosure package of
2026-09-25, confidential parts included; its `README.md` says which is current and what must never leave this repository.

`synthetic_spine/` holds the published per-level vertebral morphometry series collected in CTSpinoPelvic1K to compare
ostk's measurements against, Panjabi's and the rest: 40 series in two tables, Panjabi's whole-spine table beside them, 42
papers. It gives each paper's citation and its DOI, PubMed and PMC links, a check of every value against the paper
itself where it can be read, and the code that redoes each step; its `README.md` lists what the checks found. It is a
collection, not a systematic review.

One private repository that seeds a set of Claude Code projects, one per numbered folder, dividing the spine imaging
programme of the Open Spine Consortium (Department of General Surgery, Wayne State University School of Medicine /
Detroit Medical Center) into self-contained units. It was built on 2026-10-08 from the laptop folders, the memory notes
and one read-only pass over the grid (`ls`, `cat`, `squeue`; nothing written). Nothing here is imaging data or a model
weight; everything of that kind is recorded by path in the owning folder's `MANIFEST_GRID.md` or `MANIFEST_LOCAL.md`.

**This repository is private and stays private.** It holds the SchwingNet level-identification code paths, results and
manuscripts, the FluoroCap record, the hospital test plan and the invention-disclosure references, all of which stay out
of public view until Greg says otherwise (`_plan/PLAN.md` section 2, rule "What stays private"). It also holds redacted
copies of working notes that name students by role; the unredacted notes are on the laptop and in
`spinesurg-ct-nnunet/HANDOFF/GREG_ONLY/`, never here. The "student-safe" label on a folder is about hand-outs cut from it,
not about this repository.

## The programme in one paragraph

A CT dataset of 802 abdominopelvic records (CTSpinoPelvic1K, release v11, concept DOI 10.5281/zenodo.22139642; the v11
deposit is recorded in `03_ctspinopelvic1k_dataset/STATUS.md`) built to ask whether local morphology can name a vertebra
without counting from C2; a public measurement toolkit (OpenSpineToolkit); a private convolutional-recurrent network
(SchwingNet) that names lumbar levels on intraoperative C-arm exposures, held out on one unseen C-arm at 595 of 617
lateral vertebrae (96.4 %; `01_carm_level_detection/docs/handoff/RESULTS_CATALOG.md` row A2.1); a census of transitional
anatomy across 21,622 public CTs; a data platform of 211 sources migrating to Ceph; and the student framework (Beethoven,
the lab recipe) that lets medical students work on the grid. Every number above carries its file in the folder that owns it.

## The folders, in triage order

Rank is by how likely the folder is to return a real result from what is on disk and on the grid, with two stated
exceptions: 01 is first by Greg's instruction, and 02 follows it because the hospital test's pre-registered endpoint is
transitional and 01's hospital plan cannot be written without 02's truth file (`_plan/PLAN.md` section 4).

| rank | folder | title | reader | likelihood | depends on |
|---|---|---|---|---|---|
| 01 | `01_carm_level_detection` | Intraoperative C-arm level detection: from SchwingNet as it stands to a model tested on real fluoroscopy at the hospital | Greg-only | engineering steps S0-S2 likely within weeks; the hospital number gated by an unknown device and IRB lead time | 10, 02, 08 (if a device card is chosen), 09 (the per-case form), 12 (the client) |
| 02 | `02_transitional_naming_truth` | Transitional-aware naming and the real-frame truth file (paper 2) | Greg-only | unlikely to reach its pre-stated bounds from the holding (0 verified persons against 22 or 35); likely to return a decisive screen number cheaply | 06, 10, 01, 08 |
| 03 | `03_ctspinopelvic1k_dataset` | CTSpinoPelvic1K: release v11, the dataset article and the NeurIPS camera-ready | student-safe after redaction | highest: one paper accepted, one submitted; editing, a rebuild and Greg's answers remain | 10, 05, 04, 06 |
| 04 | `04_openspinetoolkit` | OpenSpineToolkit: the v11 defects and their tests | student-safe | high and bounded: every defect has a one-hour test with a number; blocks 05 | 03 |
| 05 | `05_ct_morphometry_parity` | CT morphometry, the spinopelvic estimator and 3-D to 2-D parity | student-safe | high for a number within days (PAR-1 is one laptop hour) | 04, 03, 10, 02, 08 |
| 06 | `06_transitional_ct_census` | The transitional census: harvest, registry, ruleclass arms and the review tree | student-safe after redaction | medium: the machine side is nearly done; the result needs readers (0 verdicts filled on 446 registry review cases plus 103 labeller-validation renders) | 10, 03, readers |
| 07 | `07_plain_film_level_id` | Plain-film level identification and the radiograph corner detector | Greg-only | medium: held-out corner numbers are real; the film naming numbers are leaked or wrong-bank; venue windows passed | 10, 03, 01, 04 |
| 08 | `08_render_devices` | Image formation: DRR banks, device cards, PolyPose and synthetic-to-real | Greg-only | low as a claim (styled corpora failed the pre-stated 97 % on two of three devices), medium as support for 01 and 05 | 10, 03, 02 |
| 09 | `09_wrong_level_clinical_qi` | Wrong-level surgery: the iliac-crest paper, the scoping review and the QI protocol | Greg-only | medium-low near term: the iliac-crest number is v5-era, the review needs human charting, the QI protocol waits on 01 | 05, 01, Greg |
| 10 | `10_data_platform_grid` | The data platform: 211 sources, the Ceph migration, identity and leakage, grid operations | student-safe | support; mechanical and high (three migration jobs were running on 2026-10-08) | Greg's per-batch decisions |
| 11 | `11_students_grid_access` | Students on the grid: Beethoven, onboarding, the lab recipe and the med-ed record | Greg-only until the Beethoven notes are redacted; the guides student-safe | support; operational (release 14.0.0 in field use) with two unfixed field failures | 10 |
| 12 | `12_website_pacs_demo` | The public site, the PACS demo and the level-service client | student-safe | support; operational (PACS demo 1,360 ms); the level service is not live | 01, 04, 05, 11 |
| 99 | `99_archive` | Archive: superseded, refuted and dormant work kept as a record | Greg-only | not a project to work; a record with the reason each item is here | none |

### One paragraph per folder

**01 C-arm level detection.** Take the reported SchwingNet stack (naming detector, sacrum and vertebra detector, the v9
level encoder, the recurrent head, the count from the sacrum, alphabet coupling and the stop signal) from four weight files
on the grid to a packaged service, a measured latency, a pre-registered hospital protocol and a test on real fluoroscopy
from patients at the hospital where Greg works. The engineering steps (freeze and register the stack, measure uncontended
latency, package the service) are likely within weeks; the hospital number waits on a C-arm whose make is not yet known,
a faculty sponsor and IRB lead time. First step: TODO S0, register the reference stack with its metrics. Open issues:
#31, #32.

**02 Transitional naming truth.** Name the level correctly on a transitional spine (L6, T13, sacralised L5, four-lumbar)
from C-arm exposures at parity with an ordinary spine, or write "not at parity" with its number. The folder owns the
real-frame transitional truth file, the reader protocol and the power table that 01's hospital plan needs. Unlikely to
reach its pre-stated bounds from the current holding; likely to return a decisive screen number from a one-hour render.
First step: the one-hour COBRA coverage render. Open issues: #33, #34.

**03 CTSpinoPelvic1K dataset.** Close out the public dataset: the Medical Physics dataset article, the accepted NeurIPS 2026
Evaluations and Datasets paper 3474 (camera-ready with 134 `[pending]` slots), the Zenodo v11 deposit and the Hugging Face
mirror still at v10. The most likely folder to return a finished result, because two papers already exist; what remains is
editing, one rebuild measured by `build.sh --reprint`, and Greg's answers. First step: ask Greg the questions no file answers.
Open issues: #21, #22.

**04 OpenSpineToolkit.** Keep the public measurement library correct for release v11: the canal-closing regression that
inflates two measures by 10-17 mm on about one vertebra in seven, the retired identifier 29, the empty pedicle-width column.
Every defect has a one-hour test with a number; this folder blocks 05. First step: CT-1, the canal-closing fix. Open
issues: #23, #24.

**05 CT morphometry and parity.** Make the measurements of CTSpinoPelvic1K right and extend them: the spinopelvic
estimator's three open items, the level atlas with its withheld L5 columns, and whether a 2-D render reproduces the 3-D
measure (parity). A number within days is likely; PAR-1 is one laptop hour. First step: PAR-1, the single-vertebra 3-D target.
Open issues: #25, #26.

**06 Transitional CT census.** Find enough transitional people across every public CT to test naming: the harvest over 18
collections, the registry, the ruleclass arms and the review tree. The machine side is nearly done; the result needs human
readers, and none of the 446 registry review cases has a verdict yet. First step: one read-only job that answers the five
open counting questions. Open issues: #27, #28.

**07 Plain-film level identification.** The line the C-arm work grew out of: the radiograph corner detector (held-out
numbers real), XRSpinoPelvic1K and the film-naming experiments whose quoted numbers are leaked or from the wrong bank. The
venue windows that motivated it have passed. First step: purge the tracked junk from XRSpinoPelvic1K's history, then
rebuild its data from v11 labels. Open issues: #35, #36.

**08 Render devices.** The rendering side that feeds every 2-D model: the DRR banks, the nine-term device cards, PolyPose
and the synthetic-to-real attempts. As a claim it is low (the styled corpora failed the pre-stated 97 % on two of three
devices); as support for 01 and 05 it is medium. First step: a read-only job that settles two open questions about the
refitted cards and the box convention. Open issues: #37, #38.

**09 Wrong-level surgery and QI.** The clinical argument and its three instruments: the iliac-crest paper (a v5-era
number), the scoping review (protocol v1.0, manuscript v0.4, no number yet) and the QI protocol that waits on 01. Medium-low
near term. First step: recompute the iliac-crest statistic on v11 labels with `labels_for`. Open issues: #39, #40.

**10 Data platform and grid.** One record of where every imaging source came from, where it sits (HOME versus Ceph), its
migration and verification state batch by batch, the identity and leakage rules every bank must pass, the model registry
and the grid operating rules. Support, mechanical and high; nearly everything else depends on it. On 2026-10-12 (Greg,
issue #68) the migration chain completed at 08:41 EDT: every batch with data is copied, verified, cut over and
finalized; HOME stood at 520 GB of the 4,295 GB soft limit; every folder under `/rs/rs_grp_oschome/go2432/data/` is
readable by approved students except `ctspinopelvic1k_build_tree/derived/build_archive_private` (its one file is the
annotator map, students' personal data), `ctspinopelvic1k_build_tree/derived/s1v11` included since visibility job
40602925 (issue #69). First step:
build the holding index (`TODO.md` step 3); the folder's `TODO.md` still words steps 1 and 2 as they stood on
2026-10-08. Open issues: #17, #18.

**11 Students and grid access.** Keep the path by which students reach the grid and do a project working: Beethoven
(release 14.0.0 in field use, two unfixed field failures), the onboarding one-liner, the lab recipe and board, and the
medical-education record. Support, operational. First step: redact and copy the six Beethoven notes and the access-gate
note. Open issues: #19, #20.

**12 Website and PACS demo.** Maintain the public site, the NiiVue PACS demo (1,360 ms) and the level-service client, which
waits on 01's packaged service. Support, operational. First step: `git pull` the site clone, which was ten commits behind.
Open issues: #29, #30.

**99 Archive.** Superseded, refuted and dormant work, dated, with the reason each item is here and what replaced it, so
nobody repeats it; never a source of a quotable number. First step: none to run; add dated records as later work supersedes more.
Open issues: #41, #42.

## How a student starts

A student given this repository starts from this page alone. There are two ways in, a claude.ai Project and Claude Code
on the student's own computer, and the four paragraphs below hold for both.

Greg first gives the student Write on `OpenSpineConsortium/spine-program` (a collaborator invite). The student works as
the worker named by their GitHub login: the claim skill makes the label `worker:<GitHub login>` the first time it needs
it, and the claim file's Worker line is that login. Write means the student may read all 13 folders,
the Greg-only ones included (Greg's answer of 2026-10-12, issue #68): "Greg-only" and the label `greg-first` govern
claiming and hand-outs, not reading. An issue labelled `greg-first`, or one in a folder marked Greg-only, is claimed by a
student only after Greg hands it out, either with a comment on the issue naming the student's login or by removing the
label `greg-first`.

How work is claimed is [docs/agents/PROTOCOL.md](docs/agents/PROTOCOL.md). Four labels drive it: todo marks the queue,
and an issue labelled todo that the board shows unclaimed is free to take. Claimed means a worker has pushed its
branch, and the worker's own label goes on with it; a claim with no commit for 24 hours is released by the board's own
run. In-review means the pull request is ready, so the owner merges it
and the merge closes the issue. Blocker means the issue stops everyone until it is done.

The skills named on this page are the committed, unprefixed ones under `.claude/`: `/claim`, `/remember`, `/checkpoint`
and `/board`, kept in the repository so a cloud session, which loads no plugin, has them; the symphony plugin's
`/symphony:*` copies are the same procedures, and a local session may use either.

The data lives on the Wayne State grid and is reached through the Beethoven app
(https://openspineconsortium.com/beethoven/). Approved students pass a named-user gate on the Ceph volume. Three
datasets carry terms of use — VinDr-SpineXR, BUU-LSPINE and Mendeley 5jdfdgp762 — and need those credentials. Each
project's `DATA.md` gives the paths; what students could read on 2026-10-12 is in "The grid in one paragraph" below.

### From Claude Code locally

Clone `OpenSpineConsortium/spine-program`, open the clone's top folder in Claude Code, and trust it when asked. Run
`claude plugin install symphony@symphony-marketplace --scope project` once: the committed `.claude/settings.json` names
the plugin but does not download it, so this one command fetches it. On Windows, `python3 --version` must print a
version in Git Bash (the Microsoft Store alias is not Python), or the plugin's push guard silently does nothing; the
claim push runs in Claude Code's Bash tool, never through `wsl`. Then, in a new session, run `/board` to read the board,
pick from its Queue an unclaimed issue labelled todo, and claim it with `/claim`. Work on the branch `claude/<issue>`,
open the draft pull request at once, and never push to main.

### From a claude.ai Project

Projects are on Pro and Max plans only. At https://claude.ai/code make a Project and link this repository as its only
resource, leaving its instructions, description and memory blank: the goal, the memory, the board and the rules are read
from the clone in every thread. Each thread starts from a fresh clone of main. Add the symphony plugin under the
Project's settings where it is offered; otherwise run `/board` first in each thread. The Claude GitHub App must already
be installed on the repository by the organization owner. The issue is chosen as "Choosing a project" below says. Add
these two lines to a cloud-session prompt (the label `worker:<GitHub login>` is made by the claim skill, not by Greg):

```
gh issue and gh pr are refused here, so add the labels, post the plan and open the draft pull request with your GitHub tools or gh api (repos/OpenSpineConsortium/spine-program/issues/N/labels, repos/OpenSpineConsortium/spine-program/issues/N/comments, repos/OpenSpineConsortium/spine-program/pulls). Mark the pull request ready with your GitHub tool update_pull_request (draft false), not gh api, which cannot change a draft; if you have no such tool, say so and stop before you delete the claim file.
My worker name is my GitHub login, <login>: the label worker:<login> and the claim file's Worker line.
```

One ready-to-paste prompt for a Project thread, followed by the two lines above:

```
Claim issue N with the claim skill and carry it to a ready pull request, as docs/agents/PROTOCOL.md says; work on the branch claude/N, not this session's own branch. If the push of claude/N is refused, another session holds the issue: say so in one line and stop. Do not merge.
```

A Project thread cannot reach the grid, ssh or `sbatch`, Greg's HOME `/wsu/home/go/go24/go2432`, or the other
repositories (the code repositories each folder's `MANIFEST_CODE.md` names). For an issue that needs any of them, paste
this prompt instead, followed by the same two lines:

```
Claim issue N with the claim skill, write the plan, the job script and the draft pull request, then stop at the first step that needs the grid or another repository and say exactly what to run where. Do not merge.
```

## Choosing a project

Always open the clone's top folder, in Claude Code or as a Project's repository; a numbered folder is never opened as
the project root. The project is the folder named in the claimed issue's title. Before the first change, read that
folder's `CLAUDE.md` (the working context: goal, rules, traps, where things are), `README.md`, `DATA.md` (the grid paths,
reached through Beethoven), `TODO.md` (the ordered steps with gate, pre-stated number, dependency and who decides),
`STATUS.md` (the results in hand, each with its number, file and rigor mark) and `MANIFEST_GRID.md` (every grid path the
folder uses or produced, HOME and Ceph, with what it holds, its size where known and its migration state; check it
against the grid before trusting a path). Work starts from the claimed issue's acceptance lines, not from `TODO.md` step
1; a TODO step with no issue gets a todo issue, which Greg opens, before work starts. A change to another repository
lands as `<folder>/patches/<N>-<slug>.patch` in the claim's pull request. The folder's `results/`, `figures/`, `manuscripts/` and
`regulatory/` are symlinks to the grid, where the salvaged record lives since 2026-10-13: a Project thread reads one of their
files from git history, and a task that must change one brings it back into its branch first (`ARCHIVE.md`).

The folder's `MEMORY.md` indexes `memory/`; every note carries its status (CURRENT, DATED, PARTLY SUPERSEDED, SUPERSEDED,
LEAKED, RECORD ONLY, DORMANT) carried over from the handoff index. `MANIFEST_CODE.md` gives every repository with URL,
branch, commit and the files that matter; `MANIFEST_LOCAL.md` gives every file copied into the folder, where it came
from, and every valuable file that was not copied, with the reason. The only references outside a folder are grid
paths, code repositories and sibling folders of this repository.

## The rules that bind every folder

Each folder's `CLAUDE.md` restates these in its own words and adds its own traps; the root `CLAUDE.md` carries them in full.
In short: never the banned word (write origin, lineage, where it came from); no fractional version numbers; captions at
most 60 words; plain sentences; every number with its file, "not recorded" where no file records it; check against
something outside the computation, because the recurring failure is a number that is wrong but plausible; two label
schemes exist and mixing them does not raise, so call `ostk.labels.labels_for(volume)`, treat identifier 29 as retired,
`zfill(4)` the case ids, canonicalise to analyse and never reorient when writing; held out means the person was never seen
by the checkpoint or any ancestor, every quoted score passes the evaluation gate, the leaked banks are never quoted;
pre-register, then score; nothing runs on the login node (`sbatch -D`, `afterany`, `/dev/shm`, Ceph for large outputs, bash
4.2); SchwingNet and all level-identification code, text and weights stay private; use all of a public dataset and fix or
justify every truncation; network through WSL, except the claim push, which runs in Claude Code's Bash tool; tokens read
from files only; in spine-program, claim branches and pull requests only, and "commit only when Greg asks" means the code
repositories; Ashley Schehr is a person; the affiliation is General Surgery (Wayne State University School of Medicine /
Detroit Medical Center), never Neurosurgery.

## What is deliberately not here, and where it lives

Imaging data, arrays and weights (on the grid, Zenodo, Hugging Face or in their public sources; every item recorded by
path in the owning folder's manifest); anything under `.git`, environments, caches, logs over 2 MB, files over 25 MB;
credentials (a rotation list by path in `_plan/PLAN.md` section 6, contents never read); personal and administrative
material; the U251 and LITT studies and the case reports outside the spine; `HANDOFF/GREG_ONLY/`, `private_ip/` and the
invention-disclosure material (referenced by path from 01); student names and usernames and researcher e-mail addresses
(redacted copies where the research content matters; the author lists inside submitted or published manuscript sources are
kept as the record of authorship, a keep that is Greg's to confirm). The full list with reasons is `_plan/EXCLUDED.md`;
every inventory row and where it went is `_plan/DISPOSITION.tsv`.

## The grid in one paragraph

The grid as it stood on 2026-10-12 (Greg, issues #68 and #72; `10_data_platform_grid/MANIFEST_GRID.md` section 2).
Every migration batch with data was finalized on 2026-10-11 (B00, B01, B02, B04, B06, B07, B08, B09 and B14, each
`.pre-ceph` original deleted after a full comparison; B03 had nothing to move; B12 was dropped; Greg's record of
2026-10-11, issue #49). B05, B10, B11 and B13, submitted as one chain on 2026-10-11, completed at 08:41 EDT on
2026-10-12: every batch with data is copied, verified, cut over and finalized (B13 3/3), with no refusal. Visibility job
40599867 opened the VinDr and BUU banks in `multisource_banks`; dedup group A14 linked 1,413 files; job 40599718 deleted
the TotalSegmentator v3.0.0 zip (37.4 GB) and the NHANES extracted pickles (159 GB), and job 40602927 deletes the v2.0.1
zip (23.58 GB). HOME `/wsu/home/go/go24/go2432` stood at 520 GB of the 4,295 GB soft limit (4,050.75 GB of 4,294.97 GB
on 2026-10-08); Ceph `/rs/rs_grp_oschome/go2432` held 9 of 20 TB. Every folder under `/rs/rs_grp_oschome/go2432/data/`
is readable by approved students, `ctspinopelvic1k_build_tree/derived/s1v11` included (opened without the token check by
visibility job 40602925, issue #69), except `ctspinopelvic1k_build_tree/derived/build_archive_private`, whose one file is
the annotator map (students' personal data, not a dataset or a token). Job 40602926 opened
`/rs/rs_grp_oschome/go2432/envs/spineps212` and `/rs/rs_grp_oschome/go2432/results` to approved students
(`11_students_grid_access/STUDENT_ENV.md`); nothing on HOME is readable by students (`10_data_platform_grid/DATA.md`
section 1). The per-batch truth is
`~/spinesurg-ct-nnunet/data_platform/plan/runs/<B>/STATUS` on the grid. Known losses, as recorded on 2026-10-08: the TCIA
CT Colonography raw and NIfTI trees (1,057 GB) are on neither volume; CTPelvic1K datasets 1-5 are absent; the
`allspine_v2..v5c` banks were deleted on 2026-09-20 (`10_data_platform_grid/MANIFEST_GRID.md`,
`_plan/inventories/grid_manifest.md`).

## Where the plan is

`_plan/PLAN.md` (the division, the rules, the projects, where the two proposals disagreed, the decisions reserved to Greg,
the unknowns, and section 9, the corrections of the final pass), `_plan/DISPOSITION.tsv` (every inventory row and where it
went), `_plan/EXCLUDED.md`, `_plan/ROOT_FILES.md` (the specification of this file), `_plan/inventories/` (the seven
inventories of 2026-10-08), `_plan/BUILD_RECORD.md` (how the tree was built, interrupted and completed), and `INDEX.md`
(one line per folder).

## Dates and commits of the sources this seed was cut from

`spinesurg-ct-nnunet` branch `L6_Class` 097933a (private); `CTSpinoPelvic1K` `master` 7ddfe38 (working tree modified);
`OpenSpineToolkit` `main` cb43197; `XRSpinoPelvic1K` `main` 4f22935 (private); `OpenSpineConsortium/beethoven` 2f90319;
`beethoven-vscode` 8d7fc65; `openspineconsortium.github.io` local c1800f8, behind origin a17ea39; `SpineSurg-CT` 0051074;
`lstv-fusion` 3c8f5c1; the memory folder's newest note 2026-10-08 16:43; the grid pass 2026-10-08 22:20 UTC.
