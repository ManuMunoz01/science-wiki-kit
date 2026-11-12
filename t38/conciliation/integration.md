# Vocabulary as an auxiliary review tool for existing glossaries

## Smallest technical proposal

Use one ordinary UTF-8 JSON file per run, in a NEW directory outside the glossary.
This reuses the JSON tooling already present; no database, extra YAML fields,
replacement taxonomy, new canonical-glossary format or automatic editor is needed.
A Markdown summary can be generated later for review, but is not another source
of definitions. suggestions.example.json is an invented interface example, not
an approved schema for the real Biblioteca and not executable functionality.

## Confirmed formats to preserve

The user confirms shoulder concept sections with individually identified records
(e.g. H-001) and other glossaries using Markdown tables that may lack IDs. This
confirmation is accepted as current scope; original glossary files were not opened
here. Both formats remain canonical and unchanged. There is no single target
schema, migration, replacement taxonomy or ID-assignment operation.

For identified records, carry the exact existing ID, not the section name or a
normalized/generated substitute. For tables without IDs, leave entry_id null and
use an external locator tied to an authorized read-only snapshot: document
reference, section, row reference and, optionally, snapshot/content fingerprint.
A row number/locator is temporary, not a stable glossary ID; revalidate it if the
source changes. A missing ID is not a documentary error. A document path/reference
can identify a glossary that itself has no glossary_id, without inserting metadata.

A future adapter would accept an explicitly authorized read-only export plus
existing per-source term observations. The exact export/parser waits for a real
anonymized example of each confirmed format: do not infer exact layouts or
pretend they are aliases frontmatter or the current synthetic glossary JSON. No bulk NLP extraction or
new library-wide scan is proposed.

## Minimal suggestion envelope

- `suggestion_id`: local report identifier only; never replaces an existing ID.
- `kind`: term_candidate, terminology_overlap, glossary_inconsistency,
  bibliographic_identity_candidate or dataset_relationship_review.
- `target`: existing `glossary_id` and `entry_id`, copied exactly WHERE PRESENT. For a
  document/table without IDs, use null plus an external document/snapshot locator.
  Distinguish a known no-ID row from an unresolved target; never mint an
  authoritative entry ID or treat missing identifiers as errors.
- `observations`: preserve original term/canonical label, explicit aliases,
  definition and its nature, citekey, year, context, location and existing source
  reference. Use distinct external observation IDs (not new glossary IDs); never overwrite the source definition.
- `reason` and `status`: explain the candidate and leave pending-review.
- `action`: none. Any accepted correction belongs to a later separately authorized
  change, with source checking, concurrency/hash check and old/new review diff.

Optional existing source IDs, DOI or confirmed study/dataset IDs can be carried
unchanged when provided. No new identifiers are inferred from title/year/citekey.
Unknown locations stay unknown; flag missing provenance rather than invent pages.
The adapter must preserve accents and exact glossary IDs; normalization is only
an auxiliary comparison key. Bilingual aliases must be explicit, not translated
or declared equivalent by the detector. Multiple definitions of the same term
remain separate by source, including contradictory or temporally different usages.

## What the current code already does / what it does not

`skills/vocabulary-update/scripts/build_vocabulary.py`: retains note stems and
aliases; finds two-or-more normalized shared terms within one field. Default run
OVERWRITES _VOCABULARY.md and its duplicate report, so do not point it at the real
glossary. Explicit --out/--dupes also overwrite existing target files; the T-38
wrapper's new-directory policy is safer. Original collection is not recursive.

`t38/diagnostics.py`: recursive configured collection and single-term review
candidates; still organized around canonical concept/method notes and is the
historical test contract, not the actual glossary layout.

`t38/bib1/audit.py` vocabulary: preserves three test per-source records, distinct
definitions, source/year/location, and topic grouping; detects normalized overlap
without merging. It checks source-note/citekey/year consistency within the marked
synthetic fixture. It does NOT know existing glossary IDs or the format of real
glossaries, classify bibliographic duplicates, identify shared datasets or apply
corrections. It remains unchanged in this intervention.

## Different review problems: keep them separate

| Observation | What it may mean | Required evidence / prohibited inference |
|---|---|---|
| Same term/alias in two definitions | Terminological overlap, ambiguity or proposed synonym | Read both source contexts; no automatic concept/definition merge |
| Explicit alias redirect to an existing entry | Alternate label for that target under current glossary policy | Preserve target ID and redirect; do not count as a new concept/publication |
| Documented bibliographic alias/remission for one publication | Alternate bibliographic reference to the same publication, not a terminology alias | Preserve original citekeys/remissions and supporting documentation; do not count another publication or automatically delete a record |
| Two records appear to describe one publication | Bibliographic duplicate candidate | Check exact bibliographic identity/version and existing alias notes; citekey/title overlap alone is insufficient |
| Different publications describe the same cohort/dataset | Separate publications with dependent evidence | Preserve each publication/citekey; confirm methods/cohort/registration and annotate dependency, never merge publications |
| Similar metadata without relationship evidence | Unresolved candidate | Do not infer duplicate, alias, shared cohort or independence |
| One source has mismatched year/citekey/location | Documentary inconsistency candidate | Compare the actual source/record; no metadata rewrite or invented page |

Existing aliases can explain repeated citekeys/files, as the BIB-1 diagnostic
already reports for human review. A normalized term match says NOTHING about
bibliographic identity or dataset independence. Counting publications is not
counting independent studies or samples; the original kit's distinct-work
thresholds do not solve shared-dataset dependence.

## Acceptance criteria for a later small adapter

Use invented fixtures for BOTH formats first: identified concept records and
Markdown table rows without IDs, preserved in place. Exact existing IDs unchanged (including punctuation
and accents), null/unresolved targets preserved, two definitions for one term
retained, same term in unrelated contexts not merged, explicit aliases preserved,
missing provenance flagged, and bibliography/cohort cases kept distinct. Verify
input hashes, repeatability, refusal of overwrite and all prior regression tests.
No real input/export or parser was validated here; only the user-confirmed
format distinction is accepted. No new parser is implemented in this revision. Real review
queues and definitions must remain private; only synthetic examples belong in Git.
