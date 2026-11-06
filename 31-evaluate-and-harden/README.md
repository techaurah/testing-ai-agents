# Lesson 31: Evaluate and harden

Time: ~45 min | Difficulty: Advanced | Prerequisites: Lesson 30

Step one is the gate table: every gate declared in Lesson 29 checked against the Lesson 30 suite's measured results, pass or fail with its number, nothing rounded and nothing averaged. Step two is the hardening argument, and it is made with evidence rather than adjectives.

The evidence is a controlled comparison. The same eight mutants are run against the Lesson 05 style harness, outcome assertions only (score, band, stage), and the kills are counted. The mutants that survive the weak harness are not exotic: a silenced injection flag, a leaked score in the replies, a duplicated CRM record, a dropped followup. Each survivor names the check the full suite carries that the weak one lacks, which is the entire justification for the full battery's size, stated as data.

## Run it

```bash
python3 evaluate_and_harden.py
```

The gate table passes 7 of 7: scenarios, safety, and regression at full marks, goldens exact, budgets clean, idempotency holding, and the mutation gate met at 8 of 8 against at least 7 required. The comparison: the outcome only harness kills 4 of 8 mutants (m1, m3, m4, m8, the ones that move scores, bands, and stages), and the full suite kills 8 of 8. The four survivors under the weak harness are m2, m5, m6, and m7, and each maps to one battery component: flags in the outcome, the reply content scan, the idempotency check, and the tool sequence comparison.

## Common failures

- Hardening by adding checks until the number looks good. Each check in the battery is justified by a named survivor; a check without a mutant (or a production incident) behind it is speculative weight.
- Comparing harnesses on different case sets. The comparison here uses identical gated sets and identical mutants; change either and the numbers stop meaning anything.
- Treating 8 of 8 as the end of the story. Lesson 30's exercise already found a wording mutant that survives; mutation scores measure the mutants you thought of, and the honest report says so.

## Recap checklist

- [ ] Gate table: 7 of 7 passing, mutation gate met at 8 of 8
- [ ] Outcome only harness kills 4 of 8; you can name the four survivors and their killing checks
- [ ] You can state what a mutation score does and does not claim

## Resources

- [Lesson 19](../19-error-analysis/): classifying this suite's own failures, the same discipline
- [RESEARCH.md](../../RESEARCH.md): mutation testing's origins and the score's definition
