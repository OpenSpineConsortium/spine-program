"""Write the reference .docx that build_pdf.sh hands to pandoc: Liberation Sans 10 pt, 0.7 inch margins, black
headings, compact spacing, and a page break before every top-level heading, so each component of the call
starts its own page and the narrative fits the page limits without a binary checked in.

Pandoc's own default reference document is taken from pandoc itself and patched in place, so the result follows
whatever pandoc version runs the build.
"""

import re
import subprocess
import sys
import zipfile
from pathlib import Path

FONT = "Liberation Sans"
RFONTS = f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}" w:eastAsia="{FONT}" />'
SECT = (
    '<w:sectPr><w:pgSz w:w="12240" w:h="15840" />'
    '<w:pgMar w:top="1008" w:right="1008" w:bottom="1008" w:left="1008" w:header="576" w:footer="576" w:gutter="0" />'
    "</w:sectPr>"
)


def style_block(styles: str, style_id: str) -> str:
    match = re.search(r'<w:style [^>]*w:styleId="%s".*?</w:style>' % re.escape(style_id), styles, re.S)
    if match is None:
        raise SystemExit(f"style {style_id} is not in pandoc's reference document")
    return match.group(0)


def set_paragraph(styles: str, style_id: str, before: int, after: int, size: int | None = None, bold: bool | None = None) -> str:
    block = style_block(styles, style_id)
    new = block
    if "<w:pPr>" in new:
        new = re.sub(r"<w:spacing [^/]*/>", f'<w:spacing w:before="{before}" w:after="{after}" />', new, count=1)
        if "<w:spacing" not in new:
            new = new.replace("<w:pPr>", f'<w:pPr><w:spacing w:before="{before}" w:after="{after}" />', 1)
    else:
        new = new.replace("</w:style>", f'<w:pPr><w:spacing w:before="{before}" w:after="{after}" /></w:pPr></w:style>', 1)
    if size is not None:
        rpr = f"<w:rPr>{RFONTS}{'<w:b /><w:bCs />' if bold else ''}<w:color w:val=\"000000\" /><w:sz w:val=\"{size}\" /><w:szCs w:val=\"{size}\" /></w:rPr>"
        if "<w:rPr>" in new:
            new = re.sub(r"<w:rPr>.*?</w:rPr>", rpr, new, count=1, flags=re.S)
        else:
            new = new.replace("</w:style>", rpr + "</w:style>", 1)
    return styles.replace(block, new, 1)


def patch_styles(styles: str) -> str:
    styles = re.sub(
        r"<w:rPrDefault>.*?</w:rPrDefault>",
        f'<w:rPrDefault><w:rPr>{RFONTS}<w:sz w:val="20" /><w:szCs w:val="20" />'
        '<w:lang w:val="en-US" w:eastAsia="en-US" w:bidi="ar-SA" /></w:rPr></w:rPrDefault>',
        styles, count=1, flags=re.S,
    )
    styles = re.sub(r"<w:pPrDefault>.*?</w:pPrDefault>", '<w:pPrDefault><w:pPr><w:spacing w:after="0" /></w:pPr></w:pPrDefault>', styles, count=1, flags=re.S)
    styles = set_paragraph(styles, "BodyText", 0, 80)
    styles = set_paragraph(styles, "Compact", 10, 10, size=18)
    styles = set_paragraph(styles, "Heading1", 0, 80, size=28, bold=True)
    heading = style_block(styles, "Heading1")
    styles = styles.replace(heading, heading.replace("<w:pPr>", "<w:pPr><w:pageBreakBefore />", 1), 1)
    styles = set_paragraph(styles, "Heading2", 110, 30, size=23, bold=True)
    styles = set_paragraph(styles, "Caption", 40, 120, size=18)
    return styles


def set_page(docx: Path) -> None:
    """Give a finished .docx the Letter page and 0.7 inch margins, since pandoc 3.1 writes an empty section
    element and LibreOffice then falls back to one inch margins."""
    tmp = docx.with_suffix(".page.docx")
    with zipfile.ZipFile(docx) as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "word/document.xml":
                text = data.decode("utf-8")
                text = re.sub(r"<w:sectPr\s*/>", SECT, text, count=1)
                if "<w:sectPr" not in text:
                    text = text.replace("</w:body>", SECT + "</w:body>", 1)
                data = text.encode("utf-8")
            dst.writestr(item, data)
    tmp.replace(docx)


def main(out: Path) -> None:
    default = subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"], check=True, capture_output=True).stdout
    tmp = out.with_suffix(".default.docx")
    tmp.write_bytes(default)
    with zipfile.ZipFile(tmp) as src, zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "word/styles.xml":
                data = patch_styles(data.decode("utf-8")).encode("utf-8")
            if item.filename == "word/document.xml":
                text = data.decode("utf-8")
                if "<w:sectPr" not in text:
                    text = text.replace("</w:body>", SECT + "</w:body>", 1)
                data = text.encode("utf-8")
            dst.writestr(item, data)
    tmp.unlink()
    print("wrote", out)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--page":
        set_page(Path(sys.argv[2]))
    else:
        main(Path(sys.argv[1] if len(sys.argv) > 1 else "reference.docx"))
