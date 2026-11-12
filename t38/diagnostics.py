"""T-38 provisional, read-only adapters. MIT; original kit attribution in ../LICENSE."""
import argparse
import datetime
import importlib.util
import json
from pathlib import Path
import sys
import unicodedata

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT))
from wikikit.config import load_config
from wikikit.lint.context import Context
from wikikit.lint import engine
from wikikit.textio import read_text, write_text

spec = importlib.util.spec_from_file_location('kit_vocabulary', KIT / 'skills/vocabulary-update/scripts/build_vocabulary.py')
vocabulary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vocabulary)


def prepare(vault):
    vault = Path(vault).resolve()
    if not (vault / 'wiki.config.json').is_file():
        raise ValueError('Explicit vault root with wiki.config.json required')
    root, cfg = load_config(vault)
    ctx = Context(root, cfg)
    if not ctx.notes:
        raise ValueError('No notes loaded; zero is not a clean audit')
    for folder in cfg['folders']:
        if not (ctx.wiki / folder).is_dir():
            raise ValueError('Missing configured folder: ' + folder)
    all_notes = [n for notes in ctx.files.values() for n in notes]
    names = [unicodedata.normalize('NFC', n.name).casefold() for n in all_notes]
    if len(names) != len(set(names)):
        raise ValueError('Ambiguous canonical basenames; resolve manually before audit')
    return ctx


def collect(ctx):
    rows = []
    for folder in ctx.cfg['concept_folders']:
        d = ctx.wiki / folder
        paths = d.rglob('*.md') if folder in ctx.cfg['recursive_folders'] else d.glob('*.md')
        # Reuse the upstream parser and source-hint rules for each actual directory.
        for parent in sorted({p.parent for p in paths}):
            cfg = dict(ctx.cfg, concept_folders=[str(parent.relative_to(ctx.wiki))])
            rows.extend(vocabulary.collect(ctx.wiki, cfg))
    return sorted(rows, key=lambda r: r['canonical'])


def candidates(rows):
    """Any shared normalized term is a REVIEW candidate, never an identity assertion."""
    pairs = []
    for i, a in enumerate(rows):
        terms = {vocabulary.norm(t) for t in [a['canonical']] + a['aliases']} - {''}
        for b in rows[i + 1:]:
            shared = sorted(terms & ({vocabulary.norm(t) for t in [b['canonical']] + b['aliases']} - {''}))
            if shared:
                pairs.append({'left': a['canonical'], 'right': b['canonical'], 'shared': shared,
                              'same_field': a['field'] == b['field'], 'action': 'human-review-only'})
    return pairs


def audit(ctx, out):
    counters = engine.run(ctx, out_dir=out, quiet=True)
    vocab = ctx.wiki / ctx.cfg['vocabulary_file']
    # Add a Unicode-aware check, without redefining or concealing upstream Check 30.
    live = {r['canonical'] for r in collect(ctx)}
    listed = set()
    if vocab.is_file():
        import re
        listed = set(re.findall(r'^\|[^\n]*?\[\[([^\]|]+)\]\]', read_text(vocab), re.M))
    scope = {'notes_loaded': len(ctx.notes), 'checks_called': sorted({n for n, _ in engine.ALL_CHECKS}),
             'counters': counters, 'conditional_checks': {
                 '7': 'skipped' if ctx.index_is_bases else 'manual index',
                 '14': 'enabled' if ctx.lcfg['language_radar']['enabled'] else 'disabled',
                 '21': 'cutoff set' if ctx.cfg['synthesis']['prefulltext_cutoff'] else 'no cutoff: inactive',
                 '29': 'prefixes set' if ctx.lcfg['memory_slug_prefixes'] else 'no prefixes: inactive',
                 '30': 'present' if vocab.is_file() else 'missing vocabulary: skipped'},
             'unicode_vocabulary': {'available': vocab.is_file(), 'missing': sorted(live - listed),
                                    'ghost': sorted(listed - live)}}
    write_text(out / 'scope.json', json.dumps(scope, ensure_ascii=False, indent=2) + '\n')
    return scope


def propose(ctx, out, today):
    rows = collect(ctx)
    if not rows:
        raise ValueError('No concepts or methods; nothing to propose')
    text, _, _ = vocabulary.render(rows, ctx.cfg, today)
    write_text(out / '_VOCABULARY.proposed.md', text)
    write_text(out / 'duplicates.proposed.json', json.dumps(candidates(rows), ensure_ascii=False, indent=2) + '\n')
    return {'entries': len(rows), 'candidate_pairs': len(candidates(rows))}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode', choices=['lint', 'vocabulary'])
    p.add_argument('--vault-root', required=True)
    p.add_argument('--out-dir', required=True, help='New directory outside the vault; never reused')
    args = p.parse_args()
    ctx = prepare(args.vault_root)
    out = Path(args.out_dir).resolve()
    if out == ctx.vault.resolve() or ctx.vault.resolve() in out.parents:
        p.error('Output must be outside the vault')
    # Exclusive directory creation prevents overwriting previous reports/proposals.
    out.mkdir(parents=True, exist_ok=False)
    result = audit(ctx, out) if args.mode == 'lint' else propose(ctx, out, datetime.date.today().isoformat())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0  # findings are diagnostics, not a scientific validity gate


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, FileExistsError) as exc:
        sys.exit(str(exc))
