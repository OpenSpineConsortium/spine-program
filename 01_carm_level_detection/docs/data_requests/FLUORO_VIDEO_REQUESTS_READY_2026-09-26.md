# Fluoroscopy video: requests ready to send (2026-09-26)

This file holds one ready-to-send message for each source that can only be obtained by asking. They are ordered by value to a spine-level cine test set: per-frame level labels first, then lumbar coverage, then volume.

**The quickest way to send.** Each email also exists as a draft file in `docs/fluoro_requests_eml/`, named `NN_source.eml`. Double-click one and it opens in Outlook as an unsent message with To, Cc, Subject and Body already filled; press Send. If your mail client opens it read-only, copy the text block below instead. Two drafts are named `..._CHECK_ADDRESS.eml`: confirm their To address in a browser before sending. Contact-form, fax and WhatsApp routes (9, 12, 13) have no draft file; their text is below, ready to paste. The drafts are not in git, and neither is this file.

Every address below was checked on 2026-09-26 against the page named in its "Verified" line. Where a site hides its address from scripts, or was deliberately not fetched, the entry says **UNVERIFIED** and tells you where to confirm it by eye.

## Checklist

| # | Source | What it gets you | How to send | Effort | Status |
|---|---|---|---|---|---|
| 1 | Bournemouth QF (Branney, Breen) | DICOM cine behind the 252 public per-frame, level-named corner tracks (C1–C6), plus the lumbar L2–S1 cine (127 people) | Email, `01_bournemouth.eml` | 1 min to send; a UK data-sharing agreement follows | Ready. 4 addresses verified |
| 2 | Maastricht UMC+ / Zuyderland (E. van Santbrink, Caelers) | 112 cervical cines with per-frame C0–C7 contours; lumbar L1–S1 cine (11 men, 7.5 fps) | Email, `02_maastricht.eml` | 1 min; GDPR data-transfer agreement | Ready. 4 addresses verified |
| 3 | Inselspital Bern (Dobrocky) | Native DICOM behind the 4 dynamic-myelography videos (pulsed 7.5 f/s; the detector follows the contrast cranially during tilting). The CC BY MP4s are already on the grid. Also asks about the 62-patient cohort | Email, `03_bern.eml` | 1 min; Swiss agreement | Ready. Verified |
| 4 | Pittsburgh swallow corpus (Sejdić, Coyle) | About 1,500 lateral clips with C2 and C4 corners on every frame | Email, `04_pittsburgh.eml` | 1 min; Pitt data-use agreement | Ready. Verified |
| 5 | Seattle Science Foundation | Raw C-arm recordings behind 12 procedure demos (kyphoplasty, SCS, percutaneous fixation; mostly lumbar and thoracolumbar), and whether each was a cadaver | Email, `05_seattle_science_foundation_CHECK_ADDRESS.eml` | Confirm the address first (30 s) | **Address UNVERIFIED** (the site hides it; see entry) |
| 6 | Mayfield Brain & Spine | The AP (98-frame) and lateral (65-frame) native series from the kyphoplasty alignment video | Email, `06_mayfield.eml` | 1 min | Ready. Verified |
| 7 | DMX Imaging | Lateral lumbar flexion-extension motion X-ray at 30 frames/s, which is found nowhere public | Email, `07_dmx.eml` | 1 min | Ready. Verified |
| 8 | Radiopaedia | 7 cases, including the rotational spin (rID 24796) and the 61-projection series (rID 90103) | Open radiopaedia.org/licence in your browser, then file the application or send `08_radiopaedia_CHECK_ADDRESS.eml` | 5 min; fee reported as USD 250 | **Address UNVERIFIED** (the site was deliberately not fetched) |
| 9 | The Procedure Guide (Puranik) | Original C-arm exports for 4 live-contrast lumbar clips | Contact form: paste the text | 2 min | Ready |
| 10 | Konica Minolta Healthcare | Source DDR sequences (flat-panel dynamic radiography, not fluoroscopy) | Email, `10_konica.eml`, or the web form | 1 min | Ready. Verified |
| 11 | Jefferson (Hines) | Original file of the DRG lead-placement video (L5, S1); the YouTube copy is CC BY | Email, `11_jefferson.eml` | 1 min | Ready. The address comes from the 2020 article; he is still listed at Jefferson Health |
| 12 | MTFI (Mohanty) | Original of a 10 s lumbar coupling videofluoroscopy | Email (copy the address from the site) or WhatsApp | 2 min | **Address hidden** from scripts; the phone number is verified |
| 13 | Christopher Faubel MD | Originals of 2 short lumbar injection clips | Fax the letter, or phone | 3 min | No email published; fax verified |
| 14 | DARADIA (Kolkata) | Original vertebroplasty fluoroscopy and patient consent status | Email, `14_daradia.eml` | 1 min | Ready. Verified |

## Read once before sending

1. **Commercial scope.** Every letter says the use is non-commercial academic evaluation. If any of these frames might ever validate the 510(k) level-confirmation product, that use is commercial, so change the sentence and ask for a commercial licence. The Radiopaedia, Procedure Guide and DysphagiaBank terms are non-commercial.
2. **IRB.** Sources 1–4 will ask about ethics. Before the files arrive, ask the WSU IRB whether de-identified data received under a data-use agreement is covered by the existing not-human-participants determination or needs its own. Clinician footage (sources 5–14) may need the same determination.
3. **"We would not train on it."** Letters 1–3 carry this sentence. Delete it if you might fine-tune on the data.
4. **Co-authorship.** Letters 1–4 offer involvement or co-authorship. Check that against your authorship plans.
5. **YouTube copies.** The YouTube versions of the 28 listed videos are already on the grid (yt-dlp, best quality). YouTube's terms restrict downloading without permission. The letters to YouTube uploaders (5–7 and 9–14) therefore say that we saved copies for screening and will delete them if asked, and the permission requested covers them. If you would rather not say this, delete that sentence, but the copies then remain unpermitted.
6. **Radiopaedia.** Nothing here works around Radiopaedia's blocks on automated access, and nothing should. Their terms bar scripted downloading and require an application to use images to evaluate an ML model. Letter 8 is the route. You may still view the cases in your own browser, but saving frames for model evaluation needs their permission however the frames are saved.

## Already obtained (no request needed)

These are on the grid under `/rs/rs_grp_oschome/go2432/data/external/fluoro_video/`, listed in `manifest.tsv`:
- Bern Videos 1–4 (PMC8463391, CC BY 4.0; 5–21 s each);
- the PMC10242080 SpineJack AVI;
- the PMC11328828 Cureus paediatric cervical exam;
- the PMC4852439 MOV;
- three Wikimedia Commons items;
- the YouTube re-encodes of all 28 ids.

The Bournemouth corner tracks are at `.../data/realxray/bournemouth_qf/raw/`. C-ArmLSpine is held separately; its CBCT sweeps are in case39 and case134.

---

## 1. Bournemouth: cervical and lumbar quantitative-fluoroscopy cine

**To:** [e-mail withheld]
**Cc:** [e-mail withheld]; [e-mail withheld]; [e-mail withheld]
**Subject:** Request for the DICOM cine behind BORDaR 385 and the lumbar QF reference database, for a vertebra-tracking evaluation

Verified:
- **[e-mail withheld]:** the contact line on the BORDaR 385 record (https://bordar.bournemouth.ac.uk/385/), and his BU staff profile (https://staffprofiles.bournemouth.ac.uk/display/jbranney, written as "jbranney at bournemouth dot ac dot uk"; Principal Academic).
- **[e-mail withheld]:** the correspondence line of Breen et al. 2021 (frontiersin.org, 10.3389/fbioe.2021.745837; also PMC8503612). It is also listed on BORDaR 385.
- **[e-mail withheld]:** Alex Breen, dataset creator, listed on BORDaR 385.
- **[e-mail withheld]:** corresponding author of Branney et al. 2024 (JFMK 9:55, PMC10970965). That article's data statement says the underlying data are available from the corresponding author on request, so he is copied.

Expect: a UK GDPR data-sharing agreement, which WSU's Institutional Official will probably have to sign. Weeks to months. The cervical DICOM exists; the README describes it.

```text
Dear Dr Branney and colleagues,

I am a surgeon-scientist at Wayne State University School of Medicine and the Detroit Medical Center. My group develops a neural network that detects vertebrae and names spinal levels on intraoperative C-arm images. We have tested it only on single frames. We would now like to know how it behaves on continuous fluoroscopy: whether it holds each vertebra's identity from frame to frame and how its boxes compare with an established tracker.

Your cervical quantitative-fluoroscopy database (BORDaR 385, doi:10.18746/bmth.data.00000385; Branney et al., J Funct Morphol Kinesiol 2024;9:55) is the best reference we have found for this. It has level-named vertebral-body corners on every frame of 252 flexion and extension sequences. We have downloaded the corner tracks under the CC BY 4.0 licence, but the images themselves are not in the deposit. I am writing to ask whether you would share them. The requests are:

1. The anonymised lateral DICOM sequences, 16-bit and 1024 x 1024 at 15 fps, for the 126 imaging events. Please key them to the ImageEvent identifiers in "Cervical Database.mat" (for example HV01a and HV01b), with flexion and extension kept separate.
2. Confirmation of how frames are indexed. Does row 1 of each template array correspond to the first frame of the exported sequence? Were any frames dropped, cropped or resampled between acquisition and tracking? In 87 of the 252 sequences, MachineAngle has 1 to 59 more rows than the templates; what explains the difference? Are the template coordinates 1-based (MATLAB) pixel positions? Is the grey-scale polarity bone-bright as exported?
3. The pixel spacing or calibration used, so that we can report corner and box errors in millimetres as well as pixels, and whether image-intensifier distortion was corrected.
4. Professor Breen, for the lumbar reference database (Breen et al., Front Bioeng Biotechnol 2021, doi:10.3389/fbioe.2021.745837; OSF a27py): the weight-bearing and recumbent L2-S1 cine, and whether per-frame vertebral corner templates exist for it, as they do for the cervical set.

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
```

---

## 2. Maastricht UMC+ / Zuyderland: cervical and lumbar flexion-extension cine

**To:** [e-mail withheld]
**Cc:** [e-mail withheld]; [e-mail withheld]; [e-mail withheld]
**Subject:** Request for dynamic cervical and lumbar X-ray recordings for a vertebra-tracking evaluation

Verified:
- **[e-mail withheld]:** the correspondence line of van Santbrink et al. 2026 (Bioengineering 13:351, PMC13024292). Its data statement reads "available on request from the corresponding author due to privacy restrictions".
- **[e-mail withheld]:** the affiliation line of the same article.
- **[e-mail withheld]:** the correspondence line of Caelers et al. 2020 (JMIR Res Protoc 9:e14741, PMC7078620). The same address is still her correspondence address in April 2026 (PMC13097038, Zuyderland).
- **[e-mail withheld]:** the author email list of the 2025 Medicina review (PMC12388827). Prof. van Santbrink is senior author on both datasets.

Expect: a GDPR data-transfer agreement under the Dutch WMO framework, possibly with local ethics sign-off for secondary use. Months.

```text
Dear Dr van Santbrink and Dr Caelers,

I am a surgeon-scientist at Wayne State University School of Medicine and the Detroit Medical Center. My group develops a neural network that detects vertebrae and names spinal levels on intraoperative C-arm images. We have tested it only on single frames. We would now like to know how it behaves on continuous fluoroscopy: whether it holds each vertebra's identity from frame to frame, and how well its boxes and corners agree with an established per-frame reference.

Your group has built the two best-annotated collections of dynamic spine X-ray recordings we have found, and I am writing to ask whether you would share them for this evaluation:

1. Cervical flexion-extension recordings (van Santbrink et al., Bioengineering 2026;13:351): the 112 lateral cine recordings, 89 from 39 healthy participants and 23 from pre-operative patients with cervical radicular syndrome, at 1024 x 1024 and 15 fps. We would like them together with the per-frame C0-C7 vertebral contours that carry each level's identity, and a note on which frames were manually adjusted.
2. Lumbar flexion-extension cinematographic recordings of healthy male participants (Caelers et al., JMIR Res Protoc 2020;9:e14741): the L1-S1 recordings acquired under this protocol, and any per-frame vertebral landmarks, contours or angles derived from them.
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
```

---

## 3. Inselspital Bern: native DICOM for the dynamic myelography videos

**To:** [e-mail withheld]
**Subject:** Request for the native fluoroscopy runs behind the dynamic myelography videos (Clin Neuroradiol 2021), for a vertebra-tracking evaluation

Verified:
- **[e-mail withheld]:** the corresponding-author record of Piechowiak et al., "Role of Conventional Dynamic Myelography for Detection of High-Flow CSF Leaks: Optimizing the Technique", Clin Neuroradiol, doi:10.1007/s00062-020-00943-w (PMC8463391, JATS corresp="yes").
- The same address is current on his Stroke Research Center Bern member page (https://www.stroke.unibe.ch/about_us/members/pd_dr_med_dobrocky_tomas/index_eng.html; attending, Institute of Diagnostic and Interventional Neuroradiology).
- The article's data statement says the data are not public "owing to preclusion from dissemination under Swiss Federal Law regulations; however, they are available from the corresponding author on reasonable request."

Expect: a Swiss data-transfer agreement. Further use of coded health data may also need the cantonal ethics committee (KEK Bern) or general consent. Months, and it may be refused. The CC BY MP4s are already in hand, so a refusal costs nothing.

```text
Dear Dr Dobrocky,

I am a surgeon-scientist at Wayne State University School of Medicine and the Detroit Medical Center. My group develops a neural network that detects vertebrae and names spinal levels on C-arm images. We have tested it on single frames and now want to test it on continuous fluoroscopy: whether it keeps each vertebra's identity from frame to frame as the field of view moves.

Your article on conventional dynamic myelography (Piechowiak et al., Clin Neuroradiol, doi:10.1007/s00062-020-00943-w) includes four videos from pulsed fluoroscopy runs (7.5 f/s by default), and it describes moving the detector cranially to follow the contrast column during tilting. That is the case we have not found anywhere else: consecutive, overlapping frames of one spine while the field travels along it. We are using the published videos under their CC BY licence, with attribution. I am writing to ask for three things:

1. The native runs behind Videos 1-4 as de-identified DICOM, as acquired on the Artis zee. The web versions are re-encoded and cropped and have lost the frame timing and geometry.
2. If the DICOM headers do not carry it, the table and detector position for each frame (or the start and end positions of each run), and the vertebral levels covered by each run as you read them.
3. Whether further runs from the 62-patient cohort, particularly thoracolumbar and lumbosacral ones, could be shared under a data-transfer agreement.

How we would use and protect the data:
- Only to evaluate our detector, its level naming and its frame-to-frame tracking. We would not use it to train the network unless you agree otherwise.
- The data would stay on Wayne State's secured research storage, would not be redistributed, and would be deleted at the end of the project if you wish.
- We understand the data statement cites Swiss federal law. We are glad to sign whatever agreement Inselspital and the ethics committee require, and to obtain the matching determination from our institutional review board.
- Any publication would cite your article. We would share our per-frame results and code with you and would welcome your involvement.

With thanks and kind regards,

Gregory J. Schwing, MD, PhD
Department of General Surgery
Wayne State University School of Medicine / Detroit Medical Center
Detroit, Michigan, USA
go2432@wayne.edu
```

---

## 4. Pittsburgh videofluoroscopic swallow corpus

**To:** [e-mail withheld]
**Cc:** [e-mail withheld]
**Subject:** Request for videofluoroscopy clips with per-frame C2/C4 landmarks, for a vertebra-naming evaluation

Verified:
- **[e-mail withheld]:** his U of T ECE page (https://www.ece.utoronto.ca/people/sejdic-e/; Professor, and Research Chair in AI for Health Outcomes, North York General). It is also the correspondence address on Li et al. 2024 (PMC11300761). Zhang et al. 2021 (PMC8560570) printed an older address, [e-mail withheld].
- **[e-mail withheld]:** his Pitt SHRS page (https://www.shrs.pitt.edu/person/james-coyle/; now emeritus). He is co-author on both papers, and the data were collected at Pitt under R01HD074819.

Expect: Sejdić moved from Pitt to Toronto in 2021, so the clips are probably held at Pitt, and the data-use agreement would then go through Pitt. Months. The corpus is cervical only and centred on the hyoid.

```text
Dear Professor Sejdić and Professor Coyle,

I am a surgeon-scientist at Wayne State University School of Medicine and the Detroit Medical Center. My group develops a neural network that detects vertebrae and names spinal levels on fluoroscopic images. We have tested it on single frames and now want to test it on continuous fluoroscopy: whether it names the same vertebra correctly frame after frame.

Your videofluoroscopic swallow corpus (Zhang et al., Med Image Anal 2021;74:102218; Li et al., J Imaging Inform Med 2024;37:1922; NIH R01HD074819) carries anterior corner landmarks of C2 and C4 on every frame of roughly 1,500 lateral clips. For us, those are two named cervical levels per frame, which is exactly the reference we lack. I am writing to ask whether you would share:

1. The clips with their per-frame C2 and C4 landmarks (and C3 where labelled), for the patient cohort and the healthy-volunteer set, with the subject identifiers kept so that we can split by subject.
2. The capture details: final frame rate, any cropping or resizing, and a pixel scale if one is known.
3. If the data are now held at Pitt, the right person there to approach for a data-use agreement.

How we would use and protect the data:
- Only to evaluate our detector and its level naming. We would not use it to train the network unless you agree otherwise.
- The data would stay on Wayne State's secured research storage, would not be redistributed, and would be deleted at the end of the project if you wish.
- We are glad to sign a data-use agreement and to obtain the matching determination from our institutional review board.
- Any publication would cite both papers and the grant. We would share our per-frame results and code with you, and would welcome your involvement and co-authorship if it leads to a paper.

With thanks and kind regards,

Gregory J. Schwing, MD, PhD
Department of General Surgery
Wayne State University School of Medicine / Detroit Medical Center
Detroit, Michigan, USA
go2432@wayne.edu
```

---

## 5. Seattle Science Foundation: one request covering all 12 videos

**To:** info@seattlesciencefoundation.org
**Subject:** Research request: original C-arm recordings from 12 Seattle Science Foundation spine videos

Verified: **UNVERIFIED.**
- The address comes from a search engine's index of seattlesciencefoundation.org/overview.
- The live site (https://www.seattlesciencefoundation.org/) shows its footer email to people but hides it from scripts, so the address was not decoded here.
- Open the home page in your browser, scroll to the footer, and check the address before sending.
- The phone number, [phone withheld], and the address, 550 17th Avenue, James Tower Suite 600, Seattle, WA 98122, are verified on the home page and on /pages/about-us.
- Dr Rod Oskouian, whose video is on the list, sits on the SSF board (about-us page); a word from him may speed this up.

Expect: SSF is a non-profit education foundation that records its own labs. If the labs were cadaveric, the permission is simple. The raw C-arm output may not have been kept separately from the composited video. Weeks.

```text
Dear Seattle Science Foundation team,

I am a surgeon-scientist at Wayne State University School of Medicine and the Detroit Medical Center. My group develops a neural network that detects vertebrae and names spinal levels on intraoperative C-arm images. We are building a small test set of continuous spine fluoroscopy, to check whether the network keeps each vertebra's identity from frame to frame. Your procedure demonstrations are among the clearest recordings of live C-arm spine imaging available.

We have screened these twelve videos on your YouTube channel and saved copies for that screening only; we will delete them if you prefer:

- Yme7AxnIRWI  Live Demonstration - Lumbar Spinal Cord Stimulation Trial, Brett Stacey, MD
- ot_gIGZdUWw  Spinal Cord Stimulation Procedure Boston Scientific, Brett Stacy, MD
- RrRN6GMkkEQ  LAB DEMO: Spinal Cord Stimulation Procedure, Jennifer Lee, MD
- cTvR6wt303k  Live Demo: Kyphoplasty Pearls of the Thoracic Spine, Jeffrey S. Roh, MD
- eF3gPgRYxy0  Live Demo: Percutaneous Long Segment Fixation, Jeffrey S. Roh, MD
- B7RHD25tCkU  Vertebral Augmentation Balloon Kyphoplasty, Douglas P. Beall, MD
- VtmxIlY8S9w  Live Demonstration: Vertebral Augmentation Case, Douglas P. Beall, MD
- RMM56ibtcQI  Latest Techniques in Vertebral Augmentation Side by Side, Douglas Beall, MD and Glen David, MD
- 0sbrxbhfts0  Vertebroplasty & Kyphoplasty Demonstration, Glen David, MD
- szH5DsL8KLM  Surgical Demo: MIS TLIF, Paul Park, MD
- pufAzs_VpVc  Percutaneous Spinal Fixation with Fenestrated Screws with Cement, Rod J. Oskouian Jr, MD
- 9imNQTwETCY  Percutaneous Spinal Fixation w/Fenestrated Screws & Cement, Anu Amin, MD

For any of these you are able to share, we would be grateful for:
1. The original C-arm recordings rather than the composited video: the fluoroscope's own video output or DICOM export (for example the Ziehm export for the SCS trial).
2. Whether each session used a cadaver or a patient, and, for patients, whether the consent covers research reuse.
3. The treated or targeted level in each fluoroscopy segment.
4. Permission to use the recordings for non-commercial research evaluation, and the attribution wording you would like.

The recordings would be used only to evaluate our model, would stay on Wayne State's secured research storage, and would not be redistributed. Any publication would credit the Foundation and the faculty involved.

With thanks and kind regards,

Gregory J. Schwing, MD, PhD
Department of General Surgery
Wayne State University School of Medicine / Detroit Medical Center
Detroit, Michigan, USA
go2432@wayne.edu
```

---

## 6. Mayfield Brain & Spine: kyphoplasty alignment series

**To:** [e-mail withheld]
**Subject:** Research request: the two fluoroscopy series in "Fluoroscopic alignment for kyphoplasty"

Verified:
- **[e-mail withheld]:** shown on https://mayfieldclinic.com/contact.htm, with the main line [phone withheld].
- The same page lists Public Relations/Events at [phone withheld]. If the email gets no answer in two weeks, call that number.
- The video is on the "Mayfield Brain & Spine" YouTube channel (fkRFgkESCgQ). No surgeon is named on it.

Expect: this is a clinical practice, so the request will be routed. HIPAA de-identification may be asked about. Replies can be slow. It covers only two series, though they are native DICOM.

```text
Dear Mayfield team,

Could you please forward this to the surgeon who posted "Video1. Fluoroscopic alignment for kyphoplasty" on the Mayfield Brain & Spine YouTube channel (https://www.youtube.com/watch?v=fkRFgkESCgQ)?

I am a surgeon-scientist at Wayne State University School of Medicine and the Detroit Medical Center. My group develops a neural network that detects vertebrae and names spinal levels on C-arm images, and we are testing it on consecutive fluoroscopy frames. The video plays two native series in OsiriX, an AP run of about 98 frames and a lateral run of about 65, which are exactly the kind of sequence we need. We have saved a copy of the YouTube version for screening only and will delete it if you prefer.

We would be grateful for:
1. The two series as de-identified DICOM.
2. The level or levels treated, and whether each series was continuous cine or separate exposures (and the frame rate if cine).
3. Permission to use them for non-commercial research evaluation, with the attribution you would like.

One small point: the overlay in the posted video appears to show the patient's date of birth. You may wish to review it.

The images would stay on Wayne State's secured research storage and would not be redistributed.

With thanks and kind regards,

Gregory J. Schwing, MD, PhD
Department of General Surgery
Wayne State University School of Medicine / Detroit Medical Center
Detroit, Michigan, USA
go2432@wayne.edu
```

---

## 7. DMX Imaging: digital motion X-ray studies

**To:** [e-mail withheld]
**Subject:** Research request: de-identified lumbar DMX studies for a vertebra-tracking evaluation

Verified:
- **[e-mail withheld]:** shown, with a mailto link, on https://www.dmxworks.com/ together with [phone withheld] and 4159 Corporate Ct, Palm Harbor, FL 34683.
- The site states that "The DMX acquires 30 sequential radiographs per second".
- "Dr John" is not named in full anywhere on the site.

Expect: this is a vendor. It may answer quickly, or may want a commercial arrangement or an NDA. Ask for a small sample first.

```text
Dear DMX Imaging team,

I am a surgeon-scientist at Wayne State University School of Medicine and the Detroit Medical Center. My group develops a neural network that detects vertebrae and names spinal levels on X-ray images, and we are testing whether it keeps each vertebra's identity across consecutive frames. Lateral lumbar flexion-extension at video frame rates is the view we most need, and we have found none publicly available. Your digital motion X-ray at 30 frames per second is the closest thing to it. We have saved a copy of your "Scoliosis Patient - DMX" video (https://www.youtube.com/watch?v=WUWfgkEIYTs) for screening only and will delete it if you prefer.

Would you be willing to share a small set, say 10 to 20 de-identified studies, of:
1. Lateral lumbar flexion-extension, and AP lumbar or thoracolumbar side-bending.
2. In the native format, with the frame rate and any pixel-scale or calibration information.
3. With the levels reported, where the report names them, and the consent status for research reuse.

The studies would be used only for non-commercial research evaluation, kept on Wayne State's secured research storage, and not redistributed. Any publication would credit DMX Imaging as you wish. I am happy to discuss terms or to start with a single study.

With thanks and kind regards,

Gregory J. Schwing, MD, PhD
Department of General Surgery
Wayne State University School of Medicine / Detroit Medical Center
Detroit, Michigan, USA
go2432@wayne.edu
```

---

## 8. Radiopaedia: permission and native DICOM for seven cases

**To:** [e-mail withheld]
**Subject:** Research-use request and native DICOM for seven fluoroscopy cases (vertebra-tracking evaluation)

Verified: **UNVERIFIED.**
- The address comes from a search snippet in the earlier draft. Today's search engine results show it only as a hidden "[email protected]".
- Radiopaedia was deliberately not fetched, because its terms bar automated access.
- **How to send:** open https://radiopaedia.org/licence in your browser.
  - If it links an application form for non-commercial machine-learning use, file that, pasting the text below as the project description.
  - Otherwise email the address the page shows. Their stated rule is not to email first to ask whether you qualify.

Expect: an application, with a fee reported as USD 250, non-refundable. Non-commercial use only; commercial AI use needs a negotiated licence. The contributors keep their rights.

```text
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
```

Cases 4–7 show about one level each. Drop them if the application is priced per case.

---

## 9. The Procedure Guide (Rohit Puranik, MD): contact form

**To:** contact form at https://theprocedureguide.com/contact (no email is published)
**Subject:** not a form field; the text below opens with one line saying what the message is about

Verified:
- **Form fields:** First name, Last name, Email, and "Comment or Message", all required.
- **Founder:** Rohit Puranik, MD, "founder and primary editor", named on https://theprocedureguide.com/about-our-team/.
- **Site licence:** the footer reads "Everything on the site is under a creative commons license (CC BY-NC-SA 4.0)". The site does not say whether that covers its YouTube clips.

Fill in: First name `Gregory`, Last name `Schwing`, Email `go2432@wayne.edu`, then paste:

```text
Research request: original C-arm exports for four of your live fluoroscopy clips.

Dear Dr Puranik,

I am a surgeon-scientist at Wayne State University School of Medicine / Detroit Medical Center. My group develops a neural network that detects vertebrae and names spinal levels on C-arm images, and we are testing it on consecutive fluoroscopy frames. Your live-contrast clips are unusually clean. We have saved copies of these YouTube versions for screening only and will delete them if you prefer:
- KXz2k8lOt9U and 4q8LjcE0vsI (L3 transforaminal injection; we believe the same patient)
- 6MBj9SBZrno (interlaminar lumbar epidural, lateral)
- DCLd6DsoUSg (caudal epidural)

Could you tell us: (1) whether your site's CC BY-NC-SA 4.0 licence covers these clips; (2) whether the original C-arm exports (DICOM or the fluoroscope's video output) still exist and could be shared, de-identified; (3) the level targeted in each, and the frame rate if known.

Use would be non-commercial research evaluation only, kept on Wayne State's secured storage, not redistributed, and credited to The Procedure Guide.

Many thanks,
Gregory J. Schwing, MD, PhD, Department of General Surgery, Wayne State University School of Medicine / Detroit Medical Center, go2432@wayne.edu
```

Expect: a small site that may reply quickly. The original exports may not have been kept.

---

## 10. Konica Minolta Healthcare Americas: DDR source sequences

**To:** [e-mail withheld]
**Subject:** Research request: de-identified lumbar Dynamic Digital Radiography sequences

Verified:
- **[e-mail withheld]:** shown on https://healthcare.konicaminolta.us/contact-us, with [phone withheld].
- **Alternative:** the web form on the same page, where you tick "Radiography" under Areas of Interest and paste the body into "More Info / Message". Email and Contact Number are required fields.

Expect: corporate marketing will route the request. It may lead to a research agreement or an NDA, or to a pointer to a DDR clinical site. These are flat-panel sequences, not fluoroscopy, so keep them in a separate arm.

```text
Dear Konica Minolta Healthcare team,

I am a surgeon-scientist at Wayne State University School of Medicine and the Detroit Medical Center. My group develops a neural network that detects vertebrae and names spinal levels on X-ray images, and we are testing whether it keeps each vertebra's identity across sequential frames. Your video "Explore Spine Movement with Dynamic Digital Radiography (DDR)" (https://www.youtube.com/watch?v=Eq8m0e6AGGw) shows exactly the kind of sequence we would like to test on. We have saved a copy for screening only and will delete it if you prefer.

Would Konica Minolta, or a DDR research site you work with, be able to share a small set of de-identified lumbar DDR sequences: AP side-bending and lateral flexion-extension, in the native format with frame timing and pixel spacing, and the levels in the report where given? If there is a DDR research-collaboration programme, I would be glad to apply through it.

Use would be non-commercial research evaluation only, on Wayne State's secured storage, not redistributed, and credited as you wish.

With thanks and kind regards,

Gregory J. Schwing, MD, PhD
Department of General Surgery
Wayne State University School of Medicine / Detroit Medical Center
Detroit, Michigan, USA
go2432@wayne.edu
```

---

## 11. Jefferson Neurosurgery (Kevin Hines, MD): DRG stimulation video

**To:** [e-mail withheld]
**Subject:** Original file for your Neurosurgical Focus: Video article on DRG stimulation (10.3171/2020.7.FOCVID2034)

Verified:
- **[e-mail withheld]:** the correspondence line of Hines et al., "Dorsal root ganglion stimulation for treatment of complex regional pain syndrome of the foot", Neurosurg Focus Video 2020;3(2) (PMC9542308).
- He is still listed by Jefferson Health (https://www.jeffersonhealth.org/find-a-doctor/h/hines-kevin-j), but the address itself is from 2020.
- **Licence:** the YouTube copy (_1xMxFZa6tU, AANS channel) is marked "Creative Commons Attribution license (reuse allowed)" in its metadata. The PMC text says "distributed under the CC BY-NC-ND license" while linking the CC BY 4.0 URL.

Expect: an academic request, weeks. The original file may sit with JNS/AANS rather than the authors; if so, he will say so.

```text
Dear Dr Hines,

I am a surgeon-scientist at Wayne State University School of Medicine and the Detroit Medical Center. My group develops a neural network that detects vertebrae and names spinal levels on C-arm images, and we are testing it on consecutive fluoroscopy frames. Your video article on DRG stimulation for CRPS of the foot (Neurosurg Focus Video 2020, doi:10.3171/2020.7.FOCVID2034) shows lumbosacral fluoroscopy with the L5 and S1 levels named, which gives us level ground truth.

The YouTube copy carries a CC BY licence, and we have saved it for screening. Would you be able to share:
1. The original-resolution video file, or the underlying C-arm runs if they were kept, de-identified.
2. Which segments are live fluoroscopy rather than saved images, and the level in each.
3. Which licence applies: the article text says CC BY-NC-ND but links CC BY 4.0.

Use would be non-commercial research evaluation only, on Wayne State's secured storage, not redistributed, and cited to your article.

With thanks and kind regards,

Gregory J. Schwing, MD, PhD
Department of General Surgery
Wayne State University School of Medicine / Detroit Medical Center
Detroit, Michigan, USA
go2432@wayne.edu
```

---

## 12. Manual Therapy Foundation of India (Prof. Umasankar Mohanty)

**To:** the address on https://www.mtfi.net/Contact%20Us.html (hidden from scripts, **not decoded here**). Open the page in your browser and copy it; the page lists two addresses.
**Alternative:** WhatsApp or call +91 99016 59074, the mobile number on mtfi.net (verified), with the short version below.
**Subject:** Research request: original file of "Lumbar Coupling (Video Fluoroscopy)"

Verified:
- The founder, "Prof. Umasankar Mohanty", is named on https://www.mtfi.net/.
- The address and phone numbers are on its Contact Us page: 301-302 Janvi Plaza, Bunts Hostel Road, Mangalore 575003.
- The video (56Sxu0thpcU, 10 s) is titled "... by Prof. Mohanty and Dr. Shamla Pazare of MTFI".

Expect: low value. The clip is 10 s and the YouTube copy films a monitor. It is worth sending only because it costs a minute.

```text
Dear Prof. Mohanty,

I am a surgeon-scientist at Wayne State University School of Medicine and the Detroit Medical Center. My group develops a neural network that detects vertebrae and names spinal levels on X-ray images, and we are testing it on consecutive fluoroscopy frames. Your YouTube video "Lumbar Coupling (Video Fluoroscopy)" with Dr Shamla Pazare (https://www.youtube.com/watch?v=56Sxu0thpcU) shows AP lumbar side-bending with rotation, which is a view we lack. We have saved a copy for screening only and will delete it if you prefer.

Would you be able to share the original recording file (the YouTube version appears to be filmed from a monitor), with the frame rate, the equipment used and the levels in view? Use would be non-commercial research evaluation only, not redistributed, and credited to you and MTFI.

With thanks and kind regards,

Gregory J. Schwing, MD, PhD
Department of General Surgery
Wayne State University School of Medicine / Detroit Medical Center
Detroit, Michigan, USA
go2432@wayne.edu
```

Short WhatsApp version: *"Dear Prof. Mohanty, I am Dr Gregory Schwing, Wayne State University (USA). For a non-commercial research study of vertebra tracking on fluoroscopy, may I request the original file of your YouTube video 'Lumbar Coupling (Video Fluoroscopy)' (56Sxu0thpcU)? Could you tell me the best email to write to? Thank you."*

---

## 13. Christopher Faubel, MD (ThePainSource / OrthoIllinois): fax or phone

**To:** fax **[phone withheld]**, attention Dr Christopher Faubel; phone [phone withheld]. No email or message form is published.
**Subject:** Research request: original fluoroscopy clips from ThePainSource videos

Verified:
- The fax, phone and address (650 S. Randall Road, Algonquin, IL 60102) are on https://www.faubelmd.com/contact-us and on his OrthoIllinois provider page.
- ThePainSource.com footer: "© The Pain Source, All Rights Reserved"; it names Dr Faubel as creator.
- **Easiest route:** call the office, ask for an email address for Dr Faubel, and send the text below. Otherwise fax it as a letter.

Expect: low value. These are two clips of a few seconds each, and the site reserves all rights.

```text
Dear Dr Faubel,

I am a surgeon-scientist at Wayne State University School of Medicine and the Detroit Medical Center. My group develops a neural network that detects vertebrae and names spinal levels on C-arm images, and we are testing it on consecutive fluoroscopy frames. Two of your ThePainSource videos show short live runs that would help. We have saved copies of the YouTube versions for screening only and will delete them if you prefer:
- 6Y2QDj_xUbQ, "Right L5-S1 facet injection under fluoroscopic guidance"
- CTyIu-EGby8, "Lumbar Transforaminal Epidural - Neurogram to Epidural with an Extra Millimeter"

Would you be able to share the original clips, de-identified, with the level in each (and the frame rate if known), and permit their use for non-commercial research evaluation? They would stay on Wayne State's secured storage, would not be redistributed, and would be credited to you and ThePainSource.

With thanks and kind regards,

Gregory J. Schwing, MD, PhD
Department of General Surgery
Wayne State University School of Medicine / Detroit Medical Center
Detroit, Michigan, USA
go2432@wayne.edu
```

---

## 14. DARADIA: The Pain Clinic (Kolkata)

**To:** info@daradia.com
**Subject:** Research request: original fluoroscopy from your percutaneous vertebroplasty video

Verified:
- **info@daradia.com:** shown on https://daradia.com/, with +91 92 0559 0559 and the Daradia Pain Hospital address in New Town, Kolkata.
- The video (xciOcPXLcGs) credits "Procedure Performed by: Dr. Gautam Das MD, FIPP".

Expect: low value. The patient is live and in front of an audience, and a skin grid lies over the spine. Consent for research reuse is the deciding question.

```text
Dear Dr Das and the DARADIA team,

I am a surgeon-scientist at Wayne State University School of Medicine and the Detroit Medical Center. My group develops a neural network that detects vertebrae and names spinal levels on C-arm images, and we are testing it on consecutive fluoroscopy frames. Your video "Percutaneous Vertebroplasty | Step-by-Step Technique Under Fluoroscopy" (https://www.youtube.com/watch?v=xciOcPXLcGs) shows the kind of sequence we need. We have saved a copy for screening only and will delete it if you prefer.

Would you be able to share:
1. The original fluoroscopy recording, de-identified.
2. The level treated.
3. Whether the patient's consent covers research reuse of the images.

Use would be non-commercial research evaluation only, on Wayne State's secured storage, not redistributed, and credited to Dr Das and DARADIA.

With thanks and kind regards,

Gregory J. Schwing, MD, PhD
Department of General Surgery
Wayne State University School of Medicine / Detroit Medical Center
Detroit, Michigan, USA
go2432@wayne.edu
```

---

## Not drafted, and why

- **Samuel Ralls, DC** (`T3vsvpkRR14`, `b8ZgL4mBqdA`): clean direct cervical cine, lateral and AP open-mouth. The video description gives www.rallsfamilychiro.com and [phone withheld]; no email was found. It is cervical only. Add a letter like no. 12 if the cervical arm needs more.
- **University of Utah OLIF video** (`KWwGMIoDrmU`, AANS): it is CC BY on YouTube, and that copy is already on the grid, so no permission is needed. The fluoroscopy is probably saved stills. The corresponding contact on PMC9521211 is [e-mail withheld].
- **PUMCH stitching series** (Liu et al., Eur Spine J 2026): the data statement says "No datasets were generated or analysed". Asking is unlikely to succeed.
- **DysphagiaBank (TalkBank)**: this is a registration, not a letter. It is non-commercial and cervical only. The scan counted about 53 adults, but the UNM corpus page read today lists 7 participants; check the count when registering. The PI contact on that page is [e-mail withheld].
