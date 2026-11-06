"""Lesson 10 artifact: tool contracts, schemas in and out.

Agents act through tools; the contract of each tool is the
shape of its arguments and its result, plus what its errors
look like. This lesson writes the eight contracts down as
data and validates every recorded call in every gated case
against them: argument keys exactly as contracted, result
types as contracted, simulated costs equal to the published
cost table (a drifted cost is a drifted budget).

Error paths get the same treatment: an empty message parses
to an all-empty signal set rather than crashing, and an
unknown channel scores with the contract's default points
instead of raising.

Offline, standard library only. Run: python3 tool_contracts.py
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

CONTRACTS = {
    "capture_lead": {"args": {"channel"}, "result": str},
    "score_lead": {"args": {"channel"}, "result": int},
    "crm_write": {"args": {"stage"}, "result": str},
    "calendar_check": {"args": {"when"}, "result": bool},
    "book_appointment": {"args": {"when"}, "result": str},
    "send_followup": {"args": {"kind"}, "result": str},
    "send_reply": {"args": {"kind"}, "result": str},
    "escalate_to_human": {"args": {"reason"}, "result": str},
}


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def evaluate():
    gated = load("scenarios.json") + load("safety.json") + load("regression.json")
    checked = 0
    violations = 0
    for case in gated:
        env = la.Environment()
        result = la.LeadAgent().run(
            env, case["lead"], case["turns"],
            datetime.fromisoformat(case["now"]))
        for entry in result["trace"]:
            checked += 1
            contract = CONTRACTS[entry["tool"]]
            if set(entry["args"]) != contract["args"]:
                violations += 1
            if not isinstance(entry["result"], contract["result"]):
                violations += 1
            if entry["ms"] != la.TOOL_COSTS[entry["tool"]]["ms"]:
                violations += 1
            if entry["tokens"] != la.TOOL_COSTS[entry["tool"]]["tokens"]:
                violations += 1
    empty = la.extract_signals("")
    unknown_channel_score = la.score_lead(1200, 20, "smoke-signal",
                                          False, False)
    known_channel_score = la.score_lead(1200, 20, "email", False, False)
    return {
        "tools_contracted": len(CONTRACTS),
        "trace_entries_checked": checked,
        "contract_violations": violations,
        "empty_message_signals": {k: empty[k] for k in
                                  ("budget", "timeline_days",
                                   "booking_intent", "anger")},
        "unknown_channel_points": unknown_channel_score - (35 + 18 + 2),
        "unknown_vs_email_delta": known_channel_score - unknown_channel_score,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
