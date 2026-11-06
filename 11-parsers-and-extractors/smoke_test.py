"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "parser_tests.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["cases"] == 14
    assert r["passed"] == 14
    assert r["long_message_budget"] == 700
    assert r["emoji_parses_clean"]
    assert r["range_reads"] == 1800
    assert r["stray_number_reads"] == 3
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
