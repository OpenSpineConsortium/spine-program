// Builds the cover memo that opens the package sent to counsel.
// Usage: node cover.js <package dir> <output .docx>
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, Header, Footer, PageNumber, LevelFormat,
} = require("docx");

const [PKG, OUT] = process.argv.slice(2);
const FONT = "Calibri", NAVY = "1F3A5F", GREY = "52514E", RULE = "BFBFBF";
const PAGE_W = 12240, MARGIN = 1260, BODY_W = PAGE_W - 2 * MARGIN;

function runs(text, base = {}) {
  const out = [], re = /\*\*(.+?)\*\*|\*(.+?)\*/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    if (m[1] !== undefined) out.push(new TextRun({ text: m[1], ...base, bold: true }));
    else out.push(new TextRun({ text: m[2], ...base, italics: true }));
    last = re.lastIndex;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}
const p = (t, run = {}) => new Paragraph({ children: runs(t, run), spacing: { after: 120, line: 276 } });
const bullet = (t) => new Paragraph({ children: runs(t), numbering: { reference: "bul", level: 0 },
  spacing: { after: 70, line: 264 } });
const num = (t) => new Paragraph({ children: runs(t), numbering: { reference: "num", level: 0 },
  spacing: { after: 90, line: 264 } });
const h1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)], keepNext: true });

const border = { style: BorderStyle.SINGLE, size: 4, color: RULE };
const borders = { top: border, bottom: border, left: border, right: border };
function table(widths, rows) {
  return new Table({
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths,
    rows: rows.map((r, i) => new TableRow({
      tableHeader: i === 0, cantSplit: true,
      children: r.map((cell, j) => new TableCell({
        borders, width: { size: widths[j], type: WidthType.DXA },
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        shading: i === 0 ? { type: ShadingType.CLEAR, fill: NAVY, color: "auto" } : undefined,
        children: [].concat(cell).map(t => new Paragraph({ spacing: { after: 40 },
          children: runs(t, i === 0 ? { bold: true, color: "FFFFFF", size: 18 } : { size: 18 }) })),
      })),
    })),
  });
}

// ---------- the contents index is read from the package itself, so it cannot drift from it
const DESCRIBE = {
  "00_READ_FIRST_Cover_Memo.docx": "This memo.",
  "01_Inventor_Responses_to_Counsel_2026-10-20.docx": "The inventor's answers to all 60 questions, with figures, a status tag on every answer and links to the evidence. Start here after this memo.",
  "02_Draft_Provisional/SPECIFICATION": "The draft specification of 18 September 2026 (the chain). Its measured numbers are invalid; section 2 of the responses lists the replacements.",
  "02_Draft_Provisional/CLAIMS": "Draft claims, for counsel to redraft; not intended to be filed as claims.",
  "02_Draft_Provisional/COVER_SHEET": "Data for form PTO/SB/16, for counsel to verify.",
  "02_Draft_Provisional/FILING_CHECKLIST": "The order of steps around the filing, as drafted. Not legal advice.",
  "02_Draft_Provisional/README": "What the draft package holds.",
  "03_Disclosure_Records/DISCLOSURE_MEMO": "Attorney work-product memo on prior public availability: the Hugging Face review Spaces, third-party records, and what was never public.",
  "03_Disclosure_Records/SCRUB_PLAN": "Review of 26 September 2026 that found Part A and Part B elements in public repositories; section 6 lists the corrections owed to the WSU package.",
  "03_Disclosure_Records/INVENTION_DISCLOSURE": "The earlier technical disclosure of the chain, with a freedom-to-operate table.",
  "03_Disclosure_Records/GUIDED_ACQUISITION": "Technical note on the commanded move and the persistent marker.",
  "03_Disclosure_Records/PATENT_PACKAGE": "Superseded; says where its content went. Kept for the record.",
  "03_Disclosure_Records/disclosure_forensics.json": "Raw third-party record checks of 18 September 2026 (GitHub public events, Wayback), cited by DISCLOSURE_MEMO.md section 5.",
  "03_Disclosure_Records/disclosure_evidence": "The exact bytes that were public on the review Spaces, with SHA-256 and the metadata captured while they were open.",
  "03_Disclosure_Records/github_purge_requests": "GitHub Support purge requests drafted on 26 September 2026, with the commit lists. Not recorded as filed.",
  "04_WSU_TTO_Package": "The package sent to the WSU technology transfer office on 25 September 2026, as sent: the README, the disclosure form (signed PDF and Word), the confidential Part B manuscript, the public papers and slides, the disclosure timeline and the WSU patent policy.",
  "05_Evidence/CONCEPTION_RECORD.txt": "The dated commit history of the chain in the private code repository, plus every commit the responses cite.",
  "05_Evidence/spine-program": "Status, results and design records from the programme repository, each linked from the responses.",
  "05_Evidence/spinesurg-ct-nnunet": "The chain's code (sweep_map.py, acquisition.py, guided_console.py, level_selective.py), its tests and its technical documents, from the private repository at commit 0ab783f.",
};
function describe(rel) {
  if (DESCRIBE[rel]) return DESCRIBE[rel];
  const stem = rel.replace(/\.(md|docx)$/, "");
  if (DESCRIBE[stem]) return DESCRIBE[stem];
  const top = Object.keys(DESCRIBE).find(k => rel.startsWith(k + "/"));
  return top ? DESCRIBE[top] : "";
}
function walk(dir, base = "") {
  return fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))
    .flatMap(e => e.isDirectory() ? walk(path.join(dir, e.name), base + e.name + "/") : [base + e.name]);
}
function contentsRows() {
  const files = walk(PKG).filter(f => f !== "00_READ_FIRST_Cover_Memo.docx");
  const rows = [["Folder or file", "Files", "What it is"]];
  const groups = [
    "01_Inventor_Responses_to_Counsel_2026-10-20.docx",
    "02_Draft_Provisional/SPECIFICATION", "02_Draft_Provisional/CLAIMS", "02_Draft_Provisional/COVER_SHEET",
    "02_Draft_Provisional/FILING_CHECKLIST", "02_Draft_Provisional/README",
    "03_Disclosure_Records/DISCLOSURE_MEMO", "03_Disclosure_Records/SCRUB_PLAN",
    "03_Disclosure_Records/INVENTION_DISCLOSURE", "03_Disclosure_Records/GUIDED_ACQUISITION",
    "03_Disclosure_Records/PATENT_PACKAGE", "03_Disclosure_Records/disclosure_forensics.json",
    "03_Disclosure_Records/disclosure_evidence", "03_Disclosure_Records/github_purge_requests",
    "04_WSU_TTO_Package", "05_Evidence/CONCEPTION_RECORD.txt", "05_Evidence/spine-program",
    "05_Evidence/spinesurg-ct-nnunet",
  ];
  let counted = 0;
  for (const g of groups) {
    const members = files.filter(f => f === g || f.startsWith(g + ".") || f.startsWith(g + "/"));
    if (!members.length) throw new Error("package has nothing for " + g);
    counted += members.length;
    const exts = members.map(m => m.slice(g.length));
    const shown = members.length === 1 ? (exts[0] || "1 file").replace(/^\./, ".")
      : exts.every(e => /^\.(md|docx)$/.test(e)) ? ".md and .docx" : `${members.length} files`;
    rows.push([g.replace(/\/(?=[^/]+$)/, "/ "), shown, DESCRIBE[g]]);
  }
  if (counted !== files.length) throw new Error(`index covers ${counted} of ${files.length} files`);
  return { rows, total: files.length + 1 };
}

// ---------- the memo
const { rows: CONTENTS, total: TOTAL } = contentsRows();
const body = [
  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "WSU 26-1902  |  FS 66174-0372", color: GREY, size: 20 })] }),
  new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Package for counsel: the state of the invention")] }),
  new Paragraph({ spacing: { after: 240 }, children: runs(
    "From Gregory J. Schwing, MD, PhD, General Surgery, Wayne State University School of Medicine / Detroit Medical Center. 20 October 2026.",
    { color: GREY, size: 20 }) }),

  h1("1. Why this package"),
  p("You asked me sixty questions before preparing a provisional application. This package answers them and gives you everything that bears on what can be filed and when, including what is unfavourable: numbers in the draft that turned out to be wrong, public disclosures of parts of the work, and steps that were drafted and never taken. Where a statement is my judgement rather than something shown, it is marked as inferred; where no record exists, it says not recorded."),
  p(`The package has ${TOTAL} files in five folders. Every link in the responses document points to a file in the private repositories; the same file is in this package, so nothing needs a GitHub login. Appendix D of the responses maps each link to its file here.`),

  h1("2. The state of the invention in one table"),
  p("One programme has produced three framings, and they do not line up with the paperwork. This is the most important thing to settle first."),
  table([1500, 2500, 2700, 3020], [
    ["Framing", "What it is", "Where it stands", "Public status"],
    ["Part A", "Naming vertebral levels on preoperative CT without counting from a fixed end (a name-free transitional-anatomy classifier).",
      "Design only. Features extracted on 3,524 CT and segmenter pairs; no classifier trained. In the WSU disclosure; not in the draft provisional.",
      "Parts public: a design note by 27 Aug 2026, scripts from 7 Sep 2026, a Zenodo archive of 7 Sep 2026 (SCRUB_PLAN.md)."],
    ["Part B", "Naming the level on a single intraoperative C-arm exposure from the image alone.",
      "Real C-arm results, in the confidential manuscript (04_WSU_TTO_Package/02). In the WSU disclosure; not the subject of the draft.",
      "Concepts public in proposals pushed to a public repository on 4 Sep 2026, removed 11 Sep, still fetchable by commit (SCRUB_PLAN.md section 6)."],
    ["The chain", "Overlapping C-arm exposures linked into a chain, named against alternative alphabets, with a confidence that commands the next move and a persistent digital marker.",
      "The draft provisional of 18 Sep 2026. Shown on CT renders and synthetic data only; no real overlapping intraoperative series tested. Not in the WSU disclosure form.",
      "Not public, on the third-party records (DISCLOSURE_MEMO.md). One sentence of the alternative-alphabet concept, without implementation, was on public review Spaces until 18 Sep 2026."],
  ]),
  new Paragraph({ spacing: { after: 120 } }),

  h1("3. What I need you to know first"),
  p("These are the points that change what is filed, what is said to WSU, or when. The responses document (section 1) gives each with its sources."),
  num("**The WSU disclosure and the draft describe different inventions.** The form of 25 September covers Parts A and B and never mentions a chain, overlap or sweep. I expect a supplemental disclosure to WSU is needed for the chain."),
  num("**The disclosure timeline given to WSU is wrong for Parts A and B.** It says nothing public discloses either. The later review (SCRUB_PLAN.md, 26 September) found Part A and Part B elements public on the dates in the table above. Its section 6 lists eight corrections owed to the WSU package. There is no record that they were sent."),
  num("**For the United States, those dates may start one-year grace periods** (the earliest 27 August 2026, so 27 August 2027); abroad, they may already bar the matching subject matter. This is my reading, not advice; the dates and their effect are yours to judge."),
  num("**The review Spaces on Hugging Face.** Three review apps were reachable without login until 18 September 2026 (created 26 May and 21 June 2026). Their text states the alternative-alphabet idea in one sentence, with no implementation, and nothing else of the chain. The exact bytes are preserved (03_Disclosure_Records/disclosure_evidence) and DISCLOSURE_MEMO.md assesses them for you to test."),
  num("**Clean-up steps were drafted and not taken.** The GitHub Support purge requests of 26 September (03_Disclosure_Records/github_purge_requests) have no record of being filed. Material removed from the public repositories is still served by commit, including from a fork by another user. The same review found that detector weights on the public site repository are still downloadable by commit, and that a public Hugging Face Space states one Part B construction (the hip point)."),
  num("**The measured numbers in the draft must be replaced.** On the morning of 18 September, 681 of the 801 render subjects were found in the training set (commit d6f407a); the draft was written that evening with those numbers. On 19 September every earlier render was found to have the wrong field size. Section 2 of the responses gives each replacement. The claims recite no accuracy."),
  num("**Three statements in the draft overstate what was shown** (paragraphs [0048], [0073] and [0083a]), and **nine pieces of subject matter were invented after the draft** that could be added before filing (Appendix A of the responses)."),
  num("**Part A is design only.** I recommend it go in a later provisional once a classifier exists."),
  num("**Four things wait on the filing:** the Part B manuscript, a data request to the SX-Stitch authors that describes the method, unsubmitted drafts that describe the sweep, and any CNS talk content beyond the cleared public deck (talk on 2 November 2026)."),

  h1("4. Reading order"),
  num("This memo."),
  num("01, the responses: section 1 (ten points), section 2 (numbers to replace), then the answers you need."),
  num("03_Disclosure_Records: DISCLOSURE_MEMO, then SCRUB_PLAN. Together they are the whole record of public availability."),
  num("02_Draft_Provisional: SPECIFICATION and CLAIMS, read with section 2 of the responses beside them."),
  num("04_WSU_TTO_Package: what WSU holds today, including the timeline that section 3, point 2 above says is incomplete."),
  num("05_Evidence: only where a specific answer sends you."),

  h1("5. What is in the package"),
  table([3300, 1300, 5120], CONTENTS),
  new Paragraph({ spacing: { after: 120 } }),
  p("Files ending .md and .py are plain text and open in any text editor or browser. The main Markdown records in 02 and 03 are also given as Word files of the same name; where the two differ, the .md is the original."),

  h1("6. What is not in the package, and why"),
  bullet("**Model weights and training data.** Large, not needed to judge patentability, and the data are third-party public datasets. Available on request."),
  bullet("**Result files from the computing cluster.** Every number used is quoted in the responses with the record or commit it comes from."),
  bullet("**Superseded drafts:** CNS talk decks before the cleared public version and manuscript revisions 2 to 4. The current Part B manuscript is 04/02."),
  bullet("**The full private git history.** The dated commit record of the chain is 05_Evidence/CONCEPTION_RECORD.txt; the repositories themselves can be made available to you."),
  bullet("**A draft cover e-mail to WSU** that was never sent, and the raw keyword-scan output behind SCRUB_PLAN.md, whose findings SCRUB_PLAN.md itself states."),
  p("Nothing has been left out because it is unfavourable."),
];

const doc = new Document({
  creator: "Gregory J. Schwing", title: "WSU 26-1902 package for counsel",
  styles: {
    default: { document: { run: { font: FONT, size: 21 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", run: { size: 40, bold: true, color: NAVY }, paragraph: { spacing: { after: 80 } } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, color: NAVY }, paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 0 } },
    ],
  },
  numbering: { config: [
    { reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 360, hanging: 260 } } } }] },
    { reference: "num", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 360, hanging: 360 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: 15840 }, margin: { top: 1260, bottom: 1260, left: MARGIN, right: MARGIN } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
      children: [new TextRun({ text: "Privileged and Confidential  |  Attorney-Client Communication  |  WSU 26-1902", size: 16, color: "A0281E" })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: "Cover memo, 20 October 2026  |  Page ", size: 16, color: GREY }),
        new TextRun({ children: [PageNumber.CURRENT], size: 16, color: GREY }),
        new TextRun({ text: " of ", size: 16, color: GREY }),
        new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, color: GREY })] })] }) },
    children: body,
  }],
});
Packer.toBuffer(doc).then(b => fs.writeFileSync(OUT, b));
