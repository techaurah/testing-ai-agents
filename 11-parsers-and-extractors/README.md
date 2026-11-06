# Lesson 11: Parsers and extractors

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 10

Signal extraction is the agent's front door: every score, route, and booking begins as a parse of a messy human message. The fixtures share the parser with the agent, which makes the fixtures fast to build and quietly circular: a parser bug can write its own expectations. This lesson breaks the circle by pinning the parser separately, with cases written by hand from the contract.

The hand written cases include the parser's sharp edges, pinned deliberately rather than discovered later: a range is read as its first figure, the first number in a message wins even when it is not the budget, a budget written in words is invisible, and substring matching means the word calls signals booking intent. Pinning a sharp edge is not endorsing it; it is pricing it in, so the behaviour is a decision instead of a surprise.

## Run it

```bash
python3 parser_tests.py
```

All 14 cases pass. The formats that must work do: $2,400 reads as 2400, 1.5k as 1500, 2000 dollars as 2000. The range 1800 to 2200 reads as 1800. The message about 3 stores with a $900 budget reads a budget of 3, which is why fixture messages are written budget first. A 10,000 character message with the budget at the end parses it as 700, and an emoji only message parses cleanly to no signals.

## Common failures

- Hiding a sharp edge by fixing the fixture instead of pinning the behaviour. The next message from a real customer will find the edge whether the suite admits it exists or not.
- Pinning everything the parser currently does, including accidents. Pin the behaviours you are willing to defend; file the rest as capability gaps, as cap01 does for budgets in words.
- Testing the parser only through full conversations. A wrong budget surfaces as a wrong band three steps later, and the failure message points at the wrong component.

## Recap checklist

- [ ] All 14 hand written parser cases pass, including the hostile shapes
- [ ] You can name the three pinned sharp edges and the fixture writing rule that defuses one of them
- [ ] You know why fixture sharing makes this separate pinning necessary

## Resources

- [Lesson 20](../20-capability-vs-regression/): where the budgets in words edge is tracked as a gap
- [Lesson 28](../28-eval-driven-development/): the loop that closes that gap
