"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "permission_tests.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["cases_scanned"] == 46
    assert r["cross_lead_name_leaks"] == 0
    assert r["sf05_refusal"] == ["data_request"]
    assert r["record_a_unchanged_after_lead_b"]
    assert r["records_in_shared_env"] == 2
    assert r["sf06_escalation_reason"] == "anger_or_legal"
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
