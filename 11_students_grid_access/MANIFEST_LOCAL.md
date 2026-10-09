# MANIFEST_LOCAL.md: every file copied into this folder, and every valuable file not copied

Built 2026-10-08 by the copy stage of this folder's build (187 files; 10,887,624 bytes as copied, 10,886,710 bytes after the
second pass of the same day, section 8; log kept with the build).
Sections 1 to 3 are the record of what was copied and from which set at which commit. **Section 4 is history, not a
dependency**: it lists the laptop path each copy was read from on 2026-10-08 so the origin of every file is on
record; nothing in this folder depends on those paths, and the live reference for every copied repository file is
the repository at the commit named in `MANIFEST_CODE.md` and in the copy-record line at the top of each copy.

## 1. What was copied, by group

| group | files | bytes | from |
|---|---|---|---|
| `memory/` | 39 | 122,099 | `HANDOFF/context/` (33 redacted copies with INDEX statuses) and `HANDOFF/GREG_ONLY/context_beethoven/` (6, redacted by hand here) |
| `docs/handoff/` | 8 (+ `EXTRACTS_11.md` written here) | 395,695 | the eight student-readable handoff files, whole |
| `docs/beethoven/` | 37 | 1,336,671 | `OpenSpineConsortium/beethoven` main 2f90319: root texts, `docs/`, `guides/`, `store/`, release 14.0.0 texts |
| `docs/beethoven_vscode/` | 50 | 2,187,091 | `OpenSpineConsortium/beethoven-vscode` main 8d7fc65: root texts, `docs/`, manual sources, legal, research reports and notes, probes |
| `figures/beethoven_vscode/` | 6 | 183,369 | the same repository's `docs/figures/` |
| `code/student_projects_3f1cf04/` | 29 | 355,814 | `OpenSpineConsortium/Student_Projects` local main 3f1cf04 (not on origin) |
| `code/beethoven_framework_profiles/` | 1 | 4,290 | `framework/profiles/wayne.json` at 2f90319 |
| `docs/` (loose) | 4 | 1,099,048 | two HPC-orchestration PDFs (dataset repository root, untracked), the Lab Recipe export (`STARTHERE.pdf`, untracked), `survey_protocol.md` (dataset repository, tracked) |
| `docs/outreach/` | 2 | 8,283 | `proposals/` of the dataset repository, redacted |
| `regulatory/openresearch/` | 7 | 21,294 | the untracked `openresearch/` folder of the dataset repository root |
| `manuscripts/` | 2 | 1,193,024 | the Cureus article (Desktop loose file) and the JEEHP draft (dataset repository root, untracked) |
| `manuscripts/talks/` | 2 | 3,980,032 | the two CNS poster decks (dataset repository root, untracked) |
| **total** | **187** | **10,886,710** | nothing over 25 MB was met; nothing skipped for size |

Every Markdown copy carries a copy-record line (an HTML comment at the top, or a blockquote under the front matter of
a memory note) naming its source set, commit, path and the redactions applied by kind and count, and saying, where it
applies, that laptop paths were replaced by kind and that short prefixes are the source's own wording. Shell and Python
copies carry the same record as a comment line after the shebang, or as the first line where there is no shebang (the
four research probes under `docs/beethoven_vscode/research/` received theirs in the second pass; `wayne.json` cannot
carry one and is covered by section 2 only). PDF, PNG, SVG, JSON, CSV, YAML, LOG and plain-text copies are byte-identical
to their sources (the prompts under `regulatory/openresearch/` are verbatim by intent). The DOCX and the two PPTX are
not: their core properties (creator, last modified by) were emptied and the DOCX's corresponding address struck
(section 3); their text, slides and figures are unchanged, and section 2 gives the edited files' bytes and sha256.

## 2. The copied files

| copied to (this folder) | source set and commit | path in the source | bytes | sha256 (first 16 hex) | redactions by kind (count) |
|---|---|---|---|---|---|
| `code/beethoven_framework_profiles/wayne.json` | OpenSpineConsortium/beethoven main 2f90319 | `framework/profiles/wayne.json` | 4290 | cd718ac844f63cf6 | none |
| `code/student_projects_3f1cf04/.claude/commands/grid-pull.md` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `.claude/commands/grid-pull.md` | 1157 | ef8c1a2753df3d88 | none |
| `code/student_projects_3f1cf04/.claude/commands/grid-status.md` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `.claude/commands/grid-status.md` | 1110 | 2955c34e2ce6a37a | none |
| `code/student_projects_3f1cf04/.claude/commands/grid-submit.md` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `.claude/commands/grid-submit.md` | 1452 | 15d794fa2f3b02b8 | none |
| `code/student_projects_3f1cf04/.claude/commands/new-project.md` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `.claude/commands/new-project.md` | 2384 | e6b32e23090399c0 | lead address (1) |
| `code/student_projects_3f1cf04/.claude/commands/onboard.md` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `.claude/commands/onboard.md` | 9027 | 806a1f196159f1ca | lead address (1) |
| `code/student_projects_3f1cf04/.claude/settings.json` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `.claude/settings.json` | 2324 | fa3ee7973d198735 | none |
| `code/student_projects_3f1cf04/.github/PULL_REQUEST_TEMPLATE.md` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `.github/PULL_REQUEST_TEMPLATE.md` | 893 | 37701bb6da7bef98 | none |
| `code/student_projects_3f1cf04/CLAUDE.md` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `CLAUDE.md` | 4111 | b78686d310b637c2 | none |
| `code/student_projects_3f1cf04/CONTRIBUTING.md` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `CONTRIBUTING.md` | 3859 | 36309211f868be70 | none |
| `code/student_projects_3f1cf04/GETTING_STARTED.md` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `GETTING_STARTED.md` | 4765 | f1678c4480229a80 | lead address (1) |
| `code/student_projects_3f1cf04/IDEAS.md` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `IDEAS.md` | 9650 | 9281d2cc8a30b5f3 | none |
| `code/student_projects_3f1cf04/LICENSE` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `LICENSE` | 1209 | ceafea4da303631a | none |
| `code/student_projects_3f1cf04/README.md` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `README.md` | 5506 | 7982112ecb305d51 | lead address (1) |
| `code/student_projects_3f1cf04/RECIPE.md` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `RECIPE.md` | 39786 | 8afb969345d46375 | banned word (1) |
| `code/student_projects_3f1cf04/examples/pelvic_width_dimorphism/README.md` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `examples/pelvic_width_dimorphism/README.md` | 5561 | e45786a73d8fa783 | none |
| `code/student_projects_3f1cf04/examples/pelvic_width_dimorphism/measure_pelvic_width.py` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `examples/pelvic_width_dimorphism/measure_pelvic_width.py` | 13494 | ca4e259732e1e9ef | none |
| `code/student_projects_3f1cf04/examples/pelvic_width_dimorphism/results/pelvic_width.csv` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `examples/pelvic_width_dimorphism/results/pelvic_width.csv` | 47778 | 46a969d0e3e901ba | none |
| `code/student_projects_3f1cf04/examples/pelvic_width_dimorphism/results/pelvic_width.png` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `examples/pelvic_width_dimorphism/results/pelvic_width.png` | 165529 | d29aea23ceec2701 | none |
| `code/student_projects_3f1cf04/examples/pelvic_width_dimorphism/results/report.txt` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `examples/pelvic_width_dimorphism/results/report.txt` | 907 | 0b70590be7bd7bd0 | none |
| `code/student_projects_3f1cf04/examples/proposal_example/proposal.md` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `examples/proposal_example/proposal.md` | 5655 | 6869c02fb7f3a7b0 | lead address (1) |
| `code/student_projects_3f1cf04/templates/CLAUDE.md` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `templates/CLAUDE.md` | 9893 | 98c1b4cf10265ca8 | none |
| `code/student_projects_3f1cf04/templates/environment.yml` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `templates/environment.yml` | 227 | 272f43cafa071abc | none |
| `code/student_projects_3f1cf04/templates/get_dataset.sh` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `templates/get_dataset.sh` | 2171 | c9bd180dfcdeba72 | none |
| `code/student_projects_3f1cf04/templates/make_env.sh` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `templates/make_env.sh` | 2089 | 50d146c370420de6 | none |
| `code/student_projects_3f1cf04/templates/proposal_template.md` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `templates/proposal_template.md` | 2722 | 31b33058b7552afa | none |
| `code/student_projects_3f1cf04/templates/slurm_job.sh` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `templates/slurm_job.sh` | 2964 | e30f0428b45a94ca | none |
| `code/student_projects_3f1cf04/templates/ssh_config` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `templates/ssh_config` | 567 | 82b329f7d4852e70 | none |
| `code/student_projects_3f1cf04/tools/grid.sh` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `tools/grid.sh` | 2679 | c9c2345974cd5ac4 | none |
| `code/student_projects_3f1cf04/tools/render_board.py` | OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08) | `tools/render_board.py` | 6345 | c088c6e504760b59 | none |
| `docs/Browser_Extension_HPC_Orchestration_Protocols.pdf` | CTSpinoPelvic1K-1 root (untracked) | `Browser Extension HPC Orchestration Protocols.pdf` | 349792 | 6568f78c7145223a | none |
| `docs/STARTHERE_the_lab_recipe_2026-09-27.pdf` | Student_Projects working tree (untracked file) | `STARTHERE.pdf` | 490565 | a1087e4741126454 | none |
| `docs/University-Agnostic_HPC_AI_Architecture.pdf` | CTSpinoPelvic1K-1 root (untracked) | `University-Agnostic HPC AI Architecture.pdf` | 247649 | 2c5f5270af1c7d5b | none |
| `docs/beethoven/ARCHITECTURE.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/ARCHITECTURE.md` | 95077 | 1907daa84bba0e87 | environment id (1) |
| `docs/beethoven/DIAGNOSTICS.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/DIAGNOSTICS.md` | 42348 | 2f9c31d1277972c5 | none |
| `docs/beethoven/LICENSE-FULL-NOTE.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/LICENSE-FULL-NOTE.md` | 2302 | 4ce5781203256083 | none |
| `docs/beethoven/MAC_AND_SAFARI.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/MAC_AND_SAFARI.md` | 4977 | f9d7fc2a829725f1 | laptop path (1) (second pass) |
| `docs/beethoven/OPEN_QUESTIONS.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/OPEN_QUESTIONS.md` | 31160 | 4aa0f0c062827a25 | student AccessID (1); staff AccessID (1); environment id (1) |
| `docs/beethoven/PUBLISHING_SITE.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/PUBLISHING_SITE.md` | 18157 | 8a44236db4bdba90 | laptop path (5) (second pass) |
| `docs/beethoven/RESEARCH_REPORT.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/RESEARCH_REPORT.md` | 97151 | a1be419a46a02336 | none |
| `docs/beethoven/STORE_LISTING.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/STORE_LISTING.md` | 23418 | 21c923866b48abe4 | none |
| `docs/beethoven/TESTERS.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/TESTERS.md` | 11771 | 10d6c7a49d4ab5f5 | none |
| `docs/beethoven/TEXTS_V8_V9.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/TEXTS_V8_V9.md` | 78839 | 4a47184a6fde9ed5 | none |
| `docs/beethoven/TEXTS_V9_V10.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/TEXTS_V9_V10.md` | 74384 | fc4b093be8e5a315 | none |
| `docs/beethoven/V11_CONTRACT.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/V11_CONTRACT.md` | 85331 | d03c9ef2241adbec | none |
| `docs/beethoven/V11_STATUS.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/V11_STATUS.md` | 29237 | 4b350884ada55aaf | none |
| `docs/beethoven/V12_CONTRACT.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/V12_CONTRACT.md` | 12610 | 534566b998fe5f7e | none |
| `docs/beethoven/V12_STATUS.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/V12_STATUS.md` | 76370 | b9b8cd4616a55587 | student AccessID (1) |
| `docs/beethoven/WAYNE_STATE_PILOT.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/WAYNE_STATE_PILOT.md` | 25262 | 839b293b1c4c0e0c | staff AccessID (1) |
| `docs/beethoven/extension_README.md` | OpenSpineConsortium/beethoven main 2f90319 | `extension/README.md` | 36138 | 8377353eaf4b707b | laptop path (1) (second pass) |
| `docs/beethoven/framework_README.md` | OpenSpineConsortium/beethoven main 2f90319 | `framework/README.md` | 118701 | 5d304a64b9b38625 | none |
| `docs/beethoven/guides/ACCOUNTS.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/guides/ACCOUNTS.md` | 15545 | 10024229259bfe93 | none |
| `docs/beethoven/guides/INSTALL.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/guides/INSTALL.md` | 13386 | cb0c4cbbfce7ed23 | none |
| `docs/beethoven/guides/LAB_LEAD.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/guides/LAB_LEAD.md` | 39008 | a2573a5e926a8557 | student AccessID (3); staff AccessID (2); laptop path (2) (second pass) |
| `docs/beethoven/guides/USE.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/guides/USE.md` | 22846 | 0f947ca43b4e0747 | none |
| `docs/beethoven/prior_analysis_architecture.txt` | OpenSpineConsortium/beethoven main 2f90319 | `docs/prior_analysis_architecture.txt` | 33444 | 76b97053087b9c28 | none |
| `docs/beethoven/prior_analysis_protocols.txt` | OpenSpineConsortium/beethoven main 2f90319 | `docs/prior_analysis_protocols.txt` | 48616 | 8c70a6fa23375e17 | none |
| `docs/beethoven/release_14.0.0/README.md` | OpenSpineConsortium/beethoven main 2f90319 | `release/14.0.0/README.md` | 19389 | 63d8a6bcc92c59e8 | none |
| `docs/beethoven/release_14.0.0/SHA256SUMS.txt` | OpenSpineConsortium/beethoven main 2f90319 | `release/14.0.0/SHA256SUMS.txt` | 986 | 5ad2ed39ba00c296 | none |
| `docs/beethoven/release_14.0.0/STUDENT_QUICKSTART.md` | OpenSpineConsortium/beethoven main 2f90319 | `release/14.0.0/guides/STUDENT_QUICKSTART.md` | 4667 | 423dc15e71759b29 | none |
| `docs/beethoven/repo_root/CLAUDE.md` | OpenSpineConsortium/beethoven main 2f90319 | `CLAUDE.md` | 23044 | 0d30d4068ca5ea90 | laptop path (4) (second pass) |
| `docs/beethoven/repo_root/LICENSE.txt` | OpenSpineConsortium/beethoven main 2f90319 | `LICENSE.txt` | 49318 | 22dd4f909a45f1b6 | none |
| `docs/beethoven/repo_root/PRIVACY.md` | OpenSpineConsortium/beethoven main 2f90319 | `PRIVACY.md` | 57178 | 31cac06bea7d083f | none |
| `docs/beethoven/repo_root/README.md` | OpenSpineConsortium/beethoven main 2f90319 | `README.md` | 26603 | 346a1ca16a4aea11 | laptop path (1) (second pass) |
| `docs/beethoven/repo_root/SECURITY.md` | OpenSpineConsortium/beethoven main 2f90319 | `SECURITY.md` | 15710 | 1652ce68db9f30d8 | none |
| `docs/beethoven/repo_root/THIRD_PARTY_NOTICES.md` | OpenSpineConsortium/beethoven main 2f90319 | `THIRD_PARTY_NOTICES.md` | 5630 | f4368fcd1e1a003c | none |
| `docs/beethoven/store/LISTING.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/store/LISTING.md` | 38348 | 0bd419ccfe7c9c61 | none |
| `docs/beethoven/store/PASTE.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/store/PASTE.md` | 23646 | a07376d70c20a780 | laptop path (1) (second pass) |
| `docs/beethoven/store/SUBMISSION.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/store/SUBMISSION.md` | 21651 | 9ce2c2ed573a986e | none |
| `docs/beethoven/store/TEST_BEFORE_UPLOAD.md` | OpenSpineConsortium/beethoven main 2f90319 | `docs/store/TEST_BEFORE_UPLOAD.md` | 14423 | bb136283bc7ac647 | none |
| `docs/beethoven_vscode/ANTHROPIC_REQUEST.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/ANTHROPIC_REQUEST.md` | 3831 | 36591f35137c2a2c | none |
| `docs/beethoven_vscode/ARCHITECTURE.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/ARCHITECTURE.md` | 31717 | 0cfe9b581a8756a4 | none |
| `docs/beethoven_vscode/CHECKPOINT_2026-09-28.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/CHECKPOINT_2026-09-28.md` | 93704 | 9637328a03e05699 | personal e-mail (1); maintainer address (2); student AccessID (2); staff AccessID (2); key id (4); key id (2); key id (1); environment id (3); vendor path (1); token path (1); token path (1); laptop path (25) (second pass) |
| `docs/beethoven_vscode/DIAGNOSTICS.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/DIAGNOSTICS.md` | 24517 | 8eb3b2fe674be526 | none |
| `docs/beethoven_vscode/ENGINEERING.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/ENGINEERING.md` | 5680 | ed2bebab5a1da401 | none |
| `docs/beethoven_vscode/INSTALL.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/INSTALL.md` | 9144 | 90f3f0638b225874 | none |
| `docs/beethoven_vscode/LICENSING.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/LICENSING.md` | 13099 | 2320798c4c03ea47 | token path (1); laptop path (2) (second pass) |
| `docs/beethoven_vscode/LIMITS.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/LIMITS.md` | 6442 | 7f476d49c1d58ca1 | none |
| `docs/beethoven_vscode/MAC.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/MAC.md` | 7843 | 72177140afdb53c5 | laptop path (6) (second pass) |
| `docs/beethoven_vscode/MARKETPLACE.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/MARKETPLACE.md` | 8894 | 7768aeed9124274c | token path (1); laptop path (5) (second pass) |
| `docs/beethoven_vscode/PITCH.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/PITCH.md` | 5173 | e0f465887a07daae | none |
| `docs/beethoven_vscode/RESEARCH.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/RESEARCH.md` | 213653 | 792713ffc03f3acb | none |
| `docs/beethoven_vscode/diagnostics_graph.json` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/diagnostics_graph.json` | 25847 | 886f8e9d9da812df | none |
| `docs/beethoven_vscode/legal/ARBITRATION_OPTION.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/legal/ARBITRATION_OPTION.md` | 6344 | 723983e162e09412 | none |
| `docs/beethoven_vscode/manual/00_getting_started.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/manual/00_getting_started.md` | 10083 | c1fddba086b7d5c5 | none |
| `docs/beethoven_vscode/manual/90_troubleshooting.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/manual/90_troubleshooting.md` | 9184 | 03497180c4ad24a0 | none |
| `docs/beethoven_vscode/manual/manual_assembled.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/build/manual.md` | 72993 | a66f8da90e631071 | none |
| `docs/beethoven_vscode/repo_root/CLAUDE.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `CLAUDE.md` | 5859 | 28075b45cac796de | laptop path (4) (second pass) |
| `docs/beethoven_vscode/repo_root/CONTRIBUTING.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `CONTRIBUTING.md` | 3823 | e528b848d64841d7 | none |
| `docs/beethoven_vscode/repo_root/LICENSE` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `LICENSE` | 524 | 148ff65fa4964748 | none |
| `docs/beethoven_vscode/repo_root/README.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `README.md` | 5729 | 69bb1220f2a02c24 | none |
| `docs/beethoven_vscode/repo_root/SECURITY.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `SECURITY.md` | 2369 | 21e8aeb5e393371f | none |
| `docs/beethoven_vscode/research/claude_swap_notes.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/claude_swap_notes.md` | 31678 | 9e1a86ab8b3c36a6 | none |
| `docs/beethoven_vscode/research/latency_baseline.csv` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/latency_baseline.csv` | 483 | 8c886eb46c5024cd | none |
| `docs/beethoven_vscode/research/latency_node.csv` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/latency_node.csv` | 35 | 7f15200200db4962 | none |
| `docs/beethoven_vscode/research/latency_probe.sh` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/latency_probe.sh` | 2565 | 3b10b5405c60b611 | none (copy-record line added in the second pass) |
| `docs/beethoven_vscode/research/latency_relay.csv` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/latency_relay.csv` | 450 | 6d35155a12fec297 | none |
| `docs/beethoven_vscode/research/library_peer_test.log` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/library_peer_test.log` | 13386 | 2daba144accad452 | none |
| `docs/beethoven_vscode/research/library_peer_test.sh` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/library_peer_test.sh` | 2739 | 1d382e98da687d79 | none (copy-record line added in the second pass) |
| `docs/beethoven_vscode/research/plot_latency.py` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/plot_latency.py` | 3448 | f03515ea4660d1ad | none (copy-record line added in the second pass) |
| `docs/beethoven_vscode/research/rc_probe.log` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/rc_probe.log` | 2581 | f965f935938b1eee | none |
| `docs/beethoven_vscode/research/rc_probe.sh` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/rc_probe.sh` | 1648 | 6320965e3fe9ee62 | none (copy-record line added in the second pass) |
| `docs/beethoven_vscode/research/reports/Ashley liability shield and Marketplace.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/reports/Ashley liability shield and Marketplace.md` | 116861 | b77c8ec1df3dbfb9 | none |
| `docs/beethoven_vscode/research/reports/Ashley terms of service constraints.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/reports/Ashley terms of service constraints.md` | 90777 | 7932fc8c241140d9 | none |
| `docs/beethoven_vscode/research/reports/Browser extension HPC Claude worker.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/reports/Browser extension HPC Claude worker.md` | 97195 | 3ae8729382838584 | none |
| `docs/beethoven_vscode/research/research_notes/Ashley liability shield and Marketplace/contract_dispute_shields.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/research_notes/Ashley liability shield and Marketplace/contract_dispute_shields.md` | 105445 | 93a7e5192086f38b | none |
| `docs/beethoven_vscode/research/research_notes/Ashley liability shield and Marketplace/entity_insurance_filings.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/research_notes/Ashley liability shield and Marketplace/entity_insurance_filings.md` | 92258 | d3b6c16becbf65a3 | none |
| `docs/beethoven_vscode/research/research_notes/Ashley liability shield and Marketplace/marketplace_removal_prevention.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/research_notes/Ashley liability shield and Marketplace/marketplace_removal_prevention.md` | 87309 | 311ccf82bb99b7c8 | none |
| `docs/beethoven_vscode/research/research_notes/Ashley liability shield and Marketplace/regulatory_multistate_exposure.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/research_notes/Ashley liability shield and Marketplace/regulatory_multistate_exposure.md` | 198797 | 21fa062eb11f0c4a | laptop path (2) (second pass) |
| `docs/beethoven_vscode/research/research_notes/Ashley terms of service constraints/anthropic_terms.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/research_notes/Ashley terms of service constraints/anthropic_terms.md` | 65356 | 2e7519278349f395 | none |
| `docs/beethoven_vscode/research/research_notes/Ashley terms of service constraints/eula_law_and_marketplace.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/research_notes/Ashley terms of service constraints/eula_law_and_marketplace.md` | 92887 | c9f4bb5afae96b35 | none |
| `docs/beethoven_vscode/research/research_notes/Ashley terms of service constraints/github_huggingface_terms.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/research_notes/Ashley terms of service constraints/github_huggingface_terms.md` | 64469 | 5c7c078e84fd8b81 | none |
| `docs/beethoven_vscode/research/research_notes/Ashley terms of service constraints/telemetry_and_ai_maintenance_practice.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/research_notes/Ashley terms of service constraints/telemetry_and_ai_maintenance_practice.md` | 88354 | fd2d257e0b88500e | banned word (5) |
| `docs/beethoven_vscode/research/research_notes/Ashley terms of service constraints/wsu_grid_and_it_policy.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/research_notes/Ashley terms of service constraints/wsu_grid_and_it_policy.md` | 56248 | d84114b7ae406ec3 | staff e-mail (1) (second pass) |
| `docs/beethoven_vscode/research/research_notes/Browser extension HPC Claude worker/anthropic_surfaces_and_terms.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/research_notes/Browser extension HPC Claude worker/anthropic_surfaces_and_terms.md` | 58796 | 7644ced9453cb7ee | none |
| `docs/beethoven_vscode/research/research_notes/Browser extension HPC Claude worker/browser_extension_platform.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/research_notes/Browser extension HPC Claude worker/browser_extension_platform.md` | 65631 | 97f6b2f5e4d71b13 | none |
| `docs/beethoven_vscode/research/research_notes/Browser extension HPC Claude worker/hpc_portability_layer.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/research_notes/Browser extension HPC Claude worker/hpc_portability_layer.md` | 74787 | e53ac69ec796ca0f | none |
| `docs/beethoven_vscode/research/research_notes/Browser extension HPC Claude worker/open_ondemand_gateway.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/research_notes/Browser extension HPC Claude worker/open_ondemand_gateway.md` | 82940 | 3d4ebc2a3bff3b13 | none |
| `docs/beethoven_vscode/research/research_notes/Browser extension HPC Claude worker/prior_art_and_comparables.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/research_notes/Browser extension HPC Claude worker/prior_art_and_comparables.md` | 55878 | 3796918021c8b941 | laptop path (6) (second pass) |
| `docs/beethoven_vscode/research/research_notes/Browser extension HPC Claude worker/security_policy_licensing.md` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/research/research_notes/Browser extension HPC Claude worker/security_policy_licensing.md` | 67638 | dfadd28e7b1d4cd1 | banned word (3); laptop path (1) (second pass) |
| `docs/handoff/DATASET_USAGE.md` | spinesurg-ct-nnunet HANDOFF (untracked on 2026-10-08 except LITERATURE_STATE and RESEARCH_DIRECTIONS) | `HANDOFF/DATASET_USAGE.md` | 37716 | 61bea8937a5a3d43 | none |
| `docs/handoff/GLOSSARY.md` | spinesurg-ct-nnunet HANDOFF (untracked on 2026-10-08 except LITERATURE_STATE and RESEARCH_DIRECTIONS) | `HANDOFF/GLOSSARY.md` | 25825 | 7f35e50d8071506e | none |
| `docs/handoff/INFRASTRUCTURE.md` | spinesurg-ct-nnunet HANDOFF (untracked on 2026-10-08 except LITERATURE_STATE and RESEARCH_DIRECTIONS) | `HANDOFF/INFRASTRUCTURE.md` | 49190 | 41a2781ae9b250aa | staff AccessID (1); laptop path (3) (second pass) |
| `docs/handoff/LEAKAGE.md` | spinesurg-ct-nnunet HANDOFF (untracked on 2026-10-08 except LITERATURE_STATE and RESEARCH_DIRECTIONS) | `HANDOFF/LEAKAGE.md` | 25755 | c5398113b7e57a75 | none |
| `docs/handoff/OPEN_QUESTIONS.md` | spinesurg-ct-nnunet HANDOFF (untracked on 2026-10-08 except LITERATURE_STATE and RESEARCH_DIRECTIONS) | `HANDOFF/OPEN_QUESTIONS.md` | 28995 | d28e87ea8cf62d9f | none |
| `docs/handoff/README.md` | spinesurg-ct-nnunet HANDOFF (untracked on 2026-10-08 except LITERATURE_STATE and RESEARCH_DIRECTIONS) | `HANDOFF/README.md` | 43061 | db23169f43dabca3 | laptop path (9) (second pass) |
| `docs/handoff/RECIPES.md` | spinesurg-ct-nnunet HANDOFF (untracked on 2026-10-08 except LITERATURE_STATE and RESEARCH_DIRECTIONS) | `HANDOFF/RECIPES.md` | 74166 | 2446ac5e2e1e62bc | laptop path (2) (second pass) |
| `docs/handoff/RESULTS_CATALOG.md` | spinesurg-ct-nnunet HANDOFF (untracked on 2026-10-08 except LITERATURE_STATE and RESEARCH_DIRECTIONS) | `HANDOFF/RESULTS_CATALOG.md` | 110987 | 49bbbc2ac4e304ed | laptop path (5) (second pass) |
| `docs/outreach/cm_spine_request_email.md` | OpenSpineConsortium/CTSpinoPelvic1K master 7ddfe38 | `proposals/cm_spine_request_email.md` | 4339 | a3fabc136bc02009 | lead address (1); researcher e-mail (1); affiliation (1); affiliation (1) |
| `docs/outreach/student_primer_email.md` | OpenSpineConsortium/CTSpinoPelvic1K master 7ddfe38 | `proposals/student_primer_email.md` | 3944 | 0b9cf9b76b32a495 | lead address (1); student names (1) |
| `docs/survey_protocol.md` | OpenSpineConsortium/CTSpinoPelvic1K master 7ddfe38 | `docs/survey_protocol.md` | 11042 | 11b7251827e5ace3 | clinician names (1) |
| `figures/beethoven_vscode/accounts.svg` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/figures/accounts.svg` | 2756 | 06e392264cfe8bce | none |
| `figures/beethoven_vscode/latency.png` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/figures/latency.png` | 108130 | 76ce25dd777177e7 | none |
| `figures/beethoven_vscode/latency.svg` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/figures/latency.svg` | 61353 | 34f067bfe7653ac6 | none |
| `figures/beethoven_vscode/lifecycle.svg` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/figures/lifecycle.svg` | 2743 | 882e9c890034d3cc | none |
| `figures/beethoven_vscode/topology.svg` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/figures/topology.svg` | 4100 | f147512b47f2f953 | none |
| `figures/beethoven_vscode/wizard.svg` | OpenSpineConsortium/beethoven-vscode main 8d7fc65 | `docs/figures/wizard.svg` | 4287 | ad296b3dc6a2aa3b | none |
| `manuscripts/OSC_MedEd_Manuscript_JEEHP.docx` | CTSpinoPelvic1K-1 root (untracked) | `OSC MedEd Manuscript - JEEHP.docx` | 44672 | 1a0f38801ea633c1 | corresponding author's university address (1, body); core properties creator and lastModifiedBy emptied (2) (second pass) |
| `manuscripts/cureus_2026_e112661_Schehr_Kim_Schwing.pdf` | Desktop root loose file | `cureus.pdf` | 1148352 | 5645bdcad824ae74 | none; DELIBERATE KEEP: the published author list and the corresponding author's university address are the public record of the article (CC-BY, 2026-07-14) |
| `manuscripts/talks/Med_Ed_CNS.pptx` | CTSpinoPelvic1K-1 root (untracked) | `Med_Ed_CNS.pptx` | 1411043 | b5736abbc786b6b2 | core properties creator and lastModifiedBy emptied (2) (second pass); DELIBERATE KEEP for Greg (PLAN section 5): the accepted poster's author list on the slide ("Ten sub-projects span 16 contributors", named there) |
| `manuscripts/talks/Med_Ed_CNS_visual_abstract.pptx` | CTSpinoPelvic1K-1 root (untracked) | `Med_Ed_CNS_visual_abstract.pptx` | 2568989 | 69ddea56961540e3 | core properties creator and lastModifiedBy emptied (2) (second pass); DELIBERATE KEEP for Greg (PLAN section 5): the accepted poster's author list on the slide ("Ten sub-projects span 16 contributors", named there) |
| `memory/ashley-bridge-project.md` | HANDOFF/GREG_ONLY/context_beethoven (Greg-only origin) | `GREG_ONLY/context_beethoven/ashley-bridge-project.md` | 23435 | 205dfee0352bf7ba | tester e-mail (1); student AccessID (2); staff AccessID (1); key id (2); key id (2); environment id (1); vendor path (1); token path (1); token path (1); laptop path (2) (second pass); version shorthand written in full (2) (second pass) |
| `memory/ashley-compliance-boundary.md` | HANDOFF/GREG_ONLY/context_beethoven (Greg-only origin) | `GREG_ONLY/context_beethoven/ashley-compliance-boundary.md` | 5687 | 1a6eaae2995b71d0 | none |
| `memory/ashley-extension-project.md` | HANDOFF/GREG_ONLY/context_beethoven (Greg-only origin) | `GREG_ONLY/context_beethoven/ashley-extension-project.md` | 5944 | e54c5e5f2284cc5f | personal e-mail (2); maintainer address (1); key id (1); environment id (1); token path (1); laptop path (3) (second pass) |
| `memory/bash-heredoc-backslashes.md` | HANDOFF/context (redacted copy set) | `context/bash-heredoc-backslashes.md` | 1291 | 7a72e7b39bbd7329 | none |
| `memory/beethoven-2026-10-02-field-failures.md` | HANDOFF/GREG_ONLY/context_beethoven (Greg-only origin) | `GREG_ONLY/context_beethoven/beethoven-2026-10-02-field-failures.md` | 4355 | fed5dcfc0606d077 | student AccessID (3) |
| `memory/beethoven-browser-ssh.md` | HANDOFF/GREG_ONLY/context_beethoven (Greg-only origin) | `GREG_ONLY/context_beethoven/beethoven-browser-ssh.md` | 6835 | 02e997a159bc7854 | version shorthand written in full (4) (second pass) |
| `memory/beethoven-first-run-ux.md` | HANDOFF/GREG_ONLY/context_beethoven (Greg-only origin) | `GREG_ONLY/context_beethoven/beethoven-first-run-ux.md` | 8062 | 6d8a9098bb1951f7 | version shorthand written in full (2) (second pass) |
| `memory/ct-volumes-are-pir-not-ras.md` | HANDOFF/context (redacted copy set) | `context/ct-volumes-are-pir-not-ras.md` | 2285 | 002f177483180cb4 | none |
| `memory/data-directives-2026-09-23.md` | HANDOFF/context (redacted copy set) | `context/data-directives-2026-09-23.md` | 2417 | 9a8fde792e4deb4e | none |
| `memory/diagnostics-graph-required.md` | HANDOFF/context (redacted copy set) | `context/diagnostics-graph-required.md` | 1671 | 3a886837379c893e | none |
| `memory/figure-captions-terse.md` | HANDOFF/context (redacted copy set) | `context/figure-captions-terse.md` | 1556 | 10812f857d28008b | none |
| `memory/fluorocap-repo-private.md` | HANDOFF/context (redacted copy set) | `context/fluorocap-repo-private.md` | 1702 | 8cf2943deff82c59 | none |
| `memory/grid-access-list-gate.md` | HANDOFF/context (redacted copy set) | `context/grid-access-list-gate.md` | 2448 | 6bb37d94100192e7 | student AccessID (1); staff AccessID (1) |
| `memory/grid-access.md` | HANDOFF/context (redacted copy set) | `context/grid-access.md` | 1811 | 908f6d8294233a1e | none |
| `memory/grid-apptainer-module-works.md` | HANDOFF/context (redacted copy set) | `context/grid-apptainer-module-works.md` | 1873 | 519b01478b00b78e | none |
| `memory/grid-ashley-deletion-2026-09-28.md` | HANDOFF/context (redacted copy set) | `context/grid-ashley-deletion-2026-09-28.md` | 1951 | a4daccfeab88d99c | none |
| `memory/grid-bash-4-2-quoting.md` | HANDOFF/context (redacted copy set) | `context/grid-bash-4-2-quoting.md` | 1795 | e8777c583dc2fbfe | none |
| `memory/grid-ceph-volume-oschome.md` | HANDOFF/context (redacted copy set) | `context/grid-ceph-volume-oschome.md` | 1594 | 5d1c0011a0e924c6 | staff AccessID (1) |
| `memory/grid-local-singularity-is-broken.md` | HANDOFF/context (redacted copy set) | `context/grid-local-singularity-is-broken.md` | 2658 | cfdfdb660a9dedf3 | none |
| `memory/grid-slurm-inside-apptainer.md` | HANDOFF/context (redacted copy set) | `context/grid-slurm-inside-apptainer.md` | 1764 | c0f12bd2d78c101f | none |
| `memory/grid-ssh-second-factor.md` | HANDOFF/context (redacted copy set) | `context/grid-ssh-second-factor.md` | 2297 | ac80bc5a184af529 | none |
| `memory/hf-mirror-is-v10.md` | HANDOFF/context (redacted copy set) | `context/hf-mirror-is-v10.md` | 2176 | 70fa7effeb0e7fda | none |
| `memory/key-patients-from-metadata-not-filenames.md` | HANDOFF/context (redacted copy set) | `context/key-patients-from-metadata-not-filenames.md` | 2457 | d2ec475edf8addcf | none |
| `memory/lab-recipe-and-board.md` | HANDOFF/context (redacted copy set) | `context/lab-recipe-and-board.md` | 3358 | 8fd5d67137ba59dd | laptop path (1) (second pass) |
| `memory/label-scheme-v4-vs-ostk.md` | HANDOFF/context (redacted copy set) | `context/label-scheme-v4-vs-ostk.md` | 2704 | 4e91e07ce9f40481 | none |
| `memory/morphology-deformation-feasibility.md` | HANDOFF/context (redacted copy set) | `context/morphology-deformation-feasibility.md` | 2559 | a07a57c7e6875f2d | none |
| `memory/never-reorient-when-writing-labels.md` | HANDOFF/context (redacted copy set) | `context/never-reorient-when-writing-labels.md` | 2184 | 4d0029810a17a82c | none |
| `memory/no-jobs-on-login-node.md` | HANDOFF/context (redacted copy set) | `context/no-jobs-on-login-node.md` | 2427 | 13224f6bf6871fac | none |
| `memory/no-unexplained-subsets-fix-not-disclose.md` | HANDOFF/context (redacted copy set) | `context/no-unexplained-subsets-fix-not-disclose.md` | 2394 | 4c58469738e2ebfb | none |
| `memory/scratchpad-shadows-stdlib.md` | HANDOFF/context (redacted copy set) | `context/scratchpad-shadows-stdlib.md` | 1647 | 745c632308935c2c | none |
| `memory/student-onboarding-structure.md` | HANDOFF/context (redacted copy set) | `context/student-onboarding-structure.md` | 3034 | 6d2702757a6c01da | laptop path (1) (second pass) |
| `memory/students-see-no-internals.md` | HANDOFF/context (redacted copy set) | `context/students-see-no-internals.md` | 1254 | cd6a2cf9f8ba0e20 | none |
| `memory/submit-and-sleep-orchestration.md` | HANDOFF/context (redacted copy set) | `context/submit-and-sleep-orchestration.md` | 2176 | 14032b5e58dff4ba | none |
| `memory/user-affiliation-general-surgery.md` | HANDOFF/context (redacted copy set) | `context/user-affiliation-general-surgery.md` | 1806 | a6a0267f59ba855c | none |
| `memory/windows-junction-worktree-trap.md` | HANDOFF/context (redacted copy set) | `context/windows-junction-worktree-trap.md` | 1946 | e8e591b8b615a445 | laptop path (2) (second pass) |
| `memory/windows-ssh-to-grid.md` | HANDOFF/context (redacted copy set) | `context/windows-ssh-to-grid.md` | 1858 | 6d638f12f529c5e7 | laptop path (1) (second pass) |
| `memory/writing-preferences.md` | HANDOFF/context (redacted copy set) | `context/writing-preferences.md` | 1065 | 72dbff9994d4dcf0 | none |
| `memory/wsl-for-network.md` | HANDOFF/context (redacted copy set) | `context/wsl-for-network.md` | 1877 | a31ab19c41d401ae | laptop path (1) (second pass) |
| `memory/wsu-library-access-cutoff.md` | HANDOFF/context (redacted copy set) | `context/wsu-library-access-cutoff.md` | 1761 | d87098e33fa26f14 | none |
| `regulatory/openresearch/command.txt` | CTSpinoPelvic1K-1 root (untracked folder) | `openresearch/command.txt` | 359 | fa46bc81f7cba6b2 | none |
| `regulatory/openresearch/extension.txt` | CTSpinoPelvic1K-1 root (untracked folder) | `openresearch/extension.txt` | 862 | a0a6b82d2e019a9f | none |
| `regulatory/openresearch/firstprompt.txt` | CTSpinoPelvic1K-1 root (untracked folder) | `openresearch/firstprompt.txt` | 10984 | bc5f9f25d2f80f29 | none |
| `regulatory/openresearch/fourthprompt.txt` | CTSpinoPelvic1K-1 root (untracked folder) | `openresearch/fourthprompt.txt` | 2716 | 0220b9bdb647fbbe | none |
| `regulatory/openresearch/secondprompt.txt` | CTSpinoPelvic1K-1 root (untracked folder) | `openresearch/secondprompt.txt` | 532 | 355b1ec7ffe41471 | none |
| `regulatory/openresearch/thirdprompt.txt` | CTSpinoPelvic1K-1 root (untracked folder) | `openresearch/thirdprompt.txt` | 3551 | 05f09d64b419ca16 | none |
| `regulatory/openresearch/zeroethprompt.txt` | CTSpinoPelvic1K-1 root (untracked folder) | `openresearch/zeroethprompt.txt` | 2290 | 0e46c331eaf6ecf8 | none |

## 3. Redactions, by kind (never by value)

Applied to every text copy by one regular-expression map; counts are over all 187 copies:

| kind | replaced by | count | where it mattered |
|---|---|---|---|
| one student's AccessID (the first tester) | `[student-1 AccessID]` | 13 | the six Beethoven notes, `grid-access-list-gate`, `LAB_LEAD.md`, `V12_STATUS.md`, Beethoven `OPEN_QUESTIONS.md`, the VS Code checkpoint |
| the C&IT staff AccessID that owns the volume link | `[C&IT staff AccessID]` | 10 | the same documents and `INFRASTRUCTURE.md` section 2.2 |
| a tester's personal e-mail | `[tester e-mail withheld]` | 1 | `ashley-bridge-project` |
| Greg's personal e-mail | `[personal e-mail withheld]` | 3 | `ashley-extension-project`, the VS Code checkpoint |
| Greg's university address (used as the Cloudflare account and as the service's notify address) | `[maintainer university address]` | 3 | `ashley-extension-project`, the VS Code checkpoint |
| the lead's university address in public student documents | `[the lead's university address]` | 7 | `Student_Projects` README, GETTING_STARTED, two commands, the two outreach drafts |
| an external researcher's e-mail | `[researcher e-mail withheld]` | 1 | `cm_spine_request_email.md` |
| three licence key ids (tester site key, store-reviewer key, Greg's own) | `[key id withheld]` | 12 | the Beethoven notes, the VS Code checkpoint |
| Remote Control environment ids | `env_[withheld]` | 7 | the Beethoven notes, the VS Code checkpoint |
| vendor token paths and the vendor licence folder | `[vendor token path withheld]`, `[vendor folder, never read]/licenses/` | 9 | the Beethoven notes, `LICENSING.md`, `MARKETPLACE.md`, the VS Code checkpoint |
| ten student annotators named in the primer e-mail | `[ten student annotators, names struck]` | 1 | `student_primer_email.md` (Ashley Schehr and the two radiology residents, who are published co-authors, stay) |
| two clinician advisors named in the survey protocol | `[two clinician advisors]` | 1 | `survey_protocol.md` |
| the affiliation in the CM Spine request (said "neurosurgery resident") | "surgical resident" and "Resident, Department of General Surgery, Wayne State University School of Medicine / Detroit Medical Center" | 2 | `cm_spine_request_email.md` (a draft; whether it was ever sent is not recorded) |
| the banned word | "origin" / "Origin" | 9 | `RECIPE.md` (3f1cf04) and two of the VS Code edition's research notes |
| laptop paths: the author's Windows user folder, the OneDrive Desktop folder and the Claude project slug, in the Windows (`C:/`, `C:\`), Git Bash (`/c/`) and WSL (`/mnt/c/`) spellings (second pass) | `[laptop home]/`, `[laptop Desktop]/`, `[laptop project slug]`; one placeholder for all three spellings, the tail of each path kept | 96 in 26 copies | the two Beethoven repositories' documents (the four full vendor-folder paths among them), the handoff files, seven memory notes; section 5 lists the files; the full paths stand in section 4 of this file and nowhere else |
| a WSU licensing-office staff member's e-mail (second pass) | `[licensing office staff e-mail]` | 1 | `wsu_grid_and_it_policy.md` line 140 |
| the JEEHP draft's corresponding address, a university AccessID address (second pass) | `[corresponding author's university address]` | 1 | `OSC_MedEd_Manuscript_JEEHP.docx`, `word/document.xml` |
| Office core properties `dc:creator` and `cp:lastModifiedBy` (a personal name and Greg's name in the DOCX; a template author's name and Ashley Schehr's name in both PPTX, last modified 2026-09-01) (second pass) | emptied; `dcterms:created`, `dcterms:modified`, `cp:lastPrinted` and `cp:revision` kept | 6 fields in 3 files | the DOCX and the two decks |
| two-part Beethoven version shorthand (the no-fractional-versions rule) (second pass) | the three-part numbers `11.0.0`, `12.0.0` | 8 | `ashley-bridge-project` (2), `beethoven-browser-ssh` (4), `beethoven-first-run-ux` (2) |

**Deliberate keeps, reserved to Greg (PLAN section 5, co-author names).** The published Cureus article
(`manuscripts/cureus_2026_e112661_Schehr_Kim_Schwing.pdf`) keeps its author list and the corresponding author's
university address: they are the public record of the article and the PDF is byte-identical. The two accepted CNS poster
decks keep the author list on their one slide ("Ten sub-projects span 16 contributors", the contributors named there);
only their core properties were touched. Greg decides whether the decks' names stay.

A grep over the finished folder for the banned word, the struck identifiers, `@gmail`, the key ids, the environment
ids and the token paths returns nothing (run 2026-10-08 after the copy). After the second pass a grep for `C:/Users`,
`C:\Users`, `/c/Users`, `/mnt/c/Users`, the Claude project slug, the laptop user name and the struck staff address
returns nothing outside section 4 of this file; the one remaining `Users` fragment, `C:Users[laptop user]AppData...` in
the VS Code checkpoint (line 970), is that text's illustration of a backslash-eating bug, not a path. Placeholders `st1234`, `cd5678`, `zz9999`
and `ab1234` in the Beethoven documents are the product's own example and reviewer-mock accounts, not people.

## 4. Where each copy was read from on 2026-10-08 (history; not a dependency)

| copied to (this folder) | laptop path it was read from on 2026-10-08 |
|---|---|
| `code/beethoven_framework_profiles/wayne.json` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/framework/profiles/wayne.json` |
| `code/student_projects_3f1cf04/.claude/commands/grid-pull.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/.claude/commands/grid-pull.md` |
| `code/student_projects_3f1cf04/.claude/commands/grid-status.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/.claude/commands/grid-status.md` |
| `code/student_projects_3f1cf04/.claude/commands/grid-submit.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/.claude/commands/grid-submit.md` |
| `code/student_projects_3f1cf04/.claude/commands/new-project.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/.claude/commands/new-project.md` |
| `code/student_projects_3f1cf04/.claude/commands/onboard.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/.claude/commands/onboard.md` |
| `code/student_projects_3f1cf04/.claude/settings.json` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/.claude/settings.json` |
| `code/student_projects_3f1cf04/.github/PULL_REQUEST_TEMPLATE.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/.github/PULL_REQUEST_TEMPLATE.md` |
| `code/student_projects_3f1cf04/CLAUDE.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/CLAUDE.md` |
| `code/student_projects_3f1cf04/CONTRIBUTING.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/CONTRIBUTING.md` |
| `code/student_projects_3f1cf04/GETTING_STARTED.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/GETTING_STARTED.md` |
| `code/student_projects_3f1cf04/IDEAS.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/IDEAS.md` |
| `code/student_projects_3f1cf04/LICENSE` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/LICENSE` |
| `code/student_projects_3f1cf04/README.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/README.md` |
| `code/student_projects_3f1cf04/RECIPE.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/RECIPE.md` |
| `code/student_projects_3f1cf04/examples/pelvic_width_dimorphism/README.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/examples/pelvic_width_dimorphism/README.md` |
| `code/student_projects_3f1cf04/examples/pelvic_width_dimorphism/measure_pelvic_width.py` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/examples/pelvic_width_dimorphism/measure_pelvic_width.py` |
| `code/student_projects_3f1cf04/examples/pelvic_width_dimorphism/results/pelvic_width.csv` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/examples/pelvic_width_dimorphism/results/pelvic_width.csv` |
| `code/student_projects_3f1cf04/examples/pelvic_width_dimorphism/results/pelvic_width.png` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/examples/pelvic_width_dimorphism/results/pelvic_width.png` |
| `code/student_projects_3f1cf04/examples/pelvic_width_dimorphism/results/report.txt` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/examples/pelvic_width_dimorphism/results/report.txt` |
| `code/student_projects_3f1cf04/examples/proposal_example/proposal.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/examples/proposal_example/proposal.md` |
| `code/student_projects_3f1cf04/templates/CLAUDE.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/templates/CLAUDE.md` |
| `code/student_projects_3f1cf04/templates/environment.yml` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/templates/environment.yml` |
| `code/student_projects_3f1cf04/templates/get_dataset.sh` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/templates/get_dataset.sh` |
| `code/student_projects_3f1cf04/templates/make_env.sh` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/templates/make_env.sh` |
| `code/student_projects_3f1cf04/templates/proposal_template.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/templates/proposal_template.md` |
| `code/student_projects_3f1cf04/templates/slurm_job.sh` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/templates/slurm_job.sh` |
| `code/student_projects_3f1cf04/templates/ssh_config` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/templates/ssh_config` |
| `code/student_projects_3f1cf04/tools/grid.sh` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/tools/grid.sh` |
| `code/student_projects_3f1cf04/tools/render_board.py` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/tools/render_board.py` |
| `docs/Browser_Extension_HPC_Orchestration_Protocols.pdf` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Browser Extension HPC Orchestration Protocols.pdf` |
| `docs/STARTHERE_the_lab_recipe_2026-09-27.pdf` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Student_Projects/STARTHERE.pdf` |
| `docs/University-Agnostic_HPC_AI_Architecture.pdf` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/University-Agnostic HPC AI Architecture.pdf` |
| `docs/beethoven/ARCHITECTURE.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/ARCHITECTURE.md` |
| `docs/beethoven/DIAGNOSTICS.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/DIAGNOSTICS.md` |
| `docs/beethoven/LICENSE-FULL-NOTE.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/LICENSE-FULL-NOTE.md` |
| `docs/beethoven/MAC_AND_SAFARI.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/MAC_AND_SAFARI.md` |
| `docs/beethoven/OPEN_QUESTIONS.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/OPEN_QUESTIONS.md` |
| `docs/beethoven/PUBLISHING_SITE.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/PUBLISHING_SITE.md` |
| `docs/beethoven/RESEARCH_REPORT.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/RESEARCH_REPORT.md` |
| `docs/beethoven/STORE_LISTING.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/STORE_LISTING.md` |
| `docs/beethoven/TESTERS.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/TESTERS.md` |
| `docs/beethoven/TEXTS_V8_V9.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/TEXTS_V8_V9.md` |
| `docs/beethoven/TEXTS_V9_V10.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/TEXTS_V9_V10.md` |
| `docs/beethoven/V11_CONTRACT.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/V11_CONTRACT.md` |
| `docs/beethoven/V11_STATUS.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/V11_STATUS.md` |
| `docs/beethoven/V12_CONTRACT.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/V12_CONTRACT.md` |
| `docs/beethoven/V12_STATUS.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/V12_STATUS.md` |
| `docs/beethoven/WAYNE_STATE_PILOT.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/WAYNE_STATE_PILOT.md` |
| `docs/beethoven/extension_README.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/extension/README.md` |
| `docs/beethoven/framework_README.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/framework/README.md` |
| `docs/beethoven/guides/ACCOUNTS.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/guides/ACCOUNTS.md` |
| `docs/beethoven/guides/INSTALL.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/guides/INSTALL.md` |
| `docs/beethoven/guides/LAB_LEAD.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/guides/LAB_LEAD.md` |
| `docs/beethoven/guides/USE.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/guides/USE.md` |
| `docs/beethoven/prior_analysis_architecture.txt` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/prior_analysis_architecture.txt` |
| `docs/beethoven/prior_analysis_protocols.txt` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/prior_analysis_protocols.txt` |
| `docs/beethoven/release_14.0.0/README.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/release/14.0.0/README.md` |
| `docs/beethoven/release_14.0.0/SHA256SUMS.txt` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/release/14.0.0/SHA256SUMS.txt` |
| `docs/beethoven/release_14.0.0/STUDENT_QUICKSTART.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/release/14.0.0/guides/STUDENT_QUICKSTART.md` |
| `docs/beethoven/repo_root/CLAUDE.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/CLAUDE.md` |
| `docs/beethoven/repo_root/LICENSE.txt` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/LICENSE.txt` |
| `docs/beethoven/repo_root/PRIVACY.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/PRIVACY.md` |
| `docs/beethoven/repo_root/README.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/README.md` |
| `docs/beethoven/repo_root/SECURITY.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/SECURITY.md` |
| `docs/beethoven/repo_root/THIRD_PARTY_NOTICES.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/THIRD_PARTY_NOTICES.md` |
| `docs/beethoven/store/LISTING.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/store/LISTING.md` |
| `docs/beethoven/store/PASTE.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/store/PASTE.md` |
| `docs/beethoven/store/SUBMISSION.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/store/SUBMISSION.md` |
| `docs/beethoven/store/TEST_BEFORE_UPLOAD.md` | `C:/Users/grego/OneDrive/Desktop/ashley-bridge/docs/store/TEST_BEFORE_UPLOAD.md` |
| `docs/beethoven_vscode/ANTHROPIC_REQUEST.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/ANTHROPIC_REQUEST.md` |
| `docs/beethoven_vscode/ARCHITECTURE.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/ARCHITECTURE.md` |
| `docs/beethoven_vscode/CHECKPOINT_2026-09-28.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/CHECKPOINT_2026-09-28.md` |
| `docs/beethoven_vscode/DIAGNOSTICS.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/DIAGNOSTICS.md` |
| `docs/beethoven_vscode/ENGINEERING.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/ENGINEERING.md` |
| `docs/beethoven_vscode/INSTALL.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/INSTALL.md` |
| `docs/beethoven_vscode/LICENSING.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/LICENSING.md` |
| `docs/beethoven_vscode/LIMITS.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/LIMITS.md` |
| `docs/beethoven_vscode/MAC.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/MAC.md` |
| `docs/beethoven_vscode/MARKETPLACE.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/MARKETPLACE.md` |
| `docs/beethoven_vscode/PITCH.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/PITCH.md` |
| `docs/beethoven_vscode/RESEARCH.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/RESEARCH.md` |
| `docs/beethoven_vscode/diagnostics_graph.json` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/diagnostics_graph.json` |
| `docs/beethoven_vscode/legal/ARBITRATION_OPTION.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/legal/ARBITRATION_OPTION.md` |
| `docs/beethoven_vscode/manual/00_getting_started.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/manual/00_getting_started.md` |
| `docs/beethoven_vscode/manual/90_troubleshooting.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/manual/90_troubleshooting.md` |
| `docs/beethoven_vscode/manual/manual_assembled.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/build/manual.md` |
| `docs/beethoven_vscode/repo_root/CLAUDE.md` | `C:/Users/grego/OneDrive/Desktop/ashley/CLAUDE.md` |
| `docs/beethoven_vscode/repo_root/CONTRIBUTING.md` | `C:/Users/grego/OneDrive/Desktop/ashley/CONTRIBUTING.md` |
| `docs/beethoven_vscode/repo_root/LICENSE` | `C:/Users/grego/OneDrive/Desktop/ashley/LICENSE` |
| `docs/beethoven_vscode/repo_root/README.md` | `C:/Users/grego/OneDrive/Desktop/ashley/README.md` |
| `docs/beethoven_vscode/repo_root/SECURITY.md` | `C:/Users/grego/OneDrive/Desktop/ashley/SECURITY.md` |
| `docs/beethoven_vscode/research/claude_swap_notes.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/claude_swap_notes.md` |
| `docs/beethoven_vscode/research/latency_baseline.csv` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/latency_baseline.csv` |
| `docs/beethoven_vscode/research/latency_node.csv` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/latency_node.csv` |
| `docs/beethoven_vscode/research/latency_probe.sh` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/latency_probe.sh` |
| `docs/beethoven_vscode/research/latency_relay.csv` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/latency_relay.csv` |
| `docs/beethoven_vscode/research/library_peer_test.log` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/library_peer_test.log` |
| `docs/beethoven_vscode/research/library_peer_test.sh` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/library_peer_test.sh` |
| `docs/beethoven_vscode/research/plot_latency.py` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/plot_latency.py` |
| `docs/beethoven_vscode/research/rc_probe.log` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/rc_probe.log` |
| `docs/beethoven_vscode/research/rc_probe.sh` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/rc_probe.sh` |
| `docs/beethoven_vscode/research/reports/Ashley liability shield and Marketplace.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/reports/Ashley liability shield and Marketplace.md` |
| `docs/beethoven_vscode/research/reports/Ashley terms of service constraints.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/reports/Ashley terms of service constraints.md` |
| `docs/beethoven_vscode/research/reports/Browser extension HPC Claude worker.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/reports/Browser extension HPC Claude worker.md` |
| `docs/beethoven_vscode/research/research_notes/Ashley liability shield and Marketplace/contract_dispute_shields.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/research_notes/Ashley liability shield and Marketplace/contract_dispute_shields.md` |
| `docs/beethoven_vscode/research/research_notes/Ashley liability shield and Marketplace/entity_insurance_filings.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/research_notes/Ashley liability shield and Marketplace/entity_insurance_filings.md` |
| `docs/beethoven_vscode/research/research_notes/Ashley liability shield and Marketplace/marketplace_removal_prevention.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/research_notes/Ashley liability shield and Marketplace/marketplace_removal_prevention.md` |
| `docs/beethoven_vscode/research/research_notes/Ashley liability shield and Marketplace/regulatory_multistate_exposure.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/research_notes/Ashley liability shield and Marketplace/regulatory_multistate_exposure.md` |
| `docs/beethoven_vscode/research/research_notes/Ashley terms of service constraints/anthropic_terms.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/research_notes/Ashley terms of service constraints/anthropic_terms.md` |
| `docs/beethoven_vscode/research/research_notes/Ashley terms of service constraints/eula_law_and_marketplace.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/research_notes/Ashley terms of service constraints/eula_law_and_marketplace.md` |
| `docs/beethoven_vscode/research/research_notes/Ashley terms of service constraints/github_huggingface_terms.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/research_notes/Ashley terms of service constraints/github_huggingface_terms.md` |
| `docs/beethoven_vscode/research/research_notes/Ashley terms of service constraints/telemetry_and_ai_maintenance_practice.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/research_notes/Ashley terms of service constraints/telemetry_and_ai_maintenance_practice.md` |
| `docs/beethoven_vscode/research/research_notes/Ashley terms of service constraints/wsu_grid_and_it_policy.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/research_notes/Ashley terms of service constraints/wsu_grid_and_it_policy.md` |
| `docs/beethoven_vscode/research/research_notes/Browser extension HPC Claude worker/anthropic_surfaces_and_terms.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/research_notes/Browser extension HPC Claude worker/anthropic_surfaces_and_terms.md` |
| `docs/beethoven_vscode/research/research_notes/Browser extension HPC Claude worker/browser_extension_platform.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/research_notes/Browser extension HPC Claude worker/browser_extension_platform.md` |
| `docs/beethoven_vscode/research/research_notes/Browser extension HPC Claude worker/hpc_portability_layer.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/research_notes/Browser extension HPC Claude worker/hpc_portability_layer.md` |
| `docs/beethoven_vscode/research/research_notes/Browser extension HPC Claude worker/open_ondemand_gateway.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/research_notes/Browser extension HPC Claude worker/open_ondemand_gateway.md` |
| `docs/beethoven_vscode/research/research_notes/Browser extension HPC Claude worker/prior_art_and_comparables.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/research_notes/Browser extension HPC Claude worker/prior_art_and_comparables.md` |
| `docs/beethoven_vscode/research/research_notes/Browser extension HPC Claude worker/security_policy_licensing.md` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/research/research_notes/Browser extension HPC Claude worker/security_policy_licensing.md` |
| `docs/handoff/DATASET_USAGE.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/DATASET_USAGE.md` |
| `docs/handoff/GLOSSARY.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/GLOSSARY.md` |
| `docs/handoff/INFRASTRUCTURE.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/INFRASTRUCTURE.md` |
| `docs/handoff/LEAKAGE.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/LEAKAGE.md` |
| `docs/handoff/OPEN_QUESTIONS.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/OPEN_QUESTIONS.md` |
| `docs/handoff/README.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/README.md` |
| `docs/handoff/RECIPES.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/RECIPES.md` |
| `docs/handoff/RESULTS_CATALOG.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/RESULTS_CATALOG.md` |
| `docs/outreach/cm_spine_request_email.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/proposals/cm_spine_request_email.md` |
| `docs/outreach/student_primer_email.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/proposals/student_primer_email.md` |
| `docs/survey_protocol.md` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/docs/survey_protocol.md` |
| `figures/beethoven_vscode/accounts.svg` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/figures/accounts.svg` |
| `figures/beethoven_vscode/latency.png` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/figures/latency.png` |
| `figures/beethoven_vscode/latency.svg` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/figures/latency.svg` |
| `figures/beethoven_vscode/lifecycle.svg` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/figures/lifecycle.svg` |
| `figures/beethoven_vscode/topology.svg` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/figures/topology.svg` |
| `figures/beethoven_vscode/wizard.svg` | `C:/Users/grego/OneDrive/Desktop/ashley/docs/figures/wizard.svg` |
| `manuscripts/OSC_MedEd_Manuscript_JEEHP.docx` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/OSC MedEd Manuscript - JEEHP.docx` |
| `manuscripts/cureus_2026_e112661_Schehr_Kim_Schwing.pdf` | `C:/Users/grego/OneDrive/Desktop/cureus.pdf` |
| `manuscripts/talks/Med_Ed_CNS.pptx` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Med_Ed_CNS.pptx` |
| `manuscripts/talks/Med_Ed_CNS_visual_abstract.pptx` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Med_Ed_CNS_visual_abstract.pptx` |
| `memory/ashley-bridge-project.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/GREG_ONLY/context_beethoven/ashley-bridge-project.md` |
| `memory/ashley-compliance-boundary.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/GREG_ONLY/context_beethoven/ashley-compliance-boundary.md` |
| `memory/ashley-extension-project.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/GREG_ONLY/context_beethoven/ashley-extension-project.md` |
| `memory/bash-heredoc-backslashes.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/bash-heredoc-backslashes.md` |
| `memory/beethoven-2026-10-02-field-failures.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/GREG_ONLY/context_beethoven/beethoven-2026-10-02-field-failures.md` |
| `memory/beethoven-browser-ssh.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/GREG_ONLY/context_beethoven/beethoven-browser-ssh.md` |
| `memory/beethoven-first-run-ux.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/GREG_ONLY/context_beethoven/beethoven-first-run-ux.md` |
| `memory/ct-volumes-are-pir-not-ras.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/ct-volumes-are-pir-not-ras.md` |
| `memory/data-directives-2026-09-23.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/data-directives-2026-09-23.md` |
| `memory/diagnostics-graph-required.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/diagnostics-graph-required.md` |
| `memory/figure-captions-terse.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/figure-captions-terse.md` |
| `memory/fluorocap-repo-private.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/fluorocap-repo-private.md` |
| `memory/grid-access-list-gate.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-access-list-gate.md` |
| `memory/grid-access.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-access.md` |
| `memory/grid-apptainer-module-works.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-apptainer-module-works.md` |
| `memory/grid-ashley-deletion-2026-09-28.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-ashley-deletion-2026-09-28.md` |
| `memory/grid-bash-4-2-quoting.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-bash-4-2-quoting.md` |
| `memory/grid-ceph-volume-oschome.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-ceph-volume-oschome.md` |
| `memory/grid-local-singularity-is-broken.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-local-singularity-is-broken.md` |
| `memory/grid-slurm-inside-apptainer.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-slurm-inside-apptainer.md` |
| `memory/grid-ssh-second-factor.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-ssh-second-factor.md` |
| `memory/hf-mirror-is-v10.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/hf-mirror-is-v10.md` |
| `memory/key-patients-from-metadata-not-filenames.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/key-patients-from-metadata-not-filenames.md` |
| `memory/lab-recipe-and-board.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/lab-recipe-and-board.md` |
| `memory/label-scheme-v4-vs-ostk.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/label-scheme-v4-vs-ostk.md` |
| `memory/morphology-deformation-feasibility.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/morphology-deformation-feasibility.md` |
| `memory/never-reorient-when-writing-labels.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/never-reorient-when-writing-labels.md` |
| `memory/no-jobs-on-login-node.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/no-jobs-on-login-node.md` |
| `memory/no-unexplained-subsets-fix-not-disclose.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/no-unexplained-subsets-fix-not-disclose.md` |
| `memory/scratchpad-shadows-stdlib.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/scratchpad-shadows-stdlib.md` |
| `memory/student-onboarding-structure.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/student-onboarding-structure.md` |
| `memory/students-see-no-internals.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/students-see-no-internals.md` |
| `memory/submit-and-sleep-orchestration.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/submit-and-sleep-orchestration.md` |
| `memory/user-affiliation-general-surgery.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/user-affiliation-general-surgery.md` |
| `memory/windows-junction-worktree-trap.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/windows-junction-worktree-trap.md` |
| `memory/windows-ssh-to-grid.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/windows-ssh-to-grid.md` |
| `memory/writing-preferences.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/writing-preferences.md` |
| `memory/wsl-for-network.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/wsl-for-network.md` |
| `memory/wsu-library-access-cutoff.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/wsu-library-access-cutoff.md` |
| `regulatory/openresearch/command.txt` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/openresearch/command.txt` |
| `regulatory/openresearch/extension.txt` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/openresearch/extension.txt` |
| `regulatory/openresearch/firstprompt.txt` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/openresearch/firstprompt.txt` |
| `regulatory/openresearch/fourthprompt.txt` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/openresearch/fourthprompt.txt` |
| `regulatory/openresearch/secondprompt.txt` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/openresearch/secondprompt.txt` |
| `regulatory/openresearch/thirdprompt.txt` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/openresearch/thirdprompt.txt` |
| `regulatory/openresearch/zeroethprompt.txt` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/openresearch/zeroethprompt.txt` |

## 5. Copied records that carried laptop paths or short prefixes inside their text

Twenty-six copies mentioned a laptop path (`C:/Users/...`, `C:\Users\...`, `/c/Users/...`, `/mnt/c/Users/...`, the
OneDrive Desktop folder or the Claude project slug) in their own wording. The copy stage left them as written, as dated
records. The verifier of 2026-10-08 counted every laptop path outside this file as a defect against self-containment,
and this folder's `CLAUDE.md` says the vendor folder is never named beyond its folder name, which four of the copies
contradicted (`LAB_LEAD.md` lines 315 to 316, `PUBLISHING_SITE.md` line 108, the two repositories' `CLAUDE.md`, the
VS Code checkpoint). The second pass therefore replaced the paths by kind (section 3: 96 replacements) and wrote
`laptop path (n)` into each copy's record line, with the sentence that the placeholders stand for the Windows, Git Bash
and WSL spellings alike. The files, with counts: `docs/beethoven/` `MAC_AND_SAFARI.md` (1), `PUBLISHING_SITE.md` (5),
`extension_README.md` (1), `guides/LAB_LEAD.md` (2), `repo_root/CLAUDE.md` (4), `repo_root/README.md` (1),
`store/PASTE.md` (1); `docs/beethoven_vscode/` `CHECKPOINT_2026-09-28.md` (25), `LICENSING.md` (2), `MAC.md` (6),
`MARKETPLACE.md` (5), `repo_root/CLAUDE.md` (4), the research notes `regulatory_multistate_exposure.md` (2),
`prior_art_and_comparables.md` (6), `security_policy_licensing.md` (1); `docs/handoff/` `INFRASTRUCTURE.md` (3),
`README.md` (9; its section 0 now defines the prefixes against `[laptop Desktop]/...`), `RECIPES.md` (2),
`RESULTS_CATALOG.md` (5); `memory/` `ashley-bridge-project` (2), `ashley-extension-project` (3), `lab-recipe-and-board`
(1), `student-onboarding-structure` (1), `windows-junction-worktree-trap` (2), `windows-ssh-to-grid` (1),
`wsl-for-network` (1). The short prefixes (`ssn:`, `ctsp:`, `bth:`, `students:`) stay as written. The path each copy was
read from is in section 4 of this file and nowhere else; the unredacted originals are reachable through the commit named
in each copy record. The eight files written for this folder (`CLAUDE.md`, `README.md`, `MEMORY.md`, `STATUS.md`,
`TODO.md`, `MANIFEST_GRID.md`, `MANIFEST_CODE.md`, `docs/handoff/EXTRACTS_11.md`) carry no laptop path. Word-level
mentions of OneDrive (`templates/CLAUDE.md` line 125, `cm_spine_request_email.md` line 51, a WSU policy title in
`wsu_grid_and_it_policy.md`) are words, not paths, and stay.

## 6. Valuable files NOT copied, and why

| file or folder | where it lives | why not copied | how to reach it |
|---|---|---|---|
| the six e-mail drafts and `EMAIL.md` in the dataset repository's private backup folder `CTSP1K_private/proposals_backup_20260911/` (Annotator_Email.docx, annotator_email.md, a named student's e-mail, lab_update_email_2026-09-07.md, student_primer_email.md, cm_spine_request_email.md) | the laptop only | personal and administrative correspondence, classified from the file names and not opened (the task's rule); the two research-relevant drafts exist in the tracked `proposals/` and are copied redacted | Greg's private records |
| `AI_Imaging_Workshop.docx` (199,200 B, 2026-05-26) and `AI_Imaging_Workshop.pdf` (90,034 B on the Desktop; 90,116 B tracked in the website repository) | Desktop root; website repository | the tracked website copy is the record (note the two sizes differ, measured 2026-10-08; the disposition row had them the other way round); the Word source adds nothing a student needs | `openspineconsortium.github.io/AI_Imaging_Workshop.pdf` |
| `AshleyBridge-6.0.0-tester-package.zip` (371,017 B, 2026-09-29) and the unpacked `Ashley Bridge for testers/` folder | Desktop root | superseded by release 14.0.0 and the private Chrome listing; a package, not text; listed by path in `99_archive` | `OpenSpineConsortium/beethoven` `release/6.0.0/` |
| the Beethoven release packages (`release/4.0.0` to `14.0.0` zips, the bridge installers, the reviewer mock zip, store screenshots) | the Beethoven repository | packages and images, in the repository at 2f90319 | the repository |
| `extension/`, `framework/` and `tools/` code of both repositories (including `tools/grid_access.sh`, `tools/deploy_shared.sh`, `grid/bootstrap.sbatch`, `grid/worker.sbatch.tpl`, `tools/intake/worker.js`) | the two repositories | better referenced than copied: they are tracked at known commits and change with every release; only the Wayne site profile is copied because it is the lever of TODO step 2 | `MANIFEST_CODE.md` section 1 |
| `grid/license_keys.json`, `extension/src/licensing/keys.json` | the two repositories | verification keys only, but keys by name; nothing secret is in them and nothing key-shaped is copied here | the repositories |
| the vendor folder (signing keys, admin token, GitHub admin token, the Marketplace PAT) | outside every repository, on Greg's laptop and under his grid HOME | never read, never copied, never listed beyond its name | Greg only |
| `docs/DEPENDENCY_MAP.md` (440 KB), `docs/manual.pdf` (931 KB), `docs/manual.html` (263 KB), `docs/research/deep_research_2026-09-28.json` (1.7 MB), `deep_research_raw_2026-09-28.txt` (2.0 MB), `dependency_map_2026-09-28.json` (517 KB), `access_review_2026-09-28.json` (154 KB), `claude_swap_study_2026-09-28.json` (59 KB) of the VS Code edition | `OpenSpineConsortium/beethoven-vscode` 8d7fc65 | generated or raw tool output; the reports and notes distilled from them are copied | the repository |
| `docs/site/beethoven/` of the Beethoven repository | the repository | generated site fragments; the site repository builds the pages | the repository |
| `Student_Projects/board.json` and `BOARD.md` | the nested repository, local 3f1cf04 | they name members by name; the cards' facts (12 cards, 10 unstaffed, the roles) are in `STATUS.md` section D; the people table names Greg, Ashley Schehr, "Dr Tech" and the faculty sponsor only | the repository once 3f1cf04 is pushed, or Greg's clone |
| `Student_Projects/projects/` | a clone of the private `OpenSpineConsortium/Projects` | private project folders; one proposal there | that repository |
| `spinesurg-ct-annotator/assignments.json` (204 B) | `Gregory-Schwing-MD-PhD/spinesurg-ct-annotator` 1083c4f | may name students; the app is superseded | the repository |
| `morphometrics/annotation_counts.csv` (11 student usernames) and `morphometrics/annotator_names.csv` (names) | `OpenSpineConsortium/CTSpinoPelvic1K` 7ddfe38, tracked in a public repository | usernames and names; Greg decides their removal (PLAN section 5); the count is quoted in `STATUS.md` section F | the repository |
| the raw medical-education survey CSV and its zip | never committed; the laptop | holds names; the published article and the JEEHP draft carry the aggregate (16 respondents, six domains) | Greg only |
| the participation survey, `CNS 2026 ABSTRACT PROJECTS.csv`, the student headshots and `contributions/manifest.json` | various | identities; listed in `../_plan/EXCLUDED.md` | — |
| the review Space trees on the grid (`/wsu/home/go/go24/go2432/CTSpinoPelvic1K-review`, `/wsu/home/go/go24/go2432/ctspinopelvic1k-review-triaged`, `/wsu/home/go/go24/go2432/spinesurg-ct-annotator.backup`) | HOME on the grid | may hold reviewer usernames; never copied (`MANIFEST_GRID.md` section 4) | the grid |
| `HANDOFF/GREG_ONLY/` (PRIVATE_STATE.md, README.md, `context/` with the five moved notes and three full copies) | the private repository's handoff folder, untracked | Greg-only by the handoff's own split; referenced by path from `01_carm_level_detection` and `../_plan/EXCLUDED.md` | Greg |
| `HANDOFF/MANUSCRIPTS.md`, `CONTEXT_EXPORT.md`, `RESEARCH_DIRECTIONS.md`, `LITERATURE_STATE.md`, `working_notes/` | the same | Greg-only handoff files; this student-safe-after-redaction folder receives their sections as extracts only (`MANUSCRIPTS.md` section 12 and 21 item 7 are quoted in `STATUS.md` and `TODO.md`) | the Greg-only folders 01, 02, 07, 08, 09 |
| the IRB determination letters (HPR 2026-269 of 2 September 2026 and the public-datasets determination) | the dataset repository root (untracked PDFs) | regulatory documents of the hospital-testing plan: copied into `01_carm_level_detection/regulatory/` by the plan, not duplicated here; the student umbrella rule is quoted from `RECIPE.md` section 3 | `01_carm_level_detection/regulatory/` |
| the memory notes `review-space-repos`, `annotator-roster` (redacted) | `HANDOFF/context/` | their row homes are the dataset family (folder 03); their facts that matter here are in `docs/handoff/INFRASTRUCTURE.md` section 11 | `03_ctspinopelvic1k_dataset/memory/` |
| the five Greg-only memory notes, the seven U251 / LITT notes, the six history-only resume notes, the live `MEMORY.md` index | the live memory folder; `GREG_ONLY/context/` | never copied into any project folder (PLAN section 2 rule 5) | Greg |
| the session scratchpads (the v11 and v12 build trees, the IWA spike's `REPORT.md` and `STUDENT_STEPS.md`, the browser-ssh design `SSH_DESIGN.md`, the site backup bundle of 172 MB) | the laptop's temporary folders | not in any repository; the memory notes record their results; `TODO.md` step 14 names the three tests written there | not reachable from a repository: **not on disk in a repository** |

## 7. Departures from the disposition rows, recorded

| row | disposition said | done here | why |
|---|---|---|---|
| the med-ed docx and the two decks | `manuscripts/talks/` for all three | the docx under `manuscripts/`, the decks under `manuscripts/talks/` | a manuscript is not a talk |
| the two Beethoven repositories | reference only (`MANIFEST_CODE.md`) | referenced, and their documents copied under `docs/beethoven/` and `docs/beethoven_vscode/` | the plan's section for this folder names the documents to copy; the task text repeats the list |
| `Student_Projects` | reference only | referenced, and the recipe, templates, tools, commands and examples copied under `code/student_projects_3f1cf04/` | commit 3f1cf04 is not on the remote, so a reader with only the repository cannot reach the recipe; self-containment requires the copy; `board.json` / `BOARD.md` stay out |
| `STARTHERE.pdf` | not in any row (untracked, found on 2026-10-08) | copied to `docs/` | it is the 14-page export of the Lab Recipe Claude Doc of 2026-09-27, named by `@greg` only |
| `survey_protocol.md` | copied as the med-ed survey protocol | copied, and described as what it is: the PACS-demo usability survey protocol | read on 2026-10-08; the med-ed instrument is not on disk as a separate file |
| the HANDOFF section rows (README 4, 8, 9, 10; INFRASTRUCTURE 8, 11; GREG_ONLY/context_beethoven folder) | "copy" to `docs/handoff/` and `memory/` | the whole student-readable files copied, the sections extracted into `docs/handoff/EXTRACTS_11.md`, the six notes copied redacted | the HANDOFF rule of PLAN section 2 rule 3 |
| file names with spaces | — | the two PDFs and the docx renamed with underscores; the Cureus PDF named by journal, year, article id and authors | git-friendly names; the original names are in section 4 |

## 8. The second pass of 2026-10-08 (the verifier's fixes)

Applied after the verification of this folder, on the copies and on this file; nothing was re-copied from a source.

- Laptop paths replaced by kind in 26 copies, 96 replacements (sections 3 and 5); each copy record amended.
- `wsu_grid_and_it_policy.md`: one staff e-mail struck by kind (section 3).
- `OSC_MedEd_Manuscript_JEEHP.docx`: the corresponding address struck in the body and the core properties emptied; the two
  PPTX: core properties emptied; the Cureus PDF and the decks' author lists kept deliberately (section 3).
- The four research probes under `docs/beethoven_vscode/research/`: copy-record comment lines added (section 1).
- `ashley-bridge-project`, `beethoven-browser-ssh`, `beethoven-first-run-ux`: version shorthand written in full (8).
- Section 2: bytes and sha256 recomputed from disk for every row (37 rows changed); section 1 totals recomputed
  (10,886,710 bytes).


## Final pass of 2026-10-08 (after the critic's check of the whole tree)

Rows added by the final pass; the sections above are the first build and the verifier's fix pass as they were. Sources are laptop paths of 2026-10-08 (history, not dependencies). sha1 is the first 16 hex digits of the copy.

### Record added, nothing copied

`STATUS.md` section E gained one row (the Preston M. Hickey Medical Student Symposium placings of 2026-08-07) citing `../99_archive/manuscripts/talks/PRESENTATIONS_RECORD_2026-08-17.md`, a redacted extract of the laptop file `<laptop:Desktop>/Schwing_Presentations.docx`; no student name enters this folder by it.

### Redaction made the same in every folder

The one Hugging Face handle quoted beside a published co-author's name was withheld in some folders and kept in others for the same source line (the critic's finding). It now reads `(HF username withheld)` everywhere (one occurrence per file below); the person's name stays (a person, never renamed). Greg may restore it; it is his decision (PLAN.md section 5).

- `docs/handoff/RECIPES.md`

### E-mail address withheld

`memory/wsu-library-access-cutoff.md`: the library contact address replaced by `[library e-mail withheld]` (the library's public phone numbers kept), the same as 08's copy already read.

### Example account withheld

An example sign-in line in two Beethoven documents named a short university account (`alex@...`); whether it is a real tester's account is not recorded, so it now reads `<AccessID>@wayne.edu`:

- `docs/beethoven/framework_README.md` (2)
- `docs/beethoven/V11_CONTRACT.md` (3)

### Laptop paths rewritten to markers (self-containment)

The critic's tree-wide scan still found laptop spellings in copied files of this folder outside `MANIFEST_LOCAL.md`. They are now the markers the other folders use: `<laptop:Desktop>` for the Desktop root that held every repository checkout (`<laptop:Desktop>/spinesurg-ct-nnunet` = spinesurg-ct-nnunet at 097933a, `<laptop:Desktop>/CTSpinoPelvic1K-1` = CTSpinoPelvic1K at 7ddfe38, `<laptop:Desktop>/OpenSpineToolkit` = OpenSpineToolkit at cb43197, `<laptop:Desktop>/XRaySpinoPelvic1K` = XRSpinoPelvic1K at 4f22935), `<laptop:Temp scratchpad>` for the swept session scratchpad (nothing there is a dependency), `<laptop memory folder>` for the live memory notes (copied redacted into `memory/`), `<laptop vendor folder, never read>` and `<laptop home>`. The marker is a spelling of where the file came from, not a path to resolve; the repository and commit are the dependency. Scripts among these copies (`.py`, `.sh`) hard-coded laptop roots and did not run anywhere else before this change either; they are records of how a document was built.

| file | laptop spellings rewritten | left |
|---|---:|---:|
| `code/student_projects_3f1cf04/templates/ssh_config` | 1 | 0 |
| `docs/beethoven_vscode/research/research_notes/Browser extension HPC Claude worker/prior_art_and_comparables.md` | 3 | 0 |
| `docs/handoff/RESULTS_CATALOG.md` | 1 | 0 |

### A third-party address withheld

`docs/beethoven_vscode/research/research_notes/Ashley terms of service constraints/telemetry_and_ai_maintenance_practice.md`: a kernel mailing-list Message-ID carried the poster's address; the local part now reads `[poster address withheld]` (the date token that locates the post is kept).
