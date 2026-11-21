# Combat Interaction Specification (opponent-relative model)

| Document ID | DOC-CMB-001 | Version | 0.3 | Status | Principles [C]; all equations and coefficients **[P] proposals** — starting values for spike S-1 |
|---|---|---|---|---|---|---|---|

## 1. Principles
- [C] A Bey's performance depends on **its opponent's characteristics**, not only its own stats.
- [C] Similar Energy → RPS differences strongly matter. Large Energy gap → RPS matters progressively less, **never completely irrelevant**; smooth transitions.
- [C] No simplistic rules ("Attack always beats Defense").
- [P] Everything is evaluated **per contact, per pair** on the Match Server at the fixed tick (60 Hz). In a 5-competitor FFA each contact is a pair interaction.
- [P] The physics engine provides contact detection, contact normal, relative normal speed `v_n` and contact height difference; this spec converts them into game effects.
- Nothing in this document is an official Beyblade formula (official sources give none — DOC-RES-001 §3).

## 2. Symbols and definitions
`A_i` attributes (ATK, DEF, STA, MAG), `E_i` Energy, `m_i` mass, `mob_i` mobility, `lock_i` lock strength, `h_i` height, `prof_i` contact profile, `ω_i` **current** spin (RPS), `L_i` Lock Integrity, `G_i` skill gauge.

**Normative definitions** (identical in all documents):
```
rel(a, b) = (a − b) / ((a + b) / 2)                symmetric relative difference, range (−2, +2), rel(b,a) = −rel(a,b)
g = rel(E_i, E_j)                                  Energy gap;   E_i/E_j = (2 + g)/(2 − g)
r = rel(ω_i, ω_j)                                  current-spin gap (equals the launch gap at battle start)
```
Examples: Energy 66 vs 60 → ratio 1.10, g = +0.0952. Energy 78 vs 60 → ratio 1.30, g = +0.2609. Spin 120 vs 80 → r = +0.40.

## 3. Advantage function S (RPS–Energy model) [C principle / P formula — ADR-013]
```
w(g)  = w_min + (w_max − w_min) · exp(−(g/σ)²)        share of the advantage that comes from RPS
S_ij  = (1 − w) · tanh(k_E · g) + w · tanh(k_R · r)     ∈ (−1, +1),   S_ji = −S_ij
```
Proposed values: `w_max = 0.60, w_min = 0.15, σ = 0.25, k_E = 3.0, k_R = 2.5`.

| g | 0 | 0.05 | 0.10 | 0.15 | 0.20 | 0.25 | 0.30 | 0.40 | 0.60 | ≥ 1.0 |
|---|---|---|---|---|---|---|---|---|---|---|
| w(g) | 0.6000 | 0.5824 | 0.5335 | 0.4640 | 0.3873 | 0.3155 | 0.2566 | 0.1848 | 0.1514 | 0.1500 (limit) |

### 3.1 Where RPS acts (corrected in v0.3)
| Channel | Attenuated by Energy gap? | Note |
|---|---|---|
| Advantage S in impact (§4.1) | **Yes** — weight w(g) | single *impact* channel (√ω scaling removed in v0.2) |
| Spin reservoir → Spin Finish | No | physical: a weaker launch spins out earlier |
| Stability `Stab(ω)` below 25 RPS | No | physical wobble |
| Burst threshold `T(ω)` (β) | No | burst-stopper analogue |
v0.2 stated RPS enters "only through S"; that was true for impact only. The outcome-level effect of all channels together is **measured** in DOC-BAL-001 §6.

### 3.2 Numerical scenarios (exact)
See DOC-BAL-001 §4 for S1–S9 with g, r, w and both terms to four decimals. Summary: equal Energy, RPS 120 vs 80 → S = +0.4570; ratio 1.10 with RPS 80 vs 120 → −0.2825 (RPS wins the contact); ratio 1.30 with RPS 80 vs 120 → +0.2274 (Energy wins); ratio 0.818 with RPS 140 vs 60 → +0.0443 (near even); ratio 1.60 with RPS 50 vs 150 → +0.5739.

### 3.3 Outcome-level behaviour (measured, DOC-BAL-001 §6)
Effect of a ±30 RPS launch swing on win probability (Attack mirror): 62.0 points at g = 0 → 51.2 at g = 0.095 → 19.7 at g = 0.174 → 7.5 at g = 0.223. Balance mirror: 95.9 → 88.7 → 30.3 → **1.8 at g = 0.261**.
**Proposed requirement wording (OQ-CB-08):** per contact, w ≥ 0.15 always; per outcome, for g ≤ 0.20 a 30-RPS launch advantage changes win probability by ≥ 10 points. For larger gaps the stronger build is expected to dominate.

## 4. Per-contact effects (pair i → j) [P]
### 4.1 Impact power and resistance
```
I_ij = v_n · (0.4 + 0.6·mob_i) · (0.5 + ATK_i/100) · √m_i · Pk(prof_i, prof_j) · (1 + α·S_ij) · K_skill_i        α = 0.5
R_j  = (0.5 + DEF_j/100) · √m_j · Stab(ω_j) · Abs(prof_j) · K_skill_j
Stab(ω) = min(1, 0.45 + 0.55·ω/25)
N_ij = I_ij / R_j                         normalised impact (≈ 1 at parity)
```
(v0.3: the mobility speed factor `(0.4 + 0.6·mob_i)` used in the analysis model is now written into the spec.)

### 4.2 Profile matrix (knockback factor Pk / burst factor Pb), proposed values
| attacker ↓ / defender → | SMASH | UPPER | ABSORB | ROUND |
|---|---|---|---|---|
| SMASH | 1.0 / 1.0 | 1.0 / 1.0 | 0.85 / 0.85 | 1.1 / 0.95 |
| UPPER | 0.85 / 1.2 | 0.9 / 1.1 | 0.8 / 1.0 | 0.9 / 1.25 |
| ABSORB | 0.8 / 0.8 | 0.8 / 0.8 | 0.7 / 0.7 | 0.8 / 0.8 |
| ROUND | 0.9 / 0.9 | 0.9 / 0.9 | 0.8 / 0.8 | 0.85 / 0.85 |
The UPPER row applies only if `h_i ≤ h_j` (hitting from below); otherwise use the SMASH row. `Abs(ABSORB) = 1.15`, others 1.0.

### 4.3 Knockback, recoil and movement stability
- Impulse on j along the contact normal: `J_j = c_kb · N_ij · v_n · m_i/(m_i + m_j)`. Ring-out (OVER) emerges physically from position.
- **Recoil on the attacker (new in v0.3):** `J_i,recoil = c_kb · ρ_rec · N_ij · mob_i · v_n`, with `ρ_rec = 0.15`, ×2.5 when the defender is ABSORB. Implements "ABSORB rebounds attackers" and gives attackers a self-ring-out risk.
- Stagger 0.3 s: control authority × (1 − 0.5·min(1, N_ij)).

### 4.4 Rotation speed loss and stamina consumption
- Collision: `Δω_j = c_s · N_ij · (1 − STA_j/250)`, `c_s = 1.6`.
- Continuous decay per second: `c_d · (1.25 − STA/100) · friction · (1 + c_move · mobility · |u|)` — v0.3 candidate `c_d = 0.85`, `c_move = 1.0` (v0.2: 0.55, 0.5).

### 4.5 Burst damage → DOC-BURST-001 §3
`D = c_b · max(0, N_ij · Pb · A(θ) − T_j) · (1 + ε)`, `T_j = T0 · lock_j · (1 + β · ω_j/150)` — v0.3 candidate `T0 = 0.20, β = 2.0, c_b = 3`.

### 4.6 Skill effectiveness vs opponent
`Eff = base · Pot(MAG_i) · (1 − ρ·Res_j)`, `Pot = 0.8 + 0.4·MAG/100`, `Res_j = 0.5·DEF_j/100 + 0.5·MAG_j/100`, `ρ = 0.3`.

### 4.7 Optional type modifier
`M_type(i, j)` ∈ [0.95, 1.05] multiplies `I_ij`; config table, default 1.0 (disabled).

### 4.8 Coefficient sets (both proposals; neither approved)
| Coefficient | v0.2 set | v0.3 candidate |
|---|---|---|
| T0 / β / c_b | 0.95 / 0.35 / 6 | **0.20 / 2.0 / 3** |
| c_d / c_move | 0.55 / 0.5 | **0.85 / 1.0** |
| ρ_rec | — | **0.15** |
| c_s, α, w_max, w_min, σ, k_E, k_R, crit | 1.6, 0.5, 0.60, 0.15, 0.25, 3.0, 2.5, 2.5 | unchanged |
Measured consequences of each set: DOC-BAL-001 §5. The v0.3 candidate is better on every metric but still fails some bands (§5.3 there).

## 5. Opponent interaction matrix
Mechanisms, with the **measured** v0.3-candidate win probability of the favoured side (N = 4,000):

| Interaction | Main mechanism | Measured (v0.3 candidate) | What can overturn it |
|---|---|---|---|
| Defense vs Attack | ABSORB lowers impact (Pk 0.85, Abs 1.15) and adds recoil; attacker pays movement spin cost | Defense wins **82.8%**; Attack finishes: SPIN 61%, OVER 27%, BURST 12% | Attack Energy ratio ≳ 1.15, large launch lead, UPPER vs higher defender |
| Attack vs Stamina | High N vs low DEF → lock damage | Attack wins **90.2%**, BURST 72%, median 12.2 s | Stamina launch lead, steering evasion, Energy gap |
| Stamina vs Defense | Lower decay (STA 88, friction 0.9) vs Defense's low output | Stamina wins **90.0%**, SPIN 95%, median 94 s | Launch lead for Defense (decisive in spin races) |
| Attack vs Balance | Concentrated ATK beats even spread (threshold-gated damage) | Attack wins **64.4%** | Balance lock/mass, Adapt skill |
| Defense vs Balance | Spin race | Defense wins **63.2%** | Launch |
| Stamina vs Balance | Mixed | Stamina 50.6% / Balance 48.6% | — |
| Magic vs defensive capabilities | Pot(MAG) vs Res(DEF, MAG) | not measurable in this model | skill tuning (spike) |
| RPS differences | S + spin reservoir | DOC-BAL-001 §6 | Energy gap > ~0.2 |
Favoured matchups at 83–90% exceed the proposed "tendency" band of 55–80% (FR-215) — open balancing item C7.

## 6. Outcome
The match outcome is the sequence of eliminations determined by the Match Server — BURST (primary) and the secondary finishes defined in DOC-BURST-001 §4 — and the last Bey remaining wins (FFA).
