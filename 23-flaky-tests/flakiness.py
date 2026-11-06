"""Lesson 23 artifact: flaky tests, found and classified.

A flaky test passes sometimes and fails sometimes on the same
code. In agent suites most flakiness is not a broken test or
a broken agent; it is an assertion written at the wrong
strength for a case that sits on a decision boundary. This
lab proves the split:

- Outcome assertions over every scenario, 20 stand-in trials
  each: the flaky list arrives through both of the stand-in's
  channels. Boundary cases flake on threshold jitter. But
  comfortable cases flake too, when a phrasing swap hides the
  phrase their routing depends on: s01 and its Saturday twin
  s13 score 93, far from every edge, and still miss trials.
- Exact reply assertions on the most comfortable case in the
  set: they flake hardest of all, on wording alone, because
  the stand-in sometimes appends a courtesy suffix. Same
  system, same case, different assertion, different flakiness.

The response differs by class: outcome flakiness is handled
with statistics (Lessons 22 and 24); wording flakiness is
handled by weakening the assertion to what matters.

Offline, standard library only. Run: python3 flakiness.py
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

TRIALS = 20


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def evaluate():
    scenarios = load("scenarios.json")
    rates = {}
    for case in scenarios:
        hits = sum(1 for seed in range(TRIALS)
                   if standin.outcome_matches(
                       standin.run_trial(case, seed)["result"],
                       case["expect"]))
        rates[case["id"]] = hits / TRIALS
    flaky = sorted(cid for cid, r in rates.items() if 0 < r < 1)
    always_fail = sorted(cid for cid, r in rates.items() if r == 0)
    s01 = {c["id"]: c for c in scenarios}["s01"]
    goldens = load("golden_trajectories.json")
    golden_replies = next(g["replies"] for g in goldens
                          if g["source_case"] == "s01")
    exact_reply_passes = 0
    for seed in range(TRIALS):
        result = standin.run_trial(s01, seed)["result"]
        if result["replies"] == golden_replies:
            exact_reply_passes += 1
    return {
        "scenarios": len(scenarios),
        "trials_each": TRIALS,
        "flaky_cases": flaky,
        "always_fail_cases": always_fail,
        "stable_cases": len(scenarios) - len(flaky) - len(always_fail),
        "s01_exact_reply_passes_of_20": exact_reply_passes,
        "s01_outcome_passes_of_20": int(rates["s01"] * TRIALS),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
