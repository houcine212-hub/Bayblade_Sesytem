# ADR-015: Launch RPS model, fairness and validation
- **Status:** **Accepted with changes at G0** (owner accepted G0 for M1 on 2026-11-22) — D-01…D-03 owner-confirmed and **amended by owner decision OQ-LN-08**; D-04 decided under owner delegation. **Pending M1 verification** (S-5 input study, S-1 physics). (v0.3.1 proposal of a saturating curve is superseded.)

## Decision
- **D-01/D-03 as amended (owner, OQ-LN-08):** `RPS = max(20, 10 × n)` — 10 RPS per accepted press with a 20-RPS floor; zero presses launch automatically at 20 RPS; no exponential, saturating or rescaled formula.
- **D-02 (owner):** 1.5 s READY cue without accepted presses, then exactly 5.0 s window.
- **D-04 (delegated):** cap **35** accepted presses (provisional, from a provisional 7 presses/s median); interval floor 142 857 µs; half-open window; max **350 RPS**; FC-1 kept; **ranked gate FR-186** kept; no automated punishment from regularity alone; spin modelled as an authoritative scalar (DOC-CMB-001 §2.4). Re-select the cap after measuring mobile and keyboard/gamepad distributions in S-5; re-run FC-1, S-1 and balance.

## Evidence (`tools/analysis/results/e5_launch.csv`, v0.4.1 model — not M1 validation)
Capped presser (35 → 350) vs 35 presses: 47.1% / 51.0% (FC-1 passes only if the median is 35); vs 32: 65.8% / 91.0%; vs 30: 73.8% / 97.8%. Caps above a 35 median: 40 → 71.4% / 97.1%.

## Known issues flagged for the owner
- **Zero-tap / one-tap inversion:** resolved by the owner (OQ-LN-08, R1 `max(20, 10·n)`); 0, 1 and 2 presses now give the same 20 RPS.
- **Launch sensitivity (F-11) and accessibility (OQ-LN-09):** small press gaps are decisive under linear launch.
- Client input cannot prove a physical human press; macros reach the cap.

## Alternatives (historical)
Saturating curve (v0.3/v0.3.1, superseded by D-01), 12/10/8 presses/s caps, accuracy layer, server challenge windows, hold-to-charge (excluded).

## Revisit when
S-5 measured medians differ from 35; FC-1 fails.
