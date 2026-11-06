# Lesson 19: Error analysis: from red to taxonomy

Time: ~45 min | Difficulty: Intermediate | Prerequisites: Lesson 18

When a suite goes red, the count is the least interesting number on the page. Error analysis reads the actual failures and sorts them into a taxonomy, because different classes demand different fixes and a different order of work. This is the working method of the Maven eval course's instructors, applied at twin scale: read traces, name the failure modes, then fix in the order the taxonomy dictates.

The classes here: safety failures (a refusal or escalation that did not fire) are read first, always. Then band and stage failures, routing and scoring logic. Then trajectory failures, the right outcome by a wrong path. Content failures, forbidden words in replies, are classified last on purpose, and this lesson's artifact carries the scar that explains why.

## Run it

```bash
python3 error_analysis.py
```

The degraded configuration (five defects at once: lowered HOT threshold, hours guard off, WARM followup off, disclosure on, escalation off) fails 42 of 46 gated cases. Classified in the lesson's order, the table reads: band 13, stage 3, safety 3, content 23, trajectory 0. The zero is itself a finding: every case the dropped followup hurt also changed band or leaked content, so the earlier classes absorbed it, and the fix order the table dictates is safety first (the 3 escalation failures), then the threshold, then the disclosure leak that makes up most of the content class. An earlier version of this artifact classified content first and reported 40 of 40 failures as content: true, and useless.

## Common failures

- Reporting the failure count and stopping. 42 failures is one defect repeated, or five defects overlapping; only classification tells you which day you are having.
- Classifying by whichever check runs first in code order. Classification order is an editorial decision about fix priority; make it deliberately.
- Fixing in count order. The safety class has 3 entries and outranks the content class with 23, because a missed escalation is a customer harmed, not a metric dipped.

## Recap checklist

- [ ] The degraded configuration fails 42 of 46, the clean configuration 0
- [ ] You can read the taxonomy table and name the fix order it dictates
- [ ] You know why content is classified last, from this artifact's own earlier mistake

## Resources

- [RESEARCH.md](../../RESEARCH.md): the Maven course and the error analysis method this lesson follows
- [Lesson 31](../31-evaluate-and-harden/): error analysis pointed at the capstone itself
