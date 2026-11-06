# Lesson 12: State testing: the CRM is the outcome

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 11

Anthropic's evaluation guidance makes the point this lesson operationalises: grade the outcome in the world, not the agent's narration of it. The agent's world here is the fake environment, so state tests assert on it directly. After a conversation, the CRM record, the calendar, and the outbox are the truth; the reply is a claim about that truth.

State tests also own idempotency, the property that doing the same thing twice changes nothing the second time. Lead capture is the classic place it breaks: a retried webhook or a double submitted form creates a duplicate record, and every downstream count quietly doubles.

## Run it

```bash
python3 state_testing.py
```

Across all 24 scenarios the state agrees with the narration: exactly one CRM record per conversation, its stage, score, and band equal to the reported outcome, and calendar bookings equal to the fixture's count, 0 mismatches. The idempotency check runs the same lead twice in one environment and still finds 1 record with the same lead id. The mutant with idempotent writes disabled finds 2 records, while its replies stay word perfect: only a state test sees this defect.

## Common failures

- Asserting on the reply when the state is available. Replies are generated to sound right; state merely has to be right.
- Testing idempotency by calling capture twice with different leads. The defect lives in the same lead arriving twice, which is the case retries actually produce.
- Snapshotting the entire environment as a golden. State assertions should name the fields that matter, or every irrelevant change becomes a failure to triage.

## Recap checklist

- [ ] 24 scenarios, 0 state mismatches between CRM, calendar, and outcome
- [ ] Double run leaves 1 record for the reference, 2 for the idempotency mutant
- [ ] You can explain why reply based checks are blind to this mutant

## Resources

- Anthropic, "Demystifying evals for AI agents" (engineering blog, 2026-01-09): the task, trial, transcript, outcome vocabulary this course uses. See [RESEARCH.md](../../RESEARCH.md).
- [Lesson 08](../08-trajectory-assertions/): path assertions, the state assertions' sibling
