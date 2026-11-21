# Combat balance analysis bundle (design phase)

> **This is a design-analysis tool, not game code.** It is not part of the client, the Match Server or the Backend, and nothing in the game will import it. It exists so that every number in `docs/10-game-design/balancing-simulation-report.md` can be reproduced and re-checked (audit finding C-05).

## Scope — what the numbers mean
- **1-v-1 analytic Monte Carlo model only.** It applies the canonical equations of DOC-CMB-001 / DOC-BURST-001 / DOC-STAT-001 / DOC-LAUNCH-001 to an *average* contact process.
- It is **not** gameplay validation and **cannot** prove balance. In particular it says nothing reliable about: real 3D positions and steering, five-competitor FFA, the actual skill catalogue (no skills are modelled), Magic's real value, arena geometry.
- Analysis-only proxies (not part of the game formulas):

| Proxy | Stands in for | In the game |
|---|---|---|
| contact events ~ Poisson(h·dt), at most 1 per pair per 100 ms step | real collisions | physics engine contacts + 100 ms debounce (DOC-CMB-001 §4.0) |
| `v_norm = clamp(skill × u × (0.4 + 0.6·mobility), 0, 3)`, u ~ lognormal(mean 1, σ 0.30) | normalised contact speed | `v_norm = clamp(v_n / v_ref, 0, 3)` from physics |
| skill ~ Normal(1, 0.15) per player | steering skill (assumption A-14) | real joystick play |
| ring-out hazard with recoil | position-based OVER | physical ring-out |
| A(θ) = 1 | upward contact angle | DOC-BURST-001 §2.2 |

## How to reproduce
Requirements: Python ≥ 3.10, numpy ≥ 2.0. Results in `results/` were produced with Python 3.13.18 and numpy 2.5.3.
```bash
cd tools/analysis
python3 run_all.py
```
Runtime ≈ 1–2 minutes. Seeds are fixed in `run_all.py`; outputs are deterministic for a given numpy version.

## Files
| File | Content |
|---|---|
| `combat_model.py` | model implementation |
| `configs/v0.3.1-candidate.json` | **proposal** — spike S-1 starting coefficients and example archetype builds (not approved, not balanced) |
| `configs/v0.2-reference.json` | superseded v0.2 coefficients, re-run under the v0.3.1 model structure for comparison |
| `run_all.py` | experiments E1–E6 |
| `results/e1_advantage_table.csv` | S1–S9 advantage values |
| `results/e2_type_matrix_*.csv` | 16 ordered pairings (row seat vs column seat) |
| `results/e2_type_pairs_*.csv` | 10 unordered pairs, **seat-averaged** (used in the documents) |
| `results/e3_rps_vs_energy.csv` | outcome-level RPS influence vs Energy gap |
| `results/e4_magic_weight.csv` | equal-budget Magic tests (skills not modelled) |
| `results/e5_launch.csv` | zero/low presses, capped presser vs humans, cap options |
| `results/summary.json` | aggregates, environment, TC-023 check |

## Seeds
E2 type matrices: `101 + cell index` (candidate), `11 + cell index` (v0.2 reference); E3: 3/4/5; E4: 14 and 9; E5: 31/32 (low presses), 12/13 (capped presser). N = 4,000 duels per cell.
