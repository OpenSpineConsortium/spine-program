<!-- spine-program/11_students_grid_access copy record. Source: OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path .claude/commands/new-project.md. Copied 2026-10-08. Redactions applied by kind: lead address (1). Any laptop path or short prefix inside this text is the source's own wording and is history, not a dependency of this folder; the live reference is the repository at the commit named. -->

Start a new project folder for: $ARGUMENTS

Projects live in `projects/`, which is its own private git repository (OpenSpineConsortium/Projects)
cloned inside this public one. Every git command below runs inside `projects/`.

1. Check `projects/.git` exists; if not, run `gh repo clone OpenSpineConsortium/Projects projects`
   (if that fails with not found, I have not been added yet: tell me to email my GitHub
   username to [the lead's university address], subject "Projects access", and stop).
2. Ask me for my last name and a two-or-three-word topic if they are not in the arguments,
   and form the folder name `<lastname>_<topic>` in lower case with underscores.
3. In `projects/`: `git pull`, then create a branch `proposal/<lastname>-<topic>` from `main`.
4. Create the folder with: `proposal.md` copied from `templates/proposal_template.md`,
   `CLAUDE.md` copied from `templates/CLAUDE.md` with the EDIT lines filled from what I
   tell you, `JOURNAL.md` with today's date and one line, and empty `results/` and
   `figures/` folders (with a `.gitkeep` each).
5. Walk me through the proposal one section at a time, asking one question per section,
   and write my answers into `proposal.md` in full sentences. If I chose an entry from
   `IDEAS.md`, start from its measurement and comparison. For section 3, insist on label
   identifiers, an axis and a unit for every measurement, and check the identifiers against
   `dataset_labels.json` if the dataset is on this machine.
6. When every section is filled, show me the whole proposal, then commit it in `projects/`
   with the message `Proposal: <title>` and push the branch. Open the pull request with
   `gh pr create --fill --base main` in `projects/`, then edit its body to the template
   (`projects/.github/PULL_REQUEST_TEMPLATE.md`), asking me for the email for my ClickUp
   invitation and the mentor I am requesting. Show me the PR link.
