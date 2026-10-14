"""Print, for each page of the packet's PDF, how far its lowest text sits above the text block's bottom.

The packet fills its pages, so an edit that adds a line to a full page pushes a section onto an extra page and
build_pdf.sh fails. Run this after each build to see which pages have room: python3 page_slack.py <packet PDF>.
"""
import re
import subprocess
import sys

TEXT_BLOCK_BOTTOM = 792 - 0.7 * 72  # letter paper with 0.7 inch margins, in points


def lowest_text_per_page(pdf):
    html = subprocess.run(["pdftotext", "-bbox", pdf, "-"], capture_output=True, text=True, check=True).stdout
    for page in re.findall(r"<page.*?</page>", html, re.S):
        bottoms = [float(y) for y in re.findall(r'yMax="([\d.]+)"', page)]
        yield max(y for y in bottoms if y < TEXT_BLOCK_BOTTOM + 8)


for number, lowest in enumerate(lowest_text_per_page(sys.argv[1]), 1):
    print(f"page {number}: lowest text {lowest:.1f} pt, slack {TEXT_BLOCK_BOTTOM - lowest:.1f} pt")
