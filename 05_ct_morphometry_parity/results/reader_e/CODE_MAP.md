# Reader E — exact reuse map for the feature extractor (J0/J1)

> Copied 2026-10-08 into the spine programme seed from `spinesurg-ct-nnunet` 097933a `SchwingNet/results/reader_e/CODE_MAP.md`.
> "local" below means the laptop clones as they stood on 2026-09-24: OpenSpineToolkit (cb43197 in `../../MANIFEST_CODE.md`),
> spinesurg-ct-nnunet (097933a) and CTSpinoPelvic1K (7ddfe38); the one absolute laptop path (section 2.1) was replaced by
> `<laptop Desktop>`. Line numbers are those of 2026-09-24 and nothing else was changed (`../../MANIFEST_LOCAL.md` section 2).

Written 2026-09-24 for the implementer of `docs/CT_LSTV_CLASSIFIER_PLAN.md` §4 (feature table) and §8 (J0). Every
row names the function that already computes the quantity, its local path, the same path on the grid, the signature
as read from the code (argument names, array orientation, units, return structure) and the trap in it. Line numbers
were checked on both sides on 2026-09-24 and agree for every file listed in §1 unless a row says otherwise.

Repo state at writing: local `spinesurg-ct-nnunet` `L6_Class` = `1d8ac4b`; grid `~/spinesurg-ct-nnunet` = `c0b752a4`,
an ancestor three commits behind (`git pull --ff-only` on the login node brings it level; the grid tree is clean apart
from build artefacts under `SchwingNet/`).

---

## 1. Where things are on the grid, and what the Python has

| what | grid path | state |
|---|---|---|
| this repo | `~/spinesurg-ct-nnunet` (git, `L6_Class`) | ship by commit + push + `git pull --ff-only`; never scp |
| CTSpinoPelvic1K scripts | `~/CTSpinoPelvic1K/scripts/` (git clone, `master` @ `a0c5139` 2026-09-07, 133 dirty status lines; that commit is **not** in the local history, so do not `git pull` it blindly) | `extract_transition_morphometrics.py` 507 lines, `measure_sacral_ala.py` 233, `measure_tp_height.py` 243: identical line counts and identical `def` line numbers to local. `label_scheme.py` differs (159 vs 176 lines) but the constants used (`RIB_LEFT_OFFSET, RIB_RIGHT_OFFSET = 33, 46`; `LUMBAR_RIB_LEFT, LUMBAR_RIB_RIGHT = 60, 61`; `SACRUM_ID = 26`; `S1_ID = 29`) are the same. `extract_level_gradients.py` differs (430 vs 423) — do not import it from the grid; it is not needed (ostk covers it). `morphometrics/` exists there too (`sacral_ala.csv`, `tp_height.csv` are CTSP release-only tables) |
| OpenSpineToolkit | `~/OpenSpineToolkit/ostk/` — **not a git checkout** (no `.git`; an rsync copy). `labels.py` 156 lines, `morphometry.py` 412 lines, `labels_for` L135 / `detect_scheme` L106 / `level_morphometry` L380 all match local. `~/ostk_run/OpenSpineToolkit` is a second, scratch copy: ignore it | **not installed** in the spineps env (no `ostk` in site-packages, no editable `.pth`). Use the pattern already in `slurm/polypose_check.sh` L37-38: `export PYTHONPATH=$HOME/OpenSpineToolkit:$HOME/spinesurg-ct-nnunet/tools${PYTHONPATH:+:$PYTHONPATH}`. Its `pyproject.toml` deps are only numpy/scipy/nibabel, all present |
| Python | `~/mambaforge/envs/spineps/bin/python` = **3.11.16** (`site-packages` listing 2026-09-24) | nibabel 5.4.2, numpy **2.2.6**, scipy 1.15.3, scikit-image 0.25.2, pandas 2.3.2, scikit-learn 1.7.2, matplotlib 3.11.1, SimpleITK 2.5.6, torch 2.6.0 (+torchvision 0.21.0, torchmetrics 1.9.0), TPTBox 0.8.2, spineps 2.1.1, nnunetv2 2.8.1 |
| **absent** from spineps env | — | **pyarrow, fastparquet, lightgbm, xgboost, shap, catboost**. pyarrow exists in `fluorogen`/`spinedet` (25.0.0), `totalseg` (24.0.0), `vista3d` (20.0.0). lightgbm/xgboost/shap exist in **no** env. Consequences: J1 writes CSV/JSONL from the spineps env (or the consolidation step runs under `~/mambaforge/envs/spinedet/bin/python` for parquet); J3's GBT arm can start on `sklearn.ensemble.HistGradientBoostingClassifier` (has `monotonic_cst`); LightGBM needs an install job first. numpy 2.x: `arr.ptp()` and `np.float_` are gone (`np.ptp(arr)` is fine — `tp_morphology.py` already uses the function form) |
| reader C inputs (lists) | `/rs/rs_grp_oschome/go2432/data/or_ready/auto_reference/lists/{ctsp,verse,ts12,cobra_ct,cobra_cbct,carmlspine}.csv` | columns `corpus,case,raw_key,person_key,split_side,ct,ts,ts_kind,modality,src`. CTSP: `ct=~/data/CTSpinoPelvic1K/ct/<case>_ct.nii.gz`, `ts=~/bench/totalsegmentator/native/COLONOG_<n>.nii.gz` (`ts_kind=ml`, multilabel; 804 files). VerSe: `ct=~/VerSeFusion/data/unified/scan-<cid>/scan-<cid>_ct.nii.gz`, `ts=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/verse/ts/<cid>.nii.gz`. The CTSP case -> `COLONOG_<n>` map is `tools/rib_count_ts_prep.py` `ctsp_ts_map()` L64 (reads the symlinks in `~/bench/ct_by_case`; the retry folder `/rs/.../anomaly_harvest/ctsp/ts_retry/native` wins, 0533) |
| TS class map | `~/bench/totalsegmentator/class_map.json` (hard-coded at **import time** by `rib_count_reader.py` L81/L118 — importing the module off-grid raises) and `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/verse/class_map.json` | `{str(id): name}`; TS v2 `total`: `sacrum` and `vertebrae_S1` disjoint; hips `hip_left`/`hip_right` |
| SPINEPS post-fix masks, CTSP | `/rs/rs_grp_oschome/go2432/data/spineps/ctsp/CTSP_<case>_{seg-vert_msk.nii.gz,seg-spine_msk.nii.gz,ctd.json,harvest.json}` (801 masks; what reader A used) and `~/bench/spineps/native_ctd/COLONOG_<n>_*` (796, ctd-relabelled, `_relabel.json` beside) | both pass through `assert_verse_monotonic` before any id is read |
| SPINEPS post-fix masks, VerSe | `/rs/rs_grp_oschome/go2432/data/spineps/ctd_relabel/bench_ts_native/VERSE_<cid>_{seg-vert_msk.nii.gz,ctd.json}` (reader A's choice) and `~/bench_ts/spineps/native_ctd/VERSE_<cid>_*` | the mask and ctd that **passed the guard per case** are recorded in `readersAB/a/<corpus>/<case>.json` fields `mask`, `ctd`, `guard` — read those rather than re-deciding |
| VerSeFusion expert masks | `~/VerSeFusion/data/unified/scan-<cid>/scan-<cid>_msk.nii.gz` (+ `_ct.nii.gz`, `_meta.json`) | VerSe alphabet, no sacrum id |
| CTSpine1K | `/rs/rs_grp_oschome/go2432/data/ctspine1k/raw_data/{volumes,labels}/<collection>/` (COLONOG, COVID-19, HNSCC-3DCT-RT, MSD-T10, ...) | VerSe-like ids, no sacrum |
| evidence already on disk | `.../auto_reference/readerC/<corpus>/json/<case>.json` + `render/<case>.jpg`; `.../auto_reference/readersAB/{a,b}/<corpus>/<case>.json`; `/rs/.../anomaly_harvest/verse/census_v3/<cid>.json` | reader C JSON top-level keys: `corpus case ct ts modality refusals thoracic_refusals notes shape zooms anchors n_seeds ts_s1_mm_on_column sacrum_run_mm junction_tests fused_evidence rib_hu_reference rib_cage_levels rib_levels_outside_cage runs junction_tl junction_ls n_rib_free n_rib_free_is_lower_bound stump_levels n_rib_bearing sacrum_fused_evidence subtype_call lumbar_names ribs seconds_core seconds row` |
| reader E output root | `/rs/rs_grp_oschome/go2432/data/or_ready/auto_reference/readerE/` | **does not exist yet** — `mkdir -p` in the job |
| slurm pattern to copy | `SchwingNet/slurm/rc_read.sh` | `reqp --qos=requeue`, `-D $HOME/spinesurg-ct-nnunet`, `--output` on CephFS logs, `PYTHONNOUSERSITE=1`, `TMPDIR=/rs/.../tmp`, `MPLCONFIGDIR` per job, `.part` + `os.replace` for resumable JSON |

---

## 2. The three loaders

### 2.1 `ostk.labels.labels_for` — CTSP release v11

- local `<laptop Desktop>\OpenSpineToolkit\ostk\labels.py` L135; grid `~/OpenSpineToolkit/ostk/labels.py` L135.
- `labels_for(volume=None, *, scheme: str | None = None, counts=None) -> dict[str, int]` — the `{name: id}` map.
  `detect_scheme(volume, *, counts=None) -> "v4" | "v10"` decides on pelvis voxel mass under each hypothesis
  (v4 hips/femurs at 9-12 vs v10 at 30-33, winner must hold 4x the loser, `_MARGIN` L94).
- Returns `LABELS_V10` for v10 **and v11** (same ids: C1..C7 1-7, T1..T12 8-19, L1..L5 20-24, L6 25, sacrum 26,
  coccyx 27, T13 28, `"S1": 29`, hips 30/31, femurs 32/33, ribs 34-46 / 47-59, lumbar ribs 60/61, hardware 62-68).
- Raises `SchemeError` when both hypotheses are within the margin. **Returns the default `v10` silently when no
  pelvis exists under either** (a spine-only crop) — that is not a v11 confirmation, it is "nothing to get wrong".
- Pass `counts=` (from `np.bincount`, 6 s on a 160 M-voxel volume, vs `np.unique` 23 s — `measure_tp_height.py`
  docstring) to avoid a second full pass; `volume` may be any orientation (only counts are used).
- The caller still owes the §4 self-check, which the loader does not do: `29 not in counts` (v11 dissolved S1), sacrum
  26 mass > 0, hips 30/31 present; write `sacrum_source="release_26"`, `sacrum_ml`.

### 2.2 `tools/spineps_ids.assert_verse_monotonic` — SPINEPS / VerSeFusion / CTSpine1K

- local `tools\spineps_ids.py` L394; grid `~/spinesurg-ct-nnunet/tools/spineps_ids.py` L394 (`check_ids` L256,
  `read_ctd` L149, `find_ctd` L177, `load_mask` L132, `instance_stats` L206).
- `assert_verse_monotonic(mask, ctd="auto", *, require_ctd=True, strict=False, what="", kind=None, quiet=False,
  allow_skipped_names=False) -> dict` (the `check_ids` report). `mask` = path | nibabel image | `(array, affine)`;
  `ctd` = `"auto"` (found beside the path — needs a path, not an array), a ctd path, or a dict `{label: world RAS xyz}`.
- Raises `SpinepsIdError` unless verdict is `verse_ok`, `misnamed_1_2_levels` (warning; raises with `strict`), `empty`,
  or `verse_ok_no_ctd` **only with `require_ctd=False`**. Also raises on VERIDAH's skipped T12 unless
  `allow_skipped_names=True`. Report keys worth keeping in the feature JSON: `verdict`, `ids`, `order_top_to_bottom`,
  `ctd_agree`, `ctd_disagree`, `veridah_skipped_names`, `spine_axis_cos_S`, `contiguous_from_1`.
- Family calls: SPINEPS post-fix -> `assert_verse_monotonic((arr, A), ctd=<ctd path from readersAB/a json>)`;
  VerSeFusion expert / CTSpine1K -> `assert_verse_monotonic((arr, A), ctd=None, require_ctd=False)` (no ctd test; a
  mask whose ids are exactly 1..N with cervical/lumbar sizes contradicting the names is refused as raw). Ids >= 100
  (discs/end plates) and id 80 are ignored; instances < 50 voxels are left out of the order test.
- `read_ctd(path) -> {label: world RAS}` computes `rotation @ (xyz * zoom) + origin` from the TPTBox POI header
  (`"GLOBAL"` format points are taken as is). `instance_stats(arr, A) -> {id: (voxels, world RAS centroid)}` is the
  name-free instance list you order by centroid z.
- Trap: the guard proves the ids are names; reader E then **drops** them. A mask relabelled from a raw tree carries
  **no sacrum 26** (module docstring d.); take the sacrum from TS in that case and say so in `sacrum_source`.

### 2.3 TotalSegmentator `total` — `harvest_verse_census.py`

- local `tools\harvest_verse_census.py`; grid `~/spinesurg-ct-nnunet/tools/harvest_verse_census.py` (same lines).
- Class map: `main()` L743 `cm_p = Path(a.class_map) if a.class_map else Path(a.ts_dir).parent / "class_map.json"`;
  `cmap = json.loads(cm_p.read_text())` = `{str(id): name}`. `labeller_b` builds `inv = {name: int(id)}` L184 and
  never touches `labels_for`.
- `labeller_b(ts, A, zooms, cmap, verse=None) -> dict` — `ts` uint8 multilabel **on the CT grid, native orientation**
  (world through `A`; nothing reoriented; `census()` L711 refuses a TS file whose grid differs from the mask's, so the
  harvest works on the segmenter's own grid), `zooms` 3-tuple mm.
- Sacrum L233-278: `sac_id = inv.get("sacrum")`; the TS `vertebrae_S1` instance is dilated by one voxel and its
  touching-voxel count against `sacrum` becomes `s1.contact_mm2` (midline vs lateral split: `contact_mid_mm2`,
  `contact_lat_mm2`, L253-261); `mobile = contact_mm2 < 100`; a non-mobile S1 is `is_sacral` and the sacral complex is
  `sacrum ∪ S1` (`sacrum` dict: `ml, zmax, zmin, only_s1, touches_bottom, z_extent_mm, zmax_mid`). With **no TS sacrum
  at all** the S1 stands in for it (`only_s1=True`, field cut below S1). Bodies below `zmax_mid - 10 mm` are dropped as
  artefacts (L426-430).
- Hips: `hip_left`/`hip_right` in the class map (TS ids 77/78); `labeller_b` does not read them — the crest feature
  reads them directly.
- The multilabel/dir loader with canonicalisation is `rib_count_reader.load(row)` L148: `ts_kind == "dir"` assembles
  the per-class files through `on_grid(img, ref)` (order-0 resample onto the canonical CT), else `on_grid` on the
  multilabel; returns `(ctc, hu, ts)` all on the canonical RAS grid.

---

## 3. Feature rows of plan §4 -> the function that already computes them

Conventions in this table. "RAS" = the array was made by `nib.as_closest_canonical` (axis 0 = L->R, 1 = P->A,
2 = I->S); "native" = the array is read as stored and axes are taken from the affine. All lengths mm, areas mm²,
volumes ml unless stated. Grid path = `~/spinesurg-ct-nnunet/tools/...` for this repo, `~/CTSpinoPelvic1K/scripts/...`
for the dataset repo, `~/OpenSpineToolkit/ostk/...` for ostk.

### 3.1 Rib presence, traced length, lateral reach, HU, head; stump (12-38 mm) vs rib (>= 38)

- **`tools/rib_count_reader.py` `find_ribs(hu, ts, A, C, zoom, sac_top_z, fill) -> list[dict]`** L515 (grid L515).
  `hu` float32 RAS CT (from `load(row)`), `ts` int16 TS multilabel on the same grid (TS ids), `A` the canonical affine,
  `C` (N,3) world points of the column curve from `build_curve(sd)` L271, `zoom` = voxel volume in ml
  (`abs(det(A[:3,:3]))/1000`), `sac_top_z` world z of the sacral top (`C[runs[sac_idx]["i0"], 2]`, else `C[:,2].min()`),
  `fill` = None for CT (the CBCT padding value otherwise).
  Per bone component: `vox, ml, medial_mm, medial_dy, hu_mean, hu_p90, medial_xyz, lateral_mm, side ("left"/"right"),
  ts_rib_frac, cut_si, cut_lat, how ("bone"/"stall"/"none"/"skipped"), steps, stall_mm, contact_xyz (the
  costovertebral joint), chord_mm (max distance of the component from the joint), attached, rib_like, is_rib, stump`.
  Constants: `RIB_HU 200`, `PATH_HU 150`, `RIB_LEN_MM 38` (L88), `STUMP_MIN_MM 12` (L95), `RIB_LAT_MM 30`,
  `RIB_MEDIAL_MM 45`, `STALL_MM 6`.
  The post-filters live in `read_one` L929-957 and are not a function: `rib_hu_reference` (median `hu_mean` of attached
  TS ribs >= 38 mm), the three rejection rules, the nubbin rule for stumps, and `level_of(p, C, runs) -> (run index,
  curve index)` L598 (a joint in a disc gap goes to the body below). `whole = is_rib and not cut_si and level is not
  None`; `stumps = stump and level is not None`.
  Traps: `level` is a **run index from the top of the field**, never a name; `chord_mm` is a traced chord from the
  joint (lower bound on arc length), never a bounding box; needs TS for the seeds and the `blocked` organ mask
  (contrast in the aorta reaches the body at >= 150 HU); the module reads the class map at import.
- Second implementation, TS rib labels only: `harvest_verse_census.labeller_b` L441-541 (pieces of one TS rib class
  chained within `RIB_GAP_MM 12`; `length_mm = pca_extent(w)` L172 — first principal axis, a lower bound;
  `cut_by_fov`; attachment by the **medial end**: `dist_mm, head_present (dmin <= CONTACT_MM 4), head_z, head_dz,
  head_dx, votes, k_centroid, rule`), per-body `rib_type` in {thoracic, stump, none} L544-550 (`STUMP_MM 38`,
  `MIN_THOR_RIB_ML 0.3`, stump >= 8 mm). Output rows `ribs_all` L569-573.
- CTSP release ribs (ids 34-59, 60/61) with PCA length: `extract_transition_morphometrics.py` `_pca_length(mask,
  spacing)` L99 and `one()` L280-312 / L438-448 (`rib11/12_len_{side}_mm`, `rib12_11_ratio`, `n_rib_bearing` by
  `_nearest_vert` within `ANCHOR_MM 15`). RAS, label-named; use only as a cross-check on CTSP.

### 3.2 Rib-free body count between the last rib-bearing body and the sacral plateau; FOV gates; rib-bearing count

- **`rib_count_reader.py` `read_one(row, render_dir=None, force_render=False) -> R`** L714. `row` keys: `corpus, case,
  person_key, ct, ts, ts_kind ("ml"|"dir"), modality ("ct"|"cbct")`. The count and every gate are **inline** in
  `read_one` L991-1148 (`tl_no_rib`, `tl_isolated_rib`, `tl_rib_cut`, `tl_lowest_is_last`, `tl_next_cut`,
  `tl_lateral_fov` via `lateral_ok(C, i, hu, Ainv, fill)` L610 with `LAT_MM 65`; `chain_*`, `ls_no_sacrum`,
  `ls_sacrum_cut` with `SAC_MIN_MM 25`, `MAX_DISC_MM 20`; thoracic `t1_*`, `t_side_mismatch`, `t_unilateral_end`;
  the stump rule L1121-1147). `R` keys: see §1 (notably `junction_tl`, `junction_ls`, `n_rib_free`,
  `n_rib_free_is_lower_bound`, `lumbar_lower_bound`, `n_rib_bearing`, `rib_cage_levels`, `rib_levels_outside_cage`,
  `stump_levels`, `rib_components_per_side`, `refusals`, `thoracic_refusals`, `subtype_call`).
  `resolve(runs, occ, hmean, sac_idx, cls) -> (runs, n_mob)` L415 folds fragments (`FRAG_RATIO 0.45`, < 10 mm) and
  splits merged bodies (`MERGE_RATIO 1.6`, `try_split` L383 at an occupancy dip < 0.85 or a >= 60 HU CT dip).
  `finish(R, row, t0)` L1210 adds `seconds` and the section-14 `row`.
  Trap: a cut field is `no_count`, never ordinary — keep that. `read_one` is ~480 lines and TS-bound (see 3.3);
  the cheapest reuse for J0 is to **call it unchanged for the TS family and read `R` back** (it is already on disk for
  CTSP 802 / VerSe 374 under `readerC/<corpus>/json/`), and to feed the release and SPINEPS families through the
  adapter in §4.
- `harvest_verse_census.labeller_b` count block L552-660: `partial` bodies (within 2 mm of the field ends) never
  serve as references; `junction_tl_in_fov`, `junction_ls_in_fov`, `n_lumbar_contact`, `n_lumbar` (38 mm rule),
  `n_thoracic_rib_bearing`, `thoracic_top_bounded`, `lumbar_rib`, `stump_levels_at_junction`, `reasons_no_count`.

### 3.3 1-mm occupancy + mean-HU profile along the column; body runs {len_mm, cut flags}

- **`rib_count_reader.py` `profile(C, T, hu, ts, Ainv, fill) -> (occ, infield, hmean, cls)`** L303: `C`,`T` (N,3)
  curve points and tangents at `STEP 1.0` mm; a 6 mm disc (`DISK_R`) of 17 samples per point; `occ` = min(whole-disc
  fraction, centre + 3 mm ring fraction) of samples inside `VERT + [S1, SAC]`, `infield` = >= 80 % valid samples,
  `hmean` trilinear mean CT value, `cls` majority TS id per sample. Needs `seeds(ts, A, zoom_ml) -> (seeds,
  sac_top_seed)` L176 (one seed per TS vertebra component: anterior half of the medial band, then S1/sacrum in 15 mm
  slabs), `clean_seeds` L241, `build_curve(sd) -> (C, T)` L271, `make_runs(occ, infield, hmean, cls, ends_in_field)
  -> (runs, occ_s)` L356 (median-filtered occupancy >= `OCC_BODY 0.5`, one-sample holes bridged, runs >= 3 mm).
  Run dict: `i0, i1, cut_top, cut_bot, at_curve_end, split, len_mm, comp ({TS short name: fraction}), sac_frac,
  sac_only, s1_frac, lumbar_ts_frac, hu, flag`. Serialised in `R["runs"]` L992 as `k, len_mm, s=[i0,i1], z (world z at
  the run middle), ts, hu, cut=[top,bot], split, flag, sacrum, ribs (["L","R"])` — **this is already a name-free
  per-instance table ordered top to bottom**, with the sacrum flagged, and is on disk for every CTSP/VerSe case.
  Trap: everything keys on the module-level TS id lists `VERT`, `S1`, `SAC`, `LUMBAR_TS` (L120-127). For the release
  and SPINEPS families the adapter (§4) remaps every vertebral instance to some id in `VERT`, the sacrum to `SAC`, and
  builds the seeds from instance centroids; `cls`/`comp` then carry the remapped ids, which is fine because names are
  dropped anyway.

### 3.4 L5-S1 junction: joined vs disc; S1-sacrum contact; two-S1 case; L5-S1 gap; contact area mid vs lateral

- **`rib_count_reader.py` `class_contact(ts, A, ca, cb, p, t, R_=14.0, H_=35.0) -> dict(state, why, d_min,
  contact_mm2)`** L625: label array `ts` (any ids), affine, the two ids, a world point `p` on the curve and the tangent
  `t`; both classes cut to a cylinder of radius `R_` and half-height `H_` around the column; `d_min` from an EDT of the
  upper class sampled on the lower; `contact_mm2` = lower-class voxels within 1.05 voxel × in-plane voxel area.
  `separate` if `d_min > 1.5 voxel or contact < 100`, `joined` if `contact >= 350`, else `unclear`; `absent` when a
  class has < 20 voxels beside the column. `runs_contact(ts, A, C, a0, a1, b0, b1, R_=12.0)` L667 does the same
  between two **runs** (curve index ranges) when TS named two bodies S1 — this one uses `np.isin(sub, VERT+[S1,SAC])`,
  so it is TS-id bound. In `read_one` L786-919 the results become `junction_tests` (list of `{upper, lower, state,
  why, d_min, contact_mm2, [ct_dip], [gap_mm, gap_min_occ]}`), `fused_evidence` (strings), `ts_s1_mm_on_column`
  (refused above 45 mm: `ls_s1_long`), `sacrum_run_mm`; `sac_inner_gap(r, occ)` L1203 flags a disc-like stretch in the
  top 45 mm of the sacral run (a fused L5 with a remnant disc). The unclear case falls back to `ct_dip(t_)` (>= 60 HU
  dip = a disc) only across a run, never across a gap (CTSP 0569).
- `harvest_verse_census.labeller_b`: `ls_gap_mm` L589-604 = lowest body's **anterior half** lowest z minus the sacral
  top under the body column (±20 mm of the body's x, in front of the body centroid) — body to body, so alae and facets
  cannot hide a level; `>= 25 mm` refuses (`an unlabelled level between?`). `s1` dict `contact_mm2`, `contact_mid_mm2`,
  `contact_lat_mm2`, `mobile` L259-262 is the mid-versus-lateral contact the plan asks for (a Castellvi III/IV body TS
  called S1 touches the sacrum laterally only).
- Traps: the sacrum source differs per family (TS `sacrum ∪ vertebrae_S1`; release 26; VerSeFusion/CTSpine1K none ->
  every row of this block is `NaN` with `sacrum_source="none"`, never 0). `class_contact` is class-agnostic and works
  on a release or SPINEPS map directly with `ca` = lowest instance id, `cb` = 26.

### 3.5 Per-side TP reach, thickness, slenderness; TP rostrocaudal height (Castellvi I >= 19 mm)

- **`tools/tp_morphology.py` `tp_metrics(mask: np.ndarray, zooms, ax) -> dict`** L65, `axes_of(affine)` L51 ->
  `{"lr": (axis, sign), "ap": (axis, sign), "si": (axis, sign)}`. `mask` boolean, **native** orientation, `zooms`
  3-tuple. Returns `body_half_mm`, `{left,right}_reach_mm`, `_thickness_mm`, `_slenderness`, `_ap_spread_mm`,
  `_si_spread_mm`; `{}` below `MIN_VOX 2000`. Reach = 99.5th-percentile lateral distance minus the body half-width
  measured on the anterior third; thickness = sqrt(cross-section area) of the slab from the body edge to half the reach.
  **Trap (verify by render before trusting on RAS arrays):** L83 `ant = ap <= np.percentile(ap, 33)` uses the raw
  index × zoom **without the AP sign**. On a P-I-R array (CTSP native) low index = anterior and the body half-width is
  right; on an RAS array (axis 1 increasing toward anterior) the "anterior third" is the **posterior** third (the
  arch), and reach is measured from the wrong datum. Feed native P-first arrays or flip `ap` by `ax["ap"][1]` first.
- TP height (Castellvi I criterion): `CTSpinoPelvic1K-1/scripts/measure_tp_height.py` `one(path: Path) -> dict`
  L76 (native axes via `axes_from(affine)` L63; lowest lumbar = max present id in 20..25; 12 mm lateral tip slab
  (`TIP_MM`, `LATERAL_FRAC 0.45`); height = craniocaudal extent of the **largest connected component** of the tip,
  `tp_height_{left,right}_mm`, `tp_height_slab_*_mm`, `tp_tip_components_*`). The same block, RAS, inside
  `extract_transition_morphometrics.one` L351-406 (adds `tp_height_max_mm`, `tp_height_asym_mm`). Table on disk for
  the CTSP release: `CTSpinoPelvic1K-1/morphometrics/tp_height.csv` (columns `case, lowest_lumbar_label, axcodes,
  tp_height_left_mm, tp_height_right_mm, tp_height_slab_*, tp_tip_components_*, labels_present, n_voxels_fg, error`).
  Trap: both pick the vertebra **by name** (max lumbar id); reader E passes the instance mask of the lowest presacral
  instance instead — the tip logic is ~40 lines and takes a boolean mask + zooms + (lat, cc) axes.

### 3.6 TP-to-ala gap / contact area per side; sacral-ala rise asymmetry

- Gap: `extract_transition_morphometrics.py` `one()` L351-376: `tp_gap_{left,right}_mm` = `_mindist` (L92, brute force
  on point clouds subsampled to `cap` = 400 / 700 points) from the 12 mm lateral tip slab of the lowest lumbar
  (`TIP_MM`, lateral 45 % bands) to `sacrum ∪ S1` (26, 29) and separately to the ilium (30/31:
  `tp_gap_ilium_*_mm`); `tp_gap_min_mm`, `tp_gap_asym_mm`; `ll_span_{left,right,asym,total}_mm`. RAS array,
  fixed ids. Trap: a **minimum distance on a subsampled cloud** (resolution of a few mm), not a contact area; the
  file's own docstring records the two ways this measurement was wrong before (facet joint read as the gap; ilium
  pooled with the sacrum). The plan's *contact area in a named plane* does not exist anywhere: write it with the EDT
  pattern of `class_contact` (EDT of the ala mask, count TP-tip voxels within 1.05 voxel, × in-plane area).
- Ala rise: **`CTSpinoPelvic1K-1/scripts/measure_sacral_ala.py` `one(path: Path) -> dict`** L79 (grid same):
  native axes via `axes_from(affine)` L67 -> `(lat, cc, up, left_is_low, ant_is_low)`; sacrum = ids 26|29, needs
  >= 5000 voxels; anterior half only (`ANT_FRAC 0.50` — the whole-depth version measured the S1 superior articular
  process and gave AUC 0.450); midline band `MID_FRAC 0.18`, lateral bands beyond `LAT_FRAC 0.55` of the sacral
  half-width; `ala_rise_{left,right}_mm` = top of the lateral band minus top of the midline band (mm, sides named
  anatomically), `ala_rise_max_mm`, `ala_rise_asym_mm`, `ala_rise_wholedepth_max_mm` (kept to show the failure).
  Table: `morphometrics/sacral_ala.csv` (`case, lowest_lumbar_label, axcodes, sacrum_voxels, ala_rise_left_mm,
  ala_rise_right_mm, ala_rise_max_mm, ala_rise_asym_mm, error`). Trap: takes a **path** and fixed ids; for TS pass the
  `sacrum ∪ vertebrae_S1` boolean — refactor `one` into `ala_rise(sac_bool, affine, zooms)` (the body is ~60 lines).

### 3.7 Sacral foramina count (thin coronal slab)

- **`extract_transition_morphometrics.py` `count_foramina(lab, spacing) -> (left, right, median_area_mm2,
  best_slab_offset_mm)`** L111: `lab` **RAS** int array (the caller does `as_closest_canonical`), `spacing` 3-tuple;
  sacrum = `isin(lab, [26, 29])`, needs >= 5000 voxels; an 8 mm slab (the docstring says ~12; the code L135 uses
  8.0 mm) slides along axis 1 (A-P) in steps of a third; per slab, `binary_closing` (4 mm SE) then
  `binary_fill_holes & ~proj`, holes of 8-700 mm² counted per side of the sacral mass midline (axis 0); the slab with
  the most holes wins. `(None, None, 0.0, None)` when there is no sacrum.
  Trap: assumes RAS axis roles; documented failure modes 0/0 and 4/3 on a normal sacrum — a weak feature, never a
  gate; on TS pass an array where `sacrum ∪ S1` is written as 26.

### 3.8 Disc heights, L5-S1 / L4-5 ratio (column-restricted)

- **`extract_transition_morphometrics.py` `_disc_height_mm(lab, upper_mask, lower_mask, sp, half_mm=8.0) -> float |
  None`** L180: boolean masks on one **RAS** grid (`lab` is unused inside; kept for the signature), `sp` 3-tuple. The
  column bundle (±8 mm) is centred on the **upper bone's inferior 20 %** (not the pooled centroid — pooling with the
  sacrum dragged the bundle off the disc and read 25.6 mm), one column per (x, y), gap = upper's min z minus lower's
  max z, median × `sp[2]`; `None` with < 15 columns or a median outside (-2, 60) voxels; clamped at 0.
  Used at L412-421 as `disc_low_mm` (lowest lumbar vs `sacrum ∪ S1`), `disc_above_mm`, `disc_ratio`.
  Trap: voxel columns along array axis 2 (RAS S), not the vertebra frame — fine for a ratio and for a "rudimentary
  disc" test; measured as a disc, never as the nearest bony approach (facets read 1.7-4.9 mm).

### 3.9 Body heights, end-plate widths, canal width/depth, wedge ratio; per-body volume, S-I extent

- **`OpenSpineToolkit/ostk/morphometry.py` `level_morphometry(label, affine, level_id: int, *,
  sup_axis=WORLD_SUPERIOR, lr=(1.0, 0.0, 0.0), max_plate_rms_mm=2.0) -> dict | None`** L380 (grid L380). `label` an
  int array, `level_id` **any integer id present in it** (so an instance map with arbitrary ids is fine — this is
  name-free by construction). Returns mm rounded to 2 dp: `VBHa, VBHp` (corner to corner in the plate frame),
  `EPWu, EPDu, EPWl, EPDl` (width over a 3 mm band at the plate, depth = corner chord), `SCW`, `SCD` (midsagittal
  chord over the central half of the closed-ring column — a diameter, not an extent), `l, r, mean` pedicle widths from
  `pedicle_widths`, `plate_rms_mm`; `None` when the mask < 200 voxels, the body cut fails, a plate does not fit, or the
  plate RMS exceeds 2 mm.
  Orientation: the frame is built from world points through `affine`, `canal_mask` finds the superior array axis from
  the affine (`_sup_array_axis`), **but `pedicle_widths` L347 takes `lat_dir = [1, 0, 0]` in array space ("array x is
  left-right after canon.")** — so pass `as_closest_canonical` arrays.
  Cost: `pedicle_widths` resamples an SDF to 0.35 mm, **30-60 s per level** (comment L284-304), and the 2026-09-10 shard
  run never populated it. For J0/J1 call the parts directly and skip PDW: `body = body_mask(m, affine)`,
  `sup = endplate_corners_body(m, affine, "superior", body=body)`, `inf = ...("inferior", ...)` (each returns
  `(anterior_pt, posterior_pt, rms)`), `frame = vertebra_frame(sup, inf)`, `body_heights(sup, inf)`,
  `endplate_dimensions(body, affine, corners, frame)`, `canal_dimensions(m, affine, frame)` (all in `ostk.morphometry`
  / `ostk.vertebral_body`).
  Per-body volume and S-I extent are one line from `instance_stats` / `label_stats` (`harvest_verse_census.label_stats
  (arr, A, zooms, ids=None) -> {id: {vox, ml, c, zmin, zmax}}` L79).
- The CTSP release table `extract_level_gradients.py` `one(path)` (`endplate_width_{L}_mm`, `body_height_{L}_mm`,
  `body_height_post_{L}_mm`, `body_height_wall_{L}_mm`, `wedge_ratio_{L}`, `canal_width_{L}_mm`, `tp_span_{L}_mm`;
  RAS; ids 18-24 fixed) is label-named and its canal width `_canal` L61 is a filled-hole **extent** (a maximum, not a
  diameter). Do not port it; the ostk frame version is the one whose definition matches the literature.
- Spread rule (`CTSpinoPelvic1K-1/docs/LEVEL_MORPHOMETRY.md`): L17-19 the table "this cohort's SD vs the widest SD in
  any published living cohort"; L80 the canal (21 % of L3 below any living canal); **L176 "L5 is withheld for
  end-plate width and pedicle width"** (TP shoulders survive the canal cut). Every measure enters J2 with that
  comparison, and the share below a published threshold against the published prevalence.

### 3.10 Iliac crest line relative to the last two bodies

- Existing, label-named, RAS: `extract_transition_morphometrics.one` L423-436 — `crest_z` = highest voxel of
  `isin(lab, [30, 31])`; the first vertebra id whose z-range contains it -> `iliac_crest_at`, `iliac_crest_at_id`.
  Name-free version = the same 14 lines over the instance list (crest z projected onto instances; report the instance
  index from the sacral plateau and the fraction of that body's height at which the crest falls). TS: `hip_left`,
  `hip_right` from the class map; release: 30/31 from `labels_for`; VerSeFusion/CTSpine1K: NaN + mask bit.

### 3.11 Spacing anomalies: 1.6x gap = missing body; squeeze = two bodies under one name; volume ratio to the case median

- `harvest_verse_census.labeller_b`: `split_doubled(bodies)` L310-360 (candidate >= 1.6x the median volume of up to
  two neighbours each side **and** >= 1.25x their median S-I extent, or 1.3x/1.5x, or 1.8x volume alone; cut at the
  deepest minimum of the anterior-half z-profile in the middle 30-70 %, only when that minimum is < 50 % of the smaller
  flanking maximum; sides under 3 ml are not split; every candidate is reported in `doubled_objects`), fragment fold
  L364-391 (< 0.4x neighbour median with >= 50 % S-I overlap -> `fragments_folded`), halves merge L399-421 (centroid gap
  < 0.62 of the local spacing **and** union <= 1.35x the median volume -> `halves_merged`), spacing gaps L575-588
  (`d > 1.6 * median(neighbouring gaps)`, partial bodies excluded -> `gaps`, `spacing_mm`). These are **closures inside
  `labeller_b`** and not importable; copy them (about 110 lines). Reader C's equivalents on the 1-mm profile are
  `resolve` / `try_split` (§3.2).
- Case-median normalisation: `CTSpinoPelvic1K-1/scripts/test_morphometric_separability.py` `build(path)` L53-93:
  for each measure the case's own median over its measured levels (>= 3 levels), features = value / case median plus
  six size-free ratios (`tp_span/endplate_width`, `canal_width/endplate_width`, `body_height/endplate_width`,
  `anterior/posterior height`, `tp_span/body_height`, `canal_width/body_height`). CSV-bound; copy the 15 lines.

### 3.12 Sequence context: name-free position index from the sacral plateau upward and from the last rib-bearing body downward

- New. Both indices fall out of reader C's `R["runs"]` (`k`, `sacrum`, `ribs`) and `R["rib_cage_levels"]`: position
  from the plateau = `sac_idx - k`; position from the last rib-bearing body = `k - rib_cage_levels[-1]`. For the
  release/SPINEPS families the same two numbers come from the ordered instance list plus the rib evidence of §3.1.

### 3.13 Render (midsagittal + coronal PNG over the CT)

- **`rib_count_reader.render(R, row, C, occ, hmean, runs, sac_idx, whole, ribs, hu, ts, A, out_dir)`** L1225: coronal
  MIP + mid-sagittal ±10 mm MIP + the occupancy/HU profile, runs coloured (cyan sacrum, red unresolved), rib contacts as
  dots with chord lengths, the call and refusals in the titles; writes `<out_dir>/<case>.jpg` at 95 dpi. `read_one`
  renders only for non-ordinary calls or a 4 % hash sample unless `force_render=True` — J0 passes `force_render=True`.
- `tools/transitional_mask_census.py` `png(arr, dz, path, title, ct_path=None) -> bool` L130 (mid-sagittal label slice
  over the CT, one colour per id, names from `NAMES`) with `load_ras(p) -> (arr, dz)` L67 (a TS folder is assembled by
  `TS_ORDER` L50 — note it writes TS `vertebrae_S1` as **29**, a census convention, not v11). Both need matplotlib
  `Agg` and a writable `MPLCONFIGDIR` (`rc_read.sh` sets it per job).

---

## 4. What has to be written new (the implementer's list)

1. **Instance-table builder per mask family** (~120 lines): load (§2), assert, `instance_stats` -> order by world-S
   centroid, drop names, compute per-instance `ml`, `zmin/zmax`, centroid, `partial` (within 2 mm of the field ends,
   `harvest_verse_census.fov_z` L73), and the family's sacrum mask with `sacrum_source` in
   {`release_26`, `spineps_26`, `ts_sacrum_union_S1`, `ts_S1_only`, `none`} and `sacrum_ml`.
2. **Adapter that lets `rib_count_reader.profile/make_runs/resolve/find_ribs/class_contact` run on a release or
   SPINEPS map**: a `ts`-like int16 array on the canonical CT grid with every vertebral instance remapped to an id in
   `VERT`, the sacrum to `SAC`, hips left as any non-`VERT` id (they only feed `nonrib`/`blocked` in `find_ribs`), and
   seeds built from instance centroids instead of `seeds(ts, A, zoom)`. Without this the TS family is the only one
   with ribs, junction tests and the 1-mm profile, and §6 ii (segmenter invariance) cannot be measured.
3. **TP-ala contact area per side in a named plane** (EDT pattern of `class_contact`), and the ala-rise / TP-height
   / foramina / disc-height functions refactored to take **(boolean mask(s), affine, zooms)** instead of a path with
   fixed ids (§3.5-3.8). Vendor these four from `~/CTSpinoPelvic1K/scripts` into `tools/` rather than importing: the
   originals import `label_scheme` from their own directory, hard-code `S1 = 29` (retired in v11; harmless as a
   union member, wrong as a source), and the grid clone is at a commit the local history does not contain.
4. **Iliac crest line** name-free (§3.10) and the **sequence indices** (§3.12).
5. **Skeletal-immaturity gate** for `LS-NA`/`unusual_spine`: open iliac apophysis on the hip mask, S1-S2 disc gap in
   the sacral occupancy profile (`sac_inner_gap` covers only the top 45 mm = an L5 remnant; S1-S2 needs the profile
   below it), DICOM age where present. Nothing existing does this.
6. **JSON envelope** per (CT, segmenter): per-stage `seconds` (load / instance table / ribs / TP-ala / discs /
   end plates / render), `code_sha256` (`hashlib.sha256(Path(__file__).read_bytes()).hexdigest()`), `mask_family`,
   `loader`, `guard_verdict`, `sacrum_source`, `sacrum_ml`, FOV flags (`junction_tl_in_fov`, `junction_ls_in_fov`,
   `partial_top`, `partial_bottom`, `lateral_fov_ok`), written `.part` + `os.replace` (`cmd_read` L1337-1339).
7. **Release v11 self-check** after `labels_for`: `29` absent, sacrum 26 mass > 0, hips 30/31 present; raise, do not
   warn.
8. **Table writer**: CSV/JSONL from the spineps env (no pyarrow); parquet only under `spinedet`'s python.
9. **J0 slurm**: copy `rc_read.sh`; array of 60 = 20 CTs × {release-or-expert, SPINEPS, TS}; 1 core, 16 GB, 1 h per
   task; `sacct --format=JobID,MaxRSS,Elapsed` afterwards. The 20-CT list must name, per CT, the three mask paths
   (§1): CTSP release `~/data/CTSpinoPelvic1K/labels/<case>_label.nii.gz`, SPINEPS from `readersAB/a/ctsp/<case>.json`
   `mask`/`ctd`, TS from `lists/ctsp.csv` `ts`; VerSe expert `scan-<cid>_msk.nii.gz`, SPINEPS from
   `readersAB/a/verse/<cid>.json`, TS from `lists/verse.csv`.
10. **Verify `tp_metrics` on an RAS array by render** before it enters a row (§3.5 trap).
