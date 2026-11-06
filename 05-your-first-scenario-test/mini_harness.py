"""Lesson 05 artifact: the mini harness, and its blind spot.

The mini harness is the smallest honest runner: fresh
environment per case, run the agent, compare the outcome
(score, band, stage) with the fixture expectation. It passes
the whole scenario set. Then the lesson runs it against a
mutant whose routing changed underneath identical outcomes
(the WARM follow-up silently dropped): the outcome-only
harness still passes every case, which is exactly the blind
spot Lessons 08 and 12 exist to close.

Offline, standard library only. Run: python3 mini_harness.py
"""

import json
import os
import sys
from datetime import datetime

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
import lead_agent as la


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def outcome_passes(case, config=None):
    env = la.Environment()
    result = la.LeadAgent(config).run(
        env, case["lead"], case["turns"],
        datetime.fromisoformat(case["now"]))
    expect = case["expect"]
    return (result["score"] == expect["score"]
            and result["band"] == expect["band"]
            and result["stage"] == expect["stage"])


def evaluate():
    scenarios = load("scenarios.json")
    passed = sum(1 for c in scenarios if outcome_passes(c))
    mutant = {"warm_followup": False}
    mutant_passed = sum(1 for c in scenarios if outcome_passes(c, mutant))
    warm_cases = [c for c in scenarios if c["expect"]["band"] == "WARM"]
    warm_mutant_passed = sum(1 for c in warm_cases if outcome_passes(c, mutant))
    return {
        "scenarios": len(scenarios),
        "outcome_passed": passed,
        "mutant_name": "warm_followup_off",
        "mutant_outcome_passed": mutant_passed,
        "warm_cases": len(warm_cases),
        "warm_cases_mutant_outcome_passed": warm_mutant_passed,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
