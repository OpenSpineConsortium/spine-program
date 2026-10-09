#!/usr/bin/env python
"""Extract the 44 CLAIM 2024 items, verbatim, from the published checklist table.

Source: Tejani AS, Klontzas ME, Gatti AA, Mongan JT, Moy L, Park SH, Kahn CE Jr; CLAIM 2024 Update Panel.
Checklist for Artificial Intelligence in Medical Imaging (CLAIM): 2024 Update. Radiol Artif Intell
2024;6(4):e240300. doi:10.1148/ryai.240300. The journal's own page and its Word appendix answer 403 to every
client tried from this workstation (curl and curl_cffi with four browser profiles, 2026-09-23), so the table is
read from the open-access copy of the same article: https://escholarship.org/content/qt9zf6q2rb/qt9zf6q2rb.pdf
(8 pages; SHA-256 85c864815ce5830c6cd7a1916038dbafb9914d04e3144cbebdbc7f6a210c2922 on 2026-09-23).

    python extract_items.py <path-to-that-pdf>      # writes items.json beside this script

The table's text is taken exactly as printed (wrapped lines joined with one space); section and topic headings
are carried per item. Fails unless exactly items 1-44 come out, in order.
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SECTIONS = ["TITLE/ABSTRACT", "ABSTRACT", "INTRODUCTION", "METHODS", "RESULTS", "DISCUSSION", "OTHER INFORMATION"]
TOPICS = ["Study Design", "Data", "Reference Standard", "Data Partitions", "Testing Data", "Model", "Training",
          "Evaluation", "Model Performance"]
# 2024 item -> the 2020 item it continues (Mongan 2020, doi 10.1148/ryai.2020200029), None = new in 2024.
# 2020 item 11 (definitions of data elements) was deleted in 2024 (the article, "Key Features"); the mapping of the
# rest is by item text, read side by side with claim_checklist.json (the 2020 docx), not stated by the article.
CROSSWALK_2020 = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 12, 12: 13, 13: None,
                  14: 14, 15: 15, 16: 16, 17: 17, 18: 18, 19: 20, 20: 21, 21: 19, 22: 22, 23: 23, 24: 24,
                  25: 25, 26: 26, 27: 27, 28: 28, 29: 29, 30: 30, 31: 31, 32: None, 33: 32, 34: 40, 35: 33,
                  36: 34, 37: 35, 38: 36, 39: 37, 40: 38, 41: 39, 42: 41, 43: None, 44: 42}


def main() -> int:
    pdf = Path(sys.argv[1])
    import fitz
    raw = pdf.read_bytes()
    text = "".join(p.get_text() for p in fitz.open(stream=raw, filetype="pdf"))
    start = text.index("TITLE/ABSTRACT\n1\n")
    stop = text.index("Indicate page and/or line number for each checklist item that is present.")
    lines = [ln.strip() for ln in text[start:stop].splitlines() if ln.strip()]
    items, section, topic, cur = [], "", "", None
    for ln in lines:
        if ln in SECTIONS:
            section, topic, cur = ln, "", None
        elif ln in TOPICS:
            topic, cur = ln, None
        elif ln.isdigit():
            cur = {"item": int(ln), "section": section, "topic": topic, "text": ""}
            items.append(cur)
        elif cur is not None:
            cur["text"] = (cur["text"] + " " + ln).strip()
        else:
            raise SystemExit(f"unplaced line: {ln!r}")
    assert [it["item"] for it in items] == list(range(1, 45)), [it["item"] for it in items]
    for it in items:
        it["claim_2020_item"] = CROSSWALK_2020[it["item"]]
    out = {
        "checklist": "CLAIM 2024 Update",
        "citation": "Tejani AS, Klontzas ME, Gatti AA, Mongan JT, Moy L, Park SH, Kahn CE Jr; CLAIM 2024 Update "
                    "Panel. Checklist for Artificial Intelligence in Medical Imaging (CLAIM): 2024 Update. Radiol "
                    "Artif Intell 2024;6(4):e240300. doi:10.1148/ryai.240300",
        "response_options": ["Yes", "No", "NA"],
        "instruction": "Indicate page and/or line number for each checklist item that is present.",
        "source_pdf": "https://escholarship.org/content/qt9zf6q2rb/qt9zf6q2rb.pdf",
        "source_pdf_sha256": hashlib.sha256(raw).hexdigest(),
        "extracted_by": "SchwingNet/packet_src/claim2024/extract_items.py",
        "crosswalk_note": "claim_2020_item = the item of CLAIM 2020 (the docx at the repository root) that this "
                          "item continues; null = new in 2024 (13 image acquisition protocol; 43 availability "
                          "of software, model and data; 32 evaluation on internal data has no 2020 counterpart, 2020 "
                          "item 35 asked for performance on all partitions). 2020 item 11 (data elements) was "
                          "deleted; 2020 item 40 (registration) is now 34, 2020 item 19 (sample size) now 21.",
        "items": items,
    }
    io.open(HERE / "items.json", "w", encoding="utf-8", newline="\n").write(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote items.json: {len(items)} items, sha256 {out['source_pdf_sha256'][:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
