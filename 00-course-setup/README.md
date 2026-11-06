# Lesson 00: Course setup: what you need, and how this course works

Time: ~20 min | Difficulty: Beginner | Prerequisites: None

This course teaches you to test AI agents by building a complete test suite for one small agent, and it makes a promise most courses do not: every number it quotes is the output of the code in the lesson, run on the fixtures bundled in this repository. If a technique measures badly here, the lesson prints the bad number and explains it. There are no borrowed benchmarks, no market statistics, and no certificates at the end, just a suite you built and can defend.

Everything runs offline on the Python standard library. The agent under test lives in `agent/`, the fixtures in `fixtures/`, and each lesson carries one runnable artifact that demonstrates its idea against both. This first lesson verifies your environment and walks the shape of what you will be testing, so later surprises are about ideas, not setup.

## Run it

```bash
python3 check_environment.py
```

The check confirms Python 3.11 or newer, finds the agent under test (8 tools, 4 stages: NEW, QUALIFIED, BOOKED, LOST), and counts the fixtures: 24 scenarios, 12 safety cases, 10 regression cases, 6 capability cases, and 6 golden trajectories. The three gated sets total 46 cases; the capability set is reported but never gated, for reasons Lesson 20 makes precise.

## Common failures

- Running a lesson's code from the repository root instead of its own folder. Each artifact finds the repo root by walking up from its own file, so it works from anywhere, but the smoke tests expect to run from the lesson folder.
- Expecting to install something. There is nothing to install; if you reach for pip, you have taken a wrong turn.
- Skipping the fixture folders. `agent/` and `fixtures/` are shared instruments for the whole course, not per lesson code.

## Recap checklist

- [ ] `python3 check_environment.py` runs and prints gated_cases: 46
- [ ] You can name the four fixture sets and which three are gated
- [ ] You know the course rule: every number comes from running the code

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [agent/README.md](../../agent/README.md): the contract of the agent under test
