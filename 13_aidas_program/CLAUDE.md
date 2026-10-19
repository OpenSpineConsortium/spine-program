# 13 The AIDaS program: working context

The work that follows the AIDaS Seed Grant proposal of 2026-10-16, mapped as issues (`README.md`, `PLAN.md`). Reader:
Ashley and Greg; the tasks are given to `worker:aschehr` unless they name another owner. The root `CLAUDE.md` rules bind
here; these are this folder's.

## Rules that bind this program

- **No patient data reaches a cloud AI service, the Claude agent included.** Claude works on code, public data and
  aggregate results only, under a grid account with no read access to the cohort's directories; jobs that touch the
  cohort are started by study personnel and return aggregates. Nothing from E3 or E6.6 starts before IRB-26-03-8648 is
  approved (E2.1) and DMC access is recorded (E2.4).
- **Elsevier content is never made public.** WSU's text and data mining grant covers Scopus and ScienceDirect, text,
  images and multimedia. On 2026-10-19 the WSU library confirmed that academic access is unrestricted, and Elsevier
  clarified that Claude may read the text, so long as the token and the text are never made publicly accessible
  (Greg, `memory/elsevier-grant-and-terms.md`). It never trains or fine-tunes a model, as WSU told Elsevier on
  2026-10-15, and appears in anything published only as short quotations with citation and DOI. The API key and the
  institutional token are kept server-side, readable by their owner alone, sent only in the headers X-ELS-APIKey and
  X-ELS-Insttoken over HTTPS; never in git, a browser, a URL, a log or a command line.
- **OpenEvidence gets only the question on a public image and the detectors' reading**, never a passage or a record.
- **Seal, then score.** Each task's gate is sealed by hash before its first job; a number produced before that is
  calibration (root rule 6). The REFORMS record is kept as the work goes (`REFORMS.md`).
- **The two gates.** Code passes beethoven-qa (contracts searched by CrossHair and Z3); every held-out number passes
  beethoven-research's split check (no patient, study, cadaver or CT source volume shared with training) and the
  evaluation gate (root rule 5). Of REFORMS, only the split check is built today; the other checks are tasks here.
- **Private stays private.** The level-identification code, text, figures and weights stay private (root rule 8); the
  disclosure audit runs before any talk, poster, upload or submission. Weights trained on patient data stay on the grid.
- **The grid.** Every computation is an sbatch job; nothing on the login node (root rule 7).
- **No run that spends tokens on the protocol comparison (E7.5) starts without Greg's word and number.**
- **People.** Ashley Schehr is a person, never a product name; the product is Beethoven. No student name or username,
  and no researcher or personal e-mail address, in any file here (root rule 12): trainees are coded, never named.

## Files

- `plan.json`: the program as data, the source of `PLAN.md` and of the issues.
- `render_plan.py`, `make_issues.py`: write `PLAN.md`; open and link the issues.
- `REFORMS.md`: the REFORMS checklist's eight modules against the tasks that fill them and the check that holds each.
- `templates/`, `reports/`: the gate and record templates (E1.2) and the monthly notes (E1.6), filled by those tasks.
- `STATUS.md`, `TODO.md`, `MEMORY.md` and `memory/`: as in every folder.
