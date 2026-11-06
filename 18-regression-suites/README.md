# Lesson 18: Regression suites

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 17

A regression set is not a smaller scenario set. It is the fossil record of behaviour the team has decided never to lose: boundary scores pinned exactly, formats that once broke, cases that once failed. It has rules of its own, and they are stricter than the scenario set's.

Entries are added when behaviour is fixed or pinned, and almost never edited afterwards; editing a regression expectation to match new behaviour is how suites learn to lie. It runs fast and gates everything. And it is judged at 100 percent: a 9 of 10 regression suite is a failing suite with good public relations.

## Run it

```bash
python3 regression_suite.py
```

The set passes 10 of 10 against the reference agent, pinning boundary scores at 100, 80, 78, 65, 64, 50, and 49, plus a no signals case at 21, the 1.5k budget format at 90, and a mid nurture case at 60. Against a mutant with the HOT threshold lowered to 60, the suite passes only 6 of 10, failing r03, r04, r05, and r10: every failure a score sitting just under the old HOT line, exactly the population the boundary pins exist to protect.

## Common failures

- Regenerating regression expectations after a refactor because most still pass. The failures are the information; regeneration deletes it.
- Adding ordinary scenarios to the regression set until it is just a second scenario set. Regression entries earn their place by having broken, or by sitting on a boundary.
- Accepting 9 of 10 with a plan to fix the tenth later. The gate is the discipline; later is how 9 becomes 7.

## Recap checklist

- [ ] The regression set passes 10 of 10 and pins seven boundary scores
- [ ] The threshold mutant passes only 6 of 10, first failure r03
- [ ] You can state the rule about editing regression expectations

## Resources

- [Lesson 20](../20-capability-vs-regression/): the other suite species, and why it must never gate
- [Lesson 02](../02-meet-the-agent-under-test/): where the boundary pins were first audited
