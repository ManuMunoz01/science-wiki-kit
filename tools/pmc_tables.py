"""pmc_tables.py -- tables and text of an open-access paper straight from the Europe PMC JATS XML.

    python tools/pmc_tables.py <DOI | PMID | PMCID> [--out file.md] [--json file.json] [--body]

Why it exists: when a paper is in PMC, the publisher XML carries the tables cell by cell
(`<table-wrap>` with `<td>`), independent of the PDF text layer. That makes it the cleanest source
for checking numbers: every cell, every row kept together, nothing fabricated, no extractor and no
page image needed. Rule of wiki-ingest: **if there is a PMCID, check table figures against the JATS
before the page image**; keep the image for what the XML lacks (figures, the publisher's own
misprints, papers outside PMC). On a JATS-versus-PDF discrepancy the printed PDF wins and the
discrepancy is noted.

Resolution: Europe PMC REST (`search?query=DOI:"..."` | `EXT_ID:<pmid>` | `PMCID:PMC...`) gives the
PMCID, then `rest/<PMCID>/fullTextXML`. No PMCID or no XML (paywall, abstract only): exit 2 with the
reason; continue with the PDF or with PubMed's `article_getter(<PMID>)` (same text with tabulated
tables; by DOI it returns empty).

Standard library only. Output: Markdown with one section per table (label, caption, rows, footer)
and, with `--body`, the body paragraphs in order. `--json` saves tables, paragraphs and numeric tokens.
"""
import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
NUM_RE = re.compile(r"\d(?:[\d.,]*\d)?")


def _get(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "science-wiki-kit pmc_tables.py"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def resolve(ident: str) -> dict:
    """DOI / PMID / PMCID -> {pmid, pmcid, doi, title, isOpenAccess, inEPMC}."""
    ident = ident.strip()
    if re.fullmatch(r"(?i)pmc\d+", ident):
        q = f"PMCID:{ident.upper()}"
    elif ident.isdigit():
        q = f"EXT_ID:{ident} AND SRC:MED"
    else:
        q = f'DOI:"{ident}"'
    url = f"{EPMC}/search?query={urllib.parse.quote(q)}&format=json&resultType=core&pageSize=3"
    data = json.loads(_get(url))
    res = data.get("resultList", {}).get("result", [])
    if not res:
        return {}
    return meta_from_core(res[0])


def meta_from_core(r: dict) -> dict:
    """Europe PMC `core` record -> the bibliographic fields a paper note needs.

    `authors` is Europe PMC's own author string; `pages` is `pageInfo` (a page range or an article number)."""
    out = {k: r.get(k) for k in ("pmid", "pmcid", "doi", "title", "isOpenAccess", "inEPMC",
                                 "journalTitle", "pubYear")}
    ji = r.get("journalInfo") or {}
    out["journalTitle"] = out["journalTitle"] or (ji.get("journal") or {}).get("title")
    out["authors"] = (r.get("authorString") or "").rstrip(".")
    out["volume"] = ji.get("volume")
    out["issue"] = ji.get("issue")
    out["pages"] = r.get("pageInfo")
    return out


def norm(s: str) -> str:
    s = s.replace("−", "-").replace("–", "-").replace("—", "-")
    s = s.replace(" ", " ").replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def text_of(el) -> str:
    return norm(" ".join(el.itertext()))


def parse_jats(xml_bytes: bytes) -> dict:
    root = ET.fromstring(xml_bytes)
    tables = []
    for tw in root.iter("table-wrap"):
        label = tw.find("label")
        cap = tw.find("caption")
        foot = tw.find("table-wrap-foot")
        rows = [[text_of(c) for c in tr if c.tag in ("td", "th")] for tr in tw.iter("tr")]
        tables.append({"id": tw.get("id") or f"t{len(tables)+1}",
                       "label": text_of(label) if label is not None else "",
                       "caption": text_of(cap) if cap is not None else "",
                       "rows": rows,
                       "foot": text_of(foot) if foot is not None else ""})
    abstract = [text_of(p) for ab in root.iter("abstract") for p in ab.iter("p")]
    abstract = [p for p in abstract if p]
    body = root.find("body")
    blocks = body_blocks(body) if body is not None else []
    paras = [b["text"] for b in blocks if b["type"] == "p"]
    full = text_of(root)
    return {"tables": tables, "abstract": abstract, "paragraphs": paras, "blocks": blocks,
            "numbers": sorted(set(NUM_RE.findall(full))), "chars_full": len(full)}


def body_blocks(body) -> list:
    """The body in document order as [{"type": "heading", "level": n, "title": s} | {"type": "p", "text": s}].

    A `<sec>` contributes its `<title>` as a heading (level 1 for a top-level section, 2 for its
    subsections, ...); paragraphs inside figures, table wrappers and the like are kept in place, so the
    paragraph list is the same as `body.iter("p")` gave before headings were tracked."""
    out = []

    def walk(el, level):
        for child in el:
            if child.tag == "sec":
                title = child.find("title")
                t = text_of(title) if title is not None else ""
                if t:
                    out.append({"type": "heading", "level": level, "title": t})
                walk(child, level + 1)
            elif child.tag == "title":
                continue
            elif child.tag == "p":
                t = text_of(child)
                if t:
                    out.append({"type": "p", "text": t})
            else:
                for p in child.iter("p"):
                    t = text_of(p)
                    if t:
                        out.append({"type": "p", "text": t})

    walk(body, 1)
    return out


def to_markdown(doc: dict, meta: dict, body: bool) -> str:
    out = [f"# {meta.get('title') or ''}".rstrip(),
           f"PMCID {meta.get('pmcid')} · PMID {meta.get('pmid')} · DOI {meta.get('doi')} · "
           f"{meta.get('journalTitle') or ''} {meta.get('pubYear') or ''} · source: Europe PMC JATS XML"]
    if meta.get("authors"):
        out.append(f"Authors: {meta['authors']}")
    biblio = [f"{k} {meta[k]}" for k in ("volume", "issue", "pages") if meta.get(k)]
    if biblio:
        out.append("Bibliographic data (Europe PMC): " + ", ".join(biblio))
    out.append("")
    for t in doc["tables"]:
        out.append(f"## {t['label']} {t['caption']}".rstrip())
        out.append("")
        if t["rows"]:
            w = max(len(r) for r in t["rows"])
            for i, r in enumerate(t["rows"]):
                r = r + [""] * (w - len(r))
                out.append("| " + " | ".join(r) + " |")
                if i == 0:
                    out.append("|" + "---|" * w)
        if t["foot"]:
            out.append("")
            out.append(t["foot"])
        out.append("")
    if body:
        if doc.get("abstract"):
            out.append("## Abstract")
            out.append("")
            out.extend(p + "\n" for p in doc["abstract"])
        out.append("## Body")
        out.append("")
        for b in doc["blocks"]:
            if b["type"] == "heading":
                out.append("#" * min(2 + b["level"], 6) + " " + b["title"] + "\n")
            else:
                out.append(b["text"] + "\n")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Tables of an open-access paper from the Europe PMC JATS XML")
    ap.add_argument("ident", help="DOI, PMID or PMCID")
    ap.add_argument("--out", help="write the Markdown here (default: stdout)")
    ap.add_argument("--json", help="save tables, paragraphs and numeric tokens as JSON")
    ap.add_argument("--body", action="store_true", help="include the body paragraphs")
    a = ap.parse_args()

    meta = resolve(a.ident)
    if not meta:
        print(f"[pmc] Europe PMC cannot find {a.ident!r}", file=sys.stderr)
        return 2
    if not meta.get("pmcid"):
        print(f"[pmc] no PMCID (PMID {meta.get('pmid')}, OA={meta.get('isOpenAccess')}): "
              f"no JATS available; continue with the PDF", file=sys.stderr)
        return 2
    url = f"{EPMC}/{meta['pmcid']}/fullTextXML"
    try:
        xml_bytes = _get(url)
    except Exception as exc:  # noqa: BLE001
        print(f"[pmc] {meta['pmcid']} no fullTextXML ({exc}); continue with the PDF", file=sys.stderr)
        return 2
    doc = parse_jats(xml_bytes)
    ncell = sum(1 for t in doc["tables"] for r in t["rows"] for c in r if NUM_RE.search(c))
    print(f"[pmc] {meta['pmcid']} (PMID {meta.get('pmid')}) -> {len(doc['tables'])} tables, "
          f"{ncell} numeric cells, {len(doc['paragraphs'])} paragraphs", file=sys.stderr)
    md = to_markdown(doc, meta, a.body)
    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"meta": meta, **doc}, f, ensure_ascii=False, indent=1)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"[written] {a.out}", file=sys.stderr)
    else:
        sys.stdout.buffer.write(md.encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
