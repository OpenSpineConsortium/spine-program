# counsel: the inventor's responses to counsel's questions (WSU 26-1902)

Privileged and confidential: an attorney-client communication prepared at counsel's request for the meeting on the
provisional application. It stays in this private repository; nothing here goes to a public place.

| Path | What it is |
|---|---|
| `WSU_26-1902_Inventor_Responses_2026-10-20.docx` | The answers to counsel's 60 questions ("WSU 26-1902 FS 66174-0372 Questions to Inventor", received 2026-10-20), each with its status, sources and a drafting suggestion; the numbers to replace in the draft specification; post-draft subject matter; IDS references |
| `figures/` | The eight figures in the document; schematics are labelled illustrative, and every plotted number names its file in the caption |
| `source/` | `figures.py` draws the figures (matplotlib); `build.js` with `content.js` and `answers.js` builds the document (the `docx` npm package) |

Rebuild: `python3 source/figures.py figures && node source/build.js figures out.docx`, from this folder.

Sources are linked at fixed commits: spine-program 240cabc and spinesurg-ct-nnunet 0ab783f.
