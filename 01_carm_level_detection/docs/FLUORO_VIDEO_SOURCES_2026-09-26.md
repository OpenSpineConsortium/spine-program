# Public spine fluoroscopy video for a temporal test set (deep research, 2026-09-26)

Question: every publicly available source of spine fluoroscopy VIDEO (lateral or AP) to test the vertebra detector and level-naming network on consecutive frames and track vertebrae. Workflow wf_0a5da043-1a5: 6 search angles, 22 sources fetched, 106 claims extracted, 25 verified by three adversarial votes, 21 confirmed, 4 refuted.

## Summary

None of the confirmed sources is an open download of spine fluoroscopy video with vertebra labels. The best-labelled spine cine sets all have to be requested from their authors: (a) the Maastricht lateral cervical flexion-extension cine (112 recordings, 1024x1024, 15 fps, uncompressed, C0-C7 contours on every frame); (b) the Bournemouth cervical quantitative-fluoroscopy (QF) set, where the per-frame, level-named vertebral-corner tracks for 252 sequences from 63 people are public under CC BY 4.0 but the DICOM cine is not; (c) the Bournemouth lumbar L2-S1 QF set (127 subjects, 15 fps, with only per-frame angles public on OSF); and (d) the Pittsburgh swallow-study corpus (about 1,500 lateral clips at 30 fps, with corner landmarks on C2 and C4 only). The only confirmed open spine download is C-ArmLSpine (Zenodo, CC BY 4.0): 149 lumbar AP+lateral stills with paired intraoperative CBCT. Two of its cases contain raw CBCT projection sweeps, which are the only confirmed consecutive-frame sequences that come with a paired volume. No confirmed source records overlapping frames at a known cranio-caudal displacement. The single overlapping cranio-caudal series found (PUMCH, 43 scoliosis patients, AP stills) is not released. This run did not re-verify the already-known sources, simulated or cadaver sequences, or injection video beyond one AJR teaching article. The most useful next step is to ask Bournemouth for the cervical and lumbar DICOM cine, since the cervical per-frame track labels are already public.

## Confirmed findings

### (high, vote 3-0 (specs); 3-0 (access))

Maastricht dynamic cervical X-ray set (van Santbrink et al., Bioengineering 2026). Lateral cervical flexion-extension cine: 112 recordings, 89 from 39 healthy people and 23 from preoperative patients with cervical radicular syndrome. Recorded on three systems (Siemens Arcadis Avantic VC10A, Toshiba Infinix Vi, Philips Allura Xper FD20) at 1024x1024 and 15 fps with no compression; the paper does not name the file container. Access is by request only; no code or weights are released. This source is described only in a paper.

Evidence: Methods: 'All systems recorded at a resolution of 1024 x 1024 pixels and a frame rate of 15 frames per second. No compression was applied to the images.' Searches of the text for DICOM, cine, AVI, MP4, format and PACS found nothing. Data statement: 'available on request from the corresponding author due to privacy restrictions.' No GitHub, Zenodo or weights link appears in either this paper or its predecessor (PMID 40722371), and a web search found no release. Ethics: Maastricht UMC committee under WMO, with informed consent. The predecessor paper reports about 52 frames per recording (4,671 frames over 89 recordings). A separate claim of about 150 frames per recording (10 s at 15 fps) was refuted 0-3. The route the paper states is 'on request'; a DUA is inferred, not stated.

Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC13024292/, https://doi.org/10.3390/bioengineering13030351, https://pmc.ncbi.nlm.nih.gov/articles/PMC12292518/

### (medium, vote 2-1)

The Maastricht labels are per-vertebra contours named C0 (skull base, from a sella/clivus template) through C7, on every frame, and each vertebra keeps its identity through the sequence. In practice this is level-named segmentation with track IDs. Two raters drew each contour once on the median frame. Normalized-gradient-field template matching carried it to the other frames, and the contours were checked and corrected by hand on every frame. An nnU-Net v2 (ResEnc M) trained on these labels is scored per level.

Evidence: Quote: 'Template areas containing each vertebral body and the skull base were manually drawn ... in the median frame of the recording, labeled C0-C7 ... matching normalized gradient field images ... The contours were manually checked and adjusted in every frame when necessary.' Table 2 gives Dice, IoU and HD95 per level. C0 Dice is about 0.69-0.71, and C0 is left out of the motion analysis. Limits: each frame's shape is a moved copy of the median-frame template, not an independent drawing. The authors say the odontoid and the spinous-process landmark were annotated inconsistently. An earlier study that fed this dataset analysed only C4-C7, so full C0-C7 labelling may come from re-annotation.

Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC13024292/

### (high, vote 3-0)

Bournemouth cervical QF, BORDaR 385 (Branney, Breen and Breen; doi:10.18746/bmth.data.00000385; CC BY 4.0; open download). The deposit holds only derived data: Cervical Database.mat (24 MB), seven .xls workbooks and a README. It contains no DICOM or video. The .mat stores per-frame 4-corner vertebral templates, with level identity from C0 to T1, as pixel X,Y coordinates at 15 Hz. These are ready-made level-named track labels with no pixels attached. The source images are lateral cine, 16-bit DICOM at 1024x1024 and 15 fps; the README describes them but they are not deposited.

Evidence: README: 'fluoroscopic images were acquired in the lateral view at 15 frames per second. Anonymised images were exported in DICOM format (16bit 1024x1024 pixels).' Templates were placed by hand on the first frame five times, then carried forward by automatic tracking; templates that failed were removed or re-tracked, and the survivors averaged. Failed frames are stored as NaN. Loading the .mat with scipy showed: Database.Templates is 126 imaging events x (flexion, extension) = 252 sequences; 63 people, each at baseline and at a 4-week follow-up; 181-339 frames per sequence (median 301, about 12-23 s); coordinates 57-957 px. Level fill across 126 events: C1-C6 in 123-126, C0 in 22-26, C7 in 22-28, T1 in 3-4. The companion article (Branney et al. 2024, J Funct Morphol Kinesiol 9(1):55, PMC10970965) reports 29 neck-pain patients and 30 controls on a Siemens Arcadis Avantic VC10A, with underlying data available on reasonable request. README.rtf alone is CC BY-ND. A claim that the motion frame ran at 6 deg/s to 60 deg with the centre of rotation at C3-C4 did not survive verification (0-3).

Sources: https://bordar.bournemouth.ac.uk/385/, https://bordar.bournemouth.ac.uk/385/9/README.pdf, https://doi.org/10.3390/jfmk9010055

### (high, vote 3-0)

Bournemouth lumbar QF reference database (Breen et al., Front Bioeng Biotechnol 2021, doi:10.3389/fbioe.2021.745837). Lateral, weight-bearing L2-S1 cine at 15 fps on a Siemens Arcadis Avantic C-arm, in 131 asymptomatic adults recruited and 127 analysed. Each performed a guided 60-degree flexion-and-return arc at 6 deg/s. The public OSF deposit (osf.io/a27py) holds only per-frame vertebral midplane angles in seven .xls files. The raw cine is described only in the paper and must be requested. This is the only confirmed lumbar cine source.

Evidence: Four participants were excluded for tracking errors on at least one vertebra. Table 1 gives 48.8% female among the 127. The paper states no resolution, frames per sequence or clip length; at 6 deg/s a 60-degree arc implies about 10 s and about 150 frames per phase, but that is not stated. The OSF API lists seven .xls files, about 17.2 MB in total: WB/recumbent flexion and extension normative sets, 8 controls, 8 non-mechanical patients and demographics. The node has no child components and no image, video or DICOM files. The paper's data statement covers only the article and its supplementary tables and directs further inquiries to the corresponding author.

Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC8503612/, https://osf.io/a27py/

### (high, vote 3-0)

Pittsburgh videofluoroscopic swallow corpus (Sejdic/Coyle; NIH R01HD074819). About 1,500 lateral swallow clips captured by video card, not DICOM cine. Zhang et al. 2021 (Med Image Anal 74:102218) used 1,518 clips from 265 patients on a Toshiba Ultimax (2012-2015), with 70 healthy volunteers on a GE Precision 500D (2018-2019) as a separate test set on a different machine. Li et al. 2024 (J Imaging Inform Med 37:1922) used 1,488 clips and 59,468 frames from 238 subjects (187 patients, 51 healthy). Frames were captured at 60 fps from 30-pulse/s fluoroscopy through an AccuStream Express HD card and LabVIEW, then downsampled to 30 fps. Resolution is 720x1080 for patients and 1280x1024 for volunteers. The corpus is not public: Li 2024 says 'available from the corresponding author by request' and Zhang 2021 has no data statement.

Evidence: Zhang 2021: more than half the videos were excluded for patient motion, the shoulder hiding C4, or poor exposure. Li 2024: all frames were resized to 448x448. The corresponding author is Ervin Sejdic (University of Toronto, [e-mail withheld]); Pitt IRB approval with informed consent. Searches of Zenodo, PhysioNet and GitHub found no public copy. The 2012-2015 Ultimax cohort overlaps between the two papers, but the counts differ (1,518 clips / 265+70 subjects vs 1,488 clips / 238 subjects), so they are different subsets of one corpus. 720x1080 is reproduced as printed in both papers.

Sources: https://doi.org/10.1016/j.media.2021.102218, https://pmc.ncbi.nlm.nih.gov/articles/PMC8560570/, https://link.springer.com/article/10.1007/s10278-024-01039-4, https://pmc.ncbi.nlm.nih.gov/articles/PMC11300761/

### (high, vote 3-0)

On question (2): in the Pittsburgh corpus the vertebrae are annotated, but only thinly. There are named corner landmarks on every frame, with no boxes, no segmentation, no other cervical levels and no track IDs. Zhang 2021 marks the anteroinferior corner of C2 and the anterosuperior and anteroinferior corners of C3 and C4, frame by frame in MATLAB (59,810 frames). C3 is labelled only on the first three frames of each subject, so in practice the per-frame labels are C2 and C4. Li 2024 labels the anterior-inferior corners of C2 and C4 plus two hyoid points on every frame. Annotation covers only the swallow window, from the bolus at the mandible until it passes the UES.

Evidence: Zhang: 'annotated the landmark frame by frame in MATLAB ... the head and tail of third vertebra were labeled on only first three frames of each subjects.' Li: 'anterior-inferior corners of the C2 and C4 vertebrae. All landmarks were labeled on all video frames'. Raters had to reach an ICC of at least 0.9 before annotating and kept it on 1 swallow in 10. Li's network outputs four heatmap channels: two vertebral points and two hyoid points. For a level-naming test this gives two named cervical anchors per frame, and the field is centred on the hyoid rather than on the spine.

Sources: https://doi.org/10.1016/j.media.2021.102218, https://link.springer.com/article/10.1007/s10278-024-01039-4

### (high, vote 3-0)

C-ArmLSpine (ZWC-SMU / Feng Qianjin; Zenodo 10.5281/zenodo.22768651; CC BY 4.0; open, with no registration or DUA). 149 intraoperative spine cases from a Surgio-B51 mobile C-arm (FIRST). Each case pairs AP and lateral 2-D images with a CBCT volume from the same device, which makes this the only confirmed open spine source with a paired volume. The files are stills, not cine, with two exceptions: raw CBCT projection sweeps in case134/ori and case39/CBCT (301 XA files) at quantised, known gantry angles. These are the only confirmed consecutive-frame sequences of one subject with a paired volume. The motion is a rotational arc, not a cranio-caudal translation. The release has no labels.

Evidence: README: '149 cases collected during routine intraoperative imaging procedures, with each case providing paired 2D X-ray views, including anteroposterior (AP) and lateral (Lat) projections, together with a corresponding 3D CBCT volume'. The Zenodo API shows one 15,581,614,253-byte C-ArmLSpine.zip, v1, published 2026-09-17, and an unauthenticated HEAD request returns 200. The README never says 'lumbar'; only the name implies it. The project's own inspection of the archive (spinesurg-ct-nnunet/docs/HANDOFF_2026-09-21_PM.md) adds: CBCT is 394^3 at 0.5 mm covering about T12/L1-S1; case134 has no C-arm frames outside CBCT/; case118 is AP plus a -58 deg oblique, so 148 usable AP+lateral pairs; DICOM PixelSpacing 1.0 is a placeholder (true about 0.15 mm); there is no FrameOfReferenceUID; the frames predate the CBCT by 1-2 min; all 149 cases fall on five days about 4 min apart with no instrumentation, and whether the subjects were living or cadaver is unknown. The claim that the dataset is stills only was refuted 0-3 because of these sweeps.

Sources: https://github.com/ZWC-SMU/C-ArmLSpine, https://zenodo.org/records/22768651, https://doi.org/10.1016/j.media.2024.103283

### (medium, vote 3-0)

On question (3): Neurosurgical Focus: Video publishes every article under CC BY 4.0, and PMC serves the full MP4. That makes it a legally reusable library of spine-surgery video, frames included, with attribution. The one article checked is not useful for tracking. PMC13418632 (Duke, TrackX-assisted prone lateral lumbar interbody fusion, L3-5, DOI 10.3171/2026.4.FOCVID2643, PMID 42529588) is a 200.3 MB compressed MP4 of about 8 min 26 s. It shows saved AP and lateral C-arm stills under a live instrument-tracking overlay, not continuous cine of moving vertebrae.

Evidence: The JATS licence reference is creativecommons.org/licenses/by/4.0 with specific-use=textmining, and the journal policy page says the journal is 'published under the ... CC BY 4.0 license' (a web summary claiming CC BY-NC-ND was wrong). Transcript: TrackX gives 'real-time tracking of instrument overlay on saved AP and lateral fluoroscopic images'; the workflow is designed for 'less images required'. Separately, TrackX cuts x-ray shots by 78% (IJSS 2020, PMC7343269). Scripted download hits a JavaScript proof-of-work cookie gate; a browser passes it. CC BY does not license privacy or publicity rights, and a footer on the AANS site reserves TDM/AI-training rights. Other spine videos in the journal were not screened, which is why confidence is medium.

Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC13418632/, https://stream.cadmore.media/r10.3171/2026.4.FOCVID2643, https://thejns.org/page/72659, https://pmc.ncbi.nlm.nih.gov/articles/PMC7343269/

### (high, vote 3-0)

The only confirmed series of overlapping cranio-caudal shots of one subject is Liu et al., PUMCH (Eur Spine J 2026, DOI 10.1007/s00586-026-09872-7, PMID 41910750). It covers 43 scoliosis patients (62 screened, 2018-2023, single centre) on a Philips Zenition 70. The C-arm was stepped along the cranio-caudal axis for 4-6 prone AP exposures per patient at 512x512, aiming for 20-30% overlap. The shift between shots is estimated by registering on detected pedicle screws, not recorded. These are stills, AP only, and not released; the source exists only in the paper.

Evidence: Full text: 'The C-arm was translated stepwise along the cranio-caudal axis with minimal rotation changes and an intended 20-30% overlap between adjacent segments'. Data statement: 'No datasets were generated or analysed during the current study'. There is no code or supplement. The article itself is CC BY-NC-ND 4.0. The related SX-Stitch paper (arXiv 2409.05681, PUMCH) has no public dataset. Reading the displacement as estimated rather than recorded is an inference from the method; the paper does not say so in those words.

Sources: https://pubmed.ncbi.nlm.nih.gov/41910750/, https://doi.org/10.1007/s00586-026-09872-7

### (high, vote 3-0)

On question (4), only one item survived verification: Rosas and Lee, 'Performing fluoroscopically guided interlaminar lumbar epidural injections', AJR 2012;199(2):419, DOI 10.2214/AJR.12.8541, PMID 22826406. It is a single step-by-step teaching video article, indexed as Video-Audio Media. It is not a dataset. Its licence, frame content and whether it contains live fluoroscopy loops were not established.

Evidence: The PubMed and Crossref records agree (one page, August 2012). The AJR page returned HTTP 403 to automated fetches, so every detail comes from bibliographic records. It is of low value for a test set unless the video turns out to contain continuous lateral or AP lumbar fluoroscopy and AJR reuse terms allow extracting frames.

Sources: https://www.ajronline.org/doi/10.2214/AJR.12.8541, https://pubmed.ncbi.nlm.nih.gov/22826406/

### (medium, vote derived from 3-0 and 2-1 claims)

On question (6), vertebra-tracking methods: three groups track vertebrae across fluoroscopic frames, and all on data they have not released. (a) Maastricht: NGF template matching to build the labels, then per-frame nnU-Net v2 segmentation scored per level (C0 Dice about 0.70; other levels are in their Table 2). (b) Bournemouth: manual 4-corner templates on the first frame (five repeats), then automatic image tracking. This failed badly enough to exclude 4 of 131 lumbar subjects, and left 3,776 NaN coordinates in the cervical .mat. (c) Pittsburgh: per-frame heatmap landmark networks for C2 and C4 corners (Zhang 2021, detection then landmarking; Li 2024, 4-channel heatmaps). None releases a tracking benchmark with public images.

Evidence: Assembled from the verified method descriptions above. Only Maastricht's C0 Dice appears in the surviving evidence. Per-level accuracy for C1-C7, the Bournemouth tracker's error, and the Pittsburgh landmark errors were not captured, so this finding does not answer the accuracy part of question (6).

Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC13024292/, https://bordar.bournemouth.ac.uk/385/, https://pmc.ncbi.nlm.nih.gov/articles/PMC8503612/, https://doi.org/10.1016/j.media.2021.102218, https://link.springer.com/article/10.1007/s10278-024-01039-4

### (medium, vote synthesis)

The requested flags. Consecutive overlapping frames of one subject at a KNOWN cranio-caudal displacement: none of the confirmed sources has this. The kinematic cine sets move by flexion and extension, and the Bournemouth lumbar protocol fixes a known angular rate (60 deg at 6 deg/s), not a translation. The PUMCH series is cranio-caudal, but its displacement is estimated and the data are unreleased. Paired CT: only C-ArmLSpine, and that is intraoperative CBCT from the same C-arm, not diagnostic CT. None of the cine sources has paired CT.

Evidence: This is a synthesis across the verified set. Its confidence is capped because the run did not verify DeepFluoro, Pelphix, LevelCheck, CM Spine or DeepDRR-style simulations, some of which may carry paired CT or known pose.

Sources: https://zenodo.org/records/22768651, https://pubmed.ncbi.nlm.nih.gov/41910750/, https://pmc.ncbi.nlm.nih.gov/articles/PMC8503612/

### (medium, vote judgement)

Ranked shortlist for a spine video test set, with the next step for each. (1) Bournemouth cervical QF, BORDaR 385: the per-frame level-named C1-C6 corner tracks for 252 sequences are already public. Email [e-mail withheld] citing doi:10.18746/bmth.data.00000385 and 10.3390/jfmk9010055, and ask for the anonymised 16-bit DICOM sequences keyed to the .mat event IDs. (2) Bournemouth lumbar QF (Breen 2021): the only confirmed lumbar cine. In the same request, write to the corresponding author of 10.3389/fbioe.2021.745837 for the L2-S1 cine behind osf.io/a27py, and ask whether corner templates exist as they do for the cervical set. (3) Maastricht cervical: best existing per-frame C0-C7 segmentation with identity. Email the corresponding author of 10.3390/bioengineering13030351 for the recordings and contours, and expect a Dutch WMO/GDPR data-transfer agreement. (4) C-ArmLSpine: open now and already in the project's hands. Extract the case39 (301 XA) and case134/ori projection sweeps, fix the PixelSpacing placeholder, and project CBCT level labels through the known gantry angles to get per-frame level ground truth. Only two sequences, and rotational. (5) Pittsburgh swallow corpus: email [e-mail withheld] citing R01HD074819, and expect a Pitt DUA. It has many clips, but only C2 and C4 anchors. (6) Neurosurgical Focus: Video: search PMC for spine articles in the journal, download MP4s in a browser, and screen them for live fluoroscopy segments. CC BY 4.0 with attribution, compressed. (7) PUMCH stitching series: email the corresponding author, Liang J; the data statement says no datasets, so success is unlikely. (8) AJR Rosas and Lee: view the video to see whether it shows live fluoroscopy and check AJR reuse terms. Lowest value.

Evidence: The ranking weighs how complete the labels are, relevance to the lumbar level, and how easy the data are to obtain. Items 1-3 and 5 depend on authors agreeing, which is not guaranteed. Item 4 is the only one usable today, but it does not test tracking under translation. The ranking is a judgement built on the verified facts, not a verified claim in itself.

Sources: https://bordar.bournemouth.ac.uk/385/, https://osf.io/a27py/, https://pmc.ncbi.nlm.nih.gov/articles/PMC13024292/, https://zenodo.org/records/22768651, https://link.springer.com/article/10.1007/s10278-024-01039-4, https://thejns.org/page/72659, https://pubmed.ncbi.nlm.nih.gov/41910750/, https://pubmed.ncbi.nlm.nih.gov/22826406/

## Refuted (0-3)

- The Maastricht dynamic cervical-spine X-ray dataset has 112 flexion-extension cine recordings: 89 from 39 healthy individuals and 23 from preoperative patients. Each subject moved from full extension to full flexion and back in about 10 s. At 15 fps that is roughly 150 consecutive frames per recording, which makes it a candidate lateral cervical video test set. (https://pmc.ncbi.nlm.nih.gov/articles/PMC13024292/)

- The source recordings are lateral-view cervical flexion and extension cine at 15 fps and 1024x1024 at 16 bit. They were taken on a Siemens Arcadis Avantic VC10A fluoroscope with a motorised motion frame: 6 deg/s up to 60 deg of flexion or extension, with the centre of rotation aligned to C3-C4. (https://bordar.bournemouth.ac.uk/385/)

- The dataset is still images, not video. Each case has one AP and one lateral projection. The README gives no cine or multi-frame sequence, frame rate, resolution, file format, or annotation type (no boxes, landmarks, level names, segmentation or track IDs). Any labels would have to be derived, for example by 2D/3D registration to the paired CBCT. It cannot serve as a consecutive-frame tracking test on its own. (https://github.com/ZWC-SMU/C-ArmLSpine)

- This source is only described in a paper, not a released dataset, and it contains no spine video. The cadaver experiment used discrete multi-view C-arm shots, one spine image per C-arm view plus one image for each injection-device pose. The full text (PMC10544812) never mentions video, cine, continuous fluoroscopy or frame rate. It has no data-availability statement and releases no fluoroscopic images or CT; only code is linked. (https://doi.org/10.1109/tmrb.2022.3196321)


## Caveats

Coverage is incomplete. Only 21 claims survived, and none concern the already-known sources the user asked to have verified and extended: DeepFluoro, Pelphix, Veriserum, CAMS-Knee, CM Spine, LevelCheck, CADICA, ARCADE and XCAD. Their status is unchanged by this run, neither confirmed nor refuted. Question (5), simulated or cadaver sequences with ground-truth pose or paired CT, has no verified source: the one cadaver candidate (the TMRB 2022 injection-robot paper, doi:10.1109/tmrb.2022.3196321, PMC10544812) was refuted 0-3, and its actual contents remain unresolved. Question (4) rests on a single AJR teaching video whose licence and content were not checked, and YouTube and VuMedi reuse terms were not examined. Four other claims were refuted: Maastricht at about 150 frames per recording (the predecessor paper implies about 52); the Bournemouth cervical motion-frame details (6 deg/s, 60 deg, centre of rotation at C3-C4); C-ArmLSpine as stills only (it contains projection sweeps); and the TMRB cadaver description. The Maastricht label description passed only 2-1. Details of the C-ArmLSpine sweeps and data quality come from the project's own handoff document, not the public README. Every labelled cine source listed is available on request only, so access, timing and terms are unknown and may take institutional DUAs. The Pittsburgh subject and clip counts disagree between the two papers (1,518 clips from 265+70 subjects vs 1,488 from 238). The 720x1080 raster is reproduced as printed. Time-sensitive items: C-ArmLSpine v1 was published 2026-09-17, and the Neurosurgical Focus: Video article on 2026-07-01. Scripted PMC video downloads currently hit a proof-of-work gate.

## Open questions

- Will the Bournemouth group (Branney, Breen) release the raw DICOM cine behind BORDaR 385 and the lumbar OSF database a27py, and on what terms? And do lumbar per-frame corner templates exist like the cervical Database.Templates?
- Which cohort does the BORDaR .mat hold? It covers 63 people (HV and P prefixes), while the linked article reports 29 patients plus 30 controls, which is 59.
- Do any of the unverified already-known sources, such as LevelCheck, CM Spine, Pelphix or DeepFluoro, or DeepDRR-style simulations, contain multi-frame spine sequences with a recorded cranio-caudal displacement or known C-arm pose and paired CT?
- What per-level tracking accuracy (C1-C7 Dice or HD95, landmark error in mm, track-failure rate) do the Maastricht, Bournemouth and Pittsburgh methods report? The surviving evidence gives only Maastricht's C0 Dice of about 0.70.


## Sources

- https://pmc.ncbi.nlm.nih.gov/articles/PMC13024292/ (primary; Kinematic / quantitative fluoroscopy datasets (lumbar and cervical flexion-extension cine))
- https://pmc.ncbi.nlm.nih.gov/articles/PMC8503612/ (primary; Kinematic / quantitative fluoroscopy datasets (lumbar and cervical flexion-extension cine))
- https://bordar.bournemouth.ac.uk/385/ (primary; Kinematic / quantitative fluoroscopy datasets (lumbar and cervical flexion-extension cine))
- https://doi.org/10.1016/j.media.2021.102218 (primary; Videofluoroscopic swallow studies (VFSS/MBSS) showing the lateral cervical spine)
- https://link.springer.com/article/10.1007/s10278-024-01039-4 (primary; Videofluoroscopic swallow studies (VFSS/MBSS) showing the lateral cervical spine)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC13418632/ (primary; Public intraoperative spine-surgery C-arm video and surgical video libraries)
- https://github.com/ZWC-SMU/C-ArmLSpine (primary; Public intraoperative spine-surgery C-arm video and surgical video libraries)
- https://doi.org/10.1109/tmrb.2022.3196321 (primary; Fluoroscopy-guided spinal injection and pain-procedure video)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC13232890/ (secondary; Fluoroscopy-guided spinal injection and pain-procedure video)
- http://thepainsource.com/video-lumbar-facet-injection-under-fluoroscopy/ (blog; Fluoroscopy-guided spinal injection and pain-procedure video)
- https://radiopaedia.org/cases/l5-nerve-root-block-fluoroscopic?lang=gb (secondary; Fluoroscopy-guided spinal injection and pain-procedure video)
- https://pubmed.ncbi.nlm.nih.gov/41910750/ (primary; Fluoroscopy-guided spinal injection and pain-procedure video)
- https://www.ajronline.org/doi/10.2214/AJR.12.8541 (primary; Fluoroscopy-guided spinal injection and pain-procedure video)
- https://pubmed.ncbi.nlm.nih.gov/16192053/ (primary; Simulated or cadaver spine fluoroscopy sequences with paired CT or ground-truth pose)
- https://arxiv.org/abs/2607.20037 (primary; Simulated or cadaver spine fluoroscopy sequences with paired CT or ground-truth pose)
- https://arxiv.org/html/2511.03882 (primary; Simulated or cadaver spine fluoroscopy sequences with paired CT or ground-truth pose)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12292518/ (primary; Methods that track vertebrae across fluoroscopic frames)
- https://pubmed.ncbi.nlm.nih.gov/34487983/ (primary; Methods that track vertebrae across fluoroscopic frames)
- https://link.springer.com/article/10.1007/s10278-019-00273-5 (primary; Methods that track vertebrae across fluoroscopic frames)
- https://link.springer.com/article/10.1007/BF02345268 (primary; Methods that track vertebrae across fluoroscopic frames)
- https://link.springer.com/chapter/10.1007/978-3-642-04268-3_65 (primary; Methods that track vertebrae across fluoroscopic frames)
- https://www.tandfonline.com/doi/abs/10.1080/10255842.2017.1302435 (primary; Methods that track vertebrae across fluoroscopic frames)
