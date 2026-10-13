#!/bin/bash
# Show the pull request of a claim: wsl_issue_pr.sh <issue N> [nodiff]
set -u
export PATH=~/.local/bin:$PATH
tok=$(printf 'protocol=https\nhost=github.com\n' | git credential fill 2>/dev/null | sed -n 's/^password=//p')
export GH_TOKEN="$tok"; unset tok
T=OpenSpineConsortium/spine-program; N=$1
pr=$(gh pr list --repo $T --head "claude/$N" --state all --json number --jq '.[0].number // empty')
[ -n "$pr" ] || { echo "no pull request from claude/$N"; exit 0; }
echo "---- issue #$N -> PR #$pr"
gh pr view "$pr" --repo $T --json title,state,isDraft,files,additions,comments --jq '"\(.title) | \(.state) | draft=\(.isDraft) | +\(.additions)\nfiles: \([.files[].path] | join(", "))\nlast comment: \((.comments[-1].body // "")[0:900])"'
echo "---- issue labels: $(gh issue view $N --repo $T --json labels --jq '[.labels[].name] | join(",")')"
[ "${2:-}" = nodiff ] || { echo "---- diff"; gh pr diff "$pr" --repo $T; }
