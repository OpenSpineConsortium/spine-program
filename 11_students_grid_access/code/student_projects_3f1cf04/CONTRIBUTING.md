<!-- spine-program/11_students_grid_access copy record. Source: OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path CONTRIBUTING.md. Copied 2026-10-08. Redactions applied by kind: none. Any laptop path or short prefix inside this text is the source's own wording and is history, not a dependency of this folder; the live reference is the repository at the commit named. -->

# Contributing

## Proposing a project

1. Clone this public repository, then clone the private
   [Projects](https://github.com/OpenSpineConsortium/Projects) repository inside it as
   `projects/` (`gh repo clone OpenSpineConsortium/Projects projects`). You will have been
   added as a collaborator after emailing the project lead your GitHub username; `/onboard`
   in Claude Code does both clones.
2. Inside `projects/`, create a branch named `proposal/<lastname>-<topic>`, for example
   `proposal/schwing-pelvic-width-dimorphism`.
3. Copy `templates/proposal_template.md` to `projects/<lastname>_<topic>/proposal.md` and
   fill it in. Keep it to about one page. Every section of the template exists because a
   reviewer will ask about it.
4. Push the branch and open a pull request in Projects (private, so only collaborators see
   it). The PR template asks for three things beyond
   the proposal: the email address that should receive the ClickUp invitation, the mentor
   you are requesting, and a checklist confirming you have run the demo study.
5. The review happens in the PR thread. Expect questions about the measurement (what
   exactly is measured, from which labels, in which units) and about the comparison (who is
   compared with whom, and what is excluded). Revise by pushing to the same branch.
6. When approved, the PR is merged and a ClickUp workspace invitation goes to the email
   you gave. Milestones from the proposal become ClickUp tasks.

## Working on an approved project

- Work on a branch per piece of work (`<lastname>/<what>`), open a PR when it is ready for
  eyes, and reference the ClickUp task in the PR description.
- Put code in your project folder. Scripts should run from the repository root with the
  environment in `templates/environment.yml` (copy it into your folder if you need more).
- Put derived data (per-record CSVs of measurements) in `results/` inside your folder.
  Never commit CT or label volumes.
- Every figure in your write-up must come from a script in your folder, and the script must
  produce the numbers you quote. If a number is in the text, it is in a CSV or a report the
  script wrote.
- Keep a short `JOURNAL.md` in your folder: dated notes of what you tried and what you
  found, including the dead ends. It is the raw material of the methods section.

## Using Claude Code

Claude Code is the assistant you will write most of your code with. Copy
`templates/CLAUDE.md` into your project folder and edit the paths; it tells Claude how the
grid works, where the data is, and which rules never to break. Claude drafts, you read. You
run `sbatch` yourself (or say "submit it" and Claude runs exactly that one command), and you
look at every figure before you believe it. The repository's `.claude/` folder gives Claude the
`/grid-status`, `/grid-submit`, `/grid-pull` and `/new-project` commands and pre-approves the
routine tools; `tools/grid.sh` is what those commands call.

## Authorship

Contributions are recorded as the work proceeds. Authorship on anything published follows
the ICMJE criteria: substantial contribution to design, data or analysis; drafting or
critical revision; approval of the final version; and accountability for the work.

## Data rules

The datasets are released under their own licenses (CTSpinoPelvic1K: CC BY-NC-SA 4.0).
They are research-use only. Do not redistribute volumes, and cite the dataset DOI.
