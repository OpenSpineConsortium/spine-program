# The medical-education visual abstract

Copied on 2026-10-08 from `poster/` of the public repository `CTSpinoPelvic1K`, where the folder is **untracked** (head
7ddfe38; `git ls-files poster` lists nothing), which is why the scripts travel here rather than by reference
(`../../MANIFEST_LOCAL.md` records every file). It is the centre column of the CNS 2026 printed poster on the
OpenSpineConsortium medical-education study (CNS 66639; the study is Cureus 2026;18(7):e112661;
`../../docs/handoff/EXTRACT_MANUSCRIPTS_12.md`). The one-slide decks that use it are routed to `11_students_grid_access`.

| file | what |
|---|---|
| `OSC_visual_abstract.pdf`, `OSC_visual_abstract.png` | the finished figure, 14.5 x 30.8 inches (the poster's middle column), dated 2026-09-01 |
| `ORIGINAL_center_Picture_6.png` | the centre picture it replaced, kept for comparison |
| `make_visual_abstract.py` | draws the figure from `panels/`: four beats (students meet on a call; ITK-SNAP and Colab; the server refuses a save that violates anatomy, quoting the real check; the corrected labels become the findings). Its docstring records two geometry traps: axes-fraction shapes stretch about 3:1 on a 13.6 x 3.9 inch axes, so the call panel works in inches; a portrait CT in a landscape frame with `aspect="auto"` is squashed anatomy, so `place_image()` crops and never rescales |
| `render_0231_panels.py` | the rib half of the before/after: case 0231, where the pseudolabeller split one rib across two ids and called a rib on a lumbar vertebra rib 7; the student's correction turned the second into the finding, a lumbar rib. Resamples the anisotropic voxels (0.545 mm in plane, 0.8 mm through) to isotropic before projecting, so a rib's angle on the poster is the rib's angle |
| `render_0068_panels.py` | the vertebra half: case 0068, where one L1 label covered two bodies so every level beneath was named one too high and L3's mask had 19 % of its bone in a stray blob; renumbered L1-L6 against the twelfth rib, T10-T12 added |
| `spine_qc.py`, `spine_qc_0068.py` | run the three spine checks (`spine_sanity`, `class_mixing_qc`, `spine_extend_qc`) of `scripts/review_anatomy_qc.py` in the `CTSpinoPelvic1K` repository on the before and after revisions and print the failing messages the poster quotes |
| `panels/0231_v4.png`, `0231_v6.png`, `0068_v5.png`, `0068_v6.png` | the rendered before and after rasters at true proportion |
| `panels/markers.json`, `markers_0068.json` | the marker boxes (pixel coordinates per label id and revision) the figure script reads |

## Label ids in these files are the review scheme of 2026-08, not the release scheme

The scripts and markers name lumbar ribs as ids 74 and 75 (`rib_left_lumbar`, `rib_right_lumbar`) and rely on the ITK-SNAP
descriptor `itksnap_v6_labels.txt`. The release (v10, v11) puts lumbar ribs at 60 and 61 and L1-L6 at 20-25
(`../../memory/label-scheme-v4-vs-ostk.md`). Nothing here is to be reused as a label map; it is the record of a figure.

## Regenerating

The inputs are imaging data and are not in this folder: `0231_ct.nii.gz`, `0231_label_v4.nii.gz`, `0231_label_v6.nii.gz`,
`0068_ct.nii.gz`, `0068_label_v5.nii.gz`, `0068_label_v6.nii.gz`, read from the working directory. Where those review
revisions live today is not recorded (the release labels on the grid are v11, a later revision). The descriptor exists
on the grid at `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/itksnap_v6_labels.txt` (5,421 B, 2026-08-27, listed
2026-10-08); the laptop copy was 3,713 B (2026-09-03); which one the 2026-09-01 run used is not recorded. The panels
and markers are copied, so `python make_visual_abstract.py` alone regenerates the figure (matplotlib) without the
volumes. On the grid every render is an `sbatch` job.

## Edits made to the copies

Four scripts carried one absolute laptop path each (`SCHEME = Path(...)` in the two render scripts; `sys.path.insert` in
the two QC scripts). Those lines now read the descriptor from beside the script and the `scripts/` folder of the
repository, and are marked `spine-program edit`. Each script begins with a three-line origin header. Nothing else was
changed; the PNG, PDF and JSON files are byte-identical to their sources.
