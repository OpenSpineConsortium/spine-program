"""Record the reframing of 2026-10-16 in RECORD.md: amended rows, new rows, a [31] row, a section 4 bullet, section 6."""
import sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()

def swap(old, new, count=1):
    global text
    n = text.count(old)
    assert n == count, (n, old[:80])
    text = text.replace(old, new)

# Section 1: rows whose packet text changed in the reframing.
swap("| on rebuilt truth, 82.2 % of the 287 (236 / 287) and 93.9 % of the 214 vertebrae whose truth is complete and at least 80 % visible (201 / 214) | row A6.5,",
     "| (cut for room in the reframing of 2026-10-16) on rebuilt truth, 82.2 % of the 287 (236 / 287) and 93.9 % of the 214 vertebrae whose truth is complete and at least 80 % visible (201 / 214) | row A6.5,")
swap("| one US insurer's 68 wrong-site claims closed in 2013 to 2020 averaged $136,453, 60.3 % settled, spine the commonest procedure [25] | `09_wrong_level_clinical_qi/docs/WRONG_SITE_BURDEN_EVIDENCE.md` (Tan 2023: mean closed claim value $136,452.84, 60.3 % settled;",
     "| one US insurer's 68 wrong-site claims closed in 2013 to 2020 averaged $136,453, spine the commonest procedure [25] (\"60.3 % settled\" was cut for room in the reframing of 2026-10-16) | `09_wrong_level_clinical_qi/docs/WRONG_SITE_BURDEN_EVIDENCE.md` (Tan 2023: mean closed claim value $136,452.84, 60.3 % settled;")
swap("| every item keyed to a person, which closed the two cross-naming leaks the identity checks found; nine leakage checks |",
     "| every item keyed to a person; nine leakage checks (\"which closed the two cross-naming leaks the identity checks found\" was cut for room in the reframing of 2026-10-16) |")
swap("| one labeler called a thirteenth rib-bearing vertebra in 9.3 % of 367 chest CTs, five to fifteen times the published rate; requiring a rib on the named body brought it to 1.4 % |",
     "| a labeler's 9.3 % rate of thirteenth rib-bearing vertebrae in 367 chest CTs fell to 1.4 % once a rib on the named body was required (\"five to fifteen times the published rate\" was cut for room in the reframing of 2026-10-16) |")
swap("| gh-aw's work queue, unsorry, Copilot's cloud agent and Claude Code's agent teams, placed on the twelve-axis taxonomy (who pays, how a claim is kept, what decides acceptance) |",
     "| gh-aw's work queue, unsorry, Copilot's cloud agent and Claude Code's agent teams, on the twelve-axis taxonomy written for the comparison (the three axes named in parentheses were cut for room in the reframing of 2026-10-16) |")

new_rows = """| the project's goal, "a customizable, locally hosted retrieval-augmented language model for spine care (a RAG-LLM)" that reads the image through the consortium's detectors, retrieves from its index of Scopus and ScienceDirect spine literature, answers with cited quotations, is fine-tuned on images paired with clinical charts under the pending protocol, is compared with OpenEvidence through its plug-in for Claude [31], and lets a lab swap in its own corpus, detectors and records; the spine program as "the case example" (the title, the cover's area 4 line, the abstract, section 1's premise, Aim 3's heading and its paragraph "The RAG-LLM", section 3, the alignment page) | the owner's message of 2026-10-16 02:30 UTC in the Project's chat: the proposal "can be reworked such that the SpineAI project is simply a case example of what this organized AI assisted tool can facilitate in a short period of time, the goal is to develop a customizable RAG-LLM, where I will train a multimodal LLM which uses my XRay detector and my Scopus and now science direct Text, Image, Multimedia database to create a RAG of spine literature/imaging and pretrained spine detector on my corpus to fine tune on / with images corresponding with clinical charts under the auspices of this IRB which will be amended however necessary / and either compare with or used to augment / augment an OpenEvidence plug in claude" (the mcpmarket.com link of [31]); "compare with or ... augment" is kept as both, the side-by-side grading and the detectors offered to OpenEvidence as a tool |
| "IRB-26-03-8648, whose stated purpose is a locally hosted multimodal spine LLM, amended as the work requires" (Aim 3); "fine-tuned on images paired with clinical charts under the consortium's pending IRB protocol (about 4,000 Detroit Medical Center spine surgery patients; amended as the work requires)" (the abstract); "the pending protocol's own stated purpose" (section 1) | the IRB form's print view (section 6; given again with the owner's message of 2026-10-16), whose purpose section reads "Multimodal AI Development: To train and validate a proprietary, multimodal spine surgery Large Language Model (LLM)", with "all deep learning and model training ... executed locally on the secured Wayne State University high-performance computing grid" and "Public or cloud-based AI systems (e.g., ChatGPT) ... strictly prohibited", for "report-and-image-to-mask" tasks, decision support and synthetic planning and educational imagery; "amended as the work requires" is the owner's "which will be amended however necessary" |
| the index of "Scopus and ScienceDirect spine literature (text, images and multimedia, under WSU's text and data mining rights)" (the abstract) and Aim 2's "Scopus, and ScienceDirect's text, images and multimedia ... under the text and data mining and AI rights Elsevier approved for WSU" | the owner's message of 2026-10-16 ("my Scopus and now science direct Text, Image, Multimedia database"); the correspondence of 2026-10-15 (section 6) had Scopus approved and ScienceDirect's amendment pending, so the owner's "now" is read as that amendment having come through, a reading the owner confirms before submission, since no later correspondence was given to the thread |
| "its answers and OpenEvidence's, through OpenEvidence's plug-in for Claude [31], are graded side by side for correctness and for quotations that support them; our detectors' reading of an image can be handed to OpenEvidence as a tool, while no indexed passage and no patient record leaves the grid" (Aim 3), H3's "graded correct at least as often as OpenEvidence where the question needs the image, with no unsupported quotation", and the Measures' "graded correctness and quotation support against OpenEvidence" | a design of this thread's, from the owner's "either compare with or used to augment": the correspondence of 2026-10-15 told Elsevier that no outside AI service receives its content and the protocol's own text bars public or cloud AI on its data, so the comparison sends OpenEvidence only the question and the detectors' reading of the image, and the mentors grade the two answers by hand; the threshold "at least as often ... where the question needs the image" is a hypothesis written before any run, this thread's choice |
| "the RAG-LLM's first release, on the public corpus (CTSpinoPelvic1K, the films and their reports, COBRA)", its second "on images paired with operative notes and radiology reports under IRB-26-03-8648" (Aim 3, section 3's quarters 3 and 4) | a design of this thread's: the public corpus is the one in hand (section 1's rows for 802 CTs, 39,705 radiographs, COBRA), so the first release and its graded question set fit the award year while the protocol is amended and approved; the films' reports are VinDr-SpineXR's and NHANES II's published readings (`10_data_platform_grid/docs/DATA_COMPLETENESS_AUDIT.md`), none a patient record of the consortium's |
"""
anchor = "| compute is GitHub's free standard runners on public repositories (Aim 1c and the budget's C1, C2 note) |"
i = text.index(anchor)
j = text.index("\n", i) + 1
text = text[:j] + new_rows + text[j:]

# Section 2: [31].
swap("The rewrite for issue #106 (the owner's items 5 to 12 of 2026-10-15) added references [21] to [30]. The cost",
     "The rewrite for issue #106 (the owner's items 5 to 12 of 2026-10-15) added references [21] to [30], and the\nreframing of 2026-10-16 (the owner's message of 02:30 UTC, section 4) added [31]. The cost")
swap("| [30] C-ArmLSpine. Med Image Anal 2024;97:103283 |",
     "| [31] OpenEvidence, openevidence.com; its Claude Code set-up skill, mcpmarket.com/tools/skills/openevidence-api-setup-auth | https://mcpmarket.com/tools/skills/openevidence-api-setup-auth, read on 2026-10-16: a Claude Code skill, \"OpenEvidence API Setup & Auth\" by jeremylongshore, that \"configures and verifies OpenEvidence API authentication for clinical decision support integrations in healthcare applications\"; the link the owner's message of 2026-10-16 gave; openevidence.com itself was not read, so the packet calls it a clinical evidence service and quotes no figure about it |\n| [30] C-ArmLSpine. Med Image Anal 2024;97:103283 |")
swap("Since issue #106 the list is [1] to [30]; [1] to [20] are as before.",
     "Since issue #106 the list is [1] to [31]; [1] to [20] are as before.")

# Section 4: the rewrite bullet's layout sentence is superseded; a new bullet for the reframing.
swap("the references are 5.8 pt in five columns. Cutting 1d or the Measures clauses would give back 9.5 to 10 pt.",
     "the references are 5.8 pt in five columns (the layout changed again in the reframing, two bullets below).")
reframe = """- **The reframing of 2026-10-16 (the owner's message of 02:30 UTC).** The spine program is now the case example and
  the project's end product is the customizable, locally hosted spine RAG-LLM (section 1's five rows on it). Changed:
  the title; the cover's area 4 line; the abstract's goal sentence and its deliverables; section 1's premise paragraph
  and its Aim 3 line; Aim 2's grounding sentence (ScienceDirect's text, images and multimedia beside Scopus); Aim 3's
  heading, a new paragraph "The RAG-LLM" (the detectors as the model's tools, the first release on the public corpus,
  the second on paired images and charts under the protocol, the side-by-side grading against OpenEvidence), H3 and
  the Measures; section 3's deliverables and quarters 3 and 4; the alignment page's R21 item and team sentence; the
  budget's C2 line; and reference [31]. Displaced for room, with nothing else lost: A6.5's rebuilt-truth clause (82.2
  and 93.9 %), Tan's "60.3 % settled", the identity checks' two closed leaks, D.12's "five to fifteen times the
  published rate", "End-to-end latency is unmeasured; Aim 3 measures it first" (the latency measures and the budget's
  latency runs stay), the three taxonomy axes named in parentheses, the keywords "3-D Gaussian splatting" and "domain
  transfer", COBRA's "by supervision" and the cost list's wording, and section 3's heading paragraph, now one
  paragraph. The layout now: the abstract in \\small, the narrative 8.8 pt on 9.8 pt leading with 0.5 pt paragraph
  skip and 4 pt float separation, captions at 1 pt skip, the references' column separation 1 pt, Figures 1 and 4 at
  0.50 of the line and Figure 2 at 0.48, Figure 3's panels 2.55 and 1.56 in; 10 pages, no overfull line, 16 red marks.
  Not changed, since the owner's message did not ask it: the holds of 2026-10-15 (no coordbench run data; VinDr and
  FluoroCap's results stay; rule 9), the names kept private, and the eight red marks' owners.
"""
anchor4 = "  gantry angle; no same-case pair, so the by-case split holds; `01_carm_level_detection/docs/DATASHEET.md`).\n"
i = text.index(anchor4)
j = i + len(anchor4)
text = text[:j] + reframe + text[j:]

# Section 6: where the two sources now reach the packet.
swap("In the packet: the cover's area 3 line, the abstract, Aim 2's grounding sentence,\n  the evaluation table's Aim 2 metrics and the clinical collaborator's roles.",
     "In the packet: the cover's area 3 line, the abstract, Aim 2's grounding sentence,\n  the evaluation table's Aim 2 metrics and the clinical collaborator's roles; since the reframing of 2026-10-16 also\n  the abstract's goal sentence, section 1's premise and Aim 3's \"The RAG-LLM\", which name ScienceDirect's text,\n  images and multimedia on the owner's word of that day (\"now science direct\"), the amendment this correspondence\n  left pending; the owner confirms it before submission.")
swap("In the packet: the\n  abstract (\"an IRB protocol awaiting submission would add about 4,000\" patients' \"CTs, operative notes and radiology\n  reports\"), the alignment page's R21 item (\"pending\", \"about 4,000 adult DMC spine surgery patients, their CT and\n  records\") and its team paragraph (\"the pending protocol\"), nothing more; since issue #100 section 4 no longer\n  names it.",
     "In the packet: since the\n  reframing of 2026-10-16, the abstract (\"fine-tuned on images paired with clinical charts under the consortium's\n  pending IRB protocol (about 4,000 Detroit Medical Center spine surgery patients; amended as the work requires)\"),\n  section 1 (\"the pending protocol's own stated purpose\"), Aim 3 (\"IRB-26-03-8648, whose stated purpose is a locally\n  hosted multimodal spine LLM, amended as the work requires\"; the form's purpose paragraph is quoted in section 1's\n  row), the alignment page's R21 item (\"pending\", \"about 4,000 adult DMC spine surgery patients, their CT and\n  records, the RAG-LLM's paired images and charts\") and its team paragraph (\"the pending protocol\"); the form was\n  given to the thread again on 2026-10-16 with the owner's message and stays out of git.")

open(path, "w", encoding="utf-8").write(text)
print("ok", len(text.splitlines()), "lines")
