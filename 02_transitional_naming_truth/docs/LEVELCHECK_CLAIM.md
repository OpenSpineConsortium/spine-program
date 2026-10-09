# The LevelCheck claim: what the literature supports, what it does not, and the power we actually have

Written 2026-09-23 for gate G6 (`docs/FLAGSHIP_PLAN.md`). Every citation below was verified against PubMed
this day; where a sentence Greg wants is not in the record, this file says so instead of rounding toward it.

---

## 1. The LevelCheck literature

LevelCheck is 3-D/2-D intensity-based registration of the preoperative CT to the intraoperative radiograph.
The vertebral labels it displays are annotations on the preoperative CT, projected through the solved pose.
**Every published accuracy number is registration accuracy: whether the projected label lands on the correct
vertebra as that vertebra is named in the CT annotation. The name itself is imported, never inferred.**

| paper | design | n | headline number | PMID / DOI |
|---|---|---|---|---|
| Otake 2012, Phys Med Biol 57(17):5485-508 | simulation from patient CTs | 10 CTs, 50,000 simulated fluoro images | 99.998 % success (1 failure in 50,000); 4.7 s on GPU | 22864366 / 10.1088/0031-9155/57/17/5485 |
| Lo 2015, Spine 40(8):E476-83 | retrospective clinical, thoracolumbar | 20 patients, 10,000 registration trials | 100 % labeling accuracy at 200 multistarts (~26 s); 99.3 % at 50 multistarts (~7 s) | 25646750 / 10.1097/BRS.0000000000000814 |
| De Silva 2016, Spine 41(20):E1249-E1256 | retrospective utility, 3 spine surgeons | 398 intraoperative radiographs, 178 CTs | 100 % geometric accuracy; judged *helpful* in 42.2 % (168/398), confidence up in 30.6 %, diminished performance in 0 | 27035579 / 10.1097/BRS.0000000000001589 |
| Ketcha 2017, Phys Med Biol 62(11):4604-4622 | multi-stage 3-D/2-D registration under anatomical deformation | (method paper) | maps CT point labels onto radiographs despite non-rigid deformation between preop and intraop positioning | 28375139 / 10.1088/1361-6560/aa6b3e |
| Ketcha 2017, IEEE Trans Med Imaging 36(10) | Cramer-Rao limits of registration accuracy vs image quality (noise, resolution, dose) | (theory) | registration accuracy bounded by image-quality factors | 28708549 / 10.1109/TMI.2017.2725644 |
| Manbachi 2018, Ann Biomed Eng 46(10):1548-1557 | the clinical series: reader study + operating room | Study 1: 5 surgeons x 62 challenging cases. Study 2: 20 patients in the OR | Study 1: median localization error 30.4 % unassisted, 2.4 % with LevelCheck (p < 0.01), confidence up in 91 %. Study 2: accurate in all 20 cases; runtime 17-72 s | 30051244 / 10.1007/s10439-018-2099-2 |

**A note on the reference list Greg dictated:** there is no first-author "Ketcha 2018" LevelCheck paper on
PubMed. Ketcha's 2018 publications with the Siewerdsen group are ultrasound slice-to-volume, MR-CT demons,
CBCT calibration and virtual fluoroscopy. The 2018 entry in this program is the clinical translation paper,
first author Manbachi. Cite it as Manbachi 2018.

**Transitional anatomy in the LevelCheck record:** none of the four abstracts above mentions transitional
vertebrae, LSTV, numbering variants or labelling conventions. The closest sentence in the record is De Silva
2016 listing "anatomical variations/abnormalities" among the clinical contexts where LevelCheck is *most
likely to be beneficial* — i.e., the published position is that variation is where the tool helps, not where
it fails. The convention problem (whose count does the CT annotation carry?) is simply not addressed in
this literature. That silence is our opening, and it must be stated as silence, not as a reported failure.

**What LevelCheck needs:** a preoperative CT with vertebral labels annotated on it; an intraoperative
radiograph; no tracker, no fiducials (Otake 2012's design goal). Runtime 17-72 s in the OR as deployed
(Manbachi 2018). It is research software from the Johns Hopkins I-STAR laboratory used under research
agreements; I found no FDA clearance and no commercial release in the record. Do not write "DUA-only" in
the manuscript without a citable source for the licensing status — I could not find one.

---

## 2. The wrong-level literature, and the LSTV numbers

### Wrong-level events

| paper | design | number | PMID / DOI |
|---|---|---|---|
| Mody 2008, Spine 33(2):194-8 | anonymous survey, 3,505 AANS members, 415 (12 %) responding | 50 % of surgeons (207/415) had performed >= 1 wrong-level surgery in their career; 15 % (64) prepared the wrong level but caught it before incision; 418 wrong-level operations in an estimated 1,300,000 procedures = **1 in 3,110** | 18197106 / 10.1097/BRS.0b013e31816043d1 |
| Ammerman 2006, Surg Neurol 66(5):470-4 | prospective, 100 consecutive lumbar discectomies, single surgeon | wrong level **initially exposed in 15 %**; pathology above L5-S1 and age > 55 predicted it; "four patients had transitional vertebrae" — no analysis of that subgroup | 17084188 / 10.1016/j.surneu.2006.05.069 |
| Jhawar 2007, J Neurosurg Spine 7(5):467-72 | national survey | wrong-level lumbar surgery **12.8 per 10,000 operations** | 17977186 / 10.3171/SPI-07/11/467 |
| Longo 2012, J Bone Joint Surg Br 94(11):1546-50 | systematic review | "the current literature does not provide a definitive estimate of the occurrence of wrong-site spinal surgery" | 23109637 / 10.1302/0301-620X.94B11.29553 |
| Grimm 2014, JBJS Rev 2(3):e2 | review | (no numbers in abstract) | 27490754 / 10.2106/JBJS.RVW.M.00052 |
| Srivatsa 2021, Spine 46(11):E648-E654 | 10-year single-institution root-cause series | 15 wrong-level surgeries in 21,179 operations (0.07 %) | 33306612 / 10.1097/BRS.0000000000003864 |
| Furuya 2026, Bone Joint J 108-B(5):673-680 | multicentre, 34,544 consecutive cases | 40 events; overall incidence **0.12 %** (95 % CI 0.09-0.16); lumbar 0.13 %, thoracic 0.42 %, cervical 0.05 %; mechanisms: intraoperative disorientation 81.3 %, image misinterpretation 18.8 %; disorientation occurred **exclusively at L4/5 or L5/S1** | 42061893 / 10.1302/0301-620X.108B5.BJJ-2025-1129.R2 |

### The share attributable to LSTV / miscounting — the honest answer

**No paper quantifies the fraction of wrong-level events caused by transitional anatomy.** I looked. Furuya's
mechanism split does not name LSTV in the abstract (the full text is paywalled; the accessible text has no
LSTV breakdown — if the manuscript wants to quote one, someone has to read the paper). Ammerman had four
LSTV patients and did not analyse them. What the record *does* support, and it is strong enough:

| paper | what it quantifies | number | PMID / DOI |
|---|---|---|---|
| Nakagawa 2017, Tohoku J Exp Med 242(3):223-228 | 550 consecutive lumbar spine surgery patients | LSTV in 71 (**12.9 %**); the vertebrae were **miscounted at the outpatient clinic in 38 of those 71 (54 %)**; the planned surgical level was altered in 11 (15 %) | 28717058 / 10.1620/tjem.242.223 |
| Shah 2020, Cureus 12(7):e9433 | review: lumbosacral anatomical variants as wrong-level risk | qualitative — "major risk factor", no quantification | 32864257 / 10.7759/cureus.9433 |
| Liebrand 2026, Eur Spine J (online ahead of print) | systematic review of spinal level determination accuracy *including transitional vertebrae* | in studies involving transitional vertebrae, **no conventional method achieved 100 %** level-determination accuracy | 42009915 / 10.1007/s00586-026-09925-x |

The chain the manuscript can build is: LSTV is common (below) -> when present, the level is miscounted more
than half the time at the planning stage (Nakagawa) -> no conventional determination method reaches 100 % on
transitional spines (Liebrand) -> and LevelCheck imports the planning-stage name (section 1). Each link is
citable. The welded sentence "LSTV causes X % of wrong-level surgery" is not.

### LSTV prevalence

| paper | cohort | prevalence | PMID / DOI |
|---|---|---|---|
| Tini 1977, Rheumatol Rehabil 16(3):180-5 | classic series | abstract carries no number; the commonly quoted ~7 % is in the full text — verify before quoting | 143714 / 10.1093/rheumatology/16.3.180 |
| Konin & Walz 2010, AJNR 31(10):1778-86 | review (the standard citation for classification) | abstract carries no prevalence number; cite it for Castellvi classification, not for a rate | 20203111 / 10.3174/ajnr.A2036 |
| Apazidis 2011, Spine J 11(9):858-62 | 211 abdominal films | **35.6 %** (75/211); most common Castellvi IA (14.7 %) | 21951610 / 10.1016/j.spinee.2011.08.005 |
| Nardo 2012, Radiology 265(2):497-503 | 4,636 films (Osteoarthritis Initiative) | **18.1 %** (841/4,636); men 28.1 %, women 11.1 % | 22952380 / 10.1148/radiol.12112747 |
| Nakagawa 2017 (above) | 550 lumbar surgical patients | **12.9 %** (37 sacralised L5, 34 lumbarised S1) | 28717058 |
| Hanhivaara 2020, Eur Radiol 30(6):3409-3416 | 3,855 consecutive abdominal CTs | **29 %** (1,101/3,855); of those, Castellvi I 68 %, II 16 %, III 13 %, IV 3 % | 32072261 / 10.1007/s00330-020-06691-2 |

Read Hanhivaara carefully before using 29 % as the operative number: 68 % of that 29 % is Castellvi type I
(dysplastic transverse process, no articulation), which does not change the count a surgeon or our network
sees on a frame. The numbering-relevant types II-IV are ~32 % of 29 % ~= **9 % of scans**, which sits
consistently beside Nakagawa's 12.9 % in a surgical cohort. Quote the type breakdown, not the headline.

---

## 3. The claim, in two columns (G6)

| Greg CAN say | Greg CANNOT say |
|---|---|
| LevelCheck's published accuracy is registration accuracy; the level name is imported from the preoperative CT annotation (design of all four papers, sec. 1). | "LevelCheck fails on transitional anatomy." No published LevelCheck failure on an LSTV exists. The record is silent, and De Silva 2016 lists anatomical variation as a context where LevelCheck *helps*. |
| A registration system that imports the name cannot, by construction, detect that the imported name follows a different counting convention than the surgeon's; on a transitional spine the two conventions disagree by one level. This is a mechanism statement, argued, not cited. | "Surgeon + LevelCheck makes wrong-level errors at rate X on LSTV." No such rate is published. Our number for this comes from OUR simulation (sec. 5) and must be labelled simulated everywhere it appears, including the title's "versus registration-assisted neurosurgeons". |
| LSTV is present in ~9-18 % of people when counted by numbering-relevant types (Hanhivaara II-IV ~9 %; Nardo 18.1 %; Nakagawa 12.9 % of surgical patients), and when present the level was miscounted at the planning stage in 54 % (Nakagawa). | "Transitional anatomy plus miscounting is the entire set of reasons for wrong-level surgery" (the 02:00 frame). Furuya's mechanism split (disorientation 81.3 % / image misinterpretation 18.8 %) is broader and does not name LSTV. Drop "entire". |
| Wrong-level surgery is real and quantified: 1 in 3,110 procedures (Mody), 12.8/10,000 lumbar (Jhawar), 0.12 % of 34,544 (Furuya), 15 % initial wrong exposure without intraoperative x-ray (Ammerman); half of surveyed surgeons have done one (Mody). | Any single "the wrong-level rate is X" sentence. The estimates span two orders of magnitude by design (career survey vs consecutive series vs exposure-before-imaging), and Longo 2012 says outright there is no definitive estimate. Quote the span, attribute each number to its design. |
| No conventional level-determination method achieved 100 % in studies involving transitional vertebrae (Liebrand 2026 systematic review). | "We beat LevelCheck." On its own terms (registration with a correctly labelled CT) LevelCheck is the ceiling and our oracle-boxes arm reproduces it at 100 % by construction. The claim is parity-or-better with **surgeon + LevelCheck on transitional spines**, where the convention gap lives. |
| IF the G6 numbers land (sec. 4): "on real transitional frames, exact level named with Wilson 95 % lower bound >= 90 %, variant detected with sensitivity lower bound >= 85 %, versus a simulated surgeon + LevelCheck workflow that cannot resolve the convention disagreement." | Any of that BEFORE the COBRA transitional test pool exists: today's real-frame transitional test n is **3** (Wilson lower bound at 3/3 correct: 43.9 %). No phrasing survives n = 3. |
| SchwingNet needs no preoperative CT and no registration — a single exposure suffices (our system's design; contrast with LevelCheck's requirements, sec. 1). | That LevelCheck is "DUA-only" or unavailable — the licensing status has no citable source I could find. Say "research software, not commercially released" and cite Manbachi 2018 for deployment status, or find a source. |

---

## 4. The power table

Wilson two-sided 95 % interval, lower bound on the success proportion with k errors in n transitional test
persons (z = 1.96; script: this file's numbers reproduce with `scipy` or the twenty-line formula; the G6
evidence file recomputes them). **Bold** = meets the level target (lower bound >= 90 %); *italic* = meets
only the variant-sensitivity target (>= 85 %).

| n \ k | 0 | 1 | 2 | 3 | 5 |
|---|---|---|---|---|---|
| 30 | *88.6* | 83.3 | 78.7 | 74.4 | 66.4 |
| 45 | **92.1** | *88.4* | *85.2* | 82.1 | 76.5 |
| 60 | **94.0** | **91.1** | *88.6* | *86.3* | 81.9 |
| 80 | **95.4** | **93.3** | **91.3** | *89.5* | *86.2* |
| 100 | **96.3** | **94.6** | **93.0** | **91.5** | *88.8* |
| 130 | **97.1** | **95.8** | **94.6** | **93.4** | **91.3** |

Minimum n to clear each target: level >= 90 % needs n >= 35 at k=0, 53 at k=1, 69 at k=2, 84 at k=3, 113 at
k=5. Variant sensitivity >= 85 % needs n >= 22 at k=0, 34 at k=1, 45 at k=2, 55 at k=3, 74 at k=5.

**What the current inventory gives** (`SchwingNet/results/anomalous_inventory.md`: VerSe 56, CTSP 18,
TotalSegmentator 12, C-ArmLSpine 3 = **89 transitional persons**, of which 83 L6 and 6 T13; zero typed
sacralised-L5 or four-lumbar rows exist in the inventory today, so two of the four claimed strata currently
have no denominator at all):

- Under the headline 50/10/40 split: test n ~= 36. Lower bound at 36/36 correct: 90.4 % — the level target
  is met only with **zero errors**. One error drops the bound to 85.8 % and fails it.
- Under the plan's own small-inventory rule (< 150 persons -> test takes 50 %): test n ~= 44-45. Zero errors
  92.1 %, one error 88.4 % — still a zero-or-one-error claim with no room.
- **The binding constraint is worse than either number.** The pre-stated target is on transitional REAL
  frames, and real transitional test subjects today are the 3 C-ArmLSpine patients. n = 3, k = 0 gives a
  lower bound of 43.9 %. The 36 and 44 apply only to styled renders, which the plan does not allow for the
  headline claim. The TotalSegmentator 12 are SPINEPS+VERIDAH calls, not release truth, and 3 of them are
  not even in the bank.

**What COBRA must add.** All 692 COBRA cases carry a planning CT, every COBRA transitional case goes to TEST
entirely (G3 rule), and its frames are real. At Nakagawa's surgical-cohort prevalence (12.9 %) the screen
should surface ~89 transitional cases; at the numbering-relevant CT rate (~9 %, Hanhivaara II-IV) ~62. Either
lands the real-frame transitional test n in the 60-90 range on its own, and with C-ArmLSpine takes the total
test pool to the n ~= 100-130 rows, where the level claim tolerates 3-5 errors and the sensitivity claim is
comfortable. **If the COBRA screen surfaces materially fewer (e.g., the planning CTs are FOV-cropped below
the thoracolumbar junction, killing T13 detection), the manuscript reports the bound it has and says the
target was not met — the plan already commits to this.** COBRA is not an enrichment; it is the claim.

---

## 5. The "surgeon + LevelCheck" simulation (G6 experiment 3)

What is being simulated: the surgeon counts vertebrae from a landmark on the intraoperative frame (that is
`tools/count_from_sacrum_eval.py`'s ordinal, with its measured error process — missed or spurious bodies
shifting every ordinal above them); LevelCheck displays the name imported from the preoperative CT (that is
the truth box's name under the convention the CT annotation carries — perfect registration granted, which
the published 100 % clinical series justifies and which makes the simulation conservative in LevelCheck's
favour). The combination fails exactly where the two disagree and nothing in the room can arbitrate.

Inputs that already exist — nothing new is trained:

- `SchwingNet/results/counting.json` + `SchwingNet/results/counting/*.json`: per-frame detected ordinals,
  truth ordinals, match status, per-cell error rates (the surgeon's counting process, measured).
- `tools/alphabet_couple.py` + per-frame `*.couple.json`: ordinals, candidate alphabets, posteriors, calls
  (our system, and the alphabet machinery `sweep_map.alphabet` that turns an ordinal into a name under a
  convention).
- `SchwingNet/results/coupling.json`: our classifier / count / coupled accuracies with intervals.

```
for each transitional test frame f with truth sacrum:                # counting.json rows
    for each truth body b in f with truth ordinal n_b:
        # --- the surgeon ---
        surgeon_ordinal = detected ordinal of b's matched detection  # counting cell; missed -> no count
        surgeon_name    = alphabet("ordinary")(surgeon_ordinal)      # ordinal 1 = L5, five-lumbar assumption
        # --- LevelCheck (perfect registration, imported convention) ---
        for conv in {count_from_C2, count_from_sacrum, morphology}:  # experiment 1's conventions
            lc_name[conv] = name of b in the CT annotation under conv    # = alphabet(conv)(n_b) on truth
        # --- the combination ---
        agree = (surgeon_name == lc_name[conv])
        if agree:   final = surgeon_name          # both proceed; correct only if conv matches truth naming
        else:       UNRESOLVED                    # the disagreement has no arbiter in this workflow;
                                                  # score BOTH policies: defer-to-LevelCheck, defer-to-count
        # --- ours, same frame ---
        ours = coupled call from f's *.couple.json    # variant named; disagreement is a STOP SIGNAL,
                                                      # not an unresolvable conflict
score per stratum, per convention, per policy; person-clustered bootstrap as everywhere else
```

Where the combination cannot resolve a variant, stated plainly: on an ordinary spine, surgeon and LevelCheck
agree whenever both are individually right — the combination is strong, and we do not pretend otherwise. On
an L6 spine, the surgeon's five-lumbar alphabet names ordinal 1 "L5" while a CT annotated by a
count-from-C2 radiologist imports "L6" (or vice versa): **a disagreement that is not an error signal but a
convention gap, and neither party holds the third piece of information — the variant — needed to resolve
it.** Deferring to LevelCheck reproduces the CT convention, right or wrong for the surgical plan; deferring
to the count reproduces the five-lumbar assumption, wrong by construction on the variant. The disagreement
rate on transitional spines equals experiment 1's convention-disagreement rate, and that is the quantity our
variant call removes. That sentence — not "LevelCheck fails" — is the claim.

Honesty constraints carried into the manuscript: (a) the surgeon model is a geometric counter with the
detector's own error process, not a human; label it simulated in every table, figure and the title phrase;
(b) perfect registration is granted to LevelCheck, so every LevelCheck-side number is an upper bound —
say so; (c) the convention set {C2-count, sacrum-count, morphology} is our formalisation; no paper
enumerates radiologists' conventions this way (the systematic review PMID 42009915 is the nearest support);
(d) all numbers on the old whole-vertebra boxes must be rescored on body boxes before quoting (A28).
