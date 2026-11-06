# Changelog

All notable changes to this course are recorded here. The format follows the usual Keep a Changelog shape, and versions are the course's own (a version is a state of the lessons, fixtures, and capstone gates, not of any library).

## [1.0.0] - 2026-11-06

First complete release.

- 33 lessons in 10 modules, from why agent testing is different to a shipped capstone suite, every lesson with a runnable standard library artifact, an exercise, a worked solution, and a smoke test.
- The agent under test: a deterministic lead qualification twin (`agent/`) with a written contract, eight tools, and a labelled seeded stand-in for the nondeterminism module.
- Fixtures: 24 scenarios, 12 safety cases, 10 regression cases with boundary scores pinned exactly, 6 capability cases with named gaps (2 of 6 passing at baseline), 6 golden trajectories, and a budgets contract.
- The capstone: gates fixed in advance in Lesson 29 (including a mutation gate of at least 7 of 8), a full suite in Lesson 30, and the evaluate and harden comparison in Lesson 31. Reference build: all gated sets pass in full and 8 of 8 mutants are killed; the Lesson 05 outcome only harness kills 4 of 8 on the same mutants.
- Eight branded SVG diagrams, course validators and a link checker in `tools/`, and CI running compile, validation, link checks, and every lesson smoke test.
