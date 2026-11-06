"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "conversation_tests.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["checks"] == 9
    assert r["checks_passed"] == 9
    assert r["details"]["s15_followup_sent_once"]
    assert r["details"]["sf09_stage_kept_from_turn_one"]
    assert r["details"]["termination_no_booking_after"]
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
