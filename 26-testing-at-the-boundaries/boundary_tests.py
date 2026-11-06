"""Lesson 26 artifact: testing at the boundaries (MCP + retrieval).

Agents meet other systems at boundaries, and boundaries get
their own test shapes. Two are worked here, both offline.

Part A: an MCP style tool boundary. A small JSON-RPC twin in
this file exposes the scoring function as one tool, the way
Course 3 (Build MCP Servers) builds real ones. Boundary tests
check the contract, not the maths (the maths is pinned in
Lessons 07 and 11): the advertised input schema matches the
parameters the handler accepts; a grid of 25 input
combinations agrees exactly with the direct function; and
the three error shapes (unknown method, missing parameter,
wrong type) return the standard JSON-RPC codes.

Part B: a retrieval boundary, the way Course 5 (Agentic RAG)
tests one. A keyword stand-in retriever over six documents is
graded with recall at 3 over six labelled queries. It misses
one: the query says connect, the document says integrations.
That vocabulary gap is the honest, typical retrieval failure,
printed here at its real rate rather than rounded away.

Offline, standard library only. Run: python3 boundary_tests.py
"""

import json
import os
import sys

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

# ---- Part A: the MCP style boundary -------------------------------
TOOL_SCHEMA = {
    "name": "score_lead",
    "description": "Score a lead from its signals.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "budget": {"type": ["integer", "null"]},
            "timeline_days": {"type": ["integer", "null"]},
            "channel": {"type": "string"},
            "booking_intent": {"type": "boolean"},
            "pricing_intent": {"type": "boolean"},
        },
        "required": ["budget", "timeline_days", "channel",
                     "booking_intent", "pricing_intent"],
    },
}


def rpc(request):
    method = request.get("method")
    if method == "tools/list":
        return {"tools": [TOOL_SCHEMA]}
    if method == "tools/call":
        params = request.get("params", {})
        args = params.get("arguments", {})
        schema = TOOL_SCHEMA["inputSchema"]
        for field in schema["required"]:
            if field not in args:
                return {"error": {"code": -32602,
                                  "message": f"missing parameter: {field}"}}
        for field in ("budget", "timeline_days"):
            value = args[field]
            if value is not None and (not isinstance(value, int)
                                      or isinstance(value, bool)):
                return {"error": {"code": -32602,
                                  "message": f"wrong type: {field}"}}
        if not isinstance(args["channel"], str):
            return {"error": {"code": -32602, "message": "wrong type: channel"}}
        score = la.score_lead(args["budget"], args["timeline_days"],
                              args["channel"], args["booking_intent"],
                              args["pricing_intent"])
        return {"result": {"score": score,
                           "band": la.band_for(score, la.DEFAULT_CONFIG)}}
    return {"error": {"code": -32601, "message": "method not found"}}


# ---- Part B: the retrieval boundary -------------------------------
DOCS = {
    "d1": {"pricing", "cost", "packages", "monthly", "plans", "price"},
    "d2": {"booking", "calendar", "appointment", "schedule", "call"},
    "d3": {"refunds", "guarantee", "terms", "conditions", "policy"},
    "d4": {"onboarding", "setup", "timeline", "implementation", "weeks"},
    "d5": {"support", "hours", "contact", "email", "response"},
    "d6": {"integrations", "crm", "hubspot", "salesforce", "api"},
}
QUERIES = [
    ("q1", {"monthly", "cost", "packages"}, "d1"),
    ("q2", {"booking", "appointment"}, "d2"),
    ("q3", {"refunds", "policy", "terms"}, "d3"),
    ("q4", {"setup", "timeline", "weeks"}, "d4"),
    ("q5", {"support", "response", "hours"}, "d5"),
    ("q6", {"connect", "tools", "together"}, "d6"),
]


def retrieve(tokens, k=3):
    scored = sorted(DOCS.items(),
                    key=lambda kv: (-len(tokens & kv[1]), kv[0]))
    return [doc_id for doc_id, _ in scored[:k]]


def evaluate():
    listing = rpc({"method": "tools/list"})
    schema_fields = set(TOOL_SCHEMA["inputSchema"]["properties"])
    grid_mismatches = 0
    grid_cases = 0
    for budget in (None, 300, 750, 1500, 2500):
        for days in (None, 5, 20, 45, 120):
            args = {"budget": budget, "timeline_days": days,
                    "channel": "whatsapp", "booking_intent": True,
                    "pricing_intent": False}
            via_rpc = rpc({"method": "tools/call",
                           "params": {"arguments": args}})["result"]
            direct = la.score_lead(budget, days, "whatsapp", True, False)
            grid_cases += 1
            if via_rpc["score"] != direct or via_rpc["band"] != la.band_for(
                    direct, la.DEFAULT_CONFIG):
                grid_mismatches += 1
    errors = [
        rpc({"method": "tools/explode"}),
        rpc({"method": "tools/call", "params": {"arguments": {
            "timeline_days": 5, "channel": "web",
            "booking_intent": False, "pricing_intent": False}}}),
        rpc({"method": "tools/call", "params": {"arguments": {
            "budget": "lots", "timeline_days": 5, "channel": "web",
            "booking_intent": False, "pricing_intent": False}}}),
    ]
    error_codes = [e["error"]["code"] for e in errors]
    hits = 0
    missed = []
    for qid, tokens, relevant in QUERIES:
        if relevant in retrieve(tokens):
            hits += 1
        else:
            missed.append(qid)
    return {
        "mcp_tools_listed": len(listing["tools"]),
        "schema_fields": sorted(schema_fields),
        "grid_cases": grid_cases,
        "grid_mismatches": grid_mismatches,
        "error_cases": len(errors),
        "error_codes": error_codes,
        "retrieval_queries": len(QUERIES),
        "recall_at_3": round(hits / len(QUERIES), 4),
        "missed_queries": missed,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
