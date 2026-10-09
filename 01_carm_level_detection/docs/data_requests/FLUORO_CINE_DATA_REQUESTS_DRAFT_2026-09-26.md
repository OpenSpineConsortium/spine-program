# Draft 1: Bournemouth request, cervical and lumbar quantitative-fluoroscopy cine

To: [e-mail withheld] (Dr Jonathan Branney)
Cc: [corresponding author of Breen et al. 2021, Front Bioeng Biotechnol, doi:10.3389/fbioe.2021.745837; confirm the address on the article page before sending]
Subject: Request for the DICOM cine behind BORDaR 385 and the lumbar QF reference database, for a vertebra-tracking evaluation

---

Dear Dr Branney,

I am a surgeon-scientist at Wayne State University School of Medicine and the Detroit Medical Center. My group develops a neural network that detects vertebrae and names spinal levels on intraoperative C-arm images. We have tested it only on single frames. We would now like to know how it behaves on continuous fluoroscopy: whether it holds each vertebra's identity from frame to frame and how its boxes compare with an established tracker.

Your cervical quantitative-fluoroscopy database (BORDaR 385, doi:10.18746/bmth.data.00000385; Branney et al., J Funct Morphol Kinesiol 2024;9:55) is the best reference we have found for this. It has level-named vertebral-body corners on every frame of 252 flexion and extension sequences. We have downloaded the corner tracks under the CC BY 4.0 licence, but the images themselves are not in the deposit. I am writing to ask whether you would share them. The requests are:

1. The anonymised lateral DICOM sequences, 16-bit and 1024 × 1024 at 15 fps, for the 126 imaging events. Please key them to the `ImageEvent` identifiers in `Cervical Database.mat` (for example HV01a and HV01b), with flexion and extension kept separate.
2. Confirmation of how frames are indexed. Does row 1 of each template array correspond to the first frame of the exported sequence? Were any frames dropped, cropped or resampled between acquisition and tracking? In 87 of the 252 sequences, `MachineAngle` has 1 to 59 more rows than the templates; what explains the difference? Are the template coordinates 1-based (MATLAB) pixel positions? Is the grey-scale polarity bone-bright as exported?
3. The pixel spacing or calibration used, so that we can report corner and box errors in millimetres as well as pixels. We would also like to know whether image-intensifier distortion was corrected.
4. For the lumbar reference database (Breen et al. 2021, OSF a27py): the weight-bearing and recumbent L2–S1 cine. We would also like to know whether per-frame vertebral corner templates exist for it, as they do for the cervical set.

How we would use and protect the data:
- We would use it only to evaluate our detector, its level naming and its frame-to-frame tracking against your corner tracks. We would not use it to train the network unless you agree otherwise.
- Data would be held on Wayne State's secured research computing storage. We would not redistribute it and would delete it at the end of the project if you wish.
- We are glad to sign a data-sharing agreement and to obtain the corresponding determination from our institutional review board.
- Any publication would cite both datasets and the companion articles. We would share our per-frame results and evaluation code with you, and we would welcome your involvement and co-authorship if the work leads to a paper.

If it would help, I would be happy to send a short summary of the evaluation protocol first, or to arrange a call.

With thanks and kind regards,

Gregory J. Schwing, MD, PhD
Department of General Surgery
Wayne State University School of Medicine / Detroit Medical Center
Detroit, Michigan, USA
go2432@wayne.edu

---


# Draft 2: Maastricht UMC+ / Zuyderland request, cervical and lumbar flexion-extension cine

To: [the corresponding author of van Santbrink et al. 2026, Bioengineering 13:351, doi:10.3390/bioengineering13030351; the MDPI article page gives the address]
Cc: [the corresponding author of Caelers et al. 2020, JMIR Res Protoc 9:e14741, doi:10.2196/14741; Prof. H. van Santbrink and Dr T. Boselie are authors on both]
Subject: Request for dynamic cervical and lumbar X-ray recordings for a vertebra-tracking evaluation

---

Dear Dr van Santbrink,

I am a surgeon-scientist at Wayne State University School of Medicine and the Detroit Medical Center. My group develops a neural network that detects vertebrae and names spinal levels on intraoperative C-arm images. We have tested it only on single frames. We would now like to know how it behaves on continuous fluoroscopy: whether it holds each vertebra's identity from frame to frame, and how well its boxes and corners agree with an established per-frame reference.

Your group has built the two best-annotated collections of dynamic spine X-ray recordings we have found, and I am writing to ask whether you would share them for this evaluation:

1. **Cervical flexion-extension recordings** (van Santbrink et al., Bioengineering 2026;13:351). These are the 112 lateral cine recordings: 89 from 39 healthy participants and 23 from pre-operative patients with cervical radicular syndrome, at 1024 × 1024 and 15 fps. We would like them together with the per-frame C0–C7 vertebral contours that carry each level's identity, and a note on which frames were manually adjusted.
2. **Lumbar flexion-extension cinematographic recordings** of healthy male participants (Caelers et al., JMIR Res Protoc 2020;9:e14741). We would like the L1–S1 recordings, and any per-frame vertebral landmarks, contours or angles you derived from them.
3. For both sets: the pixel spacing or calibration and the frame rate, so that we can report errors in millimetres, plus any record of frames that were dropped or cropped.

How we would use and protect the data:
- We would use it only to evaluate our detector, its level naming and its frame-to-frame tracking against your contours. We would not use it to train the network unless you agree otherwise.
- The data would be held on Wayne State's secured research computing storage. We would not redistribute it and would delete it at the end of the project if you wish.
- We understand that a data-transfer agreement under the GDPR and your institution's WMO framework is likely to be needed. We are glad to sign one and to obtain the corresponding determination from our institutional review board.
- Any publication would cite both datasets and papers. We would share our per-frame results and evaluation code with you, and we would welcome your involvement and co-authorship if the work leads to a paper.

I would be glad to send a one-page evaluation protocol or to arrange a call.

With thanks and kind regards,

Gregory J. Schwing, MD, PhD
Department of General Surgery
Wayne State University School of Medicine / Detroit Medical Center
Detroit, Michigan, USA
go2432@wayne.edu

---


# Draft 3: Radiopaedia, permission and native DICOM for seven fluoroscopy cases

To: [e-mail withheld] [taken from a search snippet; the address on radiopaedia.org/licence is obfuscated, so confirm it there before sending]
Subject: Research-use request and native DICOM for seven fluoroscopy cases (vertebra-tracking evaluation)

---

Dear Radiopaedia team,

I am a surgeon-scientist at Wayne State University School of Medicine and the Detroit Medical Center. My group develops a neural network that detects vertebrae and names spinal levels on intraoperative C-arm images. We would like to test how it behaves across consecutive fluoroscopy frames. A few Radiopaedia cases are among the very few public multi-frame spine fluoroscopy series.

Your licence page says that machine-learning research goes through an application process. I would be grateful to know whether the use below needs that application, and to start it if so. The cases are:

1. rID 24796, compression fracture with vertebral body stenting: the rotational C-arm spin (contributor Dr Salem Bauones)
2. rID 90103, oblique sublaminar lumbar puncture: the 61-projection series (contributor Dr Jeffrey Hocking)
3. rID 21585, percutaneous vertebroplasty: the lateral L1 series (contributor Dr Chris O'Donnell)
4. https://radiopaedia.org/cases/lumbar-transforaminal-epidural-steroid-injection-fluoroscopic-guided
5. https://radiopaedia.org/cases/lumbar-transforminal-epidural-steroid-injection-fluoroscopic-guided
6. https://radiopaedia.org/cases/s1-transforaminal-epidural-steroid-injection-fluoroscopic-guided
7. https://radiopaedia.org/cases/l5-nerve-root-block-fluoroscopic

The intended use:
- The images would be used only to evaluate an existing model, not to train it. The work is non-commercial academic research, for publication.
- The images would stay on Wayne State's secured research storage and would not be redistributed. Any figure would carry the attribution your licence requires, with links to each case.
- The first three cases matter most. If their contributors still have the native DICOM, it would be far more useful than the web images, because it carries the pixel spacing, the C-arm angles and the frame timing. We would be glad to credit or involve them as they wish.

Thank you for considering this. I am happy to provide any further detail the application needs.

With kind regards,

Gregory J. Schwing, MD, PhD
Department of General Surgery
Wayne State University School of Medicine / Detroit Medical Center
Detroit, Michigan, USA
go2432@wayne.edu

---

Notes for Greg (delete before sending):
- Radiopaedia (terms v4.2, 14 Aug 2026; licence page): scripted or systematic downloading is barred for all purposes. Using images to "evaluate, validate" an ML model is a restricted use. Non-commercial ML research "must go through an application process" (reported as USD 250, non-refundable; their rule is not to email first to ask whether you qualify, so be ready to file the application if they point you to it). Commercial AI use is not permitted without a negotiated licence. Individual images can be saved one at a time from the viewer's download icon, as JPEG/PNG with no geometry.
- The letter says non-commercial academic evaluation. If these frames would ever validate the 510(k) product, that is commercial: say so and ask for a commercial licence instead.
- Cases 4-7 show about one level each and are low value; drop them if the application is priced per case.
- Maastricht: the cervical paper's data statement says "available on request from the corresponding author due to privacy
  restrictions". The lumbar source is a protocol paper (11 healthy men, L1–S1, 7.5 fps per the scan). Its results paper, if
  one exists, may name the dataset differently; ask for "the recordings acquired under this protocol".
- Their contours were drawn once on the median frame and carried to the other frames by template matching, with manual
  correction where needed. That is the same kind of reference as Bournemouth's.

- The corner tracks are already on disk, on the local machine at `laptop:data\bournemouth_qf\raw\` (outside git) and on the grid at
  `/rs/rs_grp_oschome/go2432/data/realxray/bournemouth_qf/raw/`, md5 aec3d16d031f62c4a4b7725cd5e0a0be. The harness
  (`tools/bournemouth_qf_eval.py`, `docs/BOURNEMOUTH_QF_HARNESS.md`) scores against them the day the frames arrive.
- Check the co-authorship offer against your authorship plans. Check the sentence about not training on the data: remove it if you might want to fine-tune.
- Expect a UK data-sharing agreement (UK GDPR). WSU's signatory, the IO, is likely needed on it.
- The lumbar corresponding author's address was left as a placeholder on purpose; I did not want to guess it.
