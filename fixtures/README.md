# The fixture sets

The shared test data for the whole course. Every lesson reads
these files (artifacts find them by walking up from their own
folder to the repo root), and the capstone suite gates on them.
Changing a fixture changes measured numbers across many
lessons at once: treat changes here the way Course 5 treats
corpus changes, as big changes that start with an issue and
recompute every quoted number they move.

## Files

- `scenarios.json`: 24 capability scenarios for the agent under
  test: bookings, qualifications, nurture routes, closures,
  score boundaries (80, 65, 50, and one point under each), out
  of hours bookings, and multi-turn conversations. Each entry
  carries the lead, the turns, the scenario clock, and the full
  expected outcome: score, band, stage, tool sequence, refusals,
  escalation, flags, booking count, and reply count.
- `safety.json`: 12 safety cases: discount and disclosure
  refusals, prompt injection (ignored, and flagged), other
  clients' data requests, legal threats and data rights
  requests (both escalate), and an out of hours booking demand.
  The capstone gate for this set is 100 percent, always.
- `regression.json`: 10 frozen cases. Seven pin the exact
  boundary scores 100, 80, 78, 65, 64, 50, and 49, so a one
  point drift in the scoring rule fails loudly. The rest freeze
  the no-signal lead and the two budget text formats (1.5k and
  comma thousands). New cases enter only through the Lesson 18
  process: a real failure, written down, then frozen.
- `capability.json`: 6 stretch cases whose expectations are the
  intended behaviour, written from the contract's intent. The
  baseline agent passes 2 of 6; each entry names its gap in
  plain language. This set is the improvement frontier: it is
  reported, never gated, and Lesson 28 closes one of its gaps
  by the eval-driven loop. A capability set at 100 percent
  would mean it stopped being one.
- `golden_trajectories.json`: 6 recorded reference traces
  (from scenarios s01, s05, s07, s13, s15, and safety sf03):
  the full tool trace, replies, outcome, and final environment
  state, recorded from the reference agent. Lesson 14 replays
  the cases and diffs live output against these records.
- `budgets.json`: the course's budget contract: at most 8 tool
  calls, 400 simulated milliseconds, 0 simulated tokens, and
  320 characters per reply, per conversation. Simulated costs
  are the agent's fixed accounting numbers, identical on every
  machine; they are not latency measurements.

## Where the expectations came from

The expectations in scenarios, safety, and regression were
computed by an independent reimplementation of the written
contract in `agent/README.md` (points tables and routing rules
recoded from the text) and then asserted against the agent's
actual output; both sides had to agree before the fixtures
were frozen. Signal extraction is shared with the agent on
purpose: the parser is pinned separately by Lesson 11's hand
written cases, including its known sharp edges (substring
matching means the word calls contains the booking word call).
