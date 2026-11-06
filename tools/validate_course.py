#!/usr/bin/env python3
"""Validate every JSON file in this repo.

Checks:
- Any .json file must parse as JSON.
- Fixture entries in the gated sets (scenarios, safety,
  regression: recognised as a list of dicts carrying "lead",
  "turns", "now", and "expect") must carry an id and a type,
  and the expectation must carry the nine outcome fields:
  score, band, stage, tools, refusals, escalated, flags,
  bookings, replies.
- Capability entries (recognised by an "assert_on" field)
  must name the fields they assert on and carry a "gap"
  explaining the missing behaviour.
- The capstone spec (recognised by a "capstone_suite" key)
  must carry the three sections Lesson 29 fixes in advance:
  sets, gates, and mutants.
Exits nonzero on any failure, so CI can gate on it.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPECT_FIELDS = ["score", "band", "stage", "tools", "refusals",
                 "escalated", "flags", "bookings", "replies"]
SPEC_SECTIONS = ["sets", "gates", "mutants"]


def iter_json():
    for dirpath, _dirs, files in os.walk(ROOT):
        if ".git" in dirpath:
            continue
        for name in sorted(files):
            if name.endswith(".json"):
                yield os.path.join(dirpath, name)


def check(data):
    errors = []
    if isinstance(data, list) and data and isinstance(data[0], dict):
        for entry in data:
            if not isinstance(entry, dict):
                continue
            label = entry.get("id", "<no id>")
            if ("expect" in entry and "lead" in entry and "turns" in entry
                    and "assert_on" not in entry):
                for field in ["id", "type", "lead", "turns", "now", "expect"]:
                    if field not in entry:
                        errors.append(f"{label}: missing field {field}")
                for field in EXPECT_FIELDS:
                    if field not in entry.get("expect", {}):
                        errors.append(f"{label}: expect missing {field}")
            if "assert_on" in entry:
                if not entry["assert_on"]:
                    errors.append(f"{label}: capability entry asserts nothing")
                if not entry.get("gap"):
                    errors.append(f"{label}: capability entry names no gap")
    if isinstance(data, dict) and "capstone_suite" in data:
        suite = data["capstone_suite"]
        for section in SPEC_SECTIONS:
            if section not in suite:
                errors.append(f"capstone_suite missing section: {section}")
    return errors


def main():
    total, bad = 0, 0
    for path in iter_json():
        total += 1
        rel = os.path.relpath(path, ROOT)
        try:
            with open(path) as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            bad += 1
            print(f"FAIL {rel}: does not parse: {exc}")
            continue
        errors = check(data)
        if errors:
            bad += 1
            for e in errors:
                print(f"FAIL {rel}: {e}")
        else:
            print(f"OK   {rel}")
    print(f"\n{total} JSON files checked, {bad} failing")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
