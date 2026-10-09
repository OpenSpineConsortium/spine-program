# Labellers A and B on CTSpinoPelvic1K, before and after the 2026-09-24 COBRA rules

Built by `tools/harvest_cobra_validation.py`. Before = the per-case jsons of 2026-09-23 (`validate_a_ctsp/`, `validate_b_ctsp/`); after = the same CTs through the current code (`validate_a_ctsp_v2/`, `validate_b_ctsp_v2/`). A counts where it names two thoracic vertebrae and a sacrum, after the id guard; B counts where its reference is established.

Against reader truth (two-reader Castellvi consensus + release lumbar ids; 18 L6):

| | before | after |
|---|---|---|
| CTs | 802 | 802 |
| A counts | 789 | 772 |
| B counts | 799 | 732 |
| B: six / of them L6 | 51 / 11 | 19 / 10 |
| B: ordinary counted 5 / 4 / 6 | 657/747 / 48 / 40 | 668/686 / 8 / 9 |
| A: six / of them L6 | 18 / 9 | 13 / 7 |
| A: ordinary counted 5 / 4 / 6 | 712/739 / 18 / 9 | 700/724 / 18 / 6 |
| both count / agree | 786 / 664 | 719 / 667 |
| **two-labeller L6 / of them L6** (Wilson 95 %) | **12 / 6** ([25.4, 74.6]) | **7 / 5** ([35.9, 91.8]) |
| two-labeller L6 that are not L6 | 0105, 0419, 0474, 0672, 0895, 1151 | 0090, 0474 |
| L6 reaching the two-labeller tier | 6 of 18 ([16.3, 56.3]) | 5 of 18 ([12.5, 50.9]) |
| two-labeller four / on ordinary spines | 13 / 1 ({'sacralised_L5_fused': 3, 'lumbar_rib': 6, 'ordinary': 1, 'unassigned': 3}) | 9 / 1 ({'sacralised_L5_fused': 2, 'ordinary': 1, 'lumbar_rib': 4, 'unassigned': 2}) |
| ordinary: both count / agree on 5 | 736 / 630 | 677 / 643 |

The reader truth names only the release's own L6 ids and the readers' Castellvi calls. The CTSP stream found eleven more L6 in it (nine with six rib-free vertebrae by the release's own voxels, two hidden by release labelling defects: SchwingNet/results/transitional_registry/ctsp/SUMMARY.md), so a 'two-labeller L6 that is not L6' above can be a registry L6; the registry table below is the better reference.

Against the CTSP registry (reads + release + three body labellers on the release's student-reviewed ribs; 29 L6):

| | before | after |
|---|---|---|
| CTs | 802 | 802 |
| A counts | 789 | 772 |
| B counts | 799 | 732 |
| B: six / of them L6 | 51 / 20 | 19 / 15 |
| B: ordinary counted 5 / 4 / 6 | 655/735 / 47 / 31 | 667/679 / 7 / 4 |
| A: six / of them L6 | 18 / 15 | 13 / 12 |
| A: ordinary counted 5 / 4 / 6 | 707/727 / 17 / 3 | 695/713 / 17 / 1 |
| both count / agree | 786 / 664 | 719 / 667 |
| **two-labeller L6 / of them L6** (Wilson 95 %) | **12 / 11** ([64.6, 98.5]) | **7 / 7** ([64.6, 100.0]) |
| two-labeller L6 that are not L6 | 0419 | none |
| L6 reaching the two-labeller tier | 11 of 29 ([22.7, 56.0]) | 7 of 29 ([12.2, 42.1]) |
| two-labeller four / on ordinary spines | 13 / 0 ({'sacralised_L5_fused': 3, 'lumbar_rib': 6, 'unassigned': 4}) | 9 / 0 ({'sacralised_L5_fused': 2, 'unassigned': 3, 'lumbar_rib': 4}) |
| ordinary: both count / agree on 5 | 724 / 629 | 670 / 642 |

On CTSpinoPelvic1K after the change, B's split-pair rule fired on 93 CTs, the stub rule on 19; B refused an unestablished reference on 55 and a split body on 12. The stub rule was DERIVED on CTSpinoPelvic1K (19 of B's false sixes carried a short TS rib piece on the first free body), so its share of the improvement is not an independent test. The split-pair, reference and fragment rules and A's two rules were written from COBRA failures; the fragment rule's thresholds were checked here before adoption, so that one is only half independent.

**Castellvi mask morphology fails its outside check** (after the change): of 33 spines with a reader Castellvi grade above 0, A marks 15, B 29, both 15; of the reader-ordinary spines, A marks 379 of 741 measured, B 676 of 747, both 370. A screen that marks most ordinary spines assigns no subtype here.


## Refusals after the change

B:

- 23 x thoracolumbar reference not established: the object directly above the last rib-bearing on
- 3 x thoracolumbar reference not established: the last rib-bearing object [T12:89%/T11:11%] is 
- 2 x thoracolumbar reference not established: the last rib-bearing object [T12:96%/T11:4%] is c
- 2 x count refused, a split body: free body [L1:100%] is 0.27 x the median volume of the other 
- 2 x thoracolumbar reference not established: the last rib-bearing object [T12:100%/T11:0%] is 
- 2 x thoracolumbar reference not established: the last rib-bearing object [T12:83%/T11:17%] is 
- 2 x thoracolumbar reference not established: the last rib-bearing object [T12:85%/T11:15%] is 
- 2 x thoracolumbar reference not established: the last rib-bearing object [T12:88%/T11:12%] is 
- 1 x count refused, a split body: two bodies of the chain [T12:100%] and [T12:100%] are 16 mm a
- 1 x thoracolumbar reference not established: the last rib-bearing object [T12:100%] is cut by 
- 1 x thoracolumbar reference not established: the last rib-bearing object [T12:95%/T11:5%] is c
- 1 x count refused, a split body: two bodies of the chain [T12:100%] and [L1:100%] are 22 mm ap
- 1 x thoracolumbar reference not established: the last rib-bearing object [T11:55%/T10:41%/T9:4
- 1 x count refused, a split body: two bodies of the chain [L5:100%] and [L5:100%] are 20 mm apa
- 1 x thoracolumbar reference not established: the last rib-bearing object [T12:99%/T11:1%] is c
- 1 x thoracolumbar reference not established: the last rib-bearing object [T12:97%/T11:3%] is c
- 1 x count refused, a split body: free body [L2:100%] is 0.39 x the median volume of the other 
- 1 x thoracolumbar reference not established: the last rib-bearing object [T12:98%/T11:2%] is c
- 1 x count refused, a split body: two bodies of the chain [L2:100%] and [L2:100%] are 17 mm apa
- 1 x count refused, a split body: free body [L2:100%] is 0.48 x the median volume of the other 
- 1 x thoracolumbar reference not established: the last rib-bearing object [T12:57%/T11:39%/T10:
- 1 x no rib-bearing vertebra in the field: the thoracolumbar reference is cut
- 1 x thoracolumbar reference not established: the last rib-bearing object [T12:91%/T11:9%] is c
- 1 x thoracolumbar reference not established: the last rib-bearing object [T12:84%/T11:16%/T10:
- 1 x count refused, a split body: free body [L3:100%] is 0.23 x the median volume of the other 
- 1 x count refused, a split body: two bodies of the chain [L1:100%] and [L1:100%] are 15 mm apa
- 1 x thoracolumbar reference not established: the last rib-bearing object [L1:100%/T12:0%] is c
- 1 x thoracolumbar reference not established: the last rib-bearing object [T12:91%/T11:9%] is t
- 1 x thoracolumbar reference not established: the last rib-bearing object [T12:93%/T11:7%] is t
- 1 x thoracolumbar reference not established: the last rib-bearing object [L1:83%/T12:17%] is c
- 1 x count refused, a split body: free body [L2:100%] is 0.24 x the median volume of the other 
- 1 x thoracolumbar reference not established: the last rib-bearing object [T12:94%/T11:6%] is t
- 1 x thoracolumbar reference not established: the last rib-bearing object [T12:87%/T11:13%] is 
- 1 x thoracolumbar reference not established: the last rib-bearing object [T12:94%/T11:6%] is c
- 1 x thoracolumbar reference not established: the last rib-bearing object [T12:79%/T11:21%] is 
- 1 x thoracolumbar reference not established: the last rib-bearing object [T12:90%/T11:10%] is 
- 1 x count refused, a split body: free body [L2:100%] is 0.19 x the median volume of the other 
- 1 x thoracolumbar reference not established: the last rib-bearing object [L1:100%] is cut by t

A:

- 9 x VERIDAH named only one thoracic vertebra (T11, the top of the field): the thoracolumbar ju
- 4 x ctd naming failed its checks: instance 26 holds the points of L6+sacrum
- 4 x VERIDAH named only one thoracic vertebra (T12, the top of the field): the thoracolumbar ju
- 4 x VERIDAH named L6 but SPINEPS has no body for it (a sliver under 150 voxels, or no instance
- 2 x ctd naming failed its checks: instance 26 holds the points of L5+sacrum
- 2 x ctd naming failed its checks: instance 24 holds the points of L5+L6
- 2 x VERIDAH named no thoracic vertebra above the lumbar set (cranial-most named: L1): the thor
- 1 x ctd naming failed its checks: instance 26 holds the points of T9+sacrum
- 1 x ctd naming failed its checks: instance 26 holds the points of T10+sacrum
