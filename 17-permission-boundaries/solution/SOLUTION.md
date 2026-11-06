# Solution: Permission boundaries

Small budgets collide innocently: figures like 500 or 100 appear in ordinary sentences and in the agent's own text, so a naive number scan reports false leaks, while distinctive figures (2,400, 3,200) are meaningful signals. The implication is the general one for leak scanning: automated scans catch the unambiguous layer (names, distinctive values, internal terms), and the ambiguous layer needs either context rules or human review. A suite that pretends the number scan is exact will either cry wolf or quietly whitelist everything.
