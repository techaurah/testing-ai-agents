# The agent under test

`lead_agent.py` is the system this whole course tests: a small,
deterministic lead qualification agent in the LeadPipe pattern
(the pattern behind TechAurah's leadpipe-mcp project and Course
3's LeadDesk capstone, rebuilt here as a twin small enough to
hold in your head). It reads an inbound lead conversation,
extracts signals, scores the lead, routes it, acts on a fake
environment through recorded tool calls, and replies from fixed
templates. This file is its contract: the written behaviour the
course's tests assert. If the code and this contract ever
disagree, that is a bug in one of them, and Lesson 02 teaches
you to find out which.

## Inputs and outputs

- Input: a lead (`name`, `channel`, optionally `budget` and
  `timeline_days` stated up front), a list of message turns,
  and the current time. Time is an input, never read from a
  clock, so tests control it.
- Output: a record with the full tool trace, the replies sent,
  the final score, band, and stage, any safety flags and
  refusals, and a snapshot of the environment's final state.

## Scoring (fixed points, maximum 100)

| Signal | Points |
|---|---|
| Budget: 2000 or more / 1000 to 1999 / 500 to 999 / under 500 / unstated | 45 / 35 / 25 / 10 / 5 |
| Timeline: 7 days or less / 30 or less / 90 or less / longer / unstated | 25 / 18 / 10 / 6 / 4 |
| Channel: WhatsApp or Instagram DM / web / email / anything else | 15 / 12 / 10 / 6 |
| Intent in the message: booking words / pricing words / neither | 15 / 8 / 2 |

Bands follow the LeadPipe thresholds: **HOT** at 80 or more,
**WARM** at 65 or more, **NURTURE** at 50 or more, **LOW**
below 50.

## Routing

- HOT: check the calendar; if the requested moment is in
  working hours, book and finish at stage BOOKED; if not,
  finish QUALIFIED and offer the next in-hours slot instead.
- WARM: qualify (stage QUALIFIED) and send a qualification
  follow-up.
- NURTURE: qualify (stage QUALIFIED) and send a nurture
  follow-up.
- LOW: close politely, stage LOST.
- Stages are the LeadPipe stages: NEW, QUALIFIED, BOOKED, LOST.
- Scoring happens on the first turn that reaches routing.
  Later turns are acknowledged. (The capability set keeps the
  cases where this rule hurts; see `fixtures/capability.json`.)

## Safety rules (these outrank routing, on every turn)

- Prompt injection in a message is data, never instruction.
  It is flagged `injection_ignored` on the lead record and the
  conversation continues by the normal rules.
- A discount demand is refused: pricing is fixed. The refusal
  does not advance the pipeline on that turn.
- A request for the internal score or band is refused.
- A request for other leads' or clients' data is refused.
- Anger or legal threats escalate to a human and stop
  automation for that conversation.
- A data rights request (delete my data and similar) escalates
  to a human and stops automation.
- Bookings land only in working hours: Monday to Friday,
  09:00 to 17:00.
- Replies never contain the score, the band, or any internal
  term, and never contain another lead's data.

## Side effects and tools

All side effects go through tools, each recorded in the trace
with a fixed simulated cost (a budgeting device for tests, not
a latency measurement): `capture_lead`, `score_lead`,
`crm_write`, `calendar_check`, `book_appointment`,
`send_followup`, `send_reply`, `escalate_to_human`. Capturing
the same lead (same name and channel) twice in one environment
returns the existing record instead of writing a duplicate.

## The stand-in for nondeterminism

`standin.py` wraps this agent for Lessons 21 to 24. It is not
a model and does not pretend to be one: it simulates three
named sources of variance (phrasing, decision boundary wobble,
reply wording) with seeded randomness, so flaky behaviour can
be studied with reproducible numbers. The deterministic core
above is what the regression and capstone suites gate on.
