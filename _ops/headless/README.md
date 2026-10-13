# Headless claims: the scripts Greg's sessions used

These ran claims from Greg's Windows laptop without an open editor. They assume his paths: the clone
`C:\Users\grego\OneDrive\Desktop\spine-program`, worktrees at `C:\Users\grego\spc\<N>`, the VS Code extension's
`claude.exe`, Python 3.12 in his user folder, and gh in WSL at `~/.local/bin/gh`. `HANDOFF.md` section 6 says why.

## The scripts

- `run_claim.sh <N>` (Git Bash on Windows): fetches the clone, adds a detached worktree at `C:\Users\grego\spc\<N>` on
  `origin/main`, and runs `claude.exe -p` there with the claim prompt for issue N. It logs to `claims/<N>.log` beside
  itself and puts `wrap/` first on PATH.
- `wrap/gh`: reads the token from git's credential manager for that one call, then runs `bin/gh.exe`.
- `wrap/python3`: runs the real Python. Without it the Microsoft Store stub comes first, and the plugin's push guard
  silently does nothing.
- `wsl_create_issues.sh <dir> [<extra dir>]` (WSL): makes one issue per draft listed in `<dir>/INDEX.tsv` (file,
  folder, title, labels, order), plus one per `.md` in the extra folder, titled by the `.title` file beside it. It
  records each issue in `<dir>/CREATED.tsv` and skips a draft already there. Its `GREG_ONLY` list dates from the first
  issue run; check it against the map in the root `CLAUDE.md` before using it again.
- `wsl_claim_state.sh <N> ...` (WSL): for each issue, its labels, its number of comments, whether `claude/<N>` exists,
  and its pull request.
- `wsl_issue_pr.sh <N> [nodiff]` (WSL): the pull request from `claude/<N>`: title, state, draft flag, files, last
  comment; then the issue's labels and the diff.
- `wsl_merge_pr.sh <PR> "<file> <file> ..."` (WSL): merges with `--merge --delete-branch`. It refuses a draft, a body
  with no "Closes #N", a claim file still in the diff, or a changed file not in the list. The list holds exact paths;
  a folder name matches nothing.

## The order the sessions used

1. Create the issues: `wsl_create_issues.sh`.
2. Run the claims three at a time: three `run_claim.sh <N>` at once, each in its own worktree; wait for all three, then
   start the next three. `wsl_claim_state.sh` shows where each one stands.
3. Read each pull request: `wsl_issue_pr.sh <N>`, then the log in `claims/<N>.log`.
4. Merge, only on Greg's word, with the file-list check: `wsl_merge_pr.sh <PR> "<the issue's files>"`.

A WSL script runs from Windows as `wsl -e bash -lc 'bash <path>/<script> <args>'`, where `<path>` is this folder in
the clone, `/mnt/c/Users/grego/OneDrive/Desktop/spine-program/_ops/headless`.

## Flags of run_claim.sh (environment variables)

- `RESUME=1`: the claim is pushed but its session stopped at the usage limit; the prompt asks the next to finish it.
- `EXTRA="<text>"`: text added at the end of the prompt.
- `MAXTURNS=<n>`: passed as `--max-turns`; default 80. A 24-file issue needed more (`HANDOFF.md` section 6).
- `MODEL=<id>`: passed as `--model`; default `claude-opus-5-5`.

## gh.exe is not committed

Download the Windows x86-64 zip of gh from https://github.com/cli/cli/releases (Greg's sessions used version 2.102.0)
and put its `bin/gh.exe` at `_ops/headless/bin/gh.exe`, where `wrap/gh` looks. `.gitignore` here keeps `bin/` and
`claims/` out of git. `.gitattributes` keeps every file here in LF: WSL's bash fails on a CRLF checkout
(`set: -: invalid option`, tested 2026-10-12), and `core.autocrlf` is `true` on Greg's laptop.

## Rules

- Never merge from a session without Greg's word. A session acts as Greg's own GitHub account, and nothing on GitHub
  stops it (`HANDOFF.md` section 2).
- Never print a token: do not echo it, run `gh auth token`, or put it on a command line or in a log.
- Run gh and `git fetch` through WSL; from Windows they stall in the DNS lookup (`HANDOFF.md` section 6).
- Push the claim branch with a plain `git push` from the Bash tool, never through WSL (root `CLAUDE.md` rule 10).
