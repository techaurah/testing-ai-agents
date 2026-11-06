# Exercise: State testing: the CRM is the outcome

Extend the state checks to the outbox: assert that the number of sent messages equals the number of `send_reply` plus `send_followup` trace entries for every scenario, and that every outbox entry's kind matches a template kind from Lesson 09.
