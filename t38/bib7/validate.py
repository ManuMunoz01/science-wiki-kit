"""Reproduce BIB-7 synthetic evidence and prior regressions in a NEW directory (MIT)."""
import json
from pathlib import Path
import shutil
import subprocess
import sys

KIT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KIT))
from t38.bib1.validate import snapshot
from t38.bib7.adapter import export


def main():
    out = Path(sys.argv[1]).resolve()
    if out == KIT or KIT in out.parents:
        raise ValueError('Evidence directory must be outside the development checkout')
    out.mkdir(parents=True, mode=0o700, exist_ok=False)
    results = {}
    def run(name, *args):
        proc = subprocess.run([sys.executable, *args], cwd=KIT, text=True, capture_output=True)
        (out / (name + '.log')).write_text(proc.stdout + proc.stderr, encoding='utf-8')
        results[name] = {'exit_code':proc.returncode}
        if proc.returncode:
            raise RuntimeError('Validation failed: ' + name)
    run('unittest-all', '-I', '-m', 'unittest', 'discover', '-s', 'tests')
    run('original-selftest', '-I', 'skills/wiki-lint/scripts/lint.py', '--self-test', '--out-dir', str(out/'original-selftest'))
    root = out/'synthetic-inputs'
    shutil.copytree(Path(__file__).with_name('fixtures'), root)
    inputs = [('a',root/'shoulder.synthetic.md'), ('b',root/'force.synthetic.md')]
    before = snapshot(root)
    first = export(root,inputs,out/'proposal-a')
    export(root,list(reversed(inputs)),out/'proposal-b')
    if before != snapshot(root):
        raise RuntimeError('Input bytes changed')
    if (out/'proposal-a/suggestions.proposed.json').read_bytes() != (out/'proposal-b/suggestions.proposed.json').read_bytes():
        raise RuntimeError('Proposals are not repeatable')
    results['invariants'] = {'inputs_unchanged':True, 'repeatable_proposals':True, 'real_sources_accessed':False}
    results['adapter_summary'] = first['summary']
    (out/'summary.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(results,indent=2,ensure_ascii=False))


if __name__ == '__main__':
    main()
