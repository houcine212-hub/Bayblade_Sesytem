# ADR-015: Launch RPS model, fairness and validation
- **Status:** Proposed (revised v0.3.1, 2026-11-21) — not approved

## Decision (proposed)
- `RPS(n) = 20 + 130·(1 − e^(−n/19.0575))`, anchored at 5 presses = 50.000 RPS [C anchor]; 0 presses → 20.00 RPS.
- **Counted-press cap `r_cap` = measured median sustained touch rate** (provisional 7/s ⇒ `n_max = 35`, max 129.3 RPS) — CHG-13; replaces the v0.3 proposal of 12/s (`n_max = 60`, 144.42 RPS), which remains the alternative.
- Half-open window; edge + release counting; server timestamp bounds; regularity flags without automatic penalty.
- **Ranked gate (FR-186):** no ranked matchmaking or rating until FC-1 passes with S-5/S-1 data.

## Fairness evidence (`tools/analysis/results/e5_launch.csv`)
Capped presser vs median (35-press) player, Attack / Stamina mirror: 12/s → 68.9% / 93.6%; 10/s → 65.0% / 88.6%; 8/s → 55.1% / 71.0%; **median cap → 47.5% / 50.8%** (FC-1 ≤ 60% passes).

## Known limitations (accepted for friendly play; gated for ranked)
- Client input cannot prove a physical human press; a macro always reaches the cap.
- The launch-zone check is client-side.
- Below-median players stay disadvantaged (as against fast humans).
- The median cap lowers the skill ceiling: pressing faster than the median gives nothing.
- Spin-race matchups are very sensitive to small launch differences (F-11) — to be addressed in S-1.

## Alternatives
12/s / 10/s / 8/s caps; accuracy layer (moving sweet spot, evaluate in S-5); server challenge windows (rejected: automatable, latency-unfair); lower launch weight (with F-11); literal linear 10·n (unbounded); hold-to-charge (excluded by user).

## Revisit when
S-5 measures the real touch median and per-device distributions; FC-1 re-evaluated before any ranked feature.
