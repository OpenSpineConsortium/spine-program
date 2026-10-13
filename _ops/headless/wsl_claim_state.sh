#!/bin/bash
set -u
export PATH=~/.local/bin:$PATH
tok=$(printf 'protocol=https\nhost=github.com\n' | git credential fill 2>/dev/null | sed -n 's/^password=//p')
export GH_TOKEN="$tok"; unset tok
T=OpenSpineConsortium/spine-program
for n in "$@"; do
  echo "#$n labels: $(gh issue view $n --repo $T --json labels --jq '[.labels[].name] | join(",")') | comments: $(gh issue view $n --repo $T --json comments --jq '.comments | length') | branch: $(gh api repos/$T/branches/claude%2F$n --jq .name 2>/dev/null || echo none) | PR: $(gh pr list --repo $T --head claude/$n --state all --json number,isDraft,state --jq '.[0] | "\(.number) draft=\(.isDraft) \(.state)"' 2>/dev/null)"
done
