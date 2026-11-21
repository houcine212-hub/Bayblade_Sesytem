# Burst Finish & Elimination Specification

| Document ID | DOC-BURST-001 | Version | 0.3 | Status | Burst = primary elimination **[C]**; Lock Integrity model and all numbers **[P]** (ADR-014) |
|---|---|---|---|---|---|---|---|

## 1. Official Burst mechanics (verified, DOC-RES-001 §2)
| # | Official fact | Quote / source |
|---|---|---|
| OB-1 | Definition | Burst Finish "occurs when the parts of the opponent's Bey detach and separate before your Bey. (such as the blade, ratchet, or bit)" — Regulation 6th ed. (O-2) |
| OB-2 | Timing | "The moment a Bey's parts detach and separate." First finish in time wins. (O-2) |
| OB-3 | Points | Burst Finish = 2 points (Over 2, Xtreme 3, Spin 1; first to 4). (O-2, O-4) |
| OB-4 | Burst resistance depends on parts | "Dash performance and burst resistance are depending on the type of bit." (O-1) |
| OB-5 | Strong launch protects | Cho-Z "Burst Stopper that activates upon a strong shoot to prevent bursting". (O-3) |
| OB-6 | Character of bursts | Burst Finish added "thrilling, unpredictable battles". (O-3) |
| OB-7 | Opposite-spin burst tactic | "low-speed burst … to burst an opponent's Beyblade with the opposite spin". (O-3) |
| OB-8 | Staged burst state in an official game | XONE "Burst Gauge … changes in stages according to the Bey's condition". (O-5) |
| OB-9 | Simultaneous finishes | "considered a draw, and the battle will be restarted". (O-2) |

**Not official:** any numeric threshold, damage accumulation, durability value, or probability. The spring/teeth wear explanation is secondary (fan sources, R-11). The v0.2 claim that Takara Tomy describes tops "clicking together over and over" before bursting was **not found** on the cited page and has been removed (DOC-RES-001 §5).

## 2. Our proposed model — "Lock Integrity" (original game design) [P]
### 2.1 Options compared
| Option | Official fit | Fairness | Verdict |
|---|---|---|---|
| Single-impact threshold | OB-1 (parts separate on a hit) | predictable; one-shots feel unfair | partial |
| Cumulative durability | not stated officially; plausible from wear (secondary R-11) and OB-8's staged gauge | readable | good |
| Pure probability per hit | OB-6 ("unpredictable") | hurts competitive fairness | rejected |
| **Hybrid: cumulative Lock Integrity + critical burst after weakening + bounded seeded variance** | OB-1, OB-4 (lock from parts), OB-5 (spin-dependent threshold), OB-6 (bounded variance), OB-8 (stages) | readable, no one-shots at full lock | **recommended** |

### 2.2 Equations (proposal)
Each Bey starts with `L = 100`.
```
Threshold      T_j = T0 · lock_strength_j · (1 + β · ω_j / 150)                    (OB-5 analogue: faster spin → harder to burst)
Burst load     B_ij = N_ij · Pb(prof_i, prof_j) · A(θ) · K_burst_skill
Angle factor   A(θ) = 1 + 0.5 · sin(θ_up)
Damage         D = c_b · max(0, B_ij − T_j) · (1 + ε),   ε ~ U[−0.10, +0.10], server RNG seeded per match
L_j ← L_j − D
BURST  if  L_j ≤ 0   or   (B_ij ≥ 2.5 · T_j  and  L_j ≤ 50)
```
| Coefficient | v0.2 set | v0.3 candidate | Effect (measured, DOC-BAL-001) |
|---|---|---|---|
| T0 | 0.95 | **0.20** | low base threshold … |
| β | 0.35 | **2.0** | … but strongly spin-dependent: at 140 RPS T = 0.57·lock, at 20 RPS T = 0.25·lock |
| c_b | 6 | **3** | slower accumulation |
| Burst share (uniform matchup mix) | 14.8% | **34.9%** | |
`lock_strength` comes mostly from CORE and TIP parts (official OB-4: burst resistance depends on the bit).

### 2.3 Burst gauge UI (inspired by OB-8)
| L | Stage |
|---|---|
| 100–76 | SECURE |
| 75–51 | LOOSENING |
| 50–26 | CRITICAL (critical bursts possible) |
| 25–1 | DANGER |
Opponent visibility of stages: OQ-BU-03 (proposal: visible).

## 3. Primary vs secondary elimination
### 3.1 Primary — BURST [C]
Burst Finish is the **primary elimination mechanic** (BR-015): the featured finish (UI, effects, event feed, highest emphasis in skills and parts design). **Open measurement question:** in the analysis model with a uniform matchup mix, Burst is 34.9% of eliminations and SPIN is the most frequent (46.2%); Burst dominates in pairings with an Attack- or Balance-type Bey (56–72%) and almost never occurs in Defense-vs-Defense/Stamina pairings (0–3%). See CHG-09 for the decision on what "primary" must mean numerically.

### 3.2 Secondary eliminations
| Finish | Condition (server) | Official basis | Status | Can it be switched off? |
|---|---|---|---|---|
| **OVER** (ring-out) | Bey fully leaves the arena or settles in an over pocket ≥ 0.5 s and cannot return | Over Finish (O-2) | **[C]** — Brief §E1: "When a player's spinning top exits the arena, that player is eliminated." | Only by changing a confirmed decision |
| **SPIN** | `spin_rps < 8` (game stop threshold) | Spin Finish: spin "becomes zero" (O-2) | **[P] required** — a stopped top cannot stay in the match; without SPIN a match could never end without a time limit | No (structural); the threshold value is tunable |
| **XTREME** | Over via a dedicated Xtreme zone | Xtreme Finish (O-2) | **[P] optional**, arena-dependent (OQ-CB-03) | Yes — arena without Xtreme zone |
| **DISCONNECT** | Grace period expired (if that rule is chosen) | none | **[TBD]** OQ-GP-05 | Yes |
| **TIME LIMIT** | Not an elimination; ends the match (sudden-death/placement rule TBD) | none | **[TBD]** OQ-GP-18 | Yes |

### 3.3 Same-tick eliminations
Official rule: draw and **restart** (OB-9). Online FFA proposal: eliminated competitors share the placement, no restart (OQ-GP-04) — a deliberate deviation needing approval.

## 4. Elimination flow (authoritative)
1. Detection in the server tick → `{userId, finishType, tick, creditedTo?}` (credit: opponent who dealt the last lock damage/knockback within 3 s).
2. `S2C_Eliminated` (reliable) to all; burst visual = client presentation of that event.
3. Eliminated peer → SPECTATOR (`S2C_RoleChanged`); inputs ignored.
4. Remaining competitors continue; ≤ 1 remaining → ENDED; result with finish types to Backend (SQ-07).
Sequence: `../02-uml/sequence/SQ-05-elimination.puml`.
