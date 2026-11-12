"""Local Skill wiring/integrity and safe synthetic invocation (MIT)."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from t38.bib9.check import layout,originals
from t38.bib9.smoke import run
from t38.bib1.validate import snapshot
from t38.probe_codex_skills import probe


class SkillPreparation(unittest.TestCase):
    def copy_layout(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root=Path(temp.name)/'repo'
        root.mkdir()
        for folder in ('.agents','skills','t38'):
            shutil.copytree(ROOT/folder,root/folder,ignore=shutil.ignore_patterns('__pycache__'))
        return root

    def test_five_modes_and_all_original_dependency_blobs_preserved(self):
        modes=layout()['canonical_entries']
        self.assertEqual(len(modes),5)
        self.assertEqual(sum(m=='planning-only' for m in modes.values()),3)
        integrity=originals()
        self.assertEqual(integrity['original_files_verified'],134)
        self.assertEqual(sum(integrity['skill_file_counts'].values()),21)

    def test_broken_dependency_and_missing_policy_are_not_valid_structure(self):
        root=self.copy_layout()
        path=root/'.agents/skills/wiki-lint/SKILL.md'
        text=path.read_text()
        path.write_text(text.replace('../../../t38/bib1/README.md','../../../MISSING.md'))
        with self.assertRaisesRegex(ValueError,'Broken/outside'):layout(root)
        path.write_text(text)
        (root/'t38/bib9/POLICY.md').unlink()
        with self.assertRaisesRegex(ValueError,'policy missing'):layout(root)

    def test_held_workflow_cannot_be_wired_to_an_executable_adapter(self):
        root=self.copy_layout()
        path=root/'t38/bib9/entrypoints.json'
        cfg=json.loads(path.read_text())
        cfg['entries'][2]['adapter']='tools/seal.py'
        path.write_text(json.dumps(cfg))
        with self.assertRaisesRegex(ValueError,'Planning-only'):layout(root)

    def test_aliases_delegate_and_explicit_only_metadata_is_checked(self):
        root=self.copy_layout()
        self.assertEqual(len(layout(root)['legacy_aliases']),2)
        metadata=root/'.agents/skills/wiki-ingest/agents/openai.yaml'
        metadata.write_text(metadata.read_text().replace('false','true'))
        with self.assertRaisesRegex(ValueError,'Explicit-only'):layout(root)

    def test_existing_adapters_invoke_with_synthetic_inputs_only(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        out=Path(temp.name)/'run'
        before=snapshot(ROOT/'t38/bib7/fixtures')
        result=run(out)
        self.assertEqual(result['wiki-lint']['exit_code'],0)
        self.assertEqual(result['vocabulary-update']['exit_code'],0)
        self.assertFalse(result['invariants']['planning_only_scripts_executed'])
        self.assertEqual(before,snapshot(ROOT/'t38/bib7/fixtures'))
        with self.assertRaises(FileExistsError):run(out)
        with self.assertRaises(ValueError):run(ROOT/'_temp/bib9-forbidden')

    def test_native_startup_failure_is_not_reported_as_success(self):
        with patch('t38.probe_codex_skills.subprocess.Popen',side_effect=PermissionError('synthetic read-only state')):
            with self.assertRaises(PermissionError):probe(expected=layout()['canonical_entries'])


if __name__=='__main__':unittest.main()
