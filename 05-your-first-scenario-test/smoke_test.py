"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "mini_harness.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["scenarios"] == 24
    assert r["outcome_passed"] == 24
    assert r["mutant_outcome_passed"] == 24
    assert r["warm_cases"] == 6
    assert r["warm_cases_mutant_outcome_passed"] == 6
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
