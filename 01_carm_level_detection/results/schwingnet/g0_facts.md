# G0 facts, with evidence (2026-09-24)

Written by the G0 fact-finding step. No .tex, .bib, manifest or table was edited. Paths are absolute;
grid paths are on go2432@grid.wayne.edu. "Ctime" is the file's change time on the grid (`find -printf %C`),
which is when the file landed on that filesystem; archive members keep their packed mtimes, so mtime alone
is not a download date.

## 1. The two Castellvi readers

| | Miraziz Ismoilov | Nizar Alnabahneh |
|---|---|---|
| Ledger initials | MI, "2nd reviewer" | NA, "1st Reviewer" |
| Degree | MD | MD |
| Department (recorded) | Department of Radiology, Detroit Medical Center and Wayne State University | Department of Radiology, Detroit Medical Center and Wayne State University |
| Training year (PGY) | **recorded nowhere** | **recorded nowhere** |
| Greg, 2026-09-24 | "Resident, radiology, Wayne State University" | "Resident, Wayne State University" (department not stated by Greg; every record says Radiology) |

Evidence for the department (both readers, same lines):
- `CTSpinoPelvic1K:paper\mpda\title_page.tex` lines 54-55 (`Miraziz Ismoilov, MD $^{3}$`, `Nizar Alnabahneh, MD $^{3}$`) and lines 62-63 (`$^{3}$Department of Radiology, Detroit Medical Center and Wayne State University, Detroit, Michigan`).
- `CTSpinoPelvic1K:paper\mpda\main.tex` lines 201-203 (`\author{...}` + `\affiliation{Department of Radiology, Detroit Medical Center and Wayne State University, ...}`); line 207 comment: "Affiliations were confirmed by the corresponding author: the annotators are School of Medicine, the two readers are Radiology."
- `CTSpinoPelvic1K:zenodo\zenodo.json` lines 70-77 (Zenodo/DataCite creators 13 and 14, affiliation "Department of Radiology, Detroit Medical Center / Wayne State University").
- `CTSpinoPelvic1K:paper\mpda\ARXIV_SUBMISSION.md` lines 42-44.
- `CTSpinoPelvic1K:paper\cns2026\make_cns_deck.py` line 358 ("Miraziz Ismoilov and Nizar Alnabahneh (Radiology, DMC/WSU)").
- Role: `title_page.tex` line 90 (CRediT comment): "M.I., N.A. formal analysis (Castellvi grading, hardware adjudication), supervision (CT-reading training of the annotators)".

Evidence that they are residents and that the descriptor's wording is "two radiology resident physicians":
- `CTSpinoPelvic1K:paper\mpda\main.tex` lines 707-710: "Two radiology resident physicians graded every case independently and resolved their six disagreements by consensus; both reads and the consensus are in the manifest. The distinction they disagreed on, type II (articulation) against type III (bony fusion), is the one that matters clinically, and four of the six disagreements were III against II." Also line 898.
- `CTSpinoPelvic1K:zenodo\KNOWN_ISSUES.md` lines 10-11: "33 of 802 records carry a Castellvi grade that is the consensus of two radiology residents".

Searched for a training year and found none: grep for `PGY|postgraduate|resident` over both repos (`CTSpinoPelvic1K-1` incl. docs/, paper/mpda/*.tex, zenodo/, review ledgers, `_roster5.py`, `scratchpad/authors.py`; `spinesurg-ct-nnunet` incl. SchwingNet, docs/, lit/). The only PGY string anywhere is Greg's own signature ("PGY-1, Surgery-Preliminary", `docs/email_update.md` line 118). `SchwingNet/REVISION_LOG2.md` line 86 already records "The years are not in the descriptor."

Ledger spelling: `docs/castellvi_readers_2026-09-04.csv` line 45 and `Lumbosac.csv` line 45 spell the name "Mizaziz Ismoilov (MI)" (a typo in the ledger; every other record has Miraziz).

### "Six disagreements resolved by consensus": confirmed

`CTSpinoPelvic1K:docs\castellvi_consensus.csv` (34 rows; columns volume_id, token, read_1_NA, read_2_MI, agreement, consensus, comment): 27 rows `agreement=True`, 7 rows `agreement=False`. One of the seven is volume 0016 / token 10 (read_1_NA "0", read_2_MI blank, consensus 0): a single unpaired read, not a disagreement (the raw ledger lists it as "reference NL"). The six paired disagreements:

| volume | token | NA | MI | consensus |
|---|---|---|---|---|
| 0033 | 22 | IIa | IIIa | IIa |
| 0176 | 123 | IIb | IIIb | IIb |
| 0179 | 125 | IIb | IIIb | IIb |
| 0196 | 140 | IIa | IIIa | IIa |
| 0268 | 189 | IIIb | IIb | IIIb |
| 0302 | 215 | Ib | IIb | Ib |

Raw ledger agrees: `docs/castellvi_readers_2026-09-04.csv` (identical to `Lumbosac.csv`), rows for tokens 215, 189, 123, 125, 140, 22 carry "agreed on ..." comments.

Aside for the descriptor, not this manuscript: five of the six (22, 123, 125, 140, 189) are II-against-III; only 215 is I-against-II. The descriptor's "four of the six disagreements were III against II" (main.tex line 710) reads as five from the CSV.

### Recommended wording (Methods line ~44)

"CTSpinoPelvic1K from two radiology residents (in-training, Department of Radiology, Wayne State University; years of training not recorded) grading independently, six disagreements resolved by consensus \citep{ctsp1kdescriptor}"

Shorter: "two radiology residents (in-training; Wayne State University)". Never a year. RSNA_AI_REQUIREMENTS.md line 42 asks for training and expertise in years; the record does not hold it, and Greg has not supplied it, so the sentence says so or omits it.

## 2. First download date

### Per source (earliest verifiable acquisition; grid ctimes unless stated)

| Collection (Table 1) | Earliest evidence | Date | Precision |
|---|---|---|---|
| CTSpinoPelvic1K (its CT is TCIA CT COLONOGRAPHY) | `CTSpinoPelvic1K-1` git: first commit 550cfff 2026-04-18 21:50 -0400 already contains `scripts/download_tcia_colonog.py` and `scripts/tcia_index.py`; "fix raw" 8e68379 2026-04-19; "finalize dataset" 8f1ed51 2026-04-25. No on-grid trace of the April download survives (`~/data/hf_export` is gone; `~/CTSpinoPelvic1K/data/patient_db.json` is a 2026-05-16 rebuild). The v11 release used by the paper landed at `~/data/CTSpinoPelvic1K` 2026-09-07 (LICENSE, fetch_from_tcia.py) with labels 2026-09-16. | **April 2026** (repo anchor 18-19 April) | month |
| VerSe 19/20 (via VerSeFusion) | `~/VerSeFusion/data/raw` ctime 2026-05-12 18:16; `unified` 2026-05-12 23:46; `canonical` 2026-05-13 00:01; repo files 2026-05-12 16:21 | 2026-05-12 | day |
| BUU-LSPINE | `~/XRSpinoPelvic1K/data/dataset2024.zip` 2026-08-06 13:43; `.../BUU-LSPINE/AP/0001-F-037Y0.jpg` ctime 2026-08-06 14:11 (the "buu_2000" copy); full v1 re-download `~/spine-detector/data/raw/buu_full` 2026-09-09 22:50; smoke test `buu_v1` 2026-09-01 23:28 | 2026-08-06 | day |
| CSXA | `~/spine-detector/data/raw/csxa/CSXA-dataset-main/LICENSE` ctime 2026-09-01 22:50; images dir 2026-09-09 23:00 | 2026-09-01 | day |
| NHANES II (annotated) | `~/spine-detector/data/raw/nhanes_annotated/NHANESII_Annotations_VertebralOsetophytes.zip` + `.download_complete` 2026-09-01 23:28; full 17,073-film set from 2026-09-09 13:03, `.download_complete` 2026-09-23 03:00 | 2026-09-01 | day |
| VinDr-SpineXR | `~/spine-detector/data/raw/vindr/1.0.0/LICENSE.txt`, `SHA256SUMS.txt` ctime 2026-09-07 17:49; `.download_complete` 2026-09-10 17:25 | 2026-09-07 | day |
| FluoroCap (literature panels) | `~/FluoroCap/openi/*.png` ctime 2026-09-13 15:27; git cc59e71 2026-09-13 15:46 | 2026-09-13 | day |
| TotalSegmentator v2 (v201) | `~/data/TotalSegmentator/dl.log` created 2026-09-14 10:16; `Totalsegmentator_dataset_v201.zip` complete 2026-09-14 12:36 (`dl.status` DL_DONE) | 2026-09-14 | day |
| TotalSegmentator v3 (v300) | `~/data/TotalSegmentator_v3/dl.log` 2026-09-19 12:50; zip complete 2026-09-19 14:36 | 2026-09-19 | day |
| DeepFluoro | `~/deepfluoro/data/ipcai_2020_ds_16x.zip` 2026-09-20 19:25; git 057d77a "Acquire DeepFluoro" 2026-09-20 18:53; vendor DICOM deposit `/rs/rs_grp_oschome/go2432/data/deepfluoro_vendor/*` 2026-09-22 01:23 | 2026-09-20 | day |
| Ljubljana 2D-3D-GS | local `CTSpinoPelvic1K:2D-3D-GS.zip` birth 2026-09-21 13:30; grid `/rs/.../ljubljana/2D-3D-GS.zip` 2026-09-21 14:17 | 2026-09-21 | day |
| COBRA2026 | `/rs/.../cobra2026/COBRA2026_Train_overviews` 2026-09-21 15:21; pilot cases A004/A005 15:25 (DATA_COMPLETENESS_AUDIT.md line 804); git 59bb679 2026-09-21 15:57 | 2026-09-21 | day |
| Geneva hip | `/rs/.../geneva_hip_src/headers.txt` 2026-09-21 16:59, zip 17:00 | 2026-09-21 | day |
| C-ArmLSpine | git aca0a60 "found ... being fetched" 2026-09-21 16:39; `/rs/.../carmlspine/C-ArmLSpine.zip` complete 2026-09-21 17:32, `.ok` 17:33 | 2026-09-21 | day |

`docs/RSNAI_DATA_MANIFEST.json` (built 2026-09-22 06:49 on hao1) lists roots and file counts but carries no download dates, despite `docs/DATASHEET.md` section 3 saying it does. `docs/DATA_COMPLETENESS_AUDIT.md` gives dates only for RSNA-cspine (2026-09-19, unused) and the COBRA pilot (2026-09-21).

### Overall earliest and what to print

- Earliest acquisition of any collection the paper uses: **April 2026** (TCIA CT COLONOGRAPHY, the CT behind CTSpinoPelvic1K; both repos' first commits are 2026-04-18). Defensible at **month** precision; the only day-level anchor is the 18 April 2026 commit that already ships the download script, which bounds the download from above, not below.
- If the sentence should count only collections fetched for this manuscript's own pipeline (CTSpinoPelvic1K taken as a finished release), the earliest external download is VerSe via VerSeFusion, **12 May 2026** (day precision); the first film corpus is BUU-LSPINE, 6 August 2026; the first real-exposure set is DeepFluoro, 20 September 2026.
- Recommended: "analysed between April 2026 and 24 September 2026" (Methods line ~26) and "analysed April--September 2026" (abstract, main.tex line ~91). Do not print a day for April.

## 3. The Ethics line (main.tex line 118)

Full line: "Secondary analysis of de-identified imaging, determined by the institutional human research protection office not to be human participant research (determination 2026-269). C-ArmLSpine and COBRA2026 are used under their own releases (CC BY 4.0 and CC BY-NC 4.0), the Geneva phantom under CC BY-SA 4.0, and the DeepFluoro and Ljubljana cadaveric sets under CC BY-NC-SA 4.0 and CC BY-NC-ND. VinDr-SpineXR was obtained under its PhysioNet data use agreement (\PENDING{G0}{determination covering it, or its removal from the fold models}); the literature fluoroscopy panels are figures of published articles, used for training only and not redistributed. One C-ArmLSpine directory, one patient's rotational acquisition used only for Figure S5, carries a residual name and identifier in its image headers; its frames were exported without header data and checked to carry no identifier value, and the dataset authors were notified on \PENDING{G0}{date notified}."

### The determination itself (context for the whole line)

`CTSpinoPelvic1K:2026_269 Schwing IRB Not HPR Determination 9.2.26.pdf` (14 pages, scanned; page 1 read as an image): Wayne State University IRB Administration Office, "Notice of IRB Administrative Determination: Non-Human Participant Research (HPR)", To Gregory Schwing, From Heather Park-May, **Date September 2, 2026**, Re "Open Spine Consortium: Secondary Analysis of Publicly Available, De-Identified Imaging Datasets and the Derived Annotations, Software, and Models Produced From Them", **WSU IRB HPR Number 2026 269**, materials received via the HPR Determination Tool 09/02/26; "This project does not constitute human participant research ... IRB review and oversight is not required"; digitally signed Helen Craigie 2026.09.02 15:53:20 -04'00'. The memo also says projects "must obtain support from any unaffiliated institution(s) involved" and to contact DMC etc. for authorization, which does not apply (no covered-entity data).

The tool as submitted, `CTSpinoPelvic1K:OSC_HPR_Determination_public_datasets.pdf` (12 pages, text): completed 08/28/2026 by Gregory Schwing, Resident, Department of Surgery, faculty sponsor Loren Schwiebert. Section B item 6 names the source as "Public data archives that release de-identified imaging under open licences **without application or data use agreement** (for example The Cancer Imaging Archive public collections, VerSe, TotalSegmentator)." Item 7/8 states the scope: the determination covers datasets meeting ALL of (1) public and de-identified at source; (2) "can be downloaded by any member of the public without an application, request for permission, eligibility review, or data use agreement"; (3) not restricted-use; (4) no re-identification key; (5) no re-identification attempt. Then: "If a dataset does NOT meet all five criteria -- in particular if it is restricted-use, requires a proposal or application to obtain, or is governed by a data use agreement -- **it falls outside this determination and a separate IRB submission will be made before that dataset is used.**"

### Placeholder A: `\PENDING{G0}{determination covering it, or its removal from the fold models}`

Asks: which determination covers VinDr-SpineXR, obtained under the PhysioNet credentialed data use agreement; or else it must leave the fold models.

Value from the repo: **no determination covers it.** Determination 2026-269's own scope statement (criterion 2, quoted above) excludes DUA-governed data by name and commits to a separate IRB submission before such a dataset is used. No separate submission, determination or HPR number for VinDr-SpineXR exists in either repo (grep `vindr|physionet` over `CTSpinoPelvic1K-1` root PDFs, `docs/`, and `spinesurg-ct-nnunet/docs`, `SchwingNet/*.md`: only the manuscript's own placeholder and REVISION_LOG2 rows 63/77/175). The VinDr download landed on the grid 2026-09-07 17:49, after the tool was completed (08/28) and five days after the memo (09/02). Where VinDr sits: `docs/DATASHEET.md` section 2.6 and Table 1 footnote f: 2,071 films as 2,632 crops in the intraoperative fold banks only (none in the film bank behind the plain-film accuracies; 0 in allspine_v8/v9). So the honest resolutions are: (i) remove VinDr from the fold banks and retrain the fold models (a G5 re-run, not a text edit), or (ii) obtain a separate determination before submission and cite its number. Which one is Greg's decision; the text cannot claim 2026-269 covers it. Note also the "Greg signs no DUAs" premise in the task: the PhysioNet credentialed download requires accepting the PhysioNet Credentialed Health Data License online; how the 2026-09-07 download was authorised is not recorded in either repo.

The other named licences in the line are consistent with the tool's criteria: C-ArmLSpine (Zenodo 10.5281/zenodo.22768651, CC BY 4.0) and COBRA2026 (Zenodo 10.5281/zenodo.21322350, CC BY-NC 4.0) are click-free public releases; Geneva (Yareta, CC BY-SA 4.0), DeepFluoro (JHU Dataverse, CC BY-NC-SA 4.0), Ljubljana (laboratory page, CC BY-NC-ND; `tables/tab_corpus.sources.md` line 167) likewise. Table 1 (`tables/tab_corpus.tex`) itself carries no licence column; the licences are in the Ethics line and `tab_corpus.sources.md`.

### Placeholder B: `\PENDING{G0}{date notified}`

Asks: the date the C-ArmLSpine authors were told that `case134/ori/` (302 XA frames of one rotational acquisition, used only for Figure S5) carries a real patient name and identifier in its headers.

Value: **unknown; no record that a notification was sent.** The finding is dated 2026-09-22 (`docs/RESUME_2026-09-22_PM.md` line 2273; `docs/PATIENT_IDENTITY_SPEC.md` alias 16; `SchwingNet/REVIEW2_RSNA.md` line 90). `SchwingNet/REVISION_LOG2.md` line 76 already states "no record of the report was found" and line 176 asks Greg "Was the dataset authors' notification sent, and when?". Grep for `notif` over `spinesurg-ct-nnunet/docs`, `docs/outreach`, `docs/data_requests` and `SchwingNet` finds nothing else. Until Greg sends it and gives the date, the clause "and the dataset authors were notified on ..." cannot stand; the alternatives are to send the notice (to the Zenodo record's contact) and date it, or to drop the clause and say only what was done to the frames.

## 4. Age and sex by source (Greg's add-on: "a small script over release metadata")

Not a G0 field in the structured output; recorded here because Greg asked. Counted locally from release metadata copied off the grid (no computation on the login node):

| Source | Age / sex in the release? | Tally |
|---|---|---|
| CTSpinoPelvic1K (`CTSpinoPelvic1K-1/data/zenodo_deposit/manifest.json`, fields `age`, `sex`) | yes | 802: female 393, male 345, other 11, none 53; age present 709, median 59, range 50-89 (matches descriptor main.tex lines 801-804). The 801 used (0533 out): female 393, male 344, other 11, none 53; age n 708, median 59, range 50-89. |
| TotalSegmentator v2 (`meta.csv`, `age;gender`) | yes | 1,228 scans: m 716, f 510, blank 2; age n 1,227, median 65, range 15-98 (release-wide; the paper's 1,170 renders are a subset, and 24 renumbered pairs/three duplicate groups per Table 1 note c are not de-duplicated here) |
| TotalSegmentator v3 (`meta.csv`) | yes | 1,939 scans: m 1,100, f 823, blank 16; age n 1,924, median 61, range 0-118 (release-wide; paper uses 1,735 renders) |
| BUU-LSPINE (sex and age are in the file names `NNNN-F-013Y0`) | yes | 3,600 cases: F 2,280, M 1,320; age median 57, range 6-97 |
| VerSe 19/20 | no per-subject age/sex in the release | -- |
| CSXA | none found in the release files inspected | -- |
| NHANES II | demographics exist at CDC, not in the annotation archive or the film index on disk | not counted |
| VinDr-SpineXR | DICOM headers; needs a grid job to read | not counted (and see placeholder A) |
| C-ArmLSpine, DeepFluoro, COBRA2026, Geneva, Ljubljana, FluoroCap | none (DATASHEET section 2.4; COBRA metadata.yaml carries ages per `docs/HANDOFF` "properties plot ... ages" but was not read here) | as the text says |

Files behind the tallies: `laptop-scratchpad:agesex\{ts_v2_meta.csv, ts_v3_meta.csv, buu_names.txt}` (scratch; re-copy from `~/data/TotalSegmentator/meta.csv`, `~/data/TotalSegmentator_v3/Totalsegmentator_dataset_v300/meta.csv`, `ls ~/spine-detector/data/raw/buu_full/BUU-LSPINEv1/{AP,LA}` to reproduce). A subset-exact tally for the renders actually in the banks needs the bank manifests and is a separate step.
