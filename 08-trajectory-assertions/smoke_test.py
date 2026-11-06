"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "trajectory_assertions.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["rules"] == 5
    assert r["cases_checked"] == 46
    assert r["violations_reference"] == 0
    assert r["crafted_caught"] == 3
    assert r["crafted_verdicts"]["book_without_check"] == ["T3"]
    assert r["crafted_verdicts"]["duplicate_booking"] == ["T4"]
    assert r["crafted_verdicts"]["act_after_escalation"] == ["T5"]
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
