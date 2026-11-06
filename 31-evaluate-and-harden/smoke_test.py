"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "evaluate_and_harden.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["gates_declared"] == 7
    assert r["gates_passing"] == 7
    assert all(r["gate_table"].values())
    assert r["mutants_killed_full_suite"] == "8 of 8"
    assert r["mutants_killed_outcome_only"] == "4 of 8"
    assert not r["mutant_comparison"]["m2"]["killed_by_outcome_only"]
    assert not r["mutant_comparison"]["m5"]["killed_by_outcome_only"]
    assert not r["mutant_comparison"]["m6"]["killed_by_outcome_only"]
    assert not r["mutant_comparison"]["m7"]["killed_by_outcome_only"]
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
