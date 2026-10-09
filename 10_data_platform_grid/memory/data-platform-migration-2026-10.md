---
name: data-platform-migration-2026-10
description: "The imaging data platform (Greg 2026-10-07): manifest of 212 sources, re-acquisition driver, Ceph layout, migration plan and index DB live in spinesurg-ct-nnunet/data_platform; migration runs as sbatch batches B00-B14 with rename+symlink cut-over; the report is a Claude Doc; students read everything except VinDr and BUU"
metadata:
  node_type: memory
  type: project
  originSessionId: 0599380b-0d32-4e19-b5be-65bdd1017566
  modified: 2026-10-08T20:43:09.535Z
---

**Status on 2026-10-08 (HANDOFF/context/INDEX.md; carried on this copy):** CURRENT; this copy is the live note of 2026-10-08 20:43 UTC, newer than the HANDOFF/context copy of 16:39 (the difference is one paragraph recording the HANDOFF commit); INDEX.md status CURRENT. A note is a dated record from the session that did the work, not an instruction; where it and a result file or docs/handoff/RESULTS_CATALOG.md disagree, the file and the catalog win.

Greg, 2026-10-07: "manifest of where all my raw data came from ... programmatic re-acquisition ... move all
X-ray/fluoro/CT data to oschome ... a database indexing by annotation status, modality, position"; 2026-10-08:
"create an artifact of this report, begin moving all of them ... students should be able to see all of this data".

**Where things are.** `spinesurg-ct-nnunet/data_platform/` (branch L6_Class, commit 5811eda, pushed; also copied
to the grid checkout with `git archive | ssh tar` because the grid cannot fetch the private repo):
DATA_MANIFEST.md (212 cards, 929 KB), sources.yaml/json, reacquire/ (driver, refuses the login node),
LAYOUT.md (`/rs/rs_grp_oschome/go2432/data/<source_id>/{raw,converted,derived,labels,meta}` + README.yaml),
MIGRATION_PLAN.md + plan/ (build_plan.py, preflight.sbatch, migrate_batch.sbatch, cutover.sh with FINALIZE and
ROLLBACK, verify_transfer.py, publish_visibility.sh), db/ (SCHEMA.sql, build_index.py), VERIFICATION.md.
The report is the Claude Doc "Imaging data holding: manifest, migration and index"
https://claude.ai/code/artifact/74a2ec52-90e4-4f20-82a5-5c8648668676 (doc node 2fba9a59-8077).

**Procedure per batch (all sbatch, never warrior):** preflight → migrate_batch (rsync -aH, verify by counts,
sizes, links, hashed sample) → cutover (rename to `<path>.pre-ceph` + symlink at the old path) → FINALIZE
(second comparison, then delete the .pre-ceph copy: the only step that frees HOME quota) → publish_visibility
(o+rX for non-restricted folders; VinDr/BUU and banks with their pixels 0700). State: `plan/runs/<B>/STATUS`.

**Census (jobs 40578909, 40580051, 40580052; `data/inventory/census_2026-10-07/`):** Ceph 7.7 TB apparent
(data/ 5.33 TB; u251 2.2 TB non-imaging); HOME `~/CTSpinoPelvic1K` is 7.7 GB (the 1.9 TB September tree was
reclaimed 2026-09-07), `~/data/CTSpinoPelvic1K` 196 GB is the only HOME copy of the 802 CTs, `~/data` 624 GB,
VerSeFusion 195 GB, ablate 202 GB. Python `sorted()` walks uppercase names first; FluoroCap alone took > 7 h.

**Why:** the plan was built from documents whose sizes were a month stale; the census decides. **How to apply:**
regenerate with `plan/build_plan.py --census <tsv with path,gb>` (my census.tsv has path+gb columns), re-read
`migration_batches.csv`, then continue batches in dependency order (B03 after B02; B05 after B04; B10 after
B02/B04/B06/B07; B11 after B10). B13 (results, 627 GB) and deletions are Greg's calls. Related:
[[grid-access-list-gate]], [[grid-ceph-volume-oschome]], [[no-jobs-on-login-node]].

**2026-10-08 later.** Batches B00, B01, B02, B03, B08 cut over (symlinks at the old home paths, .pre-ceph originals kept
until FINALIZE); B06 (VerSe, 14 items) verified and cutting over; B04/B07/B09 copying; B14 = the fifteen "unknown"
home entries, identified from their own files: spondy_landmark = Mendeley 5jdfdgp762 (url.txt); s1v11 = the CTSP v11
build workspace (irreplaceable); pitest/pdwtest = the 2026-09-10 pelvic-incidence and pedicle-width test copies
(companions ~/pi_ostk2.csv, ~/pdw_why.py, ~/ostk_level_morphometry.csv move with them); dis_renders = 5 BUU renders;
qc.tar.gz = June CTSP QC PNGs; Multi-View-Vertebra = cloned MICCAI 2023 code; ~/docs = Feb 2026 weak-label docs;
3, 6, ada, output, v = GOMC/CHARMM chemistry; morphdef = empty scaffold; **~/github = a plain-text GitHub PAT**
(set 0600 on 2026-10-08; Greg to rotate and delete; never copy it). Students read every Ceph source folder except
VinDr, BUU, the banks with their pixels, and build_archive_private (publish_visibility.sh). The one-installation
rule on the access service is Off since 2026-10-03 00:13Z. The Claude Docs: data report 74a2ec52…, handoff
c3c7acfd…, literature state 3b03e849… (all six sections filled 2026-10-08 midday from HANDOFF/LITERATURE_STATE.md,
committed on L6_Class), **research directions 93705038-d1f9-46df-a267-da8f2c2e2d17** (filled 2026-10-08 16:15 from
HANDOFF/RESEARCH_DIRECTIONS.md, commit e4c3e88: 16 ranked projects; PAR-1 ratio-only 3-D target first, PAR-2 projected
morphometry on the 802 v11 volumes second, FLU-1 the 63-volume reader queue third; parity = 5-point non-inferiority on
one label set; one open comment to Greg on that margin). **HANDOFF/ committed 097933a (2026-10-08 ~16:45)**: README,
RESULTS_CATALOG, RECIPES, DATASET_USAGE, LEAKAGE, MANUSCRIPTS, INFRASTRUCTURE, CONTEXT_EXPORT + context/ (141 redacted
memory copies, INDEX.md with LEAKED/SUPERSEDED statuses), GLOSSARY, OPEN_QUESTIONS, working_notes/builders; the handoff
Claude Doc c3c7acfd filled the same evening. **HANDOFF/GREG_ONLY/ is deliberately untracked** (credential locations,
commercial stance, withheld contacts, student usernames, Greg's personal e-mail) until Greg decides whether it enters
the private repo; the reader split (OPEN_QUESTIONS A29) is unconfirmed, so the whole folder is Greg-only for now.
Before any handover re-run `HANDOFF/working_notes/builders/refresh_context.py` then `build_context_index.py`.

**2026-10-08 midday.** B06 (VerSe: VerSeFusion/data, vf_813, implant_verse, ctsp_drr_obl …) and B14 cut over, .pre-ceph
kept; B04/B07/B09 still copying; TotalSegmentator v2.0.1, BUU, FluoroCap and the banks are NOT on Ceph yet. HOME is
4,051 of 4,295 GB: only FINALIZE (deletes .pre-ceph) frees it, and that is Greg's call. **The handoff workflow
(wf_78420abb-db7) was interrupted at 09:42 before writing anything; HANDOFF/ held only LITERATURE_STATE.md until it was
resumed at 11:45** (readers, author, three verifiers, fixer; output HANDOFF/README, RESULTS_CATALOG, RECIPES,
DATASET_USAGE, LEAKAGE, MANUSCRIPTS, INFRASTRUCTURE, CONTEXT_EXPORT, GLOSSARY, OPEN_QUESTIONS). Dedup plan written by
workflow wf_f61cc81c-91a into data_platform/dedup/ (DEDUP_PLAN.md: 46 groups; at most 97.7 GB linkable byte-identical;
482.9 GB deletion candidates for Greg; 1,659 index alias rows); its hash job `dedup_hash.sbatch` is read-only and gates on
VERIFIED + cut over + no running batch job; `dedup_apply.sbatch` also requires FINALIZED. Nothing of dedup is on the grid
yet: copy the folder (git archive | ssh tar), then `sbatch -D "$PWD" dedup_hash.sbatch` from
~/spinesurg-ct-nnunet/data_platform/dedup after the B06 cut-over job ends (B06 and its visibility pass finished 12:35;
dedup committed 9bc7303 and shipped; hash job 40581845 submitted 12:44, results in dedup/hash_results/<gid>.json;
groups whose batch is still copying (B04 BUU/AASCE/Mendeley_716, B07 TotalSegmentator v2, B09 FluoroCap, B10/B11
banks) come back not_ready and are rerun with GROUP_IDS later). **Hash verdicts 13:03:** A01 VerSe'19 = VerSe'20 for
185 files, 8.42 GB (identical, linkable after FINALIZE); A02 canonical/ has 224 links and no byte copy; A03 the HF
staging trees are NOT hard links (27 same inode, 2,753 files with no byte twin: 56 GB of distinct bytes, a kind-(b)
candidate for Greg, not a link); A07 s1v11 build labels = release labels, 802 files 1.19 GB (hold greg_review); A09
0533 repair = release; A08/A10 no twins (ctsp_april shares no CT bytes with the release); A04 came back "missing"
because **the grid's bash 4.2.46 keeps the quotes of a quoted replacement in `${var/pat/"$new"}`** (WSL bash 5.2 does
not; the 106-check suite missed it); fixed, rerun as job 40581924: 357 renders identical, the 13 `ann/glgl*.json`
differ only by the embedded name, hold `removal_preferred` stands. Summary in dedup/HASH_RESULTS.md. **The TCIA CT Colonography raw DICOM (721 GB) and tcia_nifti (336 GB) are on
neither HOME nor Ceph** (dedup readers, 2026-10-08 census); nothing records what removed them beyond the 2026-09-07
reclaim; the manifest card says on_disk_state_unknown and the re-acquisition route is `tcia_ctsp_download`.
