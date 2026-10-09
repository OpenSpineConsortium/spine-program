# MANIFEST_CODE.md: every code repository and service this project references

Commits and branches as read on the laptop clones on 2026-10-08 (`git log -1`, `git status -sb`, `git remote -v`).
"Pushed?" is "not recorded" wherever no file or command output of that day says. Files copied into this folder are
listed in `MANIFEST_LOCAL.md`; everything else named here is reached through the repository at the commit given.

## 1. The Beethoven repositories

| repository | URL | branch | commit | visibility | pushed? | push route |
|---|---|---|---|---|---|---|
| Beethoven (browser extension + `hpcworker` framework; the repository and folder keep the code name "ashley-bridge") | `https://github.com/OpenSpineConsortium/beethoven` | `main` | 2f90319 (2026-10-03, "Beethoven 14.0.0 and framework 14: a resumed session's link is accepted beside the environment link; a copyable debug log; the terminal-code stripper no longer eats the letter after a clear-line code"); 32 commits since 2026-09-28; working tree clean | private | not recorded (no remote configured in the clone) | `bash tools/push_org.sh` from WSL (the grid token has no organisation rights; `push_via_grid.sh` retired) |
| Beethoven for VS Code + the access service (the folder keeps the code name "ashley") | `https://github.com/OpenSpineConsortium/beethoven-vscode` | `main` | 8d7fc65 (2026-10-02, "Access service: a service-wide switch for the one-installation rule (settings:seat_rule one\|any), GET and POST /admin/settings, admin.mjs settings and roster"); 56 commits since 2026-09-27; clean | private | not recorded | same |
| the personal copies `GregorySchwing/ashley-bridge`, `GregorySchwing/ashley` | GitHub redirects the first to the organisation copy | — | ab1e1fa / 05efbf6 verified equal to the organisation copies on 2026-09-30 | private | to be deleted by Greg (TODO step 20) | — |

**Files that matter in `OpenSpineConsortium/beethoven` 2f90319** (the ones copied here are marked C):

- `CLAUDE.md` (C) the product's working context and non-negotiable rules; `README.md` (C); `SECURITY.md` (C);
  `PRIVACY.md` (C, version 10); `LICENSE.txt` (C, version 9); `THIRD_PARTY_NOTICES.md` (C); `.gitattributes`,
  `.gitignore`.
- `framework/`: `bin/hpcworker` (the one command; bash 4.2 plus Python 3.6 standard library), `lib/profile.py`,
  `lib/profile.awk`, `lib/profile_sh.sh`, `lib/browser_key.sh`, `lib/adapters/{common,slurm,pbs,lsf}.sh`,
  `profiles/wayne.json` (C, the site profile), the job template and probe job, `tests/run.sh` and six unittest
  files, `README.md` (C as `docs/beethoven/framework_README.md`; "Framework 14"). Anything that copies `framework/`
  by a file list must include `lib/profile.awk` and `lib/profile_sh.sh` (V12_STATUS section 8).
- `extension/`: `wxt.config.ts` (the manifest), `src/core/terms.ts` (`PRODUCT_NAME`, `TERMS_VERSION` 8, `TERMS_DATE`
  2026-10-01), `src/core/keys.ts` (`DEFAULT_PREFS`), `src/core/{audit,net,redact,shell driver}`, `src/licensing/`
  (kill-list verification; `keys.json` holds one base64 verification key, `k1`, and nothing secret), `src/entrypoints/`
  (onboarding, popup, sidepanel), `mock-ood/server.mjs` (the reviewers' mock portal), `scripts/sync-profiles.mjs`,
  `public/` (byte-identical copies of the two agreement texts), `README.md` (C as `docs/beethoven/extension_README.md`),
  `package.json` (wxt 0.21.4, vite 8.3.1, typescript 5.9.3, vitest 5.0.2, ws 8.22.0).
- `helper/build.mjs` and the bundled script bridge (PowerShell on Windows, Perl on macOS and Linux; helper 1.0.0,
  protocol 1, unchanged since 13.0.0).
- `docs/` (C whole, except `site/`): RESEARCH_REPORT (the build specification, governs), ARCHITECTURE, DIAGNOSTICS,
  OPEN_QUESTIONS, WAYNE_STATE_PILOT, V11_CONTRACT, V11_STATUS, V12_CONTRACT, V12_STATUS, TESTERS, STORE_LISTING,
  PUBLISHING_SITE, MAC_AND_SAFARI, LICENSE-FULL-NOTE, TEXTS_V8_V9, TEXTS_V9_V10, the two `prior_analysis_*.txt`
  (rejected designs), `guides/{ACCOUNTS,INSTALL,LAB_LEAD,USE}.md`, `store/{LISTING,PASTE,SUBMISSION,TEST_BEFORE_UPLOAD}.md`;
  `docs/site/beethoven/` are generated site fragments (not copied; the site repository builds the pages).
- `release/4.0.0` to `release/14.0.0`: each with the Chrome zip, `SHA256SUMS.txt`, `README.md`, `guides/`, from 12.0.0
  the `bridge/` installers and store kits, from 10.0.0 a `reviewer/beethoven-mock-portal.zip`. `release/14.0.0/README.md`,
  `SHA256SUMS.txt` and `guides/STUDENT_QUICKSTART.md` (C); the four other guides there are byte-identical to
  `docs/guides/` (same sizes: 15,156, 12,998, 38,356, 22,462 B) and not copied twice; the zip (503,489 B) is a package,
  not copied.
- `tools/`: `deploy_shared.sh` (publishes the framework to the shared copy over ssh; 16,348 B), `grid_access.sh` (the
  ACL reconciler, 29,643 B), `grid_access_task.ps1` (the Windows scheduled task "Beethoven grid access"),
  `push_org.sh`, `push_via_grid.sh` (retired), `tests/`.
- The vendor folder (signing keys, admin token) is outside the repository and is never read.

**Files that matter in `OpenSpineConsortium/beethoven-vscode` 8d7fc65:**

- `CLAUDE.md`, `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE` (all C under `docs/beethoven_vscode/repo_root/`).
- `docs/` (C): `CHECKPOINT_2026-09-28.md` (the handoff; read "CURRENT STATE" first), ARCHITECTURE, DIAGNOSTICS,
  LICENSING, ENGINEERING, INSTALL, LIMITS, MAC, MARKETPLACE, PITCH, ANTHROPIC_REQUEST (the draft to Anthropic),
  RESEARCH.md (213 KB), `diagnostics_graph.json` (the graph the diagnostics rule requires), `legal/ARBITRATION_OPTION.md`,
  `manual/{00_getting_started,90_troubleshooting}.md` and `build/manual.md` (C as `manual/manual_assembled.md`),
  `figures/` (C under `figures/beethoven_vscode/`), `research/reports/` (three reports, C), `research/research_notes/`
  (fifteen notes, C), the probes and their logs (C). Not copied: `DEPENDENCY_MAP.md` (440 KB, generated from
  `research/dependency_map_2026-09-28.json`), `manual.pdf` (931 KB) and `manual.html` (built from the sources),
  `research/deep_research_2026-09-28.json` (1.7 MB), `deep_research_raw_2026-09-28.txt` (2.0 MB),
  `dependency_map_2026-09-28.json` (517 KB), `access_review_2026-09-28.json` (154 KB), `claude_swap_study_2026-09-28.json`
  (59 KB): raw tool outputs, in the repository.
- `grid/`: `bootstrap.sbatch`, `worker.sbatch.tpl`, `beethoven` (83 KB; the grid command, alias `ashley`),
  `beethovend.js`, `phone.js`, `license.js` and `license.d.ts` (the Ed25519 verifier), `license_keys.json` (the `k1`
  and `trial` verification keys only), `login_relay.sh`, `bashrc.block`, `VERSION`.
- `cli/{beethoven,beethoven.ps1,ashley,ashley.ps1}`.
- `tools/intake/` (the access service, a Cloudflare Worker): `worker.js`, `service.mjs`, `admin.mjs` (`approve`,
  `grant`, `roster`, `reset-seat`, `settings`), `deploy.sh`, `publish.sh`, `publish_revoked.mjs`, `register_subdomain.sh`,
  `wrangler.toml` (vars `ALLOWED_DOMAINS` wayne.edu, `TRIAL_DAYS` 365, `KEY_PREFIX` ashley, `REQUIRE_INSTALL_ID`,
  `MAIL_STUDENTS`), `worker.test.mjs`, `ACCESS_CHECK.md`, `README.md`; `tools/license/` (the issuer and the kill-list
  signer; keys outside the repository), `tools/sandbox/` (the Windows Sandbox kit), `release.mjs`, `release_check.mjs`,
  `publish_marketplace.sh`, `grid_tests.sh`, `third_party_notices.mjs`, `wizard_figure.py`, `diag_doc.py`, `depmap_doc.py`.
- `extension/` (the VS Code extension; `src/core/terms.ts`, `src/core/diagnostics.ts`, `vscode/termsPanel.ts`);
  `.github/workflows/triage.yml` (the maintenance pipeline on Greg's own Console key); `.wrangler/` is Cloudflare
  state (ignored).

## 2. Student_Projects and the lab recipe

| repository | URL | branch | commit | visibility | pushed? |
|---|---|---|---|---|---|
| Student_Projects (the nested checkout inside the CTSpinoPelvic1K clone) | `https://github.com/OpenSpineConsortium/Student_Projects` | `main` | local 3f1cf04 (2026-09-27, "The Lab Recipe and the project board ..."); `origin/main` fd60c58 ("Fewer prompts: acceptEdits as the shared default mode ..."); `git status -sb`: `## main...origin/main [ahead 1]`; one untracked file `STARTHERE.pdf` | public | **no**: 3f1cf04 is local only (OPEN_QUESTIONS A25) |
| Projects (the private project folders, cloned inside Student_Projects as `projects/`, gitignored there) | `https://github.com/OpenSpineConsortium/Projects` | `main` | not recorded (the nested clone was not opened on 2026-10-08) | private | — |

Files that matter at 3f1cf04 (C = copied under `code/student_projects_3f1cf04/`): `RECIPE.md` (C), `README.md` (C),
`GETTING_STARTED.md` (C), `CLAUDE.md` (C), `CONTRIBUTING.md` (C), `IDEAS.md` (C), `LICENSE` (C), `templates/`
(C: `CLAUDE.md`, `environment.yml`, `get_dataset.sh`, `make_env.sh`, `proposal_template.md`, `slurm_job.sh`,
`ssh_config`), `tools/grid.sh` and `tools/render_board.py` (C), `.claude/settings.json` and `.claude/commands/`
(C: `/onboard`, `/grid-status`, `/grid-submit`, `/grid-pull`, `/new-project`), `.github/PULL_REQUEST_TEMPLATE.md` (C),
`examples/pelvic_width_dimorphism/` and `examples/proposal_example/` (C). **Not copied:** `board.json` and `BOARD.md`
(they name members; the cards' facts are in `STATUS.md` section D), `projects/` (private), `STARTHERE.pdf` is copied
to `docs/` as the Lab Recipe export. The living copy of the recipe is the Claude Doc "The Lab Recipe"
(`https://claude.ai/code/artifact/03a25fb6-b679-4386-bb04-31f0a965e587`, private until Greg shares it).

## 3. The dataset repository (the review tooling, guides and outreach it holds)

| repository | URL | branch | commit | visibility |
|---|---|---|---|---|
| CTSpinoPelvic1K | `https://github.com/OpenSpineConsortium/CTSpinoPelvic1K` (also `Gregory-Schwing-MD-PhD/CTSpinoPelvic1K`; push both remotes) | `master` | 7ddfe38 (2026-10-08, "CLAUDE.md: grid etiquette from C&IT ..."); working tree modified | public |

Files that matter here: `review_service/` (FastAPI as Hugging Face Docker Spaces: `app.py`, `service.py`, `store.py`,
`admin.py`, `deploy_v4_spaces.py`, `Dockerfile`, `requirements.txt`, `README.md`), `reviewtool/` (`cli.py` 116 KB,
`README.md`), the student-facing review guides `docs/RIB_REVIEW_GUIDE.md`, `SPINE_REVIEW.md`, `CLASSFIX_REVIEW.md`,
`REVIEW.md`, `STUDENT_ANNOTATION_PROTOCOL.md`, `LABELING_GUIDE.md`, `RIB_ANCHOR_REVIEW_GUIDE.md` and the root
`REVIEWERS*.md`; `morphometrics/annotation_counts.csv` (11 student usernames plus Greg; Greg decides its fate) and
`annotator_names.csv` (not copied anywhere); `docs/survey_protocol.md` (C), `proposals/student_primer_email.md` and
`cm_spine_request_email.md` (C, redacted); the untracked `openresearch/` (C), the two HPC-orchestration PDFs (C), the
med-ed docx and the two decks (C); `CLAUDE.md` "Grid" (the login-node and container etiquette every student copies).
The Hugging Face namespaces the review tooling uses: `anonymous-mlhc/CTSpinoPelvic1K-review-<slug>` (Spaces) and
`anonymous-mlhc/CTSpinoPelvic1K-reviews-<slug>` (ledgers; slugs spine, ribs, nerve, ili, classfix, triaged); the older
single Space `gregoryschwingmdphd/ctspinopelvic1k-review-triaged` with ledger `gregoryschwingmdphd/CTSpinoPelvic1K-reviews-triaged`
and dataset `gregoryschwingmdphd/CTSpinoPelvic1K` branch `v2`; `gregoryschwingmdphd/CTSpinoPelvic1K-reviews` is an
empty decoy (`docs/handoff/INFRASTRUCTURE.md` section 1 and 11).

## 4. The older annotator

| repository | URL | branch | commit | visibility | state |
|---|---|---|---|---|---|
| spinesurg-ct-annotator (a Hugging Face Space app) | `https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-annotator` | `master` (as cloned) | 1083c4f (2026-04-24, "slicer") | private (per the inventory) | superseded by `review_service/`; files `app.py` (32 KB), `audit.py`, `sync_manager.py`, `config.py`, `Dockerfile`, `.env.example`, `requirements.txt`, `README.md`, `assignments.json` (204 B; may name students: never copied) |

## 5. The website (onboarding, tutorials, the Beethoven pages)

| repository | URL | branch | local | origin | visibility |
|---|---|---|---|---|---|
| openspineconsortium.github.io | `https://github.com/OpenSpineConsortium/openspineconsortium.github.io` | `master` | c1800f8 ("Site: the remaining pages re-stamped with the same asset stamp") | `origin/master` a17ea39, ten commits ahead of the clone on 2026-10-08 (`## master...origin/master [behind 10]`; `../_plan/PLAN.md` section 3, "12"): pull before any edit (folder 12 step 1) | public |

Files that matter: `onboard.sh` (3,855 B) and `onboard.ps1` (2,304 B) at the site root (the one-command onboarding;
`curl -fsSL https://openspineconsortium.com/onboard.sh | bash`, `irm https://openspineconsortium.com/onboard.ps1 | iex`);
`onboarding/index.html` (the primer); `tutorials/01_environment_setup.md` to `06_writing_an_ai_paper.md`, their HTML
twins, `tutorials/README.md` (still names the `anonymous-mlhc` mirror), `tutorials/_build.py`; `tools/build_site.py`
(the one navigation definition; renders the Beethoven agreement and privacy from the Beethoven repository's
`LICENSE.txt` and `PRIVACY.md`); `tools/pages/beethoven/{admin,privacy,request,reviewers,support,terms,vscode}` and
`tools/pages/onboarding/`; `AI_Imaging_Workshop.pdf` (90,116 B, tracked; the record copy of the workshop agenda);
`contributions/manifest.json` (the people page; public by design, not copied). The site serves no package and no
weights; the `/beethoven/downloads/` history was purged on 2026-09-30 (site 3f805f4).

## 6. The handoff and the toolkits (referenced, not owned)

| repository | URL | branch | commit | what this project reads there |
|---|---|---|---|---|
| spinesurg-ct-nnunet | `https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet` | `L6_Class` | 097933a; `HANDOFF/` untracked that day except `LITERATURE_STATE.md`, `literature_state/`, `RESEARCH_DIRECTIONS.md` | the eight student-readable handoff files (C under `docs/handoff/`); `HANDOFF/context/` (the redacted memory copies, C under `memory/`); `tools/pipeline_state.py` (the student's first tool; run in a job, never over ssh on the login node); `CLAUDE.md` (its login-node line is stale: OPEN_QUESTIONS F10); `data_platform/README.md`. Private: nothing of SchwingNet is referenced from here |
| OpenSpineToolkit | `https://github.com/OpenSpineConsortium/OpenSpineToolkit` (also `Gregory-Schwing-MD-PhD/OpenSpineToolkit`) | `main` | cb43197 | `python -m pytest` is the student's day-3 self-test (one known failure, `tests/test_cobb.py::test_cobb_falls_back_gracefully_without_femurs`, OPEN_QUESTIONS F18); `ostk.labels.labels_for(volume)`; its `CLAUDE.md` to be checked for login-node instructions (F8) |
| XRSpinoPelvic1K | private `OpenSpineConsortium/XRSpinoPelvic1K` | `main` | 4f22935 | named in the student primer as the radiograph counterpart needing annotators; nothing else here depends on it |

## 7. Services, listings and living documents (not repositories)

| service | address | state on 2026-10-08 | source |
|---|---|---|---|
| the access service (Cloudflare Worker, two names for one deployment) | `https://beethoven-access.openspineconsortium.workers.dev` (7.0.0 and later; VS Code 4.0.0 and later), `https://ashley-service.openspineconsortium.workers.dev` (installed older builds) | deployed; last service commit 8d7fc65; the admin page `https://openspineconsortium.com/beethoven/admin.html` behind the admin token and Cloudflare Access | `docs/beethoven/repo_root/README.md` "Access service"; `docs/beethoven_vscode/ARCHITECTURE.md` |
| the request page | `https://openspineconsortium.com/beethoven/request.html` (posts `v: 2`) | live | `docs/beethoven/WAYNE_STATE_PILOT.md` |
| the Chrome Web Store private listing | trusted testers = the Google Group Greg maintains; Official URL verified 2026-10-01 | which build is uploaded: not recorded | `memory/ashley-bridge-project.md` |
| the VS Code Marketplace | `OpenSpineConsortium.ashley` 3.0.0 published 2026-09-28 20:24 UTC; `openspineconsortium.beethoven` 4.0.0 built, upload not recorded | see `STATUS.md` C | `memory/ashley-extension-project.md` |
| Resend (confirmation and approval e-mails) | sender `access@openspineconsortium.com`; domain verified 2026-10-01; `MAIL_STUDENTS` "1" | the confirm e-mail not yet exercised with a real unapproved student | `memory/ashley-bridge-project.md` |
| the Claude Doc "The Lab Recipe" | `https://claude.ai/code/artifact/03a25fb6-b679-4386-bb04-31f0a965e587` | private until Greg shares it; 14-page export of 2026-09-27 in `docs/` | `memory/lab-recipe-and-board.md` |
| the Hugging Face review Spaces and ledgers | section 3 above | live state not re-checked (no network used) | `docs/handoff/INFRASTRUCTURE.md` |
