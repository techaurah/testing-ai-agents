# Lesson 06: Exact and structural assertions

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 05

Assertion styles form a ladder of coupling. Outcome assertions (band, stage) survive almost everything and see almost nothing. Structural assertions check the shape of the result (keys, types, the trace entries' fields) and catch contract drift while ignoring values. Exact assertions compare the whole result byte for byte and catch everything, including things you did not want to catch.

This lesson runs one boundary case, s03 at score 80, through three disturbances and prints the survival table: a courtesy suffix appended to replies, a one point threshold shift that flips the band, and a shape break (the tokens field dropped from trace entries). Read the table by columns: each style has a job, and the failures are as informative as the survivals.

## Run it

```bash
python3 assertion_styles.py
```

Wording change: outcome survives, structural survives, exact fails. Boundary shift: outcome fails (the band flipped, which is a real behaviour change), structural survives (the shape did not change), exact fails. Shape break: outcome survives, structural fails (its home ground), exact fails. No style is best. Exact assertions belong on a few golden conversations (Lesson 14), structural assertions on the tool and result contracts (Lesson 10), and outcome assertions everywhere, backed by the stronger styles where the risk lives.

## Common failures

- Reaching for exact assertions as the default because they feel rigorous. They fail on a courtesy suffix, and a suite that cries wolf gets ignored.
- Expecting structural assertions to catch value changes. Shape is all they see; a flipped band in a well shaped result passes them, correctly.
- Using one style for the whole suite. The capstone layers all of them, each where its blindness is acceptable.

## Recap checklist

- [ ] You can reproduce the three by three survival table from the artifact output
- [ ] You can say which style catches a renamed trace field, and which catches a flipped band
- [ ] You know where exact assertions legitimately belong (goldens)

## Resources

- [Lesson 14](../14-golden-trajectories/): exact comparison, used with discipline
- [Lesson 08](../08-trajectory-assertions/): the style that grades the path itself
