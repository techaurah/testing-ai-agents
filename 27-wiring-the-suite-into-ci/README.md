# Lesson 27: Wiring the suite into CI

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 26

One suite, three tiers, because CI time and merge risk are both real. The smoke tier runs on every push: two load bearing cases per gated set, seconds of work, catching a build that cannot run the agent at all. The core tier runs on every pull request: the full gated sets, and it is the merge gate. The full tier runs nightly and on demand: core plus budget checks, golden replay, and the capability report printed for humans, reported and never gated (Lesson 20).

This repository's own CI workflow (`.github/workflows/ci.yml`) wires the same shape to real events, adding course validation and a smoke test in every lesson folder. This lesson's artifact runs the tiers in process and proves the gate logic end to end.

## Run it

```bash
python3 ci_tiers.py
```

Smoke: 6 cases, 6 passing on the reference agent. Core: 46 cases, 46 passing, exit code 0. Then the proof that the gate is a gate: a degraded configuration (the HOT threshold moved to 60) passes only 33 of 46 core cases and the tier exits 1. A CI wiring that cannot demonstrate its own failure mode is a decoration; this one fails on demand, in the lesson, before it ever has to fail on a pull request.

## Common failures

- Putting the full tier on every push because thoroughness feels safer. Slow gates get bypassed, and a bypassed thorough gate is worse than a fast gate that runs.
- Gating on the capability report because it is printed right there. Lesson 20's rule survives contact with CI: reported, never gated.
- Letting the smoke tier grow case by case until it is the core tier with worse coverage. Tiers have jobs; a case joins smoke by being load bearing, not by being someone's favourite.

## Recap checklist

- [ ] Smoke 6 of 6, core 46 of 46, reference exit code 0
- [ ] The degraded configuration passes 33 of 46 and exits 1
- [ ] You can name the three tiers, their triggers, and their jobs

## Resources

- [.github/workflows/ci.yml](../../.github/workflows/ci.yml): this repo's real wiring
- [Lesson 24](../24-how-many-runs-are-enough/): sizing the nightly trials tier
