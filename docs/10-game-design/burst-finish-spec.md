# Burst Finish & Elimination Specification

| Document ID | DOC-BURST-001 | Version | 0.2 | Status | Burst = primary elimination [C]; model [P] (ADR-014) |
|---|---|---|---|---|---|---|---|

## 1. Research basis
Repeated clicking impacts lead to a burst (R-08, official); burst rates vary by top (R-09, official); a strong launch can engage burst protection (R-10, official); burst resistance comes from lock/spring parts and tooth wear (R-11, secondary); the official game XONE shows a staged gauge leading to burst (R-16, official). Official finish types: Spin, Over, Burst, Xtreme (R-05).

## 2. Model options
| Option | Pros | Cons | Fit |
|---|---|---|---|
| Deterministic single-impact threshold | Predictable | Ignores cumulative clicking; one-shot bursts feel unfair | Partial |
| Component-specific durability (cumulative) | Matches "click over and over" | Purely deterministic → mirrors are identical | Good |
| Pure probability per hit | Captures "rates vary" | Feels random; hurts competitive fairness | Poor |
| **Hybrid: cumulative Lock Integrity + capped single-hit critical + bounded seeded variance** | Faithful + fair + readable | More parameters | **Recommended** |

## 3. Recommended hybrid model
Each Bey starts the match with `L = 100` (Lock Integrity, "burst gauge").
```
Threshold      T_j  = T0 · lock_strength_j · (1 + β · ω_j / 150)            T0 = 0.95, β = 0.35   (strong spin protects, R-10)
Burst load     B_ij = N_ij · Pb(prof_i, prof_j) · A(θ) · K_burst_skill
Angle factor   A(θ) = 1 + 0.5 · sin(θ_up)   θ_up = upward contact angle (hits from below)
Damage         D    = c_b · max(0, B_ij − T_j) · (1 + ε),  ε ∈ [−0.10, +0.10]  (server RNG, seeded per match)   c_b = 6 (start value)
L_j ← L_j − D
BURST when  L_j ≤ 0
   OR  (B_ij ≥ 2.5·T_j  AND  L_j ≤ 50)       "critical burst" only after the lock is already weakened
```
- Relative velocity enters through `v_n` in N; RPS through S and T; Energy through S; Defense through R; attack through I; configuration through lock, profile, mass, height.
- No burst from impacts below the threshold → light contacts never burst.
- A Bey at full lock **cannot be one-shot** (fairness).
- Persistent part wear across matches: **not in MVP** (would create repair economy; OQ-BU-02).

### 3.1 Burst gauge UI stages (inspired by R-16)
| L | Stage | UI |
|---|---|---|
| 100–76 | SECURE | green |
| 75–51 | LOOSENING | yellow |
| 50–26 | CRITICAL (critical bursts possible) | orange, pulsing |
| 25–1 | DANGER | red |
Whether opponents see each other's stage: OQ-BU-03 (proposal: yes).

## 4. All finish types [P — CHG-04]
| Finish | Condition (server) | Inspiration | Eliminates? |
|---|---|---|---|
| **BURST** (primary) | L ≤ 0 or critical burst | R-05, R-08 | Yes |
| **OVER** | Top fully crosses arena boundary or settles in an over pocket for ≥ 0.5 s | R-05 (Over Finish); v0.1 ring-out rule | Yes |
| **XTREME** | Over via the special Xtreme zone (if arena has one) | R-05 | Yes (score bonus only) |
| **SPIN** | `spin_rps < 8` | R-05 | Yes |
Design target (NFR-070): BURST ≥ 40% of eliminations across all matches; tuned via `c_b`, `T0`, `β`.

## 5. Elimination flow (authoritative)
1. Detection in the server tick → elimination record `{userId, finishType, tick, creditedTo?}` (credit: opponent who dealt the last lock damage/knockback within 3 s).
2. Same-tick eliminations share a placement (R-06 analogue; OQ-GP-04 proposal).
3. `S2C_Eliminated` (reliable) to all; the burst visual (parts separating) is client-side presentation of that event.
4. Eliminated peer → SPECTATOR role (`S2C_RoleChanged`); inputs ignored.
5. Remaining competitors continue; when ≤ 1 remain → ENDED; result with finish types sent to Backend (SQ-07).
Sequence: `../02-uml/sequence/SQ-05-elimination.puml`.
