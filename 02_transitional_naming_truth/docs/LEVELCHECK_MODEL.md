# The LevelCheck comparator, pre-specified and frozen

Written 2026-09-23. The commit that adds this file is the pre-registration timestamp
(`git log --diff-filter=A --format='%H %cI' -- SchwingNet/LEVELCHECK_MODEL.md`).

**The rule.** The comparator values, strata, endpoint, test, multiplicity rule and sweep range below are FROZEN.
They may not be changed after any SchwingNet transitional result on the G3 test persons is computed. Section 9
says what counts as "computed", what may still change before then and how, and what happens to a change made
after. Section 8 lists every transitional result that had been seen when this file was written, because some
had.

Sources were read for this file on 2026-09-23. For Manbachi 2018, De Silva 2016, Nakagawa 2017 and Liebrand 2026
the full text was read. For Lo 2015, Otake 2012, Peh 1999, Yun 2018 and Albano 2024 only the PubMed abstract
was read. Section 10 lists what this reading corrects in `LEVELCHECK_CLAIM.md`.

---

## 1. The model

LevelCheck registers the preoperative CT to the intraoperative radiograph by 3-D/2-D intensity registration. It
then projects the vertebral labels that a reader assigned on that CT. It does not infer a name; it carries one
over from the CT. Every published LevelCheck accuracy uses those same CT labels as its truth:

- Lo 2015: "A board-certified neuroradiologist determined the 'true' vertebra levels".
- De Silva 2016: "Definition of vertebral levels was provided in each preoperative CT by a fellowship-trained
  neuroradiologist".
- Manbachi 2018: "The true location of each vertebra was defined in preoperative CT for each patient by a
  board-certified neuroradiologist".

So a published LevelCheck study cannot detect an error in the planning read, by design. The comparator is
therefore modelled, per stratum *s*, as

    p_LC(s) = r x (1 - e(s))

- **r** is the probability that registration succeeds.
- **e(s)** is the probability that the preoperative label of a scored vertebra differs from the reference name
  used to score SchwingNet.

Two simplifications both favour LevelCheck and are deliberate:

- No residual surgeon error is multiplied in.
- A surgeon who reads a wrong imported label on a transitional spine is not credited with catching it. The
  surgeon's own count from the sacrum errs in the same direction. Nakagawa's miscounts are themselves surgeons'
  counts.

The first choice lifts p_LC. The second is argued in `LEVELCHECK_CLAIM.md` §5 and cited to nobody.

**What the LevelCheck group itself says about transitional anatomy.** The literature does not ignore it:

- De Silva 2016 allowed "for normal anatomical variations, such as L6, T13" in the neuroradiologist's CT labels.
- It names "counting from the 12th rib vs counting from the sacrum" as a problem LevelCheck could help
  standardise, and shows an LSTV example (its Fig. 4e).
- It raises the scenario "in which the surgeon makes a localization error, followed by the algorithm making the
  same error", and says it "did not encounter this scenario", judged "according to annotations defined by the
  neuroradiologist".
- Manbachi 2018 shows two operating-room patients with variants labelled consistently with the CT read: a 13th
  rib at L1 (Fig. 6b) and a lumbarised S1 (Fig. 6c). Both were among 20 of 20 that were accurate.

The published position is therefore that LevelCheck carries a variant-aware read into the room. Where the
preoperative read counted correctly, e = 0, and LevelCheck with a surgeon is the ceiling. SchwingNet can at best
reach parity there. **SchwingNet can only exceed surgeon + LevelCheck where the preoperative read did not count
correctly**, and the manuscript's claim must carry that condition (§6).

---

## 2. The parameters, one source at a time

**Registration success, r. Point 1.0; range 0.993-1.000.**

- Lo 2015 (PMID 25646750): 20 consecutive thoracolumbar patients, 500 random initialisations each (10,000
  trials). Success was a projection distance of at most 5 mm: 100 % at 200 multistarts (about 26 s) and 99.3 % at
  50 (about 7 s). The trials share 20 patients, so no binomial interval applies.
- De Silva 2016 (PMID 27035579): 504 radiographs from 198 patients, of which 89 were excluded:
  - 13 showed three or fewer levels;
  - 22 had minimal overlap with the CT;
  - 53 were cervical cases with head or neck repositioning;
  - 21 had poor image quality.

  That left 398 radiographs from 178 patients, all registered to within 30 mm projection distance.
- Otake 2012 (PMID 22864366): 10 CTs and 50,000 simulated images, 99.998 % at mean projection distance under
  5 mm.
- r = 1.0 grants LevelCheck perfect registration.

**The published surgeon + LevelCheck accuracy: 97.6 % (the "~97 %"). Manbachi 2018 (PMID 30051244), Study 1.**

What the number is:

- Five surgeons read 62 radiographs (7 cervical, 32 thoracic, 23 lumbar), chosen as "the most challenging cases
  to localize" from the De Silva dataset.
- 16 of the 62 carried a deliberately shifted label ("labeling error—e.g., shift by one vertebra").
- Each surgeon's error rate was computed. The reported value is the **median over the five surgeons**:
  - 30.4 % (IQR 5.2) unassisted;
  - 2.4 % with LevelCheck as Independent Check (IQR 10.6);
  - 2.4 % with LevelCheck as Active Assistant (IQR 3).
- The unassisted and assisted rates were compared with a paired t test, P < .01.
- 97.6 = 100 - 2.4.

What it is not:

- **No per-surgeon denominator and no confidence interval is published, so no Wilson interval can be computed
  for 97.6 %.** It enters this model as a fixed constant.
- It is not LevelCheck alone: it is surgeons overriding labels, a quarter of which were deliberately wrong.
- Confidence rose in 373 of 410 readings (91.0 %; Wilson 87.8-93.4).

**The operating-room series: 20 of 20. Manbachi 2018, Study 2.**

- 20 patients (8 cervical, 4 thoracic, 8 lumbar), 2 surgeons, Independent Check mode.
- "No wrong-level localizations on the part of the surgeon, and ... no registration errors". Wilson 83.9-100.
- Two of the 20 carried variants (Fig. 6b, 6c). Both were labelled as the CT read labelled them. The paper
  reports no whole-spine count for them.

**The planning read on lumbosacral transitional spines. Nakagawa 2017 (PMID 28717058).**

- 550 consecutive lumbar operations, March 2011 to May 2012. 71 had LSTV (12.9 %); Castellvi type I
  sacralisation was excluded from the definition.
- Index read: the outpatient count on lumbar radiographs and/or MRI.
- Reference: whole-spine AP radiograph, with the cervical and thoracic counts fixed at 7 and 12.
- Miscounted: 38 of 71 (53.5 %; Wilson 42.0-64.6). By Castellvi type (Table 2):

  | Subtype | Castellvi type | Miscounted |
  |---|---|---|
  | Sacralisation | II | 0/23 |
  | Sacralisation | III | 10/14 |
  | Lumbarisation | I | 14/14 |
  | Lumbarisation | II | 8/9 |
  | Lumbarisation | III | 4/8 |
  | Lumbarisation | IV | 2/3 |

- Counted correctly, as accuracies:

  | Group | Counted correctly | % | Wilson 95 % |
  |---|---|---|---|
  | All LSTV | 33/71 | 46.5 | 35.4-58.0 |
  | Lumbarised S1 (six lumbar) | 6/34 | 17.6 | 8.3-33.5 |
  | Sacralised L5, type III | 4/14 | 28.6 | 11.7-54.6 |
  | Count-changing (sacralisation III plus all lumbarisation) | 10/48 | 20.8 | 11.7-34.3 |
  | Sacralised L5, type II (count unchanged) | 23/23 | 100 | 85.7-100 |

- 11 of 71 (15.5 %; Wilson 8.9-25.7) needed an altered or additional operation:
  - 9 were among the miscounted, which is 9 of 38 (23.7 %);
  - 2 had been counted correctly and had a second lesion.

  **Every one of the 11 was an added level ("One lower-level fenestration added", "One upper-level ... added";
  Table 4). None was a level substituted for another.** This is not a wrong-level surgery rate, and it is not
  used as one.

**A radiologist's planning read without a count from C2. Peh 1999 (PMID 10488518).**

- 129 patients (from 141 consecutive), two radiologists. The index was the lumbosacral localiser scans alone;
  the reference was a count down from C2 on a cervicothoracic localiser.
- Lumbar segments were identified correctly in:
  - 80.2 % from the sagittal localiser;
  - 82.2 % from the coronal localiser;
  - 77.9 % from both together.
- Interobserver discordance was 11.6 %. LSTV was present in 17 (13.2 %).
- These percentages are over **all** patients, not the transitional ones, so on transitional spines they
  overstate the read's accuracy. That is why 82.2 % is the value frozen (§3).
- The abstract states no denominator. All three percentages fit 258 reads (207, 212 and 201 of 258). That is
  arithmetic, not a quoted count, and nothing below uses it.

**Thoracolumbar variants. Yun 2018 (PMID 30386145).**

- 100 patients with spinal variants, from 1,446 consecutive spine CTs.
- By morphology, L1 was the 21st segment in 65 %, the 20th in 31 % and the 19th in 4 %.
- A count that assumes twelve thoracic vertebrae (20th = L1) therefore agrees with morphology on L1 in 31 of
  100 (Wilson 22.8-40.6).
- This measures disagreement between conventions, not error against an external count.

**The systematic review. Liebrand 2026 (PMID 42009915).**

- Four studies specific to transitional vertebrae (its Table 2):
  - Nakagawa: "54 % incorrect";
  - Peker 2019: "not accurate";
  - Yan 2018: "96,6 %";
  - Yun 2018: "99 %".
- The Yan and Yun values are agreement measures: surgeon against radiologist, and κ 1.00 between readers.
  Neither is accuracy against a reference. Both were rated at high risk of bias.
- "In the studies involving transitional vertebrae no 100% was achieved." "Studies focusing on the full spine
  showed high accuracies, whereas lumbar-oriented studies had very low accuracies."
- On LevelCheck, the review lists as limitations "the assumption of 12 thoracic vertebrae in CT image definition"
  and that "most studies measure technical registration, not true clinical accuracy". The first conflicts with
  De Silva's "allowed for normal anatomical variations, such as L6, T13". Both statements are recorded here;
  neither decides p0.

**Outcome, not naming. Albano 2024 (PMID 38350597).**

- 39 studies, 885 surgical patients with LSTV.
- Wrong-level surgery in 12 (1.4 %; Wilson 0.8-2.4). Liebrand quotes this as 1.3 %.
- These are pooled case series, and reporting is probably incomplete.
- This is the rate at which the whole clinical process ends in wrong-level surgery. **Neither SchwingNet's naming
  accuracy nor p_LC is a wrong-level surgery rate.** No sentence in the manuscript may convert one into the
  other.

---

## 3. The frozen comparator, stratum by stratum

The strata are defined from the reference standard alone, never from a prediction. **Membership is fixed in the
frozen truth file before unblinding (§5).**

**At risk.** A transitional person whose scored frame carries at least one reference-named vertebral body whose
reference name differs from the name the ordinary alphabet gives it under either convention:

- (i) counting up from the sacrum with five lumbar vertebrae (what a surgeon, or a planning read limited to the
  lumbar spine, does);
- (ii) counting down from C2 with 7 cervical, 12 thoracic and 5 lumbar, at the vertebra's reference ordinal.
  This is what a read does that assumes twelve thoracic vertebrae.

In practice the rule flags:

- L6 with its own label when the L6 body is on the frame;
- a sacralised L5 merged into the sacrum label, or left unlabelled;
- T13 on any frame showing its thoracolumbar or lumbar bodies.

It does not flag:

- L6 fused to the sacrum and left unlabelled;
- a sacralised L5 that keeps its own L5 label;
- Castellvi I/II;
- a lumbar rib.

Persons of those kinds, and transitional persons with no frame on which the rule flags a difference, form the
**variant, naming unaffected** stratum. Counting them as at risk would credit SchwingNet with LevelCheck errors
that cannot happen on the frame.

For the sweep, "Nakagawa 17.6 %" means lumbarised S1: 6/34 counted correctly, and 28.6 % means sacralisation
type III: 4/14. The frozen p0 is 82.2 %.

| Stratum | Frozen p0 (point) | Source of the point value | Literature range of p_LC (low to high) | Sweep | Test |
|---|---|---|---|---|---|
| **At risk, pooled** (H1) | **0.822** | Peh 1999, coronal localiser: the most favourable to LevelCheck of the published accuracies of a planning read made without a count from C2. Measured on all patients, so generous on transitional ones. | 20.8 % (Nakagawa count-changing, 10/48) to 100 % (the read counted correctly; Manbachi OR 2/2 variant cases). Also 46.5 % (Nakagawa all LSTV, 33/71) and 77.9-82.2 % (Peh). | 0.10-1.00 | superiority, exact, one-sided |
| **At risk, pooled, versus the published figure** (H2) | **0.976** | Manbachi 2018 Study 1, surgeon + LevelCheck median. Assumes the planning read counted the variant correctly. | as H1 | as H1 | superiority, exact, one-sided |
| At risk, L6 (H3) | 0.822 | as H1 (Peh gives no subtype) | 17.6 % (Nakagawa lumbarised S1, 6/34) to 100 % | 0.10-1.00 | superiority |
| At risk, sacralised L5 (H4) | 0.822 | as H1 | 28.6 % (Nakagawa sacralisation III, 4/14) to 100 % | 0.10-1.00 | superiority |
| At risk, T13 (H5) | 0.822 | Borrowed from H1: no planning-read series on thoracolumbar variants exists | 31 % (Yun: a twelve-thoracic count agrees with morphology on L1 in 31/100 variant patients) to 100 % | 0.10-1.00 | superiority |
| **Ordinary** (H6) | 0.926 = 0.976 - 0.05 | Non-inferiority to the published 97.6 %. The margin of 5 points is the author's judgement, **made knowing the development accuracy on ordinary spines (§8)**. | 97.6 % (Manbachi Study 1) to 100 % (Manbachi OR 20/20, Wilson 83.9-100) | 0.90-1.00 | non-inferiority, exact, one-sided |
| Variant, naming unaffected | none; descriptive against 0.976 and 1.00 | Nakagawa sacralisation type II: 23/23 counted correctly (no count gap) | 97.6-100 % | 0.90-1.00 | descriptive only |

---

## 4. The endpoint, the unit and what is scored

**Unit.** The person (G2 person key). There is one Bernoulli outcome per person.

**Frames.**

- **Primary: real frames only**, which are the only real transitional frames there are: COBRA and C-ArmLSpine,
  G3 test side.
- Styled renders of test persons who exist only as CT are a secondary analysis, labelled as renders.

**Eligible frame.**

- At least four reference-named vertebral bodies are in the field. This matches LevelCheck's own evaluation, which
  excluded frames showing three or fewer levels (De Silva 2016, 13 of 504).
- For an at-risk stratum, it must also be a frame on which the §3 rule flags a naming difference.
- Frames with one to three bodies are a secondary, limited-field analysis.

**The scored frame.**

- One eligible frame is drawn per person using `numpy.random.default_rng(20260923)`.
- Persons are visited in ascending person-key order and draw once each: `rng.integers(len(frames))` over that
  person's eligible frames, sorted by frame stem.
- The draw uses the truth only, so it is fixed before any prediction exists. Every eligible frame is also scored,
  in a secondary analysis with a person-clustered bootstrap (2,000 resamples, seed 0, percentile).

**Correct.** Every reference-named vertebral body on the scored frame receives SchwingNet's reference name. Any of
the following counts as not correct:

- a truth body with no detection;
- a detected body with no name;
- an abstention or low-margin stop;
- a frame without an anchor.

This is the matched endpoint. A planning-read miscount on a transitional spine shifts every lumbar name at once,
so for LevelCheck the model gives one outcome per person: correct with probability p_LC.

**What SchwingNet is scored.** Exactly one configuration is primary, and it is named in the G5 manifest and
committed before unblinding:

- the held-out-transitional evaluation arm, which is never trained on any test person;
- the coupled call (classifier plus count, through the alphabet coupling);
- detector confidence 0.74, the cross-device operating point already stated before these results;
- the whole frame.

If G5 trains several seeds, seed 0 is primary and every other seed is reported beside it. **No configuration,
checkpoint, threshold or seed is chosen on test persons.** "The best possible model" in Figure 6 means this
configuration. Anything else is a labelled secondary result.

**Reference standard.**

- The source's release truth where a human read exists: VerSe, and the CTSpinoPelvic1K consensus.
- Where the subtype and names come from SPINEPS+VERIDAH (COBRA, TotalSegmentator, C-ArmLSpine), a human
  verification of subtype and names is written to a frozen truth file, and its SHA-256 is recorded, **before
  unblinding**.
- Naming follows the rib convention used in `SchwingNet/results/rare_class/transitional_subtypes.md`: L6 is six
  rib-free vertebrae above the sacrum; T13 is thirteen rib-bearing vertebrae.
- A person whose reference cannot be verified is excluded before unblinding, and the reason is counted in the flow
  diagram.

**Excluded from the primary analysis in advance: the three real C-ArmLSpine L6 patients.** Their SchwingNet
outputs were examined before this file existed (§8). Their reference is two labellers who disagree on a
lumbar-only CBCT, and "neither could count" (`results/COUPLING.md`). They are reported descriptively.

---

## 5. The statistical comparison

**Per hypothesis:**

- k correct of n persons.
- Accuracy with its Wilson 95 % interval (z = 1.959964), reported for description.
- The one-sided exact binomial P = P(X >= k | n, p0), which decides.

Near the boundary the Wilson bound and the exact test can disagree; the exact test governs.

**Eligibility.** A hypothesis is tested only if its stratum's test n is at least n_min: the smallest n at which n
of n correct gives P <= 0.025. This is decided from the frozen split and truth file, before unblinding.

| p0 | n_min at 0.025 | at 0.025/2 | at 0.025/3 | at 0.025/6 |
|---|---|---|---|---|
| 0.822 (H1, H3-H5) | 19 | 23 | 25 | 28 |
| 0.926 (H6) | 48 | 57 | 63 | 72 |
| 0.976 (H2) | 152 | 181 | 198 | 226 |

**Multiplicity.** Holm step-down over the eligible hypotheses among H1-H6, at a familywise one-sided alpha of
0.025. An ineligible hypothesis is reported descriptively (accuracy, Wilson interval, the frozen p0 beside it),
and **the manuscript may not claim it**.

**Secondary analyses (outside the family, each labelled secondary):**

- **Break-even p\***: the one-sided 97.5 % Clopper-Pearson lower bound on SchwingNet's accuracy per stratum. This
  is the largest LevelCheck accuracy SchwingNet beats at one-sided 0.025. It is drawn on the §7 sweep.
- **Confidently wrong**: a wrong name, excluding abstentions, compared with e = 1 - p0.
- Every eligible frame, with the person-clustered bootstrap.
- Styled renders of test persons who exist only as CT.
- Frames with one to three bodies.
- **Excluding everyone whose frames entered any SchwingNet evaluation before this commit**: the 27 COBRA test
  patients of `results/COUNTING.md`, and every C-ArmLSpine case.
- The simulated surgeon + LevelCheck arm of `LEVELCHECK_CLAIM.md` §5, labelled simulated everywhere. It is
  derived from our data and **never replaces the frozen p0**.

The G6 targets in `docs/FLAGSHIP_PLAN.md` still stand, and are separate from this comparator: exact level with a
Wilson lower bound of at least 90 %, and variant sensitivity with a lower bound of at least 85 %.

---

## 6. What the manuscript may say

**H1 rejected.** The manuscript may write:

> "On real frames of transitional spines at risk of a naming error, SchwingNet named every vertebra correctly in
> k of n persons (x %; 95 % CI a-b), exceeding the 82.2 % modelled for surgeon + LevelCheck when the preoperative
> labels come from a planning read without a count from C2 (Holm-adjusted P = ...)."

The condition clause and the word "modelled" are part of the claim.

**H1 not rejected.** The bound is reported, and the manuscript says the comparison was not met.

**H2.** "Exceeds the published 97.6 % accuracy of surgeon + LevelCheck" is allowed **only if H2 is eligible and
rejected**. Otherwise the text puts the interval beside 97.6 % and makes no claim.

**Always stated:**

- No study has measured LevelCheck against an external count on transitional spines. p_LC is a model.
- Where the preoperative read counted correctly, LevelCheck is the ceiling.
- Neither number is a wrong-level surgery rate (Albano 2024: 12 of 885).

---

## 7. Power, and the plain answer about 97 %

Everything in this section uses the one-sided exact binomial test.

**H1 against 0.822, unadjusted alpha 0.025.** "Errors allowed" is n minus the smallest passing k.

| Test persons n | Errors allowed | Power if true accuracy is 90 % | 95 % | 97 % |
|---|---|---|---|---|
| 20 | 0 | 0.12 | 0.36 | 0.54 |
| 30 | 1 | 0.18 | 0.55 | 0.77 |
| 45 | 2 | 0.16 | 0.61 | 0.85 |
| 60 | 4 | 0.27 | 0.82 | 0.97 |
| 80 | 7 | 0.45 | 0.95 | 1.00 |
| 100 | 10 | 0.58 | 0.99 | 1.00 |
| 130 | 14 | 0.68 | 1.00 | 1.00 |

**H1 at the Holm step alpha/3** (three eligible hypotheses, the likely family):

| Test persons n | Errors allowed | Power if true accuracy is 90 % | 95 % | 97 % |
|---|---|---|---|---|
| 30 | 0 | 0.04 | 0.21 | 0.40 |
| 45 | 1 | 0.05 | 0.33 | 0.61 |
| 60 | 3 | 0.14 | 0.65 | 0.89 |
| 80 | 6 | 0.30 | 0.89 | 0.99 |
| 100 | 8 | 0.32 | 0.94 | 1.00 |
| 130 | 12 | 0.46 | 0.99 | 1.00 |

**H2 against 0.976 (the "~97 %").**

- The test needs **at least 152 at-risk real-frame test persons with zero errors**, and 198 at the alpha/3 step.
- At 152 persons, a network that is truly 99 % accurate passes with probability 0.22. At 300 persons it passes
  with probability 0.42. At a true 97 %, about 0.01.
- **At the current inventory, SchwingNet cannot be shown to exceed 97.6 %, however well it performs.** That
  number is reported beside the interval, not beaten.

**H6 against 0.926.**

- At least 48 ordinary persons with zero errors.
- At 145 persons, power is 0.44 at a true 98 % and 0.82 at 99 % (unadjusted).

**Break-even p\*** (one-sided 97.5 % Clopper-Pearson lower bound, %):

| Test persons n | 0 errors | 1 | 2 | 3 | 5 | 10 |
|---|---|---|---|---|---|---|
| 20 | 83.2 | 75.1 | 68.3 | 62.1 | 50.9 | 27.2 |
| 30 | 88.4 | 82.8 | 77.9 | 73.5 | 65.3 | 47.2 |
| 45 | 92.1 | 88.2 | 84.9 | 81.7 | 75.9 | 62.9 |
| 60 | 94.0 | 91.1 | 88.5 | 86.1 | 81.6 | 71.5 |
| 80 | 95.5 | 93.2 | 91.3 | 89.4 | 86.0 | 78.2 |
| 100 | 96.4 | 94.6 | 93.0 | 91.5 | 88.7 | 82.4 |
| 130 | 97.2 | 95.8 | 94.6 | 93.4 | 91.3 | 86.3 |

**The sweep Figure 6 draws.**

- **x axis**: the modelled p_LC, from 0.10 to 1.00 in steps of 0.005 (181 values); for ordinary spines and the
  unaffected stratum, 0.90 to 1.00.
- **What is drawn** at each x: SchwingNet's accuracy with its Wilson band, and the exact one-sided P.
- **Marked**: p\* and the frozen p0.
- **Anchor ticks** (`anchors` in §11), so that the reader sees where the published figures fall.
- **Registration**: r is not swept separately, because its published range moves p_LC by less than 0.7 points.
- **Caption**: the figure says "modelled".

---

## 8. What had been seen when this file was written

The G3 split does not exist yet (`tools/make_split.py` is being written by another workflow). So no output on a
G3 test person has been scored under this endpoint. **But this file is not blind to transitional results.** These
had been computed and read:

1. **Ordinary spines, C-ArmLSpine (development, all 145 cases).** Every lateral vertebra right in 138 of 141
   cases (97.9 %; Wilson 93.9-99.3; `results/a4.json`). Coupled per body 97.5 % (1,120/1,149) at detector
   confidence 0.25 (`NUMBERS.md`, Table 3). The H6 margin was chosen knowing these numbers.
2. **The three real L6 patients (C-ArmLSpine), frame by frame** (`results/COUPLING.md`). With detected boxes, the
   coupled names matched the VERIDAH L6 naming on 1 of 5 anchored whole frames. Variant calls on ordinary frames:
   6 of 266 anchored frames were called L6.
3. **Renders.** Body-level L6 recall was 56.1-72.4 % on 10 held-out L6 spines (v9 validation, three seeds, loss
   weights 0, 0.3 and 1.0; `results/alphabet_loss.json`, `results/ALPHABET_LOSS.md`). The sweep_v3 variant calls covered one L6 spine per arm
   (`results/COUPLING.md`).
4. **COBRA.** Counting from the sacrum on 648 frames of 27 COBRA test patients (`results/COUNTING.md`), seen in
   aggregate before anyone knew which of them are transitional. The CT-based COBRA LSTV screen (a subtype census
   from SPINEPS+VERIDAH, not a SchwingNet output).

**The closest development measurements of transitional naming (items 2 and 3) are all below the frozen 82.2 %.**
The freeze is not set below any transitional accuracy that had been seen. The persons behind items 1, 2 and 4
are handled by the §4 exclusion and the §5 sensitivity analysis.

---

## 9. The freeze

**Frozen:** everything in §3-§5 and the JSON block in §11, that is:

- the p0 values and margin;
- the strata and their truth-only membership rule;
- the endpoint;
- frame eligibility, the draw seed and the draw order;
- the test;
- the alpha;
- Holm;
- the eligibility rule;
- the sweep range.

**Unblinding** is the earliest of two events: the first run of any SchwingNet model on any frame of a G3 test
person in a transitional stratum, or the first scoring of such an output against truth. The G6 evaluator must
record the UTC time and `git rev-parse HEAD` at that moment. The commit that adds this file must be an ancestor of
that HEAD and earlier than that time. If it is not, the analysis is reported as not pre-specified.

**Before unblinding**, a value may change only by a new commit to this file. That commit lists the old value, the
new value and the reason, and the manuscript reports both.

**After unblinding**, nothing in the frozen list changes. Any analysis at another p0 is labelled post hoc, and it
is printed after the frozen analysis, never instead of it. If a reference name is corrected after unblinding (a
radiologist re-read, for example), both analyses are reported.

**If a live workflow's output disagrees with a definition here**, this file governs the confirmatory analysis.
Examples are the harvest's subtype names or the G3 stratum labels. The mapping between the two is written down
before unblinding.

---

## 10. What this reading corrects in `LEVELCHECK_CLAIM.md`

That file is not edited here. Its owner should take these changes.

- **"The convention problem ... is simply not addressed in this literature" is wrong at the full-text level.**
  De Silva 2016:
  - allowed L6 and T13 in the CT labels;
  - discusses 12th-rib versus sacrum counting;
  - raises the case of a surgeon and the algorithm making the same error.

  Manbachi 2018:
  - names "lumbarized sacrum or thirteenth thoracic vertebra" as sources of counting error;
  - shows two variant operating-room cases labelled consistently with the CT read.

  The accurate statement is that the literature addresses the problem, and its evidence is judged only against
  the neuroradiologist's own labels.
- **The 97.6 % needs its full definition wherever it appears:**
  - the median of five surgeons' error rates;
  - 62 challenging radiographs;
  - 16 of them with deliberately shifted labels;
  - truth = the CT labels;
  - no interval computable.
- **Nakagawa's "planned level changed in 11 (15 %)" means additional levels were added in 11**:
  - 9 of them among the 38 miscounted;
  - 2 among patients counted correctly;
  - no level was substituted.
- **Nakagawa's LSTV definition excludes Castellvi type I sacralisation, and its miscounts are concentrated by
  type**: 0 of 23 for sacralisation type II, against 28 of 34 lumbarised S1.
- Liebrand 2026 adds a citable limitation of LevelCheck ("the assumption of 12 thoracic vertebrae in CT image
  definition") and a citable outcome figure (Albano 2024, wrong-level surgery in 12 of 885 LSTV surgical patients).

---

## 11. The frozen values, machine-readable, and how to reproduce every number

```json
{
  "file": "SchwingNet/LEVELCHECK_MODEL.md",
  "version": 1,
  "frozen_by": "the commit that adds this file",
  "model": "p_LC(stratum) = r * (1 - e(stratum))",
  "r_registration_success": 1.0,
  "r_published_range": [0.993, 1.0],
  "unit": "person (G2 person key)",
  "primary_frames": "real",
  "frame_min_reference_named_bodies": 4,
  "frame_draw": "numpy.random.default_rng(20260923); persons in ascending person-key order; rng.integers(len(frames)) over eligible frames sorted by stem",
  "correct": "every reference-named body on the drawn frame receives its reference name; missed, unnamed, abstained or unanchored = not correct",
  "schwingnet_primary": "the single G5-manifest configuration committed before unblinding: held-out-transitional arm, coupled call, detector confidence 0.74, whole frame, seed 0",
  "test": "one-sided exact binomial, P = P(X >= k | n, p0); Wilson 95 % reported (z = 1.959964)",
  "alpha_one_sided_familywise": 0.025,
  "multiplicity": "Holm over eligible hypotheses",
  "eligibility": "tested only if n >= n_min, the smallest n with P(X >= n | n, p0) <= 0.025",
  "hypotheses": [
    {"id": "H1", "stratum": "at_risk_pooled", "test": "superiority", "p0": 0.822, "n_min": 19, "role": "primary"},
    {"id": "H2", "stratum": "at_risk_pooled", "test": "superiority", "p0": 0.976, "n_min": 152, "role": "key secondary"},
    {"id": "H3", "stratum": "at_risk_L6", "test": "superiority", "p0": 0.822, "n_min": 19},
    {"id": "H4", "stratum": "at_risk_sacralised_L5", "test": "superiority", "p0": 0.822, "n_min": 19},
    {"id": "H5", "stratum": "at_risk_T13", "test": "superiority", "p0": 0.822, "n_min": 19},
    {"id": "H6", "stratum": "ordinary", "test": "non_inferiority", "p_ref": 0.976, "margin": 0.05, "p0": 0.926, "n_min": 48}
  ],
  "descriptive_only": ["variant_naming_unaffected", "renders", "frames_with_1_to_3_bodies", "carmlspine_three_L6"],
  "sweep": {"transitional": {"min": 0.10, "max": 1.00, "step": 0.005}, "ordinary_and_unaffected": {"min": 0.90, "max": 1.00, "step": 0.005}},
  "anchors": [
    {"label": "Nakagawa 2017, lumbarised S1 counted correctly", "k": 6, "n": 34, "value": 0.176, "pmid": "28717058"},
    {"label": "Nakagawa 2017, count-changing LSTV counted correctly", "k": 10, "n": 48, "value": 0.208, "pmid": "28717058"},
    {"label": "Nakagawa 2017, sacralisation type III counted correctly", "k": 4, "n": 14, "value": 0.286, "pmid": "28717058"},
    {"label": "Yun 2018, twelve-thoracic count agrees with morphology on L1", "k": 31, "n": 100, "value": 0.310, "pmid": "30386145"},
    {"label": "Nakagawa 2017, all LSTV counted correctly", "k": 33, "n": 71, "value": 0.465, "pmid": "28717058"},
    {"label": "Peh 1999, lumbosacral localisers, both", "value": 0.779, "pmid": "10488518"},
    {"label": "Peh 1999, sagittal localiser", "value": 0.802, "pmid": "10488518"},
    {"label": "Peh 1999, coronal localiser (frozen p0)", "value": 0.822, "pmid": "10488518"},
    {"label": "Manbachi 2018, surgeon + LevelCheck, median of five surgeons", "value": 0.976, "pmid": "30051244"},
    {"label": "Manbachi 2018, operating-room series", "k": 20, "n": 20, "value": 1.0, "pmid": "30051244"}
  ]
}
```

Every interval, n_min, power, errors-allowed and break-even value above reproduces with this (scipy 1.18):

```python
import math
from scipy.stats import binom, beta

Z = 1.959963984540054

def wilson(k, n):
    p = k / n
    d = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / d
    h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)

def p_exact(k, n, p0):           # one-sided P(X >= k | n, p0)
    return binom.sf(k - 1, n, p0)

def n_min(p0, alpha=0.025):
    n = 1
    while p_exact(n, n, p0) > alpha:
        n += 1
    return n

def k_crit(n, p0, alpha=0.025):  # smallest passing k, or None
    return next((k for k in range(n + 1) if p_exact(k, n, p0) <= alpha), None)

def power(n, p0, p1, alpha=0.025):
    k = k_crit(n, p0, alpha)
    return 0.0 if k is None else binom.sf(k - 1, n, p1)

def break_even(k, n):            # one-sided 97.5 % Clopper-Pearson lower bound
    return 0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1)
```

---

## 12. Added before unblinding: the mechanism test and the transitional flag

Added 2026-09-23 at 20:50 EDT (the commit time governs), by a new commit to this file, as §9 requires. **Nothing in §3-§5 or §11
changes:** no p0, stratum, endpoint, draw, test, alpha, Holm family or sweep. The analyses below are
pre-specified SECONDARY analyses. They sit outside the H1-H6 family, and the manuscript may not present them as
confirmatory. At this commit no SchwingNet model had run on any frame of a G3 test person: the only Figure 6
grid jobs were COBRA frame exports (`f6cobx`), and `results/fig6/` held only the export list and a name remap.

**Why (Greg, 2026-09-23):** a surgeon is tricked by the count on a transitional spine. The network carries both
the count and the local morphology of each vertebra. This section tests that directly, on the same frames.

### M1. The count against the count plus morphology

- **Persons:** the G3 test persons of the lumbosacral transitional strata (L6; sacralised or fused L5;
  four-lumbar), on the §4 scored frame with the §4 eligibility, reference standard and draw.
- **Arms, all from ONE SchwingNet run, the same detector at confidence 0.74 and the same frame:**
  - COUNT: the name each body gets by counting up from the detected sacrum with the ordinary alphabet, as
    `tools/alphabet_couple.py` computes it. This is a within-study surrogate for a surgeon's count from the
    sacrum, and it is called a surrogate wherever it is quoted.
  - MORPHOLOGY: the level classifier's own names, with no count.
  - COUPLED: the primary configuration of §4.
- **Outcome:** §4 "correct" (every reference-named body gets its reference name), one outcome per person per
  arm.
- **Test:** exact one-sided McNemar, COUPLED better than COUNT, on the discordant persons, at alpha 0.025. It
  is tested only if at least 6 persons are discordant; otherwise it is reported descriptively. MORPHOLOGY is
  reported beside both arms.
- **T13 is descriptive only.** A count from the sacrum names the lumbar bodies of a T13 spine correctly. The
  surgeon's T13 error is a count from the ribs, which this system does not make. Claiming M1 on T13 would test a
  surrogate that does not err.
- **Ordinary persons:** the same three-arm table, reported to show what the coupling costs where the count is
  already right.

### F1. The transitional flag (a high-sensitivity stop signal)

- **The flag, per person, on the §4 scored frame:** the spine is flagged transitional when ANY of these holds:
  - (a) the coupling chooses a non-ordinary alphabet;
  - (b) the count and the morphology disagree on any reference-named body;
  - (c) in the dual-loss arm only, the spine-level transitional probability is at or above tau.
- **tau is fixed on the G3 VALIDATION split only.** It is the largest value that gives at least 95 % validation
  sensitivity. It is written with its SHA-256 into `results/fig6/frozen/` before any test person is scored.
- **Endpoint:**
  - sensitivity on transitional test persons (every subtype pooled, then per subtype);
  - specificity on ordinary test persons;
  - Wilson intervals for both.
- **Target**, carried over from `docs/FLAGSHIP_PLAN.md` G6: a sensitivity lower bound of at least 85 %.
- **The flag's clinical role:** stop and check. It gives no name. It is reported separately from naming accuracy.

### D1. The dual-loss arm (a pre-specified secondary model)

- **What:** the recurrent head trained on the SAME frozen bank and split as the primary. The loss has three terms:
  - the level cross-entropy;
  - the alphabet-consistency term at lambda = 1.0. It was the only lambda that raised L6 recall on all three
    seeds (+11 to +13 points to 67-72 %), with film naming unchanged and false L6 up 0.23 points
    (`results/ALPHABET_LOSS.md`);
  - a spine-level transitional head: pooled recurrent state, sigmoid, binary cross-entropy weighted by the
    inverse subtype frequency.
- **How it is scored:** on M1 and F1 exactly as above, beside the primary.
- **It never replaces the primary configuration of §4**, whichever scores higher.

### What had been seen for these three

These are development measurements, and none is on a G3 test person:

- `results/COUPLING.md`, real C-ArmLSpine frames, detector confidence 0.74, whole frame. The disagreement /
  stop signal fired on 4 of 5 frames with a coupled error and on 17 of 225 fully correct frames. Unflagged
  coupled accuracy was 921 of 922 bodies.
- `results/ALPHABET_LOSS.md`, as quoted above.
- The three real C-ArmLSpine L6 patients remain excluded from the primary analysis (§4) and from M1 and F1.

---

## 13. Added before unblinding: accuracy when SchwingNet accepts, against 97.6 %

Added 2026-09-23 by a new commit to this file, as §9 requires. The commit time governs. **Nothing in §3-§5,
§11 or §12 changes.** At this commit `results/fig6/` held only the COBRA export list and a name remap, and no
SchwingNet model had run on a G3 test person.

**Why.** Greg asked for an operating point that exceeds LevelCheck's 97 %. §7 shows that overall accuracy cannot
show this at any feasible n. What can be tested honestly is **selective**: SchwingNet names the levels only when
it accepts a frame, and otherwise hands the frame back to the surgeon. **These are not the same quantity as
LevelCheck's 97.6 %.** LevelCheck's figure covers every frame with no abstention. The manuscript must print
coverage beside every accepted-accuracy number and must say this in words.

### S1. Accepted-person accuracy

- **Accept** a person's §4 scored frame when all four hold:
  - it is anchored;
  - the F1 rules (a) and (b) of §12 do not fire;
  - every named body's coupled posterior margin is at or above tau_s;
  - the frame is §4-eligible.
  Otherwise the person is **referred**.
- **tau_s is fixed on the G3 VALIDATION persons only.** It is the loosest margin (the one with the largest
  validation coverage) whose validation accepted-person accuracy is at least 0.995. If no margin reaches that,
  the strictest margin is used. It is written with its SHA-256 into `results/fig6/frozen/tau_s.json` before any
  test person is scored.
- **Population:** every G3 test person with real frames (COBRA and C-ArmLSpine). Ordinary and transitional
  persons are pooled. The three real C-ArmLSpine L6 patients are excluded, as in §4.
- **Primary test of S1:** accepted-person accuracy, one-sided exact binomial against p0 = 0.976, alpha 0.025.
  p0 is Manbachi 2018: a 2.4 % error with LevelCheck, from §2. The test is run only if the number of accepted
  persons is at least n_min = 152. Otherwise S1 is descriptive.
- **Reported beside it, always:**
  - coverage: accepted / all, with a Wilson interval;
  - the same test against p0 = 0.97;
  - the transitional persons alone: accepted accuracy, how many were referred, and the **confidently wrong**
    count (accepted but wrong). The confidently wrong count is the dangerous error, and it is printed as its own
    number.
- **Power, fixed now** (unit = accepted person, one-sided exact binomial, alpha 0.025, p0 = 0.976). Exact-test
  power is sawtoothed in n. Each entry is the first n with 80 % power, then the n from which 80 % power always
  holds:

  | true accuracy of accepted persons | 80 % power at n | 90 % power at n |
  |---|---|---|
  | 0.999 | 152 (always from 230) | 230 |
  | 0.995 | 299 (always from 363) | 424 |
  | 0.990 | 708 (always from 763) | 922 (always from 974) |

  Power is 0 below n = 152 at any true accuracy. Against p0 = 0.97, the 80 % first-n values are 122, 239 and
  386.

### F1b. A second pre-specified flag operating point

- tau for F1(c) is also fixed on validation at **at least 97 % validation sensitivity**.
- It is reported beside the 95 % operating point of §12, with its test sensitivity and specificity.
- Neither operating point is chosen on test persons.

---

## 14. Added before unblinding: an automated reference standard, calibrated on reader truth

Added 2026-09-24 by a new commit to this file, as §9 requires. The commit time governs. At this commit
`results/fig6/` held only the COBRA export list, the TS12 name remap and a detector lineage file, and no
SchwingNet model had run on a G3 test person.

**Why.** Greg, 2026-09-24: get the best number possible without a human read. §4 required a human to verify every
real-frame test person whose truth comes from SPINEPS+VERIDAH. That remains the preferred reference. This section
adds a pre-specified automated reference that can be used when no human read exists, with its error rate measured
and reported, as is done with an imperfect reference standard.

### R1. The readers (independent where possible)

- **A.** SPINEPS+VERIDAH, read only through the ctd names, behind the `tools/spineps_ids.py` guard (no raw ids,
  no out-of-order names, no T12 skip).
- **B.** TotalSegmentator: bodies and ribs, counted geometrically. Its level names are not used.
- **C.** A direct CT count: bone outside every TotalSegmentator label except the ribs, traced to rib-vertebra
  contact, as in `SchwingNet/results/spineps_ids/TS12_VERIFY.md`. Rib-bearing and rib-free bodies are counted
  down to the sacrum.
- **D (COBRA only).** The same readers run on the case's planning CT and on its CBCT. Agreement across the two
  acquisitions of one patient is a further check.

### R2. The consensus rule, chosen on CALIBRATION data only

- **Calibration sets.** Both are human-read:
  - CTSpinoPelvic1K: 802 CTs. Two-reader truth, `docs/castellvi_consensus.csv` and the release L6 ids.
  - VerSe: Loffler 2021 two-neuroradiologist consensus read.
  G3 test persons of these corpora are excluded from calibration, so no test person tunes the rule.
- **Candidate rules:** unanimity of A, B and C; 2 of 3; and latent-class (Dawid-Skene) posteriors. The last
  estimates each reader's accuracy without truth and is checked against the reader truth.
- **Rule selection.** The chosen rule is the one with the highest calibration coverage whose per-subtype PPV
  (L6, T13, sacralised/four-lumbar, ordinary) has a Wilson lower bound of at least 0.90.
- **Freezing.** The rule, and its calibration PPV, sensitivity and coverage per subtype with intervals, are written
  to `results/fig6/frozen/auto_reference.json` with its SHA-256 BEFORE any test person is scored.

### R3. How it is used

- **Human-verified truth** (§4) remains primary wherever it exists.
- **A person with no human read** enters the primary analysis only if the frozen rule assigns a subtype and every
  lumbar name. Otherwise the person is excluded, and the reason is counted in the flow diagram.
- **Every result that rests on automated truth:**
  - is labelled "automated reference (calibrated PPV …)";
  - is reported twice: once on the unanimous subset and once on the rule's full subset;
  - carries the calibration error bound. A reference with PPV p can depress measured accuracy by at most 1 - p,
    and the text says so.
- **If a human later reads these persons,** both analyses are reported (§9).

---

## 15. Added before unblinding: the detector for the primary analysis

Added 2026-09-24 by a new commit to this file, as §9 requires. The commit time governs. At this commit, no
SchwingNet model had run on a G3 test person. The Figure 6 evaluation jobs were HELD (JobHeldUser), and
`/rs/.../data/fig6/unblinding/` was empty.

**What §4 left open.** §4 fixes the confidence (0.74), the whole frame and the coupled call. It does not fix which
detector boxes the bodies and anchors the sacrum. `slurm/fig6_eval.sh` had chosen the device-held-out ("LODO")
detectors: `rx_lodo_cobra_elekta_1024` for COBRA2026 and `rx_lodo_carmlspine_1024` for C-ArmLSpine. Each had never
seen the device it scores.

**Why that choice cannot test naming.** Development measurements, all on persons seen before §4 was written (§8
item 4) and none on a G3 test person (`SchwingNet/REVIEW2_STATS.md`; `results/stats_review2/recompute.json`
S11, S12):

- The LODO sacrum anchor found the sacrum on **21 of 609 COBRA2026 frames (3.4 %)**. 19 of 27 patients had no
  anchored frame.
- On ordinary C-ArmLSpine frames, the §4 endpoint held on 162 of 284 frames. **Naming failed on 1.** The
  remaining failures were anchoring (55) and unboxed bodies (66).

With those detectors, H1 and H2 would be decided by device transfer of the detector, whatever the naming. Figure 5
already measures device transfer: in-domain frames are required.

**Change (old -> new).**

- **Primary detector for T2 and T3.** Old: the LODO detectors named above. New: **one detector trained on the G3
  TRAIN side of every device and corpus**, with the vertebra and sacrum classes. It is trained on real frames and
  styled renders of TRAIN persons only, with checkpoint selection on the G3 VALIDATION side. Its lineage is
  recorded in the model registry and checked by `tools/eval_gate.py` against every test person before scoring.
- **Configuration details.** Its path, sha256 and training lists, and whether the keypoint body detector
  `detect_v5z_final` is kept for body boxes, are written into the G5 manifest and committed before unblinding.
- **Unchanged:** confidence 0.74, the whole frame, the coupled call, and everything else in §3-§5 and §11-§14.
- **The LODO detectors become a pre-specified SECONDARY analysis,** "detector never saw this device". It is
  reported beside the primary, with the §4 endpoint unchanged.

**What the manuscript must say.** The primary analysis is **patient**-held-out, and the detector has seen the
device. The LODO result is the device-transfer number, and the text says which is which.
