"""Lesson 00 artifact: environment, agent, and fixture check.

Verifies the Python version, finds the agent under test and the
fixture sets by walking up from this file, and reports the shape
of everything the course will test. Offline, standard library
only. Run: python3 check_environment.py
"""

import json
import os
import sys


def find_root():
    here = os.path.dirname(os.path.abspath(__file__))
    cur = here
    while True:
        if os.path.isfile(os.path.join(cur, "agent", "lead_agent.py")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise FileNotFoundError("repo root (agent/) not found above " + here)
        cur = parent


ROOT = find_root()
sys.path.insert(0, os.path.join(ROOT, "agent"))
import lead_agent as la


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def evaluate():
    scenarios = load("scenarios.json")
    safety = load("safety.json")
    regression = load("regression.json")
    capability = load("capability.json")
    goldens = load("golden_trajectories.json")
    return {
        "python_ok": sys.version_info >= (3, 11),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "agent_found": True,
        "tools_in_agent": len(la.TOOL_COSTS),
        "stages": la.STAGES,
        "scenarios": len(scenarios),
        "safety_cases": len(safety),
        "regression_cases": len(regression),
        "capability_cases": len(capability),
        "golden_trajectories": len(goldens),
        "gated_cases": len(scenarios) + len(safety) + len(regression),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
