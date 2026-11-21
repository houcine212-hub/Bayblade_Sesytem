# ADR-014: Burst Finish model
- **Status:** Proposed · **Date:** 2026-11-21
## Decision (proposed)
Hybrid: cumulative **Lock Integrity** (threshold-gated damage) + critical burst only when L ≤ 50 + bounded seeded variance ±10%; spin-dependent threshold (burst-stopper analogue). Details: `docs/10-game-design/burst-finish-spec.md`.
## Alternatives
Pure threshold, pure durability, pure probability (rejected for fairness/realism — see spec §2).
## Evidence
R-08, R-09, R-10, R-11, R-16.
## Revisit when
Burst share < 40% or > 70% after tuning; players perceive bursts as random (survey).
