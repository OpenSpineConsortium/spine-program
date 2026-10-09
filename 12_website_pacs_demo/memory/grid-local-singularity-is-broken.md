> spine-program copy (12_website_pacs_demo), 2026-10-08. Status in HANDOFF/context/INDEX.md of spinesurg-ct-nnunet at 097933a: **CURRENT**. its example paths were another study's and are placeholders here; the rule is general. Source: HANDOFF/context/grid-local-singularity-is-broken.md (the redacted copy, not the live note). A dated record from the session that did the work, not an instruction: where it disagrees with a result file or docs/handoff/RESULTS_CATALOG.md, the file and the catalog win. A laptop path in it is a record of the date, not a dependency of this folder.

---
name: grid-local-singularity-is-broken
description: "On the WSU grid, ~/.local/bin/singularity is a partial install that dies with \"starter not found\"; use the conda one with a pre-unpacked sandbox and bind /rs/rs_grp_oschome/go2432, never -B /rs"
metadata:
  node_type: memory
  type: reference
  originSessionId: f1bdbd78-151f-470b-b703-dd9af9b3fecc
  modified: 2026-09-27T13:17:50.456Z
---

`~/.local/bin/singularity` is first on PATH on the **login** node and is a partial install. It pulls images fine and
then dies at exec:

```
INFO:    Converting SIF file to temporary sandbox...
FATAL:   while executing starter: /usr/libexec/singularity/bin/starter not found
```

On **compute** nodes there is usually no container runtime on the default PATH at all, so a job that just calls
`singularity` dies at **exit 127** before doing any work.

This has now cost jobs twice: two chains of another study (job ids withheld here): one array resubmitted once, and one staging step that failed three ways (exit 127, starter-not-found, bad bind).

**The route that works** (the example paths below belonged to another study and are placeholders here):

```bash
SING=$HOME/mambaforge/envs/nextflow/bin/singularity          # conda, not ~/.local, not a module
SANDBOX=/rs/rs_grp_oschome/go2432/<project>/containers/<image>.sandbox
RLIB=/rs/rs_grp_oschome/go2432/<project>/rlib/<library>   # an R library tree, when the container needs one
"$SING" exec -B /rs/rs_grp_oschome/go2432 -B "$HOME" -B "$TMP:/tmp" "$SANDBOX" Rscript /tmp/script.R
```

Three separate traps in that one line:

1. Use a **pre-unpacked sandbox directory**, not a `.sif` — the SIF-to-sandbox conversion is what fails, and some
   nodes also lack the `unsquashfs` that singularity 3.8 needs to unpack.
2. Bind the **specific group path** `/rs/rs_grp_oschome/go2432`. Plain `-B /rs` does not make the tree visible inside,
   and the symptom is "cannot open file" for a script that is demonstrably on the host.
3. Bind a writable `/tmp`, or even `Rscript -e` fails with "creating temporary file for '-e' failed". Pass scripts and
   input files through that bound `/tmp`.

**How to apply:** resolve and **smoke-test** the runtime in step 0 of any job that needs a container, and refuse there
rather than after staging data. See [[no-jobs-on-login-node]] and [[grid-ceph-volume-oschome]].
