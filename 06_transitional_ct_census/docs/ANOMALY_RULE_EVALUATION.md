# The R + C anomaly rule, measured on real spines

Numbers here come from `docs/anomaly_rule_evaluation.json`, written by `tools/eval_anomaly_rule.py`
(`slurm/eval_anomaly_rule.sh` on the grid). Do not retype them; regenerate.

**Verdict.** The rule is arithmetic, not a test. `R + C = N - 1` for every choice of target, so
"R + C != 22" is exactly "the chain does not hold 23 vertebrae" and its whole content is one count over
the entire presacral column. That has three consequences, all measured below: it is **computable on 14 of
1,175 annotated spines (1.2 %)** in the two corpora, because it needs C2 and the lumbosacral junction in
one field; where it is computable it agrees with the truth by construction rather than by evidence; and
its error rate is the counting error rate compounded over 23 links, so **a 1 % per-vertebra miss rate
flags 21 % of normal spines and a 2 % rate flags 37 %**. It is usable as a consistency check on a
deliberate whole-column sweep. It is not usable on a partial field, it cannot say which vertebra is
extra, and no figure should imply that it can.

## What was used as truth

The raw VerSe label volumes under `VerSeFusion/data/unified` (374 scans, VerSe's own numbering, 25 = L6
and 28 = T13), not the render annotations. The renders drop any silhouette under `MIN_PIX = 60 px`
(`tools/make_drr_dataset.py`), so a vertebra can be in the volume and absent from the annotation. In
practice that happened **once in 374 cases**: verse753 carries a `T9` of **12 voxels**, a speck that the
renderer dropped, that sits out of anatomical order geometrically, and that a count over labels would
have counted as a vertebra. CTSpinoPelvic1K was read from its render annotations
(`~/ctsp_drr/ann`, 801 cases, Dataset813 ids, T10 down).

Two things found on the way that are not about the rule. **The render bank holds 13 exact duplicates**:
`glgl003 … glgl146` repeat `gl003 … gl146` with identical shapes and identical boxes, so `~/verse_drr`
has 387 files for 374 spines. **CTSP_COLONOG_730's levels are named T10, T11, T12, L1, L2, L4, L5** with
an ordinary step between the bodies named L2 and L4 (0.91 of its neighbours, rendered and looked at), so
either the patient has four lumbar bodies named as five or the name L3 was skipped; either way a count
over that case's names is not a count of its bodies.

## 1. Where the rule can be computed at all

A case counts as computable when the rostral anchor (C2) is in the field, the column reaches the
lumbosacral junction, and no body inside the run is unlabelled. Completeness is settled geometrically,
not from the name list: a box gap cannot find a missing body because posterior elements overhang the body
below and neighbouring boxes always overlap, so the test is **centre-to-centre**, each step compared with
its own neighbours (a skipped body doubles the step; observed p99 is 1.17 and the threshold is 1.6). Two
of 374 VerSe cases trip it: verse753, on the 12-voxel `T9` above, and verse097, whose cervicothoracic
junction is angulated sharply enough that a step measured along one axis is not a step along the column.
Neither is computable, so neither changes the table; the second is a limitation of this completeness test
and is recorded as one.

| corpus | spines | C2 in field | reaches sacrum | no unlabelled body | **computable** |
|---|---|---|---|---|---|
| VerSe (raw masks) | 374 | 76 (20.3 %) | 239 (63.9 %) | 372 (99.5 %) | **14 (3.7 %)** |
| CTSpinoPelvic1K (renders) | 801 | 0 | 801 | 801 | **0 (0 %)** |
| both | 1,175 | 76 | 1,040 | 1,173 | **14 (1.2 %)** |

CTSpinoPelvic1K cannot be tested with this rule at all, and not by accident: the spines are
abdominopelvic, the field starts around T10, and the label scheme has no cervical class to begin with.
A rule that needs the whole column cannot be applied to a partial field of view, and 801 of the 1,175
spines here are partial fields. The same holds for 96 % of VerSe.

**The anomalous spines are mostly out of reach.** The two corpora hold 74 transitional spines (VerSe 50
L6 and 6 T13, no case with both; CTSP 18 L6). **Four of the 74 (5.4 %)** sit in a field where the rule
could be computed.

## 2. Sensitivity and specificity where it is computable

Fourteen spines: nine structurally ordinary, five anomalous (three T13, one L6, one column of 22).

| | TP | FN | FP | TN | sensitivity | specificity |
|---|---|---|---|---|---|---|
| C1 excluded from the count (the rule as stated) | 5 | 0 | 0 | 9 | 1.000 (95 % CI 0.566–1.000) | 1.000 (0.701–1.000) |
| C1 counted, as a detector that boxes C1 does | 4 | 1 | 9 | 0 | 0.800 (0.376–0.964) | **0.000 (0.000–0.299)** |

The first row is not evidence that the rule works. With an exact count the rule and the definition of
"anomalous" are the same sentence, so the only cases that could disagree are anomalies that preserve the
count, and there were none among these fourteen. What the row does establish is the size of the test set:
five anomalous spines, an interval on sensitivity that runs from 0.57 to 1.

The second row is the trap. **C1 is labelled in every one of the 76 VerSe cases that carry C2.** The
constant 22 assumes C1 is excluded; a detector that boxes C1 counts 24 on an ordinary column and the rule
then flags every normal spine — specificity 0 of 9. The constant belongs to the counting convention, not
to anatomy, and has to be set from what the detector actually puts a node on.

## 3. Under counting error, which is the realistic case

Each of the N true bodies is missed with probability p; each contributes a spurious extra node with
probability q. The rule sees N' = N − misses + inserts and fires when N' != 23. Computed exactly by
binomial convolution and checked by 200,000 Monte Carlo draws with Wilson intervals (they agree to within
0.3 points everywhere).

False alarm on a structurally normal spine, P(N' != 23):

| p \ q | 0.00 | 0.01 | 0.02 | 0.05 | 0.10 |
|---|---|---|---|---|---|
| 0.00 | 0.0 % | 20.6 % | 37.2 % | 69.3 % | 91.1 % |
| 0.01 | 20.6 % | 33.6 % | 44.6 % | 68.3 % | 88.2 % |
| 0.02 | 37.2 % | 44.6 % | 51.4 % | 68.2 % | 85.7 % |
| 0.05 | 69.3 % | 68.3 % | 68.2 % | 71.4 % | 80.9 % |
| 0.10 | 91.1 % | 88.2 % | 85.7 % | 80.9 % | 80.1 % |

Missed anomaly, a spine with an extra vertebra (N = 24), P(N' == 23):

| p \ q | 0.00 | 0.01 | 0.02 | 0.05 | 0.10 |
|---|---|---|---|---|---|
| 0.01 | 19.0 % | 15.4 % | 12.4 % | 6.4 % | 2.0 % |
| 0.02 | 30.2 % | 25.1 % | 20.8 % | 11.7 % | 4.2 % |
| 0.05 | 36.9 % | 33.4 % | 30.1 % | 21.1 % | 10.6 % |
| 0.10 | 21.3 % | 22.4 % | 23.0 % | 22.4 % | 17.2 % |

A missing vertebra (N = 22) is never missed when q = 0 and is missed in up to 37.5 % of cases once the
detector invents nodes, because an insertion restores the count. Over the real computable cohort, whose
N is 22, 23 or 24 rather than always 23, the false alarm is 20.6 % at p = 0.01 and 37.2 % at p = 0.02 and
the missed-anomaly rate is 15.2 % and 24.1 %.

Read the other way: **holding the false alarm at 5 % on a 23-body column needs p <= 0.223 %**, that is,
the chain must come out complete on 95 % of whole columns; 1 % false alarm needs p <= 0.044 %. Those are
the numbers to compare against what this project has actually measured for chain completeness
(`docs/SWEEP_PROTOCOL.md`): 95 % of chains complete on 203 C2-anchored TotalSegmentator scans, 98.5 % on
522 spines with the fixed-step protocol, 120 of 120 abdominopelvic, every one of 12 whole-spine scans. On
the C2 sweep, which is the one this rule needs, the measured completeness implies a false-alarm rate of
about 5 % before any spurious node is counted — on rendered CT, not on real intraoperative frames.

The model assumes misses are independent across the 23 links. They are not: the measured failures cluster
by region, cervical worst. Independence is the convenient case, not the safe one.

## 4. What the rule cannot see

- **It localises nothing.** Five of five computable anomalous spines were flagged; **zero were
  localised**. The rule returns one integer for the whole column. Both the three T13 spines and the one
  L6 spine land in the same bin, N = 24, and nothing in the rule separates a thirteenth thoracic
  vertebra from a sixth lumbar one.
- **Transpositions pass.** R + C is invariant under any permutation of the names, so a chain whose names
  are swapped satisfies the rule exactly. This is not hypothetical: verse753's labels are out of
  anatomical order relative to the geometry.
- **An extra and a missing vertebra cancel.** A column carrying both satisfies R + C = 22. There was no
  such case among the fourteen computable spines — 0 of 5 anomalous — which bounds nothing at that sample
  size, and the thoracolumbar and lumbosacral border variants are known to co-occur in this data
  (`tools/anomaly_cooccurrence.py`).
- **A skipped name is not a missing body.** Eight VerSe columns are named T11 then L1 across an ordinary
  disc (verse544, verse559, verse581, verse606, verse626, verse636, verse642, verse814; the T11-to-L1
  step is 0.94–1.09 of its neighbouring steps, and two were rendered and looked at). The rule fires on
  them and the count of 22 is right, but whether those are patients with eleven thoracic vertebrae or an
  annotation convention cannot be decided from the labels. One of them, verse581, is in the computable
  fourteen and is the only "missing vertebra" case in the confusion table above.

## Where the rule is usable, and where it is not

**Usable** as a consistency check on a deliberate whole-column sweep from C2 to the sacrum, where it
costs nothing and catches a chain that came out the wrong length. Its false-alarm rate there is the
chain-incompleteness rate, which is measured, and its constant must match the counting convention
(23 bodies excluding C1, 24 including it).

**Not usable** on a partial field — 0 of 801 abdominopelvic spines and 96 % of VerSe — which is most of
the intended clinical setting, where the C-arm sees a few vertebrae. **Not usable** as an anomaly
detector with a quotable sensitivity: the test set here is five spines. **Not usable** to say which
vertebra is the extra one, which is the question a surgeon at the lumbosacral junction is actually
asking.

**If a figure quotes the rule** it must show a whole column, must not draw it as a per-frame test, and
must not imply it names the anomalous level.

## Not known

- Whether the eight T11-then-L1 columns are eleven-thoracic patients or an annotation convention. The
  labels cannot settle it; ribs or a radiologist read could.
- The per-vertebra miss rate on real intraoperative C-arm frames. Every completeness number quoted above
  comes from rendered CT.
- The population rate of count-preserving anomalies. Zero of fourteen complete columns is not a bound.

## Reproduce

```
sbatch -D /wsu/home/go/go24/go2432/spinesurg-ct-nnunet slurm/eval_anomaly_rule.sh
# or, with the mask inventory already on hand:
python tools/eval_anomaly_rule.py eval --verse-masks verse_mask_levels.json \
    --verse-ann ~/verse_drr/ann --ctsp-ann ~/ctsp_drr/ann --out docs/anomaly_rule_evaluation.json
```

Keys a figure row can read from the JSON: `headline` (computable fraction, the three false-alarm rates,
the p for a 5 % false alarm), `corpora.<name>` (per-corpus computability), `computable_cases` (the
fourteen, with names and truth), `confusion` (both C1 conventions), `counting_error.false_alarm` and
`counting_error.miss_L6_or_T13` (keyed `"p,q"`), and `blind_spot.bins` (which phenotypes share a count).
