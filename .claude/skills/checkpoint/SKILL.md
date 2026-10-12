---
name: checkpoint
description: Use at the end of a session, or before handing work to another account or session, to record where things stand as one comment on the claim's pull request.
---

# Write a checkpoint

A checkpoint is what the next session reads first: where one claim's work stands, posted as one comment on that claim's pull request. It is a comment and not a file, so two claims working in parallel never edit the same file, and it commits nothing. N stands for the issue's number, and the claim's pull request is the one opened from `claude/N`.

1. Collect from the conversation: what was completed, where things stand now (the branch, the pull request, what is pushed and what is not), what remains, and every line tagged `Decision:` or `Constraint:`, word for word.
2. Write the comment to a scratch file outside the repository, `checkpoint.md`, with these sections, in this order: `## Session checkpoint`, `### Completed work`, `### Current state`, `### Remaining tasks`, `### Decisions`, `### Constraints`, each with its items or `- (none recorded)`. Decisions and constraints from earlier checkpoint comments on the same pull request stay unless a later one reverses them, so the newest comment is whole on its own. Plain prose and short lists; under 16 KB; no secrets, no tokens, no tool output, no logs. Say plainly what is not known rather than guessing.
3. Post it as one comment on the claim's pull request: `gh pr comment claude/N --body-file checkpoint.md`. Where gh pr is refused, as in a cloud session, use the session's GitHub tools, or `gh api repos/OpenSpineConsortium/spine-program/issues/P/comments -F body=@checkpoint.md`, with P the pull request's number (a pull request's comments go through the issues endpoint). A claim with no pull request yet opens its draft first (the claim skill, step 7).
4. Write nothing into the repository for it: no `.claude/session.md`, no block in CLAUDE.md.

What belongs here and not in docs/memory/: the state of one piece of work. A fact that holds for the project as a whole is a memory (the remember skill, `/remember`).
