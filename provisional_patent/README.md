# provisional_patent — the SchwingNet provisional and invention-disclosure materials

Every patent document for the level-identification work (SchwingNet) that was on Greg's laptop on 2026-10-20, in one
place so any of his sessions can read it. **Not legal advice.** As far as these files show, nothing has been filed: the
provisional packet says it is not filed until counsel has reviewed it, and the WSU disclosure package of 25 September
2026 was signed and zipped that day with a cover e-mail drafted (`07_cover_email_draft.md`). Whether and when it was
sent is not recorded here. Ask the office before relying on any of this.

## Who can read this, and what it holds

This repository is **internal**, not private: Greg and one outside collaborator can read every branch. Greg chose on
2026-10-20 to keep all of this material here anyway, the confidential parts included. Two items carry a restriction of
their own:

- `DISCLOSURE_MEMO.md` is marked "for patent counsel only, attorney work product".
- `wsu_tto/TTO_package_2026-09-25/02_CONFIDENTIAL_Part_B_manuscript_Radiology_AI.pdf` and its revisions in `followup/`
  are the **unpublished** Part B manuscript, held from submission pending the office's advice. It is the first
  disclosure of Part B.

Nothing in this folder goes to a public repository, the website, a Hugging Face Space, a student project or a talk. The
root `.gitignore` keeps any folder named `private_ip/` out of git; this folder is the deliberate exception, under
another name.

## Which packet is the current one

| What | Date | Where |
|---|---|---|
| **Provisional application packet**: specification, claims, cover-sheet data, filing checklist | 18 Sep 2026 | `provisional/` |
| Invention disclosure for the office and counsel, and the counsel memorandum it travels with | 18 Sep 2026 | `INVENTION_DISCLOSURE.md`, `DISCLOSURE_MEMO.md` |
| WSU invention disclosure package (signed form, Part B manuscript, papers, slides, timeline) | 25 Sep 2026 | `wsu_tto/TTO_package_2026-09-25/` |
| Plan for scrubbing public disclosures of Parts A and B from git, and the GitHub purge requests | 26 Sep 2026 | `wsu_tto/TTO_package_2026-09-25/SCRUB_PLAN.md`, `wsu_tto/github_purge_requests/` |

`provisional/` is the only provisional draft on the laptop. `spinesurg-ct-nnunet/docs/provisional.zip` (zipped
2026-10-19) holds the same five files.

The two disclosures frame the invention differently, and the provisional follows the earlier one:

- **18 Sep** (`provisional/`, `INVENTION_DISCLOSURE.md`): naming vertebrae on limited-field projection images by
  linking overlapping exposures into a patient-specific chain, and commanding where the C-arm moves next.
- **25 Sep** (the WSU form): Part A, a segmenter-agnostic classifier that flags transitional vertebrae on preoperative
  CT; and Part B, a network that names levels from a single intraoperative C-arm exposure without registration.

No provisional draft written after 25 September was found on this computer.

## Contents

| Path | What it is |
|---|---|
| `provisional/README.md` | The packet: what each file is, what is built and what is only described, reading order for counsel |
| `provisional/SPECIFICATION.md` | The technical disclosure, written to enable; FIG. 1–13 are described but not drawn |
| `provisional/CLAIMS.md` | What will be claimed at twelve months, each limitation pointed at its support; not filed |
| `provisional/COVER_SHEET.md` | Data for form PTO/SB/16 (residence, address and entity status left for counsel) |
| `provisional/FILING_CHECKLIST.md` | What must happen, in order |
| `INVENTION_DISCLOSURE.md` | The invention for the office and counsel: aspects, claim scope, §101 strategy, freedom to operate |
| `DISCLOSURE_MEMO.md` | Counsel only: publication timing and prior public availability, element by element |
| `PATENT_PACKAGE.md` | Superseded by the two above; kept for the three corrections it records |
| `GUIDED_ACQUISITION.md` | The closed-loop acquisition as built and measured; the specification cites it |
| `research_patent_2026-09-18.json` | The research run on what a US academic inventor must do, in what order and by when |
| `tools/disclosure_audit.py` | Re-runs the check of what is publicly reachable, anonymously and with timestamps; run before any submission, talk or release |
| `wsu_tto/TTO_package_2026-09-25/` | The package for the WSU Office for Technology Commercialization, items 00–06; `00_README_for_TTO.md` lists them |
| `wsu_tto/TTO_package_2026-09-25/followup/` | Part B manuscript revisions 2–5 and the CNS 2026 talk drafts (7 Sep draft, v2–v10) |
| `wsu_tto/idf_work/` | The scripts that filled the WSU form, and the form's unpacked Word XML |
| `wsu_tto/*.docx` | The modified blank form, and the completed form of 25 Sep (identical to item 01's .docx) |
| `wsu_tto/github_purge_requests/` | The three GitHub Support requests and the commit lists they attach |
| `wsu_patent_policy.pdf` | The WSU patent policy |

Paths such as `tools/sweep_map.py` and `tests/test_acquisition.py` in the packet are in **spinesurg-ct-nnunet**, the
repository the packet was written in. That code is not copied here.

## Changes from the originals

- In `wsu_tto/TTO_package_2026-09-25/SCRUB_PLAN.md` and `scrub_hits.json`, four students' GitHub names are replaced by
  `[student A]` to `[student D]`, the same letter for the same person. Nothing else in either file changed. The scrub
  plan says one of them wrote the DRR code, which bears on inventorship if a claim covers it; counsel should read the
  original for the name.
- The Word, PowerPoint and PDF files are unchanged. The CNS talk drafts and the Part B manuscript PDFs carry author or
  acknowledgement lists that name students.

## Left out

- `TTO_package_2026-09-25.zip`: its ten files are byte-identical to the folder's, and the root `.gitignore` refuses
  `*.zip`.
- `Neurocheck Provisional approval.zip` on the Desktop: a separate application of February 2025, for a different
  invention.
- `spinesurg-ct-nnunet/tools/fluorocap_patents.py`: a FluoroCap tool that harvests figures from published patents as
  fluoroscopy images. Only its name matched.

## Where the originals are

- `C:\Users\grego\OneDrive\Desktop\private_ip\`, copied into `wsu_tto/` here.
- `spinesurg-ct-nnunet/docs/` (the packet, the disclosure, the memo, the research run) and `tools/disclosure_audit.py`.
  The packet and the disclosure are committed there in b063b3c, df26da0 and 19d8dbf.
- `/rs/rs_grp_oschome/go2432/private_ip/git_bundles_2026-09-26/` on the grid: the git bundles kept as conception
  evidence before any history rewrite (sha256 verified 26 Sep 2026).
