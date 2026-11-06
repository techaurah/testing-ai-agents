# Lesson 09: Prompts and templates as data

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 08

In a model based agent the prompt is data with behaviour attached; in this twin, the reply templates are that data. Either way, the text layer can be tested as data, cheaply and exactly, without judging a single conversation. This lesson drives the agent across all gated cases and collects every reply it can produce.

The checks are data checks: every reply kind the agent defines is exercised by some case (an unexercised template is untested code wearing a costume), no rendered reply keeps a placeholder brace, no reply contains an internal term the contract forbids disclosing, every reply fits the budget contract's character limit, and every reply opens the way the contract's tone requires.

## Run it

```bash
python3 template_tests.py
```

All 10 reply kinds are exercised across the gated sets (acknowledge, booked, closed, escalation, nurture, offer_alternative, qualified, refuse_data, refuse_discount, refuse_score), over 50 replies checked: 0 placeholder residue, 0 forbidden terms, 0 overlong replies, and 50 of 50 polite openings. Then the disclosure mutant renders routing replies with an internal note attached (band and score), and the same forbidden term check counts 40 hits. The check is three lines of code; what makes it a test is that it runs over everything the agent can say.

## Common failures

- Reviewing templates by reading them in the source file. Reading finds typos; only rendering finds the unfilled placeholder and the term that leaks in one branch.
- Checking one reply per kind. The mutant leaks only on routing replies, so a sample of one per kind can pass while forty production replies leak.
- Forbidding words without a contract behind the list. The forbidden list here is the contract's disclosure rule, not a vibe.

## Recap checklist

- [ ] All 10 reply kinds are exercised and 50 replies pass every data check
- [ ] The disclosure mutant produces 40 forbidden term hits under the same check
- [ ] You know why rendered output, not source text, is the thing to scan

## Resources

- [Lesson 17](../17-permission-boundaries/): the disclosure rule's other half, between leads
- [Lesson 25](../25-budgets-as-tests/): where the character limit comes from
