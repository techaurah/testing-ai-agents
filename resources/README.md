# Resources

Curated resources for Testing AI Agents, grouped by theme. Lessons
link to the items they use; this page is the full shelf.
Primary sources first, because they age best, with the check
date where a page describes a fast moving field. If a link here
breaks, that is a lesson problem: please open an issue so it
gets fixed for everyone.

New to a word? The [glossary](glossary.md) defines every term
this course uses, in plain language.

## The companion shelf (this programme)

- [Agentic AI for Beginners](https://github.com/techaurah/agentic-ai-for-beginners): Course 1. How agents work inside: loops, tools, memory, evaluation, MCP. The agents this course teaches you to test are built there.
- [AI Automation with n8n](https://github.com/techaurah/ai-automation-with-n8n): Course 2. Workflow automation with validated, forkable workflows.
- [Build MCP Servers](https://github.com/techaurah/build-mcp-servers): Course 3. The tool layer agents use; Lesson 26 tests exactly such a tool boundary.
- [AI Agents for Business](https://github.com/techaurah/ai-agents-for-business): Course 4. The commissioning side: choosing, piloting, and supervising agents, for owners and operators.
- [Agentic RAG](https://github.com/techaurah/agentic-rag-course): Course 5. Retrieval systems in depth; Lesson 26's retrieval boundary is its home ground.
- [QualBench](https://github.com/techaurah/qualbench): TechAura's deterministic agent benchmark: 50 scenarios, no LLM judge. This course's harness philosophy comes from it.

## Primary sources (facts checked 2026-11-06; see RESEARCH.md)

- Anthropic, "Demystifying evals for AI agents" (engineering blog, 2026-01-09): the task, trial, transcript, and outcome vocabulary, pass@k and pass^k, capability versus regression evals, and the clean environment rule this course is built on.
- Hamel Husain's LLM Evals FAQ (on his site and Substack): error analysis, failure taxonomies, and why code based evaluators come before judges, from the Maven course's instructors.
- Shankar et al., "Who Validates the Validators?" (UIST 2024): the criteria for trusting an LLM judge, and why judges are validated against human labels before use.
- Wikipedia, "Mutation testing", and the Stryker documentation: the mutant, killed mutant, and mutation score definitions the capstone uses.
- [Python documentation](https://docs.python.org/3/): the standard library every artifact in this course is built on.

## Frameworks, in their own words (checked 2026-11-06; expect drift)

- [Promptfoo](https://www.promptfoo.dev): MIT licensed, YAML configured evaluation with deterministic and model graded assertions, cost and latency assertions, and red teaming. Lesson 26 names it as the closest industrial relative of this course's harness.
- [DeepEval](https://github.com/confident-ai/deepeval): Apache 2.0, pytest style, with agentic metrics such as Task Completion and Tool Correctness; most headline metrics need a judge model.
- [RAGAS documentation](https://docs.ragas.io): the standard RAG metric set (faithfulness, answer relevancy, context precision, context recall), judge based; Course 5 covers its territory deterministically.
- [LangSmith](https://www.langchain.com/langsmith): LangChain's observability and evaluation platform; datasets, evaluators, and experiments, account based.
- [Braintrust](https://www.braintrust.dev): evaluation platform built on data, task, and scores primitives, with an MIT licensed autoevals library.

## Going further in this repo

- [resources/glossary.md](glossary.md): every course term, defined plainly.
- The capstone [showcase](../showcase/): finished, graded test suites from learners, with their gate tables.
