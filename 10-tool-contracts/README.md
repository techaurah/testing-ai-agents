# Lesson 10: Tool contracts

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 09

Agents act through tools, and every tool has a contract: the shape of its arguments, the type of its result, and what its failures look like. In Course 3 you built these contracts for an MCP server; here you test them from the caller's side. This lesson writes the eight tools' contracts down as data and validates every recorded call in every gated case against them.

Two details matter. First, the validation includes the simulated costs: a drifted cost is a drifted budget, and Lesson 25's budget tests are only as honest as the cost table they read. Second, error paths get contracts too: an empty message must parse to an all empty signal set rather than crash, and an unknown channel must score with the contract's default points rather than raise.

## Run it

```bash
python3 tool_contracts.py
```

223 trace entries across the gated sets validate with 0 contract violations: argument keys exactly as contracted, result types as contracted, simulated milliseconds and tokens equal to the published cost table. The error paths behave as contracted: the empty message yields budget None, timeline None, and no intents, and the unknown channel `smoke-signal` scores with the default 6 channel points, 4 points below email's 10.

## Common failures

- Contracting only the happy path. The failures a contract does not describe become stack traces in production.
- Letting the test import the cost table from the agent and also validate against it, without noticing the circularity. Here the check is that the recorded costs equal the table; the table itself is reviewed as contract data in agent/README.md.
- Validating arguments but not results. A tool that starts returning strings where ints were promised breaks scoring downstream in ways outcome tests attribute to the wrong cause.

## Recap checklist

- [ ] 223 trace entries validate against 8 contracts with 0 violations
- [ ] Empty input and unknown channel both follow their contracts
- [ ] You can name the four things each tool contract pins

## Resources

- [Course 3: Build MCP Servers](https://github.com/techaurah/build-mcp-servers): the same contracts from the server's side
- [Lesson 26](../26-testing-at-the-boundaries/): these contracts at a real protocol boundary
