# Lesson 14: Golden trajectories

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 13

A golden trajectory is a recorded, reviewed, frozen run: the complete trace of a conversation a human has read and signed off as correct. Goldens catch drift that outcome and trajectory assertions cannot see, because they compare the whole path at once, replies included. They are also the most brittle tool in this course, so the lesson is mostly discipline.

Goldens are recorded from reviewed behaviour, never generated blindly from the code under test, or the golden freezes whatever the code happened to do. They are few on purpose: six load bearing conversations, not forty six. And when one fails, the output is a drift report for a human to judge, not a verdict: legitimate change earns a re-recorded golden with a reason in the commit, illegitimate drift earns a fix.

## Run it

```bash
python3 golden_trajectories.py
```

All 6 goldens replay exactly against the recorded file (full trace, replies, score, band, stage, and final state). The drift demonstration runs g-s01 under a halved budget weight: the report shows the first differing step at index 2, where the golden has calendar_check and the drifted run writes the CRM instead, because the drifted score (70, down from the golden 93) routes WARM and never consults the calendar. That is a drift report a reviewer can judge in seconds.

## Common failures

- Recording goldens from unreviewed runs. An unreviewed golden is the code grading its own homework.
- Golden inflation: recording every case because recording is easy. Each golden is a future triage obligation; six is a commitment, forty six is a backlog.
- Re-recording a golden to make a red suite green without writing down why. The reason in the commit is the entire value of the exercise.

## Recap checklist

- [ ] 6 of 6 goldens replay exactly
- [ ] The drift report names step 2, calendar_check expected, crm_write actual
- [ ] You can state when a golden should be re-recorded versus when the code should be fixed

## Resources

- [Lesson 06](../06-exact-and-structural-assertions/): why exact comparison lives here and not everywhere
- [fixtures/golden_trajectories.json](../../fixtures/golden_trajectories.json): the recorded traces, with their source cases
