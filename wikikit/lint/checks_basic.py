"""Checks 1-5: graph connectivity, provenance of claims, broken links."""
import re

from .result import Result
from .text import clean_link_item, preprocess_body, split_lines


def _link_index(sources, extra_key):
    """{target_lower: {source_name_lower}} over `sources`: inline wikilinks plus the list-valued
    frontmatter field `extra_key` (`concepts_touched`, `related_concepts`)."""
    idx = {}
    for n in sources:
        targets = {t.lower() for t, _, _ in n.wikilinks}
        extra = n.fm.get(extra_key)
        if isinstance(extra, list):
            targets |= {clean_link_item(i).lower() for i in extra}
        for t in targets:
            idx.setdefault(t, set()).add(n.name.lower())
    return idx


def check1(ctx):
    """Orphan concept notes: nobody links to them.

    Backlinks that count: a paper or book note (inline wikilink, or `concepts_touched`), or a sibling
    concept note (inline wikilink, or `related_concepts`). The sibling leg keeps synthesis-hub notes,
    referenced by other concepts and a MOC but never by a paper, from being false orphans."""
    from_sources = _link_index(ctx.folder_notes(ctx.papers, ctx.books), "concepts_touched")
    from_concepts = _link_index(ctx.folder_notes(ctx.concepts), "related_concepts")
    out = []
    for c in ctx.folder_notes(ctx.concepts):
        if ctx.stub_exempt_for(1, c.status):
            continue
        me = c.name.lower()
        linked = (from_sources.get(me, set()) - {me}) or (from_concepts.get(me, set()) - {me})
        if not linked:
            out.append(c.name)
    return Result("orphan concepts", {"check1": len(out)}, {"wiki_check1_orphan_concepts.txt": sorted(out)})


def check2(ctx):
    """Orphan method notes: no paper/book links to them AND they link to no paper/book."""
    works = ctx.folder_notes(ctx.papers, ctx.books)
    backlinks = {t.lower() for n in works for t, _, _ in n.wikilinks}
    work_names = {n.name.lower() for n in works}
    out = []
    for m in ctx.folder_notes(ctx.methods):
        if ctx.stub_exempt_for(2, m.status):
            continue
        if m.name.lower() in backlinks:
            continue
        if any(t.lower() in work_names for t, _, _ in m.wikilinks):
            continue
        out.append(m.name)
    return Result("orphan methods", {"check2": len(out)}, {"wiki_check2_orphan_methods.txt": sorted(out)})


def check3(ctx):
    """Paper notes with an empty `concepts_touched` (stubs excepted)."""
    out = []
    for n in ctx.folder_notes(ctx.papers):
        if n.status.lower() == "stub":
            continue
        ct = n.fm.get("concepts_touched")
        if ct is None or ct == "" or ct == []:
            out.append(n.name)
    return Result("empty concepts_touched", {"check3": len(out)}, {"wiki_check3_empty_concepts.txt": sorted(out)})


def check4(ctx):
    """Unsourced verb-bearing claims in concept notes.

    A prose line with a claim verb and no `[[wikilink]]` within +/- `unsourced_radius` lines, and not
    under a section heading that itself carries a wikilink. A note is listed when it has at least
    `unsourced_threshold` such lines."""
    d = ctx.lcfg["defaults"]
    radius, threshold = d["unsourced_radius"], d["unsourced_threshold"]
    verbs = ctx.lcfg["verb_list"]
    rx = re.compile(r"\b(" + "|".join(re.escape(v) for v in verbs) + r")\b", re.I)
    out = []
    for n in ctx.folder_notes(ctx.concepts):
        if ctx.stub_exempt_for(4, n.status):
            continue
        lines = split_lines(preprocess_body(n.body))
        has_link = ["[[" in t for t in lines]
        is_heading = [t.lstrip().startswith("#") for t in lines]
        count = 0
        for i, raw in enumerate(lines):
            t = raw.strip()
            if not t or t.startswith(("#", ">", "---", "|")):
                continue
            if re.match(r"^\s*[a-zA-Z_]+:", t) or not rx.search(t):
                continue
            lo, hi = max(0, i - radius), min(len(lines) - 1, i + radius)
            if any(has_link[lo:hi + 1]):
                continue
            head_sourced = False
            for j in range(i - 1, -1, -1):
                if is_heading[j]:
                    head_sourced = has_link[j]
                    break
            if head_sourced:
                continue
            count += 1
        if count >= threshold:
            out.append("%s|%d" % (n.name, count))
    return Result("unsourced claims (concepts)", {"check4": len(out)},
                  {"wiki_check4_unsourced_claims.txt": sorted(out)})


def check5(ctx):
    """Broken and placeholder wikilinks, resolved against the WHOLE vault (cross-folder).

    `placeholder` only fires for a target that does not resolve (a legitimate ALL-CAPS abbreviation
    note never flags). Targets matching `link_target_ignore_patterns` (Bases embeds) are skipped.
    An EMPTY target (`[[]]`, `[[|alias]]`) is invisible to the wikilink extractor, so it is looked
    for separately on the raw body, skipping fences and code spans."""
    placeholder = [re.compile(p) for p in ctx.lcfg["placeholder_wikilink_patterns"]]
    ignore = [re.compile(p) for p in ctx.lcfg["link_target_ignore_patterns"]]

    def classify(target):
        if ctx.in_vault(target) or any(r.search(target) for r in ignore):
            return None
        return "placeholder" if any(r.search(target) for r in placeholder) else "broken"

    out = []
    for n in ctx.notes.values():
        for target, line, _ in n.wikilinks:
            kind = classify(target)
            if kind:
                out.append("%s|%s|%d|%s" % (n.name, target, line, kind))

    empty = re.compile(r"\[\[\s*(?:\|[^\]]*)?\]\]")
    for n in ctx.notes.values():
        in_fence = False
        for i, line in enumerate(split_lines(n.body)):
            if re.match(r"^\s*(```|~~~)", line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for h in empty.finditer(line):
                if line[:h.start()].count("`") % 2 == 1:  # inside a code span: quoted text, not a link
                    continue
                out.append("%s|(empty target)|%d|empty-target" % (n.name, i + 1 + n.body_offset))

    for target, line, _ in ctx.index_wikilinks:
        kind = classify(target)
        if kind:
            out.append("index|%s|%d|%s" % (target, line, kind))
    return Result("broken wikilinks", {"check5": len(out)}, {"wiki_check5_broken_links.txt": sorted(out)})


CHECKS = [(1, check1), (2, check2), (3, check3), (4, check4), (5, check5)]
