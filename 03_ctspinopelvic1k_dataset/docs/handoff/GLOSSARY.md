# Glossary

> **Copied whole into `03_ctspinopelvic1k_dataset` on 2026-10-08.** The path prefixes this file uses (`ssn:`, `sn:`, `ctsp:`, `ostk:`, `mem:` / `context/`, `Desktop/`, `np:`, `~`, `$RS`) and every laptop path it quotes resolve as `PREFIXES.md` says: to a repository at a named commit, to a file in this folder, or to the grid. Nothing in this folder depends on a laptop path (`../../MANIFEST_LOCAL.md` section 3.6).

The words a newcomer meets in this programme, each with the file that defines or uses it. Every path prefix and
identifier namespace used in the handoff is defined once, in `README.md` "Keys: path prefixes and identifier
namespaces".

## Anatomy and clinical terms

| term | meaning | source |
|---|---|---|
| level identification, level naming | saying which vertebra a body in an image is (L4, T12 ...); the naming is "exact" when the name matches truth | `sn:main.tex` |
| wrong-level surgery | an operation at the wrong vertebra; about 1 in 3,110 (Mody 2008), 12.8 / 10,000 (Jhawar 2007), 0.12 % of 34,544 (Furuya 2026) | `sn:LEVELCHECK_CLAIM.md` §2 |
| transitional anatomy, transitional vertebra | a vertebra at a junction that looks partly like its neighbour region, so counting gives the wrong name | `ctsp:CLAUDE.md` |
| LSTV | lumbosacral transitional vertebra: at the lumbar-sacral junction (sacralised L5, lumbarised S1); about 12.9 % of people (Nakagawa 2017) | `sn:LEVELCHECK_CLAIM.md` §2 |
| TLTV | thoracolumbar transitional vertebra: at the thoracic-lumbar junction (T13, lumbar ribs, stump ribs) | `context/lstv-tltv-detection-goal.md` |
| L6 | a sixth lumbar vertebra (six rib-free presacral bodies); label id 25 in VerSe-native schemes; 2-5 % prevalence window | `ssn:docs/ruleclass/PREREG_rules.md` |
| T13 | a thirteenth rib-bearing (thoracic) vertebra; label id 28; prevalence 0.37-0.88 % window; the scarcest class (no T13 crop in v9 validation) | `PREREG_rules.md`; `RESULTS_CATALOG.md` A1.8 |
| sacralised L5 / four-lumbar | the lowest lumbar body fused into the sacrum, leaving four free lumbar bodies; in CTSP 9 records, all Castellvi IIIb; the fused segment is labelled with the sacrum | `ctsp:zenodo/KNOWN_ISSUES.md` §2 |
| lumbarised S1 | the first sacral segment free, reading as a sixth lumbar body | `ctsp:results/six_lumbar_readings/report.txt` |
| Castellvi grade | the standard radiographic classification of LSTV by how the lowest transverse process meets the sacral ala (types I-IV, suffix a = one side, b = both sides; in its usual reading I is a dysplastic process, II a pseudarthrosis, III a fusion, IV mixed); the grades in this programme are the two-reader CTSP consensus (IIIb 16, IIb 6, IV 4, IIa 4, Ib 2, IIIa 1) | `ctsp:docs/castellvi_consensus.csv`; `ctsp:paper/mpda/main.tex` "Castellvi typing" (the type definitions are not restated from a file here) |
| lumbar rib | a rib on a vertebra the source named lumbar; classes 60 / 61 in v10 / v11; 16 CTSP records | `RESULTS_CATALOG.md` F.11 |
| stump rib | a hypoplastic lowest rib (lowest-rib length ratio < 0.33, or <= 38.0 mm in the pre-registration); 12.4 % of CTSP | `RESULTS_CATALOG.md` F.12; `PREREG_rules.md` rule 3 |
| rib-free count | the number of free presacral bodies between the lowest rib-bearing vertebra and the sacrum (4, 5, 6 or `no_count`); rule 1 of the pre-registration | `PREREG_rules.md` |
| junction references | the two anatomical anchors a count needs: the lowest rib-bearing vertebra and the sacrum (for L6 / four-lumbar), or the rib cage counted from T1 (for T13); a CT without both is `no_count` | `working_notes/topic2_scaling_samples_anomaly_power.md` B.1 |
| spinopelvic parameters | PI (pelvic incidence), SS (sacral slope), PT (pelvic tilt), LL (lumbar lordosis), PI-LL; PI = SS + PT by construction | `ctsp:docs/SPINOPELVIC_ESTIMATOR.md` |
| APP, aSS | anterior pelvic plane; anatomical sacral slope = SS - APP angle (not measured; the decisive open experiment) | same §5 |
| plate gate | the QC that rejects an S1 end-plate fit whose normal tilts too far or leans posteriorly; rejects 44 of 802 records | `RESULTS_CATALOG.md` F.21, F.23 |
| canal depth, end-plate width, VBHa / VBHp, EPWu / EPWl, EPD, SCW / SCD, PDW | per-level morphometry: canal anteroposterior chord, end-plate widths (upper / lower), body heights (anterior / posterior), end-plate depth, spinal canal width / depth, pedicle width | `ctsp:docs/LEVEL_MORPHOMETRY.md`; `ostk:ostk/morphometry.py` |
| Panjabi | the cadaveric normative series (Panjabi 1991, 1992) the morphometry is compared with; 1991 p. 892 Table 3 obtained 2026-09-13 | `context/panjabi-1991-page-892.md` |
| C-arm, fluoroscopy, spot frame | the mobile X-ray used in theatre; a single exposure is a spot frame; a rotational acquisition is a spin or sweep | `context/carmlspine-level-experiment.md` |
| AP, LAT (lateral) | the two standard projections; zero-shot naming is near-perfect on lateral and poor on AP | `RESULTS_CATALOG.md` A2 |
| CBCT | cone-beam CT acquired by the C-arm; the source of C-ArmLSpine truth | same |
| field of view, "in field", whole frame / three / one in field (`kfull`, `k3`, `k1`) | how many vertebrae the image shows; results are reported for the whole frame and for windows of three or one vertebra | `sn:results/eval_gate/closure/cv_v9/cv_v9.json` |

## Datasets and devices

| term | meaning | source |
|---|---|---|
| CTSpinoPelvic1K (CTSP) | Greg's CT dataset: 802 abdominopelvic records from TCIA CT COLONOGRAPHY with CTSpine1K vertebrae and CTPelvic1K pelves in one frame, plus ribs, femora, hardware, Castellvi grades | `ctsp:paper/mpda/main.tex` |
| release v10 / v11 | the label versions on Zenodo; v11 dissolved the carved S1 (id 29) back into the sacrum (26) and retired 29. Two dates: v11 was defined in the repository on 2026-09-16 (commit 73cc398, "v11: the manuscript, the scheme and the working notes stop claiming an S1"); its Zenodo record 10.5281/zenodo.22797014 was published 18 Sep 2026 (`ctsp:paper/mpda/cover_letter.md`) | `ctsp:CLAUDE.md`; `ctsp:docs/BUILD_CHAIN.md`; `git log` |
| the S1 carve, id 29 | v3-v10's automatic cut of S1 out of the sacrum; unreliable (median extent 57.6 mm against ~30); withdrawn in v11 | `RESULTS_CATALOG.md` F.5-F.7 |
| MPDA (alias MDPA) | the CTSpinoPelvic1K dataset article for Medical Physics ("Dataset and Software Article"); the handoff writes MPDA, the CTSP files themselves often write MDPA (`ctsp:paper/mpda/build.sh` "Compile the MDPA paper"; `ssn:docs/ruleclass/PREREG_rules.md` "the MDPA thoraco-lumbar shape score"; the Desktop `MDPA*.pdf`): the same article | `ctsp:paper/mpda/` |
| COLONOG fold | the CTSpine1K subset built on the TCIA CT Colonography CTs, whose vertebral masks CTSpinoPelvic1K starts from | `ctsp:docs/BUILD_CHAIN.md` L22-23 |
| CTSpine1K, CTPelvic1K | the two public annotation sets CTSP was assembled from (COLONOG fold); CTSpine1K's selector never selected | `ctsp:docs/BUILD_CHAIN.md`; `context/ctspine1k-selection-code-deleted.md` |
| fused / separate / spine only / pelvis only | how a CTSP record's spine and pelvis masks were matched: 342 / 351 / 89 / 20 | `RESULTS_CATALOG.md` F.1 |
| Dataset803 / 810 / 813 / 815 | nnU-Net datasets: 803 = the pelvic pseudolabeller (sacrum + hips; "good only at the pelvis"); 810 = the one-shot LSTV model (retired 2026-09-08); 813 = numbered ribs; 815 = more L6 cases (built, never trained) | `context/lstv-oneshot-training-run.md`; `context/l6-sample-count-and-counting-decoder.md` |
| VerSe, VerSeFusion | the VerSe 19/20 vertebra CT challenge (374 series / 355 subjects, with a published variant table) and Greg's fused VerSe tree; VerSeFusion's `has_T13` flag is wrong | `context/versefusion-t13-flag-wrong.md` |
| TotalSegmentator (TS) v2 / v3 | the public CT segmenter and its datasets (v2.0.1 1,228 subjects; v3.0.0 1,935 scans); TS `sacrum` excludes S1 | `context/ts-sacrum-excludes-s1.md` |
| SPINEPS, VERIDAH | a public vertebra-instance segmenter and its labeller (names L6 = 25, T13 = 28); masks harvested before commit 147428d carry raw ids | `context/spineps-ids-can-be-scrambled.md` |
| Moller rib net | the public binary rib nnU-Net (Zenodo 14864106) used in arm B | `ssn:docs/ruleclass/CLASSIFIERS.md` |
| C-ArmLSpine | the real intraoperative C-arm set (Surgio-B51 C-arm; 149 cases, AP + LAT spot frames, same-session CBCT); the paper's test set | `context/carmlspine-level-experiment.md` |
| COBRA2026 | a public radiotherapy CBCT collection (Elekta XVI and Varian OBI kV imagers; 692 cases fetched) | `DATASET_USAGE.md` §2.3 |
| DeepFluoro | six cadaver specimens imaged on a Siemens Cios Fusion C-arm | `context/deepfluoro-convention.md` |
| Geneva hip, Ljubljana | a BV Pulsera phantom (116 frames) and a PIXIUM 4600 cadaver (18 frames) used for device cards and tests | `DATASET_USAGE.md` §2.3 |
| SpineSAC | sawbones imaged on six C-arms; no bone truth, unused | same |
| CSXA, BUU-LSPINE, NHANES II | the three plain-film corpora in the level bank (cervical; lumbar; the 543 annotated US survey films) | same §2.1 |
| VinDr-SpineXR | a lesion-box radiograph set under a PhysioNet data use agreement; 0 in the level bank, 2,632 crops in the fold banks | same |
| AASCE, Mendeley 5jdfdgp762, IEEE lateral-236, Spinal-AI2024 | other film sets; not in the level bank (test only, excluded duplicate, unlabelled, machine-generated) | same |
| FluoroCap | panels harvested from figures of published articles (72.8 % reproductions); dropped from training by D1 | `context/fluorocap-is-reproductions-not-fluoroscopy.md` |
| FluoroGen | SDXL + ControlNet + LoRA synthetic fluoroscopy frames | `context/fluorogen-synthetic.md` |
| RSNA 2022 | the RSNA cervical-spine fracture CT archive (203 GB, never unpacked, unused) | `DATASET_USAGE.md` §7 |
| device card | a fitted set of nine image-formation terms per device (`ssn:docs/devices/<device>.json`) used to style renders like that device | `RECIPES.md` §6 |

## Images, banks and models

| term | meaning | source |
|---|---|---|
| DRR, render | digitally reconstructed radiograph: a synthetic X-ray ray-cast through a CT; inherits the CT's person | `RECIPES.md` §5 |
| styled render | a render passed through a device card to look like that device | `ssn:docs/DATASHEET.md` §2.7 |
| `*_drr` render banks | directories of renders or converted films (`films_drr` real films, `ctsp_drr`, `verse_drr`, `physics_drr` physics-based cone-beam renders, `physics_rare` rare-anatomy oversample, `ts_drr`) | `DATASET_USAGE.md` §3 |
| `*_fov96_ctx`, crop bank, rung | a bank of context crops: field-of-view mode (`fov`), 320 px crop, target vertebra about 96 px (`tgt-px 96`), with context; `rung_1.npz` holds the crops; "rung" indexes crop scale | `ssn:slurm/allspine_v9_bank.sh` |
| `allspine_v9` | the current level bank (`allspine_v9_fov96_ctx`) and its encoder; earlier versions v2-v7 leaked; v8 keyed VerSe by series | `DATASET_USAGE.md` §1 |
| fold banks `carm_cvmix{k}` | the C-ArmLSpine cross-validation banks: v7 base sample + the fold's real frames, merged at `real_share` 0.5 | same §3.2 |
| `real_share` | the fraction of rows from real films in a merged bank (`tools/merge_banks.py` line 60); fixed at 0.5, never swept | `RESULTS_CATALOG.md` A10.11 |
| level encoder | the ResNet-18 that embeds one vertebra crop and classifies it into 27 classes | `DATASET_USAGE.md` §1 |
| recurrent head, mixed-length head | the two-layer BiGRU that names a run of 2-9 bodies together | same |
| body detector (`detector_v5z_final`) | the film-trained YOLO11m-pose that boxes vertebral bodies for naming | same |
| sacrum detector (`rx_lodo_carmlspine_1024`) | the YOLO11m trained on real COBRA + DeepFluoro frames that finds vertebrae and the sacrum; C-ArmLSpine held out | same |
| count from the sacrum, ordinal | numbering bodies upward from the detected sacrum, with no classifier | `sn:results/COUNTING.md` |
| coupling, alphabet, stop signal | choosing the ordinary / L6 / T13 / both "alphabet" from the classifier posteriors and the count; disagreement or a low margin = stop (no answer) | `sn:results/COUPLING.md` |
| answered, abstention, "at full coverage" | the share of bodies the model names when it may abstain; every headline is quoted at full coverage, with the abstention point beside it | `MANUSCRIPTS.md` §2.4 (A7) |
| zero-shot | evaluated on a device with no frame of it in training | `RESULTS_CATALOG.md` A2 |
| `v9init_pre` | the C-ArmLSpine fold models fine-tuned from the v9 encoder, scored on PRE truth | `sn:results/eval_gate/closure/cv_v9/CV_V9.md` |
| case-grouped, day-grouped | C-ArmLSpine folds by case (`md5(case) % 5`) or by acquisition day (66 / 43 / 40 cases) | same |
| PRE / REP truth | C-ArmLSpine labels before / after the 2026-09-23 repairs; printed numbers use PRE | `RESULTS_CATALOG.md` part A |
| WV / outline box vs BODY box | whole-vertebra box projected from the CT vs the vertebral-body box; detectors trained on one score poorly under the other | same A6 |
| operating points 0.25 / 0.74 / 0.60 / 0.35 / 0.05 | YOLO default; "cross-device" (adopted after 0.25 was seen: never "pre-stated"); own best F1, test-tuned (a bound only); keypoint-detector default; film-detector comparisons | `RESULTS_CATALOG.md` A4, A6 |
| LODO | leave one device out: the held-out device contributes no frame, pose or calibration term to training | `LEAKAGE.md` §3 |
| design A / B / P | device-corpus training designs: A renders every card under the Cios pose pool; B uses styled renders of the other devices + their real frames; P pools every device's frames | same |
| repaired denominator | C-ArmLSpine test vertebrae kept only if complete, not a fallback box, >= 80 % visible and body area <= outline area (287 -> 214) | `sn:results/indomain/DENOMINATOR_REPAIR.md` |
| the plateau | same-device detection stops near 84 % from 24 frames; it is the truth boxes, not the detector | `RESULTS_CATALOG.md` A8.7 |
| film N-curve | film naming against the number of training persons, from a render-only encoder | `RECIPES.md` §2 |
| render-only / ImageNet / film-only arms | the three arms of the render ablation | same §2.2 |
| H*, coverage C | normalised entropy of where frames sit in acquisition-space bins, and the share of relevant bins occupied | `sn:results/coverage/COVERAGE.md` |
| pooled fit M0 / M1 | accuracy vs N alone (M0) or N plus lateral-angle coverage (M1) | `sn:results/coverage/POOLED_FIT.md` |
| Figueroa inverse power law | acc(N) = A - B N^(-C), the learning-curve model behind the fits | `sn:results/indomain/INDOMAIN.md` §1 |
| case134 spin | one real 301-frame rotational C-arm acquisition used for detection against angle | `RESULTS_CATALOG.md` A11.4 |
| PolyPose | a NeurIPS 2025 deformation method used to vary lordosis within published ranges | `context/polypose-decision.md` |
| sweep, chain, digital fiducial, guided acquisition | the overlapping-exposure counting method, its chained naming, a persistent on-screen marker and closed-loop acquisition control: private (why: `GREG_ONLY/PRIVATE_STATE.md` §3) | `context/sweep-map-replaces-registration.md`; `context/guided-acquisition-loop.md` |
| k-devices | one network over k C-arms: per-device formation parameters (device cards), styled renders per device, leave-one-device-out | `context/k-devices-one-network.md` |
| LevelCheck | a published registration-based level-confirmation method (CT-to-radiograph); its numbers are registration accuracy, not naming | `sn:LEVELCHECK_CLAIM.md` |
| level service | the FastAPI service that serves the X-ray model; weights never on the website | `context/level-service-serving.md` |
| PACS demo, `metrics.json`, engine swap | the NiiVue viewer on the website, driven by a JSON contract so the engine can be swapped | `context/engine-swap-architecture.md` |
| ostk | OpenSpineToolkit, the measurement library; `ostk.labels.labels_for(volume)` detects the label scheme | `INFRASTRUCTURE.md` §7 |
| legacy ostk map ("v4") vs VerSe-native (v10 / v11) | L1 = 1 ... femurs 11 / 12 vs L1 = 20 ... femurs 32 / 33; mixing them returns plausible wrong answers | `context/label-scheme-v4-vs-ostk.md` |
| PIR, RAS | voxel axis orders: CTSP volumes are stored (P, I, R); analysis canonicalises to RAS (right, anterior, superior); never write a reoriented label | `context/ct-volumes-are-pir-not-ras.md` |

## Leakage, statistics and the manuscript build

| term | meaning | source |
|---|---|---|
| held out | the item's person is in neither training nor validation of the checkpoint or any ancestor | `LEAKAGE.md` §1 |
| selection split | the validation split that chose a checkpoint; numbers on it are not held out (Figure 2, the film rows) | same |
| patient key, item key, store / pixel key | person identity across naming schemes; one acquisition after alias resolution; sha256 of bytes / of a reduced image | same |
| alias | one item or person under two names (NHANES twice; CTSP under two names) | same §5 |
| CHK-1 ... CHK-9 | the nine leakage checks of `ssn:docs/DATA_ACCOUNTING.md` | `LEAKAGE.md` §2 |
| the gate (evaluation gate) | `ssn:tools/eval_gate.py`: refuses to score a seen or unresolved item and stamps the verdict into every result | same §3 |
| EVAL_LEAKS verdicts L1-L7, U1 | the leaked families and the unresolved v2 lineage of `sn:results/eval_gate/EVAL_LEAKS.md` | same §5.4 |
| G3 split | the person-disjoint, transitional-stratified 80 / 10 / 10 split (50 / 10 / 40 for transitional people) built 2026-09-23 | `sn:results/rare_class/split_plan.md` |
| G0-G7 | the gates of the flagship programme: G0 data complete (every D1-D9 directive repaired or justified), G1 transitional inventory, G2 identity keys, G3 the split, G4 the corpus (every rendered box a vertebral-body box), G5 models (`sn:results/final/`, never built), G6 the claim (the LevelCheck comparison, now paper 2), G7 manuscript + cards | `ssn:docs/FLAGSHIP_PLAN.md` lines 57-64 |
| open gate / blinded gate | paper 2's two Figure-6 evaluation jobs: ordinary strata scored openly; transitional strata blinded until a frozen human truth | `MANUSCRIPTS.md` §3 |
| Wilson lower bound, n_eff, design effect | the score-interval lower limit used for "certify 90 %"; the effective n after clustering; the variance inflation from clustering | `RESULTS_CATALOG.md` part E |
| BCa, percentile bootstrap, case-cluster bootstrap | bias-corrected accelerated and percentile intervals; resampling whole cases or patients (2,000 resamples, seed 0) | `sn:results/RIGOR_FIXES.md` |
| Holm, sign test | multiplicity correction; exact test on case-level wins and losses | same |
| `\RESULT{key}`, `numbers_manifest.json`, `results_macros.py --check` | the build that puts every number into the tex from a results file and fails on a bare numeral | `sn:RESULTS_BUILD.md` |
| CLAIM, ATLAS cards | the CLAIM checklist for AI in medical imaging (the journal wants 2024); the RSNA ATLAS model and dataset cards | `MANUSCRIPTS.md` §2.2 |
| PREREG, freeze, `prereg_sha256` | a pre-registered rule document; signing fixes its hash, which every output row then carries | `RECIPES.md` §4 |
| rigor audit A1-A9 | the 2026-09-22 adversarial audit and its fixes | `MANUSCRIPTS.md` §2.4 |
| directives D1-D9 | Greg's data directives of 2026-09-23 (FluoroCap out; use all; fix or justify every truncation ...) | `context/data-directives-2026-09-23.md` |
| at-risk person | a test person whose frozen stratum is L6, sacralised L5, four-lumbar or T13, where a count can name the wrong level; "naming unaffected" variants are not at risk | `sn:packet_src/persons_available_2026-09-24.json#rows/at_risk_pooled/frozen_strata`; `sn:LEVELCHECK_MODEL.md` L223 |
| `anchor_drr` | a render bank (CTSP 1,602 + implant variants 3,036, TotalSegmentator 2,456, VerSe 748) behind the render detector `anchor_det_v1`; its split was seeded on the implant-variant stem, so 301 of 801 CTSP people sit on both sides; never quote from it | `DATASET_USAGE.md` §2.2; `LEAKAGE.md` §5.3 |
| `vindrps` | the VinDr-SpineXR pseudo-labelled crop bank `vindrps_fov96_ctx` (7,625 films, 43,244 crops) behind `allspine_v7` and the fold banks; keyed per image, so 77.8 % of its validation leaked; never quote from it | `DATASET_USAGE.md` §2.1; `LEAKAGE.md` §4, §5.3 |
| A5, `a5`, `a5-rows` | rigor-audit item A5: per-source plain-film naming (CSXA, BUU, NHANES) on the encoder's selection split; `tools/rigor_fixes.py a5-rows` writes the per-row scores, which the film N-curve cells reuse | `sn:results/RIGOR_FIXES.md` "A5"; `RESULTS_CATALOG.md` A15; `RECIPES.md` §2.1 |
| `det_fill`, `name_fill`, `lcurve` | the Figure 5c same-device detection-against-frames fill, the Figure 5b C-arm naming-against-persons fill (250 fine-tuned cells), and the 2026-09-23 real-frame detection learning curve | `RECIPES.md` §1.2, §1.3, §2.4 |
| f6eval | paper 2's Figure-6 blinded-gate evaluation job (40438005 by memory; 40431765 / 66 by `sn:REVISION_LOG3.md` line 7), cancelled 2026-09-27 | `RESULTS_CATALOG.md` B.6 |
| Box E3, C7 criterion | items of the checklist `ssn:docs/RSNAI_PLAN.md`: E3 is the leakage audit over every device-corpus training list used in C7-C11 (never run; a second "E3 (new)" there is the bibliography audit); C7 is the pooled detector over all device distributions with leave-one-device-out, designs A and B, "the test that matters for the paper" | `ssn:docs/RSNAI_PLAN.md` L126-128, L187, L262 |
| G8 | section "G8. Films" of `sn:results/indomain/INVENTORY.md` (the film N sweep exists only on the leaky v2 bank); not a flagship gate | `INVENTORY.md` L486-490 |

## The anomaly scan

| term | meaning | source |
|---|---|---|
| anomaly harvest | screening every CT held for transitional anatomy (directive of 2026-09-23) | `context/anomaly-harvest-directive.md` |
| labeller A / B, reader C | SPINEPS + VERIDAH names bound through the centroid file / TotalSegmentator geometry with a 38 mm stump rule / a direct CT rib count | `RECIPES.md` §3 |
| truth tiers: read, two-labeller, single-labeller, morphology-only, none, `no_count`, unresolved | the order of trust in the registry; only `read` is truth | same |
| the registry | `sn:results/transitional_registry/registry.csv`: one row per CT from five streams; 6,108 persons | `RESULTS_CATALOG.md` D.8 |
| MAXIMIZE | the pass that renders every registry person the recipe allows | same D.10 |
| acquisition screen, stopping rule | fetching public CT collections to find more transitional people, with a rule written before any fetch | same D.11 |
| ruleclass, "SUPER DETECTOR RUN" | the census of 21,622 CTs under two segmentation arms (A: TotalSegmentator; B: SPINEPS + VERIDAH + Moller ribs, with Dataset803 for the pelvis) at `$RS/ruleclass/` | `context/ruleclass-super-detector-run.md` |
| tier 1 / tier 2 | the ruleclass lists: flagged and benchmark CTs first (5,094), every other CT with a SPINEPS mask second (12,217) | `ssn:docs/ruleclass/TIERS.md` |
| rules 1, 1b, 2, 3, 4 and the sweet spot | the four-rule pre-registration (rib-free count; sixth-body shape; pelvis morphology; stump rib; MDPA thoracolumbar score) and its pre-stated operating point | `RECIPES.md` §3.3 |
| review tree | per-flagged-CT case folders for human review (stage 1 Ashley Schehr, stage 2 "Dr Tech") | same |
| R + C = 22 rule | a refuted counting rule (ribs + cervical = 22) | `RESULTS_CATALOG.md` D.24 |

## Grid and operations

| term | meaning | source |
|---|---|---|
| the grid, warrior | Wayne State's HPC cluster (`grid.wayne.edu`) and its login node, which runs nothing | `INFRASTRUCTURE.md` §2 |
| reqp / requeue | the preemptible CPU partition and its QoS (most CPU jobs) | same §2.4 |
| secp / secondary | a long-running partition and QoS (priority 200, 90-day MaxWall) | same |
| gmsap, gvohp, galhp, QoS `gpu` | GPU partitions (H200, Tesla, L40S) | same |
| HOME (Panasas), Ceph / oschome, `$RS` | the 4.3 TB home quota; the 20 TB lab volume `/rs/rs_grp_oschome/go2432` | same §2.5 |
| `model_night` | the folder of experiment roots and logs (`~/model_night/logs/` for job output) | same |
| `.pre-ceph`, FINALIZE, batch B00-B14 | the migration's kept originals, the step that deletes them after Greg looks, and the migration batches | same §4 |
| model registry | the content-addressed weights store `~/model_registry`; never `ln -sf` a model | same §5 |
| `pipeline_state.py` | the tool that computes what is done, running, ready or blocked | same §3 |
| JOBS_RECORD | the record written before cancelling jobs (`ssn:docs/grid_records/`) | same §2.3 |
| Beethoven, `hpcworker`, the sitting | the lab's browser extension and worker framework (was "Ashley Bridge"; Ashley Schehr is a person); a sitting is one Claude sign-in session inside a grid job, shown in the panel | `bth:docs/guides/USE.md`, `LAB_LEAD.md` |
| the approved list | named ACL entries on `/rs/rs_grp_oschome` | `context/grid-access-list-gate.md` |
| GlobalProtect, Open OnDemand | WSU's VPN client (`protect.wayne.edu`, needed once to enrol the grid's second factor) and the grid's web portal, where the 2FA Setup app runs | `INFRASTRUCTURE.md` §2.1 |
| HPR 2026-269 | the IRB "not human-participant research" determination covering public de-identified datasets (2 Sep 2026) | `MANUSCRIPTS.md` §19 |
| Part A, Part B | the two halves of the programme as the private records name them: the CT transitional classifier (A) and the single-exposure C-arm naming network (B); CT-side Part A material is public, Part B is private | `INFRASTRUCTURE.md` §1.1; `GREG_ONLY/PRIVATE_STATE.md` §3 |
| "Dr Tech" | the senior clinical reader named on the board; full name recorded nowhere on disk | `ctsp:Student_Projects/RECIPE.md` §0 |
| Claude Docs | living documents on claude.ai (data report, Lab Recipe) | `CONTEXT_EXPORT.md` §4 |
| workflow journals | background multi-agent runs' logs (`wf_<id>/journal.jsonl`) | same |
