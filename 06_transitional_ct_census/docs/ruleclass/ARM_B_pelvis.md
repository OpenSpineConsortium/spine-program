# ARM B pelvis: Greg's Dataset803 ensemble as the caudal anchor (sacrum and hips only)

This is part of the SUPER DETECTOR RUN. Greg's determination (2026-09-26 23:50) is that arm B is SPINEPS + VERIDAH
+ Möller ribs + Greg's Dataset803 ensemble, and that the ensemble is used **for the pelvis only**. Its sacrum and
left/right hip labels are kept, and its L1-L5 labels are discarded. Nothing in this arm compares Greg's model with
VERIDAH, and there is no Dataset802 L6 comparison. Code is in `RS/ruleclass/code/pelvis/`, with a local copy in
`<session scratchpad, not kept>`. Outputs go to `RS/ruleclass/arms/pelvis/`. `RS` is `/rs/rs_grp_oschome/go2432`.

## 0. Status

**02:25 EDT, 2026-09-27. Nothing has been predicted yet.** The GPU pool is full. Everything upstream of the GPU is
built and checked, and the whole chain is submitted with dependencies. `RS/ruleclass/arms/pelvis/JOBS.txt` holds
the ids.

| job | id | state at 02:25 | what |
|---|---|---|---|
| build | 40481571 | **done, BUILD_OK** | model hard-linked and size-checked. Work lists: tier 1 5,094 CTs / 128 shards, tier 2 12,217 / 256, timing 20 + 6. Sandbox built. Probe: nnunetv2 2.7.0, torch 2.4.1+cu124, dynamic_network_architectures 0.4.3, the trainer class resolves, the CLI has `--disable_tta` / `--disable_progress_bar`, and `sbatch` works from a compute node |
| census | 40481647 | **done** | tier 1: 5,094/5,094 headers, 191,054 tiles (mean 37.5, median 29, p90 80, max 420). Tier 2: 12,215/12,217, 436,917 tiles (mean 35.8). The 2 failures are AbdomenAtlas headers with extensions, which take the median |
| CPU end-to-end check | 40481771 | pending (prip/mdtp) | one TS CT (s1998) through the full worker on CPU: container, binds, recoding, `labels_for`, sidecar. Written to `_timing/cputest/` |
| timing | 40481679 | **pending (Priority)**, GPU | 20 CTs without TTA, then 6 with TTA. 10 h limit |
| summary | 40481573 | afterany timing | mode rule, GPU-h projection, tier-1 time limit, tier 2 if <= 600 GPU-h, renders and agreement preview for the timing CTs |
| **tier 1** | **40481574 [0-127]%24** | afterany summary, GPU | 5,094 CTs |
| agreement | 40481575 [0-63] | afterany tier 1 (secp) | section 6 over tier 1 |
| tier 2 | not submitted | | the summary submits it iff its projection is <= 600 GPU-h |

**ETA.** This is an estimate, not a measurement. The per-forward time below is assumed until the timing job
reports.

- The timing job needs one GPU. None was free at 02:20, and Greg's own GPU tasks queue ahead of it at equal
  priority. **The start is estimated at 2-12 h out.**
  - It then runs about 2 h on an H200: 7,195 patch forwards without TTA plus 10,080 with TTA, at an assumed
    0.3-0.5 s each. On a V100 it runs up to about 8 h.
  - The summary job follows within about 1 h.
- **Tier 1 without TTA:** about 955,000 forwards, roughly 80-135 H200-GPU-h, or 4-6 h wall at 24 concurrent GPUs.
  **Tier 1 with TTA:** roughly 640-1,060 H200-GPU-h, or 27-44 h at 24 GPUs.
  - Both walls stretch by however few GPUs the queue actually gives. At 02:20 it gave none.
- **Tier 2 without TTA** projects to roughly 180-300 H200-GPU-h, so it would be auto-submitted if the timing
  lands on an H200 or L40S and without-TTA is chosen. With TTA it projects to about 1,450-2,400 GPU-h and would
  not be submitted.

**Check progress:**
- in a CPU job: `~/mambaforge/envs/spineps/bin/python RS/ruleclass/code/pelvis/pelvis_status.py`, which gives done,
  failed and not-started per tier and collection, and the shards with work left;
- the decision: `_timing/DECISION.json`;
- the timing table: `_timing/SUMMARY.md`;
- renders: `_timing/renders/*.png`. Look at these before believing any Dice.

## 1. What runs

- **Model: the released spinopelvic-seg ensemble.** Dataset803_SpineSurgCTFullMerged, trainer
  `nnUNetTrainerWandB_500ep_LSTVOversample`, plans `nnUNetResEncUNetPlans_100G`, `3d_fullres`, folds 0-4,
  `checkpoint_best.pth`.
  - It was not in `~/spinesurg-ct-nnunet/nnunet/results/`, which holds only 802, 810 and 813. The NeurIPS v11 workflow
    had already fetched it from HF `OpenSpineConsortium/spinopelvic-seg-checkpoints` into
    `RS/neurips_v11/ens/nnunet_results/`, and each fold was size-checked against the HF listing.
  - The build job hard-links those files into `arms/pelvis/_model/nnunet_results/` (2 links each) and checks the
    sizes again. A cleanup in the v11 tree therefore cannot remove them.
  - The classes come from its `dataset.json`: 1-4 L1-L4, 5 last_lumbar (L5 and L6 merged), 6 sacrum, 7 left_hip,
    8 right_hip, 9 ignore (never predicted). 3d_fullres spacing is 0.8 x 0.75 x 0.75 mm and the patch is
    256 x 320 x 320.
- **Runtime:** `~/CTSpinoPelvic1K/containers/ctspinopelvic1k-ts.sif`, the nnU-Net+CUDA container that CTSpinoPelvic1K's
  pseudolabel stage ran Dataset803 in, plus the inference-only trainer shim (`containers/nnunet_wandb_variant.py`).
  - The shim resolves the trainer class by name. The network is built from the plans, so a mismatch fails loudly
    at state-dict load and cannot fail silently.
  - It is unpacked once into a persistent sandbox (`RS/ruleclass/containers/nnunet_ts.sandbox`) with the shim copied
    in, so the array tasks do not each unpack 3.6 GB. Singularity here is an unprivileged user install, so a SIF is
    otherwise unpacked on every exec.
  - The probed versions are in `_model/probe.txt`.
- **Call**, per chunk of 12 CTs, with the model loaded once per chunk. The CT is never copied: the input is a
  symlink `<key>_0000.nii.gz` to it.
  ```
  nnUNetv2_predict -i <chunk> -o <raw> -d Dataset803_SpineSurgCTFullMerged -tr nnUNetTrainerWandB_500ep_LSTVOversample \
     -p nnUNetResEncUNetPlans_100G -c 3d_fullres -f 0 1 2 3 4 -chk checkpoint_best.pth -device cuda -npp 4 -nps 4 \
     [--disable_tta] [--disable_progress_bar]
  ```
  - The five folds are averaged in memory, with no `--save_probabilities`.
  - nnU-Net's multiprocessing IPC runs in `/dev/shm`, because `/tmp` is swept.
  - Success is validated by the output file, not the exit code (the known shutdown race).
  - A chunk that fails is retried one CT at a time. A CT that fails twice is recorded and skipped.
  - Everything is resumable: resubmitting a task skips CTs whose JSON says `ok` in the same mode.

## 2. Output contract (what arm B and the rules read)

**`arms/pelvis/<collection>/<case_id>.nii.gz`** holds the pelvis only. The ids are **sacrum 26, left_hip 30,
right_hip 31**, which are the release (v10/v11, VerSe-native) ids. Everything else is 0.

- **Why recode, and not keep 6/7/8.** Dataset803's numbering matches neither ostk scheme.
  - Read as v4 legacy, its 8 is "sacrum" (it is the right hip) and its 6 is "L6" (it is the sacrum).
  - Read as v10 it has no pelvis at all, so `labels_for` falls back to the default and every sacrum lookup is empty.
  - Both failures are silent. MORPH_API section 2 row "Dataset803 prediction" records the second.
- **`labels_for` is the self-check.** After recoding, `ostk.labels.labels_for` must resolve the written volume to
  `{sacrum: 26, left_hip: 30, right_hip: 31}`, or the case fails.
  - The JSON records `scheme_detected` and `labels_for_ids`.
  - It also records `scheme_by_default = true` when the CT holds no pelvis. A chest CT then resolves v10 by
    default, and that is not evidence.
- **Geometry.** The prediction sits on the CT's voxel grid, because nnU-Net's SimpleITK reader and writer keep the
  index order.
  - The file is written with the CT's own affine and qform/sform codes, with scaling reset, and is **never
    reoriented**.
  - It is read back and must match the CT's affine and shape and hold only {0, 26, 30, 31}.
  - `pred_affine_maxdiff_mm` records any disagreement between nnU-Net's SimpleITK header and nibabel's reading of
    the CT.
- **The `.json` sidecar**, written last, marks a case done. Its fields:
  - `status` (`ok` / `predict_failed` / `post_failed` with `error`), `mode` (`notta` / `tta`), `attempt`;
  - the GPU and job ids, `t_predict_s` (the GPU segment from the timestamped nnU-Net log), `chunk_wall_s`;
  - `ct_shape`, `ct_zooms`, `ct_axcodes`, the q/sform codes, `raw_label_counts` (all nine classes, as numbers only);
  - per structure: mL, centroid, RAS min/max, number of components (and those of 1 mL or more), and the largest
    component's fraction;
  - `sacrum_top_S_mm`, the **anchor**: the most superior world-S of the sacrum's largest connected component. A stray
    fragment higher in the field cannot move it (MORPH_API section 4, CTSP 0001). `sacrum_top_S_mm_whole_mask` is
    kept beside it;
  - `sacrum_height_S_mm`, and `{left,right}_hip_crest_top_S_mm` (largest component);
  - `laterality`: `consistent` when the left hip's RAS x is smaller than the right's (RAS +x is the patient's right),
    `flipped` otherwise, or n/a;
  - `pelvis_present`.

## 3. Pre-registered decisions

These were fixed in `pelvis_summary.py`, which was shipped at 00:55 before the timing job was submitted.

- **TTA or not.** The released ensemble predicts with mirroring (8 flips), which costs about 8x.
  - The timing job predicts 20 CTs without TTA and 6 of them with TTA.
  - Tier 1 runs **without TTA only if**, on every one of the 6 CTs and for every structure present in either run,
    Dice(TTA, no TTA) >= 0.98 for the sacrum and for each hip, **and** the anchor (`sacrum_top_S_mm`) moves by no
    more than 2.0 mm.
  - Otherwise tier 1 keeps the released TTA.
  - The array tasks read the mode from `_timing/DECISION.json` and refuse to run without it.
- **Cost model.** `t = a + b * tiles` seconds per CT, fitted by least squares on the no-TTA timing CTs.
  - Tiles come from a header census of every tier-1/2 CT: the nnU-Net resampled shape, sliding window at step 0.5.
  - The fit is multiplied by the measured pipeline factor (chunk wall time / summed GPU segments).
  - For TTA it is further multiplied by the measured median TTA / no-TTA ratio.
  - The projection is at the timing GPU's speed, and that GPU is recorded.
- **Tier 2** (12,217 CTs) is submitted `afterany` tier 1 only if its projected GPU time is at most 600 GPU-hours.
  The summary job does this itself when a compute node can run `sbatch`; the build job probes that. Otherwise it
  writes `tier 2 ready, NOT submitted` with the number.

## 4. The timing sample (20 tier-1 CTs, `_lists/timing20.tsv`)

| collection | case | why | TTA too |
|---|---|---|---|
| ctsp | 0059 | held-out clean record with a **manual** pelvis GT (fused record) | yes |
| ctsp | 0179 | held-out clean, manual pelvis GT, subgroup sacralization | yes |
| ctsp | 0809 | largest CTSP CT file (401 MB) | |
| ctsp | 0950 | registry L6 (read) | |
| ts | s2105 | largest TS v300 CT file (174 MB) | yes |
| ts | s1157 | median TS CT | |
| ts | s1998 | registry L6 (single-labeller), small CT | |
| verse | verse026 | registry L6 (read) | yes |
| verse | verse648 | unflagged | |
| cobra | G079 | largest COBRA CT (Varian) | |
| cobra | C113 | median COBRA CT | yes |
| cobra | B127 | registry L6 (two-labeller) | |
| abdomenatlas3_mini | aa3_BDMAP_00000041, aa3_BDMAP_00005431 | screen L6 (two-labeller) | |
| idc | idc_varepop_apollo_AP-78LL | screen L6 (two-labeller) | |
| idc | idc_pediatric_ct_seg_Pediatric-CT-SEG-380 | a child (the sacrum is not adult shape) | |
| tcia_fdg_pet_ct_lesions | fdg_PETCT_05808cf24e | whole-body PET-CT, screen L6 | yes |
| tcia_fdg_pet_ct_lesions | fdg_PETCT_7faf36a152 | whole-body PET-CT, unassigned | |
| ribfrac | RibFrac482 | chest CT: expected to hold no pelvis (negative control) | |
| quadra_hc | quadra_QUADRA_HC_015 | the path contains a space; screen L6 | |

## 5. Tier arrays

- **Tier 1:** 5,094 CTs in 128 shards (row i goes to shard i % 128, so every shard mixes collections), `%24`
  concurrent.
  - Partitions `gmsap,galhp,gvohp` (H200 / L40S / V100), one GPU, 12 CPUs, 128 GB, 72 h per task.
  - Array 40481574, `afterany` on the summary job. The summary job resets the array's time limit to 3x the slowest
    shard's projection (4-72 h), because a short limit backfills sooner.
- **Tier 2:** 12,217 CTs in 256 shards, same script with `TIER=2`. It is submitted only under section 3's rule. By
  hand: `sbatch -D RS/ruleclass/arms/pelvis --dependency=afterany:40481574 --array=0-255%24 --export=ALL,TIER=2
  RS/ruleclass/code/pelvis/pelvis_array.sh`.
- **A priori cost, not a measurement:**
  - The estimate is about 1-3 GPU-minutes per CT without TTA on an H200, and about 8x that with TTA. V100 is several
    times slower.
  - For tier 1 that gives roughly 85-255 GPU-h without TTA, or 700-2,000 GPU-h with TTA. For tier 2 it gives
    roughly 200-600 GPU-h without TTA.
  - `_timing/DECISION.json` replaces these numbers. Section 0 carries the measured figures once they exist.

## 6. Pelvis agreement spec (for the report)

**Question.** Does Greg's pelvis agree with TotalSegmentator's on the same CT? And where a hand-drawn pelvis
exists, which of the two is closer to it? This is the check from outside the computation. It is implemented in
`pelvis_agree.py`: `_timing/agree_timing20.tsv` covers the timing CTs, and job 40481575 covers tier 1 (64 CPU
shards to `_agree/tier1_NN.tsv`, `afterany` tier 1).

**Sources.** Every label is resolved by name.

- **B:** the pelvis file above, through `labels_for`.
- **A, TotalSegmentator**, from the tier table's `ts_output` / `ts_kind`:
  - `total_multilabel` (1,927 tier-1 CTs: CTSP, COBRA, VerSe, RibFrac, CTSpine1K, C-ArmLSpine) uses the row's
    class map;
  - `gt_dataset_masks` (the 1,278 TS-dataset scans) uses `segmentations/*.nii.gz`;
  - `roi_subset_dir` (1,889 acquisition CTs) **has no hips**, so its hips are "not run" until arm A's gap-fill
    lands. Then rerun the job.
  - **A's sacrum = `sacrum` UNION `vertebrae_S1`**, because the two are disjoint in TS v2.
  - The TS v300 dataset ships no S1 file, and whether its `sacrum` includes S1 is unverified (CORPUS.md). If it
    does not, the TS-dataset rows will show a sacral Dice(B, A) near 0.8 and B's anchor about one segment above A's.
    That pattern would be the convention showing through, not a model error.
  - B's sacrum includes S1, because Dataset803 was trained on CTSP labels. It also includes a fused L5 (the CTSP
    convention, MORPH_API section 4). A sacrum-only TS mask would lose about one segment and read as disagreement.
- **GT:** CTSP v11 (`labels/`, never `labels_v10/`), through `labels_for`. Id 29 must be absent, and any voxels of it
  are counted.
  - `neurips_v11/run/volumes.csv` gives each record's `pelvis_origin` and held-out status.
  - **Only a `manual` pelvis on a `clean` held-out record is an external check of B (54 records, `gt_external`).**
  - The other CTSP pelves were either drawn by Dataset803 itself as pseudo-labels (`pelvis_origin = pseudo`, which
    makes the comparison circular) or trained on.
  - VerSe and CTSpine1K GT have no sacrum and no hips.
- Any source on a different grid is resampled onto the CT grid (nearest neighbour through the affines), for
  analysis only.

**Per CT:**

- mL per structure per source;
- Dice(B, A), Dice(B, GT) and Dice(A, GT) for the sacrum, left hip and right hip. When both are absent there is
  no Dice: the pair is counted as agreement on absence. When only one source has the structure, that is a
  presence disagreement;
- the laterality cross-check Dice(B left, A right). A value near 1 means the two models use opposite
  left/right conventions, or the header is wrong. This complements the sidecar's `laterality`;
- **the anchor:** `sacrum_top_S` (largest component) for B, A and GT, and the differences B-A and B-GT in mm;
- the iliac-crest top per side, for B and A.

**Reported per collection, and for CTSP split external / in-sample / pseudo.** The spread goes in the report as
well as the medians:

- n, median, IQR and the 5th percentile of each Dice;
- the share of Dice below 0.80;
- the share of presence disagreements;
- for the anchor: median |d|, and the shares of |d| above 5, 10 and 20 mm. 10 mm is about a third of a lumbar
  body's height, so a larger shift can move the count by one.

**What gets rendered.** Every CT with a sacral Dice(B, A) below 0.80, or an anchor |d| above 10 mm, or a laterality
flag, is a disagreement. It is rendered as coronal plus mid-sagittal through B's sacrum, with B filled and A
outlined, and a random 20 agreements are rendered with them. `pelvis_render.py` makes these panels (the summary job
already renders the 20 timing CTs to `_timing/renders/`). Those renders go to the adjudication table. **These are flags, not
verdicts:** a disagreement can be either model's error, or a real sacralization that one convention absorbs and
the other does not.

## 7. How the anchor enters the count

This is proposed for `PREREG_rules.md`, which owns the final thresholds.

- **The count** is the number of free presacral vertebral bodies (SPINEPS/VERIDAH instances) between the last
  rib-bearing vertebra (Möller ribs) and the **cranial end of B's sacrum**.
  - The anchor is the SPINEPS sacral end-plate (subregion 74) where it lies inside B's sacrum. Otherwise it is
    `sacrum_top_S_mm`.
  - B's sacrum is used, not SPINEPS's own sacrum instance, because SPINEPS can swallow the lowest mobile body. On
    CTSP 0005 (a read L6), its "L5" is an 810-voxel fragment and its sacrum starts 8 mm above that (MORPH_API
    section 4).
- **Per SPINEPS instance** (ids 19-25 and 28), compute f = |instance ∩ B sacrum| / |instance|:
  - **f < 0.10: free.** The body is counted.
  - **0.10 <= f < 0.50: contact.** The body is counted and flagged as a partial-sacralization / Castellvi II-IV
    candidate.
  - **f >= 0.50: absorbed.** The body is not counted as free, and is flagged as a complete-sacralization candidate.
    Under the CTSP convention B puts a fused L5 inside the sacrum.
  - **A body with f < 0.10 lying wholly below the anchor** (a mobile segment that B left out of the sacrum) is
    flagged as a lumbarization candidate.
- **The same computation on A's sacrum (sacrum ∪ S1)** gives the arm-A anchor. Where "absorbed" differs between A
  and B, that difference is the SPINEPS-vs-TS confusion Greg proposed as the sacralization and lumbar-rib signal.
- **No anchor.** The count is not made (`no_anchor`) when:
  - B has no sacrum, or less than 5 mL of it;
  - the sacrum touches the bottom slice of the field;
  - or B and A disagree on the anchor by more than 20 mm and no GT exists. That case goes to adjudication and is
    not guessed.

## 8. What the pelvis gives the sacral-shape rule

The inputs come from B's sacrum (largest component) and hips, in world mm:

- sacral volume;
- sacral craniocaudal extent. It is unreliable inferiorly, because labels run past the apex, so it is not used alone;
- the **sacral top relative to the iliac crests**: `sacrum_top_S` minus the mean crest top. This is what the hips
  add. An absorbed L5 raises the sacral base toward the crest line, and a free S1 lowers it;
- the ala-to-ala width at the top plate (SPINEPS 70/71 inside B);
- the MORPH_API section 4 additions (fused-segment count, top-plate / lowest-presacral width ratio), measured
  inside B's sacrum.

The intercrestal line is a known radiographic numbering cue, but **no accuracy figure for it is quoted here**,
because none has been read from a source in this project.

"Normal sacral shape" means the central 95 % of these features. The reference is adult persons whose count is five
free lumbar bodies, with all existing labellers agreeing, split by person into a reference half and a test half.
Thresholds are frozen on the reference half before anything else is classified. Children are excluded, because an
unfused S1 is normal in a child.

## 9. Not known / risks

- **Out of distribution.** Dataset803 was trained on CTSpinoPelvic1K-lineage colonography CTs (979 records). On
  every other collection its pelvis has no validation except agreement with TotalSegmentator, which is the job of
  section 6. **Nothing here says the model is right outside CTSP.** The AbdomenAtlas, IDC, PET-CT, COBRA
  planning-CT and TS-dataset rows are the test.
- **CTSP is mostly in-sample or circular.** Only the 54 held-out clean records with a manual pelvis are an external
  check. Every other CTSP record was either a training record or had its pelvis pseudo-labelled by this same
  model.
- **Left and right.** The label names come from the CTSP scheme. That they mean the patient's left and right
  relative to each CT header is checked per case (`laterality`), not assumed. A collection that reads `flipped`
  throughout points to a header or convention problem, and must be resolved before any side-specific rule uses it.
- **Children** (114 in tier 1): the sacrum is not adult shape, and an unfused S1 is normal. They are kept in the
  run and excluded from the sacral-shape reference.
- **The TS v300 sacrum** may exclude S1. See section 6.
- **Cost is not measured yet.** Section 5's numbers are an a priori guess. The census gives a mean of 37.5 sliding
  -window tiles per tier-1 CT (median 29, p90 80, max 420). With 5 folds that is about 190 patch forwards per CT
  without TTA and about 1,500 with it. The measured seconds per forward replace the guess in `DECISION.json`.
- **Queue.** At 01:30 every H200, L40S and V100 was allocated, much of it to other users' 1-2.5-day jobs. Greg's
  own GPU jobs (nv11_enspred, nv11_ts, smoke_spineps, armA_timing, armA_ts_t1, and spineps_april once released)
  queue ahead of this arm at equal priority. The wall-clock time is set by the queue, not by the model.
- **Things that failed and were fixed tonight**, so the next agent does not repeat them:
  - Build 40481468: `~/.local/bin/singularity` 4.0.2 builds a sandbox but cannot `exec` ("starter not found").
    Use the nextflow env's 3.8.6, as the older scripts do.
  - Census 40481469: `nib.load(...).header` on CephFS read 97 GB in 27 minutes. The client reads ahead on every
    open. The fix is to read at most 256 KB with `POSIX_FADV_RANDOM`, after which the whole census took 5
    minutes.
  - Timing 40481572: a SLURM user can lower a pending job's time limit but not raise it. It was resubmitted as
    40481679 with 10 h. Its TTA sample swaps TS s2105 (420 tiles, about 2 GPU-h with TTA on its own) for
    s1157.
  - Scripts edited from Windows Python came out with CRLF line endings, and sbatch refuses those. Write in binary
    mode or strip the `\r`.
