# Lesson 13: Multi-turn conversations

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 12

Single message tests miss the failures that live between turns: side effects repeated per turn, routing that rewinds when a later message objects, and conversations that keep processing after they should have stopped. This lesson tests conversations at three levels.

Turn level: each turn gets exactly one reply, in order. Conversation level: side effects happen once per conversation, not once per turn. Memory level: what turn one decided stays decided when turn two pushes back. And termination: after an escalation, the conversation is over, and the test proves a third turn changed nothing.

## Run it

```bash
python3 conversation_tests.py
```

Nine checks pass over four multi turn cases. Case s15 (a WARM lead over two turns) gets exactly 2 replies and exactly 1 followup, ending QUALIFIED. Case sf09 records its turn two discount refusal while keeping the stage turn one earned. Case sf07 keeps its booking when turn two escalates: stage BOOKED, 1 booking, escalated. And the synthetic termination case, polite opener, legal threat, then a rich booking offer, produces 2 replies and 0 bookings: the third turn is never processed.

## Common failures

- Asserting per turn in isolation and missing that the followup fired twice. Conversation level counts exist because per turn assertions are structurally blind to duplicates.
- Letting an escalation case end the test at the escalation. The termination check needs the extra turn; without it, continues processing is untestable.
- Scoring every turn. This agent scores on the first routing turn by design; a suite that expects re-scoring teaches the agent to re-decide, and cap03 in Lesson 20 tracks the real cost of that design honestly.

## Recap checklist

- [ ] All 9 conversation checks pass, across turn, conversation, memory, and termination levels
- [ ] You can explain why sf07's booking must survive its escalation
- [ ] You know what the third turn in the termination case proves

## Resources

- [Lesson 15](../15-refusal-tests/): the refusal half of the memory level checks
- [Lesson 08](../08-trajectory-assertions/): rule T5, the trajectory form of the termination rule
