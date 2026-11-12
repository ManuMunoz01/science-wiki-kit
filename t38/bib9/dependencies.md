# BIB-9 · Conserved packages and active dependencies

This supplements ../conciliation/skills-inventory.md; it does not duplicate packages.
Integrity preflight checks the existing original manifest (134 Git-content files,
including 21 original Skill-tree files). No original Skill/script/reference,
shared template, kit module, dependency declaration or test was changed.

| Entry | Original conserved package | Active Oficina route | Deferred dependencies / procedures |
|---|---|---|---|
| wiki-lint | 5 files in skills/wiki-lint: SKILL, 2 scripts, 2 references; shared wikikit/lint and fixtures | t38/bib1/audit.py lint; config/schema comparison and synthetic builder | Original repair/promotion/index fixes; semantic rules incompatible with actual metadata |
| vocabulary-update | 2 files: original SKILL and build_vocabulary.py; shared frontmatter/config | t38/bib7/adapter.py with explicit invented A/B fixtures; BIB-1 helpers reused | Original in-place generator; real glossary export reading, merges and scientific relationship validation |
| wiki-ingest | 5 files: SKILL and four references; shared templates/paper/concept/method, tools and schema | Chat planning only; full package linked, not copied | Actual identity/source retrieval, file naming/writes, propagation, taxonomy, seals, index/log updates |
| wiki-synthesize | 5 files: SKILL, two workflow references, validator/writer; shared synthesis/seals/sections and template | Chat planning only | Validator/writer/batch execution, block absorption, thresholds, source reads, seals and note changes |
| wiki-ingest-book | 4 files: SKILL, detailed reference, two chapter helpers; shared book/chapter templates and ingest references | Chat planning only | Book/edition/TOC sources, PDF extraction, stubs, derived identifiers, model-memory fallbacks and propagation |

Original README, CONTRIBUTING, pyproject, licences, docs, tests/examples and optional
installers remain in Git, not duplicated under .agents. Runtime is Python stdlib;
Git is used for blob integrity and Codex only for the optional native metadata
probe. No package installation is needed to run local preflight/synthetic adapters.
Optional PDF extractors, network-backed PMC tools and Zotero/PubMed integrations
are preserved but not required, installed or enabled by BIB-9.

Original Skill conservation is verified against bb639423771a60b430819f11f62c56e29c225324.
Working changes start at 45da7f2. The manifest's original Windows installer EOL
normalization is already documented; Git contents stay unchanged. Metadata and
local wrappers are new instruction adapters, not replacements of original packages.
