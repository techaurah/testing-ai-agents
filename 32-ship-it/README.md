# Lesson 32: Ship it: document, demo, and showcase your suite

Time: ~30 min | Difficulty: Intermediate | Prerequisites: Lesson 31

The last lesson is a checklist that runs. Before a suite (or a course about suites) ships, the audit in this lesson's artifact confirms three things. Every lesson folder on the map carries its four parts: the written lesson, the exercise, the runnable artifact with its smoke test, and the worked solution. The capstone scorecard the README quotes is regenerated from the suite itself, so the numbers in the documentation are the numbers the code produces today. And three demo conversations run end to end for the showcase: one booking, one nurture, one escalation.

If any row is red, the work is not done, whatever the calendar says. That is the whole lesson, and it is also the job on every project after this one: the deliverable is not the suite, it is the suite plus the evidence that it does what its documentation claims.

## Run it

```bash
python3 ship_it.py
```

The audit reports 33 lesson folders with no incomplete parts. The regenerated scorecard matches the README: scenarios 24 of 24, safety 12 of 12, regression 10 of 10, mutants 8 of 8, goldens exact. The demos: the booking conversation ends HOT and BOOKED in 6 tool calls; the nurture conversation ends NURTURE and QUALIFIED in 5; the escalation conversation ends at stage NEW with no band (it was escalated before scoring) in 3 tool calls, which is the correct shape for a conversation a human now owns. The showcase row the artifact prints is the format the showcase file asks learners to submit with their own numbers.

## Common failures

- Quoting a scorecard from the day the docs were written. Suites drift; a shipped claim should be regenerated at ship time, which is why this audit re-runs the capstone instead of reading its old output.
- Shipping with a red row explained in a comment. If the row matters, fix it; if it does not, delete the row and say why in the commit. An explained red is still red.
- Ending a course (or a project) with the demo untested. The three demos here are assertions, not screenshots; they run in CI like everything else.

## Recap checklist

- [ ] 33 lesson folders, no incomplete parts
- [ ] The regenerated scorecard matches the README's quoted numbers
- [ ] The three demo conversations produce their asserted outcomes

## Resources

- [showcase/README.md](../../showcase/README.md): the row this lesson generates, in place
- [PROGRESS.md](../../PROGRESS.md): your own checklist, if you worked the course in order
