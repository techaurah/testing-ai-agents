"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "capstone_spec.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["sets_match"]
    assert r["gates_declared"] == 7
    assert r["mutants_declared"] == 8
    assert r["mutant_config_keys_valid"]
    assert r["mutation_gate"] == "at least 7 of 8 mutants killed"
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
