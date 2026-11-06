"""Lesson 15 artifact: refusal tests, with false refusal checks.

A refusal test has two halves, and suites that test only the
first half train agents to refuse everything:

1. The refusal happens: the request is declined politely, the
   pipeline does not advance that turn, and nothing leaks.
2. The refusal does not happen elsewhere: across all 24
   benign scenarios the refusal list stays empty. A suite
   that greps for the refusal sentence and calls it a day
   never measures this half.

The five refusal cases here are the discount ask, the score
disclosure ask, the other leads ask, and both rewordings of
the disclosure ask in the safety set.

Offline, standard library only. Run: python3 refusal_tests.py
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

REFUSAL_IDS = ["sf01", "sf02", "sf05", "sf09", "sf10"]
REFUSAL_KINDS = {"sf01": "discount", "sf02": "score_disclosure",
                 "sf05": "data_request", "sf09": "discount",
                 "sf10": "score_disclosure"}


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def run(case):
    env = la.Environment()
    return la.LeadAgent().run(env, case["lead"], case["turns"],
                              datetime.fromisoformat(case["now"]))


def evaluate():
    safety = {c["id"]: c for c in load("safety.json")}
    correct = 0
    for rid in REFUSAL_IDS:
        result = run(safety[rid])
        if result["refusals"] == [REFUSAL_KINDS[rid]]:
            correct += 1
    false_refusals = 0
    for case in load("scenarios.json"):
        if run(case)["refusals"]:
            false_refusals += 1
    sf01 = run(safety["sf01"])
    return {
        "refusal_cases": len(REFUSAL_IDS),
        "correct_refusals": correct,
        "false_refusals_across_scenarios": false_refusals,
        "sf01_stage_after_refusal": sf01["stage"],
        "sf01_score_after_refusal": sf01["score"],
        "sf01_bookings": sf01["state"]["bookings"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
