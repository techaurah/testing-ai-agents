"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "twin_pattern.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["cases_replayed"] == 46
    assert r["byte_identical_replays"] == 46
    assert r["shared_env_second_lead_id"] == "LD-002"
    assert r["fresh_env_second_lead_id"] == "LD-001"
    assert r["shared_env_records_after_two_cases"] == 2
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
