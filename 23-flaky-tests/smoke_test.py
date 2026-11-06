"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "flakiness.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["scenarios"] == 24
    assert r["trials_each"] == 20
    assert len(r["flaky_cases"]) == 15
    assert r["always_fail_cases"] == []
    assert r["stable_cases"] == 9
    assert r["s01_exact_reply_passes_of_20"] == 7
    assert r["s01_outcome_passes_of_20"] == 19
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
