# ARC_CHECK: adversarial check of the oblique-arc work (2026-09-23)

Each item was checked against the files themselves, not the agents' reports. Where possible the check uses a
computation independent of the code under test. Grid half: job 40424737 (`/rs/rs_grp_oschome/go2432/tmp/arccheck/grid_checks.py`,
log `~/model_night/logs/arccheck_40424737.out`). Local half: scratchpad `arccheck/{indep_lat,mag_check,curve_check}.py`.
The local copies of `audit/`, `recall_vs_angle/` and `proof_surgio/proof.json` are the same size in bytes as the grid originals.

| # | item | verdict |
|---|---|---|
| 1 | arc poses span -90..+90 | **PASS** |
| 2 | sign convention, read anatomically from a +45-ish and a -45-ish render | **PASS** for the convention; **FAIL** for the proof's own automated hip check (the check is wrong, not the arc) |
| 3 | recall curve JSON matches the figure | **PASS** |
| 4 | held-out subjects never in a scored detector's training data | **PARTIAL**: clean for training in P/A/B, but they are P/A/B's *validation* subjects, and real_lodo's pretrain trained on 5 of them |
| 5 | case134 meta carries no PatientID / name / birth date | **PASS** |
| 6 | case134 sweep boxes sit on vertebrae | **PASS**, with one caveat (L4/L5 boxes run into the pedicles at oblique and lateral angles) |

## 1. Arc span: PASS

I recomputed the source position from `M = ext @ inv(T)` alone (`s = -R^T t`) and took
`lat = atan2(s_x - a_x, s_y - a_y)` about the stored anchor. This uses no `pose_arc` code
(`/rs/.../devcorpus_arc/poses/*.json`).

| pool | poses | lat min..max | 15-deg bins, -90..+90 | lat < -45 / > +45 | independent vs recorded lat |
|---|---:|---|---|---:|---:|
| surgio_b51_dr, arc | 592 | -90.0..+90.0 | 36 46 56 43 45 50 54 52 52 63 47 48 | 138 / 158 | 0.0000 deg |
| surgio_b51_dr, real | 296 | -94.5..+1.9 | 148 at 0 (+/-2), 148 at -90..-94.5, **zero obliques** | 0 / 0 | 0.0000 deg |
| cios_fusion, arc | 1100 | -90.0..+90.0 | 82 90 103 84 91 96 94 89 94 105 86 86 | 275 / 277 | 0.0000 deg |

The arc tilt (independent reading) runs from -13.5 to +13.2 deg (p5..p95). I read Elekta only from the audit
(`audit/pose_pools.json`): 4216 arc poses, spread evenly from -90 to +90, with 36 non-empty 5-degree bins.
The real Surgio laterals put the source at patient-frame -x, the patient's right, in all 148.

## 2. Sign convention: convention PASS; `proof.json` check FAIL (the check is wrong)

`proof.json` `checks`: `source_x_sign_follows_lat` true, `readback_max_err_deg` 0.0, `spine_boxes_min` 7,
`hips_converge` true, `near_hip_taller_at_minus45` true, **`near_hip_taller_at_plus45` false** (checked at +40 and -50).
The right hip box is the taller at *every* angle, from 3.8 px taller at -90 up to 84.2 px taller at +90.

**Why the check fails, and why the arc is still right.** In every frame I opened (-90, -50, 0, +40, +90), both hip
boxes run off the bottom edge of the panel (y1 = 1024). The hips also sit below the principal point. Magnification
therefore pushes the crest of the hip nearer the source further down, which *shortens* its visible box. So
"near hip taller" is inverted by construction. The observable that does track magnification is the crest (the box's
top edge), which is 1024 minus the height. Left-minus-right crest depth in px, from `proof.json` heights:
-90: +3.8, -50: +14.2, 0: +29.8, +40: +73.1, +50: +77.5, +90: +84.2. The difference rises monotonically as lat goes
positive, so the left crest is being magnified away from the centre. That means the source is moving toward the
patient's LEFT, which is the documented convention. An independent synthetic test (`mag_check.py`) put two vertical
rods at anchor +/-100 mm in x. At lat +90 the +x rod is 644 mm from the source and projects 2417 px tall, against
1844 px for the -x rod, so the geometry magnifies the side the convention says it should.

**Anatomy read from the renders.** At lat 0 the `hip_left` box sits on image right. At **+40**, air and the posterior
skin appear on image LEFT, and at **+90** the posterior soft tissue and natal cleft are on the left: posterior
projects to -u. So +40 is source posterior-left, the right-anterior-oblique family. At **-50** and **-90** the air
and posterior skin are on image RIGHT, so -50 is source posterior-right (LAO) and -90 matches the side of the real
Surgio lateral. This is consistent with `tools/pose_arc.py`.

**What should change:** replace `near_hip_taller_*` in `tools/pose_arc_proof.py` with a crest-depth or
box-top-edge criterion, or use an unclipped marker. The criterion as written can never pass on this detector at
L3 centring. Separately, `spine_boxes_min` counts *projected* boxes, not visible bone. Under the surgio card the
lumbar column is faint at 0 deg and not readable from about 40 deg outward (lat+000, +040, -050, +/-090 opened).
That is the exposure confound the measurement agent reported, and nothing in the proof's checks tests for it.

## 3. Recall JSON vs figure: PASS

Eight spot values read off `fig_recall_vs_angle.png` agree with `recall_vs_angle.json` (conf 0.25). Examples:
pooled/surgio body tilt 0 at -50 = 0.606 [0.461, 0.748] (the visible dip); pooled/elekta body tilt 0 at -10 = 0.952;
LODO A/elekta body tilt -15 at +20 = 0.953; LODO B/surgio body tilt 0 at +20 = 0.279; pooled/surgio sacrum tilt 0
at -30 = 1.000 (n = 9); real_lodo/elekta sacrum at -40 = 0.111 (the only visible real_lodo bump).
I recomputed the falloff from the curves using the stated rule for all 96 cells, and **96/96** agree with the `falloff` block.

Headline, body recall at conf 0.25 and tilt 0, re-read from the JSON (n = 104 boxes at lat 0, 17 subjects):

| detector | card | -90 | -60 | -30 | 0 | +30 | +60 | +90 | first below 90% of lat-0 (-side / +side) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| pooled | surgio_b51_dr | 0.79 | 0.70 | 0.79 | 0.91 | 0.86 | 0.76 | 0.85 | -30 / +40 |
| pooled | elekta_xvi | 0.39 | 0.60 | 0.77 | 0.89 | 0.77 | 0.64 | 0.35 | -30 / +30 |
| LODO A | surgio_b51_dr | 0.21 | 0.13 | 0.32 | 0.26 | 0.35 | 0.15 | 0.18 | -10 / +50 |
| LODO A | elekta_xvi | 0.19 | 0.38 | 0.60 | 0.78 | 0.71 | 0.15 | 0.19 | -30 / +40 |
| LODO B | surgio_b51_dr | 0.13 | 0.06 | 0.36 | 0.40 | 0.44 | 0.15 | 0.16 | -10 / +20 |
| LODO B | elekta_xvi | 0.19 | 0.27 | 0.50 | 0.54 | 0.40 | 0.22 | 0.21 | -40 / +30 |
| real_lodo | surgio_b51_dr | 0.04 | 0.01 | 0.00 | 0.00 | 0.00 | 0.02 | 0.02 | undefined (lat-0 recall 0) |
| real_lodo | elekta_xvi | 0.01 | 0.01 | 0.00 | 0.03 | 0.03 | 0.01 | 0.02 | meaningless at this level |

How to read it:
- The pooled detector on the surgio card is non-monotonic. Recall dips to 0.61 at -50 and recovers to 0.79/0.85 at
  the laterals. That is the shape expected from a detector trained on AP and lateral poses only. It is a reading,
  not a tested cause.
- The LODO A/B surgio-card falloff angles are computed on curves whose lat-0 recall is only 0.26 and 0.40, so they
  are noise-level and should not be quoted as falloff angles.
- real_lodo never detects on these renders.

## 4. Held-out subjects vs training data: PARTIAL

The 17 sweep subjects come from `anglesweep/SET_INFO.json`: s0585 s0970 s1045 s1062 s1159 s1384 s1535 s1579 s1700
s1836 s1842 s1872 s1880 s1883 s1902 s2033 s2053. I matched them against every file basename with the token
`s[0-9]{4}` (grid job 40424737).

- **P / A / B train lists: 0 of 17 present.** Each train list holds 125 distinct TS subjects (12,730 / 5,408 /
  4,676 subject-tagged files), so the regex does find subjects. All 16 styled corpora agree: train has 125
  subjects and 0 held-out; val has exactly these 17.
- **But all 17 are the VAL subjects of P, A and B**, and the scored weights are `best.pt`, which YOLO picks on val
  fitness. The subjects were held out from gradient updates but not from checkpoint selection, on AP, lateral and
  Cios-geometry renders. The arc poses themselves were never seen. "Held out" should be stated as "validation
  subjects", or the sweep should move to subjects outside train and val.
- **rx_lodo_carmlspine_1024 ("real-only") is not clean.** Its own data is real COBRA and DeepFluoro frames with 0
  TS tokens. But it was initialised from `runs/pose/anchor_none_v2_17-1882`, whose **train set contains 5 sweep
  subjects (s0585, s0970, s1045, s1159, s1384)** and whose val set contains s1062. Because its recall is about 0
  everywhere, the leak inflated nothing measurable. The label "real-only / no C-ArmLSpine" in the figure and md is
  still inaccurate about what the network saw, and s0585 is also the proof subject.

## 5. case134 anonymity: PASS

The grid job read 302 headers under `case134/ori` and collected the identifier values without printing them.
Classes found, one value each: PatientID, PatientName, PatientBirthDate, PatientSize, PatientWeight,
InstitutionAddress, StationName, Study/Series/AcquisitionDate. The "case134" pseudonym is excluded by design.

Every byte of every file was scanned, PNGs included (the export's own scan skips PNGs):

| scope | files | files containing any identifier value |
|---|---:|---:|
| `realxray/carmlspine_sweep` | 907 (303 json) | 0 |
| `or_ready/arc/case134_sweep` | 6 | 0 |
| local `SchwingNet/results/arc/` case134 files | 6 | 0 |

The union of key names across the meta files (78 keys) contains no patient, birth, ID or accession field. The only
keyword matches are the English word "patient" in prose ("this patient's two SPOT frames", "ONE patient"). The
three truth PNGs have no text chunks and, as viewed, no burned-in text.

## 6. Sweep boxes on vertebrae: PASS (caveat)

All three truth overlays were opened.
- `frame_00_truth.png` (AP): four boxes sit tightly on four consecutive lumbar bodies.
- `frame_45_truth.png`: the boxes sit on the bodies. The L4 and L5 boxes run posteriorly over the pedicles and are
  about 270 px wide, against about 200 px for the upper two.
- `frame_90_truth.png` (lateral): the top box and the L3 box are on the bodies. The L4 and L5 boxes extend about
  100-120 px posteriorly over the pedicles and foramina. That lowers the IoU a correct body-tight detection can
  reach on those two levels.

The boxes are captioned L1, L3, L4, L5 on four consecutive bodies because TS's L2 was dropped as a duplicate
instance of the same vertebra. The set scores detection only, but anyone reading the overlay will see an L2 that
seems to be missing. The sacrum is not boxed; it was dropped by repair. `overlays()` picks frames by the nearest
|header angle|, so this check does not establish whether frame_90 is at +90 or -90 in the lat_signed convention.

## case134 numbers, re-read from `case134_sweep.json`

Body recall over the 301-frame spin: 1204 truth boxes (4 per frame), one patient, so no interval is valid.

| detector | conf 0.25 | conf 0.74 |
|---|---:|---:|
| pooled | 0.936 (1127/1204) | 0.781 |
| LODO A | 0.372 | 0.292 |
| LODO B | 0.297 | 0.235 |
| real_lodo | 0.495 | 0.494 |

The per-bin hits sum exactly to the pooled fields. The pooled detector saw this patient's two spot frames in
training, which the file itself discloses.
