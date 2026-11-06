"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "scenario_anatomy.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["gated_entries"] == 46
    assert r["capability_entries"] == 6
    assert r["schema_errors"] == 0
    assert r["duplicate_ids"] == 0
    assert r["distinct_types"] == 25
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
