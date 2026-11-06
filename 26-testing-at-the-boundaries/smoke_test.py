"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "boundary_tests.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["mcp_tools_listed"] == 1
    assert r["grid_cases"] == 25
    assert r["grid_mismatches"] == 0
    assert r["error_codes"] == [-32601, -32602, -32602]
    assert r["retrieval_queries"] == 6
    assert r["recall_at_3"] == 0.8333
    assert r["missed_queries"] == ["q6"]
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
