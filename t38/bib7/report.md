# T-38 · BIB-7 implementation report and BIB-4 implications

2026-11-12 (Europe/Madrid). Fork ManuMunoz01/science-wiki-kit, branch t-38.
Starting commit: 594ea89a1ff71a971b6c52c1ffeafb713e402108.
All current additions are local; no commit, push, PR or environment publication.

## Delivered

A read-only, synthetic-only adapter for identified concept records and three-column
Markdown glossary tables. It reuses BIB-1 normalization/YAML, kit I/O/table helpers,
existing snapshot hashes and the conciliation proposal design. It does not replace
or modify previous tools, tests, taxonomy, templates, Skills or the original kit.

Two invented fixtures are included: four concept entries with exact IDs (including
an accented ID), and four table rows without IDs. Definitions, context, citekeys,
declared years, source/location text, explicit aliases and unknown/repeated fields
are retained. Raw spans permit lossless source inspection without editing inputs.
Rows with multiple studies remain undivided; source-to-definition binding stays
pending, not automatically assigned. Existing IDs are unchanged and ID-less rows
remain ID-less, using snapshot-specific external locators.

Review proposals distinguish term overlap, declared bibliographic aliases,
explicit possible duplicate records and explicit possible shared-data relations.
Nothing is merged or corrected. In particular, repeated citekeys, identical terms
or similar words do not establish duplicate records, aliasing or dataset reuse.

## Reproducible evidence

Run: `python t38/bib7/validate.py /tmp/t38-bib7-validation-reviewed`.
Use a NEW directory for future runs. This creates only synthetic evidence outside
Git: combined unittest log, original self-test log, two proposal files, copied
invented inputs and summary.json. CLI counts are not a scientific approval gate.

| Check | Actual result |
|---|---|
| Full unittest suite | 65 passed = 53 retained + 12 new BIB-7 tests |
| Original lint self-test | PASS, 43 expected counters unchanged |
| Fixture parsing | 8 observations; 0 parse diagnostics for supported fixture grammar |
| Proposal kinds | 8 term observations, 5 provenance/binding review items, 3 terminology-overlap pairs, 1 declared bibliography-alias statement, 1 explicit possible duplicate, 1 explicit possible dataset reuse |
| Preservation | All input file hashes unchanged; exact IDs and raw spans retained |
| Repeatability | Two byte-identical proposal files even with reversed input argument order |
| Source separation | Different source definitions remain separate; multi-source row is not split or attributed by guess |
| False-positive guards | Similar-but-different terms, repeated source, comments/fenced examples and escaped pipes do not create spurious identity/data relationships or records |
| Explicit errors/pending cases | Duplicate entry ID, malformed table/header, missing/unverified metadata, conflicting declared years and malformed relation syntax are reported |
| Safety negatives | Existing output, output inside input/repository, unmarked scope, outside/symlinked inputs, duplicate input, symlinked output and zero recognized records refused |
| Output privacy | Directory 0700, proposal 0600 on POSIX; stdout contains counts/types, not source text |

No unexpected test failures in the final run. Negative tests deliberately exercise
refusals; these are passed safeguards, not unexplained failures. Original Skills
remain unchanged. No real glossary, publication, scientific PDF, Drive, Zotero,
update register or ChatGPT Skill was accessed. No installers were run.

## Limits (not validated by passing tests)

- This is a conservative Markdown subset, not a general Markdown/YAML/NLP parser.
  A requires H2 concepts and H3 ID/author headers; field-label synonyms are limited.
  B requires the specified three headers and single physical rows; HTML br tags
  remain literal content, not inferred study/definition boundaries. Arbitrary
  multiline tables, plugin-generated views and alternative relation grammars need
  explicit future fixtures/mappings. Unknown fields/raw text remain preserved;
  unsupported recognized rows/headers are flagged, not silently treated as clean.
- Text outside recognized entries/rows is not semantically extracted. A document
  snapshot SHA and source spans identify what was parsed; no claim of whole-document
  scientific coverage follows from zero diagnostics. A file with no supported
  observations is flagged, and an entirely empty supported scope is refused.
- All extracted information is declared/unverified. Unknown provenance stays
  pending; inferred page numbers, translations, DOI identities or dates are absent.
  Terminology overlap is a lexical candidate only and may be a false positive.
- Multi-source entries/rows are not split into source-specific claims without
  authoritative binding. Distinct definitions and discrepancies remain present;
  the adapter does not verify their fidelity, evolution or scientific truth.
- Bibliographic identity and shared datasets are NOT detected from metadata
  heuristics; only explicit supported source declarations are surfaced for review.
  Confirming them requires authorized sources/registry inspection. No evidence
  weighting, independent-sample count or auto-consolidation is implemented.
- No real export/parser roundtrip has been tested. The update register with later
  exceptions remains unavailable and was not reviewed. The only fixture content
  is invented. The synthetic marker is not proof that arbitrary data is synthetic.
- Read permissions and snapshot checks do not establish a secure future storage
  service. Real definitions/raw spans must remain in a private review location;
  the current CLI rejects output inside this checkout. Real-input mode is not
  enabled or authorized in this intervention.

## Subsequent integration proposal and decisions

1. Review this local implementation and the external proposal contract. No write
   or merge operation should be added to vocabulary generation.
2. Provide small anonymized exports of each real format plus the relevant update
   register exceptions. Verify label variants, ID/glossary references, row layouts,
   explicit aliases, missing-value notation and any relation-statement syntax.
3. Add only the necessary adapter mappings/fixtures; do not migrate original
   glossaries or impose identifiers on tables. Require explicit source binding
   before separating multi-study cells into scientific records.
4. Agree a private destination and authorization for reading specific exports.
   Keep real outputs outside the public checkout; review concurrency/retention
   and access policy before any real data is used.
5. Keep application of accepted corrections a separate human-authorized task,
   with exact target, snapshot recheck and old/new diff. No source/alias mutation
   is part of this adapter.

## T-38 update proposal (not sent)

**BIB-7:** minimal A/B reader and external suggestions implemented/tested on
synthetic data; source and ID preservation, no-overwrite and repeatability verified.
Real parser compatibility, registry exceptions, scientific/source binding and
private-destination approval remain pending.
**BIB-4:** no lint engine changes. Shared documentary concerns (missing provenance,
ambiguous source binding, duplicate glossary IDs and malformed table rows) are
exposed as pending external proposals. These are not scientific-validity findings.
**BIB-1:** existing documentary comparison remains intact; unseen update-register
exceptions are not declared reconciled. T-38 and all subtasks remain open for
Manu's review. No installation or native Skill activation is claimed.
