"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "check_environment.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["python_ok"]
    assert r["tools_in_agent"] == 8
    assert r["scenarios"] == 24
    assert r["safety_cases"] == 12
    assert r["regression_cases"] == 10
    assert r["gated_cases"] == 46
    assert r["golden_trajectories"] == 6
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
