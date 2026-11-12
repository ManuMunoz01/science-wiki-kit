"""Read-only structural/integrity preflight; NOT a native Codex Skill validator (MIT)."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

KIT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KIT))
from t38.bib1.audit import parse


def layout(root=KIT):
    root = Path(root).resolve()
    cfg = json.loads((root/'t38/bib9/entrypoints.json').read_text())
    if not (root/cfg['shared_policy']).is_file():
        raise ValueError('Shared policy missing')
    modes = {}
    for entry in cfg['entries']:
        folder = root/'.agents/skills'/entry['name']
        path = folder/'SKILL.md'
        fm, body = parse(path.read_text())
        if fm.get('name') != entry['name'] or not isinstance(fm.get('description'), str) or not fm['description'].strip():
            raise ValueError('Invalid local Skill frontmatter: '+entry['name'])
        if len(fm['name']) > 64 or len(fm['description']) > 1024:
            raise ValueError('Oversize Skill metadata')
        if 'shared policy' not in body or 'POLICY.md' not in body:
            raise ValueError('Missing policy binding')
        for link in re.findall(r'\]\(([^)]+)\)', body):
            resolved = (folder/link).resolve()
            if root not in resolved.parents or not resolved.is_file():
                raise ValueError('Broken/outside Skill dependency: '+link)
        metadata = (folder/'agents/openai.yaml').read_text()
        if 'allow_implicit_invocation: false' not in metadata:
            raise ValueError('Explicit-only metadata request missing')
        if not (root/entry['original']/'SKILL.md').is_file():
            raise ValueError('Original package missing')
        if entry['mode']=='planning-only':
            if entry['adapter'] is not None or 'planning only' not in body.lower():
                raise ValueError('Planning-only entry has an executable adapter')
        elif not (root/entry['adapter']).is_file():
            raise ValueError('Existing adapter missing')
        modes[entry['name']] = entry['mode']
    if set(modes) != {'wiki-lint','vocabulary-update','wiki-ingest','wiki-synthesize','wiki-ingest-book'}:
        raise ValueError('Expected exactly five canonical entries')
    for alias, target in cfg['legacy_aliases'].items():
        fm, body = parse((root/'.agents/skills'/alias/'SKILL.md').read_text())
        if fm.get('name') != alias or '../'+target+'/SKILL.md' not in body:
            raise ValueError('Legacy alias not delegated')
    return {'canonical_entries':modes, 'legacy_aliases':cfg['legacy_aliases'],
            'native_validation':'not-performed-by-this-check'}


def originals(root=KIT):
    root = Path(root).resolve()
    manifest = json.loads((root/'t38/conciliation/preservation-manifest.json').read_text())
    count = 0
    for row in manifest['files']:
        path = root/row['path']
        if not path.is_file():
            raise ValueError('Original dependency missing: '+row['path'])
        actual = subprocess.check_output(['git','hash-object','--path='+row['path'],row['path']],cwd=root,text=True).strip()
        if actual != row['git_blob']:
            raise ValueError('Original Git content changed: '+row['path'])
        count += 1
    return {'original_files_verified':count, 'skill_file_counts':manifest['skill_file_counts'],
            'original_reference':manifest['original_reference']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--native',action='store_true',help='Also attempt metadata-only local skills/list; no model turn')
    args = p.parse_args()
    result = {'structure':layout(), 'integrity':originals()}
    print(json.dumps(result,indent=2))
    if args.native:
        from t38.probe_codex_skills import probe
        probe(expected=result['structure']['canonical_entries'])


if __name__ == '__main__':
    main()
