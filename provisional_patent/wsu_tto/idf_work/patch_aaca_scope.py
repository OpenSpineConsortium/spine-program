r"""Greg 2026-09-25 ~13:50: the AACA Tech Fair pipeline was built from third-party segmenters and is a separate project ->
the disagreement mechanism leaves the CLAIMED invention; AACA stays listed as a related public presentation that disclosed
neither Part A (name-free classifier) nor Part B. Regenerates the form from the original."""
import subprocess, sys, zipfile, os, shutil, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
SRC = HERE / "fill_idf.py"
s = SRC.read_text(encoding="utf-8")
def rep(old, new):
    global s
    assert s.count(old) == 1, old[:90]
    s = s.replace(old, new, 1)
# Part A description: drop the two mechanisms that are public (AACA disagreement idea; NeurIPS oversampling)
rep(' "outside the field of view, and an \'unusual spine\' score. Two further mechanisms belong to it: disagreement between independently trained "\n'
    ' "segmenters used as the detection signal, and transitional-aware oversampling that repairs the class-imbalance failure of standard "\n'
    ' "segmenter training.",',
    ' "outside the field of view, and an \'unusual spine\' score.",')
rep(' "segmenter-agnostic, name-free CT flag; ensemble disagreement as an anomaly detector. Unexpected: naming accuracy on an unseen C-arm "',
    ' "segmenter-agnostic, name-free CT flag. Unexpected: naming accuracy on an unseen C-arm "')
rep('set_cell(6, 0, 0, ["Combination: new processes/methods (name-free transitional-phenotype classification from segmentations; ensemble-"\n'
    '                   "disagreement detection; transitional-aware oversampling; level naming from local morphology coupled with a count and "\n'
    '                   "abstention; render-based per-device training) embodied in software (trained neural-network weights, training and "\n'
    '                   "inference code, per-device image-formation parameters)."])',
    'set_cell(6, 0, 0, ["Combination: new processes/methods (name-free transitional-phenotype classification from segmentations; level "\n'
    '                   "naming from local morphology coupled with a count and abstention; render-based per-device training) embodied in "\n'
    '                   "software (trained neural-network weights, training and inference code, per-device image-formation parameters)."])')
# conception dates: no AACA item in the invention's timeline
rep('set_cell(9, 0, 0, ["Part A (CT-side detection of transitional/count anomalies): conceived spring 2026, before the June presentation; disagreement-between-"\n'
    '                   "segmenters as the detection signal: spring 2026 (presented Saturday 13 June 2026 at the AACA Tech Fair). Part B (level naming from local morphology on a "',
    'set_cell(9, 0, 0, ["Part A (name-free transitional-phenotype classifier on CT segmentations): the CT-side count-anomaly work began spring 2026; the "\n'
    '                   "name-free, segmenter-agnostic classifier as claimed was designed on 24-25 September 2026. Part B (level naming from local morphology on a "')
# public disclosure (c): AACA is a separate project built from third-party segmenters
rep(' "(c) \'Harnessing Algorithmic Disagreement for Automated Lumbosacral Transitional Vertebrae Detection\', Tech Fair presentation and "\n'
    ' "hands-on demonstration, 43rd AACA annual meeting, Mayo Clinic, Rochester MN, Saturday 13 June 2026 (slides attached): a CT pipeline "\n'
    ' "in which two segmentation models\' level disagreement names the phenotype, with Castellvi typing from transverse-process height and "\n'
    ' "gap and an open-source repository named on the closing slide -- this discloses the disagreement-as-signal mechanism and those "\n'
    ' "geometric heuristics; it does not disclose Part A\'s name-free classifier or Part B.",',
    ' "(c) \'Harnessing Algorithmic Disagreement for Automated Lumbosacral Transitional Vertebrae Detection\', Tech Fair presentation and "\n'
    ' "hands-on demonstration, 43rd AACA annual meeting, Mayo Clinic, Rochester MN, Saturday 13 June 2026 (slides attached): a separate, "\n'
    ' "earlier project -- an LSTV screening pipeline assembled from third-party open-source segmenters (TotalSpineSeg, SPINEPS/VERIDAH) whose "\n'
    ' "level disagreement flags the phenotype, with Castellvi heuristics -- released as open source. It is listed for completeness; it does "\n'
    ' "not disclose Part A\'s name-free classifier or Part B, neither of which existed then, and neither claim relies on that mechanism.",')
SRC.write_text(s, encoding="utf-8")
print("fill_idf.py patched for the AACA scope")

# regenerate from the original
unp = HERE / "unpacked"
if unp.exists(): shutil.rmtree(unp)
zipfile.ZipFile(str(HERE.parent / "Modified WSU invention_disclosure_form 2026.docx")).extractall(str(unp))
merge = Path(r"C:\Users\grego\.claude\skills\synced\e84b423f-5f43-41e5-92ba-e004e5534a25_68447606-b425-40e9-a098-6d113b058eb4\docx\scripts\merge_runs.py")
subprocess.run([sys.executable, str(merge), str(unp)], check=True)
subprocess.run([sys.executable, str(SRC)], check=True)
p = unp / "word" / "document.xml"; x = p.read_text(encoding="utf-8")
tbls = list(re.finditer(r"<w:tbl>.*?</w:tbl>", x, flags=re.S)); t = tbls[27]; tbl = t.group(0)
rows = list(re.finditer(r"<w:tr[ >].*?</w:tr>", tbl, flags=re.S)); r = rows[0]
cells = list(re.finditer(r"<w:tc>.*?</w:tc>", r.group(0), flags=re.S)); c = cells[1]; cell = c.group(0)
tcpr = re.match(r"<w:tc>(<w:tcPr>.*?</w:tcPr>)", cell, flags=re.S).group(1)
first_p = re.search(r"<w:p[ >].*?</w:p>", cell, flags=re.S).group(0)
head = re.match(r"<w:p[^>]*>", first_p).group(0); ppr = re.search(r"<w:pPr>.*?</w:pPr>", first_p, flags=re.S)
runx = '<w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:color w:val="0000FF"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr><w:t xml:space="preserve">100 %</w:t></w:r>'
new_cell = "<w:tc>" + tcpr + head + (ppr.group(0) if ppr else "") + runx + "</w:p></w:tc>"
x = x[:t.start()] + tbl[:r.start()] + r.group(0)[:c.start()] + new_cell + r.group(0)[c.end():] + tbl[r.end():] + x[t.end():]
p.write_text(x, encoding="utf-8")
out = HERE.parent / "WSU_Invention_Disclosure_Schwing_2026-09-25.docx"
if out.exists(): out.unlink()
z = zipfile.ZipFile(str(out), "w", zipfile.ZIP_DEFLATED)
for root, _, files in os.walk(unp):
    for f in files:
        fp = os.path.join(root, f); z.write(fp, os.path.relpath(fp, unp).replace(os.sep, "/"))
z.close()
print("regenerated", out.name)
