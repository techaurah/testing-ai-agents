# Lesson 23: Flaky tests: find them, classify them

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 22

A flaky test passes sometimes and fails sometimes on the same code. In agent suites most flakiness is neither a broken test nor a broken agent; it is an assertion written at the wrong strength for the case it grades, or a case sitting where the system's outcome is genuinely undecided. The craft is classification, because the responses differ: outcome flakiness near boundaries is handled with statistics, wording flakiness by weakening the assertion to what matters, and genuine defects by fixing the agent.

This lab runs every scenario through the stand-in for 20 trials and sorts the results, then aims the strongest assertion in the course, exact reply equality, at the most comfortable case in the set.

## Run it

```bash
python3 flakiness.py
```

15 of 24 scenarios flake under outcome assertions (0 always fail, 9 are stable), arriving through both channels: boundary cases on threshold jitter, and comfortable cases like s01, s13, and s14 when a phrasing swap hides the phrase their routing depends on. Then the wording result: exact reply assertions on s01 pass only 7 of 20 trials, against 19 of 20 for its outcome assertions, because the courtesy suffix alone defeats byte equality two times in three. Same system, same case, different assertion, completely different flakiness.

## Common failures

- Retrying a flaky test until it passes and merging. That converts information into noise and teaches the suite to lie on schedule.
- Weakening every assertion that flakes. Some flaky cases are defects wearing a disguise; classification comes before any weakening, and the stand-in's channels give you the vocabulary to tell them apart.
- Quarantining flaky cases silently. A quarantined case is a deleted case with extra steps; if it leaves the gate, the report should say so and say why.

## Recap checklist

- [ ] 15 flaky, 9 stable, 0 always failing scenarios under outcome assertions
- [ ] s01: outcome 19 of 20, exact replies 7 of 20, and you can explain the gap
- [ ] You can match each flakiness class to its response

## Resources

- [Lesson 21](../21-the-seeded-stand-in/): the two channels that produce the flaky list
- [Lesson 06](../06-exact-and-structural-assertions/): assertion strength, the dial this lesson turns
