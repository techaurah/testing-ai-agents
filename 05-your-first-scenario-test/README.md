# Lesson 05: Your first scenario test: the mini harness

Time: ~35 min | Difficulty: Beginner | Prerequisites: Lesson 04

Time to run something. The mini harness is the smallest honest runner: fresh environment per case, run the agent, compare the outcome (score, band, stage) with the fixture. It is about thirty lines, it needs no framework, and it passes the whole scenario set. Most real agent test suites start exactly here, and many stop here, which is the problem this lesson demonstrates.

The demonstration is a mutant: a configuration with the WARM followup silently dropped. Leads still qualify, scores and stages are unchanged, customers simply never receive the followup message. Watch what the outcome only harness says about it.

## Run it

```bash
python3 mini_harness.py
```

The reference agent passes 24 of 24 scenarios on outcome. The mutant also passes 24 of 24, including all 6 WARM cases, because outcome assertions cannot see a missing step in the middle of the path. This is not an argument against the mini harness; it is the argument for the next eleven lessons. Every check the capstone suite carries exists because some realistic defect walks past everything weaker, and this dropped followup is the first of them.

## Common failures

- Growing the mini harness by adding more scenarios. Volume does not fix blindness; assertion strength does.
- Comparing reply text in the mini harness to catch path problems. That trades blindness for brittleness (Lesson 06 shows the cost).
- Dismissing the mutant as artificial. A dropped followup is a one line config or routing error, the most ordinary defect there is.

## Recap checklist

- [ ] The mini harness passes 24 of 24 on the reference agent
- [ ] It also passes 24 of 24 on the followup mutant, and you can explain why
- [ ] You can name which later lessons close this blind spot (trajectory, state)

## Resources

- [Lesson 08](../08-trajectory-assertions/): the assertion style that catches this mutant
- [Lesson 30](../30-build-the-capstone-suite/): where this harness grows into the full suite
