"""Lesson 32 artifact: ship it, the pre publish audit.

The last lesson is a checklist that runs. Before this course
(or any agent suite) ships, the audit confirms:

- Every lesson folder on the map carries its four parts:
  README.md, exercise.md, a runnable artifact, solution.
- The capstone scorecard the README quotes is regenerated
  here from the suite itself, so the numbers in the docs are
  the numbers the code produces today, not the numbers from
  the day the docs were written.
- Three demo conversations run end to end for the showcase:
  one booking, one nurture, one escalation, printed in the
  showcase file's shape.

If any row is red, the course is not done, whatever the
calendar says. That is the whole lesson, and it is also the
job, on every project after this one.

Offline, standard library only. Run: python3 ship_it.py
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


def evaluate():
    folders = sorted(d for d in os.listdir(ROOT)
                     if len(d) > 3 and d[:2].isdigit()
                     and os.path.isdir(os.path.join(ROOT, d)))
    incomplete = []
    for folder in folders:
        base = os.path.join(ROOT, folder)
        py = [f for f in os.listdir(base) if f.endswith(".py")
              and f != "smoke_test.py"]
        for needed in ("README.md", "exercise.md",
                       os.path.join("solution", "SOLUTION.md"),
                       "smoke_test.py"):
            if not os.path.isfile(os.path.join(base, needed)):
                incomplete.append(f"{folder}:{needed}")
        if not py:
            incomplete.append(f"{folder}:artifact")
    scorecard = suite.evaluate()
    scenarios = {c["id"]: c for c in load("scenarios.json")}
    safety = {c["id"]: c for c in load("safety.json")}
    demos = {}
    for label, case in (("booking", scenarios["s01"]),
                        ("nurture", scenarios["s07"]),
                        ("escalation", safety["sf06"])):
        env = la.Environment()
        result = la.LeadAgent().run(
            env, case["lead"], case["turns"],
            datetime.fromisoformat(case["now"]))
        demos[label] = {"band": result["band"], "stage": result["stage"],
                        "tools": len(result["trace"])}
    showcase_row = (f"| testing-ai-agents capstone | "
                    f"{scorecard['sets']['scenarios']} scenarios, "
                    f"{scorecard['sets']['safety']} safety, "
                    f"mutants {scorecard['mutants_killed']} |")
    return {
        "lesson_folders": len(folders),
        "incomplete_parts": incomplete,
        "capstone_sets": scorecard["sets"],
        "capstone_mutants": scorecard["mutants_killed"],
        "capstone_goldens_exact": scorecard["goldens_exact"],
        "demo_conversations": demos,
        "showcase_row": showcase_row,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
