# T-38 · Limited glossary conciliation and Skill preservation

Review baseline: `8bf13207a523e2972482c4ad8b5c5fc25dd1bf02`, branch t-38,
user fork only. This is a documentary intervention, not a repeat technical audit,
whole-library review or implementation of all five future adapters.

## BIB-1: reconciled conclusion

The current user instruction confirms that thematic glossaries ALREADY EXIST.
They are authoritative existing artifacts to preserve. Earlier BIB-1 statements
that common-glossary consolidation/format was pending reflected the supplied
older guide, not a verified absence of actual glossaries. Do not create a
replacement glossary or taxonomy on that basis. The historic reports/matrix
remain snapshots; this report qualifies their glossary-related conclusions.

User-confirmed criteria for this revision (not an inspection of the glossaries):
shoulder uses concept sections and identified individual records (for example
H-001); other glossaries, including maximal isometric force, may use Markdown
tables without record IDs. Preserve BOTH formats in place. Do not impose one
structure, migrate documents, invent IDs or replace existing taxonomy. The initial
vocabulary workflow produces external proposals only, with no glossary, source-note
or alias changes. Preserve individual definitions, provenance, context, location
and discrepancies between sources.

The previously read guide and scientific template remain available unchanged
(fingerprints match t38/bib1/sources.json). Relevant principles remain: per-source
term/definition/context/year/location; no assumed synonymy; preserve manual work,
citekeys, classifications and source limits. Their internal content is not copied
here. Their instructions are evidence, not permission to touch the real library.

The separate REGISTRO_ACTUALIZACIONES_BIBLIOGRAFICAS.md dated 12/11/2026 is not
among the locally available attachments; no callable Drive connector is available.
No remote-library access was attempted. Consequently these exact checks remain:

1. Confirm registry entries documenting the current glossary files, paths, stable
   glossary/entry identifiers WHERE PRESENT and any later exceptions. User-reported
   concept/record and table formats are accepted without claiming direct inspection.
2. Reconcile actual identifier/alias policies, corrections, preserved historical
   definitions and entry-specific exceptions against the older guide/template.
3. Check recorded bibliographic duplicates, alias redirects and publication/dataset
   relationships before suggesting consolidation or counting independent evidence.
4. Verify whether the registry approved any vocabulary automation, review queue,
   source-location notation or work after the supplied guide's last update.
5. Compare a user-supplied anonymized glossary example against the proposed adapter
   interface for both confirmed formats. Actual files, record IDs and table layouts
   have not been inspected here; do not infer them from the test-only BIB-1 JSON.

These gaps do not block a read-only design proposal. They do block claiming
completed registry conciliation or a validated integration with actual glossaries.

## BIB-7: proposed auxiliary use

Keep original glossaries canonical. A future adapter reads only an authorized
snapshot/export and emits a new external suggestions JSON, optionally with a
short Markdown summary. Preserve exact existing glossary/entry IDs where present and every
source-specific definition. For tables without IDs, refer to a read-only snapshot
with a temporary locator; never insert permanent IDs into the original. The test-sidecar format from BIB-1 is not promoted
to a library schema. Details and a synthetic example are in integration.md and
suggestions.example.json; neither is an importer or glossary writer.

Terminological overlap, bibliographic duplicate candidates, bibliographic alias
remissions and shared-dataset publications are different kinds of evidence. One cannot be used
to infer another. Candidate detection never establishes synonymy, record identity,
independent samples or a correction to apply automatically.

## Preservation and adoption

All five original Skill trees are preserved byte-for-byte against the original
baseline, and their scoped dependency Git contents are unchanged. The optional
Windows installer has checkout-only EOL normalization (not a code change). preservation-manifest.json lists the
Git blobs, file modes and SHA-256 values checked against HEAD and local bytes.
The inventory and priorities are in skills-inventory.md. No originals were copied,
installed, rewritten, executed or activated as part of this check.

## Evidence and scope

Only documents, a synthetic JSON example and a preservation manifest are added.
No application code, tests, templates, previous report or Skill definition changed.
The example is parsed as JSON and checked for synthetic IDs, per-source provenance,
separate definitions and no automatic action. The manifest verifies preservation;
it does not certify scientific behavior or platform activation.

No repeat execution of the 53 tests/autotest was needed because executable code
was unchanged. Their previous results remain historical results of 8bf1320, not a
new test run. No library, Drive, Zotero, ChatGPT Skill, main or upstream change;
no global installation, PR or external task update. The user has authorized
commit/push of these documentary deliverables to the fork branch t-38 only; this
does not authorize activation, library writes or development of new functionality.

## Decisions for Manu and next step

- Supply the 12/11 register, and optionally a small anonymized glossary example
  covering concept records and table rows, any existing IDs, an alias and two
  source-specific definitions. No full vault
  or private PDFs are needed.
- Review the proposed external suggestion format and where a PRIVATE review queue
  should live; it must not be the public code repository when populated with real data.
- Confirm actual document references and any existing identifiers for a later
  adapter. Records without IDs stay without IDs; unknown targets remain unresolved.
  Explicit bibliographic alias/relationship exceptions await the unread register.
- Approve a later small synthetic adapter if this proposal fits the actual format.
- Review adoption order before any ingest/synthesis/book workflow is enabled.

T-38 update proposal: BIB-1 corrected to acknowledge existing glossaries, registry
conciliation pending; BIB-7 external suggestion design prepared, actual integration
pending; BIB-4 unchanged. All remain open for review. Five original Skills preserved
and inventoried; this is not installation in Codex or availability in ChatGPT.
