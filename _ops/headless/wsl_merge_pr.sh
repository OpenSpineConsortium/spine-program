#!/bin/bash
# Merge a ready pull request as the owner's account after checking it: wsl_merge_pr.sh <PR> "<allowed file 1> [<file 2> ...]"
# Refuses when the PR is a draft, when a changed file is not in the allowed list, or when the claim file is still there.
set -u
export PATH=~/.local/bin:$PATH
tok=$(printf 'protocol=https\nhost=github.com\n' | git credential fill 2>/dev/null | sed -n 's/^password=//p')
export GH_TOKEN="$tok"; unset tok
T=OpenSpineConsortium/spine-program; N=$1; ALLOWED=$2
j=$(gh pr view "$N" --repo $T --json isDraft,state,mergeable,files,body)
draft=$(printf '%s' "$j" | python3 -c 'import json,sys; print(json.load(sys.stdin)["isDraft"])')
state=$(printf '%s' "$j" | python3 -c 'import json,sys; print(json.load(sys.stdin)["state"])')
files=$(printf '%s' "$j" | python3 -c 'import json,sys; print("\n".join(f["path"] for f in json.load(sys.stdin)["files"]))')
closes=$(printf '%s' "$j" | python3 -c 'import json,sys,re; m=re.search(r"Closes #(\d+)", json.load(sys.stdin)["body"]); print(m.group(1) if m else "")')
[ "$state" = OPEN ] || { echo "PR #$N is $state; nothing to do"; exit 0; }
[ "$draft" = False ] || { echo "PR #$N is still a draft; not merged"; exit 1; }
[ -n "$closes" ] || { echo "PR #$N body has no Closes #N; not merged"; exit 1; }
bad=0
while IFS= read -r f; do
  [ -n "$f" ] || continue
  case "$f" in docs/agents/claims/[0-9]*.md) echo "  claim file still in the diff: $f"; bad=1; continue;; esac
  ok=0; for a in $ALLOWED; do [ "$f" = "$a" ] && ok=1; done
  [ $ok -eq 1 ] || { echo "  file outside the issue's list: $f"; bad=1; }
done <<< "$files"
[ $bad -eq 0 ] || { echo "PR #$N not merged (see above)"; exit 1; }
if gh pr merge "$N" --repo $T --merge --delete-branch >/dev/null 2>&1; then echo "MERGED PR #$N (closes #$closes): $(printf '%s' "$files" | tr '\n' ' ')"; else echo "merge of PR #$N FAILED"; exit 1; fi
