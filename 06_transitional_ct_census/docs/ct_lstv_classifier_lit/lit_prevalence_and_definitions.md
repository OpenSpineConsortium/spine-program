# Prevalence and definitions: the outside check for a CT LSTV/TLTV census classifier

**Angle:** `prevalence_and_definitions`. **Checked 2026-09-24** against live records: PubMed E-utilities
(`esearch`, `efetch` text and XML), Europe PMC REST (`resultType=core`), PMC full texts, one publisher HTML page
(Bone & Joint), one PDF read locally (Vitale 2018). Blocked from this tool: pubmed.gov article pages (cookie wall),
SpringerLink article pages (303 to an IdP), SAGE (403), the Oulu repository PDF (403). Every claim below carries a
PMID or DOI that was opened by one of the working routes, and the number was read there. Where only the abstract
was read, the row says so.

**Cross-check against `../CITABLE_CLAIMS.md` and `../refs_additions.bib`:** neither file holds any LSTV, numbering,
rib-count, kappa or wrong-level row; nothing here is "already in CITABLE_CLAIMS". Three keys already exist in the
manuscripts' own bibs and cost no slot: `mody2008` (SchwingNet `refs.bib` line 39; CTSP `ctspinopelvic1k.bib` line
493), `castellvi1984` (`refs.bib` line 481), `konin2010` / `koninwalz2010` (review; `refs.bib` line 90). CTSP's bib
also carries `hanhivaara2022` (line 676) and `carrino2011` (line 690).

**Why the modality matters for a census.** The prevalence band is not one number. Castellvi type I is a
transverse-process height ≥ 19 mm; on CT with coronal reformats it is called far more often than on a standing pelvic
radiograph, so CT series run near 29 % and radiograph series near 16–18 %, with type I making up 68 % of CT calls and
42–45 % of radiograph calls. A census classifier that reports "LSTV" without splitting type I from II–IV cannot be
checked against either band. The stable, modality-robust quantities are (i) the type II–IV share (about 9–11 % on CT
and abdominal-MRI series, 8–10 % on radiographs) and (ii) the presacral count (25 in ~5–8 %, 23 in ~3–5 %).

---

## Decision table: what a census should land inside

| Quantity | Value | Cohort, modality | Source |
|---|---|---|---|
| LSTV any type (Castellvi I–IV) on abdominal CT | 1101/3855 = 28.6 % | consecutive abdominal CT, Finland, T12 fixed by last rib | Hanhivaara 2020 |
| … type II–IV only on CT | (171+143+33)/3855 = 347/3855 = 9.0 % | same | Hanhivaara 2020 |
| LSTV any type on standing pelvic radiograph | 841/4636 = 18.1 %; men 28.1 %, women 11.1 % | OAI cohort, 45–80 y | Nardo 2012 |
| LSTV any type on standing pelvic radiograph | 928/5860 = 15.8 % | Chinese Han volunteers 18–60 y | Tang 2014 |
| Type II–IV LSTV, sacralised vs lumbarised | 877/8280 = 10.6 %; sacralised L5 439 (5.3 %), lumbarised S1 438 (5.3 %) | lumbar MRI + cervicothoracic scout + radiograph | Paik 2013 |
| 4 / 5 / 6 lumbar-type vertebrae | 214 (2.6 %) / 7384 (89.2 %) / 682 (8.2 %) | same | Paik 2013 |
| 4 / 5 / 6 lumbar-type vertebrae, whole-spine MRI | 5.3 % / ~80 % / 14.5 %; 1 case of 3 (0.13 %) | 750 outpatients, LBP | Hanson 2010 |
| 23 / 24 / 25 / 26 presacral segments | 104 (3.3 %) / 2868 (91.1 %) / 174 (5.5 %) / 1 (0.03 %) | 3147 full-length standing radiographs | Sabri 2025 |
| 11 / 12 / 13 rib pairs | 143 (4.5 %) / 2976 (94.6 %) / 28 (0.88 %) | same | Sabri 2025 |
| 11 / 12 / 13 rib pairs, whole-spine CT | 107 (8.0 %) / 1228 (91.6 %) / 5 (0.4 %) | 1340 consecutive whole-spine CT, Korea | Doo 2020 |
| Sacralisation / lumbarisation, whole-spine CT (count-based) | 68 (5.1 %) / 43 (3.2 %); TLTV 150 (11.2 %) | same | Doo 2020 |
| Sacralisation / lumbarisation, whole-spine CT | 12.3 % / 4.0 % of 551; 12th hypoplastic rib 12.6 %, lumbar rib 1.5 % | Japan, 407 F / 144 M | Nagata 2025 (abstract only) |
| Lumbar rib, pooled | 2.1 % (95 % CI 1.0–4.6); CT-only 1.6 % (0.6–4.3) | meta-analysis, 9 studies | Osiowski 2024 |
| Castellvi inter-rater κ on CT | 0.855 (intra 0.928) | 3855 CT | Hanhivaara 2020 |
| Castellvi inter-reader κ: CT / MRI / CR | 0.63–0.71 / 0.24–0.56 / 0.16–0.32; CT sens 76 %, spec 93 % | 100 LSTV patients, all three modalities | Hanhivaara 2024 (abstract only) |
| Castellvi κ within AP radiograph and within coronal CT; radiograph-vs-CT | X-ray 0.893, 0.880; CT 0.921, 0.874; X-ray vs CT κ 0.502/0.493, 35.2 % of types changed | 91 type II–IV cases | Hou 2020 |
| Wrong-level surgery among LSTV surgical patients | 12/885 = 1.4 % | systematic review, 39 studies | Albano 2024 |
| Wrong-level treatment determination in LSTV | 36/214 = 16.8 %; ambiguous 106/214 | 4184 radiculopathy patients, LSTV 5.1 % | Liebrand 2025 |
| Surgeons who have operated at a wrong level | 207/415 = 50 %; 1 in 3110 procedures; 71 % lumbar | AANS survey | Mody 2008 (already cited) |
| Radiologist reports naming a count variant | 11/657 = 1.7 % of reports vs 70/657 = 10.6 % true | AIS radiographs | Hu 2016 |
| Consensus guideline on counting | C2 as the counting standard (100 %); aberrant anatomy discussed at a preoperative conference (100 %); standardised naming/counting (82 %) | 16 deformity surgeons, Delphi | Vitale 2018 |

---

## Sources opened, in the order opened

### (a) LSTV prevalence, with definitions

**Hanhivaara J, Määttä JH, Niinimäki J, Nevalainen MT.** Lumbosacral transitional vertebrae are associated with lumbar
degeneration: retrospective evaluation of 3855 consecutive abdominal CT scans. *Eur Radiol* 2020;30(6):3409–3416.
PMID 32072261, PMC7248049, doi:10.1007/s00330-020-06691-2. **Route:** PMC full text. **Read there:** 3855 consecutive
abdominal CT scans from 2017; "LSTV was found in 1101 (29%) scans" (28.6 %); type I 754 (68.4 % of LSTV), II 171
(15.5 %), III 143 (13.0 %), IV 33 (3.0 %); "Males and females had type I LSTV in 77% and 54% of all cases; type II
11% and 24%; type III 10% and 18%; and type IV 3% and 4%, respectively"; definition quoted in full ("enlarged
transverse processes measuring at least 19 mm craniocaudally" for type I; pseudoarticulation II; osseous fusion III;
II one side + III other = IV); "The last ribs were used to define the Th12 vertebra"; "both the intra-rater and
inter-rater agreements were excellent (κ = 0.928 and 0.855, respectively)". **Standing:** VERIFIED, full text.
**Caveat for the census:** numbering was from the last rib, not from C2, so a 13th-rib or 11-rib spine would be
misnumbered here; the type distribution is unaffected by that, the sacralised/lumbarised split is.

**Nardo L, Alizai H, Virayavanich W, et al.** Lumbosacral transitional vertebrae: association with low back pain.
*Radiology* 2012;265(2):497–503. PMID 22952380, doi:10.1148/radiol.12112747. **Route:** efetch text and XML.
**Read there:** "Standard standing pelvic radiographs that included the transverse processes of L5 were graded … in
4636 participants (1992 men and 2804 women; aged 45-80 years)"; "Prevalence of LSTV was 18.1% (841 of 4636)";
"higher rate in men than in women (28.1% vs 11.1%, respectively; P<.001)"; type I 41.72 %, II 41.4 %, III 11.5 %,
IV 5.2 % of LSTV. **Standing:** VERIFIED, abstract (numbers are all in the abstract). Radiograph, not CT.

**Tang M, Yang XF, Yang SW, et al.** Lumbosacral transitional vertebra in a population-based study of 5860
individuals: prevalence and relationship to low back pain. *Eur J Radiol* 2014;83(9):1679–1682. PMID 24935139,
doi:10.1016/j.ejrad.2014.05.036. **Route:** efetch text and XML. **Read there:** "Typical standing pelvic
radiographs were obtained for 5860 volunteers between 18 to 60 years of age"; "LSTV was found in 15.8% (928 of 5860)";
type I 44.8 %, II 43.2 %, III 7.2 %, IV 4.8 % of LSTV. No sex split in the abstract. **Standing:** VERIFIED, abstract.
Radiograph, not CT; the task text's "CT" attribution to Tang is wrong.

**Apazidis A, Ricart PA, Diefenbach CM, Spivak JM.** The prevalence of transitional vertebrae in the lumbar spine.
*Spine J* 2011;11(9):858–862. PMID 21951610, doi:10.1016/j.spinee.2011.08.005. **Route:** efetch. **Read there:**
211 adequate abdominal (KUB) radiographs of 1100; LSTV 75/211 = 35.6 %, type IA 14.7 % most common; 197 (93.4 %)
five lumbar, 14 (6.6 %) six lumbar. **Standing:** VERIFIED, abstract. Small, radiograph, upper end of the band.

**Sugiura K, Morimoto M, Higashino K, et al.** Transitional vertebrae and numerical variants of the spine:
prevalence and relationship to low back pain or degenerative spondylolisthesis. *Bone Joint J*
2021;103-B(7):1301–1308. PMID 34192932, doi:10.1302/0301-620X.103B7.BJJ-2020-1760.R1. **Route:** Europe PMC core
+ publisher HTML (boneandjoint.org.uk, opened). **Read there:** 1179 patients (691 M, 488 F) with thoracic,
abdominal and pelvic CT; normal 12 T + 5 L without TLTV/LSTV in 900 (76.3 %); TLTV 15.8 % M / 16.0 % F; LSTV 7.1 % M /
9.0 % F; "16 presacral mobile vertebrae without LSTV" 1.0 % M / 4.1 % F and 18 without LSTV 5.3 % M / 1.2 % F (their
"16/17/18" count the thoracolumbar segments, i.e. 23/24/25 presacral). Counting method and definitions were not in
the accessible text. **Standing:** PARTLY (numbers verified; definitions not read).

**Yoon ES, Pishgar F, Chhabra A, Del Grande F, Carrino JA.** Frequency of coexistent spinal segment variants:
retrospective analysis in asymptomatic young adults. *AJNR* 2023;45(1):119–126. PMID 38123916, PMC10756567,
doi:10.3174/ajnr.A8071. **Route:** Europe PMC core. **Read there:** 450 asymptomatic young adults; distribution
variants 23.8 %, cervical rib 4.2 %, TLTV 15.3 %, LSTV 26.4 %; TLTV↔LSTV OR 1.87 (1.08–3.20). Modality not in the
abstract summary returned. **Standing:** PARTLY (abstract; modality unread).

**Fidan F, Çay N, Asiltürk M, Veizi E.** *J Orthop Sci* 2022;27(6):1167–1171. PMID 34391615. **Route:** efetch.
3132 asymptomatic young Turkish men; LSTV 12.9 %; spina bifida occulta 16.2 %. Modality not read. Not used.

**Chiu CK, et al.** *Spine* 2024;49(1):64–70. PMID 37146062. **Route:** efetch. 998 AIS radiographs; 23 or 25
vertebrae 9.8 %; LSTV 25.1 %. Scoliosis cohort; not used for the band.

**Wu B, et al.** *Eur Spine J* 2026;35(4):2219–2225. PMID 41196384. **Route:** efetch. 909 patients, LSTV 105
(11.6 %): lumbarisation 76 (8.4 %), sacralisation 29 (3.2 %) — the reverse ratio to every other series, in a
case-control design; not used.

**Jagannathan D, et al.** *Asian Spine J* 2017;11(3):365–379. PMID 28670404. **Route:** efetch. Lumbar MRI; 81.4 %
normal, sacralisation 14.7 %, lumbarisation 3.8 %; "none [of the landmarks] were 100 % accurate". Not used.

Reviews seen and not cited for numbers: Konin & Walz 2010 AJNR (`konin2010`, already in refs.bib); PMC12549404
(2025 systematic review and narrative analysis, quoted by search as 4290/28106 = 15.3 %, range 4.5–35.6 %; pooled
across modalities, so not a check); PMC12969546 (Pain Pract 2026 review); PMC13584665 (LSTV and spondylolisthesis
meta-analysis); Liebrand 2026 *Eur Spine J* systematic review PMID 42009915 (29 studies; "no 100 % was achieved" in
the transitional-vertebra investigations — a statement, no census number); Shah 2020 Cureus Part II/III PMIDs
32699684, 32864257 (narrative).

### (b) Presacral count: 25 (L6 / lumbarised S1) and 23 (sacralised L5 / four lumbar)

**Paik NC, Lim CS, Jang HS.** Numeric and morphological verification of lumbosacral segments in 8280 consecutive
patients. *Spine* 2013;38(10):E573–E578. PMID 23392421, doi:10.1097/BRS.0b013e31828b7195. **Route:** efetch.
**Read there:** 8280 consecutive lumbar-MRI patients with cervicothoracic scanning and radiography; 4 lumbar 214
(2.6 %), 5 lumbar 7384 (89.2 %), 6 lumbar 682 (8.2 %); type II–IV LSTV 877 (10.6 %): sacralised L5 439 (5.3 %),
lumbarised S1 438 (5.3 %); commonest variants L5 with unilateral type II (222, 2.7 %) and L6 with bilateral type III
(174, 2.1 %); modal anatomy (five lumbar, no LSTV) 6945 (83.9 %). **Standing:** VERIFIED, abstract. The largest
counted series; MRI-based counting with a whole-spine scout.

**Hanson EH, Mishra RK, Chang DS, et al.** Sagittal whole-spine magnetic resonance imaging in 750 consecutive
outpatients: accurate determination of the number of lumbar vertebral bodies. *J Neurosurg Spine* 2010;12(1):47–55.
PMID 20043764, doi:10.3171/2009.7.SPINE09326. **Route:** efetch. **Read there:** 750 of 762 outpatients; six lumbar
14.5 %, four lumbar 5.3 %, three lumbar 1 (0.13 %); "one in five" lacked five lumbar-type vertebrae; six-lumbar
two-thirds male, four-lumbar two-thirds female. **Standing:** VERIFIED, abstract. MRI, LBP outpatients; the
lumbar-type count here is morphologic (lumbar-type bodies), not a presacral count, which is why 14.5 % exceeds every
presacral-count series.

**Sabri SA, Laynes RA, Hoffman CJ, et al.** Implications of lumbosacral transitional anatomy on vertebral numbering:
evaluation of 3147 adult full-length spine radiographs. *Neurosurg Focus* 2025;58(6):E13. PMID 40450886,
doi:10.3171/2025.3.FOCUS2555. **Route:** Europe PMC core. **Read there:** 3147 patients 18–89 y; 24 presacral mobile
segments 2868 (91.1 %); 25 in 174 (5.5 %), 23 in 104 (3.3 %), 26 in 1 (0.03 %); 12 ribs 2976 (94.6 %), 11 ribs 143
(4.5 %), 13 ribs 28 (0.88 %); LSTV + abnormal rib count together 56 (1.8 %); authors designate the first non-ribbed
vertebra L1. **Standing:** VERIFIED, abstract. Radiograph; the only large series giving all three presacral counts
and all three rib counts in one cohort.

**Tins BJ, Balain B.** Incidence of numerical variants and transitional lumbosacral vertebrae on whole-spine MRI.
*Insights Imaging* 2016;7(2):199–203. PMID 26873359, doi:10.1007/s13244-016-0468-7. **Route:** efetch. **Read
there:** 418 evaluable of 420 prospective whole-spine MRI; transitional vertebrae 14 (3.3 %): 8 sacralised L5, 4
lumbarised S1 (sic, 12 listed of 14); numerical variants 32 (7.7 %): increased 18 (12 M, 6 F), decreased 14 (4 M,
10 F); "numerical variants … almost 2.5 times as frequent as transitional lumbosacral vertebrae". **Standing:**
VERIFIED, abstract. Note that this series defines "transitional" narrowly and separately from count, which is why its
LSTV figure is an order below the others; a census must state which definition it uses.

**Carrino JA, Campbell PD, Lin DC, et al.** Effect of spinal segment variants on numbering vertebral levels at lumbar
MR imaging. *Radiology* 2011;259(1):196–202. PMID 21436097, doi:10.1148/radiol.11081511 (`carrino2011` in the CTSP
bib). **Route:** efetch. **Read there:** 147 subjects, spinal radiography as reference; anomalous total count 12
(8.2 %); TLTV 6 (4.1 %), LSTV 22 (15.0 %), both 4 (2.7 %); LSTV↔anomalous numbering OR 7.4, P < .001; iliolumbar
ligament at L5 in 122/126 (96.8 %). **Standing:** VERIFIED, abstract. Small; the OR is the useful number.

**Yun S, Park S, Park JG, et al.** Spinal enumeration by morphologic analysis of spinal variants: comparison to
counting in a cranial-to-caudal manner. *Korean J Radiol* 2018;19(6):1140–1146. PMID 30386145, PMC6201970,
doi:10.3348/kjr.2018.19.6.1140. **Route:** publisher HTML (kjronline). **Read there:** 100 CT patients selected for
having a variant ("All patients showed anomalous distribution"); 22 presacral 1, 23 in 9, 25 in 19; TLTV 85 %, LSTV
13 %, both 9 %; morphologic L1 = 21st segment in 65 %, 20th in 31 %, 19th in 4 %; κ = 1.00 between two readers for
morphologic L1. **Standing:** VERIFIED, but a selected sample: no prevalence. Useful as the statement that
cranial-to-caudal counting under a 12-thoracic assumption mislabels L1 in 35 % of variant spines.

**Tatara Y, Niimura T, Sekiya T, Mihara H.** *JB JS Open Access* 2021;6(3):e20.00167. PMID 34278183, PMC8280013.
**Route:** Europe PMC core. 880 patients; LSTV 111 (12.6 %); TLTV present in 87/111 (78.4 %) of LSTV, at T13 in 59/87
(67.8 %). Modality not read. **Standing:** PARTLY. Not used in the seven.

### (c) Rib-count variants: 13 pairs / lumbar ribs / 11 pairs

**Doo AR, Lee J, Yeo GE, et al.** The prevalence and clinical significance of transitional vertebrae: a radiologic
investigation using whole spine spiral three-dimensional computed tomographic images. *Anesth Pain Med (Seoul)*
2020;15(1):103–110. PMID 33329798, PMC7713870, doi:10.17085/apm.2020.15.1.103. **Route:** PMC full text. **Read
there:** 1553 consecutive adults 18–80 y with whole-spine spiral 3-D CT for trauma or disease in 2018, 1340 analysed
(857 M, 483 F); counted "craniocaudally, starting from C1, based on the assumption of 7 cervical, 12 thoracic, and 5
lumbar vertebrae", 20th = L1, 25th = S1; sacralisation = "anomalous fusion of L5 (24th vertebra) and S1",
lumbarisation = "non-fusion of S1 and S2 (26th vertebra)" — i.e. count-based, not Castellvi; 12 ribs 1228 (91.6 %),
11 ribs 107 (8.0 %), 13 ribs 5 (0.4 %); TLTV 150 (11.2 %); LSTV 111 (8.3 %) = sacralisation 68 (5.1 %) +
lumbarisation 43 (3.2 %); TLTV↔abnormal rib count OR 117.26 (60.77–226.27); TLTV↔LSTV OR 7.38 (3.99–13.63); two
readers, 95.3 % agreement on TLTV. **Standing:** VERIFIED, full text. The one whole-spine CT series with every
quantity the census needs, counted from C1. Note the 11-rib share (8.0 %) is high against Sabri's 4.5 %; the CT
reader can see a hypoplastic 12th rib a radiograph cannot, and the two series will define "11 ribs" differently.

**Nagata S, Yamada C, Sawano M, et al.** Lumbosacral transitional vertebra on whole-spine CT: prevalence and
association with rib abnormalities. *Skeletal Radiol* 2025;54(10):2169–2177. PMID 40381031,
doi:10.1007/s00256-025-04952-z. **Route:** efetch + Europe PMC core (abstract); SpringerLink page redirected to an
IdP and was not read; pubmed.gov page is cookie-walled. **Read there:** 551 patients (407 F, 144 M); LSTV 16.3 % =
sacralisation 12.3 % + lumbarisation 4.0 %; rib abnormality 14.0 % = twelfth hypoplastic rib 12.6 % + lumbar rib
1.5 %; "all twelfth hypoplastic ribs were found in the sacralization group and all lumbar ribs were found in the
lumbarization group (p < 0.001)"; lumbarisation more frequent in males (p = 0.031). How LSTV was defined and how the
spine was counted are not in the abstract. **Standing:** PARTLY (abstract only; definitions unread). The 100 %
co-segregation of rib type with LSTV direction is the strongest published support for using the rib count as the
independent partner route in the fusion.

**Osiowski M, Osiowski A, Preinl M, et al.** Prevalence and characteristics of lumbar ribs: a meta-analysis with
anatomical and clinical considerations. *Surg Radiol Anat* 2024;46(12):2057–2066. PMID 39377983, PMC11579145,
doi:10.1007/s00276-024-03504-9. **Route:** efetch + Europe PMC core. **Read there:** 9 studies; pooled lumbar-rib
prevalence 2.1 % (95 % CI 1.0–4.6); CT 1.6 % (0.6–4.3); X-ray 2.1 % (0.4–11.1); bilateral in 65.4 % (39.4–84.6).
**Standing:** VERIFIED, abstract. A meta-analysis is cited here for its own pooled number, not for a primary's.

**Sabri 2025** (above): 13 ribs 0.88 %, 11 ribs 4.5 % on 3147 radiographs.

**Abul K, et al.** *Spine Deform* 2023;11(1):105–114. PMID 35921040. **Route:** efetch. 187 AIS; sacralised L5 22 %,
11 rib pairs 7 %. Scoliosis; not used.

**Garg B, et al.** *Int J Spine Surg* 2021;15(2):359–367. PMID 33900995. **Route:** efetch. 198 AIS; 40 (20.2 %)
abnormally numbered; radiology reports identified 2/40, operation notes 4/40. Under-reporting; scoliosis.

**Hu Z, et al.** *Medicine (Baltimore)* 2016;95(34):e4682. PMID 27559975, doi:10.1097/MD.0000000000004682.
**Route:** efetch. 657 AIS; 70 (10.6 %) with a count variant; "a variation in the number of vertebrae had been
identified in 1.7% (11) of the reports by the radiologist"; 248 normal adolescents 10.9 %. **Standing:** VERIFIED,
abstract. Used in claim 7 as the under-reporting number.

Dead ends in the rib search: PMID 29761492 (Pug dogs, *J Anat*), 30113323 (DISH on whole-spine CT), 28816877
(ankylosing fractures) — returned by the presacral/whole-spine esearch, irrelevant.

### (d) Inter-reader agreement for Castellvi grading

**Hanhivaara J, Määttä JH, Kinnunen P, Niinimäki J, Nevalainen MT.** Castellvi classification of lumbosacral
transitional vertebrae: comparison between conventional radiography, CT, and MRI. *Acta Radiol*
2024;65(12):1515–1520. PMID 39444351, doi:10.1177/02841851241289355. **Route:** efetch (abstract). SAGE page 403;
the Oulu dissertation PDF that reprints it 403. **Read there:** 100 patients with LSTV imaged with all three
modalities; CT sensitivity/specificity/accuracy/balanced accuracy 76 % / 93 % / 77 % / 84 %; MRI 54 / 88 / 56 / 68;
CR 32 / 85 / 42 / 59; inter-reader κ CT 0.63–0.71, MRI 0.24–0.56, CR 0.16–0.32. **What was not read:** the reference
standard against which "sensitivity" is computed (most likely a consensus CT read; unconfirmed). **Standing:**
PARTLY (numbers verified in the abstract; reference standard unread).

**Hou L, Bai X, Li H, et al.** Lumbar plain radiograph is not reliable to identify lumbosacral transitional vertebra
types according to Castellvi classification principle. *BMC Musculoskelet Disord* 2020;21(1):333. PMID 32471475,
PMC7260820, doi:10.1186/s12891-020-03358-3. **Route:** PMC full text. **Read there:** 298/2026 (14.7 %) suspected
type II–IV on AP lumbar radiograph, 91 with coronal CT reformats; two readers, two readings each; κ X-ray 0.893
(0.855–0.931) and 0.880 (0.840–0.920); κ CT 0.921 (0.887–0.955) and 0.874 (0.832–0.916); radiograph-vs-CT type
agreement κ 0.502 / 0.493; "35.2% of the suspected MA-LSTV types judged by AP-LPR were not consistent with the final
types judged by CT-CRIs"; 39 IIa, 17 IIb, 2 IIIa, 20 IIIb, 13 IV. **Standing:** VERIFIED, full text. Note the
contrast with Hanhivaara 2024: readers agree with each other on a radiograph (κ 0.89) while being wrong against CT
(κ 0.50) — inter-reader κ on one modality is not accuracy.

**Hanhivaara 2020** (above): CT inter-rater κ 0.855, intra 0.928.

**Farshad-Amacker NA, Aichmair A, Herzog RJ, Farshad M.** *Eur Spine J* 2015;24(3):600–608. PMID 25223429.
**Route:** efetch. 71 LSTV + 62 controls on MRI; iliac-crest tangent sign sensitivity 81 %, specificity 64–88 %,
inter-reader κ 0.75; "anatomical landmarks are not always reliable". Not used in the seven.

**Doo 2020** (above): 95.3 % raw agreement on TLTV, two readers, no κ. **Yun 2018**: κ 1.00 for morphologic L1 on
100 selected CTs.

### (e) Clinical harm and guideline statements

**Mody MG, Nourbakhsh A, Stahl DL, et al.** The prevalence of wrong level surgery among spine surgeons. *Spine*
2008;33(2):194–198. PMID 18197106, doi:10.1097/BRS.0b013e31816043d1. **Already cited** as `mody2008` in
SchwingNet `refs.bib` and the CTSP bib. **Route:** efetch. **Read there:** 3505 AANS members surveyed, 415 (12 %)
responded; 64 (15 %) prepared the wrong level and caught it before incision; 207 (50 %) had performed ≥ 1 wrong-level
surgery; 418 wrong-level operations in an estimated 1,300,000 procedures = 1 in 3110; lumbar 71 %, cervical 21 %,
thoracic 8 %; 73 (17 %) led to legal action. LSTV is not itemised as a cause in the abstract. **Standing:** VERIFIED,
abstract.

**Albano S, Brown NJ, Pennington Z, et al.** Risks associated with surgical management of lumbosacral transitional
vertebrae: systematic review of surgical considerations and illustrative case. *World Neurosurg* 2024;186:e54–e64.
PMID 38350597, doi:10.1016/j.wneu.2024.02.033. **Route:** efetch + Europe PMC core. **Read there:** PRISMA review,
39 studies, 885 LSTV patients operated (disc herniation 37 %, Bertolotti 35 %, stenosis 25 %); "Wrong level surgery
occurred in 1.4% (n = 12) of patients"; reherniation 12 (5.5 %). **Standing:** VERIFIED, abstract. This is a
systematic review's pooled count, cited as such; the 12 cases are spread across its 39 primaries and the review does
not name which. Against Mody's 1/3110 in the general run of procedures, 1.4 % in LSTV patients is ~40-fold.

**Liebrand B, van der Wal S, Slob M, et al.** Diagnostic precision in lumbar radiculopathy: impact of transitional
vertebrae on treatment level selection and outcomes. *Pain Med* 2025;26(10):681–688. PMID 40408166,
doi:10.1093/pm/pnaf061. **Route:** efetch. **Read there:** 4184 patients assessed, LSTV 214 (5.1 %); level
determination correct 72, wrong 36 (16.8 %), ambiguous 106; "Discrepancies between reported MRI- and treatment
levels in the records increased the chance for wrong level treatment (P < .001)". **Standing:** VERIFIED, abstract.
Interventional pain, not open surgery.

**Liebrand B, Brakel K, Boon A, et al.** *Reg Anesth Pain Med* 2022;47(3):177–182. PMID 34921051. **Route:**
efetch. 143 patients with anomalous numbering, 114 analysed; level in file/referral/treatment differed in 40 %;
MRI-report vs treatment level differed in 46 %. **Standing:** VERIFIED, abstract. Same group, earlier cohort.

**Vitale M, Minkara A, Matsumoto H, et al.** Building consensus: development of best practice guidelines on wrong
level surgery in spinal deformity. *Spine Deform* 2018;6(2):121–129. PMID 29413733, doi:10.1016/j.jspd.2017.08.005.
**Route:** Europe PMC core (abstract) + the author-posted PDF (pediatricscoliosissurgery.com), text extracted with
pypdf and read. **Read there:** 16 fellowship-trained spine surgeons, Delphi + nominal group, 24,200 combined
procedures, ≥ 80 % = consensus; 15/16 had no standardised counting method at their institution; cited preoperative
errors include "lack of attention to potential anatomical variants on preoperative images"; consensus items (Table
4): "A standardized technique of vertebral naming and counting should be adopted for all pre- and intraoperative
radiographs" (82 %); SDSG method as the standard (81 %); "The Axis (C2) should be used as a standard for cervical
level counting" (100 %); "A preoperative conference … is the optimal time to discuss aberrant anatomy and vertebral
level selection" (100 %); "In the situation of any ambiguity, another surgeon or radiologist should be consulted"
(88 %). **The words "transitional vertebra", "rib count" and "whole-spine imaging" do not appear as items.**
Non-consensus items include pre-incision radiographs (63 %) and X-ray as intraoperative gold standard (56 %
disagree). **Standing:** VERIFIED, full text. This is a deformity-society consensus, not a NASS/AAOS guideline.

**Not found:** any NASS, AAOS, Joint Commission or radiology-society guideline that names LSTV or whole-spine
counting as a required preoperative step. The Universal Protocol and NASS SMaX are cited by reviews (George 2023
*Br J Neurosurg* PMID 36541119: "up to half" of SBNS surgeons, 40 % of NHSE wrong-site reports at L4/5; Robertson
2024 chapter PMID 38700681; PMC8247699 Epstein perspective; NBK617525) but none of those reviews quotes a guideline
sentence about LSTV, and no primary guideline document was reached. Treat "guideline statements on preoperative LSTV
flagging" as **absent from the literature reachable today**; Vitale 2018 is the nearest, and Konin & Walz 2010
(already cited) is the radiology-review statement that "most wrong-level spine surgery occurs in patients with
variant spine anatomy" (that sentence was seen only in search snippets attributed to the review; not re-read here).

**Longo UG, Loppini M, Romeo G, Maffulli N, Denaro V.** Errors of level in spinal surgery: an evidence-based
systematic review. *J Bone Joint Surg Br* 2012;94(11):1546–1550. PMID 23109637. **Route:** efetch. 12 studies;
lumbar > cervical; "the current literature does not provide a definitive estimate"; one study found protocols failed
to prevent about one-third of cases. No LSTV-attributable fraction. Not used.

**Ammerman JM, et al.** *Surg Neurol* 2006;66(5):470–473. PMID 17084188. **Route:** efetch. 100 consecutive lumbar
discectomies, intended level exposed first in 85 %; four patients had transitional vertebrae. Not used.

**Etheridge JB, et al.** *Reg Anesth Pain Med* 2020;45(3):176–179. PMID 31653796. 3 of 5 block failures in
transitional anatomy (n = 100). Not used. **Malanga 2004** case report PMID 16868621. Not used. **Kwak D, Ro DH,
Kang DH.** *J Clin Med* 2025;14(21):7671, PMID 41227066: radiograph deep-learning LSTV detector, accuracy 76.4 %,
sensitivity 85.1 %, specificity 61.9 % (already known to the project as the only published 2-D LSTV model).

---

## What is not known, and what to say plainly

- No published CT-based LSTV prevalence series counts from C2 **and** grades Castellvi **and** reports κ in one
  cohort. Hanhivaara 2020 grades and reports κ but numbers from the last rib; Doo 2020 counts from C1 but defines
  LSTV by fusion, not by Castellvi; Nagata 2025's definitions were not readable.
- The Hanhivaara 2024 reference standard for its sensitivity figures was not read.
- Prevalence by sex is available on radiographs (Nardo: men 28.1 %, women 11.1 %) and in the direction of count
  variants (Hanson, Tins, Sugiura: 25 presacral / six lumbar skews male; 23 / four lumbar skews female), but not for
  CT Castellvi grades overall.
- No guideline names LSTV flagging.

## Bands to hold the census to (derived from the rows above; not themselves citable)

- CT, Castellvi I–IV: ~29 % (one series). Radiograph: 16–18 % (two population series). If the classifier splits type
  I from II–IV, check II–IV against 9.0 % (Hanhivaara CT), 10.6 % (Paik), ~7–9 % (Sugiura CT).
- Sacralised : lumbarised ≈ 1 : 1 by Castellvi II–IV (Paik 439 : 438) but ≈ 1.6–3 : 1 by count-based fusion on
  whole-spine CT (Doo 68 : 43; Nagata 12.3 : 4.0). The ratio depends on the definition; state which one is used.
- 25 presacral: 5.5 % (Sabri), 8.2 % six lumbar (Paik), 5.3 % M / 1.2 % F (Sugiura). 23 presacral: 3.3 % (Sabri),
  2.6 % (Paik), 1.0 % M / 4.1 % F (Sugiura).
- 13 rib pairs: 0.4 % (Doo CT), 0.88 % (Sabri radiograph). Lumbar rib: 1.5 % (Nagata CT), 1.6 % CT pooled
  (Osiowski). 11 rib pairs: 4.5 % (radiograph) to 8.0 % (CT).
- A CT census that returns type-II–IV LSTV at 0.5 % or 40 %, a 13-rib share above ~2 %, or a lumbarised share
  exceeding the sacralised share, has a broken feature, not a finding.
