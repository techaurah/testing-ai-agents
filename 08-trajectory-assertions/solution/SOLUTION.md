# Solution: Trajectory assertions

The reference agent writes the CRM record once per conversation on every route, so T6 shows 0 violations over 46 cases. A trace with two `crm_write` entries and otherwise legal ordering violates only T6. No gated case comes close: the one near miss is the idempotency territory of Lesson 12, where a repeated run, not a repeated write inside one run, is the risk. That distinction is why T6 belongs here and the double run check belongs in state testing.
