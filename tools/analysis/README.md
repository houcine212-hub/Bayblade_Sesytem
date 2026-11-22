# Combat balance analysis bundle (design phase)

> **This is a design-analysis tool, not game code.** It is not part of the client, the Match Server or the Backend, and nothing in the game will import it. It exists so that every number in `docs/10-game-design/balancing-simulation-report.md` can be reproduced and re-checked (audit finding C-05).

## Scope — what the numbers mean
- **1-v-1 analytic Monte Carlo model only.** It applies the canonical equations of DOC-CMB-001 / DOC-BURST-001 / DOC-STAT-001 / DOC-LAUNCH-001 to an *average* contact process.
- It is **not** gameplay validation and **cannot** prove balance. In particular it says nothing reliable about: real 3D positions and steering, five-competitor FFA, the actual skill catalogue (no skills are modelled), Magic's real value, arena geometry.
- Analysis-only proxies (not part of the game formulas):

| Proxy | Stands in for | In the game |
|---|---|---|
| contact events ~ Poisson(h·dt), at most 1 per pair per 100 ms step | real collisions | physics engine contacts + 100 ms debounce (DOC-CMB-001 §2.3) |
| `v_norm = clamp(skill × u × (0.4 + 0.6·mobility), 0, 3)`, u ~ lognormal(mean 1, σ 0.30) | normalised contact speed | `v_norm = clamp(v_n / v_ref, 0, 3)` from physics |
| skill ~ Normal(1, 0.15) per player | steering skill (assumption A-14) | real joystick play |
| ring-out hazard with recoil | position-based OVER | physical ring-out |
| A(θ) = 1 | upward contact angle | DOC-BURST-001 §2.2 |

## How to reproduce
Requirements: Python ≥ 3.10, numpy ≥ 2.0. Results in `results/` (v0.4) were produced with Python 3.13.18 and numpy 2.5.3. `run_all.py` deletes and regenerates `results/`.
```bash
cd tools/analysis
python3 run_all.py
```
Runtime ≈ 1–2 minutes. Seeds are fixed in `run_all.py`; outputs are deterministic for a given numpy version.

## Files
| File | Content |
|---|---|
| `combat_model.py` | model implementation |
| `configs/v0.4-candidate.json` | **primary** — G0 decisions applied (D-01 linear launch 10 RPS/press, D-03 zero presses = 20 RPS, D-04 cap 35 presses, D-16 120 s limit with spin ranking); spin-rate coefficients re-expressed for the 350-RPS scale (see `scaling_note` in the file); **S-1 experimental starting values, not balanced (D-12)** |
| `configs/v0.3.1-candidate.json` | superseded (exponential launch curve), kept for comparison |
| `configs/v0.2-reference.json` | superseded v0.2 coefficients, re-run under the v0.3.1 model structure for comparison |
| `run_all.py` | experiments E1–E6 |
| `results/e1_advantage_table.csv` | S1–S9 advantage values |
| `results/e2_type_matrix_*.csv` | 16 ordered pairings (row seat vs column seat) |
| `results/e2_type_pairs_*.csv` | 10 unordered pairs, **seat-averaged** (used in the documents); `*_v0.4` is current |
| `results/e3_rps_vs_energy.csv` | D-17 test: 30-RPS launch difference (320 vs 350) vs Energy gap |
| `results/e3b_rps_vs_energy_relative.csv` | same with a 70-RPS difference (280 vs 350, r = 0.222 — the relative gap of the old 120-vs-150 test) |
| `results/e4_magic_weight.csv` | equal-budget Magic tests (skills not modelled) |
| `results/e5_launch.csv` | zero-vs-one-press paradox, low presses, capped presser vs humans (FC-1), higher caps |
| `results/summary.json` | aggregates, environment, TC-023 check |

## Seeds
E2 type matrices: `101 + cell index` (v0.4 and superseded v0.3.1), `11 + cell index` (v0.2 reference); E3: 3/4/5; E3b: 6/7; E4: 14 and 9; E5: 31/32 (zero/low presses), 12/13 (capped presser). N = 4,000 duels per cell.
