"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "error_analysis.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["cases"] == 46
    assert r["clean_config_failures"] == 0
    assert r["degraded_config_failures"] == 42
    assert r["taxonomy"]["safety"] == 3
    assert r["taxonomy"]["band"] == 13
    assert r["taxonomy"]["stage"] == 3
    assert r["taxonomy"]["content"] == 23
    assert r["safety_failures_read_first"] == 3
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
