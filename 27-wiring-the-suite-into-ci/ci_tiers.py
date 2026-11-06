"""Lesson 27 artifact: tiered suites for CI.

One suite, three tiers, because CI time and merge risk are
both real:

- Smoke (every push): a handful of load bearing cases, two
  per gated set. Seconds. Catches a build that cannot run
  the agent at all.
- Core (every pull request): the full gated sets, scenarios,
  safety, regression. This is the merge gate.
- Full (nightly and on demand): core plus budgets, golden
  trajectories, and the capability report printed for humans
  (reported, never gated, per Lesson 20).

This artifact runs the tiers in process and reports their
shape, then proves the gate logic: the reference agent exits
0 on core; a degraded configuration (moved HOT threshold)
fails core and exits 1. The repository CI workflow in
.github/workflows/ci.yml wires the same tiers to real events.

Offline, standard library only. Run: python3 ci_tiers.py
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


def full_match(case, config=None):
    env = la.Environment()
    result = la.LeadAgent(config).run(
        env, case["lead"], case["turns"],
        datetime.fromisoformat(case["now"]))
    e = case["expect"]
    return (result["score"] == e["score"] and result["band"] == e["band"]
            and result["stage"] == e["stage"]
            and [t["tool"] for t in result["trace"]] == e["tools"]
            and result["refusals"] == e["refusals"]
            and result["escalated"] == e["escalated"])


def evaluate():
    sets = [load("scenarios.json"), load("safety.json"),
            load("regression.json")]
    smoke = [c for s in sets for c in s[:2]]
    core = [c for s in sets for c in s]
    smoke_passed = sum(1 for c in smoke if full_match(c))
    core_passed = sum(1 for c in core if full_match(c))
    degraded_passed = sum(1 for c in core
                          if full_match(c, {"hot_threshold": 60}))
    return {
        "smoke_cases": len(smoke),
        "smoke_passed_reference": smoke_passed,
        "core_cases": len(core),
        "core_passed_reference": core_passed,
        "reference_exit_code": 0 if core_passed == len(core) else 1,
        "core_passed_degraded": degraded_passed,
        "degraded_exit_code": 0 if degraded_passed == len(core) else 1,
        "full_tier_adds": ["budget checks on all gated cases",
                           "golden trajectory replay",
                           "capability report (not gated)"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
