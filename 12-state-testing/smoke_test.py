"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "state_testing.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["scenarios_checked"] == 24
    assert r["state_mismatches"] == 0
    assert r["records_after_double_run"] == 1
    assert r["mutant_records_after_double_run"] == 2
    assert r["idempotent_same_lead_id"]
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
