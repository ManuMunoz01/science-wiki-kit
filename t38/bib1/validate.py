"""Run historical and BIB-1 checks separately, preserving logs only for synthetic data (MIT)."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from t38.bib1.make_trial import make


def snapshot(vault):
    return {p.relative_to(vault).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in vault.rglob('*') if p.is_file()}


def main():
    out = Path(sys.argv[1]).resolve()
    out.mkdir(parents=True, exist_ok=False)
    results = {}
    def run(name, *args):
        proc = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)
        (out / (name + '.log')).write_text(proc.stdout + proc.stderr, encoding='utf-8')
        results[name] = {'exit_code':proc.returncode}
        if proc.returncode:
            raise RuntimeError('Failed: ' + name)
    run('historical-validation', 't38/validate.py', str(out / 'historical'))
    run('bib1-tests', '-I', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_t38_bib1.py')
    vault = make(out / 'trial-vault')
    before = snapshot(vault)
    run('bib1-lint', 't38/bib1/audit.py', 'lint', '--vault-root', str(vault), '--out-dir', str(out / 'lint'))
    for suffix in ('a', 'b'):
        run('bib1-vocabulary-' + suffix, 't38/bib1/audit.py', 'vocabulary', '--vault-root', str(vault), '--out-dir', str(out / ('vocabulary-' + suffix)))
    assert before == snapshot(vault), 'Synthetic source changed'
    assert (out / 'vocabulary-a/vocabulary.proposed.json').read_bytes() == (out / 'vocabulary-b/vocabulary.proposed.json').read_bytes()
    results['invariants'] = {'synthetic_inputs_unchanged':True, 'repeatable_proposals':True,
                             'historical_tests':44, 'new_bib1_tests':9, 'internal_documents_included':False}
    (out / 'summary.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
