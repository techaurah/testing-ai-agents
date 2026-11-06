"""Lesson 04 artifact: audit the scenario fixtures themselves.

A scenario is data with a contract of its own: an id, a type, a
lead, turns, a clock, and an expectation complete enough that a
runner needs no other knowledge. This audit validates every
fixture entry against that schema, counts the coverage by
type, and checks the invariants that make a set trustworthy:
unique ids, expectations whose tool sequence starts with
capture_lead, and capability entries that each name their gap.

Offline, standard library only. Run: python3 scenario_anatomy.py
"""

import json
import os
from collections import Counter

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
EXPECT_KEYS = {"score", "band", "stage", "tools", "refusals", "escalated",
               "flags", "bookings", "replies"}


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def evaluate():
    errors = []
    types = Counter()
    ids = []
    gated = []
    for name in ("scenarios.json", "safety.json", "regression.json"):
        for entry in load(name):
            gated.append(entry)
            ids.append(entry["id"])
            types[entry["type"]] += 1
            for key in ("id", "type", "lead", "turns", "now", "expect"):
                if key not in entry:
                    errors.append(f"{entry.get('id')}: missing {key}")
            if set(entry.get("expect", {})) != EXPECT_KEYS:
                errors.append(f"{entry['id']}: expect keys incomplete")
            if entry["expect"]["tools"][0] != "capture_lead":
                errors.append(f"{entry['id']}: trace does not start with capture")
            if not entry["turns"]:
                errors.append(f"{entry['id']}: no turns")
    capability = load("capability.json")
    for entry in capability:
        if not entry.get("gap"):
            errors.append(f"{entry['id']}: capability entry names no gap")
        if not entry.get("assert_on"):
            errors.append(f"{entry['id']}: capability entry asserts nothing")
    return {
        "gated_entries": len(gated),
        "capability_entries": len(capability),
        "distinct_types": len(types),
        "types": dict(sorted(types.items())),
        "duplicate_ids": len(ids) - len(set(ids)),
        "schema_errors": len(errors),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
