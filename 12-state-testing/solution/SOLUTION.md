# Solution: State testing: the CRM is the outcome

The counts agree on all 24 scenarios for the reference agent: the outbox is written by exactly those two tools (in this twin, followups and replies both land in the outbox with their kind recorded), and every kind is one of the 10 known template kinds. The check earns its keep against a plausible defect the other state checks miss: a routing change that sends the followup twice would keep the CRM perfect and double the outbox, which is a customer facing bug, a person contacted twice, that only an outbox count exposes.
