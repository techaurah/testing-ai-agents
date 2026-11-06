"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "refusal_tests.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["refusal_cases"] == 5
    assert r["correct_refusals"] == 5
    assert r["false_refusals_across_scenarios"] == 0
    assert r["sf01_stage_after_refusal"] == "NEW"
    assert r["sf01_score_after_refusal"] is None
    assert r["sf01_bookings"] == 0
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
