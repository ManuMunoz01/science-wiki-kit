"""Synthetic A/B glossary proposals; no real definitions or sources (MIT)."""
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from t38.bib7.adapter import build, export
from t38.bib1.validate import snapshot


class Glossaries(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'inputs'
        shutil.copytree(ROOT / 't38/bib7/fixtures', self.root)
        self.a = self.root / 'shoulder.synthetic.md'
        self.b = self.root / 'force.synthetic.md'
        self.inputs = [('a', self.a), ('b', self.b)]

    def test_both_formats_preserve_ids_definitions_sources_and_input_bytes(self):
        before = snapshot(self.root)
        result = export(self.root, self.inputs, self.base / 'output')
        self.assertEqual(len(result['observations']), 8)
        a = [r for r in result['observations'] if r['target']['entry_id'] is not None]
        self.assertEqual([r['target']['entry_id'] for r in a], ['H-001', 'H-002', 'H-Á-03', 'H-004'])
        self.assertTrue(all(r['target']['glossary_id'] == 'EXAMPLE:shoulder-glossary' for r in a))
        self.assertNotEqual(a[0]['definitions_or_uses'], a[1]['definitions_or_uses'])
        self.assertEqual(a[0]['declared_citekeys'], ['ExampleA2026'])
        self.assertEqual(a[1]['declared_years'], ['2025'])
        self.assertEqual(a[0]['contexts'], ['Escenario inventado A, no un protocolo real.'])
        self.assertEqual(a[0]['locations'], ['sección sintética A'])
        self.assertEqual(before, snapshot(self.root))
        for row in result['observations']:
            path = self.root / row['target']['locator']['document_reference']
            loc = row['target']['locator']
            self.assertEqual(row['raw_markdown'], ''.join(path.read_bytes().decode().splitlines(keepends=True)[loc['line_start']-1:loc['line_end']]))

    def test_table_multiple_studies_stay_unbound_and_no_ids_created(self):
        result = build(self.root, self.inputs)
        rows = [r for r in result['observations'] if r['target']['format'] == 'markdown-table-without-ids']
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(r['target']['entry_id'] is None and r['target']['glossary_id'] is None for r in rows))
        first = rows[0]
        self.assertEqual(first['source_references'], ['ExampleA2026', 'ExampleD2024'])
        self.assertEqual(len(first['definitions_or_uses']), 1)
        self.assertIn('definición inventada D', first['definitions_or_uses'][0])
        self.assertEqual(first['source_binding'], 'row-level-unresolved')
        self.assertEqual(first['declared_years'], [])  # no year guessed from citekey
        self.assertEqual(first['locations'], [])  # no page invented from mixed prose
        self.assertTrue(all(r['target']['locator']['scope'] == 'snapshot-only-not-a-stable-id' for r in rows))

    def test_relation_kinds_are_separate_unverified_and_never_merged(self):
        result = build(self.root, self.inputs)
        kinds = ('bibliographic_alias_statement', 'bibliographic_identity_candidate', 'dataset_relationship_review')
        for kind in kinds:
            group = [s for s in result['suggestions'] if s['kind'] == kind]
            self.assertEqual(len(group), 1)
            self.assertEqual(group[0]['verification'], 'not-verified')
            self.assertEqual(len(group[0]['related_source_references']), 2)
        overlap = [s for s in result['suggestions'] if s['kind'] == 'terminology_overlap']
        self.assertEqual(len(overlap), 3)
        self.assertTrue(all(s['dataset_relationship'] == 'not-inferred' and s['synonymy'] == 'not-established' for s in overlap))
        self.assertTrue(all(s['action'] == 'none' and s['status'] == 'pending-review' for s in result['suggestions']))

    def test_same_source_or_similar_words_do_not_imply_duplicate_alias_or_dataset(self):
        self.a.write_text('## Ensayo uno\n### H-010 · Example (2026)\nTérmino original: synthetic load\nCitekey: Same2026\n'
                          '## Ensayo dos\n### H-011 · Example (2026)\nTérmino original: synthetic loading\nCitekey: Same2026\n')
        result = build(self.root, [('a', self.a)])
        kinds = {s['kind'] for s in result['suggestions']}
        self.assertFalse(kinds & {'terminology_overlap','bibliographic_alias_statement','bibliographic_identity_candidate','dataset_relationship_review'})
        self.assertEqual(len(result['observations']), 2)

    def test_comments_and_fences_do_not_create_fake_entries_or_relations(self):
        original = build(self.root, [('a', self.a)])
        with self.a.open('a') as f:
            f.write('\n<!--\n### H-FAKE · Hidden (2026)\nAlias bibliográfico: [[X]] -> [[Y]]\n-->\n'
                    '```markdown\n### H-CODE · Example (2026)\nPosible reutilización de datos: [[X]] -> [[Y]]\n```\n')
        result = build(self.root, [('a', self.a)])
        self.assertEqual(len(result['observations']), len(original['observations']))
        self.assertFalse(any('FAKE' in r['target']['entry_id'] or 'CODE' in r['target']['entry_id'] for r in result['observations']))
        self.assertEqual(result['summary']['suggestions_by_kind'], original['summary']['suggestions_by_kind'])
        self.assertIn('H-FAKE', result['observations'][-1]['raw_markdown'])

    def test_repeated_fields_unknown_text_crlf_and_escaped_table_pipe_preserved(self):
        text = self.a.read_text().replace('Definición: Definición inventada B DISTINTA para el mismo concepto.',
                    'Definición: Definición inventada B DISTINTA para el mismo concepto.\nDefinición: Otra formulación inventada B2.\nCampo libre: no descartar\ncontinuación libre')
        self.a.write_bytes(text.replace('\n','\r\n').encode())
        before = self.a.read_bytes()
        result = build(self.root, self.inputs)
        a = next(r for r in result['observations'] if r['target']['entry_id'] == 'H-002')
        self.assertEqual(len(a['definitions_or_uses']), 2)
        self.assertTrue(any(f['label'] == 'Campo libre' and 'continuación libre' in f['value'] for f in a['fields']))
        self.assertIn('\r\n', a['raw_markdown'])
        self.assertEqual(before, self.a.read_bytes())
        self.assertEqual(result['summary']['parse_diagnostics'], 0)
        self.assertTrue(any('\\| literal' in r['canonical'] for r in result['observations']))
        escaped = next(r for r in result['observations'] if '\\| literal' in r['canonical'])
        self.assertEqual(escaped['source_references'], ['ExampleA2026'])

    def test_unsupported_rows_headers_and_duplicate_ids_are_loud_not_dropped(self):
        with self.b.open('a') as f:
            f.write('| malformed | extra | cell | fourth |\n\n| Unknown | Header | X |\n|---|---|---|\n| a | b | c |\n')
        with self.a.open('a') as f:
            f.write('\n### H-001 · Repeated ID (2026)\nDefinición: preserve this separate record\n')
        result = build(self.root, self.inputs)
        diagnostics = [d for doc in result['documents'] for d in doc['diagnostics']]
        self.assertIn('unsupported-table-row', [d['code'] for d in diagnostics])
        self.assertIn('unsupported-table-header', [d['code'] for d in diagnostics])
        self.assertTrue(any('fourth' in d.get('raw_markdown','') for d in diagnostics))
        self.assertEqual(sum(r['target']['entry_id'] == 'H-001' for r in result['observations']), 2)
        self.assertTrue(any('duplicate-entry-id' in s.get('pending_fields',[]) for s in result['suggestions']))

    def test_missing_values_remain_pending_and_malformed_relation_not_inferred(self):
        with self.a.open('a') as f:
            f.write('Alias bibliográfico: [[OnlyOne]]\nAño: 2025\n')
        result = build(self.root, self.inputs)
        missing = next(r for r in result['observations'] if r['target']['entry_id'] == 'H-Á-03')
        self.assertEqual(missing['source_references'], [])
        self.assertIn('location', missing['pending'])
        self.assertIn('definition-or-use', missing['pending'])
        self.assertEqual(missing['definitions_or_uses'], ['pendiente'])
        self.assertTrue(any('relationship-binding' in s.get('pending_fields',[]) for s in result['suggestions']))
        self.assertEqual(sum(s['kind'] == 'bibliographic_alias_statement' for s in result['suggestions']), 1)
        conflict = next(r for r in result['observations'] if r['target']['entry_id'] == 'H-004')
        self.assertEqual(conflict['declared_years'], ['2025', '2026'])
        self.assertIn('conflicting-declared-years', conflict['pending'])

    def test_repeatable_proposals_independent_of_argument_order_snapshot_changes(self):
        first = export(self.root, self.inputs, self.base / 'one')
        export(self.root, list(reversed(self.inputs)), self.base / 'two')
        self.assertEqual((self.base/'one/suggestions.proposed.json').read_bytes(), (self.base/'two/suggestions.proposed.json').read_bytes())
        with self.b.open('a') as f: f.write('\n')
        changed = build(self.root, self.inputs)
        before = next(r for r in first['observations'] if r['target']['entry_id'] is None)
        after = next(r for r in changed['observations'] if r['target']['entry_id'] is None)
        self.assertNotEqual(before['target']['locator']['snapshot_sha256'], after['target']['locator']['snapshot_sha256'])
        self.assertIsNone(after['target']['entry_id'])

    def test_no_overwrite_or_repository_output_private_permissions(self):
        out = self.base / 'out'
        export(self.root, self.inputs, out)
        original = (out/'suggestions.proposed.json').read_bytes()
        with self.assertRaises(FileExistsError): export(self.root, self.inputs, out)
        for target in (self.root/'output', ROOT/'_temp/bib7-forbidden-output'):
            with self.assertRaises(ValueError): export(self.root, self.inputs, target)
        self.assertEqual(original, (out/'suggestions.proposed.json').read_bytes())
        if os.name == 'posix':
            self.assertEqual(stat.S_IMODE(out.stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE((out/'suggestions.proposed.json').stat().st_mode), 0o600)

    def test_unmarked_outside_duplicate_and_symlink_inputs_refused(self):
        with self.assertRaises(ValueError): build(self.root, self.inputs * 2)
        outside = self.base/'outside.md';outside.write_text(self.a.read_text())
        with self.assertRaises(ValueError): build(self.root, [('a',outside)])
        link = self.root/'link.md';link.symlink_to(self.a)
        with self.assertRaises(ValueError): build(self.root, [('a',link)])
        directory_link = self.root/'linked';directory_link.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError): build(self.root, [('a',directory_link/self.a.name)])
        output_link = self.base/'output-link';output_link.symlink_to(self.base/'not-created')
        with self.assertRaises(ValueError): export(self.root,self.inputs,output_link)
        (self.root/'.t38-synthetic').unlink()
        with self.assertRaises(ValueError): build(self.root,self.inputs)

    def test_cli_metadata_only_and_optional_outer_pipes_empty_scope_rejected(self):
        # Valid three-column Markdown does not require outer pipes.
        self.b.write_text('## Synthetic\nTérmino | Uso documentado y localización | Fuente\n---|---|---\nPrueba | uso sin verificar | [@Example2026]\n')
        cmd = [sys.executable, str(ROOT/'t38/bib7/adapter.py'), '--synthetic-root',str(self.root), '--b',str(self.b),'--out-dir',str(self.base/'cli')]
        proc = subprocess.run(cmd,check=True,capture_output=True,text=True)
        self.assertEqual(json.loads(proc.stdout)['observations'],1)
        self.assertNotIn('Example2026',proc.stdout)
        self.assertEqual(len(build(self.root,[('b',self.b)])['observations']),1)
        self.b.write_text('# No recognized glossary entries\n')
        with self.assertRaisesRegex(ValueError,'No supported'):build(self.root,[('b',self.b)])


if __name__ == '__main__':
    unittest.main()
