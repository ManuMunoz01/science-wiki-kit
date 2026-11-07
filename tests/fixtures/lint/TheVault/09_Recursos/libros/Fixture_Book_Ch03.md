---
tags: [book-chapter, fixture]
date: 2024-01-15
project: Investigacion
type: book-chapter
title: "Chapter three on filesystem but not declared"
book: "[[Fixture_Book]]"
chapter_number: 3
citekey: "brown2024book_ch3"
---

# Brown 2024 - Ch03

Exists on filesystem but parent book has `chapters_ingested: [Ch01, Ch02]` so Check 8 should flag the sync mismatch.
Body has [[BrokenTarget]] and [[ChapterNote]] (placeholder) to exercise Check 5 broken + placeholder detection.
