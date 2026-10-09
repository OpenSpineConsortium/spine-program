# Transitional spines available as evidence, by source and split

| source | total | L6 | T13 | in v8 validation | in v8 train (not evidence) | not in the bank |
|---|---:|---:|---:|---:|---:|---:|
| verse | 56 | 50 | 6 | 13 | 43 | 0 |
| ctsp | 18 | 18 | 0 | 5 | 13 | 0 |
| totalsegmentator | 4 | 3 | 1 | 0 | 4 | 0 |
| carmlspine_real | 3 | 3 | 0 | 0 | 0 | 3 |

TotalSegmentator rows are the verified subtypes of `SchwingNet/results/rare_class/ts12_subtype_override.json`
(F1, `SchwingNet/results/spineps_ids/TS12_VERIFY.md`: an independent count from SPINEPS instances
and CT rib components, no VERIDAH name used; no radiologist read). They were once selected by 'SPINEPS mask id 25
present' on masks whose ids are a raw 1..N enumeration; of those 12, 8 are normal spines and are not listed (TS_s0224, TS_s0790, TS_s1124, TS_s1171, TS_s1178, TS_s1304, TS_s1350, TS_s1380).
Only those 12 TotalSegmentator spines were examined; the rest of TotalSegmentator is not screened here.
VerSe from raw masks; CTSP from the release labels and the anomaly manifest; C-ArmLSpine from the CBCT labels
of the real frames.
