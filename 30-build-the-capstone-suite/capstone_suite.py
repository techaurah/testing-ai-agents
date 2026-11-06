"""Lesson 30 artifact: the capstone suite itself.

Everything the course taught, assembled into one suite for
the bundled agent, graded against the gates declared in
Lesson 29 (capstone/gates.json):

- Full outcome match on scenarios, safety, and regression:
  score, band, stage, tool sequence, reply count, refusals,
  escalations, flags, and final state counts.
- Trajectory rules from Lesson 08 on every gated case.
- Reply content scan: no internal term in any reply.
- Budget checks from Lesson 25 on every gated case.
- Golden trajectories replayed exactly (Lesson 14).
- Idempotency: a double run leaves one CRM record.
- Mutation run: the eight declared mutants, each graded by
  the same battery. A mutant is killed when at least one
  check fails under it; the first failing check is reported.

The suite prints its scorecard as JSON. Lesson 31 reads the
scorecard, compares it with a weaker harness, and hardens.

Offline, standard library only. Run: python3 capstone_suite.py
"""

import json
import os
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

FORBIDDEN = ["score", "band", "HOT", "WARM", "NURTURE", "LOW", "internal"]
ROUTING_EFFECTS = ["crm_write", "book_appointment", "send_followup"]


_CACHE = {}


def load(name):
    if name not in _CACHE:
        with open(os.path.join(ROOT, "fixtures", name)) as f:
            _CACHE[name] = json.load(f)
    return _CACHE[name]


def gates_spec():
    path = os.path.join(ROOT, "29-capstone-spec", "capstone", "gates.json")
    with open(path) as f:
        return json.load(f)["capstone_suite"]


def trajectory_ok(tools):
    if not tools or tools[0] != "capture_lead":
        return False
    if "score_lead" in tools:
        at = tools.index("score_lead")
        if any(t in tools[:at] for t in ROUTING_EFFECTS):
            return False
    if "book_appointment" in tools:
        at = tools.index("book_appointment")
        if "calendar_check" not in tools[:at]:
            return False
        if tools.count("book_appointment") > 1:
            return False
    if "escalate_to_human" in tools:
        at = tools.index("escalate_to_human")
        if any(t != "send_reply" for t in tools[at + 1:]):
            return False
    return True


def run_case(case, config=None):
    env = la.Environment()
    result = la.LeadAgent(config).run(
        env, case["lead"], case["turns"],
        datetime.fromisoformat(case["now"]))
    return env, result


def check_case(case, config=None):
    """Return the name of the first failing check, or None."""
    budgets = load("budgets.json")
    env, result = run_case(case, config)
    e = case["expect"]
    tools = [t["tool"] for t in result["trace"]]
    outcome = (result["score"] == e["score"] and result["band"] == e["band"]
               and result["stage"] == e["stage"]
               and result["refusals"] == e["refusals"]
               and result["escalated"] == e["escalated"]
               and result["flags"] == e["flags"]
               and result["state"]["bookings"] == e["bookings"]
               and len(result["replies"]) == e["replies"])
    if not outcome:
        return "outcome"
    if tools != e["tools"]:
        return "tool_sequence"
    if not trajectory_ok(tools):
        return "trajectory_rules"
    if any(term in reply for reply in result["replies"] for term in FORBIDDEN):
        return "reply_content"
    ms = sum(t["ms"] for t in result["trace"])
    tokens = sum(t["tokens"] for t in result["trace"])
    longest = max((len(r) for r in result["replies"]), default=0)
    if (len(tools) > budgets["max_tool_calls_per_conversation"]
            or ms > budgets["max_simulated_ms_per_conversation"]
            or tokens > budgets["max_simulated_tokens_per_conversation"]
            or longest > budgets["max_reply_chars"]):
        return "budgets"
    record = env.crm[result["lead_id"]]
    if record["stage"] != result["stage"] or record["score"] != result["score"]:
        return "state_agreement"
    return None


GOLDEN_KEYS = ("trace", "replies", "score", "band", "stage", "state")


def check_goldens(config=None):
    sources = {}
    for name in ("scenarios.json", "safety.json", "regression.json"):
        for case in load(name):
            sources[case["id"]] = case
    for golden in load("golden_trajectories.json"):
        env, result = run_case(sources[golden["source_case"]], config)
        actual = {k: result[k] for k in GOLDEN_KEYS}
        recorded = {k: golden[k] for k in GOLDEN_KEYS}
        if actual != recorded:
            return golden["id"]
    return None


def check_idempotency(config=None):
    case = load("scenarios.json")[0]
    env = la.Environment()
    agent = la.LeadAgent(config)
    now = datetime.fromisoformat(case["now"])
    agent.run(env, case["lead"], case["turns"], now)
    agent.run(env, case["lead"], case["turns"], now)
    return len(env.crm) == 1


def battery(config=None):
    """Run the full battery under a config; return failure map."""
    failures = {}
    for set_name, filename in (("scenarios", "scenarios.json"),
                               ("safety", "safety.json"),
                               ("regression", "regression.json")):
        for case in load(filename):
            failing = check_case(case, config)
            if failing:
                failures[f"{set_name}:{case['id']}"] = failing
    drift = check_goldens(config)
    if drift:
        failures[f"goldens:{drift}"] = "golden_drift"
    if not check_idempotency(config):
        failures["idempotency"] = "duplicate_records"
    return failures


def evaluate():
    spec = gates_spec()
    sets = {name: load(name + ".json") for name in
            ("scenarios", "safety", "regression")}
    reference_failures = battery()
    per_set = {}
    for set_name, cases in sets.items():
        bad = [k for k in reference_failures
               if k.startswith(set_name + ":")]
        per_set[set_name] = f"{len(cases) - len(bad)} of {len(cases)}"
    goldens_ok = not any(k.startswith("goldens:")
                         for k in reference_failures)
    idem_ok = "idempotency" not in reference_failures
    mutants = {}
    killed = 0
    for mutant in spec["mutants"]:
        failures = battery(mutant["config"])
        first = next(iter(failures.values()), None)
        first_case = next(iter(failures.keys()), None)
        mutants[mutant["id"]] = {
            "name": mutant["name"],
            "killed": bool(failures),
            "first_failing_check": first,
            "first_failing_case": first_case,
            "total_failures": len(failures),
        }
        if failures:
            killed += 1
    total_gated = sum(len(v) for v in sets.values())
    return {
        "reference_failures": reference_failures,
        "sets": per_set,
        "gated_cases": total_gated,
        "goldens_exact": goldens_ok,
        "idempotency": idem_ok,
        "mutants": mutants,
        "mutants_killed": f"{killed} of {len(spec['mutants'])}",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
