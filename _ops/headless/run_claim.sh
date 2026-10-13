#!/bin/bash
# One headless Symphony claim session on Windows: run_claim.sh <issue number>
# Makes a detached worktree of the spine-program clone at C:\Users\grego\spc\<N> on origin/main, runs the VS Code
# extension's claude.exe there with the symphony plugin (user scope) and the claim prompt, logs to claims/<N>.log beside this script.
# gh and python3 come from the wrapper dir (token fetched per call from git's credential manager, never stored).
set -u
N=$1
S=$(cd "$(dirname "$0")" && pwd)
CLONE=/c/Users/grego/OneDrive/Desktop/spine-program
W=/c/Users/grego/spc/$N
CLAUDE=$(ls -d /c/Users/grego/.vscode/extensions/anthropic.claude-code-*-win32-x64/resources/native-binary/claude.exe | sort -V | tail -1)
LOG=$S/claims/$N.log
mkdir -p "$S/claims" /c/Users/grego/spc
export PATH="$S/wrap:$PATH"
cd "$CLONE" || exit 1
git fetch -q origin || wsl -e bash -lc "git -C /mnt/c/Users/grego/OneDrive/Desktop/spine-program fetch -q origin" || { echo "fetch failed" | tee -a "$LOG"; exit 1; }
if [ ! -d "$W" ]; then git worktree add --detach "$W" origin/main >>"$LOG" 2>&1 || { echo "worktree failed" | tee -a "$LOG"; exit 1; }; fi
cd "$W" || exit 1
if [ "${RESUME:-0}" = 1 ]; then FIRST="You already hold the claim on issue #$N: the branch claude/$N is pushed with its claim file docs/agents/claims/$N.md as the first commit, the labels claimed and worker:Gregory-Schwing-MD-PhD are on the issue and the plan is posted; an earlier session stopped at its usage limit. This worktree has claude/$N checked out. git fetch, make sure the branch is up to date with origin/claude/$N, open the draft pull request with Closes #$N if none exists yet (gh pr list --head claude/$N), then do the work and finish exactly as docs/agents/PROTOCOL.md says."; else FIRST="Claim issue #$N with /symphony:claim and carry it to a ready pull request, exactly as docs/agents/PROTOCOL.md says."; fi
read -r -d '' PROMPT <<PEOF
$FIRST Read the issue first (gh issue view $N): its Goal, Acceptance and "Files likely touched" define the whole job; do that and nothing else, and touch no other file. Your worker name is your GitHub login, Gregory-Schwing-MD-PhD (label worker:Gregory-Schwing-MD-PhD; claim file Worker line: Gregory-Schwing-MD-PhD).

Facts about this machine and this repository:
- You are in a detached worktree at origin/main; step 2 of the skill (git switch -c claude/$N origin/main) works from here.
- Network calls to GitHub take about 15 seconds each here; that is normal. Run every gh and git call in the foreground and wait for it to finish; never run one in the background, and never retry a call that merely took long.
- gh and python3 are on PATH. The push guard runs before every Bash call; it refuses what the protocol forbids.
- This repository has no scripts/check.sh and no CI check yet. Before marking the pull request ready, check by hand: the claim file docs/agents/claims/$N.md is deleted in the pull request, the body says "Closes #$N", every acceptance line of the issue is met, and only the files the issue names changed.
- Grid paths come verbatim from the project's MANIFEST_GRID.md; never invent a path, a number or a result. Where the folder does not record a fact, write "not recorded" rather than guess.
- Never use the banned word of the root CLAUDE.md (write origin or lineage). Version numbers are whole integers. Plain prose, no marketing.
- Finish: push, mark the pull request ready (gh pr ready), add the label in-review to the issue (gh issue edit $N --add-label in-review), post one short comment on the pull request saying what was done and what was left as "not recorded". Do not merge, and do not touch main.
${EXTRA:-}
PEOF
{
  echo "==== claim #$N started $(date -Is) in $W"
  "$CLAUDE" -p --model "${MODEL:-claude-opus-5-5}" --dangerously-skip-permissions --output-format text --max-turns "${MAXTURNS:-80}" "$PROMPT" < /dev/null
  echo "==== claim #$N exit $? at $(date -Is)"
} >>"$LOG" 2>&1
tail -3 "$LOG"
