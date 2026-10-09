# MANIFEST_LOCAL.md: every file copied into this folder, and what was not

Built 2026-10-08. **The source paths below are history, not a dependency.** They say where each copy was taken
from on the laptop (or on the grid) at build time so the copy can be audited; nothing in this folder reads them.
Laptop paths appear in this file only. The live versions of anything that lives in a repository are at the
commits in `MANIFEST_CODE.md`; grid paths are spelled in full and are current as of the dates in `MANIFEST_GRID.md`.
Hashes are sha256 of the written file (first 16 hex digits; the full value is in the build's copy log). "Source
bytes" is the file as found; "written bytes" includes any header or redaction described in "what was done".

Copy rules applied (`../_plan/PLAN.md` section 2 rule 6): no imaging data, weights, `.git`, environments,
caches, logs over 2 MB, files over 25 MB, credentials, personal or administrative material, student names or
usernames, researcher or personal e-mail addresses. The largest file copied is 3,438,335 B; the largest source
file considered and not copied is 4,893,904 B (for its content, not its size); no source for this project
exceeded 25 MB, so nothing is referenced by path for size.


**Totals: 68 files written by copy, 6,997,090 bytes** (recounted 2026-10-08 after the marker substitutions of section 2). The documents written by the builder (`CLAUDE.md`, `README.md`, `MEMORY.md`, `MANIFEST_*.md`, `STATUS.md`, `TODO.md`, the sub-folder READMEs and `docs/handoff/ABOUT.md`) are not copies and are not listed below.


## 1. Copied


### Figure panels of May 2026 (verbatim)

| written to | taken from | source date | source bytes | written bytes | sha256 (written) | what was done |
|---|---|---|---|---|---|---|
| `figures/student_panels_2026-05/Cobb.png` | `C:/Users/grego/OneDrive/Desktop/NextPaper/old/Cobb.png` | 2026-05-18 09:25 | 1,432,763 | 1,432,763 | `f8c4766af20df135` | verbatim |
| `figures/student_panels_2026-05/Figure1_OSC_measurement_panels.png` | `C:/Users/grego/OneDrive/Desktop/NextPaper/old/Figure1_OSC_measurement_panels.png` | 2026-05-18 09:33 | 3,438,335 | 3,438,335 | `bf5df53b9db4b503` | verbatim |
| `figures/student_panels_2026-05/LDI.png` | `C:/Users/grego/OneDrive/Desktop/NextPaper/old/LDI.png` | 2026-05-18 09:26 | 91,420 | 91,420 | `9c52705460ef6752` | verbatim |
| `figures/student_panels_2026-05/TRALL.png` | `C:/Users/grego/OneDrive/Desktop/NextPaper/old/TRALL.png` | 2026-05-18 09:25 | 700,964 | 700,964 | `8ef4c81539ddec69` | verbatim |
| `figures/student_panels_2026-05/Tortuosity.jpg` | `C:/Users/grego/OneDrive/Desktop/NextPaper/old/Tortuosity.jpg` | 2026-05-18 09:28 | 113,588 | 113,588 | `3d4280855373603e` | verbatim |
| `figures/student_panels_2026-05/VWI.png` | `C:/Users/grego/OneDrive/Desktop/NextPaper/old/VWI.png` | 2026-05-18 09:29 | 381,306 | 381,306 | `cb608ecebe81a8ff` | verbatim |

### Pre-ostk scripts of 2026-05-17 (a header prepended; body verbatim)

| written to | taken from | source date | source bytes | written bytes | sha256 (written) | what was done |
|---|---|---|---|---|---|---|
| `code/pre_ostk_2026-05/spine_analysis_v316.py` | `C:/Users/grego/OneDrive/Desktop/NextPaper/spine_analysis_v316.py` | 2026-05-17 16:07 | 78,753 | 79,255 | `c35bfd462cb00f36` | header prepended (no laptop path in it); body verbatim |
| `code/pre_ostk_2026-05/spine_analysis_v317.py` | `C:/Users/grego/OneDrive/Desktop/NextPaper/spine_analysis_v317.py` | 2026-05-17 16:14 | 80,348 | 80,850 | `e15ee2bf5addec4b` | header prepended (no laptop path in it); body verbatim |
| `code/pre_ostk_2026-05/test.py` | `C:/Users/grego/OneDrive/Desktop/NextPaper/test.py` | 2026-05-17 21:56 | 14,650 | 15,152 | `44e3be5e73cf0f83` | header prepended (no laptop path in it); body verbatim |
| `code/pre_ostk_2026-05/test_v2.py` | `C:/Users/grego/OneDrive/Desktop/NextPaper/test_v2.py` | 2026-05-17 22:11 | 25,723 | 26,225 | `02311a1b4b43ae8e` | header prepended (no laptop path in it); body verbatim |
| `code/pre_ostk_2026-05/test_v3.py` | `C:/Users/grego/OneDrive/Desktop/NextPaper/test_v3.py` | 2026-05-17 22:22 | 29,540 | 30,042 | `f868aec019aeb176` | header prepended (no laptop path in it); body verbatim |
| `code/pre_ostk_2026-05/vertebral_corners.py` | `C:/Users/grego/OneDrive/Desktop/NextPaper/vertebral_corners.py` | 2026-05-17 15:57 | 22,028 | 22,530 | `e5dfb00e710223ad` | header prepended (no laptop path in it); body verbatim |

### The BIBM draft of 2026-06-28 (one redaction)

| written to | taken from | source date | source bytes | written bytes | sha256 (written) | what was done |
|---|---|---|---|---|---|---|
| `manuscripts/bibm_spinopelvic/README.md` | `C:/Users/grego/OneDrive/Desktop/NextPaper/bibm-spinopelvic/README.md` | 2026-06-28 18:24 | 1,835 | 1,835 | `deef23930b6737e6` | verbatim |
| `manuscripts/bibm_spinopelvic/main.tex` | `C:/Users/grego/OneDrive/Desktop/NextPaper/bibm-spinopelvic/main.tex` | 2026-06-28 18:23 | 17,059 | 17,082 | `1ef372a21fb3d148` | line 24: the personal e-mail address replaced by a bracketed note; everything else verbatim |
| `manuscripts/bibm_spinopelvic/tools/cohort_stats.py` | `C:/Users/grego/OneDrive/Desktop/NextPaper/bibm-spinopelvic/tools/cohort_stats.py` | 2026-06-28 18:23 | 2,958 | 2,958 | `0ea878dcdc00809f` | verbatim |

### Memory notes (the handoff's redacted context copies; a status line prepended)

| written to | taken from | source date | source bytes | written bytes | sha256 (written) | what was done |
|---|---|---|---|---|---|---|
| `memory/bash-heredoc-backslashes.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/bash-heredoc-backslashes.md` | 2026-10-08 16:39 | 1,009 | 1,487 | `77ca9f9b4fd3d2fb` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/commit-directly-to-master.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/commit-directly-to-master.md` | 2026-10-08 16:39 | 829 | 1,277 | `f65577a057236738` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/ct-volumes-are-pir-not-ras.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/ct-volumes-are-pir-not-ras.md` | 2026-10-08 16:39 | 2,001 | 2,468 | `2fda3c54c16be567` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/data-directives-2026-09-23.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/data-directives-2026-09-23.md` | 2026-10-08 16:39 | 2,133 | 2,613 | `ae4feeecb2ea66eb` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/engine-swap-architecture.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/engine-swap-architecture.md` | 2026-10-08 16:39 | 1,670 | 2,115 | `8d8cee5b55f175f0` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/figure-captions-terse.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/figure-captions-terse.md` | 2026-10-08 16:39 | 1,277 | 1,752 | `a93e927eb113ef78` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/fluorocap-repo-private.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/fluorocap-repo-private.md` | 2026-10-08 16:39 | 1,422 | 1,898 | `cacc9cb87c3aba3f` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/grid-access.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-access.md` | 2026-10-08 16:39 | 1,342 | 1,873 | `8bb009fddfc6eab5` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/grid-bash-4-2-quoting.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-bash-4-2-quoting.md` | 2026-10-08 16:39 | 1,380 | 1,872 | `70ee8f6ea97b369c` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/grid-ceph-volume-oschome.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-ceph-volume-oschome.md` | 2026-10-08 16:39 | 1,283 | 1,761 | `3bbb7c52570779e1` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/grid-local-singularity-is-broken.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-local-singularity-is-broken.md` | 2026-10-08 16:39 | 2,368 | 2,854 | `b9fb8017efc8b629` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/key-patients-from-metadata-not-filenames.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/key-patients-from-metadata-not-filenames.md` | 2026-10-08 16:39 | 2,159 | 2,653 | `ff895c564b23d2c6` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/label-scheme-v4-vs-ostk.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/label-scheme-v4-vs-ostk.md` | 2026-10-08 16:39 | 2,423 | 2,887 | `204059ae4caf6ad7` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/morphology-deformation-feasibility.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/morphology-deformation-feasibility.md` | 2026-10-08 16:39 | 2,267 | 2,755 | `8c783d4da06701bb` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/never-reorient-when-writing-labels.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/never-reorient-when-writing-labels.md` | 2026-10-08 16:39 | 1,892 | 2,367 | `1e7f353a6b4ff606` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/no-jobs-on-login-node.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/no-jobs-on-login-node.md` | 2026-10-08 16:39 | 2,148 | 2,623 | `96ee45f9cdf84812` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/no-unexplained-subsets-fix-not-disclose.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/no-unexplained-subsets-fix-not-disclose.md` | 2026-10-08 16:39 | 2,097 | 2,590 | `8363ffb63fd1f9fb` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/ostk-canal-closing-regression.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/ostk-canal-closing-regression.md` | 2026-10-08 16:39 | 2,323 | 2,782 | `9bbe2dc4a0ffaf1d` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/pacs-demo-and-ostk-params.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/pacs-demo-and-ostk-params.md` | 2026-10-08 16:39 | 2,005 | 2,438 | `8c771cd7c7affe0b` | status line prepended; body = the HANDOFF/context copy with 1 absolute laptop path replaced by `<laptop Desktop>` (line 14; section 2); copy-time sha256 `ef3ccbb00cd7d333` |
| `memory/postop-jaggedness-future.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/postop-jaggedness-future.md` | 2026-10-08 16:39 | 1,333 | 1,778 | `16c63de65df149da` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/postop-spine-synthesis.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/postop-spine-synthesis.md` | 2026-10-08 16:39 | 2,961 | 3,404 | `225391cb0c71ec9e` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/scratchpad-shadows-stdlib.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/scratchpad-shadows-stdlib.md` | 2026-10-08 16:39 | 1,364 | 1,843 | `05ae9b535e44328f` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/submit-and-sleep-orchestration.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/submit-and-sleep-orchestration.md` | 2026-10-08 16:39 | 1,888 | 2,372 | `ebd3c5123a9db93a` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/user-affiliation-general-surgery.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/user-affiliation-general-surgery.md` | 2026-10-08 16:39 | 1,516 | 2,002 | `718e0cb5cffe9921` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/windows-junction-worktree-trap.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/windows-junction-worktree-trap.md` | 2026-10-08 16:39 | 1,490 | 1,958 | `4af542fe73c79bce` | status line prepended; body = the HANDOFF/context copy with 2 absolute laptop paths replaced (`<laptop Desktop>` line 16, `<laptop home>` line 26; section 2); copy-time sha256 `35d42e52998771ae` |
| `memory/writing-preferences.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/writing-preferences.md` | 2026-10-08 16:39 | 788 | 1,261 | `9e82bd58b3c438db` | status line prepended; body = the HANDOFF/context copy verbatim |
| `memory/wsl-for-network.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/wsl-for-network.md` | 2026-10-08 16:39 | 1,439 | 1,896 | `ed31b33368ae13f0` | status line prepended; body = the HANDOFF/context copy with 1 absolute laptop path replaced by `/mnt/c/<laptop Desktop>/...` (line 17; section 2); copy-time sha256 `f011fc842169aeb5` |
| `memory/wsu-library-access-cutoff.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/wsu-library-access-cutoff.md` | 2026-10-08 16:39 | 1,478 | 2,053 | `93c51e7982771211` | status line prepended; body = the HANDOFF/context copy verbatim except the library contact (redacted) |

### The eight student-readable handoff files (three verbatim; five with absolute laptop paths replaced by markers, section 2)

| written to | taken from | source date | source bytes | written bytes | sha256 (written) | what was done |
|---|---|---|---|---|---|---|
| `docs/handoff/DATASET_USAGE.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/DATASET_USAGE.md` | 2026-10-08 16:35 | 37,254 | 37,254 | `8a3e0de6e956b142` | verbatim |
| `docs/handoff/GLOSSARY.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/GLOSSARY.md` | 2026-10-08 16:20 | 25,368 | 25,368 | `a01539499ebb2e0a` | verbatim |
| `docs/handoff/INFRASTRUCTURE.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/INFRASTRUCTURE.md` | 2026-10-08 16:31 | 48,550 | 48,536 | `492fab772c43f5a9` | 3 absolute laptop paths replaced by markers (lines 5, 114, 380); otherwise verbatim; source sha256 `fd90e68d8c16ab09` |
| `docs/handoff/LEAKAGE.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/LEAKAGE.md` | 2026-10-08 16:06 | 25,299 | 25,299 | `121631d92d5463a8` | verbatim |
| `docs/handoff/OPEN_QUESTIONS.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/OPEN_QUESTIONS.md` | 2026-10-08 16:35 | 28,532 | 28,544 | `0c75c84af5a1b882` | row A1 (line 21): three phrases that named a CV through its application system and folder generalised (section 2); otherwise verbatim; source sha256 `51c87379d06ae779` |
| `docs/handoff/README.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/README.md` | 2026-10-08 16:36 | 42,567 | 42,414 | `b2f8fe3a921af302` | 8 absolute laptop paths replaced by markers (lines 34, 36-38, 40-42, 241); the private-folder row (line 153) and one CV phrase (line 281) generalised (section 2); otherwise verbatim; source sha256 `9db77ff0bea0fe4b` |
| `docs/handoff/RECIPES.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/RECIPES.md` | 2026-10-08 16:35 | 73,585 | 73,583 | `0d92ac0c1d4ece1b` | 2 absolute laptop paths replaced by markers (lines 29, 77); the laptop-only list (lines 75-76) generalised (section 2); otherwise verbatim; source sha256 `e611bed3135db715` |
| `docs/handoff/RESULTS_CATALOG.md` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/RESULTS_CATALOG.md` | 2026-10-08 16:20 | 110,438 | 110,286 | `7fcd5e61fc4be208` | 4 absolute laptop paths replaced by markers (lines 12-14, 637); otherwise verbatim; source sha256 `7fcb5ab36518fc98` |

### The 0097 reference rows (an extract)

| written to | taken from | source date | source bytes | written bytes | sha256 (written) | what was done |
|---|---|---|---|---|---|---|
| `results/ostk_level_morphometry_0097_reference_90a27a7.csv` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/morphometrics/ostk_level_morphometry.csv` | 2026-09-11 09:06 | 298,249 | 455 | `0409485400db820e` | EXTRACT: header + the six case-0097 rows of the 4,744-row file at CTSpinoPelvic1K commit 90a27a7 (the whole file goes to 05_ct_morphometry_parity) |

### Grid-only scripts of the 2026-09-10 run (read with cat; a header prepended)

| written to | taken from | source date | source bytes | written bytes | sha256 (written) | what was done |
|---|---|---|---|---|---|---|
| `code/grid_ostk_run_2026-09-10/ostk_extract.py` | `grid:/wsu/home/go/go24/go2432/ostk_run/ostk_extract.py` | 2026-09-10 03:41 | 2,751 | 3,220 | `9e5b25b3379fac27` | read from the grid with cat (read-only) 2026-10-09 00:12 UTC; header prepended |
| `code/grid_ostk_run_2026-09-10/ostk_morph.py` | `grid:/wsu/home/go/go24/go2432/ostk_run/ostk_morph.py` | 2026-09-10 03:01 | 4,775 | 5,242 | `a87fbd66b4c567ab` | read from the grid with cat (read-only) 2026-10-09 00:12 UTC; header prepended |
| `code/grid_ostk_run_2026-09-10/pdw_why.py` | `grid:/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/pdw_why.py` | 2026-09-10 16:00 | 1,761 | 2,276 | `5c6bf0baaae3a417` | read from the grid with cat (read-only) 2026-10-09 00:12 UTC; header prepended |
| `code/grid_ostk_run_2026-09-10/ped_batch.py` | `grid:/wsu/home/go/go24/go2432/ostk_run/ped_batch.py` | 2026-09-10 06:02 | 2,228 | 2,694 | `f7ab5a4be3802db1` | read from the grid with cat (read-only) 2026-10-09 00:12 UTC; header prepended |
| `code/grid_ostk_run_2026-09-10/pedicle_dev.py` | `grid:/wsu/home/go/go24/go2432/ostk_run/pedicle_dev.py` | 2026-09-10 05:59 | 10,796 | 11,392 | `f16d70e3e677786f` | read from the grid with cat (read-only) 2026-10-09 00:12 UTC; header prepended |

### Grid-only records of the 2026-09-10 run (read with cat; text verbatim, the four CSVs CRLF on the grid and LF here) and the listing

| written to | taken from | source date | source bytes | written bytes | sha256 (written) | what was done |
|---|---|---|---|---|---|---|
| `results/grid_run_2026-09-10/grid_listing_2026-10-09T0012Z.txt` | `grid: ls/stat output of 2026-10-09 00:12 UTC` | 2026-10-09 00:12 UTC | 10,156 | 10,156 | `946b33762f10f18f` | written by the builder from the ssh output |
| `results/grid_run_2026-09-10/logs_ostkext_40183713_0.err` | `grid:/wsu/home/go/go24/go2432/logs_ostkext_40183713_0.err` | 2026-09-10 | 81 | 81 | `551b7230e07fa941` | read from the grid with cat (read-only) 2026-10-09 00:12 UTC; verbatim |
| `results/grid_run_2026-09-10/logs_ostkext_40183713_0.out` | `grid:/wsu/home/go/go24/go2432/logs_ostkext_40183713_0.out` | 2026-09-10 | 23 | 23 | `f8d34ce6943647d9` | read from the grid with cat (read-only) 2026-10-09 00:12 UTC; verbatim |
| `results/grid_run_2026-09-10/logs_ostkmorph_40183643.out` | `grid:/wsu/home/go/go24/go2432/logs_ostkmorph_40183643.out` | 2026-09-10 03:17 | 11,438 | 11,438 | `f46b6fcfd0268c94` | read from the grid with cat (read-only) 2026-10-09 00:12 UTC; verbatim |
| `results/grid_run_2026-09-10/logs_ostkmorph_40183680.err` | `grid:/wsu/home/go/go24/go2432/logs_ostkmorph_40183680.err` | 2026-09-10 | 81 | 81 | `3ee4bff90511c2fa` | read from the grid with cat (read-only) 2026-10-09 00:12 UTC; verbatim |
| `results/grid_run_2026-09-10/logs_pedbatch_40183964.out` | `grid:/wsu/home/go/go24/go2432/logs_pedbatch_40183964.out` | 2026-09-10 | 601 | 601 | `e1478d902657e0b8` | read from the grid with cat (read-only) 2026-10-09 00:12 UTC; verbatim |
| `results/grid_run_2026-09-10/logs_peddev_40183959.out` | `grid:/wsu/home/go/go24/go2432/logs_peddev_40183959.out` | 2026-09-10 | 602 | 602 | `d1e6b3866952aad0` | read from the grid with cat (read-only) 2026-10-09 00:12 UTC; verbatim |
| `results/grid_run_2026-09-10/ostk_morph_out_shard_0.csv` | `grid:/wsu/home/go/go24/go2432/ostk_morph_out/shard_0.csv` | 2026-09-10 05:10 | 12,764 (grid `ls`, CRLF) | 12,563 (LF) | `45666374a433326e` | read from the grid with cat (read-only) 2026-10-09 00:12 UTC; CRLF on the grid, LF as written (201 lines, one byte per line fewer); text verbatim |
| `results/grid_run_2026-09-10/ostk_shards_mout_morph_6.csv` | `grid:/wsu/home/go/go24/go2432/ostk_shards/mout/morph_6.csv` | 2026-09-10 13:18 | 40,724 (grid `ls`, CRLF) | 40,623 (LF) | `993cb8018782d767` | read from the grid with cat (read-only) 2026-10-09 00:12 UTC; CRLF on the grid, LF as written (101 lines); text verbatim |
| `results/grid_run_2026-09-10/ostk_shards_out_spinopelvic_0.csv` | `grid:/wsu/home/go/go24/go2432/ostk_shards/out/spinopelvic_0.csv` | 2026-09-10 13:24 | 7,873 (grid `ls`, CRLF) | 7,771 (LF) | `2126043f92cbee28` | read from the grid with cat (read-only) 2026-10-09 00:12 UTC; CRLF on the grid, LF as written (102 lines); text verbatim |
| `results/grid_run_2026-09-10/pi_ostk2.csv` | `grid:/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/pi_ostk2.csv` | 2026-09-10 11:46 | 662 (grid `ls`, CRLF) | 651 (LF) | `d73896296dc2cccb` | read from the grid with cat (read-only) 2026-10-09 00:12 UTC; CRLF on the grid, LF as written (11 lines); text verbatim |

Notes on the groups.

- **Memory notes** were copied from `HANDOFF/context/` (the redacted copies with statuses), not from the live memory
  folder `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/`, as the plan
  requires. On 2026-10-08, 26 of the 28 context copies were byte-identical to their live notes; `writing-preferences`
  differs because the context copy does not spell the banned word, and `label-scheme-v4-vs-ostk` differs in one
  renamed link. The status line prepended to each copy carries the `HANDOFF/context/INDEX.md` status verbatim. Three notes had
  four absolute laptop paths replaced by markers (section 2).
- **Handoff files**: three were copied byte for byte; in five the absolute laptop paths were replaced by markers and
  four phrases were generalised (section 2), so this file is the only one in the folder that spells a laptop path.
  `docs/handoff/ABOUT.md` is the builder's index, not a copy; the prefix tables resolve through `MANIFEST_CODE.md`.
- **Grid files** were read on 2026-10-09 00:12 UTC with `cat` over ssh (login node; read-only; nothing written) and
  the text hashed on the laptop. The four CSVs are CRLF on the grid (their `ls` sizes exceed the written files by
  exactly their line counts: 201, 101, 102 and 11) and were written LF; the log files' sizes equal their `ls` sizes.
  The "source date" is the grid `ls` date (-0400).
- **Code headers** name the working folder or the grid path, the date and (grid files) the hash, never a laptop drive path.


## 2. Redactions made on copy

| file | what was changed | why |
|---|---|---|
| `manuscripts/bibm_spinopelvic/main.tex` line 24 | the correspondence e-mail replaced by "[personal e-mail struck on copy, 2026-10-08]" | Greg's personal address (plan rule 7) |
| `memory/wsu-library-access-cutoff.md` line 24 (now line 26 after the status line) | a library staff e-mail and two phone numbers replaced by "[library contact withheld on copy]" and "[phone withheld]" | a named staff contact; the rest of the note (what the library dropped and when) is intact |
| `docs/handoff/README.md` lines 34, 36-38, 40-42 and 241 | 8 absolute laptop paths replaced: six Desktop-clone prefixes by `<laptop Desktop>/`, the live memory folder by `<laptop memory folder>/`, the vendor folder by `<laptop vendor folder, never read>` | self-containment: no text outside this file names a laptop path; the markers are those of `12_website_pacs_demo` so the folders agree |
| `docs/handoff/RESULTS_CATALOG.md` lines 12-14 and 637 | 3 prefix definitions by `<laptop Desktop>/`; the Temp scratchpad path of row F.48 by `<laptop Temp scratchpad, swept>/neurips_fixes/cr_apply/` | same |
| `docs/handoff/INFRASTRUCTURE.md` lines 5, 114 and 380 | the Beethoven clone by `<laptop Desktop>/ashley-bridge`, the vendor folder by the vendor marker, the portable Node path by `<laptop home>\tools\node22` | same |
| `docs/handoff/RECIPES.md` lines 29 and 77 | the WSL mount path by `/mnt/c/<laptop Desktop>/spinesurg-ct-nnunet`; the Desktop root by `<laptop Desktop>` | same |
| `docs/handoff/OPEN_QUESTIONS.md` row A1 (line 21); `docs/handoff/README.md` lines 153 and 281; `docs/handoff/RECIPES.md` lines 75-76 | a CV cited through its application system and folder now reads "a CV" and, in A1's file column, "a CV in an application folder (laptop only, never copied)"; the private-records folder of README section 4 now reads "a laptop-only private folder (never copied)"; RECIPES' laptop-only list now reads "two personal folders that stay on the laptop and were never copied" | application material and the private folder are excluded from this seed by name (plan section 2 rule 6), so a student-safe folder does not name them. Rows E10 and F2 of `OPEN_QUESTIONS.md` and README line 284 use "scratchpad" as a noun with no path and are unchanged, as in `12_website_pacs_demo` |
| `memory/pacs-demo-and-ostk-params.md` line 14; `memory/windows-junction-worktree-trap.md` lines 16 and 26; `memory/wsl-for-network.md` line 17 | four absolute laptop paths replaced by `<laptop Desktop>` (three) and `<laptop home>` (one) | self-containment; `MEMORY.md` records it |

No other copied file was altered beyond the prepended header or status line described in section 1. The texts,
numbers and ids of the eight handoff copies are the originals'; the section-1 rows give both the hash as written here
and the source hash at 097933a. The two
institutional service addresses inside the handoff copies (the HPC help desk and the IRB office) were left: they
are offices, not people.


## 3. Valuable material NOT copied, and why

| item | where it is | why not copied |
|---|---|---|
| The OpenSpineToolkit repository (54 `.py`, 19 `.md`, tests, projects, tools, `SPEC.md`) | GitHub, `main` cb43197 (`MANIFEST_CODE.md`) | lives in a repository; referenced by commit; copying code that is in a repo is the thing this folder avoids |
| `C:/Users/grego/OneDrive/Desktop/OpenSpineToolkit/_v.txt` (tracked) | the repository | a UTF-16 scratch readout of one case's PI/SS/PT/LL; no value beyond the repo (inventory row inv3 r3) |
| `OpenSpineToolkit/build/`, `openspinetoolkit.egg-info/`, `ostk/__pycache__/`, `.pytest_cache/` | laptop clone | build artefacts and caches (`../_plan/EXCLUDED.md`) |
| `C:/Users/grego/OneDrive/Desktop/NextPaper/old/OpenSpineConsortium Participation Survey .csv` (10,384 B, 2026-05-18) | laptop only | names and demographics of students; the site README forbids committing it (plan rule 6; `EXCLUDED.md`) |
| `C:/Users/grego/OneDrive/Desktop/NextPaper/old/2026 CNS Abstract Submission Portal - Congress of Neurological Surgeons (CNS).pdf` (4,893,904 B, 2026-05-18; the inventory recorded it as 11 MB) | laptop only | the disposition row allowed it, but its text (3 pages, read with pypdf on 2026-10-08) carries fifteen co-author `wayne.edu` addresses, which are student usernames, plus the submitter's: student usernames and researcher addresses are never copied. It is the abstract-portal printout of the May 2026 medical-education abstract ("Beyond the Cadaver Lab: the OpenSpineConsortium as an asynchronous, open-source framework for medical student engagement"), whose record belongs to `11_students_grid_access` (handoff `MANUSCRIPTS.md` section 12) |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/morphometrics/ostk_level_morphometry.csv` (298,249 B on the laptop, LF, 4,745 lines = header + 4,744 rows; the Ceph original is 302,994 B with CRLF) | the repository at 90a27a7 and 7ddfe38; `05_ct_morphometry_parity/results/morphometrics/` | copied whole into 05 (plan rule 2: nothing copied twice); the six 0097 rows are extracted here |
| `CTSpinoPelvic1K-1/docs/{SPINOPELVIC_ESTIMATOR,OSTK_VS_EXTRACTION,LEVEL_MORPHOMETRY,BODY_HEIGHT_INVESTIGATION}.md`; `morphometrics/{level_references,pedicle_width_references}.csv`; `scripts/extract_surgical_morphometrics.py`; `scripts/label_scheme.py` | the repository (7ddfe38); copies in 03 and 05 | plan rule 2(d) names 03 and 05 as their two homes; this folder cites them by repository and line |
| `spinesurg-ct-nnunet/SchwingNet/results/reader_e/diag/` (7 files, 3.2 MB: `0097_v11_diag.json`, `0097_v11_k2_T11_corners.png`, `k3_T12`, `k6_L3`, `k7_L4` ...) | the private repository (097933a); `05_ct_morphometry_parity/results/reader_e/diag/` | the renders that found the regression; routed to 05 by the disposition; referenced from `STATUS.md` G.2 |
| `spinesurg-ct-nnunet/SchwingNet/results/reader_e/J3_NOT_SUBMITTED.md`; `SchwingNet/tools/reader_e_features.py` | the private repository; 05 | the 15.8 % and 5.2 % numbers are quoted with line numbers in `TODO.md` and `STATUS.md` |
| `HANDOFF/RESEARCH_DIRECTIONS.md`, `MANUSCRIPTS.md`, `CONTEXT_EXPORT.md`, `LITERATURE_STATE.md`, `literature_state/`, `working_notes/`, `GREG_ONLY/` | the private repository (097933a) | Greg-only handoff files; this folder is student-safe, so only extracts with ids are carried (`TODO.md`, `STATUS.md`; plan rule 3) |
| Memory notes `scheme-bone-hardware-only`, `s1-carve-changed-spinopelvic`, `panjabi-1991-page-892`, `push-both-github-remotes`, `hf-mirror-is-v10`, `zenodo-deposit`, `pacs-website-latency-root-cause`, `level-service-serving` | `HANDOFF/context/`; copied into 03, 05 or 12 per the cut lists | not on this folder's cut list; the facts this project needs from them are in `CLAUDE.md` and `MEMORY.md` |
| The live `MEMORY.md` index and the five Greg-only, seven U251/LITT and six history-only notes | the live memory folder; `GREG_ONLY/` | never copied into any project folder (plan rule 5) |
| `CTSpinoPelvic1K-1/CLAUDE.md` | the repository | the project's standing context; its rules are restated in `CLAUDE.md` here |
| Grid: `~/ostk.tgz` contents; `~/ostk_run/edge_probe.py` (6,138 B), `render_height.py` (6,825 B); `~/ostk_shards/mout/morph_{0..5,7}.csv`, `out/spinopelvic_{1..7}.csv`; `~/ostk_morph_out/shard_{1..23}.csv`; `logs_peddev_*` other than 40183959; the 48 `logs_ostkext_*` other than `_0` | grid HOME (`MANIFEST_GRID.md`) | listed, not read; one representative of each kind was read and copied; the rest are reproducible from the same run or are duplicates of what the committed CSV holds |
| The twelve `*_height.png` renders of job 40183679 | location not recorded | not found in either grid listing |
| `~/ostk_run/OpenSpineToolkit/` and `~/OpenSpineToolkit/` module texts read for hashing (`vertebral_body.py`, `morphometry.py`, `labels.py`, `spine.py`) | grid HOME | read only to compare with the repository; the repository holds the same text at the commits named in `STATUS.md`; not copied |
| The build's scratch captures (`grid_check.out`, `grid_files*.out`, `copy_log.json`, this generator) | the builder's scratchpad, not part of the folder | working files of the build; the facts they established are written into the manifests |


## 4. Where the rest of this project's material lives (cross-references, not copies)

- `03_ctspinopelvic1k_dataset`: the v11 labels on the grid, `scripts/label_scheme.py`, `merge_s1_into_sacrum.py`, the
  dataset article and `REPRODUCE.md`.
- `05_ct_morphometry_parity`: the whole morphometry CSVs, the four morphometry documents, reader E's renders and J3.
- `08_render_devices`: PolyPose (imports ostk; measures through the release plate fits).
- `12_website_pacs_demo`: the PACS demo the exporter feeds.
- `11_students_grid_access`: the student entry (`Student_Projects/RECIPE.md`) and the May 2026 medical-education record.
- `10_data_platform_grid`: the migration state of the 2026-09-10 scratch (batch B14) and the deletion decisions.



## Final pass of 2026-10-08 (after the critic's check of the whole tree)

Rows added by the final pass; the sections above are the first build and the verifier's fix pass as they were. Sources are laptop paths of 2026-10-08 (history, not dependencies). sha1 is the first 16 hex digits of the copy.

### Redaction made the same in every folder

The one Hugging Face handle quoted beside a published co-author's name was withheld in some folders and kept in others for the same source line (the critic's finding). It now reads `(HF username withheld)` everywhere (one occurrence per file below); the person's name stays (a person, never renamed). Greg may restore it; it is his decision (PLAN.md section 5).

- `docs/handoff/RECIPES.md`
