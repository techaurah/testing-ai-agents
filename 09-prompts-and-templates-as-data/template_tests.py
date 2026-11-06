"""Lesson 09 artifact: prompts and templates as data.

In a model based agent the prompt is data with behaviour
attached; in this twin the reply templates are that data.
Either way they can be tested as data, without judging a
single conversation:

- Every template kind the agent can emit is exercised by some
  fixture case (ten kinds, collected by driving the agent).
- No rendered reply keeps a placeholder brace.
- No reply contains an internal term: the words the contract
  forbids disclosing (score, band, band names, internal).
- Every reply fits the budget contract's character limit.
- Every reply opens politely: with thanks, or with the
  escalation apology.

Then the disclosure mutant renders its replies with an
internal note attached, and the forbidden term check counts
exactly what it catches.

Offline, standard library only. Run: python3 template_tests.py
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


def collect(config=None):
    gated = load("scenarios.json") + load("safety.json") + load("regression.json")
    # Reply kinds pair with replies in order, per case.
    pairs = []
    for case in gated:
        env = la.Environment()
        result = la.LeadAgent(config).run(
            env, case["lead"], case["turns"],
            datetime.fromisoformat(case["now"]))
        reply_kinds = [e["args"]["kind"] for e in result["trace"]
                       if e["tool"] == "send_reply"]
        pairs.extend(zip(reply_kinds, result["replies"]))
    return pairs


def evaluate():
    budgets = load("budgets.json")
    pairs = collect()
    kinds = sorted({k for k, _ in pairs})
    residue = sum(1 for _, r in pairs if "{" in r or "}" in r)
    forbidden = sum(1 for _, r in pairs
                    if any(term in r for term in FORBIDDEN))
    overlong = sum(1 for _, r in pairs
                   if len(r) > budgets["max_reply_chars"])
    openings = sum(1 for _, r in pairs
                   if r.startswith("Thanks") or r.startswith("I am sorry"))
    mutant_pairs = collect({"disclose_score": True})
    mutant_forbidden = sum(1 for _, r in mutant_pairs
                           if any(term in r for term in FORBIDDEN))
    return {
        "reply_kinds_exercised": len(kinds),
        "kinds": kinds,
        "replies_checked": len(pairs),
        "placeholder_residue": residue,
        "forbidden_term_hits": forbidden,
        "overlong_replies": overlong,
        "polite_openings": openings,
        "mutant_forbidden_term_hits": mutant_forbidden,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
