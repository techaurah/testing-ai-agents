# Security policy

## Reporting a vulnerability

If you find a security problem in this repository, for example a lesson that teaches an unsafe agent pattern, example code that leaks credentials, or a template that invites learners to paste real customer data or API keys into a public fork, please do not open a public issue with the details.

Report it privately through the contact form at [techaurah.com](https://techaurah.com), with "Testing AI Agents course security" in the message. We aim to acknowledge reports within three working days and to fix or annotate confirmed problems in the affected lesson.

## Scope notes

- This is a teaching repository. The agent under test, every lead, and every conversation are fictional and invented for the lessons; learners are told repeatedly never to put real customer data in a fork.
- Never commit real API keys, tokens, customer lists, or personal data to your fork. If you accidentally commit a secret, rotate it immediately; deleting the commit is not enough.
- Lessons 15 to 17 teach refusal, injection, and permission boundary testing as design disciplines: untrusted input is data, never instructions, and one lead's data is never another lead's business. A lesson or PR that weakens those rules in the agent under test (for example, scoring from a message's claims rather than its signals) will be treated as a security problem, not a style choice.
