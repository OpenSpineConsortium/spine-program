# Hash results

What `dedup_hash.sbatch` found on the Ceph copies, run by run. The record is `hash_results/<gid>.json` and `.tsv`
(one row per file) and `logs/dedup_hash_<job>.out`; this file only reads them. Nothing has been linked or deleted.

## Run 1: job 40581845, 2026-10-08 12:44 to 13:03, every kind-(a) group

| group | verdict | files | what it means |
|---|---|---|---|
| A01 VerSe'19 copies inside raw/ against VerSe'20 | identical | 185 identical, 439 unpaired; 8.42 GB identical | 185 VerSe'19 files are byte copies of VerSe'20 files and can become links after B06 is FINALIZED; the other 439 VerSe'19 files have no byte twin (VerSe'20 re-released those series as `*_CT-iso` with corrected labels) and stay |
| A02 canonical/ against raw/ | none | 224 already links, 1,123 unpaired | canonical/ holds no byte copy of raw/: the 224 PIR scans are already symlinks and the rest are re-encoded, as the plan expected; canonical/ stays a kind-(b) candidate (67 GB) on its four conditions |
| A03 HF staging against raw/, corrected/ | review | 27 same inode, 2,753 unpaired, 1 key_mismatch | the staging trees are not hard links of raw/ (only 27 files share an inode); 2,753 files have no byte twin, so the 56 GB is distinct bytes, a kind-(b) deletion candidate for Greg, not a link candidate; the one twin is `hf_staging/corrections/veridah_manifest.json` = `corrected/veridah_manifest.json` |
| A04 verse_drr doubled-prefix renders | missing (defective run, see run 2) | 370 missing_canonical | the rename helper kept literal quotes on the grid's bash 4.2 (`"gl"146.npy`); fixed and rerun |
| A05 TotalSegmentator v2.0.1 ct = v3.0.0 ct | not_ready | | v2.0.1 is not on Ceph yet and the v3 item of B07 has no STATUS: B07 is still copying |
| A06 TotalSegmentator v3 in-release duplicates | not_ready | | B07 still copying |
| A07 s1v11 build labels = release labels | identical | 802 identical, 1 unpaired (`dataset_labels.json`); 1.19 GB | the v11 build output is the release, file for file; held for Greg's review of ~/s1v11 before any link |
| A08 pitest, pdwtest against the v11 labels | none | 12 unpaired | the 10 September scratch copies are not v11 files (v10 copies, as the plan expected); 17 MB, nothing to link |
| A09 CT 0533 repair work copy = release | identical | 1 identical, 1 unpaired (the `.cast` candidate) | record only |
| A10 ctsp_april against the v11 release CTs | none | 1,504 unpaired | no April input CT is a byte copy of a release CT; the April tree stays its own kind-(b) item |
| A11 to A15 BUU, Mendeley, AASCE | not_ready | | their Ceph roots do not exist yet: B04 still copying |
| A16 FluoroCap subsets | not_ready | | B09 still copying |
| A17 to A19, A22, A23 banks | not_ready | | B10 and B11 not started |

## Run 2: job 40581924, 2026-10-08 13:07 to 13:08, group A04 after the fix

| group | verdict | files | what it means |
|---|---|---|---|
| A04 verse_drr: `img/glgl*` against `img/gl*`, `path/glverse*` against `path/verse*`, `ann/glgl*` against `ann/gl*` | different | 357 identical (13 img, 344 path; 188 MB), 13 size_differs (all 13 `ann/glgl*.json`, each 1 to 29 bytes smaller than its `ann/gl*.json`) | every doubled-prefix image and path render is a byte copy of its single-prefix twin; the 13 annotation files differ only in size by about the length of the embedded name, consistent with the JSON carrying its own file stem, so they are the same annotation under another name, not independent data. The plan's hold (`removal_preferred`: Greg deletes the `glgl*` twins rather than linking them, because a bank builder that reads both names would still ingest the render twice) stands; the ann files must not be linked, because their bytes differ |

## What follows

- Nothing is linked before its batch is FINALIZED (`plan/cutover.sh FINALIZE=1`), and FINALIZE is Greg's call.
  After B06 is finalized, `dedup_apply.sbatch` may link A01 (185 files, 8.42 GB). A07 waits for Greg's review.
- Rerun the not_ready groups when their batches land: `sbatch -D "$PWD" --export=ALL,GROUP_IDS="A05 A06" dedup_hash.sbatch`
  after B07; `A11 A12 A13 A14 A15` after B04; `A16` after B09; `A17 A18 A19 A22 A23` after B10 and B11.
- The grid's bash is 4.2.46. Any further bash written for these jobs must avoid constructs newer than that; the test
  suite runs under WSL bash 5.2 and did not catch the quoting difference.
