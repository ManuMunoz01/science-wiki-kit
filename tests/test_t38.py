"""T-38 adapter tests; synthetic data only (MIT)."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 't38'))
import diagnostics as d
from make_trial import make


class Trial(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.vault = make(self.base / 'vault')

    def snapshot(self):
        return {str(p.relative_to(self.vault)): p.read_bytes() for p in self.vault.rglob('*') if p.is_file()}

    def test_controlled_errors_and_guards(self):
        before = self.snapshot()
        ctx = d.prepare(self.vault)
        out = self.base / 'lint'
        result = d.audit(ctx, out)
        self.assertEqual(result['notes_loaded'], 6)
        self.assertEqual(result['checks_called'], list(range(1, 34)))
        for counter in ['check3', 'check4', 'check5', 'check14', 'check16', 'check19', 'check23', 'check26', 'check33']:
            self.assertGreater(result['counters'][counter], 0, counter)
        broken = (out / 'wiki_check5_broken_links.txt').read_text()
        self.assertIn('Missing_Controlled_Target', broken)
        self.assertNotIn('Fixture_Project', broken)
        self.assertNotIn('Fuerza máxima', broken)
        self.assertNotIn('Fuerza máxima', result['unicode_vocabulary']['missing'])
        self.assertIn('Ghost_Controlled', result['unicode_vocabulary']['ghost'])
        # Paired guard: changing ONLY the controlled source defect must move its detector.
        p = self.vault / '2. Papers/Fixture2026a.md'
        p.write_bytes(p.read_bytes().replace(b'[[Missing_Controlled_Target]]', b'[[Fixture_Project]]'))
        guarded = d.audit(d.prepare(self.vault), self.base / 'guard')
        self.assertEqual(guarded['counters']['check5'], result['counters']['check5'] - 1)
        p.write_bytes(before['2. Papers/Fixture2026a.md'])
        self.assertEqual(before, self.snapshot())

    def test_bilingual_repeatability_and_alias_change(self):
        before = self.snapshot()
        ctx = d.prepare(self.vault)
        for name in ['a', 'b']:
            d.propose(ctx, self.base / name, '2026-11-12')
        for p in (self.base / 'a').iterdir():
            self.assertEqual(p.read_bytes(), (self.base / 'b' / p.name).read_bytes())
        text = (self.base / 'a/_VOCABULARY.proposed.md').read_text()
        self.assertIn('Fuerza máxima', text)
        self.assertIn('maximal strength', text)
        self.assertIn('Dinamometría', text)
        pairs = d.candidates(d.collect(ctx))
        self.assertEqual(len(pairs), 1)
        self.assertEqual({pairs[0]['left'], pairs[0]['right']}, {'Fuerza máxima', 'Maximal_Strength'})
        self.assertEqual(before, self.snapshot())
        p = self.vault / '4. Temas/Conceptos/Potencia.md'
        p.write_bytes(p.read_bytes().replace(b'potencia, power', b'potencia, power, maximal strength'))
        changed = d.prepare(self.vault)
        self.assertEqual(len(d.candidates(d.collect(changed))), 3)
        d.propose(changed, self.base / 'changed', '2026-11-12')
        self.assertNotEqual(text, (self.base / 'changed/_VOCABULARY.proposed.md').read_text())

    def test_nested_notes_and_collision_rejection(self):
        folder = self.vault / '4. Temas/Conceptos/Nested'
        folder.mkdir()
        p = folder / 'Extra.md'
        p.write_text('---\ntype: concept\nstatus: draft\naliases: [extra]\n---\n')
        self.assertIn('Extra', [r['canonical'] for r in d.collect(d.prepare(self.vault))])
        (folder / 'Potencia.md').write_text(p.read_text())
        with self.assertRaisesRegex(ValueError, 'Ambiguous'):
            d.prepare(self.vault)

    def test_cli_refuses_overwrites_inside_vault_and_empty_scope(self):
        cmd = [sys.executable, str(ROOT / 't38/diagnostics.py'), 'vocabulary', '--vault-root', str(self.vault), '--out-dir']
        out = self.base / 'proposal'
        subprocess.run(cmd + [str(out)], check=True, capture_output=True)
        original = (out / '_VOCABULARY.proposed.md').read_bytes()
        for target in [out, self.vault / 'output']:
            failed = subprocess.run(cmd + [str(target)], capture_output=True)
            self.assertNotEqual(failed.returncode, 0)
        self.assertEqual(original, (out / '_VOCABULARY.proposed.md').read_bytes())
        for p in self.vault.rglob('*.md'):
            p.unlink()
        with self.assertRaisesRegex(ValueError, 'No notes'):
            d.prepare(self.vault)

    def test_single_shared_alias_cross_field_is_review_only(self):
        rows = [{'canonical':'A', 'aliases':['acción'], 'field':'one'},
                {'canonical':'B', 'aliases':['ACCION'], 'field':'two'},
                {'canonical':'C', 'aliases':['different'], 'field':'one'}]
        self.assertEqual(d.vocabulary.find_dupes(rows), [])
        pairs = d.candidates(rows)
        self.assertEqual(len(pairs), 1)
        self.assertFalse(pairs[0]['same_field'])
        self.assertEqual(pairs[0]['action'], 'human-review-only')


if __name__ == '__main__':
    unittest.main()
