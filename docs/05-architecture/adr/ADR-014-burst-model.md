# ADR-014: Burst Finish model
- **Status:** Proposed (revised v0.3, 2026-11-21) — not approved

## Official facts (verified — DOC-BURST-001 §1)
Burst = parts (blade, ratchet, bit) detach and separate; 2 points; burst resistance depends on the bit; Burst Stopper engages on a strong shoot; Burst added "unpredictable battles"; simultaneous finishes = draw and restart. **No official numeric model exists.** (v0.2 cited an official "click together over and over" statement — not found on the page; removed.)

## Decision (proposed, original game design)
Hybrid **Lock Integrity** model: cumulative threshold-gated damage; threshold rises with current spin (burst-stopper analogue); critical burst only once L ≤ 50; bounded seeded variance ±10%; 4-stage gauge. v0.3 candidate coefficients `T0 = 0.20, β = 2.0, c_b = 3` (v0.2: 0.95, 0.35, 6).

## Primary vs secondary
BURST primary [C]. OVER secondary [C, Brief §E1]. SPIN secondary and structurally required (official Spin Finish). XTREME optional (arena). DISCONNECT and time-limit rules TBD.

## Measured consequence
Burst share 14.8% (v0.2) → 34.9% (v0.3 candidate); Burst 56–72% of finishes in pairings with an Attack/Balance Bey, 0–3% in Defense-vs-Defense/Stamina. A wobble-weakened threshold variant changed the share by ≤ 1.4 points.

## Alternatives
Pure threshold, pure durability, pure probability (DOC-BURST-001 §2.1).

## Revisit when
CHG-09 target not met in S-1; players perceive bursts as random.
