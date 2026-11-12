"""Read-only local Codex skills/list probe; no model turn, credentials or global installation."""
import json
from pathlib import Path
import selectors
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]

def probe(expected=None):
    expected = set(expected or ["oficina-wiki-lint", "oficina-vocabulary-update"])
    with subprocess.Popen(['codex', 'app-server', '--listen', 'stdio://'], cwd=ROOT,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                          text=True, bufsize=1) as proc:
        sel = selectors.DefaultSelector()
        sel.register(proc.stdout, selectors.EVENT_READ)
        def send(data):
            proc.stdin.write(json.dumps(data) + '\n')
            proc.stdin.flush()
        def receive(request_id):
            deadline = time.monotonic() + 20
            while time.monotonic() < deadline:
                if not sel.select(timeout=1):
                    continue
                line = proc.stdout.readline()
                if not line:
                    raise RuntimeError('Codex app-server closed before response')
                obj = json.loads(line)
                if obj.get('id') == request_id:
                    return obj
            raise TimeoutError('Codex skill probe timed out')
        try:
            send({'id':1,'method':'initialize','params':{'clientInfo':{'name':'t38-skill-probe','version':'1'}}})
            receive(1)
            send({'method':'initialized','params':{}})
            send({'id':2,'method':'skills/list','params':{'cwds':[str(ROOT)],'forceReload':True}})
            result = receive(2)
            # Emit only metadata for this repository's skills, never global configuration.
            entries = result.get('result', {}).get('data', [])
            found = []
            errors = []
            for entry in entries:
                for skill in entry.get('skills', []):
                    if skill.get('name', '') in expected:
                        found.append({k:skill.get(k) for k in ['name','path','enabled','scope']})
                errors.extend(str(e.get('path', 'unknown')) for e in entry.get('errors', []))
            print(json.dumps({'local_skills':found,'error_paths':errors,'rpc_error':result.get('error')},indent=2))
            if {s['name'] for s in found} != expected:
                raise RuntimeError('Expected local skills missing from native discovery')
        finally:
            sel.close()
            proc.terminate()
            proc.wait(timeout=5)

if __name__ == '__main__':
    probe()
