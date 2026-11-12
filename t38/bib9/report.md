# T-38 · BIB-9 preparation results

2026-11-12, Europe/Madrid. User fork ManuMunoz01/science-wiki-kit, branch t-38.
Baseline 45da7f230d6e0407e806df899eb13ed00be37584.
All new work remains local, with no commit, push, PR or environment publication.

## Separate verification outcomes

| Item | Result and practical limit |
|---|---|
| Five original Skill packages | Conserved intact in skills/; 21 original Skill files and 134 original dependency Git contents verified against the existing manifest |
| Project-local structure | Five canonical .agents/skills entrypoints, correct names/descriptions, original-package links, shared policy and local metadata; narrow structural preflight passes |
| Native Codex recognition | BLOCKED/UNVERIFIED: installed CLI 0.167.0-alpha.4 app-server cannot open its state_5.sqlite in read-only Codex home; fresh metadata probe closed before initialize response |
| wiki-lint invocation | Existing BIB-1 CLI procedure executed, exit 0, 6 synthetic notes; documentary findings retained, no repairs or scientific approval |
| vocabulary-update invocation | Existing BIB-7 CLI procedure executed, exit 0, 6 invented A/B observations; external proposals only, identities/definitions retained and relationship statements unverified |
| Other three Skills | PLAN-ONLY entrypoints prepared; original packages retained but their scientific workflows were not invoked through these wrappers |
| No unauthorized input changes | Synthetic vault/glossary hashes unchanged; original components unchanged; output only in new external directories |
| Regression tests | 76 passed = previous 70 + 6 BIB-9 tests; original self-test PASS with 43 expected counters |
| Global/persistent installation | None; original installers not executed; no user/home Skill folders, config.toml, credentials or ChatGPT Skills modified |

Invocation evidence is procedural/CLI, NOT native model-triggered Skill activation.
No model/subagent turn was launched for discovery. The native probe submits only
initialize and skills/list, using the current checkout and forceReload. It remains
a separate failed capability check, not folded into passing structural tests.

The six new tests cover preserved originals/five modes, broken dependencies or
missing policy, rejection of executable binding on planning-only entries, legacy
alias delegation/explicit-only metadata, real synthetic adapter calls and refusal
of overwrite/checkout output, and native startup failure propagation. The tests
use invented temporary data; legacy unit tests may exercise their own temporary
fixture operations, not real-library workflows.

## What changed

Five short canonical wrappers and their agents/openai.yaml metadata request
explicit-only use. The two previous oficina-* entrypoints now delegate to these
canonical wrappers rather than retaining parallel/outdated default procedures.
Original scripts/references/assets are linked in place, not copied or forked.
One common POLICY.md defines the synthetic-only / planning-only boundary.

The original native probe is reused with an optional expected-name parameter;
default behavior still checks its two legacy aliases. New preflight/smoke helpers
provide reproducible local checks and invoke existing Oficina adapters, not new
lint/vocabulary implementations. entrypoints.json and dependencies.md record
bindings, complete preserved packages and deferred capabilities.

Local instruction restrictions are not OS access controls. The optional explicit-
invocation metadata was confirmed in accessible current-main official Codex source,
but actual support in the installed alpha/Desktop remains unverified. No claim is
made that these packages are natively installed, available in ChatGPT or safe to
run unadapted against private documents simply because files are present.

## Evidence and documentation availability

- python t38/bib9/check.py: passes structural + 134-file integrity preflight.
- python t38/bib9/smoke.py /tmp/t38-bib9-smoke: passes both existing procedures;
  logs, external outputs and input invariants are retained there.
- python -I -m unittest discover -s tests: 76 passed; log
  /tmp/t38-bib9-unittest.log.
- Original lint self-test: PASS; log /tmp/t38-bib9-selftest.log.
- python t38/bib9/check.py --native: exit 1, log
  /tmp/t38-bib9-native-probe.log; no native response before server exit.
- Direct server startup showed read-only SQLite state initialization failure;
  the subsequent RPC probe only confirms premature process exit. No workaround,
  credential/state relocation, user-config edit or sandbox bypass was attempted.

Official skills documentation URL returned 403, so its content is not claimed
read. Accessible official GitHub docs point to it. Current-main official source
for project roots/frontmatter/local metadata was consulted (links in README).
Those source versions are reference evidence, not proof of the installed binary's
behavior. The installed protocol schema verifies the request fields; Desktop's
actual catalog and native invocation remain to test separately.

## Disabled functions and remaining adoption steps

Keep scientific source access, all real-library inputs, repairs/promotion,
create/rename/write/delete/merge, concept propagation, index/log/seal changes,
batch synthesis, chapter stubs/derived identifiers, source-memory fallbacks,
private-data export, external sync, global installers and Git publication off
within these Skill procedures. Three planning-only wrappers must never fall
through to the originals' write workflows.

After review, transfer/commit only approved project files and verify discovery
in a fresh Codex Desktop session using the concrete procedure in README. Check
all five names/paths/scopes/enabled flags, then explicitly invoke the two synthetic
procedures and inspect actual tool/output traces. Test the other three only for
chat plans. Do not equate CLI metadata discovery with Desktop UI availability. The reused
stdio probe uses POSIX-style selectors; native Windows pipe compatibility is not
asserted. Desktop UI verification is required there, or use a separately available
WSL runtime for CLI metadata checks, without changing the Windows user configuration.

Future real-data read mode, ingestion/synthesis/book adaptations, private storage,
source access and any writes require separate scoped authorization and tests.
Later bibliographic-register exceptions remain unreviewed. No real Biblioteca,
Drive, Zotero, private scientific source or ChatGPT Skill was accessed here.

T-38/BIB-9 update proposal: original packages conserved, local structure and
synthetic procedures prepared/tested; native Cloud discovery blocked, Desktop
activation and actual host compatibility pending. No task/subtask is declared
approved or closed. This is a reviewable preparation, not deployment or installation.
