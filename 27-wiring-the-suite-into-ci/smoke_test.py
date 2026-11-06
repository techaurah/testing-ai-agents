"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "ci_tiers.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["smoke_cases"] == 6
    assert r["smoke_passed_reference"] == 6
    assert r["core_cases"] == 46
    assert r["core_passed_reference"] == 46
    assert r["reference_exit_code"] == 0
    assert r["core_passed_degraded"] == 33
    assert r["degraded_exit_code"] == 1
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
