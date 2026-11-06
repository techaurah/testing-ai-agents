"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "ship_it.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["lesson_folders"] == 33
    assert r["incomplete_parts"] == []
    assert r["capstone_mutants"] == "8 of 8"
    assert r["capstone_goldens_exact"]
    assert r["demo_conversations"]["booking"]["stage"] == "BOOKED"
    assert r["demo_conversations"]["nurture"]["band"] == "NURTURE"
    assert r["demo_conversations"]["escalation"]["stage"] == "NEW"
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
