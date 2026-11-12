# BIB-9 · Project-local Codex Skill preparation

Baseline 45da7f230d6e0407e806df899eb13ed00be37584, user fork, t-38.
This prepares five local entrypoints; it does not install global Skills, modify
Codex user configuration, change ChatGPT Skills or authorize real scientific work.
All current edits are local and uncommitted pending Manu's review.

## Structure and shared dependencies

```text
.agents/skills/
  wiki-lint/SKILL.md                    # existing BIB-1 synthetic diagnostic
  vocabulary-update/SKILL.md            # existing BIB-7 synthetic proposals
  wiki-ingest/SKILL.md                  # PLAN ONLY
  wiki-synthesize/SKILL.md              # PLAN ONLY
  wiki-ingest-book/SKILL.md              # PLAN ONLY
  <each canonical skill>/agents/openai.yaml
  oficina-wiki-lint/SKILL.md             # compatibility alias, delegates
  oficina-vocabulary-update/SKILL.md     # compatibility alias, delegates
skills/<original-name>/                  # complete originals, unchanged
  SKILL.md, references/, scripts/ as originally supplied
t38/bib9/POLICY.md                       # one shared boundary
t38/bib9/entrypoints.json                # mode/dependency index
```

No package/asset is duplicated into .agents. Relative links resolve back to the
original full packages. Shared templates/, docs/, tools/, wikikit/, original
fixtures/tests/examples, pyproject and licences remain versioned in place.
The existing preservation manifest lists all 134 original dependency files;
`python t38/bib9/check.py` verifies their Git content, plus the five wrapper
names, descriptions, mode bindings, links and explicit-invocation metadata.
This is a narrow structural preflight, NOT the native Codex parser or a full
YAML/security audit. Names/descriptions use a simple quoted flat format.

The two oficina-* aliases now delegate, removing parallel/outdated default
recipes. Previous recipes remain in Git history and t38/ historical profiles.
The old native probe is reused with an optional expected-name set; its default
two-alias behavior is retained, and BIB-9 requests the five canonical names.

Dependencies: Python >=3.9 declared in original kit (3.12.14 tested here), stdlib
runtime and Git for integrity checks. Codex is needed only for native discovery.
No pip install, Claude installer, user Skill folder, config.toml edit, credentials,
Zotero, Drive or network is needed for the synthetic Skill procedures.
Source/PDF/network integrations remain optional preserved components, NOT enabled
by local preparation. See ../conciliation/skills-inventory.md for the original
complete per-Skill inventory, write risks and deferred dependencies.

## Installation and activation without global changes

The versioned .agents/skills directories ARE the project-local preparation.
No installer is needed. Keep this checkout complete (do not copy SKILL.md alone),
run the preflight from its root, then open that root in a NEW Codex project/session.
Do not link/copy these packages into home-level skills folders. Do not run
install.sh/install.ps1 or change persistent Codex configuration.

These local additions are not yet in the remote branch. For a later Desktop
check, first transfer only the reviewed project files into the same fork checkout
(or use a later explicitly approved commit). Check existing files/conflicts before
copying; do not overwrite another project's Skills or private data.

Original package preservation is distinct from local discovery, metadata loading,
explicit invocation and actual execution. All five have project entrypoints;
only lint and vocabulary have runnable synthetic procedures. The other three
return chat plans only. Nothing here makes the five Skills available in ChatGPT.

## Reproducible checks in this workspace

```bash
python t38/bib9/check.py
python t38/bib9/smoke.py <NEW_EXTERNAL_DIRECTORY>
python -I -m unittest discover -s tests
python -I skills/wiki-lint/scripts/lint.py --self-test --out-dir <NEW_EXTERNAL_DIRECTORY>
python t38/bib9/check.py --native
```

Use distinct NEW directories, outside inputs and the checkout. The smoke runner
invokes the exact existing BIB-1 lint and BIB-7 vocabulary procedures, checks scope
and input hashes and records exit codes. Its success demonstrates procedural/CLI
invocation only. It does not call another model or prove native `$skill` activation.
It never invokes original ingest/synthesis/book workflows or real data.

The final `--native` check uses the installed Codex app-server initialize +
skills/list protocol with this checkout as cwd and forceReload=true; it submits
NO model turn. Success must return all five names with project-local paths and
no relevant errors; inspect enabled flags and scopes too. In this Cloud runtime
server startup fails before the response because Codex state storage is read-only.
A failed native probe is NOT evidence that .agents entries were recognized.
Do not move credentials/state, change user configuration, disable sandboxing or
bypass the runtime restriction to make it pass.

## Concrete Codex Desktop verification (pending)

1. Put the reviewed files in the fork checkout; verify branch t-38 and run
   `python t38/bib9/check.py` from its root. Record Codex/Desktop/CLI versions.
2. Open that root in Codex Desktop and start a fresh session, so local Skill
   metadata can be rescanned. Use the Skill selector (type `$` where offered).
   Confirm the FIVE canonical names, their local paths and PLAN ONLY labels.
   UI details vary by version; do not infer discovery from files merely existing.
3. On Linux/macOS/WSL with a compatible Codex CLI installed, run
   `python t38/bib9/check.py --native`. The reused stdio probe uses POSIX-style
   selectors and is not asserted compatible with native Windows pipe handles;
   on native Windows use the Desktop selector/invocation checks below (or a
   separately available WSL runtime), not an assumed successful Python probe.
   That checks the CLI process, not necessarily Desktop's separate runtime: verify
   the Desktop selector as well. A missing/disabled/error entry is unresolved.
4. Explicitly request in Desktop (synthetic input only):
   `$wiki-lint Follow the local synthetic-only procedure and report scope and findings.`
   Then `$vocabulary-update Follow the local invented A/B glossary proposal procedure.`
   Check the tool trace uses t38/bib1/audit.py and t38/bib7/adapter.py, NEW external
   output directories, no repair or network operations, and unchanged input hashes.
   A model response claiming success is not execution evidence: inspect output files.
5. For the other three, request a CHAT PLAN ONLY using invented inputs. Confirm
   no original scripts, source reads, scientific writes or propagation occur.
6. Record discovery, UI availability, explicit invocation and executed behavior
   separately. Stop on a policy conflict; do not enable writes or global settings.

## Codex evidence consulted

The installed binary is codex-cli 0.167.0-alpha.4. Its generated SkillsListParams
schema confirms cwds/forceReload. Official documentation URL
https://developers.openai.com/codex/skills/ returned HTTP 403 here; it was not read.
The official openai/codex docs/skills.md was retrieved and points to that URL.
Accessible official current-main source confirms project .agents/skills roots,
SKILL.md frontmatter, agents/openai.yaml and allow_implicit_invocation metadata:

- https://raw.githubusercontent.com/openai/codex/main/codex-rs/ext/skills/src/host_roots.rs
- https://raw.githubusercontent.com/openai/codex/main/codex-rs/skills/src/parser.rs
- https://raw.githubusercontent.com/openai/codex/main/codex-rs/skills/src/metadata.rs
- https://raw.githubusercontent.com/openai/codex/main/codex-rs/ext/skills/src/loader/mod.rs

Current-main source is reference evidence, NOT proof that the installed alpha or
Desktop implements every field identically. The local metadata requests
allow_implicit_invocation=false; actual enforcement remains host-specific and
unverified. Wrapper/shared-policy restrictions apply even if that field is ignored.
They are instruction boundaries, not technical revocation of filesystem access.

## Functions that stay off

Scientific source access; real-library input mode; any create/edit/rename/delete,
merge or propagation of scientific records; changes to aliases/classifications;
original fix/promotion/index/ingest/batch/synthesis/seal/stub workflows; chapter
identifier derivation and model-memory source fallbacks; private-data uploads;
global installation, user configuration, Git publication and external sync.
See POLICY.md for the complete common boundary and report.md for actual outcomes.
