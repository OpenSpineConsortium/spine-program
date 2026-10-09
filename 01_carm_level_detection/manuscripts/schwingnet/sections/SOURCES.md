# Sources for `introduction.tex` and `discussion_motivation.tex`

> **2026-09-23, six-figure wrap.** `introduction.tex` and `discussion_motivation.tex` were rewritten around the six
> figures. New literature in them: Peh 1999 (`peh1999`, 77.9-82.2 %) and Yun 2018 (`yun2018`, 31 of 100), both from
> `SchwingNet/LEVELCHECK_MODEL.md` §2 and added to `SchwingNet/refs.bib` from PubMed E-utilities; the LevelCheck
> paragraph of the Discussion follows `LEVELCHECK_MODEL.md` §1, §2 and §6-§7 and `CLAIMS_LEDGER.md` §8. Dropped:
> DeepDRR, SyntheX, Killeen 2025, PolyPose and the corpus/device-term comparisons (the formation claim moved to the
> supplement). The paragraph-by-paragraph trace below is of the 2026-09-22 text and is kept for the sentences that
> survived (the count, wrong-level rates, Konin, Sabri, Nakagawa, LevelCheck 100 % / 97.6 %, VDVM, Huang, Rao,
> VERIDAH).


> **2026-09-24, re-wrap.** Introduction: the Yun 2018 clause was cut for length (it stays in Table 3). Discussion:
> the Peh 1999 and Nakagawa 2017 numbers are cited without the numbers (both stay in the Introduction or Table 3);
> the VERIDAH anomalous-recall sentence (96.3 % to 25.9 %) was cut for length; the Rao 2024 comparison is shortened
> to "class-agnostic and in-pool"; the second paragraph adds the fused-L5 caveat and the contested never-seen L6
> (`CLAIMS_LEDGER.md` §8 row 2); the third says 97.6 % is "reported beside an interval, not beaten". No new
> literature.

Every paragraph below was distilled from files already in the repository. No new literature was searched.
Paths are relative to `spinesurg-ct-nnunet:` unless stated; line ranges
are as of 2026-09-22. Every `\citep` key is copied verbatim from `paper/rsnai/refs.bib` into `refs_used.bib`
by `extract_refs.py` (scratchpad), which fails if a key is absent.

## introduction.tex

### Paragraph 1 — the count, and wrong-level surgery as a never event
- `paper/rsnai/main_v2.tex` 56 (opening sentence "A vertebral level is not marked; it is counted"; the
  count up from the sacrum or down from C2; Mody, Furuya, Dablouk, Ammerman figures).
- `paper/rsnai/main.tex` 101–116 (never-event framing; survey and registry rates).
- `paper/focused/main.tex` 142–158 and `paper/focused/_drafts/clinical.tex` 84–100 (the standard technique;
  three or four bodies per field).
- `paper/qi_universal_protocol/main.tex` 67–86 (the Universal Protocol verifies a mark; a level has none).
- `docs/WRONG_LEVEL_AND_TRANSITIONAL.md` 9–12 ("It is common").

### Paragraph 2 — why counting from a landmark on a limited field fails
- `paper/rsnai/main.tex` 126–136 (a count to a mid-thoracic level passes through several exposures, each
  joinable one body off; a transitional vertebra shifts the count for the whole column) and 163–167
  (adjacent vertebrae resemble one another; the separating cue is position in a chain whose end is known).
- `paper/focused/main.tex` 182–188; `paper/focused/_drafts/clinical.tex` 126–137;
  `paper/qi_universal_protocol/main.tex` 134–147 (the images supply the failure modes).
- `CTSpinoPelvic1K:paper/mpda/main.tex` 246–263 (transitional variants
  change the count at both borders; the gold standard is whole-spine imaging counted from C2; no
  spine-limited acquisition supplies the count) and 307–319 (counting distinguishes neither phenotype).
- `docs/WRONG_LEVEL_AND_TRANSITIONAL.md` 13–18 (Konin and Walz: counting from the sacrum names a different
  vertebra than counting from C2).
- `paper/rsnai/graveyard.tex` 418 (Sabri 2025: 8.8 % of 3,147 full-length radiographs lacked 24 presacral
  segments) and 447 (Liebrand 2026: the systematic review's remedy is whole-spine radiography).
- `docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` 27–33 (De Silva 2016: 106 of 504 radiographs excluded, 13 of
  them for a field of three or fewer levels).

### Paragraph 3 — what registration needs and therefore cannot do; access to navigation
- `paper/rsnai/main.tex` 155–161 and 429–437 (registration imports identity: a six-degree-of-freedom pose,
  the name transferred from a human's reading of the preoperative volume; unavailable without a CT; a
  miscounted CT propagates faithfully; the failure mode of a transitional spine).
- `paper/focused/_drafts/deployment.tex` 143–147; `paper/focused/_drafts/methods.tex` 123–131;
  `paper/focused/main.tex` 182–188 (the same argument in three later drafts).
- `paper/rsnai/main_v2.tex` 56–58 (navigation reads the level off a registration to an intraoperative 3-D
  scan; Dea 2016 break-even of 254 procedures; Kanmounye 2021 fluoroscopy 96.5 % against navigation 8.8 %;
  "Every hospital has the C-arm").
- `docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` 27–41 (LevelCheck lineage figures are registration success
  given a labelled CT; De Silva's 100 % is label placement given a correctly annotated CT).
- `CTSpinoPelvic1K:paper/mpda/main.tex` 280–284 (LevelCheck's labels are
  placed by hand on the CT and verified by the surgeon).

### Paragraph 4 — the gap: no published system names the level from the C-arm alone
- `paper/rsnai/main_v2.tex` 58 (VDVM 73.3 % on 31 C-arm images imports identity from a preoperative
  radiograph; Rao 2024 recalls 0.96–0.98 name nothing; Huang 2022 88.3 % on cadaver long-length
  tomosynthesis).
- `paper/focused/main.tex` 773–788 (the 22 September 2026 search: no method names vertebrae from the
  content of real intraoperative fluoroscopy above 73.3 %; Killeen 2025 Dice 0.04 on real cadaver C-arm
  frames; per-body recall compounds and is not a quantity the field reports).
- `paper/rsnai/graveyard.tex` 409–413 (Huang 2022 is the only registration-free naming number; every
  panoramic method imports names from elsewhere).
- `docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` 43–49 (Huang 2022 details: 13 cadavers, trained on renders
  from 297 CTs, long-length field).

### Paragraph 5 — intended use, objective and hypotheses (CLAIM items 3 and 4)
- `paper/rsnai/main_v2.tex` 38 (Purpose) and 60 ("We ask whether the navigation can be built from the
  C-arm shots alone"; the two obstacles measured rather than assumed; the per-device parameterisation and
  the held-out-device test).
- `paper/rsnai/main_kdevices_skeleton.tex` 26–31 (Purpose: without a preoperative 3-D scan or navigation
  hardware, on C-arm models the model never saw).
- `paper/focused/_drafts/clinical.tex` 138–142 and 295–302; `paper/focused/_drafts/deployment.tex` 148–153
  (intended use: a count displayed beside the surgeon's own before incision; two counts that must agree).
- The hypothesis list follows `docs/RSNAI_PLAN.md`: the C-ArmLSpine cross-validation with CBCT truth is a
  ledger claim (plan line 184), C2 is the film-to-fluoroscopy failure, C5 is device separability, and C7 is the
  held-out-device detector, whose "counting grade" is defined there for detection (at least 97 % of sacra and
  97 % of vertebrae found); the naming hypothesis is stated without a threshold because the plan sets none.
  No result is quoted.

## discussion_motivation.tex

### Paragraph 1 — LevelCheck as a registration ceiling; what registration cannot do
- `paper/rsnai/graveyard.tex` 443 ("no two systems in this space report the same quantity"; registration
  convergence, label placement given a correct CT, questionnaire utility, detection F1 and naming accuracy
  are different measurements; the 99.998 % moves with computation budget; the 100 % is conditioned on the
  CT having been labelled correctly; the 97.6 % is five surgeons on 62 difficult films with the overlay,
  a human-plus-machine number whose right comparator is a human plus this system).
- `paper/rsnai/main.tex` 429–437 ("Why this cannot be ranked against registration").
- `paper/rsnai/main_v2.tex` 97–99 (comparison with prior art is indirect).
- `docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` 11–41 (verified Manbachi, Otake, Lo and De Silva figures).

### Paragraph 2 — the registration-free literature, and the render-to-fluoroscopy gap
- `paper/focused/main.tex` 773–788 (Rao 2024 detection is class-agnostic; VDVM imports identity by
  matching; Huang 2022 on cadaver long-length tomosynthesis; Killeen 2025 Dice 0.04; per-body recall
  compounds) and 736–748 (SyntheX: realistic simulation with strong domain randomisation and no real image
  matched CycleGAN, ADDA and real training on cadaveric hip fluoroscopy).
- `paper/rsnai/graveyard.tex` 409–413 (Huang 2022 comes from the LevelCheck laboratory; needs the multi-slot
  collimator; VDVM's reference film is what a sweep builds from the C-arm itself; none releases code or
  weights; each row states the task it performs) and 439 (what the synthetic-data literature supports).
- `docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` 43–49 (Huang 2022: about 17 vertebrae per long-length image,
  trained on 297 CTs, 13 cadavers, no CT of the test subject).
- `paper/rsnai/main_v2.tex` 60 (the design: parameterise each C-arm rather than translate images).

## Deliberately omitted
- **Pelphix (99.2 % simulated → 71.7 % cadaver).** Named in the task brief, but it has no entry in
  `paper/rsnai/refs.bib`, and `docs/FLUORO_DATASET_STRATEGY.md` 114–128 and `docs/HANDOFF_PHYSICS.md` 377–379
  withdraw the comparison: the figure is average surgical-phase recognition accuracy over four sequence
  heads on the pelvis, not detection or naming, and its agreement with a detector recall here was a
  coincidence between two different quantities. Citing it would repeat a false equivalence the project
  has already retracted.
- **This study's own numbers.** None appears in either file. They belong to the results half of the
  manuscript, so that only values passing the rigor audit (case-level interval, stated operating point, source
  file) are printed.
- **Liebrand 2026** is cited only for the remedy it proposed (whole-spine radiography); the counted-from-C2
  gold standard is attributed elsewhere in the repository to a reference that is not in `paper/rsnai/refs.bib`.
