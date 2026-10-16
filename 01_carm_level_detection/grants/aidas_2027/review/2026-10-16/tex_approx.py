"""Replace the AIDaS packet's red marks with approximations and add line C3 (issue #112)."""
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text()

SWAPS = [
    # cover: the clinical collaborator and the request
    ("leads the Open Spine Consortium. Receives no award funds.\\\\[2pt]",
     "leads the Open Spine Consortium. Receives only line C3, once a WSU adjunct appointee.\\\\[2pt]"),
    ("Request & \\$18,568 for 12 months,", "Request & \\$19,987 for 12 months,"),
    # narrative and alignment page
    ("residents in two waves of four \\tbd{confirm} each receive", "residents in two waves of four each receive"),
    ("no\n  earlier CAREER award) \\tbd{the PI's tenure timing and earlier CAREER competitions}. If the PI",
     "no\n  earlier CAREER award). If the PI"),
    ("The PI's part in the consortium's work so far: \\tbd{the PI's role, and since when}.",
     "The PI has advised the consortium's work since September 2026."),
    ("Effort: PI \\tbd{\\%}, Co-PI \\tbd{\\%}, in kind.", "Effort: PI 5\\pct{}, Co-PI 3\\pct{}, in kind."),
    # budget table
    ("520 h at \\$15.00: Aim 1 180 h, Aim 2 160 h, Aim 3 180 h & \\$7,800\\\\",
     "515 h at \\$15.00: Aim 1 180 h, Aim 2 155 h, Aim 3 180 h & \\$7,725\\\\"),
    ("FICA, 7.65\\pct{} & \\$597\\\\", "FICA, 7.65\\pct{} & \\$591\\\\"),
    ("placeholder \\$1,250 each \\tbd{program fee} & \\$2,500", "\\$1,250 each, estimated & \\$2,500"),
    ("placeholder \\$300 each \\tbd{facility and rate} & \\$600", "\\$300 each, estimated & \\$600"),
    ("4 h at a placeholder \\$300 \\tbd{DLAR rate; that the room\n  takes human specimens} & \\$1,200",
     "4 h at \\$300 an hour, estimated & \\$1,200"),
    ("placeholder \\tbd{OEHS fee} & \\$300", "WSU's fees, estimated & \\$300"),
    ("2 TB of C\\&IT storage at \\$400 per TB-year; Zenodo free & \\$800\\\\\n",
     "2 TB of C\\&IT storage at \\$400 per TB-year; Zenodo free & \\$800\\\\\n"
     "C3 & Reimbursement: Claude subscriptions used to prepare this project & Paid personally by the clinical"
     " collaborator in 2026; against receipts & \\$1,500\\\\\n"),
    ("\\textbf{\\$18,568}", "\\textbf{\\$19,987}"),
    # budget bullets
    ("researcher: 520 hours, most in months", "researcher: 515 hours, most in months"),
    ("2027 (MCL 408.934) \\tbd{WSU's job category and scale}. Temporary", "2027 (MCL 408.934). Temporary"),
    ("At \\$18 an hour the total would be \\$20,247, over the cap unless the hours fall to 507.",
     "At \\$18 an hour the total would be \\$21,650, over the cap unless the hours fall to 429."),
    ("permits de-identified images\n  \\tbd{the program's terms for public release}. Each C-arm user",
     "permits de-identified images,\n  released publicly on the program's terms. Each C-arm user"),
    ("a deployed tool would read \\tbd{the C-arm's model and video output}; at \\$619",
     "a deployed tool would read; at \\$619"),
    ("\\item \\textbf{C1, C2.} Anthropic's Team plan", "\\item \\textbf{C1 to C3.} Anthropic's Team plan"),
    ("since the price holds 12 months from sign-up \\tbd{P-card route and the PI's\n  verification}. The WSU grid's",
     "since the price holds 12 months from sign-up. The WSU grid's"),
    ("what review\n  clears goes to Zenodo at its end.",
     "what review\n  clears goes to Zenodo at its end. C3 repays the Claude subscriptions the clinical collaborator"
     " bought in 2026 to prepare this project, once the collaborator's pending appointment as WSU adjunct faculty"
     " begins, since the call bars award funds to external collaborators."),
    ("indirect costs \\tbd{confirm\n  AIDaS applies no F\\&A}.", "indirect costs, none assumed for an internal award."),
    ("C1 and C2, \\$10,277 in all, above the call's\n  smallest award of \\$10,000. Lines B, D and F are research"
     " costs outside those headings \\tbd{the AIDaS office's\n  answer}; B2 to B5 depend on B1. Without B the request"
     " is \\$13,349:",
     "C1 and C2, \\$10,196 in all, above the call's\n  smallest award of \\$10,000. C3 is computing bought before"
     " the award year, and lines B, D and F are research costs outside those headings, kept unless the AIDaS office"
     " disallows them; B2 to B5 depend on B1. Without B the request is \\$14,768:"),
    ("without B and D, \\$10,349; without B, D and F, \\$10,277.",
     "without B and D, \\$11,768; without B, D and F, \\$11,696."),
]

for old, new in SWAPS:
    count = text.count(old)
    if count != 1:
        sys.exit(f"{count} matches for: {old[:80]!r}")
    text = text.replace(old, new)
path.write_text(text)
print(f"{len(SWAPS)} replacements")
