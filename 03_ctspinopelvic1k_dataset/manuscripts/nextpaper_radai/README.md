# Radiology: Artificial Intelligence submission — working notes

Target: RSNA *Radiology: Artificial Intelligence*, Original Research. Submission is through
Manuscript Central (https://mc.manuscriptcentral.com/rad-ai). The journal's own author pages
(https://pubs.rsna.org/page/ai/author-instructions and .../checklist) refuse automated
fetches, so the limits below come from the RSNA family instructions and the journal's public
summary. **Verify each number against the live checklist before submission** (open the two
pages in a browser; ten minutes).

| item | requirement as gathered 2026-09-08 |
|---|---|
| article type | Original Research (hypothesis-driven, statistics required) |
| main text | ≤ 3,000 words, Introduction to Discussion (Conclusion inside Discussion) |
| abstract | structured, ≤ 250 words (some RSNA pages say 300): Purpose / Materials and Methods / Results / Conclusion; M&M must state retrospective or prospective, date range, numbers, groups, procedures, statistics; Results carry the numbers with P values |
| summary statement | one sentence |
| key points / key results | up to three, each with summary data |
| abbreviations | list, ≤ 10, each used ≥ 3 times |
| figures and tables | only what the text needs; RSNA's usual ceiling is six figures and four tables; each figure legend after its figure in one figures document |
| references | RSNA style (numbered, order of citation); keep under ~40 |
| reporting checklist | CLAIM 2024 (Tejani et al., Radiology: AI 2024) filled and uploaded; STARD elements where diagnostic accuracy is claimed |
| blinding | manuscript file anonymized (abbreviated title page without authors; acknowledgments anonymized); full title page separate |
| statements | IRB / HPR determination (we have "Not Human Subjects Research" determinations, 2026_269 and the public-datasets determination), data sharing statement (Zenodo DOI, HF), code availability (GitHub), funding, conflicts, AI-tool disclosure |
| file formats | Word or PDF for review; LaTeX is not the house format, so `main.tex` here is built to Word-like structure and can be converted with pandoc (`pandoc main.tex -o main.docx --bibliography=refs.bib`) |
| units and style | SI units; P values two decimals (three when < .01); no "significant" without a test; abbreviations defined at first use; patients not "cases" |

Layout of this folder: `main.tex` (the anonymized manuscript in RSNA order), `title_page.tex`
(authors, affiliations, funding, statements), `claim_checklist.md` (to fill), `refs.bib`
(shared with the NeurIPS draft; copy `../AR/bib/references.bib` and prune), `figs/`.

Framing for this venue: a diagnostic-accuracy paper, not a benchmark paper. The question is
whether a segmentation network trained on transitional anatomy, plus a sequence decoder,
reports the rib-free lumbar count and the lumbosacral transitional status correctly on CT,
against radiologist consensus, and how the public alternatives fare on the same scans. The
dataset and the sequence decoder are Materials and Methods, not the contribution.
