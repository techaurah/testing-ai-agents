"""Lesson 06 artifact: three assertion styles, two disturbances.

Styles, weakest to strongest coupling:
- Outcome: band and stage only. Survives almost everything,
  sees almost nothing.
- Structural: the result record's shape, the trace entries'
  keys, the CRM record's fields and types. Survives wording
  changes, catches contract drift.
- Exact: the whole result, byte for byte, replies included.
  Catches everything, breaks on a courtesy suffix.

Disturbances:
- Wording: a courtesy suffix appended to replies.
- Boundary: a one point threshold shift flipping s03's band.
- Shape: the tokens field dropped from trace entries, the
  kind of silent contract drift a refactor produces.

The measured table in the lesson text is this file's output:
which styles survive which disturbance, and which catch it.

Offline, standard library only. Run: python3 assertion_styles.py
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


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


def run(case, config=None):
    env = la.Environment()
    return la.LeadAgent(config).run(
        env, case["lead"], case["turns"],
        datetime.fromisoformat(case["now"]))


def outcome_ok(result, reference):
    return (result["band"] == reference["band"]
            and result["stage"] == reference["stage"])


def structural_ok(result, reference):
    if set(result) != set(reference):
        return False
    for entry, ref in zip(result["trace"], reference["trace"]):
        if set(entry) != set(ref):
            return False
        if not isinstance(entry["ms"], int) or not isinstance(entry["tokens"], int):
            return False
    return True


def exact_ok(result, reference):
    return json.dumps(result, sort_keys=True) == json.dumps(reference,
                                                            sort_keys=True)


def evaluate():
    scenarios = {c["id"]: c for c in load("scenarios.json")}
    case = scenarios["s03"]  # score exactly 80, the HOT boundary
    reference = run(case)
    wording = run(case)
    wording["replies"] = [r + " Thanks again." for r in wording["replies"]]
    boundary = run(case, {"hot_threshold": 81})
    shape = run(case)
    for entry in shape["trace"]:
        entry.pop("tokens", None)
    styles = {"outcome": outcome_ok, "structural": structural_ok,
              "exact": exact_ok}
    return {
        "case": "s03 (score 80, the HOT boundary)",
        "outcome_survives_wording": styles["outcome"](wording, reference),
        "structural_survives_wording": styles["structural"](wording, reference),
        "exact_survives_wording": styles["exact"](wording, reference),
        "outcome_survives_boundary_shift": styles["outcome"](boundary, reference),
        "structural_survives_boundary_shift": styles["structural"](boundary, reference),
        "exact_survives_boundary_shift": styles["exact"](boundary, reference),
        "outcome_survives_shape_break": styles["outcome"](shape, reference),
        "structural_survives_shape_break": styles["structural"](shape, reference),
        "exact_survives_shape_break": styles["exact"](shape, reference),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
