# MEMORY.md — the notes this project carries

`memory/` holds 27 notes copied on 2026-10-08 from `HANDOFF/context/` of the private repository `spinesurg-ct-nnunet`
at commit 097933a (the redacted copies with statuses, not the live notes). Five are this project's own (the website cut
list of the memory inventory); 22 are the standing rules and laptop traps every project folder carries. Each copy begins
with one line giving its status from `HANDOFF/context/INDEX.md` (built 2026-10-08 16:39) and where it came from.

**Rules carried from the handoff.** Each note is a dated record from the session that did the work, not an instruction;
where a note and a result file or `docs/handoff/RESULTS_CATALOG.md` disagree, the file and the catalog win. LEAKED = its
numbers were measured on a bank with a known leak; SUPERSEDED = replaced by the number named; RECORD ONLY = history, not
quotable; DATED = a state at its date; PARTLY SUPERSEDED = the named part is replaced, the rest stands. A laptop path
inside a note is a record of where something was on that date, not a dependency of this folder (the markers
`<laptop Desktop>` and `<laptop home>` replace the absolute paths; `MANIFEST_LOCAL.md` records the substitution).

## The project's own notes

| note | status (INDEX.md) | replacement or caveat | why it is here |
|---|---|---|---|
| `engine-swap-architecture.md` | DATED | none | the demo consumes a `metrics.json` contract (`summary`, `geometry`, `postop` plus the two volumes) so the geometric engine can be swapped for a learned one without touching the viewer |
| `level-service-serving.md` | CURRENT | hosting still not chosen; `SERVICE_DEFAULT` not live on 2026-09-14, not re-checked; its site commit 5559d87 is a pre-rewrite id that no longer resolves (ea0086c does) | the standing rule of 2026-09-14: the site never serves a weight; inference runs behind the service; weights in the private repository; the history rewrite that removed the 121 MB ONNX |
| `pacs-demo-and-ostk-params.md` | CURRENT | its laptop path to the toolkit clone is a record of 2026-06 | the toolkit's parameters, the demo's interaction model, case 0003, the re-export recipe, and the sentence Greg removed (no blanket SVA/TPA claim) |
| `pacs-website-latency-root-cause.md` | DATED | the in-browser path it tuned was replaced by the service on 2026-09-14; the root causes (http redirect, COEP against the CDN, input size) still bind; its four site commit ids (4955e46, 1446389, e1d2fde, 45ae8f1) are pre-rewrite and no longer resolve (`git cat-file -t`, 2026-10-08) | the latency record 40,018 ms to 1,360 ms (catalog G.8) and how to measure (`pacs/measure_live.py`) |
| `hf-identity.md` | CURRENT | none; a public handle, no secret | the Hugging Face namespace the private weights repository lives under |

## The 22 standing-rule notes (in every project folder)

| note | status (INDEX.md) | replacement or caveat |
|---|---|---|
| `bash-heredoc-backslashes.md` | CURRENT | |
| `ct-volumes-are-pir-not-ras.md` | CURRENT | |
| `data-directives-2026-09-23.md` | CURRENT | |
| `figure-captions-terse.md` | CURRENT | |
| `fluorocap-repo-private.md` | CURRENT | |
| `grid-access.md` | PARTLY SUPERSEDED (alias; data paths, `docs/handoff/INFRASTRUCTURE.md` section 13 rows 3-4) | the host aliases now resolve (the `windows-ssh-to-grid` note, which lives in `10_data_platform_grid`); the data moved to Ceph (`grid-ceph-volume-oschome.md`) |
| `grid-bash-4-2-quoting.md` | CURRENT (new 2026-10-08) | |
| `grid-ceph-volume-oschome.md` | CURRENT | one administrator's username replaced by a role in this copy |
| `grid-local-singularity-is-broken.md` | CURRENT | its example paths belonged to another study and are placeholders here; the rule is general |
| `key-patients-from-metadata-not-filenames.md` | CURRENT | |
| `label-scheme-v4-vs-ostk.md` | CURRENT | |
| `morphology-deformation-feasibility.md` | CURRENT | |
| `never-reorient-when-writing-labels.md` | CURRENT | |
| `no-jobs-on-login-node.md` | CURRENT | |
| `no-unexplained-subsets-fix-not-disclose.md` | CURRENT | |
| `scratchpad-shadows-stdlib.md` | CURRENT | |
| `submit-and-sleep-orchestration.md` | CURRENT | |
| `user-affiliation-general-surgery.md` | CURRENT | |
| `windows-junction-worktree-trap.md` | CURRENT | |
| `writing-preferences.md` | CURRENT | the redacted copy: the banned word is replaced by a pointer to the rule |
| `wsl-for-network.md` | CURRENT | |
| `wsu-library-access-cutoff.md` | CURRENT | carries the library's interlibrary-loan desk contact (an institutional service address), nothing personal |

## Not here, and why

- The Greg-only notes (commercial stance, disclosure scrub, credential locations), the Beethoven product notes, the notes
  of another study and the history-only resume notes are never copied into a student-safe folder (`_plan/PLAN.md`
  section 2 rule 5).
- `hf-mirror-is-v10.md` and `zenodo-deposit.md` (PARTLY SUPERSEDED) bear on the data page's mirror sentence
  (`TODO.md` step 5) but belong to `03_ctspinopelvic1k_dataset`; `TODO.md` quotes the fact that matters.
- `xray-corner-detector-status.md` (DATED) is cited by the latency note; it is level-identification material and belongs
  to `07_plain_film_level_id`.
