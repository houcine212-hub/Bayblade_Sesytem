# Combat Interaction Specification (opponent-relative model)

| Document ID | DOC-CMB-001 | Version | 0.4 (G0 decisions integrated) | Status | Principles [C]; equation **structure decided under owner delegation (D-12, D-18)**; all coefficients **S-1 experimental starting values** — not balanced; pending M1 verification |
|---|---|---|---|---|---|---|---|

v0.4 changes (G0 D-01, D-04, D-12, D-17, D-18): spin is an authoritative scalar on the 10–350 RPS scale (§2.4); absolute spin coefficients re-expressed for that scale (§4.9); D-17 results under the linear launch (§3.3); v0.4 matchup numbers (§5). v0.3.1 changes (audit C-02, C-04): units and normalisation; contact events and aggregation; mobility factor only as analysis proxy; linear knockback; canonical burst equation in DOC-BURST-001 §2.2; worked examples. All measured numbers: `tools/analysis/` (DOC-BAL-001).

## 1. Principles
- [C] A Bey's performance depends on **its opponent's characteristics**, not only its own stats.
- [C] Similar Energy → RPS differences strongly matter. Large Energy gap → RPS matters progressively less, **never completely irrelevant**; smooth transitions. (How "never irrelevant" is measured is decision D-17.)
- [C] No simplistic rules ("Attack always beats Defense").
- [P] Everything is evaluated per **contact event**, per pair, on the Match Server at the fixed tick (60 Hz). In a five-competitor FFA each contact is a pair interaction.
- Nothing here is an official Beyblade formula (official sources give none — DOC-RES-001 §3).

## 2. Symbols, units and normalisation
### 2.1 Units
| Quantity | Symbol | Unit | Notes |
|---|---|---|---|
| Position, distance | x | m (1 game unit = 1 m) | arena size is content data |
| Contact normal | n̂ | unit vector from i to j | from the physics engine |
| Relative normal speed | `v_n = (v_i − v_j)·n̂` | m/s | > 0 when approaching |
| Reference contact speed | `v_ref` | m/s | content parameter; proposal **1.0 m/s**, calibrated in S-1 so a typical Attack contact has `v_norm ≈ 1–1.5` |
| Normalised contact speed | `v_norm = clamp(v_n / v_ref, 0, 3)` | dimensionless | upper clamp bounds extreme physics glitches |
| Minimum effective speed | `v_min = 0.05·v_ref` | m/s | `v_n ≤ v_min` (resting, sliding or separating) ⇒ **no impact effects** |
| Mass property | `mass` | dimensionless (relative to `m_ref`) | physics mass = `mass × m_ref`; only ratios enter formulas |
| Attributes | ATK, DEF, STA, MAG | 0–100, dimensionless | |
| Spin | ω | RPS (rotations/s) | current spin; launch range 10–350 RPS (20 for zero presses), D-01/D-03/D-04 |
| Lock Integrity | L | lock points, 0–100 | |
| Normalised impact | `N_ij` | dimensionless | ≈ `Pk` at parity (§4.6) |
| Knockback | Δv | m/s | velocity change along the normal |
| Coefficients | `c_s` RPS · `c_d` RPS/s · `c_b` lock points · `k_kb`, `α`, `ρ_rec`, `T0`, `β`, `k_E`, `k_R` dimensionless | | |

### 2.2 Normative definitions (identical in all documents)
```
rel(a, b) = (a − b) / ((a + b) / 2)            range (−2, +2), rel(b, a) = −rel(a, b)
g = rel(E_i, E_j)        Energy gap            E_i/E_j = (2 + g)/(2 − g)
r = rel(ω_i, ω_j)        current-spin gap      equals the launch gap at battle start
```

### 2.3 Contact event and aggregation (new)
- A **contact event** is a physics contact *begin* between Beys i and j with `v_n > v_min`. The same pair cannot create another contact event for **100 ms (6 ticks)** — debounce against multi-tick contact reports.
- Each contact event is resolved once, in **both** directions (i → j and j → i), using values from the **start of the tick** (S, ω, L, Stab).
- If several contact events hit the same Bey in one tick (FFA), their effects are **summed**, processed in a deterministic order (ascending pair id), with the per-tick lock-damage cap of DOC-BURST-001 §2.2.


### 2.4 Spin as an authoritative gameplay quantity (D-04)
`spin_rps` is a server-authoritative **scalar state** per Bey. It drives decay, stability, burst threshold, the advantage function and outcomes. The 3D rigid body is **not** physically rotated at 350 RPS (5.83 revolutions per 60 Hz tick would alias); the physics body may use a nominal angular velocity for gyroscopic feel, and clients render a visually capped/blurred spin. The displayed RPS equals the authoritative value (no hidden rescaling). This is a design approach **to prototype in S-1**, not a validated result.
## 3. Advantage function S (RPS–Energy model) [C principle / P formula — ADR-013]
```
w(g)  = w_min + (w_max − w_min) · exp(−(g/σ)²)
S_ij  = (1 − w) · tanh(k_E · g) + w · tanh(k_R · r)      ∈ (−1, +1),  S_ji = −S_ij
```
`w_max = 0.60, w_min = 0.15, σ = 0.25, k_E = 3.0, k_R = 2.5` (proposal).

| g | 0 | 0.05 | 0.10 | 0.15 | 0.20 | 0.25 | 0.30 | 0.40 | 0.60 | ≥ 1.0 |
|---|---|---|---|---|---|---|---|---|---|---|
| w(g) | 0.6000 | 0.5824 | 0.5335 | 0.4640 | 0.3873 | 0.3155 | 0.2566 | 0.1848 | 0.1514 | 0.1500 |

### 3.1 Where RPS acts
| Channel | Attenuated by Energy gap? |
|---|---|
| Advantage S in impact (§4.1) | **Yes** — weight w(g) |
| Spin reservoir → Spin Finish | No (physical) |
| Stability `Stab(ω)` below ω_wob (58.33 RPS) | No (physical) |
| Burst threshold `T(ω)` (β) | No (burst-stopper analogue) |

### 3.2 Numerical scenarios
S1–S9 with g, r, w and both terms: DOC-BAL-001 §4 (`results/e1_advantage_table.csv`).

### 3.3 Outcome-level behaviour (measured, `results/e3_rps_vs_energy.csv`)
Linear launch (v0.4), **D-17 test as written — 30-RPS launch difference (320 vs 350, r = 0.09)**, `results/e3_rps_vs_energy.csv`: Attack mirror 37.1 points at g = 0 → 22.3 at g = 0.095 → 12.1 at g = 0.140 → **6.3 at g = 0.174**; Balance mirror 77.5 → 38.6 → 13.5 → **2.8 at g = 0.182**; Stamina mirror 81.5 → 21.1 (g = 0.095) → **3.9 at g = 0.135**. → **D-17 option (b) fails as written** for g ≳ 0.13–0.17. With a **70-RPS difference (280 vs 350, r = 0.22 — the relative gap of the old v0.3.1 test)**, `results/e3b_rps_vs_energy_relative.csv`: Attack 18.3 points at g = 0.174, Balance 29.5 at g = 0.182, Stamina 29.0 at g = 0.161 → passes up to |g| ≈ 0.2. Cause: under the linear launch, 30 RPS is only ~9% of a typical launch (it was ~22% under the old curve). **Owner decision OQ-CB-12:** keep D-17 in absolute RPS (and accept failure / retune), or restate it relatively (e.g. 7 presses or r ≥ 0.2). Not changed unilaterally.

## 4. Per-contact effects (pair i → j) [P]
### 4.1 Impact and resistance (game formula)
```
I_ij = v_norm · (0.5 + ATK_i/100) · √mass_i · Pk(prof_i, prof_j) · (1 + α·S_ij) · K_atk_i          α = 0.5
R_j  = (0.5 + DEF_j/100) · √mass_j · Stab(ω_j) · Abs(prof_j) · K_def_j
Stab(ω) = min(1, 0.45 + 0.55·ω/ω_wob),   ω_wob = 58.33 RPS (v0.4; v0.3.1: 25 RPS)
N_ij = I_ij / R_j                                                                                    dimensionless
```
`K_atk_i`, `K_def_j` = product of active skill modifiers on impact / resistance (1.0 when no skill is active; caps in DOC-SKILL-001 §4).
**Correction v0.3.1:** v0.3 multiplied `I_ij` by `(0.4 + 0.6·mobility_i)`. In the game, `v_n` from physics already reflects how fast a top moves, so that factor would double-count mobility. It remains **only** as the analysis-model proxy for `v_norm` (tools/analysis/README.md).

### 4.2 Profile matrix (knockback factor Pk / burst factor Pb), proposed values
| attacker ↓ / defender → | SMASH | UPPER | ABSORB | ROUND |
|---|---|---|---|---|
| SMASH | 1.0 / 1.0 | 1.0 / 1.0 | 0.85 / 0.85 | 1.1 / 0.95 |
| UPPER | 0.85 / 1.2 | 0.9 / 1.1 | 0.8 / 1.0 | 0.9 / 1.25 |
| ABSORB | 0.8 / 0.8 | 0.8 / 0.8 | 0.7 / 0.7 | 0.8 / 0.8 |
| ROUND | 0.9 / 0.9 | 0.9 / 0.9 | 0.8 / 0.8 | 0.85 / 0.85 |
UPPER row only if `height_i ≤ height_j`; otherwise SMASH row. `Abs(ABSORB) = 1.15`, others 1.0.

### 4.3 Knockback and recoil (velocity changes, m/s)
```
Δv_j (along +n̂)  = k_kb · N_ij · v_ref · mass_i / (mass_i + mass_j)
Δv_i (along −n̂)  = k_kb · ρ_rec · N_ij · mobility_i · v_ref · (2.5 if prof_j = ABSORB else 1)
```
`k_kb = 0.6`, `ρ_rec = 0.15` (proposal). Impulse applied by physics = physics mass × Δv. Knockback is now **linear** in contact speed (through `N_ij`), not quadratic. Ring-out (OVER) emerges from positions. Stagger 0.3 s: control authority × (1 − 0.5·min(1, N_ij)).

### 4.4 Spin loss and stamina consumption
- Collision: `Δω_j = c_s · N_ij · (1 − STA_j/250)` RPS, `c_s = 3.733 RPS` (v0.4; v0.3.1: 1.6).
- Continuous decay: `dω/dt = −c_d · (1.25 − STA/100) · friction · (1 + c_move · mobility · |u|)` RPS/s, `c_d = 1.983 RPS/s` (v0.4; v0.3.1: 0.85), `c_move = 1.0`; `|u|` = joystick magnitude (0–1).

### 4.5 Burst damage
**Canonical equation: DOC-BURST-001 §2.2** (single source; not repeated here to avoid drift).

### 4.6 Worked examples (v0.4 coefficients; v_ref = 1.0 m/s; ω_j above ω_wob so Stab = 1; S = 0)
| Case | v_n | v_norm | I_ij | R_j | **N_ij** | Δω_j (RPS) | Δv_j (m/s) | B | T_j | D (lock pts, ±10%) |
|---|---|---|---|---|---|---|---|---|---|---|
| **Parity**: Balance vs Balance (ATK = DEF = 57, mass 1.08, ROUND/ROUND), ω_j = 300 | 1.0 m/s | 1.000 | 0.9452 | 1.1120 | **0.8500** | 2.450 | 0.255 | 0.7225 | 0.6243 | 0.295 |
| Attack (85, mass 1.0, SMASH) → Stamina (DEF 50, mass 0.95, ROUND), ω_j = 280 | 1.5 m/s | 1.500 | 2.2275 | 0.9747 | **2.2854** | 5.528 | 0.703 | 2.1711 | 0.5200 | 4.953 |
| Attack → Defense (DEF 85, mass 1.15, ABSORB), ω_j = 280 | 1.5 m/s | 1.500 | 1.7213 | 1.6649 | **1.0339** | 3.088 | 0.289 | 0.8788 | 0.5980 | 0.842 |
| Extreme glitch: Attack → Stamina, ω_j = 280 | 10 m/s | **3.000** (clamped) | 4.4550 | 0.9747 | 4.5707 | 11.057 | 1.406 | 4.3422 | 0.5200 | 11.467 |
At parity `N_ij = Pk` exactly when ATK = DEF, masses are equal, S = 0 and `v_norm = 1`.

### 4.7 Skill effectiveness vs opponent (Magic vs defensive capabilities)
`Eff = base · Pot(MAG_i) · (1 − ρ · Res_j)`, `Pot = 0.8 + 0.4·MAG_i/100`, `Res_j = 0.5·DEF_j/100 + 0.5·MAG_j/100`, `ρ = 0.3` (dimensionless). Applies to opponent-directed skill effects only; skill → modifier mapping in DOC-SKILL-001 §5.1. (Restored in v0.3.1 — accidentally omitted from the first v0.3.1 draft.)

### 4.8 Optional type modifier
`M_type(i, j)` ∈ [0.95, 1.05] multiplies `I_ij`; default 1.0 (disabled).

### 4.9 Coefficient sets (structure decided D-12/D-18; values = S-1 experimental starting values, not balanced)
| Coefficient | v0.2 reference | v0.3.1 (superseded) | **v0.4 candidate** |
|---|---|---|---|
| T0 / β / c_b | 0.95 / 0.35 / 6 | 0.20 / 2.0 / 3 | **0.20 / 2.0 / 3** |
| D_cap (per tick, per victim) / critical gate | — / L ≤ 50 (after damage) | 49 / L_start ≤ 50 | **49 / L_start ≤ 50** (D-14) |
| c_d (RPS/s) / c_move | 0.55 / 0.5 | 0.85 / 1.0 | **1.983 / 1.0** |
| ρ_rec / k_kb | — / — | 0.15 / 0.6 | **0.15 / 0.6** |
| v_ref / v_norm max / v_min | — | 1.0 m/s / 3 / 0.05·v_ref | **same** |
| c_s (RPS) / ω_wob (RPS) / ω_ref in T (RPS) / stop (RPS) | 1.6 / 25 / 150 / 8 | 1.6 / 25 / 150 / 8 | **3.733 / 58.33 / 350 / 8** |
| α, w_max, w_min, σ, k_E, k_R, crit factor | 0.5, 0.60, 0.15, 0.25, 3.0, 2.5, 2.5 | same | same |
| Launch | — | saturating 20→150 | **linear 10/press, 0 → 20, cap 35 (D-01/03/04)** |
**Scale note (v0.4):** c_s, c_d and ω_wob were multiplied by κ = 350/150 and ω_ref set to 350 so that spin dynamics keep their shape on the new launch scale. This re-tunes *experimental coefficients*; it does **not** convert displayed RPS. The stop threshold stays at 8 RPS so a 1-press launch (10 RPS) is not an immediate Spin Finish.
Machine-readable: `tools/analysis/configs/*.json`.

## 5. Opponent interaction matrix (measured, seat-averaged, `results/e2_type_pairs_v0.4.csv`)
| Interaction | Mechanism | Measured (v0.4 candidate) | What can overturn it |
|---|---|---|---|
| Defense vs Attack | ABSORB (Pk 0.85, Abs 1.15) + recoil; attacker pays movement spin cost | Defense wins **79.5%**; finishes SPIN 56.2%, OVER 28.9%, BURST 14.6% | Attack Energy ratio ≳ 1.15, launch lead, UPPER vs higher defender |
| Attack vs Stamina | High N vs low DEF → lock damage | Attack wins **86.3%**; BURST 66.6%; median 13.9 s | Stamina launch lead, steering evasion, Energy gap |
| Stamina vs Defense | Lower decay vs low output | Stamina wins **80.8%**; SPIN 74.0%, time-limit 15.8%; median 106.7 s | Launch lead for Defense |
| Attack vs Balance | Concentrated ATK beats even spread | Attack wins **60.1%** | Balance lock/mass, Adapt skill |
| Defense vs Balance | Spin race | Defense wins **61.3%** | Launch |
| Stamina vs Balance | Mixed | Stamina 51.9% / Balance 47.7% | — |
| Magic vs defensive capabilities | Pot(MAG) vs Res(DEF, MAG) | **not measurable** (no skills in the model) | skill tuning in S-1 |
Favoured matchups 79.5–86.3%: Defense > Attack is now inside the proposed 55–80% band; Attack > Stamina and Stamina > Defense still exceed it (AC-2 fails) — open item for S-1.

## 6. Outcome
Eliminations are determined by the Match Server — BURST (primary) and the secondary finishes of DOC-BURST-001 §3 — and the last Bey remaining wins (FFA).
