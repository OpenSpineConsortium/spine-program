# Talks kept here, and the deck lineage

One deck is copied: `TechFair_LSTV_Schwing.pptx` (2,861,510 B; 15 slides; file dated 2026-07-24), "Harnessing
Algorithmic Disagreement for Automated Lumbosacral Transitional Vertebrae Detection", presented at the 43rd AACA meeting,
Mayo Clinic, 13 June 2026 (`../../docs/handoff/GREG_ONLY_SECTION_EXTRACTS.md` section 14). It was built from third-party
segmenters (TotalSegmentator, SPINEPS / VERIDAH) and discloses neither Part A nor Part B of the invention disclosure. Its
title slide says "Department of Neurosurgery" and "NIH F30 Fellow": historical, and wrong under the standing rule (the
affiliation is General Surgery, Wayne State University School of Medicine / Detroit Medical Center). Nothing is reused
from it without that correction. Two byte-identical twins existed on 2026-10-08 (`../../MANIFEST_LOCAL.md` section 2.1).

## The CNS 2026 deck lineage (all superseded members by path; `../../MANIFEST_LOCAL.md` section 2.2)

From `../../_plan/inventories/desktop_root_loose_files.md`, section "The CNS 2026 deck lineage"; the same decks sat under descriptive names in Greg's private TTO follow-up
package, matched by byte size.

| deck | date | slides | state | where |
|---|---|---|---|---|
| `CNS2026_Schwing_LSTV.pptx` | 2026-09-07 | 17 | draft, not presented; the only deck framed on the dataset rather than the detector | copied into `03_ctspinopelvic1k_dataset/manuscripts/talks/cns2026/` |
| `CNS2026_Schwing_Spine_v2.pptx` | 2026-09-25 | 21 | v2 "results only"; superseded by v10 and v12 | by path |
| `CNS2026_Schwing_SchwingNet.pptx` | 2026-09-25 | 21 | v3 "SchwingNet results only", before the CNS template; superseded by v10; discloses Part B; private | by path |
| `CNS2026_Schwing_SchwingNet_CNStemplate_v9.pptx` | 2026-09-25 | 21 | v9 on the CNS ACCME template; superseded by v10; private | by path |
| `CNS2026_Schwing_SchwingNet_CNStemplate_v10.pptx` (= `_CNStemplate.pptx`, md5 aa8df26fb2) | 2026-09-26 | 21 | the full private deck; discloses Part B and the unfiled sweep; never shown publicly | copied into `01_carm_level_detection/manuscripts/talks/` |
| `CNS2026_Schwing_NotAllSpines_public_v11.pptx` | 2026-09-26 | 15 | superseded the same day by v12 | by path |
| `CNS2026_Schwing_NotAllSpines_public_v12.pptx` | 2026-09-26 | 17 | the current disclosure-safe deck, CT side only; title slide reads General Surgery | copied into 03 |

The generators (`paper/cns2026/` in CTSpinoPelvic1K) are excluded from git since 45df97d and must never be pushed; they are
copied into 03. Whether the slides were submitted to the meeting, and by what deadline, is not recorded
(`../../docs/handoff/OPEN_QUESTIONS.md` A23). Deck rules: `../../memory/cns-deck-v2-2026-09-25.md`.

## Two clinical teaching decks, by path

`GREG_PRES.pptx` (6 slides, lumbar spinal stenosis, 2025-06-20) and `SPINAL_AVM.pptx` (8 slides, spinal arteriovenous
malformation, 2025-06-20) are clinical teaching, not research; `../../MANIFEST_LOCAL.md` section 2.2 records their paths.
The August 2026 MANS teaching talk's outlines are in `../../docs/mans_talk/`; its 12 MB deck is by path.
