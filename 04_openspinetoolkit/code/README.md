# code/

Scripts this project needs that are in no repository. Each file carries a header saying where it came
from (a working folder or a grid path), its date and, for the grid files, the sha256 of the text as read.
The OpenSpineToolkit code itself is not copied: it is referenced by commit in `../MANIFEST_CODE.md`.

## `pre_ostk_2026-05/` (lineage; superseded)

The scripts of 2026-05-17 that preceded ostk, kept as dated lineage: `spine_analysis_v316.py` and
`spine_analysis_v317.py` (TRALL lumbar lordosis after Chernukha, with body centroids as the arc landmarks;
v317 is v316 with small edits and still says "v316" in its docstring), `test.py`, `test_v2.py`, `test_v3.py`
(hip sphere fit and pelvic incidence on case 0022), `vertebral_corners.py` (the four sagittal corners of each
lumbar body and the wedging angles on the Hugging Face sample). They read the May 2026 sample export under the
legacy label map (L1 = 1 ... femur_right = 12) and must not be run on a v11 volume without
`ostk.labels.labels_for(volume)`. Nothing in `TODO.md` depends on them.

## `grid_ostk_run_2026-09-10/` (the shard run that made the committed CSV)

Read from the grid on 2026-10-09 00:12 UTC (`../MANIFEST_GRID.md` section 1):

| file | grid path | role |
|---|---|---|
| `ostk_extract.py` | `/wsu/home/go/go24/go2432/ostk_run/ostk_extract.py` (03:41) | the 24-shard per-level extractor; `FIELDS` names `PDW_l`, `PDW_r`, `PDW` and drops every other key, which is why the committed PDW columns are empty (`../STATUS.md` G.4) |
| `ostk_morph.py` | `~/ostk_run/ostk_morph.py` (03:01) | the 60-case check of the frame-based estimator against Panjabi 1992, with the old posterior-height estimator beside it |
| `ped_batch.py` | `~/ostk_run/ped_batch.py` (06:02) | pedicle width over many cases against four published series; imports `pedicle_dev.isthmus_width` |
| `pedicle_dev.py` | `~/ostk_run/pedicle_dev.py` (05:59) | `isthmus_width`: the pedicle as the narrowest neck between body and arch, by erosion; the function behind the 118-pedicles-per-level table; a different method from `ostk.morphometry.pedicle_widths` |
| `pdw_why.py` | `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/pdw_why.py` (16:00) | probes where `pedicle_widths` bails on L1 and L5 of named cases (body, canal, the three resamples) |

They expect `OpenSpineToolkit/` beside them on `sys.path` (the grid copy `~/ostk_run/OpenSpineToolkit`) and
a labels folder of `NNNN_label.nii.gz`; on the grid they run only as `sbatch` jobs with
`~/mambaforge/envs/spineps/bin/python`.
