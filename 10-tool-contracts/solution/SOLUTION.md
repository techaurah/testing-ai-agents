# Solution: Tool contracts

The contract audit in Lesson 02 would fail first: its `no_unnamed_tools` clause compares the tools seen against the contract set from the agent's cost table, and the tool contracts check would raise a KeyError on the uncontracted name, which is a failure by noise rather than by assertion. The cleaner design, which the exercise exposes, is for the checker to look up contracts defensively and report an explicit uncontracted tool violation. Outcome and trajectory checks would not notice a well behaved extra tool at all, which is why contracts need their own lesson.
