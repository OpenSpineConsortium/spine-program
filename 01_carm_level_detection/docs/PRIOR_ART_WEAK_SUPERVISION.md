# Prior art: labels for unannotated radiographs

Scan date 2026-09-14 (OpenAlex, ten queries, top-cited per query, `tools/prior_art_weak.py`). The question
was: FluoroCap has captions but no per-vertebra labels; how does the field get labels onto unannotated
images, and what is that problem called?

## What the problem is called

| Name | What it means | Where it sits in FluoroCap |
|---|---|---|
| Semi-supervised learning, self-training, pseudo-labelling | a model trained on labelled data proposes labels for unlabelled data; confident proposals are kept and the model is retrained (Noisy Student, Xie 2020; Mean Teacher, Tarvainen 2017; FixMatch, Sohn 2020) | films (labelled) -> FluoroCap panels (unlabelled): the detector and level model propose, the run decoder filters |
| Weak supervision | a label at coarser granularity than the target (an image-level caption for a box-level task); text-supervised localisation (CLIP-style, BioViL) | the caption gives the level SET and, with the hardware parser, which vertebrae carry devices; the decoder turns that into per-box labels |
| Model-assisted annotation, pre-annotation, human-in-the-loop | the model pre-fills, a person corrects (CVAT, Label Studio call this pre-annotation) | `fluorocap_annotate.py`: anchor click + contiguity, A/N accept/reject, two readers + adjudication |
| Active learning | choose which unlabelled images to send to the readers first (disagreement, low confidence, rare classes) | caption-vs-model disagreement and low `anchor_margin` order the reading queue |
| Landmark detection, keypoint regression | the annotation act itself: corners or centroids per vertebra | our pose detector (four corners) IS a landmark model; Payer 2019 is the classic spine-landmark method |
| Promptable / zero-shot segmentation | a foundation model (SAM, MedSAM, SAM 2) turns a point or box prompt into a mask without training | optional mask-quality outlines from the detector's boxes; runs locally on the GPU nodes |

Landmark placement is not a different problem from these; it is the ground-truth act that the others
reduce, order, or verify. Nothing replaces the reader for the TEST set. For the TRAINING set,
pseudo-labels constrained by captions and hardware are the standard route.

## Papers the scan surfaced that matter here

- **VerSe** (Sekuboyina et al., Medical Image Analysis 2021, 376 citations): the vertebra labelling benchmark; the reference for "identify each vertebra" evaluation and the source of the CT-side labels in this project.
- **Integrating spatial configuration into heatmap regression based CNNs for landmark localization** (Payer et al., Medical Image Analysis 2019, 371 citations): landmark heatmaps plus a learned spatial-configuration prior; the ancestor of every "corners per vertebra" detector, ours included.
- **Zero-Shot Vertebral Instance Segmentation on DICOM Spine Radiographs Using Promptable Segment Anything Models** (Journal of Clinical Medicine 2026): SAM with box/point prompts on radiographs, no training; the option for mask outlines from our boxes.
- **Semi-Supervised Vertebra Segmentation and Identification in CT Images** (Tomography 2026): teacher-student pseudo-labelling for vertebra identification, the recipe transposed to 2-D here.
- **Bidirectional Copy-Paste for Semi-Supervised Medical Image Segmentation** (2023): the labelled/unlabelled mixing trick that stabilises self-training; applicable to our crops.
- **SAM Fewshot Finetuning for Anatomical Segmentation in Medical Images** (2024): what it costs to adapt SAM with a handful of labelled cases.
- **Hide-and-Seek Attribution: Weakly Supervised Segmentation of Vertebral Metastases in CT** (2025): image-level labels to voxel-level output, the weak-supervision pattern.

The remaining rows of the scan were reviews or off-topic hits and are listed in the raw table below only
for completeness.

## What was NOT found

No paper uses caption-named hardware (screws in named vertebrae) as a per-vertebra constraint for level
identification on radiographs. Text-supervised localisation exists for chest radiographs (BioViL, MIMIC-CXR
report grounding) but not for spinal levels. That combination, caption -> device -> vertebra -> constraint on
a contiguous run, is implemented in `tools/fluorocap_hardware.py` + `tools/fluorocap_anchor.py` and appears
to be new.

## Raw scan table

| Year | Title | Venue | Cited | Found by |
|---|---|---|---|---|
| 2021 | VerSe: A Vertebrae labelling and segmentation benchmark for multi-detector CT images | Medical Image Analysis | 376 | pseudo-label vertebra detection x-ray |
| 2019 | Integrating spatial configuration into heatmap regression based CNNs for landmark localization | Medical Image Analysis | 371 | pseudo-label vertebra detection x-ray |
| 2013 | The current state-of-the-art of spinal cord imaging: Methods | NeuroImage | 345 | (off topic) |
| 2019 | Artificial intelligence and machine learning in spine research | JOR Spine | 334 | (review) |
| 2009 | Minimally invasive spine technology and minimally invasive spine surgery: a historical review | Neurosurgical FOCUS | 233 | (review) |
| 2020 | The Role of Machine Learning in Spine Surgery: The Future Is Now | Frontiers in Surgery | 113 | (review) |
| 2022 | A Review of the Methods on Cobb Angle Measurements for Spinal Curvature | Sensors | 99 | (review) |
| 2024 | Artificial Intelligence in Spinal Imaging and Patient Care: A Review of Recent Advances | Neurospine | 67 | (review) |
| 2023 | Revolutionizing Spinal Care: Current Applications and Future Directions of AI | Journal of Clinical Medicine | 63 | (review) |
| 2023 | Bidirectional Copy-Paste for Semi-Supervised Medical Image Segmentation | arXiv | 13 | teacher student vertebra segmentation |
| 2023 | Sparse annotation learning for dense volumetric MR image segmentation with uncertainty estimation | Physics in Medicine and Biology | 5 | teacher student vertebra segmentation |
| 2026 | Neuro-Geometric Graph Transformers with Differentiable Radiographic Geometry for Spinal X-Ray Image Analysis | Journal of Imaging | 3 | teacher student vertebra segmentation |
| 2026 | Zero-Shot Vertebral Instance Segmentation on DICOM Spine Radiographs Using Promptable SAM | Journal of Clinical Medicine | 1 | MedSAM vertebra x-ray |
| 2026 | Semi-Supervised Vertebra Segmentation and Identification in CT Images | Tomography | 1 | teacher student vertebra segmentation |
| 2026 | CervSpineNet: segmentation of cervical spinous processes | Frontiers in Bioengineering | 0 | MedSAM vertebra x-ray |
| 2025 | Hide-and-Seek Attribution: Weakly Supervised Segmentation of Vertebral Metastases in CT | arXiv | 0 | MedSAM vertebra x-ray |
| 2024 | SAM Fewshot Finetuning for Anatomical Segmentation in Medical Images | arXiv | 0 | MedSAM vertebra x-ray |

## Competitor note: xvr (Gopalakrishnan et al., MIT CSAIL / Harvard, arXiv 2503.16309v2, May 2026)

"Rapid patient-specific neural networks for intraoperative X-ray to volume registration". A different
problem: 2-D/3-D rigid registration of a C-arm image to the patient's OWN preoperative CT or MR, giving the
C-arm pose (level identity follows only implicitly, as in LevelCheck). ResNet-34 pose regressor, pretrained
on 2,245 volumes, then 5 minutes of patient-specific fine-tuning on renderings of that patient's scan,
plus iterative refinement (1–8 s per image). Reported mTRE 0.9 mm (DeepFluoro, six cadaver pelves),
1.2 mm on 122 clinical neurosurgical X-rays. Code released, CC BY 4.0 (xvr.csail.mit.edu).

What it needs that we do not: a preoperative volume for every patient, calibrated intrinsics, five minutes
of GPU training per patient before the case, and seconds per frame at run time. It cannot answer "which
level is this" for a patient without a scan, and none of its public test sets contain a spine (pelvis,
femur, cerebral DSA). Our claim is the complement: level identity from the image alone, milliseconds,
no scan, no per-patient training. A head-to-head is only possible on data with both a CT and
intra-operative images; CTSpinoPelvic1K DRRs plus FluoroCap give the no-scan side, and a small paired
set (ours, prospectively) would give the other. Their renderer and self-supervised pose labels are the
same idea as our DRR crop banks; nothing in it bears on level naming.

## Purchasable data (checked 2026-09-14)

No marketplace lists intra-operative spine fluoroscopy. Segmed (segmed.ai) and Gradient Health sell
de-identified hospital imaging (CT/MR/X-ray) under licence and can be asked for spine radiographs and
C-arm captures by procedure code; that is a quote, not a catalogue item. The "ex-vivo paired real X-ray +
DRR" lumbar sets from the 3-D reconstruction papers (X23D, Jecklin et al.) are withheld for patent reasons
and available on request only. VinDr-SpineXR (PhysioNet DUA) remains the only large annotated public
spine radiograph set; DeepFluoro is pelvic.
