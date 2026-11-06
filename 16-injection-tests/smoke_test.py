"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "injection_tests.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["injection_cases"] == 3
    assert r["flagged"] == 3
    assert r["controls_matching_band_and_stage"] == 3
    assert r["controls_matching_score"] == 2
    assert r["sf04_actual_score"] == 93
    assert r["sf04_control_score"] == 80
    assert r["sf04_stage"] == "BOOKED"
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
