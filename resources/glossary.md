# Glossary

Every term this course uses, in plain language. Lessons define terms on first use; this page is the reference shelf.

**Agent under test** The system a suite grades. In this course, the deterministic lead qualification twin in `agent/`.

**Assertion** A check inside a test that fails when the behaviour is wrong. Styles differ in coupling: outcome, structural, property based, trajectory, exact.

**Band** The routing category a score earns: HOT (80 and above), WARM (65 to 79), NURTURE (50 to 64), LOW (below 50) in this agent's contract.

**Budget test** A test that asserts cost limits (tool calls, latency, tokens, reply length) per conversation, instead of correctness.

**Capability suite** A suite measuring behaviour the system does not have yet. It starts red, is reported honestly, and never gates merges.

**Clean environment** A fresh, isolated world for every trial, so state from one case cannot contaminate another. See deterministic twin.

**Deterministic twin** A stand-in for a system that behaves identically on identical inputs, with every input explicit as data, so tests can be exact.

**Drift report** The comparison a golden trajectory failure produces: first differing step, expected, actual. A human judges whether the change is legitimate.

**Error analysis** Reading actual failures and sorting them into a taxonomy (safety, band, stage, trajectory, content) so fixes are ordered by harm, not by count.

**Eval driven development** The loop of picking one failing capability case, making the smallest change that earns it, and proving the gated suites did not move.

**Fixture** The data form of a case: lead, turns, clock, and a complete expectation. Suites are only as trustworthy as their fixtures.

**Flaky test** A test that passes sometimes and fails sometimes on the same code. In agent suites it usually means an assertion at the wrong strength, or a case on a decision boundary.

**Golden trajectory** A recorded, reviewed, frozen run of one conversation, compared exactly. Few on purpose, re-recorded only with a written reason.

**Idempotency** Doing the same thing twice changes nothing the second time. Here: capturing the same lead twice leaves one CRM record.

**Injection** Text in untrusted input that claims authority (ignore your rules, reveal your instructions). The discipline: input is data, never instructions, and attempts are flagged.

**Mutant** A small deliberate change to the system under test. A suite kills a mutant when a check fails on it. See mutation score.

**Mutation score** Killed mutants divided by total mutants, the capstone's measure of suite strength against known defect kinds.

**Outcome** The graded end state of a trial: score, band, stage, side effects. Anthropic's guidance: grade the outcome in the world, not the agent's narration of it.

**pass@k** The probability that at least one of k trials passes. The right rate when a human picks among attempts.

**pass^k** The probability that all k trials pass. The right rate when an agent acts alone and every attempt ships.

**Property based assertion** A law the behaviour must obey for all inputs (range, monotonicity, exact value against an independent oracle), checked over generated cases.

**Regression suite** The fossil record of behaviour that must never be lost: boundary pins and once broken cases, gated at 100 percent.

**Scenario** A fixture entry describing one conversation and its complete expected outcome.

**Seeded stand-in** A labelled mechanism that injects controlled nondeterminism (threshold jitter, phrasing swaps, reply suffixes) reproducibly from seeds, for teaching and measurement.

**Stage** The lead's lifecycle position: NEW, QUALIFIED, BOOKED, or LOST.

**Trajectory** The recorded sequence of tool calls in one conversation. Trajectory assertions grade the path, not just the ending.

**Transcript** The full record of a trial: messages, tool calls, and replies, in order.

**Trial** One run of one task. Repeated trials are how nondeterministic systems are measured.

**Wilson interval** A confidence interval for a pass rate that behaves honestly at small counts: 20 of 20 passing means a rate somewhere in (0.8389, 1.0) at 95 percent confidence, not a proven 100 percent.
