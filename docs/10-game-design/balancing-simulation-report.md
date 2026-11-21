# Theoretical Balancing & Simulation Report

| Document ID | DOC-BAL-001 | Version | 0.2 | Status | **Mathematical predictions — not proof of balance** |
|---|---|---|---|---|---|---|---|

## 1. Method
- A simplified **1-v-1 analytic duel model** (time step 0.1 s) applying the combat-spec equations with an average contact rate instead of real positions. Ring-out is approximated as a hazard probability (in the real game it is physical).
- Calculator: a throw-away analysis script kept outside the repository (no implementation code is committed in the design phase). Every equation and starting value it used is listed in the combat/burst/stats specs, so results are reproducible by hand or spreadsheet.
- Archetype example builds (Energy ≈ 56, not approved content):

| Build | ATK | DEF | STA | MAG | mass | mobility | lock | profile | Energy |
|---|---|---|---|---|---|---|---|---|---|
| Attack | 85 | 45 | 40 | 55 | 1.00 | 1.00 | 0.95 | SMASH | 56.3 |
| Defense | 40 | 85 | 50 | 50 | 1.15 | 0.35 | 1.15 | ABSORB | 56.6 |
| Stamina | 35 | 50 | 88 | 50 | 0.95 | 0.55 | 1.00 | ROUND | 56.1 |
| Balance | 57 | 57 | 57 | 55 | 1.00 | 0.70 | 1.00 | ROUND | 56.6 |

Labels: **[RES]** research finding · **[PRED]** model prediction · **[REC]** design recommendation · **[PLAY]** requires real gameplay testing.

## 2. Type matchups — equal Energy, equal launch (90 RPS)
| Matchup | Predicted winner / finish / time | Notes |
|---|---|---|
| Attack vs Attack | Mirror → simultaneous burst ~18 s | [PRED] deterministic mirror; real outcome decided by launch, steering, skill timing [PLAY] |
| Attack vs Defense | **Defense by SPIN, 42 s** | Attack exhausts spin; Defense lock barely touched [PRED] ✓ matches official tendency [RES R-01/R-02] |
| Attack vs Stamina | **Attack by BURST, 30 s** | ✓ official tendency |
| Defense vs Stamina | **Stamina by SPIN, 84 s** | ✓ official tendency |
| Defense vs Defense | Double spin-out ~94 s | Tie/time-limit rule needed (OQ-GP-04, OQ-GP-18) |
| Stamina vs Stamina | Double spin-out ~85 s | Launch RPS decides in reality |
| Balance(57) vs Attack | Attack by SPIN 28 s | |
| Balance(57) vs Defense | Defense by SPIN 65 s | |
| Balance(57) vs Stamina | **Balance** by SPIN 57 s | |
| Balance vs Balance | Mirror ~45 s | |

## 3. Balance sensitivity ("knife-edge") — key finding
| Balance attributes | vs Attack | vs Defense | vs Stamina |
|---|---|---|---|
| 56/56/56 | loses | loses | loses |
| 57/57/57 | loses | loses | **wins** |
| 58/58/58 | **wins** | **wins** | **wins** |
**F2 [PRED]:** +1 point on every attribute flips Balance from "worst" to "best". An all-rounder that is marginally above the specialists' *effective* values beats them all. **[REC]** (a) enforce the same attribute budget for every build tier; (b) keep Balance at or slightly below specialists' effective budget and give it identity through **Adapt** skill and lack of hard counters; (c) monitor Balance win-rate first in telemetry (NFR-071). Real-match variance (steering, launch) will soften the edge [PLAY].

## 4. RPS vs Energy (Attack mirror)
| Situation | Energy A vs B | Launch A vs B | Prediction |
|---|---|---|---|
| Equal Energy, big RPS gap | 56.3 vs 56.3 | 120 vs 80 | A wins by BURST 10.6 s — RPS decisive ✓ [C principle] |
| Equal Energy, small gap | 56.3 vs 56.3 | 100 vs 90 | A wins by BURST 13.1 s — even 10 RPS matters at parity ✓ |
| Moderate Energy lead (+10%) | 62.3 vs 56.3 | 80 vs 120 | **B** wins by BURST — moderate Energy cannot beat a 40-RPS deficit |
| Large Energy lead (+25%) | 68.7 vs 56.3 | 80 vs 120 | **A** wins by BURST 15.5 s — Energy dominates ✓ |
| Large Energy lead, extreme RPS gap | 68.7 vs 56.3 | 50 vs 150 | **B** wins by SPIN 11 s — RPS never irrelevant ✓ |

**F3 [PRED]:** In the first draft spin also scaled impact directly (√ω). Then RPS dominated even +25% Energy, violating the confirmed principle. **[REC] applied:** RPS enters impact only through S (single-channel rule).

## 5. Cross-type with launch swings
| Matchup | Equal 90/90 | Underdog launches 140 vs 60 | Favourite launches 140 vs 60 |
|---|---|---|---|
| Defense vs Attack | Defense (SPIN 42 s) | Attack wins (SPIN 24 s) | Defense (SPIN 23 s) |
| Stamina vs Defense | Stamina (SPIN 84 s) | Defense wins | Stamina |
| Attack vs Stamina | Attack (BURST 30 s) | Stamina wins (SPIN 21 s) | Attack (BURST 16 s) |
**F5 [PRED]:** an extreme launch gap (≈ 8 vs 50 presses) overturns every type matchup. With realistic human spreads (25–45 presses → 115–138 RPS, r ≈ 0.18) the type tendency mostly holds. **[REC]** keep k = 19.06; verify human press distributions in spike S-5 [PLAY].

## 6. Component configurations
| Build variant | vs Defense | vs Stamina | Finding |
|---|---|---|---|
| Standard Attack (mob 1.0, mass 1.0) | loses (SPIN) | wins (BURST 30 s) | baseline |
| Heavy Attack (mass 1.12, mob 0.75, lock 1.05) | loses (SPIN 48 s, slower) | wins by **SPIN** 42 s (not burst) | changes *finish type* → variety ✓ |
| Upper Attack, weak lock (lock 0.8, Pb ×1.2) | loses | — ; mirror vs standard Attack: **loses by BURST** | glass-cannon trade-off ✓ |

## 7. Magic
| MAG | Skill potency | Gauge fill | Rail Dash impact bonus | Energy contribution |
|---|---|---|---|---|
| 20 | ×0.88 | ×0.91 | +22% | 4.2 |
| 50 | ×1.00 | ×1.00 | +25% | 10.5 |
| 80 | ×1.12 | ×1.09 | +28% | 16.8 |
| 100 | ×1.20 | ×1.15 | +30% | 21.1 |
**F10 [PRED]:** Magic's direct skill effect is bounded (±20%). Its **indirect** effect through Energy (S function) is larger than its skill effect → see OQ-ST-02. High-Magic / low-physical builds are predicted weak in clashes but strong in skill timing [PLAY].

## 8. Dominant / weak combinations identified
| ID | Combination | Risk | Mitigation |
|---|---|---|---|
| D-1 | Balance slightly above budget | Dominant | Budget parity, telemetry (F2) |
| D-2 | Max-launch Attack | Dominant early if launch spread is wide | Curve compression, opening skill lockout |
| D-3 | Defense mirror | Stalemate / draws | Time limit + sudden-death rule (OQ-GP-18) |
| W-1 | Low-lock UPPER | Weak vs other attackers | Intended trade-off |
| W-2 | High-Magic, low-physical | Weak in clashes | Intended; skill identity |
| ? | 5-player FFA dynamics (third-party hits, kingmaking) | Unknown | **Not modelled** — playtest [PLAY] |

## 9. What still needs real gameplay testing
Steering feel and its effect on contact rate; perceived fairness of the launch across devices; burst frequency (target ≥ 40%); match length (target 30–90 s); 5-player chaos; skill timing value; whether the triangle emerges with real physics (spike S-1).
