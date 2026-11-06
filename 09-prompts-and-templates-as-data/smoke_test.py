"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "template_tests.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["reply_kinds_exercised"] == 10
    assert r["replies_checked"] == 50
    assert r["placeholder_residue"] == 0
    assert r["forbidden_term_hits"] == 0
    assert r["overlong_replies"] == 0
    assert r["polite_openings"] == 50
    assert r["mutant_forbidden_term_hits"] == 40
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
