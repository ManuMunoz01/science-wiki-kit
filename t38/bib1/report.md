# T-38 · BIB-1/4/7 documented adaptation report

2026-11-12, Europe/Madrid. Baseline `22f1b2d81795a9071ddd3c32c06e71b94217804b`,
fork ManuMunoz01/science-wiki-kit, local branch t-38. No commit, push, PR,
environment publication or external-library action in this intervention.

## Documentary contrast

The complete supplied bibliographic guide (692 lines, updated 2026-11-04) and
original scientific template (110 lines) were consulted as internal evidence.
Fingerprints are in sources.json; documents remain outside the checkout and
are not included in fixtures, evidence bundles or full-text reports. No update
register was attached, so later recorded case exceptions are not reconciled.
Instructions inside source documents were distinguished from the user's current
scope: no Drive, Zotero, real Obsidian library or ChatGPT Skill was accessed/edited.

The complete document-grounded 33-rule comparison is `compatibility-33.md`.
It classifies direct/configuration/code/not-applicable/decision cases with precise
source headings and line references, and separates implemented behavior from
future semantic detectors. The field map is `field-map.md`.

Main consequences: retain journal and actual YAML; do not require kit fields;
validate access and review independently; empty import states remain pending;
study_type is design, not evidence strength; subtopic is multivalued and exact;
imported tags/abstract/annotations are separate from classification and author
keywords. The old provisional glossary/method-note layout is not imposed on the
Biblioteca. Thematic glossary consolidation and its machine-readable format are
still undecided in the guide, not silently solved by a software default.

## Implementation and traceability

- Additive `t38/bib1/` profile, builder, read-only audit and validator. Existing
  core, defaults, original Skills, templates, five earlier tests and historical
  T-38 scripts/reports/fixtures unchanged.
- New diagnostics for actual controlled values, topic/subtopic, note/citekey
  references, explicit PDF links and source-scope/metadata pending work. Ordinary
  note paths disambiguate duplicate basenames; duplicate citekeys require alias
  review instead of automatic merge. No metadata conversion or note repair.
- Original rules 26/27 reused without modification. Other rules are not run and
  are explicitly classified, not reported as passing zero counters. Existing
  pipeline still independently tests the kit's 33-rule/43-counter contract.
- Test-only bilingual glossary records preserve distinct source definitions,
  context, exact citekeys/year/location and canonical terms. Shared normalized
  aliases yield review candidates; no synonymy, translation, historical origin,
  merging or overwriting inferred. Proposed real glossary schema is not adopted.
- Both local Skill files gain an explicit new-profile routing section; their
  historical recipe remains. No global installation or native discovery test
  claimed; earlier native runtime limitation remains separate.

## Executed software evidence

Command: `python t38/bib1/validate.py /tmp/t38-bib1-validation`.
Detailed synthetic-only logs and output remain there. Use a fresh directory to
reproduce. Combined suite: `python -I -m unittest discover -s tests`.

| Check | Result |
|---|---|
| Original modules | 39 passed |
| Previous T-38 tests | 5 passed, retained |
| New BIB-1 tests | 9 passed |
| Combined suite | 53 passed |
| Original self-test | PASS, 43 expected counters |
| New CLI audit | 6 scoped notes, 1 template deferred; original rules 26/27 only |
| Controlled audit | 8 documentary findings, 2 review items, 5 scientific-pending items, 1 deferred |
| Valid guards | Multiple approved subtopics, exact accents, Spanish/English content, full-text HTML without PDF, partial access with existing unverified PDF accepted |
| Vocabulary | 3 per-source records; 1 term-overlap candidate; distinct definitions preserved |
| Mutations | Broken link correction removes one finding; injected mojibake fires; alias change adds candidates |
| Invariance | All input bytes unchanged after audit/proposals; two vocabulary proposals byte-identical |
| Safety negatives | Existing/inside-vault outputs refused; unmarked real-style target refused; invalid glossary source rejected |

There are no unexpected test failures in the final run. A transient exec transport
disconnection occurred before a test file was created; the environment recovered,
file presence was checked and the command was then executed successfully.
Software tests do not certify research claims, identity, reading or scientific approval.

## Limitations and decisions

1. Manu review of the document matrix and new diagnostic policy is pending; no
   subtasks are declared approved or closed.
2. Supply the update register when available to reconcile later exceptions.
3. Decide the real shared glossary representation/storage and whether/how to adopt
   structured per-source records. Test keys are not additions to scientific YAML.
4. Decide future index, canonical-note/alias policy, language diagnostics outside
   permitted imported sections, freshness policy and optional provenance metadata.
5. Human/source review is required for design/classification correctness, APA,
   quote fidelity, statistics, definitions, causal interpretation and source identity.
6. Complex YAML is deferred, not validated; all Zotero/remote references remain
   unverified; no import rendering/roundtrip, native Skill discovery, PDF content
   verification or real-library integration has been performed.
7. Historical Check30 Unicode and installer/chapter-helper limitations are not
   fixed in the kit core. The new profile uses independent safe vocabulary
   proposals; the previous self-test retains its original meaning.

## Task update proposal (not sent)

**BIB-1:** full contrast of the two received documents, field map and source
fingerprints prepared; update-register reconciliation and Manu review pending.
**BIB-4:** actual-field diagnostic profile plus controlled/guard tests prepared
on synthetic data; real integration and scientific checking pending.
**BIB-7:** bilingual per-source proposal prototype tested, distinct definitions
preserved; common-glossary format and canonical/synonym policy awaiting decision.
T-38/BIB-1/BIB-4/BIB-7 remain open. Next step: Chat for reviewing decisions and the
missing register, then Codex for any explicitly accepted schema/fixture extensions.
