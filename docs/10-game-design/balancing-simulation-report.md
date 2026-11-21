# Theoretical Balancing & Simulation Report

| Document ID | DOC-BAL-001 | Version | 0.3 (correction pass, 2026-11-21) | Status | **Measured model outputs — not proof of balance.** All coefficient sets are proposals. |
|---|---|---|---|---|---|---|---|

Labels: **[RES]** research finding · **[MEAS]** number measured from the analysis model (actual output) · **[REC]** design recommendation (proposal) · **[PLAY]** needs real gameplay testing.

## 1. Definitions (normative for all documents)
For two Beys A and B at the moment of a contact:

| Symbol | Definition | Range | Notes |
|---|---|---|---|
| `E_A`, `E_B` | Energy of each build (stats spec §4) | 0–100 | static per match |
| **`g`** | **`g = (E_A − E_B) / ((E_A + E_B) / 2)`** — symmetric relative Energy difference | (−2, +2) | `g(A,B) = −g(B,A)`. Conversion to ratio: `E_A/E_B = (2 + g)/(2 − g)`; e.g. ratio 1.10 ⇔ g = 0.0952; ratio 1.30 ⇔ g = 0.2609 |
| `ω_A`, `ω_B` | **current** spin in RPS (equals launch RPS at battle start, then decays) | 0–150 | not the Stamina attribute |
| **`r`** | **`r = (ω_A − ω_B) / ((ω_A + ω_B) / 2)`** — symmetric relative spin difference | (−2, +2) | evaluated every contact |
| `w(g)` | RPS weight `= w_min + (w_max − w_min)·exp(−(g/σ)²)` | [0.15, 0.60] | symmetric in g |
| `S_AB` | Advantage `= (1 − w)·tanh(k_E·g) + w·tanh(k_R·r)` | (−1, +1) | `S_BA = −S_AB` |

Two levels must not be confused:
- **Per-contact level:** the share of the advantage that comes from RPS is `w(g)`, guaranteed ≥ 0.15 by construction.
- **Outcome level:** how much a launch difference changes the *probability of winning*. This is measured (§6) and can saturate when one Bey is much stronger overall.

## 2. Analysis model (method)
- **What it implements:** the equations of DOC-CMB-001 §3–4 (advantage, impact, resistance with profile matrix and ABSORB factor, knockback-proxy, spin loss), DOC-STAT-001 §5 (decay with movement cost), DOC-BURST-001 §3 (threshold, cumulative damage, critical burst, ±10% variance), SPIN finish < 8 RPS. Same-step double elimination = draw.
- **Monte Carlo:** each duel run is independent; contact count per 0.1 s step ~ Poisson(h·dt); impact speed factor ~ lognormal (σ 0.30); launch presses ~ Normal(35, 8) rounded and clipped to [0, 60] unless a fixed RPS is stated; **player-skill proxy** per run and player ~ Normal(1.0, 0.15) clipped [0.5, 1.5] multiplying impact speed (stands in for steering skill — assumption A-14).
- **Not modelled:** real 3D positions and steering, 5-player FFA dynamics, real skills (a generic symmetric skill approximation changed results by < 1 point and is not used for conclusions), arena geometry (ring-out is a hazard proxy).
- **Reproducibility:** throw-away analysis script kept outside the repository (design phase rule: no code committed). Seeds: type matrices `seed = 101 + pairing index` (N = 4,000 per pairing); RPS–Energy experiments seeds 3/4/5 (N = 4,000); Magic tests 9/14; launch tests 12/13/31/32. All coefficients are listed in §2.1, so results can be reproduced.

### 2.1 Coefficient sets (all proposals)
| Coefficient | Meaning | v0.2 set | **v0.3 candidate** | Why changed |
|---|---|---|---|---|
| `T0` | base burst threshold | 0.95 | **0.20** | v0.2 produced Burst 14.8% (C2) |
| `β` | spin-dependence of threshold (burst-stopper analogue) | 0.35 | **2.0** | fresh, fast-spinning tops resist; weakened tops burst before spinning out |
| `c_b` | lock damage per unit excess load | 6 | **3** | keeps Attack matchups from ending in 2–4 s |
| `c_d` | natural decay | 0.55 | **0.85** | Defense/Stamina matches were 135–150 s |
| `c_move` | movement spin cost (decay × (1 + c_move·mobility)) | 0.5 | **1.0** | attackers pay for mobility (official: Defense strong vs Attack) |
| `ρ_rec` | **new** recoil: attacker receives `ρ_rec·N_ij·mobility_i` knockback (×2.5 vs ABSORB) | — (absent) | **0.15** | equation missing in v0.2; ABSORB "rebounds attackers" had no implementation (C5) |
| `p_ko` | ring-out hazard scale (proxy) | 0.02 | 0.02 | — |
| `c_s`, `α`, `w_max`, `w_min`, `σ`, `k_E`, `k_R`, `crit` | — | 1.6, 0.5, 0.60, 0.15, 0.25, 3.0, 2.5, 2.5 | unchanged | — |
| Balance example build | content | lock 1.00, mass 1.00, mobility 0.70 | **lock 1.15, mass 1.08, mobility 0.75** | official Balance identity "improves your ability to repel different opponents" (O-1) |

Example archetype builds (content examples, not approved): Attack 85/45/40/55 (SMASH, mob 1.0, mass 1.0, lock 0.95) · Defense 40/85/50/50 (ABSORB, mob 0.35, mass 1.15, lock 1.15) · Stamina 35/50/88/50 (ROUND, mob 0.55, mass 0.95, lock 1.0, friction 0.9) · Balance 57/57/57/55 (ROUND). Energy (wM 0.8): 56.32 / 56.58 / 56.05 / 56.58.

## 3. Contradictions found and how they are resolved
| ID | Contradiction (v0.2) | Evidence [MEAS] | Resolution (v0.3) |
|---|---|---|---|
| **C1** | ADR-013 defines acceptance bands as **win rates** (45–55%) and a **Burst share** (≥ 40%), but the v0.2 report used a **deterministic** model that can only produce a single winner per pairing — the bands were never measured, yet the report marked results "✓". | — | Monte Carlo model; every band now measured (§5). |
| **C2** | "Burst is the primary elimination" (BR-015, NFR-070 ≥ 40%) vs v0.2 coefficients. | v0.2 set, spec-consistent model: **BURST 14.8%**, OVER 22.9%, SPIN 61.1% | v0.3 candidate raises Burst to **34.9%**; still < 40% → decision CHG-09 / OQ-CB-06. |
| **C3** | v0.2 report: "Defense beats Attack by SPIN at 42 s". Spec-consistent model with v0.2 coefficients: **Attack beats Defense 55.2%**. The v0.2 numbers came from a model that did not implement the published profile matrix. | v0.2 set: Attack 77.0% overall | v0.3: Defense beats Attack **82.8%**; Attack overall **57.3%**. |
| **C4** | Energy-gap labels: "+25% Energy" rows were actually ratio **1.19–1.22** (g = 0.174–0.198) because attributes cap at 100. | recomputed | Labels now state ratio and g (§4, §6). |
| **C5** | ABSORB "rebounds attackers" (CLS spec) and "Defense → Attack counter" (CMB §5) had no equation. | — | Recoil term `ρ_rec` added to CMB spec §4.3. |
| **C6** | ADR-013 claims RPS is "never irrelevant"; at outcome level a 30-RPS swing changes win probability by only **1.8 points** in a Balance mirror at g = 0.26. | §6 | Requirement split into per-contact guarantee (holds) and outcome-level target for g ≤ 0.20 (holds: ≥ 19.7 points); large-gap behaviour is a decision (OQ-CB-08). |
| **C7** | FR-215 "no absolute counter" vs favoured matchups of **90%** (A>S, S>D) in the v0.3 candidate. | §5 | Proposed band for favoured matchups 55–80%; not yet met → open balancing item for spike S-1. |

## 4. Advantage function — exact values (recalculated)
| ID | Scenario | E_A | E_B | E_A/E_B | g | ω_A | ω_B | r | w(g) | (1−w)·tanh(3g) | w·tanh(2.5r) | **S_AB** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Equal Energy, RPS 120 vs 80 | 60 | 60 | 1.000 | +0.0000 | 120 | 80 | +0.4000 | 0.6000 | +0.0000 | +0.4570 | **+0.4570** |
| S2 | Equal Energy, RPS 100 vs 95 | 60 | 60 | 1.000 | +0.0000 | 100 | 95 | +0.0513 | 0.6000 | +0.0000 | +0.0765 | **+0.0765** |
| S3 | Ratio 1.10, equal RPS 100 | 66 | 60 | 1.100 | +0.0952 | 100 | 100 | +0.0000 | 0.5392 | +0.1282 | +0.0000 | **+0.1282** |
| S4 | Ratio 1.10, RPS 80 vs 120 | 66 | 60 | 1.100 | +0.0952 | 80 | 120 | −0.4000 | 0.5392 | +0.1282 | −0.4107 | **−0.2825** |
| S5 | Ratio 1.30, RPS 80 vs 120 | 78 | 60 | 1.300 | +0.2609 | 80 | 120 | −0.4000 | 0.3015 | +0.4570 | −0.2296 | **+0.2274** |
| S6 | Ratio 1.30, RPS 60 vs 140 | 78 | 60 | 1.300 | +0.2609 | 60 | 140 | −0.8000 | 0.3015 | +0.4570 | −0.2906 | **+0.1664** |
| S7 | Ratio 0.818, RPS 140 vs 60 | 54 | 66 | 0.818 | −0.2000 | 140 | 60 | +0.8000 | 0.3873 | −0.3291 | +0.3734 | **+0.0443** |
| S8 | Ratio 1.10, RPS 70 vs 110 | 66 | 60 | 1.100 | +0.0952 | 70 | 110 | −0.4444 | 0.5392 | +0.1282 | −0.4338 | **−0.3056** |
| S9 | Ratio 1.60, RPS 50 vs 150 | 80 | 50 | 1.600 | +0.4615 | 50 | 150 | −1.0000 | 0.1649 | +0.7365 | −0.1627 | **+0.5739** |

`w(g)`: 0 → 0.6000 · 0.05 → 0.5824 · 0.10 → 0.5335 · 0.15 → 0.4640 · 0.20 → 0.3873 · 0.25 → 0.3155 · 0.30 → 0.2566 · 0.40 → 0.1848 · 0.60 → 0.1514 · ≥ 1.0 → 0.1500 (limit). The S values are identical to v0.2 to four decimals; only labels changed (C4).

## 5. Type matrix — measured
### 5.1 v0.2 coefficients (spec-consistent model, N = 2,000/pairing, launch SD 6, no skill proxy) [MEAS]
Overall win rate vs other types: **Attack 77.0%, Defense 39.8%, Stamina 48.1%, Balance 35.7%**. Finishes: **BURST 14.8%**, OVER 22.9%, SPIN 61.1%, draw 1.2%. Attack beats Defense 55.2%; Defense–Defense median 149.6 s; Defense–Stamina 135.2 s. → fails every ADR-013 band.

### 5.2 v0.3 candidate (N = 4,000/pairing) [MEAS]
P(row Bey wins) — row vs column; draw shares in brackets where > 1%:

| Row \ Column | Attack | Defense | Stamina | Balance |
|---|---|---|---|---|
| **Attack** | 0.471 (draw 0.049) | 0.157 | 0.902 | 0.644 (draw 0.021) |
| **Defense** | 0.828 | 0.501 | 0.095 | 0.632 |
| **Stamina** | 0.098 (draw 0.011) | 0.900 | 0.515 | 0.506 |
| **Balance** | 0.329 (draw 0.019) | 0.367 | 0.486 | 0.483 |

| Pairing | Median duration | BURST | OVER | SPIN | Draw |
|---|---|---|---|---|---|
| Attack–Attack | 7.6 s | 0.56 | 0.39 | 0.00 | 0.05 |
| Attack–Defense | 47.0 s | 0.12 | 0.27 | 0.61 | 0.00 |
| Attack–Stamina | 12.2 s | 0.72 | 0.26 | 0.01 | 0.01 |
| Attack–Balance | 13.1 s | 0.61 | 0.37 | 0.00 | 0.02 |
| Defense–Defense | 99.2 s | 0.00 | 0.00 | 1.00 | 0.00 |
| Defense–Stamina | 94.1 s | 0.03 | 0.02 | 0.95 | 0.00 |
| Defense–Balance | 70.3 s | 0.00 | 0.04 | 0.96 | 0.00 |
| Stamina–Stamina | 93.6 s | 0.67 | 0.11 | 0.22 | 0.00 |
| Stamina–Balance | 54.8 s | 0.38 | 0.14 | 0.47 | 0.01 |
| Balance–Balance | 43.4 s | 0.64 | 0.15 | 0.21 | 0.00 |

Overall: **Attack 57.3%, Defense 51.9%, Stamina 50.4%, Balance 39.8%** (vs other types). Finishes over the 16 ordered pairings: **BURST 34.9%, OVER 18.1%, SPIN 46.2%, draw 0.9%**, timeout 0%.
With the v0.3 Energy recommendation (Magic weight 1.0 instead of 0.8, same seeds): Attack 57.5%, Defense 51.8%, Stamina 50.2%, Balance 40.2%; BURST 35.0%, OVER 18.1%, SPIN 46.1% — all differences ≤ 0.4 points.

### 5.3 Acceptance check
| Criterion | Source | v0.2 set | v0.3 candidate | Result |
|---|---|---|---|---|
| Each type 45–55% vs other types | ADR-013 / NFR-071 | 77 / 40 / 48 / 36 | 57.3 / 51.9 / 50.4 / 39.8 | **fail** (Attack high, Balance low) |
| Burst ≥ 40% of eliminations (uniform matchup mix) | NFR-070 | 14.8% | 34.9% | **fail** |
| Median match length 30–90 s | NFR-072 | 78.8 s (median of pairing medians) | 50.9 s | pass (both) |
| Every pairing median 15–100 s | proposed v0.3 | 11–150 s | 7.6–99.2 s | **fail** (Attack–Attack 7.6 s, Attack–Stamina 12.2 s, Attack–Balance 13.1 s) |
| Favoured matchups 55–80% ("tendency") | proposed v0.3 (FR-215) | A>S 93%, S>D 88%, D>A 48% | A>S 90.2%, S>D 90.0%, D>A 82.8% | **fail** (too strong) |
| Draws ≤ 5% per pairing | proposed v0.3 | ≤ 4.4% | ≤ 4.9% | pass |
| Triangle direction (A>S, S>D, D>A) | official tendency [RES O-1] | D>A fails | all hold | pass |

**Conclusion [MEAS]:** the v0.3 candidate is materially better than v0.2 but **does not meet all bands**. Four parameter searches (162 + 288 + 144 + 216 = 810 combinations of the global coefficients, N = 300–500 per pairing) found no combination meeting all bands at once: raising Burst share shortens Attack matchups; slowing bursts returns finishes to SPIN. In this model the structural limits are (a) Defense/Stamina pairings rarely exceed any burst threshold, (b) threshold-gated damage favours concentrated Attack over even builds. These are inputs for spike S-1 with real physics, not reasons to finalise numbers now.

## 6. RPS influence vs Energy gap — outcome level [MEAS]
Mirror builds; A's attributes scaled by f (capped at 100); fixed launches; "RPS swing" = P(A wins | A 150, B 120) − P(A wins | A 120, B 150) in percentage points.

| Mirror | f | E_A | E_B | ratio | g | P(A) equal RPS 120/120 | P(A) A=120 B=150 | P(A) A=150 B=120 | **RPS swing** |
|---|---|---|---|---|---|---|---|---|---|
| Attack | 1.00 | 56.32 | 56.32 | 1.000 | 0.000 | 0.483 | 0.179 | 0.799 | **62.0** |
| Attack | 1.05 | 59.13 | 56.32 | 1.050 | 0.049 | 0.624 | 0.227 | 0.833 | **60.6** |
| Attack | 1.10 | 61.95 | 56.32 | 1.100 | 0.095 | 0.742 | 0.340 | 0.853 | **51.2** |
| Attack | 1.15 | 64.76 | 56.32 | 1.150 | 0.140 | 0.823 | 0.532 | 0.867 | **33.5** |
| Attack | 1.20 | 67.05 | 56.32 | 1.191 | 0.174 | 0.858 | 0.682 | 0.878 | **19.7** |
| Attack | 1.30 | 70.45 | 56.32 | 1.251 | 0.223 | 0.889 | 0.821 | 0.896 | **7.5** |
| Balance | 1.00 | 56.58 | 56.58 | 1.000 | 0.000 | 0.505 | 0.019 | 0.978 | **95.9** |
| Balance | 1.10 | 62.24 | 56.58 | 1.100 | 0.095 | 0.918 | 0.105 | 0.992 | **88.7** |
| Balance | 1.20 | 67.89 | 56.58 | 1.200 | 0.182 | 0.994 | 0.694 | 0.998 | **30.3** |
| Balance | 1.30 | 73.55 | 56.58 | 1.300 | 0.261 | 0.997 | 0.981 | 0.999 | **1.8** |

Findings: (1) RPS influence **decreases smoothly** with the Energy gap — the confirmed principle holds at outcome level up to g ≈ 0.2. (2) At g ≈ 0.26 in the Balance mirror the stronger Bey wins 99.7% regardless of launch — RPS becomes practically irrelevant at outcome level, **because all its physical attributes are 30% higher**, not because of S. (3) At equal Energy the Balance mirror is decided almost entirely by launch (95.9 points) — launch may be *too* decisive between equal Bey's [PLAY].

Softer Energy steepness `k_E` (same seeds): k_E 3.0 → 2.0 → 1.5 raises the swing at large gaps only modestly: Attack mirror g = 0.223: 7.5 → 12.5 → 16.8 points; Balance mirror g = 0.261: 1.8 → 4.1 → 7.7 points. **[REC]** keep k_E = 3.0 and define the outcome-level requirement for g ≤ 0.20 (OQ-CB-08); optional Energy-band matchmaking for ranked play.

## 7. Balance-type sensitivity [MEAS]
v0.2 found a ±1-point knife-edge in a deterministic model. With the stochastic model and v0.3 global coefficients (N = 1,000), Balance's overall win rate by content variant: lock 1.00/mass 1.00/mob 0.70 → **29.9%**; lock 1.10 → 30.7%; lock 1.10 + mass 1.05 → 36.1%; lock 1.15 + mass 1.05 + mob 0.75 → 40.5%; lock 1.15 + mass 1.08 + mob 0.75 → **43.6%** (before the skill proxy). Balance remains the weakest archetype: threshold-gated burst damage rewards concentrated attributes. **[REC]** give Balance its identity through properties (lock, mass) and the Adapt skill, then verify in spike S-1.

## 8. Magic weight [MEAS] (details in stats spec §4.5)
- Equal budget (226 points): Balance 57/57/57/55 vs physical-shift 66/66/66/28 — P(physical-shift wins) = 0.915 (wM 0.0), 0.872 (0.3), 0.845 (0.5), 0.832 (0.6), 0.823 (0.7), **0.811 (0.8)**, **0.789 (1.0)**.
- Equal budget (225): Attack 85/45/40/55 vs High-Magic 75/40/35/75 — P(High-Magic wins) = 0.227 (0.0), 0.301 (0.5), 0.315 (0.6), **0.333 (0.8)**, **0.351 (1.0)**.
→ Moving points out of Magic is strongly favourable at **every** tested weight; lowering the weight makes it worse. Magic's value must come from skills (not modelled).

## 9. Launch [MEAS] (details in launch spec)
- Zero presses (20.0 RPS) vs a 35-press player (129.3 RPS): wins 3.5% (Attack mirror, median 1.9 s) and 0.1% (Stamina mirror, median 8.7 s). 1 press (26.6 RPS): 6.4% / 0.1%. 5 presses (50.0 RPS): 12.2% / 0.2%.
- Capped presser (60 presses = 144.42 RPS) vs human: 25 presses → wins 78.9% (Attack mirror) / 98.7% (Stamina mirror); 35 → 68.6% / 93.3%; 45 → 57.0% / 76.6%; 55 → 49.5% / 58.2%.
- Cap options vs a 35-press human (Stamina / Attack mirror): 12/s (cap RPS 144.4) 93.3% / 68.6%; 10/s (140.6) 88.2% / 64.2%; 8/s (134.1) 70.9% / 55.0%; 12/s with RPS_max 130 (127.6) 87.0% / 63.3%; 10/s with RPS_max 130 (125.4) 82.4% / 59.9%.

## 10. Burst-share options tested [MEAS]
| Option | BURST | SPIN | Note |
|---|---|---|---|
| v0.3 candidate | 34.9% | 46.2% | — |
| + wobble-weakened threshold (T × Stab(ω)^p), p = 1 / 2 / 4 | 35.4 / 35.8 / 36.3% | 45.9 / 45.5 / 45.0% | negligible; Defense pairings still ≤ 4% burst |
| Search best (Burst-weighted objective) | 45–49% | ~36% | but Attack matchups end in 2–4 s and Attack mirror draws 31% → rejected |
So "≥ 40% Burst over a uniform matchup mix" conflicts with "reasonable match length" in this model → decision CHG-09.

## 11. Dominant / weak combinations
| ID | Combination | Measured | Status |
|---|---|---|---|
| D-1 | Attack archetype | 57.3% overall | Too strong; [PLAY] check with real steering |
| D-2 | Capped launch presser (macro or elite tapper) | 68.6–98.7% vs typical humans | Integrity limitation (launch spec §7) |
| D-3 | Physical-heavy builds over Magic | 79–92% at equal budget | Requires skill tuning |
| W-1 | Balance archetype | 39.8% | Weak; content + Adapt skill |
| W-2 | Zero/low-press players | ≤ 12% | Intended consequence |
| — | 5-player FFA (third-party hits, kingmaking) | not modelled | [PLAY] |

## 12. Needs real gameplay testing
Steering feel and its real variance (replaces the skill proxy), 5-player FFA, real skills and Magic value, burst frequency with real physics, human press distributions per device (spike S-5), whether favoured matchups land in 55–80%.
