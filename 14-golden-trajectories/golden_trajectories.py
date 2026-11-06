"""Lesson 14 artifact: golden trajectories and drift reports.

A golden trajectory is a recorded, reviewed, frozen run: the
complete trace of a conversation someone has read and signed
off as correct. Goldens catch drift that outcome assertions
cannot see, because they compare the whole path at once.

The discipline matters more than the comparison:

- Goldens are recorded from reviewed behaviour, never
  generated blindly from the code under test.
- On a mismatch, the test prints a drift report (first
  differing step, expected next, actual next) for a human to
  judge: legitimate change gets a re-recorded golden with a
  reason in the commit; illegitimate drift gets a fix.
- Goldens are few on purpose: six load bearing conversations,
  not forty six.

Here: all six replay exactly against the recorded file, and
a drifted configuration produces the report format on g-s01.

Offline, standard library only. Run: python3 golden_trajectories.py
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


GOLDEN_KEYS = ("trace", "replies", "score", "band", "stage", "state")


def sources():
    out = {}
    for name in ("scenarios.json", "safety.json", "regression.json"):
        for case in load(name):
            out[case["id"]] = case
    return out


def replay(golden, config=None):
    case = sources()[golden["source_case"]]
    env = la.Environment()
    result = la.LeadAgent(config).run(
        env, case["lead"], case["turns"],
        datetime.fromisoformat(case["now"]))
    return {k: result[k] for k in GOLDEN_KEYS}


def golden_view(golden):
    return {k: golden[k] for k in GOLDEN_KEYS}


def drift_report(expected, actual):
    want_tools = [t["tool"] for t in expected["trace"]]
    got_tools = [t["tool"] for t in actual["trace"]]
    for i, (want, got) in enumerate(zip(want_tools, got_tools)):
        if want != got:
            return {"first_difference_step": i, "expected_tool": want,
                    "actual_tool": got}
    if len(want_tools) != len(got_tools):
        return {"first_difference_step": min(len(want_tools),
                                             len(got_tools)),
                "expected_tool": "end or more steps",
                "actual_tool": "length differs"}
    return {"first_difference_step": None}


def evaluate():
    goldens = load("golden_trajectories.json")
    exact = 0
    for golden in goldens:
        if replay(golden) == golden_view(golden):
            exact += 1
    g01 = goldens[0]
    drifted = replay(g01, {"budget_weight": 0.5})
    return {
        "goldens": len(goldens),
        "exact_replays": exact,
        "drift_case": g01["id"],
        "drift_report": drift_report(golden_view(g01), drifted),
        "drifted_score": drifted["score"],
        "golden_score": g01["score"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
