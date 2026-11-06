"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "contract_audit.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["clauses_checked"] == 6
    assert r["clauses_passing"] == 6
    assert r["cases_audited"] == 46
    assert r["tools_seen"] == 8
    assert r["forbidden_term_hits"] == 0
    assert r["out_of_hours_bookings"] == 0
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
