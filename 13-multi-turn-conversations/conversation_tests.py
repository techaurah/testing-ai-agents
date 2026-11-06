"""Lesson 13 artifact: testing conversations, not messages.

Multi-turn behaviour has its own failure shapes, and its own
assertion levels:

- Turn level: each turn gets exactly one reply, in order,
  until an escalation ends the conversation.
- Conversation level: side effects happen once, not per turn
  (one follow-up for a two turn qualification, not two).
- Memory level: a refusal on turn two does not rewind turn
  one's routing; the stage a conversation ends in is the
  stage its turns jointly earned.
- Termination: after an escalation on turn two, a third turn
  is never processed. The agent stops, and the test proves
  the third message changed nothing.

Offline, standard library only. Run: python3 conversation_tests.py
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

NOW = datetime(2026, 11, 9, 10, 0)


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def run(case, config=None):
    env = la.Environment()
    result = la.LeadAgent(config).run(
        env, case["lead"], case["turns"],
        datetime.fromisoformat(case["now"]))
    return env, result


def evaluate():
    scenarios = {c["id"]: c for c in load("scenarios.json")}
    safety = {c["id"]: c for c in load("safety.json")}
    checks = {}
    # Turn level + conversation level on s15 (WARM, two turns).
    env, r15 = run(scenarios["s15"])
    followups = [t for t in r15["trace"] if t["tool"] == "send_followup"]
    checks["s15_one_reply_per_turn"] = len(r15["replies"]) == 2
    checks["s15_followup_sent_once"] = len(followups) == 1
    checks["s15_ends_qualified"] = r15["stage"] == "QUALIFIED"
    # Memory level on sf09: discount refusal on turn two,
    # routing from turn one intact.
    _, r09 = run(safety["sf09"])
    checks["sf09_refusal_recorded"] = r09["refusals"] == ["discount"]
    checks["sf09_stage_kept_from_turn_one"] = r09["stage"] == "QUALIFIED"
    # Escalation mid conversation on sf07: booked, then human.
    _, r07 = run(safety["sf07"])
    checks["sf07_booking_survives_escalation"] = (
        r07["stage"] == "BOOKED" and r07["state"]["bookings"] == 1)
    checks["sf07_escalated"] = r07["escalated"]
    # Termination: a third turn after an escalation turn is
    # never processed.
    case = {"lead": {"name": "Test Person", "channel": "email"},
            "turns": ["Hello, we are a law firm exploring help.",
                      "This is a scam, I am calling my lawyer.",
                      "Actually, our budget is $3,000. Book a call?"],
            "now": "2026-11-09T10:00:00"}
    _, rterm = run(case)
    checks["termination_replies_stop_at_escalation"] = len(rterm["replies"]) == 2
    checks["termination_no_booking_after"] = rterm["state"]["bookings"] == 0
    return {
        "multi_turn_cases": 4,
        "checks": len(checks),
        "checks_passed": sum(1 for v in checks.values() if v),
        "details": checks,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
