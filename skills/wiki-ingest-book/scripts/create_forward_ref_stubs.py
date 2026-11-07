#!/usr/bin/env python3
"""Create status:stub chapter notes for forward-references to sibling chapters.

Scans a just-ingested chapter for [[{book}_ChNN]] wikilinks (alias-aware). For each one
that does not resolve to a note, reads the book hub's Table of Contents table to recover
title and pages, derives DOI and citekey from the hub frontmatter, and writes a stub.
Forward-refs with no TOC row are skipped and reported (manual ingest required).

Usage:
  python create_forward_ref_stubs.py CHAPTER.md BOOK_HUB.md [--dry-run] [--log _temp/stubs.md]
"""
import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import wikikit  # noqa: F401
except ImportError:  # running from a checkout without `pip install -e .`
    for _p in Path(__file__).resolve().parents:
        if (_p / "wikikit" / "__init__.py").is_file():
            sys.path.insert(0, str(_p))
            break
    else:
        sys.exit("wikikit not found: run `pip install -e <kit>` or keep the skills inside the kit checkout")

from wikikit import frontmatter  # noqa: E402
from wikikit.textio import append_log, read_text, write_text  # noqa: E402


def parse_toc(hub_body):
    """TOC rows come in several shapes: chapter number in column 1, or Part in column 1 and
    chapter number in column 2. The chapter number is the FIRST pure-integer cell; the title is
    the next non-empty cell; pages is the cell right after the title if it is a page number/range."""
    rows = {}
    for line in hub_body.splitlines():
        if not re.match(r"^\s*\|", line):
            continue
        cells = [c.strip() for c in line.split("|")]
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]
        num_idx = next((i for i, c in enumerate(cells) if re.fullmatch(r"\d+", c)), -1)
        if num_idx < 0:
            continue  # part header, separator, or no chapter number
        title, title_idx = "", -1
        for j in range(num_idx + 1, len(cells)):
            if cells[j]:
                title, title_idx = cells[j], j
                break
        if not title:
            continue
        pages = ""
        if title_idx + 1 < len(cells) and re.fullmatch(r"\d+([-–]\d+)?", cells[title_idx + 1]):
            pages = cells[title_idx + 1]
        title = re.sub(r"\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]", r"\1", title)
        rows[int(cells[num_idx])] = {"title": title, "pages": pages}
    return rows


def build_stub(book, n, row, fm, source_chapter, today):
    doi = f"{fm['doi']}_{n}" if fm.get("doi") else ""
    citekey = f"{fm['citekey']}_ch{n}" if fm.get("citekey") else ""
    year = fm.get("year", "")
    return "\n".join([
        "---",
        "tags: [book-chapter, stub]",
        f"date: {today}",
        f"last_verified: {today}",
        "status: stub",
        "type: book-chapter",
        'title: "' + row["title"].replace('"', '\\"') + '"',
        f'book: "[[{book}]]"',
        f"chapter_number: {n}",
        f'pages: "{row["pages"]}"',
        f"year: {year}",
        f'doi: "{doi}"',
        f'citekey: "{citekey}"',
        "research_lines: []",
        "concepts_touched: []",
        "---",
        "",
        f"# Ch. {n}: {row['title']}",
        "",
        f"*Part of: [[{book}]]*",
        "",
        "> [!note] Stub pending ingest",
        f"> Auto-generated forward-ref stub. Referenced by [[{source_chapter}]].",
        f'> Run `/wiki-ingest-book "{book}" > Chapter {n}` to ingest.',
        "",
    ])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("chapter")
    ap.add_argument("hub")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--log", default="_temp/wiki_ingest_book_stubs_created.md")
    a = ap.parse_args()

    chapter, hub = Path(a.chapter), Path(a.hub)
    for p in (chapter, hub):
        if not p.is_file():
            sys.exit(f"File not found: {p}")

    book, source = hub.stem, chapter.stem
    chapter_txt = read_text(chapter)
    pattern = r"\[\[" + re.escape(book) + r"_Ch(\d+)(?:\|[^\]]*)?\]\]"
    refs = {int(m.group(1)) for m in re.finditer(pattern, chapter_txt)}
    if not refs:
        print(f"No forward-refs found in {source}")
        return

    fm, body = frontmatter.parse(read_text(hub))
    toc = parse_toc(body)
    today = date.today().isoformat()
    created, skipped = [], []
    for n in sorted(refs):
        name = f"{book}_Ch{n:02d}"
        path = hub.parent / f"{name}.md"
        if path.exists():
            continue
        if n not in toc:
            skipped.append(f"Ch{n} (not in TOC; manual ingest required)")
            continue
        if a.dry_run:
            print(f"DRY-RUN would create: {path}")
        else:
            write_text(path, build_stub(book, n, toc[n], fm, source, today))
            print(f"Created stub: {name}")
        created.append(f"Ch{n} ({toc[n]['title']}) -> {name}.md")

    if skipped:
        print("WARN: skipping forward-refs without TOC entry:")
        for s in skipped:
            print(f"  - {s}")
    if created and not a.dry_run:
        lines = [f"## {datetime.now():%Y-%m-%d %H:%M} - {book}", f"Source chapter: {source}"]
        lines += [f"- {c}" for c in created]
        if skipped:
            lines += ["", "Skipped (no TOC entry):"] + [f"- {s}" for s in skipped]
        append_log(a.log, "# Forward-ref Stubs Created", lines)
    print(f"Done. Created {len(created)} stub(s); skipped {len(skipped)}.")


if __name__ == "__main__":
    main()
