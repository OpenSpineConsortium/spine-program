# The AIDaS packet as submitted, 2026-10-16

Written on 2026-10-18 by the thread "AIDaS final into spine-program" of the owner's claude.ai Project (issue #118), from
the final PDF the owner shared that day and from the owner's Outlook, read through the Microsoft 365 connector. It
follows `HANDOFF_2026-10-16.md`, whose "What remains" it closes in part.

## What was submitted

- **Sent** on Friday 2026-10-16 at 19:19 UTC (3:19 p.m. ET), before the call's 11:59 p.m. ET deadline, from the owner's
  WSU mailbox to aidas@wayne.edu, the PI and the Co-PI copied and a consortium member in blind copy, subject "AIDAS
  Seed Grant Submission", "On behalf of Drs. Han, Schwiebert, and Schwing", with one attachment,
  `AIDaS_SEED_2027_Proposal_Final.pdf`. No answer from the AIDaS office was in the mailbox on 2026-10-18 at 22:40 UTC.
- **The PDF** the owner shared on 2026-10-18 under the same name: 10 pages, letter, built by pdfTeX on 2026-10-16 at
  16:46 UTC (after the Co-PI's update of 15:19 UTC), 362,244 bytes, sha256
  `7c4c459c393c52bcdb01284b50259fdc96a6e56d6beb70ee29ec74fbae10a861`. The sent attachment has the same name and Graph
  reports 362,524 bytes for it, a size that counts the attachment's own metadata, so the two are taken as one file;
  the attachment itself was not downloaded.
- **Its narrative is `latex/main.tex` at 88871de** (#112): the text of its pages 1 to 6 differs from
  `AIDaS_SEED_2027_packet.pdf`, the committed draft built from that commit, only in the two contact lines of the cover,
  which the Co-PI updated in the Overleaf copy, and pages 7 to 10 are the two biosketches. So nothing in the tracked
  source changes; the PDF, the contact lines and the biosketches stay out of git (root `CLAUDE.md` rule 12,
  `.gitignore`).
- **Not recorded**: whether the disclosure audit (root `CLAUDE.md` rule 8) ran on this PDF before it was sent.

## What Elsevier's message of 2026-10-16 changes

Elsevier's data support answered on 2026-10-16 at 04:42 UTC, and the owner forwarded it to the Project on 2026-10-18.
Its value is not written here or anywhere in git: Elsevier issued WSU's institutional token, with these terms of use.

- The token is kept server-side in a password-protected environment, never in browser-side code and never in the
  address bar; it represents full access to WSU's account and may be revoked at any time without notice.
- Every request goes over HTTPS with the API key in the header `X-ELS-APIKey` and the token in `X-ELS-Insttoken`,
  never as a query parameter.
- ScienceDirect's text and data mining amendment was still not finalized: Elsevier asks to be told once it is, to
  update the key's configuration. Elsevier's account manager had written on 2026-10-15 that the amendment would reach
  the WSU Library within days for review and approval.

For the packet this means the reading `RECORD.md` section 1 and section 6 left for the owner to confirm, that the
owner's "now science direct" of 2026-10-16 meant the amendment had come through, did not hold when the packet was
sent: Scopus's text and data mining and AI rights were in place, ScienceDirect's were in process. The submitted PDF says
"under WSU's text and data mining rights" (the abstract) and "under WSU's text and data mining and AI rights from
Elsevier" (Aim 2) for both. Whether to tell the AIDaS office, or to leave it, since the amendment is expected well
before the award year begins in January 2027, is the owner's call.

## Changes proposed for the next submissions, none made

Each waits for the owner's word, and Dr. Han's edits stay word for word.

1. Say the Elsevier rights as they stand: Scopus's in place, ScienceDirect's amendment in process (the abstract,
   section 1's premise, Aim 2's grounding sentence and Aim 3's "The RAG-LLM"), until the amendment is signed.
2. Add one clause to Aim 2's grounding sentence: Elsevier's key and institutional token are held server-side on the
   grid and sent only in request headers over HTTPS, never in browser code or a URL.
3. Run the disclosure audit on the PDF before each further submission.
4. For Anthropic's AI for Science program and the other fits named in the owner's e-mail of 2026-10-16, the parts
   written for AIDaS (the cover's call line, the alignment page, the budget held to the $20,000 cap and line C3's
   reason) are rewritten for that venue's own form; the narrative carries over.

## What remains, the owner's

1. The allowability question to the AIDaS office (`HANDOFF_2026-10-16.md`, step 4): lines B, C3, D and F, and how line A
   may be hired.
2. The approximations, as values come in (`APPROXIMATIONS.md`).
3. Tell Elsevier once the ScienceDirect amendment is signed, and keep the token on the grid as its terms say.
