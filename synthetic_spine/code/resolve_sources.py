"""Resolve every paper behind the reference tables to its identifiers and links.

    python3 code/resolve_sources.py [key ...]     # from synthetic_spine/; network; standard library only

For each paper in PAPERS:
  1. Crossref gives the DOI: directly when the citation carries one, otherwise by a bibliographic query whose
     candidate is accepted only when the cited author is among its authors, the year agrees within one (print against
     online), the journal agrees, and the first page agrees when both the citation and Crossref give one. A paper no
     candidate passes for is given no DOI, not a plausible wrong one.
  2. PubMed (NCBI E-utilities) gives the PubMed id: by the DOI, or by the fielded search in the paper's hints when it
     has none; a record reached by a search is accepted only when the cited author, the year and the first page
     agree. Its summary gives the journal's own volume, issue and pages, and its PMC id when it has one. A DOI that
     only PubMed knows is then confirmed by Crossref.
  3. The PMC id converter gives the PMC id for a DOI that PubMed did not link.
  4. PMC's full-text service says whether the paper's own tables can be read as text (the open-access subset),
     which is what code/verify_tables.py needs: how many tables it carries, and how many of those are text and how
     many only images. The licence is read from the full text when it states one.

Every raw answer is kept under sources_raw/<key>.json (Crossref's copies of abstracts removed), so each identifier
can be checked against what the service said and when. sources.json records, per paper, how each identifier was found
and whether the resolved year, issue and first page agree with the citation. Europe PMC was the first choice and
answered 503 ("Search service is temporarily unavailable") to every request on 2026-10-27; NCBI is used instead, and
each run asks Europe PMC once and records its answer in sources_raw/_europepmc_probe.json.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
RAW = HERE / "sources_raw"
OUT = HERE / "sources.json"
UA = {"User-Agent": "spine-program synthetic_spine resolver (research; urllib)"}
TOOL = "tool=spine-program-synthetic-spine"

# key: (first author surname, year, journal pattern for the Crossref check, citation, hints)
# hints: doi with doi_from (where that DOI came from; no citation in the tables prints one), pmcid (when the
# citation carries one), pubmed (a fielded PubMed search for a paper with no DOI),
# via (the key of the paper whose table these values were read from), series (names in the data tables).
PAPERS = {
    "panjabi1992": ("Panjabi", 1992, r"spine", "Panjabi MM, Goel V, Oxland T, Takata K, Duranceau J, Krag M, Price M. Human lumbar vertebrae. Quantitative three-dimensional anatomy. Spine 1992;17(3):299-306", {"doi": "10.1097/00007632-199203000-00010", "doi_from": "the header of data/panjabi_reference.csv", "series": ["Panjabi 1992", "Panjabi"]}),
    "panjabi1991t": ("Panjabi", 1991, r"spine", "Panjabi MM, Takata K, Goel V, Federico D, Oxland T, Duranceau J, Krag M. Thoracic human vertebrae. Quantitative three-dimensional anatomy. Spine 1991;16(8):888-901", {"series": ["Panjabi 1992 (T11, T12 rows)"]}),
    "panjabi1991c": ("Panjabi", 1991, r"spine", "Panjabi MM, Duranceau J, Goel V, Oxland T, Takata K. Cervical human vertebrae. Quantitative three-dimensional anatomy of the middle and lower regions. Spine 1991;16(8):861-869", {"doi": "10.1097/00007632-199108000-00001", "doi_from": "the docstring of data/build_panjabi.py", "series": ["panjabi_full_spine (C2-C7)"]}),
    "tan2004": ("Tan", 2004, r"spine", "Tan SH, Teo EC, Chua HC. Quantitative three-dimensional anatomy of cervical, thoracic and lumbar vertebrae of Chinese Singaporeans. Eur Spine J 2004;13(2):137-146", {"series": ["Tan 2004"]}),
    "chen2011": ("Chen", 2011, r"spine", "Chen H et al. Eur Spine J 2011;20(11):1814-1820", {"series": ["Chen 2011"]}),
    "duman2026": ("Duman", 2026, r"tomography", "Duman L, Yamansavci Sirzai E. Tomography 2026;12(8):109", {"series": ["Duman 2026"]}),
    "bonczar2024": ("Bonczar", 2024, r"surg", "Bonczar M et al. Surg Radiol Anat 2024;47(1):22", {"doi": "10.1007/s00276-024-03509-4", "doi_from": "pinned here: the bibliographic query returned another paper by the same first author", "series": ["Bonczar 2024"]}),
    "gilad1985": ("Gilad", 1985, r"anat", "Gilad I, Nissan M. J Anat 1985;143:115-120", {"pubmed": "Gilad I[au] AND 1985[dp] AND J Anat[ta]", "series": ["Gilad 1985"]}),
    "busscher2010": ("Busscher", 2010, r"spine", "Busscher I, Ploegmakers JJ, Verkerke GJ, Veldhuizen AG. Comparative anatomical dimensions of the complete human and porcine spine. Eur Spine J 2010;19(7):1104-1114", {"series": ["Busscher 2010"]}),
    "kunkel2011": ("Kunkel", 2011, r"anat", "Kunkel ME et al. J Anat 2011;219(3):375-387", {"series": ["Kunkel 2011"]}),
    "frontphys2026": ("", 2026, r"front", "Front Physiol 2026;17:1820186", {"doi": "10.3389/fphys.2026.1820186", "doi_from": "the citation's article number, in the journal's DOI pattern 10.3389/fphys.<year>.<article>", "series": ["Front Physiol 2026"]}),
    "yadav2020": ("Yadav", 2020, r"spine", "Yadav U et al. Int J Spine Surg 2020;14(2):175-181", {"series": ["Yadav 2020"]}),
    "vanderhouwen2009": ("Houwen", 2010, r"biomed", "van der Houwen EB et al. Ann Biomed Eng 2010;38(1):33-40", {"series": ["van der Houwen 2009"]}),
    "tang2016": ("Tang", 2016, r"spine", "Tang R et al. Eur Spine J 2016;25(12):4116-4131", {"series": ["Tang 2016"]}),
    "griffith2016": ("Griffith", 2016, r"imaging", "Griffith JF et al. Quant Imaging Med Surg 2016;6(6):671-679", {"series": ["Griffith 2016"]}),
    "cizmic2023": ("Cizmic", 2023, r"inform", "Cizmic M et al. Acta Inform Med 2023;31(3):200-205", {"series": ["Cizmic 2023"]}),
    "abbas2021": ("Abbas", 2021, r"biomed", "Abbas J et al. BioMed Res Int 2021:7093745", {"doi": "10.1155/2021/7093745", "doi_from": "pinned here: the bibliographic query returned a paper in another journal (J Biomed Res)", "series": ["Abbas 2021"]}),
    "masharawi2021": ("Masharawi", 2021, r"musculoskelet", "Masharawi Y et al. BMC Musculoskelet Disord 2021;22:1023", {"doi": "10.1186/s12891-021-04901-6", "doi_from": "pinned here: the citation's article number is wrong (the paper is 1026), so the page test refuses the right record; every value of the series is found in context in this paper's Table 4", "series": ["Masharawi 2021"]}),
    "amonookuofi1985": ("Amonoo-Kuofi", 1985, r"anat", "Amonoo-Kuofi HS. J Anat 1985;140(1):69-78", {"pubmed": "Amonoo-Kuofi HS[au] AND 1985[dp] AND J Anat[ta]", "series": ["Amonoo-Kuofi 1985"]}),
    "amonookuofi1982": ("Amonoo-Kuofi", 1982, r"anat", "Amonoo-Kuofi HS. J Anat 1982;135(2):225-233", {"pubmed": "Amonoo-Kuofi HS[au] AND 1982[dp] AND J Anat[ta]", "series": ["Amonoo-Kuofi 1982"]}),
    "alonge2021": ("Alonge", 2021, r"afr", "Alonge OJ et al. Afr J Med Med Sci 2021;50:69-76", {"pubmed": "Alonge[au] AND 2021[dp] AND Afr J Med Med Sci[ta]", "series": ["Alonge 2021"]}),
    "ahmed2019": ("Ahmed", 2019, r"chalmeda", "Ahmed MA et al. J Chalmeda Anand Rao Inst Med Sci 2019;17(1):21-27", {"pubmed": "Ahmed[au] AND 2019[dp] AND Chalmeda[ta]", "series": ["Ahmed 2019"]}),
    "chaudhary2015": ("Chaudhary", 2015, r"adv", "Chaudhary S et al. Int J Adv Res 2015;3(8):33-36", {"pubmed": "Chaudhary[au] AND 2015[dp] AND interpedicular", "series": ["Chaudhary 2015", "Eisenstein 1977 (via)"]}),
    "italianmri": ("", 2017, r"clin", "Sagittal Normal Limits of Lumbosacral Spine in a Large Adult Population. J Clin Imaging Sci", {"series": ["Italian MRI"]}),
    "hinck1966": ("Hinck", 1966, r"roentgen", "Hinck VC, Clark WM Jr, Hopkins CE. Normal interpediculate distances (minimum and maximum) in children and adults. Am J Roentgenol Radium Ther Nucl Med 1966;97(1):141-153", {"via": "ahn2001", "series": ["Hinck 1966"]}),
    "ahn2001": ("Ahn", 2001, r"orthop", "Ahn NU et al. Acta Orthop Scand 2001;72(1):67-71", {"series": ["Hinck 1966 (via)"]}),
    "eisenstein1977": ("Eisenstein", 1977, r"bone", "Eisenstein S. The morphometry and pathological anatomy of the lumbar spine in South African negroes and caucasoids with specific reference to spinal stenosis. J Bone Joint Surg Br 1977;59(2):173-180", {"via": "chaudhary2015", "series": ["Eisenstein 1977"]}),
    "shin2024": ("Shin", 2024, r"brain", "Shin D et al. Brain Spine 2024;5:104162", {"series": ["Shin 2024"]}),
    "bach2019": ("Bach", 2019, r"neurosurg", "Bach K et al. World Neurosurg 2019;124:e106-e118", {"series": ["Bach 2019"]}),
    "twomey1985": ("Twomey", 1985, r"orthop", "Twomey L, Taylor J. Age changes in lumbar intervertebral discs. Acta Orthop Scand 1985;56(6):496-499", {"series": ["Twomey 1985"]}),
    "zindrick1987": ("Zindrick", 1987, r"spine", "Zindrick MR et al. Analysis of the morphometric characteristics of the thoracic and lumbar pedicles. Spine 1987;12(2):160-166", {"series": ["Zindrick"]}),
    "olsewski1990": ("Olsewski", 1990, r"bone", "Olsewski JM et al. Morphometry of the lumbar spine: anatomical perspectives related to transpedicular fixation. J Bone Joint Surg Am 1990;72(4):541-549", {"pubmed": "Olsewski JM[au] AND 1990[dp] AND J Bone Joint Surg Am[ta]", "series": ["Olsewski"]}),
    "lien2007": ("Lien", 2007, r"spine", "Lien SB et al. Eur Spine J 2007;16:1215-1222", {"series": ["Lien"]}),
    "hou1993": ("Hou", 1993, r"spine", "Hou S et al. Spine 1993;18(13):1850-1855", {"series": ["Hou"]}),
    "krag1988": ("Krag", 1988, r"spine", "Krag MH et al. Spine 1988;13(1):27-32", {"series": ["Krag"]}),
    "mitra2002": ("Mitra", 2002, r"spine", "Mitra SR et al. Spine 2002;27(5):453-459", {"series": ["Mitra"]}),
    "arockiaraj2025": ("Arockiaraj", 2025, r"cranio", "Arockiaraj J et al. J Craniovertebr Junction Spine 2025", {"pmcid": "PMC12459938", "series": ["Arockiaraj"]}),
    "moncadahabib2025": ("Moncada", 2025, r"cureus", "Moncada-Habib T et al. Cureus 2025", {"pmcid": "PMC12504117", "series": ["Moncada-Habib"]}),
    "robertson2000": ("Robertson", 2000, r"spine", "Robertson PA, Stewart NR. Spine 2000;25(6):709-715", {"series": ["Robertson"]}),
    "otsuki2021": ("Otsuki", 2021, r"plos", "Otsuki B et al. PLoS One 2021;16(6):e0253019", {"doi": "10.1371/journal.pone.0253019", "doi_from": "the citation's article number, in the journal's DOI pattern 10.1371/journal.pone.<article>", "series": ["Otsuki"]}),
    "makino2012": ("Makino", 2012, r"spine", "Makino T et al. Eur Spine J 2012", {"pmcid": "PMC3535235", "series": ["Makino"]}),
    "yu2015": ("Yu", 2015, r"spine", "Yu CC et al. Spine 2015;40(21):1639-1646", {"series": ["Yu"]}),
}


def get(url, as_text=False):
    """One GET, retried with backoff on a failure; the parsed answer, or {"_error": ...}. A pause follows every call
    so neither service is pressed (NCBI asks for at most three a second without a key)."""
    err = ""
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                body = r.read().decode("utf-8", errors="replace")
            time.sleep(0.5)
            return body if as_text else json.loads(body)
        except Exception as exc:
            err = f"{type(exc).__name__}: {exc}"
            time.sleep(3 * (attempt + 1))
    return {"_error": err} if not as_text else ""


def norm(text):
    return re.sub(r"[^a-z]", "", (text or "").lower())


def year_of(item):
    for k in ("published-print", "published-online", "issued", "created"):
        parts = (item.get(k) or {}).get("date-parts") or [[None]]
        if parts and parts[0] and parts[0][0]:
            return parts[0][0]
    return None


def crossref_summary(item):
    authors = item.get("author") or []
    return {
        "doi": item.get("DOI"), "title": " ".join(item.get("title") or []),
        "journal": " ".join(item.get("container-title") or []), "year": year_of(item),
        "volume": item.get("volume"), "issue": item.get("issue"),
        "page": item.get("page") or item.get("article-number"),      # an online-only article has a number, no pages
        "first_author": authors[0].get("family", "") if authors else "",
        "authors": "; ".join(f"{a.get('family', '')} {a.get('given', '')}".strip() for a in authors),
    }


def crossref_accepts(item, surname, year, journal, citation):
    s = crossref_summary(item)
    surname_ok = not surname or norm(surname) in norm(s["authors"])
    year_ok = not year or (s["year"] is not None and abs(int(s["year"]) - int(year)) <= 1)
    journal_ok = bool(re.search(journal, s["journal"], re.I))
    cited, got = cited_first_page(citation), str(s["page"] or "").split("-")[0].lstrip("e")
    page_ok = not cited or not got or cited == got
    return surname_ok and year_ok and journal_ok and page_ok


def trimmed(answer):
    """A Crossref answer without its copies of abstracts, which are the publisher's text, not bibliographic data."""
    def drop(item):
        return {k: v for k, v in item.items() if k != "abstract"} if isinstance(item, dict) else item
    if isinstance(answer, dict) and isinstance(answer.get("message"), dict):
        msg = drop(answer["message"])
        if isinstance(msg.get("items"), list):
            msg["items"] = [drop(i) for i in msg["items"]]
        return dict(answer, message=msg)
    return answer


def cited_first_page(citation):
    """The first page the citation gives ('...;135(2):225-233' gives '225'), or None."""
    m = re.search(r"\d+(?:\([^)]*\))?:e?(\d+)(?:-|\b)", citation)
    return m.group(1) if m else None


def cited_issue(citation):
    """The issue the citation gives ('...;16(6):e0253019' gives '6'), or None."""
    m = re.search(r";\s*\d+\(([^)]+)\)", citation)
    return m.group(1) if m else None


def agreement(citation, year, resolved_page, resolved_year, resolved_issue):
    """Whether the resolved first page, issue and year agree with the citation, so a wrong resolution or a wrong
    citation shows in the table."""
    page, issue = cited_first_page(citation), cited_issue(citation)
    got = str(resolved_page or "").split("-")[0].lstrip("e")
    return {"cited_first_page": page, "resolved_first_page": got or None,
            "page_agrees": None if not page or not got else page == got,
            "cited_issue": issue, "resolved_issue": resolved_issue or None,
            # PubMed writes a part as "Pt 1"; the citations write "1"
            "issue_agrees": None if not issue or not resolved_issue else re.sub(r"\D", "", str(issue)) == re.sub(r"\D", "", str(resolved_issue)),
            "year_agrees": None if not year or not resolved_year else abs(int(str(resolved_year)[:4]) - int(year)) <= 1}


def pubmed_summary(pmid, raw):
    d = get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=json&{TOOL}")
    raw[f"pubmed_summary_{pmid}"] = d
    rec = (d.get("result") or {}).get(str(pmid)) or {}
    ids = {a.get("idtype"): a.get("value") for a in rec.get("articleids") or []}
    return {
        "pmid": str(pmid), "title": rec.get("title"), "journal": rec.get("source"), "pubdate": rec.get("pubdate"),
        "volume": rec.get("volume"), "issue": rec.get("issue"), "pages": rec.get("pages"),
        "first_author": ((rec.get("authors") or [{}])[0]).get("name"),
        "authors": "; ".join(a.get("name", "") for a in rec.get("authors") or []),
        "doi": ids.get("doi"), "pmcid": ids.get("pmc") or ids.get("pmcid", "").replace("pmc-id: ", "").split(";")[0] or None,
    }


def pubmed_search(term, raw, label):
    d = get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=5&term={urllib.parse.quote(term)}&{TOOL}")
    raw[label] = d
    return (d.get("esearchresult") or {}).get("idlist") or []


def full_text_status(pmcid, raw):
    """Whether PMC serves the paper's own full text (the open-access subset): the count of tables it carries and
    the licence it states. A paper outside the subset may still be free to read on PMC's site."""
    num = pmcid.replace("PMC", "")
    xml = get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={num}&retmode=xml&{TOOL}", as_text=True)
    body = "<body" in xml
    wraps = re.findall(r"<table-wrap\b.*?</table-wrap>", xml, re.S)
    as_text = sum(1 for w in wraps if re.search(r"<table[\s>]", w))       # not <table-wrap-foot>
    lic = re.search(r"<license[^>]*?(?:xlink:href|href)=\"([^\"]+)\"", xml)
    lic_text = re.search(r"<license-p>(.*?)</license-p>", xml, re.S)
    status = {"pmc_full_text_xml": body, "pmc_tables": len(wraps), "pmc_tables_as_text": as_text,
              "pmc_tables_as_images": len(wraps) - as_text,
              "license_url": lic.group(1) if lic else None,
              "license_text": re.sub(r"<[^>]+>", "", lic_text.group(1)).strip()[:300] if lic_text else None,
              "xml_bytes": len(xml)}
    raw["pmc_efetch_status"] = status
    return status


def resolve(key, surname, year, journal, citation, hints):
    raw, out = {}, {"key": key, "citation": citation, "series": hints.get("series", []), "via": hints.get("via"),
                    "how": []}
    item = None
    # 1. Crossref
    doi = hints.get("doi")
    if not doi and hints.get("pmcid"):
        conv = get(f"https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/?ids={hints['pmcid']}&format=json&{TOOL}")
        raw["idconv_pmcid"] = conv
        rec = (conv.get("records") or [{}])[0]
        doi = rec.get("doi")
        if doi:
            out["how"].append("PMC id given in the citation; DOI from the PMC id converter")
    if doi:
        raw["crossref_doi"] = trimmed(get("https://api.crossref.org/works/" + urllib.parse.quote(doi)))
        if raw["crossref_doi"].get("message"):
            item = raw["crossref_doi"]["message"]
            out["how"].append("DOI confirmed by Crossref" + (f" (DOI from {hints['doi_from']})" if hints.get("doi") else ""))
    if item is None:
        raw["crossref_query"] = trimmed(get("https://api.crossref.org/works?rows=5&query.bibliographic=" + urllib.parse.quote(citation)))
        cands = ((raw["crossref_query"].get("message") or {}).get("items")) or []
        out["crossref_candidates"] = [dict(crossref_summary(c), accepted=crossref_accepts(c, surname, year, journal, citation)) for c in cands]
        good = [c for c in cands if crossref_accepts(c, surname, year, journal, citation)]
        if good:
            item = good[0]
            out["how"].append("Crossref bibliographic query; first candidate whose author, year, journal and first page agree")
        else:
            out["how"].append("Crossref bibliographic query: no candidate agreed on author, year, journal and first page")
    if item is not None:
        out["crossref"] = crossref_summary(item)
    # 2. PubMed
    pmids, by_identifier = [], False
    if out.get("crossref", {}).get("doi"):
        pmids = pubmed_search(f"{out['crossref']['doi']}[doi]", raw, "pubmed_by_doi")
        if pmids:
            by_identifier = True
            out["how"].append("PubMed id found by the DOI")
    if not pmids and out.get("crossref", {}).get("doi"):
        conv = get(f"https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/?ids={urllib.parse.quote(out['crossref']['doi'])}&format=json&{TOOL}")
        raw["idconv_doi"] = conv
        rec = (conv.get("records") or [{}])[0]
        if rec.get("pmid"):
            pmids, by_identifier = [str(rec["pmid"])], True
            out["how"].append("PubMed id from the PMC id converter (PubMed's DOI search did not find it)")
    if not pmids and hints.get("pubmed"):
        pmids = pubmed_search(hints["pubmed"], raw, "pubmed_by_fields")
        out["how"].append(f"PubMed fielded search: {hints['pubmed']}")
    for pmid in pmids[:5]:
        s = pubmed_summary(pmid, raw)
        # the cited author must be among the paper's authors (a table may cite a senior author as "et al."), and the
        # year within one (an issue dated the year after its online publication)
        au_ok = not surname or norm(surname) in norm(s.get("authors"))
        years = [int(y) for y in re.findall(r"\b(19|20)\d{2}\b", str(s.get("pubdate")))] and [int(m.group(0)) for m in re.finditer(r"\b(?:19|20)\d{2}\b", str(s.get("pubdate")))]
        yr_ok = not year or any(abs(y - int(year)) <= 1 for y in years)
        # a fielded search can return another paper by the same author in the same year and journal, so its first
        # page must also be the cited one when the citation gives a page
        cited_page = cited_first_page(citation)
        pg_ok = by_identifier or not cited_page or str(s.get("pages") or "").split("-")[0].lstrip("e") == cited_page
        if by_identifier or (au_ok and yr_ok and pg_ok):
            # a record reached by the DOI is that paper whatever the citation says; one reached by a fielded
            # search must name the cited author within a year
            out["pubmed"] = s
            if by_identifier and not (au_ok and yr_ok):
                out["how"].append("PubMed record reached by the DOI does not name the cited author within a year")
            break
    if pmids and "pubmed" not in out:
        out["how"].append("PubMed records found, none naming the cited author within a year; none used")
    pm_doi = (out.get("pubmed") or {}).get("doi")
    if pm_doi and "crossref" not in out:
        raw["crossref_pubmed_doi"] = trimmed(get("https://api.crossref.org/works/" + urllib.parse.quote(pm_doi)))
        if raw["crossref_pubmed_doi"].get("message"):
            out["crossref"] = crossref_summary(raw["crossref_pubmed_doi"]["message"])
            out["how"].append("DOI from the PubMed record, confirmed by Crossref")
    # the citation's first author against the paper's own, so a misattribution in the tables is shown, not repeated
    actual = ((out.get("pubmed") or {}).get("first_author") or (out.get("crossref") or {}).get("first_author") or "")
    authors = (out.get("pubmed") or {}).get("authors") or (out.get("crossref") or {}).get("authors") or ""
    if surname and actual and norm(surname) not in norm(actual):
        out["first_author_differs"] = {"cited": surname, "paper": actual,
                                       "cited_author_among_authors": norm(surname) in norm(authors)}
    # 3. PMC id
    pmcid = (out.get("pubmed") or {}).get("pmcid") or hints.get("pmcid")
    if not pmcid and out.get("crossref", {}).get("doi"):
        conv = get(f"https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/?ids={urllib.parse.quote(out['crossref']['doi'])}&format=json&{TOOL}")
        raw["idconv_doi"] = conv
        pmcid = ((conv.get("records") or [{}])[0]).get("pmcid")
    if pmcid:
        out["pmcid"] = pmcid
        out["full_text"] = full_text_status(pmcid, raw)
    c, pm = out.get("crossref") or {}, out.get("pubmed") or {}
    out["agreement"] = agreement(citation, year, c.get("page") or pm.get("pages"),
                                 c.get("year") or str(pm.get("pubdate") or "")[:4] or None, c.get("issue") or pm.get("issue"))
    # links
    doi = (out.get("crossref") or {}).get("doi") or (out.get("pubmed") or {}).get("doi")
    pmid = (out.get("pubmed") or {}).get("pmid")
    out["links"] = {
        "doi": f"https://doi.org/{doi}" if doi else None,
        "pubmed": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None,
        "pmc": f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/" if pmcid else None,
    }
    RAW.mkdir(exist_ok=True)
    (RAW / f"{key}.json").write_text(json.dumps(raw, indent=1, ensure_ascii=True) + "\n", encoding="ascii")
    return out


def probe_europepmc():
    """Ask Europe PMC for one known paper and keep what it said, so the reason it is not used stays checkable."""
    url = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&query="
           + urllib.parse.quote('DOI:"10.1097/00007632-199203000-00010"'))
    when = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
            status, body = r.status, r.read().decode("utf-8", errors="replace")[:2000]
    except urllib.error.HTTPError as exc:
        status, body = exc.code, exc.read().decode("utf-8", errors="replace")[:2000]
    except Exception as exc:
        status, body = None, f"{type(exc).__name__}: {exc}"
    RAW.mkdir(exist_ok=True)
    (RAW / "_europepmc_probe.json").write_text(json.dumps({"asked_at": when, "url": url, "http_status": status,
                                                            "body": body}, indent=1, ensure_ascii=True) + "\n", encoding="ascii")
    return f"asked {when}: HTTP {status}"


def main(argv):
    only = set(argv[1:])
    done = json.loads(OUT.read_text(encoding="ascii")) if OUT.exists() and only else {"papers": {}}
    europepmc = probe_europepmc()
    for key, (surname, year, journal, citation, hints) in PAPERS.items():
        if only and key not in only:
            continue
        r = resolve(key, surname, year, journal, citation, hints)
        done["papers"][key] = r
        ft = r.get("full_text") or {}
        print(f"{key:18s} doi={(r.get('crossref') or {}).get('doi') or (r.get('pubmed') or {}).get('doi')} "
              f"pmid={(r.get('pubmed') or {}).get('pmid')} pmcid={r.get('pmcid')} "
              f"xml={ft.get('pmc_full_text_xml')} tables={ft.get('pmc_tables')}")
    done["resolved_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    done["services"] = {
        "crossref": "https://api.crossref.org/works",
        "pubmed": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/ (esearch, esummary, efetch db=pmc)",
        "pmc_idconv": "https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/",
        "europepmc": ("not used: it answered 503 'Search service is temporarily unavailable' to every request on "
                      f"2026-10-27, when this resolver was written; this run {europepmc} (sources_raw/_europepmc_probe.json)"),
    }
    OUT.write_text(json.dumps(done, indent=1, ensure_ascii=True) + "\n", encoding="ascii")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
