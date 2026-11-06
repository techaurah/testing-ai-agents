"""Lesson 25 artifact: budgets as tests.

Correctness suites ask whether the agent did the right thing.
Budget tests ask what it cost: tool calls per conversation,
simulated latency, simulated tokens, reply length. The budget
contract lives in fixtures/budgets.json, and every gated case
is measured against it.

Then the failure this lesson exists for: a retry storm. A
plausible agent variant that retries a failed booking four
times produces a perfectly correct outcome, booked, right
stage, right words, at more tool calls and more simulated
milliseconds than the budget allows (the exact measured
figures are printed below). Every correctness assertion
passes it. Only the budget catches it. That is why budgets
are tests and not dashboards: the gate has to fire before
the cost ships.

Offline, standard library only. Run: python3 budget_tests.py
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


def measure(result):
    return {
        "tool_calls": len(result["trace"]),
        "sim_ms": sum(t["ms"] for t in result["trace"]),
        "sim_tokens": sum(t["tokens"] for t in result["trace"]),
        "max_reply_chars": max((len(r) for r in result["replies"]),
                               default=0),
    }


def evaluate():
    budgets = load("budgets.json")
    gated = load("scenarios.json") + load("safety.json") + load("regression.json")
    observed = {"tool_calls": 0, "sim_ms": 0, "sim_tokens": 0,
                "max_reply_chars": 0}
    worst_case = {"tool_calls": None, "sim_ms": None}
    breaches = 0
    for case in gated:
        env = la.Environment()
        result = la.LeadAgent().run(
            env, case["lead"], case["turns"],
            datetime.fromisoformat(case["now"]))
        m = measure(result)
        for key in observed:
            if m[key] > observed[key]:
                observed[key] = m[key]
                if key in worst_case:
                    worst_case[key] = case["id"]
        if (m["tool_calls"] > budgets["max_tool_calls_per_conversation"]
                or m["sim_ms"] > budgets["max_simulated_ms_per_conversation"]
                or m["sim_tokens"] > budgets["max_simulated_tokens_per_conversation"]
                or m["max_reply_chars"] > budgets["max_reply_chars"]):
            breaches += 1
    # Retry storm variant: s01 with four extra booking attempts
    # inserted before the write, outcome unchanged.
    case = {c["id"]: c for c in load("scenarios.json")}["s01"]
    env = la.Environment()
    result = la.LeadAgent().run(env, case["lead"], case["turns"],
                                datetime.fromisoformat(case["now"]))
    storm = [dict(t) for t in result["trace"]]
    at = next(i for i, t in enumerate(storm)
              if t["tool"] == "book_appointment")
    retry = dict(storm[at])
    storm = storm[:at] + [dict(retry) for _ in range(4)] + storm[at:]
    storm_result = dict(result)
    storm_result["trace"] = storm
    storm_m = measure(storm_result)
    storm_outcome_same = (storm_result["stage"] == result["stage"]
                          and storm_result["band"] == result["band"])
    return {
        "budgets": budgets,
        "cases_measured": len(gated),
        "budget_breaches_reference": breaches,
        "observed_max": observed,
        "most_expensive_case_by_calls": worst_case["tool_calls"],
        "most_expensive_case_by_ms": worst_case["sim_ms"],
        "retry_storm_calls": storm_m["tool_calls"],
        "retry_storm_ms": storm_m["sim_ms"],
        "retry_storm_outcome_unchanged": storm_outcome_same,
        "retry_storm_breaks_budget": (
            storm_m["tool_calls"] > budgets["max_tool_calls_per_conversation"]
            or storm_m["sim_ms"] > budgets["max_simulated_ms_per_conversation"]),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
