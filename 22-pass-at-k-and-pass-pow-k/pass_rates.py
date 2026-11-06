"""Lesson 22 artifact: pass@k and pass^k, the two honest rates.

When a system is nondeterministic, one run proves almost
nothing. The agent literature (Anthropic's eval vocabulary)
uses two rates over repeated trials:

- pass@k: the probability that at least one of k trials
  passes. Right for assistants with a human in the loop, who
  can pick the good attempt.
- pass^k: the probability that all k trials pass. Right for
  agents acting alone, where every attempt ships.

Both are computed from one measured per trial rate p:
pass@k = 1 - (1 - p)^k and pass^k = p^k. The lab measures p
empirically for the two boundary cases from Lesson 21 over
40 fresh seeds, then prints both rates for k = 1, 3, 5. The
spread between the columns is the whole lesson: the same
system looks reliable or fragile depending on which question
you honestly need answered.

Offline, standard library only. Run: python3 pass_rates.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def find_root():
    cur = HERE
    while True:
        if os.path.isfile(os.path.join(cur, "agent", "lead_agent.py")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise FileNotFoundError("repo root (agent/) not found above " + HERE)
        cur = parent


ROOT = find_root()
sys.path.insert(0, os.path.join(ROOT, "agent"))
import standin

TRIALS = 40


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def empirical_p(case, trials=TRIALS):
    hits = sum(1 for seed in range(1000, 1000 + trials)
               if standin.outcome_matches(
                   standin.run_trial(case, seed)["result"], case["expect"]))
    return hits / trials


def rates(p):
    return {f"k={k}": {"pass_at_k": round(1 - (1 - p) ** k, 4),
                       "pass_pow_k": round(p ** k, 4)}
            for k in (1, 3, 5)}


def evaluate():
    scenarios = {c["id"]: c for c in load("scenarios.json")}
    out = {"trials_per_case": TRIALS}
    for cid in ("s01", "s03", "s05"):
        p = empirical_p(scenarios[cid])
        out[cid] = {"p_empirical": round(p, 4), "rates": rates(p)}
    return out


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
