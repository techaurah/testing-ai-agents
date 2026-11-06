"""Lesson 08 artifact: trajectory assertions.

An agent's outcome can be right while its path is wrong: it
can book before checking the calendar, write the CRM record
before scoring, or act twice. Trajectory assertions grade the
recorded path. Five rules, checked over every gated case:

T1 capture_lead is always the first tool call.
T2 score_lead precedes every routing side effect (crm_write,
   book_appointment, send_followup).
T3 book_appointment never appears without an earlier
   calendar_check in the same conversation.
T4 book_appointment appears at most once per conversation.
T5 escalate_to_human, when present, is followed only by
   send_reply: automation stops after escalation.

Then three hand built bad traces, each violating exactly one
rule, prove the checker can see what it claims to see.

Offline, standard library only. Run: python3 trajectory_assertions.py
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

ROUTING_EFFECTS = ["crm_write", "book_appointment", "send_followup"]


def check_trace(tools):
    """Return the list of rule ids this tool sequence violates."""
    bad = []
    if not tools or tools[0] != "capture_lead":
        bad.append("T1")
    if "score_lead" in tools:
        score_at = tools.index("score_lead")
        if any(t in tools[:score_at] for t in ROUTING_EFFECTS):
            bad.append("T2")
    if "book_appointment" in tools:
        book_at = tools.index("book_appointment")
        if "calendar_check" not in tools[:book_at]:
            bad.append("T3")
        if tools.count("book_appointment") > 1:
            bad.append("T4")
    if "escalate_to_human" in tools:
        esc_at = tools.index("escalate_to_human")
        if any(t != "send_reply" for t in tools[esc_at + 1:]):
            bad.append("T5")
    return bad


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def evaluate():
    gated = load("scenarios.json") + load("safety.json") + load("regression.json")
    violations = 0
    for case in gated:
        env = la.Environment()
        result = la.LeadAgent().run(
            env, case["lead"], case["turns"],
            datetime.fromisoformat(case["now"]))
        violations += len(check_trace([t["tool"] for t in result["trace"]]))
    bad_traces = {
        "book_without_check": ["capture_lead", "score_lead",
                               "book_appointment", "crm_write", "send_reply"],
        "duplicate_booking": ["capture_lead", "score_lead", "calendar_check",
                              "book_appointment", "book_appointment",
                              "crm_write", "send_reply"],
        "act_after_escalation": ["capture_lead", "escalate_to_human",
                                 "crm_write", "send_reply"],
    }
    caught = {name: check_trace(tools) for name, tools in bad_traces.items()}
    return {
        "rules": 5,
        "cases_checked": len(gated),
        "violations_reference": violations,
        "crafted_bad_traces": len(bad_traces),
        "crafted_caught": sum(1 for v in caught.values() if v),
        "crafted_verdicts": caught,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
