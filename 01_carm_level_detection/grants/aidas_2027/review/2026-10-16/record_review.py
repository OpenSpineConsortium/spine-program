"""Bring RECORD.md in line with the review of 2026-10-16: rows reworded, sources added, section 3 and 4 updated."""
import sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()

def swap(old, new):
    global text
    n = text.count(old)
    assert n == 1, (n, old[:80])
    text = text.replace(old, new)

swap("| US neurosurgeons reported 418 wrong-level operations in about 1.3 million, one in 3,110, 17 % followed by legal action [2] |",
     "| US neurosurgeons reported 418 wrong-level operations in about 1.3 million, one in 3,110, 17 % followed by legal action or a settlement [2] |")
swap("| a card for each of 211 imaging sources (5.3 TB on the grid) |",
     "| a card for each of 211 imaging sources, 115 of them on the grid (5.3 TB); in the abstract \"211 catalogued sources, 115 on the grid at 5.3 TB\" |")
swap("| every item keyed to a person; nine leakage checks (\"which closed the two cross-naming leaks the identity checks found\" was cut for room in the reframing of 2026-10-16) |",
     "| every item keyed to a person; nine leakage checks (seven run on the frozen split) (\"which closed the two cross-naming leaks the identity checks found\" was cut for room in the reframing of 2026-10-16) |")
swap("| two automatic labelers chosen to fail differently screened 18 public collections (843 GPU-hours) | `06_transitional_ct_census/docs/CENSUS_TABLE_2026-09-25.md` (843 GPU-hours: TotalSegmentator 443, SPINEPS 400) and `06_transitional_ct_census/STATUS.md` (catalog D.13: 18 collections, 18,873 listed; the row is DISPUTED for its on-disk and field-gate counts only, which the packet does not quote) |",
     "| the two automatic labelers chosen to fail differently \"screened 18 further public collections (843 GPU-hours)\", after the registry | `06_transitional_ct_census/docs/CENSUS_TABLE_2026-09-25.md` (843 GPU-hours: TotalSegmentator 443, SPINEPS 400; section 1, one row per collection, 18 rows) and `06_transitional_ct_census/STATUS.md` (catalog D.13: 18 collections, 18,873 listed; the row is DISPUTED for its on-disk and field-gate counts only, which the packet does not quote); the screen is later than the registry and not in it (`evidence/spine-aim-facts-2026-10-15.md`: the registry \"leaves out the 18 acquired collections' calls\"), so since the review of 2026-10-16 the packet no longer says the screen filled the registry |")
swap("| a registry of 6,108 persons holding 146 with a sixth lumbar vertebra, 103 on an expert read, and 14 with a thirteenth thoracic | catalog row D.8 (6,131 rows, 6,108 persons, 782 alias edges; L6 146, of which 103 read by a person; T13 14) |",
     "| the labelers \"filled a registry of 6,108 persons from the collections then in hand, 146 of them with a sixth lumbar vertebra, 103 on an expert read, and 14 with a thirteenth thoracic\" | catalog row D.8 (the one registry of 2026-09-24: 6,131 rows, 6,108 persons, 782 alias edges; L6 146, of which 103 read by a person, 29 two-labeller, 10 single; T13 14) built from D.7's five harvest streams (verse, ctsp, totalsegmentator, cobra and other_ct, the last holding CTSpine1K and RibFrac among others) |")
swap("| a stopping rule fixed before any download that turned 29,479 chest CTs away | catalog row D.11 (the rule: no collection below 20 expected transitional persons per terabyte, no fetch under 5 TB free, an 8 TB cap, tier 1 before tier 2; 29,479 chest CTs, 2.9 TB, turned down) |",
     "| a stopping rule, fixed before any download, that turned 29,479 mostly chest CTs away | catalog row D.11 (the rule: no collection below 20 expected transitional persons per terabyte, no fetch under 5 TB free, an 8 TB cap, tier 1 before tier 2; 29,479 CTs, 2.9 TB, turned down), `06_transitional_ct_census/README.md` (\"tier 2 (29,479 CTs, 2.9 TB) refused\") and the census table's section 2, whose tier 2 is chest-dominated, hence \"mostly\" |")
swap("| a labeler's 9.3 % rate of thirteenth rib-bearing vertebrae in 367 chest CTs fell to 1.4 % once a rib on the named body was required (",
     "| a labeler's 9.3 % rate of thirteenth rib-bearing vertebrae in 367 chest CTs fell to 1.4 % (5 of 367) once a rib on the named body was required (")
swap("| the film detector finds 98.8 % of 161 lumbar vertebrae on 17 spines it never saw |",
     "| the film detector finds 98.8 % (at 0.25) of 161 lumbar vertebrae on 17 spines it never saw |")
swap("| 145 Elekta cases, 24 frames each, are in any training bank; 322 Elekta and all 225 Varian cases train nothing; the 372,000 unseen projections | `01_carm_level_detection/docs/handoff/DATASET_USAGE.md` section 2 (145 Elekta cases of 24 frames in the banks, 0 of 225 Varian);",
     "| 145 Elekta cases, 24 frames each, are in any frame bank (110 of them, 2,640 frames, train the detector); 322 Elekta and all 225 Varian cases train nothing; the 372,000 unseen projections, \"with a CT whose automatic labels project onto every one\" | `01_carm_level_detection/docs/handoff/DATASET_USAGE.md` section 2 (145 Elekta cases of 24 frames in the banks, 0 of 225 Varian) and its table's COBRA row (detector S trains on 110 cases and selects on 8, the other 27 its test; 110 x 24 = 2,640, the count A7.4 cuts to 240); the planning CTs' labels are the automatic labelers', none read by a person;")
swap("| COBRA's median age is 66 | row A18.1 (age known on 115 of the 145 exported cases) |",
     "| \"the median age of its exported cases is 66 (known for 115 of 145)\" | row A18.1 (age known on 115 of the 145 exported cases) |")
swap("| COBRA: 692 radiotherapy cone-beam cases (467 Elekta XVI, 225 Varian OBI), 375,618 projections, each case with its acquisition geometry and a registered planning CT [29] |",
     "| COBRA: 692 radiotherapy cone-beam cases (467 Elekta XVI, 225 Varian OBI), 375,618 projections, each case with its acquisition geometry and a registered planning CT [29] (\"exact\" was dropped in the review of 2026-10-16: the geometry is RTK's per-case file, the CT deformably registered) |")

# The latency clause H3 now carries.
anchor = "| compute is GitHub's free standard runners on public repositories (Aim 1c and the budget's C1, C2 note) |"
i = text.index(anchor)
j = text.index("\n", i) + 1
latency = ("| H3's \"the stack names a frame in under 1 s on one GPU (no latency of the stack is on file yet)\" | "
           "`01_carm_level_detection/CLAUDE.md` (\"No latency of the reported stack exists\": the 2026-09-13 bench timed older "
           "models, the 2026-09-22 run was contended and never timed the detector, the GPU job of `docs/MODEL_CARD.md` section "
           "6.6 was never run); the 1 s is a target written before any run, and the budget's latency runs measure it |\n")
text = text[:j] + latency + text[j:]

# Section 2: what the two arXiv abstracts say.
swap("the 63.8 and 82.5 % are the owner's report's reading of the paper, not read in the paper here |",
     "the 63.8 and 82.5 % are the owner's report's reading of the paper; the abstract, read on 2026-10-16, says STORM \"outperforms the git-worktree-based multi-agent baseline by +18.7 on Commit0-Lite\", and 82.5 - 63.8 = 18.7 |")
swap("2026-01-19); the counts from the taxonomy specification's section 7.1 |",
     "2026-01-19); the counts from the taxonomy specification's section 7.1; the abstract, read again on 2026-10-16, says agents \"achieve on average 30% lower success rates when working together\" (GPT-5's 183 against 315 is 42 % lower, Sonnet 4.5's 168 against 307 45 %, so the two named models sit above that average) and names jammed communication, broken commitments and wrong expectations as the issues; \"most failures duplicated or incompatible work\" is the specification's 33.2 % work overlap plus 29.7 % divergent architecture |")

# Section 3: the marks Dr. Han's edits settled.
swap("2. That the PI's appointment is tenure-track (the call requires it) and the ESI end date in eRA Commons.\n3. That the PI leads no other AIDaS proposal this cycle.",
     "2. Settled: that the PI's appointment is tenure-track (the call requires it) and the ESI end date in eRA Commons,\n   both confirmed in Dr. Han's edits of 2026-10-15 (issue #102), which commented their marks out.\n3. Settled the same way: that the PI leads no other AIDaS proposal this cycle.")

# The [9] note.
swap("- **Reference [9]** is cited without its author list, since rule 12 keeps student names out of this repository; add\n  the authors in Overleaf if wanted.",
     "- **Reference [9]** names its first author alone, \"Schehr A, et al.\" (a published co-author, root CLAUDE.md rule 1),\n  since rule 12 keeps student names out of this repository; add the other authors in Overleaf if wanted.")

# Section 4: the review.
review = """- **The adversarial review of 2026-10-16.** One reviewer read the packet against its files and traced every number
  (its report is in the thread's session, not in git); 32 findings. Applied: "an invention-disclosure review" became
  "WSU's technology-transfer review"; the registry no longer reads as filled by the 18-collection screen (rows above);
  115 of the 211 sources on the grid; seven of the nine leakage checks run; "legal action or a settlement"; the films
  "labeled", not "with their reports"; the plug-in "a Claude plug-in", not OpenEvidence's, and the question set on
  public images; the RAG-LLM's first release in the clinical collaborator's in-kind work and in line A's checking
  hours; the second release's fine-tune and "whose stated purposes include"; COBRA's frame bank against its
  training frames, "automatic labels", the exported cases' median age, no "exact" geometry; "no latency of the stack
  is on file yet" in H3; the wizard and the grid bridge in quarter 2; "at 0.25" on A14.1; "submitted" for the
  abstracts; "many GPU jobs" for "hundreds"; the PDF's title; and the record rows. Not applied: the reviewer read
  "nothing retrained" as barring the RAG-LLM's fine-tune, but that hold is about the leaked initialisations (rule 9)
  and the owner's message of 2026-10-16 asks for the fine-tune; the ScienceDirect wording stays on the owner's word
  (section 6) with "under WSU's text and data mining and AI rights from Elsevier" in place of "rights Elsevier
  approved"; the references stay 5.8 pt in five columns and the orchestrator frameworks stay named, for room. To hold
  10 pages after it: the narrative on 9.7 pt leading, Figure 2 at 0.46 of the line and Figure 4 at 0.48, two
  timeline rows and the closing line shortened. `review/page_slack.py` now measures against the 0.65 in margins.
"""
anchor4 = "  Not changed, since the owner's message did not ask it: the holds of 2026-10-15 (no coordbench run data; VinDr and\n  FluoroCap's results stay; rule 9), the names kept private, and the eight red marks' owners.\n"
i = text.index(anchor4)
j = i + len(anchor4)
text = text[:j] + review + text[j:]
swap("the names kept private, and the eight red marks' owners.\n",
     "the names kept private, and the red marks' owners.\n")

open(path, "w", encoding="utf-8").write(text)
print("ok", len(text.splitlines()), "lines")
