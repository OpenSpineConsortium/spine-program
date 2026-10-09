
## 2026-09-22 05:30 EDT — session resumed after the token limit; agents died, grid jobs finished
AUDIT TRACK (or_ready/audit/AUDIT.md; docs/or_ready_audit_track_2026-09-22.json): splits disjoint everywhere; no
real frame in any training corpus; pose QC clean. DEFECTS OF CLAIM: (1) every rx_* detector was initialised from
anchor_none_v2_17-1882, whose training renders were 44.8 % under test specimen 18-1109's POSES and whose nine terms
were fitted on real frames incl. all 104 of 18-1109 -> any rx_* number on 18-1109 carries geometry/pixel-statistics
exposure. (2) TWO GENERATIONS: the manuscript's 76.9 % is anchor_none_r2; the v2 (OR-window) generation pools to
64.0 % at 0.05 / 54.3 % at 0.25; render-only with 18-1109 truly held out (v2, 3 seeds) 88.5-91.3 % at 0.05. Claims
must name the generation. (3) lodo runs selected best.pt on the training devices' TEST splits: only the held-out
device's numbers are clean. (4) COBRA 74,364 cross-case near-duplicate laterals = positional prior.
LODO results (rx_lodo_*): C-ArmLSpine held out -> sacrum 83.9 %, vertebra recall 5.2 % (box-convention suspect:
C-ArmLSpine truth = vertebral BODY boxes, COBRA/DeepFluoro truth = whole-vertebra boxes); DeepFluoro held out ->
sacrum 100 %, vertebra 95.2 % (but init exposure above); COBRA held out -> 13.3 % (laterals blank; 43 % near-AP).
DeepFluoro vendor DICOMs: 36 GB complete (DFVENDOR_DONE). Thoracic (AASCE fetched, results in or_ready/thoracic),
robust, crossdev, spinesac partial outputs on disk; wholespine ws_mixed still training (40411495).
