# Positives census: reader-labelled transitional spines available for a CT-segmentation phenotype classifier

Inventoried 2026-09-24 from the files named in each section. Every number is copied or computed from a file; none is typed from memory. Unit is the PERSON (VerSe series are folded to subjects through `verse/screened.csv`; CTSpine1K COLONOG volumes are CTSpinoPelvic1K persons through `other_ct/alias_rows.csv`). Grid paths were listed with `ls`/`find` on the login node only; nothing was computed there.

Label tiers used throughout (the registry's own words, `SchwingNet/results/transitional_registry/REGISTRY.md` line 24):
- **read** = a human read exists (radiologist / neuroradiologist consensus, or a release author list). This is the only tier that is a training LABEL.
- **two-labeller** = SPINEPS+VERIDAH (A) and TotalSegmentator-geometry (B) agree on a count. Segmenter-derived: a CANDIDATE, not a label. On CTSpinoPelvic1K a two-labeller L6 was right 6 of 10 times against the release names (REGISTRY.md line 466).
- **single-labeller / morphology-only** = one segmenter, or appearance only. Not a label.

Label-map traps checked: CTSP v11 (L1..L5 = 20..24, L6 = 25, sacrum 26); VerSeFusion unified masks in VerSe ids (L6 = 25, T13 = 28, no sacrum id); SPINEPS masks read only through `tools/spineps_ids.py` and the VERIDAH ctd; TotalSegmentator names never used to count. Phenotypes below are counted from the LABEL SOURCE (read / release list), never from a segmenter's names.

---

## 1. Headline: reader-labelled positives (tier `read`), persons, CT-only

Source of the cross: `SchwingNet/results/transitional_registry/registry.csv` (6,113 rows, 6,108 persons, 306 positive), tabulated by `subtype x truth_tier x winning_source x castellvi x four_lumbar x lumbar_rib`.

| phenotype (registry subtype) | CTSpinoPelvic1K | VerSe (VerSeFusion) | CTSpine1K MSD-T10 | **read total** | who read it |
|---|---:|---:|---:|---:|---|
| L6 / lumbarised S1 (six rib-free presacral) | 17 | 85 | 1 | **103** | CTSP: two radiology residents (NA, MI), consensus Castellvi; VerSe: two neuroradiologists, consensus (Loffler 2021 Suppl Table 1); CTSpine1K: README "Sacral Lumbarization" list |
| sacralised L5, fused (Castellvi III/IV with five lumbar, or four lumbar ids) | 12 | 13 | 2 | **27** | same three sources |
| Castellvi II with five lumbar (I is unrecoverable: shares a cell with 0 in VerSe) | 4 | 27 | 0 | **31** | CTSP residents; VerSe neuroradiologists |
| four lumbar, no fusion (numerical reduction, 23 presacral) | 0 read (5 two-labeller: 0349 0801 0931 1000 1123, `ctsp/rows.csv` four_lumbar=True; corrected 2026-09-24 from "2", see CORRECTIONS.md) | 3 (verse549, 552 verified; verse559 contradicted) | 0 | **3** (2 verified) | VerSe read `7/12/4/5` |
| T13 (13 rib-bearing, 25 presacral) | 0 (no CTSP FOV reaches T1) | 6 | 0 | **6** | VerSe read `7/13/5/5` |
| lumbar rib on L1 (stump rib at L1, five lumbar) | 0 read (14 label-derived, see 2.3) | 12 | 0 | **12** | VerSe read `thoracolumbar_stump_ribs = L1` |
| hypoplastic 12th rib (stump at T12, normal count) | 0 read (7 reader COMMENTS on read cases; 13 release-rib records with no rib 12) | 18 persons kept as `unassigned` (of 37 subjects in the table) | 0 | **18** | VerSe read `stump_ribs = T12` |
| six-segment sacrum (`7/12/5/6`) | 0 | 2 persons (3 scans) | 0 | **2** | VerSe read |
| fused (congenital block) | 0 | 0 | 0 | **0** | no source carries a fusion column other than Castellvi III/IV |
| hemivertebra | 0 | 0 | 0 | **0** | searched both repos and the registry: no mention |
| **all read-tier transitional persons** | **33** | **166** (171 rows, 5 subjects with two series) | **3** | **202** | |

Read-tier ORDINARY (a human read says normal): CTSP 1 (0016, the readers' reference; the other 768 "normal" are source counts, not a read); VerSe 143 persons with both junctions in field (plus 15 read-normal with no junction in field); CTSpine1K 0. Registry table A: `none | read = 143`.

---

## 2. CTSpinoPelvic1K (802 records, one person per record)

Files: `<CTSpinoPelvic1K repository at 7ddfe38>/docs\castellvi_consensus.csv` (34 lines: 33 graded + 0016 reference), `docs\castellvi_readers_2026-09-04.csv` and root `Lumbosac.csv` (the readers' worksheet; reader initials NA and MI, "two radiology resident physicians", `paper/mpda/main.tex` line 707 and 898), `SchwingNet/results/polypose/inputs/lstv_flag_labels_v2.csv` (ctsp cohort 802 rows: `lstv_label`, `castellvi_type`, `castellvi_agreement`, `has_L6`, `n_lumbar_labelled`, `has_lumbar_rib`, `max_rib_number`), `SchwingNet/results/transitional_registry/ctsp/{SUMMARY.md,rows.csv}` (64 rows).

### 2.1 The 33 Castellvi-read records, by consensus grade (label source = two residents; 6 disagreements resolved to a consensus column)

| registry subtype | Castellvi consensus | records | ids |
|---|---|---:|---|
| L6 (release id 25, 6 lumbar ids) | Ib | 2 | 0244, 0302* |
| L6 | IIa | 2 | 0033*, 0565 |
| L6 | IIb | 4 | 0097, 0366, 0486, 1053 |
| L6 | IIIa | 1 | 0208 |
| L6 | IIIb | 6 | 0234, 0268*, 0831, 0950, 0960, 0999 |
| L6 | IV | 2 | 0005, 0376 |
| **L6 read** | | **17** | (18th L6 record 0068 is ungraded: the instrumented record, `main.tex` line 622; registry tier two-labeller) |
| sacralised_L5_fused, four lumbar ids, fused body inside sacrum 26 | IIIb | 9 | 0094, 0151, 0156, 0158, 0760, 0785, 0787, 0875, 1031 |
| sacralised_L5_fused, five lumbar ids, fused L5 under its own id | IIIb | 1 | 0049 |
| sacralised_L5_fused, five lumbar ids | IV | 2 | 0008, 0021 |
| **sacralised read** | | **12** | |
| castellvi_I_II, five lumbar | IIa | 2 | 0170, 0196* |
| castellvi_I_II, five lumbar | IIb | 2 | 0176*, 0179* |
| **Castellvi II read** | | **4** | |

`*` = the two readers disagreed (`agreement=False`: 0033 IIa/IIIa, 0176 IIb/IIIb, 0179 IIb/IIIb, 0196 IIa/IIIa, 0268 IIIb/IIb, 0302 Ib/IIb); consensus column used. Side is recorded only in free-text comments: 0005 and 0376 "IIa on right and IIIa on left" (= IV), 0170 "left Ia transverse process", 0208 "complete fusion of the left transverse process", 0565 "Ia on the left side, IIa on the right", 0033 "rudimentary right rib at T12". Source `lstv_label` (CTPelvic1K tag or lumbar count) disagrees with the read on the L6 group: it says LUMBARIZATION 14, SACRALIZATION 2 (0005, 0097), SEMI_SACRALIZATION 1 (0033). Readers' own non-rib-bearing count differs from the labellers' in 13 read CTs (ctsp/SUMMARY.md point 12; 0176 "S1 lumbarization" counted 6 and 5).

Reader comments naming a rib anomaly (not a graded phenotype): hypoplastic / rudimentary 12th ribs at T12 on 0008, 0033, 0760; "possible rudimentary ribs at L1 or hypoplastic ribs" on 0785, 0787, 0875, 1031 (four of the nine four-lumbar IIIb spines).

### 2.2 Label-derived (not read) candidates in CTSP

| candidate | n | source of the call | status |
|---|---:|---|---|
| L6 by the rib convention, release names ordinary (T12 carries no rib, six rib-free bodies; thoracolumbar, 24 presacral) | 9 | two-labeller (release voxels + SPINEPS) | 0105, 0359, 0474, 0544, 0552, 0672, 0895, 1151, 1153; held by the ID guard (mask lacks 25); review queue `1-candidate`. NOT the same anatomy as the 18 read L6 (ctsp/SUMMARY.md point 1) |
| L6 hidden by release label defects | 2 | 0090 two-labeller, 0150 single-labeller | queue `1-candidate` |
| four lumbar, no read | 5 | two-labeller | 0349, 0801 (look sacralised on the sacral reformat), 0931, 1123 (look like a normal four-lumbar sacrum), 1000 (L5 separate, count may be five). None is a read |
| lumbar rib (release class 60/61) | 14 rows (16 records in the master file; 0008 and 0787 are sacralised reads carrying the modifier) | release rib label = TotalSegmentator/Moller pseudolabel triaged by medical-student reviewers (`main.tex` line 533, 889); 9 two-labeller (a TS rib overlaps), 5 single-labeller | 0720's right "lumbar rib" is a 12th rib; 1090's release label is off its CT (point 6). Not a radiologist label |
| absent 12th rib in the release ribs (`max_rib_number = 11`) | 13 | release rib labels | 0105, 0179, 0359, 0474, 0544, 0552, 0672, 0785, 0875, 0895, 1043, 1151, 1153: nine are the rib-convention L6 above, i.e. the same voxels seen twice |
| Castellvi screen candidates | 25 (learned screen top 25) / 214 (type-I height pre-filter, over-calls ~1.7x) | morphology | `CTSpinoPelvic1K-1/docs/castellvi_reread_queue.csv`, `castellvi_type1_queue.csv`; no grade |
| re-read queue | 1 | adjudicator flag | `docs/lstv_reread_queue.csv`: 0172, source normal, five anterior sacral foramina + rib on the L1-labelled body, `pending_reread` |

### 2.3 CT + segmentation on the grid (ls 2026-09-24)

- CT: `~/data/CTSpinoPelvic1K/ct/<id>_ct.nii.gz`, 802 files. Label: `~/data/CTSpinoPelvic1K/labels/<id>_label.nii.gz`, 802 files (v11; `0005_ct.nii.gz` / `0005_label.nii.gz` confirmed).
- Independent segmentations: SPINEPS `~/bench/spineps/`; TotalSegmentator `~/bench/totalsegmentator/native/COLONOG_<token>.nii.gz` (804 entries; 0533 and 0921 re-run privately).
- Staged for rendering: `/rs/rs_grp_oschome/go2432/data/rare_class/ctsp_stage/<id>/{<id>_ct,<id>_msk}.nii.gz`, 25 cases; 12 held under `.../ctsp_drr_arc/held/ctsp_<id>.json`.
- Junction in FOV: all 33 read records have the lumbosacral junction in field; thoracolumbar reference established in 31 of 33 (0787 and lumbar-rib 0231 have the lowest rib cut). No CTSP FOV reaches T1: no CTSP record can be T13.

---

## 3. VerSe (VerSeFusion), 374 series / 355 subjects; read = Loffler et al. Sci Data 8:284 (2021) Suppl Table 1, two-neuroradiologist consensus

Files: `SchwingNet/results/polypose/inputs/verse_suppl_table1.csv` (325 subjects with a read), `SchwingNet/results/transitional_registry/verse/{SUMMARY.md,rows.csv,screened.csv,audit_resolution.csv}` (171 rows, 374 screened), `maximize/after/held_all.json`. Grid copy of the table: `~/lstv_flag/sources/verse_suppl_table1.csv` (+ `TRANSITIONAL_LABELS.csv`, `moller_stump_ribs.csv`).

### 3.1 The published read, whole table (325 subjects)

| column | values |
|---|---|
| `castellvi_grading` | 0/1 181; 2a 35; 2b 25; 3a 14; 3b 28; 4 7; blank 35 |
| `assumed_segment_structure` (C/T/L/S) | 7/12/5/5 228; 7/12/6/5 76; 7/11/6/5 8; 7/13/5/5 6; 7/12/5/6 3; 7/12/4/5 2; 7/11/4/5 1; 7/11,5/6/5 1 |
| six lumbar | 85 subjects; of these 76 are 25-presacral (12 thoracic), 8 are 24-presacral with 11 thoracic (verse544, 581, 606, 626, 636, 642, 765, 814; the ninth 11-thoracic subject, verse559, is the 7/11/4/5 read), 1 ambiguous (7/11,5/6/5) |
| four lumbar | 3: verse549, verse552, verse559 |
| thirteen thoracic | 6: verse547, 582, 588, 601, 602, 631 (the six the masks carry as id 28) |
| `thoracolumbar_stump_ribs` | none 209; L1 48; T12 37; T13 5; blank 26 |
| `lumbosacral_enumeration` | 0 220; 2 (six lumbar) 84; 1 3; blank 18 |
| Castellvi x lumbar count | 6 lumbar: 0/1 19, 2a 16, 2b 15, 3a 11, 3b 18, 4 6; 5 lumbar: 0/1 159, 2a 19, 2b 10, 3a 3, 3b 10, 4 1, blank 35; 4 lumbar: 0/1 3 |

The paper's own rule: a Castellvi III/IV body "partially fused with the sacrum" was NOT segmented (no id 25 in the mask, no sacrum id at all), and a rib is thoracic only if > 38 mm on at least one side.

### 3.2 What the registry made of it (persons)

| subtype | persons | Castellvi (persons) | lumbar-rib modifier | both junctions in this scan's field | mask carries the call (id 25/28) |
|---|---:|---|---:|---:|---|
| L6 | 85 | none 19; IIa 16; IIb 15; IIIa 11; IIIb 18; IV 6 | 35 | 80 (2 LS only, 1 TL only, 2 neither) | 46 rendered earlier; **39 held**: mask lacks 25 (Castellvi III/IV L6 unsegmented, or the ids stop at 24) |
| T13 | 6 | none 3; IIa 2; IIIa 1 (verse601) | 0 | 6 | 6 (id 28) |
| sacralised_L5_fused (III/IV, five lumbar) | 13 | IIIa 2; IIIb 10; IV 1 | 0 | 12 | fused body `unlabelled` in every mask |
| castellvi_I_II (grade II, five lumbar) | 27 | IIa 17; IIb 10 | 1 | 26 | n/a |
| lumbar_rib (stump at L1, five lumbar, no grade II+) | 12 | none | 12 | 11 | n/a |
| unassigned | 23 | none | 1 | 21 | 18 stump-T12 (hypoplastic last rib, normal count; kept because Greg asked for every anomaly); 3 four-lumbar (549, 552 verified; 559 contradicted, mask has five lumbar ids); 2 six-segment sacrum |
| held, no row | 2 | | | | gl279 (mask L6, no read, labellers disagree); verse707 (read normal, mask carries id 25: the mask's naming is shifted one level) |

VerSe read persons whose scan contradicts the read (queue high priority): verse278, 507, 512, 540, 559, 571, 588, 601, 612, 615, 765, 814 (audit_resolution.csv, 11 "KEPT but CONTRADICTED" + verse559). Read T13 verse588 and verse601: A counts 12 thoracic.

### 3.3 CT + segmentation on the grid

- `~/VerSeFusion/data/unified/scan-<id>_{ct,msk}.nii.gz` (+ `_meta.json`): 374 scan dirs (`ls -d scan-* | wc -l` = 374; the 375th entry is `unify_manifest.json`). Held examples confirmed present: verse024, verse502, verse707, gl279, verse547, verse255.
- Labeller B (TS 2.18 `total`) outputs: `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/verse/` (census_v3, 374 json).
- Do NOT read `~/vf_813` / Dataset813 maps (C1-T9 sent to ignore) or the VerSeFusion manifest `has_T13` (18: wrong; truth 6).

---

## 4. CTSpine1K (HF mirror, 1,005 volumes; 782 COLONOG are CTSP persons; 223 screened here: MSD-T10 150, COVID-19 40, HNSCC 31, COLONOG 2)

Files: `SchwingNet/results/transitional_registry/other_ct/{SUMMARY.md,ctspine1k_release_reads.csv,crosswalk_report.json,alias_rows.csv}`.

Label source: the CTSpine1K README "Special Cases" lists (grid `/rs/rs_grp_oschome/go2432/data/ctspine1k/README.md` lines 187 "Sacral Lumbarization: 24 cases" and 215 "Lumbar Sacralization: 13 cases with expert labeling"; the local crosswalk counts 25 L6 + 14 sacralisation names). Reader not named; it is the release authors' list, not a graded read. Of those 39 names: 25 are CTSP persons (16 L6 agree with the CTSP read; 9 sacralisation agree), 11 are VerSe persons (8 L6 agree; 1 sacralisation read NORMAL by the neuroradiologists), 3 are new MSD-T10 persons.

| phenotype | persons | ids | tier | mask |
|---|---:|---|---|---|
| L6 | 1 | MSD-T10/liver_106 | read (README list; annotation carries id 25 = 19 bodies C7-L6). The one CTSpine1K L6 the labellers do NOT reproduce | rendered |
| sacralised L5 fused, four lumbar ids, no sacrum id | 2 | liver_83, liver_93 | read (README list) | rendered; fused body `unlabelled` |
| L6 by rib convention (rib-less 20th body; annotation names it T12) | 2 | liver_119, liver_95 | two-labeller | held (mask lacks 25) |
| unresolved | 15 | | none | queue |

Grid: CT `/rs/rs_grp_oschome/go2432/data/ctspine1k/raw_data/volumes/MSD-T10/liver_106.nii.gz`, label `.../labels/MSD-T10/liver_106_seg.nii.gz` (liver_83 likewise confirmed); staged `.../rare_class/ctspine1k_stage/liver_{106,119,83,93,95}/`; SPINEPS/TS outputs `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/other_ct/ctspine1k/{spineps,ts,ts_total}` (spineps 862 files). Six COLONOG README names not in the release spreadsheet are unresolved (`crosswalk_report.json` name_not_in_xlsx 6).

---

## 5. Segmenter-only sources (no human read anywhere; candidates, not labels)

### 5.1 TotalSegmentator v2.0.1 + v3.0.0 (1,939 scans = persons; no patient id shipped)

`SchwingNet/results/transitional_registry/totalsegmentator/SUMMARY.md`: no row is `read`; `castellvi` empty on every row. Positive rows 52 (two-labeller 25, single 27); unresolved 74; none 622; no_count 1,187.

| subtype | two-labeller | single-labeller | notes |
|---|---:|---:|---|
| L6 | 14 | 8 | 9 of 23 v300 `vertebrae_L6` masks land here; rib-less-T12 kind (s0158, s0477, s0683, s1487, s1998...) is 24 presacral, not a supernumerary segment; s0477 sits under hardware |
| T13 | 3 | 1 | s1023 and s1329 carry a rib on one side only, < 40 mm: T13 by contact, lumbar rib by the 38 mm rule; s0616 is the one hand-counted T13 |
| unassigned (four lumbar 13 / eleven rib-bearing 13) | 8 | 18 | 12 of 26 are paediatric (unfused S1 reads as a free body) |
| lumbar_rib / sacralised / castellvi | 0 | 0 | need a read that does not exist |

The only human check: twelve CTs hand-counted (`other_ct/cases/val_tsgt.csv`, "counted by hand (TS12_VERIFY.md)", `tools/other_ct_screen.py` line 57): truth normal 8, T13 1 (s0616), L6 1 (s1089), L6-pattern rib-less 20th 2 (s1088, s1123). Who counted is not stated in the file; it is the project's own look, not a radiologist.

Grid: v300 CT `~/data/TotalSegmentator_v3/Totalsegmentator_dataset_v300/<s>/` (1,940 entries); v201 `~/data/TotalSegmentator/<s>/{ct.nii.gz,segmentations/}` (1,235 entries); SPINEPS `~/bench_ts/spineps/native_ctd/TS_<s>_{seg-spine_msk.nii.gz,ctd_isogrid.json,relabel.json}` (5,984 files). Checked: s0049, s0059, s1089, s1023, s1329, s0616 have v201 + v300 + SPINEPS; s1974 (L6 two-labeller) and s2047 (unassigned) are v300-only with no SPINEPS mask (`maximize/unavailable.json`). 19 TS positives rendered to `.../rare_class/totalsegmentator_drr_arc`; s0077 and s0477 stopped at the precheck (VERIDAH skips T12).

### 5.2 RibFrac (660 chest CTs; a case is a person)

T13 single-labeller 4 (RibFrac101, 93, 322, 539: 13 rib-bearing counted from C7, sacrum out of field, so T13 vs rib-on-L1 is open on all four); L6 morphology-only 1 (RibFrac482, sixth body at the caudal edge); unassigned 1 (RibFrac488); unresolved 29; none 591 (thoracolumbar junction only: 626 countable from T1, 9 reach the sacrum). Grid: `/rs/rs_grp_oschome/go2432/data/ribfrac/images/RibFrac<n>-image.nii.gz` (660); SPINEPS `.../anomaly_harvest/other_ct/ribfrac/spineps/RibFrac<n>_{seg-spine_msk.nii.gz,ctd.json,harvest.json}` (2,620 files); TS beside it. RibFrac ships no vertebra masks of its own.

### 5.3 Real-frame collections: TEST only, never rendered for training

- COBRA2026 (692 planning CTs, each with real kV projections; `cobra/SUMMARY.md`): L6 3 (B127, D238 two-labeller; A270 single), unassigned four-lumbar 6 (D014, D484, F058, F089 two-labeller; B084, B091 single), unresolved 11, normal count 175, no_count 497 (494 have only the sacrum in field). Both labellers on `ct_def`; per-case records `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/cobra/cases_v5/<case>.json` (692). Split plan: 91 earlier SPINEPS-only "transitional_call" cases (L6 38, T13 45, four_lumbar 8) are in test and UNVERIFIED (`rare_class/split_plan.md`).
- C-ArmLSpine (149 lumbar CBCTs): L6 morphology-only 3 (case42, case121, case136: VERIDAH names L2-L6, no rib head in field, no count), unassigned 1 (case97); 140 have neither reference in field. Grid `/rs/rs_grp_oschome/go2432/data/carmlspine/`.
- DeepFluoro (6 pelvis CTs), Geneva, SpineSAC, Ljubljana: no count in field; 0 positives.

### 5.4 Radiographs (not CT, out of scope, recorded so nobody re-counts them)

BUU-LSPINE 3,600 pairs: 129 "L4" + 15 "L6" numerical variants from the KIOM2022 report (`TRANSITIONAL_LABELS.csv` lstv_subtype), radiograph-only read, "No License Provided", excluded from training by decision. NHANES II: no transitional reading released. Kwak 2025 (the only 2-D LSTV model): nothing released.

---

## 6. Ordinary (negative) persons available beside the positives

| source | read-normal | two-labeller none | single-labeller none | no_count (junction not in field) | real frames |
|---|---:|---:|---:|---:|---|
| CTSpinoPelvic1K | 1 (0016) | 775 of 802 agree on a count with the release (ctsp/SUMMARY.md denominators; 738 records are not registry rows) | | 11 refusals | no |
| VerSe | 143 (+15 read-normal with no junction in field) | | | 28 | no |
| TotalSegmentator | 0 | 584 | 38 | 1,187 | no |
| CTSpine1K (non-CTSP) | 0 | 118 | 28 | 57 | no |
| RibFrac | 0 | 529 | 62 | 34 | no |
| COBRA | 0 | 112 | 63 | 497 | yes (TEST) |
| RSNA c-spine | 0 | 0 | 0 | 2,022 | no |

Registry table A, CT-only: `none` = 143 read + 1,231 two-labeller + 128 single-labeller + 4 none = 1,506 persons; `no_count` 3,343.

---

## 7. What is held or unresolved (persons whose label and mask do not yet agree)

Read from `maximize/after/held_all.json` (54 held: verse_drr 39 L6 read + 1 unassigned read; ctsp_drr_arc 10 L6 + 2 unassigned two-labeller; ctspine1k_drr_arc 2 L6 two-labeller) and `maximize/waiting.csv` (52 waiting: 13 real-frame TEST, 39 single-labeller / morphology-only awaiting adjudication).

- 39 VerSe read-tier L6 whose VerSeFusion mask carries no id 25 (ids stop at 24, or the L6 is a Castellvi III/IV body VerSe left unsegmented). The read is the label; the mask cannot yet carry it. For a segmentation-input classifier these are usable only if the input is the CT re-segmented (SPINEPS/TS), not the release mask.
- 10 CTSP two-labeller rib-convention L6 (0105, 0359, 0474, 0544, 0552, 0672, 0895, 1151, 1153 + 0090): release names five lumbar; relabel 19..24 -> 20..25 is one line once a reader confirms; NOT a read.
- 2 CTSP four-lumbar two-labeller (0349, 1000) and 3 more (0801, 0931, 1123): no reader has graded them.
- verse559: read four-lumbar, every labeller and the mask count five (held); verse707: read normal, mask id 25 (held); gl279: no read, mask L6, labellers disagree.
- CTSP 0176 ("S1 lumbarization", readers counted 6 and 5, labellers 5): may be an L6 the count missed.
- TotalSegmentator 74 unresolved + 27 single-labeller; RibFrac 29 unresolved; COBRA 11 unresolved.
- 6 CTSpine1K COLONOG README L6/sacralisation names that are not in the release spreadsheet.
- Dataset813/815 phenotype flags are stale (11 CTSP transitional records missing from Dataset813's stratum; Dataset815 stratified 6 VerSe L6 + 2 T13 as normal): `docs/DATA_COMPLETENESS_AUDIT.md` lines 141, 255-258. Do not take counts from them.

## 8. Prevalence sanity check (outside numbers)

CTSP: 33 graded / 802 = 4.1 % (a read only of records whose count differed from five plus CTPelvic1K flags; not a census). VerSe: 85 six-lumbar / 325 = 26 % and Castellvi II-IV 109 / 325 = 34 %, an enriched PACS-search sample, not a prevalence. TotalSegmentator two-labeller L6 14 / 748 countable = 1.9 %; CTSpine1K MSD-T10 read L6 1 / 150. Published: LSTV 4-30 % by definition; Castellvi I ~19.7 % of adults (Hanhivaara); L6 a few percent. Nothing here sits outside those bounds, and the CTSP census is not a prevalence.
