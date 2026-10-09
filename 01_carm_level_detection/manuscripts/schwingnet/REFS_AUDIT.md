# Reference audit: SchwingNet/refs.bib

Re-run 2026-09-24, 05:27–05:55 EDT, against live records. It replaces the audit of 2026-09-23 (evening).
Every finding of that audit was checked again today and holds. New today: the descriptor citation, the full-text
checks, the optional CTPelvic1K entry, and the upstream-bibliography gaps.

`refs.bib` was only read. Corrected and added entries are in `refs_corrections.bib`, ready to paste. Each
corrected entry keeps its key and replaces the entry of the same key.

**Tex snapshot.** Citation keys were read from `main.tex` and every file it inputs, at 05:28 and again at 05:48.
No tex file changed in between; all were last modified at or before 21:07 on 2026-09-23. The six-figure wrap
agent is editing these files, so re-run the key check (bottom of this file) after it lands.

## How each entry was checked

| Check | Source |
|---|---|
| DOI registered and resolving | doi.org handle API (`responseCode` 1 = registered) |
| Bibliographic record | Crossref for publisher DOIs; Crossref book records for the two LNCS volumes' editors; DataCite for Zenodo (10.5281) and arXiv (10.48550) DOIs; Springer book pages for LNCS volume numbers |
| PubMed | E-utilities: `esearch` on `<doi>[doi]` to find the PMID, then `efetch` for authors, title, NLM abbreviation, volume, issue, pages and abstract |
| Fields compared | authors (family and given names), year, title, journal, volume, issue, pages, DOI |
| Numbers the tex takes from a paper | the abstract; where the number is not in it, the open full text. That text came from J-STAGE for Nakagawa, NCBI BioC for the PMC author manuscripts (Manbachi, Lo, De Silva), Europe PMC for Hsiang and Yun, arXiv for VERIDAH and Rao, and Springer open access for Liebrand |

**Renders.** The corrected list was rendered both ways.
- **PDF path:** the manuscript's own `nejm.bbx` and `nejm.cbx`, biblatex and biber (texlive/2020), in a scratch
  job on the grid (job 40429463, `~/refs_audit_test2`, separate from the manuscript build). All 41 keys were
  found. biber rc 0 with no warnings; pdflatex rc 0 with no errors.
- **Docx path:** pandoc 3.8 with `packet_build/nlm.csl`, which is what `make_packet.py` uses for the submitted
  docx.
- **Result:** no identifier or audit remark printed in either render, and every name, volume and page came out
  as corrected.

## Summary

| Verdict | n | Keys |
|---|---|---|
| **FIX, substantive, cited** | 6 | cobra2026, nakagawa2017, hsiang2011, vindr, he2016, rao2024 |
| **FIX, substantive, uncited now** | 3 | liebrand2026 (recommended to cite), killeen2025, deepdrr2018 |
| **FIX, style only** | 20 | strong2021, mody2008, furuya2026, dablouk2019, ammerman2006, sabri2025, desilva2016, levelcheck2012, levelcheck2016, zhang2023vdvm, totalsegmentator, csxa, buu2023, grupp2020, nhanes, ctsp1k, veridah2026, claim2024; uncited: synthex2023, polypose2025 |
| **OK** | 6 | konin2010, yun2018, manbachi2018, peh1999, huang2022, verse2021 |
| **REMOVE** | 3 | schwing2026mixed, dea2016, kanmounye2021 (all uncited) |
| **ADD** | 4 | castellvi1984 (required), ctsp1kdescriptor (recommended), figueroa2012 (when the Figure 5 paragraph lands), liu2021ctpelvic1k (optional) |

**DOIs.** 37 of 38 entries carry a DOI; schwing2026mixed has none.
- 36 of the 37 resolve, and each resolves to the paper the entry names. **No DOI points to a different paper.**
- One DOI is dead: Hsiang 2011, `10.4103/2152-7806.79769`. It is printed on the article and in PubMed, but it
  is not registered. doi.org returns 404, the handle API returns code 100, Crossref has no record, and a Crossref
  title search finds no other DOI for the article.

**Citation keys.**
- **None is missing.** No key cited in the tex is missing from `refs.bib`.
- **Thirty keys are cited.** Eight `refs.bib` entries are not cited: liebrand2026, dea2016, kanmounye2021,
  killeen2025, synthex2023, schwing2026mixed, deepdrr2018 and polypose2025. biblatex prints only cited entries,
  so these do not reach print.
- **Castellvi is named but not cited.** The classification is named on 10 lines of the tex without a citation.

## What is wrong in print today (30 cited keys)

1. **COBRA2026 has the wrong first author and title.**
   - The entry prints "Kamp F et al." The DOI's record (Zenodo, version 1.0.0) lists Thummerer A first; Kamp F is
     third.
   - The entry's title is the arXiv preprint's ("…pelvic cone-beam computed tomography projection dataset"). The
     record the DOI resolves to is titled "…pelvic CBCT projection dataset".
   - Its note prints inside the reference list: "867 patients, six European centres, … arXiv 2607.20037".
2. **Commentary prints inside the reference list.** `nejm.bbx` redefines `note+pages` for `@article` only, so the
   `note` of a misc or inproceedings entry prints.
   - Rao 2024 prints "PMID: 40039607".
   - He 2016 prints "arXiv:1512.03385 (preprint posted 10 December 2015). IEEE".
3. **VinDr-SpineXR is typed as a journal article.** It prints "MICCAI 2021" as a journal. It is a chapter in
   LNCS 12905, pp. 291–301, Springer, Cham.
4. **Hsiang 2011 prints a dead DOI** (see "DOIs" above).
5. **The descriptor sentence cites the dataset.** Methods says "The CTSpinoPelvic1K subjects were reported in
   that release's descriptor \citep{ctsp1k}", but `ctsp1k` is the Zenodo dataset. The descriptor is arXiv:2609.22760
   (posted 19 September 2026, cs.AI). DataCite shows the same 14 authors and the same title. The journal asks that
   previously reported subjects be cited with the report (`RSNA_AI_REQUIREMENTS.md`, Methods and Ethics). Fix:
   cite `ctsp1kdescriptor` there, and cite `ctsp1k` where the data are first used ("Rendered CT came from
   CTSpinoPelvic1K").
6. **Castellvi is named 10 times without a citation.** The mentions are in `methods.tex` (2), `results.tex` (2),
   `tab4_transitional.tex` (2), `tab_levelcheck.tex` (3) and the Figure 1 legend in `main.tex` (1). Fix: add
   `castellvi1984` at the first mention in Methods.
7. **Twelve cited journal names are not NLM abbreviations.** Four uncited entries have the same problem. Both
   renderers print the `journal` field as stored. Each row below gives the NLM form.
8. **Two cited entries lack the issue number.** levelcheck2012 needs issue 17 and grupp2020 needs issue 5.
   nejm.bbx prints issues, so they are visibly absent.
9. **Stored given names are wrong in Nakagawa 2017.** The entry has Takeshi, Takashi and Tsutomu; the authors are
   Tomowaki, Takumi and Takashi. The printed initials were right, so the printed reference is unaffected.

## The claims that must stay cited correctly

| Claim | Status |
|---|---|
| **Manbachi 2018** (LevelCheck clinical series) | **OK.** PMID 30051244 is Manbachi A, De Silva T, Uneri A, … Siewerdsen JH (19 authors). *Ann Biomed Eng* 2018;46(10):1548–1557. doi:10.1007/s10439-018-2099-2. Manbachi is first author and Ketcha M sixth. **It is not a Ketcha paper**, and no manuscript file attributes it to Ketcha. `LEVELCHECK_CLAIM.md` records that no first-author "Ketcha 2018" LevelCheck paper exists. Full text (PMC9107073, author manuscript, via NCBI BioC): 5 surgeons read 62 challenging cases, and the median error with LevelCheck was 2.4 %, so 97.6 %. The clinical study had 20 patients, with "no wrong-level localizations … and … nor registration errors", so 20 of 20. Every use in the tex (Introduction, Discussion, Methods, and rows H2 and H6 of Table 3, which is `tab_levelcheck.tex`, the third table `main.tex` inputs) matches. |
| **Nakagawa 2017** | **FIX** the given names. PMID 28717058; *Tohoku J Exp Med* 2017;242(3):223–228 verified. Full text (J-STAGE PDF), Table 2, with miscounts at the outpatient department in brackets: sacralised L5 type II 23 (0); type III 14 (10); lumbarised S1 types I–IV 14 (14), 9 (8), 8 (4), 3 (2). So "38 of 71" (Introduction), "10 of 48" (4 + 6 of 14 + 34; Discussion and Table 3 H1), "6 of 34" (H3), "4 of 14" (H4) and "23 of 23" (Table 3, naming-unaffected row) are all exact. The miscount was at the outpatient department, before surgery. The tex says "the count was wrong", which is accurate. |
| **Liebrand 2026** | **Not cited now; recommend citing it.** PMID 42009915; online April 20, 2026, with no volume or pages yet (Crossref and PubMed). Open access. The full text supports the manuscript's argument almost word for word: "limitations are first, the assumption of 12 thoracic vertebrae in CT image definition, second, most studies measure technical registration, not true clinical accuracy" (citing Lo 2015 and Manbachi 2018). Cite it at the Introduction's "Its published accuracies are scored against those same labels" or the matching Discussion sentence. Before citing, fix the given names (Bart, Lisa, Mark) and the journal abbreviation (`refs_corrections.bib`). |
| **Castellvi 1984** | **ADD (required).** PMID 6495013. *Spine (Phila Pa 1976)* 1984;9(5):493–495. doi:10.1097/00007632-198407000-00014. Castellvi AE, Goldstein LA, Chan DP (Crossref and PubMed agree). The abstract describes the type I–IV classification the manuscript uses. |
| **Figueroa 2012** (learning-curve sample size) | **ADD when the Figure 5 extrapolation paragraph lands.** No tex sentence names the method yet. PMID 22336388; PMCID PMC3307431. *BMC Med Inform Decis Mak* 2012;12:8. doi:10.1186/1472-6947-12-8. Figueroa RL, Zeng-Treitler Q, Kandula S, Ngo LH. The abstract is the method: an inverse power law fitted to a learning curve by nonlinear weighted least squares, then used to predict performance, with its confidence interval, at larger sample sizes. |
| **CLAIM** | **Cite CLAIM 2024** (next section). |

## CLAIM: which version to cite

**Cite the 2024 update:** Tejani AS, Klontzas ME, Gatti AA, et al; CLAIM 2024 Update Panel. Checklist for
Artificial Intelligence in Medical Imaging (CLAIM): 2024 Update. *Radiol Artif Intell* 2024;6(4):e240300.
doi:10.1148/ryai.240300. PMID 38809149; PMCID PMC11304031. Verified against Crossref and PubMed.
This is `claim2024`; only its title braces change.

**Why 2024**
- The journal requires the CLAIM 2024 update at first submission and returns the paper without it
  (`RSNA_AI_REQUIREMENTS.md`, Limits).
- The Methods already cite `claim2024` ("reporting follows CLAIM 2024").
- The Introduction's comment "CLAIM 2024 items 3 and 4" is correct under 2024 numbering.

**What has to change with it**
- **The checklist docx on disk is the 2020 form.** Both `CLAIM+-+Checklist+for+AI+in+Medical+imaging.docx` (repo
  root) and `packet/claim_checklist.docx` (built 2026-09-23 14:37) have 42 items and the 2020 wording.
- **A 2024 form is being built.** `packet_src/build/claim_checklist_2024.docx` (05:30 today) has 44 items,
  extracted by `packet_src/claim2024/extract_items.py` from the open-access copy of Tejani 2024. It must replace
  `packet/claim_checklist.docx` before submission.
- **One tex comment uses 2020 numbering.** `supplement.tex` says the flow of cases is "CLAIM item 33". That was
  item 33 in 2020. In 2024, item 33 is "Testing on external data", and the flow of cases is item 35 ("Numbers of
  patients or examinations included and excluded").

**For the record, not to cite:** Mongan J, Moy L, Kahn CE Jr. Checklist for Artificial Intelligence in Medical
Imaging (CLAIM): a guide for authors and reviewers. *Radiol Artif Intell* 2020;2(2):e200029.
doi:10.1148/ryai.2020200029. PMID 33937821.

## Other cited numbers checked against the source

**Supported, with the source text:**

| Tex claim | Key | Source |
|---|---|---|
| half of surveyed surgeons report a wrong-level operation | mody2008 | 207 of 415 respondents (50 %). The response rate was 12 % of 3,505, so "responding" is more exact than "surveyed". |
| 0.12 % in 34,544 | furuya2026 | 40 of 34,544 (0.12 %). The paper counts consecutive **patients** operated for degenerative disorders; the tex says "operations". |
| first exposure wrong in 4.3–15 % | dablouk2019, ammerman2006 | 13 of 301 (4.3 %); the intended level was first exposed in 85 %. |
| twelve-thoracic count matched L1 in 31 of 100 | yun2018 | "20th vertebra … as the first lumbar segment in 31.0 %" (reader 1, 100 patients with variants). |
| 8.8 % of 3,147 lacked 24 presacral segments | sabri2025 | 279 patients (8.8 %). |
| 100 % label placement | desilva2016 | "100 % geometric accuracy (overlaid labels within the correct vertebral level in all cases)". |
| MRI localisers without a count from C2: 77.9–82.2 % | peh1999 | 80.2 % sagittal, 82.2 % coronal, 77.9 % combined. |
| preoperative radiograph, 73.3 % | zhang2023vdvm | "matching accuracy of 0.733 on 31 C-arm X-ray images", matched to full-length DR images. |
| recalls 0.964 and 0.982, 20 in-pool images | rao2024 | Full text (arXiv 2407.08349), Table II: Spine-Vision recall 0.96429 and YOLOv5 0.98214. The 20 test images come from a 578-image pool. |
| 96.3 % → 25.9 % without anomalous training cases | veridah2026 | Full text, Table 6 (CT): 96.30 for VERIDAH against 25.93 for 4H-P-NA. See the wording note below. |
| surgeon counts the level on the X-ray | hsiang2011 | Full text: "intra-operative X-ray which allows the surgeon to count the spine level one by one". |

**Needs a fix or a check in the tex (not in refs.bib):**

1. **Registration success: Results disagree with Methods and Table 3.**
   - `results.tex` says "LevelCheck's registration success of 99.3 % is exceeded at no size", with no citation.
   - Methods and the Table 3 footnote freeze it at 1.0, citing `levelcheck2016`.
   - Lo 2015's full text (PMC4433144) gives 100 % at 200 multistarts, the setting the authors adopt for clinical
     use, and 99.3 % at 50.
   - Fix: use the frozen 1.0, or state "99.3 % at 50 multistarts" and cite `levelcheck2016`.
2. **VERIDAH wording.**
   - The metric is recall of *thoracolumbar enumeration anomalies* on CT, not "anomalous-vertebra recall". Lumbar
     enumeration-anomaly recall fell from 97.2 % to 63.9 %.
   - The ablation was trained "on zero correctly annotated TEA and LEA cases". The anomalous spines were present
     but relabelled to twelve thoracic vertebrae, so "without correctly labelled anomalous training cases" is exact.
3. **Huang 2022: two words the abstract does not support.**
   - The abstract says "Long-Film images – a novel tomographic imaging modality with an extended field-of-view"
     (50 AP and 50 lateral images of 13 cadavers, 88.3 %).
   - "Tomosynthesis" (Introduction) and "about 17 vertebrae in view" (Introduction and Discussion) are not in the
     abstract.
   - The full text is paywalled, with no open copy on Europe PMC or arXiv.
   - The "~17" traces to `docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md`, which itself cites only the abstract.
   - Fix: confirm both against the full text, or write "long-length (Long-Film) images of cadavers" and drop the
     count.
4. **"No other subject overlaps a prior publication" (Methods, ethics paragraph).** This is not literally true.
   - The CTSpinoPelvic1K Zenodo record declares itself derived from TCIA CT Colonography (ACRIN 6664),
     doi:10.7937/K9/TCIA.2015.NWTESAY1, and from CTPelvic1K: Liu P, et al. *Int J Comput Assist Radiol Surg*
     2021;16(5):749–756, PMID 33864189.
   - Every public source's subjects were also reported in the paper the Methods cite for it.
   - Suggested wording: "every subject comes from a public collection and was reported in the publication cited
     for it".
   - If CTPelvic1K is to be named, `liu2021ctpelvic1k` (optional, verified) is in the corrections. It costs a slot.
   - The cover letter's subject-overlap statement should name the same reports.

## One row per entry

In order of first citation, then the uncited entries, then the additions. "NLM" is the PubMed ISO/NLM title
abbreviation.

| # | Key | Verdict | Verified against | Finding and fix |
|---|---|---|---|---|
| 1 | hsiang2011 | **FIX** | PubMed 21660270; PMC3108446; handle API; Crossref | **DOI not registered** (see "DOIs"): omit it and give the PMC link and publication date (April 19, 2011). Journal → "Surg Neurol Int". First to drop if the cap binds; Strong 2022 carries the same sentence. |
| 2 | strong2021 | FIX (style) | Crossref; PubMed 34798613 | Journal "Journal of Neurosurgery: Spine" → "J Neurosurg Spine". Data verified: 2022;36(5):792–799, online 19 Nov 2021. |
| 3 | mody2008 | FIX (style) | Crossref; PubMed 18197106 | "Spine" → "Spine (Phila Pa 1976)". Full given names from Crossref. Data verified. |
| 4 | furuya2026 | FIX (style) | Crossref; PubMed 42061893 | "The Bone & Joint Journal" → "Bone Joint J". Data verified: 2026;108-B(5):673–680. |
| 5 | dablouk2019 | FIX (style) | Crossref; PubMed 30741019 | "British Journal of Neurosurgery" → "Br J Neurosurg". Data verified. |
| 6 | ammerman2006 | FIX (style) | Crossref; PubMed 17084188 | "Surgical Neurology" → "Surg Neurol". Data verified: 66(5):470–473; the discussion on pp. 473–474 is not part of the range. |
| 7 | konin2010 | OK | Crossref; PubMed 20203111 | All fields match. |
| 8 | yun2018 | OK | Crossref; PubMed 30386145; PMC6201970 | All fields match. |
| 9 | sabri2025 | FIX (style) | Crossref; PubMed 40450886 | Only three names were stored, then "and others". Give all 14 so that each renderer applies its own et-al rule. Data verified. |
| 10 | nakagawa2017 | **FIX** | Crossref; PubMed 28717058; full text | **Given names wrong:** Tomowaki (not Takeshi), Takumi (not Takashi), Takashi (not Tsutomu). The printed initials were right. |
| 11 | levelcheck2012 | FIX (style) | Crossref; PubMed 22864366 | Issue **17** missing. Otherwise verified. |
| 12 | levelcheck2016 | FIX (style) | Crossref; PubMed 25646750; PMC4433144 full text | "Spine" → "Spine (Phila Pa 1976)". The key says 2016, but the paper is *Spine* 2015;40(8):E476–E483, and the year field was already right. See item 1 under "Needs a fix". |
| 13 | desilva2016 | FIX (style) | Crossref; PubMed 27035579 | "Spine" → "Spine (Phila Pa 1976)". Data verified. |
| 14 | manbachi2018 | OK | Crossref; PubMed 30051244; PMC9107073 full text | All 19 authors, title, 46(10):1548–1557 and the DOI match. |
| 15 | peh1999 | OK | Crossref; PubMed 10488518 | All fields match. |
| 16 | zhang2023vdvm | FIX (style) | Crossref; PubMed 37393485 | "Journal of X-Ray Science and Technology" → "J Xray Sci Technol". Full given names added. Data verified. |
| 17 | huang2022 | OK | Crossref; PubMed 36370597 | All fields match. Check the tex wording (item 3 under "Needs a fix"). |
| 18 | ctsp1k | FIX (style) | DataCite; Zenodo | Data verified: v11 version DOI, latest (concept 10.5281/zenodo.22139642), 14 creators, issued 18 Sep 2026. Add the publication date. **It is cited where the descriptor is meant** (print item 5). |
| 19 | totalsegmentator | FIX (style) | Crossref; PubMed 37795137 | "Radiology: Artificial Intelligence" → "Radiol Artif Intell". Data verified. The paper describes the 104-structure model; it is the standard citation for the v2 and v3 data the Methods use. |
| 20 | verse2021 | OK | Crossref; PubMed 34340104 | The paper has 69 authors; the entry stores ten, then "others", which is enough for both et-al rules. Data verified. |
| 21 | csxa | FIX (style) | Crossref; PubMed 38871800 | "Scientific Data" → "Sci Data". Data verified. |
| 22 | buu2023 | FIX (style) | Crossref (not in PubMed) | "Appl Sci" → "Appl Sci (Basel)" (NLM Catalog, ISSN 2076-3417). Data verified. |
| 23 | nhanes | FIX (style) | DataCite; Zenodo | Latest version (concept 10.5281/zenodo.10145564). Add "Published November 30, 2023". The record lists the fifth creator as "Faiz, Jabbra", apparently with the names swapped and misspelt. The entry keeps "Jabbar F". |
| 24 | vindr | **FIX** | Crossref (chapter and book); Springer book page | **Wrong entry type** (print item 3). Editors: de Bruijne M, et al. Not in PubMed. |
| 25 | grupp2020 | FIX (style) | Crossref; PubMed 32333361 | Issue **5** missing. Otherwise verified. |
| 26 | cobra2026 | **FIX** | DataCite; Zenodo; arXiv 2607.20037 | **Wrong first author and title; note printed** (print item 1). Cite the Zenodo record (13 creators, 13 Jul 2026, CC BY-NC 4.0). The arXiv descriptor lists 14 authors (it adds Intven MPW and spells "Arnold" for Zenodo's "Arnhold"). The three names that print agree in both. Cite one or the other, not both. |
| 27 | veridah2026 | FIX (style) | DataCite; arXiv v1; full text | All 17 authors and the title match. howpublished → "arXiv:2601.14066 [cs.CV]". Add "Posted January 20, 2026". |
| 28 | he2016 | **FIX** | Crossref | **Note and publisher printed in the list** (print item 2). Remove both. Data verified: pp. 770–778, June 2016. |
| 29 | claim2024 | FIX (style) | Crossref; PubMed 38809149 | Data verified. The checklist's name is braced, because pandoc lowercased it in the docx. This is the version to cite. |
| 30 | rao2024 | **FIX** | Crossref; PubMed 40039607; arXiv 2407.08349 | **Note printed in the list** (print item 2). Give it as PubMed indexes it: *Annu Int Conf IEEE Eng Med Biol Soc* 2024;2024:1–6. The title uses IEEE's dash ("Spine Vision – X-Ray Image based …"), not a colon. |
| – | liebrand2026 | **FIX** (uncited; cite it) | Crossref; PubMed 42009915; open full text | **Given names wrong:** Bart (not Bas), Lisa (not Lukas), Mark (not Maarten). Journal → "Eur Spine J". Add "Published April 20, 2026". Brace the particles. |
| – | killeen2025 | **FIX** (uncited) | Crossref; PubMed 40205315 | **"Iñígo" → "Íñigo"** (Crossref and PubMed). Journal → "Int J Comput Assist Radiol Surg". |
| – | deepdrr2018 | **FIX** (uncited) | Crossref (chapter and book); Springer book page | Its note printed a description of the method in the list when it was cited (19:23 main.pdf, ref 19). LNCS **11073**, pp. 98–106, Springer, Cham; editors Frangi AF, et al. |
| – | synthex2023 | FIX (style; uncited) | Crossref; PubMed 38523605 | Issue **3** missing. |
| – | polypose2025 | FIX (style; uncited) | DataCite (five versions, v5 23 Oct 2025) | "Advances in Neural Information Processing Systems (NeurIPS) 2025" reads as a proceedings citation, and no proceedings volume or pages were checked. Cite the arXiv record. |
| – | dea2016 | **REMOVE** (uncited) | Crossref; PubMed 26456854 | Not cited. A corrected entry is kept in case it returns: "Spine J", note dropped. |
| – | kanmounye2021 | **REMOVE** (uncited) | Crossref; PubMed 34386229 | Not cited. A corrected entry is kept in case it returns: "Ann Med Surg (Lond)", note dropped. |
| – | schwing2026mixed | **REMOVE** | cannot be checked | Not cited. It has no DOI, it points to a commit in a private repository, and its URL carries the author's GitHub username, which breaks double-anonymized review if it is ever cited. The code-availability statement covers the code. |
| new | castellvi1984 | **ADD (required)** | Crossref; PubMed 6495013 | See the claims table. |
| new | ctsp1kdescriptor | **ADD (recommended)** | DataCite 10.48550/arXiv.2609.22760; arXiv page | See print item 5. It is a self-citation in the third person, which double-anonymized review allows; the names are already public in the dataset record. |
| new | figueroa2012 | **ADD (when used)** | Crossref; PubMed 22336388 | See the claims table. |
| new | liu2021ctpelvic1k | ADD (optional) | Crossref; PubMed 33864189 | See item 4 under "Needs a fix". |

## Reference count against the cap of 35

| Step | Count |
|---|---|
| Cited now | 30 |
| + castellvi1984 (required) | 31 |
| + ctsp1kdescriptor | 32 |
| + liebrand2026 | 33 |
| + figueroa2012, when the Figure 5 paragraph lands | 34 |
| + liu2021ctpelvic1k (optional) | 35, at the cap |

- **First to drop:** hsiang2011. Its DOI is dead, and Strong 2022 carries the same sentence.
- **Re-citing costs slots.** Any of killeen2025, synthex2023, deepdrr2018 or polypose2025 costs one slot each.
- **Check the count after the wrap lands:** `tools/make_refs.py` fails above 35.

## Journal style problems

1. **Only an article's note is hidden.** Identifiers therefore go in the `note` of `@article` entries (neither
   renderer prints it) or in `%` comments. They must never go in the `note` of a misc or inproceedings entry.
2. **NLM abbreviations.** 16 journal fields had full names: 12 cited and 4 uncited. Both renderers print the field
   as stored, so the abbreviation has to be in the field.
3. **The PDF and the submitted docx print references differently.** The docx is what is submitted
   (`packet/manuscript.docx`).

   | Point | PDF (`nejm.bbx`) | docx (`nlm.csl`) |
   |---|---|---|
   | Authors | up to 6, else first **3** + "et al" (`maxbibnames=6, minbibnames=3`) | first **6** + "et al" (`et-al-min=7, et-al-use-first=6`) |
   | Issue | printed: 2008;33(2):194–198 | omitted: 2008;33:194–198 |
   | Hyphenated initials | Lo SFL, Breit HC | Lo S-FL, Breit H-C |
   | Titles | as stored | sentence-cased, with a capital after a colon ("…: A systematic review") |
   | Book chapters | editors, "Vol. 12905", "Cham: Springer" | no editors, no volume, no place |
   | Published / posted dates (`addendum`) | printed | not printed |

   Pick one rule and set both to it. My reading of RSNA's published reference lists is the PDF's: up to six
   authors, else three and "et al", with the issue in parentheses. **This is not verified.** The live author
   instructions return 403 to every client tried (curl, and curl_cffi impersonating Chrome).
4. **The style example in `RSNA_AI_REQUIREMENTS.md` is garbled.** It reads "Tyler LN, Harville TO, … Elliott M.
   … N Engl J Med 2007;357:2092-2093". PubMed (PMID 18003972) gives that letter three authors: Tyler LN, Harville
   TO, Blackall DP. No Elliott M is an author, so the line is no evidence for an "all authors" rule. It also omits
   the issue (357(20)). Re-read the example from the page.
5. **Online-only items need dates.** The journal's online-article and web-content formats want "Published …" and
   "Accessed …". The corrections carry the verified publication or posting date in `addendum`. Access dates are
   left out: take them from the download logs.
6. **Regenerating refs.bib overwrites the fixes, and would currently fail.** `refs.bib` is generated by
   `tools/make_refs.py` from `paper/rsnai/refs.bib`, "entries verbatim", and the script fails on a missing key.
   - Five keys the tex cites or will cite are absent upstream: yun2018, nakagawa2017, peh1999, cobra2026 and
     figueroa2012.
   - Apply the corrections upstream and add those keys, or the next run either fails or restores the errors.
   - `sections/refs_used.bib` is a stale partial copy. No tex file or tool references it.
7. **Citations from floats.** Under endfloat with `sorting=none`, a reference cited only in a table or legend is
   numbered after all text citations. None is affected at this snapshot: every key in `tab_levelcheck.tex` is
   first cited in the text.

## Not verified

- **The RSNA et-al and issue rule** (403, see style item 3).
- **Huang 2022:** "tomosynthesis" and "about 17 vertebrae" (paywalled; see "Needs a fix", item 3).
- **Access dates** for the Zenodo datasets.
- **PolyPose:** its NeurIPS 2025 proceedings volume and pages.
- **Konin 2010:** the review was checked on metadata only. The claim it supports (counts from the sacrum and
  from C2 name different vertebrae on a transitional spine) is general.

## Re-running the key check

The key lists above came from expanding `\input` in `main.tex` and collecting `\cite…{}` keys with comments
stripped. After the six-figure wrap lands:
- Re-run the check.
- Confirm that no new key is missing from `refs.bib`.
- Confirm that the cited count plus the additions stays at 35 or fewer.
