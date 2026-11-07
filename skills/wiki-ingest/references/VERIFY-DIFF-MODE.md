# wiki-ingest: VERIFY mode (verify-diff, non-destructive)

> Re-verifies an EXISTING note against its fulltext. It does NOT regenerate or overwrite.
> Trigger: `/wiki-ingest verify:<PaperNote>` (or argument `--verify <PaperNote>`).

## Guarantee
Read-only on the note. Changes are applied only after explicit user confirmation, always as a surgical Edit (never a full Write), with a read-before-write guard.

## Algorithm
1. Read `papers/<PaperNote>.md` (frontmatter, Useful Quotes, numbers and tables).
2. Recover the fulltext through this chain: reference-manager fulltext (by the key in `source_verification`), then the local PDF library (copy to an ASCII-only path first if the filename has accents), then the internet (PMC, open access, PubMed abstract; if paywalled, note it for later download and do NOT invent).
3. Extract from the fulltext: metadata (title, authors, year, venue, DOI, volume, issue, pages), ALL Useful Quotes, ALL numbers and statistics cited in the note, and the implied `evidence_level`.
4. Compare field by field against the note.
5. Emit a **diff report** (contract below). Do NOT write the note.

## Output contract (per paper)
```
### <PaperNote>  [key <key>]
- metadata: OK | DIFF note=<X> fulltext=<Y>
- quotes: OK N/N verbatim | DIFF quote-k note="..." fulltext="..." | UNVERIFIABLE (no fulltext)
- numbers: OK M/M exact | DIFF <value> note=<X> fulltext=<Y> [table T]
- evidence_level: OK <tag> | DIFF note=<tag> suggested=<tag> (rule)
- verdict: CLEAN | DIFFS(n) | UNVERIFIABLE (paywall, download)
```

## Applying changes (only after confirmation)
For each DIFF, propose the minimal Edit. The user confirms before it is applied. If you run a re-verification campaign, keep a ledger file (one line per note: date, verdict, edits applied).
