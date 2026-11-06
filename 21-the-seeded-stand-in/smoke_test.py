"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "standin_lab.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["trials_per_case"] == 30
    assert r["pass_counts"]["s01"] == 28
    assert r["pass_counts"]["s03"] == 19
    assert r["pass_counts"]["s05"] == 19
    assert r["pass_counts"]["s07"] == 12
    assert r["pass_counts"]["s10"] == 14
    assert r["stable_cases"] == []
    assert r["same_seed_reproduces_exactly"]
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
