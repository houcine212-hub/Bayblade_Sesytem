# Theoretical Balancing & Simulation Report

| Document ID | DOC-BAL-001 | Version | 0.3.1 (audit correction, 2026-11-21) | Status | **Reproducible model outputs — not proof of balance.** All coefficient sets are proposals. |
|---|---|---|---|---|---|---|---|

Labels: **[RES]** research finding · **[MEAS]** number produced by `tools/analysis/` (reproducible) · **[REC]** recommendation (proposal) · **[PLAY]** needs real gameplay testing.

> **Scope (audit C-05):** every number below comes from a **1-v-1 analytic Monte Carlo model** (`tools/analysis/`, run `python3 run_all.py`). It is not gameplay validation. It does **not** model real 3D steering, five-competitor FFA, the actual skills, or Magic's real value. Do not use it as proof that Magic, skills or FFA are balanced. The v0.3 numbers published earlier came from the same model *before* the v0.3.1 burst-rule corrections and are superseded by this report.

## 1. Definitions (normative)
| Symbol | Definition | Range |
|---|---|---|
| `g` | `(E_A − E_B) / ((E_A + E_B)/2)`; ratio `E_A/E_B = (2+g)/(2−g)` | (−2, 2) |
| `r` | `(ω_A − ω_B) / ((ω_A + ω_B)/2)`, ω = **current** spin | (−2, 2) |
| `w(g)` | `0.15 + 0.45·exp(−(g/0.25)²)` | [0.15, 0.60] |
| `S_AB` | `(1 − w)·tanh(3g) + w·tanh(2.5r)`, `S_BA = −S_AB` | (−1, 1) |
Per-contact level: RPS share of the advantage is `w(g) ≥ 0.15`. Outcome level: change in win probability caused by a launch difference (measured, §6).

## 2. Model and reproducibility
- Equations: DOC-CMB-001 §4 (impact, resistance, profile matrix, recoil, spin loss), DOC-STAT-001 §5 (decay with movement cost), DOC-BURST-001 §2.2 (canonical burst rule incl. per-tick cap 49 and start-of-tick critical gate), Spin Finish < 8 RPS.
- Analysis proxies (not game formulas): contact events Poisson with 100 ms debounce; `v_norm` proxy from mobility × lognormal speed × skill factor; ring-out hazard with recoil; A(θ) = 1. Listed in `tools/analysis/README.md`.
- Launch presses ~ Normal(35, 8), rounded, clipped [0, n_max]; skill proxy ~ Normal(1, 0.15) (assumption A-14).
- Files: configs `tools/analysis/configs/*.json`; results `tools/analysis/results/*.csv|json`; environment: Python 3.13.18, numpy 2.5.3; N = 4000 duels per cell; seeds in the bundle README.
- Win rates are **seat-averaged** (both orders of each pairing).

## 3. Contradictions found in v0.2/v0.3 and their status
| ID | Contradiction | Status in v0.3.1 |
|---|---|---|
| C1 | ADR-013 bands are win rates/shares but v0.2 used a deterministic model | resolved: stochastic model, bands measured (§5.3) |
| C2 | Burst ≥ 40% vs v0.2 coefficients | v0.2 reference: BURST 14.9%; candidate 32.5%; target definition → CHG-09/D-10 |
| C3 | "Defense beats Attack" claimed in v0.2 | candidate: Defense beats Attack 85.0% |
| C4 | "+25% Energy" labels | labels show ratio and g |
| C5 | ABSORB rebound had no equation | recoil term (DOC-CMB-001 §4.3) |
| C6 | "RPS never irrelevant" vs 1.7-point outcome effect at g = 0.261 | open → decision D-17 |
| C7 | "No absolute counter" vs favoured matchups 85.0%–91.2% | open (AC-2) |
| C8 (audit C-02) | `N_ij` carried speed units; knockback ∝ v² | resolved: `v_norm`, linear knockback |
| C9 (audit C-03) | "no burst from one contact at full lock" not enforced | resolved: D_cap 49 + start-of-tick gate, proof in DOC-BURST-001 §2.3 |
| C10 (audit C-05) | numbers not reproducible | resolved: `tools/analysis/` bundle |

## 4. Advantage function — exact values (`e1_advantage_table.csv`)
| ID | E_A | E_B | E_A/E_B | g | ω_A | ω_B | r | w(g) | (1−w)·tanh(3g) | w·tanh(2.5r) | **S_AB** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | 60 | 60 | 1.000 | +0.0000 | 120 | 80 | +0.4000 | 0.6000 | +0.0000 | +0.4570 | **+0.4570** |
| S2 | 60 | 60 | 1.000 | +0.0000 | 100 | 95 | +0.0513 | 0.6000 | +0.0000 | +0.0765 | **+0.0765** |
| S3 | 66 | 60 | 1.100 | +0.0952 | 100 | 100 | +0.0000 | 0.5392 | +0.1282 | +0.0000 | **+0.1282** |
| S4 | 66 | 60 | 1.100 | +0.0952 | 80 | 120 | -0.4000 | 0.5392 | +0.1282 | -0.4107 | **-0.2825** |
| S5 | 78 | 60 | 1.300 | +0.2609 | 80 | 120 | -0.4000 | 0.3015 | +0.4570 | -0.2296 | **+0.2274** |
| S6 | 78 | 60 | 1.300 | +0.2609 | 60 | 140 | -0.8000 | 0.3015 | +0.4570 | -0.2906 | **+0.1664** |
| S7 | 54 | 66 | 0.818 | -0.2000 | 140 | 60 | +0.8000 | 0.3873 | -0.3291 | +0.3734 | **+0.0443** |
| S8 | 66 | 60 | 1.100 | +0.0952 | 70 | 110 | -0.4444 | 0.5392 | +0.1282 | -0.4338 | **-0.3056** |
| S9 | 80 | 50 | 1.600 | +0.4615 | 50 | 150 | -1.0000 | 0.1649 | +0.7365 | -0.1627 | **+0.5739** |

## 5. Type matrix — measured
### 5.1 v0.3.1 candidate, seat-averaged (`e2_type_pairs_v0.3.1.csv`)
| Pair X–Y | P(X wins) | P(Y wins) | Draw | Median duration | BURST | OVER | SPIN |
|---|---|---|---|---|---|---|---|
| Attack–Attack | 48.0% | 48.0% | 4.0% | 8.7 s | 54.2% | 41.8% | 0.0% |
| Attack–Defense | 14.8% | 85.0% | 0.2% | 48.5 s | 9.6% | 26.7% | 63.4% |
| Attack–Stamina | 89.1% | 10.2% | 0.8% | 13.7 s | 69.5% | 28.8% | 1.0% |
| Attack–Balance | 64.0% | 34.5% | 1.5% | 14.7 s | 59.1% | 39.1% | 0.3% |
| Defense–Defense | 49.9% | 49.9% | 0.2% | 100.2 s | 0.0% | 0.1% | 99.7% |
| Defense–Stamina | 8.7% | 91.2% | 0.1% | 95.6 s | 2.0% | 2.4% | 95.5% |
| Defense–Balance | 63.5% | 36.2% | 0.3% | 71.7 s | 0.0% | 3.8% | 95.9% |
| Stamina–Stamina | 49.8% | 49.8% | 0.4% | 98.5 s | 60.8% | 10.4% | 28.4% |
| Stamina–Balance | 53.3% | 46.1% | 0.6% | 58.4 s | 35.0% | 14.5% | 49.9% |
| Balance–Balance | 49.9% | 49.9% | 0.2% | 46.2 s | 54.0% | 16.0% | 29.8% |

Overall vs the other three types: **Attack 56.3%, Defense 52.5%, Stamina 51.8%, Balance 39.3%**. Finish shares (uniform 16-cell mix): **BURST 32.5%, OVER 18.7%, SPIN 48.1%, draw 0.7%**. Median of cell medians 53.3 s; shortest cell 8.7 s; longest 100.2 s; max draw 4.0%.

### 5.2 v0.2 reference (`e2_type_pairs_v0.2-reference.csv`)
Overall: Attack 76.4%, Defense 38.8%, Stamina 50.4%, Balance 34.4%; BURST 14.9%, OVER 22.2%, SPIN 61.6%; cell medians 13.0–152.0 s.

### 5.3 Acceptance check (ADR-013)
| Criterion | Target | v0.3.1 candidate | Result |
|---|---|---|---|
| AC-1 each type vs other types | 45–55% | 56.3% / 52.5% / 51.8% / 39.3% | **fail** (Attack high, Balance low) |
| AC-2 favoured matchups (seat-averaged) | 55–80% | A>S 89.1%, S>D 91.2%, D>A 85.0% | **fail** |
| AC-3 Burst metric | per D-10 (proposal M-1 ≥ 30%, M-2 most frequent in A–A, A–S, A–B) | M-1 32.5%; M-2 54.2% / 69.5% / 59.1% | pass under proposal (b); fail under NFR-070 as written (≥ 40%) |
| AC-4 cell medians 15–100 s; overall 30–90 s | | 8.7–100.2 s; overall 53.3 s | **fail** (A–A, A–S, A–B too short; D–D 100.3 s) / overall pass |
| AC-5 draws ≤ 5% | | max 4.0% | pass |
| AC-6 outcome RPS effect ≥ 10 points for g ≤ 0.20 | per D-17 | §6 | pass in both mirrors up to g = 0.18 |
| AC-7 Magic equal-budget shift 45–55% | needs real skills | §7 | not measurable (fails without skills) |
| AC-8 FFA type win share within ±5 points of expectation | five-competitor bot test | — | **not measurable in this model** (S-1) |

## 6. RPS influence vs Energy gap — outcome level (`e3_rps_vs_energy.csv`)
A's attributes scaled by f (capped at 100); fixed launches; swing = P(A wins | A 150, B 120) − P(A wins | A 120, B 150).

| Mirror | f | E_A | E_B | g | P(A) at 120/120 | P(A) 120 vs 150 | P(A) 150 vs 120 | **Swing (points)** |
|---|---|---|---|---|---|---|---|---|
| Attack | 1.00 | 56.25 | 56.25 | 0.000 | 48.8% | 18.9% | 79.2% | **60.3** |
| Attack | 1.05 | 59.06 | 56.25 | 0.049 | 62.6% | 23.8% | 82.7% | **58.9** |
| Attack | 1.10 | 61.88 | 56.25 | 0.095 | 74.3% | 35.2% | 84.6% | **49.4** |
| Attack | 1.15 | 64.69 | 56.25 | 0.140 | 82.0% | 53.6% | 86.2% | **32.6** |
| Attack | 1.20 | 67.0 | 56.25 | 0.174 | 85.5% | 68.2% | 87.4% | **19.2** |
| Attack | 1.30 | 70.5 | 56.25 | 0.225 | 88.3% | 81.3% | 89.4% | **8.1** |
| Balance | 1.00 | 56.5 | 56.5 | 0.000 | 50.4% | 2.0% | 97.8% | **95.8** |
| Balance | 1.05 | 59.33 | 56.5 | 0.049 | 77.2% | 3.8% | 98.7% | **94.9** |
| Balance | 1.10 | 62.15 | 56.5 | 0.095 | 92.2% | 10.0% | 99.3% | **89.3** |
| Balance | 1.15 | 64.97 | 56.5 | 0.140 | 98.0% | 32.1% | 99.5% | **67.4** |
| Balance | 1.20 | 67.8 | 56.5 | 0.182 | 99.4% | 68.0% | 99.8% | **31.8** |
| Balance | 1.30 | 73.45 | 56.5 | 0.261 | 99.7% | 98.1% | 99.9% | **1.7** |

Findings [MEAS]: the swing falls smoothly with g; at g ≈ 0.26 (Balance mirror) the stronger build wins 99.7% regardless of launch because all its physical attributes are 30% higher. At **equal** Energy the Balance mirror is decided almost entirely by launch (95.8 points) — see finding F-11.

## 7. Magic weight — equal attribute budget, skills NOT modelled (`e4_magic_weight.csv`)
| Magic weight in Energy | P(physical-shift 66/66/66/28 beats Balance 57/57/57/55) | P(High-Magic 75/40/35/75 beats Attack 85/45/40/55) |
|---|---|---|
| 0.0 | 91.5% | 24.3% |
| 0.3 | 87.1% | 29.1% |
| 0.5 | 84.8% | 31.6% |
| 0.6 | 83.5% | 32.6% |
| 0.7 | 82.6% | 33.6% |
| 0.8 | 81.5% | 34.4% |
| 1.0 | 79.4% | 36.0% |

Interpretation: in a skill-less model, moving points out of Magic is favourable at every weight; a higher weight reduces that advantage only slightly. **This does not show that any weight is fair for Magic** — that requires the real skills (audit H-04, AC-7).

## 8. Launch (`e5_launch.csv`)
| Case | n_max | Presses A | Presses B | P(A wins) Attack mirror | P(A wins) Stamina mirror |
|---|---|---|---|---|---|
| low presses | 60 | 0 | 35 | 3.7% | 0.1% |
| low presses | 60 | 1 | 35 | 6.2% | 0.1% |
| low presses | 60 | 3 | 35 | 10.1% | 0.2% |
| low presses | 60 | 5 | 35 | 13.1% | 0.2% |
| capped presser | 60 | 60 | 25 | 78.4% | 98.8% |
| capped presser | 60 | 60 | 30 | 74.3% | 97.9% |
| capped presser | 60 | 60 | 35 | 68.8% | 93.6% |
| capped presser | 60 | 60 | 45 | 57.3% | 77.1% |
| capped presser | 50 | 50 | 25 | 77.4% | 98.6% |
| capped presser | 50 | 50 | 30 | 71.7% | 96.3% |
| capped presser | 50 | 50 | 35 | 65.0% | 88.6% |
| capped presser | 50 | 50 | 45 | 51.6% | 63.0% |
| capped presser | 40 | 40 | 25 | 74.0% | 97.6% |
| capped presser | 40 | 40 | 30 | 65.4% | 89.4% |
| capped presser | 40 | 40 | 35 | 55.1% | 71.0% |
| capped presser | 35 | 35 | 25 | 70.1% | 94.6% |
| capped presser | 35 | 35 | 30 | 57.9% | 77.8% |
| capped presser | 35 | 35 | 35 | 47.5% | 50.8% |

With the cap at the median human rate (n_max = 35 when the median is 35 presses), a capped presser beats a median player 47.5% / 50.8% — the macro advantage over median-or-better players disappears; below-median players remain disadvantaged as they would be against a fast human (DOC-LAUNCH-001 §5).

## 9. Findings
| ID | Finding [MEAS] | Recommendation |
|---|---|---|
| F-1 | Official triangle directions hold (A>S, S>D, D>A) but too strongly (85–91%) | revisit in S-1 with real steering variance (AC-2) |
| F-2 | Balance archetype weakest (39.3%) — threshold-gated damage rewards concentrated attributes | Balance identity via lock/mass + Adapt; AC-1 |
| F-3 | Attack-involving cells end in 8.7–14.8 s median | lower contact damage or raise early threshold in S-1 (AC-4) |
| F-4 | Burst 32.5% overall; ≈ 0–10% in all Defense pairings | define metric (D-10); post-MVP opposite-spin burst |
| F-5 | Per-contact RPS weight ≥ 0.15 holds; outcome effect ≤ 2 points at g ≈ 0.26 | decision D-17 |
| F-6 | Magic cannot be evaluated without skills | keep Energy weight provisional (D-07) |
| F-7 | 12/s cap: capped presser beats a 7/s player 68.9% / 93.6% | median cap + ranked gate (CHG-13, D-04) |
| F-8 | Full-lock one-contact burst impossible after v0.3.1 rule (damage cap 49 verified for N up to 10⁶) | keep (TC-023) |
| F-9 | Zero presses → wins 3.7% / 0.1% | intended (D-03) |
| F-10 | v0.2 reference set fails every band (Attack 76.4%, Burst 14.9%) | superseded |
| F-11 (new) | **Spin-race matchups are extremely launch-sensitive**: Balance mirror 95.8-point swing at equal Energy; Stamina mirror 30 vs 35 presses (123.1 vs 129.3 RPS, −5%) → 77.8% | S-1: add real steering-dependent decay variance; consider lower `k_R` or a launch-independent spin floor; new open question OQ-CB-10 |

## 10. Needs real gameplay testing
Steering feel and variance, five-competitor FFA (AC-8), real skills and Magic (AC-7), burst frequency with physics, human press distributions per device (S-5), favoured-matchup strength (AC-2).
