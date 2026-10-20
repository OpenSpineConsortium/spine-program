r"""Patch fill_idf.py with Greg's final facts (2026-09-25 ~12:15) and regenerate the form from a fresh unpack of the original."""
import re, subprocess, sys, zipfile, os, shutil
from pathlib import Path
HERE = Path(__file__).resolve().parent
SRC = HERE / "fill_idf.py"
s = SRC.read_text(encoding="utf-8")

def rep(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new, 1)

# --- co-inventors: none
rep('set_cell(2, 2, 0, ["[CONFIRM: Loren Schwiebert, PhD (WSU Computer Science) -- list only if he contributed to the inventive concept, not "\n                   "only as faculty sponsor]"])\nset_cell(2, 2, 1, ["[CONFIRM role -- or delete this row]"])\n',
    '')
rep('set_cell(2, 3, 0, ["[CONFIRM: Miraziz Ismoilov, MD and Nizar Alnabahneh, MD (WSU Radiology residents, PGY-2): produced the reference "\n                   "reads of transitional anatomy; list as inventors only if they contributed to the inventive concept]"])\nset_cell(2, 3, 1, ["Two-reader consensus Castellvi grading used as reference labels (data annotation)."])\n',
    '')
rep('set_cell(3, 1, 0, ["[CONFIRM: Patrick Schwing -- non-WSU co-author of the NeurIPS 2026 paper; list only if he contributed to the invention; "\n                   "give institution]"])\nset_cell(3, 1, 1, ["[CONFIRM role -- or delete this row]"])\n',
    'set_cell(3, 1, 0, ["None. The sole inventor is the WSU-affiliated submitter above; co-authors of the related papers contributed data annotation, "\n                   "manuscript review or mentorship, not to the inventive concept."])\n')
rep('the software; lead inventor."', 'the software; sole inventor."')
rep('"Part A (CT-side detection of transitional/count anomalies): conceived early 2026 [FILL: month]; disagreement-between-"',
    '"Part A (CT-side detection of transitional/count anomalies): conceived spring 2026, before the June presentation; disagreement-between-"')
# --- external affiliation: DMC contract has no IP clause; contributions 100 / 0
rep('set_cell(4, 1, 1, ["Detroit Medical Center (Tenet Healthcare Corporation): the lead inventor is a resident physician in the Department of "\n                   "Surgery under a DMC/Tenet employment contract. [CONFIRM whether that contract carries an invention-assignment "\n                   "obligation; attach the clause.] Student co-authors of the research programme are affiliated with WSU, Emory, Henry "\n                   "Ford Health and Children\'s Healthcare of Atlanta; none is listed as an inventor here."])',
    'set_cell(4, 1, 1, ["Detroit Medical Center (employer of record: Detroit Education and Research; Tenet Healthcare Corporation): the inventor is a "\n                   "resident physician in the Department of Surgery under a Graduate Medical Education Agreement (effective 1 July 2026). "\n                   "That agreement contains no intellectual-property or invention-assignment clause; its section 10 is a confidentiality "\n                   "clause covering the agreement\'s terms and proprietary information provided by the employer. No DMC resource, data or "\n                   "patient information was used for the invention."])')
rep('set_cell_raw(4, 2, 1, run("[FILL] ", RPR_LINE))\nset_cell_raw(4, 2, 3, run("[FILL] ", RPR_LINE))',
    'set_cell_raw(4, 2, 1, run("100 ", RPR_LINE))\nset_cell_raw(4, 2, 3, run("0 ", RPR_LINE))')
# --- university support: the inventor did all the work; WSU provided compute and storage only
rep('"(Department of Computer Science). No WSU salary support; no TDI/MTRAC funding. [CONFIRM]"',
    '"(Department of Computer Science). The inventor performed all of the work himself; WSU\'s contribution was compute and storage on "\n                    "the Grid. No WSU salary support; no TDI/MTRAC funding."')
# --- funding blanks: sponsor
rep('"  Gregory John Schwing (fellow); sponsor [FILL: F30 sponsor name]        [FILL: phone]"',
    '"  Gregory John Schwing (fellow, PI of record)        504-994-0403"')
# --- employment statement
rep('"Department of Surgery, throughout the work; statement of particulars to be attached. [CONFIRM dates]"',
    '"Department of Surgery, from 1 July 2026 under a Graduate Medical Education Agreement (the earliest work, April-June 2026, "\n                    "preceded that appointment, during the final months of medical school and the F30 fellowship). The agreement carries no "\n                    "invention-assignment clause."')
# --- conception dates: AACA date; CNS
rep('(presented June 2026). Part B (level naming from local morphology on a "', '(presented Saturday 13 June 2026 at the AACA Tech Fair). Part B (level naming from local morphology on a "')
# --- public disclosure entries
rep('"(b) Twelve abstracts accepted to the 2026 Congress of Neurological Surgeons annual meeting, including the single-shot CT detection of "\n "count anomalies (\'Not All Spines Are Created Equal\', mini-oral) [FILL: meeting date; whether abstracts are already published online].",',
    '"(b) Abstracts accepted to the 2026 Congress of Neurological Surgeons annual meeting (Washington, DC), including the single-shot CT "\n "detection of count anomalies (\'Not All Spines Are Created Equal\', mini-oral, scheduled 2 November 2026; slides not yet submitted; "\n "accepted abstracts are published in the meeting\'s abstract supplement).",')
rep('"(c) \'Harnessing Algorithmic Disagreement for Automated LSTV Detection\', Tech Fair presentation, 43rd AACA annual meeting, June 2026 "\n "[FILL: exact date] -- discloses disagreement-between-algorithms as a detection signal.",',
    '"(c) \'Harnessing Algorithmic Disagreement for Automated Lumbosacral Transitional Vertebrae Detection\', Tech Fair presentation and "\n "hands-on demonstration, 43rd AACA annual meeting, Mayo Clinic, Rochester MN, Saturday 13 June 2026 (slides attached): a CT pipeline "\n "in which two segmentation models\' level disagreement names the phenotype, with Castellvi typing from transverse-process height and "\n "gap and an open-source repository named on the closing slide -- this discloses the disagreement-as-signal mechanism and those "\n "geometric heuristics; it does not disclose Part A\'s name-free classifier or Part B.",')
rep('"Planned: manuscript on Part B to Radiology: Artificial Intelligence [FILL: intended submission date, about October 2026]; "\n                    "CNS 2026 presentations [FILL: dates]. These can be held until a provisional application is filed if the office so advises."',
    '"Planned: (1) the Part B manuscript (Radiology: Artificial Intelligence) is complete and is being HELD from submission until this "\n                    "office advises -- it is the first disclosure of Part B (a copy accompanies this form); (2) the NeurIPS 2026 camera-ready will be "\n                    "published in the proceedings about one month before the December conference (~November 2026) -- dataset and segmenter audit, "\n                    "as in (a); (3) CNS 2026 mini-oral, 2 November 2026, CT-side count anomalies; (4) the dataset article (Medical Physics) is "\n                    "being submitted -- dataset only, no method of this disclosure."')
# --- submitter info
rep('"Name  Gregory John Schwing                                    Citizenship: [FILL]                "',
    '"Name  Gregory John Schwing                                    Citizenship: United States (born in the U.S.)   "')
rep('append_to_para(353, "  [FILL if applicable]")', 'append_to_para(353, "  not applicable (U.S. citizen)")')
rep('"Student Status  [CONFIRM WSU appointment/status]     "', '"Student Status  Resident physician (WSU School of Medicine affiliate; employed by DMC)     "')
rep('"WSU Address  [FILL]                                  "', '"WSU Address  Department of Surgery, Wayne State University School of Medicine, Detroit, MI 48201  "')
rep('replace_label_text(358, "Phone                 ", "Phone  [FILL]")', 'replace_label_text(358, "Phone                 ", "Phone  504-994-0403")')
rep('"Home Address  [FILL -- required for patent filings]  "', '"Home Address  206 Josephine Ave, Royal Oak, MI 48067-2217, United States  "')
rep('replace_label_text(359, "Phone                 ", "Phone  [FILL]")', 'replace_label_text(359, "Phone                 ", "Phone  504-994-0403")')
# --- royalty: sole inventor
rep('set_cell(27, 0, 0, ["Gregory John Schwing [CONFIRM sole inventor]"])', 'set_cell(27, 0, 0, ["Gregory John Schwing (sole inventor)"])')
rep('set_cell(17, 0, 0, ["Interested in forming a company to commercialise the technology; none formed. [CONFIRM]"])',
    'set_cell(17, 0, 0, ["Interested in forming a company to commercialise the technology; none formed."])')
SRC.write_text(s, encoding="utf-8")
print("fill_idf.py patched; remaining markers:", len(re.findall(r"\[(?:FILL|CONFIRM)[^\]]*\]", s)))
for m in re.findall(r"\[(?:FILL|CONFIRM)[^\]]*\]", s): print("   ", m)

# --- regenerate from the original form
unp = HERE / "unpacked"
if unp.exists(): shutil.rmtree(unp)
zipfile.ZipFile(str(HERE.parent / "Modified WSU invention_disclosure_form 2026.docx")).extractall(str(unp))
merge = Path(r"C:\Users\grego\.claude\skills\synced\e84b423f-5f43-41e5-92ba-e004e5534a25_68447606-b425-40e9-a098-6d113b058eb4\docx\scripts\merge_runs.py")
subprocess.run([sys.executable, str(merge), str(unp)], check=True)
subprocess.run([sys.executable, str(SRC)], check=True)
# the royalty "%": rebuild that cell to "100 %" (as before)
p = unp / "word" / "document.xml"; x = p.read_text(encoding="utf-8")
tbls = list(re.finditer(r"<w:tbl>.*?</w:tbl>", x, flags=re.S)); t = tbls[27]; tbl = t.group(0)
rows = list(re.finditer(r"<w:tr[ >].*?</w:tr>", tbl, flags=re.S)); r = rows[0]
cells = list(re.finditer(r"<w:tc>.*?</w:tc>", r.group(0), flags=re.S)); c = cells[1]; cell = c.group(0)
tcpr = re.match(r"<w:tc>(<w:tcPr>.*?</w:tcPr>)", cell, flags=re.S).group(1)
first_p = re.search(r"<w:p[ >].*?</w:p>", cell, flags=re.S).group(0)
head = re.match(r"<w:p[^>]*>", first_p).group(0); ppr = re.search(r"<w:pPr>.*?</w:pPr>", first_p, flags=re.S)
runx = '<w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:color w:val="0000FF"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr><w:t xml:space="preserve">100 %</w:t></w:r>'
new_cell = "<w:tc>" + tcpr + head + (ppr.group(0) if ppr else "") + runx + "</w:p></w:tc>"
new_row = r.group(0)[:c.start()] + new_cell + r.group(0)[c.end():]
x = x[:t.start()] + tbl[:r.start()] + new_row + tbl[r.end():] + x[t.end():]
p.write_text(x, encoding="utf-8")
out = HERE.parent / "WSU_Invention_Disclosure_Schwing_2026-09-25.docx"
if out.exists(): out.unlink()
z = zipfile.ZipFile(str(out), "w", zipfile.ZIP_DEFLATED)
for root, _, files in os.walk(unp):
    for f in files:
        fp = os.path.join(root, f); z.write(fp, os.path.relpath(fp, unp).replace(os.sep, "/"))
z.close()
print("regenerated", out)
