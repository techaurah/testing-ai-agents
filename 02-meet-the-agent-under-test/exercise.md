# Exercise: Meet the agent under test: the contract audit

Add a seventh clause to the audit: no conversation in the gated sets uses more than 8 tool calls. Implement it inside `evaluate()` by counting trace lengths, and confirm the audit still reports all clauses passing. (Lesson 25 will give this clause a proper home as a budget test.)
