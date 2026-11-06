"""Lesson 11 artifact: the parser, pinned by hand written cases.

Signal extraction is the agent's front door, and the fixtures
share it with the agent, so this lesson pins it separately
with cases written by hand from the contract, including its
known sharp edges:

- Budget formats that must work: $2,400 / 1.5k / 2000 dollars.
- A range is read as its first figure (pinned behaviour).
- A budget in words is invisible (the cap01 gap, pinned here
  so the capability failure is never a surprise).
- The first number in a message wins, even when it is not the
  budget: a message mentioning 3 stores before its $900 budget
  parses a budget of 3. Pinned, named, and priced in: fixture
  messages are written to put the budget first.
- Substring matching: the word calls contains the booking
  word call, so it signals booking intent.
- Hostile shapes: empty, emoji only, and a 10,000 character
  message with the budget at the end, all parse without error.

Offline, standard library only. Run: python3 parser_tests.py
"""

import os
import sys

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

CASES = [
    ("comma budget", "Our budget is $2,400 for this.", "budget", 2400),
    ("k format", "Our budget is 1.5k for this.", "budget", 1500),
    ("dollars word", "We have 2000 dollars ready.", "budget", 2000),
    ("range reads first figure", "Budget is between 1800 and 2200 dollars.",
     "budget", 1800),
    ("budget in words is invisible", "Our budget is two thousand dollars.",
     "budget", None),
    ("first number wins", "We run 3 stores and our budget is $900.",
     "budget", 3),
    ("within days", "We need it within 10 days.", "timeline_days", 10),
    ("this week", "We need it this week.", "timeline_days", 7),
    ("asap", "We need it asap.", "timeline_days", 3),
    ("substring call inside calls", "We miss calls after hours.",
     "booking_intent", True),
    ("empty message", "", "budget", None),
    ("no money context, no budget", "We are 5 people in the office.",
     "budget", None),
]


def evaluate():
    results = {}
    passed = 0
    for name, message, field, expected in CASES:
        got = la.extract_signals(message)[field]
        results[name] = got
        if got == expected:
            passed += 1
    long_message = ("x" * 9990) + " budget is $700"
    long_budget = la.extract_signals(long_message)["budget"]
    if long_budget == 700:
        passed += 1
    emoji = la.extract_signals("Hello 🌿🌿🌿")
    emoji_ok = emoji["budget"] is None and not emoji["booking_intent"]
    if emoji_ok:
        passed += 1
    total = len(CASES) + 2
    return {
        "cases": total,
        "passed": passed,
        "long_message_budget": long_budget,
        "emoji_parses_clean": emoji_ok,
        "pinned_sharp_edges": ["first number wins",
                               "budget in words is invisible",
                               "substring call inside calls"],
        "range_reads": results["range reads first figure"],
        "stray_number_reads": results["first number wins"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
