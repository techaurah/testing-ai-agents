"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "regression_suite.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["regression_cases"] == 10
    assert r["passed"] == 10
    assert r["failed"] == []
    assert r["boundary_scores_pinned"] == {"r01": 100, "r02": 80, "r03": 78, "r04": 65, "r05": 64, "r06": 50, "r07": 49}
    assert r["mutant_hot_threshold_60_passed"] == 6
    assert r["mutant_failed"] == ["r03", "r04", "r05", "r10"]
    assert r["mutant_first_failure"] == "r03"
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
