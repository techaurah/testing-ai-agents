"""Lesson 21 artifact: the seeded stand-in laboratory.

A deterministic twin cannot teach nondeterminism, so the
course ships a labelled stand-in (agent/standin.py) that
injects controlled wobble: thresholds jitter by a seeded
amount, phrases are sometimes swapped for synonyms the parser
does not know, replies sometimes gain a courtesy suffix.
Every trial is reproducible from its seed.

The lab's first lesson: stability is a property of the case,
not of the system, and no watched case here is fully stable.
The comfortable case s01 comes closest at 28 of 30: its score
clears every threshold the jitter can reach, and its two
failures arrive through the wording channel, phrasing swaps
that hide its booking phrase. The boundary cases, whose
scores sit on the band edges (s03 at 80, s05 at 65, s07 at
50, s10 at 49), pass far fewer trials, and no amount of
re-running changes that: their outcomes are genuinely
undecided under wobble, and the suite design has to treat
them differently (Lesson 24).

Offline, standard library only. Run: python3 standin_lab.py
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

TRIALS = 30


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def pass_count(case, trials=TRIALS):
    return sum(1 for seed in range(trials)
               if standin.outcome_matches(
                   standin.run_trial(case, seed)["result"], case["expect"]))


def evaluate():
    scenarios = {c["id"]: c for c in load("scenarios.json")}
    watched = ["s01", "s03", "s05", "s07", "s10"]
    counts = {cid: pass_count(scenarios[cid]) for cid in watched}
    first = standin.run_trial(scenarios["s03"], 7)
    second = standin.run_trial(scenarios["s03"], 7)
    reproducible = (first["result"] == second["result"]
                    and first["threshold_delta"] == second["threshold_delta"])
    return {
        "trials_per_case": TRIALS,
        "pass_counts": counts,
        "stable_cases": [c for c, n in counts.items() if n == TRIALS],
        "unstable_cases": [c for c, n in counts.items() if 0 < n < TRIALS],
        "same_seed_reproduces_exactly": reproducible,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
