"""Lesson 18 artifact: the regression suite and its rules.

A regression set is not a smaller scenario set. It is the
fossil record of behaviour you have decided never to lose:
boundary scores pinned exactly, formats that once broke,
cases that once failed in production or review. Its rules:

- Entries are added when behaviour is fixed or pinned, and
  almost never edited afterwards; editing a regression entry
  to match new behaviour is how suites learn to lie.
- It runs fast and gates everything: a regression failure
  stops the line, no discussion.
- It is judged at 100 percent. There is no passing grade
  below that; a 9 of 10 regression suite is a failing suite
  with good PR.

Here the set runs clean against the reference agent, then
against a mutant with a moved HOT threshold, which the suite
catches at r03, the 78 point boundary: four entries fail,
every one a score sitting just under the old HOT line.

Offline, standard library only. Run: python3 regression_suite.py
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


def run_set(cases, config=None):
    passed = []
    failed = []
    for case in cases:
        env = la.Environment()
        result = la.LeadAgent(config).run(
            env, case["lead"], case["turns"],
            datetime.fromisoformat(case["now"]))
        e = case["expect"]
        ok = (result["score"] == e["score"] and result["band"] == e["band"]
              and result["stage"] == e["stage"]
              and [t["tool"] for t in result["trace"]] == e["tools"])
        (passed if ok else failed).append(case["id"])
    return passed, failed


def evaluate():
    regression = load("regression.json")
    passed, failed = run_set(regression)
    m_passed, m_failed = run_set(regression, {"hot_threshold": 60})
    boundary = {c["id"]: c["expect"]["score"] for c in regression
                if c["type"].startswith("boundary-score")}
    return {
        "regression_cases": len(regression),
        "passed": len(passed),
        "failed": failed,
        "boundary_scores_pinned": boundary,
        "mutant_hot_threshold_60_passed": len(m_passed),
        "mutant_failed": m_failed,
        "mutant_first_failure": m_failed[0] if m_failed else None,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
