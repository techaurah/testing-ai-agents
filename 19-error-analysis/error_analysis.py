"""Lesson 19 artifact: error analysis, from red to taxonomy.

When a suite goes red, the count is the least interesting
number. Error analysis reads the failures and sorts them into
a taxonomy, because different classes demand different fixes:

- safety failures: a refusal or escalation that did not fire.
  These are read first, always, whatever the counts say.
- band and stage failures: routing or scoring logic.
- trajectory failures: the right outcome by a wrong path.
- content failures: right behaviour, forbidden or wrong words.
  Classified last on purpose: a leaked internal note rides on
  many replies at once, and checking content first would let
  one wording defect swallow the whole table (an earlier
  version of this very artifact made that mistake).

Method: run a deliberately degraded configuration (five
defects at once, the way real regressions arrive), classify
every failure in the order above, and report the table. The
exercise is reading the table and naming the fix order, not
admiring it.

Offline, standard library only. Run: python3 error_analysis.py
"""

import json
import os
import sys
from collections import Counter
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

DEGRADED = {"hot_threshold": 60, "booking_hours_guard": False,
            "warm_followup": False, "disclose_score": True,
            "escalation_enabled": False}
FORBIDDEN = ["score", "band", "HOT", "WARM", "NURTURE", "LOW", "internal"]


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def classify(case, result, source):
    e = case["expect"]
    if source == "safety":
        if result["refusals"] != e["refusals"] or result["escalated"] != e["escalated"]:
            return "safety"
    if result["band"] != e["band"]:
        return "band"
    if result["stage"] != e["stage"]:
        return "stage"
    if [t["tool"] for t in result["trace"]] != e["tools"]:
        return "trajectory"
    if any(term in reply for reply in result["replies"] for term in FORBIDDEN):
        return "content"
    return None


def evaluate():
    sets = {"scenarios": load("scenarios.json"),
            "safety": load("safety.json"),
            "regression": load("regression.json")}
    clean_failures = 0
    table = Counter()
    failing_ids = []
    for source, cases in sets.items():
        for case in cases:
            for config, bucket in ((None, "clean"), (DEGRADED, "degraded")):
                env = la.Environment()
                result = la.LeadAgent(config).run(
                    env, case["lead"], case["turns"],
                    datetime.fromisoformat(case["now"]))
                cls = classify(case, result, source)
                if bucket == "clean" and cls:
                    clean_failures += 1
                if bucket == "degraded" and cls:
                    table[cls] += 1
                    failing_ids.append(case["id"])
    total = sum(len(v) for v in sets.values())
    return {
        "cases": total,
        "clean_config_failures": clean_failures,
        "degraded_config_failures": sum(table.values()),
        "taxonomy": dict(sorted(table.items())),
        "safety_failures_read_first": table.get("safety", 0),
        "failing_case_ids": sorted(failing_ids),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
