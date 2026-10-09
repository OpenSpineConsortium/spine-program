# A31 adversarial check: PASS/FAIL per item

2026-09-23, run after the fix pass and the figure regeneration (HEAD 421138c on L6_Class). I checked each claim
against the files, the grid listing or the images. I did not take any claim from DIAGNOSIS.md or FIX.md on trust.

| # | claim | verdict |
|---|---|---|
| 1 | Real and styled frames get the body-region window in exactly the same way | **FAIL (only literally; the practical size is not measured)** |
| 2 | No export the arms trained on was overwritten | **PASS** |
| 3 | The visibility threshold is the one that already existed | **PASS** |
| 4 | The recall delta on panel-aware truth can be reproduced from the dump files | **PASS** (one caveat) |
| 5 | The R² over the body and over the field match DIAGNOSIS/FIX | **PASS** |
| 6 | The new Figure 4a frames are AP or near-AP with bone in the field | **PASS** (two notes) |
| 7 | The Figure 3d COBRA frame has its truth inside the panel | **PASS** |

## 1. Same window for real and styled frames: FAIL (only literally)

The code I read: `deepfluoro_anchor.window_region_body` (lines 95-116), the inline copy in
`realxray_cobra_export.py` (lines 418-430), `device_style.style` (lines 269-313) and
`SchwingNet/tools/fig4_pairs_pull.py`.

These parts agree: the threshold is 0.25 everywhere, and the fallback guard is `max(2000, 2 % of the region)` everywhere.

The styled path differs from the real path in three places:

- **No styled corpus uses the body window.** Nothing in the repository calls `device_style.style(...,
  window_region="body")`. The grep finds no caller of it in any `.py` or `.sh` file. FIX.md says "a styled set
  paired with cobra_elekta_v3 must pass body", but that is a parameter that exists, not a set that has been built.
  So no styled training data has been given the v3 display yet.
- **Where the body path does exist in `device_style.style`, its ladder differs from the exporter's.** The
  exporter calls `window_or`, which extends linearly beyond p1 and p99 and uses fixed targets 27/47/126/216/239.
  `style` calls `np.interp(..., left=tgt[0], right=tgt[-1])`, which clamps at the ends, and its targets are jittered
  (N(0, 2.5) grey on each one). Its base region is also different: `inside & hit` in `style`, `I > 0` in the
  exporter. These differences were there before A31, but they still mean the two paths do not match.
- **In the Figure 4 tiles, the two regions are thresholded on different quantities.** The real tile uses
  `att - p1(att[field]) >= 0.25`, which is attenuation relative to the frame's air level
  (`body_window_real`). The styled tile uses `a_sty >= 0.25`, the forward model's absolute attenuation. The ladder
  function (`window_or`, linear at the ends) and the guard are the same for both. The two regions coincide only if
  the model's air sits at about 0 attenuation, and I did not measure that. The pair files are on the grid. The
  docstring calls the real tile's rule "the exporter's rule", but the exporter thresholds absolute
  −log(I/I0) with no p1 shift.

`device_fit.fig_frames` with `DF_WINDOW_REGION=body` does apply one region, taken from the real frame, to both
tiles. That is the one site where the treatment really is identical, and Figure 4 no longer uses it.

## 2. No training export overwritten: PASS

`ls -lR` of `/rs/rs_grp_oschome/go2432/data/realxray/cobra_elekta` on the grid, 10,794 lines:

- images and labels (train/val/test = 2,640 / 192 / 648): every file is dated **2026-09-21**.
- meta (3,480): every file is dated **2026-09-22**. That is before A31, which started on 2026-09-23 at 07:20.
- The only entry dated 2026-09-23 is `labels/val.cache` at **01:38**, the YOLO cache. It predates A31.

v3 sits in its own directory, `cobra_elekta_v3/`, created 2026-09-23 at 13:36-14:31. It holds the same 648 test
images. The eval dumps record `data=.../cobra_elekta` for v1 and `.../cobra_elekta_v3` for v3.

## 3. The threshold already existed: PASS

`MIN_VIS = 0.5` appears in `realxray_{cobra,deepfluoro,geneva}_export.py` in the parent of 7631a1c. It first
appeared in commits 3930147 and 147428d on 2026-09-21. `docs/REAL_XRAY_DATASETS_SPEC.md:56` ("Keep a box if
`visible_frac >= 0.5`") was also present before 7631a1c.

The 0.75 used in the chained sweep was new and is labelled as a sensitivity reading, which is correct.

## 4. The recall delta reproduces from the dumps: PASS (one caveat)

I recomputed every row from the per-frame `det` counts in the 18 files in `v3_eval/`. All are at conf 0.25, 648
frames, and v1 and v3 have the same stems and the same per-frame truth.

| detector | v1 @0 | v3 @0 | v3 @0.75 |
|---|---|---|---|
| render | 338/893 (sac 188/609) | 373/893 (186/609) | 325/764 (182/553) |
| lodo_cobra | 165/893 (81/609) | 190/893 (82/609) | 173/764 (81/553) |
| pooled | 870/893 (596/609) | 870/893 (595/609) | 745/764 (542/553) |

All match FIX.md §(f), and the deltas are +3.9, +2.8 and 0.0 points. The min-vis 0.5 frame lists are identical
to the min-vis 0.0 lists in all 6 pairs, with 0 truth boxes ignored. At 0.75, 129 vertebrae and 56 sacra are
ignored. FIX.md is correct that at the corpus's own rule the panel accounting changes nothing.

Caveat: **the "45 of 61 misses are off-panel" figure (conf 0.74, visible_frac < 1) cannot be reproduced from
these dumps.** They contain only conf 0.25, and they keep per-class counts without visible_frac per box. At conf
0.25 the pooled v3 arm misses 23 vertebrae at min-vis 0; of these, 4 are boxes with visible_frac < 0.75
(23 − 19). DIAGNOSIS.md §2 still says Figure 3's recall is "biased DOWN by up to 290 vertebrae … 32.5 %". FIX §(f)
now shows that bias is 0 at the corpus rule and +0.1 points for pooled at 0.75. DIAGNOSIS.md should point to FIX
§(f) instead of standing as written.

## 5. R² over body vs field: PASS

From `r2_body_vs_field.json` (n = 335):

| region | median R² |
|---|---|
| body | 0.9758 |
| full field | 0.9804 |
| fitted | 0.9785 |
| card as published | 0.9767 |
| air only (n = 87) | 0.0501 |

These round to the 0.976 / 0.980 / 0.979 / 0.977 / 0.050 quoted in DIAGNOSIS §4 and FIX §(d). The p10 and min
values also match.

Figure 4a now prints the **chosen frame's** body R² for the Elekta: 0.975, against a device median of 0.9757 from
the fig4 pull's water-path > 5 mm region. The figure no longer quotes 0.979. No R² value in the manuscript
contradicts this.

## 6. Figure 4a frames: PASS (two notes)

I opened `results/fig4_pairs/*` and `figures/fig4_formation.png`.

- **Elekta: C005_0136, 15.07° off AP, pair meta view "AP", half-fan.** The real tile is a readable radiograph.
  Air is black, and it shows the left ilium, the pelvic brim, the acetabulum, the femoral head, neck and shaft,
  and the lower lumbar spine and sacrum against the panel's right edge. It was picked from 31 of 73 joined near-AP
  frames, at body R² 0.975 against a median of 0.976.
  - Note (a): the visibility is a **proxy**. It comes from the nearest exported frame, C005_0139, 3 indices away
    (min vertebra visible_frac 0.983, sacrum 1.0), not from the pair frame itself.
  - Note (b): **the styled Elekta tile still looks poor.** It is noisy, and the pelvic brim and femoral head are
    barely readable. The cause is not the window. The card's bone scale k_b has its median at the fit's lower
    bound (the open circle in Figure 4b; physics default about 1.7). That is the pending A10/A32 refit, which the
    dagger in Figure 4b discloses. Greg's complaint will not be fully answered until that refit lands.
- **PIXIUM: LJ-L1L5_001, cropped to the specimen (308 px square).** Both tiles show a lateral lumbar specimen with
  readable bodies and end plates, and the thickest-tissue black blob is gone.
- Cios Fusion (−0.15°) and BV Pulsera are also AP.

## 7. Figure 3d COBRA frame: PASS

`examples/elekta_xvi.json`: A280_0115 from the cobra_elekta_v3 test split, 1.98° off AP. Both truth vertebrae
have visible_frac 1.0 and the sacrum 0.989, and the tile says "2° off anteroposterior". The lodo_cobra arm finds
0 of 2 at conf 0.74. By the rule this frame is the nearest to the arm's v3 set recall of 63/893 = 7.1 %.

In the image, the truth boxes sit on the lumbar spine and sacrum at the right side of the half-fan panel. The
sacrum box reaches x = 512 of 517, but it is inside the panel.

## Found beyond the seven items

- **Figure 3 mixes the two banks without saying so.** Panel (a)'s COBRA points come from
  `scored/*__cobra_test.json` with `data=.../cobra_elekta`, which is **v1**, the field window. Panel (d) comes from
  v3. For the same arm, (a) shows lodo_cobra at 55/893 = 6.2 % (v1) while (d)'s rule uses 63/893 = 7.1 % (v3).
  The caption does not say this. Either rescore (a)'s COBRA column on v3, or state the bank in the caption.
- Nothing has been trained on v3. Every v3 number tests weights trained on v1 display.
