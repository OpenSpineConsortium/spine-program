"""Point the shared note's sending step at the PDF copy whose name does not say draft."""
import pathlib
import sys

NOTE = pathlib.Path("/mnt/project-files/grant/AIDaS_where_it_stands_2026-10-16.md")

SWAPS = [
    (
        "The 10-page PDF beside this note, AIDaS_SEED_2027_draft_2026-10-16.pdf, is built",
        "The 10-page PDF beside this note, AIDaS_SEED_2027_draft_2026-10-16.pdf (also saved as"
        " AIDaS_SEED_2027_proposal_2026-10-16.pdf, the same file named for sending), is built",
    ),
    (
        "attach AIDaS_SEED_2027_draft_2026-10-16.pdf from this folder and press Send, since the Outlook"
        " connector cannot attach files.",
        "attach AIDaS_SEED_2027_proposal_2026-10-16.pdf from this folder and press Send. No connector"
        " here can attach a file: the Outlook one refuses attachments, and your account has no Gmail"
        " connector.",
    ),
]


def main() -> int:
    text = NOTE.read_text(encoding="utf-8")
    for old, new in SWAPS:
        if text.count(old) != 1:
            print(f"not found exactly once: {old[:60]}", file=sys.stderr)
            return 1
        text = text.replace(old, new)
    NOTE.write_text(text, encoding="utf-8")
    print("note updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
