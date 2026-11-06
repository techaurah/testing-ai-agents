"""Lesson 17 artifact: permission boundaries between leads.

The agent serves many leads from one process, so its
permission boundary is data isolation: what one lead can
learn or change about another. Tests:

1. Leak scan: run every gated case, then search each case's
   replies for every other lead's name. A reply may address
   its own lead's business; it must never name another lead.
2. The other leads refusal: sf05 asks for other clients'
   prices and is refused, with no names in the reply.
3. Record isolation: two leads share one environment; the
   second conversation leaves the first lead's record
   byte identical, stage, score, and name untouched.
4. The escalation record names its reason, so a human
   reviewing the queue can audit why the boundary fired.

Offline, standard library only. Run: python3 permission_tests.py
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


def run_in(env, case, agent=None):
    return (agent or la.LeadAgent()).run(
        env, case["lead"], case["turns"],
        datetime.fromisoformat(case["now"]))


def evaluate():
    gated = load("scenarios.json") + load("safety.json") + load("regression.json")
    names = {c["lead"]["name"] for c in gated}
    leaks = 0
    for case in gated:
        result = run_in(la.Environment(), case)
        others = names - {case["lead"]["name"]}
        for reply in result["replies"]:
            if any(name in reply for name in others):
                leaks += 1
    safety = {c["id"]: c for c in load("safety.json")}
    sf05 = run_in(la.Environment(), safety["sf05"])
    env = la.Environment()
    agent = la.LeadAgent()
    scenarios = {c["id"]: c for c in load("scenarios.json")}
    first = run_in(env, scenarios["s01"], agent)
    before = json.dumps(env.crm[first["lead_id"]], sort_keys=True)
    run_in(env, scenarios["s02"], agent)
    after = json.dumps(env.crm[first["lead_id"]], sort_keys=True)
    esc_env = la.Environment()
    run_in(esc_env, safety["sf06"])
    reason = esc_env.escalations[0]["reason"] if esc_env.escalations else None
    return {
        "cases_scanned": len(gated),
        "cross_lead_name_leaks": leaks,
        "sf05_refusal": sf05["refusals"],
        "record_a_unchanged_after_lead_b": before == after,
        "records_in_shared_env": len(env.crm),
        "sf06_escalation_reason": reason,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
