# Course design: Testing AI Agents

Written before the lessons, from the scan in RESEARCH.md (2026-11-06). This is the fixed spec the repo was built and verified against.

## Title and promise

**Testing AI Agents.** Learn to test agents the way they actually fail: nondeterministic outcomes, trajectories through tools with side effects, state that outlives the conversation, and inputs that attack the instructions. The course builds a complete deterministic first test suite for one small agent, on the Python standard library alone, and grades the capstone suite partly by mutation testing.

## Audience

Builders who have an agent, or are about to ship one, and whose current test strategy is trying it a few times and reading the replies. Course 1 graduates meeting their first production incident. Engineers inheriting someone else's agent and needing a safety net before they touch it. The tone is practical and plain; no statistics background is assumed, and the two statistical tools the course uses (pass rates and the Wilson interval) are built up from arithmetic.

## Prerequisites

- Python 3.11 or newer, standard library only for the whole core course.
- Course 1 (Agentic AI for Beginners) or equivalent experience building a simple agent.
- Helpful but not required: Course 3 (Build MCP Servers) for Lesson 26's tool boundary, and Course 5 (Agentic RAG) for its retrieval boundary. Both boundaries are taught self contained here and cross linked, not duplicated.

## The arc

Ten modules. Module 0 frames why agent testing is different and audits the agent's written contract. Module 1 builds the deterministic twin pattern and the scenario fixture format. Module 2 teaches assertion styles in increasing strength. Module 3 unit tests the parts: templates, tool contracts, parsers. Module 4 tests state and whole conversations, then freezes golden trajectories. Module 5 is the safety block: refusals, injection, permission boundaries. Module 6 separates regression from capability and teaches error analysis. Module 7 faces nondeterminism honestly, with a labelled seeded stand-in, pass@k and pass^k, flakiness classification, and run count arithmetic. Module 8 makes budgets tests and tests the MCP and retrieval boundaries. Module 9 wires the suite into CI tiers, runs one eval driven development loop, and lands the capstone.

## The agent under test and the fixture design

`agent/lead_agent.py` is a deterministic, rule based twin of a lead qualification agent in the LeadPipe pattern: it extracts signals from a message (budget, timeline, intents, hostile patterns), scores the lead on a published points table, routes by band (HOT 80+, WARM 65+, NURTURE 50+, LOW below 50), books only inside working hours, refuses discount, score disclosure, and other leads' data requests, and escalates anger, legal threats, and data rights requests to a human. Eight tools with fixed simulated costs. All behaviour is driven by a config dict whose overrides exist so the capstone can build mutants. `agent/README.md` is its written contract; Lesson 02 audits the code against it. `agent/standin.py` is a clearly labelled nondeterminism stand-in used only in Module 7: seeded threshold jitter, phrasing swaps, and courtesy suffixes, reproducible from seeds.

Fixtures live in `fixtures/` as first class top level data (the Course 5 corpus lesson applied): 24 scenarios, 12 safety cases, 10 regression cases with boundary scores pinned exactly (100, 80, 78, 65, 64, 50, 49), 6 capability cases whose expectations are intended behaviour the twin does not have yet (each naming its gap), 6 golden trajectories recorded from reviewed source cases, and a budgets contract. Expectations for the gated sets were verified at build time by an independent reimplementation of the scoring contract. Capability baselines are recorded in the fixture itself: 2 of 6 pass at baseline (cap04, cap05).

## Lesson map: 33 lessons, 10 modules

### Module 0: Start here
- 00 Course setup: what you need, and how this course works
- 01 Why agent testing is different
- 02 Meet the agent under test: the contract audit

### Module 1: The agent and its twins
- 03 The deterministic twin pattern
- 04 Anatomy of a scenario
- 05 Your first scenario test: the mini harness

### Module 2: Assertion styles
- 06 Exact and structural assertions
- 07 Property based assertions
- 08 Trajectory assertions

### Module 3: Unit tests for agent parts
- 09 Prompts and templates as data
- 10 Tool contracts
- 11 Parsers and extractors

### Module 4: State and conversations
- 12 State testing: the CRM is the outcome
- 13 Multi-turn conversations
- 14 Golden trajectories

### Module 5: Safety suites
- 15 Refusal tests
- 16 Injection tests
- 17 Permission boundaries

### Module 6: Regression and analysis
- 18 Regression suites
- 19 Error analysis: from red to taxonomy
- 20 Capability vs regression suites

### Module 7: Nondeterminism and statistics
- 21 The seeded stand-in
- 22 pass@k and pass^k
- 23 Flaky tests: find them, classify them
- 24 How many runs are enough

### Module 8: Budgets and boundaries
- 25 Budgets as tests
- 26 Testing at the boundaries: MCP tools and retrieval

### Module 9: Workflow and capstone
- 27 Wiring the suite into CI
- 28 Eval driven development
- 29 Capstone spec: the suite and its gates, fixed in advance
- 30 Build the capstone suite
- 31 Evaluate and harden
- 32 Ship it: document, demo, and showcase your suite

## Capstone spec (fixed in Lesson 29, built in 30, graded in 31)

The capstone is a complete test suite for the bundled agent, graded against gates declared in `29-capstone-spec/capstone/gates.json` before the suite is written:

- Scenarios 24 of 24, safety 12 of 12, regression 10 of 10, on the full outcome (score, band, stage, tool sequence, refusals, escalations, flags, state).
- Golden trajectories 6 of 6 exact, budgets within `fixtures/budgets.json` on every gated case, idempotency verified (double run leaves one CRM record).
- Mutation gate: at least 7 of 8 declared mutants killed. The eight mutants are config level defects: lowered HOT threshold, injection guard off, escalation off, booking hours guard off, score disclosure on, idempotent writes off, WARM followup off, halved budget weight.
- Reference build results (measured, and regenerated by Lesson 32's audit): all gated sets pass in full, goldens exact, and 8 of 8 mutants killed. The hardening comparison in Lesson 31 measures the Lesson 05 outcome only harness against the same mutants: it kills 4 of 8, and the four survivors (injection guard, disclosure, idempotency, followup) are the argument for the full battery.

## Visuals

Eight branded SVG diagrams in the Course 1 style family (white background, navy #0B1F4A titles, cyan #0891B2 accents, cream and sky boxes): course map, why agent testing is different, the twin pattern, assertion styles, trajectory rules, the safety suites, pass@k versus pass^k, and the capstone flow. Generated by `assets/visuals/generate_visuals.py`; indexed in `assets/visuals/VISUALS.md`.

## Offline versus install-required split

The entire core course, all 33 lessons including the capstone, runs offline on the standard library. Real frameworks (promptfoo, DeepEval, RAGAS, LangSmith, Braintrust) are named in RESEARCH.md and in Lesson 26's further reading with dates, as optional extras for learners who want them; no lesson requires installing anything, and no framework API detail is load bearing anywhere in the course.
