"""Lesson 24 artifact: how many runs are enough.

Two tools, both computable with the standard library, both
honest about their limits:

1. The Wilson score interval. Twenty passes in twenty trials
   does not mean a 100 percent pass rate; it means a rate
   whose 95 percent interval reaches down to the number this
   file prints. Fifty and a hundred perfect runs narrow the
   interval, never to a point. A suite report that prints the
   interval next to the count is telling the truth; one that
   prints only the percentage is performing.

2. The failure catching rule. To have a 95 percent chance of
   seeing at least one failure from a defect that strikes
   with probability q per run, you need
   n >= log(0.05) / log(1 - q) runs. For q = 0.05 that is 59
   runs, which is why a defect that fires once in twenty runs
   sails through a 20 trial suite about a third of the time.

No fake precision anywhere: intervals, not decimals.

Offline, standard library only. Run: python3 sample_sizes.py
"""

import math

Z = 1.96  # 95 percent


def wilson(successes, trials, z=Z):
    if trials == 0:
        return (0.0, 1.0)
    p = successes / trials
    denom = 1 + z * z / trials
    centre = (p + z * z / (2 * trials)) / denom
    margin = (z * math.sqrt(p * (1 - p) / trials
                            + z * z / (4 * trials * trials))) / denom
    return (round(max(0.0, centre - margin), 4),
            round(min(1.0, centre + margin), 4))


def runs_to_catch(q, confidence=0.95):
    return math.ceil(math.log(1 - confidence) / math.log(1 - q))


def evaluate():
    return {
        "wilson_20_of_20": wilson(20, 20),
        "wilson_50_of_50": wilson(50, 50),
        "wilson_100_of_100": wilson(100, 100),
        "wilson_47_of_50": wilson(47, 50),
        "runs_to_catch_5pct_at_95": runs_to_catch(0.05),
        "runs_to_catch_10pct_at_95": runs_to_catch(0.10),
        "runs_to_catch_1pct_at_95": runs_to_catch(0.01),
        "chance_5pct_defect_survives_20_runs": round(0.95 ** 20, 4),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
