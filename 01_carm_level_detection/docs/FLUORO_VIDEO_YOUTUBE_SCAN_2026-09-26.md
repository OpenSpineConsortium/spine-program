<!-- wf_e9507c6b-02f, 2026-09-26: 8 search angles, 17 agents; candidates independently re-checked. Raw candidates: raw section below. -->

# YouTube and public video libraries as a temporal fluoroscopy test set

## 1. Verdict

I checked YouTube: 70 entries across eight searches. It can supply a small internal stress test, but not a benchmark you could publish.

- **What YouTube has.** 18 of the 70 show live or multi-frame fluoroscopy on the evidence available. Nine of those 18 are cervical. Only one watch page shows a Creative Commons licence (`KWwGMIoDrmU`), and its fluoroscopy looks like saved stills.
- **Main obstacles:**
  - YouTube's Terms of Service restrict downloading.
  - The re-encodes are lossy, and the C-arm image often fills only 30–60% of a split-screen frame.
  - Many "fluoro" panels are last-image-hold, not live.
  - Dates and study numbers are burned into the image.
  - Levels are almost never named.
  - The C-arm usually stays parked on one level.
- **The cleaner sources are not on YouTube.**
  - CC BY journal supplements on PMC. The best is the Bern dynamic myelography set: pulsed at 7.5 frames/s, with the detector moved cranially during the run.
  - Radiopaedia multi-frame stacks, under CC BY-NC-SA.

## 2. Ranked candidates (top 25)

"Live fluoro seconds" is the continuous live footage. In most cases it could not be measured, because nothing was watched or downloaded. "n/3 samples" means fluoroscopy appeared in n of YouTube's three auto-frames, taken at about 25, 50 and 75% of the video. SSF is the Seattle Science Foundation.

| # | Title and URL | Procedure | Region | View | Live fluoro seconds | Licence | Usability | Next step |
|---|---|---|---|---|---|---|---|---|
| 1 | [Bern dynamic myelography, Videos 1–4 (Clin Neuroradiol 2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8463391/) | Unsubtracted dynamic myelography on a tilting table | Thoracic (T7/8, T9/10); one clip at L5/S1 | Lateral (V2, V4), AP (V3) | About 10–14 s per clip at 7.5 f/s, estimated from figure captions. Detector panned cranially, so frames overlap during the pan | CC BY 4.0 | good | Use under CC BY with attribution (download from PMC). Ask Inselspital for native DICOM |
| 2 | [Live Demonstration – Lumbar SCS Trial, Stacey (SSF)](https://www.youtube.com/watch?v=Yme7AxnIRWI) | Spinal cord stimulator (SCS) lead advancement | Thoracolumbar | AP | Unknown. Direct Ziehm feed; the overlay clock moves about 5 min between samples. Live vs held not confirmed | Unknown; embedding disabled | good | Ask uploader for the original C-arm output |
| 3 | [Fluoroscopic alignment for kyphoplasty (Mayfield)](https://www.youtube.com/watch?v=fkRFgkESCgQ) | C-arm alignment runs: native DICOM series played in OsiriX | Lumbar / thoracolumbar | AP (98 frames) and lateral (65 frames) | About 30–40 s in a 40–56 s video | Unknown | good | Ask uploader for the two DICOM series. The overlay shows a birth date |
| 4 | [Kyphoplasty Pearls of the Thoracic Spine, Roh (SSF)](https://www.youtube.com/watch?v=cTvR6wt303k) | Balloon kyphoplasty at T12, vertebroplasty at L1 | Thoracolumbar | Lateral (inset or large) | Unknown; 3/3 samples | Unknown; embedding disabled | possible | Ask uploader. The chapters name T12 and L1, which gives level ground truth |
| 5 | [Compression fracture with vertebral body stenting, rID 24796](https://radiopaedia.org/cases/compression-fracture-with-vertebral-body-stenting) | Rotational C-arm spin after L1 stenting (a cone-beam CT was reconstructed from it) | Thoracolumbar (L1) | Sweep of about 180°: lateral → AP → opposite lateral | 41 frames; rate unknown | CC BY-NC-SA 3.0 (site-wide) | possible | Use under the licence with attribution, research only. Ask the contributor for DICOM, geometry and commercial permission |
| 6 | [Percutaneous vertebroplasty, rID 21585](https://radiopaedia.org/cases/percutaneous-vertebroplasty) | L1 vertebroplasty; separate live exposures, cement appears | Thoracolumbar (L1) | Lateral, fixed | 21 frames; rate unknown | CC BY-NC-SA 3.0 | possible | Use under the licence with attribution, research only |
| 7 | [SCS Procedure Boston Scientific, Stacy (SSF)](https://www.youtube.com/watch?v=ot_gIGZdUWw) | SCS leads | Lumbar / thoracolumbar, about 3 levels | AP | Unknown; direct feed | Unknown; embedding disabled | good (heavy hardware overlap) | Ask uploader |
| 8 | [Vertebral Augmentation Balloon Kyphoplasty, Beall (SSF)](https://www.youtube.com/watch?v=B7RHD25tCkU) | Kyphoplasty access approaches | Thoracolumbar / lumbar, 4–6 bodies | Lateral and AP | Unknown; 2/3 samples | Unknown; embedding disabled | possible | Ask uploader |
| 9 | [Latest Techniques in Vertebral Augmentation, Beall & David (SSF)](https://www.youtube.com/watch?v=RMM56ibtcQI) | Bipedicular augmentation | Lumbar / lower thoracic (probably some cervical later on) | AP and lateral | Unknown; 3/3 samples | Unknown; embedding disabled | possible | Ask uploader |
| 10 | [Live Demonstration: Vertebral Augmentation, Beall (SSF)](https://www.youtube.com/watch?v=VtmxIlY8S9w) | Balloon kyphoplasty | Lumbar / lower thoracic | Lateral | Unknown; 3/3 samples across about 12 min of overlay clock | Unknown; embedding disabled | possible | Ask uploader |
| 11 | [Vertebroplasty & Kyphoplasty, Glen David (SSF)](https://www.youtube.com/watch?v=0sbrxbhfts0) | Augmentation with two C-arms | Lumbar | AP, plus a panel labelled "Live" (probably lateral) | Unknown; 1/3 samples | Unknown; embedding disabled | possible | Ask uploader |
| 12 | [LAB DEMO: SCS Procedure, Jennifer Lee (SSF)](https://www.youtube.com/watch?v=RrRN6GMkkEQ) | SCS lead in the SSF bioskills lab (likely cadaver) | Thoracic / thoracolumbar | Lateral | Unknown; one sampled frame is last-image-hold | Unknown; embedding disabled | possible | Ask uploader. She is at EvergreenHealth, not Amarillo |
| 13 | [Transforaminal live fluoroscopic contrast injection](https://www.youtube.com/watch?v=KXz2k8lOt9U), plus the [same patient's AP/lateral clip](https://www.youtube.com/watch?v=4q8LjcE0vsI) | L3 transforaminal epidural steroid injection (TF ESI) | Lumbar, about 3 bodies | AP (the pair adds a held lateral) | A few seconds; dose rate reads 4.24 mGy/min at one sample | The site says CC BY-NC-SA 4.0; whether that covers YouTube is not stated | possible | Ask uploader (Puranik) for the C-arm exports |
| 14 | [Lumbar Coupling (Video Fluoroscopy), Mohanty](https://www.youtube.com/watch?v=56Sxu0thpcU) | Videofluoroscopy of lumbar side-bending with rotation | Lumbar (about L2–L5) | AP | Unknown; appears continuous | Unknown | good / possible (the two verification passes disagree) | Ask uploader for the original file. The YouTube copy films a monitor |
| 15 | [Scoliosis Patient – DMX (dmxworks)](https://www.youtube.com/watch?v=WUWfgkEIYTs) | Standing digital motion X-ray (DMX), an image-intensifier technique | Mostly thoracic, some thoracolumbar | AP | Unknown; continuous at 3/3 samples; the vendor says 30 frames/s | Unknown | possible | Ask uploader (DMX Imaging) |
| 16 | [Fluoroscopy of normal barium swallow (Commons)](https://commons.wikimedia.org/wiki/File:Fluoroscopy_of_normal_barium_swallow.ogg) | Barium swallow; the field pans down the spine | Cervical → lower thoracic | AP | 28.7 s at 3 f/s | CC BY-SA 4.0 | possible | Use with attribution (share-alike) |
| 17 | [Explore Spine Movement with DDR (Konica)](https://www.youtube.com/watch?v=Eq8m0e6AGGw) | Dynamic digital radiography of lateral bending. Flat-panel, not fluoroscopy | Lumbar | AP | Unknown; first half only | Unknown | possible | Ask Konica for the source DDR sequences. Keep them apart from fluoroscopy |
| 18 | [DRG stimulation for CRPS (AANS / Neurosurg Focus Video)](https://youtu.be/_1xMxFZa6tU) | Dorsal root ganglion (DRG) lead placement | Lumbosacral (L5, S1) | AP seen; lateral per the text | Unknown; beam-on dose rate (61.91 mGy/min) at one sample; SD | The article states CC BY-NC-ND but links the CC BY 4.0 URL; YouTube licence unread | possible | Ask the Jefferson authors or JNS for the file |
| 19 | [MIS oblique interbody fusion (AANS)](https://www.youtube.com/watch?v=KWwGMIoDrmU) | OLIF positioning and graft checks (screws were navigated) | Lumbar L3–L5 | AP and lateral | Probably saved stills | CC BY, on the YouTube page and on PMC9521211 | possible / poor (passes disagree) | CC BY covers reuse. Ask AANS/JNS for the original file instead of downloading |
| 20 | [Live Demo: Percutaneous Long Segment Fixation, Roh (SSF)](https://www.youtube.com/watch?v=eF3gPgRYxy0) | Percutaneous pedicle screws L1–S1 | Lumbar / sacrum | Unknown | Unknown; no fluoroscopy confirmed | Unknown | possible (unverified) | Watch first, then include in the SSF request. The chapters name L5, S1 and L1–L4 |
| 21 | [Right L5-S1 Facet Injection (ThePainSource)](https://www.youtube.com/watch?v=6Y2QDj_xUbQ) | Facet arthrogram | Lumbosacral, 3–4 segments | Ipsilateral oblique | A few seconds of full-speed clip, replayed 3× | Site says "All Rights Reserved" | possible | Ask uploader (Faubel) for the original |
| 22 | [Lumbar Transforaminal Epidural (ThePainSource)](https://www.youtube.com/watch?v=CTyIu-EGby8) | TF ESI | Lumbar, 3–4 bodies | AP | Unknown; live not established | Site says "All Rights Reserved" | possible | Ask uploader (Faubel) |
| 23 | [Percutaneous Vertebroplasty (DARADIA)](https://www.youtube.com/watch?v=xciOcPXLcGs) | Vertebroplasty on a live patient in front of an audience | Lumbar / thoracolumbar | AP | Unknown; 3/3 samples, possibly held; a skin grid overlies the spine | Unknown | possible | Ask uploader (info@daradia.com), including patient consent |
| 24 | [SpineJack in multiple myeloma, Video S1 (Front Surg 2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10242080/) | SpineJack plus cement "under real time fluoroscopy" | Thoracic (probably T6) | Unknown | Unknown; 15.7 MB AVI, not watched | CC BY | possible | Use under CC BY with attribution after checking the content |
| 25 | [DysphagiaBank UNM corpus (TalkBank)](https://talkbank.org/aphasia/access/English/Dysphagia/UNM.html) | Clinical swallow studies | Cervical (C2 to about C4/5) | Lateral in all; AP also in 34 | Whole studies of about 1 min or more at 30 f/s; about 53 adults | CC BY-NC-SA 3.0, registration required, no commercial or LLM use | possible | Register and count the adult lateral studies. Useful only as a cervical stability test |

**Not ranked but worth knowing:**
- `T3vsvpkRR14` and `b8ZgL4mBqdA` (Samuel Ralls DC): clean direct cervical cine, lateral plus AP open-mouth, rated good. Cervical only.
- `-rWuzfYkd5M` (Chapman SCS): AP and lateral, but a small, faded inset.
- [Vimeo 1109076785](https://vimeo.com/1109076785): 30 s, all fluoroscopy, AP lumbar, CC BY-NC-ND. Possibly a montage of saved shots.
- [PMC4852439](https://pmc.ncbi.nlm.nih.gov/articles/PMC4852439/): 126.6 MB MOV, CC BY 4.0, content unverified.
- Radiopaedia TF ESI loops (rID 87907, 87287, 89588): genuinely live, but only about one level visible.
- `Tbg-a6VosJ8`: a lecture on counting levels under C-arm when a transitional vertebra is present. A qualitative reference, not test data.

**Skip:**
- `J2n_ZFh6x3I`: last-image-hold, and "PAT 17297" is burned in.
- `ZGvEoG5ar1w` and `Vu4N4uQiktg`: magnified to 1–2 bodies.
- `X9kvWXVJfoE`: tiny insets, and the rights sit with the manufacturer.
- Filmed-monitor or phone clips: `RIxoyni0cKM`, `GlyxEYCFTvE`, `xmwqcnN_r3g`, `7GdVnVnF29E`.
- Talking-head or slideshow videos: `C1e84KmcjRs`, `jAgMZcy-MEw`, `BEEuLT764zo`, `TX5gz8c765M`, `XjOdDeKrKEE`.

## 3. Counts

The eight search angles listed 113 entries; seven appear twice, leaving 106 unique. The bins below are my own tally from the verification notes.

A clip counts as **"live motion supported"** if any of these holds:
- a non-zero dose rate or a LIVE indicator is on screen;
- anatomy or contrast changes between frames at the same geometry;
- it is a native multi-frame series;
- the source itself says the footage is cine or real-time.

| | YouTube | Elsewhere | Total |
|---|---|---|---|
| Candidate entries | 70 (one is a 7-clip playlist) | 36 | 106 |
| Live motion supported | 18 | 10 | 28 |
| Fluoroscopy on screen, live vs held unresolved | 28 | 1 | 29 |
| Dynamic digital radiography (flat panel, not fluoroscopy) | 3 | 1 | 4 |
| Short GIF/JPG frame series, not cine | 0 | 2 | 2 |
| Recordings exist but only by request | 0 | 5 | 5 |
| No fluoroscopy seen, or could not be checked | 21 | 17 | 38 |

The 36 entries off YouTube are:
- 22 journal, repository or research-data sources;
- 7 Radiopaedia pages;
- 4 Wikimedia Commons items;
- 3 practice or dealer websites.

**Licences**

| Licence | YouTube-hosted | Elsewhere |
|---|---|---|
| CC BY shown on the watch page | 1 (`KWwGMIoDrmU`) | — |
| CC BY only through the journal article | 2 (`XjOdDeKrKEE`; `_1xMxFZa6tU`, whose article is ambiguous) | — |
| CC BY (any version) | — | 15 (Bern, 6 other PMC supplements, 5 Neurosurgical Focus: Video on Cadmore, 3 Commons) |
| CC BY-SA | — | 1 (Commons barium swallow) |
| CC BY-NC-SA | 5 (Procedure Guide site statement; YouTube coverage unstated) | 7 (6 Radiopaedia, DysphagiaBank) |
| CC BY-NC-ND | — | 2 (PMC6948134, JNS Case Lessons on Vimeo) |
| No Creative Commons line, or licence unread | 62 | 11 |

- **All 10 off-YouTube live items carry an open licence:** Bern and the paediatric cervical exam (CC BY), the Commons swallow (CC BY-SA), and six Radiopaedia cases plus DysphagiaBank (CC BY-NC-SA).
- **On YouTube, no live item has a confirmed Creative Commons licence.**

**Live-motion items by region and view** (fluoroscopy-on-screen but unresolved in brackets)

| Region | Live motion supported | [Unresolved] |
|---|---|---|
| Lumbar, thoracolumbar, lower thoracic | 12 | [21] |
| Sacrum / pelvis | 2 | [3] |
| Thoracic | 2 | [3] |
| Cervical / cervicothoracic | 11 | [2] |
| Spans cervical to thoracic | 1 | [0] |

| View | Live motion supported | [Unresolved] |
|---|---|---|
| AP only | 11 | [10] |
| Lateral only | 8 | [9] |
| AP and lateral | 6 | [8] |
| Oblique | 1 | [0] |
| Rotational sweep | 2 | [0] |
| Unknown | 0 | [2] |

- **On YouTube:** of the 18 live items, 9 are lumbar, lumbosacral or thoracolumbar and 9 are cervical or cervicothoracic.
- **Lateral lumbar or thoracolumbar with live motion supported: three items.** These are the Mayfield lateral run, Radiopaedia rID 21585, and `6MBj9SBZrno`, where the vertebrae cannot be made out.
- **Lateral lumbar flexion-extension cine:** none is public anywhere. One set exists by request: Maastricht, PMC7078620, 11 subjects, L1–S1, 7.5 fps.
- **Cranio-caudal translation:** only Bern (detector panned cranially) and the Commons barium swallow (the field pans down the spine) have it. SCS lead-following (`Yme7AxnIRWI`) might, but that is not verified. The earlier statement still holds strictly: no public source has overlapping frames at a known step. Bern has overlapping frames during a pan, but the step is not known.
- **Rotation:** Radiopaedia rID 24796 (about 180°) and rID 90103 (61 projections), plus the Mayfield alignment runs.
- **Stated levels** that could serve as ground truth:
  - cTvR6wt303k: chapters name T12 and L1;
  - eF3gPgRYxy0: chapters name L1–S1, but no fluoroscopy is confirmed;
  - Bern: T7/8, T9/10, L5/S1;
  - Radiopaedia captions: L1, L3/4, L4/5, S1;
  - the KXz2 pair: "L3 TF" overlay;
  - 6Y2QDj_xUbQ: L5-S1;
  - _1xMxFZa6tU: L5 and S1.

## 4. Legal and ethics notes

- **Downloading from YouTube.** YouTube's Terms of Service restrict downloading, except through features YouTube itself provides or with permission. Watching in a browser to screen and time clips is normal use. Saving the files with yt-dlp or similar, without permission, falls outside it. This holds whatever licence the video carries.
- **What CC BY on a YouTube page does and does not settle.** It licenses reuse of the work by its rights holder. On its own it does not settle the platform's download clause. The cleanest route is the uploader's written permission and the original file sent directly, which is also far better quality than the re-encode. For journal videos on the AANS channel, get the file from the publisher or authors. CC BY supplements hosted on PMC can be taken from PMC.
- **"No Creative Commons line" is not proof of the Standard YouTube License.** Several page reads were truncated or failed. Twice a fetch summary said "Standard YouTube License" and a word-for-word check found no such text, so the summary had made it up. Treat an unknown licence as all rights reserved until the uploader says otherwise.
- **The uploader is not always the rights holder:**
  - `X9kvWXVJfoE` is Vexim/Stryker material.
  - The Speech Therapy Practice playlist has unclear origin; one description appears copied from UC Davis Health.
  - MedBridge and JoVE are commercial.
  - JBJS Essential Surgical Techniques and older Neurosurgical Focus supplements are publisher copyright.
- **Non-commercial terms:**
  - They fit a research test set in a paper, but not validation data for the 510(k) product track without separate permission.
  - Radiopaedia contributors keep their rights and can grant commercial use themselves.
  - DysphagiaBank rules out commercial products, including LLMs, and makes users responsible for claims from people who appear in the videos.
  - NC-ND items forbid derivatives, and annotations may count as derivatives.
- **Privacy.** Public teaching video is usually meant to be de-identified, but every frame needs checking. Examples found:
  - a birth date and age ("3/9/31", "76 y") burned into the Mayfield overlay;
  - "PAT 17297" on `J2n_ZFh6x3I`;
  - a name field reading "speech / logan" on the swallow playlist console;
  - the patient's head visible in `Koq1t9RT9WM`;
  - live patients in `xciOcPXLcGs` (with an audience) and `L_jMZQvr2ow`.

  Mask overlays before any figure, and do not pass on raw frames. Cadaver labs lower the consent question. SR Academy states its footage is cadaveric; for SSF it is likely but the pages do not say so, so ask.
- **Journal CC BY libraries are the clean alternative.** PMC supplements under CC BY 4.0 (Bern, Cureus, Frontiers, BMC) can be downloaded and reused with attribution. Neurosurgical Focus: Video is CC BY for current articles, but its spine content is mostly navigated surgery with saved shots. Europe PMC indexes 453 of its articles; 61 mention fluoroscopy and none says "live fluoroscopy". Operative Neurosurgery, JBJS Essential Surgical Techniques, JoVE, the International Journal of Spine Surgery and VuMedi are not Creative Commons.
- **Ethics review.** Footage received from a clinician, rather than taken from a public dataset, may need its own determination. Ask the IRB before any files arrive.

## 5. Acquisition plan

**Before any email**
1. Check the shortlisted ids against the FluoroCap manifests (`~/FluoroCap_wsl`), since the earlier yt-dlp harvest of 6,085 videos may already hold some. Anything harvested that way carries the same download-clause problem, so do not put it in a test set without permission.
2. Watch the top 15 in a browser, one or two minutes each, without downloading. Log for each:
   - seconds of beam-on motion versus held frames (dose rate above zero, "LIVE" or "LIH" on the overlay);
   - view and vertebrae in the field;
   - overlays;
   - cadaver or patient.
3. Take the CC BY PMC items now: Bern Videos 1–4, PMC10242080, PMC4852439 and PMC11328828. Measure their frames, duration and resolution.

**What to ask every contact**
- **The original recording:** multi-frame DICOM, or an uncompressed export from the C-arm video output. Not the YouTube re-encode or the composited split-screen.
- **How it was acquired:**
  - frame and pulse rate;
  - whether each run is continuous live fluoroscopy or last-image-hold;
  - C-arm model;
  - gantry angle, and any table or detector movement during the run.
- **Level ground truth from the operator:**
  - the target level of each run;
  - how it was counted (from the sacrum, from the T12 rib, or from pre-op imaging);
  - any transitional vertebra or rib-count anomaly;
  - de-identified pre-op CT or MR if they can share it.
- **Subject and consent:** cadaver or patient, and for patients, the consent that covers research reuse.
- **De-identification:** remove burned-in dates, study numbers and names.
- **Permission scope:**
  - research use;
  - publishing derived figures and metrics;
  - releasing annotations;
  - whether commercial use is allowed;
  - the attribution wording they want.

**Contacts, in order**

| # | Contact | Covers | Specific ask |
|---|---|---|---|
| 1 | Seattle Science Foundation, 550 17th Ave, James Tower Suite 600, Seattle WA 98122, [phone withheld] (email on seattlesciencefoundation.org) | Ranks 2, 4, 7–12 and 20, plus unverified SSF demos (`szH5DsL8KLM`, `pufAzs_VpVc`, `9imNQTwETCY`) | One request for all of them. Ask for the raw C-arm recordings behind the composites (for `Yme7AxnIRWI`, the Ziehm native export), and whether each lab used a cadaver. Ask for the treated level per segment; `cTvR6wt303k` already names T12 and L1. |
| 2 | Inselspital Bern, via the corresponding author of PMC8463391 (Piechowiak, Beck, Gralla, Dobrocky) | Rank 1 and the 60-patient cohort behind it | Native unsubtracted dynamic-myelography DICOM with detector or table position per frame, and the level of each run. Ask whether more cases could be shared under a data-transfer agreement. This is the closest thing found to overlapping frames at a known cranio-caudal step. |
| 3 | Mayfield Brain & Spine, [e-mail withheld], [phone withheld] | Rank 3 | The de-identified 98-frame AP and 65-frame lateral series, the cemented levels, the frame rate, and whether the series are contiguous cine. |
| 4 | DMX Imaging LLC, [e-mail withheld], [phone withheld] | Rank 15 and the vendor's archive | De-identified lumbar and thoracolumbar DMX studies at 30 f/s, especially lateral lumbar flexion-extension, which appears nowhere public. |
| 5 | Maastricht, Inge Caelers, [e-mail withheld] | PMC7078620 | The lateral L1–S1 flexion-extension cine: 11 subjects, 7.5 fps, 1024×1024 on a Philips FD20. Probably the same data-agreement route as the Maastricht cervical cine. |
| 6 | The Procedure Guide (Rohit Puranik MD), theprocedureguide.com/contact | Rank 13, `6MBj9SBZrno`, `DCLd6DsoUSg` | Whether the site's CC BY-NC-SA covers the YouTube clips, the original C-arm exports, and the levels (`KXz2k8lOt9U` and `4q8LjcE0vsI` are one patient). |
| 7 | Radiopaedia contributors Salem Bauones (rID 24796), Chris O'Donnell (21585), Jeffrey Hocking (90103) | Ranks 5 and 6 | Native DICOM and projection geometry for the rotational spins, so that levels from the cone-beam CT could be projected onto each frame, as with C-ArmLSpine. Also commercial permission. |
| 8 | Konica Minolta Healthcare Americas (contact form on healthcare.konicaminolta.us) | Rank 17 and the DDR library | Source DDR sequences for L-spine AP flexion-extension and lateral views. Label them flat-panel radiography, not fluoroscopy. |
| 9 | Prof. U. S. Mohanty, Manual Therapy Foundation of India (www.mtfi.net) | Rank 14 | The original lumbar videofluoroscopy file; the YouTube copy films a monitor. |
| 10 | Christopher Faubel MD (FaubelMD.com) | Ranks 21 and 22; older clips on thepainsource.com | The original clips and levels. The site is all rights reserved. |

Optional after these: DARADIA (info@daradia.com; patient consent needed) and Kevin Hines, Jefferson ([e-mail withheld]), for the rank 18 DRG clip.

**Limits of this search**
- The shared web-search budget ran out in every angle. Not searched: Vimeo, JoVE, a YouTube Creative Commons-filtered search, and the YouTube Data API with `videoLicense=creativeCommon`.
- YouTube watch pages could not be read, so duration and licence are unknown for most videos.
- "Live versus held" rests on three sampled frames per video. No video was watched or downloaded.

## Raw candidates by angle (search + verification)

```json
[
 {
  "angle": "kypho",
  "candidates": [
   {
    "url": "https://www.youtube.com/watch?v=VtmxIlY8S9w",
    "title": "Live Demonstration: Vertebral Augmentation Case - Douglas P. Beall, M.D.",
    "channel": "Seattle Science Foundation",
    "year": "recorded 2017 (fluoro overlay dated 11/18/2017); upload year unknown",
    "duration": "unknown",
    "procedure": "Vertebral augmentation: transpedicular needle access and advancement into the vertebral body",
    "region": "lower thoracic / lumbar. Lateral bodies are visible; the level is not stated on any page read",
    "views": "unknown",
    "live_fluoro": "yes. All three YouTube auto-frames (about 25/50/75% of the video) show a large lateral fluoro panel, with clock overlays reading 11:00:43, 11:04:03 and 11:12:26. Fluoro therefore runs through at least about 12 minutes of the recording, but the continuous seconds are unknown",
    "licence": "unknown (watch page not machine-readable here; oEmbed returns 401, i.e. embedding disabled)",
    "quality": "Screen-captured C-arm output composited into a split screen: the fluoro circle takes about the right 55-60% of a 16:9 frame, with two camera insets on the left. kV/mA and date overlays are burned in. The image is grainy (low dose). There are no phone-filmed monitor artefacts. Setting looks like a cadaver lab (skin appearance), but the page does not say so",
    "reachable": "yes. Seattle Science Foundation, a non-profit at 550 17th Ave, James Tower Suite 600, Seattle WA 98122, tel [phone withheld]; an email is listed on seattlesciencefoundation.org",
    "evidence": "Title and id from WebSearch. Frames: i.ytimg.com/vi/VtmxIlY8S9w/hq1.jpg, hq2.jpg, hq3.jpg viewed, each showing a lateral fluoro with an advancing needle and the SSF watermark. oEmbed returned HTTP 401. SSF contact details are from its homepage."
   },
   {
    "url": "https://www.youtube.com/watch?v=B7RHD25tCkU",
    "title": "Vertebral Augmentation Balloon Kyphoplasty - Douglas P Beall, M.D.",
    "channel": "Seattle Science Foundation (SSF TV branding)",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "Balloon kyphoplasty (needle access shown)",
    "region": "thoracolumbar and lumbar: the AP frame shows lower ribs and upper lumbar bodies, the lateral shows lumbar bodies",
    "views": "unknown",
    "live_fluoro": "yes (both frames checked show fluoro). The 50% frame is lateral fluoro with a needle in a lumbar body; the 75% frame is AP fluoro with a needle at the thoracolumbar junction. Seconds unknown",
    "licence": "unknown (oEmbed 401, embedding disabled)",
    "quality": "Large circular fluoro, about 55% of the frame on the left, clean digital capture; presenter inset on the right; decorative purple background. Fluoro FOV spans about 4-6 vertebrae, useful for naming by context",
    "reachable": "yes, via Seattle Science Foundation (as above)",
    "evidence": "Title from a WebSearch result listing. Frames hq2.jpg and hq3.jpg viewed. oEmbed returned HTTP 401."
   },
   {
    "url": "https://www.youtube.com/watch?v=J2n_ZFh6x3I",
    "title": "Vertebral Augmentation - Douglas P. Beall, M.D.",
    "channel": "Seattle Science Foundation (SSF TV branding)",
    "year": "recorded 2022 (fluoro overlay dated 11.11.2022); upload year unknown",
    "duration": "unknown",
    "procedure": "Vertebral augmentation, needle access",
    "region": "lumbar or lower thoracic (the AP/slightly oblique view shows 4-5 bodies; level not stated)",
    "views": "unknown",
    "live_fluoro": "yes. The 50% auto-frame shows a large AP fluoro, with a needle entering the pedicle and a burned-in study/patient overlay (PAT number, 'Bone', timestamp). Seconds unknown",
    "licence": "unknown",
    "quality": "The fluoro circle takes about the right 55% of the frame; a presenter camera is on the left. Digital capture, sharp. The overlay text includes a study number, which would need masking",
    "reachable": "yes, via Seattle Science Foundation",
    "evidence": "Title from a WebSearch result listing. Frame hq2.jpg viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=0sbrxbhfts0",
    "title": "Vertebroplasty & Kyphoplasty Demonstration by Glen David, MD",
    "channel": "Seattle Science Foundation",
    "year": "2016 (the search snippet says May 25, 2016, at the 2nd Annual Spine Trauma Summit, SSF; the fluoro overlay also reads 2016)",
    "duration": "unknown",
    "procedure": "Vertebroplasty and kyphoplasty demonstration (lab)",
    "region": "lumbar (the AP view shows lumbar bodies and pedicles)",
    "views": "unknown",
    "live_fluoro": "yes. The 75% auto-frame shows simultaneous AP (left) and lateral (right) fluoro side by side from OEC-type C-arms, with the right image labelled 'Live'; the 25% and 50% frames are room camera views of the C-arm. Seconds unknown",
    "licence": "unknown (oEmbed 401)",
    "quality": "Biplane AP and lateral, full-width split, each circle about 45% of the frame width. Direct digital capture with kV/mA/dose overlays. The rest of the video is presenter and room camera",
    "reachable": "yes, via Seattle Science Foundation; Glen J. David MD has a listed Swedish (Seattle) physician profile",
    "evidence": "Frames hq1.jpg, hq2.jpg and hq3.jpg viewed. Date and event from the WebSearch summary. oEmbed returned HTTP 401."
   },
   {
    "url": "https://www.youtube.com/watch?v=cTvR6wt303k",
    "title": "Live Demo: Kyphoplasty Pearls of the Thoracic Spine - Jeffrey S. Roh, MD, MBA",
    "channel": "Seattle Science Foundation",
    "year": "2020 (WebSearch: published March 9, 2020)",
    "duration": "unknown",
    "procedure": "Balloon kyphoplasty, thoracic, with balloon inflation under fluoro",
    "region": "thoracic",
    "views": "unknown",
    "live_fluoro": "yes. At 75% there is a large lateral fluoro showing an inflated contrast-filled balloon in a thoracic body (OEC overlay, 117 kVp). At 50% there is a small lateral fluoro inset beside a room view and a model demo. Seconds unknown",
    "licence": "unknown (oEmbed 401)",
    "quality": "Layouts vary: at times the fluoro takes about 55% of the frame, at others it is a small inset of about 30% width. Digital capture",
    "reachable": "yes, via Seattle Science Foundation",
    "evidence": "Title and date from WebSearch. Frames hq2.jpg and hq3.jpg viewed. oEmbed returned HTTP 401."
   },
   {
    "url": "https://www.youtube.com/watch?v=ZGvEoG5ar1w",
    "title": "Kyphoplasty Pearls of the Thoracic Spine - Glen David, MD (as listed by WebSearch; a second WebSearch listing labelled this id 'Kyphoplasty (Osteoporosis Fracture Treatment) Video', unresolved)",
    "channel": "Seattle Science Foundation (SSF TV branding)",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "Kyphoplasty, bipedicular cannulas, cement",
    "region": "thoracic (per title)",
    "views": "unknown",
    "live_fluoro": "yes. The 50% and 75% auto-frames both show a large lateral fluoro, with bipedicular cannulas and a cement/cavity opacity in the vertebral body. Seconds unknown",
    "licence": "unknown (oEmbed 401)",
    "quality": "The fluoro circle takes about the right 60% of the frame; presenter on the left. Digital capture",
    "reachable": "yes, via Seattle Science Foundation",
    "evidence": "Frames hq2.jpg and hq3.jpg viewed. The title conflict between two WebSearch listings is noted."
   },
   {
    "url": "https://www.youtube.com/watch?v=RMM56ibtcQI",
    "title": "Latest Techniques in Vertebral Augmentation Side by Side - Douglas Beall, M.D. & Glen David, M.D.",
    "channel": "Seattle Science Foundation (SSF TV branding)",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "Vertebral augmentation technique comparison (bipedicular access)",
    "region": "lumbar or lower thoracic (lateral; level not stated)",
    "views": "unknown",
    "live_fluoro": "yes. The 50% auto-frame shows a lateral fluoro with two needles in a vertebral body. Seconds unknown",
    "licence": "unknown (oEmbed 401)",
    "quality": "The fluoro circle takes about the right 45% of the frame; a hands/field camera is on the left. Digital capture",
    "reachable": "yes, via Seattle Science Foundation",
    "evidence": "Title from WebSearch. Frame hq2.jpg viewed. oEmbed returned HTTP 401."
   },
   {
    "url": "https://www.youtube.com/watch?v=_kyEJaRYzgI",
    "title": "LAB DEMO: Common Vertebral Augmentation Approaches plus Spine Jack- Douglas P. Beall, M.D.",
    "channel": "Seattle Science Foundation (SSF TV branding)",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "Vertebral augmentation access approaches plus SpineJack (cadaver lab, per 'LAB DEMO')",
    "region": "lumbar or thoracolumbar (lateral; level not stated)",
    "views": "unknown",
    "live_fluoro": "yes. The 75% auto-frame shows a lateral fluoro, with a trocar entering the posterior vertebral body. The 50% frame is a room view of the presenter at the C-arm over a draped specimen. Seconds unknown",
    "licence": "unknown (oEmbed 401)",
    "quality": "The fluoro takes about the left 45% of the frame; field camera on the right. Digital capture",
    "reachable": "yes, via Seattle Science Foundation",
    "evidence": "Title from WebSearch. Frames hq2.jpg and hq3.jpg viewed. oEmbed returned HTTP 401."
   },
   {
    "url": "https://www.youtube.com/watch?v=Vu4N4uQiktg",
    "title": "Spine Jack - Douglas P. Beall, MD",
    "channel": "Seattle Science Foundation (SSF watermark)",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "SpineJack implant vertebral augmentation",
    "region": "lumbar or lower thoracic (lateral; level not stated)",
    "views": "unknown",
    "live_fluoro": "yes, but only as an inset. At 50% there is a lateral fluoro inset (lower left, about 35% of the frame width) with instruments in a vertebral body. Seconds unknown",
    "licence": "unknown",
    "quality": "The fluoro is a small inset beside a large instrument close-up and a room camera. Weaker than the other SSF items for tracking",
    "reachable": "yes, via Seattle Science Foundation",
    "evidence": "Title from WebSearch. Frame hq2.jpg viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=fkRFgkESCgQ",
    "title": "Video1. Fluoroscopic alignment for kyphoplasty",
    "channel": "Mayfield Brain & Spine (@MayfieldClinic)",
    "year": "2013 (feed: published 2013-09-04T14:08:25Z)",
    "duration": "unknown",
    "procedure": "C-arm alignment in the AP and lateral planes for percutaneous vertebral body access, before kyphoplasty",
    "region": "lumbar and thoracolumbar (AP of lumbar bodies with cement at two levels; lateral of thoracolumbar bodies)",
    "views": "5,630 (playlist Atom feed)",
    "live_fluoro": "yes: native fluoro cine runs. The 50% auto-frame shows an AP run with an OsiriX overlay 'Im: 59/98'; the 75% frame shows a lateral run 'Im: 32/65'. These are multi-frame DICOM fluoro loops played back, not stills. The 25% frame is a title card, 'AP left-to-right alignment'. Seconds unknown",
    "licence": "unknown",
    "quality": "The best native quality in this set: a DICOM cine exported through OsiriX (overlay 'Image size: 512 x 512', 'Fluoro', 'Made In OsiriX'), not a filmed monitor. The video is 4:3 SD. The burned-in overlay includes a date and age string that would need masking. Because the subject is C-arm alignment, the runs may include gantry adjustment",
    "reachable": "yes. Mayfield Brain & Spine, 3825 Edwards Rd Suite 300, Cincinnati OH 45209; [e-mail withheld]; [phone withheld]",
    "evidence": "Playlist Atom feed youtube.com/feeds/videos.xml?playlist_id=PLW1ylaMfcOH91_9D1yH1_9x8LfQAXZt-s gave the title, date, views and the description 'Video demonstrating the method to establish fluoroscopic alignment in the AP and lateral planes for percutaneous vertebral body access.' Frames hq1.jpg, hq2.jpg and hq3.jpg viewed. The five sibling videos (45EMxyLxHOI, a2xc9gW4zx8, 5GtDDrMBxNA, pNayih1Ol1M, H4pl1DLUfLo) showed only bone-model demos in every sampled frame and are excluded."
   },
   {
    "url": "https://www.youtube.com/watch?v=xciOcPXLcGs",
    "title": "Percutaneous Vertebroplasty | Step-by-Step Technique Under Fluoroscopy | Pain Management Procedure",
    "channel": "DARADIA: The Pain Clinic (@daradiapainclinic)",
    "year": "2026 (WebSearch: published January 2, 2026)",
    "duration": "unknown",
    "procedure": "Percutaneous vertebroplasty (performed by Dr Gautam Das, edited by Dr Sandeep Margan, per the search snippet)",
    "region": "lumbar or thoracolumbar (AP; level not stated)",
    "views": "unknown",
    "live_fluoro": "yes. All three auto-frames (25/50/75%) show a live fluoro monitor capture labelled 'Normal Fluoro', with a needle advancing through a radiopaque skin localiser grid. All three are AP; whether a lateral view appears is unknown. Seconds unknown",
    "licence": "unknown",
    "quality": "Split screen: the fluoro circle takes about the left 50% of a 16:9 frame (a clean capture of the C-arm display, not phone-filmed); two OR camera views on the right show the C-arm and an audience. The metal grid on the skin overlaps the vertebrae",
    "reachable": "yes. Daradia Pain Hospital, New Town, Kolkata 700156; info@daradia.com; +91 9205 590 559. The director, Dr Gautam Das, is named",
    "evidence": "oEmbed gave the title and channel. The date and credits come from the WebSearch summary. Frames hq1.jpg, hq2.jpg and hq3.jpg viewed. Contact details are from daradia.com. The channel feed shows other fluoroscopy 'Step-by-Step' videos in the same format (not in this angle)."
   },
   {
    "url": "https://www.youtube.com/watch?v=X9kvWXVJfoE",
    "title": "SpineJack手術過程影片",
    "channel": "凱寶生技",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "SpineJack implant kyphoplasty, surgical technique",
    "region": "lumbar or thoracolumbar (AP and lateral insets; level not stated)",
    "views": "unknown",
    "live_fluoro": "yes, as small insets only. The 50% frame has a lateral inset and the 75% frame an AP inset, in a box labelled 'Fluoroscopy' (about 30% of the frame width). Seconds unknown",
    "licence": "unknown",
    "quality": "Manufacturer surgical-technique template (SpineJack branding, 'Tool / Fluoroscopy / Procedure' panels). The fluoro insets are small (about 160x110 px at 480p). This appears to be a repost of the device maker's video, so the rights probably sit with Stryker/Vexim, not the uploader",
    "reachable": "uncertain. The uploader looks like a Taiwanese distributor; no contact was established",
    "evidence": "oEmbed gave the title and channel. Frames hq2.jpg and hq3.jpg viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=L_jMZQvr2ow",
    "title": "RENOVA SPINE™ 13G Kyphoplasty System - Live surgery with Dr.Iannucci",
    "channel": "Biopsybell SRL BPB MEDICA™ (@BPBMEDICA)",
    "year": "2021 (WebSearch: May 2021)",
    "duration": "unknown",
    "procedure": "Balloon kyphoplasty, 13G system (manufacturer's 'real case')",
    "region": "unknown (the kit is indicated for thoracolumbar VCF)",
    "views": "unknown",
    "live_fluoro": "unknown. The sampled frames (default thumbnail, 25%, 50% and 75%) show an intro card and the back-table preparation; no fluoro was seen",
    "licence": "unknown",
    "quality": "HD-looking OR video with a green title card; the fluoro content is unverified",
    "reachable": "yes. Biopsybell S.R.L., Via Aldo Manuzio 24, 41037 Mirandola (MO), Italy, tel +39 0535 27850. The operator is Dr Iannucci, Director of Neuroradiology, Ospedale San Bortolo Vicenza (per the intro card)",
    "evidence": "oEmbed gave the title and channel. The Biopsybell video library describes it as 'Real case of kyphoplasty 13G performed by Dr. Iannucci'. Contact details are from the product page. Frames hqdefault.jpg, hq1.jpg, hq2.jpg and hq3.jpg viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=3gi56mQzaLQ",
    "title": "CIFOPLASTIA LUMBAR",
    "channel": "videocolumna",
    "year": "2009 (feed: 2009-01-26)",
    "duration": "unknown",
    "procedure": "Lumbar balloon kyphoplasty (subtitled steps: 'Insertion of 1st needle', balloon inflation, 'Fill up the cavity with bone cement (PMMA)')",
    "region": "lumbar (per title)",
    "views": "17,331 (channel Atom feed)",
    "live_fluoro": "unknown. All three sampled frames are OR field footage with English subtitles; no fluoro was seen",
    "licence": "unknown",
    "quality": "4:3 SD from 2009, likely low resolution. It looks like a device-company procedure film",
    "reachable": "unknown (the channel has 3 videos from 2009 and a blank description)",
    "evidence": "oEmbed and the feed youtube.com/feeds/videos.xml?user=videocolumna gave the title, date and views. Frames hq1.jpg, hq2.jpg and hq3.jpg viewed."
   }
  ],
  "notes": "YouTube is a real source for this angle, and most of what is there comes from one uploader. The Seattle Science Foundation (SSF) channel posts vertebral-augmentation lab demos. Each has a large, clean capture of the C-arm output (often lateral, sometimes simultaneous AP and lateral, labelled 'Live') composited next to room cameras. Nine SSF videos are listed above, and the channel almost certainly holds more (Beall, Glen David, Roh and others). A title filter over the SSF catalogue (channel UChIIig54yF9aQYvpWGe1DPg) would enumerate them. SSF has embedding disabled on every video checked (oEmbed HTTP 401), so ask for permission before any reuse. The fluoro in these labs appears to be cadaveric; the pages do not say so.\n\nThe best native-quality item is Mayfield 'Video1. Fluoroscopic alignment for kyphoplasty' (2013). It plays back actual multi-frame DICOM fluoro runs in OsiriX: 98- and 65-frame AP and lateral loops, 512x512. The other five videos in that playlist appear to be bone-model demos only. DARADIA (Kolkata) has a 2026 vertebroplasty video with a clean fluoro capture (AP only in the sampled frames). DARADIA also posts other fluoroscopy 'Step-by-Step' procedures in the same split-screen format, including lumbar biacuplasty ucxNd3GP4j0 and SI joint injection UHnjQVnzln4; these are outside this angle.\n\nLimits that affect a temporal test set:\n1. The level is almost never named on screen. The augmentation view is usually a tight 2-5 vertebra FOV on one level, so ground-truth naming would have to come from the operator or be inferred from ribs or the sacrum when they are visible.\n2. Augmentation keeps the C-arm parked on one level, so frame-to-frame change is mostly needle, balloon and cement, not anatomy moving cranio-caudally. The exception is alignment runs such as the Mayfield video.\n3. The fluoro sits inside split-screen layouts (about 30-60% of the frame) and needs cropping. Burned-in overlays include dates and study numbers.\n4. Continuous-fluoro seconds could not be measured without watching. The SSF Beall live demo shows fluoro at 25/50/75% with overlay clocks spanning about 12 minutes, and the Glen David demo shows a 'Live' label, but none of this establishes how long the unbroken live stretches are.\n\nMethod and what could not be established: WebFetch of YouTube watch, results, channel and playlist pages returns only the site footer, so duration and licence could not be read for any video and are reported as unknown. Metadata came from four other sources:\n- WebSearch snippets.\n- YouTube oEmbed (title and channel; HTTP 401 means embedding is disabled).\n- YouTube Atom feeds for playlists and legacy usernames (description, publish date, views; only the latest 15 entries).\n- YouTube's auto-generated thumbnails hq1/hq2/hq3 (frames at about 25/50/75% of the video), which WebFetch saved and I viewed. These are how fluoroscopy content was verified. No video was downloaded.\n\nThe WebSearch budget ran out (200/200) partway through. Planned follow-ups were not run: the Spanish 'Transmisión En Vivo de una Cifoplastía' (l_TIi5t4XwY returns oEmbed 404, probably removed), the Japanese BKP series by 'opn' (so_R6xcnU_4 is the preparation part only), and Chinese PKP uploads.\n\nExcluded after viewing frames:\n- Interventional Clinic kyphoplasty videos (stock photo, 3D/CT composites, animation).\n- HCA 'vertebroplasty and kyphoplasty' (animation).\n- Radiology Espresso SpineJack case (MRI scroll in the frames sampled).\n- Clinicco Brasov (interview).\n- El Paso Spine Center 'Live Kyphoplasty Patient Before and After' cShRpc9-FAM: OR point-of-view camera and a named, identifiable patient, with no fluoro in the frames.\n- HealthEast/ORlive 2007 webcast 6_GquZfZF-E: promo and interview frames, low resolution, embedding disabled.\n- Off-YouTube: Radiopaedia 'Percutaneous vertebroplasty' (O'Donnell, L1) has a fluoroscopy series, but I could not confirm it is a cine, and the page as fetched stated no licence. Wikimedia Commons has only stills.\n\nRead-only context from this machine: the spinesurg-ct-nnunet docs record an earlier yt-dlp harvest of 6,085 YouTube videos (FluoroCap). Check whether these ids are already in the ~/FluoroCap_wsl manifests before contacting anyone.",
  "verify": [
   {
    "url": "https://www.youtube.com/watch?v=VtmxIlY8S9w",
    "confirmed_live_fluoro": "Yes, fluoro is visible at all three sampled points. The hq1/hq2/hq3 auto-frames (about 25/50/75%) each show a large lateral C-arm panel with the needle at a different depth. Its clocks read 11:00:43, 11:04:03 and 11:12:26, and the date is 11/18/2017. How many seconds of that is live motion rather than last-image-hold is unknown. The SSF panel shows the C-arm monitor, which holds the last image between exposures (see J2n_ZFh6x3I).",
    "confirmed_licence": "Not stated. The watch page read through r.jina.ai has no 'License', 'Creative Commons' or 'reuse allowed' string. That fits the Standard YouTube License but is not proof. oEmbed returns 401 (embedding disabled).",
    "confirmed_views": "Lateral in all three samples. AP not seen.",
    "usable_for_tracking": "possible",
    "corrections": "Published Nov 20, 2017; 10,131 views. The chapters show balloon kyphoplasty: 'Extra Binocular Approach' 9:05 (auto-transcribed 'extrapedicular'), Cavity Creation 13:08, Directional Needle 15:21, 'How Many Millimeters Is the Balloon' 19:13, Cement Injection 23:03, so the video runs at least 23 minutes. The level is not stated. The page does not say whether it is a cadaver or a patient. Contact via Seattle Science Foundation stands."
   },
   {
    "url": "https://www.youtube.com/watch?v=B7RHD25tCkU",
    "confirmed_live_fluoro": "Yes at two of three samples. At 50% there is a large lateral fluoro with a needle in a lumbar body; at 75% a large AP fluoro of about six bodies with the needle entering low in the field. At 25% it is a room view of Beall at a C-arm over a draped body in the SSF lab. The share of live motion versus last-image-hold is unknown.",
    "confirmed_licence": "Not stated (r.jina.ai read found no licence string).",
    "confirmed_views": "Lateral and AP.",
    "usable_for_tracking": "possible",
    "corrections": "Published Dec 13, 2024; 5,239 views. Chapters: Transpedicular 0:00, Parapedicular 2:45, Extrapedicular 5:39, Balloon kyphoplasty 9:15, Vertebral augmentation 20:16, Q&A 28:50, so the video runs at least 29 minutes. The fluoro circle fills about the left 55% of the frame on a purple background. The level is not stated; 'thoracolumbar' is my reading of the AP field, not a page statement."
   },
   {
    "url": "https://www.youtube.com/watch?v=J2n_ZFh6x3I",
    "confirmed_live_fluoro": "Largely no, as far as the samples show. The 25% and 50% auto-frames show the same AP fluoro image, with the needle in the same position, while the overlay clock moves from 12:35:23 to 12:35:55 and the overlay reads 'LIH 1'. That is last-image-hold, not live cine. At 75% it is a room view with no fluoro. How many seconds are live is unknown.",
    "confirmed_licence": "Not stated (r.jina.ai read found no licence string).",
    "confirmed_views": "AP / slightly oblique only. No lateral seen.",
    "usable_for_tracking": "poor",
    "corrections": "Published Feb 21, 2023; 16,019 views; no chapters. The duration is not shown. If the recording is unedited, the 32 s of clock between the 25% and 50% frames suggests about 2 minutes. The overlay carries 'PAT 17297', 'Pain', 11.11.2022 and 'LIH', and would need masking. This is the clearest evidence that SSF fluoro panels mostly show held frames."
   },
   {
    "url": "https://www.youtube.com/watch?v=0sbrxbhfts0",
    "confirmed_live_fluoro": "Yes at the 75% sample only. It shows two OEC fluoro panels side by side: the left is AP (75 kVp, 3.09 mA) with a needle at the pedicle; the right is labelled 'Live' (115 kVp, 8.01 mA) with a vertical cannula, and its orientation is unclear at thumbnail size. The 25% and 50% samples are room views of Glen David at an OEC C-arm. Seconds unknown.",
    "confirmed_licence": "Not stated (r.jina.ai read found no licence string). oEmbed returns 401.",
    "confirmed_views": "AP (left panel). The right 'Live' panel is probably lateral but that is not confirmed.",
    "usable_for_tracking": "possible",
    "corrections": "Published May 25, 2016; 91,701 views. Description: 'Vertebroplasty & Kyphoplasty was demonstrated by Glen David, MD during the 2nd Annual Spine Trauma Summit held at the Seattle Science Foundation.' Duration unknown; no chapters. Two C-arms with simultaneous AP and second-view panels would be valuable if they persist, but only one of three samples shows fluoro."
   },
   {
    "url": "https://www.youtube.com/watch?v=cTvR6wt303k",
    "confirmed_live_fluoro": "Yes at all three samples. At 25% and 50% it is a small lateral inset (lower left, about 30% of the frame width) with the trocar advancing. At 75% it is a large lateral panel with a contrast-filled balloon (OEC, 117 kVp). The share of live versus held frames is unknown.",
    "confirmed_licence": "Not stated (r.jina.ai read found no licence string).",
    "confirmed_views": "Lateral. The room camera shows two monitors (AP and lateral), but AP is not seen in the video panel samples.",
    "usable_for_tracking": "possible",
    "corrections": "Region is thoracolumbar, not only thoracic. The chapters name the levels: 'T12 trochar placement' 2:46, 'Balloon inflation at T12' 10:45, 'Cement injection at T12' 14:31, 'L1 vertebroplasty procedure' 20:22, Q&A 27:55. That gives stated level ground truth, which is rare. Published Mar 9, 2020; 35,717 views; runs at least 28 minutes. For about half the samples the fluoro is only an inset."
   },
   {
    "url": "https://www.youtube.com/watch?v=ZGvEoG5ar1w",
    "confirmed_live_fluoro": "Partly. At 50% there is a large lateral fluoro with bipedicular cannulas and a mottled opacity in the body below. At 75% the fluoro is heavily magnified or oblique, with cannulas visible and the vertebral outlines barely identifiable. At 25% it is a bone-model close-up, not fluoro. Seconds unknown.",
    "confirmed_licence": "Not stated (r.jina.ai read found no licence string).",
    "confirmed_views": "Lateral at 50%; magnified lateral or oblique at 75%.",
    "usable_for_tracking": "poor",
    "corrections": "The title resolves to 'Kyphoplasty Pearls of the Thoracic Spine - Glen David, MD' (the conflicting listing is resolved). Published May 25, 2021; 5,868 views; no chapters; duration unknown. The magnified fields show about 1-2 vertebrae, too little context to name a level."
   },
   {
    "url": "https://www.youtube.com/watch?v=RMM56ibtcQI",
    "confirmed_live_fluoro": "Yes at all three samples. At 25% it is AP with a needle and cement already in two bodies; at 50% lateral with two parallel needles; at 75% lateral with a cement or cavity opacity. The fluoro fills about the right 45% of the frame. The share of live versus held frames is unknown.",
    "confirmed_licence": "Not stated (r.jina.ai read found no licence string).",
    "confirmed_views": "AP and lateral.",
    "usable_for_tracking": "possible",
    "corrections": "Published May 2, 2022; 3,913 views. Chapters run to 43:01, from 'Arcadia Balloon' 29:45 to 'Cervical Spine Posterior Lateral Approach' 43:01, so some cervical content is likely. The specimen already carries cement from earlier demonstrations. The level is not stated."
   },
   {
    "url": "https://www.youtube.com/watch?v=_kyEJaRYzgI",
    "confirmed_live_fluoro": "Yes at one of three samples. At 75% there is a lateral fluoro (left, about 45% of the frame) with a trocar entering the posterior body and about four bodies visible. The 25% and 50% samples are room views at the C-arm. Seconds unknown.",
    "confirmed_licence": "Not stated (read via r.jina.ai of m.youtube.com; no licence string).",
    "confirmed_views": "Lateral. AP not seen.",
    "usable_for_tracking": "possible",
    "corrections": "Title confirmed as 'LAB DEMO: Common Vertebral Augmentation Approaches plus Spine Jack- Douglas P. Beall, M.D.'; published Nov 18, 2021; 2,820 views. Chapters: Transpedicular 0:00, Parapedicular 3:57, Extra-pedicular 8:54, Balloon kyphoplasty 12:30, Tumor ablation 25:50, SpineJack 29:30, Technique discussion 44:00, so it runs at least 44 minutes. The level is not stated."
   },
   {
    "url": "https://www.youtube.com/watch?v=Vu4N4uQiktg",
    "confirmed_live_fluoro": "Yes but weak. At 25% there is a small lateral inset (upper left) and at 50% a small lateral inset (lower left). At 75% the lateral panel is large (right, about 60%) but magnified to about 1.5 bodies, showing the SpineJack and cement. Seconds unknown.",
    "confirmed_licence": "Not stated (r.jina.ai read found no licence string).",
    "confirmed_views": "Lateral only.",
    "usable_for_tracking": "poor",
    "corrections": "The fluoro is not only an inset: at 75% it is large but magnified. Published Mar 9, 2020; 21,738 views; chapters run to 28:47 (Introduction to SpineJack through Risks and complications). There is too little vertebral context for level naming."
   },
   {
    "url": "https://www.youtube.com/watch?v=fkRFgkESCgQ",
    "confirmed_live_fluoro": "Very likely a native fluoro sequence. At 50% it is an AP frame 'Im: 59/98' and at 75% a lateral frame 'Im: 32/65', both 512x512 'Fluoro' series played in OsiriX. At 25% it is a title card, 'AP left-to-right alignment'. The acquisition frame rate, and whether the frames are contiguous cine rather than a stack of saved spot images, is not stated. Given the chapter timing, the fluoro plays for roughly 30-40 s in total.",
    "confirmed_licence": "Not stated. The r.jina.ai read found no licence string. A first fetch summary claimed 'Standard YouTube License', but the verbatim check returned no such text, so that claim was fabricated.",
    "confirmed_views": "AP and lateral, with alignment runs in which the C-arm is adjusted in both planes.",
    "usable_for_tracking": "good",
    "corrections": "The earlier 'views: 5,630' was a view count, not radiographic views; 5,630 is confirmed. Published Sep 4, 2013. Chapters: 'Percutaneous Vertebral Body Access' 0:01, 'AP left-to-right alignment' 0:09, 'AP cranial-caudal alignment' 0:20, 'Lateral cranial-caudal alignment' 0:28, 'Lateral left-to-right alignment' 0:38. From those and the auto-frame positions, the video runs about 40-56 s. Cement is already present in two bodies in both views. The burned-in overlay shows a birth date ('3/9/31', '76 y') and a study date, so it needs masking. It is short, but it is the only candidate with frame-indexed native fluoro series and deliberate view change."
   },
   {
    "url": "https://www.youtube.com/watch?v=xciOcPXLcGs",
    "confirmed_live_fluoro": "Yes in all three samples. A C-arm console capture labelled 'Normal Fluoro' shows the needle advancing through radiopaque rectangular grid markers. The description states 'performed under continuous fluoroscopic guidance' and 'Controlled cement injection in small aliquots under continuous fluoroscopy'. Seconds unknown; the frames at 50% and 75% look similar and could be held images.",
    "confirmed_licence": "Not stated (r.jina.ai read found no licence string).",
    "confirmed_views": "AP (some obliquity) in all three samples. Lateral not seen.",
    "usable_for_tracking": "possible",
    "corrections": "Published Jan 2, 2026; 1,455 views. Chapters: Preparation and positioning 0:00, Needle insertion 1:34, Cement preparation 3:31, Injection and monitoring 4:27, Final delivery and removal 7:10, so it runs about 7-8 minutes. Image contrast is low; the vertebral outlines are faint and partly covered by the markers. This is a live patient with an audience (a workshop), so patient consent and privacy need asking about in addition to the licence."
   },
   {
    "url": "https://www.youtube.com/watch?v=X9kvWXVJfoE",
    "confirmed_live_fluoro": "Unknown. At 50% and 75% there are small 'Fluoroscopy' insets (lateral, then AP) inside a SpineJack technique template. Whether the insets move or are static stills per step cannot be told from the samples. At 25% there is a Vexim 'REBALANCING SPINE' logo card.",
    "confirmed_licence": "Not stated (r.jina.ai read found no licence string). The Vexim logo confirms this is the manufacturer's film reposted, so the rights sit with Vexim/Stryker, not the uploader.",
    "confirmed_views": "Lateral and AP insets.",
    "usable_for_tracking": "poor",
    "corrections": "Published May 20, 2020; 718 views; the description is only the title. The insets are too small for vertebra tracking even if they are live."
   },
   {
    "url": "https://www.youtube.com/watch?v=L_jMZQvr2ow",
    "confirmed_live_fluoro": "Unknown. No fluoro appears in any sample: the 25% frame is a green intro card (Dr Iannucci, Director of Neuroradiology, Ospedale San Bortolo Vicenza), and the 50% and 75% frames show back-table preparation.",
    "confirmed_licence": "Not stated (r.jina.ai read found no licence string).",
    "confirmed_views": "unknown",
    "usable_for_tracking": "poor",
    "corrections": "Published May 4, 2021; 2,176 views. Description: 'The video is intended for healthcare professional only. Join Dr. Iannucci in this live surgery where the minimally invasive technique of kyphoplasty is presented on a real case.' No chapters; duration not shown. A real patient, so consent applies as well as the licence."
   },
   {
    "url": "https://www.youtube.com/watch?v=3gi56mQzaLQ",
    "confirmed_live_fluoro": "Unknown. All three samples are OR field footage with subtitles ('Insertion of 1st needle', balloon inflation, 'Fill up the cavity with bone cement (PMMA) or Bone Substitute'); no fluoro was seen.",
    "confirmed_licence": "Not stated (r.jina.ai read found no licence string).",
    "confirmed_views": "unknown",
    "usable_for_tracking": "poor",
    "corrections": "The duration is 9:53, per the m.youtube.com page read through r.jina.ai. It is 4:3 SD from 2009. The channel, date and views could not be re-read on this pass because the page returned 401."
   }
  ]
 },
 {
  "angle": "screws",
  "candidates": [
   {
    "url": "https://www.youtube.com/watch?v=eF3gPgRYxy0",
    "title": "Live Demo: Percutaneous Long Segment Fixation - Jeffrey S. Roh, MD, MBA",
    "channel": "Seattle Science Foundation (212K subscribers)",
    "year": "2018 (Aug 8)",
    "duration": "33:59 per Brave listing (chapters run to 30:13)",
    "procedure": "Multilevel percutaneous pedicle screws L1-S1 with percutaneous rod passage; appears to be a cadaver-lab 'Live Demo'",
    "region": "lumbar + sacrum (L1-S1)",
    "views": "Radiographic view: unknown (percutaneous L1-S1 screws are normally placed under AP and lateral C-arm). View count 14,617",
    "live_fluoro": "unknown",
    "quality": "unknown. Resolution was not visible in the page render.",
    "licence": "No Creative Commons line in the rendered watch page, so probably the Standard YouTube License (YouTube does not print that label)",
    "reachable": "yes: nonprofit CME educator, seattlesciencefoundation.org; surgeon named",
    "evidence": "r.jina.ai render of the watch page: channel, date, views and chapters 'L5 pedicle screw insertion 0:00, S1 5:13, Placing screws at L1-L4 10:01, S1 screw fixation 16:09, Percutaneous rod placement 21:57, Rod reduction 27:32, closing 30:13'. Duration from the Brave search listing. Stepping through five levels makes this the best multilevel lumbar fit in this angle, but no text confirms that fluoro loops are on screen."
   },
   {
    "url": "https://www.youtube.com/watch?v=KQig-Y1AShg",
    "title": "Percutaneous Pedicle Screw fixation",
    "channel": "SR Academy's Brain & Spine channel (395 subscribers)",
    "year": "2025 (Apr 27)",
    "duration": "16:38",
    "procedure": "Percutaneous pedicle screw fixation, cadaveric workshop ('SR Academy's Spine Cadaveric workshop - Greevasthi Batch 2025')",
    "region": "lumbar or thoracolumbar (level unknown)",
    "views": "Radiographic view: unknown. The 'Vertebral squaring' chapter implies C-arm alignment to the end plates. View count 1,440",
    "live_fluoro": "unknown. 'Vertebral squaring' at 3:11 and 'Guidewire placement' at 10:45 suggest C-arm footage.",
    "quality": "unknown",
    "licence": "No Creative Commons line on the rendered page, so probably the Standard YouTube License",
    "reachable": "probably: an Indian training academy runs the channel; no contact link captured",
    "evidence": "jina render: chapters 0:00 prep, 1:51 positioning, 3:11 'Vertebral squaring', 4:34 entry planning, 10:45 guidewire, 12:18 tapping and screws, 14:19 rod. Duration from Brave. Squaring the vertebra is a C-arm manoeuvre, so the fluoro screen is likely shown, but this is not confirmed."
   },
   {
    "url": "https://www.youtube.com/watch?v=KWwGMIoDrmU",
    "title": "Minimally invasive oblique interbody fusion for correction of iatrogenic lumbar deformity",
    "channel": "American Association of Neurological Surgeons (74.1K); the video article is Wilkerson et al., Neurosurg Focus Video 2020, Univ. of Utah",
    "year": "2020 (YouTube Feb 20; article Jan 2020)",
    "duration": "9:28",
    "procedure": "MIS OLIF followed by percutaneous pedicle screws L3-L5 (stage 2)",
    "region": "lumbar (L3-L5)",
    "views": "Radiographic: lateral and AP described. The transcript says the patient is placed 'in true lateral position with disc spaces orthogonal in the lateral fluoroscopic view and pedicles aligned in the AP view'. View count 7,872",
    "live_fluoro": "unknown. The transcript mentions 'AP and lateral images' and 'lateral fluoroscopy' checks.",
    "quality": "unknown. Journal video, age-restricted on YouTube.",
    "licence": "YouTube page states 'Creative Commons Attribution license (reuse allowed)'. The PMC article (PMC9521211) states CC BY 4.0.",
    "reachable": "yes: University of Utah Neurosurgery authors (Mazur, Dailey); AANS/JNS",
    "evidence": "The PMC9521211 full text gives the YouTube link youtu.be/KWwGMIoDrmU, the CC BY 4.0 statement and the fluoroscopy sentences. oEmbed gives the AANS channel. The jina render gives 9:28, 7,872 views and the CC licence line verbatim. This is the only verified CC BY YouTube candidate in this angle."
   },
   {
    "url": "https://stream.cadmore.media/r10.3171/2021.10.FOCVID2112",
    "title": "Outpatient endoscopic resection of large calcified thoracic disc herniation with caudal displacement (Neurosurg Focus Video, PMC9555359)",
    "channel": "Neurosurgical Focus: Video (JNS), hosted on Cadmore, not YouTube",
    "year": "2022 (Jan)",
    "duration": "about 8 min (transcript runs to 8:00)",
    "procedure": "Intraoperative level localisation by fluoroscopic counting, then endoscopic transforaminal thoracic discectomy",
    "region": "thoracic (T9-10); counting from the 12th rib and from the sacrum",
    "views": "Radiographic: AP and lateral (needle docking described on both)",
    "live_fluoro": "unknown. The transcript refers to 'intraoperative fluoroscopic image[s]'.",
    "quality": "unknown",
    "licence": "CC BY 4.0 ('This is an open access article distributed under the CC BY license')",
    "reachable": "yes: Konakondla, Slotkin et al., Geisinger Neuroscience Institute",
    "evidence": "PMC9555359 transcript: 'We counted up from the 12th rib but also from the sacrum to mark the level of T9–10'; 'Marking levels intraoperatively ... comparing to intraoperative fluoroscopic images'. Level counting is shown explicitly, and the thoracic region is where counting fails."
   },
   {
    "url": "https://stream.cadmore.media/r10.3171/2024.1.FOCVID23209",
    "title": "Full endoscopic resection of ventral thoracic osteophyte and repair of spontaneous CSF leak (Neurosurg Focus Video, PMC11013356)",
    "channel": "Neurosurgical Focus: Video (JNS), hosted on Cadmore",
    "year": "2024 (Apr)",
    "duration": "unknown",
    "procedure": "C-arm level localisation with a static spinal-needle marker, then endoscopic thoracic surgery",
    "region": "thoracic (T7-8)",
    "views": "Radiographic: AP stated ('The C-arm on the AP view was used to mark the appropriate level')",
    "live_fluoro": "unknown",
    "quality": "unknown",
    "licence": "CC BY 4.0",
    "reachable": "yes: Sofoluke and Konakondla (Geisinger), Hofstetter (U Washington), Leyendecker (Cologne)",
    "evidence": "PMC11013356 transcript: 'Intraoperative fluoroscopy is used to identify specific landmarks. After the appropriate level is identified...'; 'a spinal needle was placed on the caudal pedicle'; 'static marker at the level of interest is our preferred technique ... in the thoracic spine'."
   },
   {
    "url": "https://stream.cadmore.media/r10.3171/2024.1.FOCVID23216",
    "title": "Endoscopic MIS-TLIF with Destandau's system: leveraging endoscopy with conventional instruments (Neurosurg Focus Video, PMC11013367)",
    "channel": "Neurosurgical Focus: Video (JNS), hosted on Cadmore",
    "year": "2024 (Apr)",
    "duration": "unknown",
    "procedure": "Endoscopic MIS-TLIF with C-arm level confirmation, marking needle at the disc and cage position check",
    "region": "lumbosacral (L5-S1)",
    "views": "Radiographic: AP marking of the pedicle line and end plates; lateral implied for the disc and cage",
    "live_fluoro": "unknown",
    "quality": "unknown",
    "licence": "CC BY 4.0",
    "reachable": "yes: Kumar, Srivastava et al., Neurosurgery, SGPGIMS Lucknow",
    "evidence": "PMC11013367 transcript: 'Skin markings were made under fluoroscopic guidance'; 'Docking was done and the level was confirmed with C-arm'; 'Using a marking needle, the disc level is confirmed under the C-arm'; 'cage ... position was confirmed on the C-arm'."
   },
   {
    "url": "https://stream.cadmore.media/r10.3171/2024.1.FOCVID23231",
    "title": "Biportal endoscopic transforaminal lumbar interbody fusion using a large cage for degenerative spondylolisthesis with stenosis (Neurosurg Focus Video, PMC11013353)",
    "channel": "Neurosurgical Focus: Video (JNS), hosted on Cadmore",
    "year": "2024 (Apr)",
    "duration": "unknown",
    "procedure": "Biportal endoscopic TLIF, with portals placed under C-arm",
    "region": "lumbar (L4-5)",
    "views": "Radiographic: unknown (C-arm guidance stated)",
    "live_fluoro": "unknown",
    "quality": "unknown",
    "licence": "CC BY 4.0",
    "reachable": "yes: Dong Hwa Heo, Chungdam Harrison Spinartus Hospital, Seoul",
    "evidence": "PMC11013353 transcript: 'Under C-arm fluoroscopic guidance, two portals are created at the left-sided L4 and L5 levels.'"
   },
   {
    "url": "https://www.youtube.com/watch?v=nAG3zVMAArw",
    "title": "Minimally Invasive Sacroiliac Joint (SIJ) Fusion Two-implant technique utilizing Fluoroscopy views",
    "channel": "Mayo Clinic (1.26M subscribers)",
    "year": "2022 (May 5)",
    "duration": "19:22",
    "procedure": "MIS SI joint fusion, two implants; Dr William 'Woodie' Cross III",
    "region": "sacrum / pelvis (SI joint; implants reach the vertebral body per description)",
    "views": "Radiographic: title says 'Fluoroscopy views'. Lateral, inlet and outlet are standard for this procedure but are not named on the page. View count 29,929",
    "live_fluoro": "unknown. The 'Final Images' chapter at 19:08 suggests saved stills at the end.",
    "quality": "unknown",
    "licence": "No Creative Commons line on the rendered page, so probably the Standard YouTube License",
    "reachable": "yes: Mayo Clinic, named surgeon (Orthopaedic Surgery, Rochester)",
    "evidence": "oEmbed: Mayo Clinic channel. jina render: date, 29,929 views, description, key moments 7:39 'Decorticating Tool', 11:41 'Bone Grafting', 19:08 'Final Images'. Duration from Brave."
   },
   {
    "url": "https://www.youtube.com/watch?v=TX5gz8c765M",
    "title": "Biplanar x-ray fluoroscopy for sacroiliac joint fusion",
    "channel": "American Association of Neurological Surgeons (74.1K); authors Vanaclocha-Vanaclocha, Verdú-López, Sáiz-Sapena, Herrera, Rivera-Paz (Valencia)",
    "year": "2016 (Sep 1)",
    "duration": "5:12",
    "procedure": "SI joint fusion guided by biplanar (two-C-arm) fluoroscopy",
    "region": "sacrum / pelvis",
    "views": "Radiographic: biplanar (two simultaneous projections), exact views unknown. View count 12,712",
    "live_fluoro": "unknown. The title is about fluoroscopy, so fluoro footage is likely, but continuous vs stills is not stated.",
    "quality": "unknown; age-restricted, sign-in required",
    "licence": "No Creative Commons line on the rendered page (unlike the 2020 AANS upload above), so probably the Standard YouTube License",
    "reachable": "yes: AANS; named Spanish neurosurgeons",
    "evidence": "Brave snippet lists the authors. jina render: AANS channel, 5:12, 12,712 views, 'No description has been added', age-restricted, no licence line."
   },
   {
    "url": "https://www.youtube.com/watch?v=0VRHMrIDii0",
    "title": "INSIDE THE OR: Sacroiliac Joint Fusion (Full 25 min surgery)",
    "channel": "Antonio J. Webb, M.D. (1.06M subscribers)",
    "year": "2022 (Mar 19)",
    "duration": "24:37-24:38",
    "procedure": "Full-length SI joint fusion",
    "region": "sacrum / pelvis",
    "views": "Radiographic: unknown. View count about 162K",
    "live_fluoro": "unknown",
    "quality": "unknown",
    "licence": "No Creative Commons line seen (render partly failed), so probably the Standard YouTube License",
    "reachable": "yes: South Texas Spinal Clinic, San Antonio, [phone withheld] (phone taken from the same channel's LLIF page)",
    "evidence": "Brave listing: 24:38, 162K views, Mar 19 2022, snippet 'Dr. Webb talks about ... sacroiliac joint dysfunction'. jina render: title and 24:37 only (401 on the rest)."
   },
   {
    "url": "https://www.youtube.com/watch?v=E06MD3KnhvE",
    "title": "INSIDE THE OR: Lateral Lumbar Interbody Fusion (LLIF) w/percutaneous screws",
    "channel": "Antonio J. Webb, M.D. (1.06M subscribers)",
    "year": "2023 (Jul 23)",
    "duration": "11:05",
    "procedure": "LLIF plus percutaneous pedicle screws; fluoroscopic positioning and localisation",
    "region": "lumbar (levels not stated)",
    "views": "Radiographic: unknown. View count 96,400",
    "live_fluoro": "unknown. The chapter at 1:50 reads 'Pre surgical positioning and localization fluoroscopy images', which suggests stills.",
    "quality": "unknown",
    "licence": "No Creative Commons line seen, so probably the Standard YouTube License",
    "reachable": "yes: South Texas Spinal Clinic, San Antonio, [phone withheld]",
    "evidence": "jina render: chapters 1:50 localisation fluoro images, 8:00 'Percutaneous pedicle screw placement'; clinic phone in the description. Duration from Brave."
   },
   {
    "url": "https://www.youtube.com/watch?v=0gKbg_WetJo",
    "title": "2-level MIS TLIF my FAVORITE surgery!!",
    "channel": "Choll Kim MD PhD (247K subscribers)",
    "year": "2021 (Dec 10)",
    "duration": "6:17",
    "procedure": "Two-level MIS TLIF (L3-4 collapse, L4-5 spondylolisthesis, degenerative scoliosis)",
    "region": "lumbar (L3-L5)",
    "views": "Radiographic: unknown. View count 6,045",
    "live_fluoro": "unknown",
    "quality": "unknown",
    "licence": "No Creative Commons line on the rendered page, so probably the Standard YouTube License",
    "reachable": "yes, directly: [e-mail withheld], [phone withheld], www.excelspine.com (in the description)",
    "evidence": "jina render: channel, date, views, case description and contact details. Duration from Brave. The same surgeon also posted 'Unbelievably Perfect MIS TLIF' (O6m7jjEuIOQ, 8:32, 2022), which was not verified (401)."
   },
   {
    "url": "https://www.youtube.com/watch?v=Tbg-a6VosJ8",
    "title": "Challenges for counting the correct lumbar level in the transitional vertebra",
    "channel": "Practical Pain Management with Dr. Lee (14.9K subscribers)",
    "year": "2022 (Oct 13/14)",
    "duration": "13:07",
    "procedure": "Level counting under C-arm when a lumbosacral transitional vertebra is present (pain-procedure context: iliac-crest line, T12 rib counting, Castellvi)",
    "region": "lumbar / lumbosacral junction; thoracolumbar (T12 rib)",
    "views": "Radiographic: C-arm AP and oblique; lateral radiographs mentioned. View count 3,459",
    "live_fluoro": "unknown. The page may use C-arm stills.",
    "quality": "unknown",
    "licence": "No Creative Commons line, so probably the Standard YouTube License",
    "reachable": "probably: named physician's teaching channel; no contact captured",
    "evidence": "jina render of the description: 'iliac crest as a reference line, the T12 rib counting method, and the Castellvi classification'; imaging listed as 'C-arm fluoroscopy, AP and oblique views'. Chapters: 'Morphological mismatch' 6:17, 'How to encounter the level' 7:51. Directly on the LSTV level-naming question."
   },
   {
    "url": "https://www.youtube.com/watch?v=6MBj9SBZrno",
    "title": "Fluoroscopic lumbar epidural injection lateral contrast spread",
    "channel": "The Procedure Guide (1.58K subscribers)",
    "year": "2021 (Apr 9)",
    "duration": "unknown (likely a short clip)",
    "procedure": "Interlaminar lumbar epidural steroid injection. Outside this angle; included because it is the only page found that states live fluoro.",
    "region": "lumbar",
    "views": "Radiographic: lateral. View count 4,979",
    "live_fluoro": "yes. The description says 'Live fluoro from an interlaminar lumbar epidural steroid injection, lateral view'; seconds unknown.",
    "quality": "unknown",
    "licence": "No Creative Commons line, so probably the Standard YouTube License",
    "reachable": "yes: TheProcedureGuide.com (companion website with articles)",
    "evidence": "WebSearch snippet and jina render both quote the 'Live fluoro ... lateral view' description. The channel probably holds more short live-fluoro spine clips; its videos page would not render."
   },
   {
    "url": "https://www.youtube.com/watch?v=56Sxu0thpcU",
    "title": "Lumbar Coupling (Video Fluoroscopy) by Prof. Mohanty and Dr. Shamla Pazare of MTFI",
    "channel": "Umasankar Mohanty (5.03K subscribers)",
    "year": "2009 (Jan 9)",
    "duration": "unknown",
    "procedure": "Diagnostic videofluoroscopy of lumbar coupled motion (side flexion with rotation). Outside this angle; motion study, not surgery.",
    "region": "lumbar",
    "views": "Radiographic: probably AP, since the study is side flexion and rotation (not stated). View count 4,352",
    "live_fluoro": "yes. The title and description say video fluoroscopy of actual spinal motion; seconds unknown.",
    "quality": "unknown; 2009 upload, so likely low resolution",
    "licence": "No Creative Commons line, so probably the Standard YouTube License",
    "reachable": "probably: Prof. U. Mohanty / MTFI (Manual Therapy Foundation of India); study done at Datta Meghe Institute of Medical Sciences, Wardha",
    "evidence": "jina render of the description: 'utilized video fluoroscopy imaging to document how rotation of the lumbar region associated with the side flexion occurs'. This is continuous lumbar cine with the whole vertebral column moving, which suits frame-to-frame tracking."
   }
  ],
  "notes": "YouTube is a real source, but no page in this angle confirms live fluoro loops. Only the two out-of-angle pages (The Procedure Guide, and the MTFI lumbar-coupling cine) explicitly say live or video fluoroscopy. In surgical videos, C-arm footage usually appears as short inset shots, and from text alone I could not tell whether it is live or saved stills. Someone has to watch the shortlisted videos to settle it.\n\nHow the pages were read, and the limits:\n- The WebSearch budget ran out partway through (200 of 200 calls for the session).\n- YouTube watch pages fetched directly return only the footer.\n- Metadata came from four sources, with no video downloaded and no transcript API used:\n  - YouTube oEmbed (title and channel);\n  - the r.jina.ai reader rendering of the watch page (description, chapters, views, and the licence line when present; it returned 401 on about half the pages);\n  - Brave search result pages (durations and dates; rate-limited with a 429 after about six queries);\n  - NCBI E-utilities and PMC full text for the journal videos.\n- YouTube only prints a licence line when the video is Creative Commons. \"No Creative Commons line\" therefore means the Standard YouTube License is likely, not confirmed.\n\nMost useful legal finding: the Neurosurgical Focus: Video articles in PMC state CC BY 4.0 (checked on the 2020, 2022, 2024 and 2026 articles). I had expected CC BY-NC-ND. The AANS YouTube channel re-posts these videos with \"Creative Commons Attribution license (reuse allowed)\", checked on KWwGMIoDrmU. The older 2016 Neurosurgical Focus supplement videos on the same channel (TX5gz8c765M, 2u6H4Pc_8To) show no CC line. From 2021 the journal videos are hosted on stream.cadmore.media rather than YouTube. PMC search inside the journal found, besides the candidates listed:\n- PMC9562560: Uribe, retropleural thoracic, fluoro needle localisation;\n- PMC9558910: Alan, prone transpsoas, fluoro marking of L3/L4;\n- PMC11013336: Ohio State MIS separation surgery, cement augmentation under fluoroscopy at L1-L3, all CC BY;\n- PMC13418632 plus the Seattle Science Foundation demo gkqkRIi1W7U (Abd-El-Barr, 14:16, 2024): TrackX fluoroscopic instrument tracking. TrackX overlays instruments on saved AP and lateral shots, so it is stills plus overlay, not continuous fluoro.\n\nBest permission route: the Seattle Science Foundation channel (212K subscribers, nonprofit) is the densest pool of cadaver-lab C-arm demos. One request could cover several videos. None of these were verified for live fluoro:\n- Roh eF3gPgRYxy0;\n- Hyun Bae -K0hQ2PLaDs (19:06, 2020);\n- Paul Park 'Surgical Demo: MIS TLIF' szH5DsL8KLM (40:34, 2021; chapters include cage insertion and pedicle screw insertion);\n- Rakesh Patel u9r0QKwx0ds (20:14, 2023);\n- Oskouian xwsBx1a6T68 (12:12, 2022) and pufAzs_VpVc (32:24, 2022, fenestrated screws with cement);\n- Anu Amin 9imNQTwETCY (2024, fenestrated screws and cement; cement augmentation is normally watched under live lateral fluoro);\n- 360 Lab Qvp4x0bNzWY (2:28, 2017, embedding disabled).\n\nCholl Kim (email in his description) and Dr Webb (clinic phone) are the most directly reachable individual surgeons.\n\nSeen but not verified, all probably Standard YouTube License:\n- Dorsolumbar percutaneous screws, Dr Dhandapani SS, PGIMER Chandigarh X7Bie2MG9Ok (13:42, 2021). Academic real-OR footage; worth a look.\n- OrthoTV Peshattiwar XrcONxGMNsg (11:52, 2024).\n- CDA Spine (Jeffrey Larson): zckRlqZLyiI (3:10, 2010) and hO-sbVraM2I MIS TLIF (8:51, 2013, 309K views).\n- Eastlack, San Diego Spine Foundation, Cd8Eucp_DLQ (25:05, 2021). Lecture with chapters 'Imaging and landmarking' and 'Jamshidi needle placement'.\n- Mayo single-implant SIJ fusion 7d8QjW5gguQ (15:52, 2021, 161K views).\n- Sacrix 'Quick Technique Steps' ZUJhfOYnUgo (KIC Ventures, commercial; description says '100% fluoroscopic').\n- Chad Stephens SIJ lateral approach e0rIZRRqVPk (19:56, 2026).\n- Dr Shantanu Mallick thoracic epidural under fluoro dVBbXxjyaHk (2022; thoracic live fluoro is rare, but this is outside the angle).\n- Fluoroscopic lumbar puncture demos XN5Q1HpP0OA, CxySsRJ4-Io, zuC80-cJcwA (outside the angle).\n\nUnavailable: KkmJKuV7_14 'How to Use a C-arm: Spine Positioning' (GE, 2:46) renders 'This video isn't available anymore'.\n\nDropped:\n- Animations (Magnifi lJ-ggDAQNLQ, MAS TLIF ggdKG0OvL90, fNXwL7EN-yE, 9ZOSthJ8UNI, LC2Y5jT9RQU).\n- Radiographer positioning tutorials, which state positioning before exposure.\n- Navigated or robotic videos (Chen and Park 2u6H4Pc_8To, 11:42, AANS, no CC line; the 2025-2026 Neurosurgical Focus: Video robot series), where fluoro is minimal.\n\nNo YouTube or journal page in this angle describes overlapping frames at a known cranio-caudal step.",
  "verify": [
   {
    "url": "https://www.youtube.com/watch?v=eF3gPgRYxy0",
    "confirmed_live_fluoro": "unknown. The rendered page (via r.jina.ai) has no word for fluoro, C-arm, x-ray, AP or lateral in the title, description or chapters. The transcript panel exists but its text did not render.",
    "confirmed_licence": "No licence line on the page. 'Creative Commons' does not appear, and neither does the word 'License'. The absence of a CC line means the Standard YouTube License by default, but the page never prints that label.",
    "confirmed_views": "unknown. Nothing on the page names a radiographic view.",
    "usable_for_tracking": "possible",
    "corrections": "Confirmed: Seattle Science Foundation (212K subscribers), Aug 8 2018, 14,617 views, and chapters 0:00 L5, 5:13 S1, 10:01 L1-L4, 16:09 S1 fixation, 21:57 rod, 27:32 reduction, 30:13 closing. I could not confirm a duration from the page. 'Cadaver lab' is not supported: the description is the foundation's boilerplate and never uses 'cadaver', 'lab' or 'workshop'. An earlier WebFetch summary reported 'Standard YouTube License', but a literal-string check found no licence text at all. That label was the summariser's inference. It stays the best multilevel L1-S1 candidate only because of its chapter list; there is no evidence yet that loops appear on screen."
   },
   {
    "url": "https://www.youtube.com/watch?v=KQig-Y1AShg",
    "confirmed_live_fluoro": "unknown. The only imaging-related text is the chapter 'Vertebral squaring' at 3:11. No fluoro, C-arm or x-ray wording anywhere.",
    "confirmed_licence": "No licence line. 'Creative Commons' and 'License' are both absent, so the Standard YouTube License by default.",
    "confirmed_views": "unknown",
    "usable_for_tracking": "possible",
    "corrections": "Confirmed: SR Academy's Brain & Spine channel (@sracademy2026, 395 subscribers), Apr 27 2025, 1,440 views, description 'SR Academy's Spine Cadaveric workshop - Greevasthi Batch 2025'. It is a cadaver workshop, so there is no patient-consent problem, but levels are not stated. The 16:38 duration came from Brave. The page confirms only a last chapter at 14:19, so the video is at least that long. No contact details were captured; the channel About page returned 401. 'Vertebral squaring' is a live C-arm manoeuvre, which makes on-screen continuous fluoro plausible, but that remains unconfirmed."
   },
   {
    "url": "https://www.youtube.com/watch?v=KWwGMIoDrmU",
    "confirmed_live_fluoro": "unknown. The PMC9521211 transcript mentions lateral fluoroscopy used to position the patient (1:53) and to confirm the location, plus 'AP and lateral images' of graft position. Those read as discrete confirmation shots. Nothing says live or continuous fluoro.",
    "confirmed_licence": "CC BY, verified twice. The YouTube page states 'Creative Commons Attribution license (reuse allowed)' verbatim, and PMC9521211 states the CC BY licence (creativecommons.org/licenses/by/4.0/).",
    "confirmed_views": "Stage 1 (OLIF): lateral and AP. At 1:53 the transcript says 'true lateral position with the disc spaces orthogonal to the floor in the lateral fluoroscopic view and the pedicles aligned in the AP view'. It also says 'The location can be confirmed with lateral fluoroscopy' and 'AP and lateral images show appropriate interbody graft position'.",
    "usable_for_tracking": "possible",
    "corrections": "The percutaneous pedicle screws in stage 2 were not placed under fluoroscopy. The transcript says a reference array went on the PSIS, 'an intraoperative scan was performed', the screws were advanced 'using image guidance', and 'An intraoperative CT scan is performed' at the end. Fluoroscopy in stage 2 was used only 'to mark the midline'. Fluoro content is therefore limited to OLIF positioning and graft checks at L3-L5. The page shows 9:28; the PMC transcript's last timestamp is 8:53. Confirmed: AANS channel, Feb 20 2020, 7,872 views, age-restricted, no description. This is still the only verified CC BY YouTube item, which makes it the easiest to reuse if the footage turns out to contain loops."
   },
   {
    "url": "https://stream.cadmore.media/r10.3171/2021.10.FOCVID2112",
    "confirmed_live_fluoro": "no evidence of it, and probably stills. The transcript describes discrete shots: 'an intraoperative fluoroscopic image can be taken', 'confirmed again with fluoroscopic imaging', 'Intraoperative fluoroscopy was taken to confirm'. It never mentions live or continuous fluoro.",
    "confirmed_licence": "CC BY 4.0. PMC9555359 states open access under CC BY, and the Crossref licence entry is creativecommons.org/licenses/by/4.0/ from 2022-01-01.",
    "confirmed_views": "AP and lateral. The transcript says 'the guide needle is docked on the posterior superior apex of the inferior vertebral body (on the lateral view) and just medial to the ipsilateral pedicle (on the AP view)'.",
    "usable_for_tracking": "poor",
    "corrections": "The Cadmore player page would not render through WebFetch or r.jina.ai (empty), so I checked everything against PMC9555359 and Crossref. Confirmed: Konakondla, Sofoluke, Barber, Rimini, Slotkin (Geisinger and Houston Methodist); Neurosurg Focus Video 2022;6(1):V18; transcript ends at (8:00); 'We counted up from the 12th rib but also from the sacrum to mark the level of T9–10'. It is valuable as a documented thoracic level-counting case, but as a temporal tracking test it is likely a few stills."
   },
   {
    "url": "https://stream.cadmore.media/r10.3171/2024.1.FOCVID23209",
    "confirmed_live_fluoro": "unknown, leaning to stills. The fluoro material is only the 'Targeting and Docking' section (2:49-4:03, about 74 s, shared with dilator and retractor footage). The transcript elsewhere refers to 'the still image' for endoscopic frames.",
    "confirmed_licence": "CC BY. PMC11013356 says 'This is an open access article distributed under the CC BY license'.",
    "confirmed_views": "AP only is stated: 'The C-arm on the AP view was used to mark the appropriate level'. No lateral is mentioned.",
    "usable_for_tracking": "poor",
    "corrections": "Duration: the last transcript timestamp is 8:20 (Postoperative Course), so the video runs somewhat past 8:20. The previous entry said 'unknown'. Confirmed: authors Sofoluke, Leyendecker, Hofstetter, Konakondla; Neurosurg Focus Video 2024;10(2):V17; T7-8; spinal needle as a static marker on the caudal pedicle. The Cadmore page itself did not render."
   },
   {
    "url": "https://stream.cadmore.media/r10.3171/2024.1.FOCVID23216",
    "confirmed_live_fluoro": "unknown, leaning to stills. The C-arm appears at four discrete confirmation points: 1:41 skin marking 'under fluoroscopic guidance', 2:09 'level was confirmed with C-arm', 4:40 marking-needle disc level 'confirmed under the C-arm', and 6:26 cage 'position was confirmed on the C-arm'.",
    "confirmed_licence": "CC BY 4.0 (PMC11013367, creativecommons.org/licenses/by/4.0/)",
    "confirmed_views": "unknown for the intraoperative C-arm. The transcript does not name AP or lateral for any intraoperative shot. The only named view is a preoperative 'Standing x-ray lateral view' at 0:59. The previous entry's 'AP marking of the pedicle line' is not in the transcript as quoted.",
    "usable_for_tracking": "poor",
    "corrections": "The last transcript timestamp is 7:29. Confirmed: Kumar, Srivastava, Sardhara, Mehrotra, Bhaisora, Raj Kumar (SGPGIMS Lucknow); Neurosurg Focus Video 2024;10(2):V10; L5-S1 with a pars fracture. The Cadmore page rendered empty, so everything was checked against PMC."
   },
   {
    "url": "https://stream.cadmore.media/r10.3171/2024.1.FOCVID23231",
    "confirmed_live_fluoro": "unknown. A single sentence at 2:24 reads 'Under C-arm fluoroscopic guidance, two portals are created at the left-sided L4 and L5 levels.' The only other images are preoperative dynamic flexion/extension X-rays (0:49), postoperative MRI (7:18) and a postoperative X-ray (7:32).",
    "confirmed_licence": "CC BY 4.0 (PMC11013353, creativecommons.org/licenses/by/4.0/)",
    "confirmed_views": "unknown",
    "usable_for_tracking": "poor",
    "corrections": "The last transcript timestamp is 8:33. Author: Dong Hwa Heo (sole author), Chungdam Harrison Spinartus Hospital, Seoul; Neurosurg Focus Video 2024;10(2):V15. The intraoperative fluoro content is at most one short passage, which makes this the weakest of the four JNS items for tracking."
   },
   {
    "url": "https://www.youtube.com/watch?v=nAG3zVMAArw",
    "confirmed_live_fluoro": "unknown. 'Fluoroscopy views' in the title is the only fluoro text. The key moment 'Final Images' at 19:08 suggests saved stills at the end.",
    "confirmed_licence": "No licence line. 'Creative Commons' and 'License' are both absent, so the Standard YouTube License by default.",
    "confirmed_views": "unknown. The page names no view: no lateral, inlet or outlet.",
    "usable_for_tracking": "poor",
    "corrections": "Confirmed: Mayo Clinic, May 5 2022, 29,929 views, Dr William 'Woodie' Cross III; description as quoted before; key moments 7:39, 11:41, 19:08. I could not confirm the 19:22 duration from the page. The target is the SI joint and pelvis, where there are almost no vertebral levels to name, so it is weak for a vertebra-naming test even if loops are shown."
   },
   {
    "url": "https://www.youtube.com/watch?v=TX5gz8c765M",
    "confirmed_live_fluoro": "unknown. The YouTube page has no description. The article abstract (Crossref, DOI 10.3171/2016.2.focusvid.1687) says two x-ray machines give simultaneous AP and lateral projections that can be 'made quickly at any time during the surgical procedure'. That supports on-demand shots, not necessarily continuous loops.",
    "confirmed_licence": "No CC line on YouTube: 'Creative Commons' and 'License' are both absent. The journal record (Neurosurgical Focus 41, Video Suppl 1, 2016) has no Creative Commons licence entry in Crossref, only version-of-record links to thejns.org. The JNS page returned 403. Treat it as copyrighted: Standard YouTube License plus JNS copyright.",
    "confirmed_views": "AP and lateral, simultaneous biplanar, per the article abstract ('simultaneous AP and lateral x-ray projections').",
    "usable_for_tracking": "poor",
    "corrections": "The views are now established as AP plus lateral, from the abstract rather than the page. DOI: 10.3171/2016.2.focusvid.1687. Confirmed: AANS, Sep 1 2016, 5:12, 12,712 views, age-restricted, 'No description has been added'. SI joint and pelvis target, so few nameable vertebrae."
   },
   {
    "url": "https://www.youtube.com/watch?v=0VRHMrIDii0",
    "confirmed_live_fluoro": "unknown. The watch-page render returned 401 and gave no description or chapters.",
    "confirmed_licence": "unknown. The page did not render, so I could not check for a licence line. Probably the Standard YouTube License, but that is unverified.",
    "confirmed_views": "unknown",
    "usable_for_tracking": "poor",
    "corrections": "Only the title and channel are confirmed, via oEmbed: 'INSIDE THE OR: Sacroiliac Joint Fusion (Full 25 min surgery)', Antonio J. Webb, M.D., @antoniowebbmd. Upload date, duration and view count come only from the earlier Brave listing; I could not re-verify them. The contact details (South Texas Spinal Clinic, [phone withheld]) are confirmed from his LLIF video's description, not from this page. SI joint target, so it is weak for level naming."
   },
   {
    "url": "https://www.youtube.com/watch?v=E06MD3KnhvE",
    "confirmed_live_fluoro": "unknown, leaning to stills for localisation. The chapter at 1:50 reads 'Pre surgical positioning and localization fluoroscopy images' and runs to 2:34 (about 44 s). The chapter 'Percutaneous pedicle screw placement' at 8:00 may include C-arm footage, but no text says so.",
    "confirmed_licence": "No licence line. 'Creative Commons' and 'License' are both absent, so the Standard YouTube License by default.",
    "confirmed_views": "unknown",
    "usable_for_tracking": "poor",
    "corrections": "Confirmed: Jul 23 2023, 96,400 views, and the full chapter list (0:00 intro, 0:11, 0:50 MRI, 1:50 localisation fluoro images, 2:34 BMA, 3:54 discectomy, 5:15 trial, 5:40 DBM, 5:47 spacer, 6:45, 7:28 neuromonitoring, 8:00 percutaneous screws). The contact details are confirmed verbatim: South Texas Spinal Clinic, 9150 Huebner Rd Ste 290, San Antonio TX 78240, office [phone withheld], www.spinaldoc.com. The 11:05 duration is not shown on the rendered page."
   },
   {
    "url": "https://www.youtube.com/watch?v=0gKbg_WetJo",
    "confirmed_live_fluoro": "unknown. The page has no fluoro, C-arm or x-ray wording. The surgeon's bio in the description stresses 'computer-assisted minimally invasive spine surgery' and 'image guidance and navigation technologies'. That makes a navigated case (and not continuous C-arm) more likely, though this is not stated for this case.",
    "confirmed_licence": "No licence line. 'Creative Commons' and 'License' are both absent, so the Standard YouTube License by default.",
    "confirmed_views": "unknown",
    "usable_for_tracking": "poor",
    "corrections": "Confirmed: Choll Kim MD PhD, Dec 10 2021, 6,045 views; case text (67-year-old, degenerative scoliosis, L3-4 collapse, L4-5 spondylolisthesis); contact [phone withheld], [e-mail withheld], www.excelspine.com. The player showed 0:00/0:00, so the 6:17 duration is not confirmed. The navigation emphasis was missing from the previous entry and lowers the odds of fluoro loops."
   },
   {
    "url": "https://www.youtube.com/watch?v=Tbg-a6VosJ8",
    "confirmed_live_fluoro": "unknown. The description says 'I faced the C-arm image on AP and oblique view' (which suggests stills) and 'during the C-arm procedure, I can scan counting the upper and lower lumbar levels' (which describes live scanning in his practice but not necessarily footage in the video). The chapters (Introduction, Examples 3:17, Functionality 4:28, Morphological mismatch 6:17, How to encounter the level 7:51, Review 10:54) read like a lecture with images.",
    "confirmed_licence": "No licence line. 'Creative Commons' and 'License' are both absent, so the Standard YouTube License by default.",
    "confirmed_views": "C-arm AP and oblique (stated). Lateral is mentioned only for locating the promontory ('how about the promontory in the lateral view?').",
    "usable_for_tracking": "poor",
    "corrections": "The page title carries a stray prefix: 'C_Challenges for counting the correct lumbar level in the transitional vertebra.' Confirmed: Oct 13 2022, 3,459 views, 14.9K subscribers. Duration is not shown on the rendered page. It discusses Castellvi IB, II, IIIA and IV examples, including an L6. That makes it highly relevant as a qualitative LSTV level-naming reference, but weak as a temporal tracking test unless the 'scan' footage is on screen."
   },
   {
    "url": "https://www.youtube.com/watch?v=6MBj9SBZrno",
    "confirmed_live_fluoro": "yes, stated by the uploader. The description reads verbatim: 'Live fluoro from an interlaminar lumbar epidural steroid injection, lateral view.' The number of seconds is unknown.",
    "confirmed_licence": "The YouTube page has no CC line: 'Creative Commons' and 'License' are both absent, so the Standard YouTube License on YouTube. However, the companion website TheProcedureGuide.com states 'Everything on the site is under a creative commons license (CC BY-NC-SA 4.0)' and asks for a link back. Whether that covers this YouTube upload is not stated, so ask.",
    "confirmed_views": "lateral (stated in the title and description)",
    "usable_for_tracking": "possible",
    "corrections": "Confirmed: The Procedure Guide (@theprocedureguide, 1.58K subscribers), Apr 9 2021, 4,979 views. Duration and resolution are unknown; oEmbed does not give them and I found no Shorts marker for this video. New: the website's CC BY-NC-SA 4.0 statement, which the previous entry did not report. Contact and team pages exist at theprocedureguide.com/contact/ and /about-our-team/; no individual author is named. The site's interlaminar epidural and lumbar fluoroscopic-anatomy articles show no embedded video, only still fluoro images. The channel's videos page returned 401, so I could not enumerate other live clips. Caveats: a lateral interlaminar view is typically tightly collimated to two or three segments, and the scene is static (contrast spreading), so it is a real but easy temporal test."
   },
   {
    "url": "https://www.youtube.com/watch?v=56Sxu0thpcU",
    "confirmed_live_fluoro": "yes. The title says 'Video Fluoroscopy'. The description says 'we took this video fluoroscopy of lumbar region at the operation theatre of the orthopedic dept, Datta meghe institute of medical sciences, Wardha' and 'You can see in the video clearly the rotation of the lumbar region associated with the side flexion.' It is continuous cine of a moving lumbar spine. The number of seconds is unknown.",
    "confirmed_licence": "No licence line. 'Creative Commons' and 'License' are both absent, so the Standard YouTube License by default.",
    "confirmed_views": "unknown. The page does not state it. Side flexion with coupled rotation is normally imaged AP, but that is an inference.",
    "usable_for_tracking": "good",
    "corrections": "Exact page title: 'Lumbar Coupling ( Video Fluoroscopy)by Prof.Mohanty and Dr.Shamla Pazare of MTFI'. Confirmed: Umasankar Mohanty (5.03K subscribers), Jan 9 2009, 4,352 views. Dr Shamla Pazare is from Ravi Nair Physiotherapy College, Wardha. Duration and resolution are unknown; a 2009 upload is likely 240p-360p. This is the only candidate where continuous fluoro with multi-vertebra motion is stated in the uploader's own words, which makes it the best temporal-tracking fit here despite probable low resolution and an unstated view."
   }
  ]
 },
 {
  "angle": "inject",
  "candidates": [
   {
    "url": "https://www.youtube.com/watch?v=4q8LjcE0vsI",
    "title": "Lumbar transforaminal epidural injection with incorrect needle placement and live contrast spread",
    "channel": "The Procedure Guide (@theprocedureguide, channel UC6JX0LXHI-I2-_h37Sw5Tkg)",
    "year": "2021 (published 2021-03-25)",
    "duration": "unknown",
    "procedure": "Lumbar transforaminal epidural steroid injection (L3 TF), needle repositioning, live contrast injection",
    "region": "lumbar (about L2-L4 in frame); views: AP and lateral",
    "views": "13,229 (channel RSS feed)",
    "live_fluoro": "yes. Live runs of a few seconds each. The OEC fluoro-time counter reads 0.1-0.2 min for the whole case across the two thumbnails. Text annotation cards are laid over parts of it.",
    "quality": "Direct digital capture of the GE OEC C-arm output, not a filmed monitor. Octagonal iris collimation. Burned-in kVp/mA/dose/clock overlays. Text overlay 'Good needle placement on AP for L3 TF'. Resolutions offered: unknown.",
    "licence": "YouTube licence field unknown (watch page did not render). The uploader's site states: 'Everything on the site is under a creative commons license (CC BY-NC-SA 4.0)'.",
    "reachable": "Yes. theprocedureguide.com/contact has a contact form. The founder and primary editor is Rohit Puranik, MD (anesthesiology/pain), and the team page links his LinkedIn.",
    "evidence": "Title, date and views come from the channel RSS feed (youtube.com/feeds/videos.xml?channel_id=UC6JX0LXHI-I2-_h37Sw5Tkg). The feed description reads 'Lumbar transforaminal epidural injection with incorrect needle placement and live contrast...'. The hqdefault thumbnail shows an AP lumbar frame with an OEC overlay and the caption about L3 TF. The hq3 auto-frame shows a lateral lumbar frame. The clocks read 9:14:56 and 9:15:23 AM. CAUTION: the clocks and dose counters show this is the SAME patient and session as KXz2k8lOt9U (9:17:02 AM)."
   },
   {
    "url": "https://www.youtube.com/watch?v=KXz2k8lOt9U",
    "title": "Transforaminal live fluoroscopic contrast injection",
    "channel": "The Procedure Guide (@theprocedureguide)",
    "year": "2021 (published 2021-03-25)",
    "duration": "unknown",
    "procedure": "Lumbar transforaminal epidural injection, live contrast injection checking for vascular uptake",
    "region": "lumbar (3 vertebrae in frame); view: AP, possibly slight ipsilateral oblique",
    "views": "7,107 (RSS feed)",
    "live_fluoro": "yes. The feed description reads 'Transforaminal epidural live fluoroscopic contrast injection. No vascular uptake'. It is likely a few seconds long; the counter reads 0.4 min cumulative for the case.",
    "quality": "Direct OEC capture with the TheProcedureGuide.com watermark, kVp/mA/dose overlays and octagonal collimation. Resolutions offered: unknown.",
    "licence": "YouTube licence field unknown. The uploader's site states CC BY-NC-SA 4.0 for everything on the site.",
    "reachable": "Yes, through the contact form at theprocedureguide.com/contact. Founder: Rohit Puranik, MD.",
    "evidence": "RSS feed entry and oEmbed (author 'The Procedure Guide'). The hqdefault thumbnail shows AP lumbar with the needle and contrast, the OEC overlay and a 9:17:02 AM clock. It is the same patient and session as 4q8LjcE0vsI."
   },
   {
    "url": "https://www.youtube.com/watch?v=6MBj9SBZrno",
    "title": "Fluoroscopic lumbar epidural injection lateral contrast spread",
    "channel": "The Procedure Guide (@theprocedureguide)",
    "year": "2021 (published 2021-04-09)",
    "duration": "unknown",
    "procedure": "Lumbar interlaminar epidural steroid injection, contrast spread",
    "region": "lumbar; view: lateral",
    "views": "4,979 (RSS feed)",
    "live_fluoro": "yes. The feed description reads 'Live fluoro from an interlaminar lumbar epidural steroid injection, lateral view'. Seconds unknown; likely short, since the counter reads 0.1 min.",
    "quality": "Direct OEC capture. Heavily collimated octagonal field and low contrast, so vertebral bodies are hard to see in the thumbnail. kVp/mA/dose/clock overlays.",
    "licence": "YouTube licence field unknown. The site states CC BY-NC-SA 4.0.",
    "reachable": "Yes, through the contact form at theprocedureguide.com/contact (Rohit Puranik, MD).",
    "evidence": "RSS feed description and oEmbed. The hqdefault thumbnail was viewed: lateral view, OEC overlay, clock 12:52:27 PM."
   },
   {
    "url": "https://www.youtube.com/watch?v=DCLd6DsoUSg",
    "title": "Fluoroscopic Caudal Epidural Contrast Spread",
    "channel": "The Procedure Guide (@theprocedureguide)",
    "year": "2021 (published 2021-05-11)",
    "duration": "unknown",
    "procedure": "Caudal epidural steroid injection, contrast spread",
    "region": "sacrum and lower lumbar (the contrast column ascends the canal); view not established from the thumbnails (collimated vertical strip)",
    "views": "13,650 (RSS feed)",
    "live_fluoro": "yes. The on-screen OEC 'LIVE' indicator is visible, and the feed says 'Live fluoro from a caudal epidural steroid injection'. The run lasts only a few seconds: two auto-frames share the clock 10:15:29 AM while dose rises from 1.05 to 1.28 mGy.",
    "quality": "Direct OEC capture with the TheProcedureGuide.com watermark and a narrow rectangular collimation. kVp/mA/dose overlays.",
    "licence": "YouTube licence field unknown. The site states CC BY-NC-SA 4.0.",
    "reachable": "Yes, through the contact form at theprocedureguide.com/contact (Rohit Puranik, MD).",
    "evidence": "RSS feed and search snippet ('Live fluoro from a caudal epidural steroid injection. The full article is on TheProcedureGuide'). The hqdefault and hq3 thumbnails were viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=1eFLBwOtgGU",
    "title": "Fluoroscopic Guided Cervical Epidural Injection",
    "channel": "The Procedure Guide (@theprocedureguide)",
    "year": "2021 (published 2021-03-30)",
    "duration": "unknown",
    "procedure": "Cervical interlaminar epidural steroid injection (Tuohy needle, loss of resistance, contrast)",
    "region": "cervical; view not established (thumbnail looks lateral or contralateral oblique)",
    "views": "8,516 (RSS feed)",
    "live_fluoro": "mixed: stills plus live video. The feed describes 'Highlight images and video'. The hq2 auto-frame is a title card reading 'Inject contrast under live fluoro. Confirm epidural spread'.",
    "quality": "Direct OEC capture with a circular field. The thumbnail is overexposed and washed out. Interstitial text cards.",
    "licence": "YouTube licence field unknown. The site states CC BY-NC-SA 4.0.",
    "reachable": "Yes, through the contact form at theprocedureguide.com/contact (Rohit Puranik, MD).",
    "evidence": "RSS feed description. The hqdefault (OEC cervical frame with needle) and hq2 (text card) thumbnails were viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=CTyIu-EGby8",
    "title": "Lumbar Transforaminal Epidural",
    "channel": "ThePainSource (channel UCA4LjZ6K5NuXd6BBWvnLwdQ; Christopher Faubel, MD)",
    "year": "2011 (published 2011-12-29)",
    "duration": "unknown",
    "procedure": "Lumbar transforaminal epidural steroid injection; needle advanced 1-2 mm until good epidural spread",
    "region": "lumbar (about 3 vertebrae in frame); view: AP",
    "views": "9,895 (RSS feed)",
    "live_fluoro": "likely yes (short contrast runs), with text cards between clips. The hq3 auto-frame is a card reading 'Next, the needle was advanced another millimeter or two. This time, an excellent epidural spread was seen.' Seconds unknown.",
    "quality": "Clean direct capture: circular field, crosshair marker, needle with extension tubing. It dates from 2011, so probably SD; resolutions unknown.",
    "licence": "YouTube licence field unknown. The uploader's site footer reads '© The Pain Source, All Rights Reserved'.",
    "reachable": "Yes. Christopher Faubel, MD, founder of thepainsource.com, gives FaubelMD.com and Twitter @FaubelMD. A related 2010 TF ESI post credits the fluoro clip to Dr. Hazem Eissa; whether that is this clip is unknown.",
    "evidence": "Legacy RSS feed (feeds/videos.xml?user=thepainsource) gave the id, date, views and a description about the importance of needle placement. The hqdefault and hq3 thumbnails were viewed. The thepainsource.com About page was read."
   },
   {
    "url": "https://www.youtube.com/watch?v=6Y2QDj_xUbQ",
    "title": "Right L5-S1 Facet Injection",
    "channel": "ThePainSource (Christopher Faubel, MD)",
    "year": "2011 (published 2011-12-15)",
    "duration": "unknown",
    "procedure": "Lumbar intra-articular facet (zygapophyseal) injection with contrast arthrogram",
    "region": "lumbosacral L5-S1; view: ipsilateral oblique",
    "views": "29,729 (RSS feed)",
    "live_fluoro": "likely yes. The feed says it 'shows contrast spreading along joint line with filling of inferior capsule', which implies a live contrast run. Seconds unknown.",
    "quality": "Direct OEC capture (OEC logo visible), zoomed in. The field shows only about 1-2 segments.",
    "licence": "YouTube licence field unknown. The site footer reads '© The Pain Source, All Rights Reserved'.",
    "reachable": "Yes: Christopher Faubel, MD (FaubelMD.com, @FaubelMD).",
    "evidence": "RSS feed entry. The hqdefault thumbnail was viewed. The thepainsource.com page 'VIDEOS: Lumbar Facet Injections under Fluoroscopy' lists this and an L4/5 facet clip; the L4/5 clip's id was not found."
   },
   {
    "url": "https://www.youtube.com/watch?v=tzYc-kMRjDc",
    "title": "Cervical Interlaminar Epidural Steroid Injection",
    "channel": "ThePainSource (Christopher Faubel, MD)",
    "year": "2011 (published 2011-12-21)",
    "duration": "unknown",
    "procedure": "Cervical interlaminar epidural steroid injection, contrast spread",
    "region": "cervicothoracic junction (about C7-T1, ribs and clavicles in frame); view: AP",
    "views": "9,798 (RSS feed)",
    "live_fluoro": "yes, a short loop. The feed says 'Contrast spread during a fluoroscopically-guided cervical interlaminar epidural steroid injection', and the on-screen caption 'Repeated 3 times' suggests a short live run replayed. Seconds unknown.",
    "quality": "Clean direct capture: circular field, crosshair marker, caption overlay.",
    "licence": "YouTube licence field unknown. The site footer reads '© The Pain Source, All Rights Reserved'.",
    "reachable": "Yes: Christopher Faubel, MD (FaubelMD.com, @FaubelMD).",
    "evidence": "RSS feed entry. The hqdefault thumbnail was viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=zKd3I3kSD3A",
    "title": "Cervical Facet Injection under Fluoroscopy",
    "channel": "ThePainSource (Christopher Faubel, MD)",
    "year": "2011 (published 2011-12-22)",
    "duration": "unknown",
    "procedure": "Right C4/5 intra-articular cervical facet injection with contrast",
    "region": "cervical (C4/5); view: lateral or oblique (not firmly established)",
    "views": "15,559 (RSS feed)",
    "live_fluoro": "likely yes. The feed says it 'illustrates contrast spread during right C4/5 intraarticular facet injection'. The thumbnail carries a still-style label, so part of it may be stills. Seconds unknown.",
    "quality": "Direct capture framed with the ThePainSource logo, a yellow label bar and arrows. The field is small and square-cropped.",
    "licence": "YouTube licence field unknown. The site footer reads '© The Pain Source, All Rights Reserved'.",
    "reachable": "Yes: Christopher Faubel, MD.",
    "evidence": "RSS feed entry. The hqdefault thumbnail was viewed ('Right C4/5 Facet Injection' label)."
   },
   {
    "url": "https://www.youtube.com/watch?v=3fhPb-ZNml4",
    "title": "Lumbar Medial Branch Block",
    "channel": "The Spine & Pain Institute of New York (@TheSpinePainInstituteofNewYork)",
    "year": "2016 (search snippet: May 2016)",
    "duration": "unknown",
    "procedure": "Lumbar medial branch block",
    "region": "lumbar / lumbosacral junction (the inset shows lower lumbar, sacrum and pelvis); view: AP",
    "views": "unknown",
    "live_fluoro": "probably yes. A picture-in-picture fluoro inset runs alongside the room camera throughout, and its content changes between the hq1, hq2 and hq3 auto-frames (C-arm or field moving). Whether the inset is live or last-image-hold is unknown.",
    "quality": "The fluoro inset is a clean feed but occupies only about 30% of the 16:9 frame, top-left. The room camera shows the C-arm. A name lower-third reads 'Kenneth B. Chapman, M.D.'",
    "licence": "unknown (YouTube licence field not readable)",
    "reachable": "Yes. The physician is named on screen (Kenneth B. Chapman, MD) and the practice is The Spine & Pain Institute of New York.",
    "evidence": "oEmbed gave the title and channel. The hq1, hq2 and hq3 thumbnails were viewed. The year comes from a search snippet. The same channel probably has sibling picture-in-picture procedure videos, but it could not be listed (channel id not found)."
   },
   {
    "url": "https://www.youtube.com/watch?v=Koq1t9RT9WM",
    "title": "Live Lumbar Transforaminal Epidural Steroid Injection for Pain Radiating Down the Leg",
    "channel": "The Kahan Center for Pain Management (channel UCUQhlYUbOQUPGkuPYIC7kxw; Brian Kahan, DO)",
    "year": "2014 (search snippet: July 2014)",
    "duration": "unknown",
    "procedure": "Lumbar transforaminal epidural steroid injection (post-fusion patient)",
    "region": "lumbar, with pedicle-screw fusion hardware in frame; view: AP",
    "views": "unknown",
    "live_fluoro": "unknown. The title says 'Live', but the sampled frames show the room camera and a camera pointed at dual Siemens monitors. The monitor may be showing stored or last-image-hold frames.",
    "quality": "Filmed monitor (camera, not direct capture), blue-tinted dual-monitor display, a glove pointing, SD-era. The fusion hardware may help with level naming.",
    "licence": "unknown (YouTube licence field not readable)",
    "reachable": "Yes. Brian Kahan, DO, The Kahan Center, 170 Jennifer Road Suite 240, Annapolis MD; public practice phone [phone withheld].",
    "evidence": "oEmbed and search snippet. The hqdefault, hq2 and hq3 thumbnails were viewed: room footage, then filmed monitors. The practice homepage gives the channel id and contact."
   },
   {
    "url": "https://www.youtube.com/watch?v=RIxoyni0cKM",
    "title": "Fluoroscopic Guided Caudal Epidural Injection",
    "channel": "Dr. Vinay Kumar Singh (@DrVinayKumarSingh)",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "Caudal epidural injection",
    "region": "sacrum / sacral hiatus; view: lateral",
    "views": "unknown (the thumbnail itself claims '30K+ views')",
    "live_fluoro": "unknown. The hq2 frame shows the fluoro monitor with a gloved finger pointing; whether the monitor image is live is not established.",
    "quality": "Phone-filmed monitor with a glare-free but perspective-skewed circular field. Thumbnail text overlays. Only the sacrum is visible, not the lumbar vertebrae.",
    "licence": "unknown",
    "reachable": "Named physician; no contact route established.",
    "evidence": "oEmbed. The hqdefault and hq2 thumbnails were viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=xmwqcnN_r3g",
    "title": "Intra-Articular Injection of the Sacroiliac Joint Under Fluoroscopic Guidance",
    "channel": "JBJSmedia (@JBJSmedia)",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "Sacroiliac joint intra-articular injection with contrast",
    "region": "pelvis / sacroiliac joint (inferior sacrum only; no lumbar vertebrae expected); view: AP with cephalad tilt or oblique",
    "views": "unknown",
    "live_fluoro": "unknown. A filmed OEC monitor is visible in the thumbnail.",
    "quality": "A camera filming the OEC monitor (blue-tint display, second monitor at the edge). Low value for vertebra naming.",
    "licence": "unknown (journal media channel; likely publisher copyright, not verified)",
    "reachable": "Yes, through the publisher (Journal of Bone & Joint Surgery); an individual author was not identified.",
    "evidence": "oEmbed and a search snippet (JBJS JOPA instructional video). The hqdefault thumbnail was viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=GlyxEYCFTvE",
    "title": "caudal epidural steroids injection (fluoroscopy)-step by step",
    "channel": "mohamed al jazzar (@mohamedaljazzar8487)",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "Caudal epidural steroid injection",
    "region": "sacrum; view unknown",
    "views": "unknown",
    "live_fluoro": "unknown. The hq2 frame is a phone video of the room with the fluoro monitor small in frame (part pixelated).",
    "quality": "Phone-filmed room; the monitor occupies a small part of the frame. Poor for tracking.",
    "licence": "unknown",
    "reachable": "Individual uploader; no contact route established.",
    "evidence": "oEmbed. The hqdefault (needle at skin, caption) and hq2 thumbnails were viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=tIewz4w-Y24",
    "title": "Lumbar Stick it 2 Me transforaminal demonstration",
    "channel": "The Kahan Center for Pain Management (Brian Kahan, DO)",
    "year": "2023 (published 2023-04-26)",
    "duration": "unknown",
    "procedure": "Lumbar transforaminal injection on a PHANTOM (Stick-It-2-Me biodegradable spine training model), not a patient",
    "region": "lumbar phantom (3 vertebrae visible); view: oblique",
    "views": "1,078 (RSS feed)",
    "live_fluoro": "The feed describes it as a 'live demonstration'. The frames are a split screen of a filmed fluoro monitor and the presenter. Seconds unknown.",
    "quality": "Filmed monitor on half of a split screen. Burned-in on-screen text 'All Rights reserved' and a course-registration URL. The anatomy is a phantom.",
    "licence": "On-screen text: 'All Rights reserved'. YouTube licence field unknown.",
    "reachable": "Yes: Brian Kahan, DO, Annapolis MD (practice phone [phone withheld]).",
    "evidence": "Channel RSS feed and the hq2 thumbnail. A sibling cervical phantom video, qEOEx-rUkk4 ('Stick It 2 Me Cervical transforaminal demonstration', 2023-04-28, 8,991 views), shows an AP cervical phantom in the same format."
   }
  ],
  "notes": "Short answer: YouTube has a small amount of usable material for this angle. I found 9 clips that are genuine continuous-fluoroscopy recordings of spinal injections, captured directly from the C-arm. Five come from The Procedure Guide and four from ThePainSource. Neither uploader showed any other candidates. Each clip holds only a few seconds of live fluoroscopy: The Procedure Guide's OEC fluoro-time counters read 0.1-0.4 min for the whole case. The views are mostly one level, tightly collimated, and often have text cards cut in between. They could serve as a small qualitative temporal check, not a test set. The better use is to ask these uploaders for the original cine or DICOM.\n\nMethod and limits:\n- WebSearch ran out after about 20 queries: the session-wide cap of 200 had been reached by other workers. I did not try to get around it.\n- YouTube watch pages do not render through WebFetch (only the footer comes back). So for every candidate, the duration, the licence line and the resolutions offered are unknown.\n- Fields came from four official routes instead:\n  1. YouTube oEmbed, for title and channel.\n  2. Public channel RSS feeds (feeds/videos.xml) for three channels, giving date, description and views.\n  3. YouTube's auto-generated thumbnails (hqdefault and the hq1, hq2, hq3 frames), fetched and viewed as single JPEGs. No video was downloaded and no scraper was used.\n  4. The uploaders' own websites, for licence and contact details.\n\nLicence findings:\n- theprocedureguide.com states 'Everything on the site is under a creative commons license (CC BY-NC-SA 4.0)'. It is the only uploader with an open licence statement. Whether that covers their YouTube uploads is not confirmed.\n- ThePainSource's site footer says '© The Pain Source, All Rights Reserved'.\n- The Kahan phantom videos burn 'All Rights reserved' into the frame.\n\nCaveats:\n- 4q8LjcE0vsI and KXz2k8lOt9U are the same patient and session: the OEC clocks read 9:14-9:17 AM and the dose accumulates across them. Do not count them as independent cases.\n- No thoracic or spinal-cord-stimulator live-fluoro video was found before the search budget ran out.\n- Pain Clinic of India (channel UCKC735rN_yaT9Jfkew3R4AA) has a cervical SCS video (xdIMpzVBsVU, 2026) and a cervical epidural video (tgxBsf2-ywo). The sampled frames of both show only room or phone footage, so I did not list them.\n\nExcluded after viewing thumbnails:\n- Slideshows of saved stills: The Procedure Guide's 'quick guide' series (u_DutJTkG-g, XEghDFgjCjI, PFEYX4Ah-V4, 1jZyZ9zcPuw, s17tb5MFci4).\n- 1oSMo9l11p0 (Dr Sanjeeva Gupta): a recorded Zoom lecture with stills.\n- 4BG6LA9iS5Y and iA1I1p9ezxw (Dr Kailash Kothari): room camera with subtitles.\n- mwHn0oND06A (Sound Pain Alliance RFA): room camera with the C-arm monitor small in the background.\n- K7J-uiy2sgI (Dr Ashraf Hanna): talking head.\n- v5f5d2dxy4o ('Cervical Medial Branch – Fluoroscopy'): oEmbed returned 403 and the thumbnail 404, so it is probably private or removed.\n- RRepKwdvHac (RAYUS discogram): patient education; not checked further.\n- Radiopaedia case rID 87287 (Dai Roberts, TFESI): appears to be stills, not cine.\n- The PMC case report PMC11650285 (live-fluoro arterial uptake, CC BY): has no video supplement.\n\nWho to contact:\n1. Rohit Puranik, MD, via the contact form at theprocedureguide.com/contact. The licence is already open, the captures are clean OEC captures, and there are lumbar AP and lateral, caudal and cervical clips.\n2. Christopher Faubel, MD (FaubelMD.com). Older 2010 clips, such as the L4 TF ESI credited to Dr Hazem Eissa and an L4/5 facet clip, exist on thepainsource.com, but I could not get their YouTube ids.\n3. Kenneth B. Chapman, MD (The Spine & Pain Institute of New York). His picture-in-picture videos show the lumbosacral junction on AP. The channel could not be listed.",
  "verify": [
   {
    "url": "https://www.youtube.com/watch?v=4q8LjcE0vsI",
    "confirmed_live_fluoro": "Not observed. The title claims 'live contrast spread', but all three of YouTube's auto-frames (about 25/50/75% through) are held images: the OEC dose rate reads 0.00 mGy/min in each. Two are the AP frame at 9:14:56 AM; one is a blurry lateral at 9:15:23 AM. The rendered watch page lists key moments at 0:01, 0:09 ('Contrast spread extends medial but isn't quite right'), 0:20 ('A lateral view shows the problem') and 0:29, so the video runs about 30 s or more. Any live run is probably inside 0:09-0:20 and lasts a few seconds.",
    "confirmed_licence": "YouTube licence field: unknown. The rendered watch page showed no 'Creative Commons' line; the description was truncated, so that absence is not conclusive. The uploader's site (theprocedureguide.com, verified) says 'Everything on the site is under a creative commons license (CC BY-NC-SA 4.0)'. It does not say whether that covers the YouTube uploads. The NonCommercial term would block commercial use.",
    "confirmed_views": "AP lumbar (about 3 vertebrae plus the sacral ala region; the text overlay reads 'Good needle placement on AP for L3 TF') and lateral lumbar (blurry, low contrast). 13,230 views on the watch page; published 2021-03-25.",
    "usable_for_tracking": "possible",
    "corrections": "The recorded description fits, but the live run is unconfirmed: every sampled frame is last-image-hold (0.00 mGy/min). The upload is HD, since a 1280x720 maxresdefault exists. The same patient and session as KXz2k8lOt9U is confirmed (03/25/2021; clocks 9:14:56, 9:15:23 and 9:17:02). Its value is as a same-patient pair: AP and lateral stills plus KXz2's live AP run. General caveat for every injection video here: the C-arm is stationary during live runs, so the vertebrae barely move. That tests how stable level naming stays under noise, contrast and needle motion, not tracking under C-arm translation. Method note: the WebSearch budget was exhausted (200/200), so nothing new was searched. Checks used the channel RSS, oEmbed, YouTube's own thumbnail frames, and a rendered copy of each watch page (r.jina.ai page reader). The raw watch page returns no metadata to WebFetch. Duration is not shown anywhere."
   },
   {
    "url": "https://www.youtube.com/watch?v=KXz2k8lOt9U",
    "confirmed_live_fluoro": "Yes, at one sampled point. The 25% auto-frame is an AP exposure in progress: OEC dose rate 4.24 mGy/min, cumulative 0.4 min / 1.79 mGy, clock 9:17:02 AM, with motion blur and contrast at the foramen. The 50% and 75% frames are grey text cards ('Needle on transverse process, then advanced inferior/posterior. Live contrast injection without vascular uptake.' and 'TheProcedureGuide.com Transforaminal Epidural Contrast Spread'). The live footage is therefore short, likely less than half of a short video. Seconds unknown.",
    "confirmed_licence": "YouTube licence field: unknown; the rendered watch page listed no licence line. The uploader's site states CC BY-NC-SA 4.0 for 'Everything on the site' (verified); whether that covers the YouTube upload is not stated.",
    "confirmed_views": "AP lumbar, about 3 full vertebrae plus a partial one, needle entering from the lower right. No clear obliquity. 7,107 views; published 2021-03-25.",
    "usable_for_tracking": "possible",
    "corrections": "Live exposure is confirmed by a non-zero dose-rate readout, which the earlier record lacked. Much of the runtime is text cards, not the 'few seconds of live' implied earlier. HD: 1280x720 auto-frames exist. The only direct-capture lumbar clip in this set with a confirmed live frame and several whole vertebrae. The C-arm is static, so frame-to-frame motion comes only from blur and contrast. Reachable: contact form at theprocedureguide.com/contact (verified); founder and primary editor Rohit Puranik, MD (team page verified)."
   },
   {
    "url": "https://www.youtube.com/watch?v=6MBj9SBZrno",
    "confirmed_live_fluoro": "Yes, briefly. The 25% auto-frame is live (6.04 mGy/min, cumulative 0.1 min / 0.62 mGy, clock 12:52:27 PM, overlay date 03/30/2021). The 50% frame is a title card ('Lateral lumbar epidural contrast spread under fluorscopy') and the 75% frame is a blank grey card. The live portion is a small fraction of the video.",
    "confirmed_licence": "YouTube licence field: unknown; the rendered watch page showed no licence line. The site states CC BY-NC-SA 4.0 (applies to the site; YouTube coverage unstated).",
    "confirmed_views": "Lateral only. Heavily washed out, with an octagonal collimator inside a circular field. Vertebral bodies are barely discernible; the region cannot be confirmed as lumbar from the image. 4,979 views; published 2021-04-09.",
    "usable_for_tracking": "poor",
    "corrections": "The overlay date (03/30/2021) is earlier than the upload date. Most of the runtime is cards. Image quality is too low to name levels: vertebral outlines cannot be picked out in the sampled live frame."
   },
   {
    "url": "https://www.youtube.com/watch?v=DCLd6DsoUSg",
    "confirmed_live_fluoro": "Yes. The 50% auto-frame shows the OEC 'LIVE' indicator at 3.68 mGy/min, clock 10:15:29 AM, with contrast ascending the canal. The 75% frame has the same clock at 0.00 mGy/min (held after the run). The 25% frame is a held lateral at 10:14:43 AM (0.00 mGy/min). The live run lasts seconds.",
    "confirmed_licence": "YouTube licence field: unknown; the rendered watch page showed no licence line. The site states CC BY-NC-SA 4.0 (site-level; YouTube coverage unstated).",
    "confirmed_views": "Lateral sacrum and sacral hiatus with needle (held), and an AP collimated vertical strip over the sacrum and lower lumbar with the contrast column (live). 13,650 views; published 2021-05-11.",
    "usable_for_tracking": "poor",
    "corrections": "The view is now established: a lateral held image plus an AP live run. The earlier record left the view open. In the AP strip, bowel gas and a narrow collimation obscure the vertebral bodies; no lumbar body is cleanly delineated. HD."
   },
   {
    "url": "https://www.youtube.com/watch?v=1eFLBwOtgGU",
    "confirmed_live_fluoro": "Yes, briefly. The 75% auto-frame is live (2.25 mGy/min, cumulative 0.4 min / 0.89 mGy). The 25% and 50% frames are text cards ('Anesthetize and use that needle to map trajectory / Advance Tuohy...' and 'Inject contrast under live fluoro / Confirm epidural spread...'). The description reads 'Highlight images and video', so it mixes stills and video. Seconds unknown.",
    "confirmed_licence": "YouTube licence field: unknown; the rendered watch page showed no licence line. The site states CC BY-NC-SA 4.0 (site-level).",
    "confirmed_views": "Lateral cervical/cervicothoracic, displayed rotated about 90 degrees (spine horizontal; the patient is sitting per the linked article). Spinous processes are visible; the vertebral bodies are largely hidden by shoulder density. 8,516 views; published 2021-03-30.",
    "usable_for_tracking": "poor",
    "corrections": "The view is now established as lateral, rotated about 90 degrees on screen. Heavy exposure gradient and shoulder overlap. Cards dominate the sampled frames."
   },
   {
    "url": "https://www.youtube.com/watch?v=CTyIu-EGby8",
    "confirmed_live_fluoro": "Unknown. The auto-frames are a title card at 25% ('Lumbar Neurogram to Epidural with an Extra Millimeter'), an AP lumbar frame with contrast at 50%, and a text card at 75% ('Next, the needle was advanced another millimeter or two. This time, an excellent epidural spread was seen.'). There is no dose-rate or LIVE overlay, so live and stored frames cannot be told apart. The description describes contrast being injected twice, which implies but does not prove live runs.",
    "confirmed_licence": "YouTube licence field: unknown; the rendered watch page showed no licence line. The uploader's site footer reads '© The Pain Source, All Rights Reserved' (verified on thepainsource.com/about).",
    "confirmed_views": "AP lumbar, 3-4 vertebrae in a clean circular field with a crosshair marker. The needle and extension tubing enter from the right. 9,895 views; the watch page gives 2011-12-28 (RSS 2011-12-29 UTC).",
    "usable_for_tracking": "possible",
    "corrections": "The full title is 'Lumbar Transforaminal Epidural - Neurogram to Epidural with an Extra Millimeter - ThePainSource.com'. HD, not SD as guessed: the maxresdefault is 1280x720. It is a clean direct capture with good bone detail and several whole vertebrae. It is rated 'possible' only if the contrast segments turn out to be live runs, which is not established. Reachable: Christopher Faubel, MD via FaubelMD.com; @thepainsource on Twitter/Facebook (verified)."
   },
   {
    "url": "https://www.youtube.com/watch?v=6Y2QDj_xUbQ",
    "confirmed_live_fluoro": "Yes, likely. The 25% auto-frame is a card reading 'Full speed and replayed 3 times', which indicates one real-time live clip looped three times. The 50% frame is the fluoro run and the 75% frame is a zoomed crop of the facet (OEC logo visible). Seconds unknown; probably a few seconds, repeated.",
    "confirmed_licence": "YouTube licence field: unknown; the rendered watch page showed no licence line. The site footer reads '© The Pain Source, All Rights Reserved'.",
    "confirmed_views": "Ipsilateral oblique lumbosacral. The 50% frame shows about 3-4 lumbar segments down to the L5-S1 facet with contrast, plus a crosshair. 29,729-29,730 views; published 2011-12-15.",
    "usable_for_tracking": "possible",
    "corrections": "The full title is 'Right L5-S1 facet injection under fluoroscopic guidance - ThePainSource.com'. The field is wider than recorded: the 50% frame shows about 3-4 segments, not 1-2 (only the later zoomed crop shows 1-2). SD only: maxresdefault returns 404. The oblique view and the looped short clip limit it; the C-arm is static."
   },
   {
    "url": "https://www.youtube.com/watch?v=tzYc-kMRjDc",
    "confirmed_live_fluoro": "Yes, a short loop. The hqdefault and 50% frames show the same C-arm position with a different amount of contrast; both carry the caption 'Repeated 3 times', and the 25% frame is a 'Repeated 3 times' card. The 75% frame is an annotated 'Post Injection Image' still with yellow callouts. Seconds unknown.",
    "confirmed_licence": "YouTube licence field: unknown; the rendered watch page showed no licence line. The site footer reads '© The Pain Source, All Rights Reserved'.",
    "confirmed_views": "AP of the cervicothoracic junction (about C7-T2, with ribs and clavicles in frame), crosshair marker. 9,798 views; published 2011-12-21.",
    "usable_for_tracking": "possible",
    "corrections": "Confirmed as recorded. A large burned-in caption ('Repeated 3 times') covers the lower third of the fluoro during the loop, and the region is the cervicothoracic junction, not the lumbar spine. The loop is short, repeated, and taken with a static C-arm. Resolution beyond 480x360 was not checked."
   },
   {
    "url": "https://www.youtube.com/watch?v=zKd3I3kSD3A",
    "confirmed_live_fluoro": "Yes, likely. The 25% and 50% auto-frames show an identical C-arm position with the contrast column in the facet growing between them, consistent with a live contrast run. The 75% frame is a ThePainSource logo end card. Seconds unknown.",
    "confirmed_licence": "YouTube licence field: unknown (the rendered watch page returned a 401 error). The site footer reads '© The Pain Source, All Rights Reserved'.",
    "confirmed_views": "Lateral or oblique cervical (not firmly established), heavily magnified. Only about 1-2 segments are identifiable in a small circular field with '3C' and GE OEC logo overlays. 15,559 views (RSS); published 2011-12-22.",
    "usable_for_tracking": "poor",
    "corrections": "The full title is 'Cervical Facet Injection under fluoroscopy - ThePainSource.com'. Live is supported by the growth of contrast between frames. The field is too small, and too few vertebrae are visible, to name levels. The label-bar thumbnail is a custom thumbnail, not the video body."
   },
   {
    "url": "https://www.youtube.com/watch?v=3fhPb-ZNml4",
    "confirmed_live_fluoro": "Unknown. The fluoro sits in a picture-in-picture inset whose content changes between auto-frames. The inset time labels read '(13:51)', '(13:55)' and '(13:56)' at 25/50/75%, so the edit spans several minutes of the procedure. The field shifts between lumbosacral and higher lumbar. Whether the inset is continuous live video or a sequence of held images cannot be established.",
    "confirmed_licence": "YouTube licence field: unknown; the rendered watch page showed no licence line. No licence stated in the description.",
    "confirmed_views": "AP lumbar/lumbosacral in the inset. 285,532 views; published 2016-05-06.",
    "usable_for_tracking": "poor",
    "corrections": "The views and year are now established (285,532; May 6, 2016). HD 1280x720 overall, but the inset is only about 375x360 px, with a fluoro circle about 340 px across, at top-left. The rest of the frame is room camera. The inset looks like a rescaled monitor feed. The physician's name 'Kenneth B. Chapman, M.D.' is confirmed on screen. The description is a practice advertisement (offices in Manhattan, Staten Island, Brooklyn, the Bronx and Long Island), so the practice is reachable."
   },
   {
    "url": "https://www.youtube.com/watch?v=Koq1t9RT9WM",
    "confirmed_live_fluoro": "Unknown. The 25% and 50% auto-frames are room-camera close-ups of needle insertion through the drape. The 75% frame is a camera filming two blue-tinted Siemens monitors that show near-identical AP lumbar images with pedicle screws (monitor date 07.03.14), with a gloved finger pointing. Nothing indicates a live exposure.",
    "confirmed_licence": "YouTube licence field: unknown; the rendered watch page showed no licence line. The description reads only 'Looking for more information please visit our website at www.thekahancenter.com'.",
    "confirmed_views": "AP lumbar with fusion hardware, filmed off the monitor. 890,995 views; published 2014-07-31.",
    "usable_for_tracking": "poor",
    "corrections": "The views are now established (890,995; July 31, 2014). An HD 1280x720 thumbnail exists, but the fluoro is a camera recording of a monitor with blue tint and perspective. Most sampled frames are room footage. Privacy caution: the patient's head and hair are visible in the thumbnail, and the monitor carries facility text."
   },
   {
    "url": "https://www.youtube.com/watch?v=RIxoyni0cKM",
    "confirmed_live_fluoro": "Unknown, and doubtful. The 25% frame is the room with the physician lecturing, the monitor small in frame. The 50% frame is a phone-filmed monitor with a gloved finger over a faint lateral sacral image. The 75% frame is an animated logo. Watch-page chapters run to 5:41, so the video is about 6 min or more, mostly room and lecture.",
    "confirmed_licence": "YouTube licence field: unknown; the rendered watch page showed no licence line.",
    "confirmed_views": "Lateral sacrum (sacral hiatus); no lumbar vertebrae seen. 60,291 views; published 2022-09-02.",
    "usable_for_tracking": "not",
    "corrections": "The year and views are now established. The page's own view count is 60,291; the thumbnail's '30K+' was out of date. The fluoro content is a filmed monitor occluded by a hand. Not usable for vertebra tracking."
   },
   {
    "url": "https://www.youtube.com/watch?v=xmwqcnN_r3g",
    "confirmed_live_fluoro": "Not observed. All three auto-frames are a handheld camera filming OEC monitors; the dose rate reads 0.00 mGy/min (held images) where legible. Chapters (0:00, 1:18, 2:48, 3:30) put the video at about 4 min.",
    "confirmed_licence": "YouTube licence field: unknown; the rendered watch page showed no licence line. It is JBJS JOPA journal content, so publisher copyright is likely but was not verified.",
    "confirmed_views": "AP/oblique pelvis centred on the sacroiliac joint; no lumbar vertebrae. 46,126 views; published 2022-06-30.",
    "usable_for_tracking": "not",
    "corrections": "The year and views are now established. It is a filmed monitor of the SI joint only, with no vertebrae to track. Drop it."
   },
   {
    "url": "https://www.youtube.com/watch?v=GlyxEYCFTvE",
    "confirmed_live_fluoro": "Unknown. The 25% frame is a black text card ('2- Advance the needle targeting the sacral hiatus...'). The 50% frame is a phone video of the room with the monitor small and the patient info pixelated. The 75% frame is a phone close-up of the monitor in portrait crop with severe moire.",
    "confirmed_licence": "YouTube licence field: unknown; the rendered watch page showed no licence line.",
    "confirmed_views": "Sacrum (view not determinable). 10,191 views; published 2022-10-04.",
    "usable_for_tracking": "not",
    "corrections": "The year and views are now established. Moire and the portrait phone crop make it unusable."
   },
   {
    "url": "https://www.youtube.com/watch?v=tIewz4w-Y24",
    "confirmed_live_fluoro": "Not observed. It is a split screen: the left half films a Siemens monitor labelled 'LIH 1' (last image hold), the right half is the room camera. Cumulative dose rises 0.3 -> 8.4 -> 13.5 mGy across the 25/50/75% frames, so exposures happen between the samples, but each sampled monitor image is a held frame.",
    "confirmed_licence": "YouTube licence field: unknown; the rendered watch page showed no licence line. Burned-in on-screen text reads 'All Rights reserved'.",
    "confirmed_views": "AP (25%), oblique (50%) and lateral (75%) of a phantom lumbar spine: about 3 vertebrae plus the sacrum, bone-only, with high contrast. 1,078 views; premiered 2023-04-26.",
    "usable_for_tracking": "poor",
    "corrections": "The views were wrong: it progresses AP to oblique to lateral, not oblique only. The anatomy is a phantom (Stick-It-2-Me), not a patient. The fluoro is a filmed monitor about 300 px across on half of a 1280x720 frame, under course-registration and order-email overlays. A reachable email is burned in: [e-mail withheld]. It is interesting as one spine seen across three C-arm angles, but no live run is confirmed."
   }
  ]
 },
 {
  "angle": "scs",
  "candidates": [
   {
    "url": "https://www.youtube.com/watch?v=-rWuzfYkd5M",
    "title": "Spinal Cord Stimulator Trial",
    "channel": "The Spine & Pain Institute of New York (@TheSpinePainInstituteofNewYork)",
    "year": "2017 (search snippet: posted May 25, 2017)",
    "duration": "unknown",
    "procedure": "Percutaneous spinal cord stimulator trial on a real patient (Dr. Kenneth B. Chapman), with on-screen subtitles giving clinical pearls",
    "region": "Not stated. Standard SCS trials use lumbar needle entry and thoracic lead tips (T8-T10), so probably thoracolumbar, but the page does not confirm it.",
    "views": "unknown",
    "live_fluoro": "unknown. It is a real-patient procedure video, which makes fluoroscopy likely, but seconds and views could not be checked.",
    "licence": "unknown (the watch page could not be read)",
    "quality": "unknown",
    "reachable": "Yes. It is a named practice with a named physician: The Spine & Pain Institute of New York, 860 Fifth Ave, New York NY 10065, tel. [phone withheld] (spinepainny.com). Dr. Chapman teaches residents and fellows.",
    "evidence": "YouTube oEmbed via noembed.com returned the title and channel, so embedding is allowed. The search-result snippet reads: 'Dr. Chapman performs a spinal cord stimulator trial on a patient, with subtitles on clinical pearls for residents, fellows, and anyone that wants to learn'. The date comes from the search snippet. Contact details come from spinepainny.com/scs/. The same channel also has 0ZRJ-IuFS7k, 'How DRG stimulation at T12 reveals the transmission of low back pain in the spinal cord: The theory', which is probably a lecture and was not verified."
   },
   {
    "url": "https://www.youtube.com/watch?v=Yme7AxnIRWI",
    "title": "Live Demonstration – Lumbar Spinal Cord Stimulation Trial Brett Stacey, M.D.",
    "channel": "Seattle Science Foundation (from search snippet; oEmbed refused)",
    "year": "2017 (search snippet: November 17, 2017)",
    "duration": "unknown",
    "procedure": "Live teaching demonstration of a percutaneous SCS trial (Brett R. Stacey MD, UW Center for Pain Relief)",
    "region": "The title says 'lumbar' SCS trial, which usually means lumbar entry with the lead run up to the lower thoracic spine. Lead-tip level not established.",
    "views": "unknown",
    "live_fluoro": "unknown. A 'Live Demonstration' title suggests unedited procedure footage, possibly including the C-arm monitor. Not verified.",
    "licence": "unknown (the watch page could not be read)",
    "quality": "unknown",
    "reachable": "Yes. Seattle Science Foundation is a non-profit physician-education organisation, and Dr. Stacey is Professor of Anesthesiology & Pain Medicine at the University of Washington (anesthesiology.uw.edu).",
    "evidence": "The title and URL come from WebSearch results. Both noembed.com and youtube.com/oembed returned HTTP 401, which usually means the uploader disabled embedding (the video is still watchable on YouTube). The date and uploader come from the search summary. The same search found related Stacey/SSF titles: 7XcQTaN70aM 'Spinal Cord Stimulation: Trial - Brett R. Stacey' and _dJkuD8xyDU 'Spinal Cord Stimulation Procedure Trial Overview - Brett Stacey, MD'; both also return oEmbed 401 and are probably lectures."
   },
   {
    "url": "https://www.youtube.com/watch?v=Vluvyif1mBg",
    "title": "Spinal Cord Stimulation Trial Procedure - Jennifer Lee, M.D.",
    "channel": "Seattle Science Foundation (per search summary)",
    "year": "2022 (search summary: November 17, 2022)",
    "duration": "unknown",
    "procedure": "SCS trial procedure (Jennifer Lee MD, Texas Pain & Spine Institute, Amarillo)",
    "region": "unknown (a standard trial would be thoracolumbar)",
    "views": "unknown",
    "live_fluoro": "unknown. It is a real procedure video (a Facebook copy says 'procedure content contains video of a ... stimulator implant trial'), but the fluoroscopy content is not verified.",
    "licence": "unknown (the watch page could not be read)",
    "quality": "unknown",
    "reachable": "Yes. Acute & Chronic Pain And Spine Center / Texas Pain & Spine Institute, Amarillo, tel. [phone withheld] (from the Facebook page). SSF can also be contacted.",
    "evidence": "The title comes from WebSearch. oEmbed returned 401 (embedding disabled). The same procedure is also posted on Facebook by GotPainTexas: https://www.facebook.com/GotPainTexas/videos/procedure-content-contains-video-of-a-non-invasive-stimulator-implant-trial-stim/771817187444841/ (the fetched page describes a 'trial stimulator placed prior to permanent spinal column device', with no fluoroscopy mention and no duration)."
   },
   {
    "url": "https://www.youtube.com/watch?v=RrRN6GMkkEQ",
    "title": "LAB DEMO: Spinal Cord Stimulation Procedure- Jennifer Lee, M.D.",
    "channel": "Seattle Science Foundation (per search summary)",
    "year": "2021 (search summary: November 18, 2021)",
    "duration": "unknown",
    "procedure": "SCS procedure lab demonstration, probably in a cadaver lab. SSF runs cadaver labs, but this video is not verified.",
    "region": "unknown",
    "views": "unknown",
    "live_fluoro": "unknown. Lab demos of SCS usually run the C-arm continuously while the lead is steered; not verified.",
    "licence": "unknown (the watch page could not be read)",
    "quality": "unknown",
    "reachable": "Yes. Seattle Science Foundation (non-profit) or Dr. Jennifer Lee (Texas Pain & Spine Institute, [phone withheld]).",
    "evidence": "The title and date come from WebSearch results and summary. oEmbed returned 401 (embedding disabled). If it is a cadaver, patient-privacy barriers to permission are lower."
   },
   {
    "url": "https://www.youtube.com/watch?v=ot_gIGZdUWw",
    "title": "Spinal Cord Stimulation Procedure Boston Scientific - Brett Stacy, MD",
    "channel": "Seattle Science Foundation (inferred from the Stacey/SSF result cluster; oEmbed refused)",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "SCS procedure demonstration with Boston Scientific hardware",
    "region": "unknown",
    "views": "unknown",
    "live_fluoro": "unknown",
    "licence": "unknown (the watch page could not be read)",
    "quality": "unknown",
    "reachable": "Yes (Seattle Science Foundation / UW Anesthesiology & Pain Medicine)",
    "evidence": "The title comes from WebSearch; it appeared in results for the SSF 'Live Demonstration' query. noembed returned 401 (embedding disabled). The title does not show whether this is live procedure footage or a talk."
   },
   {
    "url": "https://www.youtube.com/watch?v=C1e84KmcjRs",
    "title": "Watch A Lumbar Spinal Cord Stimulator Trial With Nevro SCS Device | Arizona Pain",
    "channel": "Arizona Pain (@ArizonaPain)",
    "year": "2022 (search summary: May 28, 2022)",
    "duration": "unknown",
    "procedure": "Lumbar SCS trial implant, Nevro device (Dr. Paul Lynch), in a patient with pain after back surgery",
    "region": "The title says lumbar. A Nevro 10 kHz trial usually puts lead tips at T8-T11, so thoracolumbar is likely but not established.",
    "views": "unknown",
    "live_fluoro": "unknown. It is a real-patient procedure video; the fluoroscopy content is not verified.",
    "licence": "unknown (the watch page could not be read)",
    "quality": "unknown",
    "reachable": "Yes. Arizona Pain is a named practice (Phoenix area), and Dr. Paul Lynch is a named physician.",
    "evidence": "noembed returned the title and channel (embedding allowed). The search summary says 'Dr. Paul Lynch at Arizona Pain performs a lumbar spinal cord stimulator trial implant procedure for his patient with pain after back surgery'. Of all candidates, the Arizona Pain channel is the one most likely to hold further procedure videos, but it was not enumerated (the channel page cannot be read)."
   },
   {
    "url": "https://www.youtube.com/watch?v=jAgMZcy-MEw",
    "title": "Dr. Georgios Matis - Neuromodulation - Spinal cord stimulation - Percutaneous lead placement",
    "channel": "Georgios Matis - Neuromodulation (@georgiosmatis-neuromodulation)",
    "year": "2022 (search summary: May 2, 2022)",
    "duration": "unknown",
    "procedure": "Percutaneous SCS lead placement (neurosurgeon Georgios Matis, Germany)",
    "region": "unknown (probably thoracic lead placement)",
    "views": "unknown",
    "live_fluoro": "unknown",
    "licence": "unknown (the watch page could not be read)",
    "quality": "unknown",
    "reachable": "Yes. Named neurosurgeon with a dedicated educational neuromodulation channel.",
    "evidence": "oEmbed (youtube.com/oembed and noembed) returned the title and channel; embedding allowed. One search summary called it 'a Medtronic video showing placement of SCS percutaneous leads'; that is unverified. Sibling videos on the channel are device-preparation clips (PPTiSgorrck 'Preparing the Infinion CX lead', orRrr-DQZNE 'Preparing the BSC Entrada needle') and talks, which are probably not fluoroscopy."
   },
   {
    "url": "https://www.youtube.com/watch?v=_1xMxFZa6tU",
    "title": "Dorsal root ganglion stimulation for treatment of complex regional pain syndrome of the foot",
    "channel": "American Association of Neurological Surgeons (@AANSNeurosurgery)",
    "year": "2020 (Neurosurgical Focus: Video vol 3 issue 2)",
    "duration": "unknown (not stated in article)",
    "procedure": "Operative video of DRG stimulator lead placement (low lumbar/sacral DRG) for CRPS of the foot, Thomas Jefferson University (Hines, Al Saiegh, Mahtabfar, Keppetipola, Matias, Wu, Sharan)",
    "region": "lumbar / sacrum (low lumbar and sacral DRG levels)",
    "views": "unknown",
    "live_fluoro": "unknown. The article text describes fluoroscopic visualisation ('fluoroscopic visualization of the lowest levels while maximally opening the interlaminar spaces'), but the page does not say whether the video shows cine or stills.",
    "licence": "Article states: '© 2020 The Authors. This is an open access article distributed under the CC BY-NC-ND license (http://creativecommons.org/licenses/by/4.0/)'. The linked URL is CC BY, which contradicts the stated NC-ND, so the terms are ambiguous. The YouTube page's own licence is unknown.",
    "quality": "unknown; journal-produced operative video, likely edited",
    "reachable": "Yes. Corresponding author [e-mail withheld]; Dept of Neurosurgery, Thomas Jefferson University.",
    "evidence": "PMC9542308 (fetched) gives the abstract, the youtu.be/_1xMxFZa6tU link, the fluoroscopy quote and the licence line. noembed confirms the title and the AANS channel."
   },
   {
    "url": "https://drhatgis.com/procedure-videos",
    "title": "Procedure Videos (Lumbar SCS Trial; Lumbar SCS Permanent Implant; Cervical SCS Trial; DRG Stimulator Trial)",
    "channel": "Dr. Jesse Hatgis, DO (Interventional Spine, Tamarac FL)",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "Four neuromodulation procedures: lumbar SCS trial ('Watch as we perform a lumbar spinal cord stimulator (SCS) trial on a middle-aged female with chronic back and thigh pain'), lumbar SCS permanent implant, cervical SCS trial ('placement of two leads in the cervical epidural space'), and DRG stimulator trial",
    "region": "thoracolumbar (lumbar SCS trial and implant), cervical (cervical SCS trial), lumbar (DRG)",
    "views": "unknown",
    "live_fluoro": "unknown. The descriptions say 'watch as we perform' (real procedures), but fluoroscopy is not mentioned.",
    "licence": "unknown (no licence stated on page)",
    "quality": "unknown; the video host (YouTube, Vimeo, Instagram or other) could not be identified from the fetched page",
    "reachable": "Yes. [e-mail withheld], tel. [phone withheld], 7171 N University Dr Suite 300, Tamarac FL 33321.",
    "evidence": "The page was fetched twice; the quoted descriptions are verbatim. The fetched HTML contained no iframe or video URL, so the players are probably loaded by script. This is the only source found with a named cervical SCS lead placement."
   },
   {
    "url": "https://www.youtube.com/watch?v=BEEuLT764zo",
    "title": "Spinal Cord Stimulator Placement",
    "channel": "Summit Medical Institute (@summitmedicalinstitute)",
    "year": "2022 (search summary: January 19, 2022)",
    "duration": "unknown",
    "procedure": "SCS placement, neurosurgeon John R. Edwards MD (Summit Brain, Spine & Orthopedics, Lehi, Utah)",
    "region": "unknown",
    "views": "unknown",
    "live_fluoro": "unknown",
    "licence": "unknown (the watch page could not be read)",
    "quality": "unknown",
    "reachable": "Yes. Summit Brain, Spine and Orthopedics, Lehi UT, tel. [phone withheld]; named surgeon.",
    "evidence": "noembed returned the title and channel (embedding allowed). The surgeon and date come from the search summary. It is unclear whether this is procedure footage or an explanatory talk."
   },
   {
    "url": "https://www.youtube.com/watch?v=2S9IZkC8xvQ",
    "title": "Spinal Cord Stimulator Implant",
    "channel": "blueridgeorthopaedic (@blueridgeorthopaedicnova)",
    "year": "2012 (search summary: April 8, 2012)",
    "duration": "unknown",
    "procedure": "SCS implant procedure",
    "region": "unknown",
    "views": "unknown",
    "live_fluoro": "unknown. A curated list (neuromodec.org) describes a video of this title as demonstrating the implant procedure and says it 'includes surgical images with a warning'. That points to real surgical footage, but the link between the list entry and this video is not certain.",
    "licence": "unknown (the watch page could not be read)",
    "quality": "unknown; 2012 upload, so resolution is probably low",
    "reachable": "Probably. Blue Ridge Orthopaedic (Northern Virginia practice, from the handle); no named physician found.",
    "evidence": "noembed returned the title and channel (embedding allowed). The year comes from the search summary. The neuromodec.org SCS video list was fetched but gave no video IDs."
   },
   {
    "url": "https://www.youtube.com/watch?v=5Xn5aig4CHs",
    "title": "Spinal Cord Stimulation Implant",
    "channel": "Vandalia Health CAMC (@VandaliaHealthCAMC)",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "SCS implant (Charleston Area Medical Center, WV)",
    "region": "unknown",
    "views": "unknown",
    "live_fluoro": "unknown",
    "licence": "unknown (the watch page could not be read)",
    "quality": "unknown",
    "reachable": "Yes. A hospital system's official channel (CAMC / Vandalia Health).",
    "evidence": "Found in a WebSearch for SCS 'full procedure / live procedure' videos. noembed confirms the title and channel. The content type (procedure footage or patient education) is not established."
   },
   {
    "url": "https://www.youtube.com/watch?v=IFzrjOctQC8",
    "title": "Intrathecal Pump Implantation",
    "channel": "Joseph Ibrahim (@njspineandpaininst)",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "Intrathecal drug pump implantation (catheter placement plus pump pocket)",
    "region": "unknown (catheter entry is usually lumbar, with the tip advanced to lower thoracic)",
    "views": "unknown",
    "live_fluoro": "unknown",
    "licence": "unknown (the watch page could not be read)",
    "quality": "unknown",
    "reachable": "Probably. Named physician; the handle suggests NJ Spine and Pain Institute; no contact page verified.",
    "evidence": "WebSearch hit plus noembed title and channel. This is the only real-procedure-looking intrathecal catheter video found. Other intrathecal hits were talks or patient education (K0mH8d6SX0k Sound Pain Alliance 'What You Should Know'; EwXcu-KVhJE Pain Specialists of America 'Episode 14') and were excluded."
   },
   {
    "url": "https://www.youtube.com/watch?v=HArznDYpeWM",
    "title": "Implantation of Intrathecal Drug Infusion Pumps: Technical Nuances (Preview)",
    "channel": "Neurosurgical Atlas by Aaron Cohen-Gadol, MD (@neurosurgicalatlas)",
    "year": "unknown",
    "duration": "unknown (a preview; the full chapter is on neurosurgicalatlas.com, which is subscription-based)",
    "procedure": "Intrathecal drug pump implantation, including catheter placement (technical nuances)",
    "region": "unknown (lumbar entry expected)",
    "views": "unknown",
    "live_fluoro": "unknown. Neurosurgical Atlas videos mix operative footage with illustrations.",
    "licence": "unknown (the watch page could not be read); the full version is paywalled",
    "quality": "unknown; professional edit",
    "reachable": "Yes. Neurosurgical Atlas, a named organisation (Aaron Cohen-Gadol MD).",
    "evidence": "WebSearch hit plus noembed title and channel. '(Preview)' in the title means the public YouTube cut is truncated."
   },
   {
    "url": "https://www.youtube.com/watch?v=Rh-uFvpwbzg",
    "title": "Preparing for the Spinal Cord Stimulation (SCS) Procedure with the Percutaneous Lead",
    "channel": "Abbott | Neuromodulation (@AbbottNeuromodulation)",
    "year": "2021 (search summary: June 19, 2021)",
    "duration": "unknown",
    "procedure": "Manufacturer walkthrough of the Proclaim XR percutaneous-lead SCS implant procedure",
    "region": "unknown",
    "views": "unknown",
    "live_fluoro": "unknown. It is a corporate training or patient video and may be animation or narrated clips.",
    "licence": "unknown (the watch page could not be read)",
    "quality": "unknown",
    "reachable": "Yes, through the corporate channel. Permission is less likely.",
    "evidence": "noembed returned the title and channel. The search snippet says it 'walks through the implant procedure for the ProclaimXR Spinal Cord Stimulation (SCS) System with the percutaneous lead'. Included only as a low-priority check."
   }
  ],
  "notes": "YouTube does look like a possible source, but after this pass I cannot confirm that any single video contains live fluoroscopy. The limit was verification, not supply.\n\n1. YouTube watch pages were unreadable. Every WebFetch of youtube.com/watch, m.youtube and the embed and search pages returned only YouTube's footer: the page title was empty and there was no description, duration, view count or licence text. I could not establish those four fields for any YouTube candidate, which is why they read 'unknown' throughout. The only metadata that worked was YouTube oEmbed (youtube.com/oembed and noembed.com), which gives the exact title, the channel and whether embedding is allowed. Third-party front ends (Invidious, Piped) were blocked by the network. Dates come from search-engine summaries, not the watch pages, so treat them as approximate.\n\n2. Embedding is disabled on all the Seattle Science Foundation videos. oEmbed returned HTTP 401 for Yme7AxnIRWI, Vluvyif1mBg, RrRN6GMkkEQ, ot_gIGZdUWw, 7XcQTaN70aM and _dJkuD8xyDU. They are still public, since search indexes them. This channel is the most promising cluster because the titles say 'Live Demonstration' and 'LAB DEMO', and SSF is an educational non-profit, which makes asking permission realistic.\n\n3. The shared WebSearch budget ran out partway through. The session-wide cap is 200, and later searches were refused. So this angle is under-covered, and I did not work around the cap by fetching other search engines. Not searched:\n   - named interventional pain channels beyond those above;\n   - manufacturer channels (Nevro, Medtronic, Boston Scientific) for procedure footage;\n   - cervical-specific SCS videos on YouTube;\n   - retrograde or sacral lead placement;\n   - Vimeo, JoVE, and more Neurosurgical Focus: Video entries.\n\n4. No candidate has a verified number of seconds of live fluoroscopy. A person needs to open each URL for about a minute to record:\n   - whether the C-arm monitor is shown live or as saved stills;\n   - the view (SCS is mostly AP thoracic from T12 up to T6-T8, with a lateral check);\n   - the licence line under the description.\n   Real-patient procedure videos in this field usually include live AP runs while the lead is steered up the dorsal epidural space. That is a general expectation, not an observation.\n\n5. Why this angle is worth finishing:\n   - SCS lead advancement is a naturally temporal, cranio-caudal sweep of the thoracic spine in AP.\n   - The narration or caption often states the tip level ('top of T8'), which could act as a weak level label.\n   - The difficulty is that the thoracic AP field during SCS often excludes both T1 and the sacrum, so naming depends on local morphology or a T12 rib or L1 reference, which is exactly what the test targets.\n\n6. Found but excluded:\n   - Stills only: Westrup and Conner, Cureus 2021, 'Percutaneous Thoracic Spinal Cord Stimulator Placement' (PMC8051427, CC BY, contact [e-mail withheld]), and JNS Case Lessons 2024 'Intrathecal placement of percutaneous SCS leads' (PMC11418641).\n   - Wikimedia Commons: Category:Spinal_cord_stimulator has only three X-ray stills, no video.\n   - Patient vlogs and talks: 8OZ9A9bp9aM The Will to Walk, dBzNWH7TjcM Wellward Regenerative Medicine, WUp6NXVhT5o.\n   - Animations: KNSpb9nTOa4, and the Willis Knighton patient-education page.\n   - Ferrara intrathecal baclofen pump video (youtu.be/HetelPwwwak, Neurosurgical Focus: Video 2020, stated CC BY-NC-ND, contact [e-mail withheld]): its article never mentions fluoroscopy.\n   - Deuk Spine Institute playlist 'Spinal Cord Stimulator (SCS) Removal Livestreams' (PLeMOmlZnwlAUdFf5tBQ2edy2ChsZ2wOYM): long unedited livestreams, but they cover removal, not lead advancement, and whether fluoroscopy is shown is unknown.\n   - AAOS 'Open Thoracic Spinal Cord Stimulator Revision' (aaos.org video id 27602): the page could not be fetched (header overflow).\n\n7. Next steps: open the Seattle Science Foundation and Arizona Pain videos by hand first. If more of the angle is wanted, raise CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION.\n\nNo video was downloaded, no scraper or yt-dlp was used, and no files were edited.",
  "verify": [
   {
    "url": "https://www.youtube.com/watch?v=Yme7AxnIRWI",
    "confirmed_live_fluoro": "Probably live, not confirmed. The large right-hand panel is a direct video feed from the C-arm, not a filmed monitor. It shows a Ziehm live-display overlay (patient date 11/17/2017, a running clock, kV 60-61, mA 5.5, cumulative fluoro time Xt 1.38 then 1.4x). YouTube's auto-frames show fluoro at the 50% and 75% points. Between them the clock moves from 11:02:23 to 11:07:4x and the lead has advanced. The 25% frame shows the physician explaining on a spine model. How many seconds of beam-on cine there are is unknown.",
    "confirmed_licence": "unknown. For every YouTube watch page, WebFetch returned only the YouTube footer, so no licence field could be read. oEmbed returns HTTP 401, which means embedding is disabled.",
    "confirmed_views": "AP only was seen, at both sampled fluoro points. It covers the thoracolumbar region with the lead running cranially from a low entry point; exact levels are not established. Lateral was not seen.",
    "usable_for_tracking": "good",
    "corrections": "This is the strongest candidate on the list. The layout has three panels: two small camera views on the left (skin/needle and hands) and a large circular fluoro field on the right, about 790x720 px of a 1280x720 frame. maxresdefault exists, so the upload is HD. The Seattle Science Foundation logo is burned into the video, which confirms the producer; the channel itself is unconfirmed because oEmbed was refused. The C-arm is a Ziehm ('ZIEHM' in the corner of the panel). The procedure date 11/17/2017 comes from the fluoro overlay; the upload date is still unknown. Duration is unknown, but the clock advancing about 5 minutes between the 50% and 75% frames means this is long procedure footage, not a clip. SCS lead steering usually means the C-arm is moved cranially to follow the tip, which could give real cranio-caudal translation. That has not been verified. Still to check: whether the panel runs as continuous video or holds last-image frames between shots. Evidence: oEmbed 401; i.ytimg.com maxresdefault, hq2 and hq3 viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=ot_gIGZdUWw",
    "confirmed_live_fluoro": "Probably live, not confirmed. The 50% auto-frame shows a large direct-feed fluoro panel with a kVp/mA readout ('75 kVp', '2.57 mA'). The 25% frame shows a picture-in-picture fluoro inset at lower left beside an overhead view of the field. At 75% the fluoro is visible only on a filmed monitor behind the physician. Seconds of cine are unknown.",
    "confirmed_licence": "unknown (watch page not readable; oEmbed 401, so embedding is disabled)",
    "confirmed_views": "AP was seen, at two sampled points: magnified lumbar or thoracolumbar spine with several percutaneous leads and needles. Lateral was not seen.",
    "usable_for_tracking": "good",
    "corrections": "It is real procedure footage in the same Seattle Science Foundation three-panel format as Yme7AxnIRWI (the old SSF logo is burned in), not a talk. The channel is still unconfirmed because oEmbed returned 401. The upload is HD (maxresdefault exists). Heavy hardware (two leads plus needles) overlies the posterior elements in a tightly collimated, magnified field showing about 3 levels, which will make vertebra tracking harder than in Yme7AxnIRWI. Boston Scientific hardware per the title. Year and duration are unknown. Evidence: oEmbed 401; maxresdefault, hq1 and hq2 viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=RrRN6GMkkEQ",
    "confirmed_live_fluoro": "Fluoro is present; continuity is unknown. At 50% the whole frame is fluoro: a circular field on a monitor-style overlay with kVp/mA and dose readouts. That overlay reads '0.00 mGy/min', meaning the beam was off at that instant, so this frame is a last-image hold. At 75% there is a split screen with fluoro on the left and the needle/lead entry on the right. The 25% frame shows the physician talking.",
    "confirmed_licence": "unknown (watch page not readable; oEmbed 401, so embedding is disabled)",
    "confirmed_views": "Lateral was seen, at two sampled points: a thoracic or thoracolumbar lateral with the lead contacts along the dorsal epidural space and a needle. AP is not confirmed; the fluoro behind the title card cannot be assigned a view.",
    "usable_for_tracking": "possible",
    "corrections": "The affiliation is wrong. The title card reads 'Jennifer Lee, M.D.' with the EvergreenHealth logo and '8th Annual Interventional Pain Management Fellows Course' (Seattle Science Foundation TV), so the Jennifer Lee in this video is at EvergreenHealth (Kirkland, WA), not Texas Pain & Spine Institute in Amarillo. The Amarillo contact and Facebook link belong to a different physician. The setting looks like a cadaver or bioskills lab, which should make permission easier. The upload is HD. This is one of the few candidates with lateral fluoro, but it is unknown whether the lateral segments are cine or held frames. Evidence: oEmbed 401; maxresdefault, 1/2/3.jpg, hq2 and hq3 viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=-rWuzfYkd5M",
    "confirmed_live_fluoro": "Fluoro is present as a composited inset; continuity is unknown. The top-right corner carries a clean exported fluoro image, not a filmed monitor. A DICOM text corner reads '...Chapman', and the lower edge fades into the room shot. The inset appears in the thumbnail and in the 50% and 75% auto-frames with different content, while the 25% frame is a disclaimer card. Whether the inset plays as cine or shows saved images is unknown.",
    "confirmed_licence": "unknown (watch page not readable; oEmbed succeeds, so embedding is allowed)",
    "confirmed_views": "AP was seen: two leads and two Tuohy needles over the thoracolumbar vertebrae, and a thoracic AP with the lead ascending. Lateral appears at 75%: a dark lateral inset with the lead, and the burned-in subtitle 'In lateral view: Leads should be behind foramina'.",
    "usable_for_tracking": "possible",
    "corrections": "The region and views were unknown before; both AP and lateral now appear. The C-arm is a Ziehm Vision RFD (visible on the C-arm cover), not otherwise identified. The upload is HD (maxresdefault 1280x720). The fluoro inset is only about 390x470 px at 720p and is cropped and partly faded where it meets the room shot, so it is marginal for tracking even if it plays as cine. The title and channel are confirmed by oEmbed. Duration and upload year remain unverified (the year still rests on the search snippet). Evidence: oEmbed JSON; maxresdefault, 1/2/3.jpg, hq2 and hq3 viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=_1xMxFZa6tU",
    "confirmed_live_fluoro": "Fluoro is present, and at least one moment is beam-on. The 25% auto-frame shows a split screen: fluoro on the left, and on the right the OR, with the surgeon at a prone patient. The fluoro overlay reads '119 kVp' and '61.91 mGy/min'. A non-zero dose rate means the beam was on at that instant, so this is a live screen capture. The 50% and 75% frames and the thumbnail show open surgical field only. The total seconds of fluoro are unknown and are probably a small share of the video.",
    "confirmed_licence": "The article's own statement is contradictory: it reads '© 2020 The Authors. This is an open access article distributed under the CC BY-NC-ND license (http://creativecommons.org/licenses/by/4.0/)'. That was re-checked on PMC9542308. The linked URL is the CC BY 4.0 URL. The YouTube licence is unknown because the watch page was not readable.",
    "confirmed_views": "AP was seen: a circular field over the lumbosacral/pelvic region with a metal marker bar across it. The article text says confirmation was made 'on AP fluoroscopy' and on 'lateral fluoroscopy', but lateral was not seen in the sampled frames. The targets were L5 and S1 DRG.",
    "usable_for_tracking": "possible",
    "corrections": "The live-fluoro question is partly resolved: at least one live-capture segment exists. The upload is probably SD (maxresdefault returns 404; hqdefault is 480x360 letterboxed), and the fluoro occupies about half the frame. Channel (AANS) and title are confirmed by oEmbed; embedding is allowed. Corresponding author [e-mail withheld] (PMC). Useful because of the lumbosacral region and journal-grade permission routes, but the fluoro is likely brief and low-resolution. Evidence: oEmbed JSON; PMC9542308; hqdefault and 1/2/3.jpg viewed; the 1.jpg/hq1 split screen was read directly."
   },
   {
    "url": "https://www.youtube.com/watch?v=Vluvyif1mBg",
    "confirmed_live_fluoro": "None seen. The title card and all three auto-frames (25/50/75%) show Dr. Lee speaking at a draped table with the C-arm in position, and no fluoro panel. Fluoro elsewhere in the video is not excluded.",
    "confirmed_licence": "unknown (watch page not readable; oEmbed 401, so embedding is disabled)",
    "confirmed_views": "unknown (no fluoro seen)",
    "usable_for_tracking": "poor",
    "corrections": "The affiliation is wrong. The burned-in title card reads 'Spinal Cord Stimulation Trial Procedure / Surgical Demo / Kirkland, WA / Jennifer M. Lee, M.D. / EvergreenHealth Pain Care / 9th Annual Interventional Pain Management Fellows Course / Seattle Science Foundation TV'. It is not Texas Pain & Spine Institute in Amarillo, and the GotPainTexas Facebook post is a different physician and a different procedure. The setting is the SSF bioskills lab ('BIOSK...' signage), so the subject is probably a cadaver or simulator. The upload is HD. Evidence: oEmbed 401; maxresdefault, 1/2/3.jpg and hq2 viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=C1e84KmcjRs",
    "confirmed_live_fluoro": "No direct fluoro seen. The thumbnail is a title card, and all three auto-frames show Dr. Paul Lynch (name on his scrub top) talking to camera in the procedure room. The fluoro appears only as small images on the C-arm monitor cart behind him.",
    "confirmed_licence": "unknown (watch page not readable; oEmbed succeeds, so embedding is allowed)",
    "confirmed_views": "unknown. The background monitors appear to show AP spine, but they are too small to use.",
    "usable_for_tracking": "poor",
    "corrections": "The sampled frames are mostly a talking-head explainer, not continuous procedure footage. Any fluoro is at most a filmed monitor in the background. Title and channel are confirmed by oEmbed; the upload is HD. Evidence: oEmbed; maxresdefault, 1/2/3.jpg and hq2 viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=jAgMZcy-MEw",
    "confirmed_live_fluoro": "No. The thumbnail and all three auto-frames are text cards on a blue background ('Lateral lead migration is the permanent lateral movement of the lead in the epidural space away from the tissue targeted for stimulation'; 'Use a strain relief loop between the anchor and the connector').",
    "confirmed_licence": "unknown (watch page not readable; oEmbed succeeds, so embedding is allowed)",
    "confirmed_views": "none seen",
    "usable_for_tracking": "not",
    "corrections": "This looks like re-posted manufacturer training material (text-card style, 4:3, SD; maxresdefault returns 404), not a recorded procedure by Dr. Matis. That fits the earlier search summary calling it 'a Medtronic video'. Evidence: oEmbed; hqdefault and 1/2/3.jpg viewed."
   },
   {
    "url": "https://drhatgis.com/procedure-videos",
    "confirmed_live_fluoro": "unknown. The page text (re-fetched) contains no mention of fluoroscopy, X-ray or C-arm, and no video URL, iframe or ID could be extracted, so the videos could not be inspected.",
    "confirmed_licence": "The page states 'Copyright © 2026 Dr. Jesse Hatgis - All Rights Reserved'. The licence of the videos themselves is unknown.",
    "confirmed_views": "unknown",
    "usable_for_tracking": "poor",
    "corrections": "The licence field needs correcting from 'no licence stated' to the site's 'All Rights Reserved' copyright line. The page lists nine videos, not four. The other five are BMAC and stem-cell harvest, PRP, interspinous device (MILD-type decompression), occipital nerve block and stellate ganglion block. The four neuromodulation titles and descriptions are confirmed. Contact details are confirmed: [phone withheld], [e-mail withheld]. It is rated poor only because nothing could be verified; if the video host can be found, the cervical SCS trial is the one worth checking."
   },
   {
    "url": "https://www.youtube.com/watch?v=2S9IZkC8xvQ",
    "confirmed_live_fluoro": "None seen. The thumbnail shows a draped patient with the IPG on the drapes. Auto-frames show a 3-D anatomical animation at 25%, two surgeons operating in an open field at 50%, and a prepped incision at 75%.",
    "confirmed_licence": "unknown (watch page not readable; oEmbed succeeds, so embedding is allowed)",
    "confirmed_views": "none seen",
    "usable_for_tracking": "poor",
    "corrections": "It is real surgical footage mixed with animation. It is HD (maxresdefault exists), which is unexpected for a 2012 upload. No fluoro appears in the four sampled images, so the fluoro content is still unverified. The channel name in oEmbed is 'blueridgeorthopaedic' (Blue Ridge Orthopaedic, Northern Virginia); no named physician was found. Evidence: oEmbed; hqdefault, maxresdefault, 1/2/3.jpg and hq2 viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=BEEuLT764zo",
    "confirmed_live_fluoro": "No. The thumbnail and all three auto-frames show a surgeon in a 'Summit Brain & Spine' shirt talking on a couch, with a stock SCS illustration and lead images. The thumbnail caption reads 'Placement of a spinal cord stimulator'.",
    "confirmed_licence": "unknown (watch page not readable; oEmbed succeeds, so embedding is allowed)",
    "confirmed_views": "none",
    "usable_for_tracking": "not",
    "corrections": "This is a talking-head explainer, not procedure footage. The upload is SD (maxresdefault returns 404). Evidence: oEmbed; hqdefault and 1/2/3.jpg viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=5Xn5aig4CHs",
    "confirmed_live_fluoro": "No. The thumbnail (a CAMC staff member in scrubs being interviewed in a supply room) and the auto-frames (the same interview, then a patient interview) show no procedure and no fluoro.",
    "confirmed_licence": "unknown (watch page not readable; oEmbed succeeds, so embedding is allowed)",
    "confirmed_views": "none",
    "usable_for_tracking": "not",
    "corrections": "This is a hospital patient-story or interview video, not procedure footage. Channel 'Vandalia Health CAMC' is confirmed by oEmbed. Evidence: hqdefault, maxresdefault and 1/2/3.jpg viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=IFzrjOctQC8",
    "confirmed_live_fluoro": "No. The thumbnail and auto-frames show a physician in an OR explaining with a plastic spine model and a pump device. No procedure and no fluoro are visible.",
    "confirmed_licence": "unknown (watch page not readable; oEmbed succeeds, so embedding is allowed)",
    "confirmed_views": "none",
    "usable_for_tracking": "not",
    "corrections": "This is an explainer, not a recorded implantation. The channel author is 'Joseph Ibrahim' (confirmed by oEmbed). Evidence: maxresdefault and 1/2/3.jpg viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=HArznDYpeWM",
    "confirmed_live_fluoro": "No. The thumbnail and all three auto-frames are a webinar: PowerPoint slides ('Disclosures', 'Preoperative Considerations: Subfascial Pump Placement', 'Subfascial Pump') with a webcam inset of the speaker, labelled 'Michael Turner'.",
    "confirmed_licence": "unknown (watch page not readable; oEmbed succeeds, so embedding is allowed)",
    "confirmed_views": "none",
    "usable_for_tracking": "not",
    "corrections": "It is a lecture by Michael Turner (Goodman Campbell Brain and Spine / Indiana University Department of Neurological Surgery, per the slide footer), hosted on the Neurosurgical Atlas channel. It is not operative footage from Cohen-Gadol. Evidence: oEmbed; maxresdefault and 1/2/3.jpg viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=Rh-uFvpwbzg",
    "confirmed_live_fluoro": "No. The thumbnail is a lifestyle title card ('Implant Procedure - Proclaim XR SCS System with Percutaneous Lead'). The auto-frames show a clinician interview and animated silhouette graphics.",
    "confirmed_licence": "unknown (watch page not readable; oEmbed succeeds, so embedding is allowed)",
    "confirmed_views": "none",
    "usable_for_tracking": "not",
    "corrections": "This is Abbott patient-education material mixing animation and interview. No fluoro was seen. Evidence: oEmbed; maxresdefault and 1/2/3.jpg viewed."
   }
  ]
 },
 {
  "angle": "dmx",
  "candidates": [
   {
    "url": "https://www.youtube.com/watch?v=Eq8m0e6AGGw",
    "title": "Explore Spine Movement with Dynamic Digital Radiography (DDR) | Konica Minolta Healthcare",
    "channel": "Konica Minolta Healthcare Americas, Inc. (@kmha_us, channel UCiEsfWZ62SiLGzzqDE83_og)",
    "year": "unknown",
    "duration": "unknown; the thumbnails at about 50% and 75% are DDR/Konica end cards, so the cine is probably in the first half",
    "procedure": "Dynamic Digital Radiography: pulsed flat-panel radiography at up to 15 frames/s, not image-intensifier fluoroscopy. Standing lumbar lateral bending.",
    "region": "lumbar (lower thoracic to pelvis/iliac crests in frame)",
    "views": "AP only (lateral bending); no lateral flexion-extension seen in the sampled frames",
    "live_fluoro": "yes (a DDR cine loop; the opening frame is split-screen with stock yoga footage, and the frame at about 25% is full-frame AP lumbar); seconds unknown",
    "quality": "HD upload (maxresdefault thumbnail exists); native digital flat-panel image, not a filmed monitor; Konica logo overlay bottom-right; split-screen stock footage in the opening",
    "licence": "unknown (the YouTube watch page did not render via WebFetch, so the licence line could not be read)",
    "reachable": "yes: corporate uploader, Konica Minolta Healthcare Americas (Wayne, NJ); contact form on healthcare.konicaminolta.us",
    "evidence": "Title and channel from YouTube oEmbed. Content from the hqdefault thumbnail (split-screen, AP lumbar DDR) and the hq1 thumbnail (full-frame AP lumbar spine with pelvis). hq2 and hq3 are end cards. Konica's DDR page lists 'L-Spine AP Flexion and Extension' and 'up to 15 sequential radiographs per second'. The video is not in Konica's 'Dynamic Digital Radiography' playlist RSS and not among the channel's 15 newest uploads, so its date and view count were not established."
   },
   {
    "url": "https://www.youtube.com/watch?v=WUWfgkEIYTs",
    "title": "Scoliosis Patient - DMX",
    "channel": "dmxworks (DMX Imaging, LLC)",
    "year": "2015 (published 2015-01-06, channel RSS)",
    "duration": "unknown",
    "procedure": "Digital motion X-ray (image-intensifier videofluoroscopy) of a standing scoliosis patient moving",
    "region": "thoracic and thoracolumbar (the frames at about 25% and 75% show thoracic spine with ribs; the frame at about 50% shows lower thoracic to lumbar)",
    "views": "AP (coronal) only; 2,485 views (channel RSS)",
    "live_fluoro": "yes: the thumbnails at about 25%, 50% and 75% are all fluoroscopy frames, so it appears continuous throughout; seconds unknown",
    "quality": "SD 4:3 (oEmbed 200x150; no maxresdefault); direct video capture, not a filmed monitor; image-intensifier circle; patient-camera inset bottom-left; 'd' orientation marker at left",
    "licence": "unknown (the YouTube watch page did not render)",
    "reachable": "yes: DMX Imaging, LLC, 4159 Corporate Ct, Palm Harbor FL 34683; [e-mail withheld]; [phone withheld] (dmxworks.com)",
    "evidence": "oEmbed (author dmxworks); youtube.com/feeds/videos.xml?user=dmxworks (date, views); thumbnails hqdefault, hq1, hq2 and hq3 viewed. The best thoracolumbar item found. The inset would need masking or cropping."
   },
   {
    "url": "https://www.youtube.com/watch?v=SxL8wPe088g",
    "title": "Dr Woggon Scoliois DMX",
    "channel": "dmxworks (DMX Imaging, LLC)",
    "year": "2015 (published 2015-01-07, channel RSS)",
    "duration": "unknown",
    "procedure": "DMX of a scoliosis patient, reviewed on a monitor",
    "region": "thoracic (AP chest-level spine visible on the monitor)",
    "views": "AP; 2,621 views (channel RSS)",
    "live_fluoro": "yes, but only as a camera filming a desktop monitor that plays the DMX (the frames at about 0% and 50% are the same scene); seconds unknown",
    "quality": "filmed monitor at an angle with a viewer's head in the foreground; the fluoroscopy occupies a small part of the frame; patient inset; HD-looking 16:9 camera, but the effective fluoroscopy resolution is low",
    "licence": "unknown (the YouTube watch page did not render)",
    "reachable": "yes: as dmxworks above ([e-mail withheld]); Dr Woggon (named in the title) is a separate clinician",
    "evidence": "oEmbed, channel RSS, and the hqdefault and hq2 thumbnails. Lower value than WUWfgkEIYTs because of the filmed-monitor geometry; included because it is thoracic."
   },
   {
    "url": "https://www.youtube.com/watch?v=56Sxu0thpcU",
    "title": "Lumbar Coupling ( Video Fluoroscopy)by Prof.Mohanty and Dr.Shamla Pazare of MTFI",
    "channel": "Umasankar Mohanty (@usmohanty, channel UCRJYXYCk5CEafSaR3VN989A)",
    "year": "2009 (published 2009-01-09 per a search-result snippet)",
    "duration": "unknown",
    "procedure": "Videofluoroscopy of lumbar coupled motion (lateral bending with rotation), used for manual-therapy teaching",
    "region": "lumbar (roughly L2 to L5 visible)",
    "views": "AP only",
    "live_fluoro": "yes: the thumbnails at 0%, about 50% and about 75% are all live AP lumbar image-intensifier frames, so it appears continuous; seconds unknown",
    "quality": "SD 4:3 (no maxresdefault); a camcorder filming a CRT/LCD that shows the fluoroscopy inside a software UI (buttons and sliders round the circle); moire, glare, cursor visible",
    "licence": "unknown (the YouTube watch page did not render)",
    "reachable": "plausibly: a named physiotherapist, Prof. U. S. Mohanty of the Manual Therapy Foundation of India (www.mtfi.net per his other video titles); channel still active in 2026 (RSS); no contact page read",
    "evidence": "oEmbed; search snippet giving the date and the 'combination of movements' description; three thumbnails viewed. This is the only true image-intensifier LUMBAR cine found on YouTube in this pass. It was filmed off a monitor."
   },
   {
    "url": "https://www.cmsimaging.com/ddr.html",
    "title": "CMS Imaging - Dynamic Digital Radiography",
    "channel": "CMS Imaging, Inc. (a Konica DDR dealer)",
    "year": "unknown",
    "duration": "short animated GIF loops (length unknown)",
    "procedure": "DDR cine loops shown as animated GIFs",
    "region": "lumbar (ddrLspine.gif) and cervical (ddrCspine.gif), plus non-spine loops",
    "views": "unknown (the view of the GIFs was not established; the GIFs were not downloaded)",
    "live_fluoro": "yes (the page presents DDR motion loops as GIFs), not verified frame by frame; seconds unknown",
    "quality": "GIF, so palette-reduced and probably downscaled",
    "licence": "'© - CMS Imaging, Inc. All Rights Reserved' (page footer)",
    "reachable": "yes: info@cmsimaging.com, [phone withheld], 4050 Azalea Drive, North Charleston SC 29405",
    "evidence": "The page read via WebFetch lists the GIF filenames ddrLspine.gif and ddrCspine.gif. The original clips probably come from Konica Minolta, so asking Konica for the source cine is the better request."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7078620/",
    "title": "Lumbar Intervertebral Motion in Healthy Male Participants: Protocol for a Motion Analysis During Flexion and Extension Cinematographic Recordings (JMIR Res Protoc)",
    "channel": "Maastricht University / Zuyderland MC (corresponding author Inge J. M. H. Caelers)",
    "year": "2020",
    "duration": "14 s per flexion-extension cycle (metronome-paced, per the protocol)",
    "procedure": "Seated lumbar flexion-extension cineradiography, pelvis fixed",
    "region": "lumbar L1-S1",
    "views": "lateral; 11 healthy males aged 18-25, two sessions at least 2 weeks apart",
    "live_fluoro": "cine exists (7.5 frames/s) but no video is published with the article; by request only",
    "quality": "unknown (not public)",
    "licence": "article: 'Creative Commons Attribution License (https://creativecommons.org/licenses/by/4.0/)'; recordings not released",
    "reachable": "yes: [e-mail withheld]",
    "evidence": "PMC full text read via WebFetch. This is the lumbar sibling of the Maastricht cervical cine already on the list, and the same data-transfer route probably applies. It is the only lateral LUMBAR flexion-extension cine source found on this angle."
   },
   {
    "url": "https://www.youtube.com/watch?v=T3vsvpkRR14",
    "title": "Video Fluoroscopy - Cervical Spine - S_M_VF_RFC_7_17_12.wmv",
    "channel": "Samuel Ralls (Sam) (@SamuelRallsDC)",
    "year": "unknown (the filename suggests a recording dated 2012-07-17)",
    "duration": "unknown",
    "procedure": "Chiropractic videofluoroscopy (image intensifier), active cervical flexion-extension",
    "region": "cervical (occiput to about C7)",
    "views": "lateral",
    "live_fluoro": "yes: the frames at 0% and about 50% are both lateral cine with the neck at different positions; seconds unknown",
    "quality": "SD 4:3 (no maxresdefault); clean direct export (.wmv), NOT a filmed monitor; image-intensifier circle; no overlays in the sampled frames",
    "licence": "unknown (the YouTube watch page did not render)",
    "reachable": "plausibly: a named chiropractor, Samuel Ralls DC ('Ralls Family Chiropractic' per a search snippet); no contact page read",
    "evidence": "oEmbed and the hqdefault and hq2 thumbnails. The cleanest cervical cine found: an unannotated export with no inset."
   },
   {
    "url": "https://www.youtube.com/watch?v=b8ZgL4mBqdA",
    "title": "Cervical Spine Video Fluoroscopy - Chiropractic Care",
    "channel": "Samuel Ralls (Sam) (@SamuelRallsDC)",
    "year": "2011 (posted 2011-09-12 per a search snippet)",
    "duration": "unknown",
    "procedure": "Chiropractic videofluoroscopy: lateral flexion-extension plus AP left/right rotation (per a search snippet)",
    "region": "cervical",
    "views": "lateral (thumbnail) and AP (frame at about 75%)",
    "live_fluoro": "yes: lateral and AP cine frames at the sampled points; seconds unknown",
    "quality": "SD 4:3 (no maxresdefault); clean direct capture; image-intensifier circle; no overlays seen",
    "licence": "unknown (the YouTube watch page did not render)",
    "reachable": "plausibly: Samuel Ralls DC / Ralls Family Chiropractic",
    "evidence": "oEmbed; search snippet (Ralls Family Chiropractic; lateral flexion/extension and AP L/R rotation; posted Sept 12, 2011); hqdefault and hq3 thumbnails viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=ChA-xwfL0p4",
    "title": "DMX Part 1 (also DMX Part 2 GCtVKwO65mQ and 'Dynamic Motion X-Ray' BnKq0Ouahl8, same channel)",
    "channel": "XRayInMotion (channel UCh-Mgted0M2fEIXN_Ih-RBg)",
    "year": "2010 (Part 1 and Part 2 2010-02-17; BnKq0Ouahl8 2010-01-25)",
    "duration": "unknown",
    "procedure": "Digital motion X-ray (videofluoroscopy), active neck motion; used as evidence of injury",
    "region": "cervical to upper thoracic (Part 1 thumbnail shows about C2-T4); Part 2 and BnKq0Ouahl8 are upper cervical",
    "views": "lateral (all three thumbnails)",
    "live_fluoro": "yes, apparently: cine with the patient-camera inset visible; seconds unknown",
    "quality": "poor: SD 4:3 analog/VHS-era capture with a blue tint and the image off a screen; patient inset; BnKq0Ouahl8 has a red arrow overlay; descriptions empty",
    "licence": "unknown (the YouTube watch page did not render)",
    "reachable": "no: anonymous channel with 4 uploads, all from 2010",
    "evidence": "oEmbed; channel RSS (user=XRayInMotion; views 8,575 / 5,694 / 7,670); thumbnails viewed. painscience.com embeds Part 1 and Part 2 as examples of DMX. Useful mainly because Part 1 reaches the cervicothoracic junction."
   },
   {
    "url": "https://www.youtube.com/watch?v=2eXvwBD6ckA",
    "title": "Unstable C1-C2 and Stable C1-C2 under Digital Motion X-ray",
    "channel": "Caring Medical & Hauser Neck Center (@CaringmedicalProlotherapy, channel UCd7t_9FqqE9eYWBE3r1ZZOg)",
    "year": "2019 (published 2019-08-30, playlist RSS)",
    "duration": "unknown",
    "procedure": "DMX of the upper cervical spine during head lateral tilt, comparing an unstable and a stable C1-C2",
    "region": "cervical (C1-C2)",
    "views": "AP open-mouth (odontoid) during lateral bending; 56,670 views",
    "live_fluoro": "yes: DMX cine of the C1-C2 lateral mass overhang during tilting (per the description); seconds unknown",
    "quality": "HD upload container (maxresdefault exists) of an SD image-intensifier source; burned-in caption 'STABLE C1-C2' and clinic logo; orientation markers",
    "licence": "unknown (the YouTube watch page did not render)",
    "reachable": "yes: Caring Medical Florida / Hauser Neck Center, 9738 Commerce Center Ct, Fort Myers FL 33908, [phone withheld]; Ross Hauser MD",
    "evidence": "oEmbed; playlist RSS PLa5ku0Xx5Qp3_mVgamSBY715FFvrzkgdr (date, views, description); hqdefault thumbnail viewed. The same 15-video playlist holds more DMX cine: NjwswrqcDO0 (lateral flexion with drawn alignment lines, 16,887 views), UwPSutEZBw4 (anterolisthesis, 7,833 views), 4ZV9u0gcmlI (after C5-C6 disc replacement, 77,354 views) and VldpkaNx1Qw (injection under DMX, 56,687 views)."
   },
   {
    "url": "https://www.youtube.com/watch?v=TNhVQIkD7aY",
    "title": "Pinched nerve treated with Prolotherapy: Before and after Digital Motion X-ray",
    "channel": "Caring Medical & Hauser Neck Center",
    "year": "2018 (published 2018-10-22, playlist RSS)",
    "duration": "unknown",
    "procedure": "DMX cervical flexion-extension before and after treatment",
    "region": "cervical",
    "views": "lateral; 54,902 views",
    "live_fluoro": "yes, interleaved with text title cards (the frame at about 50% is a title card); seconds unknown",
    "quality": "SD 4:3 (no maxresdefault); direct capture; burned-in text at top-left and patient-camera inset at bottom-left",
    "licence": "unknown (the YouTube watch page did not render)",
    "reachable": "yes: Caring Medical (as above)",
    "evidence": "oEmbed; playlist RSS; hqdefault and hq2 thumbnails. Embedded on caringmedical.com/about/digital-motion-x-ray/, which states DMX runs at '30 individual x-ray frames per second'."
   },
   {
    "url": "https://www.youtube.com/watch?v=7GdVnVnF29E",
    "title": "Digital Motion X-Ray of Cervical Spine",
    "channel": "Spoon Central (@spooncentral5500)",
    "year": "2021 (February 2021 per a search snippet)",
    "duration": "unknown",
    "procedure": "DMX of the cervical spine in flexion-extension (a patient's own recording)",
    "region": "cervical (C1 to about C6; hardware or screws visible at mid-cervical levels)",
    "views": "lateral",
    "live_fluoro": "yes: lateral cine at 0%, about 50% and about 75%; seconds unknown",
    "quality": "a phone filming a monitor: moire, the screen bezel visible, reduced contrast; SD (no maxresdefault)",
    "licence": "unknown (the YouTube watch page did not render)",
    "reachable": "no: pseudonymous personal channel",
    "evidence": "oEmbed; search snippet; hqdefault, hq2 and hq3 thumbnails viewed."
   },
   {
    "url": "https://www.youtube.com/watch?v=heZCFwjbKDk",
    "title": "Dynamic Digital Radiography (DDR) for C-Spine Imaging | Konica Minolta Healthcare",
    "channel": "Konica Minolta Healthcare Americas, Inc. (@kmha_us)",
    "year": "2023 (2023-11-21 per a search snippet)",
    "duration": "unknown",
    "procedure": "DDR (pulsed flat-panel radiography, up to 15 frames/s), cervical flexion-extension",
    "region": "cervical",
    "views": "lateral",
    "live_fluoro": "yes (a DDR cine loop, shown split-screen beside stock footage of a person moving the neck); seconds unknown",
    "quality": "HD (maxresdefault exists); native flat-panel image; Konica logo; split-screen",
    "licence": "unknown (the YouTube watch page did not render)",
    "reachable": "yes: Konica Minolta Healthcare Americas (corporate)",
    "evidence": "oEmbed; search snippet; hqdefault thumbnail viewed. Same channel: Eeyz9ySPz2I 'X-Ray That Moves | DDR Orthopedic Applications' (2023-03-23, HD) shows a small image-intensifier cervical clip labelled 'Fluoroscopy' beside a lateral cervical DDR in flexion-extension; IwTNq5TsuK4 'Dynamic Digital Radiology View of C Spine Fuchs Imaging' (2023-06-16) is a lateral head/C-spine DDR with hardware."
   },
   {
    "url": "https://www.youtube.com/shorts/yphljivZSpA",
    "title": "Spine X-Ray in Motion",
    "channel": "Z&Z Medical, Inc. (@ZZMedical)",
    "year": "unknown",
    "duration": "unknown (a YouTube Short, so 60 s or less)",
    "procedure": "Dynamic radiography (flat-panel, DDR-like), cervical flexion-extension after ACDF",
    "region": "cervical (anterior plate and screws at about C4-C6)",
    "views": "lateral",
    "live_fluoro": "yes (the frame at about 50% is a lateral cine frame); seconds unknown",
    "quality": "vertical 9:16 Short; clean flat-panel image; crop unknown",
    "licence": "unknown (the YouTube watch page did not render)",
    "reachable": "plausibly: a company account (Z&Z Medical, Inc.); no contact page read",
    "evidence": "oEmbed (vertical 113x200) and the hq2 thumbnail."
   },
   {
    "url": "https://www.youtube.com/watch?v=WrJEnsNHxB4",
    "title": "Motion X-Ray of Cervical Spine",
    "channel": "Innovative Nerve & Joint Centers (@INJCenters)",
    "year": "2014 (August 2014 per a search snippet)",
    "duration": "unknown",
    "procedure": "Motion X-ray (DMX-type) of the cervical spine for neck and arm pain / radiculopathy",
    "region": "cervical",
    "views": "AP in the thumbnail; the snippet says 'various views taken in a Digital Motion X-ray'",
    "live_fluoro": "probably, but not verified: the frame at about 50% is a VLC-player splash cone, so this is a screen recording of a media player",
    "quality": "a custom title thumbnail; a screen recording with a player splash; SD",
    "licence": "unknown (the YouTube watch page did not render)",
    "reachable": "plausibly: a named multi-site practice (Innovative Nerve & Joint Centers)",
    "evidence": "oEmbed, search snippet, and the hqdefault and hq2 thumbnails. Low priority."
   }
  ],
  "notes": "Yes, YouTube is a possible source, but a weak one for the lumbar spine. The dynamic-motion content there is overwhelmingly cervical. I found no lateral LUMBAR flexion-extension cine on YouTube. The lumbar and thoracolumbar items are all AP:\n- Konica DDR Eq8m0e6AGGw (lateral bending, flat-panel, HD);\n- Mohanty 56Sxu0thpcU (image-intensifier fluoroscopy filmed off a monitor);\n- dmxworks WUWfgkEIYTs (a standing scoliosis patient, thoracic and thoracolumbar, direct capture with a patient inset).\n\nThe one lateral lumbar flexion-extension source found is the Maastricht lumbar cine protocol: 11 subjects, L1-S1, 7.5 fps. It is available by request only ([e-mail withheld]) and is the lumbar sibling of the Maastricht cervical cine already on the list.\n\nTwo image domains are mixed here:\n- DMX clips (Caring Medical, dmxworks, Ralls, XRayInMotion) are image-intensifier videofluoroscopy. Caring Medical states 30 frames/s. Their appearance is close to C-arm images.\n- Konica DDR, and probably Z&Z and CMS Imaging, are pulsed flat-panel radiography at up to 15 frames/s. They are sharper and look like radiographs.\n\nKeep the two apart in any test set.\n\nNearly every clinic upload carries a patient-camera inset, burned-in text, drawn lines or a logo. The cleanest items are the two Samuel Ralls DC exports (T3vsvpkRR14, b8ZgL4mBqdA): direct lateral cervical cine with no overlays in the sampled frames. Both are SD.\n\nHow the fields were established:\n- YouTube watch pages returned only the site footer via WebFetch. Invidious and Piped mirrors were blocked by the proxy (certificate mismatch).\n- Title and channel come from YouTube oEmbed. Upload date and view count come from the channel or playlist RSS where available (dmxworks, XRayInMotion, the Caring Medical DMX playlist), otherwise from search snippets.\n- Content, view and capture quality were checked by viewing YouTube's single-image thumbnails: hqdefault and hq1/hq2/hq3, at about 25/50/75% of each video. No video was downloaded.\n- SD versus HD was inferred from the oEmbed aspect ratio and whether a maxresdefault thumbnail exists.\n- Duration and licence are 'unknown' for every YouTube item. The licence line on the watch page could not be read, so do not assume Creative Commons for any of them.\n\nCoverage was cut short. The session-wide WebSearch budget (200/200) ran out partway through, so Vimeo, Ortho Kinematics/KineGraph demo videos, Bournemouth or AECC lab videos, and a dedicated search for a Konica lateral L-spine clip were not searched.\n\nWorth pursuing:\n- dmxworks (DMX Imaging LLC, [e-mail withheld]). It is the DMX vendor behind many clinic clips and may hold lumbar and thoracolumbar DMX. Its public channel shows scoliosis AP studies.\n- Konica Minolta Healthcare Americas. Its DDR product page lists 'L-Spine AP Flexion and Extension' and 'C-Spine Lat Flexion and Extension' cine, which it does not post publicly.\n\nExcluded after checking:\n- Bu6PpOGHSxc: a positioning demonstration with no X-ray.\n- Katz Chiropractic V5Ra_fcAYX8: a news piece with a talking head.\n- Alaska Back Care lz2kNa0KDQQ: a talking head in front of a DMX monitor.\n- Caring Medical -trePIGJTfQ: a talk.\n- Centeno nPBW4Bk-8l4 and G5W0iTDN0as: slide talks.\n- The Konica 'Dynamic Digital Radiography' playlist: all pulmonary or overview videos.\n\nThumbnails that WebFetch saved are under laptop-session:f1bdbd78-151f-470b-b703-dd9af9b3fecc\\tool-results\\. No project files were edited.",
  "verify": [
   {
    "url": "https://www.youtube.com/watch?v=Eq8m0e6AGGw",
    "confirmed_live_fluoro": "Moving X-ray is confirmed, but it is not fluoroscopy. It is Konica DDR (pulsed flat-panel, up to 15 frames/s; the CMS Imaging dealer page says DDR is 'NOT Fluoroscopy'). Motion shows in the first half only: hqdefault and maxresdefault are split-screen (stock yoga footage beside an AP lumbar DDR), hq1 (about 25%) is a full-frame AP lumbar DDR, and hq2 (50%) is the DDR/Konica end card. Seconds and duration are unknown.",
    "confirmed_licence": "unknown. The youtube.com watch page returns only the site footer through WebFetch (www, m., app=desktop and embed were all tried). Invidious mirrors are blocked on this network and the Wayback Machine cannot be fetched.",
    "confirmed_views": "AP only, in standing lateral bending. The frame runs from about the thoracolumbar junction to the sacrum and iliac crests. No lateral view was seen.",
    "usable_for_tracking": "possible",
    "corrections": "Confirmed: title and channel (oEmbed), and maxresdefault exists (1280x720 HD). The DDR panel is a native flat-panel image with a Konica logo and a blue bar and marker at the right edge. It is a marketing clip: the cine is short and shares the frame with stock footage for part of its length. Crop the DDR half. It is useful as a clean AP lumbar test, but it is DDR, not C-arm fluoroscopy. Date, duration and licence remain unknown."
   },
   {
    "url": "https://www.youtube.com/watch?v=WUWfgkEIYTs",
    "confirmed_live_fluoro": "Yes, probably continuous. hq1 (25%), hq2/hqdefault (50%, the same frame) and hq3 (75%) are all image-intensifier DMX frames with the patient-camera inset. dmxworks.com states that DMX acquires 30 sequential radiographs per second. Seconds and duration are unknown.",
    "confirmed_licence": "unknown (the watch page does not render through WebFetch). The channel RSS description is the placeholder text 'Description', with no licence statement.",
    "confirmed_views": "AP (coronal) only. hq1 is AP mid-thoracic with a scoliotic curve and ribs; hq3 is AP upper thoracic; hq2 is AP lower thoracic to upper lumbar.",
    "usable_for_tracking": "possible",
    "corrections": "Confirmed from the channel RSS: published 2015-01-06, 2,485 views, no description. maxresdefault returns 404, so the upload is SD 4:3. The 50% frame, the only one reaching the thoracolumbar junction, is heavily washed out and blurred (the exposure swings during motion), so the lumbar value is lower than the earlier note implied. The video is mostly thoracic. The patient-camera inset (bottom-left) and the 'd' marker would need masking. Contact confirmed on dmxworks.com: DMX Imaging, LLC, 4159 Corporate Ct, Palm Harbor FL 34683, [phone withheld], [e-mail withheld], '© 2025 DMX Imaging, LLC'."
   },
   {
    "url": "https://www.youtube.com/watch?v=SxL8wPe088g",
    "confirmed_live_fluoro": "Only incidentally, as a filmed monitor. hq2 and hqdefault show a viewer's head in the foreground and a desktop monitor playing an AP chest-level DMX in a player window with the patient inset. hq1 (25%) and hq3 (75%) show a man talking to camera with the monitor small in the background, the fluoroscopy a thumbnail-sized window. The video is mostly talking head.",
    "confirmed_licence": "unknown (the watch page does not render). The RSS description is only the placeholder 'Description'.",
    "confirmed_views": "AP (thoracic/chest level, on the monitor only).",
    "usable_for_tracking": "poor",
    "corrections": "Correction: this is not a monitor recording throughout. At 25% and 75% it is a talking-head segment (the speaker is presumably Dr Woggon but is not identified on the page) and the fluoroscopy is tiny. The effective fluoroscopy resolution is far too low for vertebra tracking. RSS confirms 2015-01-07 and 2,621 views. Drop it."
   },
   {
    "url": "https://www.youtube.com/watch?v=56Sxu0thpcU",
    "confirmed_live_fluoro": "Yes, apparently: hqdefault, hq1 (25%) and hq3 (75%) are all AP lumbar image-intensifier frames at different positions, so the cine appears to run throughout. It is a camera filming a monitor that shows the cine inside a software UI (Calibration buttons, sliders, window/level bars, a mouse cursor). Seconds and duration are unknown.",
    "confirmed_licence": "unknown (the watch page does not render)",
    "confirmed_views": "AP only (lumbar; about three to four vertebral bodies with pedicles visible per frame; lateral bending and rotation posture).",
    "usable_for_tracking": "possible",
    "corrections": "Confirmed: title and author (oEmbed; @usmohanty). The upload date of 2009-01-09 could not be re-verified: the video is not in the channel RSS, and no web search was left. Image quality is poor (off-screen capture, blur, low contrast, the UI border must be cropped). It is still the only true image-intensifier lumbar cine on YouTube in this set, so it is kept as 'possible' for a hard-case test, not a primary one."
   },
   {
    "url": "https://www.cmsimaging.com/ddr.html",
    "confirmed_live_fluoro": "Not fluoroscopy. The page describes DDR ('NOT Fluoroscopy' but 'X-Ray that Moves'), up to 15 sequential radiographs per second at up to 17x17 inches, shown as animated GIF loops. Motion was not verified frame by frame, and the GIFs were not fetched because an animated GIF is a video loop.",
    "confirmed_licence": "'© - CMS Imaging, Inc. All Rights Reserved' (page footer). No reuse grant.",
    "confirmed_views": "unknown (no caption on the page names AP, lateral, flexion or extension)",
    "usable_for_tracking": "poor",
    "corrections": "Confirmed: the filenames ddrLspine.gif and ddrCspine.gif, plus ddrNeck.gif, which the earlier note did not list. Contact confirmed: info@cmsimaging.com, [phone withheld], 4050 Azalea Drive, North Charleston SC 29405. It is a dealer page, and palette-reduced GIFs are not a test set. Ask Konica Minolta for the source DDR sequences instead."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7078620/",
    "confirmed_live_fluoro": "Recordings exist but none are published. Seated lumbar flexion-extension cineradiography at 7.5 frames/s, a 14 s metronome-paced cycle. The article has no supplementary video and no data availability statement.",
    "confirmed_licence": "Article: 'This is an open-access article distributed under the terms of the Creative Commons Attribution License...' The recordings themselves are not released, so no licence applies to them.",
    "confirmed_views": "lateral (sagittal), L1-S1",
    "usable_for_tracking": "possible",
    "corrections": "Confirmed, with additions: the device is a Philips Allura Xper FD20, the images are 1024x1024 with a field of view of 520 cm², and there were 11 healthy males with the pelvis fixed. Authors: Caelers, Boselie, Rijkers, van Hemert, de Bie, van Santbrink; corresponding author [e-mail withheld]. It is 'possible' only on request. If released, it would be the best lateral lumbar cine source here: a flat-detector C-arm-class system at native resolution with the full L1-S1 span."
   },
   {
    "url": "https://www.youtube.com/watch?v=T3vsvpkRR14",
    "confirmed_live_fluoro": "Yes. hqdefault and hq2 (50%) are lateral cervical frames; hq1 (25%) is a lateral frame in a different, washed-out position; hq3 (75%) is an AP open-mouth frame. It is a continuous image-intensifier cine export. Seconds and duration are unknown.",
    "confirmed_licence": "unknown (the watch page does not render)",
    "confirmed_views": "Lateral (flexion-extension; about C1-C5/C6 visible, the lower levels hidden by the shoulders) AND AP open-mouth (odontoid, C1-C2).",
    "usable_for_tracking": "good",
    "corrections": "Correction: the views include AP open-mouth at about 75%, not lateral only. Confirmed: a clean direct export with an image-intensifier circle, no patient inset and no text overlay. A bright collimator-blade band runs down the left edge. maxresdefault returns 404, so it is SD 4:3. Title and author confirmed by oEmbed (@SamuelRallsDC). The date is known only from the filename (7_17_12). It is the best cervical candidate, but only mid-to-upper cervical levels are trackable."
   },
   {
    "url": "https://www.youtube.com/watch?v=b8ZgL4mBqdA",
    "confirmed_live_fluoro": "Yes. hq1 (25%, the same frame as hqdefault) and hq3 (75%) are lateral cervical frames in different positions, and hq2 (50%) is an AP open-mouth frame. It is a continuous image-intensifier cine. Seconds and duration are unknown.",
    "confirmed_licence": "unknown (the watch page does not render)",
    "confirmed_views": "Lateral (about C1-C6/C7, flexion-extension) and AP open-mouth (C1-C2).",
    "usable_for_tracking": "good",
    "corrections": "Correction: the AP open-mouth frame is at about 50% (hq2), not 75%; the 75% frame is lateral. The image is clean with no inset or text overlay. The lateral frames show the vertebral bodies and facets crisply from C2 to about C6. The posting date of 2011-09-12 could not be re-verified (no search budget). It comes from the same uploader as T3vsvpkRR14, so one permission request to Samuel Ralls DC would cover both."
   },
   {
    "url": "https://www.youtube.com/watch?v=ChA-xwfL0p4",
    "confirmed_live_fluoro": "Only in parts. hqdefault (lateral cervicothoracic, about C3-T4, with the patient inset) and hq1 (lateral cervical) are DMX frames. hq2 (50%) and hq3 (75%) are anatomical illustration slides ('Posterior Longitudinal Ligament', 'Alar Ligaments'). It is a filmed presentation, probably a projector screen, with DMX clips between the slides.",
    "confirmed_licence": "unknown (the watch page does not render). The RSS description is empty.",
    "confirmed_views": "lateral (cervical to upper thoracic)",
    "usable_for_tracking": "poor",
    "corrections": "Correction: this is not continuous cine. At least half the sampled frames are illustration slides, and the cine is filmed off a screen with a blue tint. Siblings: GCtVKwO65mQ (Part 2) hq2 is a blue-tinted lateral upper cervical frame, also off a screen. BnKq0Ouahl8 hq2 is an animated 'Dynamic Motion Imaging' logo with a 3-D spine model, i.e. animation. RSS confirms 2010-02-17 / 8,575 views (Part 1), 2010-02-17 / 5,694 (Part 2), 2010-01-25 / 7,670 (BnKq0Ouahl8), and a fourth upload, V-xb2rKNmi0 'What DMX is NOT'. The channel is anonymous. Its only use is the cervicothoracic reach, and the quality defeats that."
   },
   {
    "url": "https://www.youtube.com/watch?v=2eXvwBD6ckA",
    "confirmed_live_fluoro": "Yes, per the description ('how the C1 and C2 vertebrae align when tilting the head'). hq3 and maxresdefault show AP open-mouth DMX frames, and hq1 (25%) is a title card, 'UNSTABLE C1-C2'. The cine is broken up by title cards. Seconds unknown.",
    "confirmed_licence": "unknown (the watch page does not render). The playlist RSS description has no licence, copyright or reuse statement.",
    "confirmed_views": "AP open-mouth (odontoid) only, C1-C2, during lateral head tilt; two different patients",
    "usable_for_tracking": "poor",
    "corrections": "Confirmed from the playlist RSS: 2019-08-30, 56,670 views, description as stated. The burned-in caption 'STABLE C1-C2', the Caring Medical logo and 'q' orientation markers are visible. It shows only two vertebrae, so it is almost useless for level naming. Correction: the phone number in the description is [phone withheld], not 4701; the emails are info@caringmedical.com and [e-mail withheld]."
   },
   {
    "url": "https://www.youtube.com/watch?v=TNhVQIkD7aY",
    "confirmed_live_fluoro": "Yes, apparently, with title cards between segments. hq1 (25%) is a Caring Medical title card ('DMX Showing Complete Resolution of Pinched Nerve in Neck...'). hqdefault and hq3 (75%) are lateral cervical DMX frames. caringmedical.com, which embeds this video, states '30 individual x-ray frames per second'. Seconds unknown.",
    "confirmed_licence": "unknown (the watch page does not render). The RSS description has no licence statement.",
    "confirmed_views": "lateral cervical (occiput and mandible to about C6; dental fillings and a 'd' marker visible)",
    "usable_for_tracking": "possible",
    "corrections": "Confirmed from the playlist RSS: 2018-10-22, 54,902 views. The title card sits at 25%, not only at 50% as earlier stated; hq2 was not re-viewed. The burned-in top-left text and bottom-left patient inset described earlier were not visible in hqdefault or hq3, so that claim is unconfirmed. It is a before/after comparison, so it probably holds several short lateral sequences from one patient."
   },
   {
    "url": "https://www.youtube.com/watch?v=7GdVnVnF29E",
    "confirmed_live_fluoro": "Yes, lateral cine at different positions in hq1 and hq3, but as a phone filming a CRT playing a VHS tape. hq1 carries a VCR on-screen display ('Play  SP  Hi-Fi  Line1') over the image. Seconds unknown.",
    "confirmed_licence": "unknown (the watch page does not render)",
    "confirmed_views": "lateral cervical (about C1-C6)",
    "usable_for_tracking": "poor",
    "corrections": "Addition: the source is analog VHS (VCR OSD), filmed with visible scan lines, moire and the screen bezel. The earlier claim of hardware or screws at mid-cervical levels is not confirmed: the bright vertical line in hq1 could be a plate or a collimator edge. The channel is pseudonymous (@spooncentral5500), so there is no route to permission. The February 2021 date could not be re-verified."
   },
   {
    "url": "https://www.youtube.com/watch?v=heZCFwjbKDk",
    "confirmed_live_fluoro": "Moving X-ray is confirmed but it is DDR, not fluoroscopy. hq2 (50%) and hq3 (75%) are split-screen with a lateral C-spine DDR in different positions (extension, then flexion). hq1 (25%) is full-frame stock footage of a man head-banging. Seconds unknown.",
    "confirmed_licence": "unknown (the watch page does not render)",
    "confirmed_views": "lateral cervical (about C1-C7 in the DDR half)",
    "usable_for_tracking": "possible",
    "corrections": "Confirmed: title and author (oEmbed). The DDR occupies about half the frame and only part of the running time; the rest is stock footage. It is a clean flat-panel image with a Konica logo. The 2023-11-21 date and the sibling videos (Eeyz9ySPz2I, IwTNq5TsuK4) could not be re-verified."
   },
   {
    "url": "https://www.youtube.com/shorts/yphljivZSpA",
    "confirmed_live_fluoro": "unknown. hq1, hq2 and hq3 are pixel-identical (a lateral C-spine with an anterior plate and screws at about C4-C6), so no sampled frame shows motion. It may be a still, or a loop that returns to the same position; the title 'Spine X-Ray in Motion' is the only evidence of motion.",
    "confirmed_licence": "unknown (the watch page does not render)",
    "confirmed_views": "lateral cervical (one frame seen)",
    "usable_for_tracking": "poor",
    "corrections": "Correction: 'live cine' is not supported. The three thumbnails at 25%, 50% and 75% are the same frame. oEmbed confirms the title, Z&Z Medical, Inc. (@ZZMedical), and a vertical 113x200 player. It is a clean flat-panel image, but it is a Short (60 s or less) of unconfirmed motion. It needs to be watched before it is kept."
   },
   {
    "url": "https://www.youtube.com/watch?v=WrJEnsNHxB4",
    "confirmed_live_fluoro": "Probably, not verified. hq1 (25%) is a black frame showing only the DMX patient-camera inset, hq2 (50%) is the VLC-player cone splash, and hq3 (75%) is an AP cervical DMX frame with the patient inset. It is a screen recording of a media player, and no two frames show the spine in motion.",
    "confirmed_licence": "unknown (the watch page does not render)",
    "confirmed_views": "AP cervical (hq3; mandible above, collimated)",
    "usable_for_tracking": "poor",
    "corrections": "Confirmed: title and author (oEmbed, @INJCenters). DMX content does exist (hq3), but the video is a screen capture with dead frames and a player splash. The August 2014 date is not re-verified. Low priority."
   }
  ]
 },
 {
  "angle": "vfss",
  "candidates": [
   {
    "url": "https://talkbank.org/aphasia/access/English/Dysphagia/UNM.html",
    "title": "DysphagiaBank: UNM Dysphagia Corpus (TalkBank / AphasiaBank, non-protocol English > Dysphagia)",
    "channel": "TalkBank (CMU), contributed by Phyllis M. Palmer, UNM Speech and Hearing Sciences",
    "year": "2023 (Palmer, Padilla & MacWhinney, Dysphagia 39:476-483); the directory was last modified in April 2026",
    "duration": "Whole clinical exams, trimmed only to remove PHI and clips with no bolus. Per-study length is not stated. The sample transcripts time-code swallows out to 14-59 s (e.g. 'swallow 14091_16484', '57247_58495' ms), so each study runs about 1 minute or more.",
    "procedure": "Videofluoroscopic swallow study / modified barium swallow (clinical, retrospective). Includes infants on bottles and adults with neuro, head-and-neck cancer and general medical diagnoses.",
    "region": "Cervical. The lateral field shows the skull base and upper-to-mid cervical spine; the paper's Fig. 1 shows the skull base, mandible and C1-C3/4. How far down the field reaches (C6/C7) is not stated.",
    "views": "n/a (not YouTube)",
    "live_fluoro": "Yes. Full-motion cine; the inclusion criterion was acquisition at 30 frames and 30 pulses per second. It spans roughly tens of seconds to minutes per study, but exact totals are unknown.",
    "quality": "Exported from TIMS MVP/TIMS review. The authors say they traded resolution against streaming size when choosing a format, so the files are compressed. There is an audio track (SLP speech). Transcripts are in CHAT format with millisecond swallow time codes and a %xp position code (LAT/AP). Media download is supported, per the paper.",
    "licence": "TalkBank Ground Rules state 'Creative Commons CC BY-NC-SA 3.0'. They preclude incorporating the data in commercial products, including LLMs, and say 'Those who wish to use the videos for other purposes must bear full responsibility for any legal claims brought by persons appearing in the videos.' The access page puts the Dysphagia corpus at the 'Registration required' level: 'users need to provide their email and create a password'.",
    "reachable": "Yes. Phyllis Palmer [e-mail withheld]; Brian MacWhinney [e-mail withheld]; TalkBank [e-mail withheld]",
    "evidence": "The UNM.html page gives contact, DOI 10.21415/VD8A-FX27, a media folder at media.talkbank.org/aphasia/English/Dysphagia/UNM and the participant PDF 0docs/UNM.pdf. That PDF lists IDs 001-091 with gaps (86 studies): about 53 adults aged 21-97 and 33 paediatric, most of them infants. Every study has a lateral projection and many adults also have AP. The page header says 'Participants: 7', which contradicts the PDF; it was not resolved. The Palmer 2023 paper (0docs/palmer2023.pdf) says 73 studies at publication, 30 fps / 30 pps, that the data are 'readily available to the public', and that 'TalkBank does support media download'. The access level is from talkbank.org/aphasia/access.html and the licence from talkbank.org/0share/rules.html. The media folder itself returned an empty body to WebFetch, so no file listing was seen."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12419438/",
    "title": "Dynamic motion analysis of the cervical spine during normal swallowing (Mekata, Takizawa, Takigawa, Ito; Medicine 2025;104(36):e44168)",
    "channel": "Medicine (Baltimore) / Kojiro Mekata, Shijonawate Gakuen University",
    "year": "2025",
    "duration": "Supplemental Video File 1; length not stated. The analysis window was 61 frames per swallow at 30 fps, about 2 s.",
    "procedure": "Research VFSS in healthy volunteers: seated, 10 mL of 40% barium, CUREVISTA fluoroscope (Hitachi Medico)",
    "region": "Cervical C2-C6. Every frame was tracked by template matching on spinous processes and vertebral bodies; the authors say C7 could not be tracked because of image quality.",
    "views": "n/a",
    "live_fluoro": "Yes. The data are 30 fps lateral VF recordings; the supplemental video shows the original image beside the tracked image, of unknown length (about 2 s analysed).",
    "quality": "Research-grade 30 fps. The Figure 1 caption reads 'The right and center of the figure show the original image and tracking image obtained by template matching'.",
    "licence": "Article is 'Creative Commons Attribution License 4.0 (CCBY)'. The supplement's licence is not separately stated. Data availability: 'available from the corresponding author on reasonable request.'",
    "reachable": "Yes. Kojiro Mekata, [e-mail withheld], Dept. of Rehabilitation, Shijonawate Gakuen University, Osaka",
    "evidence": "PMC full text via WebFetch: 38 subjects analysed (39 enrolled), 30 fps, C2-C6 tracked per frame, CC BY 4.0, data on request. This is the closest match to a per-frame, level-named cervical track on continuous lateral fluoroscopy. The supplement's direct URL could not be recovered because the LWW page returned 402."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8560570/",
    "title": "Automatic annotation of cervical vertebrae in videofluoroscopy images via deep learning (Zhang, Mao, Coyle, Sejdic; Med Image Anal 2021)",
    "channel": "Sejdic lab (University of Pittsburgh / UPMC, with J. Coyle)",
    "year": "2021",
    "duration": "1,518 swallow clips (per-clip length not stated)",
    "procedure": "Clinical and healthy-volunteer VFSS at UPMC Presbyterian",
    "region": "Cervical. Per-frame corner landmarks: C2 antero-inferior corner, and C3 and C4 antero-superior and antero-inferior corners.",
    "views": "n/a",
    "live_fluoro": "Yes in the source data: 59,810 annotated frames at 30 fps (downsampled from 60 fps). Nothing is public.",
    "quality": "Research dataset of 335 subjects (265 patients, 70 healthy)",
    "licence": "No data availability statement found and no public dataset or code link. The PMC copy is an NIH author manuscript.",
    "reachable": "Probably. Ervin Sejdic (corresponding author on this lab's VFSS papers) and James Coyle (Pitt). No email was captured from the page.",
    "evidence": "Read on PMC8560570 via WebFetch: 335 subjects, 1,518 clips, 59,810 frames, C2-C4 corner annotations, 30 fps. The companion paper Li et al. 2024 (J Imaging Inform Med, PMC11300761) tracks the hyoid relative to the cervical vertebrae on the same kind of data and is not open access. This is the largest per-frame, level-named cervical vertebra annotation on VFSS found; it is available only by request, if at all."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12682499/",
    "title": "An intelligent quantitative analysis software for videofluoroscopic swallowing study in patients with dysphagia",
    "channel": "Journal article (corresponding author's name was not captured)",
    "year": "2025 (inferred from PMC id; not confirmed)",
    "duration": "82 VFSS sequences (length not stated)",
    "procedure": "VFSS: 18 dysphagic patients (40 sequences) and 14 healthy controls (42 sequences)",
    "region": "Cervical. The user marks the antero-inferior corners of C2, C4 and C6 on the first clear frame, and the software then tracks them automatically.",
    "views": "n/a",
    "live_fluoro": "Yes in the source data (tracked video sequences); nothing is public",
    "quality": "unknown",
    "licence": "Article CC BY-NC-ND 4.0. Data: 'available from the corresponding author upon reasonable request. The data are not publicly available due to privacy or ethical restrictions.'",
    "reachable": "Corresponding author on request (name/email not extracted)",
    "evidence": "PMC full text via WebFetch. No supplementary videos."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12713095/",
    "title": "Introducing the Modified Cobb Angle for Measuring Cervical Spine Curvature During Swallowing (Steele et al., Laryngoscope Investig Otolaryngol 2025)",
    "channel": "Catriona M. Steele lab (UHN / KITE, Toronto) with multi-site coauthors",
    "year": "2025",
    "duration": "140 frames measured: 4 per participant (Still, BPM, MPC, SR), taken from full recordings",
    "procedure": "VFSS in 35 healthy adults, recorded at 30 fps on TIMS",
    "region": "Cervical: C0-C2, C2-C4, C2-C6 and C2-C7 Cobb angles",
    "views": "n/a",
    "live_fluoro": "Source recordings are continuous 30 fps; the measurements are on stills",
    "quality": "TIMS 30 fps research recordings",
    "licence": "Article CC BY-NC-ND. Data: 'available on request from the corresponding author. The data are not publicly available due to privacy or ethical restrictions.'",
    "reachable": "Yes. [e-mail withheld]",
    "evidence": "PMC full text via WebFetch. The lab measures down to C7 on healthy lateral VFSS, so it may hold the lower-cervical coverage the Mekata data lacks. That is not verified."
   },
   {
    "url": "https://github.com/BSEL-UC3M/VFSS_analysis",
    "title": "VFSS_analysis: automated VFSS preprocessing, nnU-Net segmentation and 21 dynamic parameters (Cubero et al., Comput Biol Med 2025)",
    "channel": "BSEL, Universidad Carlos III de Madrid, with Rennes (LTSI)",
    "year": "2025",
    "duration": "One sample video, data/raw_VFSS/test/healthy_001/t0/healthy_001_t0.AVI; length unknown",
    "procedure": "VFSS in head-and-neck cancer patients; the sample is labelled 'healthy_001'",
    "region": "Cervical (lateral VFSS). Whether the label set includes vertebrae was not confirmed.",
    "views": "n/a",
    "live_fluoro": "Yes (1 AVI clip, 'compressed to preserve quality' per README); seconds unknown",
    "quality": "AVI, compressed; resolution unknown",
    "licence": "Repo: no LICENSE seen. Models on Zenodo 10.5281/zenodo.17191973 are CC BY 4.0 (models_VFSS.zip, 6.1 GB; weights only, no videos).",
    "reachable": "Yes. [e-mail withheld], [e-mail withheld], [e-mail withheld]",
    "evidence": "GitHub repo page, README and folder listing, plus the Zenodo record, via WebFetch. Only one public clip; the value is the authors' clinical cohort, available by request."
   },
   {
    "url": "https://www.youtube.com/playlist?list=PLty92Gv98Lheo67f_a5fxXEjJe1HNXaWo",
    "title": "Modified Barium Swallow Study - Videofluoroscopy (playlist of 7 lateral-view HD MBSS clips)",
    "channel": "Speech Therapy Practice (UCwPHHKDijv62XJgt4jvMssQ)",
    "year": "2019 (all 7 uploaded 2019-01-12)",
    "duration": "unknown for each clip",
    "procedure": "Modified barium swallow: thin, nectar-thick, honey-thick, puree, mixed texture, cracker, 13 mm barium tablet",
    "region": "Cervical (lateral pharyngeal field; lowest level visible unknown)",
    "views": "phI7p1N6IVs 28,341; f1BlHjrUn0A 16,590; I3WMmwtDRMo 8,549; NRRMz04ONq0 5,018; vZB4QPdw95M 10,867; Xxfqb5I1zmc 83,332; -uVBFbV9LfI 14,540 (from the official RSS feed)",
    "live_fluoro": "Probably yes. Every title says 'Lateral View HD'; seconds unknown (not verified by viewing)",
    "quality": "Titles claim HD; one description says 'High quality barium swallow study example'. Whether it is a screen capture or a filmed monitor is unknown.",
    "licence": "unknown (the YouTube licence line cannot be read through WebFetch)",
    "reachable": "Doubtful. The Xxfqb5I1zmc description is copied verbatim from UC Davis Health's adult VFSS web page, and UC Davis does not embed these videos. The channel's recent uploads are English-idiom Shorts. The footage's origin and the owner's contact are unknown.",
    "evidence": "Titles and channel from YouTube oEmbed. IDs, dates, views and descriptions from https://www.youtube.com/feeds/videos.xml?playlist_id=PLty92Gv98Lheo67f_a5fxXEjJe1HNXaWo. Text matched against health.ucdavis.edu/pmr/.../adult vfss.html."
   },
   {
    "url": "https://radiologyassistant.nl/head-neck/swallowing/swallowing-disorders-update",
    "title": "Swallowing disorders update (Radiology Assistant)",
    "channel": "Robin Smithuis, Radiology dept., Alrijne Hospital, Leiderdorp NL",
    "year": "2018 (2018-08-13)",
    "duration": "7-10 embedded cine loops; lengths unknown",
    "procedure": "Pharyngo-oesophageal videofluoroscopy: normal lateral swallow ('in HD'), stasis with aspiration, Zenker's, aspiration before/during/after the swallow, oesophageal stasis and hiatal hernia",
    "region": "Cervical. One 'aspiration during swallowing' loop is a DISH patient with 'syndesmophytes at many levels on the anterior side of the cervical spine'.",
    "views": "n/a",
    "live_fluoro": "Yes (self-hosted video loops of real fluoroscopy); seconds unknown",
    "quality": "The normal-swallow loop is captioned as viewable 'in HD'; some loops carry arrow overlays (blue/yellow arrows mentioned)",
    "licence": "No licence or reuse statement found on the page (unknown)",
    "reachable": "Yes. Radiology Assistant site / Robin Smithuis",
    "evidence": "WebFetch of the page listed the video captions, including the DISH case. Video source URLs were not exposed."
   },
   {
    "url": "https://commons.wikimedia.org/wiki/Category:X-rays_of_disorders_of_swallow_reflex",
    "title": "Hellerhoff lateral swallow fluoroscopy frame series and animations (Wikimedia Commons)",
    "channel": "Hellerhoff (Wikimedia Commons user); derivative animation by Anka Friedrich",
    "year": "2011-2023",
    "duration": "Normal_barium_swallow_animation.gif: 33 frames, 9.9 s. Verzoegerte_Schluckreflextriggerung_mit_laryngealer_Penetration_71M_-_RF_-_001.gif: 17 frames, 6.0 s. Postdeglutitive_Aspiration_79M_-_RF.gif (Category:X-rays of aspiration): 17 frames, 6.0 s. Plus the 11-frame JPG series 53M and 87M, and the 34-frame 'Normaler Schluck-00..33.jpg' series.",
    "procedure": "Pharyngeal barium swallow / VFSS (normal swallow, delayed swallow reflex, penetration, aspiration)",
    "region": "Cervical (lateral neck; the Commons category on the animation is 'Lateral X-rays of the neck')",
    "views": "n/a",
    "live_fluoro": "Sampled frame sequences of real fluoroscopy, not full-rate cine (about 3 frames/s as displayed; acquisition rate unknown)",
    "quality": "352x512 (normal series), 800x951 (71M GIF), 974x1028 (79M GIF)",
    "licence": "Normaler Schluck frames: GFDL 1.2+ and CC BY 3.0 Unported. The animation: CC BY 4.0. The 71M and 79M GIFs and the 53M series: CC BY-SA 4.0.",
    "reachable": "Via Wikimedia user talk page only",
    "evidence": "Commons file and category pages read via WebFetch. These are genuinely reusable consecutive lateral frames, but too sparse in time for tracking at clinical frame rates."
   },
   {
    "url": "https://commons.wikimedia.org/wiki/File:ZenkerSeitlichZiel.gif",
    "title": "ZenkerSeitlichZiel.gif: Zenker diverticulum, strict lateral spot fluoroscopy (plus ZenkerPA.gif, ZenkerSchraeg.gif)",
    "channel": "Bernd Braegelmann (User:Braegel), with permission from Dr. Martin Steinhoff",
    "year": "2008",
    "duration": "7 frames, 3.5 s",
    "procedure": "Barium swallow for Zenker's diverticulum",
    "region": "Cervical / cervicothoracic junction",
    "views": "n/a",
    "live_fluoro": "Short sampled frame sequence (7 frames), not full-rate cine",
    "quality": "363x600, low resolution",
    "licence": "GFDL 1.2+ and CC BY 3.0 Unported",
    "reachable": "Via Wikimedia user page",
    "evidence": "Commons file page via WebFetch. The companion PA and oblique GIFs are in Category:X-rays of Zenker's diverticulum; they were not opened."
   },
   {
    "url": "https://commons.wikimedia.org/wiki/File:Fluoroscopy_of_normal_barium_swallow.ogg",
    "title": "Fluoroscopy of normal barium swallow (inverted)",
    "channel": "Ptrump16 (Wikimedia Commons, own work)",
    "year": "2022",
    "duration": "about 29 s",
    "procedure": "Barium swallow, GE Digital Fluoroscopy (400 mA, 91 kVp)",
    "region": "unknown (projection and anatomy not stated; probably oesophageal rather than oropharyngeal)",
    "views": "n/a",
    "live_fluoro": "Yes, continuous but at a frame time of 333.3 ms (3 fps), about 29 s",
    "quality": "1024x1024, inverted greyscale",
    "licence": "CC BY-SA 4.0 International",
    "reachable": "Via Wikimedia user page",
    "evidence": "Commons file page via WebFetch; the description quotes the technical parameters. Low value: 3 fps and the view is not stated."
   },
   {
    "url": "https://www.youtube.com/watch?v=xu_YYOAlZEw",
    "title": "Normal Swallow Tutorial with Modified Barium Swallow",
    "channel": "Fauquier ENT (@fauquierent)",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "Modified barium swallow teaching video (a normal swallow shown on x-ray and on endoscopy)",
    "region": "Cervical (presumed lateral pharyngeal view; not verified)",
    "views": "unknown",
    "live_fluoro": "unknown. The search-result summary says it shows the swallow 'from an X-ray as well as endoscopic view'; seconds unknown",
    "quality": "unknown",
    "licence": "unknown",
    "reachable": "Yes, likely: an ENT practice channel (practice contact not looked up)",
    "evidence": "Title and channel from YouTube oEmbed; content description from a WebSearch result summary; the watch page was not readable via WebFetch"
   },
   {
    "url": "https://www.youtube.com/watch?v=-7S5Hd_Xh9s",
    "title": "Modified Barium Swallow Case Study - Michael Groher | MedBridge (see also CaD4-9P3ndA 'Modified Barium Swallow Study - Michael Groher | MedBridge')",
    "channel": "Medbridge (@MedbridgeTeam)",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "MBS case-study teaching excerpt (continuing-education course preview)",
    "region": "Cervical (presumed lateral VFSS; not verified)",
    "views": "unknown",
    "live_fluoro": "unknown (probably contains real MBS clips; not verified)",
    "quality": "unknown",
    "licence": "unknown",
    "reachable": "Yes. MedBridge is a commercial CE company; Michael Groher is a named SLP author",
    "evidence": "Titles and channel from YouTube oEmbed for both IDs. Content was not viewable through WebFetch."
   },
   {
    "url": "https://www.youtube.com/watch?v=Q36T5DGHfTw",
    "title": "Videofluoroscopic Swallowing Study (VFSS) | Danielle Marks",
    "channel": "St Vincent's Hospital, Sydney (@StVincentsHospitalSydney)",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "VFSS explainer from a hospital speech pathology department",
    "region": "Cervical (if VFSS footage is shown)",
    "views": "unknown",
    "live_fluoro": "unknown (it may be a talking-head explainer with inserts)",
    "quality": "unknown",
    "licence": "unknown",
    "reachable": "Yes. Institutional channel with a named speech pathologist",
    "evidence": "Title and channel from YouTube oEmbed only"
   },
   {
    "url": "https://laryngopedia.com/videofluoroscopic-swallowing-study-vfss/",
    "title": "Laryngopedia VFSS page: embedded 'Barium Swallow (Barium Esophagram)' and 'Cricopharyngeal Dysfunction - Before and After Cricopharyngeal Myotomy'",
    "channel": "Bastian Voice Institute / Laryngopedia (YouTube channel UCOFcq1mWBXQt6JtO0HBn4jA)",
    "year": "unknown",
    "duration": "unknown",
    "procedure": "Barium swallow; cricopharyngeal bar before and after laser myotomy",
    "region": "Cervical (the cricopharyngeus sits at about C5-C6)",
    "views": "unknown",
    "live_fluoro": "Yes per captions ('x-rays of barium passing through the throat'; the cricopharyngeal video is lateral); seconds unknown",
    "quality": "unknown",
    "licence": "Site: '© 2026 Laryngopedia. All rights reserved.' The YouTube licence is unknown.",
    "reachable": "Yes. Bastian Voice Institute (named laryngology practice)",
    "evidence": "WebFetch of the laryngopedia page gave the captions and the channel ID. The individual video URLs were not exposed, and the channel RSS (latest 15 uploads) contains no swallow-study video."
   }
  ],
  "notes": "I did check YouTube, and it is a possible source, but only a weak one for this purpose. The one open source that matches the brief is not on YouTube. It is DysphagiaBank on TalkBank:\n- whole clinical swallow studies recorded at 30 frames and 30 pulses per second;\n- about 86 studies listed, about 53 of them adults;\n- every study has a lateral view and many adults also have AP;\n- free registration with email and password, media download supported, CC BY-NC-SA 3.0.\n\nFor level-named cervical tracks, the strongest lead is Mekata et al. 2025. They tracked C2-C6 on every frame of 30 fps lateral swallow studies in 38 healthy adults. The article is CC BY 4.0 and the data are available on request. The larger annotated sets (Sejdić lab: 1,518 swallows with C2-C4 corners; Steele lab; PMC12682499) are also request-only.\n\nLimits of this search:\n1. I ran out of web searches. The session's cap of 200 searches ran out after about 12 of my own queries. I did not keep searching around the cap, so YouTube coverage is thin. Zenodo, Figshare, PhysioNet, Kaggle and Korea's AI-Hub were not searched.\n2. YouTube watch pages do not come through WebFetch; it returns only the site footer. Titles and channels come from YouTube's oEmbed endpoint. Upload dates, views and descriptions come from YouTube's official RSS feed, which only worked for the Speech Therapy Practice playlist. Clip length and the licence line (Standard YouTube License or Creative Commons) could not be read for any YouTube video, so they are marked unknown. I found no YouTube swallow-study video confirmed as Creative Commons.\n3. The Speech Therapy Practice playlist is the clearest real lateral footage on YouTube: seven clips titled 'Lateral View HD', 5k-83k views. The uploader looks unaffiliated. One description is copied word for word from a UC Davis Health web page, and the channel now posts English-idiom Shorts. Getting permission from whoever owns the footage looks hard.\n\nHow far this helps the goal:\n- A lateral swallow study shows the cervical spine continuously for tens of seconds, but the spine barely moves. The only spine motion is small flexion during the swallow; Mekata measured angle changes across C2-C6. There is no craniocaudal translation.\n- C2 and the dens are always in view, so naming levels by counting from the top is trivial.\n- C7 is often hidden by the shoulders; Mekata could not track it.\n- The bolus and the hyoid/larynx move over the front of the vertebral bodies. That makes these clips a test of tracking stability under moving overlap, not of level naming at the lumbosacral junction.\n- About a third of DysphagiaBank are infants with immature vertebrae; exclude them from a mature-spine test.\n- For a lateral view with the whole of C2-C7 visible, the adult studies in DysphagiaBank are the most usable open material found. They are complementary to the Bournemouth flexion-extension cine already on the list.\n\nDiscrepancy not resolved: the DysphagiaBank page header says 'Participants: 7', while its participant PDF lists IDs 001-091 (86 studies) and the paper says 73 at publication. The media folder listing returned nothing to WebFetch, so the actual file count was not seen.\n\nSuggested next steps, all by hand and with no downloading:\n- Register for DysphagiaBank and count the adult lateral studies.\n- Email Mekata for the C2-C6 tracked data.\n- Open the Speech Therapy Practice, Fauquier ENT, MedBridge and St Vincent's watch pages in a browser to read their licence lines and lengths.\n- Rerun a YouTube search with the Creative Commons filter for 'videofluoroscopy' and 'modified barium swallow'.\n\nNo files were edited. Two PDFs fetched by WebFetch (the DysphagiaBank participant table and the Palmer 2023 paper) were saved automatically under laptop-session:f1bdbd78-151f-470b-b703-dd9af9b3fecc\\tool-results\\ and read there.",
  "verify": [
   {
    "url": "https://talkbank.org/aphasia/access/English/Dysphagia/UNM.html",
    "confirmed_live_fluoro": "Yes. Palmer et al. 2023 (0docs/palmer2023.pdf, read via WebFetch) states: 'The inclusion criterion for VFSS was that the study had been collected using 30 frames and 30 pulses per second.' Fig. 1 of the paper is a lateral frame with a CHAT transcript that time-codes swallows out to 16484 ms. Length per study is not stated, and no media file was seen because the media folder returned an empty body.",
    "confirmed_licence": "TalkBank rules page, quoted: 'the use of TalkBank data is governed by the Creative Commons CC BY-NC-SA 3.0 copyright license'. It 'precludes the incorporation of the data in commercial products, including systems such as large language models', and 'Those who wish to use the videos for other purposes must bear full responsibility for any legal claims brought by persons appearing in the videos.' The access page lists Dysphagia at 'Registration required': 'users need to provide their email and create a password.' The UNM.html page itself carries no licence line.",
    "confirmed_views": "Lateral for all 86 listed studies. 'Lateral and AP projection' appears 34 times in the participant PDF (0docs/UNM.pdf, IDs 001-091 with gaps, about 33 paediatric and 53 adult). Fig. 1 carries the code '%xp: LAT'.",
    "usable_for_tracking": "possible",
    "corrections": "Confirmed: 86 IDs, the paediatric/adult split, 73 studies at publication, 30 fps / 30 pps, and 'TalkBank does support media download'. The page header 'Participants: 7' still contradicts the PDF. Fig. 1 confirms the field: skull base, mandible and the upper cervical spine to about C4/C5, cut off at the lower-right edge of the circular field, so lower-cervical coverage is doubtful. About 40% are infants and toddlers, whose spines are poor test material. There are no vertebra labels. Contact confirmed: [e-mail withheld], DOI 10.21415/VD8A-FX27."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12419438/",
    "confirmed_live_fluoro": "Yes in the source data: 'The images were recorded at 30 fps' on a CUREVISTA (Hitachi Medico), lateral. The Supplemental Video File 1 is cited ('An example of these results is shown in Figure 1C (Supplemental Video File 1)'), but PMC exposes no link to it, so its length and content are unverified.",
    "confirmed_licence": "Article: 'Creative Commons Attribution License 4.0 (CCBY)'. The supplement's licence is not stated separately. Data: 'available from the corresponding author on reasonable request.'",
    "confirmed_views": "Lateral ('lateral filming direction').",
    "usable_for_tracking": "possible",
    "corrections": "Confirmed: 39 enrolled and 38 analysed, C2-C6 tracked per frame by template matching, and the quote 'tracking C7 is difficult owing to image processing problems'. The Fig. 1 caption confirms that the original and tracked images sit side by side and that the pharyngeal phase is at t = 31. Contact confirmed: [e-mail withheld]. Cervical only; nothing is public without a request."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8560570/",
    "confirmed_live_fluoro": "Yes in the source data: 'pulse rate of 30 pulses per second (full motion), and data were accrued at a sampling rate of 60 frames per second', then 'down-sampled ... to 30 frames/second to eliminate duplicated frames.' Nothing is public.",
    "confirmed_licence": "NIH author manuscript; no data or code availability statement found. No licence for the data.",
    "confirmed_views": "Lateral ('seated in the lateral plane with the 9 inch (22cm) image centered on the area of hyoid bone at rest').",
    "usable_for_tracking": "possible",
    "corrections": "Add these details. Resolution: patients 720x1080 captured in real time, healthy volunteers 1280x1024. Fluoroscopes: Toshiba Ultimax and GE Precision 500D, captured with an AccuStream Express HD card. Corresponding author: Ervin Sejdic, [e-mail withheld] (NIH R01HD092239, R01HD074819). Annotations confirmed: the C2 antero-inferior corner, and the C3 and C4 antero-superior and antero-inferior corners. The companion Li et al. 2024 (PMC11300761) is published 'under exclusive licence to SIIM', but it does state 'Data generated or used for the study are available from the corresponding author by request', and it tracks the C2 and C4 corners per frame. Because the field is centred on the hyoid, coverage is roughly C2-C4 only."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12682499/",
    "confirmed_live_fluoro": "The source data are tracked VFSS sequences; the frame rate is not stated. No supplementary video; nothing is public.",
    "confirmed_licence": "Article CC BY-NC-ND 4.0. Data 'available from the corresponding author upon reasonable request' and not public because of privacy or ethical restrictions.",
    "confirmed_views": "unknown (not stated in the text retrieved; presumably lateral VFSS)",
    "usable_for_tracking": "poor",
    "corrections": "Identify the paper: Wu, Li, Geng, Qian, Dai, Wang, Quantitative Imaging in Medicine and Surgery, 2025. Corresponding authors: Tong Wang [e-mail withheld], Yakang Dai [e-mail withheld], Chen Geng [e-mail withheld] (SIBET, Suzhou). Confirmed: 82 sequences (40 from 18 patients, 42 from 14 controls), with the C2, C4 and C6 antero-inferior corners and the hyoid tracked. Rated poor because the data are small, restricted and would require export from China."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12713095/",
    "confirmed_live_fluoro": "The source recordings are continuous, 'recorded at 30 frames/s' on TIMS, in lateral projection at 30 pulses/s. All measurements are on 4 selected stills per participant. No supplementary files.",
    "confirmed_licence": "Article CC BY-NC-ND 4.0. Data 'available on request from the corresponding author' and not public because of privacy or ethical restrictions.",
    "confirmed_views": "Lateral",
    "usable_for_tracking": "poor",
    "corrections": "This refutes the earlier speculation that the lab may hold lower-cervical coverage. The paper reports missing ratings for '21% of C0-C2 Cobb angles, 38% of C2-C6 Cobb angles, 82% of C2-C7 Cobb angles', because 'C5-C7 vertebrae may fall outside the field of view or be obstructed by shoulder shadows.' This holds for standard lateral VFSS in general: expect C2-C4 reliably and C5-C7 rarely. Confirmed: 35 healthy adults, contact [e-mail withheld]."
   },
   {
    "url": "https://github.com/BSEL-UC3M/VFSS_analysis",
    "confirmed_live_fluoro": "The one sample clip, data/raw_VFSS/test/healthy_001/t0/healthy_001_t0.AVI, is presumably cine; it was not opened and its size and length are not shown. README: 'The file is in AVI format, compressed to preserve quality. It may not be compatible with all video players.'",
    "confirmed_licence": "Repository: no LICENSE file or sidebar licence entry. Top level is data/, models/, README.md, VFSS_functions.py, environment.yml, paths_repository.py, run.py and setup.py. Zenodo 10.5281/zenodo.17191973 is 'Creative Commons Attribution 4.0 International': models_VFSS.zip, 6.1 GB, two nnU-Net models, no videos.",
    "confirmed_views": "unknown (lateral VFSS presumed; not stated)",
    "usable_for_tracking": "poor",
    "corrections": "The paper abstract (Europe PMC) says the framework labels 'ten regions of interest' and extracts '23 swallowing dynamic parameters'; the earlier record said 21. Neither the README, Zenodo nor the abstract names the ten ROIs, so whether they include vertebrae is still unconfirmed. Paper: Cubero et al., Comput Biol Med 2025;187:109759. Emails confirmed: [e-mail withheld], [e-mail withheld], [e-mail withheld]."
   },
   {
    "url": "https://www.youtube.com/playlist?list=PLty92Gv98Lheo67f_a5fxXEjJe1HNXaWo",
    "confirmed_live_fluoro": "Likely, from the thumbnails; not verified by playback. The hqdefault thumbnails of Xxfqb5I1zmc and phI7p1N6IVs are screen captures of a fluoroscopy acquisition console: a circular image-intensifier field, a vendor control panel on the right, a running counter (3643.86 and 3444.61), and text reading 'Continuous', '30 Fps' and 'Fluoro Cu 0.3mm'. That suggests continuous 30 fps fluoroscopy was being screen-recorded. The number of seconds per clip is unknown.",
    "confirmed_licence": "unknown. Watch, embed and mobile pages returned no metadata to WebFetch, so the licence line could not be read.",
    "confirmed_views": "Lateral. Every title says 'Lateral View'. The Xxfqb5I1zmc thumbnail shows a lateral neck with the C2-C5 bodies visible; the phI7p1N6IVs thumbnail shows a lateral oral/pharyngeal field with the cervical spine faint behind the pharynx.",
    "usable_for_tracking": "possible",
    "corrections": "The earlier 'views' field held YouTube view counts, not anatomical views; the RSS counts are confirmed (for example Xxfqb5I1zmc 83,332). All 7 were uploaded 2019-01-12, as confirmed. maxresdefault.jpg returns 404 for Xxfqb5I1zmc and phI7p1N6IVs, which suggests the uploads are below 720p despite 'HD' in the titles; this is an inference, not proof. The console overlay shows a name field reading 'speech / logan', possibly an identifier. The channel's 15 latest uploads are English-idiom Shorts plus one 2026-02-03 voice-exercise video; there is no contact link. The claim that the description was copied from UC Davis could not be re-checked: both guessed UC Davis URLs returned 404. Content-wise this is real lateral cervical cine with vertebrae visible, but the origin and rights holder are unclear. On the user's question: YouTube swallow-study material is cervical only (about C2-C5); none of these candidates is lumbar or thoracolumbar."
   },
   {
    "url": "https://radiologyassistant.nl/head-neck/swallowing/swallowing-disorders-update",
    "confirmed_live_fluoro": "Partly. 'Video of lateral view' is captioned 'Watch in HD', which implies an embedded video, though no video or source URL is exposed. 'Aspiration before swallowing' is a sequence of 8 numbered frames (stills), not cine. The frame rate and length of the others are unknown.",
    "confirmed_licence": "The site's Disclaimer page states: 'The images and illustrations on this site may be reproduced for educational purposes with due credit being given to the original author and the Radiology Assistant.' Videos, research and ML use are not addressed. The article page itself has no licence line.",
    "confirmed_views": "Lateral for the normal swallow; the other items are presumed lateral, not stated.",
    "usable_for_tracking": "poor",
    "corrections": "Correct 'licence unknown' to an education-only reproduction permission with credit, per the Disclaimer; there is a Contact page. Confirmed: 2018-08-13, Robin Smithuis, Alrijne Hospital. The DISH caption is verbatim: 'diffuse idiopathic skeletal hyperostosis (DISH) with syndesmofytes at many levels on the anterior side of the cervical spine.' At least one item is stills, so the count of real cine loops is below the 7-10 given earlier."
   },
   {
    "url": "https://commons.wikimedia.org/wiki/Category:X-rays_of_disorders_of_swallow_reflex",
    "confirmed_live_fluoro": "No. These are short sampled frame sequences of real fluoroscopy, not full-rate cine. Normal_barium_swallow_animation.gif is 33 frames over 9.9 s. The 71M GIF is 17 frames over 6.0 s, and so is the 79M GIF. The 53M and 87M cases are 11 separate JPGs each.",
    "confirmed_licence": "Normaler_Schluck-00.jpg (2011-04-11): GFDL 1.2+ and CC BY 3.0 Unported. The animation: CC BY 4.0 (derivative by Anka Friedrich). The 71M GIF (2021-12-26), the 79M GIF (2023-08-01) and the 53M series (2020-11-10): CC BY-SA 4.0.",
    "confirmed_views": "Lateral neck (the animation is in the category 'Lateral X-rays of the neck')",
    "usable_for_tracking": "poor",
    "corrections": "All confirmed. Add that the normal animation is also categorised 'Retouched pictures'. The category holds 24 files: 22 JPGs and 2 GIFs, one of which is an annotated version. 53M frame size: 972x1075. Too sparse in time for frame-to-frame tracking, but freely licensed."
   },
   {
    "url": "https://commons.wikimedia.org/wiki/File:ZenkerSeitlichZiel.gif",
    "confirmed_live_fluoro": "No. A looped GIF of 7 frames over 3.5 s.",
    "confirmed_licence": "GFDL 1.2+ and CC BY 3.0 Unported",
    "confirmed_views": "Strict lateral ('seitlich'); the companion PA and oblique GIFs were not opened",
    "usable_for_tracking": "not",
    "corrections": "Confirmed: 363x600, 2008-05-05, Bernd Braegelmann (Braegel), with permission from Dr. Martin Steinhoff. Seven low-resolution frames cannot support a tracking test."
   },
   {
    "url": "https://commons.wikimedia.org/wiki/File:Fluoroscopy_of_normal_barium_swallow.ogg",
    "confirmed_live_fluoro": "Continuous, but at a frame time of '333.3333 msec' (3 fps); 29 s long",
    "confirmed_licence": "CC BY-SA 4.0 International",
    "confirmed_views": "unknown. The description says only upper GI imaging; the projection is not stated.",
    "usable_for_tracking": "poor",
    "corrections": "Confirmed: 1024x1024, inverted, GE Digital Fluoroscopy, 400 mA, 91 kVp, 30 ms, created 2022-02-04 by Ptrump16, Ogg Theora, 1.25 MB. An oesophageal field would show thoracic rather than cervical vertebrae, if any; that is not verified."
   },
   {
    "url": "https://www.youtube.com/watch?v=xu_YYOAlZEw",
    "confirmed_live_fluoro": "unknown. The thumbnail is live-action: a clinician in a lead apron hands a cup to a seated patient beside a fluoroscope. Any x-ray segment is unverified.",
    "confirmed_licence": "unknown (the watch page is unreadable through WebFetch)",
    "confirmed_views": "unknown",
    "usable_for_tracking": "poor",
    "corrections": "Title and channel confirmed by oEmbed (Fauquier ENT, @fauquierent). The practice website fetch failed and the channel About page was unreadable, so reachability is unconfirmed. The thumbnail indicates a patient-education production, not a study recording."
   },
   {
    "url": "https://www.youtube.com/watch?v=-7S5Hd_Xh9s",
    "confirmed_live_fluoro": "unknown from the page. The thumbnail is a real fluoroscopy frame: a barium-filled oesophagus in a circular intensifier field with vendor overlay text, SD 4:3. The companion CaD4-9P3ndA thumbnail is a real lateral oral/pharyngeal VFSS frame. Whether either video plays continuous cine is unverified.",
    "confirmed_licence": "unknown",
    "confirmed_views": "-7S5Hd_Xh9s: oesophageal field, probably AP or oblique (not stated). CaD4-9P3ndA: lateral.",
    "usable_for_tracking": "poor",
    "corrections": "Titles and channel confirmed by oEmbed (Medbridge, @MedbridgeTeam). -7S5Hd_Xh9s is an oesophageal study, not pharyngeal, so any vertebrae in view would be thoracic. The footage is a low-resolution capture of commercial CE course content, and permission would come from a commercial company."
   },
   {
    "url": "https://www.youtube.com/watch?v=Q36T5DGHfTw",
    "confirmed_live_fluoro": "unknown; probably none. The thumbnail shows a speech pathologist talking to camera, the word 'DYSPHAGIA', and a photo of a man holding his throat.",
    "confirmed_licence": "unknown",
    "confirmed_views": "unknown",
    "usable_for_tracking": "poor",
    "corrections": "Title and channel confirmed by oEmbed (St Vincent's Hospital, Sydney). The thumbnail indicates a talking-head explainer; any fluoroscopy inserts are unverified."
   },
   {
    "url": "https://laryngopedia.com/videofluoroscopic-swallowing-study-vfss/",
    "confirmed_live_fluoro": "Likely, per the captions: 'x-rays of barium passing through the throat' (cricopharyngeal before and after myotomy). The number of seconds and the frame rate are unknown, and no video ID or iframe URL is exposed; only the thumbnail filenames VFSS_web.webp and CD_Xray_web.webp.",
    "confirmed_licence": "Site: '© 2026 Laryngopedia. All rights reserved.' YouTube licence unknown.",
    "confirmed_views": "Lateral for the cricopharyngeal video (per the fetch summary; not stated verbatim); the barium esophagram view is unknown.",
    "usable_for_tracking": "poor",
    "corrections": "The channel RSS (UCOFcq1mWBXQt6JtO0HBn4jA) confirms the name Laryngopedia. Its latest 15 uploads include 9BWDwq6tFY4, 'Valium Diagnostic Trial for Cricopharyngeus Spasm' (2026-08-07); nothing indicates it is a barium study, so the earlier 'no swallow-study video' still holds in substance. Reachable through Bastian Voice Institute, but every rights are reserved."
   }
  ]
 },
 {
  "angle": "cc",
  "candidates": [
   {
    "url": "https://radiopaedia.org/cases/oblique-sublaminar-lumbar-puncture-1",
    "title": "Oblique sublaminar lumbar puncture (rID 90103), fluoroscopy study 107280",
    "channel": "Radiopaedia contributor Jeffrey Hocking",
    "year": "2021 (published 7 Jun 2021)",
    "duration": "61 frames in one stack; no frame rate stored",
    "procedure": "Left oblique sublaminar lumbar puncture at L3/4 for intrathecal drug delivery",
    "region": "lumbar (L3/4, roughly 2 vertebrae in a narrow collimated band)",
    "views": "unknown (Radiopaedia does not show view counts)",
    "live_fluoro": "yes, as a rotational C-arm projection sweep: 61 raw projections with the needle in place, gantry angle changing from frame to frame (frame 1 near-lateral, frame 31 oblique). It is a rotation, not a moving-table cine.",
    "licence": "CC BY-NC-SA 3.0 (Radiopaedia's site-wide licence at radiopaedia.org/licence; attribution 'Case courtesy of Jeffrey Hocking, Radiopaedia.org, rID: 90103'). The fetched case page showed only '© 2005–2026 Radiopaedia.org', so the case-level licence was not confirmed.",
    "quality": "616x480 JPEG; about two-thirds of each frame is black collimation; lossy; no overlays. The image filenames carry Siemens XA UIDs (1.3.12.2.1107.5.4.7...).",
    "reachable": "Yes: named contributor with a Radiopaedia profile; Radiopaedia can be contacted through the site",
    "evidence": "The case page gives study 107280 (Fluoroscopy) with the finding 'Left Oblique Sublaminar approach at L3/4 level. Anatomy is well demonstrated by the 3D reconstruction' and a CT study 107350 of the same acquisition. /studies/107280/stacks returns 61 images at 616x480 with a null plane. I viewed frames 1 and 31: both are raw projections with the needle, and the projection angle differs between them. The paired CT reconstruction means level labels could in principle be projected onto each frame, the same idea as the C-ArmLSpine CBCT sweeps."
   },
   {
    "url": "https://radiopaedia.org/cases/percutaneous-vertebroplasty",
    "title": "Percutaneous vertebroplasty (rID 21585), fluoroscopy study 21534",
    "channel": "Radiopaedia contributor Chris O'Donnell",
    "year": "2013 (published 1 Feb 2013)",
    "duration": "21 frames in series 1, plus 2 single stills",
    "procedure": "Right transpedicular vertebroplasty of L1 with barium-impregnated PMMA cement",
    "region": "thoracolumbar (L1 target, about 3-4 vertebral bodies in the field)",
    "views": "unknown",
    "live_fluoro": "Probably a fixed-C-arm fluoroscopy sequence of 21 frames. Frames 1 and 21 have the same lateral geometry, and cement builds up between them. The frame rate is unknown and the frames may be saved grabs rather than a full-rate loop.",
    "licence": "CC BY-NC-SA 3.0 (Radiopaedia site-wide licence); the case-level text was not rendered in the fetch",
    "quality": "1024x1024 JPEG, clean lateral view with the needle and an overlying catheter or lead; no burned-in text",
    "reachable": "Yes: named Radiopaedia contributor",
    "evidence": "The case page lists study 21534 (Fluoroscopy) with the caption 'Right transpedicular puncture with large bore needle entering the L1 vertebral body followed by injection of barium impregnated methyl methacrylate'. /studies/21534/stacks returns series 1 with 21 images at 1024x1024 and series 2 and 3 with 1 image each. I viewed frames 1 and 21: both lateral with the same field; frame 21 shows cement in the body."
   },
   {
    "url": "https://radiopaedia.org/cases/compression-fracture-with-vertebral-body-stenting",
    "title": "Compression fracture with vertebral body stenting (rID 24796), fluoroscopy study 25059",
    "channel": "Radiopaedia contributor Salem Bauones",
    "year": "2013 (published 12 Sep 2013)",
    "duration": "41 frames in series 2. Series 1 (32 'Axial' images) is cone-beam CT slices, not projections.",
    "procedure": "Percutaneous vertebral body stenting of an L1 compression fracture",
    "region": "thoracolumbar / lumbar (L1 plus the adjacent levels)",
    "views": "unknown",
    "live_fluoro": "Saved procedural frames with changing views (frame 1 lateral/oblique, frame 20 AP), not one continuous single-view loop. Whether any runs within the 41 frames are consecutive was not established.",
    "licence": "CC BY-NC-SA 3.0 (Radiopaedia site-wide licence); the case page itself showed only '© 2005–2026 Radiopaedia.org'",
    "quality": "1024x633 PNG, clean; AP frames show both stents and 2-3 vertebrae with ribs",
    "reachable": "Yes: named Radiopaedia contributor",
    "evidence": "The case page gives the Fluoroscopy study 25059 finding 'Compression fracture of L1, treated percutaneously by vertebral body stenting at day 5 of fracture'. The stacks endpoint returns series 1 with 32 images at 849x851 (I viewed frame 1: an axial CBCT slice) and series 2 with 41 images at 1024x633 (frame 1 lateral with the stent, frame 20 AP with bilateral stents)."
   },
   {
    "url": "https://radiopaedia.org/cases/lumbar-transforaminal-epidural-steroid-injection-fluoroscopic-guided",
    "title": "Lumbar transforaminal epidural steroid injection (fluoroscopic-guided) (rID 87907), study 104409",
    "channel": "Radiopaedia contributor Dai Roberts (institution listed as Musgrave Park)",
    "year": "2021 (published 20 Mar 2021)",
    "duration": "17-frame PA stack, plus oblique and lateral stills",
    "procedure": "Lumbar TFESI, supraneural approach, with a contrast run",
    "region": "lumbar (about 1 level visible)",
    "views": "unknown",
    "live_fluoro": "Yes, a short live contrast-injection loop of 17 frames at fixed geometry. The frame rate is not stored.",
    "licence": "CC BY-NC-SA 3.0 (Radiopaedia site-wide licence); the page showed only '© 2005–2026 Radiopaedia.org'",
    "quality": "1246x1156 JPEG, tightly collimated square inside black borders, noisy low-dose frames. Only part of one level is visible, so it is weak for level naming.",
    "reachable": "Yes: named contributor with an institution",
    "evidence": "/studies/104409/stacks returns an Oblique stack (1 image), a Lateral stack (1 image) and a PA stack of 17 images at 1246x1156. I viewed frames 1 and 17: same geometry and needle, with contrast appearing along the nerve root by frame 17."
   },
   {
    "url": "https://radiopaedia.org/cases/s1-transforaminal-epidural-steroid-injection-fluoroscopic-guided",
    "title": "S1 transforaminal epidural steroid injection (fluoroscopic guided) (rID 89588), study 106613",
    "channel": "Radiopaedia contributor Dai Roberts",
    "year": "2021 (published 14 May 2021)",
    "duration": "16-frame stack, plus 2 stills",
    "procedure": "S1 TFESI through the posterior S1 foramen with a contrast run",
    "region": "sacrum / L5-S1",
    "views": "unknown",
    "live_fluoro": "Yes, a short live contrast loop of 16 frames at fixed geometry",
    "licence": "CC BY-NC-SA 3.0 (Radiopaedia site-wide licence)",
    "quality": "1328x1242 JPEG, tight collimation and noisy; little vertebral context",
    "reachable": "Yes: named contributor",
    "evidence": "The caption reads 'Using a 22 gauge Quincke needle, the posterior S1 neural foramina was cannulated under fluoroscopic guidance...'. /studies/106613/stacks returns stacks of 1, 1 and 16 images. I viewed frames 1 and 16: same field, contrast filling the S1 root by frame 16."
   },
   {
    "url": "https://radiopaedia.org/cases/lumbar-transforminal-epidural-steroid-injection-fluoroscopic-guided",
    "title": "Lumbar transforminal epidural steroid injection (fluoroscopic guided) (rID 87287), study 103573",
    "channel": "Radiopaedia contributor Dai Roberts (Musgrave Park)",
    "year": "2021 (published 26 Feb 2021)",
    "duration": "14-frame PA stack, plus oblique and lateral stills",
    "procedure": "Left L5 TFESI, infrapedicular approach",
    "region": "lumbar (L4/5-L5)",
    "views": "unknown",
    "live_fluoro": "Probably a live contrast loop (14 frames at the same size, PA) by analogy with the author's two other cases. Frames were not viewed, so this is unverified.",
    "licence": "CC BY-NC-SA 3.0 (Radiopaedia site-wide licence)",
    "quality": "1406x1200 JPEG; collimation unknown",
    "reachable": "Yes: named contributor",
    "evidence": "The case page lists studies 103573 and 103574. /studies/103573/stacks returns Oblique (1 image), Lateral (1 image) and PA (14 images at 1406x1200)."
   },
   {
    "url": "https://commons.wikimedia.org/wiki/File:Fluoroscopically-guided-transforaminal-epidural-dry-needling-for-lumbar-spinal-stenosis-using-a-1471-2474-11-180-S1.ogv",
    "title": "Fluoroscopically guided transforaminal epidural dry needling for lumbar spinal stenosis using a specially designed needle (BMC Musculoskelet Disord 2010;11:180, Additional file 1)",
    "channel": "Wikimedia Commons (Open Access Media Importer); authors Ahn K, Jhun HJ, Lim TK, Lee YS",
    "year": "2010",
    "duration": "2 min 44 s (163.7 s)",
    "procedure": "Transforaminal epidural dry needling for lumbar stenosis",
    "region": "lumbar",
    "views": "unknown",
    "live_fluoro": "unknown. The poster frame is an edited title card ('Procedure: Local Anesthesia') over a procedure photograph, so this is an edited presentation video. Whether it contains live fluoroscopy clips or only fluoroscopic stills was not established without playing it.",
    "licence": "Creative Commons Attribution 2.0 Generic (CC BY 2.0), as stated on the Commons file page; Europe PMC lists the article (PMC2927508) as CC BY",
    "quality": "640x480 Ogg Theora, edited with text overlays",
    "reachable": "Yes: Chronic Pain Management Centre, CHA Biomedical Centre, Kangnam CHA Hospital, CHA University, Seoul",
    "evidence": "The Commons file page gives the description, CC BY 2.0, the categories Fluoroscopy / Human lumbar vertebrae / Videos of neurosurgical procedures, and 640x480. The imageinfo API gives a duration of 163.71 s. I viewed the poster thumbnail. Europe PMC gives the affiliation and the CC BY licence. This is the only spine-fluoroscopy video on Commons that I found."
   },
   {
    "url": "https://commons.wikimedia.org/wiki/File:Fluoroscopy_of_normal_barium_swallow.ogg",
    "title": "Fluoroscopy of normal barium swallow (inverted)",
    "channel": "Wikimedia Commons user Ptrump16 (own work)",
    "year": "2022 (4 Feb 2022)",
    "duration": "28.7 s at about 3 fps (frame time 333.3 ms), so roughly 86 frames",
    "procedure": "Barium swallow (esophagram); the spine appears only incidentally",
    "region": "cervical and upper thoracic (roughly C3 to T6, seen through the barium column)",
    "views": "unknown",
    "live_fluoro": "Yes, continuous fluoroscopy for about 29 s at about 3 fps. The view is AP/slightly oblique, not lateral.",
    "licence": "Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0), as stated on the file page",
    "quality": "1024x1024, grey-scale inverted, round image-intensifier edge. The vertebrae are faint behind the barium, so this is marginal for level naming.",
    "reachable": "Partly: a Wikimedia username only, who also uploaded CC BY-SA lumbar MRI clips",
    "evidence": "The Commons file page gives the description, author, date, 1024x1024, 28.67 s, frame time 333.3 ms and CC BY-SA 4.0. I viewed the poster frame: an AP/oblique neck and upper chest with the esophagus opacified and the cervicothoracic spine visible behind it."
   },
   {
    "url": "https://www.youtube.com/watch?v=T3vsvpkRR14",
    "title": "Video Fluoroscopy - Cervical Spine - S_M_VF_RFC_7_17_12.wmv",
    "channel": "Samuel Ralls (Sam) (@SamuelRallsDC)",
    "year": "unknown (the filename suggests a recording dated 7/17/12)",
    "duration": "unknown",
    "procedure": "Cervical videofluoroscopy (motion study; inferred from the title only)",
    "region": "cervical",
    "views": "unknown",
    "live_fluoro": "unknown. The title says videofluoroscopy, but the page could not be read to confirm.",
    "licence": "unknown (the watch page could not be read, so the CC or Standard YouTube licence field was not seen)",
    "quality": "unknown",
    "reachable": "Probably: a named uploader whose handle suggests a chiropractor (DC)",
    "evidence": "The title and URL came from the one successful WebSearch. YouTube oEmbed returned the title and author_name 'Samuel Ralls (Sam)' with author_url youtube.com/@SamuelRallsDC. WebFetch of the watch page returned only YouTube's footer, so the licence, duration and description are unverified. It is listed because it is the only YouTube hit that is plausibly continuous spine cine."
   }
  ],
  "notes": "Short answer: I could check Wikimedia Commons and Radiopaedia properly, but I could not check YouTube's Creative Commons licences with the tools available.\n\n**Why YouTube could not be checked**\n- WebFetch of YouTube watch pages and search result pages (including the Creative Commons filter, sp=EgIwAQ%3D%3D) returns only the site footer. The page content is rendered by JavaScript, so the licence field never appears.\n- I tried two Invidious front-ends (inv.nadeko.net, yewtu.be). The network blocks both: their certificates resolve to blocked.cvnt.net. I did not try to get around that block.\n- The session's WebSearch budget ran out (200 of 200) after this agent's third search. After that I did not run searches through other engines, to stay within the budget.\n- oEmbed works, but it returns only the title and channel, not the licence or duration.\n- So none of the YouTube candidates is confirmed as Creative Commons. Two practical ways to do it:\n  - A person searches YouTube with Filters → Features → Creative Commons, using terms like \"fluoroscopy lumbar\", \"C-arm spine\", \"vertebroplasty fluoroscopy\", \"digital motion x-ray\", \"videofluoroscopy cervical\".\n  - Call YouTube Data API v3 search.list with videoLicense=creativeCommon (needs an API key).\n- YouTube's only CC option is CC BY 3.0, so any hit would be reusable with attribution.\n- Other YouTube URLs from the one search, all with unknown licence and not listed as candidates:\n  - xmwqcnN_r3g: JBJS JOPA sacroiliac joint injection, 2022; a publisher, almost certainly Standard licence.\n  - TETqUknlgyo: \"Fluoroscopy-Guided Injections for Muscle, Bone, and Joint Pain\".\n  - jJqNzMHEzVk: oEmbed returned 403, so embedding is disabled or the video is gone.\n\n**Wikimedia Commons: essentially nothing on the spine**\n- I searched with the API (fluoroscopy, fluoroscopic, vertebra, lumbar, cervical spine, C-arm/cineradiography/videofluoroscopy, intervertebral, \"x-ray video\") and listed the Fluoroscopy, X-ray videos, Human lumbar vertebrae and Videos of neurosurgical procedures categories.\n- The only spine-fluoroscopy video is the 2010 BMC dry-needling movie (CC BY 2.0), and it is an edited presentation.\n- Excluded:\n  - \"X-ray Body in Motion - Yoga by Hybrid Medical Animation\": an animation.\n  - MaskMovie.ogv: a public-domain cone-beam CT mask run of the skull; only the upper cervical spine is at the edge.\n  - The atlantoaxial case-report video (CC BY 3.0): I checked the poster and it is camera footage of a patient in a halo.\n  - The Brain+C-spine webm series: MRI.\n\n**Radiopaedia: the useful source here, but small and non-commercial**\n- A case search filtered to the Fluoroscopy modality returns at most about 15 cases per term. I ran spine, lumbar, cervical, vertebral, vertebroplasty, kyphoplasty, facet, sacroiliac, spinal, myelogram, discogram and intraoperative.\n- For every spine case I read the undocumented JSON endpoint https://radiopaedia.org/studies/{study_id}/stacks, which gives the frame count, plane and size of each stack. I viewed individual still frames only to classify stacks; no video was downloaded.\n- Only 6 cases have multi-frame stacks; they are listed as candidates.\n- The best is rID 90103: a 61-projection rotational C-arm sweep of L3/4 with a paired CT reconstruction. It is rotation only.\n- Next is rID 21585: 21 lateral frames at fixed geometry during L1 vertebroplasty.\n- The three epidural-injection loops (14, 16 and 17 frames) are genuinely live but so tightly collimated that level naming is barely possible.\n- Still-only cases, excluded:\n  - L5 nerve root block rID 5619: 6 stills.\n  - Fluoroscopic LP rID 45064: 3 stills.\n  - Interlaminar ESIs rID 75868 and 75490: 4-5 stills.\n  - Cervical interlaminar ESI rID 77352: 3 stills.\n  - Kyphoplasty T11-L2 rID 170350: 2 stills.\n  - Multilevel vertebroplasty rID 53905: 3 stills.\n  - T8-9 dislocation rID 174074: 1 lateral still.\n  - C4/5 ACDF intraoperative rID 61247: 1 still.\n  - Epidural blood patch rID 45920: 4 stills.\n  - S1/S2 nerve root injections rID 12625, 12626, 12665: 2-6 stills.\n  - SI joint rID 65802, Scottie-dog facet rID 36087, Schmorl discogram rID 35827: 1 still each.\n  - Epidural abscess rID 232785: 1 intraoperative still.\n\n**Licence caveat**\n- Radiopaedia content is CC BY-NC-SA 3.0 (radiopaedia.org/licence). The fetched case pages showed only \"© 2005–2026 Radiopaedia.org\", so I could not confirm a case-level licence line.\n- The non-commercial and share-alike terms suit a research test set in a paper. They would not suit validation data for the 510(k) product track unless the contributor grants separate permission; contributors keep full rights, so asking them is realistic.\n\n**Overall**\n- Openly licensed, continuous, level-nameable spine fluoroscopy video is close to nonexistent on Commons and Radiopaedia. The two multi-frame cases above (rID 90103 and 21585) are the only usable items, and neither involves cranio-caudal translation.\n- YouTube remains unchecked for licence, not ruled out.",
  "verify": [
   {
    "url": "https://radiopaedia.org/cases/oblique-sublaminar-lumbar-puncture-1",
    "confirmed_live_fluoro": "Yes, as a rotational C-arm sweep, not a fixed-view cine. /studies/107280/stacks returns one series of 61 JPEGs at 616x480, with plane_projection null and no timing fields. I viewed frames 1, 31 and 61. All three are raw projections with the needle in, and the gantry angle changes between them: frame 1 near-lateral, frame 31 oblique, frame 61 near-AP/oblique. The needle foreshortens as the angle changes. Frame 61 is not the opposite lateral, so it is unknown whether the 61 frames are the whole sweep or a subset. The frame rate is unknown.",
    "confirmed_licence": "The case page shows no case-level licence, only the site footer. radiopaedia.org/licence says Radiopaedia content is published under 'Creative Commons Non-Commercial Attribution, Sharealike license (currently CC-NC-BY-SA 3.0)'. Attribution must give the contributor, Radiopaedia.org and the rID. The contributor retains full rights and 'can authorize third-party commercial use without Radiopaedia permission'.",
    "confirmed_views": "Varies within the sweep (near-lateral, then oblique, then near-AP/oblique). This is a rotation with no cranio-caudal translation.",
    "usable_for_tracking": "poor",
    "corrections": "1) Collimation: I measured about 58% of every frame as black. The exposed band is roughly 616x200 px and shows only about 2 lumbar bodies plus partial neighbours, so there is little context for naming a level beyond the caption anchor ('L3/4 level'). 2) The claim that the paired CT would let labels be projected onto each frame is overstated. CT study 107350 is not a volume: it is 43 curated 1024x1024 images in three stacks (12 'Axial', 19 with no plane, 12 'Coronal'). No gantry geometry is published, so projecting labels would need a 2D/3D registration that these images may not support. 3) Display polarity is dense = dark: the needle is black and bowel gas is white. 4) Everything else checks out: Jeffrey Hocking, published 7 Jun 2021, study 107280 with the finding 'Left Oblique Sublaminar approach at L3/4 level. Anatomy is well demonstrated by the 3D reconstruction.' It is real sequential projection data, but a narrow, low-resolution rotation of 2-3 vertebrae, so it is weak as a frame-to-frame naming test."
   },
   {
    "url": "https://radiopaedia.org/cases/percutaneous-vertebroplasty",
    "confirmed_live_fluoro": "Yes, a short fixed-geometry fluoroscopy sequence. Series 1 has 21 frames at 1024x1024, with no timing fields and a null plane. I viewed frames 1, 7, 14 and 21. The geometry is the same throughout, but there is small real motion between frames: the shape of the lung-base or bowel-gas lucency changes and the overlying lead or catheter shifts. So these are separate live exposures, not duplicates. Cement is absent in frames 1 and 7, appears by frame 14 and has grown by frame 21. The image ids are not contiguous (2907043 to 2907070 across 21 positions), so the published frames may be a selection from a longer run. The frame rate is unknown.",
    "confirmed_licence": "The case page shows only '© 2005–2026 Radiopaedia.org'. No case-level licence is shown. The site-wide terms apply: CC BY-NC-SA 3.0, with the contributor retaining rights.",
    "confirmed_views": "Lateral (transpedicular needle entering from posterior; endplates slightly doubled, so mildly off-true-lateral). Series 2 and 3 are one still each.",
    "usable_for_tracking": "possible",
    "corrections": "1) The view is lateral, not unknown. 2) The frames are confirmed live sequential exposures, not copies. 3) The field shows about 2.5-3 vertebral bodies: L1 with the needle, the body below, and part of the one above. The caption anchors the level ('needle entering the L1 vertebral body'). 4) The overlying object is an ECG electrode with its lead, plus a curved line. 5) Display polarity is dense = dark (needle and cement black). 6) There is almost no translation or rotation, so this tests temporal stability under a static view, not tracking through motion. Everything else checks out: Chris O'Donnell, 1 Feb 2013, 85-year-old female; the case also has CT 21536 and MRI 21537."
   },
   {
    "url": "https://radiopaedia.org/cases/compression-fracture-with-vertebral-body-stenting",
    "confirmed_live_fluoro": "Yes, but it is a rotational C-arm spin, not saved procedural frames. Series 2 has 41 PNGs at 1024x633. I viewed positions 1, 2, 3, 10, 11, 20, 30 and 41. Frames 1-3 are near-identical lateral views that differ only in noise. Frames 10 and 11 are obliques a few degrees apart. Frame 20 is a true AP with both stents and ribs. Frame 30 is oblique from the opposite side, and frame 41 is lateral from the opposite side (the view is mirrored and the skin edge has switched sides). So the gantry sweeps about 180° from lateral through AP to the opposite lateral. The image ids widen from +1 to about +3 per position, so this may be a subsample of the native spin. The frame rate is unknown.",
    "confirmed_licence": "The case page shows only '© 2005–2026 Radiopaedia.org'. No case-level licence is shown. The site-wide terms apply: CC BY-NC-SA 3.0, with the contributor retaining rights.",
    "confirmed_views": "Continuous sweep: lateral, then oblique, then AP (frame 20), then oblique, then opposite lateral (frame 41).",
    "usable_for_tracking": "possible",
    "corrections": "1) Correct 'saved procedural frames with changing views, not one continuous single-view loop'. This is one continuous ~180° rotational acquisition after stenting. Series 1 (32 images, plane labelled 'Axial', 849x851) is the cone-beam CT reconstructed from it. The one image I viewed (position 16) is actually a sagittal reformat with an orientation-cube overlay, despite the 'Axial' label. 2) About 3 vertebrae are in the field, with ribs visible on the AP frames. L1 carries the stents, and the caption anchors it ('Compression fracture of L1'). 3) Display polarity is dense = dark (stents black). 4) Everything else checks out: Salem Bauones, 12 Sep 2013, 25-year-old female; the case also has X-ray 25062, CT 25060 and MRI 25061. It is the best of the Radiopaedia set for a rotation-tracking test (view-change robustness), but there is no cranio-caudal translation and only 41 frames."
   },
   {
    "url": "https://radiopaedia.org/cases/lumbar-transforaminal-epidural-steroid-injection-fluoroscopic-guided",
    "confirmed_live_fluoro": "Yes, a short fixed-geometry contrast run. The PA stack has 17 JPEGs at 1246x1156 with sequential filenames 0..16 and contiguous image ids (54666262 to 54666278), consistent with a multi-frame export. I viewed frames 1, 2 and 17. The geometry and needle are identical, and contrast appears along the root by frame 17. The frame rate is unknown.",
    "confirmed_licence": "No case-level licence is shown on the page. The site-wide terms apply: CC BY-NC-SA 3.0, with the contributor retaining rights.",
    "confirmed_views": "The stacks are labelled Oblique (1 image, 1214x1058), Lateral (1 image, 1208x1264) and PA (17 images). Study 104410 is one more PA still.",
    "usable_for_tracking": "poor",
    "corrections": "1) Views are established from the stack labels: the loop is PA. 2) The exposed square is roughly 935x890 px inside black borders (about 40% of the frame black). It shows parts of two bodies and one disc space around L4/5, with heavy low-dose noise and no motion, so it is not usable for naming levels beyond the caption. 3) Display polarity is dense = dark. 4) The caption fragment confirmed: 'Using a supraneural oblique approach and a 22 gauge Quincke needle'. The 50-year-old male had left L5 radicular symptoms from an L4/5 bulge. Contributor Dai Roberts, Musgrave Park, 20 Mar 2021."
   },
   {
    "url": "https://radiopaedia.org/cases/s1-transforaminal-epidural-steroid-injection-fluoroscopic-guided",
    "confirmed_live_fluoro": "Yes, a short fixed-geometry contrast run. Series 3 has 16 JPEGs at 1328x1242 with sequential filenames 0..15. I viewed frames 1 and 16: the needle and geometry are identical, and contrast outlines the S1 root by frame 16. The frame rate is unknown.",
    "confirmed_licence": "The page says only that the content is available under Radiopaedia's licensing terms. No case-level licence is shown. The site-wide terms apply: CC BY-NC-SA 3.0, with the contributor retaining rights.",
    "confirmed_views": "The 16-frame stack has no plane label. From the image it is a PA/slightly oblique view of the posterior sacrum and S1 foramen. Series 1 has no plane label (1 still); series 2 is 'Lateral' (1 still).",
    "usable_for_tracking": "poor",
    "corrections": "1) The field is almost entirely sacrum and S1 foramen, with at most the edge of the L5/S1 region, and there is heavy noise. There are essentially no whole vertebrae to track or name, so this is close to unusable. 2) Views are partly established: series 2 is labelled Lateral and the loop is unlabelled PA-type. 3) Display polarity is dense = dark. 4) Everything else checks out: Dai Roberts, Musgrave Park, 14 May 2021, 40-year-old male with a left L5/S1 subarticular extrusion; follow-up study 106614."
   },
   {
    "url": "https://radiopaedia.org/cases/lumbar-transforminal-epidural-steroid-injection-fluoroscopic-guided",
    "confirmed_live_fluoro": "Yes, now verified (the prior entry had not viewed any frames). The PA stack has 14 JPEGs at 1406x1200 with sequential filenames 0..13. I viewed frames 1 and 14: the geometry and needle are identical, and a contrast column appears along the root by frame 14. The frame rate is unknown.",
    "confirmed_licence": "No case-level licence is shown on the page. The site-wide terms apply: CC BY-NC-SA 3.0, with the contributor retaining rights.",
    "confirmed_views": "The stacks are labelled Oblique (1 image, 1300x1218), Lateral (1 image, 1370x1186) and PA (14 images). Study 103574 is post-injection imaging.",
    "usable_for_tracking": "poor",
    "corrections": "1) 'Probably a live contrast loop, unverified' is now verified. 2) Collimation: the exposed rectangle is roughly 1070x900 px inside black borders. It shows the L4/5 disc, part of L4, L5, a spinous process and the iliac crest, so about 1.5 levels, with no motion. 3) Display polarity is dense = dark. 4) Everything else checks out: Dai Roberts, Musgrave Park, 26 Feb 2021, left L5 infrapedicular approach, 40-year-old male with an L4/5 subarticular lesion on MRI."
   },
   {
    "url": "https://commons.wikimedia.org/wiki/File:Fluoroscopically-guided-transforaminal-epidural-dry-needling-for-lumbar-spinal-stenosis-using-a-1471-2474-11-180-S1.ogv",
    "confirmed_live_fluoro": "No evidence of any. I sampled server-generated thumbnails at 30, 60, 80, 90, 100, 110, 120, 125, 140 and 155 s (Commons seek thumbnails; the video was not downloaded). They show: a bullet-point text slide (30 s), a CT sagittal/coronal/axial slide (60 s), captioned procedure-photo slides (80, 90, 110 s), camera video of the operator's hands and the needle on the patient's back (100, 125, 140, 155 s), and at 120 s a composite slide of two procedure photos and two small circular fluoroscopic stills (one AP, one lateral) under a caption. Fluoroscopy appears only as stills embedded in a slide. Frames between the samples were not seen.",
    "confirmed_licence": "Creative Commons Attribution 2.0 Generic (CC BY 2.0), as stated on the Commons file page and in the API (LicenseShortName 'CC BY 2.0'). PMC2927508 says 'distributed under the terms of the Creative Commons Attribution License (http://creativecommons.org/licenses/by/2.0)'.",
    "confirmed_views": "In the one fluoroscopic composite seen (120 s): AP and lateral lumbar stills. The article says 'A C-arm fluoroscope was used to identify the bony landmark in the anteroposterior view... Then the C-arm was turned to the lateral view'.",
    "usable_for_tracking": "not",
    "corrections": "1) This is an edited slideshow-plus-camera presentation (PMC calls Additional file 1 'Windows Media Video... A movie demonstrating the technique'). I found no live fluoroscopy at any of the ten sampled times. 2) The corresponding author and contact differ from the prior entry: Hyung-Joon Jhun, Centre for Interventional Pain Management, Daejeon Woori Hospital, Daejeon, Korea, [e-mail withheld] (from PMC2927508). That is not the CHA Kangnam affiliation listed before. 3) Duration (163.71 s), 640x480 and CC BY 2.0 are confirmed."
   },
   {
    "url": "https://commons.wikimedia.org/wiki/File:Fluoroscopy_of_normal_barium_swallow.ogg",
    "confirmed_live_fluoro": "Yes, continuous. The file is 28.67 s at 3 fps (Frame Time 333.3333 msec, from a GE Digital Fluoroscopy unit), roughly 86 frames at 1024x1024. I sampled seek thumbnails at 2, 15 and 27 s. The field moves cranio-caudally during the run: at 2 s it shows the face, mandible and cervical spine in AP; at 15 s the lower cervical to upper thoracic spine with the bolus at the thoracic inlet, slightly rotated; at 27 s the lower thoracic spine with the distal oesophagus, GE junction and gastric fundus. So the table or tower pans down the spine following the bolus.",
    "confirmed_licence": "Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). The API gives UsageTerms 'Creative Commons Attribution-Share Alike 4.0'. Author Ptrump16, 'Own work', dated 2022-02-04.",
    "confirmed_views": "AP, with mild obliquity or rotation mid-run. It pans cranio-caudally from the cervical spine to the lower thoracic spine.",
    "usable_for_tracking": "possible",
    "corrections": "1) Region: the prior entry had roughly C3 to T6. The sampled frames show the field travelling from the cervical spine (face and mandible in view) down to the lower thoracic spine at the GE junction, probably around T10-T11 (estimated). 2) Most importantly, this is the only candidate with genuine cranio-caudal translation along the spine during continuous fluoroscopy. Because it starts in the cervical spine, levels could in principle be counted down frame to frame. 3) Caveats: 3 fps; the greyscale is inverted (the title says '(inverted)': barium and bone dark); vertebrae are faint behind the mediastinum and barium; the round image-intensifier edge is cropped; heavy Theora compression (1.3 MB). 4) Reachability is a Commons username only. Everything else checks out."
   },
   {
    "url": "https://www.youtube.com/watch?v=T3vsvpkRR14",
    "confirmed_live_fluoro": "Very likely, from YouTube's own frame grabs. The watch, embed, mobile and channel pages all rendered only YouTube's footer through WebFetch, so the page itself could not be read. YouTube's auto-generated thumbnails (i.ytimg.com/vi/T3vsvpkRR14/1.jpg, 2.jpg and 3.jpg) are frames taken from the video at about 25%, 50% and 75% of its length. I viewed them and hqdefault.jpg. 1.jpg is the intensifier circle with a collimator blade and almost no anatomy; 2.jpg is a lateral cervical spine; 3.jpg is an AP view with rectangular collimation. hqdefault.jpg is a clean lateral cervical fluoroscopy frame inside the round intensifier field, showing C1 to about C6/C7, with no monitor bezel. Changing views at different time points in a clip titled 'Video Fluoroscopy' fit a recorded motion study. How many seconds are continuous is unknown.",
    "confirmed_licence": "unknown. The licence field was not visible because the watch page did not render. oEmbed does not report a licence.",
    "confirmed_views": "Lateral cervical (hqdefault and the 50% frame) and AP (75% frame), from thumbnails only.",
    "usable_for_tracking": "possible",
    "corrections": "1) Live fluoroscopy was previously 'unknown'. It is now very likely: the thumbnails are frames from the video itself and show a lateral cervical spine inside an image-intensifier circle, then an AP view later in the clip. 2) Quality clue: maxresdefault.jpg returns 404, which usually means no 720p+ upload, so this is probably SD 4:3. The .wmv filename and the clean intensifier circle suggest a direct digital export rather than a phone-filmed monitor. That is an inference, not verified. 3) Duration, upload date, description and licence are still unknown. oEmbed confirms the title 'Video Fluoroscopy - Cervical Spine - S_M_VF_RFC_7_17_12.wmv' and the author 'Samuel Ralls (Sam)' at youtube.com/@SamuelRallsDC. 4) Method note for further YouTube checks: WebFetch cannot read YouTube watch pages here, but oEmbed plus the i.ytimg.com 1/2/3.jpg auto-thumbnails confirm fluoroscopic content without downloading the video. The licence still has to be read in a browser. 5) Cervical only, so it is lower priority than lumbar. The WebSearch budget ran out, so no additional YouTube candidates could be found in this pass."
   }
  ]
 },
 {
  "angle": "libraries",
  "candidates": [
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8463391/",
    "title": "Role of Conventional Dynamic Myelography for Detection of High-Flow Cerebrospinal Fluid Leaks: Optimizing the Technique (Videos 1-4)",
    "channel": "Clinical Neuroradiology (Springer), supplementary files hosted on PMC (/articles/instance/8463391/bin/62_2020_943_MOESM1..4_ESM.mp4)",
    "year": "2020 online / 2021 issue",
    "duration": "unknown; file sizes 1.3 MB, 6.9 MB, 5 MB, 3 MB",
    "procedure": "Conventional (unsubtracted) dynamic myelography on a tilting table, looking for CSF leaks",
    "region": "Mostly thoracic (49 of 60 patients); also cervical (4) and lumbar (7)",
    "views": "Lateral projection with the patient prone; AP projection in lateral decubitus",
    "live_fluoro": "yes: pulsed fluoroscopy at 7.5 frames/s; the paper gives a mean fluoroscopy time of 7.8 min. Each clip probably runs for several to tens of seconds (not measured)",
    "quality": "Native fluoroscopy export, not a filmed monitor. Contrast column is present. Detector pans cranially, so consecutive frames overlap during craniocaudal translation",
    "licence": "Creative Commons Attribution 4.0 International License (CC BY 4.0)",
    "reachable": "yes: Inselspital, Bern University Hospital, neuroradiology and neurosurgery (Piechowiak ... Beck, Gralla, Dobrocky); named academic authors",
    "evidence": "PMC page. Video 2 caption: 'Video sequence from dynamic myelography in prone position with progressive tilt of the table'. Methods: 'The default frame rate was 7.5 f/s, and the detector was slowly moved in a cranial direction following the leading edge of the contrast medium'; 'Lateral projection was used in patients in the prone position and anteroposterior projection in patients in lateral decubitus'. Licence stated on the page. Videos not watched."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11328828/",
    "title": "Examination of the Pediatric Cervical Spine Under Anesthesia (Video 1: cervical EUA under fluoroscopy)",
    "channel": "Cureus, video hosted on PMC",
    "year": "2024",
    "duration": "unknown; 7.3 MB mp4",
    "procedure": "Dynamic fluoroscopic examination under anaesthesia: distraction, flexion, extension and translation of the paediatric cervical spine",
    "region": "Cervical, focused on C0-C1-C2 (craniocervical junction); paediatric",
    "views": "Lateral assumed (flexion/extension/translation assessment); projection not stated explicitly",
    "live_fluoro": "yes. The text says the surgeon performs manoeuvres 'while obtaining live fluoroscopy' and 'we typically record the live images'. Seconds unknown",
    "quality": "Recorded live images, probably a C-arm export. Resolution unknown. Frames show real motion, not a translating detector",
    "licence": "Creative Commons Attribution License CC-BY 4.0",
    "reachable": "yes: Starship Children's Hospital, Auckland, NZ (Montgomery, Crawford et al.)",
    "evidence": "PMC page. Caption: 'Cervical EUA was performed under fluoroscopy with special attention paid to the CO/C1 joint showing normal distraction, normal flexion and extension, normal translation, and pathological anteroposterior (AP) translation.' Text: 'The surgeon manually performs distraction, flexion, extension, and translation maneuvers while obtaining live fluoroscopy'. Not watched."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10242080/",
    "title": "Re-expansion of vertebral compression fractures in patients with multiple myeloma with percutaneous vertebroplasty using SpineJack implants (Video S1)",
    "channel": "Frontiers in Surgery, supplementary file on PMC",
    "year": "2023",
    "duration": "unknown; 15.7 MB .avi",
    "procedure": "Percutaneous vertebral augmentation (SpineJack) plus PMMA cementation",
    "region": "Thoracic and lumbar (series T6-L5; the Video S1 patient had dorsal pain, so the level is likely thoracic)",
    "views": "unknown (not stated in caption)",
    "live_fluoro": "likely yes. Caption: 'Fluoroscopic stages of insertion, opening and cementation of jack plug implants'. Methods: cement 'slowly injected, under real time fluoroscopy'. Seconds unknown",
    "quality": "AVI export, probably from the angiography suite. Resolution unknown",
    "licence": "Creative Commons Attribution License (CC BY)",
    "reachable": "yes: Division of Interventional Radiology, Oncological Hospital A. Businco, Cagliari (C. Pusceddu et al.)",
    "evidence": "PMC page. Supplementary Video S1 caption quoted above. Licence stated. 'The fluoroscopic guidance allowed us a real-time synchronous opening of the implants'. Not watched."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8282264/",
    "title": "CT Scan and Clinical Outcomes of Novel Lateral-Oblique Percutaneous Sacroiliac Joint Fixation (Video 1: fluoroscopy steps and markings)",
    "channel": "Cureus, video on PMC (cdn.ncbi.nlm.nih.gov/pmc/blobs/80e9/8282264/.../cureus-0013-00000016408-i01-pmcvs_normal.mp4)",
    "year": "2021",
    "duration": "unknown; 6.7 MB mp4",
    "procedure": "Percutaneous lateral-oblique sacroiliac joint fixation",
    "region": "Sacrum/pelvis (S1, S2)",
    "views": "AP, 30-degree oblique, 15-degree outlet tilt, 45-degree inlet, lateral",
    "live_fluoro": "unknown. The caption says 'Video showing fluoroscopy steps and markings'; could be a sequence of saved shots",
    "quality": "unknown",
    "licence": "Creative Commons Attribution License (unrestricted use with credit)",
    "reachable": "yes: Kingsley R. Chin, Less Exposure Surgery (LES) Clinic, Hollywood FL / FIU",
    "evidence": "PMC page: video caption and licence. Text lists 'Fluoroscopic anteroposterior (A-P) views, 30-degree oblique views, and 15-degree pelvic outlet tilt views were obtained'. Not watched."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8687599/",
    "title": "Osteoporotic Thoracolumbar Vertebral Fractures With Neurological Deficit Treated by Balloon Kyphoplasty Augmented with Minimally Invasive Posterior Hook Stabilization (Video 1)",
    "channel": "Cureus, video on PMC (cureus-0013-00000020505-i01-pmcvs_normal.mp4)",
    "year": "2021",
    "duration": "unknown; 3.7 MB mp4",
    "procedure": "Balloon kyphoplasty plus percutaneous posterior hook stabilization",
    "region": "Thoracolumbar (T11-L1)",
    "views": "unknown",
    "live_fluoro": "unknown. The text places each step 'under fluoroscopy'; the video covers the whole procedure",
    "quality": "Small file (3.7 MB), so probably short or low resolution",
    "licence": "Creative Commons Attribution License (CC-BY)",
    "reachable": "yes: Toshio Doi, Orthopaedic Surgery, Hiroshima Red Cross Hospital & Atomic-bomb Survivors Hospital",
    "evidence": "PMC page: Video 1 caption and licence. 'The location of the T12 pedicles, T11 spinous process, and L1 lamina were marked under fluoroscopy'. Not watched."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4852439/",
    "title": "Evaluation of surgical outcome of Jack vertebral dilator kyphoplasty for osteoporotic vertebral compression fracture: 218 cases (Additional file 1: Surgical procedure)",
    "channel": "Journal of Orthopaedic Surgery and Research (BMC), file on PMC",
    "year": "2016",
    "duration": "unknown; 126.6 MB .MOV",
    "procedure": "Kyphoplasty with a Jack vertebral dilator plus cement",
    "region": "Thoracolumbar (series T10-L5, L1 most frequent)",
    "views": "unknown",
    "live_fluoro": "unknown. The caption is only 'Surgical procedure'. The large MOV may mix OR camera and fluoro-monitor footage",
    "quality": "Large MOV, probably camera-filmed. Unverified",
    "licence": "Creative Commons Attribution 4.0 International License (CC-BY-4.0)",
    "reachable": "yes: Department of Orthopaedic Surgery, First Affiliated Hospital of Nanjing Medical University (G. Yin, corresponding author, not verified)",
    "evidence": "PMC page: Additional File 1 (MOV, 126.6 MB, caption 'Surgical procedure') and the CC BY 4.0 licence. Cement filling was stopped relative to the posterior wall, which implies fluoroscopic monitoring. Not watched."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7703990/",
    "title": "Physiologic Decompression of Lumbar Spinal Stenosis ... Trans-Kambin OLLIF (Video 1 lateral fluoroscopic view; Video 2 AP fluoroscopic view)",
    "channel": "Cureus, videos on PMC (cureus-0012-00000011716-i01.mp4 / -i02.mp4)",
    "year": "2020",
    "duration": "very short: each file is 50.9 KB",
    "procedure": "Trans-Kambin oblique lateral lumbar interbody fusion (OLLIF)",
    "region": "Lumbar (series T12-S1)",
    "views": "Lateral (Video 1) and AP (Video 2), separate clips",
    "live_fluoro": "unknown. The clips are explicitly fluoroscopic, but at 50.9 KB they are likely a few frames or saved shots in sequence",
    "quality": "Very low: tiny files",
    "licence": "Creative Commons Attribution License (unrestricted use with credit)",
    "reachable": "yes: Hamid Abbasi, Inspired Spine Health, Minneapolis / Tristate Brain and Spine Institute",
    "evidence": "PMC page. Captions 'Lateral fluoroscopic view of physiologic decompression ...' and 'AP fluoroscopic view ...'; 'The steps of OLLIF under fluoroscopy are shown in Figure 2, Video 1, and Video 2.' File sizes as listed. Not watched."
   },
   {
    "url": "https://youtu.be/_1xMxFZa6tU",
    "title": "Dorsal root ganglion stimulation for treatment of complex regional pain syndrome of the foot (Neurosurgical Focus: Video, PMC9542308)",
    "channel": "American Association of Neurological Surgeons (YouTube @AANSNeurosurgery)",
    "year": "2020",
    "duration": "unknown",
    "procedure": "DRG stimulator lead placement",
    "region": "Lumbosacral (L5, S1, S2 foramina)",
    "views": "AP and lateral",
    "live_fluoro": "likely yes. The transcript describes electrodes being advanced over the DRG on AP fluoroscopy and a guide catheter advanced under lateral fluoroscopy. Seconds unknown",
    "quality": "unknown (YouTube page did not render; oEmbed only)",
    "licence": "Article: 'open access article distributed under the CC BY-NC-ND license'. YouTube licence field could not be read",
    "reachable": "yes: Thomas Jefferson University neurosurgery (A. Sharan, C. Wu)",
    "evidence": "Europe PMC full text PMC9542308: licence and quotes 'The electrodes are advanced over the DRG on AP fluoroscopy', 'the guide catheter with guidewire and electrode is advanced under lateral fluoroscopy'. YouTube oEmbed confirms title and AANS channel. Not watched."
   },
   {
    "url": "https://youtu.be/KWwGMIoDrmU",
    "title": "Minimally invasive oblique interbody fusion for correction of iatrogenic lumbar deformity (Neurosurgical Focus: Video, PMC9521211)",
    "channel": "American Association of Neurological Surgeons (YouTube @AANSNeurosurgery)",
    "year": "2020",
    "duration": "unknown",
    "procedure": "MIS oblique lumbar interbody fusion plus posterior screws (image-guided)",
    "region": "Lumbar (L1-S1)",
    "views": "Lateral and AP",
    "live_fluoro": "unknown. The text uses fluoroscopy for positioning, retractor confirmation and midline marking; screws were placed with image guidance and intraoperative CT",
    "quality": "unknown",
    "licence": "Article: 'open access article distributed under the CC BY license (http://creativecommons.org/licenses/by/4.0/)'. YouTube licence field not read",
    "reachable": "yes: University of Utah neurosurgery (M. Mazur, A. Dailey)",
    "evidence": "Europe PMC full text: licence and quotes ('The location can be confirmed with lateral fluoroscopy, although the retractor blades can partially obscure the view'). oEmbed gives the channel. Not watched."
   },
   {
    "url": "https://youtu.be/XjOdDeKrKEE",
    "title": "MIS lateral ACR for spinal deformity correction: technique and complication avoidance (Neurosurgical Focus: Video, PMC9521216)",
    "channel": "American Association of Neurological Surgeons (YouTube @AANSNeurosurgery)",
    "year": "2020",
    "duration": "unknown",
    "procedure": "MIS lateral anterior column realignment (ACR) for adult deformity",
    "region": "Lumbar (L2-S1; construct T11 to ilium)",
    "views": "True lateral and AP",
    "live_fluoro": "unknown. The text says 'Fluoroscopy should be frequently used.'",
    "quality": "unknown",
    "licence": "Article: CC BY 4.0 (quoted on the page). YouTube licence field not read",
    "reachable": "yes: Barrow Neurological Institute (J. Uribe) and UCSF (V. Deviren)",
    "evidence": "Europe PMC full text: licence and quotes 'The patient is taped into position such that a true lateral and A/P image can be obtained with fluoroscopy.' oEmbed gives the channel. Not watched."
   },
   {
    "url": "https://stream.cadmore.media/r10.3171/2022.3.FOCVID2221",
    "title": "Safe dissection and complication avoidance for L1-2 interbody placement via a lateral access approach (Neurosurgical Focus: Video, PMC9574671)",
    "channel": "Neurosurgical Focus: Video (AANS/JNSPG), Cadmore stream",
    "year": "2022",
    "duration": "unknown",
    "procedure": "Lateral transpsoas interbody fusion at L1-2",
    "region": "Thoracolumbar junction (T12-L2)",
    "views": "AP and lateral",
    "live_fluoro": "unknown. The transcript says the graft 'is placed under anteroposterior and lateral fluoroscopic guidance'",
    "quality": "unknown",
    "licence": "'open access article distributed under the CC BY license (http://creativecommons.org/licenses/by/4.0/)'",
    "reachable": "yes: Ohio State (D. Xu) and Barrow (L. Snyder, J. Uribe)",
    "evidence": "Europe PMC full text PMC9574671: licence, video URL and fluoroscopy sentence. Not watched."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6948134/",
    "title": "High-Frequency Spinal Cord Stimulation for Chronic Low Back and Leg Pain: Implantation Technique of Percutaneous Leads and IPG (video mmc1.mp4)",
    "channel": "Arthroscopy Techniques (Elsevier), video on PMC",
    "year": "2019",
    "duration": "unknown; 40.5 MB mp4",
    "procedure": "Percutaneous SCS lead placement (Tuohy needles, leads advanced to T8/9)",
    "region": "Thoracic (T8-T10 targets; lumbar entry at L1/2-L2/3)",
    "views": "AP and lateral fluoroscopic controls",
    "live_fluoro": "unknown but plausible. The text says the lead 'is advanced to the desired vertebral level (T8/9) in midline by fluoroscopic guidance'. Following an advancing lead often means panning craniocaudally",
    "quality": "unknown",
    "licence": "CC BY-NC-ND 4.0",
    "reachable": "yes: University Hospital Bonn orthopaedics (A. Kasapovic, S. G. Walter)",
    "evidence": "PMC page: video caption steps 1-27 ('The appropriate vertebral level is determined by fluoroscopy (3)...'), licence, and quotes. Not watched."
   },
   {
    "url": "https://vimeo.com/1109076785",
    "title": "Camera-assisted and navigated single-position prone transpsoas LLIF: illustrative case, Video 2 ('key surgical steps captured through fluoroscopy')",
    "channel": "JNS Publishing Group (Vimeo); J Neurosurg Case Lessons PMC12416324",
    "year": "2025",
    "duration": "30 s (Vimeo oEmbed)",
    "procedure": "Prone transpsoas lateral lumbar interbody fusion with navigation",
    "region": "Lumbar",
    "views": "Mostly AP, with a few confirmatory laterals",
    "live_fluoro": "unknown. The whole 30 s clip is fluoroscopy, but it may be concatenated saved shots",
    "quality": "Vimeo embed default 426x240; source resolution unknown",
    "licence": "CC BY-NC-ND 4.0 (http://creativecommons.org/licenses/by-nc-nd/4.0/)",
    "reachable": "yes: Rouzbeh Motiei-Langroudi, University of Kentucky neurosurgery",
    "evidence": "PMC page: Video 2 caption and licence; 'we still use fluoroscopy (more in AP, though, with a few confirmatory lateral shots) during cage placement'. Vimeo oEmbed: duration 30, author 'JNS Publishing Group'. Not watched."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6135615/",
    "title": "Lumbar Epidural Steroid Injections (JBJS Essential Surgical Techniques, 4 videos)",
    "channel": "JBJS Essential Surgical Techniques, videos on PMC",
    "year": "2016",
    "duration": "unknown",
    "procedure": "Fluoroscopy-guided lumbar epidural steroid injection with contrast",
    "region": "Lumbar",
    "views": "unknown (ESI typically AP, oblique and lateral)",
    "live_fluoro": "unknown for the videos. The text says 'Contrast material is then injected with the use of live fluoroscopy'; needle advancement uses 'intermittent fluoroscopy'",
    "quality": "unknown",
    "licence": "'Copyright © 2016 by The Journal of Bone and Joint Surgery, Incorporated' (not Creative Commons; permission needed)",
    "reachable": "yes: Seton Spine & Scoliosis Center, Austin TX (E. Pena, L. Moroz)",
    "evidence": "PMC page: copyright line and the quoted fluoroscopy sentences; four embedded videos without descriptive captions. Not watched."
   },
   {
    "url": "https://www.youtube.com/watch?v=TX5gz8c765M",
    "title": "Biplanar x-ray fluoroscopy for sacroiliac joint fusion (Neurosurgical Focus 41 videosuppl1, 2016)",
    "channel": "American Association of Neurological Surgeons (YouTube @AANSNeurosurgery)",
    "year": "2016",
    "duration": "unknown",
    "procedure": "SI joint fusion with two simultaneous C-arms (biplanar)",
    "region": "Sacrum/pelvis (lumbosacral region in the lateral view)",
    "views": "Simultaneous AP and lateral; inlet/outlet discussed",
    "live_fluoro": "unknown. The technique is biplanar and real-time by design",
    "quality": "unknown",
    "licence": "Article is not open access (Europe PMC: subscription; © JNS). YouTube licence field not read",
    "reachable": "yes: Vicente Vanaclocha-Vanaclocha, Neurosurgery, Hospital General Universitario de Valencia",
    "evidence": "Search-result abstract: 'one x-ray arch for the lateral projection is placed at a right angle to the patient, and a second x-ray machine is placed with its arch between the legs'. Europe PMC record: not OA. oEmbed confirms title and AANS channel. Not watched."
   }
  ],
  "notes": "Yes, and it turned up more than the journal sites themselves. The old Neurosurgical Focus video supplements (2012-2018) and the early Neurosurgical Focus: Video articles (2019-2020) are hosted on the AANS YouTube channel (@AANSNeurosurgery). Newer ones stream from Cadmore, and JNS Case Lessons uses Vimeo (\"JNS Publishing Group\"). The best reusable material is in open-access supplementary videos. Nothing below was watched: every live-fluoroscopy judgement comes from captions, transcripts or methods text. Nothing was downloaded.\n\nTOP FINDS\n1. Bern conventional dynamic myelography (Clin Neuroradiol 2021, CC BY 4.0, PMC8463391). Four unsubtracted clips, mostly thoracic, pulsed fluoroscopy at 7.5 frames/s, lateral view with the patient prone. The methods say the detector was slowly moved cranially following the contrast. That gives overlapping frames during a cranio-caudal pan, although the step size is unknown. It is the nearest thing yet to the \"overlapping frames at a cranio-caudal step\" the earlier report said no public source had.\n2. Cureus 2024 paediatric cervical exam under anaesthesia (CC BY 4.0, PMC11328828). Explicitly recorded live fluoroscopy of C0-C2 motion, lateral.\n3. Frontiers in Surgery 2023 SpineJack (CC BY, PMC10242080). Fluoroscopy of implant opening and cementation; the text says cement went in under real-time fluoroscopy; thoracic or lumbar.\n\nRELATED CSF-LEAK IMAGING\nDigital subtraction myelography clips subtract the bone, so they are of little use for tracking vertebrae. Examples: J Neurol 2024 Freiburg CSF-lymphatic fistula, CC BY, PMC11447140, AP view at L4/5; and the Interv Pain Med 2023 TFESI subtraction clips, CC BY-NC-ND, PMC11372927. The Bern and Mayo/Duke CSF-leak groups are worth a direct request for their unsubtracted cine.\n\nREUSE TERMS BY LIBRARY\n- **Neurosurgical Focus: Video:** open access. Europe PMC says CC BY for current articles; one 2020 article (DRG stimulation) is CC BY-NC-ND.\n  - Europe PMC indexes 453 articles; 61 mention fluoroscopy and none says \"live fluoroscopy\".\n  - Current spine content is dominated by navigation and robotics, so fluoroscopy tends to be saved shots. The 2026 Duke 2D-FIT prone LLIF (PMC13418632, CC BY) overlays instruments on SAVED AP/lateral images by design.\n  - thejns.org returns 403 to automated fetches; read the articles through PMC or Europe PMC instead.\n- **Old Neurosurgical Focus video supplements (pre-2019):** subscription, © JNS, videos on AANS YouTube. One is relevant to the LSTV work: Ohya/Mummaneni UCSF 2016, \"S-2 alar iliac screw ... in patients with transitional and normal anatomy\", youtu.be/Sj21lk13_aw; fluoroscopy content unknown.\n- **JNS Case Lessons:** CC BY-NC-ND 4.0, Vimeo. The Vimeo oEmbed shows duration.\n- **Operative Neurosurgery:** Wolters Kluwer/CNS, not open access; not screened in depth.\n- **JBJS Essential Surgical Techniques:** even 2025 articles carry \"Copyright © [year] by The Journal of Bone and Joint Surgery, Incorporated\". Videos are viewable as PMC supplements; reuse needs JBJS permission. 72 PMC articles hit fluoroscopy plus spine/pelvis. Relevant ones:\n  - anterior odontoid screw (PMC6359912): \"continuous, real-time, fluoroscopic control in two planes\", but the video is a cadaver;\n  - iliosacral screws in the dysmorphic upper sacrum (PMC6221427, UCSF): inlet/outlet/lateral sacral views, relevant to transitional anatomy;\n  - percutaneous transforaminal endoscopic discectomy (PMC12622600, HSS): five videos.\n- **Journal of Spine Surgery (AME):** CC BY-NC-ND 4.0. Videos also sit in ASVIDE, whose site says \"All rights reserved\" and whose catalogue is JavaScript-rendered, so it could not be listed. Candidate: HSS LLIF (jss.amegroups.org/article/view/6198), fluoroscopy unknown.\n- **Neurospine:** CC BY-NC 4.0, many craniovertebral-junction and endoscopy videos. The AIIMS DCER odontoid reduction (PMC10080440, 59.7 MB) says \"This maneuver was conducted under fluoroscopic guidance\".\n- **International Journal of Spine Surgery (ISASS):** \"© 2022 ISASS ... permissions\", not Creative Commons.\n- **Global Spine Journal:** not established; only abstract books were found.\n- **JoVE:** © JoVE, subscription. Candidates:\n  - SCS paddle lead at T8-T9 (PMC6101993, video 33.2 MB);\n  - transforaminal endoscopy \"under image intensifier\" (PMC6126677);\n  - vertebral cement injection (10.3791/65420);\n  - multilevel OLIF (10.3791/67543).\n- **VuMedi:** the terms bar downloading \"other than page caching\" and \"data mining, robots or similar data gathering or extraction methods\". Uploaders keep ownership and VuMedi gets a sublicensable licence, so permission would have to come from each uploader individually.\n- **AO Surgery Reference:** mostly illustrations. Reproduction permission from [e-mail withheld]. AO Video is members-only.\n- **NASS:** the terms page returned 404.\n- **SpineUniverse:** not checked.\n\nLOWER-VALUE ITEMS SEEN\n- J Cent Nerv Syst Dis 2024 SCS lead (CC BY-NC, PMC11611714): the video is mainly the endoscope view.\n- JOSR 2023 biportal endoscopy for burst fracture (CC BY, 1.8 GB): endoscope view.\n- JNS Case Lessons 2025 kyphoplasty cement leak (Vimeo): surgical views; cement was imaged after each aliquot, not continuously.\n\nMETHOD LIMITS\n- The session's WebSearch cap (200) ran out partway through, so the rest of the discovery went through the Europe PMC REST search API and PMC pages via WebFetch.\n- YouTube watch pages do not render through WebFetch. oEmbed gave title and channel only, so no YouTube licence field, view count or duration could be read. The licences given for those rows are the article's licence.\n- Suggested next step: open the top three PMC clips in a browser and measure frames, duration and resolution before asking anyone for permission.",
  "verify": [
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8463391/",
    "confirmed_live_fluoro": "Yes, from the paper's text and figures; the videos themselves were not watched. Methods: 'The default frame rate was 7.5 f/s, and the detector was slowly moved in a cranial direction.' Fig 5 (the Video 3 case) is captioned 'total time: 14 s' and Fig 6 (the Video 4 case) 'total time: 10 s', so each clip is probably about 10-15 s, roughly 75-110 frames at 7.5 f/s. I opened Fig 5: native (not filmed) AP thoracic frames with bodies and pedicles sharp, and the vertebrae shift craniocaudally between frames a-d. Fig 4 (Video 2 case): tightly collimated lateral thoracic, bodies faint.",
    "confirmed_licence": "Creative Commons Attribution 4.0 International License (stated on the page, '(c) The Author(s) 2020')",
    "confirmed_views": "Video 1: sitting lumbar puncture at L5/S1 (Fig 1), projection not stated. Video 2: prone, lateral projection, leak at T7/8. Video 3: right decubitus, AP projection, T9/10 diverticulum. Video 4: prone, lateral projection, level not stated. Fig 2d adds a slight right oblique at the cervicothoracic junction.",
    "usable_for_tracking": "good",
    "corrections": "Levels are now tied to each video: V1 lumbosacral (L5/S1, seated LP), V2 T7/8, V3 T9/10, V4 level not stated. Durations of about 10-14 s are inferred from the matching figure captions, not measured. File sizes (1.3/6.9/5/3 MB) suggest modest resolution. A contrast column is in every frame, and the lateral thoracic frames are heavily collimated with rib overlap. Best candidate on the list for detector-translation tracking (AP Video 3 especially)."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11328828/",
    "confirmed_live_fluoro": "Live, per the text ('while obtaining live fluoroscopy'). BUT the text also says 'we typically record the live images with a mobile device for subsequent review', so Video 1 is most likely a phone filming the C-arm monitor, not a native export. Duration unknown (7.3 MB mp4). Not watched.",
    "confirmed_licence": "Creative Commons Attribution License CC-BY 4.0 (stated on the page)",
    "confirmed_views": "Lateral. Text: 'The C-arm is positioned for lateral X-rays.'",
    "usable_for_tracking": "possible",
    "corrections": "Quality claim corrected: probably a phone-filmed monitor, not a C-arm export. Patient is a 9-year-old; region is C0-C2 (craniocervical junction). The motion is patient flexion/extension/translation with the detector fixed, so it tests tracking under articulation, not cranio-caudal detector translation. Paediatric upper cervical only. Published 15 July 2024; DOI 10.7759/cureus.64623 (the Cureus page returned 403)."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10242080/",
    "confirmed_live_fluoro": "Unknown from the page. Caption: 'Fluoroscopic stages of insertion, opening and cementation of jack plug implants.' Body: 'The fluoroscopic guidance allowed us a real-time synchronous opening of the implants (Supplementary Video S1)', and cement was injected 'under real time fluoroscopy'. Whether the AVI is continuous fluoro or stitched stages is not stated. Not watched.",
    "confirmed_licence": "Creative Commons Attribution License (CC BY) (stated on the page)",
    "confirmed_views": "unknown (no projection stated anywhere for the fluoroscopy)",
    "usable_for_tracking": "possible",
    "corrections": "Video S1 is a 70-year-old woman with multiple myeloma. Fig 3 shows a 70-year-old woman treated at T6, probably the same patient, but the page does not say so explicitly. Guidance was 'dual CT (SOMATOM Sensation, Siemens) and fluoroscopy', so this is a hybrid CT-fluoro suite, not a standalone C-arm. Upper-mid thoracic, not lumbar. File is 15.7 MB AVI."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8282264/",
    "confirmed_live_fluoro": "unknown. Caption: 'Video showing fluoroscopy steps and markings'. Body: 'Video 1 shows the percutaneous lateral-oblique surgical technique', which suggests mixed OR and fluoro content or saved shots. Not watched.",
    "confirmed_licence": "Creative Commons Attribution License (unrestricted use with credit) (stated on the page)",
    "confirmed_views": "From the text: AP, 30-degree oblique, 15-degree pelvic outlet, 45-degree pelvic inlet, lateral",
    "usable_for_tracking": "poor",
    "corrections": "Pelvis/sacroiliac joint, not vertebral levels; many view changes; live content unverified. Published 15 July 2021. Corresponding author is Fabio J. Pencle (University of Technology, Jamaica), not Chin; Chin is first author (LES Clinic / FIU)."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8687599/",
    "confirmed_live_fluoro": "unknown. Text: 'BKP ... was performed under fluoroscopy'; hooks are placed 'under fluoroscopy (Figures 3C-3D)'. Video 1 covers the whole procedure in 3.7 MB, so fluoro is probably brief if present. Not watched.",
    "confirmed_licence": "Creative Commons Attribution License (stated on the page)",
    "confirmed_views": "unknown for intraoperative fluoro. The only projections named are preoperative 'Lateral X-ray films ... sitting and supine'.",
    "usable_for_tracking": "poor",
    "corrections": "The video case is T12 ('using a case of T12 OVF (Video 1, Figures 1-3)'). Cases: T12, L1, T11, T12. Views unknown. The small file makes a long native fluoro run unlikely."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4852439/",
    "confirmed_live_fluoro": "unknown. Additional file 1 reads only 'Surgical procedure. (MOV 129672 kb)'. The only intraoperative fluoro sentence: 'The bilateral vertebral pedicle shadows appeared symmetrical and were equidistant from the spinous process under fluoroscopic guidance.' Not watched.",
    "confirmed_licence": "Creative Commons Attribution 4.0 International License (stated on the page)",
    "confirmed_views": "AP implied by the pedicle-symmetry sentence. Lateral intraoperative fluoro is not stated (the lateral radiographs are pre- and post-op).",
    "usable_for_tracking": "possible",
    "corrections": "The earlier summary said lateral and AP projections are used intraoperatively. I could only verify AP (implied). The file is about 126.6 MB, so the content could be substantial, but it is completely unverified. Corresponding author is Guoyong Yin, First Affiliated Hospital of Nanjing Medical University (now confirmed)."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7703990/",
    "confirmed_live_fluoro": "unknown. Body: 'The steps of OLLIF under fluoroscopy are shown in Figure 2, Video 1, and Video 2.' Both files are 50.9 KB, which is too small for more than a few low-resolution frames. Not watched.",
    "confirmed_licence": "Creative Commons Attribution License (unrestricted use with credit) (stated on the page)",
    "confirmed_views": "Video 1 lateral, Video 2 AP (from the captions)",
    "usable_for_tracking": "poor",
    "corrections": "No correction to the facts. The identical 50.9 KB sizes suggest very short loops or placeholders. Published 26 Nov 2020."
   },
   {
    "url": "https://youtu.be/_1xMxFZa6tU",
    "confirmed_live_fluoro": "Fluoro shown as video: likely. The YouTube watch page would not render (only the footer came back), so I used the auto-thumbnails. The 25% frame (hq1) is a split screen: left, a circular-field AP fluoroscopy image with a C-arm dose overlay ('119 kVp', mGy); right, an OR camera of the surgeon marking the skin at the same moment. That looks like a synchronised C-arm video-out capture, so live. The 0%, 50% and 75% frames are OR camera only. The share of fluoro in the video is unknown.",
    "confirmed_licence": "YouTube licence field: unknown (page not readable). Companion article (PMC9542308): 'open access article distributed under the CC BY-NC-ND license'.",
    "confirmed_views": "AP seen in the thumbnail. The transcript also names lateral ('Dorsal position of the electrode within the foramen is confirmed on lateral fluoroscopy').",
    "usable_for_tracking": "possible",
    "corrections": "Duration is at least 6:33 (the last transcript timestamp on PMC is 6:33). There is no maxresdefault thumbnail (404), which suggests the upload is below 720p (not proof). In split screen the fluoro takes about half the frame width, so effective resolution is low. Region is lumbosacral (L5/S1/S2 foramina). Authors: Thomas Jefferson University neurosurgery."
   },
   {
    "url": "https://youtu.be/KWwGMIoDrmU",
    "confirmed_live_fluoro": "Probably not; saved stills likely. The watch page would not render. The 25% frame (hq1) shows an AP and a lateral lumbar fluoro image side by side on a slide-style dark background with a red edge, which looks like saved shots laid out as a figure. The 0% and 50% frames are OR camera (retractor) and the 75% frame is a closed incision.",
    "confirmed_licence": "YouTube licence field: unknown (page not readable). Companion article (PMC9521211): 'open access article distributed under the CC BY license'.",
    "confirmed_views": "AP and lateral (both visible as side-by-side images in the hq1 thumbnail)",
    "usable_for_tracking": "poor",
    "corrections": "Duration unknown. Screws were placed with image guidance and intraoperative CT, so live fluoro is minimal. Thumbnail evidence points to still images, not cine."
   },
   {
    "url": "https://youtu.be/XjOdDeKrKEE",
    "confirmed_live_fluoro": "No evidence of live fluoro. The watch page would not render. Auto-thumbnails: a skin marking with a small inset of a saved lateral lumbar fluoro image carrying drawn lines (hq1); a tubular retractor or endoscopic view labelled Anterior/Cranial/Caudal/Posterior (hq2); an annotated anatomical photo with numbered markers (hq3 and default).",
    "confirmed_licence": "YouTube licence field: unknown (page not readable). Companion article (PMC9521216): 'CC BY license (http://creativecommons.org/licenses/by/4.0/)'.",
    "confirmed_views": "Lateral (inset still). AP is named in the text only.",
    "usable_for_tracking": "poor",
    "corrections": "Duration unknown. Content looks like an educational montage of photos, annotations and saved shots. First author is Ifije Ohiorhenuan (Barrow), with Deviren (UCSF) and Uribe (Barrow)."
   },
   {
    "url": "https://stream.cadmore.media/r10.3171/2022.3.FOCVID2221",
    "confirmed_live_fluoro": "unknown. The Cadmore page returned only the word 'Video' (no player metadata, duration or transcript). The article transcript has one fluoro sentence: 'A titanium interbody graft ... is placed under anteroposterior and lateral fluoroscopic guidance.'",
    "confirmed_licence": "Article PMC9574671: '(c) 2022, The Authors. This is an open access article distributed under the CC BY license (http://creativecommons.org/licenses/by/4.0/)'. Licence on the stream host: unknown.",
    "confirmed_views": "AP and lateral (text only)",
    "usable_for_tracking": "poor",
    "corrections": "Nothing could be verified from the stream page. Rated poor because of no evidence, not because of evidence against. The thoracolumbar region would be valuable if cine were present. Authors: D. Xu (Ohio State) and Paisan, Hartke, Katsevman, Uribe and Snyder (Barrow)."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6948134/",
    "confirmed_live_fluoro": "unknown. The video legend has 27 numbered steps, and fluoroscopy appears only at steps 3, 7, 9 (placement check), 11 and 15. Lead advancement 'by fluoroscopic guidance' is in the text. 40.5 MB mp4. Not watched.",
    "confirmed_licence": "'(c) 2019 by the Arthroscopy Association of North America. Published by Elsevier. This is an open access article under the CC BY-NC-ND license'",
    "confirmed_views": "AP and lateral (figure legends: 'Fluoroscopic placement control of percutaneous leads in anteroposterior projection' and '... in lateral projection')",
    "usable_for_tracking": "possible",
    "corrections": "Fluoro is a small part of a 27-step, mostly OR-camera procedure. Mid-thoracic targets T8-T10, prone. The NC-ND licence restricts derivatives, so annotations may need permission."
   },
   {
    "url": "https://vimeo.com/1109076785",
    "confirmed_live_fluoro": "The clip is all fluoroscopy, but whether it is continuous is unknown. Vimeo oEmbed: title 'CASE25-418 Video 2', duration 30 s, uploaded 2025-08-11, description 'Video clip showing the key surgical steps captured through fluoroscopy.' Thumbnail: native (not filmed) circular-field AP of the lower lumbar spine and lumbosacral junction, with percutaneous screw extenders and a navigation reference array. 'Key surgical steps' suggests a montage of saved shots. The Vimeo page itself was behind a captcha.",
    "confirmed_licence": "Article PMC12416324: '(c) 2025 the authors CC BY-NC-ND 4.0'. Vimeo page licence: unknown (captcha).",
    "confirmed_views": "AP (thumbnail). Text: 'more in AP, though, with a few confirmatory lateral shots'.",
    "usable_for_tracking": "possible",
    "corrections": "Upload date 2025-08-11 added. The 426x240 is only the embed default; source resolution is unknown. Contact: [e-mail withheld] (University of Kentucky neurosurgery)."
   },
   {
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6135615/",
    "confirmed_live_fluoro": "unknown. The four videos (38.8, 20.4, 89.1 and 91.2 MB) have no captions and are not cited in the text. The text says levels are found 'with intermittent fluoroscopy' and 'Contrast material is then injected with the use of live fluoroscopy'. Not watched.",
    "confirmed_licence": "'Copyright (c) 2016 by The Journal of Bone and Joint Surgery, Incorporated' (not Creative Commons)",
    "confirmed_views": "unknown",
    "usable_for_tracking": "poor",
    "corrections": "Video sizes are now known, but their content is not. Reuse requires JBJS permission. Authors: Pena, Moroz and Singh, Seton Spine & Scoliosis Center, Austin TX."
   },
   {
    "url": "https://www.youtube.com/watch?v=TX5gz8c765M",
    "confirmed_live_fluoro": "No. The watch page would not render. All four auto-thumbnails (0, 25, 50 and 75%) are 4:3 title-bar slides with photos: 'Prone \"Da Vinci\" position' with a C-arm photo; 'By-planar x-ray fluoroscopy' with an OR photo where the two fluoro monitors are only small boxed insets; and '1-month post-op' patient photos. It is a slideshow.",
    "confirmed_licence": "YouTube licence field: unknown (page not readable). Article: not open access (Europe PMC isOpenAccess: No), DOI 10.3171/2016.2.focusvid.1687, PMID 27364423.",
    "confirmed_views": "AP and lateral (biplanar, per the abstract). Fluoro appears only as small monitors in photos.",
    "usable_for_tracking": "not",
    "corrections": "A slideshow, not cine. Sacroiliac/pelvis. Drop it."
   }
  ]
 }
]
```
