"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "tool_contracts.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r["tools_contracted"] == 8
    assert r["trace_entries_checked"] == 223
    assert r["contract_violations"] == 0
    assert r["unknown_channel_points"] == 6
    assert r["unknown_vs_email_delta"] == 4
    print("smoke ok:", r)


if __name__ == "__main__":
    main()
