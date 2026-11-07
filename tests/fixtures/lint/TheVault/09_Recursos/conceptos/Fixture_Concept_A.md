---
tags: [concept, fixture]
date: 2024-01-15
status: final
project: fixture
type: concepto
field: "research-methods"
subfield: "fixture-sub"
aliases: [FCA]
related_concepts: [Fixture_Hub_RC]
---

# Fixture Concept A

## Definition

Concept A exists in the fixture wiki to test backlink resolution from [[Smith_2024_FakePaper]].

## Key Findings

- Backlinked from [[Smith_2024_FakePaper]] - not orphan.
- Backlinks for the abstract-seal and short-seal fixtures: [[Fixture_AbstractSeal]], [[Fixture_ShortSeal]] - keeps the concepts_touched edge symmetric.
- Backlinks for the four C-B exemption fixtures: [[Fixture_Check18ExemptOk]], [[Fixture_Check18ExemptStale]], [[Fixture_Check18ExemptBad]], [[Fixture_Check18OnlineFirst]] - same reason, they declare concepts_touched.
- Related synthesis hub: [[Fixture_Hub_Inline]].
- [[Smith_2024_FakePaper]] - [pendiente claim]
- [pendiente claim]

## State of Knowledge

> [!abstract] Synthesis · updated 2024-06-01
> - ✅ **Fixture entry — resolved.** Sourced finding from [[Smith_2024_FakePaper]] (1 src: SR-MA; High).
> - ✅ **Check 22 fixture — marker ownership.** Suffix marker on a SEALED paper must be flagged as stale: [[Fixture_GoodProvenance]]⚠ ; prefix marker on an UNSEALED paper must NOT be flagged: ⚠[[Fixture_NoProvenance]] ; and a bare prose caution ⚠ owned by no link must be ignored (2 src: fixture; High).
> - ✅ **Check 22 fixture — chained prefix, the blind spot.** A marker glued to the FOLLOWING link but preceded by another link belongs to the following one, so this must be flagged against the sealed paper: [[Fixture_NoProvenance]] ⚠[[Fixture_GoodProvenance]] . Adjudicating it to the preceding link instead hides it — that is exactly how a stale marker stayed invisible until the 2026-07-30 sweep (2 src: fixture; High).
> - ✅ **Check 22 fixture — glued on both sides is ambiguous.** With no whitespace on either side the author's intent is unrecoverable; the preceding link keeps it by convention, so this counts against the sealed paper and NOT against the unsealed one: [[Fixture_GoodProvenance]]⚠[[Fixture_NoProvenance]] (2 src: fixture; High).

## Reliability

Test-retest reliability was excellent, ICC = 0.91 (95% CI 0.84-0.95) on 2026-07-30.


- [[Smith_2024_FakePaper]] anchors the pooled estimate on the next line.
- Pooled effect size d = 1.24, inside the citation radius.

## Fixture Tables

| Column A | Column B |
|---|---|
| well formed | second cell |
| escaped pipe a \| b | second cell |
| short row |

| Header | With | Three |
|---|---|
| two | cells |
| more | cells |

```
| In Fence | Header |
|---|---|
| lonely |
```

#### Mojibake fixture RÂ²

## Check 22 exemption fixture

- **Caveat in prose.** The glyph is glued to a SEALED paper, but what comes after it is the note author's own caution about the source, written on purpose; sealing the paper does not expire it, so it must NOT be counted: [[Fixture_GoodProvenance]] ⚠ low-tier journal, no effect sizes.
- **Confidence glyph of the debates layer.** Here the glyph is notation of the confidence block, not a pre-fulltext marker, so it must NOT be counted either: [[Fixture_GoodProvenance]] ⚠ (2 src: fixture; Moderate).
- **Dated correction annotation, italic + parenthesis** (added 2026-09-16; the entire live Check 22 list was this shape). The glyph opens an annotation ABOUT the verification of a sealed paper, i.e. the opposite of "unverified source"; the caveat test missed it only because the markdown emphasis marker precedes the letter. Must NOT be counted: [[Fixture_GoodProvenance]] ⚠ *(corrected 2026-09-06: this read "validated quantitatively", which the source does not claim)*.
- **Dated correction annotation, italic without parenthesis.** Same class, different punctuation — the first pattern written for this triage used `*(` and silently missed this one, so the fixture pins both shapes: [[Fixture_GoodProvenance]] ⚠ *corrected 2026-09-05, third copy of this claim*.

## Check 5 empty-target fixture

- Empty wikilink target, the exact shape Extract-Wikilinks cannot express (its `+` requires at least one character): [[]]
- GUARD alias-only: a target that is empty but carries an alias must count too: [[|just an alias]]

GUARD code span: a `[[]]` between backticks is quoted text, not a link, and must NOT count.

GUARD fence: the same two shapes inside a fence are not links and must NOT count.

```
- [[]] and [[|alias]] inside a fence
```
