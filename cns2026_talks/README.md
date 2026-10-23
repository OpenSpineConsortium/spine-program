# cns2026_talks: Greg's two CNS 2026 talks and what they were built from

Issue #224. Copied on 2026-10-23 from the laptop folders that each talk's `MANIFEST_LOCAL.md` names, file by file, with
the md5 of every source. Like `provisional_patent/`, this folder is Greg's: no issue is cut from it, and nothing in it
goes to a public repository, the website or a Space. The two decks in the table below are the only files here meant to
be shown, and only at their sessions.

## The deck to show at each talk

| Talk | Session (from the deck's title slide) | Deck to show |
| --- | --- | --- |
| Characterizing the Transcriptomic Recurrence Signature of Glioblastoma Following Laser Interstitial Thermal Therapy (Abstract 418) | SSTU02, Sunrise Science Session, Tumor 2; Monday 2 November 2026, 7:00 to 7:06 AM; Room 147B | `litt_abstract418/SLIDES/CNS2026_Schwing_Abstract418_CNStemplate_v6.pptx`, 54 slides: 29 in the talk, of which a marked 6-minute core of 14, and 25 backups (`litt_abstract418/SLIDES/STORY_v6.md`) |
| Not All Spines Are Created Equal: A Single-Shot CT Segmentation Model For Preoperative Detection Of Lumbar And Thoracic End Anomalies | MP4SP1, Mini Podium 4, Spine Session 1; Monday 2 November 2026, 5:21 to 6:00 PM; Podium 4, Ballroom ABC | `spine_not_all_spines/decks/CNS2026_Schwing_NotAllSpines_public_v12.pptx`, 17 slides, the disclosure-safe cut (CLAUDE.md rule 8) |

**Spine talk: show only v12.** Every other spine deck here shows the C-arm work, the sweep, or both, which the WSU
invention disclosure covers (`provisional_patent/README.md`); so do the SchwingNet figures and results under
`spine_not_all_spines/spinesurg-ct-nnunet/` and the sweep results under `spine_not_all_spines/model_night/`. Treat all
of it as `provisional_patent/` is treated. `CNS2026_Schwing_NotAllSpines_public_v11.pptx` (15 slides) is the earlier
disclosure-safe cut, superseded by v12. Five decks are byte-identical to the copies the technology-transfer follow-up
already holds, so git stores each once:

| Deck here | The same file in `provisional_patent/wsu_tto/TTO_package_2026-09-25/followup/` |
| --- | --- |
| `CNS2026_Schwing_LSTV.pptx` (7 Sep draft, 17 slides) | `CNS2026_spine_talk_DRAFT_deck_2026-09-07_not_presented.pptx` |
| `CNS2026_Schwing_Spine_v2.pptx` (21 slides) | `CNS2026_spine_talk_v2_2026-09-25_results_only.pptx` |
| `CNS2026_Schwing_SchwingNet.pptx` (v3, 21 slides) | `CNS2026_spine_talk_v3_2026-09-25_SchwingNet_results_only.pptx` |
| `CNS2026_Schwing_SchwingNet_CNStemplate_v9.pptx` (21 slides) | `CNS2026_spine_talk_v9_2026-09-26_CNS_template_ACCME.pptx` |
| `CNS2026_Schwing_SchwingNet_CNStemplate_v10.pptx` (21 slides) | `CNS2026_spine_talk_v10_2026-09-26_CNS_template_ACCME.pptx` |

**LITT talk: the contralateral slides stay conditional.** Migration in life and carry-over at dissection cannot be
separated by this design, so the instrument sentence stays in the conditional (`litt_abstract418/SLIDES/STORY_v6.md`,
Greg's instruction 4). The manuscript material under `litt_abstract418/MBR/` (the supplement `ESM_1.xlsx` and the
manuscript's figure code and panels under `nature_draft/figures/`) was untracked in the study's public repository; keep
it out of public view until the manuscript is published.

## Layout

Each talk folder mirrors the tree its scripts were written against, so their relative paths find their inputs here.

- `litt_abstract418/` stands for the root of the U251 study (public repository
  `Gregory-Schwing-MD-PhD/u251-xenograft-rat-RNASeq-study`, branch `research-letter-expansion`):
  - `SLIDES/`: every deck version, the scripts that built them, `figures/` and `figures_cns/` (with `v5_data/`, byte
    copies of the grid outputs the decks' numbers come from, and `v6/`, the single panels), the plans `STORY_v4.md`,
    `STORY_v5.md`, `STORY_v6.md` and `ABSTRACT_VS_TALK.md`, and the CNS speaker template.
  - `ANALYSIS/`: the pipeline tables and reports the figure scripts read (GSEA, RUVSeq, decontamination, host, drug
    rematch, leave-one-out, counts, metadata).
  - `MBR/`, `depmap/`, `manuscript/`, `ASSETS/`: the supplement, the manuscript figure code, the DepMap U-251 MG rows,
    the drug tables and the visual abstract.
  - `abstract/`: the abstract with Tavarekere Nagaraja's edits; `Ablation video_TNN_18Sept26.pptx`, the one-slide deck
    whose 64 x 64 px intra-MRI clip `SLIDES/04_make_cns_figures.py` re-encodes at 512 px for the slides.
- `spine_not_all_spines/` stands for the laptop Desktop:
  - `CTSpinoPelvic1K/paper/cns2026/`: the generators `make_cns_deck*.py`, the figure scripts `prep_*.py`, and the figure
    folders `figs/`, `figs_v2/`, `figs_cited/` (the cited figures, digitised values and the article pages they came
    from) and `figs_public/` (the v11 and v12 charts and `public_numbers.json`).
  - `CTSpinoPelvic1K/`: the NeurIPS camera-ready PDF the public decks assert their numbers against, the CNS speaker
    template, and the ACCME guidelines the CNS-template decks were built to.
  - `spinesurg-ct-nnunet/`: the SchwingNet figures, result files, tables, `NUMBERS.md`, `LEVELCHECK_MODEL.md`, the
    figure tool `tools/fig_power.py`, and the evidence documents of `docs/` (wrong-level cost, wrong-site burden, the
    census table).
  - `model_night/sweep_v3/`: the three sweep results the per-level sweep chart reads.
  - `decks/`: every deck version that was on the Desktop.

## Rebuilding

Nothing was rerun on 2026-10-23; the copy was checked by name and md5 (`MANIFEST_LOCAL.md`).

- **LITT**, from `litt_abstract418/` (the order of `SLIDES/16_build_deck_v6.py`):

  ```
  python SLIDES/13_v5_figures.py
  python SLIDES/15_slide_panels.py
  python SLIDES/09_build_deck_v4.py     # only if the v4 deck is missing
  python SLIDES/16_build_deck_v6.py
  ```

- **Spine, v12**, from `spine_not_all_spines/CTSpinoPelvic1K/paper/cns2026/`: `python prep_v16_public_figs.py`, then
  `python make_cns_deck_v12_public.py`. The generators write their deck to the Desktop path typed in each script, not
  into this folder. `sweep_per_level.py` reads the sweep results from a laptop path; pass `--arm name=<path>` with the
  files under `model_night/sweep_v3/`. `prep_v12_figs.py` and `prep_v14_figs.py` also read two arrays that are not here
  (`.npz`, kept out by `.gitignore`; their laptop paths are in the manifest).
- To check a rebuilt deck, render its slides with PowerPoint (COM export to PNG) and look at them; LibreOffice is not
  installed on the laptop.

## Personal data (CLAUDE.md rule 12)

- **Student names.** The ten student annotators named on the spine acknowledgment slide are replaced by `[student A]` to
  `[student J]` in the 12 generator scripts that type them. The seven spine deck binaries keep that slide as it was
  built, as `provisional_patent/` keeps its decks (PR #212), and the camera-ready PDF keeps its author list (the record
  of authorship).
- **Researcher e-mail addresses.** Five addresses are replaced by `[withheld e-mail]`: in three saved journal article
  pages under `figs_cited/`, in the tracked-change record of the abstract, and in the supplement spreadsheet. Role
  mailboxes and Greg's own institutional addresses stay.
- **Patient identifiers.** The DepMap model table was left out, because it prints the cell-line donors' patient IDs.
  The SchwingNet and sweep result files were checked for patient header fields and for path strings, and carry only
  pseudonymous case labels of the public collections.

Each manifest counts these edits by kind and marks every edited file.
