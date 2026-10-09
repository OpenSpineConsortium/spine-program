# Naming a vertebra from less and less of the spine

Question: how much of the spine must be visible in a 2-D lateral image for a model to name a vertebra, down to one vertebra alone -- and does anything learned on projected CT survive contact with a real film.

Conventions. Levels are expert-annotated (VerSe, CTSpinoPelvic1K, NHANES); BUU-LSPINE was excluded because its levels were assigned by counting, the assumption under test. The target vertebra is always scaled to the same pixel height, so absolute size is withheld and every number is a lower bound on what a size-aware model could do. **mask** arms zero everything outside the visible vertebrae (the pure ablation); **fov** arms show a collimated band with everything in it visible, which is what a fluoroscopy frame is. Splits are by patient. 27 classes (C1–L6, T13, sacrum); the majority and chance columns are the floors to read against.

## 1. The context ladders (image, ResNet-18, held-out patients)


### VerSe only, mask, 22 px

| visible | n | exact level | within one | region | majority | chance |
|---|---|---|---|---|---|---|
| all vertebrae in the scan | 869 | **82.7%** | 97.9% | 98.3% | 7.4% | 3.8% |
| 17 vertebrae (rung 8) | 869 | **81.4%** | 98.0% | 97.7% | 7.4% | 3.8% |
| 13 vertebrae (rung 6) | 869 | **81.7%** | 98.2% | 97.7% | 7.4% | 3.8% |
| 9 vertebrae (rung 4) | 869 | **79.3%** | 97.9% | 97.7% | 7.4% | 3.8% |
| 7 vertebrae (rung 3) | 869 | **78.0%** | 97.9% | 97.7% | 7.4% | 3.8% |
| 5 vertebrae (rung 2) | 869 | **75.6%** | 97.2% | 97.0% | 7.4% | 3.8% |
| 3 vertebrae (rung 1) | 869 | **73.3%** | 96.8% | 97.0% | 7.4% | 3.8% |
| 1 vertebra (rung 0) | 869 | **63.5%** | 92.4% | 95.4% | 7.4% | 3.8% |

### VerSe + CTSpinoPelvic1K (302 of 802), mask, 22 px

| visible | n | exact level | within one | region | majority | chance |
|---|---|---|---|---|---|---|
| all vertebrae in the scan | 1468 | **88.2%** | 98.8% | 98.6% | 8.0% | 3.7% |
| 17 vertebrae (rung 8) | 1468 | **88.8%** | 98.9% | 98.4% | 8.0% | 3.7% |
| 13 vertebrae (rung 6) | 1468 | **88.8%** | 99.2% | 98.9% | 8.0% | 3.7% |
| 9 vertebrae (rung 4) | 1468 | **87.1%** | 98.7% | 98.4% | 8.0% | 3.7% |
| 7 vertebrae (rung 3) | 1468 | **86.0%** | 98.5% | 98.0% | 8.0% | 3.7% |
| 5 vertebrae (rung 2) | 1468 | **84.1%** | 97.7% | 97.3% | 8.0% | 3.7% |
| 3 vertebrae (rung 1) | 1468 | **80.9%** | 97.5% | 97.5% | 8.0% | 3.7% |
| 1 vertebra (rung 0) | 1468 | **70.6%** | 95.7% | 96.5% | 8.0% | 3.7% |

per corpus, exact level:

| visible | ctsp_drr | verse_drr |
|---|---|---|
| all vertebrae in the scan | 95.7% (n=535) | 83.9% (n=933) |
| 17 vertebrae (rung 8) | 96.1% (n=535) | 84.6% (n=933) |
| 13 vertebrae (rung 6) | 97.4% (n=535) | 83.8% (n=933) |
| 9 vertebrae (rung 4) | 96.6% (n=535) | 81.7% (n=933) |
| 7 vertebrae (rung 3) | 95.0% (n=535) | 80.9% (n=933) |
| 5 vertebrae (rung 2) | 92.5% (n=535) | 79.3% (n=933) |
| 3 vertebrae (rung 1) | 91.6% (n=535) | 74.7% (n=933) |
| 1 vertebra (rung 0) | 78.5% (n=535) | 66.0% (n=933) |

### VerSe + CTSpinoPelvic1K (all 802), mask, 22 px

| visible | n | exact level | within one | region | majority | chance |
|---|---|---|---|---|---|---|
| all vertebrae in the scan | 2304 | **91.8%** | 99.0% | 99.0% | 9.6% | 3.7% |
| 17 vertebrae (rung 8) | 2304 | **90.6%** | 99.0% | 98.8% | 9.6% | 3.7% |
| 13 vertebrae (rung 6) | 2304 | **90.6%** | 98.6% | 98.7% | 9.6% | 3.7% |
| 9 vertebrae (rung 4) | 2304 | **90.8%** | 98.6% | 98.9% | 9.6% | 3.7% |
| 7 vertebrae (rung 3) | 2304 | **90.0%** | 98.3% | 98.5% | 9.6% | 3.7% |
| 5 vertebrae (rung 2) | 2304 | **87.5%** | 97.2% | 97.5% | 9.6% | 3.7% |
| 3 vertebrae (rung 1) | 2304 | **84.2%** | 96.8% | 97.8% | 9.6% | 3.7% |
| 1 vertebra (rung 0) | 2304 | **73.7%** | 94.1% | 96.3% | 9.6% | 3.7% |

per corpus, exact level:

| visible | ctsp_drr | verse_drr |
|---|---|---|
| all vertebrae in the scan | 96.4% (n=1433) | 84.4% (n=871) |
| 17 vertebrae (rung 8) | 95.3% (n=1433) | 83.0% (n=871) |
| 13 vertebrae (rung 6) | 96.0% (n=1433) | 81.7% (n=871) |
| 9 vertebrae (rung 4) | 96.7% (n=1433) | 81.1% (n=871) |
| 7 vertebrae (rung 3) | 96.7% (n=1433) | 79.1% (n=871) |
| 5 vertebrae (rung 2) | 94.5% (n=1433) | 75.9% (n=871) |
| 3 vertebrae (rung 1) | 91.7% (n=1433) | 71.9% (n=871) |
| 1 vertebra (rung 0) | 81.3% (n=1433) | 61.2% (n=871) |

### VerSe only, mask, 48 px

| visible | n | exact level | within one | region | majority | chance |
|---|---|---|---|---|---|---|
| 5 vertebrae (rung 2) | 869 | **79.9%** | 98.2% | 98.5% | 7.4% | 3.8% |
| 3 vertebrae (rung 1) | 869 | **76.8%** | 97.8% | 97.9% | 7.4% | 3.8% |
| 1 vertebra (rung 0) | 869 | **68.6%** | 95.4% | 96.0% | 7.4% | 3.8% |

### VerSe only, fov, 48 px

| visible | n | exact level | within one | region | majority | chance |
|---|---|---|---|---|---|---|
| all vertebrae in the scan | 869 | **85.6%** | 99.0% | 98.8% | 7.4% | 3.8% |
| 7 vertebrae (rung 3) | 869 | **85.0%** | 98.4% | 98.0% | 7.4% | 3.8% |
| 5 vertebrae (rung 2) | 869 | **82.9%** | 98.5% | 98.4% | 7.4% | 3.8% |
| 3 vertebrae (rung 1) | 869 | **80.1%** | 98.7% | 98.6% | 7.4% | 3.8% |
| 1 vertebra (rung 0) | 869 | **72.6%** | 96.2% | 96.7% | 7.4% | 3.8% |

### VerSe + NHANES films in loop, fov, 48 px

| visible | n | exact level | within one | region | majority | chance |
|---|---|---|---|---|---|---|
| 7 vertebrae (rung 3) | 1740 | **90.1%** | 98.9% | 98.6% | 8.1% | 3.8% |
| 5 vertebrae (rung 2) | 1740 | **88.5%** | 98.4% | 98.5% | 8.1% | 3.8% |
| 3 vertebrae (rung 1) | 1740 | **86.4%** | 98.3% | 98.2% | 8.1% | 3.8% |
| 1 vertebra (rung 0) | 1740 | **77.2%** | 96.8% | 97.1% | 8.1% | 3.8% |

per corpus, exact level:

| visible | nhanes_drr | verse_drr |
|---|---|---|
| 7 vertebrae (rung 3) | 94.6% (n=871) | 85.6% (n=869) |
| 5 vertebrae (rung 2) | 93.9% (n=871) | 83.1% (n=869) |
| 3 vertebrae (rung 1) | 90.4% (n=871) | 82.4% (n=869) |
| 1 vertebra (rung 0) | 84.2% (n=871) | 70.2% (n=869) |

### VerSe + NHANES films in loop, mask, 22 px

| visible | n | exact level | within one | region | majority | chance |
|---|---|---|---|---|---|---|
| all vertebrae in the scan | 1740 | **88.6%** | 98.6% | 98.4% | 8.1% | 3.8% |
| 9 vertebrae (rung 4) | 1740 | **87.5%** | 98.2% | 97.9% | 8.1% | 3.8% |
| 5 vertebrae (rung 2) | 1740 | **82.8%** | 96.7% | 97.1% | 8.1% | 3.8% |
| 3 vertebrae (rung 1) | 1740 | **78.4%** | 96.1% | 96.7% | 8.1% | 3.8% |
| 1 vertebra (rung 0) | 1740 | **58.0%** | 88.0% | 94.4% | 8.1% | 3.8% |

per corpus, exact level:

| visible | nhanes_drr | verse_drr |
|---|---|---|
| all vertebrae in the scan | 97.1% (n=871) | 80.0% (n=869) |
| 9 vertebrae (rung 4) | 96.0% (n=871) | 78.9% (n=869) |
| 5 vertebrae (rung 2) | 91.5% (n=871) | 74.0% (n=869) |
| 3 vertebrae (rung 1) | 83.4% (n=871) | 73.5% (n=869) |
| 1 vertebra (rung 0) | 54.3% (n=871) | 61.7% (n=869) |

### VerSe soft-tissue DRR, fov, 48 px

| visible | n | exact level | within one | region | majority | chance |
|---|---|---|---|---|---|---|
| 5 vertebrae (rung 2) | 869 | **79.7%** | 97.6% | 97.7% | 7.4% | 3.8% |
| 1 vertebra (rung 0) | 869 | **63.3%** | 91.8% | 96.0% | 7.4% | 3.8% |

## 2. Where a single vertebra fails

**VerSe only, mask, 22 px** — signed error at n=1: -2: 2.9%, -1: 13.0%, +0: 63.5%, +1: 15.9%, +2: 1.6%, other: 3.1%
most confused: L2→L3 (18); L3→L2 (12); L4→L5 (11); L5→L6 (11); L4→L3 (11); L1→L2 (11); L2→L1 (10); T12→T11 (10)
by region: cervical 67.9%, thoracic 63.8%, lumbar 62.0%

**VerSe + CTSpinoPelvic1K (302 of 802), mask, 22 px** — signed error at n=1: -2: 1.4%, -1: 10.1%, +0: 70.6%, +1: 15.0%, +2: 1.2%, other: 1.8%
most confused: L3→L2 (34); L5→L6 (27); T10→T11 (23); L2→L1 (17); T11→T12 (15); L1→T12 (14, non-adjacent); T11→T10 (14); L2→L3 (13)
by region: cervical 63.7%, thoracic 67.6%, lumbar 73.0%, sacrum 98.3%

**VerSe + CTSpinoPelvic1K (all 802), mask, 22 px** — signed error at n=1: -2: 1.8%, -1: 9.5%, +0: 73.7%, +1: 10.9%, +2: 1.6%, other: 2.5%
most confused: T10→T11 (39); L3→L2 (38); L5→L6 (33); T12→T11 (31); L1→L2 (30); L3→L4 (30); L2→L1 (22); L2→L3 (19)
by region: cervical 72.6%, thoracic 68.2%, lumbar 74.8%, sacrum 99.4%

**VerSe only, mask, 48 px** — signed error at n=1: -2: 1.4%, -1: 14.3%, +0: 68.6%, +1: 12.5%, +2: 0.6%, other: 2.6%
most confused: L3→L2 (13); L4→L3 (12); T6→T7 (11); L1→L2 (11); T12→T11 (11); L6→L5 (9); T9→T8 (9); T2→T3 (8)
by region: cervical 66.7%, thoracic 67.5%, lumbar 70.7%

**VerSe only, fov, 48 px** — signed error at n=1: -2: 1.7%, -1: 12.2%, +0: 72.6%, +1: 11.4%, +2: 0.5%, other: 1.6%
most confused: L3→L2 (18); L5→L4 (10); L1→T12 (10, non-adjacent); L4→L3 (10); L3→L4 (9); T10→T11 (8); T12→T11 (8); L2→L3 (7)
by region: cervical 65.5%, thoracic 74.8%, lumbar 71.3%

**VerSe + NHANES films in loop, fov, 48 px** — signed error at n=1: -2: 1.5%, -1: 9.5%, +0: 77.2%, +1: 10.1%, +2: 1.0%, other: 0.7%
most confused: L3→L2 (28); L3→L4 (24); L1→T12 (20, non-adjacent); L2→L1 (19); L4→L3 (16); L2→L3 (15); L4→L5 (15); C4→C5 (14)
by region: cervical 84.7%, thoracic 74.0%, lumbar 74.2%

**VerSe + NHANES films in loop, mask, 22 px** — signed error at n=1: -2: 3.2%, -1: 13.3%, +0: 58.0%, +1: 16.7%, +2: 3.6%, other: 5.3%
most confused: C4→C3 (40); L3→L4 (36); L2→L3 (33); C5→C6 (31); C6→C7 (31); L2→L1 (28); L4→L5 (26); L3→L2 (24)
by region: cervical 58.7%, thoracic 64.1%, lumbar 52.9%

**VerSe soft-tissue DRR, fov, 48 px** — signed error at n=1: -2: 3.0%, -1: 15.0%, +0: 63.3%, +1: 13.6%, +2: 2.2%, other: 3.0%
most confused: L3→L2 (19); L5→L4 (13); L4→L3 (13); L1→T12 (12, non-adjacent); L2→L3 (11); T10→T11 (10); L5→L6 (10); T12→T11 (10)
by region: cervical 59.5%, thoracic 68.1%, lumbar 57.3%

## 3. Tuning at n=1 (VerSe only, mask, 22 px; single-change arms)

| arm | exact | within one | region |
|---|---|---|---|
| baseline: 40 ep, lr 3e-4, augmentation on | **63.5%** | 92.4% | 95.4% |
| 80 epochs | **63.8%** | 93.6% | 95.4% |
| lr 1e-3 | **60.2%** | 91.3% | 93.7% |
| no augmentation | **65.5%** | 94.7% | 96.9% |
| 80 epochs + lr 1e-3 | **62.7%** | 92.1% | 95.2% |

None of these moves n=1 by more than the noise; the ceiling is in the data and the representation, not the optimiser. Augmentation costs ~2 points on synthetic validation, which is the expected price of being built for the real-film gap.

## 4. Architecture arms (same crops, split and augmentation; only the backbone differs)

| arm | visible | backbone | exact | within one | region |
|---|---|---|---|---|---|
| VerSe only, mask, 22 px | 1 vertebra (rung 0) | resnet18 | **63.5%** | 92.4% | 95.4% |
| VerSe only, mask, 22 px | 5 vertebrae (rung 2) | resnet18 | **75.6%** | 97.2% | 97.0% |
| VerSe + CTSpinoPelvic1K (302 of 802), mask, 22 px | 1 vertebra (rung 0) | resnet18 | **70.6%** | 95.7% | 96.5% |
| VerSe + CTSpinoPelvic1K (302 of 802), mask, 22 px | 1 vertebra (rung 0) | resnet50 | **71.0%** | 95.2% | 96.3% |
| VerSe + CTSpinoPelvic1K (302 of 802), mask, 22 px | 1 vertebra (rung 0) | convnext_tiny (diverged to the majority class) | **8.0%** | 15.9% | 39.4% |
| VerSe + CTSpinoPelvic1K (302 of 802), mask, 22 px | 5 vertebrae (rung 2) | resnet18 | **84.1%** | 97.7% | 97.3% |
| VerSe + CTSpinoPelvic1K (302 of 802), mask, 22 px | 5 vertebrae (rung 2) | resnet50 | **86.0%** | 98.4% | 98.0% |
| VerSe + CTSpinoPelvic1K (302 of 802), mask, 22 px | 5 vertebrae (rung 2) | convnext_tiny (diverged to the majority class) | **8.0%** | 15.9% | 39.4% |
| VerSe + CTSpinoPelvic1K (all 802), mask, 22 px | 1 vertebra (rung 0) | resnet18 | **73.7%** | 94.1% | 96.3% |
| VerSe + CTSpinoPelvic1K (all 802), mask, 22 px | 1 vertebra (rung 0) | resnet50 | **72.8%** | 94.1% | 95.5% |
| VerSe + CTSpinoPelvic1K (all 802), mask, 22 px | 1 vertebra (rung 0) | convnext_tiny (diverged to the majority class) | **9.6%** | 28.8% | 48.5% |
| VerSe + CTSpinoPelvic1K (all 802), mask, 22 px | 5 vertebrae (rung 2) | resnet18 | **87.5%** | 97.2% | 97.5% |
| VerSe + CTSpinoPelvic1K (all 802), mask, 22 px | 5 vertebrae (rung 2) | resnet50 | **88.5%** | 98.1% | 98.1% |
| VerSe + CTSpinoPelvic1K (all 802), mask, 22 px | 5 vertebrae (rung 2) | convnext_tiny | **69.1%** | 88.5% | 90.6% |
| VerSe only, mask, 48 px | 1 vertebra (rung 0) | resnet18 | **68.6%** | 95.4% | 96.0% |
| VerSe only, mask, 48 px | 5 vertebrae (rung 2) | resnet18 | **79.9%** | 98.2% | 98.5% |
| VerSe only, fov, 48 px | 1 vertebra (rung 0) | resnet18 | **72.6%** | 96.2% | 96.7% |
| VerSe only, fov, 48 px | 5 vertebrae (rung 2) | resnet18 | **82.9%** | 98.5% | 98.4% |
| VerSe + NHANES films in loop, fov, 48 px | 1 vertebra (rung 0) | resnet18 | **77.2%** | 96.8% | 97.1% |
| VerSe + NHANES films in loop, fov, 48 px | 5 vertebrae (rung 2) | resnet18 | **88.5%** | 98.4% | 98.5% |
| VerSe + NHANES films in loop, mask, 22 px | 1 vertebra (rung 0) | resnet18 | **58.0%** | 88.0% | 94.4% |
| VerSe + NHANES films in loop, mask, 22 px | 5 vertebrae (rung 2) | resnet18 | **82.8%** | 96.7% | 97.1% |
| VerSe soft-tissue DRR, fov, 48 px | 1 vertebra (rung 0) | resnet18 | **63.3%** | 91.8% | 96.0% |
| VerSe soft-tissue DRR, fov, 48 px | 5 vertebrae (rung 2) | resnet18 | **79.7%** | 97.6% | 97.7% |

## 5. Outline only: the contour arm (one vertebra, no image)

| test set | n | exact | within one | region | majority |
|---|---|---|---|---|---|
| contour n=1, held-out cases | 2302 | **72.5%** | 95.0% | 94.9% | 9.6% |
| contour n=1, contours_nhanes (never seen) | 3053 | **0.1%** | 2.8% | 6.2% | 9.0% |

128 points on the silhouette, centred and unit-scaled: shape and nothing else. Read the image arm's n=1 against this: the difference is what the pixels carry that the outline does not.

**The NHANES row is not a generalisation result.** VerSe and CTSpinoPelvic1K label the whole vertebra, so their silhouettes include the arch and spinous process; NHANES masks the vertebral body alone. Those are different shapes, and a classifier of one has never seen the other. The near-zero score measures that mismatch, not the domain gap. A body-only contour arm on the CT side would be the valid comparison and was not built tonight.

## 6. Real films (NHANES II, annotated levels)

Two different questions, kept apart:

**6a. Transfer without ever seeing a film.** Models trained on projected CT, scored on NHANES cropped by the same rule. The first attempt used 22 px body-only patches on black and scored 3–20% with region *below chance* — the render showed that as a representation mismatch (NHANES annotates the body, VerSe the whole vertebra; 22 px carries no film texture), so those numbers are reported here as what they are, and the matched-construction arms follow.

| arm | visible | n films | exact | within one | region |
|---|---|---|---|---|---|
| VerSe only, mask, 22 px | all vertebrae in the scan | 2061 | **14.4%** | 27.8% | 42.7% |
| VerSe only, mask, 22 px | 17 vertebrae (rung 8) | 2061 | **5.5%** | 22.6% | 53.9% |
| VerSe only, mask, 22 px | 13 vertebrae (rung 6) | 2061 | **17.9%** | 39.0% | 48.6% |
| VerSe only, mask, 22 px | 9 vertebrae (rung 4) | 2061 | **20.2%** | 36.3% | 40.7% |
| VerSe only, mask, 22 px | 7 vertebrae (rung 3) | 2061 | **15.6%** | 26.6% | 32.8% |
| VerSe only, mask, 22 px | 5 vertebrae (rung 2) | 2061 | **8.2%** | 15.6% | 16.8% |
| VerSe only, mask, 22 px | 3 vertebrae (rung 1) | 2061 | **10.0%** | 19.5% | 22.8% |
| VerSe only, mask, 22 px | 1 vertebra (rung 0) | 2061 | **2.7%** | 7.1% | 9.9% |
| VerSe + CTSpinoPelvic1K (302 of 802), mask, 22 px | all vertebrae in the scan | 3033 | **14.0%** | 38.7% | 46.2% |
| VerSe + CTSpinoPelvic1K (302 of 802), mask, 22 px | 17 vertebrae (rung 8) | 3033 | **7.7%** | 23.4% | 41.6% |
| VerSe + CTSpinoPelvic1K (302 of 802), mask, 22 px | 13 vertebrae (rung 6) | 3033 | **12.6%** | 24.8% | 31.9% |
| VerSe + CTSpinoPelvic1K (302 of 802), mask, 22 px | 9 vertebrae (rung 4) | 3033 | **21.0%** | 41.3% | 50.6% |
| VerSe + CTSpinoPelvic1K (302 of 802), mask, 22 px | 7 vertebrae (rung 3) | 3033 | **14.6%** | 27.0% | 32.1% |
| VerSe + CTSpinoPelvic1K (302 of 802), mask, 22 px | 5 vertebrae (rung 2) | 3033 | **13.7%** | 25.9% | 33.9% |
| VerSe + CTSpinoPelvic1K (302 of 802), mask, 22 px | 3 vertebrae (rung 1) | 3033 | **13.9%** | 21.4% | 30.0% |
| VerSe + CTSpinoPelvic1K (302 of 802), mask, 22 px | 1 vertebra (rung 0) | 3033 | **1.4%** | 2.9% | 6.8% |
| VerSe + CTSpinoPelvic1K (all 802), mask, 22 px | all vertebrae in the scan | 3053 | **2.9%** | 9.0% | 26.1% |
| VerSe + CTSpinoPelvic1K (all 802), mask, 22 px | 17 vertebrae (rung 8) | 3053 | **2.0%** | 10.6% | 25.8% |
| VerSe + CTSpinoPelvic1K (all 802), mask, 22 px | 13 vertebrae (rung 6) | 3053 | **6.0%** | 13.5% | 21.7% |
| VerSe + CTSpinoPelvic1K (all 802), mask, 22 px | 9 vertebrae (rung 4) | 3053 | **12.2%** | 23.9% | 34.7% |
| VerSe + CTSpinoPelvic1K (all 802), mask, 22 px | 7 vertebrae (rung 3) | 3053 | **20.0%** | 30.6% | 45.1% |
| VerSe + CTSpinoPelvic1K (all 802), mask, 22 px | 5 vertebrae (rung 2) | 3053 | **9.6%** | 22.8% | 37.4% |
| VerSe + CTSpinoPelvic1K (all 802), mask, 22 px | 3 vertebrae (rung 1) | 3053 | **18.8%** | 31.6% | 55.3% |
| VerSe + CTSpinoPelvic1K (all 802), mask, 22 px | 1 vertebra (rung 0) | 3053 | **1.9%** | 4.8% | 10.0% |
| VerSe only, fov, 48 px | all vertebrae in the scan | 3053 | **15.4%** | 45.7% | 60.0% |
| VerSe only, fov, 48 px | 7 vertebrae (rung 3) | 3053 | **11.3%** | 29.8% | 34.9% |
| VerSe only, fov, 48 px | 5 vertebrae (rung 2) | 3053 | **12.6%** | 37.2% | 44.2% |
| VerSe only, fov, 48 px | 3 vertebrae (rung 1) | 3053 | **21.1%** | 50.0% | 63.7% |
| VerSe only, fov, 48 px | 1 vertebra (rung 0) | 3053 | **7.4%** | 13.3% | 21.5% |
| VerSe soft-tissue DRR, fov, 48 px | 5 vertebrae (rung 2) | 3053 | **27.5%** | 52.2% | 73.5% |
| VerSe soft-tissue DRR, fov, 48 px | 1 vertebra (rung 0) | 3053 | **10.8%** | 29.0% | 41.4% |

**6b. Real films in the training loop.** NHANES split by patient (30% of patients held out, both their films), joined to the synthetic crops, one model per rung. The held-out films are scored by the same model, so this is real-film accuracy with real films seen in training -- the number that says whether the approach can work on film at all, as opposed to whether CT alone transfers.

| arm | visible | held-out film crops | exact | within one | synthetic val, same model |
|---|---|---|---|---|---|
| VerSe + NHANES films in loop, fov, 48 px | 7 vertebrae (rung 3) | 871 | **94.6%** | 98.7% | 85.6% |
| VerSe + NHANES films in loop, fov, 48 px | 5 vertebrae (rung 2) | 871 | **93.9%** | 98.6% | 83.1% |
| VerSe + NHANES films in loop, fov, 48 px | 3 vertebrae (rung 1) | 871 | **90.4%** | 98.4% | 82.4% |
| VerSe + NHANES films in loop, fov, 48 px | 1 vertebra (rung 0) | 871 | **84.2%** | 97.5% | 70.2% |
| VerSe + NHANES films in loop, mask, 22 px | all vertebrae in the scan | 871 | **97.1%** | 99.4% | 80.0% |
| VerSe + NHANES films in loop, mask, 22 px | 9 vertebrae (rung 4) | 871 | **96.0%** | 98.7% | 78.9% |
| VerSe + NHANES films in loop, mask, 22 px | 5 vertebrae (rung 2) | 871 | **91.5%** | 97.4% | 74.0% |
| VerSe + NHANES films in loop, mask, 22 px | 3 vertebrae (rung 1) | 871 | **83.4%** | 96.3% | 73.5% |
| VerSe + NHANES films in loop, mask, 22 px | 1 vertebra (rung 0) | 871 | **54.3%** | 84.2% | 61.7% |

## 7. A data-integrity finding

`gzip -t` over all 802 CT volumes in the grid copy of CTSpinoPelvic1K found **1 truncated file(s)**: 0533_ct.nii.gz. 0533_ct.nii.gz is 17 MB where its neighbours are ~260 MB (an aborted transfer, dated 2026-06-25). It maps to COLONOG_378. Nothing downstream noticed until a job read it; check the released copy.

## 8. What these numbers can and cannot support

- **Can:** how exact-level accuracy falls with visible context on held-out patients, with size withheld; that region survives when ordinal position is gone; whether outline alone carries identity; how much of any of it survives contact with real film, and what real films in training buy back.
- **Cannot:** clinical validation. No number here is a claim about intra-operative safety. NHANES is 1970s film in flexion, not fluoroscopy; its annotation is body-only, which is not the whole-vertebra region the CT sources label.
- **Chance is not 1/27.** Each validation set holds a subset of levels; use the printed floors.