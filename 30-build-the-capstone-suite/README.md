# Lesson 30: Build the capstone suite

Time: ~60 min | Difficulty: Advanced | Prerequisites: Lesson 29

Everything the course taught, assembled into one suite and graded against Lesson 29's gates. The battery per gated case: full outcome match (score, band, stage, tool sequence, refusals, escalations, flags, bookings, reply count), the Lesson 08 trajectory rules, the Lesson 09 reply content scan, the Lesson 25 budget checks, and a state agreement check between the CRM record and the reported outcome. Then golden replay, the idempotency check, and the mutation run: the same battery under each mutant's configuration, a mutant killed when at least one check fails under it, with the first failing check reported.

The suite is one file, standard library only, and it prints its scorecard as JSON. Nothing in it is new; the capstone's claim is assembly, that the pieces compose into a gate a team can stand behind.

## Run it

```bash
python3 capstone_suite.py
```

The reference build passes everything: scenarios 24 of 24, safety 12 of 12, regression 10 of 10, goldens exact, idempotency holds, and the reference failure map is empty. The mutation run kills 8 of 8, above the gate of at least 7. The kill table is worth reading: m5 (disclosure) dies to the reply content scan on its first case, m6 (idempotency) dies to the duplicate records check and nothing else, m7 (dropped followup) dies to the tool sequence, m2 (injection guard) dies to the outcome check because the capstone's outcome includes the flags list, and the rest die to outcome mismatches across 3 to 41 failing checks each.

## Common failures

- Trimming the battery where it feels redundant. m6 is killed by exactly one check in the entire suite; remove that check as redundant and the suite ships a duplicate record defect.
- Reporting the mutation score without the kill table. The table is where the suite's blind spots would show; the single number hides them.
- Letting the suite import the lessons' artifacts piecemeal. The capstone re-implements its checks in one file on purpose: a shipped suite is a product with its own maintenance life, not a collage.

## Recap checklist

- [ ] Reference scorecard: 24 of 24, 12 of 12, 10 of 10, goldens exact, idempotency true, no failures
- [ ] Mutants killed 8 of 8 against a gate of at least 7
- [ ] You can name the check that kills m5, m6, and m7

## Resources

- [Lesson 31](../31-evaluate-and-harden/): the gate table and the hardening comparison
- [29-capstone-spec/capstone/gates.json](../29-capstone-spec/capstone/gates.json): the gates this suite is graded against
