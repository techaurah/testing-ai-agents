# Repository tools

- `validate_course.py`: checks every JSON file in the repo
  (parses; fixture entries in the gated sets carry id, type,
  lead, turns, now, and a complete expectation; capability
  entries carry assert_on and a named gap; the capstone spec
  carries sets, gates, and mutants). CI runs it on every push.
- `check_links.py`: checks that relative Markdown links resolve
  to files on disk. Run it before a release; external URLs are
  reviewed by humans, not by this script.

Run either from anywhere: `python3 tools/validate_course.py`.
