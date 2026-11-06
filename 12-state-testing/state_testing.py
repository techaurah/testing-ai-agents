"""Lesson 12 artifact: state testing, the CRM is the outcome.

Anthropic's agent evaluation guidance makes the point this
lesson operationalises: grade the outcome in the world, not
the agent's narration of it. The agent's world here is the
fake environment, so state tests assert on it directly:

- After every scenario, the CRM holds exactly one record, in
  the stage the outcome claims, with the score and band the
  outcome claims (narration and world agree).
- Bookings in the calendar equal the fixture's expected count.
- Idempotency: capturing and running the same lead twice in
  one environment still leaves exactly one CRM record.

The idempotency mutant (duplicate writes allowed) shows the
state test catching what every reply based check misses: its
replies are word perfect while the CRM quietly doubles.

Offline, standard library only. Run: python3 state_testing.py
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


def evaluate():
    scenarios = load("scenarios.json")
    mismatches = 0
    final_stages = set()
    for case in scenarios:
        env = la.Environment()
        result = la.LeadAgent().run(
            env, case["lead"], case["turns"],
            datetime.fromisoformat(case["now"]))
        record = env.crm[result["lead_id"]]
        final_stages.add(record["stage"])
        if not (len(env.crm) == 1
                and record["stage"] == result["stage"] == case["expect"]["stage"]
                and record["score"] == result["score"]
                and record["band"] == result["band"]
                and len(env.calendar) == case["expect"]["bookings"]):
            mismatches += 1
    case = scenarios[0]
    env = la.Environment()
    agent = la.LeadAgent()
    first = agent.run(env, case["lead"], case["turns"],
                      datetime.fromisoformat(case["now"]))
    second = agent.run(env, case["lead"], case["turns"],
                       datetime.fromisoformat(case["now"]))
    env_mut = la.Environment()
    mutant = la.LeadAgent({"idempotent_writes": False})
    mutant.run(env_mut, case["lead"], case["turns"],
               datetime.fromisoformat(case["now"]))
    mutant.run(env_mut, case["lead"], case["turns"],
               datetime.fromisoformat(case["now"]))
    return {
        "scenarios_checked": len(scenarios),
        "state_mismatches": mismatches,
        "final_stages_seen": sorted(final_stages),
        "idempotent_same_lead_id": first["lead_id"] == second["lead_id"],
        "records_after_double_run": len(env.crm),
        "mutant_records_after_double_run": len(env_mut.crm),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
