# AGENTS.md

Conventions for AI assistants working in this repository. Human contributors should read CONTRIBUTING.md; this file states the same rules in machine-checkable form.

## Repository shape

- Lessons live in root folders named `NN-kebab-lesson-name`, numbered 00 to 32, matching the lessons table in README.md exactly. Never rename a lesson folder without updating README.md, llms.txt, and PROGRESS.md in the same change.
- Each lesson folder contains: `README.md` (the lesson), one runnable artifact (a plain Python harness, checker, or lab), `exercise.md`, `smoke_test.py`, and `solution/` with the worked solution.
- The agent under test lives in `agent/`: `lead_agent.py` (the deterministic twin), `standin.py` (the labelled nondeterminism stand-in, used only in Module 7), and `README.md` (its written contract). Lesson artifacts find the repo root by walking up from their own folder; never copy the agent or the fixtures into a lesson.
- The fixtures live in `fixtures/`: scenarios.json (24), safety.json (12), regression.json (10), capability.json (6), golden_trajectories.json (6), budgets.json. The capstone spec lives in `29-capstone-spec/capstone/gates.json`.
- Root files: README.md (landing page), llms.txt (course index for AI assistants), PROGRESS.md (learner checklist), DESIGN.md (the design this repo was built to), RESEARCH.md (the competitor scan), resources/, showcase/, translations/, assets/, tools/.

## Writing rules

- Plain language, short sentences. Define every term on first use or ensure it exists in resources/glossary.md.
- No em dashes anywhere, in prose or code comments. Use commas, colons, or full stops instead.
- No invented statistics, benchmark claims, or market sizes. A number is allowed only as the measured output of the lesson's own code on the bundled agent and fixtures, or as a sourced fact with its date in RESEARCH.md.
- Never claim the seeded stand-in predicts a real model's behaviour. It is a teaching stand-in with chosen mechanisms and must be labelled as one wherever its numbers appear.
- Do not promise certificates. The course's completion artifact is the capstone suite in the showcase.
- Lessons never sell a service. The only vendor presence is the published by line and the standard footer in the root README.

## Code rules

- Every Python artifact on the canonical path runs on the standard library (Python 3.11 or newer), offline, with no credentials. Framework code (promptfoo, DeepEval, RAGAS, LangSmith) appears only inside clearly marked extras that no smoke test and no gate depends on, with its check date stated.
- Every lesson artifact exposes `evaluate()` returning the numbers its lesson text quotes, and `smoke_test.py` asserts them. If code and text disagree, the code's output is the truth and the text gets fixed.
- Every JSON file must parse and pass tools/validate_course.py; gated fixture entries carry the nine expectation fields, capability entries carry assert_on and gap, and the capstone spec carries sets, gates, and mutants. CI runs it.
- All example data is fictional. The leads and conversations are invented for this course; no real business, customer, or patient data anywhere, including in exercises and solutions.
- The agent's config keys are the mutation surface: capstone mutants are config dicts, and a new config key must be added to the capstone spec checks before it is used as one.

## Change rules

- Small fixes may go straight to a pull request. New lessons, rewritten lessons, and new translation languages start with an issue (the two-tier rule in CONTRIBUTING.md).
- If lesson titles change, update README.md, llms.txt, and PROGRESS.md together; the three must never disagree.
- If the agent, fixtures, or gates change, every lesson's quoted numbers must be recomputed and updated in the same change; CI smoke tests will catch most drift.
- Showcase rows are added by learners via PR, one row per learner, format in showcase/README.md.
