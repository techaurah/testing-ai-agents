"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "property_assertions.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["generated_leads"] == 400
    assert r["invariant_violations_reference"] == 0
    assert r["monotonicity_pairs_checked"] == 400
    assert r["monotonicity_violations"] == 0
    assert r["unique_lead_ids"] == 400
    assert r["mutant_exact_value_mismatches"] == 400
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
