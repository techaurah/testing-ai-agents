"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "capstone_suite.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["reference_failures"] == {}
    assert r["sets"]["scenarios"] == "24 of 24"
    assert r["sets"]["safety"] == "12 of 12"
    assert r["sets"]["regression"] == "10 of 10"
    assert r["gated_cases"] == 46
    assert r["goldens_exact"]
    assert r["idempotency"]
    assert r["mutants_killed"] == "8 of 8"
    assert r["mutants"]["m5"]["first_failing_check"] == "reply_content"
    assert r["mutants"]["m6"]["first_failing_check"] == "duplicate_records"
    assert r["mutants"]["m7"]["first_failing_check"] == "tool_sequence"
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
