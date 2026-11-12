"""Guide-derived BIB-1 behavior; invented content only (MIT)."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from t38.bib1 import audit
from t38.bib1.make_trial import make


class Bib1(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.vault = make(self.base / 'vault')

    def snap(self):
        return {str(p.relative_to(self.vault)):p.read_bytes() for p in self.vault.rglob('*') if p.is_file()}

    def findings(self, name=None):
        rows = audit.diagnose(self.vault)['findings']
        return [r for r in rows if name is None or r['note'].endswith(name)]

    def replace(self, filename, before, after):
        p = self.vault / filename
        old = p.read_text()
        self.assertIn(before, old)
        p.write_text(old.replace(before, after), encoding='utf-8')

    def test_controlled_errors_without_kit_fields(self):
        before = self.snap()
        result = audit.diagnose(self.vault)
        self.assertEqual(result['notes_loaded'], 6)
        self.assertEqual(result['kit_checks_run'], [26, 27])
        bad = self.findings('Fixture2026bad.md')
        self.assertEqual({r['field'] for r in bad if r['code'] == 'invalid-controlled-value'}, {'full_text_status', 'review_status', 'study_type'})
        for code in ('broken-note-link', 'pdf-link-missing', 'kit-check-26', 'subtopic-outside-topic', 'keywords-not-last-heading'):
            self.assertIn(code, [r['code'] for r in bad])
        self.assertEqual(before, self.snap())
        for path, data in before.items():
            if path.startswith('2. Papers/'):
                for key in ('type:', 'status:', 'evidence_level:', 'concepts_touched:', 'source_verification:', 'venue:'):
                    self.assertFalse(any(line.startswith(key) for line in data.decode().splitlines()))

    def test_valid_multisubtopic_html_and_unverified_pdf(self):
        a = self.findings('Fixture2026a.md')
        self.assertFalse([r for r in a if r['category'] == 'documentary'])
        self.assertIn('zotero-reference-not-verified', [r['code'] for r in a])
        self.assertFalse(any(r['code'].startswith('pdf-') for r in a))
        b = self.findings('Fixture2026b.md')
        self.assertIn('pdf-present-identity-and-reading-unverified', [r['code'] for r in b])
        self.assertNotIn('invalid-controlled-value', [r['code'] for r in b])
        self.assertEqual(audit.diagnose(self.vault)['scientific_validity'], 'not-assessed')

    def test_pending_states_and_template_expressions(self):
        pending = self.findings('Fixture2026pending.md')
        self.assertFalse([r for r in pending if r['category'] == 'documentary'])
        self.assertTrue([r for r in pending if r['category'] == 'pending-scientific-review'])
        self.assertEqual([r['code'] for r in self.findings('Fixture2026template.md')], ['template-not-rendered'])
        self.assertFalse(any('5. Templates' in r['note'] for r in self.findings()))

    def test_taxonomy_pending_suffix_exact_accents_and_single_topic(self):
        f = '2. Papers/Fixture2026a.md'
        self.replace(f, '["anatomia", "deportistas"]', '["anatomia", "categoria-nueva (pendiente)"]')
        rows = self.findings('Fixture2026a.md')
        self.assertIn('proposed-subtopic-awaiting-approval', [r['code'] for r in rows])
        self.assertNotIn('subtopic-outside-topic', [r['code'] for r in rows])
        self.replace(f, 'topic: "hombro"', 'topic: ["hombro", "fuerza"]')
        self.assertIn('invalid-topic', [r['code'] for r in self.findings('Fixture2026a.md')])
        cfg = json.loads((self.vault / 'wiki.config.json').read_text())
        self.assertIn('clasificación-movimientos', cfg['taxonomy']['inteligencia-artificial-hombro'])
        self.assertNotIn('clasificacion-movimientos', cfg['taxonomy']['inteligencia-artificial-hombro'])

    def test_link_positive_guard_and_path_disambiguation(self):
        before = len([r for r in self.findings() if r['code'] == 'broken-note-link'])
        self.replace('2. Papers/Fixture2026bad.md', '[[Missing_Controlled]]', '[[4. Temas/Término sintético\\|nombre visible]]')
        self.assertEqual(len([r for r in self.findings() if r['code'] == 'broken-note-link']), before - 1)
        p = self.vault / '4. Temas/Fixture2026b.md'
        p.write_text('---\naliases: []\n---\n# Invented collision\n', encoding='utf-8')
        self.assertIn('ambiguous-note-link', [r['code'] for r in self.findings('Fixture2026a.md')])
        self.replace('2. Papers/Fixture2026a.md', '[[Fixture2026b|otra ficha]]', '[[2. Papers/Fixture2026b|otra ficha]]')
        self.assertNotIn('ambiguous-note-link', [r['code'] for r in self.findings('Fixture2026a.md')])

    def test_mojibake_positive_and_accent_guard(self):
        p = self.vault / '4. Temas/Término sintético.md'
        original = p.read_bytes()
        self.assertNotIn('kit-check-27', [r['code'] for r in self.findings(p.name)])
        p.write_bytes(original + '\nRÂ²\n'.encode())
        self.assertIn('kit-check-27', [r['code'] for r in self.findings(p.name)])

    def test_vocabulary_source_specific_definitions_alias_delta(self):
        before = self.snap()
        result = audit.vocabulary(self.vault)
        self.assertEqual(len(result['records']), 3)
        self.assertEqual(len(result['candidates']), 1)
        a, b, _ = result['records']
        self.assertEqual(a['canonical'], b['canonical'])
        self.assertNotEqual(a['definition'], b['definition'])
        self.assertNotEqual(a['citekey'], b['citekey'])
        self.assertEqual(result['candidates'][0]['synonymy'], 'not-established')
        self.assertEqual(result, audit.vocabulary(self.vault))
        self.assertEqual(before, self.snap())
        path = self.vault / 'glossary.synthetic.json'
        rows = json.loads(path.read_text())
        rows[2]['aliases'].append('synthetic load')
        path.write_text(json.dumps(rows))
        self.assertEqual(len(audit.vocabulary(self.vault)['candidates']), 3)
        rows[0]['citekey'] = 'MissingSource'
        path.write_text(json.dumps(rows))
        with self.assertRaisesRegex(ValueError, 'source/citekey'):
            audit.vocabulary(self.vault)

    def test_yaml_subset_and_duplicate_citekey_review(self):
        fm, _ = audit.parse('---\ntitle: "A, B: C" # comment\nsubtopic:\n  - anatomia\n  - deportistas\nreview_status: reviewed # comment\n---\n')
        self.assertEqual(fm['title'], 'A, B: C')
        self.assertEqual(fm['subtopic'], ['anatomia', 'deportistas'])
        self.assertEqual(fm['review_status'], 'reviewed')
        for text in ('---\ntitle: A\ntitle: B\n---\n', '---\ntitle: |\n  complex\n---\n'):
            with self.assertRaises(ValueError):
                audit.parse(text)
        self.replace('2. Papers/Fixture2026b.md', 'citekey: "Fixture2026b"', 'citekey: "Fixture2026a"')
        duplicates = [r for r in self.findings() if r['code'] == 'duplicate-citekey-needs-alias-review']
        self.assertEqual(len(duplicates), 2)
        self.assertTrue(all(r['category'] == 'review' for r in duplicates))

    def test_cli_repeatability_refusals_no_inference(self):
        before = self.snap()
        cmd = [sys.executable, str(ROOT / 't38/bib1/audit.py'), 'vocabulary', '--vault-root', str(self.vault), '--out-dir']
        for name in ('a', 'b'):
            subprocess.run(cmd + [str(self.base / name)], check=True, capture_output=True)
        self.assertEqual((self.base / 'a/vocabulary.proposed.json').read_bytes(), (self.base / 'b/vocabulary.proposed.json').read_bytes())
        for target in (self.base / 'a', self.vault / 'out'):
            self.assertNotEqual(subprocess.run(cmd + [str(target)], capture_output=True).returncode, 0)
        self.assertEqual(before, self.snap())
        (self.vault / 'glossary.synthetic.json').unlink()
        self.assertEqual(audit.vocabulary(self.vault)['status'], 'pending-structured-extraction')
        (self.vault / '.t38-synthetic').unlink()
        with self.assertRaisesRegex(ValueError, 'synthetic'):
            audit.diagnose(self.vault)


if __name__ == '__main__':
    unittest.main()
