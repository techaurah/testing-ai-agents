# Lesson 08: Trajectory assertions

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 07

An agent's outcome can be right while its path is wrong: it can book before checking the calendar, write the CRM record before scoring, or keep acting after handing off to a human. Trajectory assertions grade the recorded path. This lesson states five rules for the agent's tool sequences and checks them over every gated case.

The rules are invariants, not scripts: they do not demand one exact sequence (Lesson 14's goldens do that, for a few conversations), they forbid the orderings that are never acceptable. Capture first. Scoring before routing side effects. No booking without a calendar check, and never two bookings. After an escalation, nothing but the closing reply.

## Run it

```bash
python3 trajectory_assertions.py
```

The reference agent violates none of the five rules across all 46 gated cases. Then three hand built bad traces, booking without a check, a duplicate booking, and acting after an escalation, are each caught by exactly their rule (T3, T4, and T5 respectively). A checker that has never been shown a violation it must catch is a hope, not a test; the crafted traces are the trajectory equivalent of a control group.

## Common failures

- Writing trajectory rules so tight they become a second copy of the routing code. Rules should forbid bad orderings and leave good ones free to vary.
- Checking trajectories only on passing cases. The crafted bad traces matter because a rule that fires on nothing proves nothing.
- Forgetting the escalation rule in real systems. Acting after handoff is how a customer gets a sales pitch minutes after being passed to a human.

## Recap checklist

- [ ] Five rules, 46 cases, 0 violations on the reference agent
- [ ] All 3 crafted bad traces are caught, each by its own rule
- [ ] You can state the difference between a trajectory rule and a golden trace

## Resources

- [Lesson 05](../05-your-first-scenario-test/): the followup mutant these rules catch
- [Lesson 14](../14-golden-trajectories/): exact paths, for the few conversations that deserve them
