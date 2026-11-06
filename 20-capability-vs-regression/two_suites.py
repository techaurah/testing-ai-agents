"""Lesson 20 artifact: capability suites vs regression suites.

Anthropic's eval vocabulary splits suites by intent, and the
split decides how a red result is handled:

- Regression suites protect behaviour you already have. They
  gate merges and must sit at 100 percent.
- Capability suites measure behaviour you are trying to gain.
  They start red, often stay partly red for months, and must
  never gate: gating on them teaches teams to delete hard
  cases or lower the bar quietly.

This course's capability set names six intended behaviours
the twin does not have yet. The report below is the honest
shape of a healthy project: gated sets at 100 percent, the
capability set at its real number, each failure still naming
the gap it tracks.

Offline, standard library only. Run: python3 two_suites.py
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


def full_match(case):
    env = la.Environment()
    result = la.LeadAgent().run(env, case["lead"], case["turns"],
                                datetime.fromisoformat(case["now"]))
    e = case["expect"]
    return (result["score"] == e["score"] and result["band"] == e["band"]
            and result["stage"] == e["stage"]
            and [t["tool"] for t in result["trace"]] == e["tools"])


def capability_match(case):
    """Capability entries assert on a named subset of fields
    (assert_on), not on the full gated expectation shape."""
    env = la.Environment()
    result = la.LeadAgent().run(env, case["lead"], case["turns"],
                                datetime.fromisoformat(case["now"]))
    values = {"band": result["band"], "stage": result["stage"],
              "bookings": result["state"]["bookings"]}
    return all(values[f] == case["expect"][f] for f in case["assert_on"])


def evaluate():
    gated_total = 0
    gated_passed = 0
    for name in ("scenarios.json", "safety.json", "regression.json"):
        cases = load(name)
        gated_total += len(cases)
        gated_passed += sum(1 for c in cases if full_match(c))
    capability = load("capability.json")
    cap_passed = []
    cap_failed = {}
    for case in capability:
        if capability_match(case):
            cap_passed.append(case["id"])
        else:
            cap_failed[case["id"]] = case["gap"]
    return {
        "gated_cases": gated_total,
        "gated_passed": gated_passed,
        "gated_rate": round(gated_passed / gated_total, 4),
        "capability_cases": len(capability),
        "capability_passed": cap_passed,
        "capability_rate": round(len(cap_passed) / len(capability), 4),
        "open_gaps": cap_failed,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
