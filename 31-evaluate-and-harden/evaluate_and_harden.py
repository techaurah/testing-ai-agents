"""Lesson 31 artifact: evaluate the capstone, then harden it.

Step one is the gate table: every gate declared in Lesson 29
checked against the Lesson 30 suite's measured results, pass
or fail printed with its number, nothing rounded.

Step two is the hardening argument, made with evidence. Run
the same eight mutants against the Lesson 05 style harness,
outcome assertions only (score, band, stage), and count the
kills. The mutants that survive it are not exotic: a dropped
follow-up, a leaked score, a duplicated CRM record. Each
survivor names the check the full suite carries that the
weak one lacks, which is the entire justification for the
full battery's size: every check in it is there because a
realistic defect walks past everything weaker.

Offline, standard library only. Run: python3 evaluate_and_harden.py
"""

import importlib.util
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

SUITE_PATH = os.path.join(ROOT, "30-build-the-capstone-suite",
                          "capstone_suite.py")
spec = importlib.util.spec_from_file_location("capstone_suite", SUITE_PATH)
suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suite)


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def outcome_only_kills(config):
    """Lesson 05 style: score, band, stage over the gated sets."""
    gated = (load("scenarios.json") + load("safety.json")
             + load("regression.json"))
    for case in gated:
        env = la.Environment()
        result = la.LeadAgent(config).run(
            env, case["lead"], case["turns"],
            datetime.fromisoformat(case["now"]))
        e = case["expect"]
        if (result["score"], result["band"], result["stage"]) != (
                e["score"], e["band"], e["stage"]):
            return True
    return False


def evaluate():
    scorecard = suite.evaluate()
    spec_gates = suite.gates_spec()["gates"]
    killed_full = int(scorecard["mutants_killed"].split(" ")[0])
    gate_table = {
        "scenarios_pass": scorecard["sets"]["scenarios"] == "24 of 24",
        "safety_pass": scorecard["sets"]["safety"] == "12 of 12",
        "regression_pass": scorecard["sets"]["regression"] == "10 of 10",
        "goldens_exact": scorecard["goldens_exact"],
        "budgets": not any(v == "budgets"
                           for v in scorecard["reference_failures"].values()),
        "idempotency": scorecard["idempotency"],
        "mutation_score": killed_full >= 7,
    }
    weak = {}
    weak_killed = 0
    for mid, info in scorecard["mutants"].items():
        config = next(m["config"] for m in suite.gates_spec()["mutants"]
                      if m["id"] == mid)
        kills = outcome_only_kills(config)
        weak[mid] = {"name": info["name"], "killed_by_outcome_only": kills,
                     "killed_by_full_suite": info["killed"],
                     "full_suite_first_check": info["first_failing_check"]}
        if kills:
            weak_killed += 1
    return {
        "gates_declared": len(spec_gates),
        "gate_table": gate_table,
        "gates_passing": sum(1 for v in gate_table.values() if v),
        "mutants_killed_full_suite": scorecard["mutants_killed"],
        "mutants_killed_outcome_only": f"{weak_killed} of 8",
        "mutant_comparison": weak,
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
