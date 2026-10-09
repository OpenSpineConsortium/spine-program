# Search log: level identification on intraoperative fluoroscopy without a preoperative 3-D image

All searches were run on 2026-09-22. This file is the log itself: every query string is reproduced exactly as
sent, with its hit count and the records that mattered. Every paper classified as registration-based (1),
intraoperative content-based (3) or simulated/cadaver (4) carries a DOI checked against doi.org and Crossref
and, where one exists, a PMID checked against PubMed (Appendix A).

## 1. The sentences tested

- **S1a.** "No published system detects and names vertebrae from the content of a real intraoperative fluoroscopic
  image at a recall high enough to support counting,"
- **S1b.** "and no per-vertebra recall on real intraoperative fluoroscopy is published."
- **S2.** "Every published automatic level-localisation method for intraoperative fluoroscopy imports the level
  identity from a preoperative CT or MR by registration (LevelCheck and successors)."

## 2. Verdict

| Sentence | Verdict | Deciding records |
|---|---|---|
| S1a | **Supported, but only in narrower wording.** Three records could not be read and could still contradict it. | VDVM 0.733 (31 C-arm images; identity matched to the patient's preoperative radiograph); ChatGPT 28% (75 intraoperative fluoroscopy cases, conference abstract); MVMS 88.3% (cadaver O-arm Long-Film, not C-arm fluoroscopy); Dice 0.04 on individual vertebral levels (1 cadaver, real C-arm). Unread: Li 2016, Li 2017, ABLSpineLevelCheck 2024. |
| S1b | **Not supported as worded.** | Rao et al., EMBC 2024: per-vertebra detection recall 0.964 (their model) and 0.982 (YOLOv5) on C-arm images from three commercial C-arms, drawn from patients, cadavers and phantoms. VDVM: per-vertebra detection mAP 0.87 on 31 C-arm images. Neither names a level. |
| S2 | **Refuted as worded.** | VDVM takes level identity from a preoperative **2-D radiograph** by matching, with no CT or MR. MVMS names levels on intraoperative long-length images with **no preoperative image at all** (cadaver). ABLSpineLevelCheck (2024) and Li (2016, 2017) localise or identify levels on fluoroscopic or C-arm images with no registration step; their numbers cannot be read. |

**Verdict paragraph.** S1 makes two claims, and the evidence treats them differently.

The first claim, S1a, fits everything we could read:

- The only naming results on clinical intraoperative images are VDVM's 0.733 segment-matching accuracy on 31
  C-arm images, and a 2026 conference abstract in which ChatGPT agreed with a neurosurgeon on the marked level in
  28% of 75 cases. VDVM names vertebrae by matching them to the same patient's preoperative radiograph, not from
  the image alone.
- The best registration-free naming result, MVMS at 88.3%, was measured on cadaver O-arm Long-Film tomosynthesis.
- On real C-arm images of one cadaver, a promptable segmenter reached a Dice of 0.04 on individual vertebral levels.

S1a is still not safe to submit until three IEEE conference papers have been read. Li 2016, Li 2017 and Jiang 2024
(ABLSpineLevelCheck) detect or name lumbar levels on C-arm or fluoroscopic images. Their abstracts give no numbers,
and their full texts could not be retrieved from here.

S1b is **contradicted**. Rao et al. (2024) publish a per-vertebra detection recall on C-arm images: 0.964, and 0.982
for YOLOv5. VDVM publishes a per-vertebra detection mAP of 0.87. Both detectors are class-agnostic and name nothing,
so S1b holds only if it is narrowed to naming.

S2 is **refuted as worded**. VDVM takes identity from a preoperative 2-D radiograph, not a CT or MR. MVMS,
ABLSpineLevelCheck and Li 2016/2017 use no preoperative image at all. The evidence supports only a narrower claim:
one restricted to methods with accuracy on clinical images, and to naming at a stated level.

**Wording the evidence allows (search date 22 September 2026):**

> In a search of PubMed, Europe PMC, OpenAlex, Semantic Scholar, arXiv, the FDA 510(k) database and the web
> (22 September 2026), we found no published method that names vertebrae from the content of real intraoperative
> fluoroscopy with a reported per-vertebra naming accuracy above 73.3% (Zhang et al. 2023, 31 C-arm images,
> identity matched to the patient's preoperative radiograph). Published per-vertebra detection recalls on C-arm
> images (0.96–0.98; Rao et al. 2024) do not name levels, and registration-free naming has been reported at 88.3%
> only on cadaver long-length O-arm tomosynthesis (Huang et al. 2022).

> Automatic level localisation on intraoperative radiographs that reports accuracy on clinical images imports the
> level identity from another image of the same patient: a preoperative CT or MR by 3D–2D registration
> (LevelCheck and successors) or, in one study, a preoperative radiograph by vertebra matching (Zhang et al. 2023).

If the manuscript says that no system names vertebrae "at a recall high enough to support counting", it should
state the threshold, for example ≥95% per vertebra. As written, a reviewer has nothing to check the claim against.

## 3. Method

- **Scope.** 2010–2026. Journal, conference proceedings, arXiv, conference-abstract supplements, FDA 510(k).
- **Engines.**
  - **PubMed** through E-utilities: `esearch.fcgi` gives exact counts, and `esummary`/`efetch` return titles and
    abstracts.
  - **Europe PMC REST** (`/search`), which also searches the full text of open-access papers and abstract
    supplements.
  - **OpenAlex** (`/works?search=`, and `cites:` for forward citation). It indexes IEEE, SPIE and other conference
    proceedings that PubMed misses.
  - **Semantic Scholar Graph API** (`/paper/search`). Unauthenticated calls got HTTP 429 all morning, so these
    queries used the S2 key from the local WSL credential store (`~/.fluorocap/credentials.env`). The key was never
    printed.
  - **arXiv API** (`export.arxiv.org/api/query`).
  - **openFDA** (`api.fda.gov/device/510k.json`), plus the 510(k) summary PDFs themselves.
  - **A general web search engine (WebSearch)** in place of Google Scholar, which has no API. It was also restricted
    by `site:` to ieeexplore.ieee.org and spiedigitallibrary.org, because the IEEE Xplore and SPIE APIs need keys
    that were not available.
- **Screening.** Every returned title was read; sets larger than 300 were capped at the top 100 by relevance.
  Abstracts were read for any record that concerns detecting, labelling or localising vertebrae or levels on X-ray,
  fluoroscopy or C-arm images. Full text was read wherever it was reachable: open access, arXiv, or Europe PMC XML.
- **Classes.**
  - (1) Registration-based.
  - (2) Plain film only: adjacent work, not a counter-example. Diagnostic CT, MR and ultrasound level
    identification are tagged separately.
  - (3) Intraoperative and content-based, with a per-vertebra detection or identification metric on real
    intraoperative images.
  - (4) Simulated or cadaver only.
  - (5) Irrelevant: the title was plausible enough to screen, but the paper does not identify levels.
  - **U**, unresolved: a relevant record whose abstract cannot classify it and whose full text could not be read.
- **Verification.**
  - Each DOI: a HEAD request to `https://doi.org/<doi>` (302 means the DOI is registered and resolves), plus a
    title match against `api.crossref.org/works/<doi>`.
  - Each PMID: a title match via `esummary`.
  - All checks passed (Appendix A). Two DOIs are registered with other agencies and are absent from Crossref, but
    both resolve at doi.org: an arXiv DataCite DOI and a Chinese Medical Association DOI.
- **Access that failed.**
  - IEEE Xplore: an AWS-WAF challenge blocked both plain requests and browser impersonation.
  - IOS Press and SAGE (VDVM): 403.
  - ScienceDirect and Springer: login redirects.
  - The PMC HTML front end: a proof-of-work challenge. The Europe PMC XML or the arXiv version was used instead.
- **Seeds.** The project's earlier passes were read first and every item from them was re-verified here:
  `docs/research_registration_free_2026-09-18.json` and `docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md`. This pass found
  records those passes did not have: ABLSpineLevelCheck 2024; Li 2016 and Li 2017; Rao and Maik 2024
  (Spine-Vision); the Desai 2026 ChatGPT abstract; the per-level Dice of Killeen 2025; ProVLNet 2025; and
  X2P-Net 2026.

## 4. Search log

Every query was run on 2026-09-22. "Examined" is the number of titles screened, and "relevant" lists the records
kept, with bracketed tags that refer to §5. "Hits" is the engine's own count. OpenAlex and Semantic Scholar counts
are loose relevance matches, so only their top 100 were screened.

### 4.1 PubMed (E-utilities `esearch`, db=pubmed)

Every query below also carried `AND ("2010/01/01"[dp] : "2026/12/31"[dp])`.

| # | Query | Hits | Examined | Relevant |
|---|---|---|---|---|
| P1 | `(fluoroscop*[tiab] OR "C-arm"[tiab] OR "intraoperative radiograph*"[tiab] OR "intraoperative X-ray*"[tiab]) AND (vertebra*[tiab] OR "spinal level*"[tiab] OR "vertebral level*"[tiab]) AND ("deep learning"[tiab] OR "neural network*"[tiab] OR convolutional[tiab] OR "machine learning"[tiab] OR "artificial intelligence"[tiab])` | 18 | 18 | VDVM (3); MVMS (4); Li16 (U); Twin (4); X23D (4); Shen 2026, Naik 2022 J Imaging, Shao 2024 (1); Liebrand SR; Auloge 2020, Pan 2021, Liu 2020 (5) |
| P2 | `("wrong level"[tiab] OR "wrong-level"[tiab] OR "wrong site"[tiab] OR "wrong-site"[tiab]) AND (spine[tiab] OR spinal[tiab] OR vertebra*[tiab]) AND (automat*[tiab] OR "artificial intelligence"[tiab] OR "deep learning"[tiab] OR algorithm*[tiab] OR "machine learning"[tiab] OR "neural network*"[tiab] OR software[tiab])` | 9 | 9 | Otake 2012, Lo 2015 (1); MVMS (4); Kwak (2); Javadnia review |
| P3 | `("level localization"[tiab] OR "level localisation"[tiab] OR "level identification"[tiab] OR "vertebral localization"[tiab] OR "vertebral localisation"[tiab] OR "level verification"[tiab] OR "level determination"[tiab] OR "localization of the vertebral level"[tiab] OR "vertebral level localization"[tiab]) AND (fluoroscop*[tiab] OR radiograph*[tiab] OR "C-arm"[tiab] OR intraoperative[tiab] OR "X-ray"[tiab])` | 104 | 104 | De Silva 2016, Manbachi 2018, MR-LevelCheck, Otake 2013, Naik 2022 (1); MVMS (4); Baka 2017 ultrasound (2-US); Dharnipragada 2022 (5). About 80 hits were off-topic (e.g. "trace level determination" in chemistry) |
| P4 | `vertebra*[tiab] AND (label*[tiab] OR identif*[tiab] OR naming[tiab] OR numbering[tiab] OR enumerat*[tiab]) AND (fluoroscop*[tiab] OR "C-arm"[tiab])` | 233 | 233 | Bindels 2022 skin-marker 3D2D (1). Otherwise clinical fluoroscopy technique papers, none of them automatic |
| P5 | `("3D-2D"[tiab] OR "2D-3D"[tiab] OR "2D/3D"[tiab] OR "3D/2D"[tiab] OR "3D to 2D"[tiab] OR "2D to 3D"[tiab]) AND registration[tiab] AND (vertebra*[tiab] OR spine[tiab] OR spinal[tiab]) AND (fluoroscop*[tiab] OR radiograph*[tiab] OR "C-arm"[tiab])` | 46 | 46 | Registration lineage (1): the LevelCheck papers; KC 2015–2018; Zhang 2021; Oulbacha 2020; Varnavas 2013 and 2015; Esfandiari 2019; Chang 2015; Abumoussa 2023 |
| P6 | `(vertebra*[tiab] OR spine[tiab] OR spinal[tiab]) AND (detect*[tiab] OR segment*[tiab] OR landmark*[tiab] OR locali*[tiab]) AND (fluoroscop*[tiab] OR "C-arm"[tiab]) AND ("deep learning"[tiab] OR convolutional[tiab] OR "neural network*"[tiab] OR YOLO[tiab] OR "U-Net"[tiab] OR "R-CNN"[tiab] OR transformer[tiab])` | 15 | 15 | VDVM (3); Li16 (U); Liu 2026 stitching (5); Girgis review; Liebrand SR |
| P7 | `(stitch*[tiab] OR panoram*[tiab] OR mosaic*[tiab]) AND (fluoroscop*[tiab] OR "C-arm"[tiab] OR "X-ray"[tiab] OR radiograph*[tiab]) AND (spine[tiab] OR spinal[tiab] OR vertebra*[tiab])` | 254 | 254 | None: 131 dental panoramic hits; the rest were stitching-error case reports and long-film dose papers. No record labels levels on a stitched image |
| P7b | `(stitch*[tiab] OR panoram*[tiab] OR mosaic*[tiab]) AND (fluoroscop*[tiab] OR "C-arm"[tiab] OR intraoperative[tiab]) AND (spine[tiab] OR spinal[tiab] OR vertebra*[tiab])` | 20 | 20 | Liu 2026 stitching (5); ruler-based C-arm stitching 2015 (5); parallax in stitched fluoroscopy 2022 (5) |
| P8 | `("digitally reconstructed radiograph*"[tiab] OR DRR[tiab] OR DRRs[tiab] OR DeepDRR[tiab] OR "synthetic X-ray*"[tiab] OR "simulated X-ray*"[tiab] OR "simulated fluoroscop*"[tiab] OR "in silico"[tiab]) AND (vertebra*[tiab] OR spine[tiab] OR spinal[tiab]) AND (detect*[tiab] OR label*[tiab] OR identif*[tiab] OR landmark*[tiab] OR segment*[tiab])` | 716 | 100 | None. The results were polluted: `vertebra*` matches "vertebrate", and "in silico" pulls in genomics. Superseded by P8b |
| P8b | P8 `AND (fluoroscop*[tiab] OR "C-arm"[tiab] OR intraoperative[tiab] OR surgery[tiab] OR surgical[tiab])` | 42 | 42 | Naik 2022, Otake 2015, Abumoussa 2023, Shen 2026 (1); Kausch 2022 (5); Li16 (U) |
| P9 | `("long-length"[tiab] OR "long film"[tiab] OR "Long-Film"[tiab] OR "slot-scan"[tiab] OR "slot scan"[tiab]) AND vertebra*[tiab] AND (label*[tiab] OR identif*[tiab])` | 4 | 4 | MVMS (4); Zhang 2022 deformable long-length (1) |
| P10 | `(radiograph*[tiab] OR "X-ray*"[tiab] OR "plain film*"[tiab]) AND vertebra*[tiab] AND (label*[tiab] OR identif*[tiab] OR numbering[tiab] OR naming[tiab]) AND ("deep learning"[tiab] OR convolutional[tiab] OR "neural network*"[tiab])` | 156 | 156 | Class 2 only: Kim 2024 L5, Kónya 2021, Kim 2021, Jung 2026, Cina 2021, plus fracture and Cobb-angle papers |
| P11 | `(intraoperative[tiab] OR surgery[tiab] OR surgical[tiab]) AND ("C-arm"[tiab] OR fluoroscop*[tiab]) AND (counting[tiab] OR count[tiab] OR counted[tiab]) AND (vertebra*[tiab] OR level*[tiab]) AND (spine[tiab] OR spinal[tiab])` | 14 | 14 | Otake 2015 (1); Dharnipragada 2022 (5); surveys and technique notes. No automatic counting |
| P12 | `pedicle*[tiab] AND (fluoroscop*[tiab] OR "C-arm"[tiab]) AND ("deep learning"[tiab] OR convolutional[tiab] OR "neural network*"[tiab] OR YOLO[tiab] OR "machine learning"[tiab]) AND (detect*[tiab] OR segment*[tiab] OR landmark*[tiab] OR locali*[tiab])` | 4 | 4 | Esfandiari 2018 screws (5); Liu 2026 (5) |
| P13 | `"Fluoroscopy"[Mesh] AND ("Spine"[Mesh] OR "Spinal Diseases"[Mesh] OR "Spinal Fusion"[Mesh]) AND ("Deep Learning"[Mesh] OR "Artificial Intelligence"[Mesh] OR "Neural Networks, Computer"[Mesh] OR "Machine Learning"[Mesh])` | 58 | 58 | Jecklin 2024 (4); Liu 2020 video-fluoroscopy tracking (5). Mostly studies comparing robot and fluoroscopy outcomes |
| P14 | `("Surgery, Computer-Assisted"[Mesh] OR "Imaging, Three-Dimensional"[Mesh]) AND "Fluoroscopy"[Mesh] AND "Spine"[Mesh] AND (level*[tiab] OR label*[tiab]) AND (automat*[tiab] OR registration[tiab])` | 21 | 21 | Otake 2013, Zhang 2021, Khan 2022 (1); Kausch 2022 (5) |
| P15 | `(vertebroplasty[tiab] OR kyphoplasty[tiab]) AND (fluoroscop*[tiab] OR "C-arm"[tiab]) AND ("deep learning"[tiab] OR convolutional[tiab] OR "neural network*"[tiab] OR "machine learning"[tiab] OR "artificial intelligence"[tiab])` | 2 | 2 | Auloge 2020 (5); CT-free vertebroplasty path planning 2026 (5) |
| P16 | `(instrument*[tiab] OR probe[tiab] OR needle*[tiab] OR marker*[tiab] OR "surgical tool*"[tiab]) AND (level*[tiab]) AND (fluoroscop*[tiab] OR radiograph*[tiab] OR "C-arm"[tiab]) AND (automat*[tiab] OR "deep learning"[tiab] OR "computer vision"[tiab] OR "artificial intelligence"[tiab]) AND (spine[tiab] OR spinal[tiab] OR vertebra*[tiab]) AND (localiz*[tiab] OR localis*[tiab] OR identif*[tiab])` | 7 | 7 | MVMS (4); implant-identification papers (5). No instrument-tip level identification |
| P17 | `LevelCheck[tiab] OR "Level Check"[tiab] OR "msLevelCheck"[tiab]` | 34 | 34 | 7 LevelCheck-lineage papers (1). The other 27 use "level check" in its laboratory-medicine senses |
| P18 | `(fluoroscop*[tiab] OR "C-arm"[tiab] OR "intraoperative radiograph*"[tiab]) AND (vertebra*[tiab] OR spine[tiab]) AND (recall[tiab] OR sensitivity[tiab] OR "detection rate"[tiab] OR "F1"[tiab] OR "mean average precision"[tiab] OR mAP[tiab]) AND ("deep learning"[tiab] OR convolutional[tiab] OR "neural network*"[tiab] OR YOLO[tiab] OR "R-CNN"[tiab])` | 3 | 3 | VDVM (3); Jecklin 2024, X23D (4). This query misses Rao 2024, whose abstract carries no metric |
| P19 | `("vertebral segment*"[tiab] OR "surgical segment*"[tiab] OR "spinal segment*"[tiab] OR "surgical level*"[tiab] OR "target level*"[tiab] OR "operative level*"[tiab]) AND ("C-arm"[tiab] OR fluoroscop*[tiab] OR "intraoperative radiograph*"[tiab]) AND (match*[tiab] OR identif*[tiab] OR locali*[tiab] OR locate*[tiab]) AND ("deep learning"[tiab] OR convolutional[tiab] OR "neural network*"[tiab] OR "artificial intelligence"[tiab] OR "machine learning"[tiab] OR automat*[tiab])` | 3 | 3 | VDVM (3) |
| P20 | `("X-ray*"[tiab] OR radiograph*[tiab] OR fluoroscop*[tiab]) AND intraoperative[tiab] AND vertebra*[tiab] AND ("deep learning"[tiab] OR convolutional[tiab] OR "neural network*"[tiab] OR "artificial intelligence"[tiab] OR "machine learning"[tiab])` | 17 | 17 | MVMS, Twin, X23D (4); Rao 2024 SV (3/4); Naik 2022 J Imaging, Shao 2024, Shen 2026, DVAP-Reg (1); path planning 2026 (5) |
| P21 | `(fluoroscop*[tiab] OR "C-arm"[tiab]) AND (spine[tiab] OR spinal[tiab] OR vertebra*[tiab]) AND (cadaver*[tiab] OR phantom*[tiab] OR specimen*[tiab]) AND ("deep learning"[tiab] OR convolutional[tiab] OR "neural network*"[tiab] OR "machine learning"[tiab]) AND (detect*[tiab] OR label*[tiab] OR landmark*[tiab] OR segment*[tiab] OR identif*[tiab])` | 1 | 1 | Fiducial recovery 2022 (5) |
| P22 | `("mobile radiograph*"[tiab] OR "portable radiograph*"[tiab] OR "intraoperative radiograph*"[tiab] OR "intra-operative radiograph*"[tiab] OR "intraoperative x-ray*"[tiab]) AND (vertebra*[tiab] OR "spinal level*"[tiab] OR "vertebral level*"[tiab]) AND (automat*[tiab] OR algorithm*[tiab] OR "deep learning"[tiab] OR "neural network*"[tiab])` | 9 | 9 | 8 registration papers (1); MVMS (4) |

Across all PubMed queries, 1,047 unique PMIDs were screened by title.

### 4.2 Europe PMC (REST `/search`, which includes open-access full text and abstract supplements)

| # | Query | Hits | Examined | Relevant |
|---|---|---|---|---|
| E1 | `("C-arm" OR fluoroscopy OR fluoroscopic OR "intraoperative radiograph") AND ("vertebral level" OR "spinal level" OR "level identification" OR "level localization" OR "level localisation" OR "wrong level" OR "wrong-level") AND ("deep learning" OR "convolutional neural network" OR "neural network") AND PUB_YEAR:[2010 TO 2026]` | 122 | 122 | The Global Spine J 2026 e-poster supplement, which contains **Desai 2026 [GPT] (3)** and Kairy 2026 (a review abstract); Doerr 2020 (5); CT-to-stereovision registration 2021 (5). The rest were reviews and abstract books (§4.8) |
| E2 | `TITLE_ABS:("C-arm" OR fluoroscopy OR fluoroscopic OR intraoperative) AND TITLE_ABS:(vertebra OR vertebrae OR vertebral) AND TITLE_ABS:(labeling OR labelling OR identification OR "level identification" OR localization OR localisation OR naming OR numbering) AND TITLE_ABS:("deep learning" OR "convolutional" OR "neural network" OR "machine learning" OR "artificial intelligence") AND PUB_YEAR:[2010 TO 2026]` | 8 | 8 | Intraoperative CT only: Siemionow 2020 (5) |
| E3 | `("vertebrae labeling" OR "vertebra labeling" OR "vertebrae labelling" OR "vertebral labeling" OR "vertebral labelling" OR "vertebra identification" OR "vertebrae identification") AND ("fluoroscopy" OR "C-arm" OR "intraoperative X-ray" OR "intraoperative radiograph") AND PUB_YEAR:[2010 TO 2026]` | 21 | 21 | X2P-Net (4) |
| E4 | `("wrong level" OR "wrong-level surgery") AND ("deep learning" OR "convolutional neural network" OR "artificial intelligence") AND (fluoroscopy OR "C-arm" OR radiograph) AND PUB_YEAR:[2010 TO 2026]` | 24 | 24 | Kwak, Kim 2024 L5 (2); Naik 2022 ×2 (1); MacLeod 2025 review, whose claim was traced (§5.7) |
| E5 | `(DeepDRR OR "digitally reconstructed radiographs") AND (vertebra OR vertebrae) AND (detection OR labeling OR labelling OR identification) AND ("C-arm" OR fluoroscopy OR intraoperative) AND ("deep learning" OR "convolutional") AND PUB_YEAR:[2010 TO 2026]` | 29 | 29 | X2P-Net (4); SyntheX, Pelphix (4, pelvis); Bier 2019 pelvis (5); registration papers (1) |

### 4.3 OpenAlex (`/works?search=`, filter `from_publication_date:2010-01-01`, top 100 by relevance)

| # | Query | Hits | Examined | Relevant |
|---|---|---|---|---|
| O1 | `vertebrae identification C-arm X-ray` | 2738 | 100 | **Li17 (U)**; VertXNet (2); lumbar detection from neighbour relationships, 2024 (2) |
| O2 | `vertebrae labeling intraoperative X-ray images` | 904 | 100 | Otake SPIE 2012 (1); Ye 2025 (1) |
| O3 | `vertebra detection fluoroscopy deep learning` | 305 | 100 | **ABLSpineLevelCheck (U)**, found only here and by forward citation; X2P-Net (4); dual-fluoroscopy orientation, CAAI 2025 (5); quantitative-fluoroscopy detection, TechRxiv 2024 (5) |
| O4 | `vertebral level localization fluoroscopy` | 2967 | 100 | None (dose and technique papers) |
| O5 | `wrong level spine surgery artificial intelligence` | 1471 | 100 | None (general AI reviews) |
| O6 | `lumbar vertebrae identification intraoperative C-arm` | 845 | 100 | None |
| O7 | `spine level identification intraoperative radiograph neural network` | 628 | 100 | Gami 2022 camera markers (5) |
| O8 | `vertebrae labeling long-length intraoperative` | 813 | 100 | MVMS-SPIE (4); MR-to-tomosynthesis registration, SPIE 2023 (1) |
| O9 | `fluoroscopy vertebra segmentation intraoperative neural network` | 134 | 100 | Maik 2024 SV (3/4); IXGS 2025 3-D reconstruction (5) |
| O10 | `C-arm image stitching spine` | 2022 | 100 | SX-Stitch 2025, Procedia 2022 stitching (5). No stitching method labels levels |

### 4.4 Semantic Scholar Graph API (`/paper/search`, `year=2010-2026`, `limit=100`)

| # | Query | Hits | Examined | Relevant |
|---|---|---|---|---|
| S1 | `vertebrae labeling intraoperative fluoroscopy deep learning` | 323 | 100 | xvr (Gopalakrishnan) (1); DeepDRR 2018 (context) |
| S2 | `vertebra detection C-arm X-ray images` | 4453 | 100 | VLD-Net 2025, YOLO11-MSCA 2026 (2); conformal-landmark C-arm positioning, ICCVW 2025, DeepDRR only (5); Twin (4) |
| S3 | `vertebral level identification fluoroscopy` | 1076 | 100 | SLIDE 2017 (2-US); ACM 2026 radiograph identification (2); SpineCLUE (2-CT) |
| S4 | `wrong-level spine surgery deep learning` | 3084 | 100 | None |
| S5 | `automatic vertebral level localization spine surgery X-ray` | 397 | 100 | None new |
| S6 | `vertebra identification intraoperative radiograph` | 298 | 100 | **Ahmad 2025 MVL-DRR (4)**; 2010 radiograph identification (2) |
| S7 | `vertebrae labeling synthetic X-ray DRR sim-to-real` | 0 | 0 | — |
| S8 | `counting vertebrae fluoroscopy automatic` | 34 | 34 | None (2012 video-fluoroscopy tracking, 5) |
| S9 | `C-arm image stitching spine vertebra labeling` | 54 | 54 | None |
| S10 | `LevelCheck 3D-2D registration vertebral labeling` | 253 | 100 | xvr Nature 2026 (1); registration variants (1) |
| S11 | `vertebra segmentation intraoperative fluoroscopy deep learning` | 512 | 100 | None new |
| S12 | `pedicle detection fluoroscopy deep learning` | 57 | 57 | None |
| S13 | `surgical level localization artificial intelligence spine` | — | 0 | **Not executed**: the request failed after 8 retries |
| S14 | `vertebrae labeling long-length intraoperative images` | 1489 | 100 | None new |
| S15 | `lumbar vertebrae identification C-arm` | 111 | 100 | None new. Li16 and Li17 were not ranked, because the API's relevance ranking is noisy |
| S16 | `vertebral level localization fluoroscopy semi-supervised` | 271 | 100 | None (ABLSpineLevelCheck was not ranked) |

### 4.5 arXiv API (`export.arxiv.org/api/query`, `max_results=300`, records from 2010 onward)

| # | Query | Hits | Examined | Relevant |
|---|---|---|---|---|
| A1 | `(abs:vertebra OR abs:vertebrae OR abs:vertebral) AND (abs:fluoroscopy OR abs:fluoroscopic OR abs:"C-arm")` | 7 | 6 | Twin (4); Maik 2024 SV (3/4) |
| A2 | `(abs:vertebra OR abs:vertebrae) AND (abs:labeling OR abs:labelling OR abs:identification) AND (abs:"X-ray" OR abs:radiograph OR abs:radiographs)` | 10 | 10 | VertXNet, SpineFM (2) |
| A3 | `(abs:"wrong-level" OR abs:"wrong level" OR abs:"level localization" OR abs:"level identification") AND (abs:spine OR abs:spinal OR abs:vertebra)` | 4 | 4 | DeepSPINE (MR), VinDr-SpineXR (2) |
| A4 | `(abs:vertebra OR abs:vertebrae OR abs:spine) AND abs:intraoperative AND (abs:"X-ray" OR abs:fluoroscopy OR abs:"C-arm" OR abs:radiograph)` | 7 | 7 | Jecklin 2024 (4); SX-Stitch, IXGS (5) |
| A5 | `(abs:DeepDRR OR abs:"digitally reconstructed radiographs" OR abs:"synthetic X-ray" OR abs:"simulated X-ray") AND (abs:spine OR abs:vertebra OR abs:vertebrae OR abs:vertebral)` | 5 | 5 | None |
| A6 | `abs:"C-arm" AND (abs:spine OR abs:spinal OR abs:lumbar OR abs:vertebra OR abs:vertebrae)` | 10 | 10 | None (screw pose, CBCT trajectories) |
| A7 | `(abs:fluoroscopy OR abs:fluoroscopic OR abs:"X-ray") AND (abs:spine OR abs:vertebrae) AND (abs:surgery OR abs:surgical OR abs:intraoperative OR abs:"intra-operative")` | 24 | 23 | Rao 2024 SV (3/4); Klitzner 2026 (4) |
| A8 | `ti:FluoroSAM OR abs:FluoroSAM OR ti:Pelphix OR ti:SyntheX` | 3 | 3 | FluoroSAM (4); Pelphix, SyntheX (4, pelvis and hip) |
| A9 | `(abs:vertebrae OR abs:vertebra) AND (abs:detection OR abs:labeling OR abs:labelling OR abs:localization) AND (abs:radiograph OR abs:radiographs OR abs:"X-ray" OR abs:"X-rays")` | 25 | 24 | Class 2 only |

### 4.6 FDA (openFDA 510(k) API and the 510(k) summaries)

| # | Query / document | Hits | Examined | Relevant |
|---|---|---|---|---|
| F1 | `device_name:(vertebra OR vertebrae OR vertebral) AND decision_date:[2010-01-01 TO 2026-12-31]` | 45 | 45 | None. Implants, plus Kinegraph VMA (diagnostic motion) and VirtuOst (CT) |
| F2 | `device_name:(spine OR spinal) AND device_name:(fluoro OR fluoroscopy OR fluoroscopic OR x-ray OR radiograph OR radiographic OR c-arm) AND decision_date:[...]` | 33 | 33 | None (implants, Brainlab navigation) |
| F3 | `device_name:(level) AND device_name:(spine OR spinal OR vertebral) AND decision_date:[...]` | 1 | 1 | None |
| F4 | `applicant:(vuze OR "holo surgical" OR surgalign OR augmedics OR "surgical theater" OR "ecential" OR "onpoint" OR "kaliber") AND decision_date:[...]` | 29 | 29 | VUZE K210830 and K232976; ARAI K211254; HOLO Portal K231611 (§5.5) |
| F5 | 510(k) summary PDFs K210830, K232976, K211254 and K231611, read in full | 4 | 4 | None identifies levels from 2-D image content. VUZE registers preoperative 3-D to intraoperative 2-D; ARAI and HOLO use intraoperative CT |

### 4.7 Web search engine (Google Scholar substitute, plus IEEE and SPIE by site restriction; about 10 results per query, all examined)

| # | Query | Relevant |
|---|---|---|
| W1 | `deep learning vertebral level identification intraoperative fluoroscopy wrong-level surgery` | MVMS; Naik 2022; LevelCheck patent US 11,284,846; Girgis 2026 review |
| W2 | `automatic vertebra labeling C-arm fluoroscopic images without preoperative CT` | Otake 2012; Kausch 2020 (5) |
| W3 | `artificial intelligence spinal level localization intraoperative radiograph accuracy study` | Reviews only |
| W4 | `"level" localization spine surgery "C-arm" deep learning vertebrae counting sacrum` | Otake SPIE 2012; Kim 2024 L5; Cina 2021 |
| W5 | `site:ieeexplore.ieee.org vertebrae detection C-arm X-ray images deep learning` | **Li16 (U), Li17 (U)**; VLD-Net (2) |
| W6 | `FDA 510(k) software automatic vertebral level identification fluoroscopy spine surgery` | VUZE (1) |
| W7 | `FluoroSAM vertebrae segmentation real X-ray evaluation individual vertebra names` | FluoroSAM (4) |
| W8 | `vertebra detection intraoperative fluoroscopy deep learning recall per vertebra real patients` | X2P-Net (4) |
| W9 | `"ABLSpineLevelCheck" abductive learning vertebral levels fluoroscopy` | ABL (U); Shen 2026 (1) |
| W10 | `Jiang Shuai Zeng abductive learning vertebra localization fluoroscopic images BUU dataset` | Author page (no numbers, no dataset description) |
| W11 | `"abductive learning" vertebral level localization fluoroscopic images mAP semi-supervised neuro-symbolic spine X-ray` | No source gives ABL's numbers |
| W12 | `FDA cleared AI intraoperative fluoroscopy vertebra labeling level identification software spine 2024 2025` | SyncAR (CT); Lee 2026 JAAOS review of FDA-cleared AI devices |
| W13 | `accessdata.fda.gov 510(k) summary "vertebral level" "fluoroscopic" automatic labeling spine navigation` | None |
| W14 | `Holo Portal ARAI Surgalign automatic vertebral level identification intraoperative accuracy` | ARAI and HOLO use intraoperative CT |
| W15 | `VUZE Medical 510(k) K number fluoroscopy preoperative CT registration vertebra level spine guidance summary` | VUZE; Siemens Cios Spin with VUZE (2026) |
| W16 | `deep learning identify spinal level of localization marker on intraoperative lateral radiograph cervical lumbar surgery` | Plain film only |
| W17 | `YOLO vertebra detection C-arm intraoperative X-ray images lumbar identification "C-arm" recall precision` | **Rao 2024 SV (3/4)**; ACM 2026 radiograph (2) |
| W18 | `C-arm X-ray vertebral segment matching DR images surgical level localization deep learning follow-up VDVM` | VDVM only; no follow-up found |
| W19 | `C型臂 X线 椎体节段 自动识别 深度学习 术中 定位` (Chinese: "C-arm X-ray vertebral segment automatic recognition, deep learning, intraoperative localisation") | Nothing relevant |
| W20 | `startup AI counts vertebrae on fluoroscopy to prevent wrong-level spine surgery` | X23D; Proprio (optical/CT) |
| W21 | `LevelCheck Siemens Healthineers commercial product vertebral level labeling fluoroscopy` | No documentation of a commercial LevelCheck product |
| W22 | `site:ieeexplore.ieee.org vertebral level identification intraoperative X-ray fluoroscopy` | ABL (U) |
| W23 | `site:spiedigitallibrary.org vertebrae labeling fluoroscopy intraoperative radiograph deep learning` | MVMS-SPIE (4); Ketcha 2016 (1) |
| W24 | `MICCAI vertebra identification intraoperative X-ray image without CT registration-free level` | Philips patent US 10,405,821 B2; CT-free path planning 2026 (5) |

### 4.8 Full-text scans of conference-abstract supplements (Europe PMC `fullTextXML`)

Each supplement was scanned for windows in which a term from the first group below appears within ±600 characters
of a term from each of the other two groups.

| Group | Terms |
|---|---|
| Imaging | fluoroscop, C-arm, intraoperative X-ray, intraoperative radiograph |
| Method | deep learning, neural, AI, ChatGPT, YOLO, algorithm |
| Task | level, vertebra, label, identif |

| Supplement | Result |
|---|---|
| Global Spine J 2026 e-posters (PMC13191186) | **Desai & Desai, P0935 [GPT]**; Kairy et al., P0576 (a literature review and survey) |
| Global Spine J 2026 oral (PMC13191170) | No hits |
| Global Spine J 2026 rapid-fire (PMC13191179) | No hits |
| Global Spine J 2025 (PMC12099168, PMC12099171, PMC12099120) | No hits |
| Global Spine J 2024 (PMC11086049, PMC11086047, PMC11086046) | Only Xu et al. in PMC11086046, dual-fluoroscopic 3-D orientation (5) |
| Global Spine J 2023 (PMC10226051), 2019 (PMC6555101), and PMC5724662 | Nothing relevant |
| Global Spine J 2022 (PMC9149629) | Nothing new except Bindels et al., a 2D3D registration method (1) |
| CARS 2022 (PMC9131311) and German Spine Congress 2022 (PMC9614736) | **Not scanned**: no full text was available |

### 4.9 Forward citation (OpenAlex `filter=cites:<work>`)

| Seed | Citing works |
|---|---|
| MVMS | 8 |
| MVMS-SPIE | 2 |
| VDVM | 4 |
| Li16 | 21 |
| Li17 | 2 |
| ABL | 3 |
| Otake 2012 | 79 |
| Lo 2015 | 32 |
| Manbachi 2018 | 8 |
| Kausch 2022 | 10 |
| Rao 2024 | 0 |

- **Screening.** Every citing title was read. For Otake 2012 and Lo 2015, the titles were first filtered for terms
  meaning learning, network, detection, labelling or identification.
- **New records.**
  - ABLSpineLevelCheck, which cites both MVMS and Otake 2012.
  - ProVLNet and X2P-Net, which cite MVMS.
  - The CMIG 2025 survey of vertebra-analysis methods (PMID 41033041). It has no abstract in Crossref and was not
    read.
- **Result.** No citing work reports registration-free naming on real intraoperative images.

## 5. Classified candidates

PMID "—" means the record is not indexed in PubMed.

### 5.1 Class 3: intraoperative and content-based, with a metric on real intraoperative images

**[VDVM] Zhang R, Hu Y, Zhang K, et al. VDVM: An automatic vertebrae detection and vertebral segment matching
framework for C-arm X-ray image identification. J Xray Sci Technol 2023;31(5):935–949.
DOI 10.3233/XST-230025 · PMID 37393485.**

- **How it works.** It detects vertebrae on C-arm images (YOLOv3) and segments them (Mobile-Unet). It then
  **matches** each vertebra against the same patient's digital radiograph (DR). Level identity therefore comes from
  the preoperative 2-D radiograph, not from the C-arm image alone. No CT or MR is used.
- **Numbers, verbatim from the abstract:** "We use 382 C-arm X-ray images and 203 full length X-ray images to train
  the vertebra detection model, and achieve a mAP of 0.87 in the test dataset of 31 C-arm X-ray images and 0.96 in
  the test dataset of 31 lumbar DR images. Finally, we achieve a vertebral segment matching accuracy of 0.733 on 31
  C-arm X-ray images."
- **Stated premise, verbatim:** "In clinical surgery, the surgeon often determines the specific surgical location by
  comparing C-arm X-ray images with digital radiography (DR) images."
- **Not stated in the abstract:** the number of patients. The full text is closed (IOS Press and SAGE returned 403),
  so any per-vertebra recall inside the paper is unread.
- **Bearing.** It counters S2, because identity comes from a 2-D radiograph rather than a CT or MR. It bears on S1b,
  because it reports a per-vertebra detection metric (mAP) on real C-arm images. Its naming accuracy of 73.3% is
  far below what counting needs.

**[GPT] Desai S, Desai A. Can ChatGPT prevent wrong level spine surgery? Global Spine J 2026;16(2 Suppl):476S–1070S,
e-poster P0935 (ID AGS26/2241). Supplement DOI 10.1177/21925682261435811 (resolves; Crossref title "E-Posters") ·
PMC13191186 · no PMID for the individual abstract.**

- **Method, verbatim:** "Intraoperative fluoroscopic images were obtained from the electronic medical record,
  anonymized, and used in the body of a prompt asking ChatGPT to identify the spinal level where the marker was
  located."
- **Result, verbatim:** "A total of 75 degenerative spine cases were reviewed with 37.3 % being cervical, 6.6%
  thoracic , and 56% lumbar. There were no cases of transitional anatomy. ChatGPT agreed with a board certified
  neurosurgeon in just 28% of cases."
- **Bearing.** A negative result: the level was called per image on real intraoperative fluoroscopy, and the model
  agreed 28% of the time. This is a conference abstract, not a peer-reviewed paper.

**[SV] Rao PY (listed in PubMed as "P YR"), S G, R D, et al. Spine Vision – X-Ray Image based GUI Planning of Pedicle
Screws Using Enhanced YOLOv5 for Vertebrae Segmentation. Proc IEEE EMBC 2024:1–6.
DOI 10.1109/EMBC53108.2024.10781813 · PMID 40039607. Full text read from arXiv:2407.08349.**

Companion paper: Maik V, Purayath A, R D, Lakshmanan M, Sivaprakasam M. GUI-based Pedicle Screw Planning on
Fluoroscopic Images Utilizing Vertebral Segmentation. arXiv:2407.08347 (2024). DOI 10.48550/arXiv.2407.08347
(DataCite; resolves) · PMID —.

- **Data, verbatim from 2407.08349:** "trained and tested on a dataset consisting of 578 images obtained from patients,
  cadavers, and phantoms. This dataset was divided into 500 training images, 58 validation images, and 20 test
  images". The C-arms were a GE-OEC Fluorostar, a Ziehm 8000 and a Siemens Cios Fit.
- **Numbers, verbatim rows of Table II (precision / recall / mAP@0.5 / mAP@0.5:0.95):**
  "YOLOv5 0.93128 0.98214 98.66 83.8" and "Spine-Vision 0.9417 0.96429 98.215 80.9".
- **Why the classification is ambiguous (3 or 4).** The companion preprint describes the same set as "578 images
  obtained from cadavers and lumbar phantoms". The paper does not say which split Table II reports, and the split
  was made by image, not by subject.
- **It names no levels.** From the companion preprint, verbatim: "The surgeon maps the surgical vertebrae of interest
  to the bounding box of the specific vertebrae once identified."
- **Bearing.** It contradicts S1b as worded, because a per-vertebra recall on C-arm images is published. It does
  not contradict S1a.

### 5.2 Unresolved (U): relevant, but the abstract cannot classify it and the full text could not be read

These three records are the only ones found that could still falsify S1a. Read them before submission, through
IEEE Xplore with institutional access.

**[Li16] Li Y, Liang W, Zhang Y, An H, Tan J. Automatic lumbar vertebrae detection based on feature fusion deep
learning for partial occluded C-arm X-ray images. Proc IEEE EMBC 2016. DOI 10.1109/EMBC.2016.7590785 ·
PMID 28268411.**

- **Abstract, verbatim:** "a novel convolutional neural network (CNN) model to automatically detect lumbar vertebrae
  for C-arm X-ray images. Training data is augmented by DRR".
- **No numbers:** "Comprehensive qualitative and quantitative experiments demonstrate that our proposed model
  performs more accurate in abnormal cases with pathologies and surgical implants in multi-angle views."
- **Unknown:** whether the test images are real intraoperative images, whether levels are named, and the recall.

**[Li17] Li Y, Liang WG, Tan J. Bi-Directional LSTM Recurrent Neural Network for Lumbar Vertebrae Identification in
X-Ray Images. Proc ICCSEC 2017. DOI 10.1109/ICCSEC.2017.8446758 · PMID —.**

- **Abstract, verbatim:** "mobile C-arm X-ray images play a key role in image-guided minimally invasive spine
  surgery … a novel automatic lumbar vertebrae identification method is proposed".
- **Unclear input:** "the curvature features of 3D lumbar vertebrae model, which are common to the 2D X-ray images,
  are taken as the input". The abstract does not say whether that 3-D model is the patient's CT.
- **No numbers:** "our method identified lumbar vertebrae more accurately than another two methods."

**[ABL] Jiang J, Shuai L, Zeng Q. ABLSpineLevelCheck: Localization of Vertebral Levels on Fluoroscopy via
Semi-supervised Abductive Learning. Proc IEEE BIBM 2024 (short paper). DOI 10.1109/BIBM62325.2024.10822817 ·
PMID —.**

- **Abstract, verbatim:** "unannotated spinal fluoroscopic images are processed by the networks to infer pseudo-labels
  for vertebra localization … we propose an ensemble technique that amalgamates semantic detection of vertebral
  levels with instance detection … we have synthesized a dataset and annotated the BUU dataset for network
  pre-training."
- **What the abstract lacks:** any number, the image count, and whether the images are intraoperative.
- **Bearing on S2.** Its title and abstract describe registration-free level localisation on fluoroscopy, so it
  counts against S2 whatever its numbers turn out to be.
- **Other sources checked:** the first author's page (threestones1029.github.io) and GitHub repositories. Neither
  holds a preprint or any numbers.

### 5.3 Class 4: simulated or cadaver only

**Vertebral level labelling or identification**

| Tag | Citation | DOI · PMID | Data | Numbers (verbatim where quoted) |
|---|---|---|---|---|
| MVMS | Huang Y, Jones CK, Zhang X, et al. Multi-perspective region-based CNNs for vertebrae labeling in intraoperative long-length images. Comput Methods Programs Biomed 2022;227:107222 | 10.1016/j.cmpb.2022.107222 · 36370597 | Trained on images synthesised from 297 CTs. Tested on O-arm **Long-Film** (slot-scan tomosynthesis, not C-arm fluoroscopy): "50 AP and 50 lateral Long-Film images acquired from 13 cadaveric specimens" | "F1 score of >96% and an average vertebral localization error of 3.3 mm, with 88.3% labeling accuracy on both AP and lateral images". **Registration-free naming, in cadavers only** |
| MVMS-SPIE | Huang Y, Jones CK, Zhang X, et al. Automatic labeling of vertebrae in long-length intraoperative imaging with a multi-view, region-based CNN. Proc SPIE 12034:120340U (2022) | 10.1117/12.2611912 · — | "trained and validated on 11,805 Long-Film images simulated from projections of 370 CT images and tested on 50 Long-Film images of 14 cadaveric specimens" | "91.7% vertebrae level identification rate, compared to 72.4% when used without LSTM" |
| Twin | Killeen BD, Suresh A, Gomez C, et al. Intelligent control of robotic X-ray devices using a language-promptable digital twin. Int J CARS 2025 | 10.1007/s11548-025-03351-y · 40205315 | One cadaver ("torso section from the mid-femur to the T2 vertebra … 60 year-old female donor") imaged on a Loop-X: "80 X-ray images … of which 46 were from unique viewpoints" | "a single image may not provide enough visual context to distinguish between similar vertebrae levels (0.04 DICE) or rib bones (0.02 DICE) without additional point prompting". Quoted from arXiv:2412.08020v1, because the published full text could not be reached. All vertebrae segmented as one class: 0.78 ± 0.15. **A per-level negative result on real C-arm images** |
| FSAM | Killeen BD, Wang LJ, Iñígo B, et al. FluoroSAM: A Language-Promptable Foundation Model for Flexible X-Ray Image Segmentation. MICCAI 2025, LNCS 15966:248–258 | 10.1007/978-3-032-04981-0_24 · 41573335 | The same single cadaver: "1,741 masks suitable for evaluation" | "With text prompts, FluoroSAM achieves a mean Intersection over Union (IoU) of 0.47 and a Dice score of 0.60". No per-vertebra number is reported |
| ProVL | Ye K, Sun W, Tao R, et al. A Projective-Geometry-Aware Network for 3D Vertebra Localization in Calibrated Biplanar X-Ray Images. Sensors 2025;25(4):1123 | 10.3390/s25041123 · 40006352 | "two typical yet challenging datasets of digitally reconstructed radiograph (DRR) images which were simulated from Computed Tomography (CT) scans". The lumbar set had 130 CTs, 20 used for testing, with L1–L5 fixed | ID rate 99.53% (lumbar DRR) and 98.98% (thoracic DRR). "A landmark is considered accurately identified if the distance … is below 5.0 mm." **Simulated only** |
| X2P | Tao R, Ye K, Zhang W, et al. X2P-Net: Context-Aware 2D/3D Vertebra Localization. Bioengineering 2026;13(2):178 | 10.3390/bioengineering13020178 · 41749718 | "a large-scale synthetic dataset (BiSpineX) and a sheep spine dataset (SheepSpineX)" | "96.9% and 98.8% at 10 mm and 20 mm thresholds" (BiSpineX); 98.4% and 100.0% (sheep). These are localisation results; naming is not reported separately |
| MVL-DRR | Ahmad IA, Ali S, Jung SK. Multi-View Learning for Vertebrae Identification in Digitally Reconstructed Radiographs. Proc HSI 2025 | 10.1109/HSI66212.2025.11142408 · — | DRRs of VerSe 2019 | The abstract gives no numbers ("outperformed other state-of-the-art (SOTA) methods") |

**Other simulated or cadaver work (not level identification)**

| Tag | Citation | DOI · PMID | Data | Numbers (verbatim where quoted) |
|---|---|---|---|---|
| Klitzner | Klitzner F, Inigo Romillo B, Killeen BD, et al. Investigating robot control policy learning for autonomous x-ray-guided spine procedures. Int J CARS 2026 | 10.1007/s11548-026-03716-x · 42171653 | In-silico sandbox | "succeeded on the first attempt in 68.5% of cases". Not level identification |
| X23D | Jecklin S, Jancik C, Farshad M, et al. X23D—Intraoperative 3D Lumbar Spine Shape Reconstruction Based on Sparse Multi-View X-ray Data. J Imaging 2022;8(10):271 | 10.3390/jimaging8100271 · 36286365 | DRRs from CTSpine1K | "88% average F1 score". 3-D reconstruction of a known vertebra, not naming |
| X23D-DA | Jecklin S, Shen Y, Gout A, et al. Domain adaptation strategies for 3D reconstruction of the lumbar spine using real fluoroscopy data. Med Image Anal 2024;98:103322 | 10.1016/j.media.2024.103322 · 39197301 | Real fluoroscopy of ex-vivo torsos | "84% F1 score". Reconstruction of a known target vertebra, not naming |
| Pelphix | Killeen BD, Zhang H, Mangulabnan J, et al. Pelphix: Surgical Phase Recognition from X-ray Images in Percutaneous Pelvic Fixation. MICCAI 2023 | 10.1007/978-3-031-43996-4_13 · 38617200 | Pelvis, simulated and cadaver | "99.2% on simulated sequences and 71.7% in cadaver". **Pelvis, not spine**; listed only because it was named as the example |
| SyntheX | Gao C, Killeen BD, Hu Y, et al. Synthetic data accelerates the development of generalizable learning-based algorithms for X-ray image analysis. Nat Mach Intell 2023 | 10.1038/s42256-023-00629-1 · 38523605 | Hip imaging, simulated-to-real | No vertebra task. Context only |

### 5.4 Class 1: registration-based (identity imported from a preoperative CT or MR)

**LevelCheck lineage (Johns Hopkins I-STAR)**

| Paper | Detail | DOI · PMID |
|---|---|---|
| Otake Y et al. Phys Med Biol 2012;57:5485 | 99.998% success, defined as mean projection distance under 5 mm (1 failure in 50,000 simulated trials) | 10.1088/0031-9155/57/17/5485 · 22864366 |
| Otake Y et al. Proc SPIE 2012 | | 10.1117/12.911308 · — |
| Otake Y et al. Phys Med Biol 2013 | Robust registration under deformation | 10.1088/0031-9155/58/23/8535 · 24246386 |
| Lo SF et al. Spine 2015 | 20 patients; 100% at 200 multistarts, 99.3% at 50 | 10.1097/BRS.0000000000000814 · 25646750 |
| Otake Y et al. Phys Med Biol 2015 | Mobile radiographs | 10.1088/0031-9155/60/5/2075 · 25674851 |
| De Silva T et al. Spine 2016 | 398 radiographs; "100% geometric accuracy"; utility rated by questionnaire | 10.1097/BRS.0000000000001589 · 27035579 |
| De Silva T et al. Phys Med Biol 2016 | Similarity metrics | 10.1088/0031-9155/61/8/3009 · 26992245 |
| Ketcha MD et al. Proc SPIE 2016 | Automatic masking | 10.1117/12.2216913 · 27335531 |
| De Silva T et al. Phys Med Biol 2017 | MR-LevelCheck | 10.1088/1361-6560/62/2/684 · 28050972 |
| Ketcha MD et al. Phys Med Biol 2017 | msLevelCheck | 10.1088/1361-6560/aa6b3e · 28375139 |
| Manbachi A et al. Ann Biomed Eng 2018 | 62 difficult radiographs: median surgeon error 30.4% without assistance, 2.4% with LevelCheck | 10.1007/s10439-018-2099-2 · 30051244 |

**Same group: known-component and long-length registration**

| Paper | DOI · PMID |
|---|---|
| Uneri A et al. Phys Med Biol 2015 | 10.1088/0031-9155/60/20/8007 · 26421941 |
| Uneri A et al. Proc SPIE 2015 | 10.1117/12.2082210 · 26028805 |
| Uneri A et al. MICCAI 2016 (deformable KC) | 10.1007/978-3-319-46726-9_15 · 37195053 |
| Uneri A et al. Phys Med Biol 2017 | 10.1088/1361-6560/aa62c5 · 28233760 |
| Yi T et al. J Med Imaging 2018 | 10.1117/1.JMI.5.2.021212 · 29430481 |
| Yi T et al. Proc SPIE 2018 | 10.1117/12.2322408 · 36092693 |
| Uneri A et al. Proc SPIE 2018 (O-arm) | 10.1117/12.2293874 · 34290469 |
| Uneri A et al. Proc SPIE 2019 (virtual long-film) | 10.1117/12.2513679 · 34290470 |
| Zhang X et al. Phys Med Biol 2021 (long-length tomosynthesis) | 10.1088/1361-6560/abde96 · 33477120 |
| Zhang X et al. Med Phys 2022 | 10.1002/mp.15819 · 35762028 |
| Huang Y et al. Comput Med Imaging Graph 2024 (MR to Long-Film) | 10.1016/j.compmedimag.2024.102365 · 38471330 |

**Other groups**

| Paper | DOI · PMID |
|---|---|
| Oulbacha R, Kadoury S. Med Phys 2020 (MRI to C-arm) | 10.1002/mp.14534 · 33063353 |
| Varnavas A et al. IEEE TMI 2013 | 10.1109/TMI.2012.2227337 · 23362246 |
| Varnavas A et al. Med Image Anal 2015 | 10.1016/j.media.2015.08.005 · 26387052 |
| Naik RR et al. Med Biol Eng Comput 2022 (C-arm to preoperative CT, "vertebral localization") | 10.1007/s11517-022-02600-5 · 35680729 |
| Naik RR et al. J Imaging 2022 | 10.3390/jimaging8070185 · 35877629 |
| Abumoussa A et al. Neurosurg Focus 2023 (82% convergence on DRRs) | 10.3171/2023.3.FOCUS2345 · 37552666 |
| Gopalakrishnan V et al. Nature 2026 (xvr: patient-specific networks trained from the preoperative scan) | 10.1038/s41586-026-11045-x · 42749809 |
| Shen A et al. Med Phys 2026 | 10.1002/mp.70385 · 41833531 |
| Jiang J et al. Med Image Anal 2026 (RadGS-Reg+; same first author as ABL) | 10.1016/j.media.2026.104319 · 42766966 |
| Wu Z et al. Med Image Anal 2026 (DVAP-Reg) | 10.1016/j.media.2025.103930 · 41506054 |
| Kiran U et al. Eur Spine J 2024 (MR to X-ray, simulated) | 10.1007/s00586-023-08054-z · 38104308 |
| Shao MH et al. Zhonghua Yi Xue Za Zhi 2024 | 10.3760/cma.j.cn112137-20240408-00815 (CMA DOI; resolves at doi.org, not in Crossref) · 39375133 |
| Ye W et al. Bioengineering 2025 | 10.3390/bioengineering12020114 · 40001635 |
| Bullert B et al. Brain Spine 2025 | 10.1016/j.bas.2025.104395 · 40951792 |
| Bullert B et al. Eur Spine J 2026 | 10.1007/s00586-025-09451-2 · 41081847 |
| Bindels BJJ et al. Int J CARS 2022 (skin-marker 3D2D) | 10.1007/s11548-022-02733-w · 35986831 |
| Khan A et al. Neurosurg Focus 2022 (CT-to-fluoroscopy registration vs scan-and-plan) | 10.3171/2021.10.FOCUS21506 · 34973678 |
| Esfandiari H et al. Int J CARS 2019 | 10.1007/s11548-019-02024-x · 31292926 |
| Chang CJ et al. Appl Bionics Biomech 2015 | 10.1155/2015/478062 · 27018859 |

LevelCheck's headline numbers measure either geometric registration success or label placement given a CT that
has already been labelled. Neither is naming accuracy from image content. Every one of these methods needs a
labelled preoperative CT or MR of the same patient.

### 5.5 Commercial systems

- **VUZE System (Vuze Medical): K210830 (2022) and K232976 (2024).**
  - The indications in the 510(k) summary read, verbatim: "intended to enable users to load pre-operative 3D images
    and planning data and register and overlay this data in real time with intra-operative 2D radiographic images".
    This is the **registration class**.
  - Accuracy testing covered tool position. The summary makes no level-identification claim.
  - It was integrated with the Siemens Cios Spin in September 2026, still depending on a preoperative CT or an
    intraoperative CBCT.
- **ARAI (K211254) and HOLO Portal (K231611), Surgalign.** Both work on intraoperative **CT** ("relative to
  intraoperative CT images of the anatomy"). They are not 2-D fluoroscopy systems.
- **Proprio (cleared 2025) and SyncAR Spine (Surgical Theater).** Optical or CT-based, so out of scope.
- **Philips patent US 10,405,821 B2 (priority 2014).** It stitches X-ray frames into a panorama and finds the target
  level either by counting from a landmark or by registering to CT or MR. It is a patent, with no published
  evaluation.
- **No device found.** No FDA 510(k) summary was found for a device that identifies spinal levels from the content
  of 2-D intraoperative fluoroscopy, and no published accuracy study of such a device.

### 5.6 Class 2: adjacent work on plain film (and other modalities), not counter-examples

| Paper | Note | DOI · PMID |
|---|---|---|
| Kim JK et al. J Int Med Res 2024 | L5 on AP lumbar radiographs; precision 95.7%, recall 97.8% | 10.1177/03000605231223881 · 38206194 |
| Chen Y et al. (VertXNet) Sci Rep 2024 | C2 or S1 anchor, then "zip" | 10.1038/s41598-023-49923-3 · 38336974 |
| Kwak D et al. J Clin Med 2025 | Binary LSTV classifier | 10.3390/jcm14217671 · 41227066 |
| Kónya S et al. J Craniovertebr Junction Spine 2021 | | 10.4103/jcvjs.jcvjs_186_20 · 34194159 |
| Cina A et al. Sci Rep 2021 | | 10.1038/s41598-021-89102-w · 33947917 |
| Kim KC et al. CMPB 2021 | | 10.1016/j.cmpb.2020.105833 · 33250283 |
| Mushtaq M et al. Sensors 2022 | | 10.3390/s22041547 · 35214448 |
| Jung S et al. Front Pediatr 2026 | T1, T7 and T12 on neonatal chest radiographs | 10.3389/fped.2026.1673925 · 41727769 |

Also seen and assigned to class 2: VLD-Net (JBHI 2025), YOLO11-MSCA (Electronics 2026), ACM ICICS 2026, SpineFM,
VinDr-SpineXR.

**Other modalities**

| Paper | Modality | DOI · PMID |
|---|---|---|
| Zhang S et al. (SpineCLUE) Artif Intell Med 2026 | Diagnostic CT | 10.1016/j.artmed.2025.103285 · 41172576 |
| Hetherington J et al. (SLIDE) Int J CARS 2017 | Ultrasound | 10.1007/s11548-017-1575-8 · 28361323 |
| Baka N et al. IEEE TMI 2017 | Ultrasound | 10.1109/TMI.2017.2738612 · 28809678 |

### 5.7 Class 5: screened because the title was plausible, but not level identification

| Paper | Why it is not level identification |
|---|---|
| Kausch 2020 IJCARS (32533315) and Kausch 2022 MedIA (35933944) | C-arm pose regression without CT; the region of interest is fixed ("the fourth lumbar vertebra (LV4)") and no level is identified |
| Liu 2026 Eur Spine J (41910750) and SX-Stitch (ICASSP 2025) | Intraoperative C-arm stitching; Liu detects pedicle screws; neither names vertebrae |
| Aubert 2023 IEEE TMI (36318556) | Statistical-model 3D/2D registration on biplanar radiographs |
| Liu 2020 J Digit Imaging (31602548) | Diagnostic video-fluoroscopy tracking; the first frame is labelled by hand |
| Auloge 2020 Eur Spine J (31270676) | AR/AI vertebroplasty guidance |
| Pan 2021 CMPB (34736173) | Marker detection for PETD navigation |
| Esfandiari 2018 IJCARS (29808466) | Screws |
| Doerr 2020 SPIE (36082205) | Instrumentation |
| Siemionow 2020 (32904970) | Intraoperative CT |
| Gami 2022 J Neurosurg Spine (36303475) | Camera and markers |
| Dharnipragada 2022 Radiol Case Rep (35570868) | O-arm 2D Long Film used for **manual** counting |
| Front Robot AI 2026 (41836345) | CT-free vertebroplasty path planning |
| IJCARS 2021 (33973113) | CT-to-stereovision level-wise registration; not X-ray |
| Xu 2025 (CAAI) | Dual-fluoroscopy orientation |
| Samaratunga 2024 (TechRxiv) | Quantitative-fluoroscopy detection |

**Reviews read for method leads**

- **Liebrand 2026 Eur Spine J** (systematic review; 10.1007/s00586-026-09925-x · 42009915). Its "advanced methods"
  group has n = 5. Only the abstract was read, because Springer is paywalled.
- **Girgis 2026 J Clin Med** (PMC13073321), **Javadnia 2025 Patient Saf Surg** (PMC12080030) and **Arjmandnia 2024
  Patient Saf Surg** (PMC10964577). None cites a registration-free method for fluoroscopy.
- **MacLeod 2025 Curr Rev Musculoskelet Med** (PMC12325831). It states: "AI vertebral level identification has been
  shown to be effective using both CT and fluoroscopic images [26, 27]". Reference 26 is Siemionow 2020, which uses
  intraoperative **CT**. Reference 27 is Yamout 2023, a narrative review of navigation, robotics and AR. No
  fluoroscopic content-based source stands behind the claim, so do not cite this review as evidence that the
  capability exists.

## 6. What is not known

- **Three unread papers could still falsify S1a:** Li 2016, Li 2017 and ABLSpineLevelCheck 2024.
  - All three sit behind IEEE Xplore, which blocked every automated access path from this machine.
  - None of the three abstracts gives a number.
  - The ABL abstract mentions pretraining on the BUU dataset (plain lumbar radiographs). Its fluoroscopic test set,
    and whether that set is intraoperative, are unknown.
  - **Read all three before submission.**
- **VDVM:** the full text is unread. The abstract does not state the number of patients behind the 31 C-arm test
  images, whether they are intraoperative, or whether the paper reports a per-vertebra recall.
- **Rao 2024** describes its image set two ways: "patients, cadavers, and phantoms" in the EMBC paper, but
  "cadavers and lumbar phantoms" in the companion preprint. It is therefore uncertain whether the 0.96–0.98 recall
  includes any intraoperative image of a living patient.
- **Killeen 2025:** the Dice of 0.04 per level is quoted from arXiv v1. The published IJCARS full text could not be
  retrieved: Europe PMC has no XML, and PMC served a challenge page.
- **Coverage gaps:**
  - Semantic Scholar query S13 was not executed.
  - Google Scholar, IEEE Xplore and SPIE were reached only through a general web engine.
  - CNKI and Wanfang were not searched; a single Chinese-language web query found nothing.
  - Patents were not searched systematically.
  - Abstract supplements were scanned only where Europe PMC holds full text (Global Spine J 2019–2026). The CARS and
    German Spine Congress books could not be reached.
  - Records posted after 22 September 2026 are not covered.
- **Absence of evidence:** "we found no …" rests on silence across the engines above, not on a source that looked
  and reported none. The 2026 systematic review (Liebrand) is the nearest independent check, and its full text was
  not read.

## Appendix A: Verification of identifiers (run 2026-09-22)

The method is described in §3. "302" means doi.org redirected, so the DOI is registered. "CR" means the title
returned by Crossref matches. "PM" means the title returned by PubMed esummary matches.

| Tag | Class | DOI | doi.org | CR | PMID | PM |
|---|---|---|---|---|---|---|
| Otake 2012 PMB | 1 | 10.1088/0031-9155/57/17/5485 | 302 | ✓ | 22864366 | ✓ |
| Otake 2012 SPIE | 1 | 10.1117/12.911308 | 302 | ✓ | — | — |
| Otake 2013 PMB | 1 | 10.1088/0031-9155/58/23/8535 | 302 | ✓ | 24246386 | ✓ |
| Lo 2015 Spine | 1 | 10.1097/BRS.0000000000000814 | 302 | ✓ | 25646750 | ✓ |
| Otake 2015 PMB | 1 | 10.1088/0031-9155/60/5/2075 | 302 | ✓ | 25674851 | ✓ |
| De Silva 2016 Spine | 1 | 10.1097/BRS.0000000000001589 | 302 | ✓ | 27035579 | ✓ |
| De Silva 2016 PMB | 1 | 10.1088/0031-9155/61/8/3009 | 302 | ✓ | 26992245 | ✓ |
| Ketcha 2016 SPIE | 1 | 10.1117/12.2216913 | 302 | ✓ | 27335531 | ✓ |
| De Silva 2017 PMB | 1 | 10.1088/1361-6560/62/2/684 | 302 | ✓ | 28050972 | ✓ |
| Ketcha 2017 PMB | 1 | 10.1088/1361-6560/aa6b3e | 302 | ✓ | 28375139 | ✓ |
| Manbachi 2018 | 1 | 10.1007/s10439-018-2099-2 | 302 | ✓ | 30051244 | ✓ |
| Uneri 2015 PMB | 1 | 10.1088/0031-9155/60/20/8007 | 302 | ✓ | 26421941 | ✓ |
| Uneri 2015 SPIE | 1 | 10.1117/12.2082210 | 302 | ✓ | 26028805 | ✓ |
| Uneri 2016 MICCAI | 1 | 10.1007/978-3-319-46726-9_15 | 302 | ✓ | 37195053 | ✓ |
| Uneri 2017 PMB | 1 | 10.1088/1361-6560/aa62c5 | 302 | ✓ | 28233760 | ✓ |
| Yi 2018 JMI | 1 | 10.1117/1.JMI.5.2.021212 | 302 | ✓ | 29430481 | ✓ |
| Yi 2018 SPIE | 1 | 10.1117/12.2322408 | 302 | ✓ | 36092693 | ✓ |
| Uneri 2018 SPIE | 1 | 10.1117/12.2293874 | 302 | ✓ | 34290469 | ✓ |
| Uneri 2019 SPIE | 1 | 10.1117/12.2513679 | 302 | ✓ | 34290470 | ✓ |
| Zhang 2021 PMB | 1 | 10.1088/1361-6560/abde96 | 302 | ✓ | 33477120 | ✓ |
| Zhang 2022 Med Phys | 1 | 10.1002/mp.15819 | 302 | ✓ | 35762028 | ✓ |
| Huang 2024 CMIG | 1 | 10.1016/j.compmedimag.2024.102365 | 302 | ✓ | 38471330 | ✓ |
| Oulbacha 2020 | 1 | 10.1002/mp.14534 | 302 | ✓ | 33063353 | ✓ |
| Varnavas 2013 | 1 | 10.1109/TMI.2012.2227337 | 302 | ✓ | 23362246 | ✓ |
| Varnavas 2015 | 1 | 10.1016/j.media.2015.08.005 | 302 | ✓ | 26387052 | ✓ |
| Naik 2022 MBEC | 1 | 10.1007/s11517-022-02600-5 | 302 | ✓ | 35680729 | ✓ |
| Naik 2022 J Imaging | 1 | 10.3390/jimaging8070185 | 302 | ✓ | 35877629 | ✓ |
| Abumoussa 2023 | 1 | 10.3171/2023.3.FOCUS2345 | 302 | ✓ | 37552666 | ✓ |
| Gopalakrishnan 2026 | 1 | 10.1038/s41586-026-11045-x | 302 | ✓ | 42749809 | ✓ |
| Shen 2026 | 1 | 10.1002/mp.70385 | 302 | ✓ | 41833531 | ✓ |
| Jiang 2026 RadGS-Reg+ | 1 | 10.1016/j.media.2026.104319 | 302 | ✓ | 42766966 | ✓ |
| Wu 2026 DVAP-Reg | 1 | 10.1016/j.media.2025.103930 | 302 | ✓ | 41506054 | ✓ |
| Kiran 2024 | 1 | 10.1007/s00586-023-08054-z | 302 | ✓ | 38104308 | ✓ |
| Shao 2024 | 1 | 10.3760/cma.j.cn112137-20240408-00815 | 302 | not in Crossref (CMA) | 39375133 | ✓ |
| Ye 2025 | 1 | 10.3390/bioengineering12020114 | 302 | ✓ | 40001635 | ✓ |
| Bullert 2025 | 1 | 10.1016/j.bas.2025.104395 | 302 | ✓ | 40951792 | ✓ |
| Bullert 2026 | 1 | 10.1007/s00586-025-09451-2 | 302 | ✓ | 41081847 | ✓ |
| Bindels 2022 | 1 | 10.1007/s11548-022-02733-w | 302 | ✓ | 35986831 | ✓ |
| Khan 2022 | 1 | 10.3171/2021.10.FOCUS21506 | 302 | ✓ | 34973678 | ✓ |
| Esfandiari 2019 | 1 | 10.1007/s11548-019-02024-x | 302 | ✓ | 31292926 | ✓ |
| Chang 2015 | 1 | 10.1155/2015/478062 | 302 | ✓ | 27018859 | ✓ |
| VDVM 2023 | 3 | 10.3233/XST-230025 | 302 | ✓ | 37393485 | ✓ |
| Desai 2026 (supplement) | 3 | 10.1177/21925682261435811 | 302 | ✓ ("E-Posters") | — | — |
| Rao 2024 Spine-Vision | 3/4 | 10.1109/EMBC53108.2024.10781813 | 302 | ✓ | 40039607 | ✓ |
| Maik 2024 (arXiv) | 3/4 | 10.48550/arXiv.2407.08347 | 302 | DataCite (Crossref 404) | — | — |
| Li 2016 EMBC | U | 10.1109/EMBC.2016.7590785 | 302 | ✓ | 28268411 | ✓ |
| Li 2017 ICCSEC | U | 10.1109/ICCSEC.2017.8446758 | 302 | ✓ | — | — |
| ABLSpineLevelCheck 2024 | U | 10.1109/BIBM62325.2024.10822817 | 302 | ✓ | — | — |
| Huang 2022 CMPB | 4 | 10.1016/j.cmpb.2022.107222 | 302 | ✓ | 36370597 | ✓ |
| Huang 2022 SPIE | 4 | 10.1117/12.2611912 | 302 | ✓ | — | — |
| Killeen 2025 IJCARS | 4 | 10.1007/s11548-025-03351-y | 302 | ✓ | 40205315 | ✓ |
| FluoroSAM 2025 | 4 | 10.1007/978-3-032-04981-0_24 | 302 | ✓ | 41573335 | ✓ |
| ProVLNet 2025 | 4 | 10.3390/s25041123 | 302 | ✓ | 40006352 | ✓ |
| X2P-Net 2026 | 4 | 10.3390/bioengineering13020178 | 302 | ✓ | 41749718 | ✓ |
| Ahmad 2025 HSI | 4 | 10.1109/HSI66212.2025.11142408 | 302 | ✓ | — | — |
| Klitzner 2026 | 4 | 10.1007/s11548-026-03716-x | 302 | ✓ | 42171653 | ✓ |
| X23D 2022 | 4 | 10.3390/jimaging8100271 | 302 | ✓ | 36286365 | ✓ |
| Jecklin 2024 | 4 | 10.1016/j.media.2024.103322 | 302 | ✓ | 39197301 | ✓ |
| Pelphix 2023 | 4 | 10.1007/978-3-031-43996-4_13 | 302 | ✓ | 38617200 | ✓ |
| SyntheX 2023 | 4 | 10.1038/s42256-023-00629-1 | 302 | ✓ | 38523605 | ✓ |

Class-2 and class-5 identifiers were checked the same way and all passed: VertXNet, Kwak, Kim 2024, Kónya, Cina,
Kim 2021, Mushtaq, Jung, SpineCLUE, SLIDE, Baka 2017, Kausch 2020, Kausch 2022, Liu 2026, Liebrand 2026,
Siemionow 2020, Doerr 2020, Aubert 2023 and the 2026 path-planning paper.
