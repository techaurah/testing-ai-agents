"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "edd_loop.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["target_case"] == "cap01"
    assert r["capability_before"] == "2 of 6"
    assert r["capability_after"] == "3 of 6"
    assert r["cap01_fixed_by_patch"]
    assert r["gated_before"] == "46 of 46"
    assert r["gated_after"] == "46 of 46"
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
