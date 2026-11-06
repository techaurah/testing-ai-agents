"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "why_different.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["same_message_both_cases"]
    assert r["monday_stage"] == "BOOKED"
    assert r["saturday_stage"] == "QUALIFIED"
    assert r["state_keys_changed_by_one_run"] == 3
    assert r["distinct_tool_paths_across_scenarios"] == 5
    assert r["deterministic_trace_variants_in_5_runs"] == 1
    assert r["standin_passes_s01_of_30"] == 28
    assert r["standin_passes_s03_of_30"] == 19
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
