# START HERE: the spine imaging programme, handed over

Written 2026-10-08 for a new student, and for a fresh Claude project that has none of the conversation that produced
this work. It answers Greg's request of 2026-10-08: summarise how every result was reached, where it lives, how to
regenerate it, what data the SchwingNet model uses and what it does not, how leakage is checked, and the state of every
manuscript, so the work can be redone in an organised way. Words you do not know are in `GLOSSARY.md`; every path
prefix and identifier namespace is defined once, in §0 below. How results were reached, in date order, is §11.

How it was written: by reading files on Greg's laptop only. Nothing was run on the grid, no network was used, and no
credential file was opened. Every count, date, path and claim names the file it comes from; a fact that no file records
is written "not recorded". Where two files disagree, both readings are given with the one trusted and why. Grid-only
files (paths starting `~` or `$RS`) were not re-verified. A verification pass on the same day checked the handoff against
its sources and ran the laptop tests (§12).

**Who may read what.** The folder sits in `spinesurg-ct-nnunet`, a private repository, and must never be copied into
CTSpinoPelvic1K, OpenSpineToolkit, Student_Projects, the website or a handout. Inside it there are two readers:

| reader | files |
|---|---|
| a student, **once Greg confirms this split** (`OPEN_QUESTIONS.md` A29) | `README.md`, `GLOSSARY.md`, `RECIPES.md`, `RESULTS_CATALOG.md`, `DATASET_USAGE.md`, `LEAKAGE.md`, `OPEN_QUESTIONS.md`, `INFRASTRUCTURE.md` |
| Greg and the Claude project only | `GREG_ONLY/` (credential locations, Greg's private records and decisions, withheld contact data), `MANUSCRIPTS.md`, `CONTEXT_EXPORT.md`, `context/`, `working_notes/`, `RESEARCH_DIRECTIONS.md`, `LITERATURE_STATE.md` and `literature_state/` |

Why each Greg-only file is Greg-only, and what a student copy of it would need cut: `GREG_ONLY/PRIVATE_STATE.md` §5.
Until Greg confirms, the whole folder is read by Greg and the Claude project only.

---

## 0. Keys: path prefixes and identifier namespaces

**Path prefixes** (every file here uses these; the Greg-only notes use older spellings, listed so they can be read):

| prefix | means | also written |
|---|---|---|
| `ssn:` | `<laptop:Desktop>/spinesurg-ct-nnunet/` (private, branch `L6_Class`) | `sscn/` (topic 4 note), `[SSN]`, `S/` (`literature_state/`) |
| `sn:` | `ssn:SchwingNet/` | — |
| `ctsp:` | `<laptop:Desktop>/CTSpinoPelvic1K-1/` (public) | `ctsp/`, `[CTSP]`, `C/` |
| `ostk:` | `<laptop:Desktop>/OpenSpineToolkit/` (public) | `ostk/`, `[OSTK]` |
| `bth:` | `<laptop:Desktop>/ashley-bridge/` (Beethoven, private) | `bth/` |
| `students:` | `ctsp:Student_Projects/` | `students/` |
| `np:` | `<laptop:Desktop>/NextPaper/` (`RESEARCH_DIRECTIONS.md` only) | — |
| `Desktop/` | `<laptop:Desktop>/` | — |
| `context/` | `HANDOFF/context/`: copies of the session's memory notes (index `context/INDEX.md`) | `mem:` in `RESULTS_CATALOG.md`; `memory/`, `[MEM]`, `M/` in the working notes and `literature_state/` mean the live memory folder `<laptop memory folder>/` (laptop only), whose spine notes are copied in `context/` or `GREG_ONLY/context*/` |
| `~`, `$HOME` | go2432's grid HOME `/wsu/home/go/go24/go2432` (a student's own `~` is different: `RECIPES.md` §0 item 9) | — |
| `$RS` | the grid Ceph volume `/rs/rs_grp_oschome/go2432` | — |
| `$RC` | `$RS/ruleclass` (`ssn:tools/transitional_review/anomaly_rules_array.sh` L16) | — |
| `D` | `~/data/CTSpinoPelvic1K` in `RECIPES.md` §9 | — |
| T1-T6 | the six reader notes `working_notes/topic1_...` to `topic6_...` (`OPEN_QUESTIONS.md` column "from") | "topic 1 §2" = `working_notes/topic1_schwingnet_carm_results.md` §2, and so on |

Bare paths: `docs/`, `tools/`, `slurm/`, `paper/rsnai/`, `paper/qi_universal_protocol/` without a prefix mean `ssn:`;
`paper/mpda/`, `scripts/`, `morphometrics/`, `zenodo/` without a prefix mean `ctsp:`; `plan/`, `db/`, `reacquire/` mean
`ssn:data_platform/`; `templates/` means `students:templates/`. A file named twice on disk is always given in full
(for example `sn:results/transitional_registry/acquisition/ACQUISITION_PLAN.md`, which also has a frozen copy under
`sn:results/fig6/frozen/v1/`). Citation keys are defined in the
file that uses them: `RESULTS_CATALOG.md` uses ids such as A3.1 and C1.6; `LITERATURE_STATE.md` uses keys such as NUM,
TAB3, CLM, RES (its key table near the top); `RESEARCH_DIRECTIONS.md` uses NUM:n, LS, ALPHA, HANH, LTDG and others
(its "File key" at the end); `literature_state/power.md` has its own "Citation keys".

**Identifier namespaces.** The same short id means different things in different files. In cross-references, write the
namespace:

| write | for | defined in |
|---|---|---|
| CAT-A1 ... CAT-G | result ids (A3.1, C1.6, F.14, ...) | `RESULTS_CATALOG.md` |
| OQ-A1 ... OQ-G | open-question rows (parts A-G) | `OPEN_QUESTIONS.md` |
| MAN-C1 ... MAN-C18 | contradictions between manuscript documents | `MANUSCRIPTS.md` §20 |
| RIG-A1 ... RIG-A9 | rigor-audit items of 2026-09-22 (A5 = per-source film naming) | `sn:results/RIGOR_FIXES.md` |
| LEAK-L1 ... LEAK-L7, LEAK-U1 | eval-gate verdicts (L = leaked family, U1 = the unresolved v2 lineage); never vertebra names | `sn:results/eval_gate/EVAL_LEAKS.md` |
| DIR-D1 ... DIR-D9 | Greg's data directives of 2026-09-23 (DIR-D1 = FluoroCap out of training) | `context/data-directives-2026-09-23.md` |
| PLAN-C7, PLAN-E3, ... | checklist boxes of `ssn:docs/RSNAI_PLAN.md` | that file |
| G0-G7 | flagship gates (G3 = the person split) | `ssn:docs/FLAGSHIP_PLAN.md` |
| INV-G8 | section G8 "Films" of `sn:results/indomain/INVENTORY.md` (not a gate) | that file |
| P2-D1 | the "D1 head" of paper 2 (`sn:tools/head_dual.py`) | `RECIPES.md` §2.4 |
| B00-B14 | data-migration batches | `ssn:data_platform/MIGRATION_PLAN.md` |

Existing text still uses the bare forms; read them through this table. Where a bare id could be ambiguous, the file says
which it means.

---

## 1. The programme in plain words

### The question

Can a computer name a vertebra (say "this is L4") from what the bone itself looks like, without counting down from the
skull (C2) or up from the sacrum? The question matters most at the lumbosacral junction, where transitional anatomy (a
sixth lumbar vertebra L6, a thirteenth rib-bearing vertebra T13, a sacralised L5) makes counting give the wrong answer
(`ctsp:CLAUDE.md` first paragraph; `context/local-level-identity-thesis.md`). The clinical stake is wrong-level spine
surgery: about 1 in 3,110 operations (Mody 2008), 12.8 per 10,000 (Jhawar 2007), 0.12 % of 34,544 (Furuya 2026);
transitional vertebrae occur in about 12.9 % of people, and 54 % of those were miscounted in clinic (Nakagawa 2017) (all as
recorded in `sn:LEVELCHECK_CLAIM.md` §2).

### The three projects

| project | what it is | where | visibility |
|---|---|---|---|
| **CTSpinoPelvic1K** | a CT dataset of 802 abdominopelvic records with per-level vertebrae, ribs, sacrum, hips, femora, surgical hardware and two-reader Castellvi grades; a Medical Physics dataset article, an accepted NeurIPS 2026 paper, and per-level and spinopelvic measurements | `ctsp:` | public |
| **SchwingNet** | a network that names vertebral levels from one intraoperative C-arm exposure or a plain film: two detectors, a ResNet-18 level encoder, a recurrent (BiGRU) head, a count from the detected sacrum, and a coupling rule that stops when the two disagree; paper 1 for Radiology: Artificial Intelligence, paper 2 against LevelCheck | `ssn:` (folder `SchwingNet/`) | **private** (repository private since 2026-09-14, `context/fluorocap-repo-private.md`; why and the current state: `GREG_ONLY/PRIVATE_STATE.md` §3) |
| **OpenSpineToolkit (ostk)** | the Python measurement library (pelvic incidence, lordosis, Cobb, per-level morphometry) the dataset and the student projects use | `ostk:` | public |

Sources: `working_notes/topic6_ctspinopelvic1k_and_toolkit.md` §1; `working_notes/topic1_schwingnet_carm_results.md` §1-2;
`working_notes/topic5_operating_here.md` §1.

### How they relate

- CTSpinoPelvic1K supplies labelled CT with transitional anatomy. Its CTs, with VerSe and TotalSegmentator, are rendered
  into synthetic radiographs (DRRs) that train SchwingNet's level encoder; these renders are the only source of labelled
  L6 and T13 examples the encoder has (`sn:REVISION_LOG3.md` §13, Greg: "if renders are my only source of rare classes they
  have to be included right?").
- ostk measures CTSpinoPelvic1K (and the dataset article's own extraction scripts measure it better on several
  quantities; see `RESULTS_CATALOG.md` part F).
- The **anomaly scan** (the transitional harvest, the registry and the "ruleclass SUPER DETECTOR RUN" over 21,622 CTs)
  exists to find enough transitional people to test SchwingNet on: paper 1 cannot certify transitional accuracy until
  35 error-free at-risk persons with a human read exist (`sn:results/power/power.json#n_needed_zero_errors`); today 7
  unverified real candidates exist, 4 from two labellers and 3 from one (`sn:sections/results.tex` lines 91-98;
  `sn:packet_src/persons_available_2026-09-24.json`; `RESULTS_CATALOG.md` A16.6).
- The **data platform** (`ssn:data_platform/`) records where every dataset came from and moves the data to the lab's Ceph
  volume; **Beethoven** (`bth:`) is how students reach the grid; **Student_Projects** (`students:RECIPE.md`) is the lab
  recipe.

### What "RSNA" and "QI" mean in Greg's request

- "RSNA" means three different things on disk (`working_notes/topic3_dataset_usage_leakage_rsna.md` §14-15): the
  **Radiology: Artificial Intelligence** manuscripts (RSNA is the publisher; this is almost certainly what "the RSNA
  work" means: `sn:main.tex` and the older `ssn:paper/rsnai/`), the **RSNA 2022 cervical-spine fracture CT archive**
  (fetched, 203 GB, never unpacked, used by nothing), and an older **RSNA 2024 lumbar MRI** download in
  `Desktop/lstv-detector`. See `MANUSCRIPTS.md` and `DATASET_USAGE.md`.
- "QI" is the quality-improvement manuscript `ssn:paper/qi_universal_protocol/main.tex` ("The Universal Protocol with a
  level in it"), a 9-page draft for The Joint Commission Journal on Quality and Patient Safety, never submitted; it must
  stay private (`MANUSCRIPTS.md` §5, Greg-only).

---

## 2. Map of repositories and folders

| place | one line | source |
|---|---|---|
| `ssn:` (private, branch `L6_Class`) | SchwingNet and the whole C-arm/film programme: `SchwingNet/` (paper 1, results, tools, slurm), `docs/` (~120 documents), `tools/` (723 Python files), `slurm/` (583 job scripts), `data_platform/`, `service/`, `benchmark/`, this `HANDOFF/` | topic 5 §1 |
| `sn:` | paper 1: `main.tex`, `sections/`, `supplement.tex`, `numbers_manifest.json`, `NUMBERS.md`, `results/`, `figures/`, `tables/`, `packet*/`, `paper2_levelcheck/` | topic 4 §2.2 |
| `ssn:data_platform/` | the data manifest (211 sources), layout, Ceph migration plan and SQLite index | `ssn:data_platform/README.md` |
| `ssn:paper/` | superseded C-arm drafts (`rsnai/main.tex`, `rsnai/main_v2.tex`, `focused/`) and the QI paper | topic 4 §4-5 |
| `ctsp:` (public, `master`, remotes `origin` and `osc`) | the dataset: build scripts, `morphometrics/`, `paper/mpda/` (dataset article), `CAMERA_READY_NEURIPS/`, `zenodo/`, `review_service/`, `docs/`; its root also holds untracked personal and administrative files and several manuscripts Greg named (`MANUSCRIPTS.md` §19) | topic 6 §0 |
| `students:` (nested repository, `main`) | the lab recipe `RECIPE.md`, the board `board.json` -> `BOARD.md`, onboarding; local commit 3f1cf04 deliberately not pushed | topic 5 §1, §11 |
| `Desktop/CTSpinoPelvic1K` | an older clone (last commit 2026-04-28); use `ctsp:` | topic 5 §1 |
| `ostk:` (public, `main`, both remotes) | ostk | topic 6 §9 |
| `Desktop/openspineconsortium.github.io` (public) | the website and the PACS demo; pushing publishes | topic 5 §1 |
| `np:spinopelvic-seg` | the Dataset803 pelvic pseudolabeller code; the NeurIPS camera-ready cites `OpenSpineConsortium/spinopelvic-seg` as the public code repository (commit 70de829, `ctsp:`); live visibility not re-checked (no network) | topic 6 §12; `MANUSCRIPTS.md` §7 |
| `np:spinopelvic-seg-mlhc` | MLHC-anonymised twin; its git configuration needs Greg's attention (`GREG_ONLY/PRIVATE_STATE.md` §2) | topic 6 |
| `np:AR`, `np:RadAI`, `np:bibm-spinopelvic`, `np:VerSeFusion` | frozen NeurIPS draft; CT one-shot Radiology: AI draft; BIBM wrap-up draft; VerSeFusion README | topic 4 §9-10 |
| `bth:` | Beethoven (browser extension + `hpcworker`), how students reach the grid; guides in `docs/guides/` | topic 5 §2.2 |
| `Desktop/ashley` | Beethoven for VS Code and the access service | topic 5 §1 |
| `Desktop/XRaySpinoPelvic1K` (private) | X-ray/DRR level localisation work, made private 2026-09-26 | topic 5 §1 |
| `Desktop/spine-detector` | radiograph corner-detector corpus (GitHub private); grid `~/spine-detector` | topic 5 §1 |
| `Desktop/private_ip/` (laptop only) | Greg's private records (`GREG_ONLY/PRIVATE_STATE.md` §3) | topic 4 §15 |
| `Desktop/u251-xenograft-murine-RNASeq-study` | a different project (U251 LITT RNA-seq); not part of this handoff | `GREG_ONLY/context/MEMORY.md` |
| Grid HOME `/wsu/home/go/go24/go2432` | code checkouts, environments, older banks (`~/*_fov96_ctx`, `~/*_drr`), `~/model_night`, `~/bench`, `~/scaling`, `~/ablate` | topic 5 §2.5 |
| Grid Ceph `$RS` | 20 TB lab volume: `data/`, `model_night/`, `ruleclass/`, `archive/`, `tmp/` | topic 5 §2.5 |

---

## 3. Where the data is

Do not rebuild the data side from this folder. Read, in order:

1. `ssn:data_platform/README.md`
2. `ssn:data_platform/DATA_MANIFEST.md` §1 (one card per source; 211 sources; totals)
3. `ssn:data_platform/MIGRATION_PLAN.md` §0 and `LAYOUT.md` (HOME to Ceph, batches B00-B14)

What SchwingNet uses and does not use is in `DATASET_USAGE.md` here. The state of the migration as last recorded on
2026-10-08 (`context/data-platform-migration-2026-10.md`, copied after its 13:34 rewrite): B00, B01, B02, B03, B08, B06
and B14 cut over (symlinks at the old paths, `.pre-ceph` originals kept until FINALIZE); B04, B07 and B09 copying;
TotalSegmentator v2.0.1, BUU, FluoroCap and the banks not yet on Ceph. **Unresolved for B01**: the same note records
B01 (TCIA CT Colonography, 1,057 GB) as cut over, and also that the dedup census found the CT Colonography raw DICOM
(721 GB) and `tcia_nifti` (336 GB) "on neither HOME nor Ceph", with nothing recording what removed them beyond the
2026-09-07 reclaim (re-acquisition route `tcia_ctsp_download`). Per-batch truth is `plan/runs/<B>/STATUS` on the grid
(`OPEN_QUESTIONS.md` B30). The literature-versus-holdings review written the same day is `LITERATURE_STATE.md` (with
`literature_state/power.md`, the full inventory of power calculations).

## 4. How to get on the grid

Use Beethoven; do not re-document it. Student guides (version 14.0.0, 2026-10-03): `bth:docs/guides/INSTALL.md`,
`USE.md`, `ACCOUNTS.md`, and the one-page `bth:release/14.0.0/guides/STUDENT_QUICKSTART.md` (its title still says 12.0.0).
A student needs a WSU grid account (sponsor Greg), Claude Pro or Max, Chrome, Google Authenticator for the grid code, and
GlobalProtect once; Greg approves the student, which adds a named ACL entry on `/rs/rs_grp_oschome` (`INFRASTRUCTURE.md`
§2; `bth:docs/guides/LAB_LEAD.md` §9). What a student account can and cannot run: `RECIPES.md` §0 item 9.

---

## 5. The ten rules that bind all work here

1. **Words and style.** Never use the word that `ctsp:CLAUDE.md` "Standing preferences" bans (the French-derived word for
   where data came from): write source, origin, lineage, where it came from, or label history
   (`context/writing-preferences.md` gives "source", "where the label came from", "label history"; Greg's brief of
   2026-10-08 gives "origin, lineage, where it came from"). No fractional version numbers; fold changes into the next
   integer version. Figure captions at most 60 words (target about 25); the argument goes in the text. Matrix tables in
   solid black with at most one outlined mark. Slides: no sideways bar charts. Affiliation is General Surgery (Wayne
   State / DMC), never Neurosurgery. Ashley Schehr is a person, never a product name. (`context/writing-preferences.md`,
   `figure-captions-terse.md`, `tables-black-not-colour.md`, `chart-preferences.md`, `user-affiliation-general-surgery.md`.)
2. **Every number carries its file.** A count, date, path or claim names the file it comes from; what no file records
   is written "not recorded"; say plainly what is not known (an unexplained failure recorded, not a guess)
   (`ctsp:CLAUDE.md` "How to be useful here").
3. **Check outside the computation.** The recurring failure here is a number that is wrong but plausible. Compare with
   published values, an independent implementation, the distribution's spread (not its median), a published
   prevalence; render the mask. An identity check (PI = SS + PT) cannot catch a shared bad landmark
   (`ctsp:CLAUDE.md`; `ctsp:docs/SPINOPELVIC_ESTIMATOR.md`).
4. **Labels and orientation.** Two label schemes exist and mixing them does not raise ("femur_left" comes back T4):
   call `ostk.labels.labels_for(volume)`, never import a fixed map. In release v11 identifier 29 is retired; anything
   that gates on 29 must go. Zero-pad case ids with `zfill(4)`. Canonicalise to RAS to analyse, never reorient when
   writing a label (`ctsp:CLAUDE.md`; `context/label-scheme-v4-vs-ostk.md`, `never-reorient-when-writing-labels.md`).
5. **Held out means the person was never seen.** An item is held out for a checkpoint only if its patient key is in
   neither the training nor the validation set of that checkpoint or any ancestor; a render inherits its CT's person;
   unknown is not clean. Every quoted score goes through `ssn:tools/eval_gate.py`. Never quote from the leaked banks
   (allspine v2, v6, v7, v8-for-VerSe, `anchor_drr`, `vindrps`: both defined in `GLOSSARY.md`)
   (`sn:results/eval_gate/EVAL_LEAKS.md`; `ssn:docs/DATA_ACCOUNTING.md`; `sn:NUMBERS.md`; `LEAKAGE.md`).
6. **Pre-register, then score; numbers come from files.** Write the rule and its success criterion before the run,
   hash it, stamp every output row with the hash; a number produced before the freeze is calibration. Comparators are
   pre-specified from the literature and never tuned. Manuscript numbers enter through `\RESULT{key}` from
   `numbers_manifest.json`, never typed (`sn:RESULTS_BUILD.md`; `ssn:docs/ruleclass/PREREG_rules.md` §9;
   `context/six-figure-paper-plan.md`; `students:RECIPE.md`).
7. **The grid's login node runs nothing.** Every computation, render, plot and download is an `sbatch` job; warrior
   kills python, rsync, node, pip, conda and others by name; no container command on warrior and nothing of ours under
   its `/tmp`. Use `sbatch -D <dir>` (relative `--output` resolves against the submit directory), `afterany` not
   `afterok`, `/dev/shm` for IPC (compute-node `/tmp` is swept), Ceph for large outputs; record a job before cancelling
   it; write grid bash for bash 4.2 (`context/no-jobs-on-login-node.md`, `grid-ssh-second-factor.md`,
   `grid-bash-4-2-quoting.md`; `ctsp:CLAUDE.md` "Grid"; `students:RECIPE.md` §5).
8. **What stays private.** SchwingNet and all level-identification code, text, figures and weights, FluoroCap, and the
   `spinesurg-ct-nnunet` and `XRSpinoPelvic1K` repositories stay private; nothing about them goes public until Greg says
   so; public framing of any work is research and education only; run `ssn:tools/disclosure_audit.py` before any talk or
   submission; for the CNS talk use only `Desktop/CNS2026_Schwing_NotAllSpines_public_v12.pptx`
   (`context/fluorocap-repo-private.md`, `cns-deck-v2-2026-09-25.md`; Greg's reasons and the current state:
   `GREG_ONLY/PRIVATE_STATE.md` §1, §3).
9. **Data directives.** Use all of a public dataset; a download budget is not a criterion; every truncation is fixed or
   justified in writing before a rerun; a leaked initialisation is fixed by retraining, never disclosed as a caveat;
   FluoroCap is out of training (DIR-D1); identity comes from metadata first and the file name last; the IRB umbrella
   (HPR 2026-269) covers only public, de-identified data downloadable without an agreement
   (`context/data-directives-2026-09-23.md`, `no-unexplained-subsets-fix-not-disclose.md`,
   `key-patients-from-metadata-not-filenames.md`; `students:RECIPE.md` §3).
10. **Git, network and credentials.** CTSpinoPelvic1K: commit directly to master and push to `origin` and `osc`;
    OpenSpineToolkit: branch `main`, both remotes; commit only when asked. Network (git push, ssh, rsync, Hugging Face)
    goes through `wsl -e bash -lc '...'` (exception: `ctsp:paper/mpda/make_submission.py` runs from Windows). Tokens are
    read from files, never echoed or put on a command line or in `sbatch --export`; nothing under
    `<laptop vendor folder, never read>` is read. Write scripts as files and run them by path (heredocs collapse
    backslashes) (`context/commit-directly-to-master.md`, `push-both-github-remotes.md`, `wsl-for-network.md`,
    `bash-heredoc-backslashes.md`; where each credential lives: `GREG_ONLY/PRIVATE_STATE.md` §2).

---

## 6. How to use this folder

| file | read it when | reader |
|---|---|---|
| `README.md` | first (this file) | student |
| `GLOSSARY.md` | a word you do not know | student |
| `RESULTS_CATALOG.md` | you need any number: its file, model, bank, split, tool, job, status, rigor marks and the figure or table it feeds. **Where any other file here (or a memory note) differs, the catalog wins** | student |
| `RECIPES.md` | you need to regenerate something: scaling plots, the film N-curve, the anomaly scan, power, DRR banks, device cards, the C-ArmLSpine experiment, the benchmark suite, CTSpinoPelvic1K measurements and figures, leakage checks; read §0 first (resume is not reproduce; who can run what) | student |
| `DATASET_USAGE.md` | Greg's question "what does SchwingNet use and what not" | student |
| `LEAKAGE.md` | how held-out is enforced, how to run the checks, what they found | student |
| `OPEN_QUESTIONS.md` | everything that could not be settled from files, with where to look and who can answer; includes where a verifier was wrong (part G) | student |
| `INFRASTRUCTURE.md` | operating the grid, storage, containers, jobs, the registry, environments | student |
| `MANUSCRIPTS.md` | every paper, abstract, deck and data request, with a redo plan in order | Greg + Claude |
| `RESEARCH_DIRECTIONS.md` (written 13:04-13:43, committed e4c3e88) | what to do next: 16 ranked projects, an anomaly-aware fluoroscopy classifier, CT projects, 3-D to 2-D parity; its keys (NUM:n, LS, ALPHA, HANH, LTDG, ...) are in its "File key" at the end, and its own header lists three cuts before a student copy | Greg + Claude |
| `LITERATURE_STATE.md`, `literature_state/` | written earlier the same day (commit d5dee9a): the literature against the holdings, dataset sizes, the power inventory; written before the catalog's supersession marks, so read its status table at the top | Greg + Claude |
| `CONTEXT_EXPORT.md` | the digest of all 165 memory notes, what was copied where, and what else lives only in the session | Greg + Claude |
| `context/` | copies of 141 live spine-imaging memory notes; **`context/INDEX.md`** lists them with a status that names what replaces a leaked or superseded note | Greg + Claude |
| `working_notes/` | the six detailed reader notes this handoff was built from (full tables, every contradiction, every unknown), `t2_wilson_check.py`, and `builders/` (the scripts that built and refresh the handoff) | Greg + Claude |
| `GREG_ONLY/` | `PRIVATE_STATE.md` (Greg's private standing positions, credential locations, Greg's private records, withheld contacts, the reader split) and the notes moved out of `context/` | Greg + Claude |

A fresh Claude project should load `README.md`, `INFRASTRUCTURE.md` and `context/INDEX.md` as standing context (not
`MEMORY.md`, which is archived in `GREG_ONLY/context/`: its one-line summaries carry leaked numbers and point at notes that
were not copied), plus `GREG_ONLY/PRIVATE_STATE.md` for Greg's own project, then open the other files as needed. The two
`CLAUDE.md` files (`ssn:CLAUDE.md`, `ctsp:CLAUDE.md`) remain the working-context files of their repositories;
`ssn:CLAUDE.md` still says to run `tools/pipeline_state.py` on the login node and does not point here
(`OPEN_QUESTIONS.md` F10). Before handing the folder over, refresh the copies:
`python HANDOFF/working_notes/builders/refresh_context.py`, then `build_context_index.py`.

---

## 7. Where things stand on 2026-10-08 (the short version)

| thread | state | source |
|---|---|---|
| SchwingNet paper 1 | complete in review and camera-ready copies; one placeholder (VinDr determination number); supplement 13 pages against a 12-page cap; Word packets stale; held from submission by Greg (the ERAS CV says "Submitted": contradiction MAN-C4; why it is held: `GREG_ONLY/PRIVATE_STATE.md` §3) | `MANUSCRIPTS.md` §2 |
| Paper 2 (LevelCheck comparison) | comparator frozen; open gate scored names only (a path bug in `sn:tools/fig6_score.py`); blinded gate cancelled 2026-09-27; needs human reads of transitional test persons | `MANUSCRIPTS.md` §3 |
| CTSpinoPelvic1K dataset article (Medical Physics) | third packet built 2026-09-25; whether uploaded not recorded | `MANUSCRIPTS.md` §6 |
| NeurIPS 2026 paper 3474 | accepted (poster); the committed camera-ready (38b0cb9) is 21 pages; the uncommitted 2026-09-27 working copy is 31 pages with 134 `[pending]` slots whose jobs were cancelled 2026-09-27; recomputation scripts only in a Temp scratchpad | `MANUSCRIPTS.md` §7 |
| CNS 2026 talk (2 Nov) | use only the public v12 deck | `MANUSCRIPTS.md` §13 |
| Anomaly scan | ruleclass arms running on 2026-09-27 (outcome after that not recorded); pre-registration DRAFT v1 unsigned; review-tree code untracked and not recorded as run | `RESULTS_CATALOG.md` part D; `RECIPES.md` §3 |
| Data platform | migration to Ceph in progress (§3) | `ssn:data_platform/` |
| Leakage | the person-level gate is in place; the full content-hash chain has never been run on the real corpus; the C-ArmLSpine fold banks behind Table 3 still hold VinDr, FluoroCap and both NHANES copies, while v9-base fold models without them exist as the 250 `name_fill` cells (REP truth, per protocol cell) | `LEAKAGE.md`; `DATASET_USAGE.md` §3.2 |

---

## 8. A student's first week

| day | do | done when |
|---|---|---|
| 1 | Read this README, `ctsp:CLAUDE.md`, `ssn:CLAUDE.md` (its login-node `pipeline_state.py` line is outdated: run it in a job), `students:RECIPE.md`. Request a WSU grid account and follow the Beethoven `INSTALL.md` and `USE.md`. Get repository access (§9). | you can open a worker on the grid |
| 2 | Read `ssn:data_platform/README.md` and `DATA_MANIFEST.md` §1, then `DATASET_USAGE.md` and `LEAKAGE.md` here. | you can say which bank trained the encoder and why VinDr is a problem |
| 3 | On the laptop (no grid; environment in §9): run the self-tests `python -m pytest tests/test_eval_gate.py -v`, `python tools/test_patient_keys.py`, `python tools/test_stats_compare.py`, `python tools/test_leak_check.py` in `ssn:`, and `python -m pytest` in `ostk:`. Re-derive the power numbers with `python HANDOFF/working_notes/t2_wilson_check.py` and compare with `RESULTS_CATALOG.md` part E. | the results match those of 2026-10-08 (§12): `test_eval_gate` 58 passed; `test_patient_keys` and `test_stats_compare` 0 failures; **`test_leak_check` fails on one known stale fixture** ("30 real names, 1 wrong": the Geneva phantom is now keyed as one person, `sn:results/eval_gate/EVAL_LEAKS.md` item 3; OQ-F17); **ostk 1 failed, 100 passed** (`tests/test_cobb.py::test_cobb_falls_back_gracefully_without_femurs`, OQ-F18); 35 / 22 persons reproduce. Any other failure is new: report it |
| 4 | Read `sn:results/eval_gate/EVAL_LEAKS.md`, `sn:results/coverage/PER_LEVEL_DOMAIN_ANGLE.md` and `RESULTS_CATALOG.md` parts A and D. Rebuild one figure from committed files in `ctsp:` without touching the committed copies: copy `morphometrics/level_atlas.csv` aside (the script always rewrites it, `paper/mpda/make_levelatlas_fig.py` L475), run `python paper/mpda/make_levelatlas_fig.py --out <scratch dir>`, then compare (`git diff --stat -- morphometrics/level_atlas.csv`; look at the new PNG beside `paper/mpda/figures/fig_levelatlas.png`) and put the copied CSV back. Its inputs `degenerative.csv` and `opportunistic.csv` were written before v11 (topic 6 flag F4). | the CSV shows no diff and the figure looks the same; commit nothing |
| 5 | With Greg, pick one item from `OPEN_QUESTIONS.md` or `students:BOARD.md`; write its `PREREG.md` (rule, success criterion, inputs) before running anything; submit nothing on the login node. | Greg has signed the PREREG |

Questions only Greg can answer (ask in week one): was SchwingNet uploaded; was the Medical Physics packet uploaded and
under what number; what is the VinDr determination number; is the NeurIPS camera-ready deadline past; does Greg want the
ratio sweep, the per-level supplement table and seeds above N = 25 (`OPEN_QUESTIONS.md` part A); is the reader split of
this folder confirmed (A29). Greg's own questions are in `GREG_ONLY/PRIVATE_STATE.md` §3.

---

## 9. Getting access

**The repositories.** Clone each folder from its remote (`git remote -v`, 2026-10-08; `INFRASTRUCTURE.md` §1):

| laptop folder | clone from | branch | visibility | who grants access |
|---|---|---|---|---|
| `ssn:` | `github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet` | `L6_Class` | private | Greg (how a student is added is not recorded) |
| `ctsp:` | `github.com/OpenSpineConsortium/CTSpinoPelvic1K` (also `Gregory-Schwing-MD-PhD/CTSpinoPelvic1K`) | `master` | public | — |
| `students:` | `github.com/OpenSpineConsortium/Student_Projects` (project work in the private `OpenSpineConsortium/Projects`) | `main` | public / private | Greg |
| `ostk:` | `github.com/OpenSpineConsortium/OpenSpineToolkit` (also `Gregory-Schwing-MD-PhD/OpenSpineToolkit`) | `main` | public | — |
| `bth:` | `github.com/OpenSpineConsortium/beethoven` | `main` | private | Greg; students install the extension from its private Chrome listing instead (`INFRASTRUCTURE.md` §2.2) |

**This folder is not in a clone yet.** On 2026-10-08 only `HANDOFF/LITERATURE_STATE.md`, `HANDOFF/literature_state/` and
`HANDOFF/RESEARCH_DIRECTIONS.md` are committed; every other file here is untracked (`git status`). Greg decides when to
commit it, and whether `GREG_ONLY/` is committed to the same repository at all (commit only when Greg asks).

**A laptop environment for the tests.** No environment file targets a laptop (`ssn:env/*.yml` are the grid's). The tests
of §8 day 3 ran on 2026-10-08 under Python 3.12.4 with numpy 2.5.3, scipy 1.18.1, pytest 9.0.3 and nibabel 5.4.2; ostk
declares numpy >= 1.24, scipy >= 1.10, nibabel >= 5 and, for its tests, pytest >= 7 (`ostk:pyproject.toml`). A student
needs Python 3.12 with those four packages; `HANDOFF/literature_state/power_calc.py` also needs scipy.

**Code to the grid.** The grid can no longer fetch the private repository; the route that worked for Greg is a
`git archive` of a committed tree piped over ssh (`RECIPES.md` §0 item 2). A student works in a grid checkout of the
public repositories; how a student gets private SchwingNet code onto the grid is not recorded (Greg decides).

---

## 10. People and roles

| who | role | source |
|---|---|---|
| Greg Schwing | resident physician (`MANUSCRIPTS.md` §20 C6), Department of General Surgery, Wayne State University School of Medicine / Detroit Medical Center (never Neurosurgery); owns grid account `go2432`; signs off on every freeze and submission | `context/user-affiliation-general-surgery.md`; `students:RECIPE.md` §0 |
| Ashley Schehr | a person (never a product name): senior scientist and co-PI; stage-1 screener of the transitional review; first author of the med-ed study; annotation lead | `students:RECIPE.md` §0; `MANUSCRIPTS.md` §0, §12; `RECIPES.md` §3.3 |
| "Dr Tech" | senior clinical PI; stage-2 confirmer of clinical reads; full name and e-mail recorded nowhere on disk | `students:RECIPE.md` §0; `OPEN_QUESTIONS.md` A18 |
| NeurIPS 3474 co-authors | Gregory John Schwing, Patrick Schwing (LSU Health Sciences Center New Orleans, School of Medicine), Miraziz Ismoilov, Nizar Alnabahneh, Loren Schwiebert | `ctsp:CAMERA_READY_NEURIPS/REVIEWER_CRITIQUES.txt` (via `MANUSCRIPTS.md` §7); `ctsp:` commit 38b0cb9 |
| MPDA authors | 14 authors on the title page (Loren Schwiebert not among them) | `MANUSCRIPTS.md` §20 C11 |
| Castellvi readers | two radiology residents, columns `read_1_NA` and `read_2_MI` of `ctsp:docs/castellvi_consensus.csv`; PGY year not recorded | `RESULTS_CATALOG.md` F.14; `OPEN_QUESTIONS.md` A27 |
| student annotators | 11 student usernames in the committed tally `ctsp:morphometrics/annotation_counts.csv` | `INFRASTRUCTURE.md` §11 |
| hpc@wayne.edu | grid accounts (sponsor Greg, about two business days) | `INFRASTRUCTURE.md` §2.1 |
| C&IT | owns group `oschome`; issued the grid etiquette of 2026-09-28 (no container commands on warrior, nothing under its `/tmp`); the contact person is not recorded | `ctsp:CLAUDE.md` "Grid"; `INFRASTRUCTURE.md` §2.2 |
| IRBQuestions@wayne.edu | where the VinDr-SpineXR HPR determination request goes | `OPEN_QUESTIONS.md` A5 |
| how to reach Greg | not recorded in any handoff file | — |

---

## 11. How the results were reached: a dated timeline

Each row is one finding or decision, the file that records it, and the catalog id where one exists. Superseded numbers
exist because a later row found the bank they were measured on leaky or replaced it; read the rows in order.

| date | finding or decision | file | catalog |
|---|---|---|---|
| 2026-09-07 | CTSpinoPelvic1K v10 published on Zenodo (22642578); the 1.9 TB September tree on the grid reclaimed | `context/zenodo-deposit.md`; `context/data-platform-migration-2026-10.md` | — |
| 2026-09-10 | ostk commit 1b7005c introduces the canal-closing regression (10-17 mm on about one vertebra in seven) | `context/ostk-canal-closing-regression.md` | G.2 |
| 2026-09-13 | first 2-D level identification on real films (`films_ann`, `films_all2` banks) | `context/level-id-2d-results-2026-09-13.md` | C1.1, C1.2 |
| 2026-09-14 | `spinesurg-ct-nnunet` made private; the deployed level bank found to hold no T2-T11, T13 or L6 crops, so all-spine banks begin | `context/fluorocap-repo-private.md`; `context/level-model-bank-coverage.md` | — |
| 2026-09-15 | evaluations found scoring renders whose CT was in training; a 2.5-hour model destroyed by `ln -sf` (the registry rule) | `LEAKAGE.md` §5.3; `ssn:docs/MODEL_REGISTRY.md` | — |
| 2026-09-16 | recurrent head restored; CTSP v11 defined (the S1 carve withdrawn, commit 73cc398) | `context/recurrent-head-restored-2026-09-16.md`; `ctsp:` git log | — |
| 2026-09-17 | the synthetic / real fraction sweep on allspine v2 (later found leaky); remedies refuted; anomaly manifest | `sn:results/indomain/grid/scaling_curve_2026-09-17.json`; `context/remedies-refuted-2026-09-17.md` | C2.1 |
| 2026-09-18 | CTSP v11 published on Zenodo (22797014) | `ctsp:paper/mpda/cover_letter.md` | — |
| 2026-09-19 | RSNA 2022 cervical archive fetched (on the login node, now forbidden) | `DATASET_USAGE.md` §7 | — |
| 2026-09-20 | allspine v2-v5c deleted for quota; hold-out runs silently fell back to fitted cases until `holdout.py` raised | `context/grid-quota-and-deleted-banks.md` | — |
| 2026-09-21 | C-ArmLSpine becomes "the project"; first cross-validation (v2 lineage) 606 / 617 | `ssn:docs/HANDOFF_2026-09-21_PM.md`; `ssn:docs/carmlspine_cv5_mixed_2026-09-21.json` | A3.11 (superseded) |
| 2026-09-22 | NHANES II found in the banks twice; CTSP under two names; VerSe series keyed as subjects; the rigor audit; the v8 bank; `sn:main.tex` begun from rigor-passing numbers | `LEAKAGE.md` §5.1-5.3; `context/rigor-audit-findings.md`; `MANUSCRIPTS.md` §2.1 | C1.6, C1.8 |
| 2026-09-23 | Greg's held-out rule and data directives D1-D9; the v9 bank chain (jobs 40415667-70); the G3 person split applied 20:18:48 (job 40426793); first CHK-9; all 692 COBRA cases fetched | `sn:results/eval_gate/EVAL_LEAKS.md`; `context/data-directives-2026-09-23.md`; `sn:results/rare_class/split_plan.md` | D.6 |
| 2026-09-24 | paper split (LevelCheck to paper 2); the EVAL_LEAKS sweep (563 quoted rows); the CV re-run on v9 (601 / 617); `det_fill` 08:07 and `name_fill` 08:35; the registry 11:07; the film N-curve 23:25 | `context/paper-split-2026-09-24.md`; `LEAKAGE.md` §5.3; `RECIPES.md` §1.2-1.3, §2.1 | A3.1, A9, A10, D.8 |
| 2026-09-25 | Figure 5 rebuilt around acquisition space (7bb37ed); the census table; the render ablation asked for; the MPDA third packet; SchwingNet held from submission | `sn:figures/figure5.record.json`; `ssn:docs/CENSUS_TABLE_2026-09-25.md`; `MANUSCRIPTS.md` §2, §6 | A10.6, D.13 |
| 2026-09-26 | `XRaySpinoPelvic1K` made private; the two-arm ruleclass design determined 23:50 | `INFRASTRUCTURE.md` §1; `RECIPES.md` §3.2 | — |
| 2026-09-27 | the ablation enters the manuscript (7e81dd7) and the builds of record (05e05dc, jobs 40483839 / 40483840); every non-ruleclass job cancelled 15:50; last spine resume block 18:05 | `ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`; `ssn:docs/RESUME_2026-09-22_PM.md` | A10.8-A10.9 |
| 2026-09-28 | C&IT grid etiquette added to `ctsp:CLAUDE.md` (7ddfe38); grid `~/.ashley` wiped during a phone session | `ctsp:` git log; `context/grid-ashley-deletion-2026-09-28.md` | — |
| 2026-10-03 | Beethoven 14.0.0 (2f90319) | `INFRASTRUCTURE.md` §1 | — |
| 2026-10-07 | the data platform begun: manifest, re-acquisition, Ceph migration, index | `context/data-platform-migration-2026-10.md` | — |
| 2026-10-08 | migration batches cut over; this handoff written and verified | §3; §12 | — |

---

## 12. Verification record

**2026-10-08, afternoon.** Three verifiers read every handoff file against its sources and reported 56 findings: 2
blockers, 25 major and 29 minor. Each was checked against the cited files before anything was changed; where a verifier was wrong
or partly wrong, the evidence is in `OPEN_QUESTIONS.md` part G. What was checked and changed:

- **Run on the laptop**: `python -m pytest tests/test_eval_gate.py` (58 passed); `tools/test_patient_keys.py` and
  `tools/test_stats_compare.py` (0 failures); `tools/test_leak_check.py` (fails: one stale Geneva fixture, recorded as
  OQ-F17, fixture not changed); `HANDOFF/working_notes/t2_wilson_check.py` (35 / 22 / 53 / 34 / 69 / 45 / 113 / 74
  reproduce); `python -m pytest` in `ostk:` (1 failed, 100 passed: `test_cobb_falls_back_gracefully_without_femurs`,
  OQ-F18); `HANDOFF/literature_state/power_calc.py` after its output path was fixed (output identical to the stored
  `power_calc.json`). Nothing ran on the grid; no network.
- **Reader split** (blocker): Greg's private standing positions, the credential locations (old `INFRASTRUCTURE.md` §9), the
  repository clean-up state and Greg's private records, the token pointers and the Greg-only questions moved to
  `GREG_ONLY/PRIVATE_STATE.md`; the five corresponding memory notes moved to `GREG_ONLY/context/`; the reader table at
  the top of this file; Greg confirms the split before any student gets access (OQ-A29).
- **Recipes** (blocker and majors): the v9 bank row is now "record of how it was built; do not rerun in place" with a
  copy-and-compare procedure; the G3 split is marked frozen; resume versus reproduce (§0 item 6); the code-to-grid route
  and the `make physics` hard-reset warning (§0 item 2); who can run what and what `~` means (§0 item 9); every array job
  given its header's `--array`; `closure_only.sh` as an `sbatch` job; CHK-9 as its recorded job; the list audit as its
  job; the scaling-sweep traps and its selection split; full argument lists for `transitional_subtypes.py`,
  `acquisition_census.py`, `counting_report.py`, `merge_banks.py`; the `name_fill` order; benchmark `-D` and partitions;
  `stats_compare.py` subcommands and its help crash; TinyTeX; the fake-corpus command; the device-card overwrite.
- **Numbers**: `RESULTS_CATALOG.md` A16.6 / A16.7 re-cited (the 7 at-risk persons are 4 two-labeller + 3
  single-labeller; the figure-record key was retired), A18.2 DISPUTED, E.14 marked, C2.1 [SEL-SPLIT] and its twin count
  re-attributed to v6 / v7, A2.7, A3.10, A8.8, A10.10, D.14, E.3 and F.14 corrected; `LEAKAGE.md` CHK-4, the first CHK-9,
  the NHANES twin count and the 149 / 148 / 141 C-ArmLSpine counts; `DATASET_USAGE.md` (the `name_fill` cells are v9-base
  fold models without VinDr or FluoroCap; a source column on every row of §2; citations); `MANUSCRIPTS.md` (last
  commits, 21 versus 31 pages, the named files in the `ctsp:` root, the released-code citation);
  `LITERATURE_STATE.md` and `literature_state/power.md` (the superseded 98.2 % replaced by 97.4 %; a status table of every
  stale number found).
- **Context**: re-copied by `working_notes/builders/refresh_context.py` (last at 16:33, after the data-platform note's rewrites of 13:34 and 16:20) with
  the new `grid-bash-4-2-quoting` note, line endings kept; three notes redacted (contact and per-student data, full
  copies in `GREG_ONLY/context/`); the six Beethoven notes copied to `GREG_ONLY/context_beethoven/`; `context/INDEX.md`
  replaces `MEMORY.md` as the standing index, with LEAKED / SUPERSEDED statuses; `CONTEXT_EXPORT.md` updated to match.
- **This README**: the keys (§0), the reader split, access (§9), people (§10), the timeline (§11), the index now lists
  `RESEARCH_DIRECTIONS.md`, `GREG_ONLY/` and `context/INDEX.md`, and the first-week checks state the known failures.
  `GLOSSARY.md` gained the missing terms and the MPDA / MDPA alias.

Not changed (decisions for Greg, all in `OPEN_QUESTIONS.md`): the stale test fixture (F17) and the ostk test (F18); the
manuscript sentence that calls the seven a two-labeller count (F19); `ssn:CLAUDE.md` (F10); commits of `HANDOFF/`.
