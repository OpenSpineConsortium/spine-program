// Builds the Word document of the inventor's responses to counsel.
// Usage: node build.js <figures dir> <output .docx>
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ExternalHyperlink, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, ImageRun, Header, Footer,
  PageNumber, TableOfContents, PageBreak, LevelFormat,
} = require("docx");
const { L, c } = require("./content.js");
const SECTIONS = require("./answers.js");

const [FIGDIR, OUT] = process.argv.slice(2);
const FONT = "Calibri";
const NAVY = "1F3A5F", GREY = "52514E", RULE = "BFBFBF";
const PAGE_W = 12240, MARGIN = 1260, BODY_W = PAGE_W - 2 * MARGIN; // 9720 DXA = 6.75 in

const STATUS = {
  SHOWN: ["Shown in the repository", "1F6F43", "E3F2E9"],
  RENDER: ["Shown on renders or synthetic data only", "7A5300", "FBF1D9"],
  INFERRED: ["Inferred: inventor's judgement, not tested", "1F3A5F", "E4ECF5"],
  NOTREC: ["Not recorded", "8A2E1F", "F8E3DE"],
  DESIGN: ["Design only", "5A3E85", "ECE6F5"],
};

// ---------- inline markup: **bold**, *italic*, [text](url)
function runs(text, base = {}) {
  const out = [];
  const re = /\*\*(.+?)\*\*|\*(.+?)\*|\[([^\]]+)\]\((https?:[^)]+)\)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    if (m[1] !== undefined) out.push(...runs(m[1], { ...base, bold: true }));
    else if (m[2] !== undefined) out.push(new TextRun({ text: m[2], ...base, italics: true }));
    else out.push(link(m[3], m[4], base));
    last = re.lastIndex;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}
const link = (text, url, base = {}) => new ExternalHyperlink({
  link: url, children: [new TextRun({ text, ...base, style: "Hyperlink" })],
});

const p = (text, opts = {}) => new Paragraph({ children: runs(text, opts.run || {}),
  spacing: { after: 120, line: 276 }, ...opts.para });
const bullet = (text) => new Paragraph({ children: runs(text), numbering: { reference: "bul", level: 0 },
  spacing: { after: 80, line: 264 } });
const h1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)], pageBreakBefore: true });
const h1nb = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });
const h2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)], keepNext: true });

// ---------- tables
const border = { style: BorderStyle.SINGLE, size: 4, color: RULE };
const borders = { top: border, bottom: border, left: border, right: border };
function table(widths, rows, header = true) {
  const total = widths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: widths,
    rows: rows.map((r, i) => new TableRow({
      tableHeader: header && i === 0,
      children: r.map((cell, j) => new TableCell({
        borders, width: { size: widths[j], type: WidthType.DXA },
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        shading: header && i === 0 ? { type: ShadingType.CLEAR, fill: "1F3A5F", color: "auto" } : undefined,
        children: [].concat(cell).map(t => new Paragraph({ spacing: { after: 40 },
          children: runs(t, header && i === 0 ? { bold: true, color: "FFFFFF", size: 19 } : { size: 19 }) })),
      })),
    })),
  });
}

// ---------- figures
function pngSize(file) {
  const b = fs.readFileSync(file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}
const FIGS = {
  1: ["fig1_three_framings.png", "Three framings of one programme. The WSU disclosure has Parts A and B; the draft provisional describes a third invention, the chain, which the disclosure form does not mention. Sources: 00_README_for_TTO.md; CLASSIFIERS.md R33; 01 STATUS.md."],
  2: ["fig2_acquisition_geometry.png", "Acquisition geometry, schematic. Each exposure spans S at the spine and overlaps the previous one by O bodies; the commanded step is S - O x p, with p the vertebral spacing measured in the image. After SPECIFICATION.md [0031]-[0036]."],
  3: ["fig3_asymmetric_window.png", "Why the window is bounded, illustrative curve (not data). The spine is nearly periodic, so similarity has competing peaks one vertebra either side of the true displacement. The search is confined to -0.5 to +0.6 of a spacing about the commanded step."],
  4: ["fig4_alphabets.png", "Alternative alphabets. Each is a complete admissible ordering of level names drawn from one output space; a naming must be a contiguous run pinned at the landmark. The four-lumbar alphabet was added after the draft (commit 4fb9d64)."],
  5: ["fig5_remedy_flow.png", "Which remedy is commanded. The geometric term is checked first; a low appearance term gets a full step toward the landmark; a refusal ends an escalation that cannot add new anatomy. Source: acquisition.py _decide."],
  6: ["fig6_overlap_ladder.png", "Chains completed against overlap, 120 held-out CT renders, 9-inch field, sweep_v3 (job 40384843), true boxes. RECORD ONLY. Replaces the 801-subject figures in [0035]. Source: sweep-map-replaces-registration.md; RESULTS_CATALOG.md C3.4."],
  7: ["fig7_window_ablation.png", "Window ablation (commit a644897). Widening the search window leaves counting 98.9 to 100 per cent exact, so the window is not the mechanism; it removes the last wrong walks. True boxes, renders. Source: COUNTING_EVIDENCE.md."],
  8: ["fig8_chain_gain.png", "Frames with two bodies named from the image alone and after registration onto the chain, held out, sweep_v3, true boxes. RECORD ONLY. These replace the figures in [0076]. Source: sweep-map-replaces-registration.md; RESULTS_CATALOG.md C3.1-C3.3."],
};
function figure(n) {
  const [file, caption] = FIGS[n];
  const f = path.join(FIGDIR, file);
  const { w, h } = pngSize(f);
  const width = 600, height = Math.round(600 * h / w);
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 120, after: 60 },
      children: [new ImageRun({ type: "png", data: fs.readFileSync(f), transformation: { width, height },
        altText: { title: `Figure ${n}`, description: caption, name: `Figure ${n}` } })] }),
    new Paragraph({ spacing: { after: 200 }, children: [
      new TextRun({ text: `Figure ${n}. `, bold: true, size: 18, color: GREY }),
      ...runs(caption, { size: 18, color: GREY })] }),
  ];
}

// ---------- one question
function statusTag(key) {
  const [label, color, fill] = STATUS[key];
  return new Paragraph({ spacing: { before: 60, after: 100 },
    children: [new TextRun({ text: " " + label.toUpperCase() + " ", bold: true, size: 16, color,
      shading: { type: ShadingType.CLEAR, fill, color: "auto" } })] });
}
function question(q) {
  const out = [];
  out.push(h2(`Question ${q.n}   ${q.ref}`));
  out.push(new Paragraph({ spacing: { after: 100, line: 264 }, indent: { left: 240 },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: NAVY, space: 8 } },
    shading: { type: ShadingType.CLEAR, fill: "F3F5F8", color: "auto" },
    children: runs(q.q, { italics: true, color: "333333", size: 20 }) }));
  out.push(statusTag(q.status));
  q.a.forEach(t => out.push(p(t)));
  if (q.d && q.d.length) {
    out.push(new Paragraph({ spacing: { before: 60, after: 60 }, keepNext: true,
      children: [new TextRun({ text: "Drafting suggestion", bold: true, color: NAVY })] }));
    q.d.forEach(t => out.push(bullet(t)));
  }
  if (q.s && q.s.length) {
    const kids = [new TextRun({ text: "Sources: ", bold: true, size: 18, color: GREY })];
    q.s.forEach((s, i) => { if (i) kids.push(new TextRun({ text: "; ", size: 18, color: GREY })); kids.push(link(s[0], s[1], { size: 18 })); });
    out.push(new Paragraph({ spacing: { before: 60, after: 200 }, children: kids }));
  }
  [].concat(q.fig || []).forEach(n => out.push(...figure(n)));
  return out;
}

// ---------- front matter
const body = [];
body.push(new Paragraph({ spacing: { before: 2400, after: 120 }, children: [new TextRun({ text: "PRIVILEGED AND CONFIDENTIAL", bold: true, color: "8A2E1F", size: 20 })] }));
body.push(new Paragraph({ spacing: { after: 360 }, children: [new TextRun({ text: "Attorney-client communication, prepared at the request of counsel. Not for filing or distribution.", color: GREY, size: 20 })] }));
body.push(new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Inventor's Responses to Counsel's Questions")] }));
body.push(new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: "WSU 26-1902  |  FS 66174-0372  |  Provisional application: vertebral level determination from limited-field projection images", size: 24, color: NAVY })] }));
body.push(table([2600, BODY_W - 2600], [
  ["Inventor", "Gregory J. Schwing, MD, PhD, Department of Surgery (General Surgery), Wayne State University School of Medicine / Detroit Medical Center"],
  ["Prepared for", "Meeting with patent counsel on preparing the provisional application"],
  ["Date", "20 October 2026"],
  ["Answers to", "\"WSU 26-1902 FS 66174-0372 Questions to Inventor\" (60 questions)"],
  ["Based on", "The draft provisional (SPECIFICATION.md, CLAIMS.md of 18 September 2026), the WSU disclosure package of 25 September 2026, and the code and result records of the research repositories, read at fixed commits (spine-program 240cabc; spinesurg-ct-nnunet 0ab783f)"],
], false));
body.push(new Paragraph({ children: [new PageBreak()] }));
body.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Contents")] }));
[["1.", "What counsel should know first"], ["2.", "Numbers in the draft to replace before filing"], ["3.", "Answers to the 60 questions"]]
  .concat(SECTIONS.map((s, i) => [`3.${i + 1}`, `${s.title} (Q${s.items[0].n}-${s.items[s.items.length - 1].n})`]))
  .concat([["A.", "Subject matter added after the draft"], ["B.", "References for the information disclosure statement"], ["C.", "Open items for the meeting"]])
  .forEach(([k, t]) => body.push(new Paragraph({ spacing: { after: 80 }, indent: { left: k.includes(".") && k.length > 2 && k[0] === "3" ? 400 : 0 },
    children: [new TextRun({ text: k + "  ", bold: true, color: NAVY }), new TextRun(t)] })));

// ---------- executive summary
body.push(h1("1. What counsel should know first"));
body.push(p("Most answers are routine: ranges, alternatives and examples to widen the specification. Nine points change what is filed or when, and they are listed here in order of consequence."));
const EXEC = [
  "**The draft provisional does not describe Part A, and the WSU disclosure does not describe the draft.** The draft (18 September) is a third invention: overlapping C-arm exposures linked into a chain, alternative alphabets, a confidence that commands the next move, and a persistent digital marker. The disclosure form (25 September) covers Part A (preoperative CT) and Part B (single C-arm exposure) and never mentions a chain, overlap or sweep. A supplemental disclosure to WSU should cover the chain (Q1, Figure 1).",
  "**Part A is design only.** Its features are extracted on 3,524 CT and segmenter pairs, but no classifier has been trained. I recommend it go in a later provisional (Q1).",
  "**The measured numbers in the draft must be replaced before filing.** On the morning of 18 September, 681 of the 801 render subjects were found to be in the naming network's training set (commit d6f407a); the draft, written that evening, still carries those numbers. On 19 September every earlier render was found to have the wrong field size. Section 2 lists each affected paragraph with its corrected, held-out value. The claims recite no accuracy, so this is a support and candour matter, not a claim matter.",
  "**Three statements of mechanism or result are now known to be overstated.** [0048]: widening the search window barely changes counting, so the window is not the mechanism (Q20, Figure 7). [0073]: the reduced-resolution search has not been shown to lose nothing; a real-frame check disagreed (Q42). [0083a]: on a later phantom about one in four asserted marker positions still fell on the neighbouring vertebra (Q47).",
  "**Subject matter invented after the draft should be added** while the provisional is still unfiled: a fifth alphabet (four lumbar), the C2 anchor class, the end rule (\"the last move is a full move or none\"), the global link solve, masked correlation for a round receptor, an end-plate filter, a pixel-spacing guard, needle confirmation and the start-from-target workflow (Appendix A).",
  "**[0071c] refers to the wrong paragraph.** The return to the operative field belongs to the start-from-target mode, which the specification never describes. It should get its own section, since claim 4 depends on it (Q37).",
  "**Closest prior art for the IDS:** SX-Stitch (arXiv:2409.05681, overlapping intraoperative C-arm images stitched, no naming) and US 8,718,346 (NuVasive; stitched C-arm composite with labels placed by hand), with the LevelCheck family and its patents for registration (Q2, Q3, Appendix B).",
  "**Timing.** Nothing public discloses the chain (DISCLOSURE_MEMO.md). Four things must wait for the filing: the Part B manuscript (held), a data request to the SX-Stitch authors (drafted, not sent, and it describes the method), older manuscript drafts and a QI paper that describe the sweep (unsubmitted), and any CNS talk content beyond the cleared public deck (talk on 2 November 2026). The memo also recommends exporting the GitHub audit log before filing.",
  "**No real overlapping intraoperative series has been tested.** Part B has real C-arm results (in the manuscript); the chain does not. A phantom or cadaver sweep on a hospital C-arm is the fastest addition before the non-provisional (Q5).",
];
EXEC.forEach((t, i) => body.push(new Paragraph({ numbering: { reference: "num", level: 0 }, spacing: { after: 100, line: 268 }, children: runs(t) })));
body.push(...figure(1));

body.push(h2("How to read the answers"));
body.push(p("Each answer carries one status tag, so counsel can see at a glance what the record supports:"));
body.push(table([3400, BODY_W - 3400], [
  ["Tag", "Meaning"],
  ["Shown in the repository", "Implemented in code, or measured with a recorded result file"],
  ["Shown on renders or synthetic data only", "Measured, but on CT renders, a synthetic subject or a phantom; not on real intraoperative images"],
  ["Inferred: inventor's judgement, not tested", "My technical view, offered to widen the specification; no code or measurement behind it"],
  ["Not recorded", "No file records the fact asked for"],
  ["Design only", "Written down as a plan; not built"],
]));
body.push(p(""));
body.push(p("**Links.** Source links point to two private GitHub repositories at fixed commits (OpenSpineConsortium/spine-program and the inventor's spinesurg-ct-nnunet). They open only for an account given access. If counsel prefers, I can supply any linked file as an excerpt instead of granting access. Numbers marked RECORD ONLY are held-out results on renders with the annotation's boxes; they support the description and are not for marketing claims."));
body.push(p("**Ranges.** Where a question asks for a working range, the value actually used is stated first; the range around it is my judgement unless the answer says it was measured."));

// ---------- numbers to replace
body.push(h1("2. Numbers in the draft to replace before filing"));
body.push(p("Two corrections reach most measured statements in the draft. (1) Training-set overlap: 681 of the 801 render subjects, 145 of 170 real radiographs and 64 of 76 whole-spine subjects had been seen by the naming network (commit d6f407a, 18 September, 07:50). (2) The row-spacing defect: every render sweep before sweep_v3 (19 September, job 40384843) used the wrong field size. Only sweep_v3 results, on the subjects held out from the network, count."));
body.push(table([1100, 3000, 2400, BODY_W - 6500], [
  ["Para.", "Draft says", "Problem", "Use instead"],
  ["[0035]", "801 subjects; 86.6 / 93.6 / 95.1 / 95.2 / 93.2 % at O = 0.5 to 4; chains 94.2 to 80.4 %", "Training-set overlap; wrong field size", "Chains completed on 120 held-out renders: 81.7 (0.5), 95.8 (1), 91.7 (1.5), 97.5 (2), 96.7 (2.5), 90.8 (3), 82.5 % (4). Figure 6"],
  ["[0036]", "2.5 / 2.6 / 3.0 / 6.9 exposures", "Same", "3.4 exposures at O = 2 (120 held out); with the end rule 120 of 120 chains complete"],
  ["[0053]", "Detector missed 2.2 %; 17.9 % entered twice (real radiographs)", "Real films, so no field-size defect; result file not named in the record", "Keep only if the file is found; otherwise state the effect without numbers"],
  ["[0063]", "85.8 % per node versus 95.5 % decoded (9.7 points)", "18-September corpus", "Re-run on sweep_v3 or state without numbers"],
  ["[0070]", "4,792 frames; 95.7 versus 95.3 %; 42 versus 82 %", "18-September corpus; result file not named", "See Q34: re-run, or keep the reasoning only"],
  ["[0076]", "69.6 to 95.1 %, 85.9 to 95.0 %, 91.2 to 95.7 %; 31.1 to 99.3 % on 76 subjects; nine transitional subjects all correct", "Training-set overlap; wrong field size", "120 held-out renders: 72.1 to 95.2 (2 bodies), 86.8 to 94.7 (3), 90.2 to 94.8 % (4). 12 held-out whole spines from C2: 9.5 to 100, 25 to 100, 30 to 100 %. Figure 8"],
  ["[0083a]", "Every asserted marker position fell on the marked vertebra", "One synthetic subject; a later phantom left about 1 in 4 on the neighbour", "Report as synthetic, or drop the numbers"],
  ["[0084], [0007]", "179 placements, 52 minutes, 183 mGy", "Correct, uncited", "Cite Siminski et al. 2023 (Q4)"],
  ["[0087]", "2.29 and 22.94 ms (GPU); 18.30 and 330.58 ms (CPU); later stages untimed", "Older benchmark of older models; later stages now timed", "Model card 6.3 timings with their limits (Q49)"],
]));
body.push(p(""));
body.push(p("Counting along the chain with correct boxes, which needs no network, gives the strongest current evidence: 834 of 834 walks from C2 on 76 whole spines; 99.66 per cent of 6,255 walks on 801 renders; and 1,204 of 1,209 walks (99.67 per cent) on 262 real cervical films (COUNTING_EVIDENCE.md). With detector boxes on renders it falls to 30.06 per cent: detection, not linking, is the binding constraint, which matters for how the product is described but not for the claims."));
body.push(...figure(8));

// ---------- answers
body.push(h1("3. Answers to the 60 questions"));
body.push(p("Grouped as in counsel's list. The question text is counsel's, sometimes shortened."));
SECTIONS.forEach((s, i) => {
  body.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(`3.${i + 1} ${s.title}`)], pageBreakBefore: i > 0 }));
  s.items.forEach(q => body.push(...question(q)));
});

// ---------- appendices
body.push(h1("Appendix A. Subject matter added after the draft"));
body.push(p("Each item is dated by a commit in the private code repository (spinesurg-ct-nnunet). All post-date the draft of 18 September and none is in it. Because the provisional has not been filed, these can go into it directly."));
const A = [
  ["4fb9d64", "19 Sep", "Fifth alphabet: four lumbar bodies (sacralised L5), and four lumbar with T13 (--alphabets ext)"],
  ["f956dae", "19 Sep", "C2 detector class: the cranial landmark found as the sacrum is; anchor by class or refuse"],
  ["8aac5b7", "19 Sep", "End rule (refuse a final move under half a body) and open last link; chains 97.5 to 120 of 120"],
  ["7325682", "19 Sep", "Soft rib term in the alphabet decoder (measured: adds nothing; a fallback)"],
  ["23fb7f3", "19 Sep", "Node merge and position ordering (opt-in)"],
  ["a644897", "20 Sep", "Window ablation: what the bounded search is worth"],
  ["4f6f25b", "20 Sep", "Field width and magnification-mismatch sweep"],
  ["6a14981, 4176667", "20 Sep", "Masked correlation over the doubly exposed region; fixes for a round receptor"],
  ["ab903a4", "20 Sep", "Each link measured against the displacement that produced it; end-plate filter"],
  ["7508769", "20 Sep", "Guard against a silent default pixel pitch"],
  ["(acquisition.py)", "18 Sep onward", "Start-from-target mode and the return to the operative field (not in the specification text)"],
  ["(needle_confirm.py)", "by 20 Sep", "Needle confirmation: a later frame with a radiopaque needle assigned to the right vertebra on 99.31 % of 5,385 confirmations (renders), 84.58 % in the cervical spine"],
  ["(sweep_map.py)", "by 20 Sep", "Global link solve; Euclidean (ECC) refinement of a link (--place ecc)"],
];
body.push(table([1900, 1300, BODY_W - 3200], [["Commit", "Date", "What it adds"], ...A.map(r => [
  r[0].startsWith("(") ? r[0] : `[${r[0]}](https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet/commit/${r[0].split(",")[0]})`, r[1], r[2]])]));
body.push(p(""));
body.push(p("From the physics work (HANDOFF_PHYSICS.md), also worth describing: the step size is the main lever under realistic image physics (a half-body step reached 88.43 per cent), storing the exposure added 4.6 points, and the global solve added 5.5 points. Nine other linking fixes were tried and refuted; they should not be described as embodiments."));

body.push(h1("Appendix B. References for the information disclosure statement"));
[
  "Siminski et al. Preoperative fiducial marker placement for thoracic spine surgery. AJNR Am J Neuroradiol 2023;44(5):618-622. PMID 37080723; DOI 10.3174/ajnr.A7854. (Background, [0007].)",
  "Li Y, Gao H, He M, Liang J, Gu J, Liu W. SX-Stitch: an efficient VMS-UNet based framework for intraoperative scoliosis X-ray image stitching. arXiv:2409.05681, 2024.",
  "US 8,718,346 B2 (NuVasive, originally Saferay Spine): stitched C-arm composite with manually placed level labels.",
  "US 11,284,846 B2 (Siemens Healthineers, Johns Hopkins); US 10,368,956 B2 (Johns Hopkins); US 12,223,118 B2: registration of a preoperative volume to intraoperative images.",
  "Otake Y et al. 2012, Phys Med Biol (LevelCheck); Lo SL et al. 2015; De Silva T et al., Spine 2016 (PMID 27035579); msLevelCheck (PMID 28375139); LevelCheck clinical evaluation (PMID 25646750); MR-LevelCheck, Phys Med Biol 2017;62(2):684 (PMC5321067).",
  "Huang et al. 2022, Comput Methods Programs Biomed 227:107222 (O-arm long-film stitching with labels).",
  "Automated vertebra labelling on radiographs: Cina et al. 2021, Sci Rep 11:9482; VertXNet 2024; Kim et al. 2024; Konya et al. 2021.",
  "The inventor's own public items (NeurIPS 2026 paper; CTSpinoPelvic1K dataset on Zenodo and arXiv 2609.22760; AACA Tech Fair slides, 13 June 2026), listed in 06_disclosure_timeline.md, for counsel to judge.",
].forEach(t => body.push(bullet(t)));
body.push(p("Not yet done: the INPADOC family search for continuations of the four patents above."));

body.push(h1("Appendix C. Open items for the meeting"));
[
  "Which invention the first provisional covers: the chain alone, the chain with Part B, or all three (Q1).",
  "A supplemental WSU disclosure for the chain.",
  "Re-running the 18-September measurements on held-out sweep_v3 data, or filing those paragraphs without numbers (Section 2).",
  "Whether counsel needs repository access, or excerpts of the linked files.",
  "Confirming the disc-based convention (Q30) and the intended hardware (Q49).",
  "The order of filing and the held disclosures: the Part B manuscript, the SX-Stitch data request, the CNS talk of 2 November 2026.",
].forEach(t => body.push(bullet(t)));

// ---------- document
const doc = new Document({
  creator: "Gregory J. Schwing", title: "Inventor's Responses to Counsel's Questions, WSU 26-1902",
  description: "Privileged and confidential",
  styles: {
    default: { document: { run: { font: FONT, size: 21 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", run: { size: 44, bold: true, color: NAVY, font: FONT }, paragraph: { spacing: { after: 160 } } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, color: NAVY, font: FONT }, paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 23, bold: true, color: NAVY, font: FONT },
        paragraph: { spacing: { before: 280, after: 80 }, outlineLevel: 1,
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 2 } } } },
    ],
  },
  numbering: { config: [
    { reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
    { reference: "num", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 400, hanging: 400 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: 15840 }, margin: { top: 1260, bottom: 1260, left: MARGIN, right: MARGIN } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
      new TextRun({ text: "Privileged and Confidential  |  Attorney-Client Communication  |  WSU 26-1902", size: 16, color: "8A2E1F" })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: "Inventor's responses to counsel, 20 October 2026   |   Page ", size: 16, color: GREY }),
      new TextRun({ children: [PageNumber.CURRENT], size: 16, color: GREY }),
      new TextRun({ text: " of ", size: 16, color: GREY }),
      new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, color: GREY })] })] }) },
    children: body,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log("wrote", OUT, b.length); });
