# Disclosure timeline — transitional-vertebra detection and level naming (G. J. Schwing)

All dates 2026 unless stated. "Public" = accessible to persons outside the research group without a confidentiality
obligation. Items that disclose Part A's name-free classifier or Part B (the C-arm level-naming network) are marked; none do.

| Date | Event | What became public | Discloses Part A / Part B? |
|---|---|---|---|
| 18 Apr | Work begins (first repository commit; TCIA CT Colonography download scripts) | nothing | — |
| 25 Apr – 3 May | April release of the CTSpinoPelvic1K CT dataset on a Hugging Face mirror (anonymous, for the NeurIPS submission); training of the merge-based segmenter from 3 May | dataset (anonymous repository) | no |
| 31 May | End of NIH F30GM147909 support; MD/PhD conferred | — | — |
| Sat 13 Jun | AACA 43rd annual meeting Tech Fair, Mayo Clinic, Rochester MN: "Harnessing Algorithmic Disagreement for Automated Lumbosacral Transitional Vertebrae Detection" — presentation and hands-on demonstration; slides in this package (05) | a separate, earlier LSTV screening pipeline assembled from third-party open-source segmenters (TotalSpineSeg, SPINEPS/VERIDAH) whose level disagreement flags the phenotype, with Castellvi heuristics; open source | no (a separate project; neither claim relies on it) |
| 1 Jul | Graduate Medical Education Agreement with Detroit Medical Center takes effect (no intellectual-property clause) | — | — |
| ~Jul | NeurIPS 2026 E&D submission 3474 under double-blind review (reviews dated 21 Jul); OpenReview page not public until decision | — | — |
| 24 Aug | Conception of Part B (level naming from local morphology on a single C-arm exposure) — dated repository record | nothing | — |
| 7 Sep | Zenodo release v10 of CTSpinoPelvic1K (public, DOI 10.5281/zenodo.22642578) | dataset, label scheme, quality-control tables | no |
| 18 Sep | Zenodo release v11 (public, DOI 10.5281/zenodo.22797014) | as above, with corrections | no |
| 19 Sep | arXiv 2609.22760: dataset article "CTSpinoPelvic1K: spine, pelvis, ribs and femora in one coordinate frame…" (submitted to Medical Physics) | dataset description | no |
| 21–23 Sep | Per-device image-formation models fitted (Part B component) — repository record | nothing | — |
| 24 Sep | NeurIPS 2026 decision: Accept (poster); OpenReview page public (title, abstract, reviews, camera-ready when uploaded) | audit of TotalSegmentator's one-level label shift; dataset; merge-based segmenter with released weights | no |
| 25 Sep | This disclosure; Part B manuscript complete and HELD pending the office's advice | — | — |

## Planned / upcoming

| Date | Event | Content | Action |
|---|---|---|---|
| on advice | Submission of the Part B manuscript to Radiology: Artificial Intelligence (item 02) | **first disclosure of Part B** | held until the office advises; a provisional application before submission preserves ex-U.S. rights |
| ~early Nov | NeurIPS 2026 proceedings online (about one month before the 6–12 Dec conference) | camera-ready of item 03 | as already disclosed on 24 Sep |
| 2 Nov | CNS 2026 annual meeting, Washington DC: mini-oral "Not All Spines Are Created Equal" (single-shot CT detection of count anomalies); slides not yet submitted | CT-side count-anomaly detection; not Part A's classifier, not Part B | slides can be scoped to already-public content |
| Oct–Nov | Medical Physics dataset article under review; camera-ready of the NeurIPS paper cites Zenodo v11 | dataset | no method of this disclosure |

## Where the dated records are

Version-controlled repositories with commit timestamps (spinesurg-ct-nnunet, private; CTSpinoPelvic1K and OpenSpineToolkit,
public), the WSU Grid job records and model registry, Zenodo deposit metadata, the inventor's dated laboratory journal, and
the manuscripts' result ledgers. Any of these can be produced on request.
