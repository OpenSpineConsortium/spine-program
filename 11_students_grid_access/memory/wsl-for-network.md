---
name: wsl-for-network
description: Windows network stack flakes out (socket/handle exhaustion); use WSL for git push + HF deploy
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 436e5c70-681e-4f38-aab2-30dfa25af7b5
---

> **Copy record (11_students_grid_access, 2026-10-08).** Status in `HANDOFF/context/INDEX.md`: CURRENT. Source: HANDOFF/context (redacted copy set) (context/wsl-for-network.md). Redactions by kind: laptop path (1). Laptop paths are replaced by kind with the placeholders [laptop home], [laptop Desktop] and [laptop project slug]; the live reference is the repository at the commit named.  Standing-rule note tagged `all`: every project folder carries it.


Route all network commands (git push/pull, HuggingFace deploy, `hf`/`huggingface_hub`) through **WSL Ubuntu**, not the Windows Git Bash / PowerShell tools. Greg asked to "switch to WSL as a default terminal" after the Windows socket pool got exhausted.

**Why:** Windows Phone Link (`PhoneExperienceHost`) periodically leaks tens of thousands of handles, exhausting the non-paged socket pool → every new Windows socket (incl. DNS via the `Dnscache` service) fails with WSAENOBUFS "insufficient buffer space". Killing PhoneExperienceHost frees raw TCP but `Dnscache` stays wedged and can't be restarted without a reboot. WSL2 networking is on a separate path (Hyper-V vSwitch) and is unaffected.

**How to apply:**
- Run network commands as `wsl -e bash -lc "cd [laptop Desktop]/CTSpinoPelvic1K-1 && <cmd>"`.
- WSL git can reach GitHub and already pushed successfully; `huggingface_hub` is installed in WSL (`python3 -m pip install --break-system-packages huggingface_hub`, v1.22.0, scripts in `~/.local/bin`).
- Local (non-network) git/file ops can still use the Windows Bash tool.
- A **reboot** fully clears the Windows Dnscache wedge if Greg wants Windows networking back.
