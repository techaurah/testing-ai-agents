# Lesson 25: Budgets as tests

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 24

Correctness suites ask whether the agent did the right thing. Budget tests ask what it cost: tool calls per conversation, latency, tokens, reply length. The budget contract lives in `fixtures/budgets.json` (at most 8 tool calls, 400 simulated milliseconds, 0 simulated tokens, 320 reply characters per conversation), and every gated case is measured against it. Costs here are the agent's fixed simulated costs, identical on every machine, so the test is exact rather than statistical. On a real system the same structure holds with measured distributions and the Lesson 24 intervals doing the honest work.

Then the failure this lesson exists for: a retry storm. A plausible variant retries a failed booking four times and produces a perfectly correct outcome at a cost the budget forbids.

## Run it

```bash
python3 budget_tests.py
```

The reference agent breaches no budget across all 46 gated cases. The observed maxima: 8 tool calls and 305 simulated milliseconds, both from sf07 (the book then escalate conversation), 0 tokens, and a longest reply of 138 characters against the 320 limit. The retry storm variant of s01 reaches 10 tool calls and 590 simulated milliseconds with its outcome unchanged, booked, right band, right words, and breaks the budget on both axes. Every correctness assertion in the course passes it. Only the budget catches it, which is why budgets are tests and not dashboards.

## Common failures

- Watching budgets on a dashboard instead of gating on them. A dashboard informs the postmortem; a gate prevents the deploy.
- Setting budgets from the current implementation's measurements plus a margin, forever. Budgets are product decisions (what is a conversation allowed to cost) reviewed like prices, not recordings.
- Budgeting the average case. The budget binds per conversation, at the maximum, because the storm case is an average of one conversation repeated.

## Recap checklist

- [ ] 0 budget breaches across 46 gated cases, observed maxima 8 calls and 305 ms (sf07)
- [ ] The retry storm breaks the budget at 10 calls and 590 ms with a perfect outcome
- [ ] You can say why budgets gate instead of merely reporting

## Resources

- [Lesson 10](../10-tool-contracts/): the cost table these budgets read
- [Lesson 30](../30-build-the-capstone-suite/): budgets inside the capstone battery
