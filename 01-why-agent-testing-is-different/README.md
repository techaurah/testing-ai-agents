# Lesson 01: Why agent testing is different

Time: ~30 min | Difficulty: Beginner | Prerequisites: Lesson 00

A classical function takes inputs and returns a value, and a test compares the value. An agent takes a conversation, a clock, and a world it can change, and returns a trail of actions. Four differences follow, and this lesson demonstrates each one on the agent under test rather than asserting it.

First, inputs classical tests ignore decide outcomes: the scenario clock is part of the input whether you write it down or not. Second, the system has side effects, so the outcome lives in changed state, not in the reply text. Third, many distinct paths reach success, so grading only the ending grades almost nothing. Fourth, near a decision boundary the outcome is genuinely unstable under small wobbles, which breaks the pass or fail habit the rest of the course has to rebuild carefully.

## Run it

```bash
python3 why_different.py
```

The artifact shows all four. The same message books on Monday morning (stage BOOKED) and does not book on Saturday (stage QUALIFIED), because Saturday is outside working hours. One run of that case changes 3 of the environment's state collections (CRM records, bookings, outbox). Across the 24 scenarios the agent takes 5 distinct tool paths to its outcomes. And under the seeded stand-in of Module 7, the boundary case s03 (score exactly 80, the HOT edge) passes only 19 of 30 trials, while even the comfortable case s01 drops 2 of 30, not to threshold jitter but to phrasing swaps that hide its booking phrase. The deterministic twin itself is exact: 5 identical runs produce 1 trace variant.

## Common failures

- Treating the reply text as the outcome. The reply is narration; the booking in the calendar is the outcome.
- Writing one happy path test and calling the agent tested. Five distinct paths run through the scenario set; one test covers one of them.
- Assuming a flaky result means a broken test. At a boundary, instability is the honest behaviour of the system, and Lesson 23 teaches you to classify it instead of fighting it.

## Recap checklist

- [ ] You can name the four differences and point at the measured example of each
- [ ] You know why the scenario clock is an input, not a detail
- [ ] You know the twin is deterministic, and that instability enters only through the labelled stand-in

## Resources

- Anthropic, "Demystifying evals for AI agents" (engineering blog, 2026-01-09): the task, trial, transcript, outcome vocabulary this course uses. See [RESEARCH.md](../../RESEARCH.md).
- [Lesson 21](../21-the-seeded-stand-in/): the stand-in this lesson previews
