# Lesson 22: pass@k and pass^k

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 21

When a system is nondeterministic, one run proves almost nothing, and a single pass rate hides the question you actually need answered. The agent literature uses two rates over repeated trials. pass@k is the probability that at least one of k trials passes: the right question for an assistant with a human in the loop, who can pick the good attempt. pass^k is the probability that all k trials pass: the right question for an agent acting alone, where every attempt ships.

Both come from one measured per trial rate p: pass@k = 1 - (1 - p)^k, pass^k = p^k. This lesson measures p empirically for three cases over 40 fresh seeds and prints both rates at k of 1, 3, and 5.

## Run it

```bash
python3 pass_rates.py
```

Case s01 measures p = 0.825: pass@5 is 0.9998 (a human picking from five attempts almost always finds a good one) while pass^5 is 0.3822 (five unsupervised attempts all pass barely a third of the time). The boundary cases s03 and s05 measure p = 0.475 each, and the columns separate brutally: pass@3 = 0.8553 against pass^3 = 0.1072. The same system, the same trials, two honest numbers an order of magnitude apart. Choosing which one to report is choosing what you are claiming.

## Common failures

- Reporting pass@k for an unsupervised agent because it is the bigger number. That is not optimism, it is a category error, and Lesson 24 shows how intervals expose thin evidence behind either rate.
- Estimating p from a handful of trials. These rates exponentiate p, so a sloppy p becomes a very sloppy pass^5; 40 trials is a floor, not a luxury.
- Computing the rates from the twin. The deterministic twin has p of exactly 1 or 0 per case; these measures only exist under the stand-in or a real model.

## Recap checklist

- [ ] s01: p 0.825, pass@5 0.9998, pass^5 0.3822
- [ ] s03 and s05: p 0.475, pass@3 0.8553, pass^3 0.1072
- [ ] You can say which rate an unsupervised booking agent should be judged by, and why

## Resources

- Anthropic, "Demystifying evals for AI agents" (engineering blog, 2026-01-09): the task, trial, transcript, outcome vocabulary this course uses. See [RESEARCH.md](../../RESEARCH.md).
- [Lesson 24](../24-how-many-runs-are-enough/): how much evidence a rate needs
