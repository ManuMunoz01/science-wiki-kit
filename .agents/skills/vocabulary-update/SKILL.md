---
name: vocabulary-update
description: "Generate external Oficina glossary proposals from invented A/B fixtures using BIB-7; preserve IDs and definitions, never merge."
---

# Synthetic glossary proposals

Read [shared policy](../../../t38/bib9/POLICY.md) first.
Original full package: [vocabulary-update](../../../skills/vocabulary-update/SKILL.md).
Do not run its write-in-place/default generation procedure. Read
[BIB-7 instructions](../../../t38/bib7/README.md) and
[compatibility review](../../../t38/bib7/compatibility-review.md).

From the checkout root, with a NEW output directory outside the checkout:
`python t38/bib7/adapter.py --synthetic-root t38/bib7/fixtures --a t38/bib7/fixtures/shoulder.compatibility.synthetic.md --b t38/bib7/fixtures/force.compatibility.synthetic.md --out-dir <NEW_EXTERNAL_OUTPUT>`

Read suggestions.proposed.json. Report exact existing IDs, temporary ID-less row
locators, distinct definitions/sources, extraction states and ambiguous bindings.
Alias/duplicate/data-reuse statements remain unverified and separate. No merge,
correction or source reading follows. Never add a synthetic marker to real data.
