# ADR-015: Launch RPS model and validation
- **Status:** Proposed (revised v0.3, 2026-11-21) — not approved

## Decision (proposed)
`RPS(n) = 20 + 130·(1 − e^(−n/19.0575))`, anchored at 5 presses = 50.000 RPS; `n_max = 60` (12/s); half-open window `[W0, W0+5000)`; 0 presses → 20.00 RPS; maximum 144.42 RPS; edge + release counting; server timestamp bounds; regularity flags without automatic penalty.

## Known limitations (accepted unless the user decides otherwise)
- A macro or modified client can always reach the cap; advantage over a 7-presses/s human measured at 68.6% (Attack mirror) / 93.3% (Stamina mirror).
- The launch-zone check is client-side only.
- Device fairness is only enforced above the cap; real per-device distributions are unknown until spike S-5.

## Alternatives
Literal linear 10·n (unbounded); linear capped at 15 presses (no reward above 3/s); lower caps 10/s or 8/s (measured in DOC-LAUNCH-001 §5); RPS_max 130; hold-to-charge (excluded by user).

## Revisit when
S-5 shows > 5% median RPS gap between input types, or integrity complaints about macros.
