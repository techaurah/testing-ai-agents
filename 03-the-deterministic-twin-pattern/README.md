# Lesson 03: The deterministic twin pattern

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 02

Real agents call models, and models wobble. The twin pattern is how you test anyway: build (or configure) a stand-in for the system that behaves identically on identical inputs, with every input explicit, and write your exact tests against the twin. The agent under test is such a twin of a lead qualification agent: rule based, deterministic, and honest about being a twin, with its contract published in `agent/README.md`.

The pattern has three rules. Give every case a fresh environment, because state is an input. Make every input data (lead, turns, clock), so any case replays from its fixture alone. And keep the twin faithful where it matters: same scoring, same routing, same safety order as the system it stands for. Where the twin is simpler than the real system, the contract says so.

## Run it

```bash
python3 twin_pattern.py
```

All 46 gated cases replay byte identically across two runs in fresh environments (46 of 46). The contamination demo shows why the fresh environment rule exists: run s01 and then s11 through one shared environment and the second lead is captured as LD-002, with 2 CRM records in the shared state; in a fresh environment the same case is LD-001. Nothing about the second case changed except the world it ran in, which is precisely the class of failure fresh environments eliminate.

## Common failures

- Sharing one environment across a test file for speed. The contamination is silent and order dependent, the worst kind of test bug.
- Making the twin smarter than the real system. A twin that fixes the real system's parser gaps teaches your suite to expect behaviour production does not have; this course's capability set exists to keep that gap visible instead.
- Hiding inputs in globals. If the clock or the config is not in the fixture, the case cannot be replayed by anyone else.

## Recap checklist

- [ ] All 46 gated cases replay byte identically in fresh environments
- [ ] You can explain why the shared environment produced LD-002
- [ ] You can name the twin's three rules

## Resources

- [Lesson 21](../21-the-seeded-stand-in/): the deliberate, labelled exception to determinism
- [QualBench](https://github.com/techaurah/qualbench): TechAura's deterministic benchmark project, the spirit this pattern follows
