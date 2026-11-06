"""Lesson 01 artifact: four ways agent testing is different,
demonstrated on the agent under test.

1. Inputs classical tests ignore decide outcomes: the same
   message books or does not book depending on the scenario
   clock (s01 on Monday morning vs s13 on Saturday).
2. The system has side effects: one run changes the world
   (CRM records, bookings, outbox, escalations), so the outcome
   lives in state, not just in the return value.
3. Many paths reach success: the 24 scenarios exercise several
   distinct tool trajectories, and a suite must grade the path
   as well as the ending.
4. Near a decision boundary, small wobbles flip outcomes: the
   seeded stand-in passes the boundary case s03 in only 19 of
   30 trials. Even the comfortable case s01 drops 2 of 30, not
   to threshold jitter (its score clears every edge the jitter
   can reach) but to phrasing swaps hiding its booking phrase.

Offline, standard library only. Run: python3 why_different.py
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
import standin


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def run_case(case, config=None):
    env = la.Environment()
    result = la.LeadAgent(config).run(
        env, case["lead"], case["turns"],
        datetime.fromisoformat(case["now"]))
    return env, result


def evaluate():
    scenarios = load("scenarios.json")
    by_id = {c["id"]: c for c in scenarios}
    # 1. Same words, same signals, different clock.
    _, mon = run_case(by_id["s01"])
    _, sat = run_case(by_id["s13"])
    same_input = by_id["s01"]["turns"] == by_id["s13"]["turns"]
    # 2. Side effects of a single run.
    env, _ = run_case(by_id["s01"])
    snap = env.snapshot()
    state_keys_changed = sum(1 for k in ("crm_records", "bookings",
                                         "outbox", "escalations")
                             if snap[k] > 0)
    # 3. Distinct trajectories across the scenario set.
    paths = set()
    for case in scenarios:
        _, result = run_case(case)
        paths.add(tuple(t["tool"] for t in result["trace"]))
    # 4. Boundary wobble under the stand-in.
    s03 = by_id["s03"]
    s01 = by_id["s01"]
    s03_pass = sum(1 for seed in range(30)
                   if standin.outcome_matches(
                       standin.run_trial(s03, seed)["result"], s03["expect"]))
    s01_pass = sum(1 for seed in range(30)
                   if standin.outcome_matches(
                       standin.run_trial(s01, seed)["result"], s01["expect"]))
    # Deterministic core: identical inputs, identical traces.
    traces = set()
    for _ in range(5):
        _, result = run_case(by_id["s01"])
        traces.add(json.dumps(result["trace"], sort_keys=True))
    return {
        "same_message_both_cases": same_input,
        "monday_stage": mon["stage"],
        "saturday_stage": sat["stage"],
        "state_keys_changed_by_one_run": state_keys_changed,
        "distinct_tool_paths_across_scenarios": len(paths),
        "deterministic_trace_variants_in_5_runs": len(traces),
        "standin_passes_s01_of_30": s01_pass,
        "standin_passes_s03_of_30": s03_pass,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
