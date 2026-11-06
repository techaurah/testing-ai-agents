"""Lesson 28 artifact: the eval driven development loop.

The loop, in the open: pick one failing capability case,
write down the behaviour it names, make the smallest change
that earns it, then prove the gated sets did not move.

The case is cap01: a budget written in words ("two thousand
dollars") loses to the first stray digit in the message (the
7 from "within 7 days"), a sharp edge of the kind Lesson 11
pins. The fix is deliberately small: a word number table that
wins when the author wrote the amount in words, patched in
here as a wrapper around the agent's extractor, the way you
would patch the parser itself in the real code.

Measured result of one loop iteration: the capability set
goes from 2 of 6 to 3 of 6, and the gated sets stay at 46 of
46. Five gaps remain open and named; the loop repeats when
someone chooses the next one, not before.

Offline, standard library only. Run: python3 edd_loop.py
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

WORD_NUMBERS = {"two thousand": 2000, "three thousand": 3000,
                "one thousand": 1000, "five hundred": 500}
_original_extract = la.extract_signals


def patched_extract(message):
    signals = _original_extract(message)
    lowered = message.lower()
    for phrase, value in WORD_NUMBERS.items():
        if phrase in lowered:
            signals["budget"] = value
            break
    return signals


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def full_match(case):
    env = la.Environment()
    result = la.LeadAgent().run(env, case["lead"], case["turns"],
                                datetime.fromisoformat(case["now"]))
    e = case["expect"]
    return (result["score"] == e["score"] and result["band"] == e["band"]
            and result["stage"] == e["stage"]
            and [t["tool"] for t in result["trace"]] == e["tools"])


def capability_match(case):
    """Capability entries assert on a named subset of fields."""
    env = la.Environment()
    result = la.LeadAgent().run(env, case["lead"], case["turns"],
                                datetime.fromisoformat(case["now"]))
    values = {"band": result["band"], "stage": result["stage"],
              "bookings": result["state"]["bookings"]}
    return all(values[f] == case["expect"][f] for f in case["assert_on"])


def run_all():
    gated = (load("scenarios.json") + load("safety.json")
             + load("regression.json"))
    capability = load("capability.json")
    return (sum(1 for c in gated if full_match(c)), len(gated),
            sum(1 for c in capability if capability_match(c)),
            len(capability))


def evaluate():
    gated_before, gated_total, cap_before, cap_total = run_all()
    la.extract_signals = patched_extract
    try:
        gated_after, _, cap_after, _ = run_all()
        cap01 = {c["id"]: c for c in load("capability.json")}["cap01"]
        cap01_fixed = capability_match(cap01)
    finally:
        la.extract_signals = _original_extract
    return {
        "target_case": "cap01",
        "capability_before": f"{cap_before} of {cap_total}",
        "capability_after": f"{cap_after} of {cap_total}",
        "cap01_fixed_by_patch": cap01_fixed,
        "gated_before": f"{gated_before} of {gated_total}",
        "gated_after": f"{gated_after} of {gated_total}",
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
