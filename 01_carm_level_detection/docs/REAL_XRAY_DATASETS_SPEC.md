# Real X-ray datasets with projected labels: the one format every builder writes

Purpose: train and test the anchor/vertebra detector, and score level naming, on REAL X-ray and fluoroscopy frames
from several devices, with labels projected from a registered CT or CBCT through each frame's known pose. Written
2026-09-21 for four sources: COBRA2026 (Elekta XVI, Varian OBI), DeepFluoro (Siemens Cios Fusion), the Geneva hip
gold standard (Philips BV Pulsera image intensifier), C-ArmLSpine (FIRST Surgio-B51, intraoperative).

## Where

`/rs/rs_grp_oschome/go2432/data/realxray/<dataset>/` on the grid CephFS volume. `<dataset>` is one of
`cobra_elekta`, `cobra_varian`, `deepfluoro`, `geneva_hip`, `carmlspine`.

## Layout

```
<dataset>/
  images/<split>/<stem>.png     8-bit display image (see "Display"), split in {train, val, test}
  labels/<split>/<stem>.txt     YOLO boxes: "cls cx cy w h" normalised to the image; cls 0 = vertebra, 1 = sacrum
  meta/<stem>.json              everything else about the frame (see "Meta")
  splits.json                   {"train": [case ids], "val": [...], "test": [...]} -- split BY CASE/SPECIMEN, never by frame
  data.yaml                     path, train/val/test image dirs, names {0: vertebra, 1: sacrum}
  qc/                           contact sheets: every frame drawn with its boxes and level names (look before training)
  summary.json                  counts per split, per level, per view-angle bin; builder version; date
```

`<stem>` = `<case>_<frame>` with no spaces. Splits are deterministic: sort case ids, assign by
`int(md5(case).hexdigest(), 16) % 10` → 0-6 train, 7 val, 8-9 test, unless a dataset's own documentation fixes a split.

## Display

Every image is converted to ATTENUATION first, then windowed the same way:
- the dataset's own stored value → attenuation (`a = -log(I / I0)` for linear detector signal such as COBRA, with I0
  per frame from the air region or the vendor flood value; the LINEAR reading `(p98 - r)/(p98 - p2)` for a stored log
  display such as DeepFluoro; for others, decide from the DICOM Pixel Intensity Relationship or by the transfer test
  `tools/deepfluoro_transfer.py`, and record the choice in meta);
- then `deepfluoro_anchor.window_or(atten, field)` with DF_WINDOW=or targets: the field's 1/5/50/95/99th percentiles
  mapped onto 27/47/126/216/239 (FluoroCap operating-room medians). Bone is BRIGHT. Pixel size resampled to 0.78 mm
  (DeepFluoro's working size) unless recorded otherwise in meta; anisotropic pixels (Varian) resampled to square first.

## Meta (per frame JSON)

```
{"dataset": "...", "case": "...", "frame": "...", "split": "...",
 "device": {"make": "...", "model": "...", "detector": "flat panel|image intensifier|unknown", "kvp": ..., "mas": ...},
 "source_image": "/abs/path/to/original", "stored_value": "linear|log|unknown", "conversion": "...",
 "px_mm": 0.78, "view": {"gantry_deg": ..., "lat_from_ap_deg": ..., "cranial_caudal_deg": ...},
 "pose": {"source": "machine geometry|fiducials|2D/3D registration|navigation", "K": [[...]], "ext": [[...]],
          "qc_edge_ncc": ..., "qc_log_ncc": ...},
 "boxes": [{"cls": 0, "level": "L4", "box": [x0, y0, x1, y1], "visible_frac": 0.93, "px": 1234}, ...],
 "label_source": "TotalSegmentator vX on <volume>, projected through pose",
 "notes": "..."}
```

Boxes: project every voxel of the mask (subsample to <= 20k points) through K·ext, take the 2nd-98th percentile
extent in x and y (robust to stray voxels), clip to the image; `visible_frac` = share of projected points inside the
image. Keep a box if `visible_frac >= 0.5` and both sides >= 8 px; otherwise drop it and count the drop in summary.
Level names use TotalSegmentator's labels (T12, L1..L5, sacrum). A vertebra box whose level cannot be trusted
(for example the CT does not contain the sacrum AND the level came only from appearance) gets `"level": null`.

## Rules for builders

- Nothing runs on the grid login node: every step (download, segmentation, projection, plotting) is an `sbatch` job.
  CPU: `--partition=reqp --qos=requeue --no-requeue`; GPU: `--partition=gvohp,galhp --qos=gpu --gres=gpu:1`.
  Compute nodes have internet. Logs to `~/model_night/logs/<name>_%j.out`. Use `sbatch -D` or absolute `--output`.
- Network from Windows goes through WSL: `wsl -e bash -lc "ssh -o BatchMode=yes go2432@grid.wayne.edu '...'"`.
  Inline Python heredocs through the Bash tool collapse backslashes: write scripts with the Write tool, scp, run by path.
- Python envs on the grid: `~/mambaforge/envs/fluorogen/bin/python` (torch, numpy, scipy, PIL, SimpleITK, h5py,
  yaml, curl_cffi); `~/mambaforge/envs/totalseg` (TotalSegmentator, being installed by job 40410019 -- read
  `~/model_night/logs/tssetup_40410019.out`); `~/mambaforge/envs/spinedet` (ultralytics 8.4). Always
  `export PYTHONNOUSERSITE=1 TMPDIR=$HOME/tmp`.
- Code lives in `spinesurg-ct-nnunet:tools\` (repo `spinesurg-ct-nnunet`, private,
  branch L6_Class). Copy to `~/spinesurg-ct-nnunet/tools/` on the grid with scp and strip CR with `sed -i 's/\r//'`.
  Do NOT git commit or push: the coordinating session commits.
- LOOK at the QC contact sheets before reporting numbers; a wrong axis, a flipped frame or an inverted polarity makes
  every downstream number plausible and wrong.

## Two labellers (added 2026-09-21 17:25 at Greg's request)

Label every CT/CBCT with BOTH TotalSegmentator and SPINEPS+VERIDAH, and use a level only where they agree.
TotalSegmentator has no L6 and no T13, so on a transitional spine it names a sixth lumbar vertebra wrongly and
silently; VERIDAH can name L6 (VerSe id 25) and T13 (28). Procedure:
1. Write a case table `cases.csv` with columns `case,ct` (NIfTI path of the volume you gave TotalSegmentator).
2. `sbatch --array=0-3 --export=ALL,CASES=<cases.csv>,OUT=<dir>/spineps slurm/spineps_cases.sh` (GPU; resumable).
3. Write `compare.csv` with columns `case,ts_dir,spineps_vert` and run `tools/dual_seg_compare.py --cases compare.csv
   --out <dir>/levels.json` in an sbatch job. It matches each TotalSegmentator vertebra to the SPINEPS instance that
   covers most of it, and gives per vertebra `ts`, `spineps`, `dice`, `agree`, and `level` (the agreed name or null),
   plus per-case `variant_flags` (VERIDAH calls L6 / T13 / names disagree).
4. In each box's meta add `"level_ts"`, `"level_spineps"`, `"level_agree"`; set `"level"` to the agreed name or null.
   Keep boxes with a null level for detection training (they are still vertebrae) but they are excluded from
   level-naming scores. Report the agreement rate and list every variant-flagged case in summary.json.
