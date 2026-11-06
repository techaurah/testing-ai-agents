"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "sample_sizes.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["wilson_20_of_20"] == (0.8389, 1.0)
    assert r["wilson_50_of_50"] == (0.9286, 1.0)
    assert r["wilson_100_of_100"] == (0.963, 1.0)
    assert r["wilson_47_of_50"] == (0.8378, 0.9794)
    assert r["runs_to_catch_5pct_at_95"] == 59
    assert r["runs_to_catch_10pct_at_95"] == 29
    assert r["runs_to_catch_1pct_at_95"] == 299
    assert r["chance_5pct_defect_survives_20_runs"] == 0.3585
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
