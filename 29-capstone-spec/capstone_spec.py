"""Lesson 29 artifact: the capstone spec, cross checked.

The capstone specification lives in capstone/gates.json next
to this file: the sets, the gates, and the eight mutants the
suite must catch. A spec that disagrees with the fixtures is
a plan to fail, so this artifact cross checks every count in
the spec against the fixture files as they actually are, and
every mutant configuration against the agent's real config
keys. If the spec and the course ever drift apart, this check
goes red before the capstone does.

Offline, standard library only. Run: python3 capstone_spec.py
"""

import json
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


def load_fixture(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def evaluate():
    with open(os.path.join(HERE, "capstone", "gates.json")) as f:
        spec = json.load(f)["capstone_suite"]
    actual = {
        "scenarios": len(load_fixture("scenarios.json")),
        "safety": len(load_fixture("safety.json")),
        "regression": len(load_fixture("regression.json")),
        "goldens": len(load_fixture("golden_trajectories.json")),
        "capability_reported_not_gated": len(load_fixture("capability.json")),
    }
    sets_match = all(spec["sets"][k] == v for k, v in actual.items())
    mutants = spec["mutants"]
    config_keys_ok = all(set(m["config"]) <= set(la.DEFAULT_CONFIG)
                         for m in mutants)
    return {
        "spec_sets": spec["sets"],
        "actual_sets": actual,
        "sets_match": sets_match,
        "gates_declared": len(spec["gates"]),
        "mutants_declared": len(mutants),
        "mutant_ids": [m["id"] for m in mutants],
        "mutant_config_keys_valid": config_keys_ok,
        "mutation_gate": spec["gates"]["mutation_score"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
