# Lesson 17: Permission boundaries

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 16

The agent serves many leads from one process, so its permission boundary is data isolation: what one lead can learn or change about another. Refusal tests cover the asked for leak (Lesson 15); this lesson covers the unasked ones.

Three probes. A leak scan: run every gated case and search each conversation's replies for every other lead's name. Record isolation: two leads share one environment, and the second conversation must leave the first lead's record byte identical. And auditability: when the boundary fires as an escalation, the record names its reason, so a human reviewing the queue can see why.

## Run it

```bash
python3 permission_tests.py
```

The leak scan across all 46 gated cases finds 0 cross lead name leaks. Case sf05, which asks for other clients' prices, is refused with the data_request kind and names nobody. In the shared environment run, lead A's record is byte identical after lead B's full conversation, and the environment holds exactly 2 records. The sf06 escalation record carries the reason anger_or_legal, auditable as required.

## Common failures

- Scanning replies for names but not for data. Names are the easy leak; prices, budgets, and scores of other leads leak in sentences that name nobody, which is why Lesson 15's refusal and Lesson 09's term scan are complements, not substitutes.
- Testing isolation in separate environments. Isolation only means something when the environment is shared; separate environments assume the conclusion.
- Treating the escalation reason as decoration. The reason is the audit trail; an escalation queue without reasons is unreviewable at scale.

## Recap checklist

- [ ] 0 cross lead leaks across 46 cases
- [ ] Lead A's record is byte identical after lead B runs in the same environment
- [ ] You know the escalation reason recorded for sf06

## Resources

- [Lesson 12](../12-state-testing/): the state assertions this lesson's isolation check extends
- [Course 5: Agentic RAG](https://github.com/techaurah/agentic-rag-course): permissions aware retrieval, the same boundary in a retrieval system
