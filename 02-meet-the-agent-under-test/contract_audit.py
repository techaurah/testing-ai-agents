"""Lesson 02 artifact: audit the agent against its contract.

The contract lives in agent/README.md. This audit turns its
clauses into probes and runs them over every gated fixture
(scenarios, safety, regression):

- The band thresholds reproduce the regression set's pinned
  boundary scores (100, 80, 78, 65, 64, 50, 49).
- Every tool the contract names is exercised somewhere, and no
  unnamed tool ever appears.
- Every stage the agent reaches is a contract stage.
- No reply ever contains an internal term (score, band, or a
  band name) the contract forbids disclosing.
- No booking ever lands outside working hours.

Offline, standard library only. Run: python3 contract_audit.py
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

FORBIDDEN = ["score", "band", "HOT", "WARM", "NURTURE", "LOW", "internal"]


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def run_case(case):
    env = la.Environment()
    result = la.LeadAgent().run(
        env, case["lead"], case["turns"],
        datetime.fromisoformat(case["now"]))
    return env, result


def evaluate():
    gated = load("scenarios.json") + load("safety.json") + load("regression.json")
    boundary_ids = ["r01", "r02", "r03", "r04", "r05", "r06", "r07"]
    regression = {c["id"]: c for c in load("regression.json")}
    boundary_ok = True
    for rid in boundary_ids:
        case = regression[rid]
        _, result = run_case(case)
        if (result["score"], result["band"]) != (case["expect"]["score"],
                                                 case["expect"]["band"]):
            boundary_ok = False
    tools_seen = set()
    stages_seen = set()
    forbidden_hits = 0
    out_of_hours_bookings = 0
    for case in gated:
        _, result = run_case(case)
        tools_seen.update(t["tool"] for t in result["trace"])
        stages_seen.add(result["stage"])
        for reply in result["replies"]:
            if any(term in reply for term in FORBIDDEN):
                forbidden_hits += 1
        now = datetime.fromisoformat(case["now"])
        if result["state"]["bookings"] and not la.in_working_hours(now):
            out_of_hours_bookings += 1
    clauses = {
        "boundary_scores_reproduce": boundary_ok,
        "all_contract_tools_exercised": tools_seen == set(la.TOOL_COSTS),
        "no_unnamed_tools": tools_seen <= set(la.TOOL_COSTS),
        "stages_within_contract": stages_seen <= set(la.STAGES),
        "no_internal_terms_in_replies": forbidden_hits == 0,
        "no_out_of_hours_bookings": out_of_hours_bookings == 0,
    }
    return {
        "clauses_checked": len(clauses),
        "clauses_passing": sum(1 for v in clauses.values() if v),
        "tools_seen": len(tools_seen),
        "stages_seen": sorted(stages_seen),
        "forbidden_term_hits": forbidden_hits,
        "out_of_hours_bookings": out_of_hours_bookings,
        "cases_audited": len(gated),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
