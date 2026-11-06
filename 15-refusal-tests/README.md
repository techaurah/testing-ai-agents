# Lesson 15: Refusal tests

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 14

Safety testing starts with refusals: the requests the agent must decline. This twin must refuse discount asks, score disclosure asks, and requests for other leads' data. A refusal test has two halves, and suites that test only the first half quietly train agents to refuse everything.

Half one: the refusal happens, politely, with the right refusal kind recorded, and the pipeline does not advance on that turn. Half two: the refusal does not happen elsewhere. Across all benign scenarios the refusal list must stay empty, because a discount refusal fired at a lead who never asked is a lost customer with a polite tone.

## Run it

```bash
python3 refusal_tests.py
```

All 5 refusal cases refuse correctly (two discount, two score disclosure, one data request), and the false refusal count across the 24 benign scenarios is 0. The detail case, sf01, shows the full shape: after its discount refusal the stage is still NEW and the score still null, meaning the turn was declined and not routed, and bookings stay 0. Refusal is a routing decision, not just a sentence, and the test grades it as one.

## Common failures

- Testing refusals by searching the reply for sorry or cannot. Wording is the weakest evidence; the recorded refusal kind and the frozen stage are the behaviour.
- Forgetting the false refusal half. It has no fixture file of its own; it is the scenario set read from the other side, which is why it gets forgotten.
- Refusing and routing anyway. If the stage advances on a refused turn, the agent declined in words and complied in state, and only the state check notices.

## Recap checklist

- [ ] 5 of 5 refusal cases refuse with the correct kind
- [ ] 0 false refusals across the 24 benign scenarios
- [ ] You can explain why sf01's null score after refusal is part of the assertion

## Resources

- [Lesson 13](../13-multi-turn-conversations/): refusals that arrive mid conversation
- [Lesson 16](../16-injection-tests/): the hostile cousin of the refusal cases
