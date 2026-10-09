# What the index builder should mark for duplicates

Companion of `index_aliases.csv` and `DEDUP_PLAN.md` (2026-10-08). The index today (`db/SCHEMA.sql`, built by `db/build_index.py`) has one subject per `<corpus>:<person>` spelling and no alias layer (SCH L7-L9, L52-L60); `duplicate_of` is filled only for a hard link, same `dev:ino` (BI L219-L226; SCH L88). Symlinks are seen two ways: the generic and VerSe adapters skip them (BI L353, L732), while the TotalSegmentator adapter tests `os.path.exists(ct)` (BI L694), which follows a link, and `item()` stats through it (BI L210-L226: `os.stat` gives the target's nlink, 1, so no `duplicate_of`); a v2 ct.nii.gz linked by A05 therefore stays indexed as a counted item of its own. Three changes follow, one per kind.

## (a) Byte-identical copies replaced by links: `duplicate_of`, `counted = 0`

- Read every ledger (`dedup/applied/<gid>.ledger.tsv`; the same rows in `$RS/dedup_ledgers/<gid>.ledger.tsv`; columns: job, utc, action, dup, canonical, bytes, sha256, mode, mtime (`stat %y`, nanoseconds), note; actions `protect`, `link_file`, `tree_member`, `tree_dir`, `link_tree`, `undo_file`, `undo_tree`). For each `link_file` and `tree_member` row whose dup path still resolves to the canonical path and has no later `undo_*` row, set on the dup path's item `duplicate_of` = the canonical item and `counted = 0`, with `sha256` from the ledger: UPDATE the item where the indexer already holds it or still walks it (the TotalSegmentator adapter does, through the link), INSERT it under its own source where the adapter skips links (generic, VerSe). Widen the SCH L88 comment from 'hard link' to 'hard link or ledgered symlink'; the meaning (the same bytes, counted once) is unchanged.

- Before linking, `--hash` plus the `hash_results/<gid>.tsv` rows with status identical give the same pairs without touching the disk: the indexer may set `duplicate_of` from them too, so the counts are right before any link exists.

- Groups held for deletion (A04 `glgl*`, A13 `(1)`) should be `counted = 0` now: the extra names are the defect.

## (b) Same data in another container: `counted = 0` and a lineage edge, never `duplicate_of`

- VerSe `canonical/` items: `counted = 0`, lineage `converted_from` the raw item of the same series (BI L756 counts them today).

- The VerSe'19 copy of a series also held as VerSe'20: `counted = 0`, lineage to the VerSe'20 item (95 series).

- TotalSegmentator v2 CTs with a v3 twin (A05): `counted = 0`, lineage to the v3 item, resolved by hash, not by `s####`. The lineage `source_ref` is resolved by path only today (BI L271-L277); it needs a hash or series-UID resolver.

- NHANES pickle images that are the same picture as a CDC TIFF (542 of 543): `counted = 0`, lineage to the TIFF; the landmark annotation attaches to the TIFF item.

- COBRA exported frames and `ct_def.mha` / `cbct_rtk.mha`: `counted = 0`, lineage to `projections.mha` / `ct_original.mha` (BI L564-L571, L595-L601).

- Archives beside unpacked trees (TS zips, vendor zips, NHANES zip, build archive): one `archive` item, `counted = 0`.

## (c) The same people: a subject-alias table

Proposed table (nothing here was applied): `subject_alias(alias_key PRIMARY KEY, subject_key REFERENCES subject, relation, unit, established_by, evidence_file, evidence_field, verified, status, group_id, note, loaded_from_sha256)`, loaded from `index_aliases.csv`; plus `subject.unit` (person, study, session, volume, specimen, object, document, none) and `subject.person_key` (the union-find representative), so `v_subjects_in_several_sources` groups by `person_key`. `duplicate_of` stays an item relation; it never joins two people.

`index_aliases.csv` columns: alias_key, subject_key, relation (same_person, same_study, renumbered_release, in_release_duplicate, same_scan_declared, near_duplicate, same_volume_other_release, own_subject, redistribution, render_of_source, same_volume_other_collection), unit, established_by (manifest, release_table, hash, declared), evidence_file, evidence_field, verified, status (concrete = load as is; rule = a name pattern the keyer applies; pending_table = a family whose rows are generated on the grid from the named file; candidate = shown, not merged), group_id, note.

| group | concrete | rule | pending_table | candidate | to do in the index |
|---|---:|---:|---:|---:|---|
| C01 VerSe: 374 series of 355 subjects; series held twice in raw/; canonical/ counted | 37 | 0 | 0 | 0 | subject alias verse:<series> -> verse:<patient_id> (37 rows); item level: the VerSe'19 copy of a series also held as VerSe'20 counted = 0 with lineage to the VerSe'20 item (95 series; duplicate_of when A01 linked it); canonical/ items counted = 0 (converted_from raw); render banks: pass the VerSe map to key_any (BI L794); match VERSE_SUB case-insensitively and lowercase the key (BI L713), or the raw GL### items stay unkeyed. |
| C02 CT COLONOGRAPHY people: TCIA, CTSpinoPelvic1K, CTSpine1K, the April release | 1,586 | 1 | 1 | 0 | subject alias tcia_ctc:<PatientID> -> ctsp:<vid> (802 rows, spelled as BI L650 keys the TCIA DICOM: 782 PatientIDs recorded in alias_rows.csv, 20 spelled by rule and marked so) plus one rule row (token = the CTC- id as is, else int() of the last OID component: ssn:tools/other_ct_dedupe.py L68-L69), and ctspine1k:COLONOG/<PatientID> -> ctsp:<vid> (782); the two non-CTSP volumes keep their own key tcia_ctc:<PatientID>; the April records need a keyed adapter and their manifest (not at any cited location). Neither tcia_ctc nor ctspine1k is in patient_keys.PERSON_FORMAT (ssn:tools/patient_keys.py L316-L337), so resolve_key refuses both until entries are added, and BI has no CTSpine1K adapter that emits ctspine1k: keys. Never write a token as ctsp:<token>: canon_key zero-pads token 100 to ctsp:0100, release 0100, another person (ssn:tools/patient_keys.py L250-L255; BI L111-L112). No item-level duplicate_of between a CTSpine1K volume and a CTSP CT until a series match is shown. |
| C03 TotalSegmentator v2.0.1 inside v3.0.0: 24 renumbered, 15 merged, 3 repeats inside v3 | 0 | 0 | 30 | 0 | release-qualified raw keys (ts201:, ts300:) mapped to the canonical subject ts:<v300 id>; all 29 rows here are pending_table until a release-qualified TotalSegmentator scheme exists (a patient_keys scheme, PERSON_FORMAT entries, a bank registry for the release, and BI emitting ts201:/ts300: instead of ts: at L698): 24 renumbered rows, 3 in-release rows, s2094 -> s2093 as same_scan_declared (as make_split and split_final.json already merge them), and s0927 -> s0254 with its release unrecorded; the other 1,204 v2 ids map from ct_fingerprints.json (or from A05's hash results). Item level: a v2 CT with a v3 twin counted = 0 with lineage to it (duplicate_of when A05 linked it). |
| C04 NHANES II under three names | 0 | 3 | 0 | 0 | three rule rows to nhanes:<5 digits>; item level: the 542 pickle images that are the same picture as a CDC TIFF counted = 0 with lineage (L00452 has no TIFF and stays counted). |
| C05 DeepFluoro specimens across the H5, the 8x H5, the vendor deposit, the HF re-host | 6 | 0 | 1 | 0 | 6 rows deepfluoro_8x:<NN> -> deepfluoro:<accession>; the HF subjectNN map waits for report/hf_vs_h5.json (U11); never key on the vendor PatientID. |
| C06 BUU-LSPINE byte pairs and the 2000/3600 releases | 2 | 0 | 0 | 0 | 2 rows buu:0719 -> buu:0140, buu:0629 -> buu:0449 (bytes proven, person not); A12's links give the 2000 JPEGs duplicate_of their buu_full items. |
| C07 VinDr-SpineXR images and studies | 0 | 0 | 1 | 0 | 10,466 rows image -> study from annotations/{train,test}.csv (on the grid, restricted under the DUA); unit = study. |
| C08 Mendeley 5jdfdgp762: a redistribution of BUU and VinDr | 0 | 0 | 1 | 0 | rows from the anns' duplicate_of (on the grid) to buu:<NNNN> and vindr:<study>. |
| C09 COBRA cases seen by several frame banks | 0 | 1 | 0 | 0 | no alias; item level: exported frames, ct_def and cbct_rtk counted = 0 with lineage to projections.mha / ct_original.mha. |
| C10 Renders keyed to their source CT (implant, PolyPose, CTSP_VERSE_, CTSP cross-naming, devcorpus, C-arm case views) | 0 | 7 | 0 | 0 | rule rows; implant renders resolve to ctsp:, ts: or verse: by their source scheme, as key_any does (make_implant_ct hardware records, else the one declared build whose case format fits: ssn:tools/patient_keys.py L393-L394, L426-L450), since implant_verse (373 VerSe series) and implant_ts exist beside the CTSP implants; the adapter must pass the Dataset813 crosswalk, the VerSe map and the implant map to key_any. |
| C11 Family B: exact pixel folds and near-duplicates across collections | 0 | 0 | 1 | 0 | rows from TIERS tier1/tier2 same_ct_as; a candidate table for the 1,186 with status unreviewed; unit = volume for AbdomenAtlas BDMAP ids and the AMOS unlabelled set. |

Rules that keep the aliases safe:

- A token or a TCIA PatientID is never written as `ctsp:<x>`: `_norm_person` zero-pads an all-digit person (ssn:tools/patient_keys.py L250-L255; BI L111-L112), so token 100 would become `ctsp:0100`, release 0100, another person. The token rows are spelled `tcia_ctc:<PatientID>`, as BI L650 keys the TCIA DICOM; 20 of the 802 PatientIDs are spelled by rule (prefix + 4-digit pad, true of every numeric PatientID on record) and say so in `verified`; a rule row converts any spelling to the manifest token. Neither `tcia_ctc` nor `ctspine1k` is in `patient_keys.PERSON_FORMAT` (ssn:tools/patient_keys.py L316-L337), so `resolve_key` refuses these keys until entries are added.

- TotalSegmentator keys must carry the release (`ts201:`, `ts300:`) before the alias maps them to `ts:<v300 id>`; a release-blind `ts:s####` splits 24 people and merges 15 (DM section 4 row 11). No keyer produces them yet (key_for and key_any return `ts:s####`: SCHEMES ts_plain, ts_render; BI L698), so every C03 row is `pending_table` until a patient_keys scheme, PERSON_FORMAT entries, a bank registry for the release and BI emitting the qualified key exist.

- VerSe: BI's VERSE_SUB (L713) is case-sensitive, so the raw VerSe'20 `GL###` items get no subject key; match it case-insensitively and lowercase the key.

- A CTSpine1K COLONOG volume and the CTSP CT of the same person are one subject but not one item until a series match is shown (ssn:tools/other_ct_dedupe.py L7-L8).

- Rows from restricted sources (VinDr, BUU) inherit the DUA or EULA of their source (`db/README.md`, last paragraph).

- The only complete alias table that exists today is `~/split_final.json` (`group_of`, `raw_to_group`; make_split's union-find, 2026-09-23); it moves to `$RS/data/multisource_banks/meta/split_final.json` in B11 (LAY L425). Loading its `raw_to_group` as `status = concrete, established_by = declared` rows is the quickest way to the pending families, with the caveat that it keys TotalSegmentator by bare `s####` and so keeps the 15 merges (side-safe for splits, wrong for counting).
