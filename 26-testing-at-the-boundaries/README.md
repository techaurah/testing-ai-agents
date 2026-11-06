# Lesson 26: Testing at the boundaries: MCP tools and retrieval

Time: ~45 min | Difficulty: Intermediate | Prerequisites: Lessons 10 and 25

Agents meet other systems at boundaries, and boundaries get their own test shapes, because the contract, not the computation, is what can break there. Two boundaries are worked here, cross linked to the courses that own them.

Part A is an MCP style tool boundary: a small JSON-RPC twin in the artifact exposes the scoring function as one tool, the way Course 3 builds real MCP servers. The tests check that the advertised input schema matches the parameters the handler accepts, that a grid of inputs agrees exactly with the direct function, and that the error shapes return standard codes. Part B is a retrieval boundary, Course 5's home ground: a keyword stand-in retriever over six documents, graded with recall at 3 over six labelled queries.

## Run it

```bash
python3 boundary_tests.py
```

Part A: 1 tool listed, its schema fields exactly the five handler parameters; the 25 combination grid (5 budgets by 5 timelines) agrees with the direct function with 0 mismatches; and the three error cases return codes -32601 (unknown method), -32602 (missing parameter), and -32602 (wrong type). Part B: recall at 3 is 0.8333, 5 of 6 queries finding their document. The miss is q6, and it is the classic one: the query says connect, the document says integrations. A vocabulary gap, printed at its real rate rather than rounded away.

## Common failures

- Testing the boundary by testing the computation again. The maths is pinned in Lessons 07 and 11; re testing it here proves nothing about the boundary.
- Accepting a schema that merely resembles the handler's parameters. The grid test exists because resembles drifts; equality does not.
- Rounding a 5 of 6 retrieval result into basically perfect. The missed query is the roadmap for the synonym work, exactly as in Course 5's gap set.

## Recap checklist

- [ ] Grid of 25 combinations, 0 mismatches between the RPC boundary and the direct function
- [ ] Error codes -32601 and -32602 returned for the right shapes
- [ ] Recall at 3 is 0.8333 with q6 missed, and you can name the failure kind

## Resources

- [Course 3: Build MCP Servers](https://github.com/techaurah/build-mcp-servers): building the server this boundary belongs to
- [Course 5: Agentic RAG](https://github.com/techaurah/agentic-rag-course): retrieval evaluation in full depth
- Frameworks named for further reading, dated 2026-11-06 in [RESEARCH.md](../../RESEARCH.md): promptfoo (MIT, YAML assertions), DeepEval, RAGAS, LangSmith; all install required extras, none needed here
