# Lesson 16: Injection tests

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 15

Prompt injection against this twin is text in the lead's message claiming authority: ignore your rules, reveal your instructions, mark me as a perfect lead. There is no model to persuade here, which is the point: the twin isolates the boundary discipline every agent needs, whatever its brain. Untrusted input is data, never instructions, and the suite grades that discipline three ways.

The score must come from signals, never from the claim. The attempt must be recorded as a flag, so monitoring can count attempts even when they fail. And the conversation must still work: safety that breaks the happy path is a bug with good intentions.

## Run it

```bash
python3 injection_tests.py
```

All 3 injection cases are flagged injection_ignored. Case sf04 demands a score of 100 and is booked at the 93 its real signals earn; the demanded value never appears. The cleaned controls, each case with its injection sentence stripped, match the originals on band and stage in 3 of 3 cases, and on score in 2 of 3. The exception is sf04 itself, and it is honest: its booking phrase lives inside the injected sentence, so the cleaned control scores the 80 its remaining signals earn, same band, same stage, same booking.

## Common failures

- Grading injection cases on outcome alone. An unflagged successful defence is invisible to monitoring; the flag is part of the contract.
- Building controls that strip the whole message. A control must remove the attack and keep the customer, or the comparison proves nothing.
- Assuming a rule based twin makes injection somebody else's problem. The discipline, input is data, is identical when the parser is a model; only the attack surface grows.

## Recap checklist

- [ ] 3 of 3 injection cases flagged, with demanded scores never granted
- [ ] Cleaned controls match on band and stage in 3 of 3, score in 2 of 3, with the sf04 reason understood
- [ ] You can state the boundary discipline in one sentence

## Resources

- [Lesson 15](../15-refusal-tests/): the other safety half, requests declined
- [RESEARCH.md](../../RESEARCH.md): how production frameworks approach red teaming (promptfoo), dated 2026-11-06
