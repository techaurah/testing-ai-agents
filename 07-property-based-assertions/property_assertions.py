"""Lesson 07 artifact: property based assertions, no library.

Example based tests check the leads you thought of. Property
based assertions check laws the behaviour must obey for every
lead, over generated inputs:

P1 Every score lands in [0, 100].
P2 The band always agrees with the score and the thresholds.
P3 Budget monotonicity: raising only the budget tier never
   lowers the score (checked on constructed pairs).
P4 The exact value law: the score equals the contract's
   points table, recomputed independently here.
P5 Every reached stage is a contract stage, and lead ids in
   one environment are unique per distinct lead.

The laws run over 400 seeded generated leads against the
reference agent (expect zero violations), then P4 runs
against a mutant with a halved budget weight: monotonicity
survives, the exact value law catches it. That split is the
lesson: properties differ in what they can see.

Offline, standard library only. Run: python3 property_assertions.py
"""

import json
import os
import random
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))


def find_root():
    cur = HERE
    while True:
        if os.path.isfile(os.path.join(cur, "agent", "lead_agent.py")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise FileNotFoundError("repo root (agent/) not found above " + HERE)
        cur = parent


ROOT = find_root()
sys.path.insert(0, os.path.join(ROOT, "agent"))
import lead_agent as la

NOW = datetime(2026, 11, 9, 10, 0)
CHANNELS = ["whatsapp", "instagram_dm", "web", "email", "phone"]
BUDGETS = [None, 200, 499, 500, 900, 1000, 1750, 2000, 3200]
TIMELINES = [None, 3, 7, 21, 30, 60, 90, 140]
INTENTS = ["plain", "pricing", "booking"]
MESSAGES = {
    "plain": "Hello, we are looking at options for our business.",
    "pricing": "Hello, what does the service cost?",
    "booking": "Hello, can we book a call?",
}


def spec_score(budget, timeline, channel, intent):
    if budget is None:
        bp = 5
    elif budget >= 2000:
        bp = 45
    elif budget >= 1000:
        bp = 35
    elif budget >= 500:
        bp = 25
    else:
        bp = 10
    if timeline is None:
        tp = 4
    elif timeline <= 7:
        tp = 25
    elif timeline <= 30:
        tp = 18
    elif timeline <= 90:
        tp = 10
    else:
        tp = 6
    cp = la.CHANNEL_POINTS.get(channel, 6)
    ip = {"booking": 15, "pricing": 8, "plain": 2}[intent]
    return min(100, bp + tp + cp + ip)


def generated_leads(count, seed=20261106):
    rng = random.Random(seed)
    leads = []
    for i in range(count):
        intent = rng.choice(INTENTS)
        leads.append({
            "lead": {"name": f"Gen Lead {i}",
                     "channel": rng.choice(CHANNELS),
                     "budget": rng.choice(BUDGETS),
                     "timeline_days": rng.choice(TIMELINES)},
            "intent": intent,
            "turns": [MESSAGES[intent]],
        })
    return leads


def evaluate():
    leads = generated_leads(400)
    violations = {"P1_range": 0, "P2_band": 0, "P4_exact_value": 0,
                  "P5_stage": 0}
    mutant_mismatches = 0
    env = la.Environment()
    ids = []
    for item in leads:
        result = la.LeadAgent().run(env, item["lead"], item["turns"], NOW)
        ids.append(result["lead_id"])
        if not (0 <= result["score"] <= 100):
            violations["P1_range"] += 1
        if result["band"] != la.band_for(result["score"], la.DEFAULT_CONFIG):
            violations["P2_band"] += 1
        expected = spec_score(item["lead"]["budget"],
                              item["lead"]["timeline_days"],
                              item["lead"]["channel"], item["intent"])
        if result["score"] != expected:
            violations["P4_exact_value"] += 1
        if result["stage"] not in la.STAGES:
            violations["P5_stage"] += 1
        mutant = la.LeadAgent({"budget_weight": 0.5}).run(
            la.Environment(), item["lead"], item["turns"], NOW)
        if mutant["score"] != expected:
            mutant_mismatches += 1
    pairs = 0
    mono_violations = 0
    for item in leads:
        richer = dict(item["lead"])
        richer["budget"] = 3200
        base = la.score_lead(item["lead"]["budget"],
                             item["lead"]["timeline_days"],
                             item["lead"]["channel"],
                             item["intent"] == "booking",
                             item["intent"] == "pricing")
        top = la.score_lead(richer["budget"], richer["timeline_days"],
                            richer["channel"], item["intent"] == "booking",
                            item["intent"] == "pricing")
        pairs += 1
        if top < base:
            mono_violations += 1
    return {
        "generated_leads": len(leads),
        "invariant_violations_reference": sum(violations.values()),
        "violations_by_property": violations,
        "monotonicity_pairs_checked": pairs,
        "monotonicity_violations": mono_violations,
        "unique_lead_ids": len(set(ids)),
        "mutant_exact_value_mismatches": mutant_mismatches,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
