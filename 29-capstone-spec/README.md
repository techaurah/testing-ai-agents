# Lesson 29: Capstone spec: the suite and its gates, fixed in advance

Time: ~30 min | Difficulty: Intermediate | Prerequisites: Lesson 28

The capstone is a complete test suite for the bundled agent, and it begins the way honest evaluations begin: with the gates written down before the suite exists. The specification lives in `capstone/gates.json` next to this lesson's artifact: the set sizes, the seven gates, and the eight mutants the suite must catch.

The gates: scenarios 24 of 24, safety 12 of 12, regression 10 of 10, golden trajectories 6 of 6 exact, budgets within the contract on every gated case, idempotency verified, and a mutation score of at least 7 of 8. The mutants are config level defects of the kinds this course has been planting since Lesson 05: a lowered HOT threshold, the injection guard off, escalation disabled, the booking hours guard off, score disclosure on, idempotent writes off, the WARM followup off, and a halved budget weight.

## Run it

```bash
python3 capstone_spec.py
```

The artifact cross checks the spec against reality before anyone builds to it: every set count in gates.json matches the fixture files exactly (24, 12, 10, 6, and 6 capability reported not gated), all 7 gates are declared, all 8 mutants are present (m1 to m8), and every mutant configuration key is a real key in the agent's config. A spec that disagrees with the fixtures is a plan to fail; this check goes red first, while fixing it is still free.

## Common failures

- Writing gates after seeing the suite's results. Gates fitted to results are decorations; the mutation gate in particular must be set without knowing the score.
- Declaring a mutation gate of 8 of 8 because it sounds stronger. The gate is at least 7 of 8 to leave room for one honestly equivalent mutant; the reference build's measured score is reported separately from the gate.
- Letting the spec and the fixtures drift. The cross check in this lesson is a test of the test plan, and it belongs in the suite permanently.

## Recap checklist

- [ ] The spec's set counts match the fixtures exactly
- [ ] 7 gates and 8 mutants declared, all mutant config keys valid
- [ ] You can recite the seven gates without looking

## Resources

- [DESIGN.md](../../DESIGN.md): the capstone spec in the course design
- [Lesson 30](../30-build-the-capstone-suite/): the suite built to this spec
