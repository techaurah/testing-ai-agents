# Solution: Exact and structural assertions

Outcome survives (band and stage untouched). Structural fails (entry key sets differ). Exact fails. No single style catches both this and the boundary shift except exact, which is the point: coverage comes from layering outcome (catches the shift) with structural (catches the rename), keeping exact for goldens. Suites that demand one assertion style to do everything end up with exact everywhere and a team that stops reading failures.
