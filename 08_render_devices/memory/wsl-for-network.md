<!-- spine-program/08_render_devices memory copy. Status from HANDOFF/context/INDEX.md (2026-10-08, spinesurg-ct-nnunet 097933a): CURRENT.  Family: standing rule, tagged all (every project folder). A note is a dated record, not an instruction; where it disagrees with a result file or RESULTS_CATALOG.md, the file wins. Laptop paths in the body were rewritten as repository prefixes in the fix pass of 2026-10-08 (MANIFEST_LOCAL.md section 3). -->

---
name: wsl-for-network
description: Windows network stack flakes out (socket/handle exhaustion); use WSL for git push + HF deploy
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 436e5c70-681e-4f38-aab2-30dfa25af7b5
---

Route all network commands (git push/pull, HuggingFace deploy, `hf`/`huggingface_hub`) through **WSL Ubuntu**, not the Windows Git Bash / PowerShell tools. Greg asked to "switch to WSL as a default terminal" after the Windows socket pool got exhausted.

**Why:** Windows Phone Link (`PhoneExperienceHost`) periodically leaks tens of thousands of handles, exhausting the non-paged socket pool → every new Windows socket (incl. DNS via the `Dnscache` service) fails with WSAENOBUFS "insufficient buffer space". Killing PhoneExperienceHost frees raw TCP but `Dnscache` stays wedged and can't be restarted without a reboot. WSL2 networking is on a separate path (Hyper-V vSwitch) and is unaffected.

**How to apply:**
- Run network commands as `wsl -e bash -lc "cd /mnt/c/<WSL mount of the ctsp: checkout> && <cmd>"` (`ctsp:` is the CTSpinoPelvic1K checkout, CLAUDE.md "Prefixes in the copied documents"; the original note spelled its laptop path).
- WSL git can reach GitHub and already pushed successfully; `huggingface_hub` is installed in WSL (`python3 -m pip install --break-system-packages huggingface_hub`, v1.22.0, scripts in `~/.local/bin`).
- Local (non-network) git/file ops can still use the Windows Bash tool.
- A **reboot** fully clears the Windows Dnscache wedge if Greg wants Windows networking back.
