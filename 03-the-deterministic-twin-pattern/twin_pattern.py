"""Lesson 03 artifact: the deterministic twin pattern.

A twin is a stand-in for the real system that behaves
identically on identical inputs, so tests can be exact. The
pattern has three rules, each demonstrated here:

1. Fresh environment per case. Run every gated case twice, each
   time in a new Environment, and the traces must be byte
   identical: the determinism is in the setup, not luck.
2. Shared environments contaminate. Run two leads through one
   environment and the second lead's id, and the shared state,
   carry the first run's fingerprints.
3. The twin's inputs are explicit: lead, turns, and clock all
   arrive as data, so any case can be replayed from its
   fixture alone.

Offline, standard library only. Run: python3 twin_pattern.py
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


def run_in(env, case):
    return la.LeadAgent().run(env, case["lead"], case["turns"],
                              datetime.fromisoformat(case["now"]))


def evaluate():
    gated = load("scenarios.json") + load("safety.json") + load("regression.json")
    identical = 0
    for case in gated:
        first = run_in(la.Environment(), case)
        second = run_in(la.Environment(), case)
        if json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True):
            identical += 1
    by_id = {c["id"]: c for c in load("scenarios.json")}
    shared = la.Environment()
    run_in(shared, by_id["s01"])
    second_shared = run_in(shared, by_id["s11"])
    second_fresh = run_in(la.Environment(), by_id["s11"])
    return {
        "cases_replayed": len(gated),
        "byte_identical_replays": identical,
        "shared_env_second_lead_id": second_shared["lead_id"],
        "fresh_env_second_lead_id": second_fresh["lead_id"],
        "shared_env_records_after_two_cases": shared.snapshot()["crm_records"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
