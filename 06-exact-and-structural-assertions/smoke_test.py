"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "assertion_styles.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["outcome_survives_wording"]
    assert r["structural_survives_wording"]
    assert not r["exact_survives_wording"]
    assert not r["outcome_survives_boundary_shift"]
    assert r["structural_survives_boundary_shift"]
    assert not r["exact_survives_boundary_shift"]
    assert r["outcome_survives_shape_break"]
    assert not r["structural_survives_shape_break"]
    assert not r["exact_survives_shape_break"]
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
