---
license: cc-by-4.0
task_categories:
- image-segmentation
language:
- en
size_categories:
- n<1K
tags:
- medical-imaging
- spine
- ct
- segmentation
- vertebra
- lstv
- tltv
- verse
pretty_name: "VerSeFusion: Re-fused VerSe 2019+2020 with VERIDAH corrections"
---

# VerSeFusion-Sample

A re-fused, PIR-canonical version of the VerSe 2019 and VerSe 2020 vertebra
segmentation challenges, with VERIDAH (Möller 2026) label corrections applied
for thoracolumbar transitional vertebrae.

## Dataset stats

- **Total scans:** 10
- **Total patients:** 10
- **Splits:** training=1, validation=4, test=5
- **Source:** VerSe 2019 + VerSe 2020 (combined) with VERIDAH corrections
- **Canonical orientation:** PIR (axis 0 = P, axis 1 = I, axis 2 = R)
- **VERIDAH-corrected subjects:** 0

## Orientation

Every scan in this dataset has been reoriented to a single canonical frame:

- **axis 0** increases toward **P** (posterior — i.e., anterior → posterior)
- **axis 1** increases toward **I** (inferior — i.e., superior → inferior; this is the spine axis)
- **axis 2** increases toward **R** (right — i.e., left → right)

This is verified end-to-end: see `orientation_audit.json` for the
per-subject report.  Rendering conventions in `previews/`:

- **Coronal:** head at top, patient's right at viewer's right
- **Axial:** anterior at top, patient's right at viewer's right
- **Sagittal:** head at top, anterior at left

## Structure

```
gregoryschwingmdphd/VerseFusion-Sample/
├── README.md
├── LICENSE
├── splits.csv                  # series_id → split (training/validation/test)
├── orientation_audit.json      # per-subject orientation verification
├── scans/
│   └── <series_id>/
│       ├── ct.nii.gz           # CT volume, HU values, PIR-oriented
│       ├── mask.nii.gz         # vertebra labels (uint8), PIR-oriented
│       └── meta.json           # per-scan origin
├── corrections/
│   └── veridah_manifest.json   # which subjects had labels corrected
└── previews/                   # optional QC renders
    └── <series_id>.png
```

## Label schema

| Label | Anatomy | | Label | Anatomy |
|-------|---------|-|-------|---------|
| 1–7   | C1–C7   | | 20    | L1 |
| 8     | T1      | | 21    | L2 |
| 9     | T2      | | 22    | L3 |
| 10    | T3      | | 23    | L4 |
| 11    | T4      | | 24    | L5 |
| 12    | T5      | | 25    | L6 (supernumerary lumbar) |
| 13    | T6      | | 26    | sacrum (variably annotated) |
| 14    | T7      | | 27    | coccyx |
| 15    | T8      | | 28    | T13 (supernumerary thoracic) |
| 16    | T9      | | | |
| 17    | T10     | | | |
| 18    | T11     | | | |
| 19    | T12     | | | |

## Loading example

```python
import nibabel as nib

ct  = nib.load("scans/verse001/ct.nii.gz")
msk = nib.load("scans/verse001/mask.nii.gz")

# Both are guaranteed to be PIR-oriented:
assert nib.aff2axcodes(ct.affine)  == ('P', 'I', 'R')
assert nib.aff2axcodes(msk.affine) == ('P', 'I', 'R')
```

## Citation

If you use this dataset, please cite the original VerSe challenges and the
VERIDAH corrections paper:

```bibtex
@article{sekuboyina2021verse,
  title={VerSe: A vertebrae labelling and segmentation benchmark for multi-detector CT images},
  author={Sekuboyina, A. and others},
  journal={Medical Image Analysis},
  year={2021}
}

@article{loffler2020verse2020,
  title={A vertebral segmentation dataset with fracture grading},
  author={Löffler, M.T. and others},
  journal={Radiology: Artificial Intelligence},
  year={2020}
}

@article{moller2026veridah,
  title={VERIDAH: Vertebral identification and transitional anomaly detection},
  author={Möller, H. and others},
  year={2026}
}
```

## Acknowledgments

VerSe challenge data: Technical University Munich.  VERIDAH corrections:
H. Möller et al. (2026).


## Note: this is a sample

This is a 10-scan sample from the full dataset, chosen as the most-completely-labeled scans (highest unique-vertebra-label count, with VERIDAH-corrected subjects prioritized to showcase the thoracolumbar transitional-vertebra corrections).

For the full VerSeFusion dataset, see: https://huggingface.co/datasets/gregoryschwingmdphd/VerseFusion
