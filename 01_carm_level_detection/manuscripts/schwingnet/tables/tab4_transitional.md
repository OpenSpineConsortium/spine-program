# Table 2 — Transitional persons by subtype (same rows as `tab4_transitional.tex`; cell sources in `tab4_transitional.sources.md`)

Rewritten 2026-09-23 for the six-figure manuscript. The file name is kept from the earlier four-table layout; the
table prints second (Methods cites it second). The claim columns of the earlier Table 4 (sensitivity, specificity,
exact level, registration ceiling, simulated surgeon + LevelCheck) moved to the comparison, which is paper 2 since 2026-09-24
(`paper2_levelcheck/`, formerly Table 3 `tab_levelcheck.tex` and Figure 6).

Transitional persons by subtype: definition, persons per source, the truth behind the subtype, the test side of the built person-disjoint split, the share of held-out persons the current level encoder trained on, the unread COBRA2026 screen calls, and the best-case Wilson 95 % lower bound the test count allows.

| Subtype (a) | Definition; what a detector can see (b) | Persons: total (CTSP / VerSe / TS / C-Arm) | Truth behind the subtype | Test persons, built split (c): CT + real | Validation and test persons the current encoder trained on (d) | Unread COBRA2026 screen calls (supported by their field) (e) | Wilson lower bound with no error at the test count, % (f) |
|---|---|---|---|---|---|---|---|
| L6 | six rib-free vertebrae above the sacrum; six lumbar bodies where the sixth carries a label | 110 (18 / 86 / 3 / 3) | CTSP two-reader consensus or release label; VerSe published read (38 persons on the audit read alone); TS independent rib count; C-Arm one automatic labeller | 43 + 3 | 49 of 54 | 38 (11) | 91.8 (43 CT); 74.1 (11 calls) |
| T13 | thirteen rib-bearing vertebrae | 7 (0 / 6 / 1 / 0) | VerSe mask label 28; TS independent rib count | 3 + 0 | 4 of 4 | 45 (38) | 43.9 (3 CT); 90.8 (38 calls) |
| Sacralised L5, four lumbar | L5 fused to the sacrum (Castellvi III or IV) and four lumbar labels; the fused body sits in the sacrum label: one box | 12 (9 / 3 / 0 / 0) | CTSP two-reader consensus; VerSe published read | 5 + 0 | 14 of 14, both sacralised rows | 8 (8) | 56.6 (5 CT); 67.6 (8 calls) |
| Sacralised L5, five lumbar | L5 fused to the sacrum on a five-lumbar count; its own label (CTSP) or none (VerSe) | 16 (3 / 13 / 0 / 0) | as the row above | 6 + 0 | with the row above | none called | 61.0 (6 CT) |
| Castellvi I/II | enlarged or articulating transverse process; the count is unchanged | 31 (4 / 27 / 0 / 0) | CTSP two-reader consensus; VerSe published read | 12 + 0 | 15 of 15 | not screened | 75.8 (12 CT) |
| Lumbar rib | rib on L1; the count is unchanged | 14 (14 / 0 / 0 / 0) | CTSP release labels | 6 + 0 | 7 of 7 | not screened | 61.0 (6 CT) |
| Unassigned | four lumbar labels, source read normal; no subtype established | 4 (4 / 0 / 0 / 0) | CTSP release labels | 2 + 0 | 3 of 3 | — | — |
| L6 and T13 in one spine | none in any truth table | 0 | — | — | — | — | — |
| Any subtype | the rows above | 194 (52 / 135 / 4 / 3) | — | 77 + 3 | 92 of 97 | 91 (57) | L6, T13 and sacralised rows: 93.7 (57 CT); 93.7 (57 calls) |

CTSP = CTSpinoPelvic1K; TS = TotalSegmentator; C-Arm = C-ArmLSpine; L5, L6 = fifth, sixth lumbar vertebra; T13 = thirteenth thoracic vertebra.

- (a) Distinct persons (patient key; two VerSe series pairs are one person each); rib convention: L6 = six rib-free vertebrae between the last rib-bearing vertebra and the sacrum, T13 = thirteen rib-bearing vertebrae. Counted 23 September 2026 from the subtype table; eight of twelve TotalSegmentator spines once called L6 from raw mask identifiers read normal on an independent rib count and are not counted.
- (b) Whether a detector sees one body or two is decided by the mask: a fused body with its own label gives two boxes, one inside the sacrum label gives one, one left unlabelled gives none.
- (c) Person-disjoint, subtype-stratified split, 50 / 10 / 40 train / validation / test within each subtype, every real transitional subject on the test side (the three C-ArmLSpine L6); built 23 September 2026, leak audit passed; Figure 5c draws these counts. The three real C-ArmLSpine L6 are scored only in cross-validation, as agreement with one labeller's read (Table 3, the naming table).
- (d) Persons on the validation or test side of the built split who sit in the training split of the level bank behind the current encoder (v8 or v9); a model descending from those banks cannot score them, so a transitional test needs an arm trained without them.
- (e) SPINEPS with VERIDAH on the planning CT deformably registered to the cone-beam CT, read by no person; on CTSP this labeller's L6 call matched the readers in 10 of 24. The screen also flagged three cases for re-reading. All calls sit on the test side; none counts as a transitional test person until verified. In brackets, the calls their own field does not contradict: 27 L6 calls see no L1, so no count stands behind them, and seven T13 calls cover only L1–L4 above the sacrum, an ordinary thoracolumbar count; four-lumbar calls are placed in the four-lumbar row.
- (f) Wilson 95 % lower bound when every test person is named correctly, the best case at that count ("calls": if every supported COBRA2026 call were confirmed); the pre-stated targets are 90 % for the exact level (35 persons with no error) and 85 % for variant sensitivity (22 carriers without a miss).

Not on the printed page: by mask stratum inside the built split (train / validation / test), L6 audit-only 18/4/14, audit+raw-mask 1/0/1, raw-mask 24/5/19, release id 25 9/2/7, verified count 1/0/2; sacralised L5 four-lumbar unchecked 1/1/1, merged into the sacrum 4/1/4, own id 9/1/6 (`results/rare_class/split_plan.md`). Of the COBRA2026 L6 calls, 27 see no L1, so the count behind the call cannot be made; 7 T13 calls name only L1–L4 above the sacrum, the ordinary thoracolumbar count (same file).
