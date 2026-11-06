"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "pass_rates.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["trials_per_case"] == 40
    assert r["s01"]["p_empirical"] == 0.825
    assert r["s01"]["rates"]["k=5"]["pass_at_k"] == 0.9998
    assert r["s01"]["rates"]["k=5"]["pass_pow_k"] == 0.3822
    assert r["s03"]["p_empirical"] == 0.475
    assert r["s03"]["rates"]["k=3"]["pass_at_k"] == 0.8553
    assert r["s03"]["rates"]["k=3"]["pass_pow_k"] == 0.1072
    assert r["s05"]["p_empirical"] == 0.475
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
