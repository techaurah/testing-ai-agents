"""A labelled stand-in for model nondeterminism.

Real agents built on language models vary between runs: users
phrase the same need differently, the model's effective decision
boundary wobbles near thresholds, and reply wording drifts. This
course runs offline with no model, so Lessons 21 to 24 study
that variance through this stand-in instead. It simulates three
named sources, each seeded so any experiment reproduces exactly:

1. Boundary wobble: the band thresholds shift by a seeded delta
   in [-4, +4] points for one trial, so leads sitting near a
   threshold can land on either side of it across trials.
2. Phrasing: with seeded probability, booking words in a turn
   are swapped for synonyms the parser does not know, the way a
   real user's wording can quietly change what an agent sees.
3. Wording: replies gain a seeded courtesy suffix, which breaks
   exact match assertions while leaving behaviour unchanged.

What it does NOT simulate: a model reasoning differently on
identical input, tool errors, or latency variance. The lesson
texts say so wherever its numbers are quoted. Standard library
only.
"""

import copy
import random

import lead_agent as la

PHRASING_SWAPS = [("book a call", "arrange a chat"),
                  ("schedule a call", "set up a chat"),
                  ("book me in", "pencil me in")]
COURTESY_SUFFIXES = [" Thanks again.", " Appreciate it.", ""]


def run_trial(case, seed, base_config=None):
    """Run one trial of a fixture case under the stand-in.
    Returns the agent result plus the trial's variance record."""
    rng = random.Random(seed)
    delta = rng.randint(-4, 4)
    config = dict(base_config or {})
    config.setdefault("hot_threshold", 80)
    config.setdefault("warm_threshold", 65)
    config.setdefault("nurture_threshold", 50)
    config["hot_threshold"] += delta
    config["warm_threshold"] += delta
    config["nurture_threshold"] += delta
    turns = []
    swapped = False
    for turn in case["turns"]:
        text = turn
        if rng.random() < 0.35:
            for old, new in PHRASING_SWAPS:
                if old in text.lower():
                    text = text.lower().replace(old, new)
                    swapped = True
        turns.append(text)
    env = la.Environment()
    result = la.LeadAgent(config).run(
        env, copy.deepcopy(case["lead"]), turns,
        la.datetime.fromisoformat(case["now"]))
    suffix = rng.choice(COURTESY_SUFFIXES)
    if suffix:
        result["replies"] = [r + suffix for r in result["replies"]]
    return {"result": result, "threshold_delta": delta,
            "phrasing_swapped": swapped, "reply_suffix": suffix}


def outcome_matches(result, expect):
    """The trial-level verdict Lessons 21 to 24 use: the outcome
    fields match the fixture expectation. Reply wording is
    deliberately not part of it; Lesson 23 shows what happens
    when a suite makes it part of the verdict by accident."""
    return (result["band"] == expect["band"]
            and result["stage"] == expect["stage"]
            and [t["tool"] for t in result["trace"]] == expect["tools"])
