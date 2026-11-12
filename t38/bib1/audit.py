"""Read-only Oficina profile for explicitly synthetic vaults; stdlib only, MIT.

No transformation of source metadata, template rendering, network access or repairs.
Findings contain paths/codes only, never source text or scientific approval.
"""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

KIT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KIT))
from wikikit.lint.context import Context
from wikikit.lint.engine import ALL_CHECKS
from wikikit.config import _merge, _derive, DEFAULTS
from wikikit.textio import read_text, write_text


def scalar(value):
    value = value.strip()
    if value.startswith('"'):
        return json.loads(value)
    if value.startswith("'"):
        if not value.endswith("'"):
            raise ValueError('Unclosed quoted scalar')
        return value[1:-1].replace("''", "'")
    if value.lower() in ('null', '~'):
        return ''
    if value.startswith(('{', '|', '>', '&', '*', '!')) or ': ' in value:
        raise ValueError('Unsupported YAML scalar')
    return value


def tokens(value):
    """Split a flat YAML inline sequence/comment outside quoted strings."""
    out, buf, quote, escape = [], '', '', False
    for char in value:
        if escape:
            buf += char
            escape = False
        elif quote:
            buf += char
            if char == '\\' and quote == '"':
                escape = True
            elif char == quote:
                quote = ''
        elif char in ('"', "'"):
            quote = char
            buf += char
        elif char == '#':
            break
        elif char == ',':
            out.append(buf.strip())
            buf = ''
        else:
            buf += char
    if quote:
        raise ValueError('Unclosed YAML quote')
    out.append(buf.strip())
    return out


def parse(text):
    """Strict flat subset only. Unsupported YAML is deferred, never silently accepted."""
    lines = text.lstrip('\ufeff').splitlines()
    if not lines or lines[0] != '---':
        raise ValueError('Missing YAML frontmatter')
    end = next((i for i in range(1, len(lines)) if lines[i] == '---'), None)
    if end is None:
        raise ValueError('Unclosed YAML frontmatter')
    fm, key = {}, None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        item = re.fullmatch(r'\s+-\s+(.+)', line)
        if item and key and isinstance(fm[key], list):
            fm[key].append(scalar(tokens(item[1])[0]))
            continue
        match = re.fullmatch(r'([\w-]+):\s*(.*)', line)
        if not match or match[1] in fm:
            raise ValueError('Unsupported or duplicate YAML field')
        key, value = match.groups()
        if not value:
            fm[key] = []
        elif value.startswith('['):
            # Remove a trailing comment only after the closing bracket.
            match_list = re.fullmatch(r'\[(.*)\]\s*(?:#.*)?', value)
            if not match_list:
                raise ValueError('Unsupported YAML list')
            fm[key] = [scalar(t) for t in tokens(match_list[1]) if t]
        else:
            parts = tokens(value)
            # An unquoted comma is legal in a plain YAML scalar; preserve it.
            fm[key] = scalar(','.join(parts))
    return fm, '\n'.join(lines[end + 1:])


def clean(body):
    """Ignore comments/code for link diagnostics; preserve lines for structural checks separately."""
    body = re.sub(r'<!--.*?-->', '', body, flags=re.S)
    body = re.sub(r'^\s*(`{3,}|~{3,}).*?^\s*\1\s*$', '', body, flags=re.M | re.S)
    return re.sub(r'`[^`\n]*`', '', body)


def load(vault):
    vault = Path(vault).resolve()
    if not (vault / '.t38-synthetic').is_file():
        raise ValueError('Only an explicitly marked synthetic vault is supported')
    cfg = json.loads(read_text(vault / 'wiki.config.json'))
    if cfg.get('profile') != 'oficina-bib1-synthetic' or cfg.get('synthetic_only') is not True:
        raise ValueError('Wrong or non-synthetic profile')
    if set(cfg['structural_checks']) - {26, 27}:
        raise ValueError('Only schema-independent structural kit checks are permitted')
    notes = []
    ignore = set(cfg['ignore_dirs'])
    for p in sorted(vault.rglob('*.md')):
        if any(part in ignore for part in p.relative_to(vault).parts[:-1]):
            continue
        if p.is_symlink() or vault not in p.resolve().parents:
            raise ValueError('Symlinked or external note is unsupported')
        role = 'paper' if cfg['papers_folder'] in p.relative_to(vault).parts else 'other'
        if cfg['themes_folder'] in p.relative_to(vault).parts:
            role = 'theme'
        text = read_text(p)
        templated = bool(re.search(r'{{|{%|{#', text))
        try:
            fm, body = parse(text)
            error = None
        except (ValueError, json.JSONDecodeError):
            fm, body, error = {}, text, 'yaml-unparsed'
        notes.append({'path':p,'name':p.stem,'role':role,'fm':fm,'body':body,
                      'template':templated,'parse_error':error})
    audited = [n for n in notes if n['role'] in ('paper', 'theme')]
    if not audited:
        raise ValueError('Empty audit scope')
    return vault, cfg, notes


def section(body, heading):
    match = re.search(r'^##\s+' + re.escape(heading) + r'\s*\n(.*?)(?=^##\s|\Z)', body, re.M | re.S)
    return match[1] if match else ''


def diagnose(vault):
    vault, cfg, notes = load(vault)
    findings = []
    def add(note, code, level='documentary', field=None):
        row = {'note':str(note['path'].relative_to(vault)), 'code':code, 'category':level}
        if field:
            row['field'] = field
        findings.append(row)
    index = defaultdict(list)
    paths = {}
    for n in notes:
        index[n['name'].casefold()].append(n)
        paths[n['path'].relative_to(vault).as_posix()] = n
    citekeys = defaultdict(list)
    for n in notes:
        if n['role'] not in ('paper', 'theme'):
            continue
        if n['template']:
            add(n, 'template-not-rendered', 'deferred')
            continue
        if n['parse_error']:
            add(n, n['parse_error'], 'deferred')
            continue
        fm = n['fm']
        if n['role'] == 'paper':
            for field in cfg['fields']:
                if field not in fm:
                    add(n, 'field-absent', 'review', field)
            for field in ('full_text_status', 'review_status', 'study_type'):
                value = fm.get(field)
                if not value:
                    add(n, 'unassigned-metadata', 'pending-scientific-review', field)
                elif not isinstance(value, str) or value not in cfg[field]:
                    add(n, 'invalid-controlled-value', field=field)
            topic = fm.get('topic')
            if not topic:
                add(n, 'unassigned-topic', 'pending-scientific-review', 'topic')
            elif not isinstance(topic, str) or topic not in cfg['taxonomy']:
                add(n, 'invalid-topic', field='topic')
            subtopics = fm.get('subtopic', [])
            if subtopics and not isinstance(subtopics, list):
                add(n, 'subtopic-must-be-list', field='subtopic')
            elif isinstance(subtopics, list):
                for sub in subtopics:
                    if sub.endswith(cfg['pending_suffix']):
                        add(n, 'proposed-subtopic-awaiting-approval', 'decision', 'subtopic')
                    elif isinstance(topic, str) and topic in cfg['taxonomy'] and sub not in cfg['taxonomy'][topic]:
                        add(n, 'subtopic-outside-topic', field='subtopic')
            for field in ('title', 'journal', 'citekey'):
                value = fm.get(field)
                if not value:
                    add(n, 'metadata-incomplete', 'review', field)
                elif not isinstance(value, str):
                    add(n, 'metadata-must-be-scalar', field=field)
            key = fm.get('citekey')
            if isinstance(key, str) and key:
                citekeys[key].append(n)
                if key != n['name']:
                    add(n, 'filename-citekey-difference', 'review', 'citekey')
            headings = re.findall(r'^##\s+(.+?)\s*$', clean(n['body']), re.M)
            last = cfg['keywords_heading']
            if last in headings and headings[-1] != last:
                add(n, 'keywords-not-last-heading')
            if not section(clean(n['body']), cfg['source_scope_heading']).strip():
                add(n, 'source-scope-awaits-documentation', 'pending-scientific-review')
        body = clean(n['body'])
        links = [(m[1].replace('\\|', '|').split('|')[0].split('#')[0].strip(), False)
                 for m in re.finditer(r'!?\[\[([^\]]+)\]\]', body)]
        links += [(m[1], True) for m in re.finditer(r'(?<!!)\[[^\]\n]*\]\(([^\s]+)\)', body)]
        for raw, markdown in links:
            target = unquote(raw).split('#')[0]
            scheme = urlsplit(target).scheme
            if scheme:
                add(n, 'zotero-reference-not-verified' if scheme == 'zotero' else 'external-reference-not-verified', 'review')
                continue
            if not target:
                continue
            # Obsidian wikilinks are vault-relative; Markdown paths are note-relative.
            if target.lower().endswith('.pdf'):
                base = n['path'].parent if markdown else vault
                p = (base / target).resolve()
                if vault not in p.parents:
                    add(n, 'pdf-path-outside-synthetic-vault', 'deferred')
                else:
                    add(n, 'pdf-present-identity-and-reading-unverified' if p.is_file() else 'pdf-link-missing',
                        'review' if p.is_file() else 'documentary')
                continue
            lookup = target if target.endswith('.md') else target + '.md'
            if markdown:
                local = (n['path'].parent / lookup).resolve()
                matches = [x for x in notes if x['path'] == local]
            elif '/' in target:
                matches = [paths[lookup]] if lookup in paths else []
            else:
                matches = index.get(Path(target).stem.casefold(), [])
            if not matches:
                add(n, 'broken-note-link')
            elif len(matches) > 1:
                add(n, 'ambiguous-note-link', 'review')
        # Embedded PDF not present is documentary; an absent PDF SECTION/link is not:
        # HTML full text is legitimate, and no route is guessed from citekey.
    for group in citekeys.values():
        if len(group) > 1:
            for n in group:
                add(n, 'duplicate-citekey-needs-alias-review', 'review')
    # Reuse only schema-independent kit checks. No injected type/status/venue/seals.
    user = {'wiki_root':'.', 'folders':[cfg['papers_folder'], cfg['themes_folder']],
            'recursive_folders':[cfg['papers_folder'], cfg['themes_folder']], 'lint':{'stub_exempt_checks':[]}}
    ctx = Context(vault, _derive(_merge(DEFAULTS, user), user))
    # Remove template/unparsed entries from in-memory checks only; original bytes untouched.
    ready = {n['path'] for n in notes if not n['template'] and not n['parse_error']}
    ctx.notes = {k:n for k,n in ctx.notes.items() if n.path in ready}
    structural = [n for files in ctx.files.values() for n in files if n.path in ready]
    for note in structural:
        ctx.notes = {note.name:note}
        for num, fn in ALL_CHECKS:
            if num in cfg['structural_checks']:
                result = fn(ctx)
                for lines in result.files.values():
                    for row in lines:
                        findings.append({'note':str(note.path.relative_to(vault)),
                                         'code':'kit-check-' + str(num), 'category':'documentary'})
    return {'profile':cfg['profile'], 'notes_loaded':sum(n['role'] in ('paper', 'theme') for n in notes),
            'template_deferred':sum(n['template'] for n in notes if n['role'] in ('paper', 'theme')),
            'kit_checks_run':cfg['structural_checks'], 'findings':findings,
            'counts':dict(Counter(row['category'] for row in findings)),
            'scientific_validity':'not-assessed', 'sources':'synthetic-only'}


def normalize(s):
    return ' '.join(re.sub(r'[^\w]+', ' ', ''.join(c for c in unicodedata.normalize('NFKD', s.casefold())
                                               if not unicodedata.combining(c))).split())


def vocabulary(vault):
    vault, cfg, notes = load(vault)
    path = vault / cfg['glossary_records']
    if not path.is_file():
        return {'status':'pending-structured-extraction', 'records':[], 'candidates':[]}
    source_index = {n['path'].relative_to(vault).as_posix():n for n in notes if n['role'] == 'paper'}
    rows = json.loads(read_text(path))
    required = ('id', 'canonical', 'aliases', 'source_note', 'citekey', 'year', 'location', 'definition', 'definition_kind', 'context')
    ids = set()
    by_topic = defaultdict(list)
    for row in rows:
        if any(key not in row for key in required) or row['id'] in ids:
            raise ValueError('Incomplete or duplicate synthetic glossary record')
        if any(not isinstance(row[key], str) for key in required if key != 'aliases'):
            raise ValueError('Glossary fields must be explicit text')
        ids.add(row['id'])
        if not isinstance(row['aliases'], list) or not all(isinstance(a, str) for a in row['aliases']):
            raise ValueError('Aliases must be an explicit list, never inferred')
        source = source_index.get(row['source_note'])
        if not source or source['template'] or source['parse_error'] or source['fm'].get('citekey') != row['citekey']:
            raise ValueError('Glossary source/citekey cannot be resolved exactly')
        topic = source['fm'].get('topic')
        by_topic[topic if isinstance(topic, str) and topic else '(unassigned)'].append(row['id'])
        if row['year'] != source['fm'].get('year'):
            raise ValueError('Glossary source year mismatch')
    pairs = []
    for i, a in enumerate(rows):
        for b in rows[i + 1:]:
            shared = sorted({normalize(t) for t in [a['canonical']] + a['aliases']} &
                            {normalize(t) for t in [b['canonical']] + b['aliases']} - {''})
            if shared:
                pairs.append({'left':a['id'], 'right':b['id'], 'shared':shared,
                              'action':'review-terminology-not-merge', 'synonymy':'not-established'})
    return {'status':'synthetic-proposal-only', 'records':rows, 'candidates':pairs,
            'scientific_validity':'not-assessed', 'chronological_origin':'not-inferred',
            'by_topic':dict(by_topic)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode', choices=['lint', 'vocabulary'])
    p.add_argument('--vault-root', required=True)
    p.add_argument('--out-dir', required=True)
    args = p.parse_args()
    vault = Path(args.vault_root).resolve()
    out = Path(args.out_dir).resolve()
    if out == vault or vault in out.parents:
        p.error('Output must be a new directory outside the synthetic vault')
    result = diagnose(vault) if args.mode == 'lint' else vocabulary(vault)
    out.mkdir(parents=True, exist_ok=False)
    write_text(out / (args.mode + '.proposed.json'), json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'mode':args.mode, 'notes_loaded':result.get('notes_loaded'),
                      'records':len(result.get('records', [])), 'counts':result.get('counts', {}),
                      'status':result.get('status', 'diagnostics-only')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
