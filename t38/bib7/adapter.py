"""Minimal glossary readers and external proposals; synthetic inputs only (MIT).

Reuses BIB-1 normalization/YAML and kit byte-safe I/O/table helpers. Never renders,
modifies or resolves source documents, Zotero, URLs or glossary identifiers.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

KIT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KIT))
from t38.bib1.audit import normalize, parse as parse_yaml
from wikikit.textio import read_text
from wikikit.lint.text import table_cell_count

RELATIONS = {
    'alias bibliografico': 'bibliographic_alias_statement',
    'posible duplicado bibliografico': 'bibliographic_identity_candidate',
    'posible reutilizacion de datos': 'dataset_relationship_review',
}
NOT_REPORTED = {'no informado', 'no informada', 'no consta'}
PENDING = {'pendiente', 'sin verificar', 'no verificado', 'desconocido'} | NOT_REPORTED


def masked_lines(text):
    """Preserve line offsets; hide comments/fences from recognition, never from raw spans."""
    text = re.sub(r'<!--[\s\S]*?-->', lambda m: re.sub(r'[^\r\n]', ' ', m[0]), text)
    lines, fence = [], None
    for line in text.splitlines(keepends=True):
        m = re.match(r'^[ \t]*(`{3,}|~{3,})', line)
        if fence:
            if m and m[1][0] == fence[0] and len(m[1]) >= len(fence) and not line[m.end():].strip():
                fence = None
            lines.append('')
        elif m:
            fence = m[1]
            lines.append('')
        else:
            lines.append(line)
    return lines


def cells(line):
    """GFM row; optional outer pipes, escaped pipes stay in cell text unchanged."""
    s = line.strip()
    if '|' not in s:
        return None
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|') and (len(s[:-1]) - len(s[:-1].rstrip('\\'))) % 2 == 0:
        s = s[:-1]
    result, current, slashes = [], '', 0
    for char in s:
        if char == '|' and slashes % 2 == 0:
            result.append(current.strip())
            current = ''
        else:
            current += char
        slashes = slashes + 1 if char == '\\' else 0
    result.append(current.strip())
    return result


def fields(lines):
    """Keep repeated/unknown labelled fields, including continuation text; do not coerce them."""
    result = []
    for line in lines:
        m = re.match(r'^[ \t]*(?:[-*] )?(?:\*\*([^*]+)\*\*:?[ \t]*|([^:\n]+):[ \t]*)(.*)', line.rstrip('\r\n'))
        if m:
            result.append({'label':(m[1] or m[2]).rstrip(':').strip(), 'value':m[3]})
        elif result:
            result[-1]['value'] += '\n' + line.rstrip('\r\n')
    return result


def values(parsed, *labels):
    wanted = {normalize(label) for label in labels}
    return [f['value'].strip() for f in parsed if normalize(f['label']) in wanted]


def nonpending_values(items):
    return [s for s in items if s and normalize(s) not in PENDING]


def extraction_state(items):
    """Describe extraction/declarations only, never prove absence in a source."""
    if not items:
        return 'not-structured'
    nonempty = [normalize(s) for s in items if s.strip()]
    if not nonempty:
        return 'declared-empty'
    if all(s in NOT_REPORTED for s in nonempty):
        return 'declared-not-reported-unverified'
    if all(s in PENDING for s in nonempty):
        return 'declared-pending'
    return 'structured-declared-unverified'


def references(text):
    """Declared references only: preserve targets, never claim Zotero/source identity."""
    links = re.findall(r'\[\[([^\]|#]+)(?:[^\]]*)\]\]', text.replace('\\|', '|'))
    citations = re.findall(r'\[@([^\]\s]+)\]', text)
    return list(dict.fromkeys(links + citations))


def make_observation(doc, start, end, section, raw, parsed, entry_id=None, heading=None, table=None):
    original_terms = nonpending_values(values(parsed, 'Término original', 'Término'))
    aliases = nonpending_values(values(parsed, 'Alias', 'Aliases terminológicos'))
    definitions = values(parsed, 'Definición', 'Definición o uso', 'Uso', 'Definición o uso — paráfrasis verificada')
    context = values(parsed, 'Contexto operativo', 'Contexto', 'Contexto y criterios operativos')
    locations = values(parsed, 'Localización')
    declared_keys = nonpending_values(values(parsed, 'Citekey', 'Citekeys'))
    sources = values(parsed, 'Fuente', 'Fuentes', 'Procedencia', 'Procedencia y atribución')
    source_refs = references('\n'.join(declared_keys + sources))
    for key in declared_keys:
        if not references(key) and not re.search(r'\s|[,;]', key):
            source_refs.append(key)
    year = values(parsed, 'Año')
    if heading:
        year = list(dict.fromkeys(year + re.findall(r'\((\d{4})\)', heading)))
    canonical = section if entry_id is not None else table[0]
    if table:
        original_terms = [table[0]]
        definitions = [table[1]]  # mixed usage/location remains ONE unbound cell
        sources = [table[2]]
        source_refs = references(table[2])
    source_urls = list(dict.fromkeys(re.findall(r'https?://[^\s<>()]+', '\n'.join(sources))))
    source_state = extraction_state(sources + values(parsed, 'Citekey', 'Citekeys'))
    if sources and nonpending_values(sources) and not (source_refs or source_urls):
        source_state = 'source-text-not-structured'
    extraction_status = {
        'source-reference':source_state, 'location':extraction_state(locations),
        'definition-or-use':extraction_state(definitions), 'context':extraction_state(context),
        'year':extraction_state(year)}
    if table:
        for name in ('location', 'context', 'definition-or-use'):
            extraction_status[name] = 'combined-cell-unparsed' if table[1].strip() else 'declared-empty'
        extraction_status['row-definition-source-binding'] = 'binding-unresolved'
    locator = {'document_reference':doc['document_reference'], 'snapshot_sha256':doc['sha256'],
               'section':section, 'line_start':start, 'line_end':end,
               'scope':'snapshot-only-not-a-stable-id'}
    pending = []
    for label, content in [('source-reference', source_refs + source_urls), ('location', nonpending_values(locations)),
                           ('definition-or-use', nonpending_values(definitions)), ('context', nonpending_values(context))]:
        if not content:
            pending.append(label)
    if not nonpending_values(year):
        pending.append('year')
    if len(set(nonpending_values(year))) > 1:
        pending.append('conflicting-declared-years')
        extraction_status['conflicting-declared-years'] = 'conflicting-declarations-unverified'
    if table:
        pending.append('row-definition-source-binding')
    return {'observation_id':doc['document_reference'] + '@' + doc['sha256'] + ':L' + str(start),
            'target':{'glossary_id':doc['glossary_id'], 'entry_id':entry_id,
                      'format':doc['format'], 'locator':locator},
            'canonical':canonical, 'original_terms':original_terms, 'aliases':aliases,
            'translations':values(parsed, 'Traducción'), 'definitions_or_uses':definitions,
            'contexts':context, 'locations':locations, 'declared_years':year,
            'declared_citekeys':declared_keys, 'source_references':list(dict.fromkeys(source_refs)),
            'source_urls':source_urls, 'extraction_status':extraction_status,
            'source_text':sources, 'fields':parsed, 'raw_markdown':raw,
            'source_binding':'row-level-unresolved' if table else 'entry-level-not-verified',
            'verification':'declared-unverified', 'pending':pending}


def read_document(path, form, root):
    if form not in ('a', 'b'):
        raise ValueError('Format must be a or b')
    path, root = Path(path).absolute(), Path(root).resolve()
    if any(p.is_symlink() for p in [path] + list(path.parents)):
        raise ValueError('Symlinked inputs are unsupported')
    if path.is_symlink() or root not in path.resolve().parents:
        raise ValueError('Input must be a non-symlink file inside the synthetic root')
    path = path.resolve()
    # Reject symlinked intermediate directories as well.
    if any(p.is_symlink() for p in [path] + list(Path(path).parents) if p != root and root in p.parents):
        raise ValueError('Symlinked inputs are unsupported')
    data = path.read_bytes()
    text = data.decode('utf-8')
    doc = {'document_reference':path.relative_to(root).as_posix(), 'sha256':hashlib.sha256(data).hexdigest(),
           'format':'concept-record' if form == 'a' else 'markdown-table-without-ids', 'glossary_id':None, 'frontmatter':{}}
    diagnostics = []
    if text.lstrip('\ufeff').startswith('---\n') or text.lstrip('\ufeff').startswith('---\r\n'):
        try:
            fm, _ = parse_yaml(text)
            doc['frontmatter'] = fm
            if isinstance(fm.get('glossary_id'), str):
                doc['glossary_id'] = fm['glossary_id']
        except ValueError:
            diagnostics.append({'code':'frontmatter-unparsed', 'line':1})
    raw_lines, masked = text.splitlines(keepends=True), masked_lines(text)
    observations, section = [], ''
    if form == 'a':
        active = None
        def finish(end):
            if active:
                start, entry_id, header, concept = active
                observations.append(make_observation(doc, start + 1, end, concept,
                    ''.join(raw_lines[start:end]), fields(masked[start + 1:end]), entry_id, header))
        for i, line in enumerate(masked):
            h2 = re.match(r'^##[ \t]+(.+?)\s*$', line)
            h3 = re.match(r'^###[ \t]+(.+?)\s*$', line)
            if h2 or h3:
                finish(i)
                active = None
                if h2:
                    section = h2[1]
                else:
                    entry = re.fullmatch(r'(H-[^\s·]*\d+)[ \t]+·[ \t]+(.+)', h3[1])
                    if entry:
                        active = (i, entry[1], entry[2], section)
                    elif h3[1].startswith('H-'):
                        diagnostics.append({'code':'unsupported-entry-heading', 'line':i + 1, 'raw_markdown':raw_lines[i]})
        finish(len(raw_lines))
    else:
        i = 0
        expected = [normalize(s) for s in ['Término', 'Uso documentado y localización', 'Fuente']]
        while i < len(masked):
            heading = re.match(r'^#{1,6}[ \t]+(.+?)\s*$', masked[i])
            if heading:
                section = heading[1]
            row = cells(masked[i])
            if row and [normalize(c) for c in row] == expected:
                sep = cells(masked[i + 1]) if i + 1 < len(masked) else None
                if not sep or len(sep) != 3 or not all(re.fullmatch(r':?-{3,}:?', c) for c in sep):
                    diagnostics.append({'code':'unsupported-table-separator', 'line':i + 1})
                    i += 1
                    continue
                i += 2
                while i < len(masked) and cells(masked[i]) is not None:
                    row = cells(masked[i])
                    if row is None or len(row) != 3 or table_cell_count(masked[i]) != 3:
                        diagnostics.append({'code':'unsupported-table-row', 'line':i + 1,
                                            'raw_markdown':raw_lines[i]})
                    else:
                        # Do not parse mixed narrative cells into per-study facts.
                        observations.append(make_observation(doc, i + 1, i + 1, section, raw_lines[i], [], table=row))
                    i += 1
                continue
            elif row and i + 1 < len(masked):
                following = cells(masked[i + 1])
                if following and all(re.fullmatch(r':?-{3,}:?', c) for c in following):
                    diagnostics.append({'code':'unsupported-table-header', 'line':i + 1, 'raw_markdown':raw_lines[i]})
            i += 1
    if not observations:
        diagnostics.append({'code':'no-supported-observations', 'line':None})
    doc['diagnostics'] = diagnostics
    return doc, observations


def proposals(documents, observations):
    suggestions = []
    def add(kind, group, reason, **extra):
        if kind == 'glossary_inconsistency':
            extra['pending_status'] = {name:group[0]['extraction_status'].get(name, 'manual-review')
                                       for name in extra.get('pending_fields', [])}
        suggestions.append({'suggestion_id':'proposal-' + str(len(suggestions) + 1), 'kind':kind,
                            'target':group[0]['target'], 'observations':group, 'reason':reason,
                            'status':'pending-review', 'action':'none', **extra})
    for row in observations:
        add('term_candidate', [row], 'Observed entry/row for review; no new glossary entry proposed automatically.')
        if row['pending']:
            add('glossary_inconsistency', [row], 'Pending structured provenance/binding, not a scientific error.',
                pending_fields=row['pending'])
        for f in row['fields']:
            kind = RELATIONS.get(normalize(f['label']))
            if kind:
                refs = references(f['value'])
                if len(refs) == 2 and '->' in f['value']:
                    add(kind, [row], 'Explicit source statement only; not independently verified.',
                        related_source_references=refs, relation_statement=f['value'], verification='not-verified')
                else:
                    add('glossary_inconsistency', [row], 'Explicit relationship label has unsupported/ambiguous syntax.',
                        pending_fields=['relationship-binding'])
    for i, a in enumerate(observations):
        terms_a = {normalize(t) for t in [a['canonical']] + a['original_terms'] + a['aliases']} - {''}
        for b in observations[i + 1:]:
            shared = sorted(terms_a & ({normalize(t) for t in [b['canonical']] + b['original_terms'] + b['aliases']} - {''}))
            if shared:
                add('terminology_overlap', [a, b], 'Shared terms only; do not merge definitions or infer bibliographic identity.',
                    shared=shared, synonymy='not-established', bibliographic_identity='not-inferred', dataset_relationship='not-inferred')
            if a['target']['entry_id'] is not None and a['target']['entry_id'] == b['target']['entry_id'] and a['target']['locator']['document_reference'] == b['target']['locator']['document_reference']:
                add('glossary_inconsistency', [a, b], 'Repeated entry identifier in one document; retain both and review.',
                    pending_fields=['duplicate-entry-id'])
    return {'schema':'t38-external-glossary-proposals-v1', 'scope':'synthetic-only', 'documents':documents,
            'observations':observations, 'suggestions':suggestions,
            'summary':{'observations':len(observations), 'suggestions_by_kind':dict(Counter(s['kind'] for s in suggestions)),
                       'parse_diagnostics':sum(len(d['diagnostics']) for d in documents)},
            'scientific_validity':'not-assessed', 'bibliographic_deduplication':'not-performed',
            'input_changes':'none'}


def build(root, inputs):
    if Path(root).is_symlink():
        raise ValueError('Symlinked input root is unsupported')
    root = Path(root).resolve()
    if not (root / '.t38-synthetic').is_file():
        raise ValueError('Only explicitly marked synthetic inputs are enabled in this iteration')
    documents, observations, seen = [], [], set()
    for form, filename in sorted(inputs, key=lambda pair: str(Path(pair[1]).resolve())):
        key = Path(filename).resolve()
        if key in seen:
            raise ValueError('Input document supplied more than once')
        seen.add(key)
        doc, rows = read_document(filename, form, root)
        documents.append(doc)
        observations.extend(rows)
    if not observations:
        raise ValueError('No supported glossary observations; nothing validated')
    return proposals(documents, observations)


def export(root, inputs, destination):
    lexical = Path(destination).absolute()
    if any(p.is_symlink() for p in [lexical] + list(lexical.parents)):
        raise ValueError('Symlinked output paths are unsupported')
    root, destination = Path(root).resolve(), lexical.resolve()
    if destination == root or root in destination.parents or destination == KIT or KIT in destination.parents:
        raise ValueError('Output must be outside the input root AND development repository')
    if destination.exists():
        raise FileExistsError('Output directory already exists; never overwrite')
    result = build(root, inputs)
    # Verify snapshot did not change during the read; avoid publishing stale bindings.
    for doc in result['documents']:
        current = (root / doc['document_reference']).read_bytes()
        if hashlib.sha256(current).hexdigest() != doc['sha256']:
            raise ValueError('Input changed during proposal generation')
    destination.mkdir(parents=True, mode=0o700, exist_ok=False)
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    path = destination / 'suggestions.proposed.json'
    with path.open('xb') as handle:
        path.chmod(0o600)
        handle.write(payload)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--synthetic-root', required=True)
    parser.add_argument('--a', action='append', default=[], help='Explicit format-A file; no recursive scan')
    parser.add_argument('--b', action='append', default=[], help='Explicit format-B file')
    parser.add_argument('--out-dir', required=True)
    args = parser.parse_args()
    inputs = [('a', p) for p in args.a] + [('b', p) for p in args.b]
    result = export(args.synthetic_root, inputs, args.out_dir)
    print(json.dumps(result['summary'], ensure_ascii=False))  # never log source content


if __name__ == '__main__':
    main()
