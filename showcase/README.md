# Capstone showcase

Finished, graded test suites from learners of Testing AI Agents.
This table is the course's completion artifact: no
certificates, just suites anyone can clone, run against the
bundled agent, and re-grade against the same gates.

## How to get your suite indexed

1. Finish the capstone (Lessons 29 to 32). Your suite must be in a public repository of your own, read its gates from a file like Lesson 29's `gates.json`, and publish its Lesson 31 gate table in its README: every gate, its threshold, and its measured value, including any gate you miss, plus your full mutation kill table.
2. Fork this repository and add **one row** to the table below: your name or GitHub handle, a link to your suite repository, and your headline results (gated sets, mutants killed).
3. Open a pull request titled `Showcase: <your handle>`. Small, single-purpose PRs like this merge directly under the course's [two-tier contribution rule](../CONTRIBUTING.md); you do not need to open an issue first.
4. A maintainer checks that the link works, the gate table and kill table are present and complete, and the numbers are the suite's output rather than aspirations. A suite that reports a surviving mutant honestly, with the check it plans to add, ranks above one that reports only kills.

One row per learner. If you harden your suite and rerun it, update your row with a second PR.

## Showcase

| Learner | Suite | Gate results (scenarios, safety, regression, mutants killed) |
|---------|-------|---------------------------------------------------------------|
| TechAura (reference build) | This repository, Lessons 29 to 32 | 24 of 24 scenarios, 12 of 12 safety, 10 of 10 regression, mutants 8 of 8 |
| _Your name here_ | _Your repository link here_ | _Your measured results here_ |
