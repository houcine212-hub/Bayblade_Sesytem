# Theoretical Balancing & Simulation Report

| Document ID | DOC-BAL-001 | Version | 0.4 (G0 decisions integrated, 2026-11-21) | Status | **Reproducible model outputs — not proof of balance, not M1 validation.** Coefficients are S-1 experimental starting values (D-12). |
|---|---|---|---|---|---|---|---|

Labels: **[RES]** research finding · **[MEAS]** produced by `tools/analysis/` (reproducible) · **[REC]** recommendation · **[PLAY]** needs real gameplay/engine testing.

> **Scope:** 1-v-1 analytic Monte Carlo model only (`tools/analysis/`, `python3 run_all.py`). It does **not** model real 3D steering, five-competitor FFA, actual skills, Magic's real value, or real device input. **No M1 test has been run.** The v0.3.1 results (exponential 20→150-RPS launch curve) are **not applicable** to the owner-selected linear launch and are kept only as a superseded comparison.

## 1. Definitions (normative)
| Symbol | Definition | Range |
|---|---|---|
| `g` | `(E_A − E_B) / ((E_A + E_B)/2)`; ratio `E_A/E_B = (2+g)/(2−g)` | (−2, 2) |
| `r` | `(ω_A − ω_B) / ((ω_A + ω_B)/2)`, ω = current spin | (−2, 2) |
| `w(g)` | `0.15 + 0.45·exp(−(g/0.25)²)` | [0.15, 0.60] |
| `S_AB` | `(1 − w)·tanh(3g) + w·tanh(2.5r)` | (−1, 1) |

## 2. Model (v0.4 configuration)
- **Launch (D-01/D-03/D-04):** `RPS = 10 × n` for n ≥ 1, `20` for n = 0, n ≤ 35 → 10–350 RPS. Presses ~ Normal(35, 8), rounded, clipped [0, 35] — **assumption**: the real median and spread come from spike S-5.
- **Spin scale:** Absolute spin-rate coefficients re-expressed for the 350-RPS launch scale: c_d, c_s and wobble multiplied by kappa = 350/150 from v0.3.1; burst-threshold reference omega_ref = 350 RPS. Stop threshold kept at 8 RPS (< 10 RPS one-press launch). Displayed RPS is NOT converted.
- **Time limit (D-16):** 120 s; survivors ranked by current spin; exact ties = draw (finish `TIME_LIMIT`).
- **Same tick (D-11):** simultaneous last eliminations = draw.
- Equations: DOC-CMB-001 §4 and DOC-BURST-001 §2.2 (cap 49, start-of-tick gate). Proxies listed in `tools/analysis/README.md`.
- Environment: Python 3.13.18, numpy 2.5.3; N = 4000 duels per cell; seeds in the bundle README; win rates seat-averaged.

## 3. Contradictions and open issues
| ID | Issue | Status in v0.4 |
|---|---|---|
| C1–C5, C8–C10 | resolved in v0.3/v0.3.1 (see v0.3.1 correction log) | resolved |
| C6 / **C11** | D-17 (b) outcome requirement with a **30-RPS** difference | **fails under the linear launch** for g ≳ 0.13–0.17 (§6); passes with a relative 70-RPS (r = 0.22) difference → owner decision OQ-CB-12 |
| C7 | favoured matchups vs 55–80% band | A>S 86.3%, S>D 80.8%, D>A 79.5% — open (AC-2) |
| **C12 (new)** | zero-tap / one-tap paradox (D-01 + D-03): 0 presses → 20 RPS beats 1 press → 10 RPS | measured 98.6% / 99.6% (§8) → owner decision OQ-LN-08; rules unchanged |
| **C13 (new)** | linear launch amplifies launch sensitivity (F-11) | 32 vs 35 presses → 91.0% in the Stamina mirror (§8) |

## 4. Advantage function on the 350-RPS scale (`e1_advantage_table.csv`)
S depends only on g and r, so it is scale-free; scenarios re-expressed with v0.4 launch values.

| ID | E_A | E_B | E_A/E_B | g | ω_A | ω_B | r | w(g) | (1−w)·tanh(3g) | w·tanh(2.5r) | **S_AB** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | 60 | 60 | 1.000 | +0.0000 | 350 | 250 | +0.3333 | 0.6000 | +0.0000 | +0.4094 | **+0.4094** |
| S2 | 60 | 60 | 1.000 | +0.0000 | 350 | 320 | +0.0896 | 0.6000 | +0.0000 | +0.1321 | **+0.1321** |
| S3 | 66 | 60 | 1.100 | +0.0952 | 300 | 300 | +0.0000 | 0.5392 | +0.1282 | +0.0000 | **+0.1282** |
| S4 | 66 | 60 | 1.100 | +0.0952 | 250 | 350 | -0.3333 | 0.5392 | +0.1282 | -0.3679 | **-0.2397** |
| S5 | 78 | 60 | 1.300 | +0.2609 | 250 | 350 | -0.3333 | 0.3015 | +0.4570 | -0.2057 | **+0.2513** |
| S6 | 78 | 60 | 1.300 | +0.2609 | 150 | 350 | -0.8000 | 0.3015 | +0.4570 | -0.2906 | **+0.1664** |
| S7 | 54 | 66 | 0.818 | -0.2000 | 350 | 150 | +0.8000 | 0.3873 | -0.3291 | +0.3734 | **+0.0443** |
| S8 | 66 | 60 | 1.100 | +0.0952 | 220 | 350 | -0.4561 | 0.5392 | +0.1282 | -0.4392 | **-0.3110** |
| S9 | 80 | 50 | 1.600 | +0.4615 | 100 | 350 | -1.1111 | 0.1649 | +0.7365 | -0.1636 | **+0.5729** |

## 5. Type matrix — measured (v0.4)
### 5.1 Seat-averaged pairs (`e2_type_pairs_v0.4.csv`)
| Pair X–Y | P(X wins) | P(Y wins) | Draw | Median duration | BURST | OVER | SPIN | TIME_LIMIT |
|---|---|---|---|---|---|---|---|---|
| Attack–Attack | 48.5% | 48.5% | 3.1% | 8.5 s | 56.0% | 40.7% | 0.2% | 0.0% |
| Attack–Defense | 20.2% | 79.5% | 0.3% | 50.0 s | 14.6% | 28.9% | 56.2% | 0.0% |
| Attack–Stamina | 86.3% | 13.0% | 0.7% | 13.9 s | 66.6% | 30.5% | 2.1% | 0.0% |
| Attack–Balance | 60.1% | 38.8% | 1.2% | 14.6 s | 58.7% | 39.5% | 0.7% | 0.0% |
| Defense–Defense | 50.0% | 50.0% | 0.1% | 109.8 s | 0.0% | 0.1% | 66.3% | 33.5% |
| Defense–Stamina | 19.1% | 80.8% | 0.0% | 106.7 s | 6.1% | 4.2% | 74.0% | 15.8% |
| Defense–Balance | 61.3% | 38.6% | 0.2% | 77.9 s | 0.0% | 5.7% | 94.1% | 0.0% |
| Stamina–Stamina | 50.0% | 50.0% | 0.0% | 99.5 s | 57.0% | 10.1% | 6.8% | 26.1% |
| Stamina–Balance | 51.9% | 47.8% | 0.4% | 57.1 s | 36.1% | 17.2% | 46.3% | 0.0% |
| Balance–Balance | 49.9% | 49.9% | 0.2% | 46.3 s | 63.9% | 16.8% | 19.0% | 0.0% |

Overall vs the other three types: **Attack 55.9%, Defense 53.4%, Stamina 48.8%, Balance 42.0%**. Finish shares (uniform 16-cell mix): **BURST 33.8%, OVER 20.0%, SPIN 39.9%, TIME_LIMIT 5.7%, draw 0.6%**. Median of cell medians 53.3 s; shortest 8.5 s; longest 109.8 s; max draw 3.1%.

### 5.2 Superseded comparisons
- v0.3.1 (exponential curve, not applicable to D-01): Attack 56.3%, Defense 52.5%, Stamina 51.8%, Balance 39.3%; BURST 32.5%.
- v0.2 reference: Attack 76.4%, Defense 38.8%, Stamina 50.4%, Balance 34.4%; BURST 14.9%.

### 5.3 Acceptance criteria AC-1…AC-9 (D-13: failed or unmeasured = not passing)
| Criterion | Target | v0.4 analytic result | Result |
|---|---|---|---|
| AC-1 type vs other types | 45–55% | 55.9% / 53.4% / 48.8% / 42.0% | **fail** (Attack high, Balance low) |
| AC-2 favoured matchups | 55–80% | A>S 86.3%, S>D 80.8%, D>A 79.5% | **fail** (D>A now inside) |
| AC-3 Burst (D-10) | M-1 ≥ 30%; M-2 most frequent in A→A, A→S, A→B | M-1 33.8%; M-2 56.0% / 66.6% / 58.7% | pass (model only) |
| AC-4 durations | cells 15–100 s; overall 30–90 s | 8.5–109.8 s; overall 53.3 s | **fail** (Attack cells short; Defense–Defense 109.8 s, Defense–Stamina 106.7 s) |
| AC-5 draws | ≤ 5% per cell | max 3.1% | pass |
| AC-6 D-17 (b) | w ≥ 0.15 and ≥ 10-point outcome effect of a 30-RPS difference for \|g\| ≤ 0.20 | per-contact holds; outcome 6.3 / 2.8 / 3.9 points at g = 0.174 / 0.182 / 0.135 | **fail as written** (passes with relative variant, §6) |
| AC-7 Magic with real skills | 45–55% | 72.7% without skills | **not measured** |
| AC-8 FFA type shares | ±5 points | — | **not measured** (needs S-1 FFA bots) |
| AC-9 FC-1 launch fairness | ≤ 60% | capped (35) vs 35: 47.1% / 51.0%; vs 32: 65.8% / 91.0% | passes **only if the real median is 35** (S-5 not run) |

## 6. D-17 — outcome effect of launch differences vs Energy gap
### 6.1 As written: 30-RPS difference, 320 vs 350 (`e3_rps_vs_energy.csv`)
| Mirror | f | E_A | E_B | g | P(A) at 350/350 | P(A) 320 vs 350 | P(A) 350 vs 320 | **Swing (points)** |
|---|---|---|---|---|---|---|---|---|
| Attack | 1.00 | 56.25 | 56.25 | 0.000 | 48.5% | 30.0% | 67.2% | **37.1** |
| Attack | 1.05 | 59.06 | 56.25 | 0.049 | 62.1% | 41.9% | 75.4% | **33.5** |
| Attack | 1.10 | 61.88 | 56.25 | 0.095 | 73.3% | 57.8% | 80.2% | **22.3** |
| Attack | 1.15 | 64.69 | 56.25 | 0.140 | 81.4% | 71.6% | 83.7% | **12.1** |
| Attack | 1.20 | 67.0 | 56.25 | 0.174 | 84.6% | 79.3% | 85.7% | **6.3** |
| Attack | 1.30 | 70.5 | 56.25 | 0.225 | 87.8% | 85.0% | 87.8% | **2.8** |
| Balance | 1.00 | 56.5 | 56.5 | 0.000 | 50.5% | 10.9% | 88.5% | **77.5** |
| Balance | 1.05 | 59.33 | 56.5 | 0.049 | 76.5% | 29.2% | 95.8% | **66.6** |
| Balance | 1.10 | 62.15 | 56.5 | 0.095 | 92.0% | 59.6% | 98.2% | **38.6** |
| Balance | 1.15 | 64.97 | 56.5 | 0.140 | 97.9% | 85.7% | 99.2% | **13.5** |
| Balance | 1.20 | 67.8 | 56.5 | 0.182 | 99.3% | 96.8% | 99.6% | **2.8** |
| Balance | 1.30 | 73.45 | 56.5 | 0.261 | 99.7% | 99.7% | 99.8% | **0.1** |
| Stamina | 1.00 | 55.75 | 55.75 | 0.000 | 51.3% | 8.8% | 90.2% | **81.5** |
| Stamina | 1.05 | 58.54 | 55.75 | 0.049 | 84.2% | 36.4% | 97.7% | **61.3** |
| Stamina | 1.10 | 61.33 | 55.75 | 0.095 | 97.4% | 77.9% | 99.0% | **21.1** |
| Stamina | 1.15 | 63.81 | 55.75 | 0.135 | 99.2% | 95.6% | 99.5% | **3.9** |
| Stamina | 1.20 | 65.5 | 55.75 | 0.161 | 99.5% | 97.7% | 99.7% | **1.9** |
| Stamina | 1.30 | 68.88 | 55.75 | 0.211 | 99.8% | 99.7% | 99.8% | **0.1** |

### 6.2 Relative variant: 70-RPS difference, 280 vs 350, r = 0.222 (`e3b_rps_vs_energy_relative.csv`)
| Mirror | f | g | P(A) 280 vs 350 | P(A) 350 vs 280 | **Swing (points)** |
|---|---|---|---|---|---|
| Attack | 1.00 | 0.000 | 18.4% | 79.7% | **61.3** |
| Attack | 1.10 | 0.095 | 35.7% | 84.2% | **48.5** |
| Attack | 1.15 | 0.140 | 55.1% | 85.9% | **30.7** |
| Attack | 1.20 | 0.174 | 69.0% | 87.2% | **18.3** |
| Attack | 1.30 | 0.225 | 81.2% | 89.7% | **8.5** |
| Balance | 1.00 | 0.000 | 2.3% | 98.0% | **95.7** |
| Balance | 1.10 | 0.095 | 11.4% | 99.3% | **87.9** |
| Balance | 1.15 | 0.140 | 35.4% | 99.6% | **64.2** |
| Balance | 1.20 | 0.182 | 70.2% | 99.8% | **29.5** |
| Balance | 1.30 | 0.261 | 98.9% | 99.9% | **1.0** |
| Stamina | 1.00 | 0.000 | 0.9% | 99.0% | **98.1** |
| Stamina | 1.10 | 0.095 | 16.2% | 99.7% | **83.4** |
| Stamina | 1.15 | 0.135 | 51.7% | 99.9% | **48.2** |
| Stamina | 1.20 | 0.161 | 70.8% | 99.9% | **29.0** |
| Stamina | 1.30 | 0.211 | 92.6% | 100.0% | **7.4** |

## 7. Magic weight — equal budget, skills NOT modelled (`e4_magic_weight.csv`)
| Magic weight | P(physical-shift 66/66/66/28 beats Balance 57/57/57/55) | P(High-Magic 75/40/35/75 beats Attack 85/45/40/55) |
|---|---|---|
| 0.0 | 83.2% | 28.5% |
| 0.5 | 76.4% | 34.3% |
| 0.8 | 74.2% | 36.9% |
| 1.0 | 72.7% | 38.5% |

These tests cannot show Magic parity (D-07 provisional, AC-7).

## 8. Launch (`e5_launch.csv`)
| Case | n_max | A presses (RPS) | B presses (RPS) | P(A wins) Attack mirror | P(A wins) Stamina mirror |
|---|---|---|---|---|---|
| zero_vs_one_press | 35 | 0 (20) | 1 (10) | 98.6% | 99.6% |
| low_press_vs_median | 35 | 0 (20) | 35 (350) | 1.1% | 0.0% |
| low_press_vs_median | 35 | 1 (10) | 35 (350) | 0.0% | 0.0% |
| low_press_vs_median | 35 | 2 (20) | 35 (350) | 1.1% | 0.0% |
| low_press_vs_median | 35 | 3 (30) | 35 (350) | 2.3% | 0.0% |
| low_press_vs_median | 35 | 5 (50) | 35 (350) | 5.4% | 0.1% |
| capped_presser_vs_human | 35 | 35 (350) | 20 (200) | 83.3% | 99.3% |
| capped_presser_vs_human | 35 | 35 (350) | 25 (250) | 81.2% | 99.1% |
| capped_presser_vs_human | 35 | 35 (350) | 28 (280) | 78.0% | 98.8% |
| capped_presser_vs_human | 35 | 35 (350) | 30 (300) | 73.8% | 97.8% |
| capped_presser_vs_human | 35 | 35 (350) | 32 (320) | 65.8% | 91.0% |
| capped_presser_vs_human | 35 | 35 (350) | 35 (350) | 47.1% | 51.0% |
| higher_cap_vs_median35 | 40 | 40 (400) | 35 (350) | 71.4% | 97.1% |
| higher_cap_vs_median35 | 50 | 50 (500) | 35 (350) | 80.5% | 98.9% |
| higher_cap_vs_median35 | 60 | 60 (600) | 35 (350) | 81.9% | 99.2% |

## 9. Findings
| ID | Finding [MEAS] | Recommendation / owner question |
|---|---|---|
| F-1 | Triangle directions hold; A>S and S>D still too strong | S-1 with real steering variance (AC-2) |
| F-2 | Balance weakest (42.0%) | Balance identity via lock/mass + Adapt (AC-1) |
| F-3 | Attack cells end in 8.5–14.6 s median | lower early contact damage / raise early threshold in S-1 (AC-4) |
| F-4 | BURST 33.8% overall (signature finish, not globally most frequent — SPIN 39.9%) | D-10 adopted as initial target |
| F-5 | D-17 as written fails under linear launch | OQ-CB-12: absolute vs relative threshold |
| F-6 | Magic not evaluable without skills | D-07 provisional |
| F-7 | FC-1 passes only if the measured median equals the cap | S-5 measurement; re-run |
| F-8 | Full-lock guarantee holds (damage 49 for N up to 10⁶) | verify in S-1 (D-14) |
| F-9 | **Zero/one-tap paradox**: 0 presses beats 1 press 98.6% / 99.6% | OQ-LN-08 (recommended R1: RPS = max(20, 10·n)) |
| F-10 | Time limit decides 33.5% of Defense–Defense, 26.1% of Stamina–Stamina, 15.8% of Defense–Stamina cells | review spin ranking in five-player tests (D-16) |
| F-11 | **Launch sensitivity amplified by linear launch:** Stamina mirror 32 vs 35 presses → 91.0%; Balance/Stamina mirrors at equal Energy: 3-press swing 77.5 / 81.5 points | OQ-CB-10 (S-1); accessibility OQ-LN-09 |

## 10. Needs real testing (M1)
S-5 real input distributions per device (Android touch, keyboard, gamepad) → cap and FC-1; S-1 physics with spin as a scalar at 60 Hz, FFA bots (AC-8), real skills (AC-7), boundary tests of the burst rule; re-run of every table above with measured inputs.
