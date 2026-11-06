# Lesson 20: Capability vs regression suites

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 19

Two suite species, distinguished by intent, and the distinction decides how a red result is handled. Regression suites protect behaviour you already have: they gate merges and sit at 100 percent (Lesson 18). Capability suites measure behaviour you are trying to gain: they start red, may stay partly red for months, and must never gate, because gating on them teaches teams to delete hard cases or quietly lower the bar.

This course's capability set names six intended behaviours the twin does not have yet. Each entry asserts on a few named fields rather than a full expectation, and carries the gap in writing: a budget written in words, an enquiry in Spanish, signals that arrive on turn two, a budget range, typo tolerance, and an explicit do not call that the parser misreads as its opposite.

## Run it

```bash
python3 two_suites.py
```

The report is the honest shape of a healthy project: gated sets at 46 of 46 (rate 1.0), the capability set at 2 of 6 (cap04 and cap05, budget ranges and typos, already pass), with four open gaps still named. Nothing about the 2 of 6 is hidden or averaged into the gated number, and nothing about it blocks a merge. It is a roadmap with a scoreboard, and Lesson 28 picks one entry off it and closes it.

## Common failures

- Merging the two rates into one suite percentage. The average of a gate and a roadmap is a number that means neither.
- Deleting a capability case that has been red for months. A stale gap is a prioritisation conversation, not a deletion; the gap text keeps the cost visible.
- Writing capability expectations vaguely so they pass early. cap06 asserts stage QUALIFIED and 0 bookings for a do not want a call lead the twin currently books; the assertion is the specification of the fix.

## Recap checklist

- [ ] Gated sets report 46 of 46 and capability 2 of 6, separately
- [ ] You can name the four open gaps and their case ids
- [ ] You can explain why capability suites must never gate

## Resources

- Anthropic, "Demystifying evals for AI agents" (engineering blog, 2026-01-09): the task, trial, transcript, outcome vocabulary this course uses. See [RESEARCH.md](../../RESEARCH.md).
- [Lesson 28](../28-eval-driven-development/): the loop that closes cap01
