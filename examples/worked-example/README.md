# Worked example

What a wiki looks like after **one paper** has been ingested with `wiki-ingest`, so you can see the result
before you start. It lints clean (`python skills/wiki-lint/scripts/lint.py --vault-root examples/worked-example`
reports no findings), and a test in the kit keeps it that way.

The paper is open access: Sharma et al. 2022, PeerJ, DOI `10.7717/peerj.13842` (PMCID PMC9527019), a randomized
trial of eccentric versus concentric isokinetic hamstring training.

| Note | What to look at |
|---|---|
| `wiki/papers/Sharma_2022_Hamstring_Isokinetic_Training.md` | Frontmatter with `evidence_level`, `volume`/`pages`, a `source_verification` line with **two seals** (one per note that cites the paper), the results table, a `## Limitations` section that separates the wiki's reading from the authors' own, and quotes copied verbatim |
| `wiki/concepts/Functional_Hamstring_Quadriceps_Ratio.md` | A concept note: every finding cites the paper with a wikilink; `status: draft` because it rests on a single source |
| `wiki/concepts/Training_Mode_Specificity.md` | Same pattern; the *Controversies or Gaps* callout says why the disagreement the authors mention cannot be sourced yet |
| `wiki/methods/Isokinetic_Dynamometry.md` | A method note: the paper is listed under *Papers Using This Method* |
| `wiki/log.md` | The ingest log entry |

How it was made: tables and body text came from `tools/pmc_tables.py PMC9527019 --body` (publisher XML, cell by
cell); every figure and quote was checked against that text before it reached a concept note; the seals were
written with `tools/seal.py` (`docs/SEALS.md`).

Notes on what you will *not* find here: no `status: final` notes (that needs at least two independent sources, see
`docs/WIKI_SCHEMA.md`), no State of Knowledge block (that needs three), and no sub-MOCs or Coverage-by-Field table
(they appear as the wiki grows; the linter ignores them until you add them).

The data in the notes come from the paper above and are reproduced only as brief factual summaries with
attribution; read the paper for the full context.
