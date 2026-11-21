# ADR-014: Burst Finish model
- **Status:** Proposed (revised v0.3.1, 2026-11-21) — not approved

## Official facts (verified — DOC-BURST-001 §1)
Burst = parts (blade, ratchet, bit) detach and separate; 2 points; burst resistance depends on the bit; Burst Stopper engages on a strong shoot; Burst added "unpredictable battles"; simultaneous finishes = draw and restart. **No official numeric model exists.** (v0.2 cited an official "click together over and over" statement — not found on the page; removed.)

## Decision (proposed, original game design)
Hybrid **Lock Integrity** model with one canonical equation (DOC-BURST-001 §2.2): cumulative threshold-gated damage; threshold rises with current spin (burst-stopper analogue); `K_burst` (attacker, [1.0, 1.3]) and `K_guard` (defender, [0.65, 1.0]); `θ_up` in radians from the contact normal; **per-tick per-victim damage cap 49** and **critical burst only if L at the start of the tick ≤ 50** → a full-lock Bey cannot burst from one contact (proof §2.3 there); bounded seeded variance ±10%; 4-stage gauge. Candidate coefficients `T0 = 0.20, β = 2.0, c_b = 3, D_cap = 49` (v0.2: 0.95, 0.35, 6, no cap).

## Primary vs secondary
BURST primary [C]. OVER secondary [C, Brief §E1]. SPIN secondary and structurally required (official Spin Finish). XTREME optional (arena). DISCONNECT and time-limit rules TBD.

## Measured consequence (`tools/analysis/`, v0.3.1)
Burst share 14.9% (v0.2 reference) → 32.5% (v0.3.1 candidate). Seat-averaged Burst share: Attack–Attack 54.2%, Attack–Stamina 69.5%, Attack–Balance 59.1%, Attack–Defense 9.6%, Defense pairings 0–2%. One-contact damage for impacts up to N = 10⁶ is capped at 49.

## Alternatives
Pure threshold, pure durability, pure probability (DOC-BURST-001 §2.1).

## Revisit when
CHG-09 target not met in S-1; players perceive bursts as random.
