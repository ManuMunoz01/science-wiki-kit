# science-wiki-kit

Skills, scripts and templates to build and maintain a **scientific knowledge wiki** (plain markdown,
Obsidian-compatible) with an AI coding agent, for any research field.

You read papers and books; the agent turns each one into a traceable note and propagates its findings into
concept and method notes. Every claim links back to a source note, which links to a DOI and a PDF. A linter keeps
the whole thing honest, and a synthesis step summarises what the evidence on a topic currently says, with a human
approving every line.

It grew out of a wiki of a few thousand notes on sport science. The machinery is domain-agnostic: folders, fields,
vocabularies and language are configuration, and sport science is only one worked example (`examples/`).

## What is in the box

| Piece | What it does |
|---|---|
| `skills/wiki-ingest` | Ingest a paper: note, concept and method propagation, index, log, source-fidelity checks, verify mode |
| `skills/wiki-ingest-book` | Ingest a book overview, then chapter by chapter |
| `skills/wiki-synthesize` | Draft or update a `## State of Knowledge` block, validated and checked against the PDFs, never autonomous |
| `skills/wiki-lint` | 33 health checks plus fix tools (`lint.py`, `fix.py`), with a regression self-test |
| `skills/vocabulary-update` | Regenerate the synonym vocabulary from note aliases |
| `tools/` | `seal.py` (record that a claim was checked against a PDF), `pmc_tables.py` (read tables from PMC XML) |
| `templates/` | paper, concept, method, book, chapter, sub-MOC and synthesis note templates |
| `docs/WIKI_SCHEMA.md` | The contract: note types, frontmatter, evidence levels, fidelity rules, synthesis format |
| `docs/GOTCHAS.md` | Operating lessons: the ways a wiki quietly goes wrong, and what to do about each |
| `wikikit/` | The shared Python package (standard library only) |

Works on Windows, macOS and Linux. Python 3.9 or newer, no third-party dependencies.

## Install in five steps

1. **Get the kit**: `git clone https://github.com/MinorBaek/science-wiki-kit` and `cd science-wiki-kit`.
2. **Run the installer**: `./install.sh ~/my-wiki` (macOS, Linux) or `.\install.ps1 C:\Wikis\mine` (Windows).
   It links the five skills into `~/.claude/skills` (override with `CLAUDE_SKILLS_DIR`), and scaffolds the wiki folder
   with `wiki.config.json`, `wiki/WIKI_SCHEMA.md`, `templates/` and the empty note folders. It never overwrites
   anything that already exists.
3. **Describe your field**: in `wiki/WIKI_SCHEMA.md`, fill the *Taxonomy* section (fields and subfield slugs), and
   list the same field slugs in `field_titlecase_map` in `wiki.config.json`. Adjust `evidence_level_vocab` if your
   discipline needs other study designs. `examples/sport-science/` shows a complete taxonomy.
4. **Check the setup**: from the wiki folder, run `python <kit>/skills/wiki-lint/scripts/lint.py`. On a fresh wiki
   every counter is 0. To test the kit itself: `python skills/wiki-lint/scripts/lint.py --self-test`.
5. **Ingest a first paper**: open your agent in the wiki folder and say `/wiki-ingest <DOI, citekey or PDF>`.

Other agents: the skills are plain markdown plus Python scripts, so they work wherever your agent can read a
`SKILL.md` and run a script. The installer's linking step targets Claude Code's skills folder.

## The flow

```
        /wiki-ingest  ------------>  /wiki-lint  ------------>  /wiki-synthesize
   paper -> note -> concepts        health checks               one mature note at a time
   (fulltext first, quotes          (links, provenance,         State of Knowledge block,
    verbatim, tables over           staleness, drift)           validated, PDF-checked,
    abstract)                                                    human-ratified
        ^                                                              |
        +-------------------- corrections propagate ------------------+
```

- **Ingest** one paper (or one book chapter) at a time. The note records where it came from (`source_verification`,
  `last_verified`) and what study design it is (`evidence_level`).
- **Lint** after every batch. It resolves links across the whole vault, and catches what a reader cannot see:
  orphans, unsourced claims, stale blocks, a corrected paper whose downstream notes were never updated.
- **Synthesize** only notes that rest on enough distinct sources. The block weighs findings by the evidence pyramid
  and every attribution is checked against the PDF before you approve it.

## Configuration

One file, `wiki.config.json`, found by walking up from the current folder. The keys that matter first:
`wiki_root`, the four folder names, `note_language`, `field_titlecase_map`, `min_distinct_sources_for_final`,
`synthesis.min_sources`, and a `lint` section that overrides the defaults in `wikikit/lint/defaults.json`.
`examples/minimal/wiki.config.json` is the smallest working config; `skills/wiki-lint/references/cli-reference.md`
lists every key.

## Principles

- **No fulltext, no numbers or quotes.** A note written from an abstract says so and carries no statistics.
- **A tool's silence is not a fact.** A zero from a search or a screen is a statement about the tool until a known
  positive case fires it. `docs/GOTCHAS.md` opens with this and keeps coming back to it.
- **The human decides.** The agent drafts and checks; it does not ratify a synthesis, merge notes or delete anything.
- **Notes are derived.** Concept notes summarise what sources claim, not what is generally true.

## Tests

```
python -I -m unittest discover -s tests
python -I skills/wiki-lint/scripts/lint.py --self-test
```

The self-test runs the linter against a synthetic mini-wiki with a frozen clock and compares 43 counters, so a
change in the logic of any check shows up as drift. CI runs both on Windows, macOS and Linux.

## Licence

Code (`wikikit/`, `tools/`, `skills/**/scripts/`, `tests/`): MIT, see `LICENSE`.
Documentation, schema, templates, examples and skill instructions: CC BY 4.0, see `LICENSE-DOCS`.

If you use the kit in published work, a link to this repository is appreciated.
