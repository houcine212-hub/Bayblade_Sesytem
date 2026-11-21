# ADR-015: Launch RPS model and validation
- **Status:** Proposed · **Date:** 2026-11-21
## Decision (proposed)
Saturating curve anchored at 5 presses = 50 RPS (min 20, asymptote 150, k = 19.06), 12 Hz counted-press cap, edge-triggered presses, server-side timestamp validation with clock offset, regularity flags (no auto-penalty in MVP). Spec: `docs/10-game-design/launch-mechanics-spec.md`.
## Alternatives
Literal linear 10·n (unbounded spread); linear with cap at 15 presses (kills skill above 3/s); hold-to-charge (excluded by user).
## Revisit when
Spike S-5 shows human press distributions differ strongly by device (> 5% median RPS gap).
