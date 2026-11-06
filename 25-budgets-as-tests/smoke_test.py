"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "budget_tests.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["cases_measured"] == 46
    assert r["budget_breaches_reference"] == 0
    assert r["observed_max"]["tool_calls"] == 8
    assert r["observed_max"]["sim_ms"] == 305
    assert r["observed_max"]["max_reply_chars"] == 138
    assert r["most_expensive_case_by_calls"] == "sf07"
    assert r["retry_storm_calls"] == 10
    assert r["retry_storm_ms"] == 590
    assert r["retry_storm_outcome_unchanged"]
    assert r["retry_storm_breaks_budget"]
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
