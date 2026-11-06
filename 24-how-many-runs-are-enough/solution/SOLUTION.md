# Solution: How many runs are enough

Solve 0.95 = 1 - (1 - q)^30, giving q = 1 - 0.05^(1/30), which is about 0.095, roughly a 1 in 10 per run defect. The README sentence: the nightly tier runs 30 trials per case and will catch, with 95 percent confidence, any defect that breaks a case at least about once in ten runs; rarer defects can pass it, and claims beyond that need a bigger tier. Stating the limit in the README is what separates a measured suite from a reassuring one.
