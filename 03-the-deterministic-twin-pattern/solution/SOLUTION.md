# Solution: The deterministic twin pattern

Several outcomes shift, all through identity and state: lead ids increment across cases (LD-002, LD-003, ...), so any expectation touching ids or record counts breaks, and idempotent captures can collide across leads with the same name and channel. The mechanism is shared mutable state acting as a hidden input. The fresh environment rule costs one object construction per case and removes the entire class.
