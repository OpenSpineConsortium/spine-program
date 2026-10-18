# 13 The AIDaS program: one map from the IRB to the spine RAG-LLM

The whole program the AIDaS Seed Grant proposal of 2026-10-16 describes, as one tree of GitHub issues that SymphonyBoard
draws: the goal ([#121](https://github.com/OpenSpineConsortium/spine-program/issues/121)), ten epics and fifty tasks,
each task with its owner, its pass/fail gate, its REFORMS modules and what it waits on. The proposal itself, its record
and its submission are `../01_carm_level_detection/grants/aidas_2027/`; this folder is the work that follows it.
Reader: Ashley and Greg; the tasks are given to Ashley's worker label `worker:aschehr` unless they name another owner.

## The epics

| epic | issue | what |
|---|---|---|
| E1 Workflow | [#122](https://github.com/OpenSpineConsortium/spine-program/issues/122) | the way of working: sealed gates, REFORMS records, beethoven-qa, beethoven-research's split check, CLAIM |
| E2 IRB and regulatory | [#129](https://github.com/OpenSpineConsortium/spine-program/issues/129) | IRB-26-03-8648, the trainee study's exempt application, DMC access, the FDA Pre-Submission, the cadaver paperwork |
| E3 Clinical data mining | [#136](https://github.com/OpenSpineConsortium/spine-program/issues/136) | the DMC cohort: data dictionary, query, de-identification, double coding, pre-registered case-control analyses |
| E4 C-arm training | [#142](https://github.com/OpenSpineConsortium/spine-program/issues/142) | COBRA's unseen projections, corner labels, the leave-one-device-out detector, learned simulation, the cadaver set, latency |
| E5 Literature data mining | [#149](https://github.com/OpenSpineConsortium/spine-program/issues/149) | the Scopus and ScienceDirect spine corpus on the grid, its passage index and the grid text model |
| E6 The spine RAG-LLM | [#154](https://github.com/OpenSpineConsortium/spine-program/issues/154) | the base model, the detectors as tools, two releases, the question set, OpenEvidence |
| E7 Aim 1, the agent's research | [#161](https://github.com/OpenSpineConsortium/spine-program/issues/161) | the 30 tasks, the planted faults, the 80 runs, the economies, the protocol comparison |
| E8 Recruitment and Aim 2 | [#167](https://github.com/OpenSpineConsortium/spine-program/issues/167) | eight trainees in two waves, accounts and seats, the matched starter tasks, the survey |
| E9 Award administration | [#173](https://github.com/OpenSpineConsortium/spine-program/issues/173) | allowability, the hire, the purchases |
| E10 Proposals and dissemination | [#177](https://github.com/OpenSpineConsortium/spine-program/issues/177) | CAREER, R21, CyberTraining, the symposium, the other fits |

`PLAN.md` is the same tree as prose, every task in a row.

## Seeing it in SymphonyBoard

The control panel (https://openspineconsortium.com/symphony/control/), signed in with GitHub and pointed at
OpenSpineConsortium/spine-program, draws the goal, the epics and the tasks from GitHub's own sub-issues, and the
Dependencies section draws each task's "blocked by" from the "waits on" column. The board (`/board`, or the file
STATE.md on the branch `board`) lists the tasks given to `worker:aschehr` under Given to workers; an epic is never
in the Queue.

## Working a task

1. Read `CLAUDE.md` here, then the task's issue.
2. Claim it by `../docs/agents/PROTOCOL.md`: a branch `claude/<issue>` whose first commit is the claim file, a draft
   pull request at once.
3. Seal the gate before the first job (`templates/GATE.md`, from task E1.2) and keep the REFORMS record as the work
   goes (`templates/REFORMS_RECORD.md`; `REFORMS.md` says which module each task feeds).
4. Code passes beethoven-qa; every held-out number passes beethoven-research's split check and the evaluation gate.
5. The pull request deletes the claim file and closes the issue; Greg merges.

## Changing the map

Edit `plan.json`, then `python3 render_plan.py` (rewrites `PLAN.md`) and `python3 make_issues.py` (opens what has no
issue yet, links it under its parent and sets its "blocked by"; `--dry-run` prints first), in one pull request.
