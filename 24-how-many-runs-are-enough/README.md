# Lesson 24: How many runs are enough

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 23

Two tools, both computable with the standard library, both honest about their limits. The Wilson score interval turns a pass count into a range: twenty passes in twenty trials does not mean a 100 percent pass rate, it means a rate whose 95 percent interval reaches down to a number this lesson prints. A suite report that shows the interval next to the count is telling the truth; one that shows only the percentage is performing.

The failure catching rule answers the design question: to have a 95 percent chance of seeing at least one failure from a defect that strikes with probability q per run, you need n >= log(0.05) / log(1 - q) runs. This is the arithmetic that decides how big a trials tier has to be before its green result means anything.

## Run it

```bash
python3 sample_sizes.py
```

The intervals: 20 of 20 gives (0.8389, 1.0), 50 of 50 gives (0.9286, 1.0), 100 of 100 gives (0.963, 1.0), and 47 of 50 gives (0.8378, 0.9794). Perfect runs narrow the interval, never to a point. The catching rule: a 5 percent per run defect needs 59 runs for 95 percent detection, a 10 percent defect needs 29, and a 1 percent defect needs 299. And the sobering corollary printed by the artifact: a 5 percent defect survives a 20 run suite with probability 0.3585, about one time in three.

## Common failures

- Quoting a pass rate without its trial count. 20 of 20 and 100 of 100 are different evidence wearing the same percentage.
- Treating the interval's top as the estimate. The interval is the claim; its width is the honesty.
- Sizing a trials tier by what CI can afford and then claiming the confidence that size cannot buy. The arithmetic runs both directions: pick the defect rate you must catch, and the run count follows.

## Recap checklist

- [ ] Wilson interval for 20 of 20 is (0.8389, 1.0), and you can say what it means
- [ ] 59 runs to catch a 5 percent defect at 95 percent confidence
- [ ] A 5 percent defect survives 20 runs with probability 0.3585

## Resources

- [Lesson 22](../22-pass-at-k-and-pass-pow-k/): the rates these intervals discipline
- [Lesson 27](../27-wiring-the-suite-into-ci/): where the trials tier lives in CI
