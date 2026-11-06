# Lesson 07: Property based assertions

Time: ~45 min | Difficulty: Intermediate | Prerequisites: Lesson 06

Example based tests check the leads you thought of. Property based assertions check laws the behaviour must obey for every lead, over generated inputs. This lesson writes five laws for the agent and runs them over 400 seeded generated leads, with no property testing library: a generator, the laws, and a counter.

The laws differ in strength, and the difference is the lesson. Range and band agreement laws are weak but universal. Budget monotonicity (raising only the budget never lowers the score) is a shape law about the scoring function's character. The exact value law, that the score equals the contract's points table recomputed independently in the test, is the strongest: it is a second implementation used as an oracle.

## Run it

```bash
python3 property_assertions.py
```

The reference agent violates none of the laws across 400 generated leads: 0 range violations, 0 band disagreements, 0 exact value mismatches, 0 illegal stages, 400 monotonicity pairs with 0 violations, and 400 unique lead ids in a shared environment. Then the halved budget weight mutant runs against the same laws: monotonicity still holds (halving preserves order), but the exact value law catches it on all 400 leads. Properties are not interchangeable; a suite needs to know which law sees which defect.

## Common failures

- Generating inputs the real system would never receive, then fixing the system to satisfy them. Generated leads here stay inside the contract's input space on purpose.
- Treating a passed property run as proof. Four hundred cases is evidence with a shape, not certainty; Lesson 24 puts intervals on claims like this.
- Writing the oracle by copying the implementation. The points table in this artifact is recoded from the contract document, not imported from the agent; a copied oracle cannot catch a copied bug.

## Recap checklist

- [ ] The reference agent shows 0 violations across all laws on 400 leads
- [ ] The budget mutant passes monotonicity and fails the exact value law 400 times
- [ ] You can explain why the oracle must be an independent implementation

## Resources

- [Lesson 11](../11-parsers-and-extractors/): the front door these generated leads walk through
- [Lesson 24](../24-how-many-runs-are-enough/): what 400 passing runs actually prove
