# Lesson 02: Meet the agent under test: the contract audit

Time: ~35 min | Difficulty: Beginner | Prerequisites: Lesson 01

Before you test a system you need to know what it claims to be. The agent under test ships with a written contract in `agent/README.md`: its inputs and outputs, the scoring table, the band thresholds, the routing rules, the safety rules, and its eight tools. This lesson turns that document into probes and audits the code against its own claims.

This is a habit worth stealing for real projects. Agents accumulate behaviour nobody wrote down, and behaviour nobody wrote down cannot be tested, only discovered in production. The audit either confirms the contract or finds the gaps while they are still cheap.

## Run it

```bash
python3 contract_audit.py
```

Six clauses are probed over all 46 gated cases, and all 6 pass. The regression set's pinned boundary scores (100, 80, 78, 65, 64, 50, 49) reproduce exactly, which pins the band thresholds. Every one of the 8 contract tools is exercised somewhere in the gated sets, and no unnamed tool ever appears. Every reached stage is a contract stage (all four occur). No reply contains an internal term the contract forbids disclosing (0 hits), and no booking lands outside working hours (0 cases).

## Common failures

- Auditing the code against your memory of the contract instead of the document. The document is the claim; memory is how drift hides.
- Counting a clause as checked because a related test exists. Each clause here has a probe that would fail if the clause broke.
- Treating a passed audit as proof the contract is complete. The audit proves the code matches the document; Lesson 20 shows the behaviours the document itself is missing.

## Recap checklist

- [ ] You have read the contract in agent/README.md end to end
- [ ] The audit reports 6 of 6 clauses passing over 46 cases
- [ ] You can state the band thresholds and the four stages from memory

## Resources

- [agent/README.md](../../agent/README.md): the contract being audited
- [Lesson 18](../18-regression-suites/): where the boundary scores get pinned permanently
