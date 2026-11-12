# Five original Skills: preservation inventory and adoption order

The five original Skill trees are already versioned under `skills/` in the user
fork. No duplication, installation or rewrite is necessary to preserve them.
Reference: original commit bb639423771a60b430819f11f62c56e29c225324, compared with
8bf13207a523e2972482c4ad8b5c5fc25dd1bf02 and local bytes. See
preservation-manifest.json for exact path lists, counts, blob IDs and hashes.
This is integrity inspection, not a repeat functional/scientific audit.

## Per-Skill inventory

| Skill / original function | Versioned components already present | Useful function for Oficina | Required adaptation / limitation | Priority |
|---|---|---|---|---|
| wiki-lint: 33 numbered health rules, regression fixture and separate repair tools | skills/wiki-lint/SKILL.md; scripts/lint.py, fix.py; references/cli-reference.md, check-origins.md; wikikit/lint/ and original tests/fixtures/lint/ | Diagnose document structure, links, encoding and actual metadata | Continue through t38/bib1 profile; most original semantic contracts are not Oficina fields. Keep repairs/promotion disabled. User confirms identified concept records and tables without IDs; actual target references/alias exceptions remain uninspected. | 1: existing diagnostic-only profile |
| vocabulary-update: generated canonical/alias table and duplicate candidates | SKILL.md; scripts/build_vocabulary.py; shared wikikit parser/config; T-38 wrappers and synthetic tests | External candidate/consistency proposals preserving per-source definitions and existing glossary IDs | Original default overwrites generated files, only reads direct concept/method notes and requires 2 shared normalized terms within a field. Preserve both identified concept sections and tables without IDs; do not migrate. Existing adapters do not parse actual glossary formats/IDs or distinguish duplicate publications/cohorts. Approve read-only interface first. | 1: bounded glossary proposal next |
| wiki-ingest: create/update paper, source-fidelity checks, propagate findings | SKILL.md; references/INGEST-WORKFLOW.md, INGEST-PITFALLS.md, CONCEPT-PROPAGATION.md, VERIFY-DIFF-MODE.md; templates/paper.md, concept.md, method.md; tools/seal.py, pmc_tables.py | Source identity, extraction provenance, verify/diff approach and human-readable proposals | Preserve actual citekeys/template/journal/states; prohibit automatic taxonomy expansion, renaming, status promotion and concept propagation. Prefer later read-only verify pilot; never treat source-note assertions as source verification. | 2: verify/propose before writes |
| wiki-synthesize: draft/ratify State of Knowledge with validation and source seals | SKILL.md; references/SYNTHESIS-WORKFLOW.md, BATCH-WORKFLOW.md; scripts/synth_validate.py, synth_write.py; templates/synthesis.md; wikikit/synthesis.py, seals.py, sections.py; tools/seal.py | Source-traceable comparison of evidence, definitions, disagreements and limits, human ratification | Original final/min_sources/SR thresholds, headings, seals and block writer are not Oficina conventions. Preserve existing thematic/glossary IDs and definitions; count publications separately from independent datasets. Do not run writer/batch modes unchanged. | 3: after glossary/ingest interfaces |
| wiki-ingest-book: overview then selected chapter ingestion | SKILL.md; references/BOOK-INGEST-WORKFLOW.md; scripts/report_missing_concepts.py, create_forward_ref_stubs.py; templates/book.md, chapter.md; shared ingestion references | Controlled edition/chapter identity, page-offset calibration, source-specific concepts | Actual book/chapter schema and IDs need agreement. Do not adopt model-knowledge fallbacks as scientific content; do not derive DOI or citekeys from parent suffixes. Prior chapter-helper incident remains unresolved; no generated stubs/metadata until verified. | 4: defer until a concrete book pilot |

## Shared preserved dependencies

The manifest covers the original versioned content in skills/, templates/, docs/,
wikikit/, tools/, tests/, examples/ and CI, plus pyproject, README, CONTRIBUTING,
licences and optional installers. It includes ALL original files in these groups,
not just the leaf scripts named above. New T-38 tests are additional, not evidence
that original tests were deleted/replaced. All preserved original Git content is
unchanged. Optional install.ps1 has checkout EOL normalization only; Skill tree
bytes themselves match the original exactly.

- Python >=3.9 declared, standard library runtime (pyproject dependencies empty);
  prior execution was Python 3.12.14, not a new cross-version test here.
- Shared config/frontmatter/textio/vault modules, lint defaults, schema, seals,
  GOTCHAS, nine note templates and original regression tests remain in Git.
- PDF workflows require accessible sources plus an extractor such as pdftotext;
  visual inspection is still needed for tables. docling is an optional external
  alternative, not an installed or required dependency of the stdlib code.
- pmc_tables.py requires network access to its source services; Zotero/PubMed
  adapters need separately verified access. None was used in this intervention.
- Optional installers can create global links and writes; do not run them here.
  Previously identified Python 3.9 installer risk was not fixed or rerun.
- MIT code / CC BY 4.0 original documentation attribution is retained. Internal
  Oficina sources are private evidence, not bundled as original kit documentation.

## Prioritized function/script adoption table

| Order | Component | Next bounded use | Keep off until explicitly adapted/approved |
|---|---|---|---|
| 1 | t38/bib1/audit.py lint; original lint check26/check27 | Existing synthetic documentary diagnosis | Original fix.py, status promotion, broad real-library scans |
| 1 | vocabulary generator + BIB-1 proposal logic | External suggestions against anonymized existing glossary IDs | Default in-place vocabulary writes, automatic merging or new taxonomy |
| 2 | wiki-ingest VERIFY-DIFF-MODE / source-fidelity references | One invented/anonymized source-note diff workflow | Creating/renaming papers, taxonomy expansion, mass propagation |
| 2 | tools/pmc_tables.py | Later authorized source-specific extraction, preserve exact attribution | Network reads not requested now; source content in public evidence |
| 3 | synth_validate.py concepts and synthesis workflow | Compare source-specific findings in a draft proposal | synth_write.py, seal.py writes, kit synthesis thresholds/batch auto-writes |
| 4 | book page calibration / report_missing_concepts.py concepts | One agreed book/chapter test, diagnostic proposals | create_forward_ref_stubs.py, derived identifiers, model-knowledge content |

## Preservation is not activation

| Platform | What is verified / present | What remains unverified |
|---|---|---|
| GitHub user fork | Five original Skills and dependencies already tracked, unchanged; versioning this conservation report does not activate them | Nothing must be duplicated for preservation; no installation implied |
| Codex Cloud | Previous CLI tests and two local instruction adapters for lint/vocabulary exist; five original Skill Markdown procedures can be read | Native discovery/activation of all five not tested; previous native probe failed on read-only state. Actual ingest/synthesis/book adaptation and permissions still needed |
| ChatGPT | No ChatGPT Skills installed/modified by this work | Packaging, available tools, private-source access, compatible execution and actual activation must be checked separately in that host |

Do not enable unadapted original workflows just because their Markdown and Python
files are present. Their write, status, naming and fallback rules require review.
