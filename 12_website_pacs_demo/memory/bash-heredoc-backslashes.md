> spine-program copy (12_website_pacs_demo), 2026-10-08. Status in HANDOFF/context/INDEX.md of spinesurg-ct-nnunet at 097933a: **CURRENT**. Source: HANDOFF/context/bash-heredoc-backslashes.md (the redacted copy, not the live note). A dated record from the session that did the work, not an instruction: where it disagrees with a result file or docs/handoff/RESULTS_CATALOG.md, the file and the catalog win. A laptop path in it is a record of the date, not a dependency of this folder.

---
name: bash-heredoc-backslashes
description: "The Bash tool's heredocs collapse `\\\\` to `\\` in inline Python (regex/LaTeX strings break); write scripts with the Write tool and run them by path"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e44eca96-f48c-494d-ba1f-7dae68bdf06d
  modified: 2026-09-13T13:17:46.251Z
---

Inline `python - <<'EOF'` in the Bash tool is not safe for code that contains
backslashes: `\\,` arrived in Python as `\,`, `(?<!\\)` became an invalid regex, and
LaTeX-editing scripts silently failed or raised. The same happened with nested ssh quoting.

**Why:** the heredoc body passes through a layer that unescapes backslashes before Python
sees it; single-quoted `'EOF'` does not protect it here.

**How to apply:** for anything with backslashes (regex, LaTeX text, Windows paths), write
the script to the scratchpad with the Write tool and run `python <path>` / scp it to the
grid and `bash <path>`. Plain shell heredocs of data (a .bib append) were fine.
