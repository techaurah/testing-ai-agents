# Lesson 28: Eval driven development

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 27

The loop, run once in the open: pick one failing capability case, state the behaviour it names, make the smallest change that earns it, then prove the gated sets did not move. It is test driven development with the capability suite as the test list, and it is the workflow Anthropic's guidance describes as hillclimbing: one change at a time, judged against held out examples, which here are the gated sets.

The case is cap01. A budget written in words (two thousand dollars) loses to the first stray digit in the message, the 7 from within 7 days, and the lead is under scored. The fix is deliberately small: a word number table that wins when the author wrote the amount in words, applied here as a wrapper around the agent's extractor, exactly where the real fix would go in the parser.

## Run it

```bash
python3 edd_loop.py
```

One loop iteration, measured: the capability set goes from 2 of 6 to 3 of 6, cap01 flips to passing, and the gated sets stay at 46 of 46 before and after. Five gaps were open at the module's start; four remain (cap02, cap03, cap06, and one more the loop did not choose), each still named in the fixture. The loop repeats when someone chooses the next gap, not before, and the suite's job is to make each iteration this boring.

## Common failures

- Fixing three gaps in one change. When the gated sets move, and they will, you will not know which fix moved them.
- Choosing the easiest gap rather than the most valuable one, repeatedly. The loop's discipline is one at a time; the roadmap's discipline is choosing by cost of the gap, and Lesson 20's entries carry the evidence.
- Declaring victory at the capability flip and skipping the gated re-run. The gated sets staying at 46 of 46 is half the result; print both halves or you have shown nothing.

## Recap checklist

- [ ] Capability moves 2 of 6 to 3 of 6 with cap01 fixed
- [ ] Gated sets hold at 46 of 46 across the change
- [ ] You can run the loop's four steps from memory

## Resources

- Anthropic, "Demystifying evals for AI agents" (engineering blog, 2026-01-09): the task, trial, transcript, outcome vocabulary this course uses. See [RESEARCH.md](../../RESEARCH.md).
- [Lesson 20](../20-capability-vs-regression/): the suite this loop draws its work from
