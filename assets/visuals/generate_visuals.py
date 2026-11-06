#!/usr/bin/env python3
"""Generate the Testing AI Agents diagram set as clean, branded SVGs.

Style: white canvas, navy (#0B1F4A) primary boxes with white text,
light blue (#E0F2FE) secondary boxes with navy text, cyan (#0891B2)
arrows, amber (#F59E0B) accent for warnings/gates. Run: python3 generate_visuals.py
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))
NAVY = "#0B1F4A"
LIGHT = "#E0F2FE"
CYAN = "#0891B2"
GREY = "#475569"
FONT = "Segoe UI, Helvetica, Arial, sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class SVG:
    def __init__(self, w, h, title, subtitle):
        self.w, self.h = w, h
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
            f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>',
            f'<text x="40" y="52" font-family="{FONT}" font-size="30" font-weight="700" fill="{NAVY}">{esc(title)}</text>',
            f'<text x="40" y="82" font-family="{FONT}" font-size="17" fill="{GREY}">{esc(subtitle)}</text>',
            f'<rect x="40" y="98" width="90" height="5" fill="{CYAN}"/>',
        ]

    def box(self, x, y, w, h, label, sub="", style="navy"):
        fill, tcol, scol = (NAVY, "#FFFFFF", "#BFE3F2") if style == "navy" else (LIGHT, NAVY, "#33506E")
        if style == "amber":
            fill, tcol, scol = "#FEF3C7", NAVY, "#7C5A03"
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}"/>')
        if sub:
            self.parts.append(f'<text x="{x + w/2}" y="{y + h/2 - 4}" text-anchor="middle" font-family="{FONT}" font-size="19" font-weight="700" fill="{tcol}">{esc(label)}</text>')
            self.parts.append(f'<text x="{x + w/2}" y="{y + h/2 + 20}" text-anchor="middle" font-family="{FONT}" font-size="14" fill="{scol}">{esc(sub)}</text>')
        else:
            self.parts.append(f'<text x="{x + w/2}" y="{y + h/2 + 7}" text-anchor="middle" font-family="{FONT}" font-size="19" font-weight="700" fill="{tcol}">{esc(label)}</text>')

    def arrow(self, x1, y1, x2, y2, label=""):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CYAN}" stroke-width="3" marker-end="url(#ah)"/>')
        if label:
            self.parts.append(f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2 - 8}" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="600" fill="{CYAN}">{esc(label)}</text>')

    def note(self, x, y, text):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="15" fill="{GREY}">{esc(text)}</text>')

    def save(self, name):
        defs = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
                'markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" '
                f'fill="{CYAN}"/></marker></defs>')
        body = "\n".join(self.parts[:2] + [defs] + self.parts[2:]) + "\n</svg>"
        with open(os.path.join(OUT, name), "w") as f:
            f.write(body)
        print("wrote", name)



def course_map():
    s = SVG(1180, 560, "Testing AI Agents: the course map",
            "Ten modules, one agent under test, one suite graded by mutation testing")
    mods = [
        ("Start here", "why agent testing is different"),
        ("The agent and its twins", "contracts, scenarios, the harness"),
        ("Assertion styles", "exact, structural, property, trajectory"),
        ("Unit tests for parts", "templates, tool contracts, parsers"),
        ("State and conversations", "the CRM is the outcome"),
        ("Safety suites", "refusals, injection, permissions"),
        ("Regression and analysis", "fossil records, error taxonomy"),
        ("Nondeterminism, honestly", "stand-in, pass rates, run counts"),
        ("Budgets and boundaries", "costs as tests, MCP, retrieval"),
        ("Workflow and capstone", "CI tiers, eval driven development"),
    ]
    x, y = 40, 140
    for i, (label, sub) in enumerate(mods):
        style = "amber" if i in (0, 9) else ("navy" if i % 2 == 0 else "light")
        s.box(x, y, 340, 76, label, sub, style)
        if i % 3 != 2 and i < 9:
            s.arrow(x + 340, y + 38, x + 380, y + 38)
        x += 380
        if i % 3 == 2:
            x = 40
            y += 120
    s.note(40, 540, "Every module tests the same agent and the same 46 gated cases. The capstone assembles all of it.")
    s.save("course-map.svg")


def why_different():
    s = SVG(1180, 480, "Why agent testing is different",
            "Four differences, each measured in Lesson 01")
    s.box(40, 140, 520, 90, "The clock is an input", "same message: BOOKED Monday, QUALIFIED Saturday", "navy")
    s.box(620, 140, 520, 90, "Outcomes live in state", "CRM, calendar, outbox: one run changes three stores", "light")
    s.box(40, 290, 520, 90, "Many paths, one ending", "5 distinct tool paths across 24 scenarios", "light")
    s.box(620, 290, 520, 90, "Boundaries are unstable", "s03 passes 19 of 30 stand-in trials, s01 passes 28", "navy")
    s.note(40, 440, "Classical tests compare a return value. Agent tests grade outcomes, paths, state, and stability.")
    s.save("why-different.svg")


def twin_pattern():
    s = SVG(1180, 460, "The deterministic twin pattern",
            "Exact tests need a system that behaves identically on identical inputs")
    s.box(40, 160, 250, 90, "The real agent", "model based, wobbles", "light")
    s.box(340, 160, 250, 90, "The twin", "same contract, deterministic", "navy")
    s.box(640, 160, 230, 90, "Fixtures", "lead, turns, clock", "amber")
    s.box(920, 160, 220, 90, "Exact tests", "byte identical replays", "navy")
    s.arrow(290, 205, 340, 205)
    s.arrow(590, 205, 640, 205)
    s.arrow(870, 205, 920, 205)
    s.note(40, 320, "Three rules: fresh environment per case, every input is data, the twin stays faithful to the contract.")
    s.note(40, 350, "Measured in Lesson 03: 46 of 46 gated cases replay byte identically in fresh environments.")
    s.save("twin-pattern.svg")


def assertion_styles():
    s = SVG(1180, 480, "Assertion styles: a ladder of coupling",
            "Each style survives some changes and catches others; suites layer them")
    s.box(40, 150, 240, 90, "Outcome", "band, stage: sees endings", "light")
    s.box(320, 150, 240, 90, "Structural", "shape: catches contract drift", "navy")
    s.box(600, 150, 240, 90, "Trajectory", "the path: order rules", "navy")
    s.box(880, 150, 260, 90, "Exact", "everything: goldens only", "amber")
    s.arrow(280, 195, 320, 195)
    s.arrow(560, 195, 600, 195)
    s.arrow(840, 195, 880, 195)
    s.note(40, 300, "Lesson 06 measures the table: a courtesy suffix defeats only exact; a band flip defeats only outcome;")
    s.note(40, 330, "a dropped trace field defeats only structural. No style is best; each has a job.")
    s.save("assertion-styles.svg")


def trajectory_rules():
    s = SVG(1180, 500, "Trajectory assertions",
            "The outcome can be right while the path is wrong; grade the path")
    s.box(40, 170, 180, 80, "capture_lead", "always first (T1)", "navy")
    s.box(250, 170, 180, 80, "score_lead", "before side effects (T2)", "navy")
    s.box(460, 170, 200, 80, "calendar_check", "before any booking (T3)", "light")
    s.box(690, 170, 200, 80, "book_appointment", "at most once (T4)", "light")
    s.box(920, 170, 220, 80, "escalate", "then only replies (T5)", "amber")
    s.arrow(220, 210, 250, 210)
    s.arrow(430, 210, 460, 210)
    s.arrow(660, 210, 690, 210)
    s.arrow(890, 210, 920, 210)
    s.note(40, 330, "Lesson 08: 0 violations over 46 gated cases, and 3 hand built bad traces each caught by its own rule.")
    s.note(40, 360, "Rules forbid bad orderings; they do not script one exact sequence. Goldens do that, for a few conversations.")
    s.save("trajectory-rules.svg")


def safety_suites():
    s = SVG(1180, 460, "The safety suites",
            "Three ways an agent can hurt someone, three suites that grade them")
    s.box(40, 160, 340, 100, "Refusals", "decline politely, freeze the turn, never refuse the benign", "navy")
    s.box(420, 160, 340, 100, "Injection", "input is data: score from signals, flag the attempt", "amber")
    s.box(800, 160, 340, 100, "Permissions", "one lead never learns or changes another", "navy")
    s.note(40, 330, "Measured: 5 of 5 refusals with 0 false refusals, 3 of 3 injections flagged and ignored,")
    s.note(40, 360, "0 cross lead leaks across 46 cases, and lead records byte identical under a shared environment.")
    s.save("safety-suites.svg")


def pass_rates():
    s = SVG(1180, 480, "pass@k and pass^k: two honest rates",
            "Same trials, different questions; choosing the rate is choosing the claim")
    s.box(40, 160, 500, 110, "pass@k: at least one of k passes", "for assistants with a human picking the good attempt", "light")
    s.box(640, 160, 500, 110, "pass^k: all k trials pass", "for agents acting alone, where every attempt ships", "navy")
    s.note(40, 330, "Measured on s03 (p = 0.475): pass@3 is 0.8553 while pass^3 is 0.1072.")
    s.note(40, 360, "On s01 (p = 0.825): pass@5 is 0.9998 while pass^5 is 0.3822.")
    s.save("pass-rates.svg")


def capstone_flow():
    s = SVG(1180, 460, "The capstone flow", "Gates fixed in advance, then build, then grade, then harden")
    s.box(40, 150, 240, 90, "Spec and gates", "Lesson 29", "amber")
    s.box(330, 150, 240, 90, "Build the suite", "Lesson 30", "navy")
    s.box(620, 150, 240, 90, "Evaluate and harden", "Lesson 31", "navy")
    s.box(910, 150, 230, 90, "Ship it", "Lesson 32", "light")
    s.arrow(280, 195, 330, 195)
    s.arrow(570, 195, 620, 195)
    s.arrow(860, 195, 910, 195)
    s.note(40, 300, "Gates: scenarios 24 of 24, safety 12 of 12, regression 10 of 10, goldens 6 of 6 exact,")
    s.note(40, 330, "budgets within contract, idempotency verified, at least 7 of 8 mutants killed.")
    s.note(40, 390, "Reference build, measured: every gate passes, and 8 of 8 mutants are killed.")
    s.save("capstone-flow.svg")


if __name__ == "__main__":
    course_map()
    why_different()
    twin_pattern()
    assertion_styles()
    trajectory_rules()
    safety_suites()
    pass_rates()
    capstone_flow()
