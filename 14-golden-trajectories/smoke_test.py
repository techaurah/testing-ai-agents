"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "golden_trajectories.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["goldens"] == 6
    assert r["exact_replays"] == 6
    assert r["drift_report"]["first_difference_step"] == 2
    assert r["drift_report"]["expected_tool"] == "calendar_check"
    assert r["drift_report"]["actual_tool"] == "crm_write"
    assert r["drifted_score"] == 70
    assert r["golden_score"] == 93
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
