# STATUS.md: what is in hand on 2026-10-08

Rigor marks used here: **MEASURED** (observed on the grid or in a running browser, dated, with the job id or file);
**RECORD** (a document states it; not re-measured today); **DATED** (a state at its date); **SUPERSEDED** (replaced
by the item named); **NOT RECORDED** (no file on the laptop or the grid says). This project owns no row of
`docs/handoff/RESULTS_CATALOG.md`: the catalog's part G is the toolkit's and G.8 (the PACS demo latency) belongs to
`12_website_pacs_demo`. Nothing here is a model score and nothing here went through the evaluation gate, because
nothing here is a model.

## A. Beethoven, the browser edition and the framework

| item | value | file | mark |
|---|---|---|---|
| current release | 14.0.0, built 2026-10-03 13:45 UTC on top of e11ae27, package `beethoven-14.0.0-chrome.zip` 503,489 B, SHA-256 `f0abebd8b6384bbbcc9adabef3c0d367936f3920d4425a6b82f50c854cd6df38`; commit 2f90319 "Beethoven 14.0.0 and framework 14" | `docs/beethoven/release_14.0.0/README.md`; `MANIFEST_CODE.md` | RECORD |
| framework on the grid | framework 14 published to `/rs/rs_grp_oschome/shared/beethoven/hpcworker/current` (the memory note, entry 5 of 2026-10-03); the release README written at build time says "Framework 14 is not published": the note is later | `memory/beethoven-2026-10-02-field-failures.md`; `docs/beethoven/release_14.0.0/README.md` | RECORD (two documents, the later one wins) |
| release ladder | 2.0.0 (2026-09-29 morning) icon-click flow; 3.0.0 (a74de0c, afternoon) store kit; 4.0.0 (835e1b4, evening) no licence keys, access check live; 5.0.0 (4c6eada, night) the shared copy; 7.0.0 (night) the name Beethoven; 8.0.0 (c05f595, 2026-09-30) private Chrome listing only, one installation per account; 9.0.0 (782e648) theme, never submitted; 10.0.0 (f8d2e88, 2026-10-01) two first-run defects fixed; 11.0.0 (95d7eea, 2026-10-02) first-run redesign, framework 10 never deployed; 12.0.0 (8af64d6, 2026-10-02) the direct way by ssh, framework 11 then 12 (7c8a484) deployed; 13.0.0 (e11ae27, 2026-10-03) the dead-run fix; 14.0.0 (2f90319) | `memory/ashley-bridge-project.md` (2.0.0 to 12.0.0 and the 2026-10-02 entries); `memory/beethoven-2026-10-02-field-failures.md` (13.0.0 e11ae27, 14.0.0 2f90319); `docs/beethoven/release_14.0.0/README.md` (14.0.0 built on e11ae27) | DATED |
| store state | 9.0.0 "NEVER submitted and must not be uploaded"; 10.0.0 "has not been submitted to the store as far as I know"; store kits exist for 9.0.0, 10.0.0, 12.0.0; the private listing's trusted testers are a Google Group Greg maintains; Official URL and trusted testers reported done in the Chrome dashboard on 2026-10-01 | `memory/ashley-bridge-project.md`; `docs/beethoven/store/SUBMISSION.md` | whether any build was submitted: NOT RECORDED |
| Remote Control from a Slurm job | registers from an `sbatch` job under a pseudo-terminal: job 40496445 on asx15, 2026-09-29 02:22 UTC (open question 1 of the product: yes) | `docs/beethoven/repo_root/CLAUDE.md` "Grid"; `docs/beethoven/OPEN_QUESTIONS.md` row 1 | MEASURED |
| compute-node egress | from asx15 on 2026-09-28: `api.anthropic.com` 404 (reachable), `platform.claude.com` 200, `claude.ai` 403 to curl, `statsig.anthropic.com` no DNS record | `code/beethoven_framework_profiles/wayne.json` `egress.measured` | MEASURED |
| the grid's ssh | `grid.wayne.edu:22` answers from the internet: OpenSSH 7.4, RSA host key only (SHA256:kLTz1xK6anQ1denM+31kDEryQtgan2P76r9aLno+K3s), aes-ctr ciphers, MAC hmac-sha1 only; publickey, password, keyboard-interactive; the second factor is Google Authenticator TOTP enrolled in Open OnDemand's 2FA Setup app on the VPN; a key skips password and code | `memory/grid-ssh-second-factor.md`; `wayne.json` | MEASURED 2026-10-01 and 2026-10-02 |
| first run as a student | Greg's worker queued 6 min on `reqp` and came online (job 40523644, 2026-10-01); the first-run flow was rejected and redesigned as 11.0.0 | `memory/beethoven-first-run-ux.md` | MEASURED |
| field use 2026-10-02 | failure 1, "Connecting to Claude..." forever on the direct way (a dead run record never aged out; Greg's worker preempted at 20:42): **fixed** in 13.0.0 + framework 13; failure 2, VPN-route sign-in sittings die at about 4 min 20 s after the job starts, four times (jobs 40552222, 40552237, 40552239, 40552241, 40552343, 40552346, exit 3), a terminal `hpcworker claude login` worked at 21:22: **open**; failure 3, `reqp --qos=requeue` preempts running workers, renewal 40523658 PENDING more than 12 h at QoS priority 100 while `secp` (priority 200, 90-day MaxWall) had 45 idle nodes: **open, Greg's call**; failure 4, group `oschome` is not the list: **resolved by the gate**; failure 5 (2026-10-03 07:50), a healthy worker on a resumed session's link shown as connecting (job 40554211; the framework's sed class `[ -\/]` also ate the letter after ESC[K): **fixed** in 14.0.0 + framework 14 | `memory/beethoven-2026-10-02-field-failures.md`; `docs/beethoven/V12_STATUS.md` (the three dated entries after section 8); `docs/beethoven/release_14.0.0/README.md` | MEASURED |
| the browser-ssh prototype | an ssh client on WebCrypto completed one pinned, unauthenticated handshake with the real `grid.wayne.edu` (2026-10-01); four fixable flaws, no fundamental one; nothing ran against the grid with a credential | `memory/beethoven-browser-ssh.md` | MEASURED (prototype) |
| the Isolated Web App spike | works on Chrome 154 stable and Chromium 153 in developer mode (raw TCPSocket, key sign-in to a grid-like local sshd, one credential-free handshake with the real grid, no VPN); install is 12 steps through developer flags; verdict: opt-in pilot beside the extension, not the main path; nine major findings incl. gate verbs running python3 on warrior | `memory/beethoven-browser-ssh.md` "Spike result" | MEASURED 2026-10-02 |
| the 12.0.0 blocker | framework 11's browser-key check refused because three CephFS scaffold folders above the volume were world-writable without sticky and owned by root or another lab; framework 12 made them notes, with four notes for C&IT | `memory/ashley-bridge-project.md` (2026-10-02 late); `docs/beethoven/V12_STATUS.md` section 7 item 3 | MEASURED |
| queue on 2026-10-08 22:20 UTC | `hpcw_worker` 40580248 RUNNING, 40581552 PENDING (Dependency), `hpcw_access` 40584406 PENDING (BeginTime) | the read-only grid pass copied into `10_data_platform_grid` | MEASURED (by listing) |

## B. The access gate

| item | value | file | mark |
|---|---|---|---|
| group `oschome` | two members on 2026-09-29 and 2026-10-02; C&IT alone adds members; students are in `wsu` / `hpcgrid` only | `memory/grid-access-list-gate.md`; `docs/beethoven/WAYNE_STATE_PILOT.md` | MEASURED |
| the volume root | `/rs/rs_grp_oschome` is a link to the physical folder, owned by go2432, `drwxrws--T`, `other::---`, sticky since 2026-10-02; entries `go2432/` (closed) and `shared/` | same | MEASURED |
| the design | approved = `user:<id>:rwx` on the root (rwx because the profile puts each student's state at `/rs/rs_grp_oschome/$USER/hpcworker`, its literal `shared_state_dir`); below the gate `shared/` `o+rx` and `shared/beethoven` `chmod -R o+rX` plus default `o::r-x` (34,000 files, 23 s, by hand 2026-10-02); `shared/access` and `go2432/` stay closed | same; `docs/beethoven/guides/LAB_LEAD.md` section 9 | MEASURED |
| reconciliation | `tools/grid_access.sh` (Beethoven repository) keeps the ACL list equal to `admin.mjs roster` about every fifteen minutes while Greg's PC is on (the Windows scheduled task "Beethoven grid access"); extension grants only; lab-only approvals and the reviewers' mock are not on it by design | `docs/beethoven/repo_root/CLAUDE.md`; `docs/handoff/INFRASTRUCTURE.md` section 2.2 | RECORD |
| what works | "only the entry ... set by hand on 2026-10-02 has been seen to work" | `docs/beethoven/guides/LAB_LEAD.md` (section 9, the line redacted here) | MEASURED, n = 1 |
| the roster | in the access service, not on disk | `docs/handoff/OPEN_QUESTIONS.md` B34 | NOT RECORDED here |

## C. Beethoven for VS Code and the access service

| item | value | file | mark |
|---|---|---|---|
| published item | Ashley for VS Code 3.0.0 published on the Marketplace 2026-09-28 20:24 UTC as `OpenSpineConsortium.ashley` under the publisher `openspineconsortium` | `memory/ashley-extension-project.md` | RECORD |
| built, not published | Beethoven for VS Code 4.0.0 built and signed 2026-09-30 (pass 28), new Marketplace id `openspineconsortium.beethoven`; Greg uploads, then unpublishes (never removes) the old item | `docs/beethoven_vscode/CHECKPOINT_2026-09-28.md` "CURRENT STATE"; `docs/beethoven_vscode/MARKETPLACE.md` | whether uploaded: NOT RECORDED |
| access service | deployed 2026-09-28 about 19:25 UTC (`ashley-service`), second name `beethoven-access` from 2026-09-29; service v2 (cb6b143, 2026-09-30: seats by installation, grants extension / lab, request portal with CV, mailbox proof); 9ba36d2 deployed under both names 2026-10-01 09:00 UTC; b7a4929 2026-10-01 (student mail on, Resend domain verified); 8d7fc65 2026-10-02 (service-wide seat rule) | `memory/ashley-bridge-project.md`; `docs/beethoven_vscode/CHECKPOINT_2026-09-28.md`; `MANIFEST_CODE.md` | RECORD |
| the compliance boundary | the extension never collects, stores or intermediates a Claude credential; the student signs in to the unmodified binary with their own subscription; enforcement since April 2026 falls on students' subscriptions | `memory/ashley-compliance-boundary.md`; `docs/beethoven_vscode/research/reports/Ashley terms of service constraints.md` | RECORD (binding) |
| terms | browser edition LICENSE version 9 and PRIVACY version 10 (2026-10-02, 12.0.0 and later); terms version 3 of the VS Code edition shipped 2026-09-28 (courts, not arbitration; 60-day notice-and-cure; cap the greater of 12 months' fees or $100) | `docs/beethoven/repo_root/LICENSE.txt`, `PRIVACY.md`; `memory/ashley-compliance-boundary.md` | RECORD |
| open written answers | Anthropic (hosting the unmodified binary under each student's subscription), Wayne State C&IT (the generative-AI guideline), WSU Office for Technology Commercialization, counsel; a notice address for the support page | `docs/beethoven/OPEN_QUESTIONS.md` "Two questions that are not technical"; `memory/ashley-extension-project.md` | NOT ANSWERED on 2026-10-08 |

## D. The recipe, the board and onboarding

| item | value | file | mark |
|---|---|---|---|
| RECIPE.md | 12 sections and 2 appendices (roles; project shape; pre-register and freeze; data rules; refuse-early code with the `run_record()` block; the 14 grid rules with the incident behind each; Nextflow; results to manuscript; checking a number; Claude session checkpoints; handover and credit; checklists; SchwingNet as the worked example; what is not yet true); committed locally 2026-09-27 as 3f1cf04 | `code/student_projects_3f1cf04/RECIPE.md`; `docs/handoff/INFRASTRUCTURE.md` section 11 | RECORD |
| the board | 12 cards (ctsp1k, schwingnet, transitional-review, u251, litt, meded, annotation, toolkit, polypose, website, demo-study, fluoro-reading); 10 with no co-lead render UNSTAFFED (the memory note's "11 of 12" is wrong); every lead assignment is a draft for Greg | `docs/handoff/INFRASTRUCTURE.md` sections 11 and 13 row 2; `memory/lab-recipe-and-board.md` | RECORD; board.json not copied (names members) |
| the living copy | Claude Doc "The Lab Recipe" (private until Greg shares it); its 14-page export of 2026-09-27 is `docs/STARTHERE_the_lab_recipe_2026-09-27.pdf` | `memory/lab-recipe-and-board.md`; `MANIFEST_CODE.md` | RECORD |
| onboarding | one command (`curl -fsSL https://openspineconsortium.com/onboard.sh \| bash`, or the PowerShell twin) built 2026-09-07: installs git, the GitHub CLI, VS Code with the Claude Code extension and Claude Code, clones `Student_Projects`, runs `/onboard` (resumable: SSH key, grid clone, `make_env.sh` and `get_dataset.sh` as jobs, the demo study, a project from IDEAS.md, `/new-project`); the primer at openspineconsortium.com/onboarding | `memory/student-onboarding-structure.md`; `code/student_projects_3f1cf04/GETTING_STARTED.md` | RECORD |
| the demo study | pelvic width dimorphism on all 802 records: "whether the female pelvis is relatively wider than the male pelvis; the honest answer, for the measurement we chose, is no" | `docs/outreach/student_primer_email.md`; `code/student_projects_3f1cf04/examples/pelvic_width_dimorphism/results/report.txt` | RECORD (v10-era) |
| grid account facts | request through the tech.wayne.edu knowledge base, sponsor Greg, about two business days; Google Authenticator through Open OnDemand's 2FA Setup app on the VPN; an SSH key installed with one password-and-code login lets `ssh -o BatchMode=yes grid` run with no prompt | `memory/student-onboarding-structure.md`; `docs/handoff/EXTRACTS_11.md` | RECORD |

## E. The medical-education study

| item | value | file | mark |
|---|---|---|---|
| published | Schehr A, Kim J, Schwing G. "OpenSpineConsortium: An Open-Source Framework for Medical Student Engagement in Computational Spine Imaging Research." Cureus 2026;18(7):e112661, doi 10.7759/cureus.112661, 2026-07-14, 8 pages, CC-BY | `manuscripts/cureus_2026_e112661_Schehr_Kim_Schwing.pdf`; the Greg-only `MANUSCRIPTS.md` section 12 | RECORD |
| JEEHP version | written 14 to 15 June 2026; the same 16 respondents and the same six-domain table; a submission would publish the same survey data twice | `manuscripts/OSC_MedEd_Manuscript_JEEHP.docx`; `docs/handoff/OPEN_QUESTIONS.md` A21 | RECORD; decision pending (TODO step 4) |
| CNS 2026 | "Beyond the Cadaver Lab ..." selected as a printed poster; the decks say "Ten sub-projects span 16 contributors"; the abstract number 66639 is in the Greg-only `MANUSCRIPTS.md` section 12 (line 60), not in the decks; one-slide poster and visual abstract, last modified 2026-09-01 by Ashley Schehr (core properties read before they were emptied, `MANIFEST_LOCAL.md` section 3) | `manuscripts/talks/Med_Ed_CNS.pptx`, `Med_Ed_CNS_visual_abstract.pptx` (the title and the 16); the Greg-only `MANUSCRIPTS.md` section 12 (the number) | RECORD |
| Preston M. Hickey Medical Student Symposium | 2026-08-07, Wayne State University School of Medicine: two student oral presentations placed, first place (automated CT Cobb angle pipeline, 1,156 cases; Schehr A first author) and third place (lumbar disc heights from CT masks, preliminary validation); five student posters (TRALL angle, lordosis distribution index, Torg ratio and canal diameter, spondylolisthesis, vertebral Hounsfield units); the same work went to CNS 2026 as digital posters | `../99_archive/manuscripts/talks/PRESENTATIONS_RECORD_2026-08-17.md` items 4, 5, 9-13 and 16-23 (redacted extract of a laptop file dated 2026-08-17) | RECORD; student names withheld there and here |
| the survey instrument | the raw survey CSV was never committed (it holds names) and is not here; `docs/survey_protocol.md` is **not** the med-ed survey: it is the CROSS / CHERRIES protocol for a usability survey of the PACS demo among spine surgeons and neuroradiologists (SUS, NASA-TLX item, society recruitment), with no record of it having run | `docs/survey_protocol.md` (read 2026-10-08) | RECORD; whether the PACS survey ran: NOT RECORDED |

## F. The review Spaces and the annotators

| item | value | file | mark |
|---|---|---|---|
| the Spaces | per-task Hugging Face Docker Spaces from `review_service/deploy_v4_spaces.py`, each with its own ledger `anonymous-mlhc/CTSpinoPelvic1K-reviews-<slug>` (spine, ribs, nerve, ili, classfix, triaged); inspect with `python3 -m review_service.admin queue`; the wrong ledger returns 0 cases with no error | `docs/handoff/INFRASTRUCTURE.md` section 11 | RECORD |
| the annotators | the only record is `slots[].reviewer` in the private ledgers; the committed tally `morphometrics/annotation_counts.csv` in the CTSpinoPelvic1K repository has 11 student usernames plus Greg; the memory note's "13 students" is not supported by a listed file; slots do not establish authorship | same; `memory/`: the roster note lives in folder 03 | RECORD; tally not copied |
| the older annotator | `spinesurg-ct-annotator` 1083c4f (2026-04-24, a Hugging Face Space app) | `MANIFEST_CODE.md` | SUPERSEDED by `review_service/` and `reviewtool/` |

## G. The workshop and the tutorials

| item | value | file | mark |
|---|---|---|---|
| AI Imaging Workshop | agenda 2026-05-26 for a 20 June session (WSU School of Medicine; Python / Slurm, DICOM and NIfTI, nnU-Net, ITK-SNAP, training on the grid, writing an AI paper); the PDF exists in two sizes (90,034 B on the Desktop, 90,116 B tracked in the website repository, measured 2026-10-08); the website copy is the record | `MANIFEST_CODE.md`; `MANIFEST_LOCAL.md` | RECORD; not copied |
| tutorials | six Markdown tutorials built by `tutorials/_build.py` in the website repository; their README still points at the `anonymous-mlhc` dataset mirror | `MANIFEST_CODE.md` | RECORD; stale link (TODO step 5) |

## H. Superseded, and by what

| superseded | by | file |
|---|---|---|
| the name Ashley Bridge, the pages under `/ashley/bridge/`, the service name `ashley-service` | Beethoven (2026-09-29, 7.0.0), `/beethoven/`, `beethoven-access` (the old names kept as links and a second Worker name for installed builds) | `memory/ashley-bridge-project.md` |
| licence keys, site keys, the paste box in the browser edition | the approved list in the access service, read for the account name the portal shows (4.0.0, 2026-09-29) | same |
| the 6.0.0 tester package and the unpacked tester folder | release 14.0.0 and the private Chrome listing (listed by path in `99_archive`) | `../_plan/EXCLUDED.md` |
| the scroll gate on the agreement (10.0.0) | one tick with "Show terms" optional (11.0.0, Greg's decision as licensor) | `memory/beethoven-first-run-ux.md` |
| framework 10 (its relay ran python3 on warrior) | framework 11's shell relay (2026-10-02) | `memory/ashley-bridge-project.md` |
| the claude.ai-interception designs of the two prior write-ups | the Remote Control design of the research report (Consumer Terms) | `docs/beethoven/prior_analysis_*.txt`; `docs/beethoven/RESEARCH_REPORT.md` |
| the personal GitHub copies of the two repositories | the organisation copies only (2026-09-30); the personal ones are to be deleted by Greg | `memory/ashley-bridge-project.md` |
| `spinesurg-ct-annotator` (April 2026) | `review_service/` and `reviewtool/` in the CTSpinoPelvic1K repository | `MANIFEST_CODE.md` |
| "11 of 12 cards unstaffed"; `Student_Projects` on the Desktop | 10 of 12; the nested repository inside the CTSpinoPelvic1K checkout | `docs/handoff/INFRASTRUCTURE.md` section 13 |
| v10 identifiers with S1 = 29 in the student template | v11 (29 dissolved into the sacrum) once the public mirror ships v11; the template stays v10 until then by the lead's choice | `memory/hf-mirror-is-v10.md`; `code/student_projects_3f1cf04/templates/CLAUDE.md` |
