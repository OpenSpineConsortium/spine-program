#!/usr/bin/env bash
# Build AIDaS_SEED_2027_packet.pdf from the markdown: the submitted part only (up to the marker line), through
# pandoc to .docx and LibreOffice to PDF, since the container has neither LaTeX nor a browser engine. Needs
# pandoc, soffice (LibreOffice) and pdfinfo; run from any directory.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
work="${TMPDIR:-/tmp}/aidas_packet_build"
mkdir -p "$work"
sed '/<!-- end of the submitted packet/q' "$here/AIDaS_SEED_2027_packet.md" > "$work/packet.md"
python3 "$here/make_reference_docx.py" "$work/reference.docx" > /dev/null
pandoc "$work/packet.md" --from markdown --to docx --reference-doc "$work/reference.docx" \
  --resource-path "$here" --output "$work/AIDaS_SEED_2027_packet.docx"
python3 "$here/make_reference_docx.py" --page "$work/AIDaS_SEED_2027_packet.docx"
soffice --headless --convert-to pdf --outdir "$work" "$work/AIDaS_SEED_2027_packet.docx" > /dev/null 2>&1
cp "$work/AIDaS_SEED_2027_packet.pdf" "$here/AIDaS_SEED_2027_packet.pdf"
pdfinfo "$here/AIDaS_SEED_2027_packet.pdf" | grep -E "^Pages"
echo "wrote $here/AIDaS_SEED_2027_packet.pdf"
