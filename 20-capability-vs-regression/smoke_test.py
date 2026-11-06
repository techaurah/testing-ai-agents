"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "two_suites.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["gated_cases"] == 46
    assert r["gated_passed"] == 46
    assert r["gated_rate"] == 1.0
    assert r["capability_cases"] == 6
    assert r["capability_passed"] == ["cap04", "cap05"]
    assert r["capability_rate"] == 0.3333
    assert len(r["open_gaps"]) == 4
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
