# Lesson 04: Anatomy of a scenario

Time: ~30 min | Difficulty: Beginner | Prerequisites: Lesson 03

A scenario is data with a contract of its own. This lesson dissects the fixture format the whole course uses, then validates the fixtures themselves, because a suite is only as trustworthy as its data. The format borrows Anthropic's vocabulary: a fixture entry is a task, running it is a trial, the recorded tool calls are its transcript, and the graded end state is its outcome.

A gated entry carries an id, a type, a lead, turns, a clock, and a complete expectation: score, band, stage, tool sequence, refusals, escalations, flags, bookings, and reply count. Complete matters. An expectation that omits the tool sequence cannot catch a wrong path; one that omits refusals cannot catch a safety regression. Capability entries deliberately use a different shape: they assert on named fields and carry a `gap` field explaining what behaviour is missing.

## Run it

```bash
python3 scenario_anatomy.py
```

The audit validates all 46 gated entries and 6 capability entries: 0 schema errors, 0 duplicate ids, every expectation key set complete, every expected tool sequence starting with capture_lead, and every capability entry naming its gap. The 46 gated cases span 25 distinct types, from plain bookings and boundary scores to injections, escalations, and a refusal that arrives on turn two. Coverage by type is how you notice the case nobody wrote.

## Common failures

- Writing expectations by running the code and pasting its output, unreviewed. That freezes bugs into fixtures. The gated expectations here were verified against an independent reimplementation of the contract at build time.
- Asserting on a subset because the full expectation is tedious. Subsets are how the warm followup mutant of Lesson 05 walks through an outcome only suite.
- Letting ids collide when merging fixture files. The audit counts duplicates precisely because humans do this.

## Recap checklist

- [ ] The fixture audit reports 0 schema errors and 0 duplicate ids
- [ ] You can list the nine fields of a gated expectation
- [ ] You know why capability entries carry assert_on and gap instead of a full expectation

## Resources

- Anthropic, "Demystifying evals for AI agents" (engineering blog, 2026-01-09): the task, trial, transcript, outcome vocabulary this course uses. See [RESEARCH.md](../../RESEARCH.md).
- [fixtures/README.md](../../fixtures/README.md): the fixture documentation
