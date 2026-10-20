# counsel: the inventor's responses to counsel's questions (WSU 26-1902)

Privileged and confidential: an attorney-client communication prepared at counsel's request for the meeting on the
provisional application. It stays in this private repository; nothing here goes to a public place.

| Path | What it is |
|---|---|
| `WSU_26-1902_Inventor_Responses_2026-10-20.docx` | The answers to counsel's 60 questions ("WSU 26-1902 FS 66174-0372 Questions to Inventor", received 2026-10-20), each with its status, sources and a drafting suggestion; the numbers to replace in the draft specification; post-draft subject matter; IDS references |
| `WSU_26-1902_Counsel_Package_Cover_Memo_2026-10-20.docx` | The cover memo of the package sent to counsel: the state of the invention in one table, the points counsel must know first (including the public disclosures of Parts A and B), the reading order, the contents and what was left out and why |
| `PACKAGE_MANIFEST.txt` | The SHA-256 and path of each of the 67 files in the package zip; the zip itself is not committed (21 MB, copies of files already in git) and is in the project's shared files as `patent/WSU_26-1902_Counsel_Package_2026-10-20.zip` |
| `figures/` | The eight figures in the document; schematics are labelled illustrative, and every plotted number names its file in the caption |
| `source/` | `figures.py` draws the figures (matplotlib); `build.js` with `content.js` and `answers.js` builds the document, and `cover.js` builds the cover memo from the assembled package folder (the `docx` npm package) |

Rebuild: `python3 source/figures.py figures && node source/build.js figures out.docx`, from this folder; the cover memo is `node source/cover.js <package folder> <package folder>/00_READ_FIRST_Cover_Memo.docx`. The package's 02 and 03 Word files are `pandoc -f gfm --reference-doc=<pandoc's default reference.docx>` of the .md files beside them.

Sources are linked at fixed commits: spine-program 240cabc and spinesurg-ct-nnunet 0ab783f.
